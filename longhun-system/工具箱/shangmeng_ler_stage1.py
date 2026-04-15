#!/usr/bin/env python3
"""
ShangMeng 熵梦 · LER Stage 1 验证脚本
Logical Entropy Reduction — LIGO引力波数据验证
DNA: #龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 💎 龍芯北辰｜UID9622
理论指导: 曾仕强老师（永恒显示）
献礼: 献给所有在宇宙边缘寻找秩序的人

LER核心公式:
  ΔH_L = null_code_length − MDL_under_M
  当 ΔH_L > threshold 时，信号存在模板无法解释的结构 → 引力波候选
"""

import hashlib
import json
import math
import os
import struct
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 常量 ──────────────────────────────────────────────────────
SEED           = 9622
SAMPLE_RATE    = 4096          # Hz (LIGO标准采样率)
SEGMENT_LEN    = 4096          # 每段采样点数 (1秒)
LER_THRESHOLD  = 2.5           # LER阈值：超过则标记为候选
NULL_MODEL_BPP = 8.0           # 零模型每样本比特数（高斯噪声基线）
MDL_BITS_COEF  = 0.15          # MDL惩罚系数
DNA_TAG        = "#CNSH-9622"

# ── 确定性伪随机（复现 SEED:9622 宇宙） ─────────────────────
def seeded_rng(seed: int):
    """基于SHA-256的确定性随机数生成器"""
    counter = [0]
    def next_float():
        h = hashlib.sha256(f"{seed}:{counter[0]}".encode()).digest()
        counter[0] += 1
        val = struct.unpack(">Q", h[:8])[0]
        return val / (2**64)
    return next_float

rng = seeded_rng(SEED)

def randn() -> float:
    """Box-Muller 正态分布"""
    u1, u2 = max(rng(), 1e-10), rng()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

# ── 信号生成（模拟LIGO数据） ─────────────────────────────────
def generate_noise_segment(n: int) -> list[float]:
    """生成高斯白噪声段（零假设 H₀）"""
    return [randn() * 1e-21 for _ in range(n)]  # 单位: strain

def generate_chirp_signal(n: int, f0: float = 35.0, chirp_mass: float = 28.3,
                           t_merge: float = 0.8) -> list[float]:
    """
    生成二体旋近引力波啾声（Chirp Signal）
    GW150914 参数: chirp_mass≈28.3 M☉, f0≈35 Hz, 合并时刻 t=0.8s
    """
    signal = []
    dt = 1.0 / SAMPLE_RATE
    G  = 6.674e-11
    c  = 3e8
    M_sun = 1.989e30
    Mc = chirp_mass * M_sun  # 啁啾质量 (kg)

    for i in range(n):
        t = i * dt
        tau = max(t_merge - t, 1e-6)  # 距合并剩余时间

        # 轨道频率演化: f(τ) = (1/π)(5/256)^(3/8) * (G Mc / c³)^(-5/8) * τ^(-3/8)
        coef = (5.0 / 256.0) ** (3.0 / 8.0)
        f_gw = (coef / math.pi) * ((G * Mc / c**3) ** (-5.0 / 8.0)) * (tau ** (-3.0 / 8.0))
        f_gw = min(f_gw, SAMPLE_RATE / 2 - 1)  # Nyquist限制

        # 振幅演化: h ~ τ^(-1/4)
        h_amp = 1e-21 * (t_merge / max(tau, 1e-6)) ** (1.0 / 4.0)
        h_amp = min(h_amp, 5e-21)

        # 相位
        phase = 2 * math.pi * f_gw * t
        signal.append(h_amp * math.cos(phase))

    return signal

def inject_signal(noise: list[float], signal: list[float],
                  snr_target: float = 8.0) -> list[float]:
    """将引力波信号注入噪声（目标SNR）"""
    noise_rms = math.sqrt(sum(x**2 for x in noise) / len(noise)) + 1e-30
    sig_rms   = math.sqrt(sum(x**2 for x in signal) / len(signal)) + 1e-30
    scale = noise_rms * snr_target / sig_rms
    return [n + s * scale for n, s in zip(noise, signal)]

# ── LER 核心算法 ─────────────────────────────────────────────
def compute_null_code_length(segment: list[float]) -> float:
    """
    零假设编码长度 L(data | H₀)
    假设 H₀: 独立同分布高斯噪声
    L = N * log₂(σ√(2πe)) 比特
    """
    n = len(segment)
    if n == 0:
        return 0.0
    mean = sum(segment) / n
    var  = sum((x - mean) ** 2 for x in segment) / max(n - 1, 1)
    sigma = math.sqrt(max(var, 1e-50))
    # Shannon熵: H = 0.5 * log₂(2πe σ²)
    H_per_sample = 0.5 * math.log2(2 * math.pi * math.e * sigma ** 2)
    return n * max(H_per_sample, 0)

