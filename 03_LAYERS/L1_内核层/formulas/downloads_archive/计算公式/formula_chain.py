#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🧮 根治理决策链 · formula_chain.py

把单条公式串成一条可审的治理流水线：
输入 → 数字根/五行 → 三色闸 → 归一权重 → 加权风险 → 综合分 → 决策 → 行动

依赖 formula_core.py（同目录）。纯标准库。

DNA: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-MATH-FORMULA-CORE-DUAL-TRACK-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
主权人: UID9622 · 龍芯北辰

“单条公式是零件·根本治理是把它们串成一条链”
"""

from __future__ import annotations
from typing import List, Dict, Any
import sys
import os

# 导入 formula_core（同目录）
sys.path.insert(0, os.path.dirname(__file__))
from formula_core import digital_root, dr_gate, normalize, truth_score, soul_score, SOUL_W

# ═════════ 数字根 → 五行（在数论之上焊属性底色）═════════
FIVE_ELEMENT = {
    1: "木", 2: "木", 3: "火", 4: "火", 5: "土",
    6: "金", 7: "金", 8: "水", 9: "水"
}

def five_element(n: int) -> str:
    """龍魂：数字根映五行，给输入定属性底色（数论之上的语义层）。"""
    dr = digital_root(n)
    return FIVE_ELEMENT[dr]

# ═════════ 三才主权指数 SI（天<0.34 一票熔断）═════════
def sovereignty_index(tian: float, di: float, ren: float) -> Dict[str, Any]:
    """
    世界标准是 MCDA 加权和；龍魂焊主权轴熔断：天<0.34 直接全盘否。
    
    天：主权轴（UID9622 不可让渡）
    地：执行能力轴（运营）
    人：人心向背轴（用户满意）
    """
    if tian < 0.34:  # 主权轴不达标 → 一票熔断
        return {
            "SI": 0.0,
            "color": "🔴",
            "veto": True,
            "reason": "主权轴不达标·熔断"
        }
    
    si = 0.34 * tian + 0.33 * di + 0.33 * ren
    
    if si >= 0.85:
        color = "🟢"
        status = "优秀·放行"
    elif si >= 0.60:
        color = "🟡"
        status = "中等·复核"
    else:
        color = "🔴"
        status = "不足·拒绝"
    
    return {
        "SI": round(si, 4),
        "color": color,
        "veto": False,
        "status": status,
        "breakdown": {"天": round(tian, 3), "地": round(di, 3), "人": round(ren, 3)}
    }

# ═════════ 决策链 dr→W→Risk→S→D→Action（六环全程可审）═════════
def decision_chain(
    n: int,
    risk_factors: List[float],
    weights: List[float],
    tian: float = 0.85,
    di: float = 0.85,
    ren: float = 0.85
) -> Dict[str, Any]:
    """
    完整决策链，六环全程可审和熔断：
    
    环1：数字根 → 五行属性
    环2：三色闸（dr 检查）
    环3：三才主权指数（天轴熔断）
    环4：权重归一
    环5：加权风险 + 综合分
    环6：最终决策 + 行动
    """
    
    # 环1：数字根 → 五行
    dr = digital_root(n)
    element = five_element(n)
    trace = {
        "输入": n,
        "数字根": dr,
        "五行": element,
        "环节": []
    }
    
    # 环2：三色闸
    gate = dr_gate(n)
    trace["三色闸"] = gate
    trace["环节"].append(f"环2·三色闸 → {gate}")
    
    if gate == "🔴":  # 第一环就拦红，链路熔断
        trace.update({
            "决策": "REJECT",
            "color": "🔴",
            "行动": "拦截·不放行",
            "熔断原因": "数字根 dr∈{3,9}，红数字根拒绝"
        })
        return trace
    
    # 环3：三才主权指数
    si_result = sovereignty_index(tian, di, ren)
    trace["三才SI"] = si_result
    trace["环节"].append(f"环3·三才SI → {si_result['color']} ({si_result['SI']})")
    
    if si_result["veto"]:  # 主权轴不达标
        trace.update({
            "决策": "REJECT",
            "color": "🔴",
            "行动": "拦截·熔断",
            "熔断原因": si_result["reason"]
        })
        return trace
    
    # 环4：权重归一
    w = normalize(weights)
    trace["归一权重"] = {f"w{i}": round(wi, 4) for i, wi in enumerate(w)}
    trace["环节"].append(f"环4·权重归一 → Σw={sum(w):.4f}")
    
    # 环5：加权风险 + 综合分
    assert len(w) == len(risk_factors), f"权重({len(w)}) 和风险因子({len(risk_factors)}) 数量不匹配"
    risk = sum(wi * ri for wi, ri in zip(w, risk_factors))
    score = 1 - risk  # 综合得分 = 1 - 风险
    
    trace["加权风险"] = round(risk, 4)
    trace["综合分"] = round(score, 4)
    trace["环节"].append(f"环5·综合分 → {round(score, 4)} (风险={round(risk, 4)})")
    
    # 环6：最终决策
    if score >= 0.85:
        decision, color, action = "PASS", "🟢", "放行·执行"
    elif score >= 0.60:
        decision, color, action = "REVIEW", "🟡", "复核·人工确认"
    else:
        decision, color, action = "REJECT", "🔴", "拦截·退回"
    
    trace.update({
        "决策": decision,
        "color": color,
        "行动": action
    })
    trace["环节"].append(f"环6·最终决策 → {decision} ({color})")
    
    return trace


# ═════════ 完整决策报告（可审计）═════════
def full_audit_report(trace: Dict[str, Any]) -> str:
    """生成可审计的决策报告"""
    report = []
    report.append("=" * 64)
    report.append("🧮 根治理决策链 · 完整审计报告")
    report.append("=" * 64)
    report.append("")
    
    report.append(f"【输入】n={trace['输入']}")
    report.append(f"【第一步】数字根 dr={trace['数字根']} → 五行={trace['五行']}")
    report.append(f"【第二步】三色闸 → {trace['三色闸']}")
    
    if "三才SI" in trace:
        si = trace["三才SI"]
        report.append(f"【第三步】三才主权指数 → {si['color']} SI={si['SI']}")
        if "breakdown" in si:
            report.append(f"          天={si['breakdown']['天']} 地={si['breakdown']['地']} 人={si['breakdown']['人']}")
    
    if "归一权重" in trace:
        report.append(f"【第四步】权重归一 → {trace['归一权重']}")
    
    if "加权风险" in trace:
        report.append(f"【第五步】风险评估 → 风险={trace['加权风险']} 综合分={trace['综合分']}")
    
    report.append(f"【最终决策】{trace['决策']} {trace['color']}")
    report.append(f"【建议行动】{trace['行动']}")
    
    if "熔断原因" in trace:
        report.append(f"【熔断信息】{trace['熔断原因']}")
    
    report.append("")
    report.append("【完整环节跟踪】")
    for step in trace.get("环节", []):
        report.append(f"  {step}")
    
    report.append("=" * 64)
    return "\n".join(report)


# ═════════ 自检：跑一次，错一条就报错 ═════════
def selftest() -> None:
    """完整决策链自检"""
    print("=" * 64)
    print("🧮 根治理决策链 · 自检")
    print("=" * 64)

    # 1. 五行映射
    assert five_element(1) == "木" and five_element(5) == "土" and five_element(9) == "水"
    print(f"[链1] dr→五行  1={five_element(1)} 5={five_element(5)} 9={five_element(9)}  ✅")

    # 2. 三才主权指数 + 天熔断
    good = sovereignty_index(0.9, 0.9, 0.9)
    assert good["color"] == "🟢" and not good["veto"]
    veto = sovereignty_index(0.2, 1.0, 1.0)  # 天<0.34
    assert veto["veto"] and veto["SI"] == 0.0 and veto["color"] == "🔴"
    print(f"[链2] 三才SI(高)=🟢  天<0.34→一票熔断={veto['color']}  ✅")

    # 3. 决策链：红数字根直接拦 / 低风险放行
    red = decision_chain(12, [0.1, 0.1], [1, 1])  # dr(12)=3 → 🔴
    assert red["决策"] == "REJECT" and red["三色闸"] == "🔴"
    print(f"[链3] dr红→{red['决策']}  ✅")
    
    ok = decision_chain(
        20260603, [0.05, 0.05], [1, 1],
        tian=0.9, di=0.9, ren=0.9  # 三才都好
    )
    assert ok["决策"] == "PASS" and ok["综合分"] >= 0.85
    print(f"[链4] 低风险+主权达标→{ok['决策']}(综合分={ok['综合分']})  ✅")
    
    # 4. 天轴熔断案例
    veto_chain = decision_chain(
        20260603, [0.05, 0.05], [1, 1],
        tian=0.2, di=0.9, ren=0.9  # 天轴不达标
    )
    assert veto_chain["决策"] == "REJECT" and veto_chain["color"] == "🔴"
    print(f"[链5] 天轴不达标→{veto_chain['决策']}(熔断)  ✅")

    print("=" * 64)
    print("🟢 决策链自检通过——零件串成链，每一环可审·可熔断。这才是根治理。🐉")
    print("=" * 64)
    
    # 生成完整审计报告示例
    print("\n【审计报告示例】\n")
    example = decision_chain(20260603, [0.1, 0.15], [2, 3], 0.9, 0.85, 0.8)
    print(full_audit_report(example))


if __name__ == "__main__":
    selftest()
