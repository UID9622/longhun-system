# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-a0ab4da4
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 采样定理引擎 v1.0（Nyquist Sampling Theorem）

核心公式: fs ≥ 2·fmax —— 采样频率必须至少是最高信号频率的2倍，否则失真(混叠)。
龍魂视角: 「因势利导」——超过人耳感知范围后收益递减，够用就好。

知识卡: 采样定理 · Nyquist Sampling Theorem（ID=116 · dr=5·中宫·土 · 🔴底座）
常见误区: 以为采样率越高越好没有上限——超过人耳感知范围(20kHz)后收益递减。
落地映射: 傅里叶变换 · 音频处理 · 信号与系统

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-SAMPLING-THEOREM-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_sampling.py --check 44100 20000   # 奈奎斯特判定
  python3 bin/lh_sampling.py --min 20000           # 最小采样率(音频20kHz)
  python3 bin/lh_sampling.py --alias-demo 8 3      # 混叠演示: fs=8 fmax=3
  python3 bin/lh_sampling.py --self-test
"""

import argparse
import os
import sys


def _stamp() -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


def nyquist_ok(fs, fmax):
    """奈奎斯特判定: fs >= 2·fmax"""
    return fs >= 2 * fmax


def min_sample_rate(fmax):
    """最小无失真采样率 = 2·fmax"""
    return 2 * fmax


def alias_frequency(f, fs):
    """混叠频率: 欠采样时高频成分折叠为 |f - k·fs|"""
    if fs <= 0:
        return float("inf")
    k = round(f / fs)
    folded = abs(f - k * fs)
    return min(folded, abs(fs - folded))


def alias_demo(fs, fmax):
    """混叠演示: 判定 + 折叠频率"""
    if nyquist_ok(fs, fmax):
        return {"ok": True, "verdict": f"fs={fs} ≥ 2·fmax={2*fmax} · 无混叠 ✅"}
    alias = alias_frequency(fmax, fs)
    return {
        "ok": False,
        "verdict": f"fs={fs} < 2·fmax={2*fmax} · 欠采样 ⚠️ 原{fmax}Hz折叠为{alias:.1f}Hz",
        "alias": round(alias, 3),
    }


def self_test():
    ok = True
    # 1) 知识卡示例: CD 44100Hz for 20kHz
    t1 = nyquist_ok(44100, 20000)
    ok &= t1
    print(f"[1] CD 44100Hz for 20kHz = {t1} {'✅' if t1 else '❌'}")
    # 2) 边界: fs = 2·fmax 恰好满足
    t2 = nyquist_ok(40000, 20000) and not nyquist_ok(39999, 20000)
    ok &= t2
    print(f"[2] 边界 fs=2·fmax: 40000≥40000✅ / 39999<40000❌ {'✅' if t2 else '❌'}")
    # 3) 最小采样率
    t3 = min_sample_rate(20000) == 40000
    ok &= t3
    print(f"[3] 人耳20kHz最小采样率 = {min_sample_rate(20000)}Hz {'✅' if t3 else '❌'}")
    # 4) 混叠: fmax=3k, fs=5k → 欠采样 (5 < 2·3=6)
    a = alias_demo(5, 3)
    t4 = not a["ok"]
    ok &= t4
    print(f"[4] 混叠演示 fs=5 fmax=3: {a['verdict']} {'✅' if t4 else '❌'}")
    # 5) 收益递减
    print(f"[5] 收益递减观: 人耳上限20kHz, 采样率超过40kHz后感知收益递减(够用就好) ✅")
    print(f"\n🐉 采样定理自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="龍魂·采样定理引擎 v1.0")
    ap.add_argument("--check", nargs=2, type=float, help="奈奎斯特判定 fs fmax")
    ap.add_argument("--min", type=float, help="最小采样率(输入最高频率)")
    ap.add_argument("--alias-demo", nargs=2, type=float, help="混叠演示 fs fmax")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.check:
        fs, fmax = args.check
        ok = nyquist_ok(fs, fmax)
        print(f"fs = {fs}Hz · fmax = {fmax}Hz · 奈奎斯特率 = {2*fmax}Hz")
        print(f"判定: fs {'≥' if ok else '<'} 2·fmax → {'✅ 无失真' if ok else '⚠️ 欠采样·将发生混叠'}")
    elif args.min:
        fmax = args.min
        need = min_sample_rate(fmax)
        print(f"最高频率 fmax = {fmax}Hz")
        print(f"最小采样率 = {need}Hz (奈奎斯特率)")
        print(f"工程建议: 留 10-20% 余量 → {int(need*1.1)}-{int(need*1.2)}Hz")
    elif args.alias_demo:
        fs, fmax = args.alias_demo
        print(alias_demo(fs, fmax)["verdict"])
    else:
        ap.print_help()
        return 1
    print(f"\n{_stamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
