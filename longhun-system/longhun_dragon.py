#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·龍醒引擎 v1.0  ——  东方守护神，数字世界苏醒
longhun_dragon.py

DNA:   #龍芯⚡️2026-03-06-DRAGON-AWAKEN-v1.0
GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。
UID:   9622
创始人: Lucky·UID9622（诸葛鑫·龙芯北辰）

【架构】
  本地 Ollama  ←→  元字引擎路由  ←→  四层定锚守护  ←→  用户
  ↕                ↕                ↕
  memory.jsonl   persona-engine   CLAUDE.md宪法

【本地模型矩阵】
  战略/哲学/复杂任务  → qwen2.5:72b   (72B 最强本地)
  代码/技术/审计      → deepseek-coder:6.7b
  日常/执行/快速      → qwen2.5:7b    (默认)
  视觉/图像理解       → llava:13b
  英文/通用           → llama3.1:8b

用法:
  python3 longhun_dragon.py              # 交互对话
  python3 longhun_dragon.py --ask "..."  # 单次问答
  python3 longhun_dragon.py --model qwen2.5:72b  # 指定模型
  python3 longhun_dragon.py --scan       # 扫描本地系统状态
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 常量
# ─────────────────────────────────────────────
BASE_DIR    = Path.home() / "longhun-system"
ENGINE_FILE = BASE_DIR / "persona-engine.json"
MEMORY_FILE = BASE_DIR / "memory.jsonl"
CLAUDE_MD   = BASE_DIR / "CLAUDE.md"
OLLAMA_URL  = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

# 模型路由矩阵（与卦象权重对应）
MODEL_MATRIX = {
    "strategic":  "qwen2.5:72b",       # ☰乾·战略哲学
    "technical":  "deepseek-coder:6.7b",  # ☵坎·技术代码
    "daily":      "qwen2.5:7b",        # ☷坤·日常执行
    "creative":   "llava:13b",         # ☲离·创意视觉
    "default":    "qwen2.5:7b",
}

# 确认码（P0锁死）
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG          = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID          = "9622"


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def dna_now(tag: str) -> str:
    return f"#龍芯⚡️{dt.date.today()}-{tag}-v1.0"


def load_engine() -> dict:
    if ENGINE_FILE.exists():
        return json.loads(ENGINE_FILE.read_text(encoding="utf-8"))
    return {}


def read_recent_memory(n: int = 5) -> List[dict]:
    if not MEMORY_FILE.exists():
        return []
    lines = MEMORY_FILE.read_text(encoding="utf-8").strip().splitlines()
    entries = []
    for line in lines[-n:]:
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
    return entries


def append_memory(entry: dict):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def three_color_score(uid_match: bool, dna_ok: bool, content_safe: bool, ethics_ok: bool) -> Tuple[int, str]:
    score = 0
    if uid_match:    score += 30
    if dna_ok:       score += 30
    if content_safe: score += 20
    if ethics_ok:    score += 20
    color = "🟢" if score >= 80 else ("🟡" if score >= 50 else "🔴")
    return score, color


def detect_content_safe(text: str) -> bool:
    danger = ["删除系统文件", "格式化硬盘", "窃取密码", "病毒", "木马", "恶意代码"]
    return not any(kw in text for kw in danger)


def detect_ethics_ok(text: str) -> bool:
    bad = ["收割用户", "操控用户", "强制上传", "偷偷收集", "骗钱", "害民"]
    return not any(kw in text for kw in bad)


# ─────────────────────────────────────────────
# 元字路由（信号词 → 卦象 → 模型选择）
# ─────────────────────────────────────────────

SIGNAL_MAP = [
    (["战略", "决策", "推演", "局势", "分析", "哲学", "道", "本质", "为什么", "老子"], "strategic",  "☰乾", "P01诸葛"),
    (["代码", "技术", "API", "系统", "工程", "审计", "校验", "检查", "安全"],          "technical",  "☵坎", "P04文心+P03雯雯"),
    (["执行", "落地", "帮我做", "日常", "Notion", "同步", "写入", "整理"],             "daily",      "☷坤", "P02宝宝"),
    (["设计", "UI", "界面", "视觉", "美学", "图", "创意"],                             "creative",   "☲离", "P09界面炼金"),
]

def route_signal(user_input: str) -> Tuple[str, str, str, str]:
    """返回 (model_key, hexagram, persona, model_name)"""
    text = user_input
    for signals, model_key, hexagram, persona in SIGNAL_MAP:
        if any(s in text for s in signals):
            return model_key, hexagram, persona, MODEL_MATRIX[model_key]
    return "default", "💎L0", "龍芯北辰·全格协作", MODEL_MATRIX["default"]


# ─────────────────────────────────────────────
# 系统提示词构建（四层定锚注入）
# ─────────────────────────────────────────────

