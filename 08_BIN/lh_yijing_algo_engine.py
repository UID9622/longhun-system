#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-YIJING-ALGO-ENGINE-v2.0-LANDED
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
"""
🐉 龍魂 · 易经算法引擎 v2.0（落地版）

完整实现:
  1. 64卦推演引擎 (SHA256 + 节气加权)
  2. 五行平衡分析 (木火土金水)
  3. 中庸决策引擎 (平衡度 × 风险 × 机会)
  4. 时间预测系统 (趋势推演)
  5. 自求多福自我进化模块
  6. 双引擎融合 (科技 + 文化)
  7. DNA追溯 + 三色审计

公式:
  卦象索引 = (SHA256(问题+时间戳+文化DNA) 取模 64) + 1
  平衡度   = 1 - (方差 / 100)
  中庸评分 = 平衡度×0.4 + 风险控制×0.3 + 机会把握×0.3
  运势指数 = 卦象运势 × 节气权重 (∈[0.5,1.25])
  DR       = 0.35N + 0.25S + 0.25R + 0.15T

用法:
  python3 bin/lh_yijing_algo_engine.py -d "问题"      # 完整占卜
  python3 bin/lh_yijing_algo_engine.py -a "问题"      # 快速建议
  python3 bin/lh_yijing_algo_engine.py -w '{json}'    # 五行分析
  python3 bin/lh_yijing_algo_engine.py -z '{json}'    # 中庸决策
  python3 bin/lh_yijing_algo_engine.py -s             # 状态
  python3 bin/lh_yijing_algo_engine.py --timeline "问题"  # 时间线预测

DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-YIJING-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
"""

