#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丁卯·丁未·䷗复-DNA-NOTION-REF-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# ============================================================
# 龍魂 DNA 对齐参考实现 v1.0（Notion 侧可用）
# ============================================================
# 本脚本是主引擎 bin/lh_dna_generator.py 的零依赖参考实现：
#   · 只用 Python 标准库（datetime / hashlib / json / argparse）
#   · 算法与主引擎逐字段一致（干支四柱·梅花易数起卦·SHA256哈希8·数字根）
#   · 直接复制到任意 Python3 环境即可运行，输出与龍魂系统完全一致
# 用途：让 Notion / 外部系统 / 人工核对，能算出与我们一样的 DNA。
#
# DNA v∞ 格式（与主引擎一致）：
#   #龍芯⚡️{年柱}·{月柱}·{日柱}·{时柱}·{卦符}{卦名}-{类别}-{动作}-{哈希8}
#   例: #龍芯⚡️丙午·丙申·丁卯·丁未·䷗复-DOC-创建-432f3aba
#
# 使用方法：
#   python3 lh_dna_ref_impl.py --title "标题" --category doc --action 创建
#   python3 lh_dna_ref_impl.py --title "标题" --category doc --action 创建 \
#       --date 2026-08-21 --hour 14 --json
#   python3 lh_dna_ref_impl.py --selftest      # 跑内置测试向量
# ============================================================

import argparse
import datetime
import hashlib
import json
import sys

# ------------------------------------------------------------
# 基表（与主引擎一致·焊死）
# ------------------------------------------------------------
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 节气月支简化节令日表（月, 日）→ 月支索引（寅=2 ... 丑=1，子=0）
# 小寒(1/6)=丑 立春(2/4)=寅 惊蛰(3/6)=卯 清明(4/5)=辰 立夏(5/6)=巳 芒种(6/6)=午
# 小暑(7/7)=未 立秋(8/7)=申 白露(9/8)=酉 寒露(10/8)=戌 立冬(11/7)=亥 大雪(12/7)=子
JIEQI = [(1, 6), (2, 4), (3, 6), (4, 5), (5, 6), (6, 6),
         (7, 7), (8, 7), (9, 8), (10, 8), (11, 7), (12, 7)]

# 通行本64卦八宫序（宫=上卦先天序: 1乾2兑3离4震5巽6坎7艮8坤；列=下卦序 乾兑离震巽坎艮坤）
GONG_TABLE = {
    1: [1, 43, 14, 34, 9, 5, 26, 11],      # 乾宫: 乾夬大有 大壮小畜需大畜泰
    2: [10, 58, 38, 54, 61, 60, 41, 19],   # 兑宫: 履兑睽归妹 中孚节损临
    3: [13, 49, 30, 55, 37, 63, 22, 36],   # 离宫: 同人革离丰 家人既济贲明夷 (CB-002: 第2位30→49泽火革·原30重复)
    4: [25, 17, 21, 51, 42, 3, 27, 24],    # 震宫: 无妄随噬嗑震 益屯颐复
    5: [44, 28, 50, 32, 57, 48, 18, 46],   # 巽宫: 姤大过鼎恒 巽井蛊升
    6: [6, 47, 64, 40, 59, 29, 4, 7],      # 坎宫: 讼困未济解 涣坎蒙师
    7: [33, 31, 56, 62, 53, 39, 52, 15],   # 艮宫: 遁咸旅小过 渐蹇艮谦
    8: [12, 45, 35, 16, 20, 8, 23, 2],     # 坤宫: 否萃晋豫 比剥坤 (CB-002: 第6位23→8水地比·原23重复)
}

