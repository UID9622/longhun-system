#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·DNA追溯码生成引擎 v2.0
统一入口·全功能·自动化标注
DNA: #龍芯⚡️丙午·丙申·己酉·庚午·䷐随-DNA-GENERATOR-v2.0-AUTO-COMPLETE-7d3f1a2b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

v2.0 新增:
  - 五行判定（天干→五行映射）
  - 数字根计算（3/6/9不动点）
  - ROOT_CARD 生成（完整数学根审计卡）
  - stats 子命令（按日/月/类型统计）
  - info 子命令（DNA详情+ROOT_CARD）
  - validate 子命令（格式校验）
  - search 子命令（注册表关键词搜索）
  - batch 子命令（CSV/JSON批量生成）
  - --output-format json/md
  - --template 抬头模板联动（1-6）
  - API模式（import调用）

用法:
  python3 lh_dna_generator.py --title "示例标题" --category doc --action 写入 --actor UID9622
  python3 lh_dna_generator.py generate --title "xxx" --category code --action 创建 --actor P04
  python3 lh_dna_generator.py stats [--days 7]
  python3 lh_dna_generator.py search "关键词"
  python3 lh_dna_generator.py validate "#龍芯⚡️..."
  python3 lh_dna_generator.py info <dna_string>
  python3 lh_dna_generator.py batch --csv input.csv --output registry/
  python3 lh_dna_generator.py --template 4 --title "对话记录" --category persona
  python3 lh_dna_generator.py --output-format json --title "测试"
