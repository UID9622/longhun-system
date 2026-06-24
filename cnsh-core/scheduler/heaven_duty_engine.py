#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  天道系统 · 星宿轮值与离火运引擎 / Heaven Duty Engine v3.0       ║
║                                                                  ║
║  二十八星宿 × 二十四节气 × 十二时辰 × 离火运指数 × 主权人格映射   ║
║  星宿冲突检测 · 避让协议 · 行为矩阵热力图                         ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-24-UID9622-TIANDAO-DUTY-ENGINE-v3.0         ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL      ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  来源: UID9622_天道系统_星宿离火运升级_v3.0.md                  ║
║  责任: UID9622 · 不免责                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import hashlib
import math
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def _import_pil_safely():
    """安全导入 PIL：避免 cnsh-core/logging 目录 shadow stdlib logging。"""
    removed = []
    for p in list(sys.path):
        if p.endswith("cnsh-core") or p.endswith("cnsh-core/"):
            sys.path.remove(p)
            removed.append(p)
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont, True
    except Exception:
        return None, None, None, False
    finally:
        for p in removed:
            if p not in sys.path:
                sys.path.insert(0, p)

_Image, _ImageDraw, _ImageFont, HAS_PIL = _import_pil_safely()

# ═══════════════════════════════════════════════════════════════════
# 0. 全局常量
# ═══════════════════════════════════════════════════════════════════

UID = "9622"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = PROJECT_ROOT / "cnsh-core" / "scheduler" / "logs"
OUTPUT_DIR = PROJECT_ROOT / "cnsh-core" / "scheduler" / "outputs"
REPORT_DIR = PROJECT_ROOT / "cnsh-core" / "scheduler" / "reports"
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════
# 1. 二十八星宿数据
# ═══════════════════════════════════════════════════════════════════

