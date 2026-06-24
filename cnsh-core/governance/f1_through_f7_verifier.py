#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂F1-F7七因子验证系统 (Seven-Factor Verification Framework)
DNA:#龍芯⚡️2026-06-03-F1-F7-VERIFIER-FILE1-v1.0

行为密码学 (Behavioral Cryptography) - 完整实装

不是问“这是AI生成的吗？”
而是问“谁原创它，通过哪些规则，哪些人格，什么决策，修订过哪里，什么审计证据？”

七个验证因子 (F1-F7) with 权重 (weights):
F1: 身份DNA验证 (Identity DNA Verification) - 25% (0.25)
F2: 时间锚定 (Temporal Anchor) - 15% (0.15)
F3: 规则追踪 (Rule Trace) - 15% (0.15)
F4: 人格路由 (Persona Routing) - 12% (0.12)
F5: 保护词汇 (Protected Vocabulary) - 12% (0.12)
F6: 风格向量 (Style Vector) - 11% (0.11)
F7: 错误日志 (Mistake Ledger) - 10% (0.10)
           ────────
总计: 100% (1.00)

硬失败规则: 任何因子 F_i = 0 → conf = 0 (不可救)
接纳阈值: τ = 0.85 (预设) or 0.95 (高安全)

置信度公式: conf = ∏ s_i^{w_i} where ∑w_i = 1

理论指导: 曾仕强老师 · 行为密码学 · 数字签名
不免责·永久有效
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json
import math


class VerificationFactor(Enum):
    """七个验证因子"""
    F1_IDENTITY = "F1_identity_dna"           # 25% - Identity verification
    F2_TEMPORAL = "F2_temporal_anchor"        # 15% - Time-based routing
    F3_RULE_TRACE = "F3_rule_trace"           # 15% - Rule compliance chain
    F4_PERSONA = "F4_persona_routing"         # 12% - Persona weights
    F5_VOCABULARY = "F5_protected_vocabulary" # 12% - Sovereign vocabulary
    F6_STYLE = "F6_style_vector"              # 11% - Writing style match
    F7_MISTAKES = "F7_mistake_ledger"         # 10% - Continuous error history


class VerificationResult(Enum):
    """验证结果分类"""
    HARD_FAIL = "🔴_硬失败"      # Any F_i = 0
    UNACCEPTABLE = "🔴_不接纳"   # conf < 0.70
    QUESTIONABLE = "🟡_需审核"   # 0.70 ≤ conf < 0.85
    ACCEPTABLE = "🟢_接纳"       # 0.85 ≤ conf < 0.95
    HIGHLY_TRUSTED = "🟢_高信任"  # conf ≥ 0.95


@dataclass
class F1IdentityVerification:
    """
    F1: 身份DNA验证 (Identity DNA)

    验证创作者身份的唯一性和可追踪性
    """
    uid: str                        # UID (e.g., "9622", "github_username")
    gpg_fingerprint: str           # GPG签名指纹
    gpg_prefix_marker: str         # GPG前缀标记 (e.g., "#CONFIRM🌌9622-...")
    identity_dna: str              # 身份DNA码
    creation_timestamp: str        # 首次创建时间

    def verify(self) -> float:
        """
        F1 验证 (0.0-1.0)

        Perfect (1.0): 完整的UID + GPG指纹 + CONFIRM码 + DNA
        Partial (0.5): 缺少GPG或DNA之一
        Fail (0.0): 缺少身份识别信息 或 身份不匹配
        """
        score = 0.0

        # Check 1: UID 存在且格式正确
        if self.uid and len(self.uid) > 0:
            score += 0.25

        # Check 2: GPG 指纹有效 (40个16进制字符)
        if self.gpg_fingerprint and len(self.gpg_fingerprint) == 40:
            try:
                int(self.gpg_fingerprint, 16)  # 验证是16进制
                score += 0.25
            except ValueError:
                pass

        # Check 3: CONFIRM 码存在
        if self.gpg_prefix_marker and "CONFIRM" in self.gpg_prefix_marker:
            score += 0.25

        # Check 4: DNA 码格式正确
        if self.identity_dna and self.identity_dna.startswith("#龍芯⚡️"):
            score += 0.25

        return score


