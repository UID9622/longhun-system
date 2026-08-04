#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行为密码学七因子 Σ(C) 引擎 v1.0
DNA: #龍芯⚡️2026-07-06-BEHAVIORAL-CRYPTO-7F-v1.0

根基算法：三才算法（天·地·人）— 属"人"才维度的行为建模

核心公式：
  Σ(C) = Σ(w_i × C_i), i=1..7
  conf = ∏ C_i^{w_i}  （行为置信度）

因子定义：
  C1 诚信-规则遵从  C2 攻击-竞争性  C3 算计-策略性
  C4 共情-利他性    C5 权力欲望     C6 情绪稳定性
  C7 风险偏好
"""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime


# ═══════════════════════════════════════
# 因子定义
# ═══════════════════════════════════════

FACTOR_DEFINITIONS = {
    "C1": {"name": "诚信-规则遵从", "weight": 0.18, "desc": "对规则和承诺的遵守程度"},
    "C2": {"name": "攻击-竞争性", "weight": 0.14, "desc": "维护自身利益的主动程度"},
    "C3": {"name": "算计-策略性", "weight": 0.16, "desc": "对规则和局势的利用能力"},
    "C4": {"name": "共情-利他性", "weight": 0.14, "desc": "对他人的体谅和照顾倾向"},
    "C5": {"name": "权力欲望",   "weight": 0.12, "desc": "对控制权和地位的追求"},
    "C6": {"name": "情绪稳定性", "weight": 0.13, "desc": "面对压力时的反应模式"},
    "C7": {"name": "风险偏好",   "weight": 0.13, "desc": "对不确定性的容忍度"},
}

# 老实人 vs 算计者典型画像
HONEST_PROFILE = {
    "C1": 0.85, "C2": 0.20, "C3": 0.25, "C4": 0.80,
    "C5": 0.20, "C6": 0.50, "C7": 0.25,
}
CALCULATOR_PROFILE = {
    "C1": 0.35, "C2": 0.85, "C3": 0.90, "C4": 0.15,
    "C5": 0.80, "C6": 0.85, "C7": 0.80,
}
BALANCED_PROFILE = {
    "C1": 0.75, "C2": 0.45, "C3": 0.50, "C4": 0.60,
    "C5": 0.40, "C6": 0.65, "C7": 0.45,
}


@dataclass
class BehaviorProfile:
    """行为密码画像"""
    factors: dict[str, float]  # C1-C7, 0-1
    confidence: float = 0.0
    profile_type: str = ""     # 老实人/算计者/均衡型/自定义
    deviation_from_honest: float = 0.0
    deviation_from_calculator: float = 0.0
    risk_flags: list[str] = field(default_factory=list)

    def __post_init__(self):
        self._calculate()

    def _calculate(self):
        """计算置信度与画像分类"""
        # conf = ∏ C_i^{w_i}
        self.confidence = 1.0
        for key, info in FACTOR_DEFINITIONS.items():
            val = self.factors.get(key, 0.5)
            self.confidence *= val ** info["weight"]  # pyright: ignore[reportOperatorIssue]

        # 任一因子为0 → 硬失败
        if any(self.factors.get(k, 0.5) == 0 for k in FACTOR_DEFINITIONS):
            self.confidence = 0.0

        self.confidence = round(self.confidence, 4)

        # 与典型画像的偏离度
        self.deviation_from_honest = round(
            sum(abs(self.factors.get(k, 0.5) - HONEST_PROFILE[k])
                for k in FACTOR_DEFINITIONS) / 7, 4
        )
        self.deviation_from_calculator = round(
            sum(abs(self.factors.get(k, 0.5) - CALCULATOR_PROFILE[k])
                for k in FACTOR_DEFINITIONS) / 7, 4
        )

        # 分类
        if self.deviation_from_honest < 0.15:
            self.profile_type = "老实人型"
        elif self.deviation_from_calculator < 0.15:
            self.profile_type = "算计者型"
        elif self.confidence > 0.6:
            self.profile_type = "均衡型"
        else:
            self.profile_type = "不稳定型"

        # 风险标记
        self._check_risk_flags()

    def _check_risk_flags(self):
        """行为风险标记"""
        f = self.factors
        if f.get("C1", 0.5) < 0.3 and f.get("C3", 0.5) > 0.7:
            self.risk_flags.append("🟠 选择性规则遵从·高策略 — 可能利用规则")
        if f.get("C2", 0.5) > 0.7 and f.get("C4", 0.5) < 0.2:
            self.risk_flags.append("🟠 高攻击·低共情 — 可能压制他人")
        if f.get("C6", 0.5) > 0.8 and f.get("C3", 0.5) > 0.7:
            self.risk_flags.append("🟡 高情绪稳定+高策略 — 难以被察觉的博弈者")
        if f.get("C1", 0.5) > 0.8 and f.get("C2", 0.5) < 0.2:
            self.risk_flags.append("🟡 高遵从·低攻击 — 可能成为被欺负对象")
        if self.confidence < 0.2:
            self.risk_flags.append("🔴 行为置信度极低 — 需要关注")


class BehavioralCrypto7F:
    """
    行为密码学七因子引擎

    用法:
        bc = BehavioralCrypto7F()
        profile = bc.analyze({"C1": 0.85, "C2": 0.2, ...})
        report = bc.generate_report(profile)
        advice = bc.anti_bully_protocol(profile)
    """

    def analyze(self, factors: dict[str, float]) -> BehaviorProfile:
        """分析行为因子，返回画像"""
        # 填充缺失因子为默认值
        full_factors = {f"C{i}": 0.5 for i in range(1, 8)}
        full_factors.update(factors)
        # 限制范围
        for k in full_factors:
            full_factors[k] = max(0.0, min(1.0, full_factors[k]))
        return BehaviorProfile(factors=full_factors)

    def generate_report(self, profile: BehaviorProfile) -> dict[str, object]:
        """生成行为分析报告"""
        return {
            "profile_type": profile.profile_type,
            "confidence": profile.confidence,
            "deviation_honest": profile.deviation_from_honest,
            "deviation_calculator": profile.deviation_from_calculator,
            "risk_flags": profile.risk_flags,
            "factors": {
                f"C{i}": {
                    "name": FACTOR_DEFINITIONS[f"C{i}"]["name"],
                    "value": profile.factors.get(f"C{i}", 0.5),
                    "level": "高" if profile.factors.get(f"C{i}", 0.5) > 0.65
                             else "低" if profile.factors.get(f"C{i}", 0.5) < 0.35
                             else "中",
                }
                for i in range(1, 8)
            },
        }

    def anti_bully_protocol(self, profile: BehaviorProfile) -> dict[str, object]:
        """
        反欺负协议 — 根据个人画像给出防护建议

        参考原文第九章：老实人该怎么办
        """
        advice = []
        f = profile.factors

        if f.get("C3", 0.5) < 0.4:
            advice.append({
                "action": "提高C3算计-策略性",
                "detail": "学习理解规则、利用规则，至少不被规则玩弄。了解基本法律常识、平台协议。"
            })
        if f.get("C2", 0.5) < 0.35:
            advice.append({
                "action": "适度提高C2攻击-竞争性",
                "detail": "在必要的时候发声、争取，而不是一味退让。学会说'不'。"
            })
        if f.get("C4", 0.5) > 0.7:
            advice.append({
                "action": "降低过度C4共情-利他性",
                "detail": "该强硬的时候不心软，该拒绝的时候不犹豫。善良要有牙齿。"
            })

        # 通用工具建议
        advice.append({
            "action": "固化证据三件套",
            "detail": "截图、录音、时间线。口头承诺不值钱，可追溯的数据才值钱。"
        })
        advice.append({
            "action": "用算法对抗算法",
            "detail": "多账号比价、多设备验证、多平台留痕。"
        })

        return {
            "profile_type": profile.profile_type,
            "advice_count": len(advice),
            "advice": advice,
            "anthem": "善良没有牙齿就只是软弱，风骨没有铠甲就只是摆设。",
        }

    def compare(self, profile_a: BehaviorProfile, profile_b: BehaviorProfile) -> dict[str, object]:
        """两个画像对比"""
        diffs = {}
        for i in range(1, 8):
            key = f"C{i}"
            a_val = profile_a.factors.get(key, 0.5)
            b_val = profile_b.factors.get(key, 0.5)
            diffs[key] = {
                "name": FACTOR_DEFINITIONS[key]["name"],
                "a_value": a_val,
                "b_value": b_val,
                "diff": round(b_val - a_val, 2),
            }

        return {
            "a_type": profile_a.profile_type,
            "b_type": profile_b.profile_type,
            "factor_diffs": diffs,
            "dominant_advantage": "A" if profile_a.confidence > profile_b.confidence else "B",
        }


def generate_dna(module: str, action: str) -> str:
    ts = datetime.now().strftime("%Y%m%d")
    h = hashlib.sha256(f"{ts}-{module}-{action}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{module}-{action}-{h}"


# ═══════════════════════════════════════
# 自测
# ═══════════════════════════════════════

if __name__ == "__main__":
    bc = BehavioralCrypto7F()
    print("🐉 行为密码学七因子 Σ(C) v1.0\n")

    for name, factors in [("老实人", HONEST_PROFILE), ("算计者", CALCULATOR_PROFILE), ("均衡型", BALANCED_PROFILE)]:
        p = bc.analyze(factors)
        r = bc.generate_report(p)
        print(f"  [{name}] 类型={r['profile_type']} 置信度={r['confidence']} 风险={len(r['risk_flags'])}个")  # pyright: ignore[reportArgumentType]
        print(f"  偏离老实人={p.deviation_from_honest:.4f} 偏离算计者={p.deviation_from_calculator:.4f}")
        print()

    # 反欺负建议
    honest = bc.analyze(HONEST_PROFILE)
    advice = bc.anti_bully_protocol(honest)
    print("  [反欺负协议]")
    for a in advice["advice"]:  # pyright: ignore[reportGeneralTypeIssues]
        print(f"    → {a['action']}: {a['detail'][:40]}...")  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]

    # 对比
    print("\n  [老实人 vs 算计者对比]")
    cmp = bc.compare(honest, bc.analyze(CALCULATOR_PROFILE))
    for k, v in cmp["factor_diffs"].items():  # pyright: ignore[reportAttributeAccessIssue,reportUnknownVariableType,reportUnknownMemberType]
        bar = "█" * max(0, min(20, int(abs(v["diff"]) * 20)))  # pyright: ignore[reportUnknownArgumentType]
        direction = "←" if v["diff"] < 0 else "→"
        print(f"    {k} {v['name']}: {v['a_value']:.2f} {direction} {v['b_value']:.2f} {bar}")

    print(f"\n  DNA: {generate_dna('BEHAVIORAL', 'TEST')}")
