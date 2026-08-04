#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 龍魂·序列执行引擎 CLI
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-SEQUENCE-CLI-v1.0

用法:
  lh seq --text "有人说只有他能教某技术"
  lh seq --file article.md
  lh seq --text "..." --pipeline safeai,kfpp,csdn,judge
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engines.lh_sequence_executor import SequenceExecutor, DEFAULT_PIPELINE


def main():
    parser = argparse.ArgumentParser(description="龍魂·序列执行引擎")
    parser.add_argument("--text", type=str, help="输入文本")
    parser.add_argument("--file", type=str, help="输入文件路径")
    parser.add_argument("--title", type=str, default="", help="标题")
    parser.add_argument("--pipeline", type=str, default=",".join(DEFAULT_PIPELINE),
                        help=f"流水线阶段，逗号分隔，默认: {','.join(DEFAULT_PIPELINE)}")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        text = path.read_text(encoding="utf-8")
        title = args.title or path.name
    elif args.text:
        text = args.text
        title = args.title
    else:
        parser.print_help()
        return

    pipeline = [s.strip() for s in args.pipeline.split(",") if s.strip()]
    executor = SequenceExecutor(pipeline=pipeline)
    report = executor.run(text, title=title)

    if args.raw:
        import json
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        # 复用引擎内部格式化逻辑太麻烦，这里直接调用引擎的 main 逻辑
        # 但为了统一，我们重新实现简洁版输出
        print("=" * 64)
        print("🔄 龍魂·序列执行引擎")
        print("=" * 64)
        print(f"输入: {report['input']['text_preview']}")
        print(f"流水线: {' → '.join(report['pipeline'])}")
        print("-" * 64)
        for r in report["results"]:
            emoji = {"ok": "🟢", "warn": "🟡", "block": "🔴", "error": "⚠️"}.get(r["status"], "⚪")
            print(f"{emoji} [{r['stage']}] {r['level']} | 得分: {r['score']}")
            print(f"   {r['summary'][:120]}")
        print("-" * 64)
        print(f"最终级别: {report['final_level']}")
        print(f"结论: {report['final_summary']}")
        print(f"🧬 {report['dna']}")
        print("=" * 64)


if __name__ == "__main__":
    main()