# 64卦: 序号 → 卦名/义/相位/卦符（与主引擎 HEXAGRAM_DATA 一致）
HEXAGRAM_DATA = {
    1: {"name": "乾为天", "meaning": "刚健不息", "phase": "执行", "symbol": "䷀"},
    2: {"name": "坤为地", "meaning": "厚德载物", "phase": "观察", "symbol": "䷁"},
    3: {"name": "屯", "meaning": "初生艰难", "phase": "调整", "symbol": "䷂"},
    4: {"name": "蒙", "meaning": "启蒙发蒙", "phase": "观察", "symbol": "䷃"},
    5: {"name": "需", "meaning": "等待时机", "phase": "观察", "symbol": "䷄"},
    6: {"name": "讼", "meaning": "争讼纷争", "phase": "调整", "symbol": "䷅"},
    7: {"name": "师", "meaning": "统帅之师", "phase": "执行", "symbol": "䷆"},
    8: {"name": "比", "meaning": "亲和比附", "phase": "执行", "symbol": "䷇"},
    9: {"name": "小畜", "meaning": "小有积蓄", "phase": "调整", "symbol": "䷈"},
    10: {"name": "履", "meaning": "履行责任", "phase": "执行", "symbol": "䷉"},
    11: {"name": "泰", "meaning": "天地交泰", "phase": "执行", "symbol": "䷊"},
    12: {"name": "否", "meaning": "天地否塞", "phase": "观察", "symbol": "䷋"},
    13: {"name": "同人", "meaning": "志同道合", "phase": "执行", "symbol": "䷌"},
    14: {"name": "大有", "meaning": "大有收获", "phase": "执行", "symbol": "䷍"},
    15: {"name": "谦", "meaning": "谦逊有礼", "phase": "调整", "symbol": "䷎"},
    16: {"name": "豫", "meaning": "愉悦安乐", "phase": "执行", "symbol": "䷏"},
    17: {"name": "随", "meaning": "随顺而行", "phase": "执行", "symbol": "䷐"},
    18: {"name": "蛊", "meaning": "反腐革新", "phase": "调整", "symbol": "䷑"},
    19: {"name": "临", "meaning": "居高临下", "phase": "执行", "symbol": "䷒"},
    20: {"name": "观", "meaning": "观察审视", "phase": "观察", "symbol": "䷓"},
    21: {"name": "噬嗑", "meaning": "咬合决断", "phase": "执行", "symbol": "䷔"},
    22: {"name": "贲", "meaning": "装饰文饰", "phase": "调整", "symbol": "䷕"},
    23: {"name": "剥", "meaning": "剥落衰败", "phase": "观察", "symbol": "䷖"},
    24: {"name": "复", "meaning": "回复复归", "phase": "调整", "symbol": "䷗"},
    25: {"name": "无妄", "meaning": "不妄为", "phase": "观察", "symbol": "䷘"},
    26: {"name": "大畜", "meaning": "大积蓄", "phase": "调整", "symbol": "䷙"},
    27: {"name": "颐", "meaning": "颐养", "phase": "观察", "symbol": "䷚"},
    28: {"name": "大过", "meaning": "大过度", "phase": "调整", "symbol": "䷛"},
    29: {"name": "坎为水", "meaning": "险陷重重", "phase": "观察", "symbol": "䷜"},
    30: {"name": "离为火", "meaning": "依附光明", "phase": "执行", "symbol": "䷝"},
    31: {"name": "咸", "meaning": "感应", "phase": "执行", "symbol": "䷞"},
    32: {"name": "恒", "meaning": "恒久", "phase": "调整", "symbol": "䷟"},
    33: {"name": "遁", "meaning": "退避", "phase": "观察", "symbol": "䷠"},
    34: {"name": "大壮", "meaning": "大强壮", "phase": "执行", "symbol": "䷡"},
    35: {"name": "晋", "meaning": "前进", "phase": "执行", "symbol": "䷢"},
    36: {"name": "明夷", "meaning": "光明受伤", "phase": "观察", "symbol": "䷣"},
    37: {"name": "家人", "meaning": "家庭", "phase": "执行", "symbol": "䷤"},
    38: {"name": "睽", "meaning": "乖离", "phase": "调整", "symbol": "䷥"},
    39: {"name": "蹇", "meaning": "艰难", "phase": "观察", "symbol": "䷦"},
    40: {"name": "解", "meaning": "解除", "phase": "执行", "symbol": "䷧"},
    41: {"name": "损", "meaning": "减损", "phase": "调整", "symbol": "䷨"},
    42: {"name": "益", "meaning": "增益", "phase": "执行", "symbol": "䷩"},
    43: {"name": "夬", "meaning": "决断", "phase": "执行", "symbol": "䷪"},
    44: {"name": "姤", "meaning": "遭遇", "phase": "调整", "symbol": "䷫"},
    45: {"name": "萃", "meaning": "聚集", "phase": "执行", "symbol": "䷬"},
    46: {"name": "升", "meaning": "上升", "phase": "执行", "symbol": "䷭"},
    47: {"name": "困", "meaning": "困顿", "phase": "观察", "symbol": "䷮"},
    48: {"name": "井", "meaning": "水井", "phase": "调整", "symbol": "䷯"},
    49: {"name": "革", "meaning": "变革", "phase": "执行", "symbol": "䷰"},
    50: {"name": "鼎", "meaning": "鼎新", "phase": "执行", "symbol": "䷱"},
    51: {"name": "震为雷", "meaning": "震动警醒", "phase": "执行", "symbol": "䷲"},
    52: {"name": "艮为山", "meaning": "止于当止", "phase": "观察", "symbol": "䷳"},
    53: {"name": "渐", "meaning": "渐进", "phase": "调整", "symbol": "䷴"},
    54: {"name": "归妹", "meaning": "归嫁", "phase": "调整", "symbol": "䷵"},
    55: {"name": "丰", "meaning": "丰盛", "phase": "执行", "symbol": "䷶"},
    56: {"name": "旅", "meaning": "旅行", "phase": "执行", "symbol": "䷷"},
    57: {"name": "巽为风", "meaning": "柔顺渗透", "phase": "调整", "symbol": "䷸"},
    58: {"name": "兑为泽", "meaning": "喜悦交流", "phase": "执行", "symbol": "䷹"},
    59: {"name": "涣", "meaning": "涣散", "phase": "调整", "symbol": "䷺"},
    60: {"name": "节", "meaning": "节制", "phase": "调整", "symbol": "䷻"},
    61: {"name": "中孚", "meaning": "诚信", "phase": "执行", "symbol": "䷼"},
    62: {"name": "小过", "meaning": "小过度", "phase": "调整", "symbol": "䷽"},
    63: {"name": "既济", "meaning": "已完成", "phase": "观察", "symbol": "䷾"},
    64: {"name": "未济", "meaning": "未完成", "phase": "执行", "symbol": "䷿"},
}