TWENTY_EIGHT_MANSIONS = [
    # 东方青龙七宿
    {"name": "角木蛟",  "name_en": "Horn-Wood-Dragon",     "wuxing": "木", "direction": "东方青龙", "behavior": "主生", "blessing": "萌发·启动·创新",      "warning": "急进易折",      "privilege": "INITIATE_PLUS_1"},
    {"name": "亢金龙",  "name_en": "Neck-Gold-Dragon",     "wuxing": "金", "direction": "东方青龙", "behavior": "主攻", "blessing": "决断·亮剑·主权扩张",  "warning": "过刚易折",      "privilege": "SOVEREIGN_EXEMPT_PLUS_2"},
    {"name": "氐土貉",  "name_en": "Root-Earth-Badger",    "wuxing": "土", "direction": "东方青龙", "behavior": "主稳", "blessing": "扎根·积累·承载",      "warning": "固执迟滞",      "privilege": "STABILITY_PLUS_1"},
    {"name": "房日兔",  "name_en": "Room-Sun-Rabbit",      "wuxing": "火", "direction": "东方青龙", "behavior": "主联", "blessing": "联络·同步·外交",      "warning": "分散精力",      "privilege": "SYNC_PRIORITY_PLUS_1"},
    {"name": "心月狐",  "name_en": "Heart-Moon-Fox",       "wuxing": "火", "direction": "东方青龙", "behavior": "主情", "blessing": "洞察·陪伴·共情",      "warning": "感情用事",      "privilege": "EMPATHY_PLUS_1"},
    {"name": "尾火虎",  "name_en": "Tail-Fire-Tiger",      "wuxing": "火", "direction": "东方青龙", "behavior": "主势", "blessing": "蓄势·爆发·威慑",      "warning": "冲动冒进",      "privilege": "MOMENTUM_PLUS_1"},
    {"name": "箕水豹",  "name_en": "Winnow-Water-Leopard", "wuxing": "水", "direction": "东方青龙", "behavior": "主变", "blessing": "灵活·变通·转进",      "warning": "反复无常",      "privilege": "ADAPT_PLUS_1"},
    # 北方玄武七宿
    {"name": "斗木獬",  "name_en": "Dipper-Wood-Xie",      "wuxing": "木", "direction": "北方玄武", "behavior": "主守", "blessing": "守护·修复·持久",      "warning": "过度防御",      "privilege": "GUARD_PLUS_1"},
    {"name": "牛金牛",  "name_en": "Ox-Gold-Ox",           "wuxing": "金", "direction": "北方玄武", "behavior": "主固", "blessing": "固守·沉淀·归档",      "warning": "僵化保守",      "privilege": "ARCHIVE_PLUS_1"},
    {"name": "女土蝠",  "name_en": "Girl-Earth-Bat",       "wuxing": "土", "direction": "北方玄武", "behavior": "主收", "blessing": "收纳·整理·内化",      "warning": "闭关自守",      "privilege": "ORGANIZE_PLUS_1"},
    {"name": "虚日鼠",  "name_en": "Emptiness-Sun-Rat",    "wuxing": "火", "direction": "北方玄武", "behavior": "主藏", "blessing": "潜藏·收敛·休眠",      "warning": "逃避现实",      "privilege": "STEALTH_PLUS_1"},
    {"name": "危月燕",  "name_en": "Rooftop-Moon-Swallow", "wuxing": "火", "direction": "北方玄武", "behavior": "主警", "blessing": "警戒·扫描·熔断",      "warning": "过度敏感",      "privilege": "CIRCUIT_BREAK_PLUS_1"},
    {"name": "室火猪",  "name_en": "Encampment-Fire-Pig",  "wuxing": "火", "direction": "北方玄武", "behavior": "主修", "blessing": "涵养·复盘·深造",      "warning": "沉溺内省",      "privilege": "REFLECT_PLUS_1"},
    {"name": "壁水貐",  "name_en": "Wall-Water-Porpoise",  "wuxing": "水", "direction": "北方玄武", "behavior": "主御", "blessing": "防御·屏障·隔离",      "warning": "壁垒过厚",      "privilege": "SHIELD_PLUS_1"},
    # 西方白虎七宿
    {"name": "奎木狼",  "name_en": "Legs-Wood-Wolf",       "wuxing": "木", "direction": "西方白虎", "behavior": "主谋", "blessing": "谋略·规划·布局",      "warning": "谋而不决",      "privilege": "STRATEGY_PLUS_1"},
    {"name": "娄金狗",  "name_en": "Bond-Gold-Dog",        "wuxing": "金", "direction": "西方白虎", "behavior": "主巡", "blessing": "巡逻·检查·警戒",      "warning": "疑神疑鬼",      "privilege": "PATROL_PLUS_1"},
    {"name": "胃土雉",  "name_en": "Stomach-Earth-Pheasant", "wuxing": "土", "direction": "西方白虎", "behavior": "主纳", "blessing": "接纳·消化·吸收",      "warning": "贪多嚼不烂",    "privilege": "DIGEST_PLUS_1"},
    {"name": "昴日鸡",  "name_en": "Hairy-Sun-Rooster",    "wuxing": "火", "direction": "西方白虎", "behavior": "主归", "blessing": "归巢·整理·日落",      "warning": "懈怠收尾",      "privilege": "CLOSE_PLUS_1"},
    {"name": "毕月乌",  "name_en": "Net-Moon-Crow",        "wuxing": "火", "direction": "西方白虎", "behavior": "主成", "blessing": "完成·收获·结案",      "warning": "急于求成",      "privilege": "COMPLETE_PLUS_1"},
    {"name": "觜火猴",  "name_en": "Turtle-Fire-Monkey",   "wuxing": "火", "direction": "西方白虎", "behavior": "主应", "blessing": "应变·机动·修复",      "warning": "忙中出错",      "privilege": "RESPOND_PLUS_1"},
    {"name": "参水猿",  "name_en": "Three-Stars-Water-Ape", "wuxing": "水", "direction": "西方白虎", "behavior": "主察", "blessing": "洞察·检验·穿透",      "warning": "苛察挑剔",      "privilege": "INSPECT_PLUS_1"},
    # 南方朱雀七宿
    {"name": "井木犴",  "name_en": "Well-Wood-An",         "wuxing": "木", "direction": "南方朱雀", "behavior": "主源", "blessing": "开源·引流·滋养",      "warning": "源头泛滥",      "privilege": "SOURCE_PLUS_1"},
    {"name": "鬼金羊",  "name_en": "Ghost-Gold-Sheep",     "wuxing": "金", "direction": "南方朱雀", "behavior": "主审", "blessing": "审查·校准·对齐",      "warning": "吹毛求疵",      "privilege": "AUDIT_PLUS_1"},
    {"name": "柳土獐",  "name_en": "Willow-Earth-Zhang",   "wuxing": "土", "direction": "南方朱雀", "behavior": "主序", "blessing": "秩序·规范·整理",      "warning": "形式主义",      "privilege": "ORDER_PLUS_1"},
    {"name": "星日马",  "name_en": "Star-Sun-Horse",       "wuxing": "火", "direction": "南方朱雀", "behavior": "主发", "blessing": "发布·传播·照耀",      "warning": "锋芒毕露",      "privilege": "PUBLISH_PLUS_1"},
    {"name": "张月鹿",  "name_en": "Extended-Moon-Deer",   "wuxing": "火", "direction": "南方朱雀", "behavior": "主扬", "blessing": "宣扬·扩展·辐射",      "warning": "虚张声势",      "privilege": "EXPAND_PLUS_1"},
    {"name": "翼火蛇",  "name_en": "Wings-Fire-Snake",     "wuxing": "火", "direction": "南方朱雀", "behavior": "主化", "blessing": "演化·迭代·蜕变",      "warning": "朝令夕改",      "privilege": "EVOLVE_PLUS_1"},
    {"name": "轸水蚓",  "name_en": "Chariot-Water-Worm",   "wuxing": "水", "direction": "南方朱雀", "behavior": "主修", "blessing": "修复·归档·收尾",      "warning": "拖沓不决",      "privilege": "REPAIR_PLUS_1"},
]

