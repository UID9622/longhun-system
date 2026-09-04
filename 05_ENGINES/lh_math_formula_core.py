#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂 · 数学公式算法核心 v2.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-MATH-FORMULA-CORE-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ═══════════════════════════════════════════
# 核心理念：
#   别人会算的世界标准算法，我们都算得出；
#   我们在上面焊了一层主权判定（三色 / 熔断 / DNA）。
#
# 覆盖十条核心公式 + 三才主权指数 + 五行 + 洛书对偶校验。
# 每条公式带 assert 自检，错一条即报错。
# ═══════════════════════════════════════════
"""

from __future__ import annotations
from math import log2, sqrt, isclose, exp, pi
from hashlib import sha256
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# ═══════════════════════════════════════════
# 0. 三色枚举（统一返回语义）
# ═══════════════════════════════════════════

class AuditColor(str, Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


def _color_from_score(score: float) -> AuditColor:
    """根据综合分返回三色标记。"""
    if score >= 0.85:
        return AuditColor.GREEN
    if score >= 0.60:
        return AuditColor.YELLOW
    return AuditColor.RED


# ═══════════════════════════════════════════
# 1. 数字根 Digital Root
# ═══════════════════════════════════════════

def digital_root(n: int) -> int:
    """世界标准：dr(n)=1+((n-1) mod 9), n>0; dr(0)=0。等价于按 9 取余。"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_gate(n: int) -> AuditColor:
    """龍魂主权层：把纯数论 dr 焊成三色治理判定。

    dr∈{3,9} → 🔴 拒绝
    dr=6    → 🟡 警告
    其余    → 🟢 通过
    """
    dr = digital_root(n)
    if dr in (3, 9):
        return AuditColor.RED
    if dr == 6:
        return AuditColor.YELLOW
    return AuditColor.GREEN


# ═══════════════════════════════════════════
# 2. 信息熵 Shannon Entropy
# ═══════════════════════════════════════════

def entropy(probs: List[float]) -> float:
    """世界标准：H(X)=-Σ p·log2 p（Shannon 1948），单位 bit。"""
    return -sum(p * log2(p) for p in probs if p > 0)


def compress_ratio(original: int, compressed: int) -> float:
    """龍魂：压缩护城河 ρ = 1 - |压缩后|/|原文|，clamp 到 [0, 1]。

    original ≤ 0 时返回 0（无法评估压缩率）。
    """
    if original <= 0:
        return 0.0
    ratio = 1 - compressed / original
    return max(0.0, min(1.0, ratio))


# ═══════════════════════════════════════════
# 3. 余弦相似度 Cosine Similarity
# ═══════════════════════════════════════════

def cosine(a: List[float], b: List[float]) -> float:
    """世界标准：cos(A,B)=A·B/(‖A‖‖B‖)。信息检索/NLP 标配。

    熔断：维度不匹配直接抛 ValueError — 静默污染比崩溃更危险。
    """
    if len(a) != len(b):
        raise ValueError(f"向量维度不匹配: len(a)={len(a)} len(b)={len(b)}，拒绝静默截断")
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


# ═══════════════════════════════════════════
# 4. 权重归一化 + α 三义锁死
# ═══════════════════════════════════════════

def normalize(xs: List[float]) -> List[float]:
    """世界标准·线性归一：wᵢ = xᵢ / Σxⱼ。

    Σxⱼ=0 时返回等权重（1/N），避免全零输出。
    """
    s = sum(xs)
    if s == 0:
        n = len(xs)
        return [1.0 / n] * n if n else []
    return [x / s for x in xs]


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


# ═══════════════════════════════════════════
# 5. 真实度评分 + 一票否决
# ═══════════════════════════════════════════

def truth_score(M: float, V: float, F: int, w: Tuple[float, float, float] = (0.4, 0.3, 0.3)) -> float:
    """龍魂：T = 0.4·M + 0.3·V + 0.3·F（标准加权平均）。"""
    return w[0] * M + w[1] * V + w[2] * F


