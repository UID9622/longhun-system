#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·责任塌缩概率模型引擎 v1.0
DNA: #龍芯⚡️2026-07-21-RESP-COLLAPSE-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

关联论文: responsibility_collapse_model_BILINGUAL (2026-07-01)
关联协议: LH-ETHICS-ANCHOR-v1.0

数学核心:
  P(善行|环境) = P₀ × [reward(kindness) / risk(kindness)]ˣ
  R = R2锐度 × R6长期权重 − R1缺席率 (责任系数)
  三色阈值: 绿(>0.7) 黄(0.3-0.7) 红(<0.3)

  95-5% 文明安全定律:
    5%恶意足毁灭体系 → 至少95%善行概率才能维持文明自愈

用法:
  python3 bin/lh_responsibility_collapse_engine.py       # 12条测试向量
  python3 bin/lh_responsibility_collapse_engine.py demo  # 演示
  python3 bin/lh_responsibility_collapse_engine.py eval <json_str> # 评估
"""

import sys, math, json, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

DNA = "#龍芯⚡️2026-07-21-RESP-COLLAPSE-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §1 概率行为体核心公式
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def kindness_probability(P0: float, reward_kindness: float,
                         risk_kindness: float, x: float) -> float:
    """核心公式: P(善行|环境) = P₀ × (reward/risk)^x

    参数:
      P0: 个人基率 [0, 1]
      reward_kindness: 善行回报 > 0
      risk_kindness: 善行风险 > 0
      x: 环境压力系数 [0.5, 3.0]

    返回: 条件概率 P ∈ [0, 1]
    """
    P0 = max(0.0, min(1.0, P0))
    x = max(0.5, min(3.0, x))

    if risk_kindness <= 0:
        return 1.0  # 零风险 → 必然善

    ratio = reward_kindness / risk_kindness
    raw = P0 * (ratio ** x)

    # clamp到[0, 1]
    return max(0.0, min(1.0, raw))


def responsibility_coefficient(r1_absence, r2_acuity, r3_emotional,
                                r4_structure, r5_lexical, r6_longterm,
                                r7_cultural, gamma_family=1.0):
    """七因子责任系数 R

    R = (R2 × R6 − R1) × min(R3, R4, R5) × R7 × γ_family

    七因子解释:
      R1 时间缺席率 [0,1] — 越低越好
      R2 语义锐度 [0,1] — 越高越好
      R3 情绪波形 [0,1] — 情绪稳定度
      R4 结构偏好 [0,1] — 思维结构化程度
      R5 词汇指纹 [0,1] — 责任相关词汇密度
      R6 长期权重 [0,1] — 延迟满足能力
      R7 文化地层 [0,1] — 集体责任意识
      γ_family 家人软肋系数 [0.5, 1.0] — 1.0为无胁迫

    返回: R ∈ [-1, 1] 然后映射到 [0, 1]
    """
    # 核心项（锐度×长期−缺席）
    core = (r2_acuity * r6_longterm) - r1_absence

    # 情绪/结构/词汇取最小（短板约束）
    floor_factor = min(r3_emotional, r4_structure, r5_lexical)

    # 文化地层为放大/缩小器
    R_raw = core * floor_factor * r7_cultural

    # 映射到 [0, 1]
    R_mapped = max(0.0, min(1.0, (R_raw + 1.0) / 2.0))

    # γ_family 家人软肋: 直接降低最终责任分（乘法效应）
    # γ=1.0 无胁迫; γ=0.5 责任腰斩
    R = R_mapped * gamma_family

    return max(0.0, min(1.0, R))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §2 三色阈值体系
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def classify_responsibility(R_val: float) -> dict[str, Any]:
    """三色阈值分类

    绿: R > 0.7 — 充分责任，文明正向贡献
    黄: 0.3 ≤ R ≤ 0.7 — 责任薄弱区，需体系保护
    红: R < 0.3 — 责任塌缩，系统性风险
    """
    if R_val > 0.7:
        return {
            "color": "🟢",
            "level": "充分责任",
            "action": "文明正向贡献·保持即可",
            "needs_intervention": False,
        }
    elif R_val >= 0.3:
        return {
            "color": "🟡",
            "level": "责任薄弱",
            "action": "需体系保护·建立正向激励·降低善行风险",
            "needs_intervention": True,
        }
    else:
        return {
            "color": "🔴",
            "level": "责任塌缩",
            "action": "紧急干预·重构激励结构·γ_family核查",
            "needs_intervention": True,
            "alert": "⚠️ 责任塌缩告警·需上游系统介入",
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §3 互联网放大效应
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def internet_amplification_factor(propagation: float, anonymity: float,
                                   algorithm: float) -> float:
    """互联网三重放大因子

    amp = propagation × anonymity × algorithm

    propagation:   传播系数 [1, 10]  (分享·转发·裂变)
    anonymity:     匿名系数   [1, 10]  (匿名度·去抑制)
    algorithm:     算法放大   [1, 10]  (推荐·排序·情绪优化)

    最大放大: 10×10×10 = 1000× (论文声称)
    """
    propagation = max(1.0, min(10.0, propagation))
    anonymity = max(1.0, min(10.0, anonymity))
    algorithm = max(1.0, min(10.0, algorithm))

    return propagation * anonymity * algorithm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §4 95-5%文明安全定律
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def civilization_safety_check(P_good: float, threshold: float = 0.95) -> dict[str, Any]:
    """95-5%文明安全定律检验

    前提: 5%恶意足以毁灭体系
    要求: P(善行) ≥ 95% 才能维持文明自愈

    返回: 安全性判定
    """
    safe = P_good >= threshold

    if safe:
        status = "🟢"
        verdict = f"文明自愈力充足·P(善行)={P_good:.4f}≥{threshold}"
    elif P_good >= 0.85:
        status = "🟡"
        verdict = f"文明自愈力不足·P(善行)={P_good:.4f}·需加强体系激励"
    elif P_good >= 0.70:
        status = "🔴"
        verdict = f"文明自愈力严重不足·P(善行)={P_good:.4f}·系统性风险"
    else:
        status = "🔴"
        verdict = f"文明自愈力崩溃·P(善行)={P_good:.4f}<0.7·注意！"

    # 计算安全边际
    margin = P_good - threshold

    return {
        "status": status,
        "P_good": round(P_good, 4),
        "threshold": threshold,
        "margin": round(margin, 4),
        "verdict": verdict,
        "safe": safe,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# §5 主引擎类
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ResponsibilityCollapseEngine:
    """责任塌缩概率模型引擎"""

    DNA = DNA
    CONFIRM = CONFIRM

    def evaluate_kindness(self, P0: float, reward: float, risk: float,
                          x: float = 1.0) -> dict[str, Any]:
        """评估善行概率"""
        P = kindness_probability(P0, reward, risk, x)

        # 判定塌缩/繁荣条件
        if risk > reward and x >= 2.0:
            condition = "责任塌缩条件满足 ⚠️"
        elif reward > risk:
            condition = "责任繁荣条件满足 ✅"
        else:
            condition = "临界平衡 ⚖️"

        return {
            "P_kindness": round(P, 6),
            "P0": P0,
            "reward/risk_ratio": round(reward / max(risk, 1e-10), 2),
            "x": x,
            "condition": condition,
            "is_collapse": risk > reward and x >= 2.0 and P < 0.3,
            "is_flourishing": reward > risk and P > 0.7,
        }

    def evaluate_responsibility(self, r1=0.3, r2=0.6, r3=0.7, r4=0.6,
                                 r5=0.5, r6=0.5, r7=0.6, gamma=1.0) -> dict[str, Any]:
        """评估责任系数"""
        R = responsibility_coefficient(r1, r2, r3, r4, r5, r6, r7, gamma)
        classification = classify_responsibility(R)

        return {
            "R": round(R, 4),
            "classification": classification,
            "factors": {
                "r1_absence": r1, "r2_acuity": r2, "r3_emotional": r3,
                "r4_structure": r4, "r5_lexical": r5, "r6_longterm": r6,
                "r7_cultural": r7, "gamma_family": gamma,
            },
        }

    def evaluate_internet_amplification(self, propagation=5.0,
                                         anonymity=7.0, algorithm=8.0) -> dict[str, Any]:
        """评估互联网放大效应"""
        amp = internet_amplification_factor(propagation, anonymity, algorithm)
        return {
            "amplification": amp,
            "factors": {
                "propagation": propagation,
                "anonymity": anonymity,
                "algorithm": algorithm,
            },
            "note": f"互联网使责任效应放大{amp:.0f}倍·论文理论最大值1000×",
        }

    def full_assessment(self, P0=0.6, reward=1.5, risk=1.0, x=1.0,
                        r1=0.3, r2=0.6, r3=0.7, r4=0.6, r5=0.5,
                        r6=0.5, r7=0.6, gamma=1.0,
                        propagation=5.0, anonymity=7.0, algorithm=8.0) -> dict[str, Any]:
        """完整评估：善行概率+责任系数+互联网放大+文明安全"""
        kindness = self.evaluate_kindness(P0, reward, risk, x)
        resp = self.evaluate_responsibility(r1, r2, r3, r4, r5, r6, r7, gamma)
        amp = self.evaluate_internet_amplification(propagation, anonymity, algorithm)

        # 综合概率（善意概率×责任系数×1/放大效应）
        adjusted_P = kindness["P_kindness"] * resp["R"] * (1.0 / max(amp["amplification"], 1.0))
        adjusted_P = max(0.0, min(1.0, adjusted_P))

        safety = civilization_safety_check(adjusted_P)

        return {
            "kindness": kindness,
            "responsibility": resp,
            "internet_amp": amp,
            "adjusted_P": round(adjusted_P, 6),
            "civilization_safety": safety,
            "overall_verdict": safety["verdict"],
            "overall_color": safety["status"],
        }

    def demo(self):
        """完整演示"""
        print("\n" + "=" * 60)
        print("龍魂·责任塌缩概率模型引擎 · 演示")
        print("DNA:", self.DNA)
        print("=" * 60)

        # 场景1: 繁荣环境
        print("\n§1 场景: 善有善报（繁荣条件）")
        print("-" * 40)
        r = self.evaluate_kindness(P0=0.6, reward=2.0, risk=0.5, x=1.5)
        print(f"  P(善行)={r['P_kindness']:.4f}  reward/risk={r['reward/risk_ratio']}")
        print(f"  {r['condition']}  {'🟢繁荣' if r['is_flourishing'] else ''}")

        # 场景2: 塌缩环境
        print("\n§2 场景: 善有恶报（塌缩条件）")
        print("-" * 40)
        r2 = self.evaluate_kindness(P0=0.6, reward=0.3, risk=2.0, x=2.5)
        print(f"  P(善行)={r2['P_kindness']:.4f}  reward/risk={r2['reward/risk_ratio']}")
        print(f"  {r2['condition']}  {'🔴塌缩' if r2['is_collapse'] else ''}")

        # 场景3: 七因子责任评估
        print("\n§3 场景: 七因子责任系数评估")
        print("-" * 40)
        # 正常人
        r_normal = self.evaluate_responsibility()
        print(f"  正常: R={r_normal['R']:.4f} {r_normal['classification']['color']} {r_normal['classification']['level']}")
        # 高风险人（高缺席+低长期+家人被胁迫）
        r_risk = self.evaluate_responsibility(r1=0.8, r2=0.3, r6=0.2, gamma=0.6)
        print(f"  高风险: R={r_risk['R']:.4f} {r_risk['classification']['color']} {r_risk['classification']['level']}")

        # 场景4: 互联网放大
        print("\n§4 场景: 互联网三重放大")
        print("-" * 40)
        amp = self.evaluate_internet_amplification()
        print(f"  传播×匿名×算法 = {amp['factors']['propagation']:.0f}×{amp['factors']['anonymity']:.0f}×{amp['factors']['algorithm']:.0f} = {amp['amplification']:.0f}×")
        amp_max = self.evaluate_internet_amplification(10.0, 10.0, 10.0)
        print(f"  最大放大: {amp_max['amplification']:.0f}× (论文理论值)")

        # 场景5: 完整评估
        print("\n§5 场景: 完整评估 → 文明安全")
        print("-" * 40)
        full = self.full_assessment()
        print(f"  调整后P(善行)={full['adjusted_P']:.4f}")
        print(f"  文明安全: {full['civilization_safety']['status']} {full['civilization_safety']['verdict'][:40]}")

        print("\n" + "=" * 60)
        print("结论: '让善良有生存空间'是可工程化的体系设计问题。")
        print("       reward(善) > risk(善) → P(善) → 1")
        print("=" * 60)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 测试向量（12条）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_tests():
    engine = ResponsibilityCollapseEngine()
    tests = []

    # T01: 核心公式计算
    P = kindness_probability(0.6, 1.5, 1.0, 1.0)
    tests.append(("T01 核心公式", 0.0 < P < 1.0, f"P={P:.4f}"))

    # T02: 繁荣条件
    P_f = kindness_probability(0.6, 2.0, 0.5, 1.5)
    tests.append(("T02 繁荣条件·P→1", P_f > 0.7, f"P={P_f:.4f}"))

    # T03: 塌缩条件
    P_c = kindness_probability(0.6, 0.3, 2.0, 2.5)
    tests.append(("T03 塌缩条件·P→0", P_c < 0.3, f"P={P_c:.4f}"))

    # T04: 责任系数通用计算
    R = responsibility_coefficient(0.3, 0.6, 0.7, 0.6, 0.5, 0.5, 0.6)
    tests.append(("T04 责任系数计算", 0.3 < R < 0.8, f"R={R:.4f}"))

    # T05: 高责任
    R_h = responsibility_coefficient(0.1, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
    tests.append(("T05 高责任R>0.7", R_h > 0.7, f"R={R_h:.4f}"))

    # T06: 家人胁迫→低责任 (gamma=0.5使R腰斩)
    R_normal = responsibility_coefficient(0.3, 0.5, 0.7, 0.6, 0.5, 0.5, 0.6, gamma_family=1.0)
    R_coerced = responsibility_coefficient(0.3, 0.5, 0.7, 0.6, 0.5, 0.5, 0.6, gamma_family=0.5)
    tests.append(("T06 家人胁迫·R骤降", R_coerced < R_normal and R_coerced < 0.4,
                  f"正常R={R_normal:.4f}→胁迫R={R_coerced:.4f}"))
    # T06b: 极端低责任场景（极度缺席+极低长期+极端胁迫）
    R_extreme = responsibility_coefficient(0.98, 0.02, 0.05, 0.05, 0.05, 0.01, 0.05, gamma_family=0.2)
    tests.append(("T06b 极端塌缩R<0.1", R_extreme < 0.1, f"R={R_extreme:.4f}"))

    # T07: 三色分类·绿
    c_g = classify_responsibility(0.85)
    tests.append(("T07 三色🟢", c_g["color"] == "🟢", c_g["level"]))

    # T08: 三色分类·红
    c_r = classify_responsibility(0.15)
    tests.append(("T08 三色🔴", c_r["color"] == "🔴", c_r["level"]))

    # T09: 互联网放大
    amp = internet_amplification_factor(5, 7, 8)
    tests.append(("T09 互联网放大", 200 < amp < 400, f"amp={amp:.0f}"))

    # T10: 最大放大=1000
    amp_max = internet_amplification_factor(10, 10, 10)
    tests.append(("T10 最大放大=1000", abs(amp_max - 1000) < 1, f"amp_max={amp_max:.0f}"))

    # T11: 文明安全检查
    safe = civilization_safety_check(0.96)
    tests.append(("T11 文明安全🟢", safe["safe"], f"P={safe['P_good']} margin={safe['margin']}"))

    # T12: 完整评估
    full = engine.full_assessment()
    tests.append(("T12 完整评估", "adjusted_P" in full and "civilization_safety" in full,
                  f"adjP={full['adjusted_P']:.4f} {full['overall_color']}"))

    print("\n" + "=" * 60)
    print("龍魂·责任塌缩概率模型引擎 · 12条测试向量")
    print("=" * 60)
    passed = 0
    for name, ok, detail in tests:
        mark = "✅" if ok else "❌"
        print(f"{mark} {name:42} {detail}")
        if ok:
            passed += 1
    print("=" * 60)
    print(f"结果: {passed}/{len(tests)} 通过")
    return passed == len(tests)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        ResponsibilityCollapseEngine().demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "eval":
        try:
            params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
            result = ResponsibilityCollapseEngine().full_assessment(**params)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"错误: {e}")
            print("示例: python3 bin/lh_responsibility_collapse_engine.py eval '{\"P0\":0.6,\"reward\":1.5,\"risk\":0.8}'")
    else:
        ok = run_tests()
        sys.exit(0 if ok else 1)
