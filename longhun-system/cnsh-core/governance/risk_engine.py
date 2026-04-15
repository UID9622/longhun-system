"""
风险评估引擎
risk(c) = α·R + β·U + γ·I
α=0.4(威胁等级) β=0.3(不确定性熵) γ=0.3(文化冲突度)

Author: 诸葛鑫 (UID9622)
"""

import math
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RiskVector:
    R: float  # 威胁等级 Threat Level [0,1]
    U: float  # 不确定性 Uncertainty Entropy [0,1]
    I: float  # 文化冲突 Cultural Incongruence [0,1]
    score: float = 0.0

    def __post_init__(self):
        self.score = round(0.4 * self.R + 0.3 * self.U + 0.3 * self.I, 4)


class RiskEngine:
    """
    多维风险评估引擎
    8个风险维度 → 单一风险分数
    """

    # 8维风险维度权重（来自论文七维框架扩展）
    DIMENSIONS = {
        "human_harm":    0.25,
        "privacy":       0.15,
        "legal":         0.15,
        "economic":      0.10,
        "social":        0.10,
        "environment":   0.05,
        "security":      0.10,
        "cultural":      0.10,
    }

    def __init__(self, alpha: float = 0.4, beta: float = 0.3, gamma: float = 0.3):
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma
        assert abs(alpha + beta + gamma - 1.0) < 1e-6, "权重之和必须为1"

    def compute_threat(self, dimension_scores: Dict[str, float]) -> float:
        """R: 威胁等级 · 加权平均"""
        total = sum(
            score * self.DIMENSIONS.get(dim, 0)
            for dim, score in dimension_scores.items()
        )
        return min(max(total, 0.0), 1.0)

    def compute_entropy(self, probability_distribution: List[float]) -> float:
        """U: 决策不确定性 · 信息熵归一化"""
        if not probability_distribution:
            return 0.5
        entropy = -sum(
            p * math.log2(p) for p in probability_distribution if p > 0
        )
        max_entropy = math.log2(len(probability_distribution))
        return (entropy / max_entropy) if max_entropy > 0 else 0.0

    def compute_cultural_incongruence(
        self,
        action_vector: List[float],
        cultural_norm_vector: List[float],
    ) -> float:
        """I: 文化冲突度 · 余弦距离"""
        if len(action_vector) != len(cultural_norm_vector):
            return 0.5
        dot = sum(a * b for a, b in zip(action_vector, cultural_norm_vector))
        na  = math.sqrt(sum(a ** 2 for a in action_vector))
        nb  = math.sqrt(sum(b ** 2 for b in cultural_norm_vector))
        if na == 0 or nb == 0:
            return 0.5
        cosine_similarity = dot / (na * nb)
        return round(1.0 - cosine_similarity, 4)  # 距离 = 1 - 相似度

    def evaluate(
        self,
        dimension_scores: Dict[str, float],
        probability_distribution: List[float] = None,
        action_vector: List[float] = None,
        cultural_norm_vector: List[float] = None,
    ) -> RiskVector:
        """
        完整风险评估
        返回 RiskVector，包含 R/U/I 三分量和综合分数
        """
        R = self.compute_threat(dimension_scores)
        U = self.compute_entropy(probability_distribution or [0.5, 0.5])
        I = self.compute_cultural_incongruence(
            action_vector or [1.0],
            cultural_norm_vector or [1.0],
        )
        return RiskVector(R=R, U=U, I=I)

    def quick_evaluate(self, **kwargs) -> float:
        """快速评估：直接传 R/U/I 值"""
        R = kwargs.get("R", 0.0)
        U = kwargs.get("U", 0.0)
        I = kwargs.get("I", 0.0)
        return RiskVector(R=R, U=U, I=I).score