@dataclass
class TruthRow:
    M: float  # 动机可信度
    V: float  # 可验证性
    F: int    # 格式安全（0=污染，1=干净）
    rho: float = 1.0  # 权重


def truth_total(rows: List[TruthRow]) -> Dict[str, Any]:
    """加权平均 + 主权熔断：任一 F=0 ⟹ 总分=0（格式安全一票否决）。

    空列表返回 🔴 — 无数据本身就不可信。
    """
    if not rows:
        return {"score": 0.0, "color": AuditColor.RED, "veto": False, "reason": "空输入，无法评估"}
    if any(r.F == 0 for r in rows):
        return {"score": 0.0, "color": AuditColor.RED, "veto": True}
    num = sum(r.rho * truth_score(r.M, r.V, r.F) for r in rows)
    den = sum(r.rho for r in rows)
    score = num / den if den > 0 else 0.0
    return {
        "score": round(score, 4),
        "color": _color_from_score(score),
        "veto": False,
    }


# ═══════════════════════════════════════════
# 6. 七维 SOUL 评分
# ═══════════════════════════════════════════

SOUL_WEIGHTS = {
    "技术": 0.20,
    "语言": 0.15,
    "文化": 0.20,
    "数据": 0.15,
    "决策": 0.15,
    "知识": 0.10,
    "身份": 0.05,
}


def soul_score(E: Dict[str, float]) -> float:
    """龍魂：SOUL = Σ wᵢ·Eᵢ，Σwᵢ=1（标准 MCDA 加权求和）。

    身份维 α=0（永不衰减）= 不可让渡的主权底。
    缺维自动补0；>1 的值会被 clamp 到 [0, 1]（发警告但不崩溃）。
    """
    assert isclose(sum(SOUL_WEIGHTS.values()), 1.0), "七维权重必须归一到 1"
    clamped = {}
    for k in SOUL_WEIGHTS:
        v = E.get(k, 0.0)
        if v < 0 or v > 1:
            clamped[k] = max(0.0, min(1.0, v))
        else:
            clamped[k] = v
    return sum(SOUL_WEIGHTS[k] * clamped[k] for k in SOUL_WEIGHTS)


# ═══════════════════════════════════════════
# 7. 哈希链 / DNA 链
# ═══════════════════════════════════════════

def hash_chain(events: List[str], signer: str = "UID9622") -> List[str]:
    """世界标准：hₜ = SHA256(hₜ₋₁ ‖ eventₜ)。区块链/Git/Merkle 同理。

    龍魂增强：加入 signer，谁说话谁签名。
    """
    chain, prev = [], ""
    for e in events:
        prev = sha256(f"{prev}{e}{signer}".encode("utf-8")).hexdigest()
        chain.append(prev)
    return chain


def dna_chain(events: List[str], signer: str = "UID9622") -> List[str]:
    """DNA 追溯链，每条带签章。"""
    return hash_chain(events, signer=signer)


# ═══════════════════════════════════════════
# 8. 洛书幻方守恒与对偶校验
# ═══════════════════════════════════════════

LUOSHU = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]


def magic_ok(m: Optional[List[List[int]]] = None) -> bool:
    """世界标准：3 阶幻方行列对角和恒=15。中宫 5=不动点=主权锚。"""
    m = m or LUOSHU
    lines = [sum(r) for r in m] + [sum(c) for c in zip(*m)]
    lines += [m[0][0] + m[1][1] + m[2][2], m[0][2] + m[1][1] + m[2][0]]
    return all(s == 15 for s in lines)


def luoshu_dual_check() -> Dict[str, Any]:
    """龍魂：洛书对偶和=10 做反向校验。"""
    pairs = [
        (LUOSHU[0][0], LUOSHU[2][2]),  # 4 + 6
        (LUOSHU[0][2], LUOSHU[2][0]),  # 2 + 8
        (LUOSHU[0][1], LUOSHU[2][1]),  # 9 + 1
        (LUOSHU[1][0], LUOSHU[1][2]),  # 3 + 7
    ]
    ok = all(a + b == 10 for a, b in pairs)
    return {"pairs": pairs, "dual_sum_ok": ok, "center": LUOSHU[1][1]}


