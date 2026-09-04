# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · DNA 干支生成器（沙箱代算版 · 🟡代算）
规范: #龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}
铁律: 干支四柱禁止手写；卦名以本地 bin/lh_dna_generator.py 为准。
     本地生成器不可达时由本模块等效代算，输出标 🟡。
"""
from datetime import date

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
# 2026 年节气日近似表（公历月 -> 节气日）
JIEQI = {1: 5, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 8, 10: 8, 11: 7, 12: 7}
# 五虎遁：年干 -> 正月天干 index
WUHU = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}
# 六十四卦（文王序）
GUA64 = [
    "乾为天", "坤为地", "水雷屯", "山水蒙", "水天需", "天水讼", "地水师", "水地比",
    "风天小畜", "天泽履", "地天泰", "天地否", "天火同人", "火天大有", "地山谦", "雷地豫",
    "泽雷随", "山风蛊", "地泽临", "风地观", "火雷噬嗑", "山火贲", "山地剥", "地雷复",
    "天雷无妄", "山天大畜", "山雷颐", "泽风大过", "坎为水", "离为火", "泽山咸", "雷风恒",
    "天山遁", "雷天大壮", "火地晋", "地火明夷", "风火家人", "火泽睽", "水山蹇", "雷水解",
    "山泽损", "风雷益", "泽天夬", "天风姤", "泽地萃", "地风升", "泽水困", "水风井",
    "泽火革", "火风鼎", "震为雷", "艮为山", "风山渐", "雷泽归妹", "雷火丰", "火山旅",
    "巽为风", "兑为泽", "风水涣", "水泽节", "风泽中孚", "雷山小过", "水火既济", "火水未济",
]


def gz_year(y: int) -> str:
    return GAN[(y - 4) % 10] + ZHI[(y - 4) % 12]


def gz_month(d: date) -> str:
    """节气月：公历 m 月节气日后 = 节气第 (m-1) 月（2月立春=正月寅）"""
    y, m = d.year, d.month
    idx = m - 1 if d.day >= JIEQI[m] else m - 2
    if idx <= 0:
        idx += 12
        y -= 1
    tg = (WUHU[(y - 4) % 10] + idx - 1) % 10
    dz = (2 + idx - 1) % 12  # 正月起寅
    return GAN[tg] + ZHI[dz]


def gz_day(d: date) -> str:
    """锚点 2000-01-01 = 戊午（六十甲子 index 54），已用 1949-10-01=甲子 双锚复核"""
    idx = (54 + (d - date(2000, 1, 1)).days) % 60
    return GAN[idx % 10] + ZHI[idx % 12]


def gua_of_day(d: date) -> str:
    """🟡代算：日柱六十甲子序号 -> 六十四卦。正式口径以本地生成器为准"""
    idx = (54 + (d - date(2000, 1, 1)).days) % 60
    return GUA64[idx % 64]


def generate_dna(action: str, version: str = "v1.0", d: date = None) -> str:
    """生成新格式 DNA：#龍芯⚡️{年}·{月}·{日}·{卦}-{动作}-{版本}"""
    d = d or date.today()
    return f"#龍芯⚡️{gz_year(d.year)}·{gz_month(d)}·{gz_day(d)}·{gua_of_day(d)}-{action}-{version}"


if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "DNA-GEN"
    ver = sys.argv[2] if len(sys.argv) > 2 else "v1.0"
    print(generate_dna(action, ver))
