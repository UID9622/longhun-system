#!/usr/bin/env python3
"""
4.8 参数标定与自学习协议 + 5.2 社会雷诺数
==========================================
三套自学习协议：
  协议一：七因子权重在线更新（梯度下降方向）
  协议二：人格响应矩阵最小二乘标定
  协议三：DNA 阈值自适应收紧-回退滞后回路

5.2 社会雷诺数：
  Re_s = v·L / μ_s
  Re_s < Re_{s,c} 层流态（可推演）/ Re_s ≥ Re_{s,c} 湍流态（降级）

DNA: #龍芯⚡️丙午·乙未·辛酉·井-PARAM-LEARNER-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field
from collections import deque

# ────────────────────────────────────────────────────
# 4.8 参数自学习协议
# ────────────────────────────────────────────────────

class WeightLearner:
    """
    协议一：七因子权重在线自学习

    初始: w_i^(0) = 1/7
    更新: w_i^(n+1) = w_i^(n) + α_n · sgn(-∂e_n/∂w_i) · g_i^(n)
    归一: Σw_i = 1, w_i ≥ 0
    步长: α_n = α_0 / (1+n)
    """

    def __init__(self, n_factors: int = 7, alpha_0: float = 0.05):
        self.n = n_factors
        self.alpha_0 = alpha_0
        self.weights = np.ones(n_factors) / n_factors
        self.iteration = 0
        self.weight_history: List[np.ndarray] = [self.weights.copy()]

    def update(self, factor_contributions: List[float], error: float,
               error_gradient_signs: Optional[List[float]] = None) -> np.ndarray:
        """
        在线更新权重

        Args:
            factor_contributions: g_i^(n) 各因子归一化贡献量 [0,1]
            error: e_n 本次验证误差
            error_gradient_signs: sgn(-∂e/∂w_i) 梯度方向符号（None则用贡献估计）
        """
        self.iteration += 1
        alpha_n = self.alpha_0 / (1 + self.iteration)

        contributions = np.array(factor_contributions, dtype=np.float64)

        if error_gradient_signs is None:
            # 简易启发：高贡献+高误差 → 降权；高贡献+低误差 → 加权
            grad_signs = np.where(
                (contributions > 0.3) & (error > 0.5),
                -1.0,  # 降权
                1.0    # 加权
            )
        else:
            grad_signs = np.array(error_gradient_signs)

        delta = alpha_n * grad_signs * (contributions / max(1e-8, contributions.sum()))
        self.weights += delta
        self.weights = np.abs(self.weights)
        self.weights /= self.weights.sum()
        self.weight_history.append(self.weights.copy())
        return self.weights.copy()

    def convergence_score(self) -> float:
        """权重稳定性评估（越低越稳定）"""
        if len(self.weight_history) < 5:
            return 1.0
        recent = np.array(self.weight_history[-5:])
        return float(np.mean(np.std(recent, axis=0)))

    def export(self) -> dict:
        return {"weights": self.weights.tolist(), "iteration": self.iteration,
                "convergence": self.convergence_score()}


class PersonaMatrixLearner:
    """
    协议二：人格响应矩阵最小二乘标定

    求解: min_M Σ_n || y_n - (M·s⃗_n)_{p*_n} ||²
    只用该通道自己经手的样本拟合
    """

    def __init__(self, n_personas: int = 16, n_dims: int = 5,
                 regularization: float = 0.01):
        self.n_personas = n_personas
        self.n_dims = n_dims
        self.M = np.ones((n_personas, n_dims)) / n_dims  # 初始均匀
        self.reg = regularization
        self.samples: Dict[int, List[Tuple[np.ndarray, float]]] = {
            i: [] for i in range(n_personas)
        }

    def add_sample(self, persona_idx: int, scene_vector: np.ndarray, outcome: float):
        """添加训练样本（该通道经手的推演-验证对）"""
        self.samples[persona_idx].append((
            np.array(scene_vector, dtype=np.float64),
            float(outcome)
        ))

    def fit_persona(self, persona_idx: int) -> np.ndarray:
        """
        对指定人格通道做最小二乘拟合
        M_p = (S^T S + λI)^{-1} S^T y
        """
        samples = self.samples[persona_idx]
        if len(samples) < self.n_dims:
            return self.M[persona_idx].copy()  # 样本不足，保持原值

        S = np.array([s[0] for s in samples])
        y = np.array([s[1] for s in samples])
        ST = S.T
        A = ST @ S + self.reg * np.eye(self.n_dims)
        try:
            b = ST @ y
            new_row = np.linalg.solve(A, b)
            self.M[persona_idx] = new_row
            return new_row
        except np.linalg.LinAlgError:
            return self.M[persona_idx].copy()

    def fit_all(self) -> np.ndarray:
        """拟合全部16条通道"""
        for p in range(self.n_personas):
            self.fit_persona(p)
        return self.M.copy()

    def export(self) -> dict:
        return {"M": self.M.tolist(), "sample_counts": {
            i: len(v) for i, v in self.samples.items()
        }}


class ThresholdController:
    """
    协议三：DNA阈值自适应收紧-回退滞后回路

    收紧: 连续3轮 A(t) 增量 < δ ⇒ ε₀ ← ε₀/2
    回退: 收紧后失败率反弹 > φ ⇒ ε₀ ← 2ε₀
    """

    def __init__(self, epsilon_0: float = 0.15, delta: float = 0.02,
                 phi: float = 0.30):
        self.epsilon_0 = epsilon_0
        self.epsilon_history: List[float] = [epsilon_0]
        self.delta = delta         # 准确率增量阈值
        self.phi = phi             # 失败率容忍上限
        self.plateau_counter = 0   # 平台期计数器
        self.last_action: Optional[str] = None
        self.failure_rate: float = 0.0

    def update(self, accuracy_history: List[float], recent_failure_rate: float) -> Tuple[float, Optional[str]]:
        """
        根据准确率走势决定收紧/回退

        Returns:
            (新阈值, 动作描述)
        """
        if len(accuracy_history) < 4:
            return self.epsilon_0, None

        recent_deltas = [
            accuracy_history[-i] - accuracy_history[-i-1]
            for i in range(1, min(4, len(accuracy_history)))
            if len(accuracy_history) - i - 1 >= 0
        ]

        action = None
        if recent_deltas:
            avg_delta = np.mean(recent_deltas)
            # 平台期检测
            if avg_delta < self.delta:
                self.plateau_counter += 1
                if self.plateau_counter >= 3:
                    # 收紧
                    new_eps = self.epsilon_0 / 2.0
                    if new_eps < 0.01:  # 下界保护
                        new_eps = 0.01
                    self.epsilon_0 = new_eps
                    self.plateau_counter = 0
                    self.last_action = "tighten"
                    action = f"收紧 → ε₀={new_eps:.3f}"
            else:
                self.plateau_counter = 0

        # 回退检查
        if recent_failure_rate > self.phi and self.last_action == "tighten":
            new_eps = self.epsilon_0 * 2.0
            if new_eps > 0.50:
                new_eps = 0.50
            self.epsilon_0 = new_eps
            self.last_action = "relax"
            action = f"回退 → ε₀={new_eps:.3f}"

        self.failure_rate = recent_failure_rate
        self.epsilon_history.append(self.epsilon_0)
        return self.epsilon_0, action

    def export(self) -> dict:
        return {"epsilon_0": self.epsilon_0, "history": self.epsilon_history[-20:],
                "plateau_counter": self.plateau_counter}


# ────────────────────────────────────────────────────
# 5.2 社会雷诺数
# ────────────────────────────────────────────────────

@dataclass
class SocialReynoldsResult:
    """社会雷诺数计算结果"""
    Re_s: float
    Re_c: float                # 临界值
    regime: str                # "laminar" / "turbulent"
    velocity: float            # v 情绪传播速度
    scope: float               # L 影响范围
    damping: float             # μ_s 社会阻尼
    confidence: float          # 推演置信度
    recommendation: str        # 建议动作


class SocialReynolds:
    """
    社会雷诺数引擎

    Re_s = v·L / μ_s
    v: 情绪传播速度（单位时间转发/评论增量）
    L: 事件影响范围（触达人数）
    μ_s: 社会阻尼系数 = 理性讨论占比 × 信息透明度

    层流态 Re_s < Re_c → 可推演
    湍流态 Re_s ≥ Re_c → 触发降级
    """

    def __init__(self, Re_c: Optional[float] = None):
        self.Re_c = Re_c if Re_c is not None else 100.0  # 默认临界值（中位数先验）
        self.history: List[SocialReynoldsResult] = []

    def compute(self, v: float, L: float, rational_ratio: float = 0.3,
                transparency: float = 0.5) -> SocialReynoldsResult:
        """
        计算社会雷诺数

        Args:
            v: 情绪传播速度（转/评/秒）
            L: 影响范围（触达人数）
            rational_ratio: 理性讨论占比 [0,1]
            transparency: 信息透明度 [0,1]
        """
        mu_s = rational_ratio * transparency
        if mu_s < 1e-8:
            mu_s = 1e-8

        Re_s = v * L / mu_s
        regime = "turbulent" if Re_s >= self.Re_c else "laminar"

        if regime == "laminar":
            confidence = max(0.5, 1.0 - Re_s / (2 * self.Re_c))
            recommendation = "常规推演：所有引擎正常运行"
        else:
            confidence = max(0.1, 1.0 - (Re_s - self.Re_c) / Re_s)
            recommendation = "降级协议：仅固化的P2规则服役 · 新推演强制低置信度标注 · 冻结全部历史规则不作删除"

        result = SocialReynoldsResult(
            Re_s=Re_s, Re_c=self.Re_c, regime=regime,
            velocity=v, scope=L, damping=mu_s,
            confidence=confidence, recommendation=recommendation
        )
        self.history.append(result)
        return result

    def calibrate_critical(self, recent_results: List[Tuple[float, bool]]):
        """
        贝叶斯更新临界值 Re_c
        recent_results: [(Re_s, 推演是否正确), ...]
        """
        if not recent_results:
            return
        correct = [r[0] for r in recent_results if r[1]]
        wrong = [r[0] for r in recent_results if not r[1]]
        if correct and wrong:
            new_c = (np.median(correct) + np.median(wrong)) / 2
            self.Re_c = max(1.0, new_c)

    def status_report(self) -> dict:
        if not self.history:
            return {"Re_c": self.Re_c, "latest": None}
        latest = self.history[-1]
        return {
            "Re_c": self.Re_c,
            "latest_Re_s": latest.Re_s,
            "regime": latest.regime,
            "confidence": latest.confidence
        }

    def export(self) -> dict:
        return {"Re_c": self.Re_c, "history": [
            {"Re_s": r.Re_s, "regime": r.regime, "confidence": r.confidence}
            for r in self.history[-20:]
        ]}


# ── 自检 ──────────────────────────────────────────
if __name__ == "__main__":
    print("🟢 参数自学习引擎 + 社会雷诺数 就绪")

    # 权重学习
    wl = WeightLearner()
    new_w = wl.update([0.3, 0.1, 0.5, 0.2, 0.0, 0.4, 0.1], error=0.15)
    print(f"   权重更新: {[f'{x:.3f}' for x in new_w]}, 收敛度={wl.convergence_score():.4f}")

    # 阈值控制
    tc = ThresholdController()
    # 模拟平台期
    acc_hist = [0.6, 0.62, 0.63, 0.63, 0.63, 0.63]
    new_eps, action = tc.update(acc_hist, 0.1)
    print(f"   阈值更新: ε₀={new_eps:.4f}, 动作={action}")

    # 社会雷诺数
    sr = SocialReynolds()
    res = sr.compute(v=500, L=10000, rational_ratio=0.2, transparency=0.4)
    print(f"   社会雷诺数: Re_s={res.Re_s:.1f}, 状态={res.regime}, 置信度={res.confidence:.2f}")
    print(f"   建议: {res.recommendation[:50]}...")