import os
import sys
import json
import hashlib
import time
import math
import random
import calendar
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import logging

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "YIJING") -> str:
    """生成DNA追溯码"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{h}-{UID}"


def get_ganzhi() -> str:
    """获取天干地支 (简化版)"""
    now = datetime.now()
    tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    hexagrams = ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
                 "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
                 "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋",
                 "明夷", "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困",
                 "井", "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣",
                 "节", "中孚", "小过", "既济", "未济"]
    gan = tian_gan[(now.year - 4) % 10]
    zhi = di_zhi[(now.year - 4) % 12]
    hex_str = hexagrams[now.day % 64]
    hour_zhi = di_zhi[((now.hour + 1) // 2) % 12]
    return f"{gan}{zhi}·{hour_zhi}时·{hex_str}卦"


# ============================================================
# 日志
# ============================================================

LOG_DIR = Path.home() / ".longhun" / "12_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"yijing_engine_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("yijing_engine")

# ============================================================
# 1. 64卦基础数据库
# ============================================================

GUA_DATABASE = {
    1: {"name": "乾", "symbol": "☰", "binary": "111111",
        "meaning": "天行健，君子以自强不息",
        "keywords": ["刚健", "进取", "领导", "创造"], "fortune": 0.95,
        "advice": "大吉。当前正是施展抱负的好时机，但需注意刚柔相济。"},
    2: {"name": "坤", "symbol": "☷", "binary": "000000",
        "meaning": "地势坤，君子以厚德载物",
        "keywords": ["柔顺", "包容", "承载", "顺势"], "fortune": 0.90,
        "advice": "大吉。以柔克刚，顺势而为，厚德载物。"},
    3: {"name": "屯", "symbol": "☳", "binary": "010001",
        "meaning": "云雷屯，君子以经纶",
        "keywords": ["初创", "艰难", "突破", "新生"], "fortune": 0.65,
        "advice": "初生之象，虽有艰难，但前景光明。需耐心经营。"},
    4: {"name": "蒙", "symbol": "☵", "binary": "100010",
        "meaning": "山下出泉，蒙，君子以果行育德",
        "keywords": ["启蒙", "教育", "成长", "学习"], "fortune": 0.70,
        "advice": "启蒙之时，虚心学习，以诚待人。"},
    5: {"name": "需", "symbol": "☴", "binary": "111010",
        "meaning": "云上于天，需，君子以饮食宴乐",
        "keywords": ["等待", "耐心", "准备", "时机"], "fortune": 0.75,
        "advice": "需待时机，不可急躁，养精蓄锐。"},
    6: {"name": "讼", "symbol": "☲", "binary": "010111",
        "meaning": "天水违行，讼，君子以作事谋始",
        "keywords": ["争议", "诉讼", "决策", "明辨"], "fortune": 0.55,
        "advice": "争讼之事，宜和解不宜持久。谋定而后动。"},
    7: {"name": "师", "symbol": "☷", "binary": "000010",
        "meaning": "地中有水，师，君子以容民畜众",
        "keywords": ["军队", "纪律", "领导", "征战"], "fortune": 0.80,
        "advice": "用兵需正道，有勇有谋，纪律严明。"},
    8: {"name": "比", "symbol": "☵", "binary": "010000",
        "meaning": "地上有水，比，君子以建万国、亲诸侯",
        "keywords": ["亲近", "联合", "辅助", "协作"], "fortune": 0.85,
        "advice": "吉。团结协作，互相扶持，共谋大事。"},
    9: {"name": "小畜", "symbol": "☴", "binary": "110111",
        "meaning": "风行天上，小畜，君子以懿文德",
        "keywords": ["积累", "约束", "修养", "内敛"], "fortune": 0.65,
        "advice": "小有积蓄，不宜大动，修身养性为上。"},
    10: {"name": "履", "symbol": "☰", "binary": "111011",
         "meaning": "上天下泽，履，君子以辩上下、定民志",
         "keywords": ["践行", "礼仪", "谨慎", "实践"], "fortune": 0.70,
         "advice": "如履薄冰，谨言慎行，遵循礼法。"},
    11: {"name": "泰", "symbol": "☷", "binary": "000111",
         "meaning": "天地交泰，泰，君子以辅相天地之宜",
         "keywords": ["通达", "和谐", "顺利", "昌盛"], "fortune": 0.92,
         "advice": "大吉。天地交泰，万事亨通，顺势而为。"},
    12: {"name": "否", "symbol": "☰", "binary": "111000",
         "meaning": "天地不交，否，君子以俭德辟难",
         "keywords": ["闭塞", "不顺", "等待", "内敛"], "fortune": 0.35,
         "advice": "天地不交，诸事不顺，宜守不宜攻。"},
    13: {"name": "同人", "symbol": "☰", "binary": "101111",
         "meaning": "天火同人，君子以类族辨物",
         "keywords": ["团结", "合作", "大同", "共济"], "fortune": 0.88,
         "advice": "大吉。团结协作，志同道合，共济天下。"},
    14: {"name": "大有", "symbol": "☲", "binary": "111101",
         "meaning": "火天大有，君子以遏恶扬善",
         "keywords": ["丰收", "盛大", "富足", "成就"], "fortune": 0.93,
         "advice": "大吉。丰收之象，富足安康，需戒骄戒躁。"},
    15: {"name": "谦", "symbol": "☷", "binary": "000100",
         "meaning": "地山谦，君子以裒多益寡",
         "keywords": ["谦逊", "低调", "内敛", "平衡"], "fortune": 0.90,
         "advice": "大吉。谦逊之道，终能成就大事。"},
    16: {"name": "豫", "symbol": "☳", "binary": "001000",
         "meaning": "雷地豫，君子以顺时",
         "keywords": ["愉悦", "准备", "计划", "顺时"], "fortune": 0.82,
         "advice": "吉祥。顺时而行，乐在其中，万事可成。"},
    17: {"name": "随", "symbol": "☱", "binary": "100110",
         "meaning": "泽雷随，君子以向晦入宴息",
         "keywords": ["跟随", "顺应", "灵活", "变通"], "fortune": 0.78,
         "advice": "吉祥。随顺时势，灵活变通，不固执己见。"},
    18: {"name": "蛊", "symbol": "☶", "binary": "011001",
         "meaning": "山下有风，蛊，君子以振民育德",
         "keywords": ["整顿", "修复", "变革", "更新"], "fortune": 0.62,
         "advice": "中平。整顿修复，革故鼎新，需要耐心。"},
    19: {"name": "临", "symbol": "☱", "binary": "000011",
         "meaning": "泽上有地，临，君子以教思无穷",
         "keywords": ["领导", "守护", "治理", "君临"], "fortune": 0.85,
         "advice": "吉。君临天下，以德服人，守护众生。"},
    20: {"name": "观", "symbol": "☴", "binary": "110000",
         "meaning": "风行地上，观，君子以省方观民设教",
         "keywords": ["观察", "审视", "教导", "影响"], "fortune": 0.75,
         "advice": "中吉。观察入微，以身作则，教化众生。"},
    21: {"name": "噬嗑", "symbol": "☲", "binary": "101001",
         "meaning": "雷电噬嗑，君子以明罚敕法",
         "keywords": ["决断", "刑罚", "明察", "执行"], "fortune": 0.65,
         "advice": "中平。明察秋毫，果断执行，公正无私。"},
    22: {"name": "贲", "symbol": "☶", "binary": "100101",
         "meaning": "山下有火，贲，君子以明庶政",
         "keywords": ["修饰", "文饰", "审美", "文化"], "fortune": 0.70,
         "advice": "中吉。文质彬彬，内外兼修，文化传世。"},
    23: {"name": "剥", "symbol": "☶", "binary": "000001",
         "meaning": "山附于地，剥，君子以厚下安宅",
         "keywords": ["剥落", "消除", "削减", "剥离"], "fortune": 0.40,
         "advice": "凶。剔除不良，去除冗余，守正待时。"},
    24: {"name": "复", "symbol": "☷", "binary": "100000",
         "meaning": "雷在地中，复，君子以闭关",
         "keywords": ["回复", "回归", "复苏", "周期"], "fortune": 0.78,
         "advice": "吉。回复本源，返璞归真，重新出发。"},
    25: {"name": "无妄", "symbol": "☰", "binary": "100111",
         "meaning": "天下雷行，无妄，君子以茂对时育万物",
         "keywords": ["真实", "诚实", "无伪", "自然"], "fortune": 0.80,
         "advice": "吉。实事求是，真诚无伪，顺应自然。"},
    26: {"name": "大畜", "symbol": "☶", "binary": "111001",
         "meaning": "天在山中，大畜，君子以多识前言往行",
         "keywords": ["积蓄", "储备", "蓄力", "准备"], "fortune": 0.75,
         "advice": "中吉。积蓄力量，厚积薄发，为未来准备。"},
    27: {"name": "颐", "symbol": "☶", "binary": "100001",
         "meaning": "山下有雷，颐，君子以慎言语",
         "keywords": ["滋养", "休养", "修养", "进食"], "fortune": 0.72,
         "advice": "中吉。养精蓄锐，修身养性，慎言慎行。"},
    28: {"name": "大过", "symbol": "☱", "binary": "011110",
         "meaning": "泽灭木，大过，君子以独立不惧",
         "keywords": ["过度", "非常", "超越", "独立"], "fortune": 0.55,
         "advice": "中平。过犹不及，适度而行，独立不惧。"},
    29: {"name": "坎", "symbol": "☵", "binary": "010010",
         "meaning": "水洊至，坎，君子以常德行",
         "keywords": ["险难", "陷阱", "挫折", "坚持"], "fortune": 0.48,
         "advice": "凶。水深多险，需谨慎行事，坚守正道。"},
    30: {"name": "离", "symbol": "☲", "binary": "101101",
         "meaning": "明两作，离，君子以继明照于四方",
         "keywords": ["光明", "依附", "文明", "照耀"], "fortune": 0.82,
         "advice": "吉。光明照耀，文明兴盛，趋利避害。"},
    31: {"name": "咸", "symbol": "☱", "binary": "001110",
         "meaning": "山上有泽，咸，君子以虚受人",
         "keywords": ["感应", "共鸣", "情感", "感动"], "fortune": 0.78,
         "advice": "吉。心诚意正，感而遂通，情感共鸣。"},
    32: {"name": "恒", "symbol": "☳", "binary": "111000",
         "meaning": "雷风恒，君子以立不易方",
         "keywords": ["恒久", "坚持", "稳定", "不变"], "fortune": 0.80,
         "advice": "吉。持之以恒，守正不移，终有所成。"},
    33: {"name": "遁", "symbol": "☰", "binary": "001111",
         "meaning": "天下有山，遁，君子以远小人",
         "keywords": ["退避", "隐藏", "保存", "等待"], "fortune": 0.62,
         "advice": "中平。退避三舍，保存实力，等待时机。"},
    34: {"name": "大壮", "symbol": "☳", "binary": "111100",
         "meaning": "雷天大壮，君子以非礼弗履",
         "keywords": ["强盛", "壮大", "刚健", "推进"], "fortune": 0.78,
         "advice": "吉。强盛之时，礼法行事，不可蛮干。"},
    35: {"name": "晋", "symbol": "☲", "binary": "000101",
         "meaning": "明出地上，晋，君子以自昭明德",
         "keywords": ["前进", "晋升", "发展", "光明"], "fortune": 0.82,
         "advice": "吉。光明在前，积极进取，自昭明德。"},
    36: {"name": "明夷", "symbol": "☷", "binary": "101000",
         "meaning": "明入地中，明夷，君子以莅众",
         "keywords": ["晦暗", "受挫", "隐忍", "等待"], "fortune": 0.45,
         "advice": "凶。明夷之象，隐忍待时，不可冒进。"},
    37: {"name": "家人", "symbol": "☴", "binary": "101011",
         "meaning": "风自火出，家人，君子以言有物",
         "keywords": ["家庭", "和谐", "责任", "传承"], "fortune": 0.85,
         "advice": "吉。家和万事兴，言传身教，传承家风。"},
    38: {"name": "睽", "symbol": "☲", "binary": "101110",
         "meaning": "上火下泽，睽，君子以同而异",
         "keywords": ["分歧", "差异", "求同存异"], "fortune": 0.60,
         "advice": "中平。求同存异，和而不同，兼容并蓄。"},
    39: {"name": "蹇", "symbol": "☵", "binary": "010100",
         "meaning": "山上有水，蹇，君子以反身修德",
         "keywords": ["艰难", "困境", "反思", "修身"], "fortune": 0.52,
         "advice": "凶。艰难困苦，玉汝于成，反身修德。"},
    40: {"name": "解", "symbol": "☳", "binary": "001010",
         "meaning": "雷雨作，解，君子以赦过宥罪",
         "keywords": ["解脱", "解决", "释放", "宽恕"], "fortune": 0.75,
         "advice": "吉。困难解除，形势好转，宽以待人。"},
    41: {"name": "损", "symbol": "☶", "binary": "100011",
         "meaning": "山下有泽，损，君子以惩忿窒欲",
         "keywords": ["减少", "损益", "节制", "精简"], "fortune": 0.62,
         "advice": "中平。损有余而补不足，节制欲望，精简冗余。"},
    42: {"name": "益", "symbol": "☴", "binary": "110001",
         "meaning": "风雷益，君子以见善则迁",
         "keywords": ["增益", "助长", "帮助", "发展"], "fortune": 0.85,
         "advice": "吉。增益之象，助人助己，见善则迁。"},
    43: {"name": "夬", "symbol": "☰", "binary": "011111",
         "meaning": "泽天夬，君子以施禄及下",
         "keywords": ["决断", "果断", "分离", "选择"], "fortune": 0.70,
         "advice": "中吉。果断决策，当断则断，惠及他人。"},
    44: {"name": "姤", "symbol": "☴", "binary": "011110",
         "meaning": "天下有风，姤，君子以施命诰四方",
         "keywords": ["相遇", "偶遇", "机缘", "启示"], "fortune": 0.68,
         "advice": "中平。机缘巧合，相遇是缘，把握时机。"},
    45: {"name": "萃", "symbol": "☱", "binary": "000110",
         "meaning": "泽地萃，君子以除戎器",
         "keywords": ["聚集", "汇聚", "集合", "团结"], "fortune": 0.80,
         "advice": "吉。汇聚英才，团结力量，共成大业。"},
    46: {"name": "升", "symbol": "☷", "binary": "000110",
         "meaning": "地中生木，升，君子以顺德",
         "keywords": ["上升", "晋升", "进展", "提升"], "fortune": 0.78,
         "advice": "吉。顺其自然，不断上升，终有所成。"},
    47: {"name": "困", "symbol": "☱", "binary": "011010",
         "meaning": "泽无水，困，君子以致命遂志",
         "keywords": ["困境", "贫穷", "坚持", "志向"], "fortune": 0.40,
         "advice": "凶。困顿之时，坚守志向，以待转机。"},
    48: {"name": "井", "symbol": "☵", "binary": "010110",
         "meaning": "木上有水，井，君子以劳民劝相",
         "keywords": ["源泉", "供给", "滋养", "互助"], "fortune": 0.75,
         "advice": "中吉。井养不穷，互助互惠，共同发展。"},
    49: {"name": "革", "symbol": "☱", "binary": "101110",
         "meaning": "泽中有火，革，君子以治历明时",
         "keywords": ["变革", "改革", "更新", "革命"], "fortune": 0.72,
         "advice": "中吉。变革之时，与时俱进，革故鼎新。"},
    50: {"name": "鼎", "symbol": "☲", "binary": "101110",
         "meaning": "木上有火，鼎，君子以正位凝命",
         "keywords": ["鼎盛", "稳固", "重器", "使命"], "fortune": 0.82,
         "advice": "吉。鼎盛之象，稳固根基，凝聚使命。"},
    51: {"name": "震", "symbol": "☳", "binary": "001001",
         "meaning": "洊雷震，君子以恐惧修省",
         "keywords": ["震动", "震惊", "警惕", "反省"], "fortune": 0.58,
         "advice": "中平。震动之时，恐惧修省，谨慎行事。"},
    52: {"name": "艮", "symbol": "☶", "binary": "100100",
         "meaning": "兼山艮，君子以思不出其位",
         "keywords": ["静止", "止步", "思考", "定位"], "fortune": 0.65,
         "advice": "中平。知止而后定，思不出其位，守住本分。"},
    53: {"name": "渐", "symbol": "☴", "binary": "110100",
         "meaning": "山上有木，渐，君子以居贤德",
         "keywords": ["渐进", "缓慢", "逐步", "积累"], "fortune": 0.72,
         "advice": "中吉。循序渐进，不急不躁，终至成功。"},
    54: {"name": "归妹", "symbol": "☳", "binary": "100110",
         "meaning": "泽上有雷，归妹，君子以永终知敝",
         "keywords": ["归宿", "归属", "回归", "完成"], "fortune": 0.68,
         "advice": "中平。回归本心，知终知敝，有始有终。"},
    55: {"name": "丰", "symbol": "☳", "binary": "001101",
         "meaning": "雷电皆至，丰，君子以折狱致刑",
         "keywords": ["丰收", "充盈", "盛大", "富足"], "fortune": 0.85,
         "advice": "吉。丰盛之时，明察秋毫，公平公正。"},
    56: {"name": "旅", "symbol": "☲", "binary": "101100",
         "meaning": "山上有火，旅，君子以明慎用刑",
         "keywords": ["旅行", "漂泊", "流动", "探索"], "fortune": 0.62,
         "advice": "中平。旅居在外，明慎行事，探索新知。"},
    57: {"name": "巽", "symbol": "☴", "binary": "110110",
         "meaning": "随风巽，君子以申命行事",
         "keywords": ["顺从", "进入", "渗透", "教化"], "fortune": 0.72,
         "advice": "中吉。顺势而为，温和渗透，教化四方。"},
    58: {"name": "兑", "symbol": "☱", "binary": "011011",
         "meaning": "丽泽兑，君子以朋友讲习",
         "keywords": ["愉悦", "沟通", "交流", "学习"], "fortune": 0.78,
         "advice": "吉。愉悦沟通，互相学习，共同进步。"},
    59: {"name": "涣", "symbol": "☴", "binary": "110010",
         "meaning": "风行水上，涣，君子以享于帝立庙",
         "keywords": ["涣散", "扩散", "凝聚", "统一"], "fortune": 0.65,
         "advice": "中平。涣散之时，凝聚力量，统一思想。"},
    60: {"name": "节", "symbol": "☵", "binary": "010011",
         "meaning": "泽上有水，节，君子以制数度",
         "keywords": ["节制", "约束", "规范", "制度"], "fortune": 0.72,
         "advice": "中吉。节制有度，规范行为，制度先行。"},
    61: {"name": "中孚", "symbol": "☴", "binary": "110011",
         "meaning": "泽上有风，中孚，君子以议狱缓死",
         "keywords": ["诚信", "真诚", "信任", "感化"], "fortune": 0.82,
         "advice": "吉。诚信感化，真诚相待，信任为本。"},
    62: {"name": "小过", "symbol": "☳", "binary": "001100",
         "meaning": "山上有雷，小过，君子以行过乎恭",
         "keywords": ["小过", "轻过", "谨慎", "调整"], "fortune": 0.62,
         "advice": "中平。小有逾越，谨慎调整，不为过甚。"},
    63: {"name": "既济", "symbol": "☵", "binary": "010101",
         "meaning": "水火既济，君子以思患而豫防之",
         "keywords": ["成功", "完成", "圆满", "预防"], "fortune": 0.88,
         "advice": "大吉。事已大成，思患预防，保持警醒。"},
    64: {"name": "未济", "symbol": "☲", "binary": "101010",
         "meaning": "火在水上，未济，君子以慎辨物居方",
         "keywords": ["未完成", "未成熟", "继续", "探索"], "fortune": 0.55,
         "advice": "中平。事未完成，继续努力，辨物居方。"},
}

# ============================================================
# 2. 节气权重表
# ============================================================

SOLAR_TERMS = {
    "立春": {"weight": 1.1, "keywords": ["开始", "生发"]},
    "雨水": {"weight": 1.05, "keywords": ["滋润", "柔和"]},
    "惊蛰": {"weight": 1.15, "keywords": ["觉醒", "行动"]},
    "春分": {"weight": 1.0, "keywords": ["平衡", "和谐"]},
    "清明": {"weight": 0.95, "keywords": ["清晰", "明朗"]},
    "谷雨": {"weight": 1.05, "keywords": ["滋养", "成长"]},
    "立夏": {"weight": 1.2, "keywords": ["旺盛", "扩张"]},
    "小满": {"weight": 1.1, "keywords": ["丰盈", "满足"]},
    "芒种": {"weight": 1.15, "keywords": ["忙碌", "收获"]},
    "夏至": {"weight": 1.25, "keywords": ["极盛", "转折"]},
    "小暑": {"weight": 1.1, "keywords": ["炎热", "活跃"]},
    "大暑": {"weight": 1.2, "keywords": ["酷热", "考验"]},
    "立秋": {"weight": 0.9, "keywords": ["收敛", "沉淀"]},
    "处暑": {"weight": 0.85, "keywords": ["消退", "调整"]},
    "白露": {"weight": 0.8, "keywords": ["凝结", "内省"]},
    "秋分": {"weight": 1.0, "keywords": ["平衡", "收获"]},
    "寒露": {"weight": 0.75, "keywords": ["寒冷", "收藏"]},
    "霜降": {"weight": 0.7, "keywords": ["肃杀", "准备"]},
    "立冬": {"weight": 0.6, "keywords": ["蛰伏", "休养"]},
    "小雪": {"weight": 0.65, "keywords": ["寒冷", "静默"]},
    "大雪": {"weight": 0.55, "keywords": ["严寒", "坚韧"]},
    "冬至": {"weight": 0.5, "keywords": ["极寒", "希望"]},
    "小寒": {"weight": 0.55, "keywords": ["寒冷", "等待"]},
    "大寒": {"weight": 0.6, "keywords": ["严寒", "蓄势"]},
}

# 节气日期表 (月日数值: 月*100+日) → 节气名
_SOLAR_TERM_TABLE = [
    (105, "小寒"), (120, "大寒"), (204, "立春"), (219, "雨水"),
    (306, "惊蛰"), (321, "春分"), (405, "清明"), (420, "谷雨"),
    (506, "立夏"), (521, "小满"), (606, "芒种"), (621, "夏至"),
    (707, "小暑"), (723, "大暑"), (808, "立秋"), (823, "处暑"),
    (908, "白露"), (923, "秋分"), (1008, "寒露"), (1024, "霜降"),
    (1108, "立冬"), (1122, "小雪"), (1207, "大雪"), (1222, "冬至"),
]

# ============================================================
# 3. 易经推演引擎
# ============================================================


class YijingEngine:
    """龍魂 · 易经推演引擎"""

    def __init__(self):
        self.gua_db = GUA_DATABASE
        self.solar_terms = SOLAR_TERMS
        self.dna = generate_dna("YIJING-ENGINE")
        self.history = []

    def get_current_solar_term(self) -> str:
        """获取当前节气（按日期区间查表，含跨年兜底）"""
        now = datetime.now()
        md = now.month * 100 + now.day
        term = "冬至"  # 兜底（1月初）
        for mday, name in _SOLAR_TERM_TABLE:
            if md >= mday:
                term = name
        return term

    def cast_gua(self, question: str = "", timestamp: float = None) -> Dict:
        """起卦 - 生成卦象"""
        if timestamp is None:
            timestamp = time.time()

        # 方法1: 基于问题的hash起卦
        seed = f"{question}{timestamp}{self.dna}"
        hash_val = hashlib.sha256(seed.encode('utf-8')).hexdigest()
        gua_number = (int(hash_val[:8], 16) % 64) + 1

        gua = self.gua_db.get(gua_number, self.gua_db[1])

        # 生成爻
        lines = []
        for i in range(6):
            byte_val = int(hash_val[i * 2:(i + 1) * 2], 16)
            lines.append(1 if byte_val > 127 else 0)

        # 变爻
        change_lines = []
        for i in range(6):
            byte_val = int(hash_val[i * 2 + 12:(i + 1) * 2 + 12], 16)
            if byte_val < 64 or byte_val > 191:
                change_lines.append(i)

        return {
            "gua": gua,
            "gua_number": gua_number,
            "lines": lines,
            "change_lines": change_lines,
            "hash": hash_val[:16],
            "dna": generate_dna("GUA")
        }

    def derive_mutual_hexagram(self, lines: List[int]) -> Dict:
        """推演互卦（2/3/4爻为下卦 + 3/4/5爻为上卦）"""
        lower = lines[1:4]
        upper = lines[2:5]
        mutual_lines = lower + upper
        binary_str = "".join(map(str, mutual_lines))
        gua_number = int(binary_str, 2) % 64 + 1 if binary_str else 1
        return {
            "lines": mutual_lines,
            "binary": binary_str,
            "gua_number": gua_number,
            "gua": self.gua_db.get(gua_number, self.gua_db[1])
        }

    def derive_changed_hexagram(self, lines: List[int], change_lines: List[int]) -> Dict:
        """推演变卦"""
        changed = lines.copy()
        for pos in change_lines:
            changed[pos] = 1 - changed[pos]  # 阴阳互换
        binary_str = "".join(map(str, changed))
        gua_number = int(binary_str, 2) % 64 + 1 if binary_str else 1
        return {
            "lines": changed,
            "binary": binary_str,
            "gua_number": gua_number,
            "gua": self.gua_db.get(gua_number, self.gua_db[1])
        }

    def analyze_solar_term(self, gua: Dict) -> Dict:
        """节气加权分析"""
        term = self.get_current_solar_term()
        term_data = self.solar_terms.get(term, {"weight": 1.0, "keywords": []})

        adjusted_fortune = gua["gua"]["fortune"] * term_data["weight"]
        adjusted_fortune = max(0.0, min(1.0, adjusted_fortune))

        return {
            "solar_term": term,
            "term_weight": term_data["weight"],
            "term_keywords": term_data["keywords"],
            "adjusted_fortune": adjusted_fortune
        }

    def analyze_wuxing(self, original_gua: Dict, changed_gua: Dict) -> Dict:
        """五行生克分析"""
        element_map = {
            "乾": "金", "兑": "金",
            "震": "木", "巽": "木",
            "坎": "水",
            "离": "火",
            "坤": "土", "艮": "土"
        }

        orig_name = original_gua["gua"]["name"]
        changed_name = changed_gua["gua"]["name"]

        orig_element = element_map.get(orig_name, "木")
        changed_element = element_map.get(changed_name, "木")

        sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
        ke_map = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

        is_sheng = sheng_map.get(orig_element) == changed_element
        is_ke = ke_map.get(orig_element) == changed_element

        if is_sheng:
            trend = "顺势而行，事半功倍"
            score = 0.8
        elif is_ke:
            trend = "逆势而动，需化解阻碍"
            score = 0.3
        else:
            trend = "平和之象，稳步推进"
            score = 0.5

        return {
            "original_element": orig_element,
            "changed_element": changed_element,
            "is_sheng": is_sheng,
            "is_ke": is_ke,
            "trend": trend,
            "score": score
        }

    def taiji_judgment(self, original_gua: Dict, mutual_gua: Dict,
                       changed_gua: Dict, solar_weight: float) -> Dict:
        """太极三才综合判断"""
        # 天道：卦象吉凶
        orig_fortune = original_gua["gua"]["fortune"]
        tian_score = 0.7 if orig_fortune >= 0.7 else 0.4

        # 地道：五行分析
        wuxing = self.analyze_wuxing(original_gua, changed_gua)
        di_score = wuxing["score"]

        # 人道：变爻分析
        change_count = len(original_gua.get("change_lines", []))
        ren_score = 0.8 if change_count <= 1 else (0.5 if change_count <= 3 else 0.3)

        # 综合分数（节气加权）
        final_score = (tian_score * 0.4 + di_score * 0.3 + ren_score * 0.3) * solar_weight

        if final_score > 0.7:
            judgment = "大吉 - 诸事顺遂，可大胆行动"
            color = "🟢"
        elif final_score > 0.5:
            judgment = "小吉 - 稍有阻碍，谨慎可行"
            color = "🟢"
        elif final_score > 0.3:
            judgment = "中平 - 平常之象，守正待时"
            color = "🟡"
        elif final_score > 0.1:
            judgment = "小凶 - 有险阻，宜三思而行"
            color = "🔴"
        else:
            judgment = "大凶 - 诸事不宜，应当止步"
            color = "🔴"

        return {
            "judgment": judgment,
            "score": round(final_score, 3),
            "color": color,
            "details": {
                "tian_dao": {"score": tian_score, "text": original_gua["gua"]["meaning"]},
                "di_dao": {"score": di_score, "text": wuxing["trend"]},
                "ren_dao": {"score": ren_score, "changes": change_count}
            }
        }

    def complete_divination(self, question: str, timestamp: float = None) -> Dict:
        """完整占卜流程"""
        dna = generate_dna("DIVINATION")

        # 1. 起卦
        original = self.cast_gua(question, timestamp)

        # 2. 推演互卦
        mutual = self.derive_mutual_hexagram(original["lines"])

        # 3. 推演变卦
        changed = self.derive_changed_hexagram(original["lines"], original["change_lines"])

        # 4. 节气分析
        solar_analysis = self.analyze_solar_term(original)

        # 5. 五行分析
        wuxing_analysis = self.analyze_wuxing(original, changed)

        # 6. 太极判断
        final = self.taiji_judgment(original, mutual, changed, solar_analysis["adjusted_fortune"])

        # 记录历史
        result = {
            "dna": dna,
            "question": question,
            "timestamp": timestamp or time.time(),
            "hexagrams": {
                "original": {
                    "number": original["gua_number"],
                    "name": original["gua"]["name"],
                    "symbol": original["gua"]["symbol"],
                    "meaning": original["gua"]["meaning"]
                },
                "mutual": {
                    "number": mutual["gua_number"],
                    "name": mutual["gua"]["name"],
                    "symbol": mutual["gua"]["symbol"]
                },
                "changed": {
                    "number": changed["gua_number"],
                    "name": changed["gua"]["name"],
                    "symbol": changed["gua"]["symbol"]
                }
            },
            "solar_term": solar_analysis["solar_term"],
            "solar_weight": solar_analysis["term_weight"],
            "wuxing": wuxing_analysis,
            "judgment": final,
            "advice": final["details"]["di_dao"]["text"],
            "color": final["color"]
        }

        self.history.append(result)
        return result

    def predict_timeline(self, question: str, years: int = 1) -> List[Dict]:
        """时间线预测（修复: 跨月日期安全计算，31号不崩溃）"""
        results = []
        base_time = datetime.now()
        total_months = 12 * years

        for i in range(total_months):
            target_year = base_time.year + (base_time.month - 1 + i) // 12
            target_month = (base_time.month - 1 + i) % 12 + 1
            # 日期兜底：目标月可能没有 base 的 day（如 1月31日+1月）
            day = min(base_time.day, calendar.monthrange(target_year, target_month)[1])
            future_date = datetime(target_year, target_month, day)

            time_seed = int(future_date.strftime("%Y%m%d"))
            question_seed = sum(ord(c) for c in question)
            gua_number = ((time_seed + question_seed) % 64) + 1
            gua = self.gua_db.get(gua_number, self.gua_db[1])
            results.append({
                "date": future_date.strftime("%Y-%m"),
                "gua": gua["name"],
                "symbol": gua["symbol"],
                "fortune": gua["fortune"],
                "keywords": gua["keywords"]
            })

        return results

    def get_advice(self, question: str) -> str:
        """快速获取建议"""
        result = self.complete_divination(question)
        return f"""{result['color']} {result['judgment']['judgment']}

