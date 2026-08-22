#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 数学公式算法核心 · 世界标准 × 龍魂主权 双轨对照 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

每条公式：先用世界标准算法算（可查出处），再叠龍魂主权判定。
纯标准库·跑一次自检全部公式。

DNA:     #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-MATH-FORMULA-CORE-DUAL-TRACK-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
主权人:  UID9622 · 龍芯北辰

别人会算的，我们都算得出；我们多的是上面那层主权判定。
"""
from __future__ import annotations
from math import log2, sqrt, isclose, exp
from hashlib import sha256
from typing import List, Dict, Any

# ═════════ 1. 数字根 Digital Root ═════════
def digital_root(n: int) -> int:
    """世界标准：dr(n)=1+((n-1) mod 9), n>0; dr(0)=0。等价于按 9 取余。"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9

def dr_gate(n: int) -> str:
    """龍魂主权层：把纯数论 dr 焊成三色治理判定。"""
    dr = digital_root(n)
    if dr in (3, 9):
        return "🔴"   # 拒绝
    if dr == 6:
        return "🟡"   # 警告
    return "🟢"        # 通过

# ═════════ 2. 信息熵 Shannon Entropy ═════════
def entropy(probs: List[float]) -> float:
    """世界标准：H(X)=-Σ p·log2 p（Shannon 1948），单位 bit。"""
    return -sum(p * log2(p) for p in probs if p > 0)

def compress_ratio(original: int, compressed: int) -> float:
    """龍魂：压缩护城河 ρ = 1 - |压缩后|/|原文|。"""
    return 1 - compressed / original if original > 0 else 0