# ═══════════════════════════════════════════
# 9. 五行 Five Elements
# ═══════════════════════════════════════════

FIVE_ELEMENT = {
    1: "木", 2: "木",
    3: "火", 4: "火",
    5: "土", 6: "土",
    7: "金", 8: "金",
    9: "水", 0: "水",
}

ELEMENT_RELATIONS = {
    "木": {"生": "火", "克": "土"},
    "火": {"生": "土", "克": "金"},
    "土": {"生": "金", "克": "水"},
    "金": {"生": "水", "克": "木"},
    "水": {"生": "木", "克": "火"},
}


def element_of(n: int) -> str:
    """数字 → 五行。"""
    return FIVE_ELEMENT.get(digital_root(n), "土")


def element_relation(a: str, b: str) -> str:
    """两个五行之间的关系。"""
    if a == b:
        return "同"
    if ELEMENT_RELATIONS.get(a, {}).get("生") == b:
        return "生"
    if ELEMENT_RELATIONS.get(a, {}).get("克") == b:
        return "克"
    # 反向关系
    if ELEMENT_RELATIONS.get(b, {}).get("生") == a:
        return "被生"
    if ELEMENT_RELATIONS.get(b, {}).get("克") == a:
        return "被克"
    return "无关"


# ═══════════════════════════════════════════
# 10. 三才主权指数 Sovereignty Index (SI)
# ═══════════════════════════════════════════

def sovereignty_index(tian: float, di: float, ren: float,
                      weights: Tuple[float, float, float] = (0.34, 0.33, 0.33)) -> Dict[str, Any]:
    """三才主权指数：SI = 0.34·天 + 0.33·地 + 0.33·人。

    规则：
    - 天 < 0.34 一票熔断（没有天道/原则，不能放行）
    - SI ≥ 0.85 🟢 放行
    - SI ≥ 0.60 🟡 复核
    - SI < 0.60 🔴 拦截

    权重不归一 → 🟡 警告但继续计算（用实际值，非 assertion 崩溃）。
    """
    if not alpha_weight_ok(list(weights)):
        si = weights[0] * tian + weights[1] * di + weights[2] * ren
        veto = tian < 0.34
        score = 0.0 if veto else si
        return {
            "SI": round(si, 4),
            "score": round(score, 4),
            "color": AuditColor.YELLOW if not veto else AuditColor.RED,
            "veto": veto,
            "warning": "三才权重未归一化，结果仅供参考",
            "reason": "天 < 0.34，一票熔断" if veto else "权重未归一 → 🟡",
        }
    si = weights[0] * tian + weights[1] * di + weights[2] * ren
    veto = tian < 0.34
    score = 0.0 if veto else si
    return {
        "SI": round(si, 4),
        "score": round(score, 4),
        "color": AuditColor.RED if veto else _color_from_score(score),
        "veto": veto,
        "reason": "天 < 0.34，一票熔断" if veto else None,
    }


# ═══════════════════════════════════════════
# 11. 简单卦象映射（8 卦 × 3 爻）
# ═══════════════════════════════════════════

GUA_NAMES = ["坤", "震", "坎", "兑", "艮", "离", "巽", "乾"]
GUA_TRIGRAMS = {
    "乾": [1, 1, 1], "兑": [0, 1, 1], "离": [1, 0, 1], "震": [0, 0, 1],
    "巽": [1, 1, 0], "坎": [0, 1, 0], "艮": [1, 0, 0], "坤": [0, 0, 0],
}


def number_to_gua(n: int) -> str:
    """数字 → 八卦（按数字根映射）。"""
    dr = digital_root(n)
    idx = dr % 8
    return GUA_NAMES[idx]


# ═══════════════════════════════════════════
# 自检：跑一次，错一条就报错
# ═══════════════════════════════════════════