"""

import os
import sys
import json
import argparse
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 固定锚点（焊死·不可修改）
# ============================================================

ENGINE_VERSION = "v2.0"
DNA_ENGINE = "#龍芯⚡️丙午·丙申·己酉·庚午·䷐随-DNA-GENERATOR-v2.0-AUTO-COMPLETE"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
OUR_BASE = Path(__file__).resolve().parent.parent  # longhun-dna-generator/

# ============================================================
# 天干地支基表（焊死·梅花易数时卦法）
# ============================================================

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
SHI_CHEN = DI_ZHI  # 时辰与地支一一对应

# ============================================================
# 五行映射（焊死）
# 天干五行: 甲乙木·丙丁火·戊己土·庚辛金·壬癸水
# 地支五行: 寅卯木·巳午火·申酉金·亥子水·辰戌丑未土
# ============================================================

TIAN_GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

DI_ZHI_WUXING = {
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "亥": "水", "子": "水",
    "辰": "土", "戌": "土", "丑": "土", "未": "土",
}

# 五行生克关系
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}  # 生
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}  # 克

# 五行→三色倾向
WUXING_TENDENCY = {
    "木": "🟢",  # 木主生发·通
    "火": "🟡",  # 火主炎上·待核
    "土": "🟢",  # 土主承载·稳
    "金": "🔴",  # 金主肃杀·红线高
    "水": "🟡",  # 水主润下·待核
}

# ============================================================
# 八卦映射（完整64卦·梅花易数起卦法）
# ============================================================

TRIGRAM_MAP = {
    1: {"name": "乾", "element": "天", "symbol": "☰"},
    2: {"name": "兑", "element": "泽", "symbol": "☱"},
    3: {"name": "离", "element": "火", "symbol": "☲"},
    4: {"name": "震", "element": "雷", "symbol": "☳"},
    5: {"name": "巽", "element": "风", "symbol": "☴"},
    6: {"name": "坎", "element": "水", "symbol": "☵"},
    7: {"name": "艮", "element": "山", "symbol": "☶"},
    8: {"name": "坤", "element": "地", "symbol": "☷"},
}

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

# ============================================================
# 六套抬头模板索引
# ============================================================

TEMPLATE_INDEX = {
    1: {"name": "学术博弈论分析型", "emoji": "📊", "phase": "🟡", "use": "论文/建模/推演"},
    2: {"name": "工程落地执行型", "emoji": "🔧", "phase": "🟢", "use": "脚本/部署/API"},
    3: {"name": "协议/原则声明型", "emoji": "📜", "phase": "🟢", "use": "宪法/条款/政策"},
    4: {"name": "人格对话/协作记录型", "emoji": "💬", "phase": "🟢", "use": "对话/推演/辅导"},
    5: {"name": "复盘/总结型", "emoji": "📝", "phase": "🟡", "use": "回顾/改进/记错本"},
    6: {"name": "快速笔记/想法型", "emoji": "💡", "phase": "🟡", "use": "灵感/备忘/待整理"},
}

# 类型到模板的自动映射
CATEGORY_TEMPLATE_MAP = {
    "paper": 1, "academic": 1, "推演": 1, "博弈": 1,
    "code": 2, "script": 2, "deploy": 2, "api": 2, "工程": 2,
    "protocol": 3, "agreement": 3, "policy": 3, "协议": 3,
    "persona": 4, "dialogue": 4, "collab": 4, "对话": 4,
    "review": 5, "复盘": 5, "总结": 5,
    "note": 6, "idea": 6, "memo": 6, "笔记": 6,
}

# ============================================================
# 颜色
# ============================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def cprint(text: str, color: str = Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")


# ============================================================
# 核心: 时间工具
# ============================================================

def _month_zhi(month: int, day: int) -> int:
    """节气月支（简化节令日表·±1天误差）· CB-001修正: 原公历月简化 8月=酉，标准应为申
    返回: 月支索引（寅=2 ... 丑=1）"""
    JIEQI = [(1, 6), (2, 4), (3, 6), (4, 5), (5, 6), (6, 6),
             (7, 7), (8, 7), (9, 8), (10, 8), (11, 7), (12, 7)]
    # 节令日 → 月支: 小寒(1/6)=丑(1) 立春(2/4)=寅(2) 惊蛰(3/6)=卯(3) ... 大雪(12/7)=子(0)
    zhi = 1  # 1/1~1/5 属上一年丑月
    for i, (m, d) in enumerate(JIEQI):
        if (month, day) >= (m, d):
            zhi = i + 1  # 小寒→1(丑) 立春→2(寅) ... 大雪→12(子)
        else:
            break
    return zhi % 12  # 子月=0


def get_ganzhi(now: datetime = None) -> Dict[str, str]:
    """计算天干地支四柱·梅花易数起卦
    CB-001修正(2026-08-12): ①月柱改节气月+五虎遁 ②日柱偏移(9,11)→(0,10) ③时柱等价五鼠遁"""
    if now is None:
        now = datetime.now()

    # 简化算法: 年干 = (year - 4) % 10, 年支 = (year - 4) % 12
    year_g = (now.year - 4) % 10
    year_z = (now.year - 4) % 12

    # 月柱（节气月·五虎遁 · CB-001修正: 原(month+1)%12 8月=酉错，标准=申）
    month_z = _month_zhi(now.month, now.day)
    month_g = (year_g * 2 + month_z) % 10  # 五虎遁: 寅月起丙(甲己)/庚(乙庚)/戊(丙辛)/壬(丁壬)/甲(戊癸)

    # 日柱（以1900-01-01=甲戌日为基准 · CB-001修正: 偏移(9,11)→(0,10)，原算法日柱错一天干+1地支）
    base_date = datetime(1900, 1, 1)
    days_diff = (now - base_date).days
    day_g = (days_diff + 0) % 10  # 1900-01-01=甲: 已验证 2024-02-10=甲辰日、2026-08-12=戊午日
    day_z = (days_diff + 10) % 12  # 1900-01-01=戌

    # 时辰
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


# 通行本64卦八宫序（宫=上卦先天序: 1乾2兑3离4震5巽6坎7艮8坤；列=下卦序 乾兑离震巽坎艮坤）
# CB-001修正: 原 (upper-1)*8+lower 非通行本序号（如坤上坤下原算64=未济，实际应=坤#2）
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


def is_369_anchor(n: int) -> bool:
    """是否为369不动点"""
    return n in (3, 6, 9)


# ============================================================
# 核心: 五行判定
# ============================================================

@dataclass
class WuxingReport:
    """五行判定报告"""
    year_wuxing: str  # 年天干五行
    month_wuxing: str  # 月天干五行
    day_wuxing: str  # 日天干五行
    hour_wuxing: str  # 时天干五行
    dominant: str  # 主导五行（出现最多的）
    tendency: str  # 三色倾向
    sheng: List[str]  # 生什么
    ke: List[str]  # 克什么
    summary: str  # 一句话总结


def calc_wuxing(ganzhi: Dict) -> WuxingReport:
    """从干支四柱计算五行"""
    tg_year = ganzhi["year"][0]
    tg_month = ganzhi["month"][0]
    tg_day = ganzhi["day"][0]
    tg_hour = ganzhi["hour"][0]

    year_wx = TIAN_GAN_WUXING.get(tg_year, "?")
    month_wx = TIAN_GAN_WUXING.get(tg_month, "?")
    day_wx = TIAN_GAN_WUXING.get(tg_day, "?")
    hour_wx = TIAN_GAN_WUXING.get(tg_hour, "?")

    # 找主导五行
    wxs = [year_wx, month_wx, day_wx, hour_wx]
    wx_count = {}
    for w in wxs:
        wx_count[w] = wx_count.get(w, 0) + 1
    dominant = max(wx_count, key=wx_count.get)
    tendency = WUXING_TENDENCY.get(dominant, "🟡")

    sheng = WUXING_SHENG.get(dominant, "?")
    ke = WUXING_KE.get(dominant, "?")
    sheng_list = [sheng] if sheng != "?" else []
    ke_list = [ke] if ke != "?" else []

    summaries = {
        "木": "万物生发·通", "火": "炎上光明·待核",
        "土": "厚德载物·稳", "金": "肃杀决断·审",
        "水": "润下流动·观",
    }

    return WuxingReport(
        year_wuxing=year_wx, month_wuxing=month_wx,
        day_wuxing=day_wx, hour_wuxing=hour_wx,
        dominant=dominant, tendency=tendency,
        sheng=sheng_list, ke=ke_list,
        summary=summaries.get(dominant, "未知"),
    )


# ============================================================
# 核心: DNA生成
# ============================================================

@dataclass
class DNAPayload:
    """完整DNA载荷"""
    dna_string: str
    compact_dna: str  # 紧凑版 #龍芯⚡️xxx
    ganzhi: Dict
    hexagram_num: int
    hexagram_name: str
    hexagram_phase: str
    hexagram_symbol: str
    wuxing: WuxingReport
    root_card: Dict
    title_hash: str
    category: str
    action: str
    actor: str
    template_id: int  # 推荐抬头模板
    timestamp: str
    digital_root: int  # 数字根
    is_369: bool  # 是否369不动点


def generate(title: str, category: str, action: str, actor: str,
             date_str: str = None, hours: int = None) -> DNAPayload:
    """主入口: 生成完整DNA"""
    now = datetime.now()
    if date_str:
        now = datetime.strptime(date_str, "%Y-%m-%d")
    if hours is not None:
        now = now.replace(hour=hours % 24)

    # 干支四柱·64卦
    ganzhi = get_ganzhi(now)
    h_num = get_hexagram(ganzhi["raw"]["day_z"], ganzhi["raw"]["shi_index"])
    hexa = HEXAGRAM_DATA.get(h_num, HEXAGRAM_DATA[1])

    # 五行
    wuxing = calc_wuxing(ganzhi)

    # 数字根
    dr = digital_root(now.strftime("%Y-%m-%d"))

    # 标题哈希
    title_hash = hashlib.sha256(title.encode()).hexdigest()[:8]

    # DNA字符串
    timetag = f"{ganzhi['year']}·{ganzhi['month']}·{ganzhi['day']}·{ganzhi['hour']}·{hexa['symbol']}{hexa['name']}"
    dna_string = f"#龍芯⚡️{timetag}-{category.upper()}-{action.upper()}-{title_hash}"
    compact_dna = f"#龍芯⚡️{ganzhi['year']}·{ganzhi['month']}·{ganzhi['day']}·{ganzhi['hour']}·{hexa['symbol']}{hexa['name']}"

    # 推荐抬头模板
    template_id = CATEGORY_TEMPLATE_MAP.get(category.lower(), 2) if category else 2

    # ROOT_CARD
    root_card = {
        "dr": dr,
        "is_369": is_369_anchor(dr),
        "wuxing_dominant": wuxing.dominant,
        "wuxing_tendency": wuxing.tendency,
        "hexagram": f"{hexa['symbol']}{hexa['name']}",
        "hexagram_num": h_num,
        "phase": hexa["phase"],
        "title_hash": title_hash,
        "template_id": template_id,
    }

    return DNAPayload(
        dna_string=dna_string,
        compact_dna=compact_dna,
        ganzhi=ganzhi,
        hexagram_num=h_num,
        hexagram_name=hexa["name"],
        hexagram_phase=hexa["phase"],
        hexagram_symbol=hexa["symbol"],
        wuxing=wuxing,
        root_card=root_card,
        title_hash=title_hash,
        category=category,
        action=action,
        actor=actor,
        template_id=template_id,
        timestamp=now.isoformat(),
        digital_root=dr,
        is_369=is_369_anchor(dr),
    )


# ============================================================
# 子命令: info — 解析已有DNA
# ============================================================

def dna_info(dna_string: str) -> Optional[Dict]:
    """解析DNA字符串，返回详情+ROOT_CARD"""
    import re
    # #龍芯⚡️丙午·丙申·己酉·庚午·䷐随-CODE-ACTION-HASH
    pattern = r"#龍芯⚡️(\w+·\w+·\w+)·(\w+)·(䷀|䷁|䷂|䷃|䷄|䷅|䷆|䷇|䷈|䷉|䷊|䷋|䷌|䷍|䷎|䷏|䷐|䷑|䷒|䷓|䷔|䷕|䷖|䷗|䷘|䷙|䷚|䷛|䷜|䷝|䷞|䷟|䷠|䷡|䷢|䷣|䷤|䷥|䷦|䷧|䷨|䷩|䷪|䷫|䷬|䷭|䷮|䷯|䷰|䷱|䷲|䷳|䷴|䷵|䷶|䷷|䷸|䷹|䷺|䷻|䷼|䷽|䷾|䷿)(\w+)-(\w+)-(\w+)-(\w+)"
    m = re.match(pattern, dna_string)
    if not m:
        return None

    timetag = m.group(1)
    shichen = m.group(2)
    hexa_char = m.group(3)
    hexa_name = m.group(4)
    category = m.group(5)
    action = m.group(6)
    title_hash = m.group(7)

    # 找卦象
    hex_num = None
    hex_data = None
    for k, v in HEXAGRAM_DATA.items():
        if v["symbol"] == hexa_char:
            hex_num = k
            hex_data = v
            break

    if not hex_data:
        return None

    # 解析干支到五行
    parts = timetag.split("·")
    wxs = []
    for part in parts:
        if len(part) >= 1 and part[0] in TIAN_GAN_WUXING:
            wxs.append(TIAN_GAN_WUXING[part[0]])

    dominant = max(set(wxs), key=wxs.count) if wxs else "?"
    tendency = WUXING_TENDENCY.get(dominant, "🟡")

    return {
        "dna_string": dna_string,
        "timetag": timetag,
        "shichen": shichen,
        "hexagram_symbol": hexa_char,
        "hexagram_name": hex_data["name"] if hex_data else hex_data.get("name","?"),
        "hexagram_num": hex_num,
        "hexagram_phase": hex_data["phase"] if hex_data else "?",
        "hexagram_meaning": hex_data["meaning"] if hex_data else "?",
        "category": category,
        "action": action,
        "title_hash": title_hash,
        "wuxing_dominant": dominant,
        "wuxing_tendency": tendency,
        "root_card": {
            "hexagram": f"{hexa_char}{hex_data['name'] if hex_data else '?'}",
            "wuxing_dominant": dominant,
            "wuxing_tendency": tendency,
            "phase": hex_data["phase"] if hex_data else "?",
            "action": action,
            "title_hash": title_hash,
        },
    }


# ============================================================
# 子命令: validate — 格式校验
# ============================================================

def validate_dna(dna_string: str) -> Dict:
    """验证DNA格式，返回错误列表"""
    errors = []
    warnings = []

    if not dna_string.startswith("#龍芯⚡️"):
        errors.append("缺少前缀 #龍芯⚡️")

    # 必须有六段: 前缀·干支四柱·时辰·卦名-类别-动作-哈希
    parts = dna_string.split("-")
    if len(parts) < 4:
        errors.append("DNA格式不完整（至少4段）")
        return {"valid": False, "errors": errors, "warnings": warnings}

    # 检查哈希长度
    last = parts[-1]
    if len(last) != 8:
        errors.append(f"哈希长度应为8，当前{len(last)}: {last}")

    # 检查是否有卦象符号
    hexa_found = False
    for h in HEXAGRAM_DATA.values():
        if h["symbol"] in dna_string:
            hexa_found = True
            break
    if not hexa_found:
        errors.append("未找到有效64卦符号")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ============================================================
# 子命令: search — 关键词搜索
# ============================================================

def search_registry(keyword: str, registry_dir: Path = None) -> List[Dict]:
    """搜索DNA注册表"""
    if registry_dir is None:
        registry_dir = OUR_BASE / "registry"

    results = []
    archive_dir = registry_dir / "archive"

    for dir_path in [registry_dir, archive_dir]:
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                # 兼容新旧格式
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = [v for k, v in data.items() if isinstance(v, dict)]
                else:
                    continue
                for item in items:
                    text = json.dumps(item, ensure_ascii=False).lower()
                    if keyword.lower() in text:
                        results.append({
                            "file": f.name,
                            "dna": item.get("dna_string", item.get("dna", "?")),
                            "title": item.get("title", item.get("dna", "?")),
                            "timestamp": item.get("timestamp", item.get("created_iso", "?")),
                        })
            except (json.JSONDecodeError, KeyError):
                continue

    return results


# ============================================================
# 子命令: stats — 统计视图
# ============================================================

def dna_stats(days: int = 7, registry_dir: Path = None) -> Dict:
    """DNA统计"""
    if registry_dir is None:
        registry_dir = OUR_BASE / "registry"

    now = datetime.now()
    cutoff = now - timedelta(days=days)

    total = 0
    types_count = {}
    actors_count = {}
    daily_count = {}
    by_day = {}

    for dir_path in [registry_dir, registry_dir / "archive"]:
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                # 兼容新旧格式
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = [v for k, v in data.items() if isinstance(v, dict)]
                else:
                    continue
                for item in items:
                    total += 1
                    cat = item.get("category", "other")
                    types_count[cat] = types_count.get(cat, 0) + 1
                    actor = item.get("actor", "unknown")
                    actors_count[actor] = actors_count.get(actor, 0) + 1

                    ts = item.get("timestamp", item.get("created_iso", ""))
                    if ts:
                        day = ts[:10]
                        by_day[day] = by_day.get(day, 0) + 1
                        try:
                            dt = datetime.fromisoformat(ts)
                            if dt >= cutoff:
                                daily_count[day] = daily_count.get(day, 0) + 1
                        except:
                            pass
            except:
                continue

    return {
        "total": total,
        "period_days": days,
        "recent_count": sum(daily_count.values()),
        "by_type": dict(sorted(types_count.items(), key=lambda x: -x[1])),
        "by_actor": dict(sorted(actors_count.items(), key=lambda x: -x[1])),
        "by_day": dict(sorted(by_day.items())),
        "daily": dict(sorted(daily_count.items())),
        "avg_per_day": round(total / max(1, len(by_day)), 1) if by_day else 0,
    }


# ============================================================
# 子命令: batch — 批量生成
# ============================================================

def batch_generate(csv_path: str = None, json_path: str = None,
                   entries: List[Dict] = None, output_dir: Path = None) -> List[DNAPayload]:
    """批量生成DNA"""
    payloads = []

    if csv_path:
        import csv
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                payloads.append(generate(
                    title=row.get("title", "untitled"),
                    category=row.get("category", "doc"),
                    action=row.get("action", "create"),
                    actor=row.get("actor", "UID9622"),
                ))
    elif json_path:
        with open(json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                payloads.append(generate(
                    title=item.get("title", "untitled"),
                    category=item.get("category", "doc"),
                    action=item.get("action", "create"),
                    actor=item.get("actor", "UID9622"),
                ))
    elif entries:
        for entry in entries:
            payloads.append(generate(
                title=entry.get("title", "untitled"),
                category=entry.get("category", "doc"),
                action=entry.get("action", "create"),
                actor=entry.get("actor", "UID9622"),
            ))

    return payloads


# ============================================================
# 输出格式化
# ============================================================

def format_output(payload: DNAPayload, fmt: str = "text") -> str:
    """格式化输出"""
    if fmt == "json":
        out = {
            "dna_string": payload.dna_string,
            "compact_dna": payload.compact_dna,
            "ganzhi": payload.ganzhi,
            "hexagram": {
                "number": payload.hexagram_num,
                "name": payload.hexagram_name,
                "phase": payload.hexagram_phase,
                "symbol": payload.hexagram_symbol,
            },
            "wuxing": {
                "year": payload.wuxing.year_wuxing,
                "month": payload.wuxing.month_wuxing,
                "day": payload.wuxing.day_wuxing,
                "hour": payload.wuxing.hour_wuxing,
                "dominant": payload.wuxing.dominant,
                "tendency": payload.wuxing.tendency,
                "summary": payload.wuxing.summary,
            },
            "digital_root": payload.digital_root,
            "is_369": payload.is_369,
            "root_card": payload.root_card,
            "category": payload.category,
            "action": payload.action,
            "actor": payload.actor,
            "template_id": payload.template_id,
            "timestamp": payload.timestamp,
        }
        return json.dumps(out, ensure_ascii=False, indent=2)
    elif fmt == "md":
        lines = []
        lines.append(f"# 龍魂DNA生成报告")
        lines.append("")
        lines.append(f"## 🧬 DNA")
        lines.append(f"```")
        lines.append(payload.dna_string)
        lines.append(f"```")
        lines.append("")
        lines.append(f"| 属性 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 干支 | {payload.ganzhi['year']}·{payload.ganzhi['month']}·{payload.ganzhi['day']}·{payload.ganzhi['hour']} |")
        lines.append(f"| 卦象 | {payload.hexagram_symbol}{payload.hexagram_name} (#{payload.hexagram_num}) |")
        lines.append(f"| 卦意 | {payload.hexagram_phase} |")
        lines.append(f"| 主导五行 | {payload.wuxing.dominant} |")
        lines.append(f"| 五行倾向 | {payload.wuxing.tendency} {payload.wuxing.summary} |")
        lines.append(f"| 数字根 | {payload.digital_root} {'⭐369不动点' if payload.is_369 else ''} |")
        lines.append(f"| 推荐模板 | #{payload.template_id} {TEMPLATE_INDEX.get(payload.template_id,{}).get('name','?')} |")
        lines.append("")
        lines.append("## 🃏 ROOT_CARD")
        lines.append("```")
        for k, v in payload.root_card.items():
            lines.append(f"{k}: {v}")
        lines.append("```")
        return "\n".join(lines)
    else:  # text (default)
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"🧬 {payload.dna_string}")
        lines.append(f"{'='*60}")
        lines.append(f"  干支: {payload.ganzhi['year']}·{payload.ganzhi['month']}·{payload.ganzhi['day']}·{payload.ganzhi['hour']}")
        lines.append(f"  卦象: {payload.hexagram_symbol}{payload.hexagram_name} #{payload.hexagram_num}")
        lines.append(f"  卦意: {payload.hexagram_phase}")
        lines.append(f"  五行: {payload.wuxing.dominant} {payload.wuxing.tendency} ({payload.wuxing.summary})")
        lines.append(f"  年{payload.wuxing.year_wuxing}月{payload.wuxing.month_wuxing}日{payload.wuxing.day_wuxing}时{payload.wuxing.hour_wuxing}")
        lines.append(f"  数字根: {payload.digital_root}{' ⭐369' if payload.is_369 else ''}")
        lines.append(f"  推荐模板: #{payload.template_id} {TEMPLATE_INDEX.get(payload.template_id,{}).get('name','?')}")
        lines.append(f"{'─'*60}")
        lines.append(f"  🃏 ROOT_CARD: dr={payload.root_card['dr']} wx={payload.wuxing.dominant} hexagram={payload.root_card['hexagram']} phase={payload.root_card['phase']}")
        lines.append(f"{'='*60}")
        return "\n".join(lines)


# ============================================================
# 注册表操作
# ============================================================

def save_to_registry(payload: DNAPayload, registry_dir: Path = None):
    """保存DNA到注册表"""
    if registry_dir is None:
        registry_dir = OUR_BASE / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = registry_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # 当前注册表
    registry_file = registry_dir / "dna_registry.json"
    registry = []
    if registry_file.exists():
        try:
            raw = json.loads(registry_file.read_text())
            if isinstance(raw, list):
                registry = raw
            elif isinstance(raw, dict):
                # 兼容旧格式（dict→list转换）
                registry = [v for k, v in raw.items() if isinstance(v, dict)]
        except json.JSONDecodeError:
            pass

    # 追加
    entry = {
        "dna_string": payload.dna_string,
        "compact_dna": payload.compact_dna,
        "ganzhi": {k: v for k, v in payload.ganzhi.items() if k != "raw"},
        "hexagram": payload.hexagram_name,
        "hexagram_num": payload.hexagram_num,
        "wuxing": payload.wuxing.dominant,
        "wuxing_tendency": payload.wuxing.tendency,
        "digital_root": payload.digital_root,
        "is_369": payload.is_369,
        "category": payload.category,
        "action": payload.action,
        "actor": payload.actor,
        "title": payload.dna_string.split("-")[1] if len(payload.dna_string.split("-")) > 1 else "",
        "timestamp": payload.timestamp,
    }
    registry.append(entry)
    registry_file.write_text(json.dumps(registry, ensure_ascii=False, indent=2))

    # 更新计数器
    counter_file = registry_dir / "counter.json"
    counter = {"total": 0, "daily": {}}
    if counter_file.exists():
        try:
            raw = json.loads(counter_file.read_text())
            # 兼容旧格式: {"2026-08-03": {"seq": 2}, "total": N}
            if isinstance(raw, dict):
                counter["total"] = raw.get("total", 0)
                counter["daily"] = raw.get("daily", {})
        except:
            pass
    counter["total"] = counter.get("total", 0) + 1
    today = datetime.now().strftime("%Y-%m-%d")
    counter.setdefault("daily", {})
    counter["daily"][today] = counter["daily"].get(today, 0) + 1
    counter_file.write_text(json.dumps(counter, ensure_ascii=False, indent=2))


# ============================================================
# 存档操作
# ============================================================

def archive_dna(dna_string: str, reason: str = "manual", registry_dir: Path = None):
    """将DNA从活跃注册表移至存档"""
    if registry_dir is None:
        registry_dir = OUR_BASE / "registry"

    registry_file = registry_dir / "dna_registry.json"
    if not registry_file.exists():
        return {"error": "注册表不存在"}

    raw = json.loads(registry_file.read_text())
    if isinstance(raw, list):
        registry = raw
    elif isinstance(raw, dict):
        registry = [v for k, v in raw.items() if isinstance(v, dict)]
    else:
        return {"error": "注册表格式不支持"}

    found = None
    new_registry = []
    for entry in registry:
        if entry.get("dna_string") == dna_string or entry.get("dna") == dna_string:
            found = entry
        else:
            new_registry.append(entry)

    if not found:
        return {"error": "DNA未找到"}

    # 写回新注册表
    registry_file.write_text(json.dumps(new_registry, ensure_ascii=False, indent=2))

    # 写存档
    archive_dir = registry_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    archive_file = archive_dir / f"{dna_string.split('-')[-1][:8]}.json"
    found["archived_at"] = datetime.now().isoformat()
    found["archive_reason"] = reason
    archive_file.write_text(json.dumps(found, ensure_ascii=False, indent=2))

    return {"archived": True, "file": str(archive_file)}


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"🐉 龍魂·DNA追溯码生成引擎 {ENGINE_VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --title "示例" --category doc --action 写入 --actor UID9622
  %(prog)s generate --title "示例" --category code --action 创建 --actor P04
  %(prog)s stats --days 7
  %(prog)s search "关键词"
  %(prog)s validate "#龍芯⚡️..."
  %(prog)s info "#龍芯⚡️..."
  %(prog)s batch --csv input.csv
  %(prog)s --template 4 --title "对话" --category persona
  %(prog)s --output-format json --title "测试"
  %(prog)s --version

DNA格式: #龍芯⚡️<干支四柱>·<时辰>·<卦><卦名>-<类别>-<动作>-<哈希8>
        """
    )

    # 主参数
    parser.add_argument("--title", "-t", type=str, help="标题（文件名/文档名/任务名）")
    parser.add_argument("--category", "-c", type=str, default="doc",
                        help="类别: doc/code/script/persona/paper/protocol/deploy/review/note/...")
    parser.add_argument("--action", "-a", type=str, default="创建",
                        help="动作: 创建/修改/归档/审查/部署/签章/...")
    parser.add_argument("--actor", type=str, default="UID9622",
                        help="执行者: UID9622/P04/P05/P01/...")

    # 输出选项
    parser.add_argument("--output-format", "-f", type=str, default="text",
                        choices=["text", "json", "md"], help="输出格式")
    parser.add_argument("--output-file", "-o", type=str, help="保存到文件")
    parser.add_argument("--registry-dir", type=str, help="注册表目录")

    # 模板联动
    parser.add_argument("--template", type=int, choices=[1, 2, 3, 4, 5, 6],
                        help="强制指定抬头模板（1-6），留空则自动匹配")

    # 时间覆盖（用于测试/历史日期）
    parser.add_argument("--date", type=str, help="覆盖日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--hour", type=int, help="覆盖时辰 (0-23)")

    # 子命令
    subparsers = parser.add_subparsers(dest="subcommand", help="子命令")

    # generate
    sp_gen = subparsers.add_parser("generate", help="生成DNA")
    sp_gen.add_argument("--title", "-t", type=str, required=True)
    sp_gen.add_argument("--category", "-c", type=str, default="doc")
    sp_gen.add_argument("--action", "-a", type=str, default="创建")
    sp_gen.add_argument("--actor", type=str, default="UID9622")
    sp_gen.add_argument("--format", "-f", choices=["text", "json", "md"], default="text")
    sp_gen.add_argument("--template", type=int, choices=[1, 2, 3, 4, 5, 6])

    # stats
    sp_stats = subparsers.add_parser("stats", help="DNA统计")
    sp_stats.add_argument("--days", "-d", type=int, default=7)

    # info
    sp_info = subparsers.add_parser("info", help="解析DNA详情")
    sp_info.add_argument("dna_string", type=str)

    # validate
    sp_val = subparsers.add_parser("validate", help="验证DNA格式")
    sp_val.add_argument("dna_string", type=str)

    # search
    sp_search = subparsers.add_parser("search", help="搜索注册表")
    sp_search.add_argument("keyword", type=str)

    # batch
    sp_batch = subparsers.add_parser("batch", help="批量生成")
    sp_batch.add_argument("--csv", type=str, help="CSV输入")
    sp_batch.add_argument("--json", type=str, help="JSON输入")

    # archive
    sp_archive = subparsers.add_parser("archive", help="归档DNA")
    sp_archive.add_argument("dna_string", type=str)
    sp_archive.add_argument("--reason", type=str, default="manual")

    # 版本
    parser.add_argument("--version", "-v", action="store_true", help="版本信息")

    args = parser.parse_args()

    # --version
    if args.version:
        cprint(f"🐉 龍魂·DNA追溯码生成引擎 {ENGINE_VERSION}", Colors.CYAN)
        cprint(f"   DNA: {DNA_ENGINE}", Colors.BLUE)
        cprint(f"   确认码: {CONFIRM_CODE}", Colors.YELLOW)
        cprint(f"   GPG: {GPG_KEY}", Colors.RED)
        cprint(f"   天干地支基表: 焊死·不可修改", Colors.GREEN)
        cprint(f"   64卦数据库: 完整·梅花易数起卦法", Colors.GREEN)
        cprint(f"   五行映射: 天干→五行·地支→五行·生克关系", Colors.GREEN)
        cprint(f"   数字根: 3/6/9不动点检测", Colors.GREEN)
        cprint(f"   模板联动: 6套抬头模板·自动类别匹配", Colors.GREEN)
        return

    # 确定registry目录
    registry_dir = Path(args.registry_dir) if args.registry_dir else OUR_BASE / "registry"

    # 子命令路由
    if args.subcommand == "stats":
        stats = dna_stats(args.days, registry_dir)
        cprint(f"\n📊 DNA统计 (最近{args.days}天)", Colors.CYAN)
        cprint(f"  总计: {stats['total']} 条", Colors.BOLD)
        cprint(f"  日均: {stats['avg_per_day']} 条", Colors.BOLD)
        cprint(f"\n  按类别:", Colors.YELLOW)
        for typ, count in list(stats["by_type"].items())[:10]:
            cprint(f"    {typ}: {count}", Colors.GREEN)
        cprint(f"\n  按执行者:", Colors.YELLOW)
        for actor, count in list(stats["by_actor"].items())[:10]:
            cprint(f"    {actor}: {count}", Colors.GREEN)
        return

    if args.subcommand == "info":
        result = dna_info(args.dna_string)
        if result:
            cprint(f"\n🧬 DNA详情", Colors.CYAN)
            for k, v in result.items():
                if k != "root_card":
                    cprint(f"  {k}: {v}", Colors.GREEN)
            cprint(f"\n🃏 ROOT_CARD", Colors.CYAN)
            for k, v in result.get("root_card", {}).items():
                cprint(f"  {k}: {v}", Colors.GREEN)
        else:
            cprint(f"❌ 无法解析DNA: {args.dna_string}", Colors.RED)
        return

    if args.subcommand == "validate":
        result = validate_dna(args.dna_string)
        if result["valid"]:
            cprint(f"✅ DNA格式有效", Colors.GREEN)
        else:
            cprint(f"❌ DNA格式无效", Colors.RED)
            for e in result["errors"]:
                cprint(f"  - {e}", Colors.RED)
        for w in result["warnings"]:
            cprint(f"  ⚠️ {w}", Colors.YELLOW)
        return

    if args.subcommand == "search":
        results = search_registry(args.keyword, registry_dir)
        if results:
            cprint(f"\n🔍 搜索 '{args.keyword}': {len(results)} 条结果", Colors.CYAN)
            for r in results:
                cprint(f"  📄 {r['file']}", Colors.GREEN)
                cprint(f"     {r['dna']}", Colors.BLUE)
                cprint(f"     标题: {r['title']} | 时间: {r['timestamp']}", Colors.YELLOW)
        else:
            cprint(f"🔍 无结果: '{args.keyword}'", Colors.YELLOW)
        return

    if args.subcommand == "batch":
        entries = []
        if args.csv:
            import csv
            with open(args.csv, 'r', encoding='utf-8') as f:
                entries = list(csv.DictReader(f))
        elif args.json:
            entries = json.loads(open(args.json, 'r', encoding='utf-8').read())

        payloads = batch_generate(entries=entries)
        cprint(f"\n📦 批量生成: {len(payloads)} 条DNA", Colors.CYAN)
        for i, p in enumerate(payloads):
            cprint(f"\n  [{i+1}] {p.dna_string}", Colors.GREEN)
            save_to_registry(p, registry_dir)
        return

    if args.subcommand == "archive":
        result = archive_dna(args.dna_string, args.reason, registry_dir)
        if "error" in result:
            cprint(f"❌ {result['error']}", Colors.RED)
        else:
            cprint(f"✅ 已归档: {result['file']}", Colors.GREEN)
        return

    # 默认: 生成DNA
    title = args.title
    if args.subcommand == "generate":
        title = args.title
        category = args.category
        action = args.action
        actor = args.actor
        fmt = args.format
        tmpl = args.template
    else:
        category = args.category
        action = args.action
        actor = args.actor
        fmt = args.output_format
        tmpl = args.template

    if not title:
        cprint("❌ 需要 --title", Colors.RED)
        parser.print_help()
        return

    # 模板覆盖
    if tmpl:
        pass  # 使用用户指定模板
    else:
        tmpl = CATEGORY_TEMPLATE_MAP.get(category.lower(), 2)

    payload = generate(
        title=title, category=category, action=action, actor=actor,
        date_str=args.date, hours=args.hour,
    )
    # 强制覆盖模板
    if tmpl:
        payload.template_id = tmpl
        payload.root_card["template_id"] = tmpl

    # 保存
    save_to_registry(payload, registry_dir)

    # 输出
    output = format_output(payload, fmt)
    if args.output_file:
        Path(args.output_file).write_text(output)
        cprint(f"✅ 已保存到 {args.output_file}", Colors.GREEN)
    else:
        print(output)

    return payload


