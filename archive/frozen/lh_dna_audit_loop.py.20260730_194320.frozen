#!/usr/bin/env python3
"""
4.6 DNA追溯审计闭环引擎
========================
推演-验证-固化三段循环：

第n次推演 → 生成 ŷ_n + DNA签名 d_n
到期观察 → 获取真实 y_n
验证误差 e_n = |ŷ_n - y_n|
固化条件：e_n < ε₀ 且连续 κ 次成立 → 规则入 P₂
单调性：A(t+1) ≥ A(t)（只增不减）

DNA: #龍芯⚡️丙午·乙未·辛酉·井-DNA-AUDIT-LOOP-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import time
import hashlib
import json
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class ProjectionRecord:
    """单次推演记录"""
    projection_id: str           # 唯一标识
    dna_signature: str           # DNA 签名 d_n
    prediction: Any              # ŷ_n 推演值
    persona_channel: str         # 路由到的人格通道
    anchor_level: int            # 所用锚点层级 3/6/9
    rules_applied: List[str]     # 应用了哪些 P2 规则
    weights_snapshot: List[float]  # 七因子权重快照
    issued_at: float             # 签发时间
    observation_window_days: int = 90  # 观察窗（天）

    # 验证阶段（观察窗到后填入）
    actual_observed: Optional[Any] = None  # y_n 真实观测
    verified_at: Optional[float] = None
    error: Optional[float] = None          # e_n
    is_verified: bool = False
    is_consolidated: bool = False          # 是否已固化入 P2
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "projection_id": self.projection_id, "dna_signature": self.dna_signature,
            "prediction": self.prediction, "persona_channel": self.persona_channel,
            "anchor_level": self.anchor_level, "rules_applied": self.rules_applied,
            "weights_snapshot": self.weights_snapshot, "issued_at": self.issued_at,
            "observation_window_days": self.observation_window_days,
            "actual_observed": self.actual_observed, "verified_at": self.verified_at,
            "error": self.error, "is_verified": self.is_verified,
            "is_consolidated": self.is_consolidated, "notes": self.notes
        }


@dataclass
class AuditTrail:
    """审计轨迹"""
    trail_id: str
    projection_id: str
    event: str                  # 事件描述
    timestamp: float
    metadata: dict = field(default_factory=dict)


class DNAAuditLoop:
    """
    DNA追溯审计闭环引擎

    用法:
        audit = DNAAuditLoop(epsilon_0=0.15, kappa=3)
        proj = audit.issue_projection(prediction, persona_channel, anchor_level, ...)
        # ... 等待观察窗 ...
        audit.verify(proj.projection_id, actual_value)
    """

    def __init__(self, epsilon_0: float = 0.15, kappa: int = 3):
        """
        Args:
            epsilon_0: 固化阈值（相对误差）
            kappa: 固化窗口长度（连续达标次数）
        """
        self.epsilon_0 = epsilon_0
        self.kappa = kappa
        self.projections: Dict[str, ProjectionRecord] = {}
        self.consolidated_rules: List[str] = []   # 已固化规则ID列表
        self.audit_trails: List[AuditTrail] = []
        self.accuracy_history: List[float] = []    # A(t) 准确率序列
        self.total_verified = 0
        self.total_correct = 0

    def _generate_dna(self, projection_id: str, metadata: dict) -> str:
        """生成 DNA 签名 d_n"""
        payload = f"{projection_id}:{json.dumps(metadata, sort_keys=True)}:{time.time()}"
        h = hashlib.sha256(payload.encode()).hexdigest()[:12]
        return f"#龍芯⚡️PROJ-{h}"

    def issue_projection(self, prediction: Any, persona_channel: str,
                         anchor_level: int, rules_applied: List[str],
                         weights: List[float]) -> ProjectionRecord:
        """
        环节一：签发推演 — 输出 ŷ_n + DNA 签名 d_n

        Args:
            prediction: 推演值 ŷ_n
            persona_channel: 人格通道
            anchor_level: 锚点层级
            rules_applied: 应用的 P2 规则列表
            weights: 七因子权重快照

        Returns:
            ProjectionRecord
        """
        pid = f"PROJ-{int(time.time() * 1000)}-{hashlib.sha256(str(prediction).encode()).hexdigest()[:6]}"
        metadata = {
            "persona_channel": persona_channel, "anchor_level": anchor_level,
            "rules_applied": rules_applied, "weights": weights
        }
        dna = self._generate_dna(pid, metadata)

        record = ProjectionRecord(
            projection_id=pid, dna_signature=dna, prediction=prediction,
            persona_channel=persona_channel, anchor_level=anchor_level,
            rules_applied=list(rules_applied),
            weights_snapshot=list(weights),
            issued_at=time.time()
        )
        self.projections[pid] = record
        self._add_trail(pid, "ISSUED", {"prediction": str(prediction), "dna": dna})
        return record

    def verify(self, projection_id: str, actual_value: Any,
               notes: str = "") -> bool:
        """
        环节三+四：对账 & 固化判定

        Args:
            projection_id: 推演ID
            actual_value: 真实观测 y_n

        Returns:
            True 如果满足固化条件
        """
        if projection_id not in self.projections:
            raise ValueError(f"推演记录不存在: {projection_id}")

        record = self.projections[projection_id]
        record.actual_observed = actual_value
        record.verified_at = time.time()
        record.is_verified = True
        record.notes = notes

        # 计算验证误差（兼容数值和类别型预测）
        error = self._compute_error(record.prediction, actual_value)
        record.error = error

        self.total_verified += 1
        if error < self.epsilon_0:
            self.total_correct += 1

        # 更新准确率
        acc = self.total_correct / max(1, self.total_verified)
        self.accuracy_history.append(acc)

        # 检查固化条件: e_n < ε₀ 且连续 κ 次
        should_consolidate = self._check_consolidation(record)
        if should_consolidate:
            record.is_consolidated = True
            rule_id = f"P2-CONSOLIDATED-{record.projection_id}"
            self.consolidated_rules.append(rule_id)
            self._add_trail(projection_id, "CONSOLIDATED",
                           {"error": error, "rule_id": rule_id})
        else:
            self._add_trail(projection_id, "VERIFIED",
                           {"error": error, "consolidated": False})

        return should_consolidate

    def _compute_error(self, prediction: Any, actual: Any) -> float:
        """计算归一化验证误差 e_n = |ŷ_n - y_n|"""
        try:
            if isinstance(prediction, (int, float)) and isinstance(actual, (int, float)):
                denom = max(abs(actual), abs(prediction), 1e-8)
                return min(1.0, abs(prediction - actual) / denom)
            elif isinstance(prediction, str) and isinstance(actual, str):
                return 0.0 if prediction == actual else 1.0
            else:
                return 0.0 if prediction == actual else 1.0
        except Exception:
            return 1.0

    def _check_consolidation(self, current: ProjectionRecord) -> bool:
        """
        固化条件检查：
        e_n < ε₀ 且连续 κ 次推演均满足此条件
        """
        if current.error is None or current.error >= self.epsilon_0:
            return False

        # 按时间排序，检查最近的推演
        sorted_projs = sorted(
            [r for r in self.projections.values() if r.is_verified and r.error is not None],
            key=lambda r: r.verified_at or 0, reverse=True
        )

        consecutive = 0
        for proj in sorted_projs:
            if proj.error < self.epsilon_0:
                consecutive += 1
                if consecutive >= self.kappa:
                    return True
            else:
                break
        return False

    def accuracy(self) -> float:
        """当前准确率 A(t)"""
        return self.total_correct / max(1, self.total_verified)

    def is_monotonic(self) -> bool:
        """
        验证单调性 A(t+1) ≥ A(t)
        由于规则只进不出，理论保证单调非降
        """
        if len(self.accuracy_history) < 2:
            return True
        return all(
            self.accuracy_history[i] >= self.accuracy_history[i-1]
            for i in range(1, len(self.accuracy_history))
        )

    def _add_trail(self, projection_id: str, event: str, metadata: dict):
        self.audit_trails.append(AuditTrail(
            trail_id=f"TRAIL-{len(self.audit_trails):06d}",
            projection_id=projection_id,
            event=event,
            timestamp=time.time(),
            metadata=metadata
        ))

    def trace(self, projection_id: str) -> List[AuditTrail]:
        """DNA追溯：回溯某次推演的完整审计轨迹"""
        return [t for t in self.audit_trails if t.projection_id == projection_id]

    def get_pending_projections(self) -> List[ProjectionRecord]:
        """获取等待验证的推演列表（观察窗未满）"""
        now = time.time()
        pending = []
        for p in self.projections.values():
            if not p.is_verified:
                elapsed_days = (now - p.issued_at) / 86400
                pending.append(p)
        return pending

    def adjust_threshold(self, new_epsilon_0: float = None, new_kappa: int = None):
        """调整固化参数（由参数自学习模块调用）"""
        if new_epsilon_0 is not None:
            self.epsilon_0 = max(0.01, min(1.0, new_epsilon_0))
        if new_kappa is not None:
            self.kappa = max(1, min(10, new_kappa))

    def status_report(self) -> dict:
        return {
            "total_projections": len(self.projections),
            "verified": self.total_verified,
            "consolidated_rules": len(self.consolidated_rules),
            "accuracy": self.accuracy(),
            "epsilon_0": self.epsilon_0,
            "kappa": self.kappa,
            "monotonic": self.is_monotonic(),
            "pending_count": len(self.get_pending_projections()),
            "accuracy_trend": self.accuracy_history[-5:] if self.accuracy_history else []
        }

    def export(self) -> dict:
        return {
            "epsilon_0": self.epsilon_0, "kappa": self.kappa,
            "projections": {k: v.to_dict() for k, v in self.projections.items()},
            "consolidated_rules": self.consolidated_rules,
            "accuracy_history": self.accuracy_history,
            "audit_trails": [
                {"trail_id": t.trail_id, "projection_id": t.projection_id,
                 "event": t.event, "timestamp": t.timestamp, "metadata": t.metadata}
                for t in self.audit_trails
            ]
        }


# ── 自检 ──────────────────────────────────────────
if __name__ == "__main__":
    audit = DNAAuditLoop(epsilon_0=0.2, kappa=3)
    print("🟢 DNA追溯审计闭环引擎就绪")
    print(f"   ε₀={audit.epsilon_0}, κ={audit.kappa}")

    # 演示：签发→验证→固化
    p1 = audit.issue_projection(100, "P01-诸葛亮", 3, ["R-001"], [0.14]*7)
    print(f"   签发: {p1.projection_id} → DNA={p1.dna_signature}")

    # 模拟3次连续验证通过
    audit.verify(p1.projection_id, 98)   # error=0.02 < 0.2
    p2 = audit.issue_projection(200, "P01-诸葛亮", 3, ["R-001"], [0.14]*7)
    audit.verify(p2.projection_id, 195)  # error=0.025 < 0.2
    p3 = audit.issue_projection(300, "P01-诸葛亮", 3, ["R-001"], [0.14]*7)
    should = audit.verify(p3.projection_id, 310)  # error=0.033 < 0.2

    print(f"   固化触发: {should}")
    print(f"   准确率: {audit.accuracy():.4f}, 单调性: {audit.is_monotonic()}")
    print(f"   固化规则数: {len(audit.consolidated_rules)}")
