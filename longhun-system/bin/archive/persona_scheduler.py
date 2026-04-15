#!/usr/bin/env python3
"""
龍魂人格调度器 · 自运行核心 v2.0
DNA: #龍芯⚡️2026-04-01-PERSONA-SCHEDULER-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622
理论指导: 曾仕强老师（永恒显示）
"""

import json
import os
import subprocess
import sys
import time
import httpx
from datetime import datetime
from pathlib import Path

MVP_BASE    = "http://localhost:8000"
OLLAMA_BASE = "http://localhost:11434"
LOG_PATH    = Path.home() / "longhun-system" / "logs" / "persona_scheduler.jsonl"
CONFIRM     = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _get_system_context() -> str:
    """抓真实系统状态注入 prompt，让人格说的是真实情况"""
    ctx = []

    # 1. 本地服务存活（只写服务名，不带端口，避免模型误读数字）
    ports = {"MVP": 8000, "龍魂API": 9622, "Ollama": 11434, "WebUI": 8080}
    alive, dead = [], []
    for name, port in ports.items():
        try:
            httpx.get(f"http://localhost:{port}", timeout=2)
            alive.append(f"{name}✅")
        except Exception:
            dead.append(f"{name}❌")
    ctx.append(f"服务状态: {' '.join(alive + dead)}")

    # 2. Ollama 已加载模型数
    try:
        r = httpx.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        n = len(r.json().get("models", []))
        ctx.append(f"Ollama 已加载 {n} 个模型")
    except Exception:
        ctx.append("Ollama 无响应")

    # 3. 人格日志条数（今日）
    today = datetime.now().strftime("%Y-%m-%d")
    if LOG_PATH.exists():
        lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
        today_count = sum(1 for l in lines if today in l)
        ctx.append(f"今日人格日志: {today_count} 条 / 累计 {len(lines)} 条")
    else:
        ctx.append("今日人格日志: 0 条（首次运行）")

    # 4. shield_burn 熔断记录
    burn = Path(__file__).parent.parent / "cnsh-mvp" / "shield_burn.jsonl"
    if burn.exists():
        n = len(burn.read_text(encoding="utf-8").splitlines())
        ctx.append(f"熔断记录: {n} 条")

    # 5. session_log 最近一条时间
    slog = Path.home() / "longhun-system" / "logs" / "session_log.jsonl"
    if slog.exists():
        last = slog.read_text(encoding="utf-8").splitlines()
        if last:
            try:
                ts = json.loads(last[-1]).get("ts", "未知")[:16]
                ctx.append(f"最近会话: {ts}")
            except Exception:
                pass

    return "\n".join(ctx)


# ── 人格表 v2.0 · 腔调+真实数据 ──────────────────────────────
# style: 该人格说话方式（几个字，模型照着说）
# task_tmpl: {ctx} 会替换为真实系统状态
PERSONAS = {
    "p01": {
        "name":   "🎯 P01 龍芯诸葛",
        "model":  "chuxinzhiyi:latest",
        "style":  "说话像诸葛亮批注战报：简短、有判断、不废话、结论在前",
        "task_tmpl": (
            "当前系统实况如下：\n{ctx}\n\n"
            "用三才算法（天机·地势·人和）各一句话点评。"
            "每句格式：【X】结论。不要解释，不要「我认为」，直接给判断。"
        ),
        "interval_hours": 6,
    },
    "p02": {
        "name":   "🐱 P02 宝宝",
        "model":  "qwen2.5:7b",
        "style":  "说话像贴心小助手：口语、具体、只说眼前这台机器上的事，不说废话",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "根据上面的真实状态，说三件今天要盯的事。"
            "不要给我说「更新天气」「整理待办」，你盯的是这台机器的服务和日志。"
            "每条一句话，直接说具体的事。"
        ),
        "interval_hours": 2,
    },
    "p03": {
        "name":   "📊 P03 雯雯",
        "model":  "qwen2.5:7b",
        "style":  "说话像质检员写巡检报告：三色标注，问题说具体，不说空话",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "输出三色巡检结果，每条必须基于上面的真实数据，不许编：\n"
            "🟢 正常：（说哪个服务/哪个指标正常，具体数字）\n"
            "🟡 待关注：（说哪里有隐患，根据什么数据判断）\n"
            "🔴 需处理：（掉线的/异常的直接指出，没有就写「暂无」）"
        ),
        "interval_hours": 4,
    },
    "p04": {
        "name":   "🧠 P04 文心",
        "model":  "chuxinzhiyi:latest",
        "style":  "说话像做语义分析的研究员：挖本质，找规律，一句话说透",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "从这些数据里，提炼一个别人没注意到的规律或趋势。"
            "一句话说透本质，再给一个可执行的改进方向（不超过20字）。"
        ),
        "interval_hours": 8,
    },
    "p05": {
        "name":   "☯️ P05 龍芯老子",
        "model":  "qwen:7b-chat",
        "style":  "引道德经原文，用现代话解释和这台系统的关系，不讲大道理",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "从道德经81章里找一句最贴这个状态的话，原文引用，"
            "然后用一句现代话说为什么选这句、跟系统当前状态有什么关系。"
        ),
        "interval_hours": 24,
    },
    "p06": {
        "name":   "📚 P06 龍芯孔子",
        "model":  "qwen:7b-chat",
        "style":  "用仁义礼智信五德框架说话，结合实际，不做道德说教",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "用仁义礼智信，各一句话评这个系统今日的社区治理状态。"
            "必须对应上面的真实数据，不要泛泛而谈。"
        ),
        "interval_hours": 24,
    },
    "p07": {
        "name":   "🕊️ P07 龍芯墨子",
        "model":  "llama3.1:8b",
        "style":  "说话直接、务实，站在普通用户立场，不说高大上的话",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "站在一个普通用户角度：这套系统今天有没有什么地方可能害到他？"
            "说一个风险（没有就说没有，不要编），说一个建议。各一句话。"
        ),
        "interval_hours": 24,
    },
    "p08": {
        "name":   "📈 P08 数据大师",
        "model":  "qwen2.5:7b",
        "style":  "说话像数据分析师：只认数字，结论后面必须有依据",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "从这些数据里提取三个健康指标，格式：\n"
            "指标名: 当前值 | 状态 | 下一步\n"
            "数字必须来自上面的实际数据，不能编造。"
        ),
        "interval_hours": 4,
    },
    "p09": {
        "name":   "🎨 P09 界面炼金",
        "model":  "qwen2.5:7b",
        "style":  "说话像产品设计师，具体到一个改动，说改了之后用户感受什么变化",
        "task_tmpl": (
            "当前系统实况：\n{ctx}\n\n"
            "针对龍魂系统的日志查看体验，提一个最小可行的改进：\n"
            "改什么（一句话）→ 改了之后用户感受到什么变化（一句话）。"
        ),
        "interval_hours": 24,
    },
}


