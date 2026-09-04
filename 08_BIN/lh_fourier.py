# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-ea81f007
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 傅里叶变换引擎 v1.0

将时域信号分解为频域正弦波之和。龍魂视角：傅里叶变换是「万象归一」——
任何复杂信号都可以拆解为简单正弦波的叠加。对应易经「易有太极，是生两仪」——
太极(信号)通过傅里叶变换揭示其内在的「两仪」(频率成分)。

知识卡: 傅里叶变换 · Fourier Transform（ID=111 · dr=2·土·坤宫 · 🔴底座）
落地映射: 采样定理(伴生) · 信息论(频谱熵) · 数字流场

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-FOURIER-TRANSFORM-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_fourier.py --dft 1,0,1,0        # 离散傅里叶变换(幅值)
  python3 bin/lh_fourier.py --fft 1,2,3,4        # 快速傅里叶变换(长度须为2的幂)
  python3 bin/lh_fourier.py --spectrum 1,0,1,0   # 幅值谱+相位谱+频率轴
  python3 bin/lh_fourier.py --idft <复数序列>     # 逆变换
  python3 bin/lh_fourier.py --self-test          # 自我验证
"""

import argparse
import cmath
import math
import os
import sys


def _stamp() -> str:
    """输出时间戳（引擎独立可用，时间引擎缺失时降级）"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


def dft(x):
    """离散傅里叶变换 O(N²)：X[k] = Σ x[n]·e^{-i2πkn/N}"""
    N = len(x)
    return [sum(x[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N))
            for k in range(N)]


def idft(X):
    """逆离散傅里叶变换：x[n] = (1/N)Σ X[k]·e^{+i2πkn/N}"""
    N = len(X)
    return [sum(X[k] * cmath.exp(2j * math.pi * k * n / N) for k in range(N)) / N
            for n in range(N)]


def fft(x):
    """快速傅里叶变换（递归 Cooley-Tukey，长度须为 2 的幂）"""
    N = len(x)
    if N <= 1:
        return list(x)
    if N & (N - 1) != 0:
        raise ValueError("FFT 长度必须是 2 的幂")
    even = fft(x[0::2])
    odd = fft(x[1::2])
    w = [cmath.exp(-2j * math.pi * k / N) for k in range(N // 2)]
    return [even[k] + w[k] * odd[k] for k in range(N // 2)] + \
           [even[k] - w[k] * odd[k] for k in range(N // 2)]


def spectrum(x, sample_rate=1.0):
    """幅值谱 + 相位谱 + 频率轴"""
    N = len(x)
    X = dft(x)
    freqs = [k * sample_rate / N for k in range(N // 2 + 1)]
    amps = [abs(X[k]) / N for k in range(N // 2 + 1)]
    phases = [cmath.phase(X[k]) for k in range(N // 2 + 1)]
    return freqs, amps, phases


def _fmt(x, digits=3):
    if abs(x.imag) < 1e-10:
        return round(x.real, digits)
    return complex(round(x.real, digits), round(x.imag, digits))


def self_test():
    """知识卡示例验证 + FFT与DFT一致性 + 逆变换还原"""
    ok = True
    # 1) 知识卡示例: dft([1,0,1,0]) 幅值应 ≈ [2, 0, 2, 0]
    x = [1, 0, 1, 0]
    amps = [abs(v) for v in dft(x)]
    expect = [2.0, 0.0, 2.0, 0.0]
    t1 = all(abs(a - e) < 1e-9 for a, e in zip(amps, expect))
    ok &= t1
    print(f"[1] DFT 知识卡示例 幅值={[round(a,3) for a in amps]} {'✅' if t1 else '❌'}")
    # 2) FFT 与 DFT 一致
    x2 = [complex(math.sin(i * 0.5), math.cos(i * 0.3)) for i in range(8)]
    t2 = all(abs(a - b) < 1e-9 for a, b in zip(fft(x2), dft(x2)))
    ok &= t2
    print(f"[2] FFT vs DFT 一致性 (N=8) {'✅' if t2 else '❌'}")
    # 3) IDFT 还原原信号
    x3 = [math.sin(2 * math.pi * 3 * n / 16) for n in range(16)]
    recon = idft(dft(x3))
    err = max(abs(a - b) for a, b in zip(recon, x3))
    t3 = err < 1e-9
    ok &= t3
    print(f"[3] 逆变换还原误差={err:.2e} {'✅' if t3 else '❌'}")
    print(f"\n🐉 傅里叶自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="龍魂·傅里叶变换引擎 v1.0")
    ap.add_argument("--dft", help="离散傅里叶变换, 逗号分隔数值")
    ap.add_argument("--fft", help="快速傅里叶变换, 逗号分隔数值(N为2的幂)")
    ap.add_argument("--idft", help="逆变换, 逗号分隔复数如 2,0+2j")
    ap.add_argument("--spectrum", help="幅值谱+相位谱, 逗号分隔数值")
    ap.add_argument("--sample-rate", type=float, default=1.0, help="采样率(默认1.0)")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.dft:
        x = [float(v) for v in args.dft.split(",")]
        X = dft(x)
        print(f"x    = {[round(v,3) for v in x]}")
        print(f"X    = {[_fmt(v) for v in X]}")
        print(f"幅值 = {[round(abs(v),3) for v in X]}")
    elif args.fft:
        x = [float(v) for v in args.fft.split(",")]
        X = fft(x)
        print(f"x    = {[round(v,3) for v in x]}")
        print(f"X    = {[_fmt(v) for v in X]}")
        print(f"幅值 = {[round(abs(v),3) for v in X]}")
    elif args.idft:
        X = [complex(v) for v in args.idft.split(",")]
        x = idft(X)
        print(f"x    = {[_fmt(v) for v in x]}")
    elif args.spectrum:
        x = [float(v) for v in args.spectrum.split(",")]
        freqs, amps, phases = spectrum(x, args.sample_rate)
        print(f"信号   = {[round(v,3) for v in x]}")
        print(f"频率轴 = {[round(f,3) for f in freqs]}")
        print(f"幅值谱 = {[round(a,3) for a in amps]}")
        print(f"相位谱 = {[round(p,3) for p in phases]}")
    else:
        ap.print_help()
        return 1
    print(f"\n{_stamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
