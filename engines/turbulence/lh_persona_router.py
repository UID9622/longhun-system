# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
4.3 16人格矩阵与五维元知路由引擎
===================================
人格矩阵 M ∈ R^{16×5}，场景向量 s⃗ ∈ R⁵，
路由 p* = argmax_p (M·s⃗)_p，
条件分布 P(y|x, p, d) 局部可估。

五维元知空间：军事/历史/哲学/经济/政治

DNA: #龍芯⚡️丙午·乙未·辛酉·井-PERSONA-ROUTER-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


# ── 五维元知基 ────────────────────────────────────
META_KNOWLEDGE_DIMS = ["军事", "历史", "哲学", "经济", "政治"]

# ── 16人格标签 ────────────────────────────────────
PERSONA_LABELS = [
    "P00-文心(意图解析)", "P01-诸葛亮(推演决策)", "P02-宝宝(情感温度)",
    "P03-雯雯(结构归档)", "P04-鲁班(技术执行)", "P05-上帝之眼(审计)",
    "P06-数学大师(权重计算)", "P07-管仲(资源调度)", "P08-仓颉(符号语言)",
    "P09-孙思邈(系统诊断)", "P10-苏东坡(豁达跨界)", "P11-李白(创意爆发)",
    "P12-屈原(价值底线)", "P13-姜子牙(封神权限)", "P14-吕蒙(部署执行)",
    "P15-乔前辈(极简工程)"
]


@dataclass
class PersonaChannel:
    """人格通道"""
    index: int
    label: str
    weight_vector: np.ndarray  # 五维权重 ∈ R⁵
    confidence: float = 1.0    # 通道置信度（随历史验证结果调整）


@dataclass
class RoutingResult:
    """路由结果"""
    persona_index: int
    persona_label: str
    score: float               # (M·s⃗)_p 响应值
    confidence: float          # 路由置信度
    runner_up_indices: List[Tuple[int, float]] = field(default_factory=list)  # 次优通道


