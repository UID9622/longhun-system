#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-03-lh-model-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2（工程层·代码可商用·署名·专利授权）
# 引擎: 龍魂模型命令 v1.1（lh model）· 2026-09-03 · 深度学习代码精修统一入口
# 精修(2026-09-03): ①统一推理 generate()(deepseek_api 委派 + ollama 原生 http.client 降级链)
#   ②list 合并输出(图谱注册 ∪ 本地 ollama 实时·去重) ③audit 底层接 lh_judge 指纹比对
#   ④bench/eval/test 子命令委派既有引擎脚本(散落工具入口归一) ⑤api 双端状态
# 命令集: list / status <name> / audit <name> [--probe] / run <prompt> / api / bench / eval / test
# 数据源: docs/topology/深度学习图谱_legion_topo.json（与 lh_topo.py 共享·lh topo register/node 维护）
# 铁律: 加载/调用/查询模型状态 = lh model 唯一入口 · 模型训练数据 = lh topo sync 深度学习图谱
#      模型输出审计 = lh model audit(接 lh_judge) · 零三方依赖（stdlib；deepseek 委派按需降级）

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "docs" / "topology" / "深度学习图谱_legion_topo.json"
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
DEFAULT_MODEL = "longhun-v4.1.9"
委派表 = {"bench": "lh_model_bench_ollama.py",
          "eval": "lh_model_eval.py",
          "test": "lh_model_test.py"}


def _load_graph() -> dict:
    if not GRAPH.is_file():
        print(f"  ❌ 未找到图谱缓存 {GRAPH.relative_to(ROOT)}（先跑: lh topo register 深度学习图谱）",
              file=sys.stderr)
        sys.exit(1)
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def _assets(data: dict):
    for g in data.get("groups", []):
        for a in g.get("assets", []):
            yield g.get("name", ""), a


def _ollama_cmd(api: str, payload: dict, timeout: int = 180) -> dict:
    """原生 http.client 调 ollama（零三方依赖·数据不出机）"""
    import http.client
    body = json.dumps(payload).encode("utf-8")
    conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=timeout)
    try:
        conn.request("POST", api, body, {"Content-Type": "application/json"})
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8", "replace")
        conn.close()
        if resp.status != 200:
            raise RuntimeError(f"ollama HTTP {resp.status}: {raw[:300]}")
        return json.loads(raw)
    finally:
        try:
            conn.close()
        except Exception:
            pass


def _ollama_list() -> str:
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=8)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


