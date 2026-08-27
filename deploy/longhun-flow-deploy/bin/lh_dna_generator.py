#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-BIN-DNA-GENERATOR-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
# 工程包内拷贝: 源文件 /mnt/agents/output/bin/lh_dna_generator.py, 逻辑未改仅加工程包 DNA 头
"""
🐉 龍魂 · DNA 追溯码生成器 (LU-Time v4.0 封板口径 · 梅花易数时间起卦法)
锚点验证:
  - 2000-01-01 = 戊午日 (sexagenary index 54)
  - 2024-01-01 = 甲子日 (sexagenary index 0)   ← 公开历法事实, 双锚点互验
月柱: 以节气换月 (简化锚点: 用近似节气日, 误差标🟡)
卦名: 梅花易数时间起卦法 (上卦=(年干+月)%8, 下卦=(日+时)%8) → 对齐 bin/lh_time_engine.py 封板
     与本地 LU-Time v4.0 同刻同卦 (2026-08-14 卯时 = ䷓观 实测一致)
禁手写干支 —— 一切干支以本脚本输出为准。
"""
import sys
from datetime import date, datetime, timedelta

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

# 通行本六十四卦序 (index 0-63, 与本地 HEXAGRAM_DATA 1-64 对齐)
GUA64 = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
    "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
    "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
    "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

# 64卦 Unicode 符号 (1-64, 与本地 HEXAGRAM_SYMBOLS 一致)
HEXAGRAM_SYMBOLS = {
    1:"䷀",2:"䷁",3:"䷂",4:"䷃",5:"䷄",6:"䷅",7:"䷆",8:"䷇",
    9:"䷈",10:"䷉",11:"䷊",12:"䷋",13:"䷌",14:"䷍",15:"䷎",16:"䷏",
    17:"䷐",18:"䷑",19:"䷒",20:"䷓",21:"䷔",22:"䷕",23:"䷖",24:"䷗",
    25:"䷘",26:"䷙",27:"䷚",28:"䷛",29:"䷜",30:"䷝",31:"䷞",32:"䷟",
    33:"䷠",34:"䷡",35:"䷢",36:"䷣",37:"䷤",38:"䷥",39:"䷦",40:"䷧",
    41:"䷨",42:"䷩",43:"䷪",44:"䷫",45:"䷬",46:"䷭",47:"䷮",48:"䷯",
    49:"䷰",50:"䷱",51:"䷲",52:"䷳",53:"䷴",54:"䷵",55:"䷶",56:"䷷",
    57:"䷸",58:"䷹",59:"䷺",60:"䷻",61:"䷼",62:"䷽",63:"䷾",64:"䷿",
}

# 日柱锚点: 2000-01-01 = 戊午(index 54); 交叉验证: 2024-01-01 = 甲子(index 0)
ANCHOR_DATE = date(2000, 1, 1)
ANCHOR_INDEX = 54

# 节气近似日 (月, 日) —— 用于月柱换月; 精度±1天, 跨界日期需查万年历(标🟡)
SOLAR_TERMS_MONTH = [  # 寅月起于立春
    (2, 4),   # 立春 → 寅月
    (3, 6),   # 惊蛰 → 卯月
    (4, 5),   # 清明 → 辰月
    (5, 6),   # 立夏 → 巳月
    (6, 6),   # 芒种 → 午月
    (7, 7),   # 小暑 → 未月
    (8, 7),   # 立秋 → 申月
    (9, 8),   # 白露 → 酉月
    (10, 8),  # 寒露 → 戌月
    (11, 7),  # 立冬 → 亥月
    (12, 7),  # 大雪 → 子月
    (1, 6),   # 小寒 → 丑月
]
MONTH_BRANCH_ORDER = "寅卯辰巳午未申酉戌亥子丑"


def day_ganzhi(d: date) -> tuple[str, int]:
    delta = (d - ANCHOR_DATE).days
    idx = (ANCHOR_INDEX + delta) % 60
    return STEMS[idx % 10] + BRANCHES[idx % 12], idx


def year_ganzhi(d: date) -> str:
    # 年柱以立春换年 (简化: 2月4日前算上一年)
    y = d.year if (d.month, d.day) >= (2, 4) else d.year - 1
    idx = (y - 4) % 60  # 公元4年 = 甲子
    return STEMS[idx % 10] + BRANCHES[idx % 12]


