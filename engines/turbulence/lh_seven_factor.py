#!/usr/bin/env python3
"""
4.2 七因子行为密码学引擎
=========================
加权行为指纹 + 余弦相似度阈值判定。
不追求全局公式，用局部可识别性覆盖全局。

核心公式：
  B⃗ = (b₁,...,b₇),  H(B⃗) = Σᵢ wᵢ·hᵢ(bᵢ),  Σwᵢ=1
  sim(A⃗,B⃗) = A⃗·B⃗ / (|A⃗|·|B⃗|)
  同源判定: sim ≥ cos(θ₀)

DNA: #龍芯⚡️丙午·乙未·辛酉·井-SEVEN-FACTOR-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import numpy as np
import hashlib
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict


# ── 七因子定义 ────────────────────────────────────
FACTOR_NAMES = [
    "语言习惯",    # b₁: 措辞风格/句式偏好
    "时间节律",    # b₂: 活跃时段/发文频率
    "情绪基调",    # b₃: 正/负/中性情绪占比
    "交互模式",    # b₄: 转发vs原创vs评论比例
    "话题偏好",    # b₅: 关注领域分布
    "立场稳定",    # b₆: 观点一致性/摇摆度
    "网络拓扑",    # b₇: 社交关系图位置特征
]

FACTOR_CN_NAMES = {
    "linguistic": "语言习惯", "temporal": "时间节律", "emotion": "情绪基调",
    "interaction": "交互模式", "topic": "话题偏好", "stance": "立场稳定",
    "topology": "网络拓扑"
}


@dataclass
class BehaviorFingerprint:
    """行为指纹"""
    vector: np.ndarray      # B⃗ ∈ R⁷
    entity_id: str          # 实体标识
    timestamp: float        # 采集时间
    raw_features: dict = field(default_factory=dict)

    @property
    def norm(self) -> float:
        return float(np.linalg.norm(self.vector))

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "vector": self.vector.tolist(),
            "timestamp": self.timestamp,
            "raw_features": self.raw_features
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BehaviorFingerprint":
        return cls(
            vector=np.array(data["vector"]),
            entity_id=data["entity_id"],
            timestamp=data["timestamp"],
            raw_features=data.get("raw_features", {})
        )


@dataclass
class SimilarityResult:
    """相似度判定结果"""
    sim_score: float           # 余弦相似度
    is_same_source: bool       # 是否同源
    confidence: float          # 置信度
    matched_entity: Optional[str] = None  # 匹配到的实体ID


class SevenFactor:
    """
    七因子行为密码学引擎

    用法:
        sf = SevenFactor(theta_0=0.85)
        fp_a = sf.register("user_001", [0.1, 0.3, 0.5, 0.2, 0.8, 0.4, 0.6])
        fp_b = sf.register("user_002", [0.1, 0.3, 0.5, 0.2, 0.8, 0.4, 0.6])
        result = sf.compare(fp_a, fp_b)  # → is_same_source=True
    """

    def __init__(self, theta_0: float = 0.85, weights: Optional[List[float]] = None):
        """
        Args:
            theta_0: 余弦相似度判定阈值（余弦值，非角度）
            weights: 七因子权重 w₁...w₇，默认等权
        """
        self.theta_0 = theta_0
        self.weights = np.array(weights) if weights else np.ones(7) / 7.0
        self._normalize_weights()
        self.fingerprints: Dict[str, BehaviorFingerprint] = {}
        self.clusters: Dict[str, Set[str]] = defaultdict(set)  # 同源聚类

    def _normalize_weights(self):
        """确保权重和=1，非负"""
        self.weights = np.abs(self.weights)
        s = self.weights.sum()
        if s > 0:
            self.weights /= s
        else:
            self.weights = np.ones(7) / 7.0

    def weighted_hash(self, fp: BehaviorFingerprint) -> str:
        """
        加权指纹哈希 H(B⃗) = Σᵢ wᵢ·hᵢ(bᵢ)
        每维用 SHA256 取前8位再加权组合
        """
        hash_components = []
        for i, (b_i, w_i) in enumerate(zip(fp.vector, self.weights)):
            h = hashlib.sha256(f"{i}:{b_i:.6f}".encode()).hexdigest()[:8]
            weighted_val = int(h, 16) * w_i
            hash_components.append(weighted_val)
        combined = sum(hash_components)
        return hashlib.sha256(str(combined).encode()).hexdigest()[:16]

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        sim(A⃗,B⃗) = cos θ = A⃗·B⃗ / (|A⃗|·|B⃗|)
        """
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na < 1e-12 or nb < 1e-12:
            return 0.0
        return float(np.dot(a, b) / (na * nb))

    def register(self, entity_id: str, features: List[float],
                 raw: Optional[dict] = None) -> BehaviorFingerprint:
        """
        注册行为指纹

        Args:
            entity_id: 实体标识
            features: 七维特征向量 [b₁,...,b₇]
            raw: 原始特征数据（可选）
        """
        vec = np.array(features, dtype=np.float64)
        if len(vec) != 7:
            raise ValueError(f"特征向量必须7维，当前: {len(vec)}")
        import time
        fp = BehaviorFingerprint(
            vector=vec, entity_id=entity_id,
            timestamp=time.time(), raw_features=raw or {}
        )
        self.fingerprints[entity_id] = fp
        return fp

    def compare(self, a: BehaviorFingerprint, b: BehaviorFingerprint) -> SimilarityResult:
        """
        比较两个指纹是否同源
        """
        sim = self.cosine_similarity(a.vector, b.vector)
        is_same = sim >= self.theta_0
        confidence = (sim - self.theta_0) / (1.0 - self.theta_0) if is_same else (self.theta_0 - sim) / self.theta_0
        confidence = max(0.0, min(1.0, confidence))

        return SimilarityResult(
            sim_score=sim, is_same_source=is_same,
            confidence=confidence,
            matched_entity=b.entity_id if is_same else None
        )

    def identify(self, target: BehaviorFingerprint) -> SimilarityResult:
        """
        在已注册指纹中识别目标（返回最佳匹配）
        """
        best_sim, best_id = -1.0, None
        for eid, fp in self.fingerprints.items():
            if eid == target.entity_id:
                continue
            sim = self.cosine_similarity(target.vector, fp.vector)
            if sim > best_sim:
                best_sim, best_id = sim, eid

        if best_sim < 0:
            return SimilarityResult(sim_score=0, is_same_source=False, confidence=0)

        is_same = best_sim >= self.theta_0
        confidence = (best_sim - self.theta_0) / (1.0 - self.theta_0) if is_same else 0
        return SimilarityResult(
            sim_score=best_sim, is_same_source=is_same,
            confidence=max(0.0, min(1.0, confidence)),
            matched_entity=best_id
        )

    def detect_water_army(self, fingerprints: List[BehaviorFingerprint],
                          min_cluster_size: int = 3) -> List[Set[str]]:
        """
        水军检测：高相似度聚类 → 同源批量账号

        Returns:
            聚类列表，每个集合为一组疑似水军
        """
        n = len(fingerprints)
        if n < min_cluster_size:
            return []

        # 构建相似度图
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.cosine_similarity(fingerprints[i].vector, fingerprints[j].vector)
                if sim >= self.theta_0:
                    edges.append((i, j))

        # 连通分量聚类
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[py] = px

        for i, j in edges:
            union(i, j)

        # 分组
        groups = defaultdict(set)
        for i in range(n):
            root = find(i)
            groups[root].add(fingerprints[i].entity_id)

        return [g for g in groups.values() if len(g) >= min_cluster_size]

    def fingerprint_separability(self) -> float:
        """
        评估指纹可分性（条件二检查）
        返回全局分离度 ∈ [0,1]，越高越可分
        """
        if len(self.fingerprints) < 2:
            return 1.0
        ids = list(self.fingerprints.keys())
        sims = []
        for i in range(min(len(ids), 50)):
            for j in range(i + 1, min(len(ids), 50)):
                sims.append(self.cosine_similarity(
                    self.fingerprints[ids[i]].vector,
                    self.fingerprints[ids[j]].vector
                ))
        if not sims:
            return 1.0
        # 高分离度 = 平均相似度低
        avg_sim = np.mean(sims)
        return max(0.0, 1.0 - avg_sim)

    def status_report(self) -> dict:
        return {
            "theta_0": self.theta_0,
            "weights": self.weights.tolist(),
            "registered_fingerprints": len(self.fingerprints),
            "separability": self.fingerprint_separability(),
            "factor_names": FACTOR_NAMES
        }

    def export(self) -> dict:
        return {
            "theta_0": self.theta_0,
            "weights": self.weights.tolist(),
            "fingerprints": {k: v.to_dict() for k, v in self.fingerprints.items()}
        }


# ── 自检 ──────────────────────────────────────────
if __name__ == "__main__":
    sf = SevenFactor(theta_0=0.85)
    print("🟢 七因子行为密码学引擎就绪")
    print(f"   阈值 θ₀={sf.theta_0}, 权重={sf.weights.tolist()}")

    # 演示：同源 vs 异源
    fp1 = sf.register("user_a", [0.1, 0.3, 0.5, 0.2, 0.8, 0.4, 0.6])
    fp2 = sf.register("user_b", [0.11, 0.29, 0.51, 0.19, 0.79, 0.41, 0.59])
    fp3 = sf.register("user_c", [0.9, 0.1, 0.2, 0.8, 0.1, 0.7, 0.3])

    r12 = sf.compare(fp1, fp2)
    r13 = sf.compare(fp1, fp3)
    print(f"   A vs B: sim={r12.sim_score:.4f} 同源={r12.is_same_source}")
    print(f"   A vs C: sim={r13.sim_score:.4f} 同源={r13.is_same_source}")
    print(f"   指纹可分性={sf.fingerprint_separability():.4f}")