# ============================================================
# API模式: import调用
# ============================================================

def quick_dna(title: str, category: str = "doc", action: str = "创建",
              actor: str = "UID9622") -> Dict:
    """API调用入口: 快速生成DNA并返回字典"""
    payload = generate(title=title, category=category, action=action, actor=actor)
    save_to_registry(payload)
    return {
        "dna_string": payload.dna_string,
        "compact_dna": payload.compact_dna,
        "template_id": payload.template_id,
        "root_card": payload.root_card,
        "wuxing": payload.wuxing.dominant,
        "digital_root": payload.digital_root,
    }


def embed_dna_in_file(filepath: str, title: str = None, category: str = "doc",
                      action: str = "创建", actor: str = "UID9622") -> str:
    """在文件头部嵌入DNA注释"""
    payload = generate(
        title=title or Path(filepath).stem,
        category=category, action=action, actor=actor,
    )
    dna_line = f"DNA: {payload.dna_string}\n"

    try:
        content = Path(filepath).read_text(encoding='utf-8')
        if "# " in content or "/*" in content:
            # 在第一个注释行后插入
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.strip().startswith(("# ", "/*", "#!/", "//")):
                    continue
                # 插入DNA
                lines.insert(i, dna_line.strip())
                break
            Path(filepath).write_text("\n".join(lines), encoding='utf-8')
        else:
            Path(filepath).write_text(dna_line + "\n" + content, encoding='utf-8')

        save_to_registry(payload)
        return payload.dna_string
    except Exception as e:
        return f"ERROR: {e}"


# ============================================================
# 自检
# ============================================================

def self_test():
    """自检: 生成100条DNA验证唯一性+频率"""
    payloads = []
    for i in range(100):
        p = generate(
            title=f"自检文件-{i:03d}",
            category=["doc", "code", "script", "persona", "paper"][i % 5],
            action=["创建", "修改", "归档", "审查"][i % 4],
            actor=["UID9622", "P04", "P01", "P05"][i % 4],
        )
        payloads.append(p)

    # 唯一性检查
    dnas = [p.dna_string for p in payloads]
    unique = set(dnas)
    unique_rate = len(unique) / len(dnas)

    # 哈希碰撞检查
    hashes = [p.title_hash for p in payloads]
    hash_collisions = len(hashes) - len(set(hashes))

    return {
        "total": len(payloads),
        "unique": len(unique),
        "unique_rate": unique_rate,
        "hash_collisions": hash_collisions,
        "passed": unique_rate == 1.0 and hash_collisions == 0,
        "wuxing_distribution": list({p.wuxing.dominant for p in payloads}),
    }


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        result = self_test()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["passed"] else 1)

    main()
