#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · LU-Time Engine v4.0
DNA: #龍芯⚡️2026-08-02-LU-TIME-ENGINE-v4.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 时间 → 天干地支 → 卦象计算引擎
  2. 64卦对照系统（完整数据库）
  3. 审计链（区块链式哈希，只增不删）
  4. Notion API 自动写入
  5. 定时任务（每日自动记录）
  6. 任务联动系统
  7. 安全监控与异常检测
  8. 预测记录与趋势分析
  9. 版本继承链（只递增）
  10. 盾加密系统（S0-S3）
  11. v4.1: 输出戳生成器 — 每句回复自动附时间戳+卦象

用法：
  python3 bin/lh_time_engine.py --run              # 立即执行一次时间记录
  python3 bin/lh_time_engine.py --daemon           # 启动守护进程（每日定时）
  python3 bin/lh_time_engine.py --hexagram 43      # 查询卦象信息
  python3 bin/lh_time_engine.py --audit            # 查看审计链
  python3 bin/lh_time_engine.py --status           # 查看系统状态
  python3 bin/lh_time_engine.py --sync             # 同步到Notion
  python3 bin/lh_time_engine.py --analyze          # 趋势分析
  python3 bin/lh_time_engine.py --stamp            # 输出当前时间戳（供其他引擎调用）
  python3 bin/lh_time_engine.py --interactive      # 交互模式

集成到lh:
  lh time-engine --run
  lh time-engine --status
  lh time-engine --hexagram 43
  lh time-engine --stamp
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import time
import argparse
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import requests

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "time_engine.db"
NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_DB_TIME = os.environ.get("NOTION_DB_TIME_ENGINE", "")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 天干地支基表（L0 焊死不可变）
# ============================================================

十天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
十二地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
十二时辰名 = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时",
              "午时", "未时", "申时", "酉时", "戌时", "亥时"]

# ============================================================
# 颜色终端
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
# 三色审计
# ============================================================

class TriColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

# ============================================================
# 八卦映射
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

# ============================================================
# 64卦数据库（完整）
# ============================================================

