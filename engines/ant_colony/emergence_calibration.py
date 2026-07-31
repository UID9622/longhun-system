# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·EMERGENCE-CALIBRATOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
E公式参数校准器 v1.0 · EmergenceCalibrator
投喂挑战 P1-A3 落地：参数敏感性分析 + 蒙特卡洛验证 + 稳定性评估

DNA: #龍芯⚡️丙午·辛未·EMERGENCE-CALIBRATOR-v1.0

核心能力:
  1. 参数敏感性分析 — α/β/γ/δ 各 ±0.05 的 E 变化
  2. 蒙特卡洛模拟 — 10000次随机采样验证 E>1.0 的概率分布
  3. 参数空间探索 — 找到最优 (α,β,γ,δ) 组合
  4. 稳定性评估 — E 对输入噪声的鲁棒性

用法:
    python3 engine/ant_colony/emergence_calibration.py run       # 完整校准
    python3 engine/ant_colony/emergence_calibration.py sensitivity  # 只跑敏感性
    python3 engine/ant_colony/emergence_calibration.py monte-carlo  # 只跑蒙特卡洛
    python3 engine/ant_colony/emergence_calibration.py report       # 查看上次报告
"""

import json
import math
import random
import time
import os
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from itertools import product

from engine.ant_colony.fixed_point_bridge import EmergenceCalculator


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·EMERGENCE-CALIBRATOR-v1.0"

# 报告输出路径
REPORT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "emergence_calibration.json"

# 默认参数（来自 L7_数据层/robot_score_calibration.json + 论文）
DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, DEFAULT_DELTA = 0.3, 0.4, 0.2, 0.1


# ═══════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════

@dataclass
class SensitivityResult:
    """单一参数点的敏感性结果"""
    alpha: float
    beta: float
    gamma: float
    delta: float
    E_value: float
    D: float
    I: float
    C: float
    V: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "alpha": round(self.alpha, 4),
            "beta": round(self.beta, 4),
            "gamma": round(self.gamma, 4),
            "delta": round(self.delta, 4),
            "E": round(self.E_value, 4),
            "D": round(self.D, 3),
            "I": round(self.I, 3),
            "C": round(self.C, 3),
            "V": round(self.V, 3),
        }


@dataclass
class CalibrationReport:
    """完整校准报告"""
    dna: str = DNA
    calibrated_at: str = ""
    
    # 敏感性分析
    sensitivity_grid: List[SensitivityResult] = field(default_factory=list)
    most_sensitive_param: str = ""
    sensitivity_rank: List[Tuple[str, float]] = field(default_factory=list)
    
    # 蒙特卡洛
    monte_carlo_samples: int = 0
    E_above_1_prob: float = 0.0
    E_mean: float = 0.0
    E_std: float = 0.0
    E_percentiles: Dict[str, float] = field(default_factory=dict)
    
    # 最优参数
    best_params: Dict[str, float] = field(default_factory=dict)
    best_E: float = 0.0
    
    # 稳定性
    stability_score: float = 0.0
    
    def summary(self) -> str:
        lines = [
            "=" * 60,
            "📐 E公式 · 校准报告",
            "=" * 60,
            f"  校准时间: {self.calibrated_at}",
            f"",
            "── 敏感性分析 ──",
            f"  最敏感参数: {self.most_sensitive_param}",
        ]
        for param, score in self.sensitivity_rank:
            lines.append(f"    {param}: 敏感性={score:.3f}")
        
        lines.extend([
            "",
            "── 蒙特卡洛 (10000样本) ──",
            f"  E > 1.0 概率: {self.E_above_1_prob:.2%}",
            f"  E 均值: {self.E_mean:.4f} ± {self.E_std:.4f}",
            f"  P10={self.E_percentiles.get('p10', 0):.3f}  "
            f"P50={self.E_percentiles.get('p50', 0):.3f}  "
            f"P90={self.E_percentiles.get('p90', 0):.3f}",
            "",
            "── 最优参数 ──",
            f"  α={self.best_params.get('alpha', '?'):.3f}  "
            f"β={self.best_params.get('beta', '?'):.3f}  "
            f"γ={self.best_params.get('gamma', '?'):.3f}  "
            f"δ={self.best_params.get('delta', '?'):.3f}",
            f"  E_max = {self.best_E:.4f}",
            "",
            f"  稳定性评分: {self.stability_score:.2f}/1.0",
            f"  DNA: {self.dna}",
        ])
        return "\n".join(lines)


# ═══════════════════════════════════════════════
# 核心校准器
# ═══════════════════════════════════════════════

class EmergenceCalibrator:
    """
    E公式参数校准器

    E = D^α · I^β · C^γ · V^δ

    目标:
      1. 找出哪个参数对 E 最敏感
      2. 验证 E>1.0 在随机输入下的概率
      3. 找到最优参数组合
    """

    # 输入空间的典型范围
    DEFAULT_INPUTS = {
        "D": 0.937,   # 多样性（16人格+5种群）
        "I": 0.720,   # 交互密度（常态）
        "C": 0.875,   # 一致性
        "V": 0.780,   # 变异容忍
    }

    def __init__(self, inputs: dict[str, Any] = None):
        self.inputs = inputs or self.DEFAULT_INPUTS.copy()
        self.calc = EmergenceCalculator()

    # ── 1. 参数敏感性分析 ──

    def sensitivity_analysis(self, perturbation: float = 0.05) -> List[SensitivityResult]:
        """
        逐一扰动 α/β/γ/δ，观测 E 的变化幅度

        对每个参数：
          - 基准 E₀ = f(α, β, γ, δ)
          - E_high = f(α+Δ, β, γ, δ)
          - E_low = f(α-Δ, β, γ, δ)
          - 敏感性 = |E_high - E_low| / E₀
        """
        D, I, C, V = self.inputs["D"], self.inputs["I"], self.inputs["C"], self.inputs["V"]

        # 基准
        E0 = self._compute_E(DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, DEFAULT_DELTA, D, I, C, V)

        results = []

        # 对每个参数测试 ±perturbation
        params = {
            "alpha": (DEFAULT_ALPHA, perturbation),
            "beta": (DEFAULT_BETA, perturbation),
            "gamma": (DEFAULT_GAMMA, perturbation),
            "delta": (DEFAULT_DELTA, perturbation),
        }

        for param_name, (base_val, delta) in params.items():
            vals = {}
            for pn, (bv, _) in params.items():
                vals[pn] = bv

            # 高估
            vals[param_name] = base_val + delta
            E_high = self._compute_E(**vals, D=D, I=I, C=C, V=V)

            # 低估
            vals[param_name] = base_val - delta
            E_low = self._compute_E(**vals, D=D, I=I, C=C, V=V)

            # 敏感性
            sensitivity = abs(E_high - E_low) / max(E0, 0.001)

            results.append(SensitivityResult(
                alpha=vals["alpha"], beta=vals["beta"],
                gamma=vals["gamma"], delta=vals["delta"],
                E_value=E_high,
                D=D, I=I, C=C, V=V,
            ))
            results.append(SensitivityResult(
                alpha=vals["alpha"], beta=vals["beta"],
                gamma=vals["gamma"], delta=vals["delta"],
                E_value=E_low,
                D=D, I=I, C=C, V=V,
            ))

        return results, E0

    def compute_sensitivity_scores(self) -> List[Tuple[str, float]]:
        """计算各参数敏感性评分"""
        D, I, C, V = self.inputs["D"], self.inputs["I"], self.inputs["C"], self.inputs["V"]
        E0 = self._compute_E(DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, DEFAULT_DELTA, D, I, C, V)

        scores = []
        params = {
            "alpha": DEFAULT_ALPHA,
            "beta": DEFAULT_BETA,
            "gamma": DEFAULT_GAMMA,
            "delta": DEFAULT_DELTA,
        }
        delta = 0.05

        for name, base in params.items():
            vals = params.copy()
            vals[name] = base + delta
            E_high = self._compute_E(**vals, D=D, I=I, C=C, V=V)
            vals[name] = base - delta
            E_low = self._compute_E(**vals, D=D, I=I, C=C, V=V)

            sensitivity = abs(E_high - E_low) / max(E0, 0.001)
            scores.append((name, round(sensitivity, 4)))

        return sorted(scores, key=lambda x: x[1], reverse=True)

    # ── 2. 蒙特卡洛模拟 ──

    def monte_carlo(self, samples: int = 10000,
                    alpha_range: Tuple[float, float] = (0.1, 0.5),
                    beta_range: Tuple[float, float] = (0.2, 0.6),
                    gamma_range: Tuple[float, float] = (0.05, 0.35),
                    delta_range: Tuple[float, float] = (0.02, 0.25),
                    add_input_noise: bool = True) -> Dict[str, Any]:
        """
        蒙特卡洛模拟 E 公式

        - 在参数空间中随机采样
        - 在输入空间中加噪声（模拟真实波动）
        - 统计 E>1.0 的概率分布
        """
        E_values = []
        above_1_count = 0

        for _ in range(samples):
            # 随机采样参数
            alpha = random.uniform(*alpha_range)
            beta = random.uniform(*beta_range)
            gamma = random.uniform(*gamma_range)
            delta = random.uniform(*delta_range)

            # 归一化使 α+β+γ+δ ≈ 1.0
            total = alpha + beta + gamma + delta
            alpha, beta, gamma, delta = alpha/total, beta/total, gamma/total, delta/total

            # 输入带噪声
            D = self.inputs["D"]
            I = self.inputs["I"]
            C = self.inputs["C"]
            V = self.inputs["V"]

            if add_input_noise:
                D += random.uniform(-0.1, 0.1)
                I += random.uniform(-0.15, 0.15)
                C += random.uniform(-0.05, 0.05)
                V += random.uniform(-0.1, 0.1)

            D = max(0.01, min(1.0, D))
            I = max(0.01, min(1.0, I))
            C = max(0.01, min(1.0, C))
            V = max(0.01, min(1.0, V))

            E = self._compute_E(alpha, beta, gamma, delta, D, I, C, V)
            E_values.append(E)
            if E > 1.0:
                above_1_count += 1

        E_sorted = sorted(E_values)
        n = len(E_sorted)

        return {
            "samples": samples,
            "above_1_count": above_1_count,
            "above_1_prob": above_1_count / samples,
            "E_mean": sum(E_values) / n,
            "E_std": (sum((e - sum(E_values)/n)**2 for e in E_values) / n) ** 0.5,
            "E_min": E_sorted[0],
            "E_max": E_sorted[-1],
            "percentiles": {
                "p10": E_sorted[int(n * 0.1)],
                "p25": E_sorted[int(n * 0.25)],
                "p50": E_sorted[int(n * 0.5)],
                "p75": E_sorted[int(n * 0.75)],
                "p90": E_sorted[int(n * 0.9)],
                "p95": E_sorted[int(n * 0.95)],
                "p99": E_sorted[int(n * 0.99)],
            },
            "raw_values": E_values,  # 用于进一步分析
        }

    # ── 3. 参数空间搜索 ──

    def search_best_params(self, grid_points: int = 10) -> Tuple[Dict[str, float], float]:
        """
        在参数空间中网格搜索最优组合

        约束: α+β+γ+δ = 1.0
        """
        D, I, C, V = self.inputs["D"], self.inputs["I"], self.inputs["C"], self.inputs["V"]
        best_params = {}
        best_E = 0.0

        # 采样网格
        step = 1.0 / grid_points
        candidates = []

        for a in range(1, grid_points):
            for b in range(1, grid_points - a):
                for c in range(1, grid_points - a - b):
                    d = grid_points - a - b - c
                    if d >= 1:
                        alpha = a * step
                        beta = b * step
                        gamma = c * step
                        delta = d * step
                        E = self._compute_E(alpha, beta, gamma, delta, D, I, C, V)
                        candidates.append((alpha, beta, gamma, delta, E))

        # 找最优
        candidates.sort(key=lambda x: x[4], reverse=True)
        
        if candidates:
            best = candidates[0]
            best_params = {
                "alpha": round(best[0], 4),
                "beta": round(best[1], 4),
                "gamma": round(best[2], 4),
                "delta": round(best[3], 4),
            }
            best_E = best[4]

        return best_params, best_E

    # ── 4. 稳定性评估 ──

    def stability_test(self, n_perturbations: int = 1000) -> float:
        """
        稳定性评估：E 对输入噪声的鲁棒性

        稳定性 = 1 - (E标准差 / E均值)
        越接近1越好
        """
        D0, I0, C0, V0 = (
            self.inputs["D"], self.inputs["I"],
            self.inputs["C"], self.inputs["V"]
        )

        E_values = []
        for _ in range(n_perturbations):
            noise = 0.05  # 5%噪声
            D = D0 * (1 + random.uniform(-noise, noise))
            I = I0 * (1 + random.uniform(-noise, noise))
            C = C0 * (1 + random.uniform(-noise, noise))
            V = V0 * (1 + random.uniform(-noise, noise))

            D = max(0.01, min(1.0, D))
            I = max(0.01, min(1.0, I))
            C = max(0.01, min(1.0, C))
            V = max(0.01, min(1.0, V))

            E = self._compute_E(
                DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, DEFAULT_DELTA,
                D, I, C, V
            )
            E_values.append(E)

        mean_E = sum(E_values) / len(E_values)
        std_E = (sum((e - mean_E)**2 for e in E_values) / len(E_values)) ** 0.5

        stability = 1.0 - (std_E / max(mean_E, 0.001))
        return max(0.0, min(1.0, stability))

    # ── 完整校准 ──

    def run_full_calibration(self) -> CalibrationReport:
        """运行完整校准流程"""
        print("📐 开始 E 公式参数校准...")
        print(f"   输入基准: D={self.inputs['D']:.3f} I={self.inputs['I']:.3f} "
              f"C={self.inputs['C']:.3f} V={self.inputs['V']:.3f}")

        report = CalibrationReport(
            calibrated_at=datetime.now(CST).isoformat(),
        )

        # 1. 敏感性分析
        print("\n🔬 1/4 敏感性分析...")
        sensitivity_scores = self.compute_sensitivity_scores()
        report.sensitivity_rank = sensitivity_scores
        report.most_sensitive_param = sensitivity_scores[0][0]
        for name, score in sensitivity_scores:
            print(f"   {name}: 敏感性={score:.4f}")

        # 2. 蒙特卡洛
        print("\n🎲 2/4 蒙特卡洛模拟 (10000样本)...")
        mc = self.monte_carlo(samples=10000)
        report.monte_carlo_samples = mc["samples"]
        report.E_above_1_prob = mc["above_1_prob"]
        report.E_mean = mc["E_mean"]
        report.E_std = mc["E_std"]
        report.E_percentiles = mc["percentiles"]
        print(f"   E>1.0 概率: {mc['above_1_prob']:.2%}")
        print(f"   E 分布: {mc['E_mean']:.4f} ± {mc['E_std']:.4f}")

        # 3. 参数搜索
        print("\n🔍 3/4 最优参数搜索...")
        best_params, best_E = self.search_best_params(grid_points=15)
        report.best_params = best_params
        report.best_E = best_E
        print(f"   最优: α={best_params.get('alpha', '?'):.3f} "
              f"β={best_params.get('beta', '?'):.3f} "
              f"γ={best_params.get('gamma', '?'):.3f} "
              f"δ={best_params.get('delta', '?'):.3f}")
        print(f"   E_max = {best_E:.4f}")

        # 4. 稳定性
        print("\n🛡️ 4/4 稳定性评估...")
        stability = self.stability_test()
        report.stability_score = stability
        print(f"   稳定性: {stability:.3f}/1.0")

        # 保存报告
        self._save_report(report)

        return report

    # ── 辅助 ──

    @staticmethod
    def _compute_E(alpha, beta, gamma, delta, D, I, C, V) -> float:
        """计算 E = D^α · I^β · C^γ · V^δ"""
        return (D ** alpha) * (I ** beta) * (C ** gamma) * (V ** delta)

    def _save_report(self, report: CalibrationReport):
        """保存校准报告到磁盘"""
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "dna": report.dna,
            "calibrated_at": report.calibrated_at,
            "sensitivity": {
                "rank": report.sensitivity_rank,
                "most_sensitive": report.most_sensitive_param,
            },
            "monte_carlo": {
                "samples": report.monte_carlo_samples,
                "above_1_prob": report.E_above_1_prob,
                "E_mean": report.E_mean,
                "E_std": report.E_std,
                "percentiles": report.E_percentiles,
            },
            "best_params": report.best_params,
            "best_E": report.best_E,
            "stability": report.stability_score,
        }
        with open(REPORT_PATH, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n📁 报告已保存: {REPORT_PATH}")


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    calibrator = EmergenceCalibrator()

    if cmd in ("run", "full"):
        report = calibrator.run_full_calibration()
        print("\n" + report.summary())

    elif cmd == "sensitivity":
        scores = calibrator.compute_sensitivity_scores()
        print("📐 参数敏感性分析:")
        for name, score in scores:
            bar = "█" * int(score * 50)
            print(f"  {name}: {score:.4f} {bar}")

    elif cmd == "monte-carlo":
        mc = calibrator.monte_carlo(samples=10000)
        print(f"🎲 蒙特卡洛 (10000样本):")
        print(f"  E>1.0: {mc['above_1_prob']:.2%}")
        print(f"  E分布: {mc['E_mean']:.4f} ± {mc['E_std']:.4f}")
        print(f"  分位数: P10={mc['percentiles']['p10']:.3f}  "
              f"P50={mc['percentiles']['p50']:.3f}  "
              f"P90={mc['percentiles']['p90']:.3f}")

    elif cmd == "search":
        params, E = calibrator.search_best_params(grid_points=15)
        print(f"🔍 最优参数: α={params['alpha']:.3f} β={params['beta']:.3f} "
              f"γ={params['gamma']:.3f} δ={params['delta']:.3f}")
        print(f"  E_max = {E:.4f}")

    elif cmd == "stability":
        s = calibrator.stability_test()
        print(f"🛡️ 稳定性: {s:.3f}/1.0")

    elif cmd == "report":
        if REPORT_PATH.exists():
            with open(REPORT_PATH) as f:
                data = json.load(f)
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("❌ 无校准报告，请先运行 'python3 emergence_calibration.py run'")

    else:
        print(f"用法: python3 {__file__} [run|sensitivity|monte-carlo|search|stability|report]")
