# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 根治理决策链 · formula_chain.py
把单条公式串成一条可审的治理流水线：
输入 → 数字根/五行 → 三色闸 → 归一权重 → 加权风险 → 综合分 → 决策 → 行动
依赖 formula_core.py（同目录）。纯标准库。
DNA:#龍芯⚡️2026-06-03-MATH-FORMULA-CORE-DUAL-TRACK-FILE1-v1.0-1
主权人: UID9622 · 龍芯北辰
"""
from __future__ import annotations
from typing import List, Dict, Any
from formula_core import digital_root, dr_gate, normalize

# ── 数字根 → 五行（在数论之上焊属性底色）──
FIVE_ELEMENT = {1: "木", 2: "木", 3: "火", 4: "火", 5: "土",
                6: "金", 7: "金", 8: "水", 9: "水"}

def five_element(n: int) -> str:
    """龍魂：数字根映五行，给输入定属性底色（数论之上的语义层）。"""
    return FIVE_ELEMENT[digital_root(n)]

# ── 三才主权指数 SI（天<0.34 一票熔断）──
def sovereignty_index(tian: float, di: float, ren: float) -> Dict[str, Any]:
    """世界标准是 MCDA 加权和；龍魂焊主权轴熔断：天<0.34 直接全盘否。"""
    if tian < 0.34:                       # 主权轴不达标 → 一票熔断
        return {"SI": 0.0, "color": "🔴", "veto": True}
    si = 0.34 * tian + 0.33 * di + 0.33 * ren
    color = "🟢" if si >= 0.85 else "🟡" if si >= 0.60 else "🔴"
    return {"SI": round(si, 4), "color": color, "veto": False}

# ── 决策链 dr→W→Risk→S→D→Action（六环全程可审）──
def decision_chain(n: int, risk_factors: List[float], weights: List[float]) -> Dict[str, Any]:
    dr = digital_root(n)
    gate = dr_gate(n)
    trace = {"输入": n, "数字根": dr, "五行": five_element(n), "三色闸": gate}
    if gate == "🔴":                       # 第一环就拦红，链路熔断
        trace.update({"决策": "REJECT", "color": "🔴", "行动": "拦截·不放行"})
        return trace
    w = normalize(weights)                # W(x)：权重归一
    risk = sum(wi * ri for wi, ri in zip(w, risk_factors))  # Risk：加权风险
    score = 1 - risk                      # S：综合得分
    if score >= 0.85:
        decision, color, action = "PASS", "🟢", "放行·执行"
    elif score >= 0.60:
        decision, color, action = "REVIEW", "🟡", "复核·人工确认"
    else:
        decision, color, action = "REJECT", "🔴", "拦截·退回"
    trace.update({"风险": round(risk, 4), "综合分": round(score, 4),
                  "决策": decision, "color": color, "行动": action})
    return trace

# ── 自检：跑一次，错一条就报错 ──
def selftest() -> None:
    print("=" * 64)
    print("🧮 根治理决策链 · 自检")
    print("=" * 64)

    # 链1 五行映射
    assert five_element(1) == "木" and five_element(5) == "土" and five_element(9) == "水"
    print(f"[链1] dr→五行  1={five_element(1)} 5={five_element(5)} 9={five_element(9)}  ✅")

    # 链2 三才主权指数 + 天熔断
    assert sovereignty_index(0.9, 0.9, 0.9)["color"] == "🟢"
    veto = sovereignty_index(0.2, 1.0, 1.0)        # 天<0.34
    assert veto["veto"] and veto["SI"] == 0.0
    print(f"[链2] 三才SI(高)=🟢  天<0.34→一票熔断={veto['color']}  ✅")

    # 链3 决策链：红数字根直接拦 / 低风险放行
    red = decision_chain(12, [0.1, 0.1], [1, 1])   # dr(12)=3 → 🔴
    assert red["决策"] == "REJECT" and red["三色闸"] == "🔴"
    ok = decision_chain(20260603, [0.05, 0.05], [1, 1])  # dr=1→🟢, 风险低
    assert ok["决策"] == "PASS" and ok["综合分"] >= 0.85
    print(f"[链3] dr红→{red['决策']}  低风险→{ok['决策']}(综合分={ok['综合分']})  ✅")

    print("=" * 64)
    print("🟢 决策链自检通过——零件串成链，每一环可审、可熔断。这才是根治理。🐉")
    print("=" * 64)

if __name__ == "__main__":
    selftest()