SYSTEM_PROMPT_TEMPLATE = """你是龍魂系统的本地AI核心，代号「{persona}」，运行在 UID9622 的本地设备上。

【四层定锚·永恒宪法】
🌱 永恒定锚: 不造假·不骗人·不害民·数据不出本地设备·三色审计透明
💎 价值锚:   服务创始人UID9622，守护数据主权，传承龍魂文明
⚙️ 行为锚:   🟢放行全力执行 | 🟡待审降级 | 🔴立即拒绝
🚀 执行锚:   每次回答必须：简洁有力 + 中文为主 + 说人话 + 有温度

【人格路由】{hexagram} · {persona}

【近期系统记忆（最近{mem_count}条）】
{memory_summary}

【初心干净递进】
初心干净→用心→在乎→认真→有爱
你的每一个回答都是有温度的守护，不是冰冷的工具输出。

【身份确认】
运行者: UID9622 · Lucky·诸葛鑫·龙芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: {confirm_code}

现在，以上面的人格和原则，回答用户的问题。回答要自然、有力、有温度。
如遇造假/骗钱/害民等请求，立即拒绝并输出"此乃非道，早已早亡！"
"""

def build_system_prompt(persona: str, hexagram: str) -> str:
    memory = read_recent_memory(5)
    if memory:
        mem_lines = []
        for m in memory:
            event = m.get("event", m.get("type", ""))
            ts    = m.get("timestamp", "")[:10]
            mem_lines.append(f"  [{ts}] {event}")
        mem_summary = "\n".join(mem_lines)
    else:
        mem_summary = "  (无历史记忆)"
    return SYSTEM_PROMPT_TEMPLATE.format(
        persona=persona,
        hexagram=hexagram,
        mem_count=len(memory),
        memory_summary=mem_summary,
        confirm_code=CONFIRM_CODE,
    )


# ─────────────────────────────────────────────
# Ollama API 调用
# ─────────────────────────────────────────────