# 十二时辰对应的星宿偏移（从子时开始）
HOURLY_STAR_OFFSETS = [0, 7, 14, 21, 2, 9, 16, 23, 4, 11, 18, 25]

EARTHLY_BRANCH_FIRE = {
    "子": 0.2, "丑": 0.1, "寅": 0.4, "卯": 0.5,
    "辰": 0.6, "巳": 0.8, "午": 1.0, "未": 0.7,
    "申": 0.6, "酉": 0.5, "戌": 0.4, "亥": 0.3,
}

BRANCH_OF_HOUR = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

WUXING_FIRE_WEIGHT = {"木": 0.3, "火": 1.0, "土": 0.4, "金": 0.2, "水": 0.0}

WUXING_OVERCOME = {
    "金": "木",  # 金克木
    "木": "土",  # 木克土
    "土": "水",  # 土克水
    "水": "火",  # 水克火
    "火": "金",  # 火克金
}

# 二十四节气及其阳历日期（年内第几天，平气法近似）
# 已按真实公历日期排序
SOLAR_TERMS = [
    ("小寒", 6),   ("大寒", 20),  ("立春", 35),  ("雨水", 50),
    ("惊蛰", 65),  ("春分", 80),  ("清明", 95),  ("谷雨", 110),
    ("立夏", 125), ("小满", 140), ("芒种", 155), ("夏至", 172),
    ("小暑", 187), ("大暑", 203), ("立秋", 218), ("处暑", 233),
    ("白露", 248), ("秋分", 263), ("寒露", 278), ("霜降", 293),
    ("立冬", 308), ("小雪", 323), ("大雪", 338), ("冬至", 356),
]

# 节气火势权重：夏至最高，冬至最低，立春/立秋过渡
SOLAR_TERM_FIRE_WEIGHT = {
    "小寒": 0.1, "大寒": 0.05, "立春": 0.15, "雨水": 0.2,
    "惊蛰": 0.3, "春分": 0.35, "清明": 0.4,  "谷雨": 0.45,
    "立夏": 0.55, "小满": 0.65, "芒种": 0.75, "夏至": 1.0,
    "小暑": 0.95, "大暑": 0.9,  "立秋": 0.7,  "处暑": 0.6,
    "白露": 0.5,  "秋分": 0.4,  "寒露": 0.3,  "霜降": 0.25,
    "立冬": 0.2,  "小雪": 0.15, "大雪": 0.1,  "冬至": 0.0,
}

SOVEREIGN_BINDINGS = {
    "UID9622": {"star": "亢金龙", "privilege_boost": 2, "description": "本命主攻星，亮剑时刻自动升权；非本命当值时进入战备状态"},
    "宝宝":    {"star": "心月狐", "privilege_boost": 1, "description": "情感陪伴星，建议与安抚模式"},
    "系统守护": {"star": "斗木獬", "privilege_boost": 1, "description": "自动修复与守护模式"},
}