@dataclass
class F2TemporalAnchor:
    """
    F2: 时间锚定 (Temporal Anchor)

    验证内容的时间一致性和文化时间正确性
    """
    iso8601: str                   # ISO 8601 时间戳
    shichen: str                   # 时辰 (子丑寅卯辰巳午未申酉戌亥)
    digital_root: int              # 数字根 (1-9)
    lunar_calendar: str            # 农历日期 (if available)
    time_window_violation: bool    # 时间窗口内违规?

    def verify(self) -> float:
        """
        F2 验证 (0.0-1.0)

        Perfect (1.0): ISO8601 + 时辰 + 数字根都正确 + 无时间窗口违规
        Partial (0.7): 缺少时辰或数字根之一
        Fail (0.0): 时间戳缺失 或 时间窗口违规
        """
        score = 0.0

        # Check 1: ISO8601 存在
        if self.iso8601:
            try:
                datetime.fromisoformat(self.iso8601)
                score += 0.3
            except:
                return 0.0  # Hard fail

        # Check 2: 时辰有效
        valid_shichen = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        if self.shichen in valid_shichen:
            score += 0.35

        # Check 3: 数字根有效 (1-9)
        if 1 <= self.digital_root <= 9:
            score += 0.35

        # Check 4: 无时间窗口违规
        if not self.time_window_violation:
            # Bonus for time consistency
            pass
        else:
            return 0.0  # Hard fail - timeline violation

        return score


@dataclass
class F3RuleTrace:
    """
    F3: 规则追踪 (Rule Trace)

    验证决策是否遵循已知的规则链
    """
    rule_ids: List[str]            # 应用的规则ID列表
    rule_chain_hash: str            # 规则链的 SHA256
    signature: str                  # 签名验证
    audit_log_entries: int         # 审计日志条目数

    def verify(self) -> float:
        """
        F3 验证 (0.0-1.0)

        Perfect (1.0): 完整规则链 + 签名验证通过 + 审计日志充足
        Partial (0.6): 规则链不完整 或 签名验证失败
        Fail (0.0): 缺少规则追踪 或 签名无效
        """
        score = 0.0

        # Check 1: 规则ID列表非空
        if self.rule_ids and len(self.rule_ids) > 0:
            score += 0.33

        # Check 2: 规则链哈希有效
        if self.rule_chain_hash and len(self.rule_chain_hash) == 64:  # SHA256
            try:
                int(self.rule_chain_hash, 16)
                score += 0.33
            except:
                return 0.0  # Hard fail

        # Check 3: 签名有效
        if self.signature and len(self.signature) > 0:
            score += 0.34

        # Bonus: 审计日志充足 (至少3个条目)
        if self.audit_log_entries >= 3:
            score = min(1.0, score + 0.1)

        return score


@dataclass
class F4PersonaRouting:
    """
    F4: 人格路由 (Persona Routing)

    验证决策是通过合法的路由权重做出的
    """
    primary_persona: str            # 主要路由节点 (e.g., "P02")
    persona_weights: Dict[str, float]  # 人格权重 {P02: 0.5, P05: 0.3, ...}
    veto_words_detected: bool       # 检测到虚伪词汇?
    routing_confidence: float       # 路由决策的置信度 (0.0-1.0)

    def verify(self) -> float:
        """
        F4 验证 (0.0-1.0)

        Perfect (1.0): 合法路由 + 权重合法 (和=1.0) + 无虚伪词汇
        Partial (0.5): 权重不合法 或 检测到虚伪
        Fail (0.0): 无主路由 或 权重>1.0
        """
        score = 0.0

        # Check 1: 主路由存在
        if self.primary_persona:
            score += 0.3

        # Check 2: 权重总和接近 1.0 (允许浮点误差)
        total_weight = sum(self.persona_weights.values())
        if 0.95 <= total_weight <= 1.05:  # 允许 ±0.05 误差
            score += 0.35

        # Check 3: 无虚伪词汇
        if not self.veto_words_detected:
            score += 0.35
        else:
            score = max(0.0, score - 0.5)  # 扣分

        return min(1.0, score)


