# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人民技能边界命令行工具

DNA:#龍芯⚡️2026-06-21-SKILL-SCOPE-CLI-v1.0

用法:
  python3 skill_scope_cli.py check <职业> <技能领域> [意图]
  python3 skill_scope_cli.py explain <UID> [--profession <职业>]
  python3 skill_scope_cli.py demo
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from people_skill_scope import get_skill_scope_guard


def cmd_check(args):
    guard = get_skill_scope_guard()
    profession = args.profession or ""
    intent = args.intent or ""
    verdict = guard.personalized_verdict(
        uid=f"cli-{profession or 'user'}",
        domain_name=args.domain,
        stated_intent=intent,
        profession=profession,
    )
    print(f"\n🐉 技能边界判定")
    print(f"   职业: {profession or '未填'}")
    print(f"   技能: {args.domain}")
    print(f"   意图: {intent or '未填'}")
    print(f"   结果: {verdict['result']}")
    print(f"   说明: {verdict['reason']}")


def cmd_explain(args):
    guard = get_skill_scope_guard()
    # 确保已按职业生成边界
    if args.profession:
        guard.get_scope(args.uid, profession=args.profession)
    print(guard.explain(args.uid))
    print("\n" + guard.recommend_pair(args.uid))


def cmd_demo(_):
    guard = get_skill_scope_guard()
    print("🐉 人民技能边界 · 示例")
    examples = [
        ("农民", "农业生产", "看天气、记农事"),
        ("医生", "医疗建议", "帮我整理病历"),
        ("自由职业", "医疗建议", "帮我诊断病情"),
        ("程序员", "编程", "我要写一个全自动工具取代同事"),
    ]
    for prof, domain, intent in examples:
        verdict = guard.personalized_verdict(
            uid=f"demo-{prof}",
            domain_name=domain,
            stated_intent=intent,
            profession=prof,
        )
        print(f"\n  {prof} → {domain}: {verdict['result']}")
        print(f"     意图: {intent}")
        print(f"     说明: {verdict['reason']}")


def main():
    parser = argparse.ArgumentParser(description="人民技能边界工具")
    sub = parser.add_subparsers(dest="cmd")

    check = sub.add_parser("check", help="检查某人能否使用某技能")
    check.add_argument("profession", help="职业/身份")
    check.add_argument("domain", help="技能领域，如 医疗建议、编程、农业生产")
    check.add_argument("intent", nargs="?", default="", help="使用意图")

    explain = sub.add_parser("explain", help="展示某用户的技能边界")
    explain.add_argument("uid", help="用户 UID")
    explain.add_argument("--profession", "-p", default="", help="职业")

    demo = sub.add_parser("demo", help="运行示例")

    args = parser.parse_args()
    if args.cmd == "check":
        cmd_check(args)
    elif args.cmd == "explain":
        cmd_explain(args)
    elif args.cmd == "demo":
        cmd_demo(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
