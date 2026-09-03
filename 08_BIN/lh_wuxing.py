#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
上位协议: 01_protocols/LH-WUXING-CALC-WELD-v4.0.md（唯一权威源）

龍魂·五行计算器CLI v4.0（焊死版） — 四柱干支→五行强度→链路分析→补益建议→对冲指数→翻译第五维
统一命令: lh wuxing 甲子 丙午 庚申 壬戌 | lh wuxing --year 2026
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lh_wuxing_core import 龍魂五行计算器  # noqa: E402

# 天干地支基本表（用于 --year 自动生成四柱）
天干表 = "甲乙丙丁戊己庚辛壬癸"
地支表 = "子丑寅卯辰巳午未申酉戌亥"


def _year_pillars(year: int) -> dict:
    """由公元年推四柱（简化：年月日时柱用公历近似）"""
    gz_y = 天干表[(year - 4) % 10] + 地支表[(year - 4) % 12]
    # 月柱以正月寅起，近似取该年立春后
    gz_m = 天干表[((year - 4) % 10 + 2) % 10] + "寅"
    # 日柱、时柱用固定参考（需完整历法，此处标记近似）
    return {
        "年柱": gz_y,
        "月柱": gz_m,
        "日柱": "庚申",
        "时柱": "壬戌",
        "备注": "年/月柱由公历近似推算，日/时柱需完整干支历（可手动指定8干支）",
    }


def main() -> None:
    p = argparse.ArgumentParser(prog="lh wuxing", description="五行计算器")
    p.add_argument("pillars", nargs="*", help="8个干支 如: 甲子 丙午 庚申 壬戌 (年干 年支 月干 月支 日干 日支 时干 时支)")
    p.add_argument("--year", type=int, metavar="Y", help="公历年份（自动近似推四柱）")
    p.add_argument("--json", action="store_true", help="JSON输出")
    args = p.parse_args()

    if args.year:
        p_ = _year_pillars(args.year)
        print(f"🐉 年份四柱(近似): {p_['年柱']} {p_['月柱']} {p_['日柱']} {p_['时柱']} · {p_['备注']}")
        args.pillars = [p_["年柱"][0], p_["年柱"][1], p_["月柱"][0], p_["月柱"][1],
                        p_["日柱"][0], p_["日柱"][1], p_["时柱"][0], p_["时柱"][1]]

    if len(args.pillars) == 8:
        年干, 年支, 月干, 月支, 日干, 日支, 时干, 时支 = args.pillars
    elif len(args.pillars) == 4:
        # 简写：年柱 月柱 日柱 时柱
        parts = []
        for c in args.pillars:
            parts.extend([c[0], c[1]])
        年干, 年支, 月干, 月支, 日干, 日支, 时干, 时支 = parts
    elif args.pillars:
        print("❌ 参数错误：需要4柱(简写)或8干支。示例: lh wuxing 甲子 丙午 庚申 壬戌")
        sys.exit(1)
    else:
        # 默认当前年
        年干, 年支, 月干, 月支, 日干, 日支, 时干, 时支 = "甲", "子", "丙", "午", "庚", "申", "壬", "戌"

    result = 龍魂五行计算器(年干, 年支, 月干, 月支, 日干, 日支, 时干, 时支)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"🐉 龍魂五行计算器 v4.0（焊死版）")
    print("=" * 56)
    print(f"四柱: {年干}{年支} {月干}{月支} {日干}{日支} {时干}{时支}")
    print(f"五行得分: {json.dumps(result['五行强度']['五行得分'], ensure_ascii=False)}")
    print(f"最强: {result['五行强度']['最强']} · 最弱: {result['五行强度']['最弱']}")
    print(f"均衡指数: {result['五行强度']['均衡指数']}")
    print(f"链路健康度: {result['链路分析']['链路健康度']}")
    print(f"对冲指数H: {result['对冲指数']['对冲指数H']} · 三色: {result['对冲指数']['三色']}")
    print(f"翻译第五维: {result['翻译引擎第五维']['状态']} → {result['翻译引擎第五维']['五行定位']} · {result['翻译引擎第五维']['翻译引擎贡献']}")
    print(f"补益建议: {json.dumps(result['补益建议'], ensure_ascii=False)}")
    print("=" * 56)
    print(f"DNA: {result['DNA追溯']}")


if __name__ == "__main__":
    main()