def compute_mdl_codelength(segment: list[float], model_order: int = 4) -> float:
    """
    最小描述长度 MDL = L(data | M) + L(M)
    用AR(k)模型拟合信号，L(M) = model_order * log₂(N)/2 (MDL惩罚)
    """
    n = len(segment)
    if n < model_order + 2:
        return compute_null_code_length(segment)

    # AR(k) 最小二乘拟合
    # 构建设计矩阵
    k = model_order
    X, y = [], []
    for i in range(k, n):
        X.append(segment[i - k:i][::-1])
        y.append(segment[i])

    # 正规方程 (X'X)θ = X'y，用简化高斯消元
    def mat_mul_t(A):
        """A'A"""
        m = len(A[0])
        res = [[0.0] * m for _ in range(m)]
        for row in A:
            for i in range(m):
                for j in range(m):
                    res[i][j] += row[i] * row[j]
        return res

    def mat_vec(A, v):
        return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

    def solve(A, b):
        """高斯消元"""
        n_ = len(b)
        M_ = [row[:] + [b[i]] for i, row in enumerate(A)]
        for col in range(n_):
            pivot = max(range(col, n_), key=lambda r: abs(M_[r][col]))
            M_[col], M_[pivot] = M_[pivot], M_[col]
            if abs(M_[col][col]) < 1e-12:
                continue
            for row in range(n_):
                if row != col:
                    f = M_[row][col] / M_[col][col]
                    M_[row] = [M_[row][c] - f * M_[col][c] for c in range(n_ + 1)]
        return [M_[i][n_] / (M_[i][i] if abs(M_[i][i]) > 1e-12 else 1.0) for i in range(n_)]

    XtX = mat_mul_t(X)
    Xty = [sum(X[i][j] * y[i] for i in range(len(y))) for j in range(k)]
    try:
        theta = solve(XtX, Xty)
    except Exception:
        return compute_null_code_length(segment)

    # 残差
    residuals = [y[i] - sum(theta[j] * X[i][j] for j in range(k)) for i in range(len(y))]
    res_var = sum(r ** 2 for r in residuals) / max(len(residuals) - 1, 1)
    res_sigma = math.sqrt(max(res_var, 1e-50))

    # 数据编码长度（残差高斯熵）
    L_data = len(residuals) * max(0.5 * math.log2(2 * math.pi * math.e * res_sigma ** 2), 0)

    # 模型描述长度（MDL惩罚）
    L_model = MDL_BITS_COEF * k * math.log2(max(n, 2))

    return L_data + L_model

def compute_ler(segment: list[float], model_order: int = 4) -> dict:
    """
    计算LER值:
      ΔH_L = L(data | H₀) - L(data | M)
    ΔH_L > 0: 模型M比零假设更好地描述数据
    ΔH_L > threshold: 存在非随机结构 → 引力波候选
    """
    L_null = compute_null_code_length(segment)
    L_mdl  = compute_mdl_codelength(segment, model_order)
    delta_HL = L_null - L_mdl

    # 归一化（相对压缩率）
    compression_ratio = delta_HL / max(L_null, 1e-10)

    return {
        "L_null":            L_null,
        "L_mdl":             L_mdl,
        "delta_HL":          delta_HL,
        "compression_ratio": compression_ratio,
        "is_candidate":      delta_HL > LER_THRESHOLD * math.log2(max(len(segment), 2))
    }