def _dna(topic: str) -> str:
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-v1.0"


def _local_log(pid: str, name: str, model: str, output: str, dna: str, elapsed: float):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts":       datetime.now().isoformat(),
        "persona":  pid,
        "name":     name,
        "model":    model,
        "output":   output[:600],
        "dna":      dna,
        "elapsed_s": round(elapsed, 2),
        "confirm":  CONFIRM,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _mvp_ingest(source: str, title: str, content: str) -> dict:
    try:
        r = httpx.post(
            f"{MVP_BASE}/shield/ingest",
            json={"content": content, "source": source, "title": title},
            timeout=15,
        )
        return r.json() if r.status_code == 200 else {"error": r.text[:100]}
    except Exception as e:
        return {"error": str(e)[:80]}


def _ollama_generate(model: str, prompt: str, timeout: int = 120) -> str:
    try:
        r = httpx.post(
            f"{OLLAMA_BASE}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.json().get("response", "（无输出）").strip()
        return f"[Ollama错误 {r.status_code}]"
    except Exception as e:
        return f"[调用失败] {str(e)[:80]}"


def run_persona(pid: str) -> dict:
    p = PERSONAS.get(pid)
    if not p:
        return {"error": f"未知人格 {pid}"}

    dna  = _dna(f"PERSONA-{pid.upper()}")
    ts   = datetime.now().strftime("%Y-%m-%d %H:%M")
    ctx  = _get_system_context()

    prompt = (
        f"你是{p['name']}，说话风格：{p['style']}。\n"
        f"时间：{ts}\n\n"
        f"{p['task_tmpl'].format(ctx=ctx)}\n\n"
        f"字数不超过150字。结尾一行写：DNA: {dna}"
    )

    print(f"[{ts}] {p['name']} · {p['model']}")
    t0      = time.time()
    output  = _ollama_generate(p["model"], prompt)
    elapsed = time.time() - t0

    _local_log(pid, p["name"], p["model"], output, dna, elapsed)

    title   = f"[人格日志] {p['name']} · {ts}"
    content = (
        f"人格: {p['name']} | 模型: {p['model']}\n"
        f"系统实况:\n{ctx}\n"
        f"输出:\n{output}\n"
        f"DNA: {dna} | {CONFIRM}"
    )
    ingest = _mvp_ingest(f"persona_{pid}", title, content)

    print(f"  {output[:100]}")
    print(f"  落地: {ingest.get('written_to', ingest.get('error', '?'))} | {elapsed:.1f}s")
    return {
        "persona": pid,
        "name":    p["name"],
        "model":   p["model"],
        "dna":     dna,
        "output":  output,
        "elapsed_s": round(elapsed, 2),
        "notion":  ingest.get("written_to", []),
    }


def run_all():
    print(f"\n{'='*55}")
    print(f"🐉 龍魂人格调度器 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}")
    results = []
    for pid in PERSONAS:
        r = run_persona(pid)
        results.append(r)
        time.sleep(1)
    print(f"\n✅ {len(results)} 个人格已运行 · 日志: {LOG_PATH}")
    return results


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--all" in args:
        run_all()
    else:
        pid = args[0].lower()
        r = run_persona(pid)
        print(json.dumps(r, ensure_ascii=False, indent=2))
