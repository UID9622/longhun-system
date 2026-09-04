# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-c125e7fb
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 信息论引擎 v1.0

香农信息熵在龍魂中的三重应用：
  (1) 基础数据熵   —— 度量数据不确定性
  (2) 语义熵       —— 衡量AI输出信息密度与潜在污染
  (3) 系统熵       —— 监控整体运行状态混乱度
三色映射实现从数学到治理的闭环：熵低=🟢有序 · 熵升=🟡关注 · 熵爆=🔴熔断。

知识卡: 信息论 · Information Theory（ID=109 · dr=4·木·巽宫 · 🔴底座）
落地映射: 三色审计 · 语义防火墙 · 风险传播模型 · 数字根 · 动态数字根DR*

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-INFORMATION-THEORY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_information_theory.py --entropy A,A,B,B,B     # 香农熵
  python3 bin/lh_information_theory.py --text-entropy "句子"   # 语义熵(文本)
  python3 bin/lh_information_theory.py --kl 0.6,0.4 0.5,0.5    # KL散度
  python3 bin/lh_information_theory.py --cross-entropy 0.6,0.4 0.5,0.5
  python3 bin/lh_information_theory.py --mutual-info A,B,B,A   # 互信息(成对)
  python3 bin/lh_information_theory.py --system-entropy 0.9,0.09,0.01  # 系统熵+三色
  python3 bin/lh_information_theory.py --self-test
"""

import argparse
import math
import os
import sys
from collections import Counter


def _stamp() -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


def entropy(data):
    """香农熵 H(X) = -Σ p(x)·log2(p(x))"""
    n = len(data)
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in Counter(data).values())


def kl_divergence(p, q, eps=1e-12):
    """KL散度 D_KL(P||Q) = Σ p(x)·log2(p(x)/q(x))"""
    if len(p) != len(q):
        raise ValueError("p 与 q 长度必须一致")
    return sum(pi * math.log2(pi / (qi + eps) + eps) for pi, qi in zip(p, q) if pi > 0)


def cross_entropy(p, q, eps=1e-12):
    """交叉熵 H(P,Q) = -Σ p(x)·log2(q(x))"""
    if len(p) != len(q):
        raise ValueError("p 与 q 长度必须一致")
    return -sum(pi * math.log2(qi + eps) for pi, qi in zip(p, q) if pi > 0)


def mutual_information(pairs):
    """互信息 I(X;Y) = H(X) + H(Y) - H(X,Y)"""
    x = [a for a, _ in pairs]
    y = [b for _, b in pairs]
    joint = entropy(pairs)
    return entropy(x) + entropy(y) - joint


def system_entropy(state_probs):
    """系统熵：输入各状态概率分布 → 熵值 + 三色治理判定"""
    h = -sum(p * math.log2(p) for p in state_probs if p > 0)
    if h < 1.0:
        color = "🟢 有序"
    elif h < 2.0:
        color = "🟡 关注"
    else:
        color = "🔴 熔断"
    return h, color


def self_test():
    ok = True
    # 1) 知识卡示例: entropy(["A","A","B","B","B"]) = 0.97095...
    h = entropy(["A", "A", "B", "B", "B"])
    expect = -(0.4 * math.log2(0.4) + 0.6 * math.log2(0.6))
    t1 = abs(h - expect) < 1e-9
    ok &= t1
    print(f"[1] 熵(知识卡示例) = {h:.6f} 期望={expect:.6f} {'✅' if t1 else '❌'}")
    # 2) 均匀分布熵最大: H(4种均匀)=2.0
    h4 = entropy(["a", "b", "c", "d"] * 5)
    t2 = abs(h4 - 2.0) < 1e-9
    ok &= t2
    print(f"[2] 4类均匀熵 = {h4:.6f} (应为2.0) {'✅' if t2 else '❌'}")
    # 3) KL散度非负 & 相同分布=0
    kl0 = kl_divergence([0.5, 0.5], [0.5, 0.5])
    kl1 = kl_divergence([0.9, 0.1], [0.5, 0.5])
    t3 = abs(kl0) < 1e-9 and kl1 > 0
    ok &= t3
    print(f"[3] KL(相同)=0 -> {kl0:.2e} · KL(0.9,0.1||0.5,0.5)={kl1:.4f} {'✅' if t3 else '❌'}")
    # 4) 确定性系统熵=0 · 完全混乱=1
    h_det = entropy(["A"] * 10)
    h_bin = entropy(["A", "B"] * 5)
    t4 = abs(h_det) < 1e-9 and abs(h_bin - 1.0) < 1e-9
    ok &= t4
    print(f"[4] 确定性熵={h_det:.2e} · 二态均匀熵={h_bin:.6f} {'✅' if t4 else '❌'}")
    # 5) 系统熵三色判定
    h_sys, color = system_entropy([0.98, 0.01, 0.01])
    t5 = color.startswith("🟢")
    ok &= t5
    print(f"[5] 系统熵={h_sys:.4f} → {color} {'✅' if t5 else '❌'}")
    print(f"\n🐉 信息论自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="龍魂·信息论引擎 v1.0")
    ap.add_argument("--entropy", help="香农熵, 逗号分隔(如 A,A,B,B,B)")
    ap.add_argument("--text-entropy", help="语义熵(按字统计)")
    ap.add_argument("--kl", nargs=2, help="KL散度: 两个概率分布")
    ap.add_argument("--cross-entropy", nargs=2, help="交叉熵: 两个概率分布")
    ap.add_argument("--mutual-info", help="互信息: 逗号分隔成对符号(如 A,A,B,B)")
    ap.add_argument("--system-entropy", help="系统熵+三色: 概率分布(如 0.9,0.09,0.01)")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    def _probs(s):
        return [float(v) for v in s.split(",")]

    if args.entropy:
        data = args.entropy.split(",")
        print(f"数据   = {data}")
        print(f"概率   = {dict(Counter(data))}")
        print(f"熵     = {entropy(data):.6f} bit")
    elif args.text_entropy:
        print(f"文本   = {args.text_entropy}")
        print(f"语义熵 = {entropy(list(args.text_entropy)):.6f} bit")
    elif args.kl:
        p, q = _probs(args.kl[0]), _probs(args.kl[1])
        print(f"P = {p}\nQ = {q}")
        print(f"KL散度 D_KL(P||Q) = {kl_divergence(p, q):.6f} bit")
    elif args.cross_entropy:
        p, q = _probs(args.cross_entropy[0]), _probs(args.cross_entropy[1])
        print(f"P = {p}\nQ = {q}")
        print(f"交叉熵 H(P,Q) = {cross_entropy(p, q):.6f} bit")
    elif args.mutual_info:
        vals = args.mutual_info.split(",")
        pairs = [(vals[i], vals[i + 1]) for i in range(0, len(vals) - 1, 2)]
        print(f"配对   = {pairs}")
        print(f"互信息 = {mutual_information(pairs):.6f} bit")
    elif args.system_entropy:
        probs = _probs(args.system_entropy)
        h, color = system_entropy(probs)
        print(f"状态概率 = {probs}")
        print(f"系统熵   = {h:.4f} bit → {color}")
    else:
        ap.print_help()
        return 1
    print(f"\n{_stamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