HEXAGRAM_DATA = {
    1: {"name": "乾为天", "meaning": "刚健不息，自强不息", "phase": "执行", "action": "积极行动，开拓进取"},
    2: {"name": "坤为地", "meaning": "厚德载物，顺承天道", "phase": "观察", "action": "静观其变，积蓄力量"},
    3: {"name": "屯", "meaning": "初生艰难，万事开头难", "phase": "调整", "action": "审时度势，稳步推进"},
    4: {"name": "蒙", "meaning": "启蒙发蒙，教育为先", "phase": "观察", "action": "学习积累，明辨是非"},
    5: {"name": "需", "meaning": "等待时机，蓄势待发", "phase": "观察", "action": "耐心等待，不急于求成"},
    6: {"name": "讼", "meaning": "争讼纷争，明辨是非", "phase": "调整", "action": "理清头绪，避免冲突"},
    7: {"name": "师", "meaning": "统帅之师，众志成城", "phase": "执行", "action": "团结协作，统一行动"},
    8: {"name": "比", "meaning": "亲和比附，团结互助", "phase": "执行", "action": "寻求合作，建立联盟"},
    9: {"name": "小畜", "meaning": "小有积蓄，量力而行", "phase": "调整", "action": "积累实力，小步快跑"},
    10: {"name": "履", "meaning": "履行责任，脚踏实地", "phase": "执行", "action": "按部就班，落实计划"},
    11: {"name": "泰", "meaning": "天地交泰，万事亨通", "phase": "执行", "action": "顺势而为，大展宏图"},
    12: {"name": "否", "meaning": "天地否塞，闭藏蓄力", "phase": "观察", "action": "韬光养晦，等待转机"},
    13: {"name": "同人", "meaning": "志同道合，汇聚力量", "phase": "执行", "action": "团结志同道合之人，共谋大业"},
    14: {"name": "大有", "meaning": "大有收获，丰盛圆满", "phase": "执行", "action": "珍惜成果，乘胜追击"},
    15: {"name": "谦", "meaning": "谦逊有礼，虚怀若谷", "phase": "调整", "action": "保持谦逊，听取建议"},
    16: {"name": "豫", "meaning": "愉悦和谐，顺势而为", "phase": "执行", "action": "顺势而上，轻松推进"},
    17: {"name": "随", "meaning": "随顺自然，不违天道", "phase": "执行", "action": "随势而动，灵活调整"},
    18: {"name": "蛊", "meaning": "革故鼎新，破旧立新", "phase": "执行", "action": "大胆改革，清除积弊"},
    19: {"name": "临", "meaning": "居高临下，统揽全局", "phase": "执行", "action": "把握全局，果断决策"},
    20: {"name": "观", "meaning": "观察审视，明辨方向", "phase": "观察", "action": "深入观察，审时度势"},
    21: {"name": "噬嗑", "meaning": "咬合咀嚼，化解矛盾", "phase": "调整", "action": "直面问题，解决冲突"},
    22: {"name": "贲", "meaning": "文饰美化，提升品位", "phase": "调整", "action": "注重外在，提升形象"},
    23: {"name": "剥", "meaning": "剥落衰败，去芜存菁", "phase": "观察", "action": "淘汰冗余，保留精华"},
    24: {"name": "复", "meaning": "回复生机，循环往复", "phase": "执行", "action": "回归本源，重新出发"},
    25: {"name": "无妄", "meaning": "真实无妄，顺应自然", "phase": "执行", "action": "真诚待人，顺其自然"},
    26: {"name": "大畜", "meaning": "积蓄大德，厚积薄发", "phase": "观察", "action": "持续积累，等待爆发"},
    27: {"name": "颐", "meaning": "颐养身心，调养恢复", "phase": "调整", "action": "修养调整，蓄力再发"},
    28: {"name": "大过", "meaning": "过度越界，危险边缘", "phase": "观察", "action": "收敛锋芒，克制过激"},
    29: {"name": "坎", "meaning": "险阻重重，砥砺前行", "phase": "观察", "action": "面对困难，坚定意志"},
    30: {"name": "离", "meaning": "光明照耀，明德天下", "phase": "执行", "action": "光明磊落，引领方向"},
    31: {"name": "咸", "meaning": "感应相通，情感共鸣", "phase": "执行", "action": "用心沟通，建立连接"},
    32: {"name": "恒", "meaning": "恒久不变，持之以恒", "phase": "执行", "action": "坚持信念，一以贯之"},
    33: {"name": "遁", "meaning": "退避隐居，避实就虚", "phase": "观察", "action": "暂时退让，另寻战机"},
    34: {"name": "大壮", "meaning": "大壮刚健，威震四方", "phase": "执行", "action": "展现力量，勇于担当"},
    35: {"name": "晋", "meaning": "晋升进步，日新月异", "phase": "执行", "action": "勇于进取，不断突破"},
    36: {"name": "明夷", "meaning": "光明受损，韬光养晦", "phase": "观察", "action": "隐藏实力，等待时机"},
    37: {"name": "家人", "meaning": "家和万事兴", "phase": "调整", "action": "和睦相处，建立规矩"},
    38: {"name": "睽", "meaning": "分歧对立，求同存异", "phase": "调整", "action": "化解分歧，寻找共识"},
    39: {"name": "蹇", "meaning": "艰难困苦，玉汝于成", "phase": "观察", "action": "克服困难，迎难而上"},
    40: {"name": "解", "meaning": "解除困难，豁然开朗", "phase": "执行", "action": "解决问题，打开局面"},
    41: {"name": "损", "meaning": "损下益上，顾全大局", "phase": "调整", "action": "适度牺牲，换取长远"},
    42: {"name": "益", "meaning": "益上益下，共同增长", "phase": "执行", "action": "互惠互利，共赢发展"},
    43: {"name": "夬", "meaning": "果断决断，果敢行动", "phase": "执行", "action": "当机立断，果断出击"},
    44: {"name": "姤", "meaning": "相遇邂逅，机缘巧合", "phase": "调整", "action": "把握机缘，顺势而为"},
    45: {"name": "萃", "meaning": "汇集精英，群英荟萃", "phase": "执行", "action": "汇聚人才，共谋大事"},
    46: {"name": "升", "meaning": "上升进取，步步高升", "phase": "执行", "action": "积极进取，追求卓越"},
    47: {"name": "困", "meaning": "困顿艰难，磨练意志", "phase": "观察", "action": "坚持忍耐，突破困境"},
    48: {"name": "井", "meaning": "井井有条，秩序井然", "phase": "执行", "action": "建立秩序，规范管理"},
    49: {"name": "革", "meaning": "革新变革，破旧立新", "phase": "执行", "action": "大胆革新，勇于突破"},
    50: {"name": "鼎", "meaning": "鼎立天下，稳重担当", "phase": "执行", "action": "稳扎稳打，承担重任"},
    51: {"name": "震", "meaning": "震动惊醒，蓄势待发", "phase": "执行", "action": "立即行动，抓住时机"},
    52: {"name": "艮", "meaning": "止于至善，知止不殆", "phase": "观察", "action": "适可而止，见好就收"},
    53: {"name": "渐", "meaning": "循序渐进，稳步前进", "phase": "执行", "action": "脚踏实地，步步为营"},
    54: {"name": "归妹", "meaning": "回归本位，各得其所", "phase": "调整", "action": "回归初心，重新定位"},
    55: {"name": "丰", "meaning": "丰盛充盈，收获满满", "phase": "执行", "action": "享受收获，乘胜前进"},
    56: {"name": "旅", "meaning": "旅行奔波，探索未知", "phase": "执行", "action": "探索尝试，勇闯新路"},
    57: {"name": "巽", "meaning": "风行天下，顺势而为", "phase": "执行", "action": "顺势而行，灵活应变"},
    58: {"name": "兑", "meaning": "喜悦沟通，和谐共赢", "phase": "执行", "action": "开心沟通，建立信任"},
    59: {"name": "涣", "meaning": "涣散聚合，统一思想", "phase": "执行", "action": "统一思想，集中力量"},
    60: {"name": "节", "meaning": "节制约束，量入为出", "phase": "调整", "action": "适度节制，开源节流"},
    61: {"name": "中孚", "meaning": "诚信中正，信守承诺", "phase": "执行", "action": "诚信待人，言行一致"},
    62: {"name": "小过", "meaning": "小有失误，及时纠正", "phase": "调整", "action": "注意细节，防微杜渐"},
    63: {"name": "既济", "meaning": "大功告成，圆满成功", "phase": "执行", "action": "庆祝成功，继续前行"},
    64: {"name": "未济", "meaning": "前路漫长，继续奋斗", "phase": "执行", "action": "再接再厉，永不放弃"},
}

