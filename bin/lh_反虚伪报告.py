# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·反虚伪视觉化报告
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-视觉报告-v1.0
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def 生成报告(文本: str, 检测结果: dict) -> str:
    """生成彩色终端报告。"""
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    报告行 = []
    报告行.append(f"{BOLD}{'='*60}{RESET}")
    报告行.append(f"{BOLD}🐉 反虚伪审计报告{RESET}")
    报告行.append(f"{BOLD}{'='*60}{RESET}")

    状态 = 检测结果.get("状态", "未知")
    状态颜色 = GREEN if 状态 == "通过" else (YELLOW if 状态 == "自动简化" else RED)
    报告行.append(f"状态: {状态颜色}{状态}{RESET}")

    分数 = 检测结果.get("虚伪度", 0)
    分数颜色 = GREEN if 分数 < 50 else (YELLOW if 分数 < 80 else RED)
    报告行.append(f"虚伪度: {分数颜色}{分数}{RESET}/100")

    一级命中 = 检测结果.get("一级命中", [])
    if 一级命中:
        报告行.append(f"{RED}🔴 一级禁用词: {', '.join(一级命中)}{RESET}")

    二级命中 = 检测结果.get("二级命中", [])
    if 二级命中:
        报告行.append(f"{YELLOW}🟡 二级禁用词: {', '.join(二级命中)}{RESET}")

    煽情计数 = 检测结果.get("煽情密度", 0)
    if 煽情计数 > 0:
        报告行.append(f"煽情词数: {煽情计数}")

    报告行.append(f"\n{BOLD}文本分布{RESET}")
    文本长度 = len(文本)
    建议长度 = 200
    比例 = min(文本长度 / 建议长度, 3)
    bar = "█" * int(比例 * 10)
    报告行.append(f"长度: {文本长度}字 {bar} {文本长度/建议长度:.1f}x")

    报告行.append(f"{BOLD}{'='*60}{RESET}")
    报告行.append(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d')}-反虚伪报告-v1.0")

    return '\n'.join(报告行)


def main():
    parser = __import__('argparse').ArgumentParser(description="龍魂反虚伪视觉化报告")
    parser.add_argument("text", nargs="?", help="要检测的文本")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取文本")
    args = parser.parse_args()

    文本 = ""
    if args.stdin:
        文本 = sys.stdin.read()
    elif args.text:
        文本 = args.text
    else:
        parser.print_help()
        sys.exit(1)

    # 调用反虚伪引擎
    try:
        sys.path.insert(0, str(Path.home() / "longhun-system" / "cnsh" / "core" / "cnsh_v2.1"))
        from cnsh_v21 import 反虚伪引擎
        检测结果 = 反虚伪引擎.检查回复(文本)
    except Exception as exc:
        检测结果 = {"状态": "错误", "虚伪度": 0, "建议": str(exc)}

    print(生成报告(文本, 检测结果))


if __name__ == "__main__":
    main()