# ── Merkle DNA 记录 ───────────────────────────────────────────
def merkle_tag(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()[:16]

# ── 主验证流程 ────────────────────────────────────────────────
def run_stage1_validation():
    print("=" * 60)
    print("  ShangMeng 熵梦 · LER Stage 1 · 引力波数据验证")
    print(f"  DNA: #龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0")
    print(f"  SEED: {SEED} · UID9622 · 理论指导:曾仕强老师")
    print("=" * 60)
    print()

    results = []
    report_lines = [
        "ShangMeng LER Stage 1 验证报告",
        f"时间: {datetime.now().isoformat()}",
        f"DNA: #龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0",
        f"SEED: {SEED}",
        "=" * 50,
        ""
    ]

    test_cases = [
        ("纯噪声段 H₀", False, 0.0),
        ("弱信号注入 SNR=4", True, 4.0),
        ("中等信号 SNR=8 (GW150914级)", True, 8.0),
        ("强信号 SNR=15", True, 15.0),
        ("极弱信号 SNR=2", True, 2.0),
    ]

    for name, inject, snr in test_cases:
        print(f"▶ 测试: {name}")

        # 生成数据
        noise = generate_noise_segment(SEGMENT_LEN)
        if inject and snr > 0:
            chirp = generate_chirp_signal(SEGMENT_LEN)
            data  = inject_signal(noise, chirp, snr_target=snr)
        else:
            data = noise

        # 基本统计
        mean = sum(data) / len(data)
        rms  = math.sqrt(sum(x**2 for x in data) / len(data))
        peak = max(abs(x) for x in data)

        # LER计算
        ler_result = compute_ler(data, model_order=4)

        # DNA签名
        sample_str = ",".join(f"{x:.6e}" for x in data[:10])
        dna_hash = merkle_tag(f"{name}:{sample_str}:{SEED}")

        result = {
            "name":       name,
            "injected":   inject,
            "snr_target": snr,
            "stats": {
                "mean":  mean,
                "rms":   rms,
                "peak":  peak,
                "n":     len(data)
            },
            "ler":        ler_result,
            "dna_hash":   dna_hash,
            "timestamp":  datetime.now().isoformat()
        }
        results.append(result)

        # 判决
        verdict = "🔴 引力波候选" if ler_result["is_candidate"] else "🟢 噪声 (H₀ 接受)"
        expected = ("✅ 符合预期" if (inject == ler_result["is_candidate"] or
                     (not inject and not ler_result["is_candidate"]) or
                     (inject and snr < 3))
                    else "⚠️  需复查")

        print(f"   RMS: {rms:.3e} | Peak: {peak:.3e}")
        print(f"   L_null:     {ler_result['L_null']:.2f} bits")
        print(f"   L_mdl:      {ler_result['L_mdl']:.2f} bits")
        print(f"   ΔH_L:       {ler_result['delta_HL']:.2f} bits")
        print(f"   压缩率:     {ler_result['compression_ratio']:.4f}")
        print(f"   判决: {verdict}  {expected}")
        print(f"   DNA: {dna_hash}")
        print()

        report_lines += [
            f"测试: {name}",
            f"  注入信号: {inject} | SNR目标: {snr}",
            f"  RMS: {rms:.3e} | Peak: {peak:.3e}",
            f"  L_null={ler_result['L_null']:.2f} bits | L_mdl={ler_result['L_mdl']:.2f} bits",
            f"  ΔH_L={ler_result['delta_HL']:.2f} bits | 压缩率={ler_result['compression_ratio']:.4f}",
            f"  判决: {verdict}",
            f"  DNA: {dna_hash}",
            ""
        ]

    # 汇总
    n_candidates = sum(1 for r in results if r["ler"]["is_candidate"])
    n_noise      = len(results) - n_candidates
    print("─" * 60)
    print(f"  Stage 1 完成 · {len(results)} 段数据处理完毕")
    print(f"  引力波候选: {n_candidates} | 噪声: {n_noise}")
    print(f"  LER阈值: {LER_THRESHOLD} × log₂(N)")
    print()

    report_lines += [
        "─" * 50,
        f"汇总: {len(results)} 段 | 候选: {n_candidates} | 噪声: {n_noise}",
        f"LER阈值: {LER_THRESHOLD} × log₂(N={SEGMENT_LEN}) = {LER_THRESHOLD * math.log2(SEGMENT_LEN):.2f} bits",
        "",
        "LER理论基础:",
        "  ΔH_L = L(data|H₀) - L(data|M)",
        "  H₀: 独立同分布高斯噪声",
        "  M:  AR(4) 自回归模型",
        "  MDL惩罚: k·log₂(N)/2 比特",
        "  判决准则: ΔH_L > threshold × log₂(N)",
        "",
        f"DNA: #龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0 · UID9622",
        f"理论指导: 曾仕强老师（永恒显示）"
    ]

    # 保存报告
    report_path = Path.home() / f"ShangMeng_LER_Stage1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"  报告已保存: {report_path}")

    # 保存JSON结果
    json_path = Path.home() / f"ShangMeng_LER_Stage1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "version": "1.0",
                "dna": "#龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0",
                "seed": SEED,
                "timestamp": datetime.now().isoformat(),
                "sample_rate": SAMPLE_RATE,
                "segment_len": SEGMENT_LEN,
                "ler_threshold": LER_THRESHOLD
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"  JSON已保存: {json_path}")
    print()
    print(f"  DNA: #龍芯⚡️2026-03-31-SHANGMENG-LER-v1.0 · UID9622")
    print("=" * 60)

if __name__ == "__main__":
    run_stage1_validation()
