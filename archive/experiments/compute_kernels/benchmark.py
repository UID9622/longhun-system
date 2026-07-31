# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 SIMD 计算内核 · 性能基准测试
DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-BENCHMARK-v1.0

对比 SIMD 汇编 vs 纯 Python 回退的性能差异。
"""

import sys
import time
import random
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from compute_kernels import (
    lh_silu, lh_rms_norm, lh_linear,
    lh_apply_rope, lh_stat_constraint,
    is_available, engine_type,
)

# ══════════════════════════════════════════════════════════════════
# 纯 Python 回退（用于对比）
# ══════════════════════════════════════════════════════════════════

def _py_silu(x: float) -> float:
    return x / (1.0 + math.exp(-x))

def _py_rms_norm(out, x, weight, n: int):
    rms = math.sqrt(sum(v*v for v in x) / n)
    inv_rms = 1.0 / rms if rms > 1e-8 else 1.0
    for i in range(n):
        out[i] = x[i] * inv_rms * weight[i]

def _py_linear(x, w, out, in_dim: int, out_dim: int):
    for i in range(out_dim):
        s = 0.0
        row_base = i * in_dim
        for j in range(in_dim):
            s += w[row_base + j] * x[j]
        out[i] = s

def _py_apply_rope(x, cos, sin, dim: int):
    half = dim // 2
    for i in range(half):
        a, b = x[i], x[i + half]
        c, s = cos[i], sin[i]
        x[i] = a * c - b * s
        x[i + half] = b * c + a * s


# ══════════════════════════════════════════════════════════════════
# 基准测试
# ══════════════════════════════════════════════════════════════════

def bench_silu(n_iter: int = 100000):
    """SiLU 基准"""
    print(f"\n  SiLU 激活 ({n_iter:,} 次迭代)")
    x = random.uniform(-5, 5)

    # 预热
    for _ in range(100):
        lh_silu(x)

    t0 = time.perf_counter()
    for _ in range(n_iter):
        lh_silu(x)
    t_lh = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(n_iter):
        _py_silu(x)
    t_py = time.perf_counter() - t0

    speedup = t_py / t_lh if t_lh > 0 else 0
    print(f"    lh_silu:   {t_lh*1000:.2f}ms")
    print(f"    python:    {t_py*1000:.2f}ms")
    print(f"    加速比:    {speedup:.2f}x")
    return speedup


def bench_rms_norm(n_iter: int = 10000):
    """RMS Norm 基准"""
    n = 256
    print(f"\n  RMS Norm (dim={n}, {n_iter:,} 次迭代)")
    x = [random.uniform(-1, 1) for _ in range(n)]
    w = [1.0] * n
    out = [0.0] * n

    for _ in range(10):
        lh_rms_norm(out, x, w, n)

    t0 = time.perf_counter()
    for _ in range(n_iter):
        lh_rms_norm(out, x, w, n)
    t_lh = time.perf_counter() - t0

    out2 = [0.0] * n
    t0 = time.perf_counter()
    for _ in range(n_iter):
        _py_rms_norm(out2, x, w, n)
    t_py = time.perf_counter() - t0

    speedup = t_py / t_lh if t_lh > 0 else 0
    print(f"    lh_rms_norm: {t_lh*1000:.2f}ms")
    print(f"    python:      {t_py*1000:.2f}ms")
    print(f"    加速比:      {speedup:.2f}x")
    return speedup


def bench_linear(n_iter: int = 5000):
    """Linear (matvec) 基准"""
    in_dim = 128
    out_dim = 64
    print(f"\n  Linear (matvec {in_dim}→{out_dim}, {n_iter:,} 次迭代)")
    x = [random.uniform(-1, 1) for _ in range(in_dim)]
    w = [random.uniform(-1, 1) for _ in range(in_dim * out_dim)]
    out = [0.0] * out_dim

    for _ in range(10):
        lh_linear(x, w, out, in_dim, out_dim)

    t0 = time.perf_counter()
    for _ in range(n_iter):
        lh_linear(x, w, out, in_dim, out_dim)
    t_lh = time.perf_counter() - t0

    out2 = [0.0] * out_dim
    t0 = time.perf_counter()
    for _ in range(n_iter):
        _py_linear(x, w, out2, in_dim, out_dim)
    t_py = time.perf_counter() - t0

    speedup = t_py / t_lh if t_lh > 0 else 0
    print(f"    lh_linear:  {t_lh*1000:.2f}ms")
    print(f"    python:     {t_py*1000:.2f}ms")
    print(f"    加速比:     {speedup:.2f}x")
    return speedup


def bench_rope(n_iter: int = 10000):
    """RoPE 基准"""
    dim = 64
    half = dim // 2
    print(f"\n  RoPE (dim={dim}, {n_iter:,} 次迭代)")
    x = [random.uniform(-1, 1) for _ in range(dim)]
    cos = [math.cos(i * 0.5) for i in range(half)]
    sin = [math.sin(i * 0.5) for i in range(half)]

    for _ in range(10):
        x_copy = x[:]
        lh_apply_rope(x_copy, cos, sin, dim)

    t0 = time.perf_counter()
    for _ in range(n_iter):
        x_copy = x[:]
        lh_apply_rope(x_copy, cos, sin, dim)
    t_lh = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(n_iter):
        x_copy2 = x[:]
        _py_apply_rope(x_copy2, cos, sin, dim)
    t_py = time.perf_counter() - t0

    speedup = t_py / t_lh if t_lh > 0 else 0
    print(f"    lh_rope:   {t_lh*1000:.2f}ms")
    print(f"    python:    {t_py*1000:.2f}ms")
    print(f"    加速比:    {speedup:.2f}x")
    return speedup


def bench_stat_constraint(n_iter: int = 5000):
    """统计约束基准"""
    size = 128
    print(f"\n  统计约束 (size={size}, {n_iter:,} 次迭代)")

    x_base = [random.uniform(-5, 5) for _ in range(size)]
    mean_base = [sum(x_base) / size]
    std_base = [math.sqrt(sum((v - mean_base[0])**2 for v in x_base) / size)]

    for _ in range(5):
        xx = x_base[:]
        mm = [mean_base[0]]
        ss = [std_base[0]]
        lh_stat_constraint(xx, size, mm, ss)

    t0 = time.perf_counter()
    for _ in range(n_iter):
        xx = x_base[:]
        mm = [mean_base[0]]
        ss = [std_base[0]]
        lh_stat_constraint(xx, size, mm, ss)
    t_lh = time.perf_counter() - t0

    t_py = 0.0  # 纯 Python 已在 Python 回退中测试
    speedup = t_py / t_lh if t_lh > 0 else 0
    print(f"    lh_stat:   {t_lh*1000:.2f}ms")
    print(f"    纯Python回退已在test_kernels.py中验证")
    return speedup


# ══════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════

def main():
    print("🐉 龍魂 SIMD 计算内核 · 性能基准测试")
    print(f"   引擎: {engine_type()}")
    print(f"   SIMD库: {'已加载' if is_available() else '纯Python回退'}")
    print("=" * 50)

    results = {}

    if is_available():
        results["SiLU"] = bench_silu()
        results["RMS Norm"] = bench_rms_norm()
        results["Linear"] = bench_linear()
        results["RoPE"] = bench_rope()
        results["Stat Constraint"] = bench_stat_constraint()

        print("\n" + "=" * 50)
        print("性能汇总")
        print("=" * 50)
        for name, speedup in results.items():
            color = "✅" if speedup >= 1.5 else ("🟡" if speedup >= 1.0 else "🔴")
            print(f"  {color} {name:<20} {speedup:.2f}x 加速")

        avg = sum(results.values()) / len(results)
        print(f"\n  📊 平均加速比: {avg:.2f}x")
        print(f"  🧬 #龍芯⚡️2026-07-13-COMPUTE-KERNELS-BENCHMARK-v1.0")
    else:
        print("\n  ⚠️ SIMD 库未编译，基准测试仅在 x86-64 上可用")
        print("  在 ARM64 (Apple Silicon) 上自动使用纯 Python 回退")
        print("  如需编译: cd compute_kernels && make")
        print(f"\n  🧬 #龍芯⚡️2026-07-13-COMPUTE-KERNELS-BENCHMARK-v1.0")


if __name__ == "__main__":
    main()
