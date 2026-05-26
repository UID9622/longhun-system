from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ELEMENTS = ["金", "木", "水", "火", "土"]

STEM_TO_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}

BRANCH_TO_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

GENERATE_MAP = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
CONTROL_MAP = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

DIGIT_ROOT_TO_ELEMENT = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}
FUSE_DIGIT_ROOTS = {3, 9}

POSITION_WEIGHTS = {
    "年柱": {"天干": 1.0, "地支": 0.8},
    "月柱": {"天干": 1.5, "地支": 1.2},
    "日柱": {"天干": 2.0, "地支": 1.6},
    "时柱": {"天干": 1.2, "地支": 1.0},
}

OVERFLOW_THRESHOLD = 0.40
CHAIN_BASELINE = 100
CHAIN_BREAK_PENALTY = 15
OVERFLOW_PENALTY = 10
GREEN_THRESHOLD = 80
YELLOW_THRESHOLD = 50

GUA_WEIGHTS = {
    "innovation": 0.30,
    "support": 0.20,
    "response": 0.10,
    "optimization": 0.10,
    "risk": 0.10,
    "expression": 0.05,
    "defense": 0.10,
    "collaboration": 0.05,
}


@dataclass
class Web3DNAPolicy:
    dna: str = "#龍芯⚡️2026-05-24-Web3-DNA-MARKET-v8.1-64GUA-AUDIT-INTEGRATED"
    confirm: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    gpg: str = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def compute_element_strength(four_pillars: dict[str, dict[str, str]]) -> dict[str, Any]:
    scores = {e: 0.0 for e in ELEMENTS}
    for pillar, pair in four_pillars.items():
        weights = POSITION_WEIGHTS.get(pillar, {"天干": 0.0, "地支": 0.0})
        stem = pair.get("天干")
        branch = pair.get("地支")
        if stem in STEM_TO_ELEMENT:
            scores[STEM_TO_ELEMENT[stem]] += weights["天干"]
        if branch in BRANCH_TO_ELEMENT:
            scores[BRANCH_TO_ELEMENT[branch]] += weights["地支"]

    total = sum(scores.values())
    mean = total / 5 if total else 0.0
    variance = sum((v - mean) ** 2 for v in scores.values()) / 5 if total else 0.0
    balance_index = max(0.0, round(1.0 - (variance ** 0.5) / (mean + 0.001), 3)) if total else 0.0

    return {
        "五行得分": scores,
        "最强": max(scores, key=scores.get),
        "最弱": min(scores, key=scores.get),
        "均衡指数": balance_index,
        "缺失五行": [k for k, v in scores.items() if v == 0.0],
    }


def analyze_element_relation(a: str, b: str) -> tuple[str, str]:
    if a == b:
        return "比和", f"{a}遇{b}·同类叠加"
    if GENERATE_MAP.get(a) == b:
        return "相生", f"{a}生{b}"
    if CONTROL_MAP.get(a) == b:
        return "相克", f"{a}克{b}"
    if GENERATE_MAP.get(b) == a:
        return "相泄", f"{b}生{a}反向"
    if CONTROL_MAP.get(b) == a:
        return "相耗", f"{b}克{a}"
    return "无关", f"{a}与{b}无直接生克"


def analyze_cycle_health(scores: dict[str, float]) -> dict[str, Any]:
    order = ["金", "水", "木", "火", "土"]
    warnings: list[str] = []
    health = CHAIN_BASELINE

    for i, source in enumerate(order):
        target = order[(i + 1) % 5]
        if scores.get(source, 0) > 0 and scores.get(target, 0) == 0:
            warnings.append(f"🔴 断链：{source}有力但生不出{target}")
            health -= CHAIN_BREAK_PENALTY

    total = sum(scores.values()) + 0.001
    for element, value in scores.items():
        if value / total > OVERFLOW_THRESHOLD:
            warnings.append(f"🟡 过旺：{element}占比{value / total:.0%}")
            health -= OVERFLOW_PENALTY

    state = "🟢 健康" if health >= GREEN_THRESHOLD else "🟡 待关注" if health >= YELLOW_THRESHOLD else "🔴 需干预"
    return {"链路健康度": max(0, health), "状态": state, "断链预警": warnings}


def compute_digit_root(text: str) -> int:
    digits = [int(c) for c in text if c.isdigit()]
    if not digits:
        return 0
    value = sum(digits)
    while value >= 10:
        value = sum(int(c) for c in str(value))
    return value


def run_fifth_dimension(text: str, four_pillars: dict[str, dict[str, str]] | None = None) -> dict[str, Any]:
    dr = compute_digit_root(text)
    element = DIGIT_ROOT_TO_ELEMENT.get(dr, "土")

    if dr in FUSE_DIGIT_ROOTS:
        return {
            "状态": "🔴 熔断",
            "数字根": dr,
            "五行": element,
            "说明": f"dr={dr}·天道系统熔断",
            "翻译路径": 0,
        }

    strength = compute_element_strength(four_pillars) if four_pillars else None
    return {
        "状态": "🟢 通行" if dr != 6 else "🟡 待审",
        "数字根": dr,
        "五行定位": element,
        "翻译引擎贡献": "第五维度·16,588,800路径中的1/5",
        "四柱分析": strength,
    }


def run_64gua_audit(scores: dict[str, float], confidence: float, violate_values: bool = False) -> dict[str, Any]:
    weighted = sum(scores.get(k, 0.0) * w for k, w in GUA_WEIGHTS.items())
    minimum = min(scores.get(k, 0.0) for k in GUA_WEIGHTS)

    if violate_values or weighted < 50 or minimum < 30 or confidence < 0.60:
        color = "🔴"
        action = "intercept"
    elif weighted < 70 or minimum < 50 or confidence < 0.75:
        color = "🟡"
        action = "conditional_approve"
    else:
        color = "🟢"
        action = "approve"

    return {
        "均分": round(weighted, 2),
        "最低分": minimum,
        "置信度": confidence,
        "颜色": color,
        "动作": action,
    }


def longhun_wuxing_calculator_v2(
    year_stem: str,
    year_branch: str,
    month_stem: str,
    month_branch: str,
    day_stem: str,
    day_branch: str,
    hour_stem: str,
    hour_branch: str,
) -> dict[str, Any]:
    pillars = {
        "年柱": {"天干": year_stem, "地支": year_branch},
        "月柱": {"天干": month_stem, "地支": month_branch},
        "日柱": {"天干": day_stem, "地支": day_branch},
        "时柱": {"天干": hour_stem, "地支": hour_branch},
    }
    strength = compute_element_strength(pillars)
    cycle = analyze_cycle_health(strength["五行得分"])
    return {
        "版本": "v2.0",
        "四柱": pillars,
        "五行强度": strength,
        "链路分析": cycle,
        "DNA追溯": "#龍芯⚡️2026-04-11-五行计算器-v2.0",
    }