# 64卦 Unicode 符号
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

def get_trigram_name(num: int) -> str:
    return TRIGRAM_MAP.get(num, {"name": "未知", "element": "未知", "symbol": "?"})["name"]

def get_hexagram_info(hexagram_id: int) -> Dict:
    return HEXAGRAM_DATA.get(hexagram_id, {
        "name": "未知卦", "meaning": "信息待补充", "phase": "观察", "action": "谨慎行事"
    })

# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            tiangan INTEGER,
            dizhi INTEGER,
            upper_trigram INTEGER,
            lower_trigram INTEGER,
            hexagram_id INTEGER,
            entropy REAL,
            phase TEXT,
            action TEXT,
            dna TEXT,
            sync_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(timestamp)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_id TEXT UNIQUE NOT NULL,
            event_type TEXT NOT NULL,
            user TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            data_hash TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            chain_hash TEXT NOT NULL,
            shield_level TEXT DEFAULT 'S0',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            time_ref_id INTEGER,
            hexagram_id INTEGER,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT '待执行',
            execution_mode TEXT,
            version INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(time_ref_id) REFERENCES time_records(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS version_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            parent_version_id TEXT,
            author TEXT DEFAULT 'UID9622',
            change_summary TEXT,
            data_snapshot TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hexagram_id INTEGER,
            prediction TEXT,
            outcome TEXT,
            accuracy REAL DEFAULT 0.0,
            dna TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT UNIQUE NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT,
            detected_time TEXT NOT NULL,
            status TEXT DEFAULT '待处理',
            resolution TEXT,
            dna TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shield_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT UNIQUE NOT NULL,
            description TEXT,
            visible_to TEXT
        )
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO shield_config (level, description, visible_to)
        VALUES
            ('S0', '公开', '所有人'),
            ('S1', '用户可见', '已认证用户'),
            ('S2', '私密', '仅UID9622'),
            ('S3', '核心加密', 'GPG签名验证')
    ''')

    conn.commit()
    conn.close()
    return True

def get_db():
    return sqlite3.connect(str(DB_PATH))

# ============================================================
# 核心: 干支四柱 + 卦象 计算引擎
# ============================================================

def 年干支(year: int = None) -> Tuple[str, str]:
    """年柱: 公元4年为甲子年基准，返回 (干支, 天干, 地支)"""
    if year is None:
        year = datetime.datetime.now().year
    base = year - 4
    gan = 十天干[base % 10]
    zhi = 十二地支[base % 12]
    return gan + zhi, gan, zhi

def 月干支(year: int = None, month: int = None) -> str:
    """月柱（五虎遁法）"""
    if year is None: year = datetime.datetime.now().year
    if month is None: month = datetime.datetime.now().month
    月支映射 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
    月支_idx = 月支映射[month - 1]
    年干 = 十天干.index(年干支(year)[1])
    寅月干映射 = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]
    寅月干 = 寅月干映射[年干]
    offset = (月支_idx - 2) % 12
    月干 = (寅月干 + offset) % 10
    return 十天干[月干] + 十二地支[月支_idx]

def 日干支(year: int = None, month: int = None, day: int = None) -> str:
    """日柱（精确序数公式）"""
    if year is None: year = datetime.datetime.now().year
    if month is None: month = datetime.datetime.now().month
    if day is None: day = datetime.datetime.now().day
    yy = year % 100
    base = (yy + 7) * 5 + 15 + (yy + 19) // 4
    base %= 60
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    月天数 = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year = sum(月天数[:month - 1]) + day
    seq = (base + day_of_year) % 60
    gan = 十天干[(seq - 1) % 10]
    zhi = 十二地支[(seq - 1) % 12]
    return gan + zhi

def 时辰(hour: int = None) -> str:
    """时柱: 23-1子时, 1-3丑时, ..."""
    if hour is None:
        hour = datetime.datetime.now().hour
    idx = ((hour + 1) // 2) % 12
    return 十二时辰名[idx]

def 当前四柱(ts: datetime.datetime = None) -> Tuple[str, str, str, str]:
    """返回 (年柱, 月柱, 日柱, 时辰)"""
    if ts is None:
        ts = datetime.datetime.now()
    nian, _, _ = 年干支(ts.year)
    yue = 月干支(ts.year, ts.month)
    ri = 日干支(ts.year, ts.month, ts.day)
    shi = 时辰(ts.hour)
    return nian, yue, ri, shi

def get_time_block(now: datetime.datetime = None) -> Dict:
    """计算当前时间的完整卦象信息"""
    if now is None:
        now = datetime.datetime.now()

    year, month, day, hour = now.year, now.month, now.day, now.hour

    # 天干地支
    tiangan = ((year - 4) % 10) + 1
    dizhi = ((year - 4) % 12) + 1

    # 上下卦（梅花易数时间起卦法）
    upper = ((tiangan + month) % 8)
    upper = 8 if upper == 0 else upper
    lower = ((day + hour) % 8)
    lower = 8 if lower == 0 else lower

    # 卦象ID
    hexagram_id = (upper - 1) * 8 + lower

    # 熵值
    entropy = abs(upper - lower) / 7

    # 相位判定
    if entropy > 0.7:
        phase = "观察"
        action = "观察等待"
        color = TriColor.RED.value
    elif entropy > 0.4:
        phase = "调整"
        action = "调整优化"
        color = TriColor.YELLOW.value
    else:
        phase = "执行"
        action = "执行推进"
        color = TriColor.GREEN.value

    hex_info = get_hexagram_info(hexagram_id)
    hex_symbol = HEXAGRAM_SYMBOLS.get(hexagram_id, "?")

    dna = f"#龍芯⚡️{now.strftime('%Y%m%d%H%M%S')}-TIME-{hashlib.md5(now.isoformat().encode()).hexdigest()[:8]}"

    nian, yue, ri, shi = 当前四柱(now)

    return {
        "timestamp": now.isoformat(),
        "tiangan": tiangan,
        "dizhi": dizhi,
        "upper": upper,
        "lower": lower,
        "hexagram_id": hexagram_id,
        "hexagram_name": hex_info.get("name", "未知"),
        "hexagram_meaning": hex_info.get("meaning", ""),
        "hexagram_symbol": hex_symbol,
        "entropy": round(entropy, 4),
        "phase": phase,
        "action": action,
        "color": color,
        "dna": dna,
        "upper_name": get_trigram_name(upper),
        "lower_name": get_trigram_name(lower),
        "year_pillar": nian,
        "month_pillar": yue,
        "day_pillar": ri,
        "hour_name": shi,
    }

def get_output_stamp(now: datetime.datetime = None, format_type: str = "full") -> str:
    """
    🔥 核心: 生成输出时间戳
    每句回复都用这个函数生成时间戳尾部
    
    format_type:
      - "full": [丙午·乙未·丙午·申时·䷪夬] 2026-08-02T15:30:00+08:00
      - "compact": #龍芯⚡️丙午·乙未·丙午·申时·䷪夬
      - "simple": 🐉丙午·乙未·丙午·申时·䷪夬
      - "json": JSON格式完整数据
    """
    data = get_time_block(now)
    
    if format_type == "compact":
        return f"#龍芯⚡️{data['year_pillar']}·{data['month_pillar']}·{data['day_pillar']}·{data['hour_name']}·{data['hexagram_symbol']}{data['hexagram_name']}"
    elif format_type == "simple":
        return f"🐉{data['year_pillar']}·{data['month_pillar']}·{data['day_pillar']}·{data['hour_name']}·{data['hexagram_symbol']}{data['hexagram_name']}·{data['color']}"
    elif format_type == "json":
        return json.dumps(data, ensure_ascii=False)
    else:  # full
        ts = now or datetime.datetime.now()
        return (f"[{data['year_pillar']}·{data['month_pillar']}·{data['day_pillar']}·"
                f"{data['hour_name']}·{data['hexagram_symbol']}{data['hexagram_name']}·"
                f"{data['color']}] "
                f"{ts.strftime('%Y-%m-%dT%H:%M:%S+08:00')}")

# ============================================================
# 审计链（区块链式哈希）
# ============================================================

def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def get_last_chain_hash() -> str:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT chain_hash FROM audit_log ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "0" * 64

def create_audit_block(event_type: str, user: str, action_desc: str, shield_level: str = "S0") -> Dict:
    log_id = f"AUDIT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now().isoformat()
    prev_hash = get_last_chain_hash()
    data_body = json.dumps({
        "log_id": log_id, "event_type": event_type, "user": user,
        "action": action_desc, "timestamp": timestamp
    }, sort_keys=True)
    data_hash = sha256_hash(data_body)
    chain_hash = sha256_hash(prev_hash + data_hash)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_log (log_id, event_type, user, action, timestamp, data_hash, prev_hash, chain_hash, shield_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (log_id, event_type, user, action_desc, timestamp, data_hash, prev_hash, chain_hash, shield_level))
    conn.commit()
    conn.close()

    return {"log_id": log_id, "timestamp": timestamp, "event_type": event_type,
            "user": user, "action": action_desc,
            "data_hash": data_hash, "prev_hash": prev_hash[:16] + "...",
            "chain_hash": chain_hash[:16] + "...", "shield_level": shield_level}

def verify_audit_chain() -> Dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, log_id, data_hash, prev_hash, chain_hash FROM audit_log ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"status": "ok", "message": "审计链为空", "verified": True}

    prev_hash = "0" * 64
    for row in rows:
        data_hash, prev_hash_record = row[2], row[3]
        if prev_hash_record != prev_hash:
            return {"status": "broken", "message": "⚠️ 审计链断裂！", "verified": False,
                    "broken_at": row[1]}
        prev_hash = sha256_hash(prev_hash + data_hash)

    return {"status": "ok", "message": "审计链完整 ✅", "verified": True, "total_blocks": len(rows)}

# ============================================================
# Notion API 自动写入
# ============================================================

def write_to_notion(time_data: Dict) -> Dict:
    if not NOTION_TOKEN or not NOTION_DB_TIME:
        return {"status": "skipped", "message": "Notion未配置"}

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "parent": {"database_id": NOTION_DB_TIME},
        "properties": {
            "Title": {"title": [{"text": {"content": time_data["timestamp"]}}]},
            "UpperTrigram": {"number": time_data["upper"]},
            "LowerTrigram": {"number": time_data["lower"]},
            "HexagramID": {"number": time_data["hexagram_id"]},
            "Entropy": {"number": time_data["entropy"]},
            "Action": {"rich_text": [{"text": {"content": time_data["action"]}}]},
            "Phase": {"select": {"name": time_data["phase"]}},
            "DNA": {"rich_text": [{"text": {"content": time_data["dna"]}}]}
        }
    }
    try:
        resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return {"status": "success", "result": resp.json()}
        return {"status": "failed", "error": resp.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
# 任务 & 安全
# ============================================================

def create_task(title: str, time_ref_id: int = None, hexagram_id: int = None, priority: int = 5) -> Dict:
    task_id = f"TASK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_id, title, time_ref_id, hexagram_id, priority, status, execution_mode, version)
        VALUES (?, ?, ?, ?, ?, '待执行', ?, 1)
    ''', (task_id, title, time_ref_id, hexagram_id, priority, "执行"))
    conn.commit()
    conn.close()
    return {"task_id": task_id, "title": title, "status": "待执行"}