def selftest() -> Dict[str, Any]:
    """运行全部公式自检。"""
    results = []

    # 1 数字根 + 三色闸
    assert digital_root(20260603) == 1
    assert dr_gate(12) == AuditColor.RED
    assert dr_gate(15) == AuditColor.YELLOW
    assert dr_gate(20260603) == AuditColor.GREEN
    results.append("[1] 数字根+三色闸 ✅")

    # 2 信息熵
    assert isclose(entropy([0.5, 0.5]), 1.0)
    assert isclose(entropy([1.0]), 0.0)
    assert isclose(entropy([0.25] * 4), 2.0)
    assert isclose(compress_ratio(1000, 200), 0.8)
    results.append("[2] 信息熵+压缩率 ✅")

    # 3 余弦相似度
    assert isclose(cosine([1, 0], [1, 0]), 1.0)
    assert isclose(cosine([1, 0], [0, 1]), 0.0)
    results.append("[3] 余弦相似度 ✅")

    # 4 归一化 + α 三义
    assert isclose(sum(normalize([1, 1, 2])), 1.0)
    assert isclose(sum(softmax([2.0, 1.0, 0.1])), 1.0)
    assert alpha_amp_ok([0.6, 0.8])
    assert alpha_weight_ok([0.4, 0.3, 0.3])
    assert not alpha_weight_ok([0.5, 0.3, 0.3])
    results.append("[4] 归一化+α三义锁死 ✅")

    # 5 真实度 + 一票否决
    clean = [TruthRow(M=1.0, V=1.0, F=1, rho=3) for _ in range(5)]
    assert truth_total(clean)["color"] == AuditColor.GREEN
    poisoned = clean + [TruthRow(M=0.0, V=0.0, F=0, rho=5)]
    res = truth_total(poisoned)
    assert res["veto"] and res["score"] == 0.0 and res["color"] == AuditColor.RED
    results.append("[5] 真实度+一票否决 ✅")

    # 6 七维 SOUL
    assert isclose(soul_score({k: 1.0 for k in SOUL_WEIGHTS}), 1.0)
    assert isclose(soul_score({k: 0.0 for k in SOUL_WEIGHTS}), 0.0)
    results.append("[6] SOUL七维评分 ✅")

    # 7 哈希链
    ch = dna_chain(["创建", "审计", "发布"])
    assert len(ch) == 3 and len(set(ch)) == 3
    assert dna_chain(["创建"])[0] != dna_chain(["审计"])[0]
    results.append("[7] DNA哈希链 ✅")

    # 8 洛书幻方
    assert magic_ok()
    assert LUOSHU[1][1] == 5
    dual = luoshu_dual_check()
    assert dual["dual_sum_ok"]
    results.append("[8] 洛书幻方+对偶校验 ✅")

    # 9 五行
    assert element_of(1) == "木"
    assert element_of(5) == "土"
    assert element_relation("木", "火") == "生"
    assert element_relation("火", "金") == "克"
    results.append("[9] 五行生克 ✅")

    # 10 三才主权指数
    si_ok = sovereignty_index(0.95, 0.90, 0.85)
    assert si_ok["color"] == AuditColor.GREEN
    si_veto = sovereignty_index(0.3, 0.9, 0.9)
    assert si_veto["veto"] and si_veto["color"] == AuditColor.RED
    results.append("[10] 三才主权指数 ✅")

    # 11 卦象
    assert number_to_gua(1) in GUA_NAMES
    results.append("[11] 八卦映射 ✅")

    return {"status": "🟢", "passed": len(results), "details": results}


if __name__ == "__main__":
    report = selftest()
    print("=" * 64)
    print("🧮 龍魂数学公式算法核心 v2.0 · 自检报告")
    print("=" * 64)
    for line in report["details"]:
        print(line)
    print("=" * 64)
    print(f"{report['status']} 全部 {report['passed']} 组公式通过自检")
    print("DNA: #龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-MATH-FORMULA-CORE-v2.0")
    print("=" * 64)
