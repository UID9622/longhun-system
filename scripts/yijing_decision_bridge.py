#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉☯️ 易经 → 根治理决策链 联动桥接 v1.0
═══════════════════════════════════════════════════════════════════════════

定位：把易经 64 卦推演的综合分/三才分，直接喂进 CNSH 根治理决策链，
      形成“卦象 → 三才主权 / 风险 → 决策行动”的完整链路。

链路：
  问题 → generate_hexagram → complete_divination
       → 提取 天道/地道/人道 三才分 + 综合风险
       → decision_chain / decision_chain_cnsh
       → 输出 {M::, CNSH::}

DNA：    #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-YIJING-DECISION-BRIDGE-v1.0-LINKAGE
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
from typing import Dict, List, Optional, Any

# 路径注入：公式目录 + 易经目录
_FORMULA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "cnsh-core", "downloads-imports",
                 "formula", "计算公式")
)
_YIJING_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "yijing_algorithm"))
for p in (_FORMULA_DIR, _YIJING_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import formula_core_v2 as fc
import formula_chain_v2 as fchain
import yijing_engine as ye


# ═════════ 桥接函数 ═════════

def yijing_to_decision(
    question: str,
    timestamp: Optional[float] = None,
    n: Optional[int] = None,
    risk_weights: Optional[List[float]] = None,
    si_weights: Optional[tuple[Any, ...]] = None,
    score_thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    易经推演 → 根治理决策链。

    输入：
      question       问题/意念
      timestamp      时间戳（默认当前时间）
      n              决策链输入整数（默认从问题+时间派生）
      risk_weights   风险因子权重（默认 [0.6, 0.4]）
      si_weights     三才权重（默认决策链配置）

    输出：
      {
        "question": 问题,
        "hexagram": {本卦, 综合分, 三才分, 建议},
        "decision": decision_chain 的完整 trace
      }
    """
    timestamp = timestamp or time.time()

    # 1. 易经完整推演
    reading = ye.complete_divination(question, timestamp)
    judgment = reading["judgment"]
    details = judgment["details"]

    # 2. 提取三才分
    tian = float(details["tian_dao"]["score"])
    di = float(details["di_dao"]["score"])
    ren = float(details["ren_dao"]["score"])

    # 3. 综合分 → 风险
    overall_score = float(judgment["score"])
    situation_risk = 1.0 - overall_score
    human_risk = 1.0 - ren

    risk_factors = [situation_risk, human_risk]
    weights = risk_weights or [0.6, 0.4]

    # 4. 生成决策链输入 n（如未提供）
    if n is None:
        seed = f"{question}{timestamp}"
        n = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    n = fc.digital_root(n)  # 压到 1-9，兼容 dr_gate

    # 5. 进入根治理决策链
    trace = fchain.decision_chain(
        n=n,
        risk_factors=risk_factors,
        weights=weights,
        tian=tian,
        di=di,
        ren=ren,
        si_weights=si_weights,
        score_thresholds=score_thresholds
    )

    return {
        "question": question,
        "timestamp": timestamp,
        "hexagram": {
            "本卦": reading["hexagrams"]["original"]["name"],
            "综合分": overall_score,
            "天道": tian,
            "地道": di,
            "人道": ren,
            "trend": details["di_dao"]["text"],
            "advice": judgment["advice"]
        },
        "decision": trace
    }


def yijing_to_decision_cnsh(
    question: str,
    timestamp: Optional[float] = None,
    n: Optional[int] = None,
    dna: str = ""
) -> Dict[str, Any]:
    """
    易经 → 决策链 的 CNSH 双视角封装。
    """
    result = yijing_to_decision(question, timestamp, n)
    trace = result["decision"]
    decision = trace.get("决策", "UNKNOWN")
    color = trace.get("color", "⚪")
    audit = color

    status_map = {"PASS": "pass", "REVIEW": "hold", "REJECT": "reject"}
    status = status_map.get(decision, "error")

    if not dna:
        h = hashlib.sha256(f"{question}{decision}{time.time()}".encode()).hexdigest()[:8].upper()
        dna = f"#龍芯⚡️yijing-decision-bridge-{h}"

    trace_hash = hashlib.sha256(
        json.dumps(result, ensure_ascii=False, default=str).encode()
    ).hexdigest()[:16]

    return {
        "M::": {
            "type": "yijing_decision_bridge",
            "status": status,
            "payload": {
                "question": result["question"],
                "hexagram": result["hexagram"],
                "decision": decision,
                "color": color,
                "action": trace.get("行动", "")
            }
        },
        "CNSH::": {
            "dna": dna,
            "gate": fchain.CONFIRM_CODE,
            "seal": fchain.SEAL_CODE,
            "audit": audit,
            "wuxing": trace.get("五行", ""),
            "policy": status,
            "trace_hash": trace_hash
        }
    }


# ═════════ 自检 ═════════

def selftest() -> None:
    """桥接模块自检"""
    print("=" * 80)
    print("🐉☯️ 易经 → 根治理决策链 联动桥接 v1.0 自检")
    print("=" * 80)

    # 1. 基础联动：输出包含决策链关键字段
    result = yijing_to_decision(
        "UID9622 龍魂系统下一步是否适合推进？",
        timestamp=1782710383.0,
        n=20260629
    )
    assert "decision" in result
    trace = result["decision"]
    assert "决策" in trace and "行动" in trace
    print(f"[1] 基础联动：本卦={result['hexagram']['本卦']} 决策={trace['决策']} ✅")

    # 2. 三才分来自易经
    assert 0.0 <= result["hexagram"]["天道"] <= 1.0
    assert 0.0 <= result["hexagram"]["地道"] <= 1.0
    assert 0.0 <= result["hexagram"]["人道"] <= 1.0
    print(f"[2] 三才分来源：天={result['hexagram']['天道']} 地={result['hexagram']['地道']} 人={result['hexagram']['人道']} ✅")

    # 3. CNSH 双视角封装
    pkg = yijing_to_decision_cnsh(
        "测试问题",
        timestamp=1782710383.0,
        dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-YIJING-DECISION-CNSH-TEST"
    )
    assert "M::" in pkg and "CNSH::" in pkg
    assert pkg["CNSH::"]["gate"] == fchain.CONFIRM_CODE
    assert pkg["CNSH::"]["seal"] == fchain.SEAL_CODE
    print(f"[3] CNSH 双视角封装：status={pkg['M::']['status']} audit={pkg['CNSH::']['audit']} ✅")

    # 4. 可复现：相同输入相同卦象，决策一致
    r1 = yijing_to_decision("复现测试", timestamp=1782710383.0, n=1)
    r2 = yijing_to_decision("复现测试", timestamp=1782710383.0, n=1)
    assert r1["hexagram"]["本卦"] == r2["hexagram"]["本卦"]
    assert r1["decision"]["决策"] == r2["decision"]["决策"]
    print(f"[4] 可复现：两次决策一致 ✅")

    print("=" * 80)
    print("🟢 易经 → 决策链联动桥接自检通过")
    print("   DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-YIJING-DECISION-BRIDGE-v1.0-LINKAGE")
    print("=" * 80)


if __name__ == "__main__":
    selftest()
