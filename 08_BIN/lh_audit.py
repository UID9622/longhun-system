#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_audit.py — 三色审计 CLI 薄包装（对齐部署文档命令）
# DNA: #龍芯⚡️2026-08-31-SOVEREIGNTY-KILLSWITCH-DEPLOY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: python3 bin/lh_audit.py --tri-color --full
#   --tri-color  三色审计（调用 P05 三色判定引擎 bin/lh_three_color_audit.py）
#   --full       全量部署检查（对象=全系统部署·类型=部署检查）
# ═══════════════════════════════════════════════════════════
"""龍魂三色审计 CLI 入口。核心判定复用 lh_three_color_audit.py，本文件仅做参数对齐薄包装。"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "lh_three_color_audit.py")

DEFAULT_OBJECT = "龍魂系统主权协议+反黑箱+KillSwitch熔断部署检查(2026-08-31)"
DEFAULT_TYPE = "部署检查"


def _run_engine(extra_args):
    if not os.path.exists(ENGINE):
        print(f"ERROR: 三色审计引擎缺失 {ENGINE}")
        return 1
    cmd = [sys.executable, ENGINE, "audit"] + extra_args
    return subprocess.call(cmd)


def _route_report(argv):
    """lh audit report → 合规报告引擎（任务E·2026-09-03）
    透传剩余参数(--out/--pdf)给 lh_audit_report.py"""
    rpt = os.path.join(HERE, "lh_audit_report.py")
    if not os.path.exists(rpt):
        print(f"ERROR: 合规报告引擎缺失 {rpt}")
        return 1
    return subprocess.call([sys.executable, rpt] + argv)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        return _route_report(sys.argv[2:])
    parser = argparse.ArgumentParser(description="🐉 龍魂·三色审计 CLI（部署文档入口）")
    parser.add_argument("--tri-color", action="store_true", help="三色审计")
    parser.add_argument("--full", action="store_true", help="全量部署检查")
    parser.add_argument("--object", "-o", default=DEFAULT_OBJECT, help="被审计对象描述")
    parser.add_argument("--type", "-t", default=DEFAULT_TYPE, help="对象类型")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    args = parser.parse_args()

    if args.tri_color:
        engine_args = ["--object", args.object, "--type", args.type]
        if args.quiet:
            engine_args.append("--quiet")
        return _run_engine(engine_args)
    if args.full:
        # 全量 = 部署检查 + JSON 留痕
        engine_args = ["--object", args.object, "--type", args.type, "--json"]
        return _run_engine(engine_args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