class PersonaRouter:
    """
    16人格矩阵路由引擎
    """
    PERSONA_LABELS = PERSONA_LABELS  # 模块级常量暴露为类属性
    META_DIMS = META_KNOWLEDGE_DIMS

    def __init__(self, initial_matrix: Optional[np.ndarray] = None):
        """
        Args:
            initial_matrix: 初始 16×5 人格矩阵，None则用默认分布
        """
        if initial_matrix is not None:
            if initial_matrix.shape != (16, 5):
                raise ValueError(f"人格矩阵必须为 16×5，当前: {initial_matrix.shape}")
            self.M = initial_matrix.copy()
        else:
            self.M = self._default_matrix()
        self.channels: Dict[int, PersonaChannel] = {}
        self._build_channels()

    def _default_matrix(self) -> np.ndarray:
        """
        默认人格矩阵 — 每行对应一个维度的主要倾向
        列序：军事/历史/哲学/经济/政治
        """
        M = np.zeros((16, 5))
        # P00 文心 — 均衡型
        M[0] = [0.20, 0.20, 0.20, 0.20, 0.20]
        # P01 诸葛亮 — 军事主导+历史+哲学
        M[1] = [0.80, 0.10, 0.05, 0.03, 0.02]
        # P02 宝宝 — 人文哲学主导
        M[2] = [0.05, 0.15, 0.70, 0.05, 0.05]
        # P03 雯雯 — 历史+政治（归档）
        M[3] = [0.05, 0.80, 0.05, 0.05, 0.05]
        # P04 鲁班 — 军事+经济（技术执行）
        M[4] = [0.60, 0.05, 0.05, 0.25, 0.05]
        # P05 上帝之眼 — 哲学+政治（审计）
        M[5] = [0.05, 0.10, 0.40, 0.05, 0.40]
        # P06 数学大师 — 哲思+军事（计算）
        M[6] = [0.25, 0.05, 0.60, 0.05, 0.05]
        # P07 管仲 — 经济+政治
        M[7] = [0.05, 0.05, 0.05, 0.75, 0.10]
        # P08 仓颉 — 历史+哲学（符号）
        M[8] = [0.02, 0.43, 0.50, 0.03, 0.02]
        # P09 孙思邈 — 哲学+政治（诊断）
        M[9] = [0.05, 0.15, 0.55, 0.10, 0.15]
        # P10 苏东坡 — 哲思+历史（人文）
        M[10] = [0.02, 0.28, 0.60, 0.05, 0.05]
        # P11 李白 — 哲思+军事（创意）
        M[11] = [0.25, 0.10, 0.55, 0.05, 0.05]
        # P12 屈原 — 政治+哲学（底线）
        M[12] = [0.10, 0.10, 0.30, 0.05, 0.45]
        # P13 姜子牙 — 军事+政治（权限）
        M[13] = [0.55, 0.05, 0.05, 0.05, 0.30]
        # P14 吕蒙 — 军事+经济（部署）
        M[14] = [0.40, 0.05, 0.05, 0.45, 0.05]
        # P15 乔前辈 — 审+哲（签章）
        M[15] = [0.05, 0.10, 0.50, 0.10, 0.25]
        return M

    def _build_channels(self):
        for i in range(16):
            self.channels[i] = PersonaChannel(
                index=i, label=PERSONA_LABELS[i],
                weight_vector=self.M[i].copy()
            )

    def route(self, scene_vector: np.ndarray, top_k: int = 3) -> RoutingResult:
        """
        路由决策：p* = argmax_p (M·s⃗)_p

        Args:
            scene_vector: 五维场景向量 s⃗
            top_k: 返回前 k 个候选通道

        Returns:
            RoutingResult 含主要通道与次优通道
        """
        if len(scene_vector) != 5:
            raise ValueError(f"场景向量必须5维，当前: {len(scene_vector)}")

        s = np.array(scene_vector, dtype=np.float64)
        scores = self.M @ s  # (M·s⃗)ₚ

        # 排序
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        primary_idx, primary_score = ranked[0]

        # 置信度 = 首选/次选之比
        if len(ranked) > 1 and ranked[1][1] > 0:
            confidence = min(1.0, primary_score / (primary_score + ranked[1][1]))
        else:
            confidence = 1.0 if primary_score > 0 else 0.0

        runners_up = [(idx, float(score)) for idx, score in ranked[1:top_k]]

        return RoutingResult(
            persona_index=primary_idx,
            persona_label=PERSONA_LABELS[primary_idx],
            score=float(primary_score),
            confidence=confidence,
            runner_up_indices=runners_up
        )

    def estimate_conditional(self, persona_idx: int, history: List[Tuple[np.ndarray, float]]) -> float:
        """
        局部分布估计 P(y|x, p, d)
        给定人格通道下的历史样本，估计当前输出期望

        Args:
            persona_idx: 人格通道索引
            history: [(scene_vector, observed_outcome), ...]

        Returns:
            该通道下当前场景的期望输出
        """
        if not history:
            return 0.0
        channel_vec = self.M[persona_idx]
        weighted_outputs = []
        for s_vec, outcome in history:
            sim = np.dot(channel_vec, s_vec) / (np.linalg.norm(channel_vec) * np.linalg.norm(s_vec) + 1e-12)
            weighted_outputs.append(outcome * sim)
        return float(np.mean(weighted_outputs)) if weighted_outputs else 0.0

    def update_matrix(self, persona_idx: int, new_weights: np.ndarray):
        """更新指定人格通道的权重（参数自学习调用）"""
        if persona_idx < 0 or persona_idx >= 16:
            raise ValueError(f"人格索引 {persona_idx} 超出范围 [0,15]")
        self.M[persona_idx] = new_weights.copy()
        self.channels[persona_idx].weight_vector = new_weights.copy()

    def scene_to_vector(self, military: float = 0, history: float = 0,
                        philosophy: float = 0, economy: float = 0, politics: float = 0) -> np.ndarray:
        """便捷：场景→向量"""
        return np.array([military, history, philosophy, economy, politics])

    def status_report(self) -> dict:
        return {
            "matrix_shape": list(self.M.shape),
            "dims": META_KNOWLEDGE_DIMS,
            "personas": PERSONA_LABELS,
            "channels": {i: c.confidence for i, c in self.channels.items()}
        }

    def export(self) -> dict:
        return {"M": self.M.tolist(), "channels_confidence": {
            i: c.confidence for i, c in self.channels.items()
        }}


# ── 自检 ──────────────────────────────────────────
if __name__ == "__main__":
    router = PersonaRouter()
    print("🟢 16人格矩阵路由引擎就绪")

    # 场景1：军事主导
    s1 = np.array([0.90, 0.03, 0.03, 0.02, 0.02])
    r1 = router.route(s1)
    print(f"   军事场景 → {r1.persona_label} (score={r1.score:.4f})")

    # 场景2：经济主导
    s2 = np.array([0.02, 0.03, 0.05, 0.85, 0.05])
    r2 = router.route(s2)
    print(f"   经济场景 → {r2.persona_label} (score={r2.score:.4f})")

    # 场景3：政治哲学
    s3 = np.array([0.05, 0.10, 0.40, 0.05, 0.40])
    r3 = router.route(s3)
    print(f"   哲政场景 → {r3.persona_label} (score={r3.score:.4f})")
    print(f"   次优: {[(PERSONA_LABELS[i], f'{s:.4f}') for i, s in r3.runner_up_indices]}")
