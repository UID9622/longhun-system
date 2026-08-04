#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🧮 根治理决策链 v2.0 · 性能+审计优化版
═══════════════════════════════════════════════════════════════════════

v1.0 → v2.0 改进：
  ✅ 五行映射带 LRU 缓存
  ✅ 三才 SI 计算缓存
  ✅ 决策链向量化
  ✅ 完整审计追踪
  ✅ SI 权重可配置
  ✅ 决策阈值动态设置

来源: UID9622 @ Downloads/计算公式/formula_chain_v2.py
DNA: #龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-FORMULA-CHAIN-v2.0-SYSTEM
"""

from __future__ import annotations
from typing import List, Dict, Optional, Tuple, Any
from functools import lru_cache
import time

from .formula_core import (
    digital_root, dr_gate, normalize, truth_score, soul_score, SOUL_W,
    AuditLog, set_config, _audit, _make_dna
)

# ═════════ 全局配置 ═════════
CHAIN_CONFIG = {
    "si_weights": (0.34, 0.33, 0.33),
    "si_thresholds": {"green": 0.85, "yellow": 0.60},
    "score_thresholds": {"green": 0.85, "yellow": 0.60},
    "enable_audit": True,
    "cache_si": True,
}

def set_chain_config(key: str, value):
    CHAIN_CONFIG[key] = value

# ═════════ 五行映射（带缓存）═════════
FIVE_ELEMENT = {
    1: "木", 2: "木", 3: "火", 4: "火", 5: "土",
    6: "金", 7: "金", 8: "水", 9: "水"
}

@lru_cache(maxsize=128)
def five_element(n: int) -> str:
    t0 = time.time()
    dr = digital_root(n)
    result = FIVE_ELEMENT[dr]
    elapsed = time.time() - t0
    dna = _make_dna("five_element", str(n))
    _audit.record("five_element", f"n={n}", f"dr={dr}→{result}", elapsed, dna)
    return result

# ═════════ 三才主权指数（带缓存）═════════
_si_cache = {}

def sovereignty_index(
    tian: float,
    di: float,
    ren: float,
    weights: Optional[Tuple[float, ...]] = None,
    use_cache: bool = True
) -> Dict[str, Any]:
    """三才主权指数·天<0.34 → 一票熔断"""
    t0 = time.time()
    weights = weights or CHAIN_CONFIG["si_weights"]
    w_tian, w_di, w_ren = weights

    cache_key = (round(tian, 6), round(di, 6), round(ren, 6), weights)
    if use_cache and CHAIN_CONFIG["cache_si"] and cache_key in _si_cache:
        result = _si_cache[cache_key]
        elapsed = time.time() - t0
        _audit.record("sovereignty_index", f"tian={tian}", "cache_hit", elapsed)
        return result

    if tian < 0.34:
        result = {
            "SI": 0.0, "color": "🔴", "veto": True,
            "reason": "主权轴不达标·熔断",
            "breakdown": {"天": tian, "地": di, "人": ren}
        }
        elapsed = time.time() - t0
        dna = _make_dna("sovereignty_index", f"tian={tian},veto=yes")
        _audit.record("sovereignty_index", f"tian={tian:.2f}", "veto_triggered", elapsed, dna)
        return result

    si = w_tian * tian + w_di * di + w_ren * ren
    thresholds = CHAIN_CONFIG["si_thresholds"]
    if si >= thresholds["green"]:
        color, status = "🟢", "优秀·放行"
    elif si >= thresholds["yellow"]:
        color, status = "🟡", "中等·复核"
    else:
        color, status = "🔴", "不足·拒绝"

    result = {
        "SI": round(si, 4), "color": color, "veto": False,
        "status": status,
        "breakdown": {"天": round(tian, 3), "地": round(di, 3), "人": round(ren, 3)}
    }
    if use_cache and CHAIN_CONFIG["cache_si"]:
        _si_cache[cache_key] = result
    elapsed = time.time() - t0
    dna = _make_dna("sovereignty_index", f"tian={tian:.2f}")
    _audit.record("sovereignty_index", f"tian={tian:.2f}", f"SI={si:.4f}→{color}", elapsed, dna)
    return result

# ═════════ 决策链（六环可审）═════════
def decision_chain(
    n: int,
    risk_factors: List[float],
    weights: List[float],
    tian: float = 0.85,
    di: float = 0.85,
    ren: float = 0.85,
    si_weights: Optional[Tuple[float, ...]] = None,
    score_thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """完整决策链 v2.0·六环全程可审

    环1：数字根 → 五行属性
    环2：三色闸（dr 检查）
    环3：三才主权指数（天轴熔断）
    环4：权重归一
    环5：加权风险 + 综合分
    环6：最终决策 + 行动
    """
    chain_start = time.time()

    t1 = time.time()
    dr = digital_root(n)
    element = five_element(n)
    trace = {"输入": n, "数字根": dr, "五行": element, "环节": [], "timings": {}}
    trace["timings"]["环1"] = (time.time() - t1) * 1000

    t2 = time.time()
    gate = dr_gate(n)
    trace["三色闸"] = gate
    trace["环节"].append(f"环2·三色闸 → {gate}")
    trace["timings"]["环2"] = (time.time() - t2) * 1000

    if gate == "🔴":
        trace.update({
            "决策": "REJECT", "color": "🔴", "行动": "拦截·不放行",
            "熔断原因": "数字根 dr∈{3,9}，红数字根拒绝",
            "总耗时_ms": round((time.time() - chain_start) * 1000, 3)
        })
        dna = _make_dna("decision_chain", f"n={n},fuse=dr-gate")
        _audit.record("decision_chain", f"n={n}", "REJECT@环2", time.time() - chain_start, dna)
        return trace

    t3 = time.time()
    si_result = sovereignty_index(tian, di, ren, si_weights)
    trace["三才SI"] = si_result
    trace["环节"].append(f"环3·三才SI → {si_result['color']} ({si_result['SI']})")
    trace["timings"]["环3"] = (time.time() - t3) * 1000

    if si_result["veto"]:
        trace.update({
            "决策": "REJECT", "color": "🔴", "行动": "拦截·熔断",
            "熔断原因": si_result["reason"],
            "总耗时_ms": round((time.time() - chain_start) * 1000, 3)
        })
        dna = _make_dna("decision_chain", f"n={n},fuse=si-veto")
        _audit.record("decision_chain", f"n={n}", "REJECT@环3", time.time() - chain_start, dna)
        return trace

    t4 = time.time()
    w = normalize(weights)
    trace["归一权重"] = {f"w{i}": round(wi, 4) for i, wi in enumerate(w)}
    trace["环节"].append(f"环4·权重归一 → Σw={sum(w):.4f}")
    trace["timings"]["环4"] = (time.time() - t4) * 1000

    t5 = time.time()
    assert len(w) == len(risk_factors), f"权重({len(w)}) 和风险因子({len(risk_factors)}) 数量不匹配"
    risk = sum(wi * ri for wi, ri in zip(w, risk_factors))
    score = 1 - risk
    trace["加权风险"] = round(risk, 4)
    trace["综合分"] = round(score, 4)
    trace["环节"].append(f"环5·综合分 → {round(score, 4)}")
    trace["timings"]["环5"] = (time.time() - t5) * 1000

    t6 = time.time()
    thresholds = score_thresholds or CHAIN_CONFIG["score_thresholds"]
    if score >= thresholds.get("green", 0.85):
        decision, color, action = "PASS", "🟢", "放行·执行"
    elif score >= thresholds.get("yellow", 0.60):
        decision, color, action = "REVIEW", "🟡", "复核·人工确认"
    else:
        decision, color, action = "REJECT", "🔴", "拦截·退回"

    trace.update({
        "决策": decision, "color": color, "行动": action,
        "总耗时_ms": round((time.time() - chain_start) * 1000, 3)
    })
    trace["环节"].append(f"环6·最终决策 → {decision} ({color})")
    trace["timings"]["环6"] = (time.time() - t6) * 1000

    dna = _make_dna("decision_chain", f"n={n},result={decision}")
    _audit.record("decision_chain", f"n={n}", f"{decision}·{decision}", time.time() - chain_start, dna)
    return trace

def full_audit_report(trace: Dict[str, Any]) -> str:
    """生成可审计的决策报告"""
    report = []
    report.append("=" * 80)
    report.append("🧮 根治理决策链 v2.0 · 完整审计报告")
    report.append("=" * 80)
    report.append(f"\n【输入】n={trace['输入']}")
    report.append(f"【第一步】数字根 dr={trace['数字根']} → 五行={trace['五行']}")
    report.append(f"【第二步】三色闸 → {trace['三色闸']}")
    if "三才SI" in trace:
        si = trace["三才SI"]
        report.append(f"【第三步】三才主权指数 → {si['color']} SI={si['SI']}")
        report.append(f"          天={si['breakdown']['天']} 地={si['breakdown']['地']} 人={si['breakdown']['人']}")
    if "归一权重" in trace:
        report.append(f"【第四步】权重归一 → {trace['归一权重']}")
    if "加权风险" in trace:
        report.append(f"【第五步】风险评估 → 风险={trace['加权风险']} 综合分={trace['综合分']}")
    report.append(f"【最终决策】{trace['决策']} {trace['color']}")
    report.append(f"【建议行动】{trace['行动']}")
    if "熔断原因" in trace:
        report.append(f"【熔断信息】{trace['熔断原因']}")
    report.append("=" * 80)
    return "\n".join(report)

def selftest() -> None:
    print("=" * 80)
    print("🧮 根治理决策链 v2.0 · 系统集成自检")
    print("=" * 80)
    five_element.cache_clear()
    _si_cache.clear()
    for i in range(100):
        five_element(1)
    assert five_element(1) == "木" and five_element(5) == "土" and five_element(9) == "水"
    print(f"[1] 五行映射 ✅")
    good = sovereignty_index(0.9, 0.9, 0.9)
    assert good["color"] == "🟢"
    print(f"[2] 三才 SI ✅")
    veto = sovereignty_index(0.2, 1.0, 1.0)
    assert veto["veto"] and veto["SI"] == 0.0
    print(f"[3] 天轴熔断 ✅")
    red = decision_chain(12, [0.1, 0.1], [1, 1])
    assert red["决策"] == "REJECT"
    print(f"[4] 决策链快速熔断 ✅")
    ok = decision_chain(20260603, [0.05, 0.05], [1, 1], tian=0.9, di=0.9, ren=0.9)
    assert ok["决策"] == "PASS"
    print(f"[5] 决策链完整流程 ✅")
    print("\n🟢 v2.0 系统集成自检通过")
    print("   DNA: #龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-FORMULA-CHAIN-v2.0-SYSTEM")

if __name__ == "__main__":
    selftest()