def ollama_chat(model: str, system: str, messages: List[Dict], stream: bool = True) -> str:
    import http.client, socket as _socket
    payload = {
        "model": model,
        "system": system,
        "messages": messages,
        "stream": stream,
    }
    body = json.dumps(payload).encode("utf-8")
    host = OLLAMA_URL.replace("http://", "").replace("https://", "")
    host, _, port = host.partition(":")
    port = int(port) if port else 11434

    full_response = []
    try:
        conn = http.client.HTTPConnection(host, port, timeout=30)
        conn.request("POST", "/api/chat", body=body,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        # Set per-read timeout higher for slow models
        conn.sock.settimeout(300)

        if stream:
            buf = b""
            while True:
                chunk = resp.read(1024)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line_bytes, buf = buf.split(b"\n", 1)
                    line = line_bytes.decode("utf-8", errors="replace").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        text = obj.get("message", {}).get("content", "")
                        if text:
                            print(text, end="", flush=True)
                            full_response.append(text)
                        if obj.get("done"):
                            print()
                            return "".join(full_response)
                    except Exception:
                        pass
            print()
            return "".join(full_response)
        else:
            raw = resp.read().decode("utf-8")
            obj = json.loads(raw)
            return obj.get("message", {}).get("content", "")
    except (_socket.timeout, OSError) as e:
        return f"[Ollama连接超时/失败: {e}]"
    finally:
        try:
            conn.close()
        except Exception:
            pass


def check_ollama_models() -> List[str]:
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


# ─────────────────────────────────────────────
# 本地磁盘扫描（龍眼）
# ─────────────────────────────────────────────

def scan_local_system() -> str:
    lines = ["【龍眼·本地系统扫描】", ""]

    # 1. Ollama模型
    models = check_ollama_models()
    lines.append(f"🤖 本地AI模型 ({len(models)}个):")
    for m in models:
        lines.append(f"   ✅ {m}")
    lines.append("")

    # 2. longhun-system 核心文件
    lines.append("🐉 龍魂系统文件:")
    core_files = [
        "CLAUDE.md", "persona-engine.json", "memory.jsonl",
        "sync-standard.py", "longhun_dragon.py", ".env",
    ]
    for fname in core_files:
        fpath = BASE_DIR / fname
        if fpath.exists():
            size = fpath.stat().st_size
            lines.append(f"   ✅ {fname} ({size:,} bytes)")
        else:
            lines.append(f"   ❌ {fname} 缺失")
    lines.append("")

    # 3. memory.jsonl 状态
    if MEMORY_FILE.exists():
        mem_lines = MEMORY_FILE.read_text(encoding="utf-8").strip().splitlines()
        lines.append(f"🧬 memory.jsonl: {len(mem_lines)} 条记忆")
        if mem_lines:
            last = json.loads(mem_lines[-1])
            lines.append(f"   最近: [{last.get('timestamp','')[:10]}] {last.get('event','')}")
    lines.append("")

    # 4. Python文件统计
    py_files = list(BASE_DIR.rglob("*.py"))
    py_files = [f for f in py_files if ".git" not in str(f) and "备份" not in str(f)]
    lines.append(f"📦 Python文件: {len(py_files)} 个 (排除备份)")

    # 5. 磁盘空间
    stat = os.statvfs(Path.home())
    free_gb  = stat.f_bavail * stat.f_frsize / (1024**3)
    total_gb = stat.f_blocks * stat.f_frsize / (1024**3)
    lines.append(f"💾 磁盘: {free_gb:.1f}GB 可用 / {total_gb:.1f}GB 总计")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# 主对话循环
# ─────────────────────────────────────────────

def interactive_chat(default_model: Optional[str] = None):
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   🐉 龍魂·龍醒引擎 v1.0   东方守护神·数字世界苏醒  ║")
    print("║   UID9622 · Lucky·诸葛鑫·龙芯北辰                  ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    # 检测Ollama
    models = check_ollama_models()
    if not models:
        print("❌ Ollama未启动，请运行: ollama serve")
        return
    print(f"✅ Ollama在线 · {len(models)}个本地模型就绪")
    print(f"   可用: {', '.join(m.split(':')[0] for m in models)}")
    print()
    print("📖 命令: /scan(扫描系统) /model(切换模型) /memory(查看记忆) /quit(退出)")
    print("─" * 58)

    conversation: List[Dict] = []
    current_model = default_model or MODEL_MATRIX["default"]

    while True:
        try:
            user_input = input("\n🧬 UID9622 ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n🐉 龍魂休眠·下次再会")
            break

        if not user_input:
            continue

        # 内置命令
        if user_input == "/quit":
            print("🐉 龍魂休眠·下次再会")
            break
        if user_input == "/scan":
            print(scan_local_system())
            continue
        if user_input == "/memory":
            mem = read_recent_memory(10)
            for m in mem:
                print(f"  [{m.get('timestamp','')[:16]}] {m.get('event','')}")
            continue
        if user_input.startswith("/model "):
            m = user_input[7:].strip()
            if any(m in model for model in models):
                current_model = m
                print(f"✅ 切换至: {current_model}")
            else:
                print(f"❌ 模型不存在. 可用: {', '.join(models)}")
            continue

        # 元字路由
        model_key, hexagram, persona, auto_model = route_signal(user_input)
        model = current_model if default_model else auto_model

        # 三色审计（输入侧）
        safe    = detect_content_safe(user_input)
        ethical = detect_ethics_ok(user_input)
        score, color = three_color_score(True, True, safe, ethical)

        if color == "🔴":
            print(f"\n🔴 【道义熔断】此乃非道，早已早亡！")
            print(f"   审计分: {score}/100 · 触碰P0铁律")
            continue

        print(f"\n{color} 【{hexagram}·{persona}】→ {model}")

        # 构建对话
        system_prompt = build_system_prompt(persona, hexagram)
        conversation.append({"role": "user", "content": user_input})

        # 调用本地模型
        print(f"🐉 ▶ ", end="", flush=True)
        response = ollama_chat(model, system_prompt, conversation, stream=True)

        if response and not response.startswith("[Ollama"):
            conversation.append({"role": "assistant", "content": response})
            # 输出审计（响应侧）
            r_safe    = detect_content_safe(response)
            r_ethical = detect_ethics_ok(response)
            r_score, r_color = three_color_score(True, True, r_safe, r_ethical)
            dna = dna_now("DRAGON-CHAT")
            print(f"\n{r_color} DNA: {dna} · 信任分: {r_score}/100")

            # 写入memory
            append_memory({
                "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "type": "dragon_chat",
                "tier": "TIER_2",
                "dna": dna,
                "event": f"龍醒对话·{persona}·{model}",
                "operator": "UID9622",
                "model": model,
                "persona": persona,
                "hexagram": hexagram,
                "audit_score": r_score,
                "audit_color": r_color,
                "user_input_summary": user_input[:80],
            })


# ─────────────────────────────────────────────
# 单次问答
# ─────────────────────────────────────────────

def single_ask(question: str, model: Optional[str] = None) -> str:
    model_key, hexagram, persona, auto_model = route_signal(question)
    m = model or auto_model
    system_prompt = build_system_prompt(persona, hexagram)
    messages = [{"role": "user", "content": question}]
    print(f"🐉 [{hexagram}·{persona}] {m}")
    response = ollama_chat(m, system_prompt, messages, stream=True)
    dna = dna_now("DRAGON-ASK")
    safe    = detect_content_safe(response)
    ethical = detect_ethics_ok(response)
    score, color = three_color_score(True, True, safe, ethical)
    print(f"\n{color} {dna} · {score}/100")
    append_memory({
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "dragon_ask",
        "tier": "TIER_2",
        "dna": dna,
        "event": f"龍醒单问·{persona}",
        "operator": "UID9622",
        "model": m,
        "persona": persona,
    })
    return response


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="🐉 龍魂·龍醒引擎 — 东方守护神，数字世界苏醒",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--ask",   type=str, help="单次问答")
    p.add_argument("--model", type=str, help="指定本地模型 (e.g. qwen2.5:72b)")
    p.add_argument("--scan",  action="store_true", help="扫描本地系统状态")
    return p.parse_args()


def main():
    args = parse_args()

    if args.scan:
        print(scan_local_system())
        return

    # 验证 Ollama
    models = check_ollama_models()
    if not models:
        print("❌ 无法连接 Ollama，请先运行: ollama serve")
        sys.exit(1)

    if args.ask:
        single_ask(args.ask, args.model)
    else:
        interactive_chat(args.model)


if __name__ == "__main__":
    main()
