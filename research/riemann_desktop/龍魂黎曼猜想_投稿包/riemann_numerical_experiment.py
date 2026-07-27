#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂黎曼猜想观察性框架 · 数值实验代码

重要声明：
  本文档是一个观察性框架（observational framework），不是数学证明。
  数值验证部分仅展示现象，不构成逻辑证明。
  我们没有证明黎曼猜想。

DNA: #龍芯⚡️2026-06-08-Riemann-Dragonhood-Framework-v1.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""

import numpy as np
from scipy.special import zeta, gamma
import matplotlib.pyplot as plt

# 权重：实验性选择，暂无法学依据
W1, W2, W3 = 0.34, 0.33, 0.33


def weight_zeta(s):
    """天轴：|ζ(s)|"""
    return np.abs(zeta(s))


def weight_symmetric(s):
    """地轴：|ζ(1-s)|"""
    return np.abs(zeta(1 - s))


def weight_factor(s):
    """人轴：|χ(s)| 的简化近似（使用 |Γ(1-s)|）"""
    return np.abs(gamma(1 - s))


def W(s):
    """三才加权函数"""
    return (W1 * weight_zeta(s) +
            W2 * weight_symmetric(s) +
            W3 * weight_factor(s))


def experiment_critical_line(t_max=50, n_points=1000, save_path="weighted_function_experiment.png"):
    """
    实验：比较 W(s) 在临界线 Re(s)=0.5 与偏离线 Re(s)=0.45 上的行为。
    """
    t_values = np.linspace(0, t_max, n_points)

    critical = [W(0.5 + 1j * t) for t in t_values]
    off_critical = [W(0.45 + 1j * t) for t in t_values]

    plt.figure(figsize=(12, 6))
    plt.plot(t_values, critical, label='W(1/2 + it)', linewidth=2)
    plt.plot(t_values, off_critical, label='W(0.45 + it)', linewidth=2, alpha=0.7)
    plt.xlabel('Im(s) = t')
    plt.ylabel('W(s)')
    plt.legend()
    plt.title('Numerical Experiment: W(s) on vs off Critical Line')
    plt.grid(True)
    plt.savefig(save_path, dpi=300)

    avg_c = np.mean(critical)
    avg_o = np.mean(off_critical)
    print(f"临界线平均值：     {avg_c:.6f}")
    print(f"偏离线平均值：     {avg_o:.6f}")
    print(f"差异比例：         {(avg_c - avg_o) / avg_o * 100:.2f}%")
    print("⚠️  这是实验观察，不是证明")


def experiment_known_zeros():
    """
    实验：在已知非平凡零点处检查 |ζ(s)| 与 W(s)。
    这些零点是数学界已验证的结果，不是本框架的发现。
    """
    known_zeros = [
        14.134725, 21.022039, 25.010857, 30.424876, 32.935061,
        37.586178, 40.918719, 43.327073, 48.005150, 49.773832
    ]

    print("\n【已知零点验证】")
    print("s = 1/2 + i·t\n")

    for t in known_zeros:
        s = 0.5 + 1j * t
        abs_z = np.abs(zeta(s))
        w_val = W(s)
        print(f"t={t:8.6f}  |ζ(s)|={abs_z:.2e}  W(s)={w_val:.6f}")

    print("\n✅ 这些零点确实位于临界线上（已知结果）")
    print("⚠️  W(s) 的行为需要更多理论分析")


if __name__ == "__main__":
    print("=" * 80)
    print("🧮 龍魂视角下的黎曼猜想 · 数值实验")
    print("=" * 80)
    print("⚠️  本代码为观察性实验，不是数学证明")
    print("=" * 80)

    print("\n【实验 1：临界线 vs 偏离线】")
    experiment_critical_line()

    experiment_known_zeros()

    print("\n" + "=" * 80)
    print("✅ 数值实验完成")
    print("   性质：观察性实验，不是证明")
    print("=" * 80)