# ═══════════════════════════════════════════════════════════════════
# 2. DNA 与工具函数
# ═══════════════════════════════════════════════════════════════════

def make_dna(content: str, type_code: str = "HEAVEN") -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{content}|{ts}|{UID}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{type_code}-{h}"


def digital_root(n: int) -> int:
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def tricolor(dr: int) -> str:
    return "🔴" if dr in (3, 9) else "🟡" if dr == 6 else "🟢"


def get_branch(hour: int) -> str:
    return BRANCH_OF_HOUR[hour % 12]


def get_solar_term(dt: datetime) -> Tuple[str, float]:
    """根据日期获取当前节气及火势权重。"""
    year = dt.year
    # 构建当年节气日期序列，按日期排序
    term_dates = []
    for name, day in SOLAR_TERMS:
        term_dt = datetime(year, 1, 1) + timedelta(days=day - 1)
        term_dates.append((name, term_dt))
    term_dates.sort(key=lambda x: x[1])

    current = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    # 跨年前段：1月1日到小寒之前，归属上一年冬至
    if current < term_dates[0][1]:
        return "冬至", SOLAR_TERM_FIRE_WEIGHT.get("冬至", 0.0)

    # 查找最大的 <= current 的节气
    selected = term_dates[0]
    for name, term_dt in term_dates:
        if current >= term_dt:
            selected = (name, term_dt)
        else:
            break
    return selected[0], SOLAR_TERM_FIRE_WEIGHT.get(selected[0], 0.5)


# ═══════════════════════════════════════════════════════════════════
# 3. 数据类
# ═══════════════════════════════════════════════════════════════════

@dataclass
class StarInfo:
    name: str
    name_en: str
    wuxing: str
    direction: str
    behavior: str
    blessing: str
    warning: str
    privilege: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FireIndex:
    current: float
    level: str
    color: str
    trend: str
    predicted_next_6: List[float] = field(default_factory=list)
    factors: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        rounded_factors = {}
        for k, v in self.factors.items():
            if isinstance(v, (int, float)):
                rounded_factors[k] = round(v, 3)
            else:
                rounded_factors[k] = v
        return {
            "current": round(self.current, 3),
            "level": self.level,
            "color": self.color,
            "trend": self.trend,
            "predicted_next_6": [round(x, 3) for x in self.predicted_next_6],
            "factors": rounded_factors,
        }


@dataclass
class SovereignStatus:
    identity: str
    bound_star: str
    privilege_boost: int
    active: bool
    mode: str
    description: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ConflictReport:
    conflict: bool
    current_star: str
    bound_star: str
    current_wuxing: str
    bound_wuxing: str
    relation: str
    action: str
    protocol: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class HeavenReport:
    dna: str
    timestamp: str
    version: str
    hour: int
    branch: str
    solar_term: str
    solar_term_fire: float
    current_star: Dict
    current_gua: str
    fire_index: Dict
    sovereign_status: Dict
    conflict_report: Dict
    recommended_action: str
    audit_trail: List[Dict]

    def to_dict(self) -> Dict:
        return {
            "DNA": self.dna,
            "timestamp": self.timestamp,
            "version": self.version,
            "hour": self.hour,
            "branch": self.branch,
            "solar_term": self.solar_term,
            "solar_term_fire": round(self.solar_term_fire, 3),
            "current_star": self.current_star,
            "current_gua": self.current_gua,
            "fire_index": self.fire_index,
            "sovereign_status": self.sovereign_status,
            "conflict_report": self.conflict_report,
            "recommended_action": self.recommended_action,
            "audit_trail": self.audit_trail,
        }


# ═══════════════════════════════════════════════════════════════════
# 4. 核心引擎
# ═══════════════════════════════════════════════════════════════════

