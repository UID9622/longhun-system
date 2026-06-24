#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  天道系统 CLI / heaven_cli.py v3.0                               ║
║                                                                  ║
║  命令行入口：查看星宿、节气、离火运、冲突检测、生成报告、热力图  ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-24-UID9622-TIANDAO-CLI-v3.0                  ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL      ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  来源: UID9622_天道系统_星宿离火运升级_v3.0.md                  ║
║  责任: UID9622 · 不免责                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cnsh-core"))

from scheduler.heaven_duty_engine import HeavenDutyEngine, make_dna


def cmd_status(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    report = engine.get_current_report(identity=args.identity)
    data = report.to_dict()

    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  天道系统 · 当前状态                                              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"DNA        : {data['DNA']}")
    print(f"时间       : {data['timestamp']}")
    print(f"节气       : {data['solar_term']} (火势权重 {data['solar_term_fire']})")
    print(f"时辰       : {data['branch']}时 ({data['hour']:02d}:00)")
    print(f"当值星宿   : {data['current_star']['name']} ({data['current_star']['name_en']})")
    print(f"  五行     : {data['current_star']['wuxing']}")
    print(f"  方向     : {data['current_star']['direction']}")
    print(f"  主事     : {data['current_star']['behavior']}")
    print(f"   Blessing: {data['current_star']['blessing']}")
    print(f"  Warning  : {data['current_star']['warning']}")
    print(f"当前卦象   : {data['current_gua']}")
    print(f"离火运指数 : {data['fire_index']['current']} ({data['fire_index']['level']} {data['fire_index']['color']})")
    print(f"趋势       : {data['fire_index']['trend']}")
    print(f"未来6时辰  : {data['fire_index']['predicted_next_6']}")
    print(f"主权身份   : {data['sovereign_status']['identity']}")
    print(f"绑定星宿   : {data['sovereign_status']['bound_star']}")
    print(f"主权模式   : {data['sovereign_status']['mode']}")
    print(f"权限提升   : +{data['sovereign_status']['privilege_boost']}")
    print(f"冲突状态   : {data['conflict_report']['relation']} [{data['conflict_report']['protocol']}]")
    print(f"推荐行动   : {data['recommended_action']}")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_reflect(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    report = engine.get_current_report(identity=args.identity)
    print(f"✅ reflection_report.json 已生成")
    print(f"   路径: {ROOT / 'cnsh-core' / 'scheduler' / 'outputs' / 'reflection_report.json'}")
    print(f"   DNA: {report.dna}")


def cmd_predict(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    dt = datetime.now()
    hours = args.hours
    print(f"🔥 未来 {hours} 小时离火运预测（每2时辰一个点）：")
    for i in range(0, hours, 2):
        future = dt.fromtimestamp(dt.timestamp() + i * 3600)
        fire = engine.compute_fire_index(future)
        star = engine.get_star_by_hour(future)
        term, term_fire = engine.get_solar_term(future)
        print(f"  +{i:3d}h ({future.strftime('%m-%d %H:%M')}) | {star.name} | {term} | {fire.current:.3f} {fire.color} {fire.level}")


def cmd_simulate(args):
    dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    report = engine.get_current_report(identity=args.identity, dt=dt)
    data = report.to_dict()
    print(f"🌌 模拟时间: {data['timestamp']}")
    print(f"   节气     : {data['solar_term']} (火势 {data['solar_term_fire']})")
    print(f"   当值星宿 : {data['current_star']['name']} ({data['current_star']['behavior']})")
    print(f"   离火运   : {data['fire_index']['current']} {data['fire_index']['color']} {data['fire_index']['level']}")
    print(f"   冲突状态 : {data['conflict_report']['relation']}")
    print(f"   推荐行动 : {data['recommended_action']}")


def cmd_conflict(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    conflict = engine.detect_conflict(args.identity)
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  星宿冲突检测报告                                                 ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"当前星宿   : {conflict.current_star} ({conflict.current_wuxing})")
    print(f"绑定星宿   : {conflict.bound_star} ({conflict.bound_wuxing})")
    print(f"五行关系   : {conflict.relation}")
    print(f"是否冲突   : {'是' if conflict.conflict else '否'}")
    print(f"执行协议   : {conflict.protocol}")
    print(f"建议行动   : {conflict.action}")


def cmd_heatmap(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    path = engine.generate_behavior_heatmap()
    print(f"🌌 二十八星宿行为矩阵热力图已生成")
    print(f"   路径: {path}")


def cmd_set_star(args):
    if args.identity != "UID9622":
        print("🔴 仅 UID9622 可手动切换主权星宿")
        sys.exit(1)
    print(f"⚡ 强制将 UID9622 主权星宿切换为: {args.star}")
    print(f"   DNA: {make_dna(f'UID9622|SET-STAR|{args.star}', 'SOVEREIGN-SET-STAR')}")
    print("   [注] v3.0 为静态绑定，此命令仅生成审计意图记录；动态切换需 v3.1 支持")


def cmd_override(args):
    engine = HeavenDutyEngine(system_load=args.system_load, user_activity=args.user_activity)
    record = engine.record_override(args.identity, args.action, args.justification)
    print(f"⚡ 主权豁免操作已记录")
    print(f"   DNA: {record['dna']}")
    print(f"   操作: {record['action']}")
    print(f"   理由: {record['justification']}")


def main():
    parser = argparse.ArgumentParser(
        description="天道系统 CLI · 二十四节气 · 二十八星宿 · 离火运 · 主权映射 · 冲突避让",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--identity", default="UID9622", help="身份标识")
    parser.add_argument("--system-load", type=float, default=0.5, help="系统负载热度 (0.0-1.0)")
    parser.add_argument("--user-activity", type=float, default=0.5, help="用户主动操作频率 (0.0-1.0)")
    parser.add_argument("--json", action="store_true", help="同时输出 JSON")

    sub = parser.add_subparsers(dest="command", help="子命令")

    p_status = sub.add_parser("status", help="查看当前天道系统状态")
    p_status.set_defaults(func=cmd_status)

    p_reflect = sub.add_parser("reflect", help="生成 reflection_report.json")
    p_reflect.set_defaults(func=cmd_reflect)

    p_predict = sub.add_parser("predict", help="预测未来离火运")
    p_predict.add_argument("--hours", type=int, default=12, help="预测小时数")
    p_predict.set_defaults(func=cmd_predict)

    p_simulate = sub.add_parser("simulate", help="模拟指定时辰")
    p_simulate.add_argument("--datetime", required=True, help="时间格式: 2026-06-24 09:00")
    p_simulate.set_defaults(func=cmd_simulate)

    p_conflict = sub.add_parser("conflict", help="检测星宿冲突")
    p_conflict.set_defaults(func=cmd_conflict)

    p_heatmap = sub.add_parser("heatmap", help="生成二十八星宿行为矩阵热力图")
    p_heatmap.set_defaults(func=cmd_heatmap)

    p_set = sub.add_parser("set-star", help="手动切换主权星宿（仅 UID9622）")
    p_set.add_argument("star", help="目标星宿名，如 亢金龙")
    p_set.add_argument("--force", action="store_true", required=True, help="必须加 --force 确认")
    p_set.set_defaults(func=cmd_set_star)

    p_override = sub.add_parser("override", help="记录主权豁免操作")
    p_override.add_argument("--action", required=True, help="操作描述")
    p_override.add_argument("--justification", required=True, help="豁免理由")
    p_override.set_defaults(func=cmd_override)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
