#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧮 数学公式核心 · CNSH 双视角封装层 v2.1
═══════════════════════════════════════════════════════════════════════════

定位：把 formula_core_v2.py 里的单公式运算和 yijing_engine.py 的卦象输出，
      全部封装成 `{M::, CNSH::}` 双视角格式。

使用方式：
    from formula_core_cnsh import dr_gate_cnsh, decision_chain_cnsh, complete_divination_cnsh
    result = dr_gate_cnsh(20260603)
    # result == {"M::": {...}, "CNSH::": {...}}

DNA：    #龍芯⚡️2026-06-29-MATH-FORMULA-CORE-CNSH-v2.1-DUAL-PERSPECTIVE
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG:     A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计：🟢 通过
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import os
import sys
import hashlib
import json
import time
from typing import Dict, Any, Optional

# 当前文件在 formula 目录；易经引擎在 scripts/yijing_algorithm
_YIJING_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "scripts", "yijing_algorithm")
)
if _YIJING_DIR not in sys.path:
    sys.path.insert(0, _YIJING_DIR)

# 导入核心实现
import formula_core_v2 as fc
import formula_chain_v2 as fchain
import yijing_engine as ye

# 从决策链复用确认码/封印，保持唯一来源
CONFIRM_CODE = fchain.CONFIRM_CODE
SEAL_CODE = fchain.SEAL_CODE


# ═════════ 通用封装器 ═════════

def _color_to_policy(color: str) -> str:
    return {"🟢": "pass", "🟡": "hold", "🔴": "reject"}.get(color, "error")


