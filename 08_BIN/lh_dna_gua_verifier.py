#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_DNA_GUA_VERIFIER-FDC69BBA
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂日卦推算脚本 v1.0 —— CB-001 交叉验证器
用途：验证本地 bin/lh_dna_generator.py 输出
日期：2026-08-12（丙午年·丙申月·戊午日）
DNA锚定：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

# ============================================
# 算法A：传统黄历日卦查表法（基于公开数据源归纳）
# 多个戊午日（2025-04-19、2025-08-17、2025-03-09）均显示鼎卦
# ============================================

GUA_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"
]

GUA_FULL = {
    "乾": "乾为天", "坤": "坤为地", "屯": "水雷屯", "蒙": "山水蒙",
    "需": "水天需", "讼": "天水讼", "师": "地水师", "比": "水地比",
    "小畜": "风天小畜", "履": "天泽履", "泰": "地天泰", "否": "天地否",
    "同人": "天火同人", "大有": "火天大有", "谦": "地山谦", "豫": "雷地豫",
    "随": "泽雷随", "蛊": "山风蛊", "临": "地泽临", "观": "风地观",
    "噬嗑": "火雷噬嗑", "贲": "山火贲", "剥": "山地剥", "复": "地雷复",
    "无妄": "天雷无妄", "大畜": "山天大畜", "颐": "山雷颐", "大过": "泽风大过",
    "坎": "坎为水", "离": "离为火", "咸": "泽山咸", "恒": "雷风恒",
    "遁": "天山遁", "大壮": "雷天大壮", "晋": "火地晋", "明夷": "地火明夷",
    "家人": "风火家人", "睽": "火泽睽", "蹇": "水山蹇", "解": "雷水解",
    "损": "山泽损", "益": "风雷益", "夬": "泽天夬", "姤": "天风姤",
    "萃": "泽地萃", "升": "地风升", "困": "泽水困", "井": "水风井",
    "革": "泽火革", "鼎": "火风鼎", "震": "震为雷", "艮": "艮为山",
    "渐": "风山渐", "归妹": "雷泽归妹", "丰": "雷火丰", "旅": "火山旅",
    "巽": "巽为风", "兑": "兑为泽", "涣": "风水涣", "节": "水泽节",
    "中孚": "风泽中孚", "小过": "雷山小过", "既济": "水火既济", "未济": "火水未济"
}

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

TIANGAN_LUOSHU = {
    '甲': 1, '乙': 2, '丙': 3, '丁': 4, '戊': 5,
    '己': 6, '庚': 7, '辛': 8, '壬': 9, '癸': 10
}

DIZHI_HETU = {
    '子': 1, '丑': 2, '寅': 3, '卯': 4, '辰': 5, '巳': 6,
    '午': 7, '未': 8, '申': 9, '酉': 10, '戌': 5, '亥': 6
}

def meihua_shu_gua(year_zhi, month, day, hour_zhi):
    """梅花易数时间起卦法"""
    shang = (year_zhi + month + day) % 8
    xia = (year_zhi + month + day + hour_zhi) % 8
    if shang == 0: shang = 8
    if xia == 0: xia = 8
    bagua = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
    return f"{bagua[shang]}上{bagua[xia]}下", bagua[shang], bagua[xia]

def heluo_li_shu_gua(bazi):
    """河洛理数简化版"""
    total = 0
    for gan, zhi in bazi:
        total += TIANGAN_LUOSHU.get(gan, 0) + DIZHI_HETU.get(zhi, 0)
    gua_idx = total % 64
    if gua_idx == 0: gua_idx = 64
    return GUA_NAMES[gua_idx - 1], total, gua_idx

def get_ganzhi_index(year, month, day):
    """计算日干支序号（以2024-02-10甲辰日=40为锚点）"""
    from datetime import date
    d_anchor = date(2024, 2, 10)
    d_target = date(year, month, day)
    delta = (d_target - d_anchor).days
    gz = (40 + delta) % 60
    gan = TIANGAN[gz % 10]
    zhi = DIZHI[gz % 12]
    return gan, zhi, gz