# ═════════ 3. 余弦相似度 Cosine Similarity ═════════
def cosine(a: List[float], b: List[float]) -> float:
    """世界标准：cos(A,B)=A·B/(‖A‖‖B‖)。信息检索/NLP 标配。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)

# ═════════ 4. 权重归一化 + α 三义锁死 ═════════
def normalize(xs: List[float]) -> List[float]:
    """世界标准·线性归一：wᵢ = xᵢ / Σxⱼ。"""
    s = sum(xs)
    return [x / s for x in xs] if s else list(xs)

def softmax(xs: List[float]) -> List[float]:
    """世界标准·概率归一：softmax(xᵢ)=e^xᵢ/Σe^xⱼ。ML 标配。"""
    m = max(xs)
    es = [exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es]

def alpha_amp_ok(amps: List[float]) -> bool:
    """龍魂 α_a 人格振幅：平方和必须=1（类量子归一）。"""
    return isclose(sum(a * a for a in amps), 1.0, abs_tol=1e-6)

def alpha_weight_ok(ws: List[float]) -> bool:
    """龍魂 α_w 目标权重：非负且凸组合和=1。"""
    return all(w >= 0 for w in ws) and isclose(sum(ws), 1.0, abs_tol=1e-6)

# ═════════ 5. 真实度评分 + 一票否决 ═════════
def truth_score(M: float, V: float, F: int, w=(0.4, 0.3, 0.3)) -> float:
    """龍魂：T = 0.4·M + 0.3·V + 0.3·F（标准加权平均）。"""
    return w[0] * M + w[1] * V + w[2] * F

def truth_total(rows: List[Dict]) -> Dict[str, Any]:
    """加权平均 + 主权熔断：任一 F=0 ⟹ 总分=0（格式安全一票否决）。"""
    if any(r["F"] == 0 for r in rows):
        return {"score": 0.0, "color": "🔴", "veto": True}
    num = sum(r["rho"] * truth_score(r["M"], r["V"], r["F"]) for r in rows)
    den = sum(r["rho"] for r in rows)
    score = num / den if den > 0 else 0
    color = "🟢" if score >= 0.85 else "🟡" if score >= 0.60 else "🔴"
    return {"score": round(score, 4), "color": color, "veto": False}

# ═════════ 6. 七维 SOUL 评分 ═════════
SOUL_W = {"技术": 0.20, "语言": 0.15, "文化": 0.20, "数据": 0.15,
          "决策": 0.15, "知识": 0.10, "身份": 0.05}

def soul_score(E: Dict[str, float]) -> float:
    """龍魂：SOUL = Σ wᵢ·Eᵢ，Σwᵢ=1（标准 MCDA 加权求和）。
    身份维 α=0（永不衰减）= 不可让渡的主权底。"""
    assert isclose(sum(SOUL_W.values()), 1.0), "七维权重必须归一到 1"
    return sum(SOUL_W[k] * E.get(k, 0.0) for k in SOUL_W)

# ═════════ 7. 哈希链（DNA / 审计） ═════════
def hash_chain(events: List[str]) -> List[str]:
    """世界标准：hₜ = SHA256(hₜ₋₁ ‖ eventₜ)。区块链/Git/Merkle 同理。"""
    chain, prev = [], ""
    for e in events:
        prev = sha256((prev + e).encode("utf-8")).hexdigest()
        chain.append(prev)
    return chain

# ═════════ 8. 洛书幻方守恒 ═════════
LUOSHU = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]

def magic_ok(m=LUOSHU) -> bool:
    """世界标准：3 阶幻方行列对角和恒=15。中宫 5=不动点=主权锚。"""
    lines = [sum(r) for r in m] + [sum(c) for c in zip(*m)]
    lines += [m[0][0] + m[1][1] + m[2][2], m[0][2] + m[1][1] + m[2][0]]
    return all(s == 15 for s in lines)

# ═════════ 自检：跑一次，错一条就报错 ═════════
def selftest() -> None:
    print("=" * 64)
    print("🧮 数学公式算法核心 · 双轨自检")
    print("=" * 64)

    # 1 数字根 + 三色闸
    assert digital_root(20260603) == 1          # 2+0+2+6+0+6+0+3=19→10→1
    assert dr_gate(12) == "🔴"                   # dr=3
    assert dr_gate(15) == "🟡"                   # dr=6
    assert dr_gate(20260603) == "🟢"            # dr=1
    print(f"[1] 数字根 dr(20260603)={digital_root(20260603)} 闸门={dr_gate(20260603)}  ✅")

    # 2 信息熵
    assert isclose(entropy([0.5, 0.5]), 1.0)     # 公平硬币=1 bit
    assert isclose(entropy([1.0]), 0.0)          # 确定事件=0
    assert isclose(entropy([0.25] * 4), 2.0)     # 四等概=2 bit
    print(f"[2] 熵([0.5,0.5])={entropy([0.5,0.5]):.3f} bit  压缩率(1000→200)={compress_ratio(1000,200):.2f}  ✅")

    # 3 余弦相似度
    assert isclose(cosine([1, 0], [1, 0]), 1.0)
    assert isclose(cosine([1, 0], [0, 1]), 0.0)
    print(f"[3] cos(同向)=1.0  cos(正交)=0.0  ✅")

    # 4 归一化 + α 三义
    assert isclose(sum(normalize([1, 1, 2])), 1.0)
    assert isclose(sum(softmax([2.0, 1.0, 0.1])), 1.0)
    assert alpha_amp_ok([0.6, 0.8])              # 0.36+0.64=1
    assert alpha_weight_ok([0.4, 0.3, 0.3])
    assert not alpha_weight_ok([0.5, 0.3, 0.3])  # 和≠1 → 不合法
    print(f"[4] normalize/softmax 和=1  α_a([0.6,0.8]) 平方和=1  α_w 守门 ✅")

    # 5 真实度 + 一票否决
    clean = [{"M": 1.0, "V": 1.0, "F": 1, "rho": 3} for _ in range(5)]
    assert truth_total(clean)["color"] == "🟢"
    poisoned = clean + [{"M": 0.0, "V": 0.0, "F": 0, "rho": 5}]  # 签章污染
    res = truth_total(poisoned)
    assert res["veto"] and res["score"] == 0.0 and res["color"] == "🔴"
    print(f"[5] 干净={truth_total(clean)['color']}  签章污染→一票否决={res['color']} (score={res['score']})  ✅")

    # 6 七维 SOUL
    assert isclose(soul_score({k: 1.0 for k in SOUL_W}), 1.0)  # 满分=1
    assert isclose(soul_score({k: 0.0 for k in SOUL_W}), 0.0)
    print(f"[6] SOUL(满分)={soul_score({k:1.0 for k in SOUL_W}):.2f}  身份维权重={SOUL_W['身份']}(α=0 永不衰减)  ✅")

    # 7 哈希链
    ch = hash_chain(["创建", "审计", "发布"])
    assert len(ch) == 3 and len(set(ch)) == 3
    assert hash_chain(["创建"])[0] != hash_chain(["审计"])[0]  # 改一字全变
    print(f"[7] DNA 哈希链尾={ch[-1][:16]}…  改一字即全链变  ✅")

    # 8 洛书守恒
    assert magic_ok()
    assert LUOSHU[1][1] == 5                      # 中宫=不动点
    print(f"[8] 洛书行列对角恒=15  中宫={LUOSHU[1][1]}(主权锚)  ✅")

    print("=" * 64)
    print("🟢 全部公式自检通过——别人会算的我们都算得出，且每条都焊了主权判定。")
    print("   天下无欺。🐉  DNA: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-MATH-FORMULA-CORE-DUAL-TRACK-v1.0")
    print("=" * 64)

if __name__ == "__main__":
    selftest()