def list_tasks(status: str = None) -> List[Dict]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY priority DESC", (status,))
    else:
        cursor.execute("SELECT * FROM tasks ORDER BY priority DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_security_event(event_type: str, severity: str, description: str) -> Dict:
    event_id = f"SEC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    detected_time = datetime.datetime.now().isoformat()
    dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-SEC-{hashlib.md5(event_id.encode()).hexdigest()[:8]}"
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO security_events (event_id, event_type, severity, detected_time, status, dna)
        VALUES (?, ?, ?, ?, '待处理', ?)
    ''', (event_id, event_type, severity, detected_time, dna))
    conn.commit()
    conn.close()
    return {"event_id": event_id, "event_type": event_type, "severity": severity,
            "detected_time": detected_time, "dna": dna, "status": "待处理"}

# ============================================================
# 主引擎
# ============================================================

class TimeEngine:
    def __init__(self):
        if not DB_PATH.exists():
            init_db()
        self.db_path = DB_PATH

    def record_time(self, now: datetime.datetime = None) -> Dict:
        if now is None:
            now = datetime.datetime.now()
        time_data = get_time_block(now)
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO time_records (timestamp, tiangan, dizhi, upper_trigram, lower_trigram, hexagram_id, entropy, phase, action, dna)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (time_data["timestamp"], time_data["tiangan"], time_data["dizhi"],
                  time_data["upper"], time_data["lower"], time_data["hexagram_id"],
                  time_data["entropy"], time_data["phase"], time_data["action"], time_data["dna"]))
            record_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return {"status": "duplicate", "message": "该时间点已记录", "data": time_data}
        conn.close()

        audit = create_audit_block(
            event_type="time_record", user="UID9622",
            action_desc=f"记录时间 {time_data['timestamp']} 卦象: {time_data['hexagram_name']}",
            shield_level="S0")
        notion_result = write_to_notion(time_data)

        if time_data["entropy"] > 0.7:
            create_security_event(event_type="高熵警告", severity="🟡",
                                  description=f"熵值 {time_data['entropy']} > 0.7，系统进入观察模式")

        return {"status": "success", "record_id": record_id, "time_data": time_data,
                "audit": audit, "notion": notion_result}

    def get_hexagram(self, hexagram_id: int) -> Dict:
        info = get_hexagram_info(hexagram_id)
        upper = (hexagram_id - 1) // 8 + 1
        lower = (hexagram_id - 1) % 8 + 1
        return {"hexagram_id": hexagram_id, "name": info.get("name", "未知"),
                "upper": upper, "upper_name": get_trigram_name(upper),
                "lower": lower, "lower_name": get_trigram_name(lower),
                "meaning": info.get("meaning", ""), "phase": info.get("phase", "观察"),
                "action": info.get("action", "谨慎行事"),
                "symbol": HEXAGRAM_SYMBOLS.get(hexagram_id, "?")}

    def get_status(self) -> Dict:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM time_records")
        time_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM audit_log")
        audit_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = '待执行'")
        pending_tasks = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM security_events WHERE status = '待处理'")
        pending_security = cursor.fetchone()[0]
        conn.close()
        return {"total_time_records": time_count, "total_audit_blocks": audit_count,
                "pending_tasks": pending_tasks, "pending_security_events": pending_security,
                "last_record": self.get_last_record()}

    def get_last_record(self) -> Optional[Dict]:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM time_records ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_audit_chain(self, limit: int = 20) -> List[Dict]:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def analyze_trends(self) -> Dict:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT phase, COUNT(*) FROM time_records GROUP BY phase")
        phase_dist = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.execute("SELECT hexagram_id, COUNT(*) FROM time_records GROUP BY hexagram_id ORDER BY COUNT(*) DESC LIMIT 10")
        top_hexagrams = []
        for row in cursor.fetchall():
            hex_id = row[0]
            info = get_hexagram_info(hex_id)
            top_hexagrams.append({"hexagram_id": hex_id, "name": info.get("name", "未知"), "count": row[1]})
        conn.close()
        total = sum(phase_dist.values()) if phase_dist else 0
        return {"total_records": total, "phase_distribution": phase_dist,
                "top_hexagrams": top_hexagrams,
                "execution_rate": phase_dist.get("执行", 0) / total if total > 0 else 0}


# ============================================================
# 便捷 API（全局导入用）
# ============================================================

_engine_singleton = None

def get_engine() -> TimeEngine:
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = TimeEngine()
    return _engine_singleton

def stamp_now(format_type: str = "full") -> str:
    """🔥 全局便捷: 获取当前时间戳"""
    return get_output_stamp(format_type=format_type)

def current_hexagram() -> Dict:
    """🔥 全局便捷: 获取当前卦象"""
    return get_time_block()


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · LU-Time Engine v4.0")
    parser.add_argument("--run", "-r", action="store_true", help="立即执行一次时间记录")
    parser.add_argument("--daemon", "-d", action="store_true", help="启动守护进程（每日定时记录）")
    parser.add_argument("--hexagram", "-H", type=int, help="查询卦象信息")
    parser.add_argument("--audit", "-a", action="store_true", help="查看审计链")
    parser.add_argument("--verify", "-v", action="store_true", help="验证审计链完整性")
    parser.add_argument("--status", "-s", action="store_true", help="查看系统状态")
    parser.add_argument("--sync", "-S", action="store_true", help="同步到Notion（最近一条）")
    parser.add_argument("--analyze", "-A", action="store_true", help="趋势分析")
    parser.add_argument("--tasks", "-t", action="store_true", help="查看待执行任务")
    parser.add_argument("--stamp", action="store_true", help="输出当前时间戳（供其他引擎调用）")
    parser.add_argument("--stamp-compact", action="store_true", help="输出紧凑时间戳")
    parser.add_argument("--stamp-simple", action="store_true", help="输出简单时间戳")
    parser.add_argument("--stamp-json", action="store_true", help="输出JSON完整时间数据")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()

    # 🔥 时间戳输出模式（纯输出，无header）
    if args.stamp:
        print(get_output_stamp(format_type="full"))
        return
    if args.stamp_compact:
        print(get_output_stamp(format_type="compact"))
        return
    if args.stamp_simple:
        print(get_output_stamp(format_type="simple"))
        return
    if args.stamp_json:
        print(get_output_stamp(format_type="json"))
        return

    engine = TimeEngine()

    if args.hexagram:
        info = engine.get_hexagram(args.hexagram)
        if args.json:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n🐉 卦象查询: {args.hexagram}", Colors.BOLD)
            cprint(f"  符号: {info['symbol']}", Colors.CYAN)
            cprint(f"  名称: {info['name']}", Colors.CYAN)
            cprint(f"  上卦: {info['upper_name']} ({info['upper']})", Colors.RESET)
            cprint(f"  下卦: {info['lower_name']} ({info['lower']})", Colors.RESET)
            cprint(f"  含义: {info['meaning']}", Colors.YELLOW)
            cprint(f"  相位: {info['phase']}", Colors.RESET)
            cprint(f"  建议: {info['action']}", Colors.GREEN)
        return

    if args.status:
        status = engine.get_status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📊 系统状态", Colors.BOLD)
            cprint(f"  时间记录: {status['total_time_records']}", Colors.RESET)
            cprint(f"  审计块: {status['total_audit_blocks']}", Colors.RESET)
            cprint(f"  待执行任务: {status['pending_tasks']}", Colors.YELLOW)
            cprint(f"  待处理安全事件: {status['pending_security_events']}", Colors.RED)
            if status['last_record']:
                last = status['last_record']
                cprint(f"\n  最近记录:", Colors.CYAN)
                cprint(f"    时间: {last.get('timestamp')}", Colors.RESET)
                cprint(f"    卦象: {last.get('hexagram_id')} {last.get('phase')}", Colors.RESET)
                cprint(f"    熵值: {last.get('entropy')}", Colors.RESET)
        return

    if args.audit:
        blocks = engine.get_audit_chain(20)
        if args.json:
            print(json.dumps(blocks, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📋 审计链 (最近{len(blocks)}条)", Colors.BOLD)
            for b in blocks:
                cprint(f"  [{b['log_id']}] {b['event_type']} | {b['user']} | {b['action'][:40]}... | {b['chain_hash'][:16]}...", Colors.RESET)
        return

    if args.verify:
        result = verify_audit_chain()
        cprint(f"\n🔍 审计链验证", Colors.BOLD)
        cprint(f"  状态: {result['message']}", Colors.GREEN if result['verified'] else Colors.RED)
        cprint(f"  总块数: {result['total_blocks']}", Colors.RESET)
        return

    if args.tasks:
        tasks = list_tasks("待执行")
        cprint(f"\n📋 待执行任务 ({len(tasks)})", Colors.BOLD)
        for task in tasks:
            cprint(f"  {task['task_id']} | {task['title']} | 优先级: {task['priority']}", Colors.RESET)
        return

    if args.analyze:
        trends = engine.analyze_trends()
        if args.json:
            print(json.dumps(trends, ensure_ascii=False, indent=2))
        else:
            cprint("\n📈 趋势分析", Colors.BOLD)
            cprint(f"  总记录: {trends['total_records']}", Colors.RESET)
            cprint(f"  执行率: {trends['execution_rate']*100:.1f}%", Colors.GREEN)
            cprint("  相位分布:", Colors.CYAN)
            for phase, count in trends['phase_distribution'].items():
                cprint(f"    {phase}: {count}", Colors.RESET)
            cprint("  热门卦象:", Colors.CYAN)
            for h in trends['top_hexagrams'][:5]:
                cprint(f"    {h['hexagram_id']} {h['name']}: {h['count']}次", Colors.RESET)
        return

    if args.sync:
        last = engine.get_last_record()
        if not last:
            cprint("❌ 暂无记录可同步", Colors.RED)
            return
        time_data = {"timestamp": last["timestamp"], "upper": last["upper_trigram"],
                     "lower": last["lower_trigram"], "hexagram_id": last["hexagram_id"],
                     "entropy": last["entropy"], "phase": last["phase"],
                     "action": last["action"], "dna": last["dna"]}
        result = write_to_notion(time_data)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📤 Notion同步", Colors.BOLD)
            cprint(f"  状态: {result.get('status')}", Colors.GREEN if result.get('status') == 'success' else Colors.RED)
        return

    if args.run:
        result = engine.record_time()
        data = result.get("time_data", {})
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n🐉 时间记录", Colors.BOLD)
            cprint(f"  时间: {data.get('timestamp')}", Colors.RESET)
            cprint(f"  卦象: {data.get('hexagram_id')} {data.get('hexagram_name')} {data.get('hexagram_symbol', '')}", Colors.CYAN)
            cprint(f"  干支: {data.get('year_pillar')}·{data.get('month_pillar')}·{data.get('day_pillar')}·{data.get('hour_name')}", Colors.RESET)
            cprint(f"  上卦: {data.get('upper_name')} ({data.get('upper')})", Colors.RESET)
            cprint(f"  下卦: {data.get('lower_name')} ({data.get('lower')})", Colors.RESET)
            cprint(f"  熵值: {data.get('entropy')}", Colors.YELLOW)
            cprint(f"  相位: {data.get('phase')} {data.get('color')}", Colors.RESET)
            cprint(f"  动作: {data.get('action')}", Colors.GREEN)
            cprint(f"\n  审计: {result.get('audit', {}).get('chain_hash', 'N/A')[:16]}...", Colors.BLUE)
        return

    if args.daemon:
        cprint("\n🐉 守护进程启动 (每日定时记录)", Colors.BOLD)
        cprint("  运行中... (按 Ctrl+C 停止)", Colors.CYAN)
        cprint("\n🔄 立即执行首次记录...", Colors.YELLOW)
        result = engine.record_time()
        cprint(f"  ✅ 记录完成: {result.get('time_data', {}).get('hexagram_name', '')}", Colors.GREEN)
        last_day = datetime.datetime.now().day
        while True:
            now = datetime.datetime.now()
            if now.day != last_day:
                cprint(f"\n🔄 每日自动记录: {now.isoformat()}", Colors.YELLOW)
                result = engine.record_time(now)
                cprint(f"  ✅ 记录完成: {result.get('time_data', {}).get('hexagram_name', '')}", Colors.GREEN)
                last_day = now.day
            time.sleep(60)

    if args.interactive:
        cprint("\n🐉 LU-Time Engine v4.0 (交互模式)", Colors.BOLD)
        cprint("命令: record, hex <ID>, status, audit, verify, tasks, analyze, stamp, exit", Colors.CYAN)
        while True:
            try:
                cmd = input("\n🔮 > ").strip()
                if not cmd: continue
                if cmd.lower() in ["exit", "quit"]: break
                if cmd.lower() == "record":
                    result = engine.record_time()
                    cprint(f"  ✅ {result.get('time_data', {}).get('hexagram_name')}", Colors.GREEN)
                elif cmd.startswith("hex "):
                    try:
                        hid = int(cmd[4:].strip())
                        info = engine.get_hexagram(hid)
                        cprint(f"  {info['symbol']} {info['name']} | {info['meaning']} | {info['phase']}", Colors.CYAN)
                    except:
                        cprint("  ❌ 请输入有效的卦象ID", Colors.RED)
                elif cmd.lower() == "stamp":
                    cprint(f"  {get_output_stamp()}", Colors.CYAN)
                elif cmd.lower() == "status":
                    status = engine.get_status()
                    cprint(f"  记录:{status['total_time_records']} | 审计:{status['total_audit_blocks']}", Colors.RESET)
                elif cmd.lower() == "audit":
                    blocks = engine.get_audit_chain(5)
                    for b in blocks:
                        cprint(f"  {b['log_id'][:20]}... | {b['event_type']}", Colors.RESET)
                elif cmd.lower() == "verify":
                    result = verify_audit_chain()
                    cprint(f"  {result['message']}", Colors.GREEN if result['verified'] else Colors.RED)
                elif cmd.lower() == "tasks":
                    tasks = list_tasks("待执行")
                    for task in tasks:
                        cprint(f"  {task['title']} | 优先级: {task['priority']}", Colors.RESET)
                elif cmd.lower() == "analyze":
                    trends = engine.analyze_trends()
                    cprint(f"  执行率: {trends['execution_rate']*100:.1f}%", Colors.GREEN)
                else:
                    cprint("  未知命令", Colors.YELLOW)
            except KeyboardInterrupt:
                break
        return

    parser.print_help()

if __name__ == "__main__":
    main()
