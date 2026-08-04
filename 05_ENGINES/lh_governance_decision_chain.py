#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-07-25-GOVERNANCE-DECISION-CHAIN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂 · 根治理决策链 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-25-GOVERNANCE-DECISION-CHAIN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# ═══════════════════════════════════════════
# 输入 → 数字根/五行 → 三色闸 → 归一权重 → 加权风险 → 综合分 → 决策 → 行动
#
# 规则：
#   任一环节亮红，整条链熔断、退回；
#   三才主权指数 SI 天 < 0.34 一票熔断；
#   综合分 ≥0.85 放行 · ≥0.60 复核 · <0.60 拦截。
# ═══════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from engines.lh_math_formula_core import (
    AuditColor,
    digital_root,
    dr_gate,
    element_of,
    normalize,
    sovereignty_index,
)


@dataclass
class RiskFactor:
    """风险因子。"""
    name: str
    weight: float          # 原始权重（会归一化）
    risk: float            # 风险值 0~1
    evidence: str = ""     # 证据/说明


@dataclass
class GovernanceInput:
    """治理链输入。"""
    identifier: str                    # 输入标识（如文件名、任务ID）
    tian: float                        # 天维评分（原则/方向）
    di: float                          # 地维评分（落地/执行）
    ren: float                         # 人维评分（人格/伦理）
    risk_factors: List[RiskFactor] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class GovernanceDecisionChain:
    """根治理决策链。"""

    DNA = "#龍芯⚡️2026-07-25-GOVERNANCE-DECISION-CHAIN-v1.0"

    def evaluate(self, inp: GovernanceInput) -> Dict[str, Any]:
        """评估一个输入，返回完整决策链记录。"""
        trace: List[Dict[str, Any]] = []

        # Step 1: 输入
        trace.append({
            "step": "输入",
            "identifier": inp.identifier,
            "天": inp.tian,
            "地": inp.di,
            "人": inp.ren,
        })

        # Step 2: 数字根 / 三色闸
        seed = int(abs(inp.tian * 1000000 + inp.di * 1000 + inp.ren))
        dr = digital_root(seed)
        gate = dr_gate(seed)
        element = element_of(seed)
        trace.append({
            "step": "数字根/五行/三色闸",
            "seed": seed,
            "数字根": dr,
            "五行": element,
            "三色闸": gate.value,
        })

        if gate == AuditColor.RED:
            return self._reject(trace, "数字根触发红色闸门")

        # Step 3: 三才主权指数
        si_result = sovereignty_index(inp.tian, inp.di, inp.ren)
        trace.append({
            "step": "三才主权指数",
            "SI": si_result["SI"],
            "score": si_result["score"],
            "color": si_result["color"].value,
            "veto": si_result["veto"],
            "reason": si_result["reason"],
        })

        if si_result["veto"]:
            return self._reject(trace, si_result["reason"] or "三才指数一票熔断")

        # Step 4: 风险加权
        if inp.risk_factors:
            weights = [f.weight for f in inp.risk_factors]
            risks = [f.risk for f in inp.risk_factors]
            norm_weights = normalize(weights)
            total_risk = sum(w * r for w, r in zip(norm_weights, risks))
        else:
            total_risk = 0.0

        trace.append({
            "step": "加权风险",
            "风险因子数": len(inp.risk_factors),
            "总风险": round(total_risk, 4),
            "因子详情": [
                {"name": f.name, "weight": round(w, 4), "risk": f.risk}
                for f, w in zip(inp.risk_factors, norm_weights if inp.risk_factors else [])
            ],
        })

        # Step 5: 综合分
        score = si_result["score"] * (1 - total_risk)
        score = max(0.0, min(1.0, score))
        color = AuditColor.GREEN if score >= 0.85 else AuditColor.YELLOW if score >= 0.60 else AuditColor.RED
        trace.append({
            "step": "综合分",
            "score": round(score, 4),
            "color": color.value,
        })

        if color == AuditColor.RED:
            return self._reject(trace, "综合分低于 0.60")

        # Step 6: 决策与行动
        if color == AuditColor.GREEN:
            decision, action = "PASS", "放行·执行"
        else:
            decision, action = "REVIEW", "复核·人工确认"

        return {
            "status": "🟢" if color == AuditColor.GREEN else "🟡",
            "decision": decision,
            "action": action,
            "score": round(score, 4),
            "SI": si_result["SI"],
            "color": color.value,
            "trace": trace,
            "DNA": self.DNA,
        }

    def _reject(self, trace: List[Dict], reason: str) -> Dict[str, Any]:
        return {
            "status": "🔴",
            "decision": "REJECT",
            "action": "拦截·退回",
            "score": 0.0,
            "SI": trace[-1].get("SI", 0.0),
            "color": "🔴",
            "trace": trace,
            "reject_reason": reason,
            "DNA": self.DNA,
        }


def demo():
    """演示：低风险输入放行，高风险输入拦截。"""
    print("=" * 60)
    print("🐉 龍魂根治理决策链 · 演示")
    print("=" * 60)

    chain = GovernanceDecisionChain()

    # 案例 1：低风险，放行
    case1 = GovernanceInput(
        identifier="browser-historian-plugin-v2.1",
        tian=0.92, di=0.85, ren=0.88,
        risk_factors=[
            RiskFactor("数据出境风险", 1.0, 0.0, "纯本地，不上传"),
            RiskFactor("代码复杂度", 1.0, 0.1, "中等规模，已审计"),
            RiskFactor("伦理对齐", 1.0, 0.05, "服务人民数据主权"),
        ],
    )
    print("\n案例1: browser-historian 插件")
    res1 = chain.evaluate(case1)
    print(f"  决策: {res1['decision']} | 综合分: {res1['score']} | 行动: {res1['action']}")

    # 案例 2：天维不足，一票熔断
    case2 = GovernanceInput(
        identifier="llama-based-chatbot",
        tian=0.20, di=0.80, ren=0.70,
        risk_factors=[
            RiskFactor("底座合规", 2.0, 0.9, "英文底座 Llama"),
        ],
    )
    print("\n案例2: Llama 底座方案")
    res2 = chain.evaluate(case2)
    print(f"  决策: {res2['decision']} | 综合分: {res2['score']} | 原因: {res2.get('reject_reason')}")

    # 案例 3：风险过高，拦截
    case3 = GovernanceInput(
        identifier="data-sharing-api",
        tian=0.75, di=0.60, ren=0.55,
        risk_factors=[
            RiskFactor("隐私泄露", 2.0, 0.8, "默认上传用户数据"),
            RiskFactor("审计缺失", 1.0, 0.7, "无DNA追溯"),
        ],
    )
    print("\n案例3: 数据共享API")
    res3 = chain.evaluate(case3)
    print(f"  决策: {res3['decision']} | 综合分: {res3['score']} | 原因: {res3.get('reject_reason')}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
