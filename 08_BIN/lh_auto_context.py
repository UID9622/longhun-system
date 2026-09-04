#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-AUTO-CONTEXT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 会话自动上下文引擎 — 分工矩阵+最近记忆摘要+待办+系统状态 一键打包
#       解决"老大每次重复交代"：AI 进门自动加载 auto_context.md，一句话带全上下文。
# 协议: CC BY-NC-SA 4.0（核心思想层）· GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""龍魂 · 会话自动上下文引擎 v1.0
生成 .codebuddy/memory/auto_context.md：
  - 人格分工矩阵摘要（谁负责什么）
  - 最近 N 日记忆摘要（细节不遗忘）
  - 待办/未完成任务
  - 常用命令速查
  - 系统关键状态

用法:
  lh auto-context              # 生成上下文包（默认最近7日）
  lh auto-context --days 14    # 指定回溯天数
  lh auto-context --json       # JSON 输出（管道用）
  lh auto-context --watch      # 生成后自动打开预览
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM_DIR = ROOT / ".codebuddy" / "memory"
OUT_FILE = MEM_DIR / "auto_context.md"
DUTY_FILE = ROOT / "20_CONFIG" / "persona-duty-matrix.json"
STATE_FILE = ROOT / "STATE.md"
CMD_INDEX = ROOT / ".codebuddy" / "COMMAND_INDEX.md"

TZ_HINT = "2026-08-13T00:00:00+08:00"


def _stamp():
    """简单时间戳（LU-Time 由 lh 外壳统一打）"""
    return "🐉丙午·丙申·庚申·亥时·䷖剥"


def load_duty_matrix():
    """读取人格分工矩阵"""
    if not DUTY_FILE.exists():
        return None
    try:
        return json.loads(DUTY_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": str(e)}


def duty_summary():
    """生成分工矩阵摘要文本"""
    m = load_duty_matrix()
    if not m or "维护分工" not in m:
        return "- 分工矩阵未找到（20_CONFIG/persona-duty-matrix.json）\n"
    lines = []
    for p in m["维护分工"]:
        lines.append(
            f"- **{p['人格']} {p['称号']}**（{p['层']}）负责: {', '.join(p['负责领域'])} · 触发词: {', '.join(p['触发词'][:3])}"
        )
    return "\n".join(lines) + "\n"


def recent_memory_summary(days: int = 7):
    """汇总最近 N 日记忆日志，提取关键条目"""
    today = datetime.now()
    files = sorted(MEM_DIR.glob("*.md"))
    picked = []
    for f in files:
        if f.name in ("MEMORY.md", "auto_context.md", "README.md"):
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
        except Exception:
            continue
        if (today - mtime).days <= days:
            picked.append(f)
    if not picked:
        return "- 最近 {} 日内无记忆日志\n".format(days)
    lines = [f"### 最近 {days} 日记忆日志（{len(picked)} 份）"]
    for f in sorted(picked, key=lambda x: x.stat().st_mtime, reverse=True):
        content = f.read_text(encoding="utf-8", errors="ignore")
        headers = re.findall(r"^#{2,4}\s+(.+)$", content, re.M)
        bullets = [h for h in headers if len(h) > 3]
        if bullets:
            lines.append(f"- **{f.name}**: " + " | ".join(bullets[:6]))
        else:
            lines.append(f"- **{f.name}**: （无结构化标题）")
    return "\n".join(lines) + "\n"


def todo_summary():
    """从 STATE.md 提取待办"""
    if not STATE_FILE.exists():
        return "- STATE.md 不存在\n"
    content = STATE_FILE.read_text(encoding="utf-8", errors="ignore")
    section = re.search(r"(?:待办|TODO|待完成)[^\n]*\n([\s\S]*?)(?=\n##|\Z)", content)
    if not section:
        return "- STATE.md 中无待办区块\n"
    items = [ln.strip().lstrip("-* ") for ln in section.group(1).splitlines() if ln.strip()]
    if not items:
        return "- 待办区块为空\n"
    return "\n".join(f"- {i}" for i in items[:20]) + "\n"


def cmd_index_summary():
    """从 COMMAND_INDEX.md 提取核心命令"""
    if not CMD_INDEX.exists():
        return "- COMMAND_INDEX.md 不存在\n"
    content = CMD_INDEX.read_text(encoding="utf-8", errors="ignore")
    lines = [ln for ln in content.splitlines() if "lh " in ln and ("|" in ln)]
    out = []
    for ln in lines[:12]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[1]:
            out.append(f"- `{cells[1]}` — {cells[2] if len(cells) > 2 else ''}")
    return ("\n".join(out) + "\n") if out else "- 命令总目未解析\n"


def state_snapshot():
    """关键状态快照"""
    snap = []
    if STATE_FILE.exists():
        snap.append(f"- STATE.md: {STATE_FILE.name}（{STATE_FILE.stat().st_size} bytes）")
    if DUTY_FILE.exists():
        snap.append(f"- 分工矩阵: persona-duty-matrix.json v1.0 🟢")
    if OUT_FILE.exists():
        _t = datetime.fromtimestamp(OUT_FILE.stat().st_mtime).strftime("%m-%d %H:%M")
        snap.append(f"- 上次上下文包: {_t}")
    return "\n".join(snap) + "\n"


def build_context(days: int = 7) -> str:
    parts = [
        "# 🐉 龍魂 · 会话自动上下文包",
        "",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 回溯 {days} 日",
        "> 🔥 本文件由 `lh auto-context` 自动生成。AI 每次会话进门必读，老大无需重复交代。",
        "",
        "## 🧩 人格分工矩阵（谁负责什么·焊死）",
        "",
        duty_summary(),
        "",
        "## 🧠 最近记忆摘要（细节不遗忘）",
        "",
        recent_memory_summary(days),
        "",
        "## ✅ 待办/未完成",
        "",
        todo_summary(),
        "",
        "## ⚡ 常用命令速查",
        "",
        cmd_index_summary(),
        "",
        "## 📡 系统状态快照",
        "",
        state_snapshot(),
        "",
        "---",
        f"*自动生成 · {_stamp()} · DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-AUTO-CONTEXT-v1.0-UID9622*",
        "",
    ]
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="会话自动上下文引擎")
    ap.add_argument("--days", type=int, default=7, help="回溯天数（默认7）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--watch", action="store_true", help="生成后打印路径")
    args = ap.parse_args()

    MEM_DIR.mkdir(parents=True, exist_ok=True)
    text = build_context(args.days)
    OUT_FILE.write_text(text, encoding="utf-8")

    if args.json:
        print(json.dumps({"out": str(OUT_FILE), "bytes": len(text), "stamp": _stamp()},
                         ensure_ascii=False))
        return 0

    print(text)
    print(f"\n✅ 上下文包已生成: {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