def _make_dna(name: str, payload: Dict[str, Any]) -> str:
    """基于负载生成确定性 DNA；若需每次不同可额外加时间戳"""
    canon = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    h = hashlib.sha256(f"{name}|{canon}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{name}-{h}"


def cnsh_package(
    name: str,
    payload: Dict[str, Any],
    audit: str,
    policy: Optional[str] = None,
    dna: str = ""
) -> Dict[str, Any]:
    """
    把任意公式/引擎输出封装成 CNSH 双视角格式。

    M::    → 机器可读：type / status / payload
    CNSH:: → 主权视角：dna / gate / seal / audit / policy / trace_hash
    """
    policy = policy or _color_to_policy(audit)
    status = _color_to_policy(audit)
    if not dna:
        dna = _make_dna(name, payload)
    trace_hash = hashlib.sha256(
        json.dumps({"name": name, "payload": payload, "audit": audit},
                   ensure_ascii=False, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]

    return {
        "M::": {
            "type": name,
            "status": status,
            "payload": payload,
        },
        "CNSH::": {
            "dna": dna,
            "gate": CONFIRM_CODE,
            "seal": SEAL_CODE,
            "audit": audit,
            "policy": policy,
            "trace_hash": trace_hash,
        },
    }


# ═════════ 单公式 CNSH 封装 ═════════

def temporal_decay_cnsh(T: float, alpha_tau: float) -> Dict[str, Any]:
    eta = fc.temporal_decay(T, alpha_tau)
    return cnsh_package("temporal_decay", {"T": T, "alpha_tau": alpha_tau, "eta": eta}, "🟢")


def content_contribution_cnsh(R: float, I: float, T: float, alpha_tau: float) -> Dict[str, Any]:
    C = fc.content_contribution(R, I, T, alpha_tau)
    return cnsh_package("content_contribution", {"R": R, "I": I, "T": T, "alpha_tau": alpha_tau, "C": C}, "🟢")


def digital_root_cnsh(n: int) -> Dict[str, Any]:
    dr = fc.digital_root(n)
    return cnsh_package("digital_root", {"n": n, "dr": dr}, "🟢")


def dr_gate_cnsh(n: int) -> Dict[str, Any]:
    gate = fc.dr_gate(n)
    return cnsh_package("dr_gate", {"n": n, "dr": fc.digital_root(n), "gate": gate}, gate)


def five_element_cnsh(n: int) -> Dict[str, Any]:
    element = fc.five_element(n)
    return cnsh_package("five_element", {"n": n, "dr": fc.digital_root(n), "wuxing": element}, "🟢")


def wuxing_vector_cnsh(text: str) -> Dict[str, Any]:
    vec = fc.wuxing_vector(text)
    return cnsh_package("wuxing_vector", {"text": text, "vector": vec}, "🟢")


def cosine_cnsh(a, b) -> Dict[str, Any]:
    sim = fc.cosine(a, b)
    color = "🟢" if sim >= 0.9 else ("🟡" if sim >= 0.6 else "⚪")
    return cnsh_package("cosine", {"similarity": round(sim, 4)}, color)


def normalize_cnsh(xs) -> Dict[str, Any]:
    vec = fc.normalize(xs)
    ok = abs(sum(vec) - 1.0) < 1e-6 if sum(xs) != 0 else True
    return cnsh_package("normalize", {"input": xs, "output": vec, "sum": round(sum(vec), 6)},
                        "🟢" if ok else "🔴")


def alpha_amp_ok_cnsh(amps) -> Dict[str, Any]:
    ok = fc.alpha_amp_ok(amps)
    return cnsh_package("alpha_amp_ok", {"amps": amps, "valid": ok}, "🟢" if ok else "🔴")


def alpha_weight_ok_cnsh(ws) -> Dict[str, Any]:
    ok = fc.alpha_weight_ok(ws)
    return cnsh_package("alpha_weight_ok", {"weights": ws, "valid": ok}, "🟢" if ok else "🔴")


def truth_total_cnsh(rows, weights=None) -> Dict[str, Any]:
    result = fc.truth_total(rows, weights)
    return cnsh_package("truth_total",
                        {"score": result["score"], "veto": result["veto"], "color": result["color"]},
                        result["color"])


def soul_score_cnsh(E: Dict[str, float]) -> Dict[str, Any]:
    score = fc.soul_score(E)
    color = "🟢" if score >= 0.85 else ("🟡" if score >= 0.6 else "🔴")
    return cnsh_package("soul_score", {"score": round(score, 4)}, color)


def hash_chain_cnsh(events) -> Dict[str, Any]:
    chain = fc.hash_chain(events)
    return cnsh_package("hash_chain", {"events": len(events), "tail": chain[-1][:16] if chain else ""}, "🟢")


def magic_ok_cnsh(m=fc.LUOSHU) -> Dict[str, Any]:
    ok = fc.magic_ok(m)
    return cnsh_package("magic_ok", {"lo_shu_valid": ok}, "🟢" if ok else "🔴")


def risk_tri_color_cnsh(impact: float, uncertainty: float, boundary: float) -> Dict[str, Any]:
    color = fc.risk_tri_color(impact, uncertainty, boundary)
    return cnsh_package("risk_tri_color",
                        {"impact": impact, "uncertainty": uncertainty, "boundary": boundary, "risk_color": color},
                        color)


def conservation_score_cnsh(主控, 任务, 边界, 留痕, 验收) -> Dict[str, Any]:
    S = fc.conservation_score(主控, 任务, 边界, 留痕, 验收)
    color = "🟢" if S >= 13 else ("🟡" if S >= 10 else ("🟡" if S >= 7 else "🔴"))
    return cnsh_package("conservation_score", {"S": S}, color)


def decision_path_score_cnsh(可执行, 安全, 主线, 验证, 风险, H_人性) -> Dict[str, Any]:
    D = fc.decision_path_score(可执行, 安全, 主线, 验证, 风险, H_人性)
    return cnsh_package("decision_path_score", {"D": round(D, 4)}, "🟢")


def human_bias_cnsh(欲望, 损失规避, 即时偏好) -> Dict[str, Any]:
    H = fc.human_bias(欲望, 损失规避, 即时偏好)
    color = "🟢" if H <= 8 else ("🟡" if H <= 27 else "🔴")
    return cnsh_package("human_bias", {"H_人性": round(H, 4)}, color)


def persona_contribution_cnsh(R, I, T_lv, B_seven, W, F, B_test) -> Dict[str, Any]:
    PC = fc.persona_contribution(R, I, T_lv, B_seven, W, F, B_test)
    return cnsh_package("persona_contribution", {"PC": round(PC, 4)}, "🟢")


def seven_dim_bonus_cnsh(covered_dims: int) -> Dict[str, Any]:
    B = fc.seven_dim_bonus(covered_dims)
    return cnsh_package("seven_dim_bonus", {"covered_dims": covered_dims, "bonus": B}, "🟢")


def activity_color_cnsh(days: int) -> Dict[str, Any]:
    color = fc.activity_color(days)
    policy = {"🔥": "pass", "✅": "pass", "⚠️": "hold", "❌": "reject"}.get(color, "error")
    return cnsh_package("activity_color", {"days": days, "activity_color": color}, color, policy=policy)


def sovereignty_index_cnsh(tian: float, di: float, ren: float) -> Dict[str, Any]:
    si = fc.sovereignty_index(tian, di, ren)
    return cnsh_package("sovereignty_index",
                        {"SI": si["SI"], "color": si["color"], "veto": si.get("veto", False),
                         "breakdown": si.get("breakdown", {})},
                        si["color"])


def behavioral_confidence_cnsh(factors, weights) -> Dict[str, Any]:
    conf = fc.behavioral_confidence(factors, weights)
    color = "🔴" if conf == 0 else ("🟢" if conf >= 0.85 else "🟡")
    return cnsh_package("behavioral_confidence", {"conf": round(conf, 4)}, color)


def ete_confidence_cnsh(cos_sim, cultural_root, emotion_keep) -> Dict[str, Any]:
    conf = fc.ete_confidence(cos_sim, cultural_root, emotion_keep)
    color = "🟢" if conf >= 0.85 else ("🟡" if conf >= 0.6 else "🔴")
    return cnsh_package("ete_confidence", {"CONF_ETE": round(conf, 4)}, color)


def generalized_addition_cnsh(A, B, alpha, beta, gamma, delta) -> Dict[str, Any]:
    result = fc.generalized_addition(A, B, alpha, beta, gamma, delta)
    color = "🔴" if result.get("violation") else "🟢"
    return cnsh_package("generalized_addition", result, color)


def royalty_cnsh(valid_citations, Q, owner_share, auth_coef, L5) -> Dict[str, Any]:
    R = fc.royalty(valid_citations, Q, owner_share, auth_coef, L5)
    return cnsh_package("royalty", {"Royalty": round(R, 6)}, "🟢")


def dna_hash_child_cnsh(parent_hash: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    child = fc.dna_hash_child(parent_hash, payload)
    return cnsh_package("dna_hash_child", {"parent_hash": parent_hash, "child_hash": child}, "🟢")


def alpha_calibration_cnsh(eta_obs, eta_init, T_days) -> Dict[str, Any]:
    alpha = fc.alpha_calibration(eta_obs, eta_init, T_days)
    T_half = fc.half_life(alpha) if alpha else None
    return cnsh_package("alpha_calibration",
                        {"alpha": round(alpha, 4), "half_life": T_half}, "🟢")


def wuxing_hedge_cnsh(克制衡, 疏导, 补益, 均衡, 链路健康度) -> Dict[str, Any]:
    H = fc.wuxing_hedge(克制衡, 疏导, 补益, 均衡, 链路健康度)
    color = "🟢" if H >= 0.8 else ("🟡" if H >= 0.5 else "🔴")
    return cnsh_package("wuxing_hedge", {"H_五行": round(H, 4)}, color)


# ═════════ 决策链 & 易经 CNSH 封装 ═════════

# 复用 formula_chain_v2 已封装的决策链
decision_chain_cnsh = fchain.decision_chain_cnsh


def generate_hexagram_cnsh(question: str, timestamp: Optional[float] = None) -> Dict[str, Any]:
    """易经起卦 CNSH 封装"""
    result = ye.generate_hexagram(question, timestamp)
    return cnsh_package("yijing_hexagram",
                        {"question": question,
                         "hexagram_id": result["hexagram_id"],
                         "binary": result["binary"],
                         "change_lines": result["change_lines"]},
                        "🟢")


def complete_divination_cnsh(question: str, timestamp: Optional[float] = None) -> Dict[str, Any]:
    """易经完整推演 CNSH 封装"""
    result = ye.complete_divination(question, timestamp)
    original = result["hexagrams"]["original"]
    judgment = result["judgment"]
    color = "🟢" if judgment["score"] > 0.6 else ("🟡" if judgment["score"] > 0.3 else "🔴")
    trend = judgment["details"]["di_dao"]["text"]
    return cnsh_package("yijing_divination",
                        {"question": question,
                         "本卦": original["name"],
                         "综合分": judgment["score"],
                         "trend": trend,
                         "advice": judgment["advice"]},
                        color)


# ═════════ 自检 ═════════

def selftest() -> None:
    """CNSH 双视角封装层自检"""
    print("=" * 80)
    print("🧮 数学公式核心 · CNSH 双视角封装层 v2.1 自检")
    print("=" * 80)

    # 1. 单公式封装结构
    r1 = dr_gate_cnsh(20260603)
    assert "M::" in r1 and "CNSH::" in r1
    assert r1["M::"]["status"] == "pass"
    assert r1["CNSH::"]["audit"] == "🟢"
    assert r1["CNSH::"]["gate"] == CONFIRM_CODE
    print("[1] dr_gate_cnsh 双视角结构正确 ✅")

    # 2. 红数字根应 reject
    r2 = dr_gate_cnsh(12)
    assert r2["M::"]["status"] == "reject"
    assert r2["CNSH::"]["policy"] == "reject"
    print("[2] dr_gate_cnsh 红数字根 policy=reject ✅")

    # 3. 三才主权封装
    r3 = sovereignty_index_cnsh(0.9, 0.85, 0.8)
    assert r3["M::"]["payload"]["SI"] > 0
    assert r3["CNSH::"]["audit"] == "🟢"
    print("[3] sovereignty_index_cnsh ✅")

    # 4. 五行对冲封装
    r4 = wuxing_hedge_cnsh(0.9, 0.9, 0.9, 0.9, 0.9)
    assert r4["M::"]["status"] == "pass"
    print("[4] wuxing_hedge_cnsh ✅")

    # 5. 易经起卦封装
    r5 = generate_hexagram_cnsh("龍魂系统自检", 1782710383.0)
    assert 1 <= r5["M::"]["payload"]["hexagram_id"] <= 64
    print("[5] generate_hexagram_cnsh ✅")

    # 6. 易经完整推演封装
    r6 = complete_divination_cnsh("龍魂系统未来走势", 1782710383.0)
    assert "本卦" in r6["M::"]["payload"]
    assert r6["CNSH::"]["audit"] in ("🟢", "🟡", "🔴")
    print("[6] complete_divination_cnsh ✅")

    # 7. 决策链封装（复用）
    r7 = decision_chain_cnsh(
        20260603, [0.05, 0.05], [1, 1],
        tian=0.9, di=0.9, ren=0.9,
        dna="#龍芯⚡️2026-06-29-DECISION-CNSH-TEST"
    )
    assert r7["M::"]["status"] == "pass"
    assert r7["CNSH::"]["audit"] == "🟢"
    print("[7] decision_chain_cnsh 复用正确 ✅")

    print("=" * 80)
    print("🟢 CNSH 双视角封装层自检通过")
    print("   DNA: #龍芯⚡️2026-06-29-MATH-FORMULA-CORE-CNSH-v2.1-DUAL-PERSPECTIVE")
    print("=" * 80)


if __name__ == "__main__":
    selftest()