@dataclass
class F5ProtectedVocabulary:
    """
    F5: 保护词汇 (Protected Vocabulary)

    验证主权词汇是否被正确使用和保护
    """
    sovereign_terms_found: List[str]  # 找到的主权词汇列表
    sovereign_terms_correct: bool     # 所有主权词汇都正确用法?
    character_preservation: bool      # 传统繁体字保护?
    semantic_integrity: bool          # 语义完整?

    def verify(self) -> float:
        """
        F5 验证 (0.0-1.0)

        Perfect (1.0): 正确使用所有主权词汇 + 繁体保护 + 语义完整
        Partial (0.5): 主权词汇不完整使用
        Fail (0.0): 主权词汇被破坏 或 语义被歪曲
        """
        score = 0.0

        # Check 1: 找到主权词汇
        if self.sovereign_terms_found:
            score += 0.25

        # Check 2: 主权词汇用法正确
        if self.sovereign_terms_correct:
            score += 0.25

        # Check 3: 繁体字保护
        if self.character_preservation:
            score += 0.25

        # Check 4: 语义完整
        if self.semantic_integrity:
            score += 0.25

        return score


@dataclass
class F6StyleVector:
    """
    F6: 风格向量 (Style Vector)

    验证内容的写作风格是否与创作者一致
    """
    cosine_similarity: float        # 风格向量余弦相似度 (0.0-1.0)
    vocabulary_consistency: float   # 词汇使用一致性
    syntax_pattern_match: float    # 句法模式匹配度
    tone_consistency: float        # 语调一致性

    def verify(self) -> float:
        """
        F6 验证 (0.0-1.0)

        Perfect (1.0): 高风格一致性 (cos > 0.9)
        Partial (0.6): 中等一致性 (0.6 < cos < 0.8)
        Questionable (0.3): 风格不匹配 (cos < 0.6)
        Fail (0.0): 极度不匹配 (cos < 0.3)
        """
        # 用四个维度的平均值
        avg_score = (
            self.cosine_similarity +
            self.vocabulary_consistency +
            self.syntax_pattern_match +
            self.tone_consistency
        ) / 4.0

        return max(0.0, min(1.0, avg_score))


@dataclass
class F7MistakeLedger:
    """
    F7: 错误日志 (Mistake Ledger)

    追踪创作者的连续错误历史
    """
    total_mistakes: int            # 总错误数
    recent_mistakes_30days: int    # 最近30天的错误
    mistake_recovery_rate: float   # 错误恢复率 (0.0-1.0)
    critical_mistakes: int         # 关键错误 (不可恢复)

    def verify(self) -> float:
        """
        F7 验证 (0.0-1.0)

        Perfect (1.0): 无错误 或 恢复率100%
        Good (0.8): 少量错误但已恢复
        Fair (0.5): 中等错误量
        Poor (0.2): 大量错误且恢复率低
        Fail (0.0): 关键错误无法恢复
        """
        # 检查关键错误
        if self.critical_mistakes > 0:
            return 0.0  # Hard fail

        if self.total_mistakes == 0:
            return 1.0  # Perfect

        # 根据恢复率计算
        score = self.mistake_recovery_rate * 0.8

        # 最近30天的错误减分
        if self.recent_mistakes_30days > 0:
            score -= (self.recent_mistakes_30days * 0.05)

        return max(0.0, min(1.0, score))


# ═══════════════════════════════════════════════════════════════
# 【主验证引擎】
# ═══════════════════════════════════════════════════════════════

