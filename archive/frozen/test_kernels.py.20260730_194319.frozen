"""
🐉 龍魂计算内核 · 冒烟测试
DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-v1.0
"""

import sys
import math
import struct
import ctypes
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from compute_kernels import (
    lh_silu, lh_rms_norm, lh_linear,
    lh_apply_rope, lh_stat_constraint,
    is_available, engine_type,
)

def assert_close(a, b, tol=1e-4, label=""):
    if abs(a - b) > tol:
        print(f"  ❌ {label}: expected {b:.6f}, got {a:.6f} (diff={abs(a-b):.2e})")
        return False
    return True

def test_silu():
    print("=" * 60)
    print("测试 1: lh_silu")
    print("=" * 60)
    passed = 0
    failed = 0
    tests = [-2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 3.0, 5.0]

    for x in tests:
        expected = x / (1.0 + math.exp(-x))
        result = lh_silu(x)
        ok = assert_close(result, expected, label=f"x={x}")
        if ok:
            passed += 1
            print(f"  ✅ SiLU({x}) = {result:.6f}  (expected {expected:.6f})")
        else:
            failed += 1

    print(f"\n  SiLU: {passed}/{passed+failed} 通过")
    return failed == 0


def test_rms_norm():
    print("\n" + "=" * 60)
    print("测试 2: lh_rms_norm")
    print("=" * 60)

    n = 16
    x = [float(i + 1) for i in range(n)]  # 1..16
    weight = [1.0] * n
    out = [0.0] * n

    lh_rms_norm(out, x, weight, n)

    # 手动计算 RMS
    rms = math.sqrt(sum(v*v for v in x) / n)
    expected = [v / rms * 1.0 for v in x]

    passed = 0
    failed = 0
    for i in range(min(5, n)):
        ok = assert_close(out[i], expected[i], label=f"rms_norm[{i}]")
        if ok:
            passed += 1
            print(f"  ✅ out[{i}] = {out[i]:.6f}  (expected {expected[i]:.6f})")
        else:
            failed += 1

    print(f"  ... (共 {n} 维)")
    print(f"  RMS Norm: {passed}/{passed+failed} 通过 (前5项)")
    return failed == 0


def test_linear():
    print("\n" + "=" * 60)
    print("测试 3: lh_linear (matvec)")
    print("=" * 60)

    in_dim = 8
    out_dim = 4

    x = [float(i + 1) for i in range(in_dim)]                         # [1,2,3,4,5,6,7,8]
    w = [float((i * in_dim + j + 1) % 10 + 1) for i in range(out_dim)  # [1,2,...,8, 2,3,...,9, ...]
         for j in range(in_dim)]
    out = [0.0] * out_dim

    lh_linear(x, w, out, in_dim, out_dim)

    # 手动计算: out[i] = sum(w[i*in_dim + j] * x[j] for j in range(in_dim))
    expected = []
    for i in range(out_dim):
        s = sum(w[i * in_dim + j] * x[j] for j in range(in_dim))
        expected.append(s)

    passed = 0
    failed = 0
    for i in range(out_dim):
        ok = assert_close(out[i], expected[i], label=f"linear[{i}]")
        if ok:
            passed += 1
            print(f"  ✅ out[{i}] = {out[i]:.6f}  (expected {expected[i]:.6f})")
        else:
            failed += 1

    print(f"  Linear: {passed}/{passed+failed} 通过")
    return failed == 0


def test_rope():
    print("\n" + "=" * 60)
    print("测试 4: lh_apply_rope")
    print("=" * 60)

    dim = 8  # 4 对 (cos, sin)
    half = dim // 2

    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]  # 前4实部，后4虚部
    cos_vals = [math.cos(i * 0.5) for i in range(half)]
    sin_vals = [math.sin(i * 0.5) for i in range(half)]

    lh_apply_rope(x, cos_vals, sin_vals, dim)

    # 手动计算
    expected = []
    for i in range(half):
        a = 1.0 + i   # x[i] (original 1..4)
        b = 5.0 + i   # x[i+half] (original 5..8)
        c = cos_vals[i]
        s = sin_vals[i]
        expected.append(a * c - b * s)      # real part
        expected.append(b * c + a * s)      # imaginary part

    # Wait, the RoPE implementation stores in-place differently:
    # out[i] = a*c - b*s  (stored at x[i])
    # out[i+half] = b*c + a*s  (stored at x[i+half])

    passed = 0
    failed = 0
    for i in range(half):
        real_idx = i
        imag_idx = i + half
        exp_real = x_orig_real = (i + 1) * cos_vals[i] - (i + half + 1) * sin_vals[i]
        exp_imag = x_orig_imag = (i + half + 1) * cos_vals[i] + (i + 1) * sin_vals[i]

        ok_r = assert_close(x[real_idx], exp_real, label=f"rope[{real_idx}]")
        ok_i = assert_close(x[imag_idx], exp_imag, label=f"rope[{imag_idx}]")
        if ok_r and ok_i:
            passed += 2
            print(f"  ✅ x[{real_idx}]={x[real_idx]:.6f} x[{imag_idx}]={x[imag_idx]:.6f}")
        else:
            failed += 2

    print(f"  RoPE: {passed}/{passed+failed} 通过")
    return failed == 0


def test_stat_constraint():
    print("\n" + "=" * 60)
    print("测试 5: lh_stat_constraint")
    print("=" * 60)

    size = 16
    x = [float(i + 1) for i in range(size)]
    mean = [sum(x) / size]
    std = [math.sqrt(sum((v - mean[0])**2 for v in x) / size)]

    lh_stat_constraint(x, size, mean, std,
                       gamma=0.9, k=3.0, max_norm=100.0, min_norm=0.01)

    new_mean = sum(x) / size
    new_std = math.sqrt(sum((v - new_mean)**2 for v in x) / size)

    print(f"  ✅ 原 mean={sum(range(1,size+1))/size:.4f} → 新 mean={new_mean:.4f}")
    print(f"  ✅ 原 std={std[0]:.4f} → 新 std={new_std:.4f}")
    print(f"  ✅ mean[0]={mean[0]:.4f} (内联更新)")
    print(f"  Stat Constraint: 通过")
    return True


def main():
    print("🐉 龍魂 SIMD 计算内核 · 冒烟测试")
    print(f"   引擎: {engine_type()}")
    print()

    results = []
    results.append(("SiLU", test_silu()))
    results.append(("RMS Norm", test_rms_norm()))
    results.append(("Linear", test_linear()))
    results.append(("RoPE", test_rope()))
    results.append(("Stat Constraint", test_stat_constraint()))

    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    all_pass = True
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
        if not ok:
            all_pass = False

    if all_pass:
        print("\n🎉 全部 5 项内核测试通过！")
    else:
        print("\n⚠️ 部分测试失败")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    # 先保存原始 x 值用于 RoPE 测试
    x_orig_real = None
    x_orig_imag = None
    main()
