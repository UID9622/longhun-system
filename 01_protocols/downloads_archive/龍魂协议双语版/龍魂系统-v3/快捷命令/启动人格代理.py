# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂·人格代理启动器 v1.0                                   ║
║  DNA: #龍芯⚡️20260529-PERSONA-AGENT-v1.0                   ║
╚══════════════════════════════════════════════════════════════╝

alias 宝宝 指向这里。
用法：python3 bin/启动人格代理.py [--persona P02] [--task "帮我做X"]
"""

import sys
import os
import argparse
from datetime import datetime

# 把上级目录加进 path·能 import 核心引擎
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from longhun_rules_engine_v2 import ScoreEngine, Event, tricolor_gate
except ImportError:
    print("⚠️  找不到 longhun_rules_engine_v2.py，请确认在 ~/longhun-system/ 目录下")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# 人格定义（精简版·P02 是默认宝宝）
# ─────────────────────────────────────────────────────────────
PERSONAS = {
    "P01": {"name": "诸葛亮", "role": "战略推演", "emoji": "🧠"},
    "P02": {"name": "宝宝",   "role": "日常接住老大", "emoji": "🐣"},
    "P03": {"name": "雯雯",   "role": "整理审计", "emoji": "📋"},
    "P04": {"name": "鲁班",   "role": "代码工程", "emoji": "🔧"},
    "P05": {"name": "上帝之眼", "role": "风险熔断", "emoji": "👁️"},
    "P13": {"name": "姜子牙", "role": "权限边界", "emoji": "⚖️"},
    "P72": {"name": "龍盾",   "role": "常驻守门", "emoji": "🛡️"},
}


def show_banner():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂·人格代理 v1.0  |  UID9622 龍芯北辰                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def show_status():
    """显示当前系统状态·分数总览"""
    engine = ScoreEngine()
    print("📊 当前账本状态：")
    if not engine.scores:
        print("   账本为空，暂无记录")
        return
    for person, score in sorted(engine.scores.items()):
        color, status = tricolor_gate(score)
        print(f"   {color} {person:8} 分={score:3d}  {status}")
    print()
    ok, msg = engine.verify_integrity()
    print(f"🔐 {msg}")


def route_task(task: str) -> str:
    """
    根据关键词路由到对应人格。
    简单版：关键词匹配。
    """
    task_lower = task.lower()

    if any(w in task for w in ["代码", "报错", "bug", "脚本", "python"]):
        return "P04"
    if any(w in task for w in ["风险", "坑", "安全", "熔断"]):
        return "P05"
    if any(w in task for w in ["战略", "推演", "下一步", "方向"]):
        return "P01"
    if any(w in task for w in ["整理", "审计", "报告", "格式"]):
        return "P03"
    if any(w in task for w in ["权限", "边界", "封神", "授权"]):
        return "P13"
    return "P02"  # 默认宝宝接


def interactive_mode():
    """交互模式·持续接老大任务"""
    show_banner()
    show_status()

    print("输入任务（直接回车退出）：")
    print()

    while True:
        try:
            task = input("老大 ▶  ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n收工！美滋滋~")
            break

        if not task:
            print("收工！美滋滋~")
            break

        # 路由
        persona_id = route_task(task)
        p = PERSONAS[persona_id]
        print(f"\n  {p['emoji']} [{persona_id}·{p['name']}] 接单：{p['role']}")
        print(f"  任务：{task}")
        print(f"  DNA：#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-TASK")
        print()


def main():
    parser = argparse.ArgumentParser(description="龍魂·人格代理启动器")
    parser.add_argument("--persona", default="P02", help="指定人格编号（默认P02宝宝）")
    parser.add_argument("--task", help="直接指定任务（不进交互模式）")
    parser.add_argument("--status", action="store_true", help="只显示当前状态")
    parser.add_argument("--list", action="store_true", help="列出所有人格")
    args = parser.parse_args()

    if args.list:
        show_banner()
        print("📋 可用人格：")
        for pid, p in PERSONAS.items():
            print(f"   {p['emoji']} {pid}·{p['name']:8}  {p['role']}")
        return

    if args.status:
        show_banner()
        show_status()
        return

    if args.task:
        show_banner()
        persona_id = args.persona if args.persona in PERSONAS else route_task(args.task)
        p = PERSONAS[persona_id]
        print(f"{p['emoji']} [{persona_id}·{p['name']}] 接单：{args.task}")
        return

    # 默认：交互模式
    interactive_mode()


if __name__ == "__main__":
    main()
