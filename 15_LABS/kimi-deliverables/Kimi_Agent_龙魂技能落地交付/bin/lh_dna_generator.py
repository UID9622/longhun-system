#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂 · DNA 追溯码生成器 (rizhu v3.0 算法口径)
锚点验证:
  - 2000-01-01 = 戊午日 (sexagenary index 54)
  - 2024-01-01 = 甲子日 (sexagenary index 0)   ← 公开历法事实, 双锚点互验
月柱: 以节气换月 (简化锚点: 用近似节气日, 误差标🟡)
卦名: 日柱六十甲子序号 mod 64 → 通行本《周易》卦序 (确定式映射, 无随机)
禁手写干支 —— 一切干支以本脚本输出为准。
"""
import sys
from datetime import date, datetime, timedelta

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

# 通行本六十四卦序
GUA64 = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
    "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
    "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
    "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

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


def gua_of_day(day_idx: int) -> str:
    return GUA64[day_idx % 64]


def generate(dt: datetime, action: str = "GEN", version: str = "v1.0") -> str:
    d = dt.date()
    dg, didx = day_ganzhi(d)
    yg = year_ganzhi(d)
    mg = month_ganzhi(d)
    hg = hour_ganzhi(dt.hour, dg[0])
    gua = gua_of_day(didx)
    return f"#龍芯⚡️{yg}·{mg}·{dg}·{hg}时·䷞{gua}-{action}-{version}-UID9622"


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
    print(f"日期: {d} {dt.hour:02d}:{dt.minute:02d}")
    print(f"四柱: {year_ganzhi(d)} · {month_ganzhi(d)} · {dg} · {hour_ganzhi(dt.hour, dg[0])}时")
    print(f"卦名: {gua_of_day(didx)} (日序{didx} mod 64)")
    print(f"DNA:  {generate(dt, action, version)}")