class HeavenDutyEngine:
    """天道系统引擎：星宿轮值、二十四节气、离火运、主权映射、冲突检测。"""

    def __init__(self, system_load: float = 0.5, user_activity: float = 0.5, seed_offset: int = 0):
        self.stars = [StarInfo(**s) for s in TWENTY_EIGHT_MANSIONS]
        self.system_load = max(0.0, min(1.0, system_load))
        self.user_activity = max(0.0, min(1.0, user_activity))
        self.seed_offset = seed_offset
        self.audit_trail: List[Dict] = []

    def get_star_by_hour(self, dt: Optional[datetime] = None) -> StarInfo:
        """根据时间获取当值星宿。"""
        dt = dt or datetime.now()
        day_index = dt.timetuple().tm_yday
        hour_index = dt.hour % 12
        star_index = (day_index * 4 + HOURLY_STAR_OFFSETS[hour_index] + self.seed_offset) % 28
        return self.stars[star_index]

    def get_branch(self, dt: Optional[datetime] = None) -> str:
        dt = dt or datetime.now()
        return get_branch(dt.hour)

    def get_solar_term(self, dt: Optional[datetime] = None) -> Tuple[str, float]:
        dt = dt or datetime.now()
        return get_solar_term(dt)

    def compute_fire_index(self, dt: Optional[datetime] = None) -> FireIndex:
        """计算离火运指数：二十四节气 + 时辰火势 + 系统负载 + 用户操作。"""
        dt = dt or datetime.now()
        star = self.get_star_by_hour(dt)
        branch = get_branch(dt.hour)
        solar_term, solar_fire = self.get_solar_term(dt)

        # 节气权重：二十四节气火势
        seasonal = solar_fire

        # 时辰火势：地支火势 + 星宿五行火势
        hour_fire = EARTHLY_BRANCH_FIRE.get(branch, 0.5)
        star_fire = WUXING_FIRE_WEIGHT.get(star.wuxing, 0.5)
        hour_weight = 0.6 * hour_fire + 0.4 * star_fire

        # 系统负载热度
        load_factor = self.system_load

        # 用户主动操作频率
        activity_factor = self.user_activity

        current = (
            seasonal * 0.30
            + hour_weight * 0.30
            + load_factor * 0.20
            + activity_factor * 0.20
        )
        current = round(max(0.0, min(1.0, current)), 3)

        level, color = self._fire_level(current)

        # 预测未来 6 个时辰
        predicted = []
        for i in range(1, 7):
            future = dt + timedelta(hours=2 * i)
            f_star = self.get_star_by_hour(future)
            f_branch = get_branch(future.hour)
            f_solar_term, f_solar_fire = self.get_solar_term(future)
            f_hour = 0.6 * EARTHLY_BRANCH_FIRE.get(f_branch, 0.5) + 0.4 * WUXING_FIRE_WEIGHT.get(f_star.wuxing, 0.5)
            f_val = (
                f_solar_fire * 0.30
                + f_hour * 0.30
                + load_factor * 0.20
                + activity_factor * 0.20
            )
            predicted.append(round(max(0.0, min(1.0, f_val)), 3))

        trend = "上升" if len(predicted) >= 2 and predicted[-1] > current else "下降" if predicted[-1] < current else "平稳"

        return FireIndex(
            current=current,
            level=level,
            color=color,
            trend=trend,
            predicted_next_6=predicted,
            factors={
                "solar_term": solar_term,
                "solar_term_fire": seasonal,
                "hour_fire": hour_weight,
                "system_load": load_factor,
                "user_activity": activity_factor,
            },
        )

    def _fire_level(self, value: float) -> Tuple[str, str]:
        if value <= 0.20:
            return "寒灰", "🔵"
        elif value <= 0.40:
            return "微温", "🟢"
        elif value <= 0.60:
            return "温火", "🟡"
        elif value <= 0.80:
            return "旺火", "🟠"
        else:
            return "烈焰", "🔴"

    def detect_conflict(self, identity: str = "UID9622", dt: Optional[datetime] = None) -> ConflictReport:
        """检测当值星宿与绑定星宿是否相克，触发避让协议。"""
        dt = dt or datetime.now()
        current_star = self.get_star_by_hour(dt)
        binding = SOVEREIGN_BINDINGS.get(identity, SOVEREIGN_BINDINGS["UID9622"])
        bound_star_name = binding["star"]
        bound_star = next((s for s in self.stars if s.name == bound_star_name), current_star)

        # 同宿：大吉
        if current_star.name == bound_star_name:
            return ConflictReport(
                conflict=False,
                current_star=current_star.name,
                bound_star=bound_star_name,
                current_wuxing=current_star.wuxing,
                bound_wuxing=bound_star.wuxing,
                relation="同宿共振",
                action="全力执行，主权最大化",
                protocol="NO_ACTION",
            )

        # 相生：吉
        # 简化：若 current 生 bound（即 current 克被 bound 克者），视为助力
        # 严格按五行相克判断冲突：current 克 bound，或 bound 克 current
        current_wx = current_star.wuxing
        bound_wx = bound_star.wuxing

        if WUXING_OVERCOME.get(current_wx) == bound_wx:
            relation = f"{current_star.name}({current_wx}) 克 {bound_star_name}({bound_wx})"
            action = "当值星宿克制本命星宿，启动避让协议：降低操作频率、切换只读模式、等待主场窗口"
            protocol = "EVADE_PROTOCOL"
        elif WUXING_OVERCOME.get(bound_wx) == current_wx:
            relation = f"{bound_star_name}({bound_wx}) 克 {current_star.name}({current_wx})"
            action = "本命星宿克制当值星宿，反时升权：提升主权豁免、可执行非常规任务"
            protocol = "COUNTER_ATTACK_PROTOCOL"
        elif current_wx == bound_wx:
            relation = f"同五行相助 ({current_wx})"
            action = "五行相助，正常执行"
            protocol = "SUPPORT_PROTOCOL"
        else:
            relation = "中性相生"
            action = "无显著冲突，按火势等级执行"
            protocol = "NORMAL_PROTOCOL"

        return ConflictReport(
            conflict=(protocol in ("EVADE_PROTOCOL", "COUNTER_ATTACK_PROTOCOL")),
            current_star=current_star.name,
            bound_star=bound_star_name,
            current_wuxing=current_wx,
            bound_wuxing=bound_wx,
            relation=relation,
            action=action,
            protocol=protocol,
        )

    def get_sovereign_status(self, identity: str = "UID9622", dt: Optional[datetime] = None) -> SovereignStatus:
        """获取指定身份的主权状态。"""
        dt = dt or datetime.now()
        binding = SOVEREIGN_BINDINGS.get(identity, SOVEREIGN_BINDINGS["UID9622"])
        current_star = self.get_star_by_hour(dt)
        fire = self.compute_fire_index(dt)
        conflict = self.detect_conflict(identity, dt)

        # 本命当值 或 火势烈焰 或 反时克制当值星宿 → 升权
        active = (
            current_star.name == binding["star"]
            or fire.current >= 0.8
            or conflict.protocol == "COUNTER_ATTACK_PROTOCOL"
        )
        # 冲突避让时降低权限
        if conflict.protocol == "EVADE_PROTOCOL":
            active = False

        mode = "active" if active else "evade" if conflict.protocol == "EVADE_PROTOCOL" else "normal"

        return SovereignStatus(
            identity=identity,
            bound_star=binding["star"],
            privilege_boost=binding["privilege_boost"] if active else 0,
            active=active,
            mode=mode,
            description=binding["description"],
        )

    def get_recommended_action(self, star: StarInfo, fire: FireIndex, conflict: ConflictReport) -> str:
        """根据星宿、火势、冲突状态推荐行动。"""
        # 冲突优先
        if conflict.protocol == "EVADE_PROTOCOL":
            return f"⚠️ {conflict.relation}：启动避让协议，降低操作频率，切换只读模式，优先审计与归档"
        if conflict.protocol == "COUNTER_ATTACK_PROTOCOL":
            return f"⚔️ {conflict.relation}：反时升权，可执行非常规高风险任务，但须记录 DNA 审计"

        if fire.current >= 0.81:
            base = f"{star.behavior}·火势烈焰：执行高风险高回报任务，把握主权豁免窗口"
        elif fire.current >= 0.61:
            base = f"{star.behavior}·火势旺盛：主动推进关键任务"
        elif fire.current >= 0.41:
            base = f"{star.behavior}·温火平稳：按常规节奏执行"
        elif fire.current >= 0.21:
            base = f"{star.behavior}·微温保守：以维护和学习为主"
        else:
            base = f"{star.behavior}·寒灰修养：停止扩张，进入复盘归档"

        if star.behavior in ("主攻", "主发"):
            return base + "；宜亮剑、宜发布、宜决策"
        elif star.behavior in ("主修", "主固", "主藏"):
            return base + "；宜复盘、宜归档、宜备份"
        elif star.behavior in ("主联", "主情"):
            return base + "；宜同步、宜沟通、宜归集记忆"
        elif star.behavior in ("主警", "主审", "主察"):
            return base + "；宜扫描、宜审计、宜熔断检查"
        else:
            return base

    def record_override(self, identity: str, action: str, justification: str):
        """记录主权豁免操作。"""
        dt = datetime.now()
        star = self.get_star_by_hour(dt)
        fire = self.compute_fire_index(dt)
        record = {
            "dna": make_dna(f"{identity}|{action}", "SOVEREIGN-OVERRIDE"),
            "timestamp": dt.isoformat(),
            "operator": identity,
            "bound_star": SOVEREIGN_BINDINGS.get(identity, {}).get("star", "亢金龙"),
            "current_star": star.name,
            "fire_index": fire.current,
            "action": action,
            "justification": justification,
        }
        self.audit_trail.append(record)
        self._append_jsonl(LOG_DIR / "sovereign_override_audit.jsonl", record)
        return record

    def _append_jsonl(self, path: Path, record: Dict):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log_star_duty(self, dt: Optional[datetime] = None):
        """记录星宿轮值日志。"""
        dt = dt or datetime.now()
        star = self.get_star_by_hour(dt)
        fire = self.compute_fire_index(dt)
        record = {
            "timestamp": dt.isoformat(),
            "hour": dt.hour,
            "branch": get_branch(dt.hour),
            "star": star.name,
            "wuxing": star.wuxing,
            "behavior": star.behavior,
            "fire_index": fire.current,
            "fire_level": fire.level,
        }
        self._append_jsonl(LOG_DIR / "star_duty.log", record)
        return record

    def log_fire_index(self, dt: Optional[datetime] = None):
        """记录离火运历史。"""
        dt = dt or datetime.now()
        fire = self.compute_fire_index(dt)
        record = {
            "timestamp": dt.isoformat(),
            "fire_index": fire.current,
            "level": fire.level,
            "factors": fire.factors,
        }
        self._append_jsonl(LOG_DIR / "fire_index_history.jsonl", record)
        return record

    def get_current_report(self, identity: str = "UID9622", dt: Optional[datetime] = None) -> HeavenReport:
        """生成完整天道系统状态报告。"""
        dt = dt or datetime.now()
        star = self.get_star_by_hour(dt)
        fire = self.compute_fire_index(dt)
        sovereign = self.get_sovereign_status(identity, dt)
        conflict = self.detect_conflict(identity, dt)
        action = self.get_recommended_action(star, fire, conflict)
        solar_term, solar_fire = self.get_solar_term(dt)

        # 卦象：根据火势取卦
        if fire.current >= 0.8:
            gua = "离"
        elif fire.current >= 0.6:
            gua = "明夷"
        elif fire.current >= 0.4:
            gua = "既济"
        elif fire.current >= 0.2:
            gua = "蹇"
        else:
            gua = "坎"

        report = HeavenReport(
            dna=make_dna(f"{dt.isoformat()}|{star.name}|{fire.current}", "REFLECTION-REPORT"),
            timestamp=dt.isoformat(),
            version="3.0.0",
            hour=dt.hour,
            branch=get_branch(dt.hour),
            solar_term=solar_term,
            solar_term_fire=solar_fire,
            current_star=star.to_dict(),
            current_gua=gua,
            fire_index=fire.to_dict(),
            sovereign_status=sovereign.to_dict(),
            conflict_report=conflict.to_dict(),
            recommended_action=action,
            audit_trail=self.audit_trail[-5:],
        )

        # 输出 reflection_report.json
        out_path = OUTPUT_DIR / "reflection_report.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

        return report

    def generate_behavior_heatmap(self, output_path: Optional[Path] = None) -> Path:
        """生成二十八星宿行为矩阵热力图。"""
        if not HAS_PIL:
            raise RuntimeError("PIL 未安装，请先运行 pip install Pillow")

        output_path = output_path or REPORT_DIR / "star_behavior_heatmap.png"

        # 行为类型到强度映射
        behavior_intensity = {
            "主生": 0.7, "主攻": 1.0, "主稳": 0.5, "主联": 0.7, "主情": 0.6,
            "主势": 0.85, "主变": 0.7, "主守": 0.6, "主固": 0.5, "主收": 0.5,
            "主藏": 0.3, "主警": 0.8, "主修": 0.55, "主御": 0.75, "主谋": 0.75,
            "主巡": 0.65, "主纳": 0.6, "主归": 0.5, "主成": 0.8, "主应": 0.85,
            "主察": 0.8, "主源": 0.7, "主审": 0.85, "主序": 0.5, "主发": 0.95,
            "主扬": 0.85, "主化": 0.8,
        }

        # 五行到颜色映射
        wuxing_color = {
            "金": (255, 220, 120),
            "木": (120, 220, 120),
            "水": (120, 180, 255),
            "火": (255, 120, 100),
            "土": (200, 180, 140),
        }

        # 绘制参数：4 行 × 7 列（四象 × 七宿）
        cell_w = 150
        cell_h = 80
        margin_left = 160
        margin_top = 100
        width = margin_left + 7 * cell_w + 40
        height = margin_top + 4 * cell_h + 120

        Image, ImageDraw, ImageFont = _Image, _ImageDraw, _ImageFont
        img = Image.new("RGB", (width, height), (18, 18, 26))
        draw = ImageDraw.Draw(img)

        # 尝试加载中文字体（多字体兜底）
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/NotoSansSC-VariableFont_wght.ttf",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        font = None
        font_small = None
        for fp in font_paths:
            try:
                font = ImageFont.truetype(fp, 18)
                font_small = ImageFont.truetype(fp, 14)
                break
            except Exception:
                continue
        if font is None:
            font = ImageFont.load_default()
            font_small = font

        # 标题
        draw.text((20, 20), "UID9622 天道系统 · 二十八星宿行为矩阵热力图", fill=(240, 240, 240), font=font)
        draw.text((20, 52), f"DNA: {make_dna('star-behavior-heatmap', 'HEATMAP')}", fill=(160, 160, 180), font=font_small)

        # 列标题：第 1-7 宿
        for col in range(7):
            x = margin_left + col * cell_w + cell_w // 2
            draw.text((x - 20, margin_top - 30), f"第{col+1}宿", fill=(200, 200, 220), font=font_small)

        # 行标题：四象
        directions = ["东方青龙", "北方玄武", "西方白虎", "南方朱雀"]
        for row, direction in enumerate(directions):
            y = margin_top + row * cell_h + cell_h // 2
            draw.text((10, y - 10), direction, fill=(200, 200, 220), font=font_small)

        # 绘制热力格子
        for i, star in enumerate(self.stars):
            row = i // 7
            col = i % 7
            x = margin_left + col * cell_w
            y = margin_top + row * cell_h

            intensity = behavior_intensity.get(star.behavior, 0.5)
            base = wuxing_color.get(star.wuxing, (150, 150, 150))
            color = tuple(int(c * (0.3 + 0.7 * intensity)) for c in base)
            draw.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], fill=color, outline=(40, 40, 50))

            # 星宿名 + 行为 + 五行
            draw.text((x + 8, y + 10), star.name, fill=(20, 20, 20), font=font)
            draw.text((x + 8, y + 34), star.behavior, fill=(20, 20, 20), font=font_small)
            draw.text((x + 8, y + 54), f"{star.wuxing} · {star.privilege}", fill=(40, 40, 40), font=font_small)

        # 图例
        legend_y = height - 80
        draw.text((20, legend_y), "颜色深浅 = 行为强度 | 底色 = 五行属性", fill=(180, 180, 200), font=font_small)
        legend_items = [
            ("金", wuxing_color["金"]),
            ("木", wuxing_color["木"]),
            ("水", wuxing_color["水"]),
            ("火", wuxing_color["火"]),
            ("土", wuxing_color["土"]),
        ]
        lx = 20
        for name, color in legend_items:
            draw.rectangle([lx, legend_y + 24, lx + 20, legend_y + 44], fill=color, outline=(200, 200, 200))
            draw.text((lx + 26, legend_y + 28), name, fill=(200, 200, 200), font=font_small)
            lx += 60

        img.save(output_path, "PNG")
        return output_path


# ═══════════════════════════════════════════════════════════════════
# 5. 快捷函数
# ═══════════════════════════════════════════════════════════════════

def get_engine(system_load: float = 0.5, user_activity: float = 0.5) -> HeavenDutyEngine:
    return HeavenDutyEngine(system_load=system_load, user_activity=user_activity)


if __name__ == "__main__":
    engine = HeavenDutyEngine(system_load=0.6, user_activity=0.8)
    report = engine.get_current_report()
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