# ------------------------------------------------------------
# 核心算法（与主引擎 get_ganzhi / get_hexagram 逐行一致）
# ------------------------------------------------------------

def _month_zhi(month: int, day: int) -> int:
    """节气月支（简化节令日表·±1天误差）
    返回: 月支索引（寅=2 ... 丑=1，子=0）"""
    zhi = 1  # 1/1~1/5 属上一年丑月
    for i, (m, d) in enumerate(JIEQI):
        if (month, day) >= (m, d):
            zhi = i + 1  # 小寒→1(丑) 立春→2(寅) ... 大雪→12(子)
        else:
            break
    return zhi % 12  # 子月=0


def get_ganzhi(now: datetime.datetime) -> dict:
    """计算天干地支四柱（CB-001修正版: 节气月+五虎遁+日柱偏移(0,10)+时柱五鼠遁）
    返回: {year, month, day, hour, raw}"""
    # 年柱: 公元4年=甲子年
    year_g = (now.year - 4) % 10
    year_z = (now.year - 4) % 12

    # 月柱: 节气月·五虎遁（寅月起丙(甲己)/庚(乙庚)/戊(丙辛)/壬(丁壬)/甲(戊癸)）
    month_z = _month_zhi(now.month, now.day)
    month_g = (year_g * 2 + month_z) % 10

    # 日柱: 以 1900-01-01=甲戌日为基准
    base_date = datetime.datetime(1900, 1, 1)
    days_diff = (now - base_date).days
    day_g = (days_diff + 0) % 10  # 1900-01-01=甲
    day_z = (days_diff + 10) % 12  # 1900-01-01=戌

    # 时柱: 五鼠遁（甲己还加甲）
    hour = now.hour
    shi_index = (hour + 1) // 2 % 12 if hour < 23 else 0
    shi_g = (day_g * 2 + shi_index) % 10

    return {
        "year": f"{TIAN_GAN[year_g]}{DI_ZHI[year_z]}",
        "month": f"{TIAN_GAN[month_g]}{DI_ZHI[month_z]}",
        "day": f"{TIAN_GAN[day_g]}{DI_ZHI[day_z]}",
        "hour": f"{TIAN_GAN[shi_g]}{DI_ZHI[shi_index]}",
        "raw": {
            "year_g": year_g, "year_z": year_z,
            "month_g": month_g, "month_z": month_z,
            "day_g": day_g, "day_z": day_z,
            "shi_g": shi_g, "shi_index": shi_index,
        }
    }


def get_hexagram(day_z: int, shi_index: int) -> int:
    """梅花易数: 上卦=日支, 下卦=时支 → 64卦通行本序号（宫位表映射）"""
    upper = (day_z % 8) + 1  # 上卦先天序 1乾2兑3离4震5巽6坎7艮8坤
    lower = (shi_index % 8) + 1
    return GONG_TABLE[upper][lower - 1]  # 1-64 通行本序号


def _digital_root(n: int) -> int:
    """数字根: 各位求和直到单位数"""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def digital_root(date_str: str) -> int:
    """从日期字符串计算数字根 (YYYY-MM-DD)"""
    return _digital_root(int(date_str.replace("-", "")))


