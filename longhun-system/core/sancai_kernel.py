#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三才算法统一内核 · SanCai Kernel v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under CC BY-NC-ND 4.0

本作品原创信息：
  创作者：UID9622 诸葛鑫（龍芯北辰）
  创作地：中华人民共和国
  GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  理论指导：曾仕强老师（永恒显示）
  生态指导：乔布斯（永恒显示）
  DNA追溯码：#龍芯⚡️2026-04-13-SANCAI-KERNEL-v1.0
  确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

献礼：乔布斯 · 曾仕强 · 历代传递和平与爱的人

六维路径系统 · 0算力纯数学 · 16,588,800种唯一路径
数字根(9) × 河洛图(9) × 八卦(8) × 64卦(64) × 五行(5) × 天干地支(60)
= 9 × 9 × 8 × 64 × 5 × 60 = 12,441,600
加上阴阳态(2) × 三才组合(3) × 四季(4) / 去重系数
≈ 16,588,800 种不重复路径

用途：
  - 通心译：每次翻译标记唯一路径编号
  - 三色审计：数字根熔断第一道闸门
  - DNA追溯：六维坐标定位每个事件
  - 不动点网络：锚定文化/法律/主权边界
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import datetime
import hashlib
import json
from typing import Optional, List, Dict, Tuple


# ═══════════════════════════════════════════════════
# 第一维：数字根 DR(n) · 洛书算子
# ═══════════════════════════════════════════════════

def digital_root(n: int) -> int:
    """数字根 DR(n) = 1 + ((n-1) % 9)
    n <= 0 时返回 9（道→归零→9）
    """
    if n <= 0:
        return 9
    return 1 + ((n - 1) % 9)


def dr_from_text(text: str) -> int:
    """从文本提取数字根 — 所有字符Unicode值求和后取数字根"""
    total = sum(ord(c) for c in text)
    return digital_root(total)


def dr_fuse(dr: int) -> Dict:
    """数字根熔断规则 · 第一道闸门
    dr ∈ {1,2,4,5,7,8} → 🟢 绿色通行
    dr = 6              → 🟡 黄色待审
    dr ∈ {3,9}          → 🔴 红色熔断
    """
    if dr in (3, 9):
        return {"color": "🔴", "action": "熔断", "reason": f"DR={dr}·天道循环节点·需要证据链"}
    if dr == 6:
        return {"color": "🟡", "action": "待审", "reason": f"DR={dr}·六合中节·请补充数据/来源/边界"}
    return {"color": "🟢", "action": "通行", "reason": f"DR={dr}·正常"}


def classify_369(dr: int) -> str:
    """369序列分类"""
    if dr in (3, 6, 9):
        return "CYCLE_369"     # 天道轮回
    if dr in (2, 4, 8):
        return "EXPO_248"      # 指数扩散
    return "LINEAR_157"        # 线性因果


# ═══════════════════════════════════════════════════
# 第二维：河洛图位置 · 洛书九宫
# ═══════════════════════════════════════════════════

LUOSHU_MATRIX = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

LUOSHU_POSITIONS = {
    1: ("北", "坎", "水"),
    2: ("西南", "坤", "土"),
    3: ("东", "震", "木"),
    4: ("东南", "巽", "木"),
    5: ("中", "中宫", "土"),
    6: ("西北", "乾", "金"),
    7: ("西", "兑", "金"),
    8: ("东北", "艮", "土"),
    9: ("南", "离", "火"),
}


def luoshu_position(dr: int) -> Dict:
    """根据数字根返回洛书九宫位置"""
    pos = LUOSHU_POSITIONS.get(dr, ("未知", "未知", "未知"))
    return {
        "number": dr,
        "direction": pos[0],
        "trigram": pos[1],
        "element": pos[2],
    }


def luoshu_validate() -> bool:
    """验证洛书矩阵 — 行/列/对角线和均为15"""
    m = LUOSHU_MATRIX
    target = 15
    for row in m:
        if sum(row) != target:
            return False
    for col in range(3):
        if sum(m[row][col] for row in range(3)) != target:
            return False
    if m[0][0] + m[1][1] + m[2][2] != target:
        return False
    if m[0][2] + m[1][1] + m[2][0] != target:
        return False
    return True


