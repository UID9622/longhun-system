"""
决策引擎 + 三色审计
D(c): risk < θ1 → EXECUTE, θ1 ≤ risk < θ2 → CONDITIONAL, ≥ θ2 → BLOCK
TriColor: 8维指标 → 🟢/🟡/🔴

Author: 诸葛鑫 (UID9622)
"""

import statistics
from typing import List, Dict, Optional
from core import Action, AuditColor, CompositeState, State


ICHING_HEXAGRAMS = {
    (0, 0): ("䷀", "乾", "天行健，自强不息"),
    (1, 1): ("䷁", "坤", "地势坤，厚德载物"),
    (2, 1): ("䷂", "屯", "初始困难，勿轻举"),
    (1, 5): ("䷃", "蒙", "启蒙教育，求知"),
    (4, 6): ("䷦", "蹇", "困境约束，宜等待"),
    (0, 7): ("䷊", "泰", "天地交泰，万物通"),
    (7, 0): ("䷋", "否", "天地不交，阻断"),
    (5, 4): ("䷾", "既济", "已完成，稳固"),
    (7, 7): ("䷿", "未济", "未完成，继续前行"),
}


class DecisionEngine:

    def __init__(self, theta1: float = 0.3, theta2: float = 0.7):
        self.theta1 = theta1
        self.theta2 = theta2

    def decide(self, risk_score: float) -> Action:
        if risk_score < self.theta1:
            return Action.EXECUTE
        if risk_score < self.theta2:
            return Action.CONDITIONAL
        return Action.BLOCK

    def tri_color_audit(self, audit_scores: List[float]) -> AuditColor:
        """
        8维审计指标 → 三色
        🟢: avg ≥ 70 & min ≥ 50 & conf ≥ 0.75
        🔴: avg < 50 or min < 30
        🟡: 其他
        """
        if not audit_scores:
            return AuditColor.YELLOW

        avg  = sum(audit_scores) / len(audit_scores)
        mn   = min(audit_scores)
        std  = statistics.stdev(audit_scores) if len(audit_scores) > 1 else 0
        conf = 1.0 - (std / 100.0)

        if avg >= 70 and mn >= 50 and conf >= 0.75:
            return AuditColor.GREEN
        if avg < 50 or mn < 30:
            return AuditColor.RED
        return AuditColor.YELLOW

    def get_hexagram(self, composite: CompositeState) -> dict:
        states = list(State)
        i = states.index(composite.primary)
        j = states.index(composite.secondary)
        default = ("❓", "未知", "此卦待解")
        symbol, name, meaning = ICHING_HEXAGRAMS.get((i, j), default)
        return {"symbol": symbol, "name": name, "meaning": meaning}

    def explain(
        self,
        composite: CompositeState,
        risk_score: float,
        action: Action,
        audit_color: AuditColor,
        ethical_pass: bool,
        blocked_rules: List[str],
    ) -> str:
        hexagram = self.get_hexagram(composite)
        lines = [
            f"复合状态: {composite}",
            f"卦象: {hexagram['symbol']} {hexagram['name']} — {hexagram['meaning']}",
            f"风险分: {risk_score:.3f}",
            f"决策: {action.value.upper()}",
            f"审计: {audit_color.value}",
        ]
        if not ethical_pass:
            lines.append(f"⚠️ 伦理阻断: {', '.join(blocked_rules)}")
        return " | ".join(lines)