def generate(title: str, category: str = "doc", action: str = "创建",
             date_str: str = None, hours: int = None) -> dict:
    """生成完整 DNA（与主引擎 generate() 字段一致）

    参数:
        title:    标题（哈希8 的输入源）
        category: 类别（如 doc/code/protocol，DNA 中大写）
        action:   动作（如 创建/修改，DNA 中大写）
        date_str: 日期 YYYY-MM-DD（缺省=今天）
        hours:    小时数 0-23（缺省=当前小时）
    """
    now = datetime.datetime.now()
    if date_str:
        now = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    if hours is not None:
        now = now.replace(hour=hours)

    ganzhi = get_ganzhi(now)
    h_num = get_hexagram(ganzhi["raw"]["day_z"], ganzhi["raw"]["shi_index"])
    hexa = HEXAGRAM_DATA[h_num]

    # 标题哈希8（与主引擎一致: sha256(title)[:8]）
    title_hash = hashlib.sha256(title.encode()).hexdigest()[:8]

    # DNA 字符串（与主引擎格式逐字一致）
    timetag = f"{ganzhi['year']}·{ganzhi['month']}·{ganzhi['day']}·{ganzhi['hour']}·{hexa['symbol']}{hexa['name']}"
    dna_string = f"#龍芯⚡️{timetag}-{category.upper()}-{action.upper()}-{title_hash}"
    compact_dna = f"#龍芯⚡️{timetag}"

    dr = digital_root(now.strftime("%Y-%m-%d"))

    return {
        "dna_string": dna_string,
        "compact_dna": compact_dna,
        "ganzhi": ganzhi,
        "hexagram_num": h_num,
        "hexagram_name": hexa["name"],
        "hexagram_symbol": hexa["symbol"],
        "hexagram_phase": hexa["phase"],
        "hexagram_meaning": hexa["meaning"],
        "title_hash": title_hash,
        "category": category,
        "action": action,
        "digital_root": dr,
        "is_369": dr in (3, 6, 9),
        "timestamp": now.isoformat(),
    }


# ------------------------------------------------------------
# 自测: 内置测试向量（来自主引擎实测输出）
# ------------------------------------------------------------
SELFTEST_CASES = [
    # (date_str, hours, title, category, action, 期望DNA)
    ("2026-08-21", 14, "Notion DNA 对齐测试", "doc", "创建",
     "#龍芯⚡️丙午·丙申·丁卯·丁未·䷗复-DOC-创建-432f3aba"),
    ("2024-02-10", 12, "甲辰日验证", "test", "验证",
     "#龍芯⚡️甲辰·丙寅·甲辰·庚午·䷑蛊-TEST-验证-3b68ab0e"),
    ("2026-08-12", 9, "戊午日验证", "test", "验证",
     "#龍芯⚡️丙午·丙申·戊午·丁巳·䷦蹇-TEST-验证-5de93687"),
    ("1900-01-01", 0, "基准日", "test", "基准",
     "#龍芯⚡️庚子·丁丑·甲戌·甲子·䷌同人-TEST-基准-75d6035e"),
    ("2026-01-01", 23, "子时边界", "test", "边界",
     "#龍芯⚡️丙午·己丑·乙亥·丙子·䷘无妄-TEST-边界-4728abb7"),
    ("2026-12-31", 23, "年末边界", "test", "边界",
     "#龍芯⚡️丙午·戊子·己卯·甲子·䷘无妄-TEST-边界-9f46bfbe"),
]


def selftest() -> int:
    """运行内置测试向量，全部通过返回 0"""
    fails = 0
    for ds, h, t, c, a, expect in SELFTEST_CASES:
        got = generate(title=t, category=c, action=a, date_str=ds, hours=h)["dna_string"]
        ok = "✅" if got == expect else "❌"
        if got != expect:
            fails += 1
        print(f"{ok} {ds} {h}时 {t!r}\n    期望: {expect}\n    实得: {got}")
    print(f"\n自测结果: {len(SELFTEST_CASES) - fails}/{len(SELFTEST_CASES)} 通过")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂 DNA 对齐参考实现 v1.0")
    ap.add_argument("--title", default="龍魂系统", help="标题（哈希8 输入源）")
    ap.add_argument("--category", default="doc", help="类别（DNA 中大写）")
    ap.add_argument("--action", default="创建", help="动作（DNA 中大写）")
    ap.add_argument("--date", default=None, help="日期 YYYY-MM-DD（缺省=今天）")
    ap.add_argument("--hour", type=int, default=None, help="小时 0-23（缺省=当前）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--selftest", action="store_true", help="跑内置测试向量")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    payload = generate(title=args.title, category=args.category, action=args.action,
                       date_str=args.date, hours=args.hour)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["dna_string"])
        print(f"紧凑: {payload['compact_dna']}")
        print(f"四柱: {payload['ganzhi']['year']}·{payload['ganzhi']['month']}·"
              f"{payload['ganzhi']['day']}·{payload['ganzhi']['hour']}")
        print(f"卦象: {payload['hexagram_symbol']}{payload['hexagram_name']} "
              f"(#{payload['hexagram_num']}·{payload['hexagram_phase']})")
        print(f"哈希: {payload['title_hash']} | 数字根: {payload['digital_root']} "
              f"{'⚡369' if payload['is_369'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
