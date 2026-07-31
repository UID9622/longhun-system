# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-FIVE-ELEMENT-AUDIT-CLI-v1.0
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# 功能: 龍魂 · 五行审计决策 CLI
"""
龍魂 · 五行审计决策 CLI v1.0

用法:
  python3 bin/lh_five_element_audit.py text "龍魂系统采用DNA追溯码..."
  python3 bin/lh_five_element_audit.py dr 123456789
  python3 bin/lh_five_element_audit.py scores --木 0.9 --火 0.8 --土 0.7 --金 0.9 --水 0.6
  python3 bin/lh_five_element_audit.py demo
"""

import sys
import json
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "engines"))

from lh_five_element_audit_engine import FiveElementAuditEngine


def _asdict(report):
    return {
        "dna": report.dna,
        "input_digest": report.input_digest,
        "audited_at": report.audited_at,
        "confirm": report.confirm,
        "fixed_point": {
            "digital_root": report.fixed_point.digital_root,
            "element": report.fixed_point.element,
            "is_369": report.fixed_point.is_369,
            "is_global_fixed": report.fixed_point.is_global_fixed,
            "is_cycle": report.fixed_point.is_cycle,
        },
        "dimension_scores": report.dimension_scores,
        "balance": report.balance,
        "shengke": report.shengke,
        "overall_score": report.overall_score,
        "color": report.color,
        "decision": report.decision,
    }


def cmd_text(args):
    engine = FiveElementAuditEngine()
    report = engine.audit_text(args.text)
    print(json.dumps(_asdict(report), ensure_ascii=False, indent=2))


def cmd_dr(args):
    engine = FiveElementAuditEngine()
    fp = engine.analyze_fixed_point(args.value)
    result = {
        "input": args.value,
        "digital_root": fp.digital_root,
        "element": fp.element,
        "is_369": fp.is_369,
        "is_global_fixed": fp.is_global_fixed,
        "is_cycle": fp.is_cycle,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_scores(args):
    engine = FiveElementAuditEngine()
    scores = {
        "木": args.mu,
        "火": args.huo,
        "土": args.tu,
        "金": args.jin,
        "水": args.shui,
    }
    report = engine.audit_scores(scores, seed=args.seed)
    print(json.dumps(_asdict(report), ensure_ascii=False, indent=2))


def cmd_demo(_):
    FiveElementAuditEngine().demo()


def main():
    p = argparse.ArgumentParser(description="龍魂 · 五行审计决策 CLI v1.0")
    sp = p.add_subparsers(dest="cmd")

    t = sp.add_parser("text", help="对文本进行五行审计")
    t.add_argument("text", help="待审计文本")

    d = sp.add_parser("dr", help="计算数字根与不动点性质")
    d.add_argument("value", help="整数或文本")

    s = sp.add_parser("scores", help="直接传入五维评分进行审计")
    s.add_argument("--木", dest="mu", type=float, default=0.0)
    s.add_argument("--火", dest="huo", type=float, default=0.0)
    s.add_argument("--土", dest="tu", type=float, default=0.0)
    s.add_argument("--金", dest="jin", type=float, default=0.0)
    s.add_argument("--水", dest="shui", type=float, default=0.0)
    s.add_argument("--seed", type=int, default=0, help="数字根种子")

    sp.add_parser("demo", help="运行演示")

    args = p.parse_args()
    if args.cmd == "text":
        cmd_text(args)
    elif args.cmd == "dr":
        cmd_dr(args)
    elif args.cmd == "scores":
        cmd_scores(args)
    elif args.cmd == "demo":
        cmd_demo(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