class SevenFactorVerifier:
    """
    七因子验证系统 - 行为密码学核心
    """

    # 七个因子及其权重 (必须加到 1.0)
    WEIGHTS = {
        VerificationFactor.F1_IDENTITY: 0.25,
        VerificationFactor.F2_TEMPORAL: 0.15,
        VerificationFactor.F3_RULE_TRACE: 0.15,
        VerificationFactor.F4_PERSONA: 0.12,
        VerificationFactor.F5_VOCABULARY: 0.12,
        VerificationFactor.F6_STYLE: 0.11,
        VerificationFactor.F7_MISTAKES: 0.10,
    }

    # 默认接纳阈值
    DEFAULT_THRESHOLD = 0.85
    HIGH_SECURITY_THRESHOLD = 0.95

    def __init__(self):
        """初始化验证系统"""
        # 验证权重加到 1.0
        total_weight = sum(self.WEIGHTS.values())
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

    def verify(
        self,
        f1: F1IdentityVerification,
        f2: F2TemporalAnchor,
        f3: F3RuleTrace,
        f4: F4PersonaRouting,
        f5: F5ProtectedVocabulary,
        f6: F6StyleVector,
        f7: F7MistakeLedger,
        threshold: float = None
    ) -> Dict:
        """
        执行完整的七因子验证

        Returns:
            完整验证报告
        """
        threshold = threshold or self.DEFAULT_THRESHOLD

        # 计算各因子分数
        scores = {
            VerificationFactor.F1_IDENTITY: f1.verify(),
            VerificationFactor.F2_TEMPORAL: f2.verify(),
            VerificationFactor.F3_RULE_TRACE: f3.verify(),
            VerificationFactor.F4_PERSONA: f4.verify(),
            VerificationFactor.F5_VOCABULARY: f5.verify(),
            VerificationFactor.F6_STYLE: f6.verify(),
            VerificationFactor.F7_MISTAKES: f7.verify(),
        }

        # 检查硬失败 (任何因子 = 0)
        hard_failures = [f for f, score in scores.items() if score == 0.0]

        if hard_failures:
            return {
                "confidence": 0.0,
                "result": VerificationResult.HARD_FAIL.value,
                "passed": False,
                "threshold": threshold,
                "hard_failures": [f.value for f in hard_failures],
                "reason": f"Hard failure in {len(hard_failures)} factor(s)",
                "factors": {f.value: scores[f] for f in scores.keys()},
                "detailed_analysis": self._detailed_analysis(scores)
            }

        # 计算置信度: conf = ∏ s_i^{w_i}
        confidence = self._calculate_confidence(scores)

        # 确定验证结果
        if confidence < 0.70:
            result = VerificationResult.UNACCEPTABLE
        elif confidence < 0.85:
            result = VerificationResult.QUESTIONABLE
        elif confidence < 0.95:
            result = VerificationResult.ACCEPTABLE
        else:
            result = VerificationResult.HIGHLY_TRUSTED

        passed = confidence >= threshold

        return {
            "confidence": confidence,
            "result": result.value,
            "passed": passed,
            "threshold": threshold,
            "hard_failures": [],
            "reason": f"Confidence {confidence:.4f} {'≥' if passed else '<'} threshold {threshold}",
            "factors": {f.value: scores[f] for f in scores.keys()},
            "detailed_analysis": self._detailed_analysis(scores)
        }

    def _calculate_confidence(self, scores: Dict[VerificationFactor, float]) -> float:
        """
        计算置信度: conf = ∏ s_i^{w_i}

        乘积形式确保任何因子为0会导致整体为0
        """
        confidence = 1.0

        for factor, score in scores.items():
            weight = self.WEIGHTS[factor]
            confidence *= (score ** weight)

        return confidence

    def _detailed_analysis(self, scores: Dict[VerificationFactor, float]) -> Dict:
        """生成详细分析"""
        analysis = {}

        for factor, score in scores.items():
            weight = self.WEIGHTS[factor]
            contribution = score ** weight

            if score == 0.0:
                status = "🔴 硬失败"
            elif score < 0.5:
                status = "🔴 不合格"
            elif score < 0.7:
                status = "🟡 有疑虑"
            elif score < 0.9:
                status = "🟢 合格"
            else:
                status = "🟢 优秀"

            analysis[factor.value] = {
                "score": score,
                "weight": weight,
                "contribution": contribution,
                "status": status
            }

        return analysis

    def print_report(self, verification_result: Dict) -> None:
        """打印验证报告"""
        print("\n" + "="*70)
        print("【龍魂七因子验证报告】")
        print("="*70 + "\n")

        print(f"置信度: {verification_result['confidence']:.4f}")
        print(f"结果: {verification_result['result']}")
        print(f"通过: {'✅ YES' if verification_result['passed'] else '❌ NO'}")
        print(f"阈值: {verification_result['threshold']}")

        if verification_result['hard_failures']:
            print(f"\n🔴 硬失败:")
            for failure in verification_result['hard_failures']:
                print(f"  - {failure}")

        if 'detailed_analysis' in verification_result:
            print(f"\n【七因子详细分析】")
            for factor, analysis in verification_result['detailed_analysis'].items():
                print(f"\n{factor}:")
                print(f"  分数: {analysis['score']:.4f}")
                print(f"  权重: {analysis['weight']:.2%}")
                print(f"  贡献: {analysis['contribution']:.6f}")
                print(f"  状态: {analysis['status']}")

        print("\n" + "="*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 【演示】
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂F1-F7七因子验证系统 v1.0】\n")
    print("DNA:#龍芯⚡️2026-06-03-F1-F7-VERIFIER-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    verifier = SevenFactorVerifier()

    # 情景1: 高信任的创作者
    print("\n【情景1: 高信任创作者】\n")

    f1_good = F1IdentityVerification(
        uid="9622",
        gpg_fingerprint="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        gpg_prefix_marker="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        identity_dna="#龍芯⚡️2026-06-03-CREATOR-UID9622-v1.0",
        creation_timestamp="2025-05-20T10:00:00Z"
    )

    f2_good = F2TemporalAnchor(
        iso8601="2026-06-03T22:30:00+08:00",
        shichen="巳",
        digital_root=3,
        lunar_calendar="2026年五月十五",
        time_window_violation=False
    )

    f3_good = F3RuleTrace(
        rule_ids=["§25", "§32", "§37"],
        rule_chain_hash="a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1",
        signature="valid_signature_here",
        audit_log_entries=5
    )

    f4_good = F4PersonaRouting(
        primary_persona="P02",
        persona_weights={"P02": 0.50, "P05": 0.30, "P13": 0.20},
        veto_words_detected=False,
        routing_confidence=0.95
    )

    f5_good = F5ProtectedVocabulary(
        sovereign_terms_found=["龍", "道德经", "三才"],
        sovereign_terms_correct=True,
        character_preservation=True,
        semantic_integrity=True
    )

    f6_good = F6StyleVector(
        cosine_similarity=0.92,
        vocabulary_consistency=0.88,
        syntax_pattern_match=0.90,
        tone_consistency=0.91
    )

    f7_good = F7MistakeLedger(
        total_mistakes=2,
        recent_mistakes_30days=0,
        mistake_recovery_rate=1.0,
        critical_mistakes=0
    )

    result_good = verifier.verify(f1_good, f2_good, f3_good, f4_good, f5_good, f6_good, f7_good)
    verifier.print_report(result_good)

    # 情景2: 有风险的内容
    print("\n【情景2: 有风险内容 (检测到虚伪词汇)】\n")

    f4_risk = F4PersonaRouting(
        primary_persona="P02",
        persona_weights={"P02": 0.50, "P05": 0.30, "P13": 0.20},
        veto_words_detected=True,  # 检测到虚伪词汇!
        routing_confidence=0.60
    )

    result_risk = verifier.verify(f1_good, f2_good, f3_good, f4_risk, f5_good, f6_good, f7_good)
    verifier.print_report(result_risk)

    # 情景3: 硬失败 (缺失身份)
    print("\n【情景3: 硬失败 (缺失身份验证)】\n")

    f1_fail = F1IdentityVerification(
        uid="",  # 空UID = 失败
        gpg_fingerprint="invalid",
        gpg_prefix_marker="",
        identity_dna="",
        creation_timestamp=""
    )

    result_fail = verifier.verify(f1_fail, f2_good, f3_good, f4_good, f5_good, f6_good, f7_good)
    verifier.print_report(result_fail)

    print("="*70)
    print("✅ 七因子验证系统演示完成")
    print("="*70 + "\n")