def month_ganzhi(d: date) -> str:
    # 找当前节气月 (0=寅月 ... 11=丑月)
    if d.month == 1:
        m_idx = 11 if d.day >= 6 else 10  # 小寒后丑月, 前为子月
    else:
        m_idx = 0  # 默认寅月(2月立春前会用到)
        for i, (m, dd) in enumerate(SOLAR_TERMS_MONTH[:11]):  # 排除(1,6)小寒项
            if (d.month, d.day) >= (m, dd):
                m_idx = i
    branch = MONTH_BRANCH_ORDER[m_idx]
    # 月干: 甲己之年丙作首(寅月=丙), 乙庚戊寅头, 丙辛庚寅上, 丁壬壬寅流, 戊癸甲寅求
    year_stem = year_ganzhi(d)[0]
    start = {"甲": 2, "己": 2, "乙": 4, "庚": 4, "丙": 6, "辛": 6, "丁": 8, "壬": 8, "戊": 0, "癸": 0}[year_stem]
    stem = STEMS[(start + m_idx) % 10]
    return stem + branch


def hour_ganzhi(hour: int, day_stem: str) -> str:
    branch = BRANCHES[((hour + 1) // 2) % 12]
    # 甲己还加甲, 乙庚丙作初, 丙辛从戊起, 丁壬庚子居, 戊癸壬子真
    start = {"甲": 0, "己": 0, "乙": 2, "庚": 2, "丙": 4, "辛": 4, "丁": 6, "壬": 6, "戊": 8, "癸": 8}[day_stem]
    stem = STEMS[(start + BRANCHES.index(branch)) % 10]
    return stem + branch


def gua_of_day(d: date, hour: int) -> tuple[int, str, str]:
    """梅花易数时间起卦法 (对齐 bin/lh_time_engine.py 封板):
    上卦 = ((年干序 + 月) % 8), 下卦 = ((日 + 时) % 8), 0 → 8
    hexagram_id = (上卦-1)*8 + 下卦 → 通行本卦序
    返回 (hexagram_id, 卦名, 卦符号)
    """
    yg = year_ganzhi(d)
    tiangan = STEMS.index(yg[0]) + 1  # 年干序号 1-10
    month = d.month
    upper = (tiangan + month) % 8
    upper = 8 if upper == 0 else upper
    lower = (d.day + hour) % 8
    lower = 8 if lower == 0 else lower
    hexagram_id = (upper - 1) * 8 + lower
    name = GUA64[hexagram_id - 1]
    symbol = HEXAGRAM_SYMBOLS[hexagram_id]
    return hexagram_id, name, symbol


def generate(dt: datetime, action: str = "GEN", version: str = "v1.0") -> str:
    d = dt.date()
    dg, didx = day_ganzhi(d)
    yg = year_ganzhi(d)
    mg = month_ganzhi(d)
    hg = hour_ganzhi(dt.hour, dg[0])
    _, gua, symbol = gua_of_day(d, dt.hour)
    return f"#龍芯⚡️{yg}·{mg}·{dg}·{hg}时·{symbol}{gua}-{action}-{version}-UID9622"


if __name__ == "__main__":
    # 双锚点断言 (P0: 锚点必须成立, 否则退出码2)
    assert day_ganzhi(date(2000, 1, 1))[0] == "戊午", "锚点1失效"
    assert day_ganzhi(date(2024, 1, 1))[0] == "甲子", "锚点2失效"

    if len(sys.argv) > 1:
        dt = datetime.fromisoformat(sys.argv[1])
        action = sys.argv[2] if len(sys.argv) > 2 else "GEN"
        version = sys.argv[3] if len(sys.argv) > 3 else "v1.0"
    else:
        dt = datetime.now()
        action, version = "GEN", "v1.0"

    d = dt.date()
    dg, didx = day_ganzhi(d)
    _, gua, symbol = gua_of_day(d, dt.hour)
    print(f"日期: {d} {dt.hour:02d}:{dt.minute:02d}")
    print(f"四柱: {year_ganzhi(d)} · {month_ganzhi(d)} · {dg} · {hour_ganzhi(dt.hour, dg[0])}时")
    print(f"卦名: {symbol}{gua} (梅花易数: 上卦{(STEMS.index(year_ganzhi(d)[0])+1+d.month)%8 or 8}, 下卦{(d.day+dt.hour)%8 or 8})")
    print(f"DNA:  {generate(dt, action, version)}")