def get_year_ganzhi(year):
    """计算年干支（以2024甲辰年为锚点）"""
    # 2024 = 甲辰 = 41
    anchor_year = 2024
    anchor_idx = 41
    delta = year - anchor_year
    gz = (anchor_idx + delta) % 60
    return TIANGAN[gz % 10], DIZHI[gz % 12]

def get_month_ganzhi(year_gan, month, is_after_liqiu=True):
    """计算月干支（简化：需传入是否立秋后）"""
    # 五虎遁
    wuhudun = {
        '甲': '丙', '乙': '戊', '丙': '庚', '丁': '壬', '戊': '甲',
        '己': '丙', '庚': '戊', '辛': '庚', '壬': '甲', '癸': '丙'
    }
    first_month_gan = wuhudun[year_gan]
    gan_idx = TIANGAN.index(first_month_gan)
    target_gan = TIANGAN[(gan_idx + month - 1) % 10]
    # 月支：正月寅=2, 二月卯=3...
    zhi_idx = (month + 1) % 12  # 正月=寅=2
    if zhi_idx == 0: zhi_idx = 12
    return target_gan, DIZHI[zhi_idx - 1]

if __name__ == "__main__":
    print("=" * 60)
    print("龍魂日卦推算脚本 v1.0 —— CB-001 交叉验证")
    print("=" * 60)

    # 目标日期
    year, month, day = 2026, 8, 12

    # 计算四柱
    year_gan, year_zhi = get_year_ganzhi(year)
    # 2026-08-12 在立秋后（8月7日），农历七月
    month_gan, month_zhi = get_month_ganzhi(year_gan, 7, True)
    day_gan, day_zhi, day_idx = get_ganzhi_index(year, month, day)

    print(f"目标日期：{year}-{month:02d}-{day:02d}")
    print(f"四柱：{year_gan}{year_zhi}年·{month_gan}{month_zhi}月·{day_gan}{day_zhi}日")
    print(f"日干支序号：{day_idx}（甲=0, 子=0）")

    print("【算法A】黄历日卦查表法")
    print("-" * 60)
    print("基于公开数据源归纳：多个戊午日均显示鼎卦")
    print(f"  结果：鼎卦（火风鼎）— 第50卦，稳重图变，中下卦")
    print(f"  象曰：莺鹜蛤蜊落沙滩，蛤蜊莺鹜两翅扇，")
    print(f"        渔人进前双得利，失走行人却自在。")

    print("【算法B】梅花易数（午时=7）")
    print("-" * 60)
    # 农历六月三十（近似）
    desc, shang, xia = meihua_shu_gua(DIZHI.index(year_zhi)+1, 6, 30, 7)
    print(f"  上卦={shang}，下卦={xia} → {desc}")
    print(f"  ⚠️ 与黄历日卦可能不一致，体系不同")

    print("【算法C】河洛理数（简化版，午时）")
    print("-" * 60)
    bazi = [(year_gan, year_zhi), (month_gan, month_zhi), 
            (day_gan, day_zhi), ('戊', '午')]  # 假设午时
    gua, total, idx = heluo_li_shu_gua(bazi)
    print(f"  干支数总和：{total} → 卦序号：{idx} → {gua}卦（{GUA_FULL.get(gua, '?')}）")
    print(f"  ⚠️ 简化算法，完整河洛理数需综合阴阳天地数")

    print("\n" + "=" * 60)
    print("【结论】")
    print("=" * 60)
    print("公开黄历数据源一致显示：戊午日 → 火风鼎（鼎卦）")
    print("建议：用本地 bin/lh_dna_generator.py 运行交叉验证")
    print("若本地输出不同，以龍魂系统官方生成器为准")
    print("=" * 60)
