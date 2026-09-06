#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-05-EXECUTOR-LOCAL-EXECUTION-LAYER-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·本地模型执行层 v1.0（调度器=CodeBuddy · 执行器=本地模型）
# 设计铁律(2026-09-05·老大焊死):
#   - CodeBuddy 是调度层: 理解意图·生成执行计划
#   - 本地模型(Ollama/llama.cpp/vLLM)是执行层: 深度分析/大批量推理/样本生成/离线任务
#   - 说真话不伪造: 文本 LLM 不做真实文件/网络写入 → 确定性操作由调度层直跑,
#     execute 只接"推理/分析/生成"类任务(这正是本地模型的增量价值)
#   - 全操作审计: 每单落盘 ~/.longhun/execution_logs/*.jsonl · 三色自动判定
# 用法:
#   lh execute "<任务>" [--model <名>] [--system "<提示>"] [--num-predict N]
#   lh executor list                 # 列出已注册本地模型(registry + ollama 实况)
#   lh executor status               # 本地模型服务状态(ping/运行中/注册表)
#   lh executor register --name X --type ollama|llamacpp|vllm --url http://...[:port]
#   lh executor log [--tail N]       # 查看最近执行记录
import json
import os
import sys
import time
import urllib.request

EXEC_ROOT = os.path.expanduser("~/.longhun")
REGISTRY = os.path.join(EXEC_ROOT, "local_executor.json")
LOG_DIR = os.path.join(EXEC_ROOT, "execution_logs")
DEFAULT_BACKEND = "ollama"
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODELS = ["longhun-v4.2.0:latest", "deepseek-r1:7b", "qwen2.5:7b"]

SYS_PROMPT = (
    "你是龍魂系统的本地执行层助手(调度器=CodeBuddy)。对任务给出简洁、可操作的结论。"
    "不知道就说不知道，不编造执行结果。回答中文为主。"
)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _ensure_root():
    os.makedirs(EXEC_ROOT, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


# ---------- ollama API ----------
def ollama_ping() -> dict:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/version", timeout=3) as r:
            return {"ok": True, "data": json.loads(r.read().decode())}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def ollama_tags() -> list:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5) as r:
            return [m["name"] for m in json.loads(r.read().decode()).get("models", [])]
    except Exception:
        return []


def ollama_ps() -> list:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/ps", timeout=3) as r:
            return [m.get("name", "?") for m in json.loads(r.read().decode()).get("models", [])]
    except Exception:
        return []


# ---------- registry ----------
def load_registry() -> dict:
    if os.path.exists(REGISTRY):
        try:
            with open(REGISTRY, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": 1,
        "updated_at": _now(),
        "default_model": "longhun-v4.2.0:latest",
        "default_backend": DEFAULT_BACKEND,
        "backends": [
            {"name": "ollama", "type": "ollama", "url": OLLAMA_URL,
             "note": "本地默认后端(Ollama)", "models": []},
        ],
    }


def save_registry(reg: dict):
    _ensure_root()
    reg["updated_at"] = _now()
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


def sync_ollama(reg: dict) -> dict:
    """ollama 后端实况模型同步进 registry"""
    tags = ollama_tags()
    for b in reg.get("backends", []):
        if b.get("type") == "ollama":
            b["models"] = tags
            b["online"] = bool(tags)
    return reg


def pick_model(reg: dict, requested: str = None) -> str:
    """选模型: 显式指定 > registry default(存在时) > 预置候选(存在时) > 任意可用"""
    tags = []
    for b in reg.get("backends", []):
        if b.get("type") == "ollama":
            tags += b.get("models", [])
    if requested:
        return requested if (not tags or requested in tags) else None
    for cand in ([reg.get("default_model")] + DEFAULT_MODELS):
        if cand in tags:
            return cand
    return tags[0] if tags else None


# ---------- audit log ----------
def append_log(entry: dict):
    _ensure_root()
    day = time.strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"executor-{day}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def tail_log(n: int = 5):
    _ensure_root()
    files = sorted(f for f in os.listdir(LOG_DIR) if f.startswith("executor-") and f.endswith(".jsonl"))
    if not files:
        print("  ℹ️  暂无执行记录")
        return
    lines = []
    for fn in files[-3:]:
        with open(os.path.join(LOG_DIR, fn), encoding="utf-8") as f:
            lines.extend(f.readlines())
    for line in lines[-n:]:
        try:
            e = json.loads(line)
            print(f"  [{e.get('color','?')}] {e.get('ts','?')} model={e.get('model','?')} "
                  f"task={e.get('task','')[:60]} out_len={e.get('out_len',0)} rc={e.get('rc','?')}")
        except Exception:
            continue


# ---------- commands ----------
def cmd_status() -> int:
    ping = ollama_ping()
    running = ollama_ps()
    reg = sync_ollama(load_registry())
    save_registry(reg)
    print(f"  🔌 Ollama:  {'✅ 在线' if ping.get('ok') else '🔴 离线: ' + str(ping.get('error'))} "
          f"({OLLAMA_URL})")
    if ping.get("ok"):
        print(f"  · 版本: {ping['data'].get('version', '?')}")
    print(f"  ▶️  运行中: {running if running else '(idle)'}")
    print(f"  📦 已装模型: {len(ollama_tags())} 个")
    for b in reg.get("backends", []):
        print(f"  · [{b.get('type')}] {b.get('name')} · {b.get('url')} · "
              f"{len(b.get('models', []))} 模型 · {'✅' if b.get('online') else '⬜'}")
    print(f"  🎯 默认模型: {reg.get('default_model')}")
    print(f"  📝 注册表: {REGISTRY}")
    return 0 if ping.get("ok") else 1