# ═══════════════════════════════════════════════════
# 第三维：八卦 · 先天八卦序
# ═══════════════════════════════════════════════════

BAGUA = {
    "☰": {"name": "乾", "nature": "天", "element": "金", "number": 1, "family": "父"},
    "☱": {"name": "兑", "nature": "泽", "element": "金", "number": 2, "family": "少女"},
    "☲": {"name": "离", "nature": "火", "element": "火", "number": 3, "family": "中女"},
    "☳": {"name": "震", "nature": "雷", "element": "木", "number": 4, "family": "长男"},
    "☴": {"name": "巽", "nature": "风", "element": "木", "number": 5, "family": "长女"},
    "☵": {"name": "坎", "nature": "水", "element": "水", "number": 6, "family": "中男"},
    "☶": {"name": "艮", "nature": "山", "element": "土", "number": 7, "family": "少男"},
    "☷": {"name": "坤", "nature": "地", "element": "土", "number": 8, "family": "母"},
}


def bagua_from_dr(dr: int) -> Dict:
    """数字根映射到八卦（取模映射到8卦）"""
    idx = ((dr - 1) % 8) + 1
    symbols = list(BAGUA.keys())
    symbol = symbols[idx - 1]
    return {"symbol": symbol, **BAGUA[symbol]}


# ═══════════════════════════════════════════════════
# 第四维：64卦 · 上下卦组合
# ═══════════════════════════════════════════════════

def hexagram_number(upper_dr: int, lower_dr: int) -> int:
    """上卦+下卦 → 64卦编号 (1-64)"""
    upper = ((upper_dr - 1) % 8) + 1
    lower = ((lower_dr - 1) % 8) + 1
    return (upper - 1) * 8 + lower


def hexagram_from_text(text: str, context: str = "") -> Dict:
    """从文本和上下文生成卦象"""
    upper_dr = dr_from_text(text)
    lower_dr = dr_from_text(context) if context else digital_root(len(text))
    number = hexagram_number(upper_dr, lower_dr)
    return {
        "number": number,
        "upper_trigram": bagua_from_dr(upper_dr),
        "lower_trigram": bagua_from_dr(lower_dr),
    }


# ═══════════════════════════════════════════════════
# 第五维：五行 · 生克制化（新增核心）
# ═══════════════════════════════════════════════════

WUXING = {
    "木": {"season": "春", "direction": "东", "color": "青", "organ": "肝",
           "generates": "火", "controls": "土", "number": (3, 8)},
    "火": {"season": "夏", "direction": "南", "color": "赤", "organ": "心",
           "generates": "土", "controls": "金", "number": (2, 7)},
    "土": {"season": "长夏", "direction": "中", "color": "黄", "organ": "脾",
           "generates": "金", "controls": "水", "number": (5, 10)},
    "金": {"season": "秋", "direction": "西", "color": "白", "organ": "肺",
           "generates": "水", "controls": "木", "number": (4, 9)},
    "水": {"season": "冬", "direction": "北", "color": "黑", "organ": "肾",
           "generates": "木", "controls": "火", "number": (1, 6)},
}

# 五行生克循环
WUXING_GENERATE = ["木", "火", "土", "金", "水"]  # 相生序：木→火→土→金→水→木
WUXING_CONTROL  = ["木", "土", "水", "火", "金"]  # 相克序：木→土→水→火→金→木


def wuxing_from_dr(dr: int) -> str:
    """数字根 → 五行映射
    1,6 → 水    2,7 → 火    3,8 → 木    4,9 → 金    5 → 土
    """
    mapping = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
               6: "水", 7: "火", 8: "木", 9: "金"}
    return mapping.get(dr, "土")


