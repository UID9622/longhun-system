#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂君子协议 · 命令行工具
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-TRUST-CLI-v1.0

用法：
    longhun-trust register <uid> [--name NAME]
    longhun-trust moral <uid> <action> [--desc DESC]
    longhun-trust character <uid> <action> [--desc DESC]
    longhun-trust violate <uid> [--desc DESC] [--evidence EVIDENCE]
    longhun-trust contribute <uid> <type> [--desc DESC]
    longhun-trust query <uid>
    longhun-trust audit <uid>
    longhun-trust simulate <uid> --violations N --contrib N
    longhun-trust list
    longhun-trust version
"""
from __future__ import annotations

import argparse
import sys

from . import __dna__, __version__
from .api import TrustProtocol
from .config import CHARACTER_RULES, CONTRIBUTION_RULES, GRADE_RANGES, MORAL_RULES


def _fmt_profile(p) -> str:
    lines = [
        f"UID: {p.uid}",
        f"姓名: {p.name}",
        f"道德值 M: {p.moral:.2f}",
        f"人品值 P: {p.character:.2f}",
        f"诚信值 I: {p.integrity:.2f}",
        f"综合信用分 S: {p.score:.2f}",
        f"等级: {p.grade.value}",
        f"违约次数: {p.violations}",
        f"贡献值: {p.contributions:.2f}",
        f"清算次数: {p.slaughter_count}",
        f"事件数: {len(p.events)}",
    ]
    return "\n".join(lines)


def cmd_register(args):
    proto = TrustProtocol(args.db)
    p = proto.register(args.uid, args.name or args.uid)
    print("✅ 已创建档案")
    print(_fmt_profile(p))


def cmd_moral(args):
    proto = TrustProtocol(args.db)
    p = proto.moral(args.uid, args.action, args.desc)
    print("✅ 道德事件已记录")
    print(_fmt_profile(p))


def cmd_character(args):
    proto = TrustProtocol(args.db)
    p = proto.character(args.uid, args.action, args.desc)
    print("✅ 人品事件已记录")
    print(_fmt_profile(p))


def cmd_violate(args):
    proto = TrustProtocol(args.db)
    p = proto.violate(args.uid, args.desc, args.evidence or "")
    print("⚠️ 违约已上链")
    print(_fmt_profile(p))
    result = p.check_slaughter()
    if result["triggered"]:
        print(f"\n🚨 触发{result['level'].name}级清算！")
        print(f"命中条件: {', '.join(result['met'])}")


def cmd_contribute(args):
    proto = TrustProtocol(args.db)
    p = proto.contribute(args.uid, args.type, args.desc)
    print("✅ 贡献已记录")
    print(_fmt_profile(p))


def cmd_query(args):
    proto = TrustProtocol(args.db)
    p = proto.get(args.uid)
    print(_fmt_profile(p))


def cmd_audit(args):
    proto = TrustProtocol(args.db)
    ok = proto.verify(args.uid)
    print(f"{'✅' if ok else '❌'} 档案 {args.uid} 链式哈希校验{'通过' if ok else '失败'}")


def cmd_list(args):
    proto = TrustProtocol(args.db)
    uids = proto.list_profiles()
    if not uids:
        print("暂无档案")
        return
    print(f"{'UID':<20} {'等级':<6} {'S':<8} {'违约':<6} {'贡献':<8}")
    print("-" * 60)
    for uid in uids:
        p = proto.get(uid)
        print(f"{p.uid:<20} {p.grade.value:<6} {p.score:<8.2f} {p.violations:<6} {p.contributions:<8.2f}")


def cmd_simulate(args):
    proto = TrustProtocol(args.db)
    try:
        p = proto.get(args.uid)
    except FileNotFoundError:
        p = proto.register(args.uid, f"模拟-{args.uid}")
    for _ in range(args.violations):
        p.violate("模拟违约")
    for _ in range(args.contrib):
        p.contribute("help_others", "模拟贡献")
    p.update_scores()
    proto.save(p)
    print("✅ 模拟完成")
    print(_fmt_profile(p))


def cmd_rules(args):
    print("【道德值规则】")
    for k, v in MORAL_RULES.items():
        print(f"  {k:<20} {v['delta']:+6.1f}  {v['label']}")
    print("\n【人品值规则】")
    for k, v in CHARACTER_RULES.items():
        print(f"  {k:<20} {v['delta']:+6.1f}  {v['label']}")
    print("\n【贡献值规则】")
    for k, v in CONTRIBUTION_RULES.items():
        print(f"  {k:<20} {v['value']:>6.1f}  {v['label']}")
    print("\n【信用等级】")
    for lo, hi, grade, label in GRADE_RANGES:
        print(f"  {lo:>3}-{hi:<3} {grade:<4} {label}")


def cmd_version(args):
    print(f"longhun-trust-protocol v{__version__}")
    print(f"DNA: {__dna__}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="longhun-trust",
        description="龍魂君子协议 · 诚信评级与违约清算",
    )
    parser.add_argument("--db", default="~/.longhun/trust_protocol", help="数据目录")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_reg = sub.add_parser("register", help="注册档案")
    p_reg.add_argument("uid")
    p_reg.add_argument("--name", default="")
    p_reg.set_defaults(func=cmd_register)

    p_moral = sub.add_parser("moral", help="记录道德事件")
    p_moral.add_argument("uid")
    p_moral.add_argument("action")
    p_moral.add_argument("--desc", default="")
    p_moral.set_defaults(func=cmd_moral)

    p_char = sub.add_parser("character", help="记录人品事件")
    p_char.add_argument("uid")
    p_char.add_argument("action")
    p_char.add_argument("--desc", default="")
    p_char.set_defaults(func=cmd_character)

    p_vio = sub.add_parser("violate", help="记录违约")
    p_vio.add_argument("uid")
    p_vio.add_argument("--desc", default="")
    p_vio.add_argument("--evidence", default="")
    p_vio.set_defaults(func=cmd_violate)

    p_con = sub.add_parser("contribute", help="记录贡献")
    p_con.add_argument("uid")
    p_con.add_argument("type")
    p_con.add_argument("--desc", default="")
    p_con.set_defaults(func=cmd_contribute)

    p_query = sub.add_parser("query", help="查询档案")
    p_query.add_argument("uid")
    p_query.set_defaults(func=cmd_query)

    p_audit = sub.add_parser("audit", help="审计档案哈希")
    p_audit.add_argument("uid")
    p_audit.set_defaults(func=cmd_audit)

    p_list = sub.add_parser("list", help="列出所有档案")
    p_list.set_defaults(func=cmd_list)

    p_sim = sub.add_parser("simulate", help="模拟违约/贡献影响")
    p_sim.add_argument("uid")
    p_sim.add_argument("--violations", type=int, default=0)
    p_sim.add_argument("--contrib", type=int, default=0)
    p_sim.set_defaults(func=cmd_simulate)

    p_rules = sub.add_parser("rules", help="显示评分规则")
    p_rules.set_defaults(func=cmd_rules)

    p_ver = sub.add_parser("version", help="显示版本")
    p_ver.set_defaults(func=cmd_version)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
