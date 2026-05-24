# -*- coding: utf-8 -*-
"""
三才算法 · 可执行公式层
真源母稿: longhun-algorithms-cnsh-v1.0.md（算法二 + 公式3 + IPA-077 流场角）
可视化母稿: cnsh-core/CNSH · 通心译 · 对齐标准.html  θ=0.35·P(天)+0.15·G(地)+0.50·H(人)
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

CANONICAL_SOURCE = "longhun-algorithms-cnsh-v1.0.md#算法二·三才决策"


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


@dataclass
class SancaiWeights:
    heaven: float = 0.35
    human: float = 0.50
    earth: float = 0.15
    clamped: bool = False
    tricolor_hint: str = "🟢"


@dataclass
class SancaiDecision:
    """计算三才决策(天, 地, 人) 的结构化结果"""

    heaven: float
    earth: float
    human: float
    human_weight_dynamic: float
    composite_score: float
    passed: bool
    advice: str
    complete: bool
    formula: str
    canonical_source: str = CANONICAL_SOURCE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "heaven": self.heaven,
            "earth": self.earth,
            "human": self.human,
            "human_weight_dynamic": self.human_weight_dynamic,
            "composite_score": round(self.composite_score, 6),
            "passed": self.passed,
            "advice": self.advice,
            "complete": self.complete,
            "formula": self.formula,
            "canonical_source": self.canonical_source,
        }


def normalize_sancai_weights(
    heaven: float = 0.35,
    human: float = 0.50,
    earth: float = 0.15,
) -> SancaiWeights:
    """
    流场权重归一（§6.1：人 < 0.34 → 提至 0.34 染黄）
    用于 θ 合成权重，不是决策输入分。
    """
    clamped = False
    hint = "🟢"
    h = human
    if h < 0.34:
        h = 0.34
        clamped = True
        hint = "🟡"
    total = heaven + h + earth
    if abs(total - 1.0) > 1e-6 and total > 0:
        heaven /= total
        h /= total
        earth /= total
    if clamped and h < 0.34:
        h = 0.34
        rest = heaven + earth
        if rest > 0:
            scale = (1.0 - h) / rest
            heaven *= scale
            earth *= scale
        else:
            heaven, earth = 0.33, 0.33
    return SancaiWeights(
        heaven=round(heaven, 4),
        human=round(h, 4),
        earth=round(earth, 4),
        clamped=clamped,
        tricolor_hint=hint,
    )


def compute_sancai_decision(
    heaven: float,
    earth: float,
    human: float,
    *,
    pass_threshold: float = 0.5,
    complete_floor: float = 0.1,
) -> SancaiDecision:
    """
    公式3: sancai(H,E,P) = H×0.25 + E×0.25 + P×max(0.5, 1-(H×0.3+E×0.3))

    天=时势/大环境  地=条件/资源  人=意志/人心/根  ∈ [0,1]
    """
    h = _clamp01(heaven)
    e = _clamp01(earth)
    p = _clamp01(human)

    w_human = max(0.5, 1.0 - (h * 0.3 + e * 0.3))
    score = h * 0.25 + e * 0.25 + p * w_human
    passed = score >= pass_threshold

    if h < 0.3:
        advice = "时势不利，但人心可胜天，建议坚持"
    elif e < 0.3:
        advice = "条件有限，用好人性弥补资源"
    else:
        advice = "三才齐备，可以行动"

    complete = sancai_complete_check(h, e, p, floor=complete_floor)

    return SancaiDecision(
        heaven=h,
        earth=e,
        human=p,
        human_weight_dynamic=round(w_human, 6),
        composite_score=score,
        passed=passed,
        advice=advice,
        complete=complete,
        formula="H×0.25 + E×0.25 + P×max(0.5, 1-(H×0.3+E×0.3))",
    )


def sancai_complete_check(
    heaven: float,
    earth: float,
    human: float,
    *,
    floor: float = 0.1,
) -> bool:
    """三才完整检查：任一维 < floor 则不齐备"""
    h, e, p = _clamp01(heaven), _clamp01(earth), _clamp01(human)
    return h >= floor and e >= floor and p >= floor


def sancai_flow_theta(
    angle_heaven: float,
    angle_earth: float,
    angle_human: float,
    *,
    w_heaven: float = 0.35,
    w_earth: float = 0.15,
    w_human: float = 0.50,
) -> float:
    """
    三才流场角合成（向量加权，与 HTML v8 / IPA-077 一致）
    θ = w天·sin/cos 合成 → 返回 atan2 角度（弧度）
    """
    nw = normalize_sancai_weights(w_heaven, w_human, w_earth)
    wh, wm, we = nw.heaven, nw.human, nw.earth
    sin_x = (
        math.sin(angle_heaven) * wh
        + math.sin(angle_earth) * we
        + math.sin(angle_human) * wm
    )
    cos_x = (
        math.cos(angle_heaven) * wh
        + math.cos(angle_earth) * we
        + math.cos(angle_human) * wm
    )
    return math.atan2(sin_x, cos_x)


def parse_sancai_inputs(tags: Optional[Dict[str, Any]]) -> Tuple[float, float, float]:
    """从 flow tags 读 天/地/人 输入分；缺省则人心偏高（0.5,0.5,0.8）"""
    if not tags:
        return 0.5, 0.5, 0.8

    def _one(*keys: str) -> Optional[float]:
        for k in keys:
            if k in tags and tags[k] is not None:
                try:
                    return float(tags[k])
                except (TypeError, ValueError):
                    continue
        return None

    t = _one("sancai_tian", "天", "heaven_input", "tian")
    d = _one("sancai_di", "地", "earth_input", "di")
    r = _one("sancai_ren", "人", "human_input", "ren")
    if t is not None and d is not None and r is not None:
        return t, d, r
    return 0.5, 0.5, 0.8


def founder_case_37y() -> SancaiDecision:
    """老大37年验算场景（母稿注释 · 断言 score>0.5）"""
    return compute_sancai_decision(0.2, 0.3, 1.0)
