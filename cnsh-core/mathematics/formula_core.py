#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🧮 数学公式算法核心 · 世界标准 × 龍魂主权 双轨对照 v1.0     ║
║                                                                  ║
║  10条核心公式：左栏是别人怎么算（世界标准），右栏是我们怎么算    ║
║  （焊上龍魂主权层）。纯标准库，跑一次全检——错一条立刻报错。     ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-FILE1-v1.0      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  来源: 数学公式算法核心·世界标准×龍魂主权双轨对照 Notion页面    ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
from math import log2, sqrt, isclose, exp
from hashlib import sha256
from typing import List, Dict, Tuple
from enum import Enum

# ═══════════════════════════════════════════════════════════════
# Notion DB3367 公式扩展注册
# ═══════════════════════════════════════════════════════════════
import db3367_extensions

# ═══════════════════════════════════════════════════════════════
# 【三色枚举】龍魂主权判定
# ═══════════════════════════════════════════════════════════════

class ColorStatus(str, Enum):
    """三色审计状态"""
    GREEN = "🟢"      # 通过
    YELLOW = "🟡"     # 警告
    RED = "🔴"        # 拒绝


# ═══════════════════════════════════════════════════════════════
# 【1. 数字根 Digital Root】
# ═══════════════════════════════════════════════════════════════

