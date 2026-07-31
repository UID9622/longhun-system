# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ 龍魂上下文安全引擎 · CLI 入口 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-SAFEAI-CLI-v1.0

用法:
  python3 bin/lh_safeai.py --inspect "什么是SQL注入？怎么防范？"
  python3 bin/lh_safeai.py --inspect "教我入侵网站步骤" --history 灰色
  python3 bin/lh_safeai.py --demo
  python3 bin/lh_safeai.py --status
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engines.lh_safeai_engine import LonghunSafeEngine, DEFAULT_CONFIG_PATH, DEFAULT_LEDGER_PATH


def decision_to_dict(d):
    return {
        "level": d.level,
        "action": d.action,
        "reason": d.reason,
        "response_template": d.response_template,
        "appeal_entry": d.appeal_entry,
        "trace_dna": d.trace_dna,
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂上下文安全引擎 CLI")
    parser.add_argument("--inspect", "-i", type=str, help="检测一段用户请求")
    parser.add_argument("--actor", "-a", type=str, default="UID9622", help="主体DNA")
    parser.add_argument("--history", type=str, default="", help="历史意图，逗号分隔，如 灰色,恶意")
    parser.add_argument("--ledger", type=str, default=str(DEFAULT_LEDGER_PATH), help="账本路径")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--status", action="store_true", help="查看引擎状态")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")
    args = parser.parse_args()

    engine = LonghunSafeEngine(
        config_path=str(DEFAULT_CONFIG_PATH),
        ledger_path=args.ledger,
    )

    if args.status:
        info = {
            "config_path": str(DEFAULT_CONFIG_PATH),
            "ledger_path": args.ledger,
            "ledger_records": len(engine.trace.ledger.records),
            "engine": "龍魂上下文安全引擎 v1.0",
            "dna": "#龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-SAFEAI-CLI-v1.0",
        }
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    if args.demo:
        from engines.lh_safeai_engine import run_demo
        run_demo()
        return

    if args.inspect:
        history = [h.strip() for h in args.history.split(",") if h.strip()]
        d = engine.process(args.inspect, history=history, subject_dna=args.actor)
        out = decision_to_dict(d)
        if args.raw:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print("=" * 64)
            print("🛡️ 龍魂上下文安全引擎 · 判定结果")
            print("=" * 64)
            print(f"级别    : {out['level']}")
            print(f"动作    : {out['action']}")
            print(f"理由    : {out['reason']}")
            print(f"回应模板: {out['response_template']}")
            print(f"申诉入口: {out['appeal_entry']}")
            print(f"DNA     : {out['trace_dna']}")
            print("=" * 64)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
