"""
龍魂五行计算器 v4.0 · 命令行入口

用法（默认示例甲子丙午庚申壬戌）：
  python -m modules.wuxing

完整指定：
  python -m modules.wuxing --nian-tg 甲 --nian-dz 子 --yue-tg 丙 --yue-dz 午 \\
                           --ri-tg 庚 --ri-dz 申 --shi-tg 壬 --shi-dz 戌

输出到文件：
  python -m modules.wuxing -o out/flow_node.json

DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from .core import 龍魂五行完整计算
from .node import 生成节点


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="longhun-wuxing",
        description="龍魂五行计算器 v4.0 · 输入八字四柱，输出 Node JSON + H 对冲指数",
        epilog="DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622",
    )
    # 四柱参数：用 ASCII dest 避免部分 shell 不兼容中文参数名
    defaults = [
        ("--nian-tg",  "nian_tg",  "甲", "年柱天干"),
        ("--nian-dz",  "nian_dz",  "子", "年柱地支"),
        ("--yue-tg",   "yue_tg",   "丙", "月柱天干"),
        ("--yue-dz",   "yue_dz",   "午", "月柱地支"),
        ("--ri-tg",    "ri_tg",    "庚", "日柱天干"),
        ("--ri-dz",    "ri_dz",    "申", "日柱地支"),
        ("--shi-tg",   "shi_tg",   "壬", "时柱天干"),
        ("--shi-dz",   "shi_dz",   "戌", "时柱地支"),
    ]
    for flag, dest, default, help_txt in defaults:
        p.add_argument(flag, dest=dest, default=default, metavar="干支",
                       help=f"{help_txt}（默认: {default}）")
    p.add_argument("--output", "-o", default=None, metavar="FILE",
                   help="输出 JSON 文件路径（不指定则打印到 stdout）")
    p.add_argument("--compact", action="store_true", default=False,
                   help="紧凑 JSON 输出（默认美化）")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # 核心计算
    结果 = 龍魂五行完整计算(
        年天干=args.nian_tg, 年地支=args.nian_dz,
        月天干=args.yue_tg,  月地支=args.yue_dz,
        日天干=args.ri_tg,   日地支=args.ri_dz,
        时天干=args.shi_tg,  时地支=args.shi_dz,
    )

    # 追加流场节点
    八字 = (args.nian_tg + args.nian_dz + args.yue_tg + args.yue_dz +
             args.ri_tg  + args.ri_dz  + args.shi_tg + args.shi_dz)
    节点 = 生成节点(八字, title=f"{八字}·龍魂节点", raw_type="rule")
    结果["流场节点"] = 节点

    # 输出
    indent = None if args.compact else 2
    output_str = json.dumps(结果, ensure_ascii=False, indent=indent)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"✅ 已写入：{args.output}", file=sys.stderr)
    else:
        print(output_str)

    # 摘要到 stderr
    H     = 结果["对冲指数"]["对冲指数H"]
    三色  = 结果["对冲指数"]["三色"]
    dna   = 结果["DNA追溯"]
    print(f"\n🐉 龍魂五行计算完成", file=sys.stderr)
    print(f"   对冲指数 H = {H}  {三色}", file=sys.stderr)
    print(f"   DNA  = {dna}", file=sys.stderr)
    print(f"   Node = {节点['node_id']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