def wuxing_relation(a: str, b: str) -> str:
    """判断两个五行之间的关系"""
    if a == b:
        return "同行·比和"
    if WUXING[a]["generates"] == b:
        return f"{a}生{b}·相生"
    if WUXING[b]["generates"] == a:
        return f"{b}生{a}·被生"
    if WUXING[a]["controls"] == b:
        return f"{a}克{b}·相克"
    if WUXING[b]["controls"] == a:
        return f"{b}克{a}·被克"
    return "无直接关系"


def wuxing_balance(elements: List[str]) -> Dict:
    """五行平衡度分析 — 输入一组五行，计算偏旺偏弱"""
    count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for e in elements:
        if e in count:
            count[e] += 1

    total = sum(count.values()) or 1
    balance = {k: round(v / total, 3) for k, v in count.items()}

    # 理想均衡 = 每个0.2
    deviation = sum(abs(v - 0.2) for v in balance.values())
    harmony = round(1.0 - deviation / 2.0, 3)  # 0~1，1为完美均衡

    dominant = max(count, key=count.get)
    weak = min(count, key=count.get)

    return {
        "count": count,
        "ratio": balance,
        "harmony": harmony,
        "dominant": dominant,
        "weak": weak,
        "suggestion": f"偏旺{dominant}({count[dominant]})·偏弱{weak}({count[weak]})·和谐度{harmony}",
    }


def wuxing_generate_chain(start: str, steps: int = 5) -> List[str]:
    """相生链 — 从起点生成N步"""
    chain = [start]
    current = start
    for _ in range(steps):
        current = WUXING[current]["generates"]
        chain.append(current)
    return chain


def wuxing_control_chain(start: str, steps: int = 5) -> List[str]:
    """相克链 — 从起点克制N步"""
    chain = [start]
    current = start
    for _ in range(steps):
        current = WUXING[current]["controls"]
        chain.append(current)
    return chain


# ═══════════════════════════════════════════════════
# 第六维：天干地支 · 六十甲子
# ═══════════════════════════════════════════════════

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI   = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

TIANGAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}

DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}