def _ollama_ps() -> list:
    try:
        r = subprocess.run(["ollama", "ps"], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            return []
        return [ln.split()[0] for ln in r.stdout.splitlines()[1:] if ln.strip()]
    except Exception:
        return []


def _default_model() -> str:
    """图谱模型层首个 model 节点名 → 缺省 ollama 主力模型"""
    try:
        for _g, a in _assets(_load_graph()):
            if a.get("type") == "model":
                return a.get("name", "").split("（")[0].strip() or DEFAULT_MODEL
    except Exception:
        pass
    return DEFAULT_MODEL


def generate(messages: list, engine: str = "auto", model: str = "",
             temperature: float = 0.7, max_tokens: int = 2048, timeout: int = 180) -> str:
    """统一模型推理入口 v1.1 — engine: auto(DeepSeek→Ollama 降级链) | deepseek | ollama
    归一: lh_dh_dispatch / deepseek_api 调用方统一改走本函数 · 返回纯文本内容"""
    errs = []
    if engine in ("deepseek", "auto"):
        try:
            sys.path.insert(0, str(ROOT / "08_BIN"))
            from deepseek_api import DeepSeekClient
            resp = DeepSeekClient(timeout=timeout).chat(
                messages, temperature=temperature, max_tokens=max_tokens)
            return resp["choices"][0]["message"]["content"]
        except Exception as e:   # noqa: BLE001 deepseek 不可达 → 记错降级
            errs.append(f"deepseek: {e}")
    if engine in ("ollama", "auto"):
        m = model or _default_model()
        try:
            out = _ollama_cmd("/api/chat", {"model": m, "messages": messages,
                                            "stream": False, "options": {
                                                "temperature": temperature,
                                                "num_predict": max_tokens}}, timeout=timeout)
            return out.get("message", {}).get("content", "") or ""
        except Exception as e:   # noqa: BLE001
            errs.append(f"ollama({m}): {e}")
    raise RuntimeError(" | ".join(errs) or "engine 参数非法")


# ─────────────────────────── 子命令：list（合并去重 v1.1） ───────────────────────────

def cmd_list(json_out: bool = False):
    data = _load_graph()
    rows = []
    for group, a in _assets(data):
        if a.get("type") not in ("model", "engine"):
            continue
        rows.append({"name": a.get("name", "?"), "type": a.get("type", ""),
                     "status": a.get("status", ""), "path": a.get("path", ""),
                     "dna": a.get("dna", ""), "group": group})
    registered_stems = {r["name"].split("（")[0].strip() for r in rows}
    # 本地 ollama 实时（NAME:latest 去 tag 对比·与注册节点合并不重复）
    out = _ollama_list()
    local = [ln.split()[0] for ln in out.splitlines()[1:] if ln.strip()] if out else []
    loaded = set(_ollama_ps())
    merged = []
    seen = set()
    for r in rows:
        key = r["name"]
        if key in seen:
            continue
        seen.add(key)
        live = None
        for m in local:
            if m.split(":")[0] == r["name"].split("（")[0].strip() or r["name"] in m:
                live = m
                break
        merged.append({"name": key, "type": r["type"], "status": r["status"],
                       "path": r.get("path", ""), "dna": r.get("dna", ""),
                       "live": live, "loaded": live in loaded})
    # 仅本地检出（未注册图谱）
    reg_in_local = {m.split(":")[0] for m in local}
    local_only = [m for m in local if m.split(":")[0] not in {x["name"].split("（")[0].strip() for x in rows}]
    if json_out:
        print(json.dumps({"owner": OWNER, "registered": rows, "merged": merged,
                          "local_ollama": local, "local_only": local_only},
                         ensure_ascii=False, indent=2))
        return
    print("\n  🧠 龍魂模型注册表 · 深度学习图谱 × Ollama 实时（v1.1 合并去重）")
    print("  " + "=" * 56)
    if not merged:
        print("  ⚪ 图谱内暂无 model/engine 节点（用 lh topo node 注册）")
    for r in merged:
        tag = r["live"] or "本地未检出"
        print(f"  {r['name']}  [{r['type']}] {r['status']}  · 路径 {r['path'] or '—'}")
        print(f"      📦 ollama: {tag}{' · 已加载内存' if r.get('loaded') else ''}"
              if r["live"] else f"      ⚠️ 图谱已注册但本地 ollama 未见「{r['name']}」")
        if r.get("dna"):
            print(f"      DNA {r['dna']}")
    if local_only:
        print(f"\n  ⚪ 本地 ollama 检出·未注册图谱 {len(local_only)}:")
        for m in local_only:
            print(f"      · {m}{'  · 已加载内存' if m in loaded else ''}")
    if not out and not merged:
        print("  （ollama 未启动/未安装 · 仅图谱注册视图）")
    print()


# ─────────────────────────── 子命令：status ───────────────────────────

def cmd_status(name: str, json_out: bool = False):
    if not name:
        raise SystemExit("  ❌ 用法: lh model status <name>")
    data = _load_graph()
    row = next((a for _, a in _assets(data) if name in a.get("name", "")), None)
    info = {"name": name, "dna": "", "registered": row is not None}
    if row is None:
        local = _ollama_list()
        print(f"  ⚠️ 图谱未注册「{name}」· 本地 ollama: {local.replace(chr(10), ' | ') or '不可达'}")
        sys.exit(1)
    info.update({"name": row.get("name"), "type": row.get("type"),
                 "status": row.get("status"), "dna": row.get("dna"),
                 "path": row.get("path"), "desc": row.get("desc")})
    stem = row.get("name", "").split("（")[0].strip()
    loaded = _ollama_ps()
    info["ollama_loaded"] = [m for m in loaded if stem in m or m in row.get("name", "")]
    live = any(stem in m for m in _ollama_list().splitlines())
    info["ollama_live"] = live
    p = (row.get("path") or "").strip()
    if p:
        info["path_exists"] = ((ROOT / p).exists() if not p.startswith("~")
                               else Path(p).expanduser().exists())
    if json_out:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return
    print(f"\n  🧠 模型状态 · {info['name']}")
    print(f"     类型 {info['type']} · 图谱状态 {info['status']}"
          f" · ollama {'在线·' + ('已加载' if info.get('ollama_loaded') else '空闲') if info.get('ollama_live') else '离线'}")
    for k in ("dna", "path", "desc"):
        if info.get(k):
            print(f"     {k} {info[k]}")
    if info.get("path_exists") is not None:
        print(f"     路径存在 {info['path_exists']}")
    print()


# ─────────────────────────── 子命令：audit（接 lh_judge 指纹比对 v1.1） ───────────────────────────

def _judge_fingerprint(text: str):
    """底层调用 lh_judge 的指纹比对（资产名集 + DNA 前缀本地判定·精修标准③）
    返回命中清单；judge 不可用时返回 None（audit 降级 🟡 注明）"""
    try:
        sys.path.insert(0, str(ROOT / "08_BIN"))
        import lh_judge
        资产 = lh_judge.加载通心译资产() or []
        集 = {a["name"] for a in 资产} | {"通心译", "龍芯北辰", "UID9622", "CNSH", "龙魂", "龍魂"}
        m = re.search(r"#龍芯⚡️[^\s，。、；：！？“”‘’（）()【】\[\]\n]+", text[:20000])
        if m:
            return ["DNA指纹:" + m.group(0)]
        return [n for n in 集 if n and n in text[:20000]][:5]
    except Exception:   # noqa: BLE001 lh_judge 依赖缺失 → 降级
        return None


def cmd_audit(name: str, json_out: bool = False, probe: str = ""):
    if not name:
        raise SystemExit("  ❌ 用法: lh model audit <name> [--probe 输出样例|@文件]")
    data = _load_graph()
    row = next((a for _, a in _assets(data) if name in a.get("name", "")), None)
    registered = row is not None
    dna = row.get("dna", "") if row else ""
    reasons = []
    if not registered:
        reasons.append("未注册到深度学习图谱（DNA 缺位）")
    if dna and not dna.startswith("#龍芯⚡️") and "继承" not in dna:
        reasons.append(f"DNA 非 #龍芯⚡️ 格式({dna[:24]})")
    if registered and not dna:
        reasons.append("注册节点缺 DNA 字段")
    # ① 注册/主权/DNA 检查（自有链） + ② lh_judge 指纹比对（模型输出/文档泄露检测）
    judge_hits = []
    judge_ok = True
    probe_text = ""
    if probe:
        pv = probe[1:] if probe.startswith("@") else probe
        if probe.startswith("@"):
            pf = Path(pv).expanduser()
            probe_text = pf.read_text(encoding="utf-8", errors="replace") if pf.is_file() else ""
            if not probe_text:
                reasons.append(f"probe 文件不可读({pv})")
        else:
            probe_text = pv
    if probe_text:
        judge_hits = _judge_fingerprint(probe_text) or []
        if judge_hits:
            judge_ok = False
            reasons.append("judge 指纹命中: 输出样例含通心译材料 " + "、".join(judge_hits[:3]))
        elif _judge_fingerprint(probe_text) is None:
            judge_ok = False
            reasons.append("lh_judge 指纹比对不可用（降级·待复核）")
    mark = "🟢" if registered and not reasons else ("🟡" if registered else "🔴")
    report = {
        "owner": OWNER, "model": name, "registered": registered, "dna": dna,
        "audit_mark": mark,
        "checks": {
            "registered_in_graph": "✅" if registered else "❌",
            "dna_valid": "✅" if (not dna or dna.startswith("#龍芯⚡️") or "继承" in dna) else "❌",
            "sovereignty": "✅ 归属名·诸葛鑫 | UID9622",
            "traceable": "✅ 图谱内可 lh topo cite 追溯" if registered else "❌",
            "judge_fingerprint": ("✅ 无通心译指纹泄露" if judge_ok and probe_text else
                                  ("🟡 未提供 --probe 输出样例" if not probe_text else "❌ 命中/降级")),
        },
        "issues": reasons,
        "conclusion": ("合规：注册+DNA+归属+judge 指纹全绿" if mark == "🟢"
                       else ("待注册/待补 probe：仅缺位可补" if mark == "🟡"
                             else "不合规：未注册或指纹命中，禁止对外使用")),
        "audited_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    if json_out:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n  🧠 模型合规审计（judge 指纹链） · {name}  {mark}")
        for k, v in report["checks"].items():
            print(f"     {v} {k}")
        for r in reasons:
            print(f"     ⚠️ {r}")
        print(f"     结论: {report['conclusion']}")
        print(f"     时间 {report['audited_at']}")
        print()
    sys.exit(0 if mark == "🟢" else 2)


# ─────────────────────────── 子命令：run / api / 委派 ───────────────────────────

def cmd_run(prompt: str, engine: str = "auto", model: str = "", system: str = "",
            json_out: bool = False):
    if not prompt.strip():
        raise SystemExit("  ❌ 用法: lh model run <prompt> [--engine auto|deepseek|ollama] [--model <name>]")
    sys_msg = system or "你是龍魂数字人（归属名: 诸葛鑫 | UID9622 · 龍芯北辰）。回答直接、真实、不虚伪。"
    try:
        content = generate([{"role": "system", "content": sys_msg},
                            {"role": "user", "content": prompt}],
                           engine=engine, model=model)
        if json_out:
            print(json.dumps({"engine": engine, "model": model or _default_model(),
                              "content": content}, ensure_ascii=False, indent=2))
        else:
            print(f"\n  🧠 lh model run（engine={engine}·model={model or _default_model()}）")
            print("  " + "-" * 50)
            print(content)
            print()
    except RuntimeError as e:
        print(f"  ❌ {e}", file=sys.stderr)
        sys.exit(1)


def cmd_api(json_out: bool = False):
    """双端状态: DeepSeek(委派 deepseek_api·本地 vLLM :8000/官方 key) + Ollama :11434"""
    state = {"owner": OWNER, "ollama": "offline", "deepseek": "未配置/不可达"}
    try:
        out = _ollama_cmd("/api/version", {}, timeout=5)
        state["ollama"] = out.get("version", "up")
    except Exception:
        pass
    try:
        sys.path.insert(0, str(ROOT / "08_BIN"))
        from deepseek_api import DeepSeekClient
        c = DeepSeekClient(timeout=3)
        state["deepseek"] = "local(vLLM :8000)" if c.is_local else "官方API(有 key)"
    except Exception:
        pass
    if json_out:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return
    print(f"\n  🧠 模型 API 状态 · {state['ollama'] if state['ollama'] != 'offline' else '❌ ollama offline'}")
    print(f"     ollama    :11434  {state['ollama']}")
    print(f"     deepseek  {state['deepseek']}（调用走 lh model generate·auto 降级链）")
    print(f"     deepseek_api.py 已归一: 直接 python3 deepseek_api.py 运行示例已移除，走 lh model run/api")
    print()


def cmd_bench_eval_test(action: str):
    """委派既有散落引擎脚本（bench/eval/test）→ 透传完整原始 argv · 入口归一 lh model"""
    script = ROOT / "08_BIN" / 委派表[action]
    if not script.is_file():
        print(f"  ❌ 委派脚本缺失 {script.relative_to(ROOT)}", file=sys.stderr)
        sys.exit(1)
    argv = [sys.executable, str(script)] + sys.argv[2:]   # 透传 action 之后的全部参数
    print(f"  🧠 lh model {action} → 委派 {script.relative_to(ROOT)}")
    sys.exit(subprocess.call(argv))


def main():
    ap = argparse.ArgumentParser(description="龍魂模型命令 v1.1 (lh model)")
    ap.add_argument("action", nargs="?", default="list",
                    choices=["list", "status", "audit", "run", "api", "bench", "eval", "test"])
    ap.add_argument("name", nargs="?", default="", help="模型名(status/audit)/提示词(run)")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--engine", default="auto", choices=["auto", "deepseek", "ollama"],
                    help="run 推理引擎 (默认 auto: deepseek→ollama 降级)")
    ap.add_argument("--model", default="", help="run 指定 ollama 模型")
    ap.add_argument("--system", default="", help="run 系统提示")
    ap.add_argument("--probe", default="", help="audit 输出样例指纹比对 (文本 或 @文件)")
    args, _unknown = ap.parse_known_args()
    if args.action in ("bench", "eval", "test"):
        cmd_bench_eval_test(args.action)
    elif args.action == "status":
        cmd_status(args.name, json_out=args.json)
    elif args.action == "audit":
        cmd_audit(args.name, json_out=args.json, probe=args.probe)
    elif args.action == "run":
        cmd_run(args.name, engine=args.engine, model=args.model, system=args.system,
                json_out=args.json)
    elif args.action == "api":
        cmd_api(json_out=args.json)
    else:
        cmd_list(json_out=args.json)


if __name__ == "__main__":
    main()
