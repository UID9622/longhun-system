#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 情绪纠偏与意图自动执行引擎 (统一入口)
DNA: #龍芯⚡️丙午·丙申·壬戌·辰时-EMOTION-ENGINE-UID9622
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from executor_optimizer import EmotionCorrectionEngine


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂情绪纠偏引擎 - 自动理解并执行，不废话",
    )
    parser.add_argument("--input", "-i", type=str, help="用户输入文本")
    parser.add_argument("--file", "-f", type=str, help="从文件读取输入")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--exec", action="store_true", help="真实执行（否则默认 dry-run）")
    parser.add_argument("--project-root", type=str, default=None, help="项目根目录")
    parser.add_argument("--mode", type=str, default=None, choices=["dry-run", "exec"], help="执行模式")

    args = parser.parse_args()

    project_root = args.project_root or os.environ.get("LONGHUN_HOME", str(Path.home() / "longhun-system"))
    exec_mode = args.mode or ("exec" if args.exec else None)
    engine = EmotionCorrectionEngine(project_root=project_root, exec_mode=exec_mode)

    if args.interactive:
        print("🐉 龍魂情绪纠偏引擎 (交互模式)")
        print("输入任意文本，系统将自动纠偏并执行 (输入 'exit' / 'quit' 退出)")
        while True:
            try:
                user_input = input("\n你: ")
            except EOFError:
                break
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            result = engine.process(user_input, force_exec=args.exec)
            print("\n系统执行结果:")
            print(result)
        return

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            input_text = f.read()
    elif args.input:
        input_text = args.input
    else:
        input_text = sys.stdin.read()

    if input_text.strip():
        result = engine.process(input_text, force_exec=args.exec)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