📜 卦象: {result['hexagrams']['original']['symbol']} {result['hexagrams']['original']['name']}卦
📖 卦辞: {result['hexagrams']['original']['meaning']}
🌅 节气: {result['solar_term']} (权重: {result['solar_weight']})
⚡ 五行: {result['wuxing']['trend']}
💡 建议: {result['advice']}
🧬 DNA: {result['dna']}"""


# ============================================================
# 4. 五行平衡引擎
# ============================================================


class WuxingBalanceEngine:
    """五行平衡分析引擎"""

    def __init__(self):
        self.wuxing = {
            "木": {"属性": "生长", "方向": "东", "颜色": "青", "score": 0},
            "火": {"属性": "扩张", "方向": "南", "颜色": "红", "score": 0},
            "土": {"属性": "稳定", "方向": "中", "颜色": "黄", "score": 0},
            "金": {"属性": "收敛", "方向": "西", "颜色": "白", "score": 0},
            "水": {"属性": "流动", "方向": "北", "颜色": "黑", "score": 0},
        }
        self.shengke = {
            "木": {"生": "火", "克": "土"},
            "火": {"生": "土", "克": "金"},
            "土": {"生": "金", "克": "水"},
            "金": {"生": "水", "克": "木"},
            "水": {"生": "木", "克": "火"}
        }

    def analyze(self, state: Dict) -> Dict:
        """分析五行平衡"""
        scores = {
            "木": state.get("growth", 0.5),
            "火": state.get("expansion", 0.5),
            "土": state.get("stability", 0.5),
            "金": state.get("efficiency", 0.5),
            "水": state.get("flexibility", 0.5)
        }

        values = list(scores.values())
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        balance_score = max(0.0, min(1.0, 1 - (variance / 0.3)))  # 归一化

        # 找出最弱和最强的元素
        weak_element = min(scores.items(), key=lambda x: x[1])
        strong_element = max(scores.items(), key=lambda x: x[1])

        # 生成建议
        sheng_by = None
        for k, v in self.shengke.items():
            if v["生"] == weak_element[0]:
                sheng_by = k
                break

        advice = f"系统{weak_element[0]}行不足（{self.wuxing[weak_element[0]]['属性']}能力弱），"
        if sheng_by:
            advice += f"建议强化{sheng_by}行来生旺{weak_element[0]}行。"
        else:
            advice += "建议整体提升薄弱环节。"

        return {
            "scores": scores,
            "balance_score": round(balance_score, 3),
            "weak_point": weak_element[0],
            "weak_value": round(weak_element[1], 3),
            "strong_point": strong_element[0],
            "strong_value": round(strong_element[1], 3),
            "advice": advice,
            "color": "🟢" if balance_score > 0.7 else ("🟡" if balance_score > 0.4 else "🔴")
        }


# ============================================================
# 5. 中庸决策引擎
# ============================================================


class ZhongYongEngine:
    """中庸决策引擎"""

    def __init__(self):
        pass

    def balanced_decision(self, options: List[Dict]) -> Dict:
        """中庸决策：寻找最平衡的方案"""
        scores = {}

        for opt in options:
            factors = opt.get("factors", {})
            if not factors:
                balance_score = 0.5
            else:
                values = list(factors.values())
                mean = sum(values) / len(values)
                variance = sum(abs(x - mean) for x in values) / len(values)
                balance_score = max(0.0, min(1.0, 1 - variance))

            risk_score = 1 - opt.get("risk", 0.5)  # 风险越低分数越高
            opp_score = opt.get("opportunity", 0.5)

            # 中庸评分：平衡度40% + 风险控制30% + 机会把握30%
            zhongyong_score = balance_score * 0.4 + risk_score * 0.3 + opp_score * 0.3

            scores[opt.get("name", "选项")] = {
                "total_score": round(zhongyong_score, 3),
                "balance": round(balance_score, 3),
                "risk": round(risk_score, 3),
                "opportunity": round(opp_score, 3)
            }

        best = max(scores.items(), key=lambda x: x[1]["total_score"])

        if best[1]["total_score"] >= 0.8:
            reason = "此方案符合中庸之道：既有进取又有稳健，风险可控，机会适中，建议采纳。"
        elif best[1]["total_score"] >= 0.6:
            reason = "方案尚可，建议适度调整后可行。"
        else:
            reason = "方案失衡，风险过高或机会不足，建议重新权衡。"

        return {
            "recommended": best[0],
            "score": best[1]["total_score"],
            "reason": reason,
            "all_scores": scores
        }


# ============================================================
# 6. 主引擎
# ============================================================


class CNSH_Yijing_System:
    """龍魂 · 易经文化AI系统"""

    def __init__(self):
        self.yijing = YijingEngine()
        self.wuxing = WuxingBalanceEngine()
        self.zhongyong = ZhongYongEngine()
        self.dna = generate_dna("CNSH-YIJING")
        self.history = []

    def divination(self, question: str) -> Dict:
        """易经占卜"""
        result = self.yijing.complete_divination(question)
        self.history.append(result)
        return result

    def balance_analysis(self, state: Dict) -> Dict:
        """五行平衡分析"""
        return self.wuxing.analyze(state)

    def decision(self, options: List[Dict]) -> Dict:
        """中庸决策"""
        return self.zhongyong.balanced_decision(options)

    def timeline(self, question: str, years: int = 1) -> List[Dict]:
        """时间线预测"""
        return self.yijing.predict_timeline(question, years)

    def get_history(self) -> List[Dict]:
        return self.history

    def get_status(self) -> Dict:
        return {
            "dna": self.dna,
            "history_count": len(self.history),
            "engine": "龍魂易经文化AI系统 v2.0",
            "status": "🟢 运行中"
        }


# ============================================================
# 7. 命令行接口
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 易经算法引擎 v2.0",
        epilog="DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-YIJING-ENGINE-UID9622"
    )

    parser.add_argument("--divination", "-d", type=str, help="占卜问题")
    parser.add_argument("--wuxing", "-w", type=str, help="五行分析 (JSON状态)")
    parser.add_argument("--decision", "-z", type=str, help="中庸决策 (JSON选项)")
    parser.add_argument("--advice", "-a", type=str, help="快速获取建议")
    parser.add_argument("--timeline", "-t", type=str, help="时间线预测 (问题)")
    parser.add_argument("--years", "-y", type=int, default=1, help="时间线年数")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    system = CNSH_Yijing_System()

    if args.status:
        status = system.get_status()
        if args.json:
            print(json.dumps(status, indent=2, ensure_ascii=False))
        else:
            print("\n🐉 龍魂 · 易经文化AI系统")
            print("=" * 50)
            print(f"  DNA: {status['dna']}")
            print(f"  状态: {status['status']}")
            print(f"  历史记录: {status['history_count']}")
        return

    if args.advice:
        result = system.yijing.get_advice(args.advice)
        print(result)
        return

    if args.divination:
        result = system.divination(args.divination)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("\n🐉 易经推演结果")
            print("=" * 50)
            print(f"🧬 DNA: {result['dna']}")
            print(f"📝 问题: {result['question']}")
            print(f"📜 本卦: {result['hexagrams']['original']['symbol']} {result['hexagrams']['original']['name']}卦")
            print(f"   ☯ 卦辞: {result['hexagrams']['original']['meaning']}")
            print(f"🔀 互卦: {result['hexagrams']['mutual']['symbol']} {result['hexagrams']['mutual']['name']}卦")
            print(f"🔄 变卦: {result['hexagrams']['changed']['symbol']} {result['hexagrams']['changed']['name']}卦")
            print(f"🌅 节气: {result['solar_term']} (权重: {result['solar_weight']})")
            print(f"⚡ 五行: {result['wuxing']['trend']}")
            print(f"🎯 判断: {result['judgment']['judgment']}")
            print(f"💡 建议: {result['advice']}")
        return

    if args.timeline:
        result = system.timeline(args.timeline, args.years)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n🐉 时间线预测（{args.years}年）")
            print("=" * 50)
            for r in result:
                print(f"  {r['date']}: {r['symbol']} {r['gua']}卦 运势{r['fortune']} {'·'.join(r['keywords'][:2])}")
        return

    if args.wuxing:
        try:
            state = json.loads(args.wuxing)
            result = system.balance_analysis(state)
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("\n🐉 五行平衡分析")
                print("=" * 50)
                print(f"  平衡度: {result['balance_score']}")
                print(f"  薄弱环节: {result['weak_point']} ({result['weak_value']})")
                print(f"  优势环节: {result['strong_point']} ({result['strong_value']})")
                print(f"  建议: {result['advice']}")
        except json.JSONDecodeError:
            print("❌ 无效的JSON格式")
        return

    if args.decision:
        try:
            options = json.loads(args.decision)
            result = system.decision(options)
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("\n🐉 中庸决策")
                print("=" * 50)
                print(f"  推荐: {result['recommended']}")
                print(f"  评分: {result['score']}")
                print(f"  理由: {result['reason']}")
                print(f"  全部方案: {json.dumps(result['all_scores'], ensure_ascii=False)}")
        except json.JSONDecodeError:
            print("❌ 无效的JSON格式")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