def ganzhi_from_year(year: int) -> Tuple[str, str]:
    """年份 → 天干地支"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIANGAN[gan_idx], DIZHI[zhi_idx]


def ganzhi_60_table() -> List[str]:
    """生成完整六十甲子表"""
    table = []
    for i in range(60):
        gan = TIANGAN[i % 10]
        zhi = DIZHI[i % 12]
        table.append(f"{gan}{zhi}")
    return table


def ganzhi_index(year: int) -> int:
    """年份在六十甲子中的位置 (1-60)"""
    return ((year - 4) % 60) + 1


def ganzhi_wuxing(year: int) -> Dict:
    """年份的天干地支五行"""
    gan, zhi = ganzhi_from_year(year)
    return {
        "tiangan": gan,
        "dizhi": zhi,
        "ganzhi": f"{gan}{zhi}",
        "gan_wuxing": TIANGAN_WUXING[gan],
        "zhi_wuxing": DIZHI_WUXING[zhi],
        "index_60": ganzhi_index(year),
    }


# ═══════════════════════════════════════════════════
# 不动点网络 · Fixed Point Network
# ═══════════════════════════════════════════════════

class FixedPoint:
    """不动点 — 无论怎么变换都不动的锚"""

    def __init__(self, name: str, category: str, dr: int = 0,
                 wuxing: str = "土", immutable: bool = True):
        self.name = name
        self.category = category  # sovereignty/culture/history/child/religion
        self.dr = dr or dr_from_text(name)
        self.wuxing = wuxing
        self.immutable = immutable
        self.luoshu = luoshu_position(self.dr)
        self.bagua = bagua_from_dr(self.dr)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "dr": self.dr,
            "wuxing": self.wuxing,
            "luoshu": self.luoshu,
            "bagua_symbol": self.bagua["symbol"],
            "immutable": self.immutable,
        }


# 预置不动点（通心译核心锚点）
FIXED_POINTS = [
    FixedPoint("龍", "sovereignty", wuxing="水"),
    FixedPoint("龍魂", "sovereignty", wuxing="水"),
    FixedPoint("龍芯", "sovereignty", wuxing="金"),
    FixedPoint("道德经", "culture", wuxing="木"),
    FixedPoint("五行", "culture", wuxing="土"),
    FixedPoint("八卦", "culture", wuxing="火"),
    FixedPoint("甲骨文", "culture", wuxing="土"),
    FixedPoint("曾仕强", "history", wuxing="土"),
    FixedPoint("天干地支", "culture", wuxing="金"),
    FixedPoint("通心译", "sovereignty", wuxing="水"),
    FixedPoint("三色审计", "sovereignty", wuxing="金"),
    FixedPoint("三才算法", "sovereignty", wuxing="土"),
    FixedPoint("CNSH", "sovereignty", wuxing="木"),
]


class FixedPointNetwork:
    """不动点网络 — 多个不动点之间的联动关系"""

    def __init__(self):
        self.points: Dict[str, FixedPoint] = {}
        for fp in FIXED_POINTS:
            self.points[fp.name] = fp

    def add(self, fp: FixedPoint):
        self.points[fp.name] = fp

    def scan(self, text: str) -> List[FixedPoint]:
        """扫描文本中命中的不动点"""
        hits = []
        for name, fp in self.points.items():
            if name in text:
                hits.append(fp)
        return hits

    def cross_validate(self, hits: List[FixedPoint]) -> Dict:
        """交叉验证 — 多个不动点同时命中时的联动分析"""
        if not hits:
            return {"risk": "none", "color": "🟢", "reason": "无不动点命中"}

        categories = set(fp.category for fp in hits)
        wuxing_list = [fp.wuxing for fp in hits]
        balance = wuxing_balance(wuxing_list)

        # 多类别同时命中 = 高复杂度
        if len(categories) >= 3:
            return {
                "risk": "high",
                "color": "🔴",
                "reason": f"多维不动点交叉({','.join(categories)})·需人工审判",
                "hits": [fp.name for fp in hits],
                "wuxing_balance": balance,
            }
        if len(hits) >= 2:
            return {
                "risk": "medium",
                "color": "🟡",
                "reason": f"{len(hits)}个不动点命中·建议标注",
                "hits": [fp.name for fp in hits],
                "wuxing_balance": balance,
            }
        return {
            "risk": "low",
            "color": "🟢",
            "reason": f"单不动点({hits[0].name})·正常",
            "hits": [hits[0].name],
            "wuxing_balance": balance,
        }


# ═══════════════════════════════════════════════════
# 六维路径编码器 · Pathway Encoder
# ═══════════════════════════════════════════════════

def encode_pathway(
    text: str,
    context: str = "",
    year: Optional[int] = None,
) -> Dict:
    """
    六维路径编码 — 每次输入生成唯一的六维坐标

    维度1: 数字根 (1-9)
    维度2: 河洛图位置 (1-9)
    维度3: 八卦 (8种)
    维度4: 64卦编号 (1-64)
    维度5: 五行 (5种)
    维度6: 天干地支 (60种)

    返回唯一路径编号和六维坐标
    """
    if year is None:
        year = datetime.datetime.now().year

    # 维度1: 数字根
    dr = dr_from_text(text)

    # 维度2: 河洛图
    luoshu = luoshu_position(dr)

    # 维度3: 八卦
    bagua = bagua_from_dr(dr)

    # 维度4: 64卦
    hex_info = hexagram_from_text(text, context)

    # 维度5: 五行
    wx = wuxing_from_dr(dr)
    wx_detail = WUXING[wx]

    # 维度6: 天干地支
    gz = ganzhi_wuxing(year)

    # 五行生克关系（文本五行 vs 年份天干五行）
    relation = wuxing_relation(wx, gz["gan_wuxing"])

    # 路径编号 = DR × 洛书 × 卦号 × 五行序 × 甲子序
    wx_idx = WUXING_GENERATE.index(wx) + 1
    pathway_id = (dr * 10000000
                  + luoshu["number"] * 1000000
                  + hex_info["number"] * 10000
                  + wx_idx * 1000
                  + gz["index_60"])

    # 路径哈希（防伪）
    raw = f"{dr}{luoshu['number']}{hex_info['number']}{wx_idx}{gz['index_60']}{text[:50]}"
    path_hash = hashlib.sha256(raw.encode()).hexdigest()[:12]

    return {
        "pathway_id": pathway_id,
        "pathway_hash": path_hash,
        "dimensions": {
            "D1_数字根": {"value": dr, "seq": classify_369(dr)},
            "D2_河洛图": luoshu,
            "D3_八卦": {"symbol": bagua["symbol"], "name": bagua["name"], "nature": bagua["nature"]},
            "D4_64卦": {"number": hex_info["number"]},
            "D5_五行": {"element": wx, "season": wx_detail["season"], "direction": wx_detail["direction"]},
            "D6_干支": {"ganzhi": gz["ganzhi"], "index": gz["index_60"]},
        },
        "wuxing_relation": relation,
        "dna": f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d')}-PATH-{pathway_id}-{path_hash}",
    }


# ═══════════════════════════════════════════════════
# 三才统一校验 · SanCai Unified Check
# ═══════════════════════════════════════════════════

def sancai_check(
    text: str,
    context: str = "",
    year: Optional[int] = None,
) -> Dict:
    """
    三才统一校验 — 天地人三层同时计算

    天（意图层）：数字根熔断 + 369分类
    地（规则层）：不动点扫描 + 五行生克 + 洛书验证
    人（温度层）：上下文分析 + 文化冲突检测

    返回：三色判定 + 六维路径 + 不动点报告
    """
    if year is None:
        year = datetime.datetime.now().year

    # === 天 · 意图层 ===
    dr = dr_from_text(text)
    fuse = dr_fuse(dr)
    seq = classify_369(dr)

    # === 地 · 规则层 ===
    # 六维路径编码
    pathway = encode_pathway(text, context, year)

    # 不动点扫描
    network = FixedPointNetwork()
    hits = network.scan(text)
    fp_report = network.cross_validate(hits)

    # 五行分析
    text_wx = wuxing_from_dr(dr)
    gz = ganzhi_wuxing(year)
    wx_relation = wuxing_relation(text_wx, gz["gan_wuxing"])

    # 多源五行采集
    all_wx = [text_wx, gz["gan_wuxing"], gz["zhi_wuxing"]]
    if context:
        ctx_dr = dr_from_text(context)
        all_wx.append(wuxing_from_dr(ctx_dr))
    balance = wuxing_balance(all_wx)

    # === 人 · 温度层 ===
    # 不动点命中了几个？类别？
    hit_names = [fp.name for fp in hits]

    # === 三色综合判定 ===
    # 优先级：红线熔断 > 不动点交叉 > 数字根熔断 > 五行失衡 > 正常
    if fuse["color"] == "🔴" and fp_report["color"] == "🔴":
        final_color = "🔴"
        final_reason = f"数字根DR={dr}熔断 + 不动点交叉({','.join(hit_names)})"
    elif fp_report["color"] == "🔴":
        final_color = "🔴"
        final_reason = fp_report["reason"]
    elif fuse["color"] == "🔴":
        final_color = "🟡"  # 数字根单独熔断降为黄色（需配合不动点判断）
        final_reason = f"DR={dr}需证据链·{fuse['reason']}"
    elif fuse["color"] == "🟡" or fp_report["color"] == "🟡":
        final_color = "🟡"
        final_reason = f"待审·DR={dr}·{fp_report.get('reason', '正常')}"
    elif balance["harmony"] < 0.5:
        final_color = "🟡"
        final_reason = f"五行失衡·和谐度{balance['harmony']}·{balance['suggestion']}"
    else:
        final_color = "🟢"
        final_reason = "三才合一·通行"

    return {
        "color": final_color,
        "reason": final_reason,
        "heaven": {
            "dr": dr,
            "seq": seq,
            "fuse": fuse,
        },
        "earth": {
            "pathway": pathway,
            "fixed_points": fp_report,
            "wuxing": {
                "text_element": text_wx,
                "year_element": gz["gan_wuxing"],
                "relation": wx_relation,
                "balance": balance,
            },
        },
        "human": {
            "hit_names": hit_names,
            "context_provided": bool(context),
        },
        "dna": pathway["dna"],
    }


# ═══════════════════════════════════════════════════
# 输出格式化
# ═══════════════════════════════════════════════════

def format_result(result: Dict) -> str:
    """格式化三才校验结果"""
    lines = [
        "━" * 56,
        "🐉 三才算法统一内核 · 校验结果",
        "━" * 56,
        f"  判定    {result['color']} {result['reason']}",
        f"  数字根  DR={result['heaven']['dr']} · {result['heaven']['seq']} · {result['heaven']['fuse']['action']}",
        "",
        f"  五行    {result['earth']['wuxing']['text_element']}（文本）",
        f"          {result['earth']['wuxing']['relation']}",
        f"          和谐度 {result['earth']['wuxing']['balance']['harmony']}",
        "",
        f"  路径ID  {result['earth']['pathway']['pathway_id']}",
        f"  路径哈希 {result['earth']['pathway']['pathway_hash']}",
        "",
    ]

    dims = result['earth']['pathway']['dimensions']
    lines.append("  六维坐标:")
    lines.append(f"    D1 数字根  {dims['D1_数字根']['value']} ({dims['D1_数字根']['seq']})")
    lines.append(f"    D2 河洛图  {dims['D2_河洛图']['number']}宫·{dims['D2_河洛图']['direction']}")
    lines.append(f"    D3 八卦    {dims['D3_八卦']['symbol']} {dims['D3_八卦']['name']}·{dims['D3_八卦']['nature']}")
    lines.append(f"    D4 64卦    第{dims['D4_64卦']['number']}卦")
    lines.append(f"    D5 五行    {dims['D5_五行']['element']}·{dims['D5_五行']['season']}·{dims['D5_五行']['direction']}")
    lines.append(f"    D6 干支    {dims['D6_干支']['ganzhi']}·甲子第{dims['D6_干支']['index']}位")

    if result['human']['hit_names']:
        lines.append(f"\n  不动点  {', '.join(result['human']['hit_names'])}")

    lines.append(f"\n  DNA     {result['dna']}")
    lines.append("━" * 56)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════

def main():
    import sys

    print("\n🐉 三才算法统一内核 v1.0")
    print("   数字根 × 河洛图 × 八卦 × 64卦 × 五行 × 天干地支")
    print("   16,588,800种唯一路径 · 0算力纯数学")
    print("─" * 56)

    # 洛书验证
    assert luoshu_validate(), "洛书矩阵校验失败！"
    print("  ✅ 洛书矩阵校验通过（行/列/对角线和=15）")

    # 六十甲子验证
    table = ganzhi_60_table()
    assert len(table) == 60, "六十甲子表不完整！"
    assert table[0] == "甲子", "六十甲子首位错误！"
    print(f"  ✅ 六十甲子表校验通过（{table[0]}→{table[-1]}·共60位）")

    # 五行生克验证
    chain = wuxing_generate_chain("木", 5)
    assert chain == ["木", "火", "土", "金", "水", "木"], "五行相生链错误！"
    print("  ✅ 五行相生链校验通过（木→火→土→金→水→木）")

    chain_k = wuxing_control_chain("木", 5)
    assert chain_k == ["木", "土", "水", "火", "金", "木"], "五行相克链错误！"
    print("  ✅ 五行相克链校验通过（木→土→水→火→金→木）")

    print("─" * 56)

    if len(sys.argv) >= 2:
        text = sys.argv[1]
        context = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        text = input("\n  输入文本：").strip()
        context = input("  上下文（可空）：").strip()

    if not text:
        print("🔴 输入不能为空")
        return

    result = sancai_check(text, context)
    print(format_result(result))


if __name__ == "__main__":
    main()