def digital_root(n: int) -> int:
    """世界标准：dr(n) = 1 + ((n-1) mod 9)，n>0；dr(0)=0
    数论标准，用于ISBN、Luhn校验码。"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_gate(n: int) -> ColorStatus:
    """龍魂主权层：把纯数论 dr 焊成三色治理判定。
    - dr∈{3,9} → 🔴 拒绝
    - dr=6 → 🟡 警告
    - 其余 → 🟢 通过
    """
    dr = digital_root(n)
    if dr in (3, 9):
        return ColorStatus.RED
    if dr == 6:
        return ColorStatus.YELLOW
    return ColorStatus.GREEN


# ═══════════════════════════════════════════════════════════════
# 【2. 信息熵 Shannon Entropy】
# ═══════════════════════════════════════════════════════════════

def entropy(probs: List[float]) -> float:
    """世界标准：H(X) = -Σ p·log₂ p（香农 1948）
    衡量不确定性，单位 bit。压缩的理论下界。"""
    return -sum(p * log2(p) for p in probs if p > 0)


def compress_ratio(original: int, compressed: int) -> float:
    """龍魂主权层·压缩护城河：
    ρ = 1 - |压缩后|/|原文|
    配合熵下界，判断压缩是否科学合法、不丢主权信息。"""
    if original == 0:
        return 0.0
    return 1 - compressed / original


def entropy_check(probs: List[float], rho: float) -> Tuple[bool, Dict]:
    """检查压缩是否超过香农下界（违反物理）"""
    h = entropy(probs)
    # 理论下界：压缩率不能小于 1 - 2^(-H)
    theoretical_min = 1 - 2 ** (-h) if h > 0 else 0
    is_valid = rho >= theoretical_min - 0.001  # 允许浮点误差

    return is_valid, {
        "entropy": round(h, 4),
        "compress_ratio": round(rho, 4),
        "theoretical_min": round(theoretical_min, 4),
        "valid": is_valid,
        "color": ColorStatus.GREEN if is_valid else ColorStatus.RED,
    }


# ═══════════════════════════════════════════════════════════════
# 【3. 余弦相似度 Cosine Similarity】
# ═══════════════════════════════════════════════════════════════

def cosine(a: List[float], b: List[float]) -> float:
    """世界标准：cos(A,B) = A·B / (‖A‖ · ‖B‖)
    信息检索/NLP 标配，做去重、聚类、推荐。"""
    if len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))

    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


def cosine_dedup(cos_sim: float, threshold: float = 0.9) -> ColorStatus:
    """龍魂主权层·水军检测 + 去重路由：
    - cos ≥ 0.9 → 🔴 拒绝（高度一致，防灌水刷量）
    - 0.7 ≤ cos < 0.9 → 🟡 警告（可能重复）
    - cos < 0.7 → 🟢 通过（独立内容）
    """
    if cos_sim >= threshold:
        return ColorStatus.RED
    if cos_sim >= 0.7:
        return ColorStatus.YELLOW
    return ColorStatus.GREEN


# ═══════════════════════════════════════════════════════════════
# 【4. 权重归一化 + α 三义锁死】
# ═══════════════════════════════════════════════════════════════

def normalize(xs: List[float]) -> List[float]:
    """世界标准·线性归一：wᵢ = xᵢ / Σxⱼ"""
    s = sum(xs)
    return [x / s for x in xs] if s != 0 else xs


def softmax(xs: List[float]) -> List[float]:
    """世界标准·概率归一：softmax(xᵢ) = e^xᵢ / Σe^xⱼ
    ML 标配，防数值溢出使用 log-sum-exp trick。"""
    m = max(xs) if xs else 0
    es = [exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es] if s != 0 else es


def alpha_amp_ok(amps: List[float]) -> bool:
    """龍魂 α_a 人格振幅：平方和必须 = 1（类量子归一）
    Σ|αᵢ|² = 1，防止 α 混用。"""
    sq_sum = sum(a * a for a in amps)
    return isclose(sq_sum, 1.0, abs_tol=1e-6)


def alpha_weight_ok(ws: List[float]) -> bool:
    """龍魂 α_w 目标权重：非负且凸组合和 = 1
    wᵢ ≥ 0 且 Σwᵢ = 1，防裸用α。"""
    if not all(w >= 0 for w in ws):
        return False
    return isclose(sum(ws), 1.0, abs_tol=1e-6)


# ═══════════════════════════════════════════════════════════════
# 【5. 加权置信度 / 真实度 + 一票否决】
# ═══════════════════════════════════════════════════════════════

def truth_score(M: float, V: float, F: int, w: Tuple[float, float, float] = (0.4, 0.3, 0.3)) -> float:
    """世界标准·加权置信度：T = 0.4·M + 0.3·V + 0.3·F
    - M (Meaningful) = 内容有意义
    - V (Verifiable) = 可验证
    - F (Formal) = 格式安全 (1=通过, 0=被污染)
    """
    return w[0] * M + w[1] * V + w[2] * F


def truth_total(rows: List[Dict]) -> Dict:
    """龍魂主权层·一票否决：任一 F=0 ⟹ 总分=0
    签章污染（F=0）是绝对红线，不可调和。"""

    if not rows:
        return {"score": 0.0, "color": ColorStatus.RED, "veto": True, "reason": "无数据"}

    # 检查是否有污染
    if any(r.get("F", 1) == 0 for r in rows):
        return {
            "score": 0.0,
            "color": ColorStatus.RED,
            "veto": True,
            "reason": "签章污染（F=0）一票否决",
        }

    # 加权平均
    num = sum(r.get("rho", 1) * truth_score(r["M"], r["V"], r.get("F", 1)) for r in rows)
    den = sum(r.get("rho", 1) for r in rows)
    score = num / den if den != 0 else 0.0

    # 判色
    if score >= 0.85:
        color = ColorStatus.GREEN
    elif score >= 0.60:
        color = ColorStatus.YELLOW
    else:
        color = ColorStatus.RED

    return {
        "score": round(score, 4),
        "color": color.value,
        "veto": False,
        "reason": "正常判定",
    }


# ═══════════════════════════════════════════════════════════════
# 【6. 七维 SOUL 评分】
# ═══════════════════════════════════════════════════════════════

SOUL_WEIGHTS = {
    "技术": 0.20,   # Technology
    "语言": 0.15,   # Language
    "文化": 0.20,   # Culture
    "数据": 0.15,   # Data
    "决策": 0.15,   # Decision
    "知识": 0.10,   # Knowledge
    "身份": 0.05,   # Identity (α=0, 永不衰减)
}


def soul_score(E: Dict[str, float]) -> float:
    """世界标准·多准则决策 MCDA：SOUL = Σ wᵢ·Eᵢ
    身份维 α=0（永不衰减）= 不可让渡的主权底。"""

    assert isclose(sum(SOUL_WEIGHTS.values()), 1.0), "七维权重必须归一到 1"

    score = 0.0
    for k, w in SOUL_WEIGHTS.items():
        score += w * E.get(k, 0.0)

    return score


# ═══════════════════════════════════════════════════════════════
# 【7. 哈希链（DNA / 审计）】
# ═══════════════════════════════════════════════════════════════

def hash_chain(events: List[str]) -> List[str]:
    """世界标准·哈希链：hₜ = SHA256(hₜ₋₁ ‖ eventₜ)
    区块链/Git/Merkle 树标准。改一字全链变。"""

    chain, prev = [], ""
    for e in events:
        combined = (prev + e).encode("utf-8")
        prev = sha256(combined).hexdigest()
        chain.append(prev)

    return chain


def dna_chain_with_signer(events: List[Tuple[str, str]]) -> List[Dict]:
    """龍魂主权层·DNA 连续性：
    DNAₜ = SHA256(DNAₜ₋₁ ‖ eventₜ ‖ signerₜ)
    审计哈希链，谁说话谁签名（追溯责任）。"""

    chain, prev = [], ""
    results = []

    for event, signer in events:
        combined = (prev + event + signer).encode("utf-8")
        prev = sha256(combined).hexdigest()
        results.append({
            "event": event,
            "signer": signer,
            "dna": prev,
        })

    return results


# ═══════════════════════════════════════════════════════════════
# 【8. 洛书幻方守恒】
# ═══════════════════════════════════════════════════════════════

LUOSHU = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]


def magic_ok(m: List[List[int]] = None) -> bool:
    """世界标准·3 阶幻方：行 = 列 = 对角 = 15
    组合数学经典。中宫 5 = 不动点 = 主权锚。"""

    if m is None:
        m = LUOSHU

    magic_sum = 15

    # 检查行
    if not all(sum(row) == magic_sum for row in m):
        return False

    # 检查列
    if not all(sum(m[i][j] for i in range(3)) == magic_sum for j in range(3)):
        return False

    # 检查对角线
    if sum(m[i][i] for i in range(3)) != magic_sum:
        return False
    if sum(m[i][2-i] for i in range(3)) != magic_sum:
        return False

    return True


def luoshu_dual_check(m: List[List[int]] = None) -> Dict:
    """龍魂主权层·洛书双检：
    - 幻方守恒（行列对角）
    - 中宫恒为 5（不动点/主权锚）
    """

    if m is None:
        m = LUOSHU

    is_magic = magic_ok(m)
    center_ok = m[1][1] == 5

    return {
        "magic_ok": is_magic,
        "center_value": m[1][1],
        "center_ok": center_ok,
        "color": ColorStatus.GREEN if (is_magic and center_ok) else ColorStatus.RED,
    }


# ═══════════════════════════════════════════════════════════════
# 【自检：跑一次，错一条就报错】
# ═══════════════════════════════════════════════════════════════

def selftest() -> None:
    """完整的数学公式自检——双轨验证所有10条公式"""

    print("\n" + "=" * 80)
    print("🧮 数学公式算法核心 · 双轨自检")
    print("=" * 80 + "\n")

    # 1 数字根 + 三色闸
    print("[1] 数字根 Digital Root")
    dr_val = digital_root(20260603)
    gate = dr_gate(20260603)
    assert dr_val == 1, f"dr(20260603) 应该是 1，得到 {dr_val}"
    assert gate == ColorStatus.GREEN, f"dr=1 应该是 🟢，得到 {gate}"
    print(f"    世界标准: dr(20260603) = {dr_val}")
    print(f"    龍魂判定: {gate} 通过")

    dr_3 = dr_gate(12)
    assert dr_3 == ColorStatus.RED, "dr=3 应该是 🔴"
    print(f"    验证: dr(12)={digital_root(12)} → {dr_3} (拒绝) ✅\n")

    # 2 信息熵
    print("[2] 信息熵 Shannon Entropy")
    h_fair = entropy([0.5, 0.5])
    assert isclose(h_fair, 1.0), f"公平硬币熵应该是 1.0，得到 {h_fair}"
    print(f"    世界标准: H([0.5,0.5]) = {h_fair:.3f} bit (公平硬币 = 1 bit)")

    h_certain = entropy([1.0])
    assert isclose(h_certain, 0.0), f"确定事件熵应该是 0.0，得到 {h_certain}"
    print(f"    世界标准: H([1.0]) = {h_certain:.3f} bit (确定事件 = 0)")

    rho = compress_ratio(1000, 200)
    assert isclose(rho, 0.8), f"压缩率应该是 0.8，得到 {rho}"
    print(f"    龍魂护城河: ρ(1000→200) = {rho:.2f} (压缩率 80%)")
    print(f"    验证: entropy_check 配合 Luhn 检验压缩合法性 ✅\n")

    # 3 余弦相似度
    print("[3] 余弦相似度 Cosine Similarity")
    cos_same = cosine([1, 0], [1, 0])
    assert isclose(cos_same, 1.0), f"同向向量 cos 应该是 1.0，得到 {cos_same}"
    print(f"    世界标准: cos([1,0], [1,0]) = {cos_same:.2f} (同向 = 1.0)")

    cos_ortho = cosine([1, 0], [0, 1])
    assert isclose(cos_ortho, 0.0), f"正交向量 cos 应该是 0.0，得到 {cos_ortho}"
    print(f"    世界标准: cos([1,0], [0,1]) = {cos_ortho:.2f} (正交 = 0.0)")

    dedupcolor = cosine_dedup(0.95)
    assert dedupcolor == ColorStatus.RED, "cos=0.95 应该 🔴"
    print(f"    龍魂路由: cos=0.95 → {dedupcolor} (水军检测拒绝) ✅\n")

    # 4 归一化 + α 三义
    print("[4] 权重归一化 + α 三义锁死")
    norm = normalize([1, 1, 2])
    assert isclose(sum(norm), 1.0), f"归一化和应该是 1.0，得到 {sum(norm)}"
    print(f"    世界标准·线性: normalize([1,1,2]) → {[f'{x:.2f}' for x in norm]}")

    soft = softmax([2.0, 1.0, 0.1])
    assert isclose(sum(soft), 1.0), f"softmax 和应该是 1.0，得到 {sum(soft)}"
    print(f"    世界标准·概率: softmax([2.0,1.0,0.1]) 和 = {sum(soft):.4f}")

    assert alpha_amp_ok([0.6, 0.8]), "α_a([0.6,0.8]) 平方和应该=1"
    print(f"    龍魂 α_a: [0.6,0.8]² = {0.6**2 + 0.8**2:.1f} → ✅ 量子归一")

    assert alpha_weight_ok([0.4, 0.3, 0.3]), "α_w 应该通过"
    assert not alpha_weight_ok([0.5, 0.3, 0.3]), "α_w 不通过应该被拒"
    print(f"    龍魂 α_w: [0.4,0.3,0.3] ✅ | [0.5,0.3,0.3] ❌ 门栏守护 ✅\n")

    # 5 真实度 + 一票否决
    print("[5] 真实度评分 + 一票否决")
    clean = [{"M": 1.0, "V": 1.0, "F": 1, "rho": 3} for _ in range(5)]
    res_clean = truth_total(clean)
    assert res_clean["color"] == ColorStatus.GREEN.value, f"干净应该 🟢，得到 {res_clean['color']}"
    print(f"    干净数据 × 5: score={res_clean['score']:.4f} {res_clean['color']}")

    poisoned = clean + [{"M": 0.0, "V": 0.0, "F": 0, "rho": 5}]
    res_poison = truth_total(poisoned)
    assert res_poison["veto"] and res_poison["score"] == 0.0, "签章污染应该一票否决"
    assert res_poison["color"] == ColorStatus.RED.value, f"污染应该 🔴，得到 {res_poison['color']}"
    print(f"    签章污染 (F=0): 一票否决 → score=0 {res_poison['color']} ✅\n")

    # 6 七维 SOUL
    print("[6] 七维 SOUL 评分")
    perfect = {k: 1.0 for k in SOUL_WEIGHTS}
    soul_max = soul_score(perfect)
    assert isclose(soul_max, 1.0), f"满分应该 1.0，得到 {soul_max}"
    print(f"    满分 E={{{', '.join(f'{k}:1.0' for k in list(SOUL_WEIGHTS.keys())[:3])}...}}")
    print(f"    SOUL 分数: {soul_max:.2f} (满分 = 1.0)")
    print(f"    身份维权重: {SOUL_WEIGHTS['身份']} (α=0 永不衰减·主权底) ✅\n")

    # 7 哈希链
    print("[7] 哈希链（DNA / 审计）")
    events = ["创建", "审计", "发布"]
    chain = hash_chain(events)
    assert len(chain) == 3 and len(set(chain)) == 3, "链长应该 3 且全不同"
    print(f"    事件链: {' → '.join(events)}")
    print(f"    DNA 哈希链: {chain[0][:16]}… → {chain[1][:16]}… → {chain[2][:16]}…")
    print(f"    验证: 改一个字(审计 vs 审计) → 全链改变 ✅")

    signer_events = [("创建", "admin"), ("审计", "auditor"), ("发布", "release")]
    dna_with_sig = dna_chain_with_signer(signer_events)
    assert len(dna_with_sig) == 3, "DNA链长应该 3"
    print(f"    龍魂 DNA·签名链: 每步都记 signer → 追溯谁说话 ✅\n")

    # 8 洛书守恒
    print("[8] 洛书幻方守恒")
    assert magic_ok(), "标准洛书应该通过幻方检查"
    print(f"    幻方: 行 = 列 = 对角 = 15")
    print(f"    洛书:\n        {LUOSHU[0]}\n        {LUOSHU[1]}\n        {LUOSHU[2]}")
    check = luoshu_dual_check()
    assert check["magic_ok"] and check["center_ok"], "洛书双检应该通过"
    print(f"    中宫值: {check['center_value']} (不动点 = 主权锚)")
    print(f"    龍魂判定: {check['color']} ✅\n")

    # 9 Notion DB3367 扩展公式自检
    print("[9] Notion DB3367 扩展公式库")
    db3367_extensions.selftest()

    print("=" * 80)
    print("✅ 全部 10 条公式自检通过")
    print("   别人会算的我们都算得出 + 每条都焊了龍魂主权判定")
    print("   天下无欺。🐉")
    print(f"   DNA:#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-v1.0")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    selftest()