def cmd_list() -> int:
    reg = sync_ollama(load_registry())
    save_registry(reg)
    print("  📦 本地执行器注册模型:")
    for b in reg.get("backends", []):
        print(f"\n  [{b.get('type')}] {b.get('name')} → {b.get('url')}")
        for m in b.get("models", []):
            mark = " ⭐默认" if m == reg.get("default_model") else ""
            print(f"    · {m}{mark}")
    if not any(b.get("models") for b in reg.get("backends", [])):
        print("  ⬜ 无可用模型 → ollama pull <model> 或 lh executor register")
    return 0


def cmd_register(name: str, mtype: str, url: str) -> int:
    reg = load_registry()
    reg["backends"].append({"name": name, "type": mtype, "url": url, "note": "手动注册", "models": []})
    save_registry(reg)
    print(f"  ✅ 已注册后端 [{mtype}] {name} → {url}")
    return 0


def cmd_execute(task: str, model: str = None, system: str = None, num_predict: int = 4000) -> int:
    if not task:
        print("  🔴 任务为空 → lh execute '<任务>'")
        return 1
    reg = sync_ollama(load_registry())
    save_registry(reg)
    chosen = pick_model(reg, model)
    if not chosen:
        tags = ollama_tags()
        print(f"  🔴 指定模型不可用: {model}")
        print(f"    可用: {', '.join(tags) if tags else '(ollama 无模型)'}")
        append_log({"ts": _now(), "color": "🔴", "model": model or "?", "task": task,
                    "rc": "no-model", "out_len": 0, "out_head": "模型不可用", "dur_ms": 0})
        return 1
    prompt = system or SYS_PROMPT
    payload = {"model": chosen, "prompt": task, "system": prompt,
               "stream": False, "options": {"num_predict": int(num_predict)}}
    t0 = time.time()
    print(f"  ⚙️  本地推理: model={chosen} · task={task[:80]} ...")
    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate", data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=900) as r:
            out = json.loads(r.read().decode()).get("response", "")
    except Exception as e:
        dur = int((time.time() - t0) * 1000)
        append_log({"ts": _now(), "color": "🔴", "model": chosen, "task": task,
                    "rc": "err", "out_len": 0, "out_head": str(e)[:200], "dur_ms": dur})
        print(f"  🔴 执行失败: {e}")
        return 1
    dur = int((time.time() - t0) * 1000)
    color = "🟢" if out.strip() else "🟡"
    head = out.strip()[:800].replace("\n", " ")
    append_log({"ts": _now(), "color": color, "model": chosen, "task": task,
                "rc": 0, "out_len": len(out), "out_head": head, "dur_ms": dur})
    print(f"\n  ── 结果 ({color} · {dur}ms · {len(out)} 字符) ──")
    print(out.strip())
    print(f"\n  📝 已审计落盘: {LOG_DIR}")
    return 0


def usage():
    print("""龍魂·本地模型执行层 v1.0
  lh execute "<任务>" [--model <名>] [--system "<提示>"] [--num-predict N]
  lh executor list | status | log [--tail N]
  lh executor register --name <名> --type ollama|llamacpp|vllm --url <http...>
设计: CodeBuddy=调度层(意图/计划) · 本地模型=执行层(推理/分析/生成) · 审计全落盘
诚实边界: 文本 LLM 不做真实文件/网络写入 → 确定性操作由调度层直跑""")


def main():
    argv = sys.argv[1:]
    if not argv:
        usage()
        return 0
    cmd = argv[0]
    if cmd == "status":
        return cmd_status()
    if cmd == "list":
        return cmd_list()
    if cmd == "register":
        name = mtype = url = None
        i = 1
        while i < len(argv):
            if argv[i] == "--name" and i + 1 < len(argv):
                name = argv[i + 1]
            if argv[i] == "--type" and i + 1 < len(argv):
                mtype = argv[i + 1]
            if argv[i] == "--url" and i + 1 < len(argv):
                url = argv[i + 1]
            i += 1
        if not (name and mtype and url):
            print("  🔴 需 --name --type --url")
            return 1
        return cmd_register(name, mtype, url)
    if cmd == "log":
        n = 5
        for i, a in enumerate(argv):
            if a == "--tail" and i + 1 < len(argv):
                n = int(argv[i + 1])
        tail_log(n)
        return 0
    # 裸词兜底: lh execute 自由文本由 lh.py 透传为位置参数（首词非子命令/非flag → 视为任务）
    if cmd not in ("status", "list", "register", "log", "execute") and not cmd.startswith("-"):
        return cmd_execute(" ".join(argv))
    if cmd == "execute":
        rest = argv[1:]
        model = system = None
        num_predict = 4000
        task_parts = []
        i = 0
        while i < len(rest):
            if rest[i] == "--model" and i + 1 < len(rest):
                model = rest[i + 1]
                i += 2
            elif rest[i] == "--system" and i + 1 < len(rest):
                system = rest[i + 1]
                i += 2
            elif rest[i] == "--num-predict" and i + 1 < len(rest):
                num_predict = int(rest[i + 1])
                i += 2
            else:
                task_parts.append(rest[i])
                i += 1
        return cmd_execute(" ".join(task_parts), model, system, num_predict)
    usage()
    return 1


if __name__ == "__main__":
    sys.exit(main())
