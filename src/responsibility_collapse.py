#!/usr/bin/env python3
"""龍魂系统 · 责任塌缩概率模型 v2.0
事不关己 vs 老好人 × 七因子融合
DNA: #龍芯⚡️2026-05-17-RESPONSIBILITY-COLLAPSE-MODEL-v2.0
公开层实现：公式与权重公开，家人具体映射不公开。
License: MulanPSL v2
"""
from __future__ import annotations
import math
from dataclasses import dataclass

GAMMA_FAMILY = {"distant": 1.0, "parent_spouse": 10.0, "child": math.inf}


@dataclass
class Factors:
    F1_risk_cost: float = 0.0        # 风险成本
    F2_reward_visible: float = 0.0   # 可见回报
    F3_social_support: float = 0.0   # 社会支持
    F5_diffusion: float = 0.0        # 责任扩散
    F6_identity: float = 0.0         # 身份认同


def r_coefficient(f: Factors) -> float:
    """R = 0.4·F2 + 0.4·F6 + 0.2·F3 − 0.5·F1 − 0.3·F5"""
    return (0.4 * f.F2_reward_visible + 0.4 * f.F6_identity
            + 0.2 * f.F3_social_support - 0.5 * f.F1_risk_cost
            - 0.3 * f.F5_diffusion)


def p_good_action(p0: float, reward: float, risk: float, x: float = 1.0) -> float:
    """P(善行|环境) = P0 × (reward / risk) ** x，x ∈ [0.5, 3.0]"""
    x = min(max(x, 0.5), 3.0)
    risk = max(risk, 1e-9)
    return min(p0 * (reward / risk) ** x, 1.0)


def r_coerced(r_baseline: float, coercion_strength: float) -> float:
    """胁迫态：R_coerced = R_baseline × (1 − coercion_strength)"""
    c = min(max(coercion_strength, 0.0), 1.0)
    return r_baseline * (1.0 - c)


def r_decay(r0: float, alpha: float, t: float) -> float:
    """时间衰减：R(t) = R0 × e^(−α·t)；L0/L1/L2 → α = 0 / 0.01 / 0.1"""
    return r0 * math.exp(-alpha * t)


def apply_family(r: float, tie: str = "distant") -> float:
    g = GAMMA_FAMILY.get(tie, 1.0)
    return math.inf if g == math.inf else r * g


def tricolor(score: float, green=0.70, yellow=0.40) -> str:
    if score is math.inf or score >= green:
        return "🟢"
    if score >= yellow:
        return "🟡"
    return "🔴"


def sixth_vow_check(external_rule_overwrites_baseline: bool) -> bool:
    """第六誓：我的世界不被规则改写。基线被外部覆盖 → 拒绝并熔断。"""
    if external_rule_overwrites_baseline:
        raise PermissionError("🔴 熔断：外部规则试图覆盖 R_baseline（第六誓）")
    return True


if __name__ == "__main__":
    f = Factors(F1_risk_cost=0.3, F2_reward_visible=0.8,
                F3_social_support=0.5, F5_diffusion=0.6, F6_identity=0.9)
    r = r_coefficient(f)
    print(f"R = {r:.3f}  {tricolor(r)}")
    print(f"P = {p_good_action(0.5, 2.0, 1.0, 1.5):.3f}")
    print(f"R_coerced = {r_coerced(r, 0.7):.3f}")
    print(f"R(t=10, L2) = {r_decay(r, 0.1, 10):.3f}")
    print(f"child tie => {apply_family(r, 'child')}")
