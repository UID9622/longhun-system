#!/usr/bin/env python3
"""
🐉 longhun 统一 CLI v1.0
一个命令入口走全部能力：
  longhun version
  longhun dna stamp --module xxx
  longhun audit file.py          # 15条国产替代扫描
  longhun audit summary          # 三色审计汇总
  longhun tricolor audit <module> <event> <color>
  longhun cnsh run <file.cnsh>

DNA: #龍芯⚡️2026-08-31-LONGHUN-CLI-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import argparse
import json
import sys
from . import __version__, __dna__
from . import dna as dna_mod
from . import tricolor as tricolor_mod
from . import evaluator as evaluator_mod
from . import cnsh as cnsh_mod


def cmd_version(args):
    print(json.dumps({
        "name": "longhun",
        "version": __version__,
        "dna": __dna__,
        "author": "诸葛鑫 | UID9622 · 龍芯北辰",
        "license": "MulanPSL v2",
    }, indent=2, ensure_ascii=False))


def cmd_dna(args):
    stamp = dna_mod.dna_stamp(args.module, args.version)
    if args.json:
        print(json.dumps(stamp, indent=2, ensure_ascii=False))


def cmd_audit(args):
    if args.target == "summary":
        counts = tricolor_mod.summary()
        print(json.dumps({"summary": counts,
                          "tricolor": "🔴" if counts["🔴"] else
                                      ("🟡" if counts["🟡"] else "🟢")},
                         indent=2, ensure_ascii=False))
        return
    result = evaluator_mod.scan_file(args.target)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_tricolor(args):
    if args.action == "audit":
        dna = tricolor_mod.audit(args.module, args.event, args.color,
                                 json.loads(args.detail or "{}"))
        print(f"✅ 已记录审计日志 · DNA: {dna}")
    elif args.action == "summary":
        counts = tricolor_mod.summary(args.module)
        print(json.dumps(counts, indent=2, ensure_ascii=False))


def cmd_cnsh(args):
    result = cnsh_mod.run_cnsh(args.file, use_code=args.code)
    if not result.get("ok"):
        print(f"❌ {result.get('error', '运行失败')}", file=sys.stderr)
        sys.exit(1)
    if result.get("stdout"):
        print(result["stdout"])
    if result.get("stderr"):
        print(result["stderr"], file=sys.stderr)


def build_parser():
    p = argparse.ArgumentParser(
        prog="longhun",
        description="🐉 龍魂主权技术栈统一 SDK · DNA追溯 + 三色审计 + 15条国产替代规则 + CNSH桥")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("version", help="版本信息")

    dna_p = sub.add_parser("dna", help="DNA 追溯码")
    dna_s = dna_p.add_subparsers(dest="dna_cmd", required=True)
    stamp_p = dna_s.add_parser("stamp", help="生成 DNA 戳")
    stamp_p.add_argument("--module", default="SDK")
    stamp_p.add_argument("--version", default="1.0")
    stamp_p.add_argument("--json", action="store_true")

    audit_p = sub.add_parser("audit", help="15条国产替代规则评估")
    audit_p.add_argument("target", help="文件路径 或 summary")

    tricolor_p = sub.add_parser("tricolor", help="三色审计")
    tri_s = tricolor_p.add_subparsers(dest="tri_cmd", required=True)
    aud_p = tri_s.add_parser("audit", help="记录审计日志")
    aud_p.add_argument("module"); aud_p.add_argument("event")
    aud_p.add_argument("color", choices=["🟢", "🟡", "🔴"])
    aud_p.add_argument("--detail", default="{}")
    tri_s.add_parser("summary", help="审计汇总").add_argument("--module")

    cnsh_p = sub.add_parser("cnsh", help="CNSH 运行桥")
    cnsh_s = cnsh_p.add_subparsers(dest="cnsh_cmd", required=True)
    run_p = cnsh_s.add_parser("run", help="运行 CNSH")
    run_p.add_argument("file", help=".cnsh 文件路径")
    run_p.add_argument("--code", action="store_true", help="按内联代码处理")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    {
        "version": cmd_version,
        "dna": cmd_dna,
        "audit": cmd_audit,
        "tricolor": cmd_tricolor,
        "cnsh": cmd_cnsh,
    }[args.command](args)


if __name__ == "__main__":
    main()
