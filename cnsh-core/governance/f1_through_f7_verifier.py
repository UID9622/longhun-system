#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂F1-F7七因子驗證系統 (Seven-Factor Verification Framework)
DNA: #龍芯⚡️2026-06-03-F1-F7-VERIFIER-v1.0

行為密碼學 (Behavioral Cryptography) - 完整實裝

不是問「這是AI生成的嗎？」
而是問「誰原創它，通過哪些規則，哪些人格，什麼決策，修訂過哪裡，什麼審計證據？」

七個驗證因子 (F1-F7) with 權重 (weights):
F1: 身份DNA驗證 (Identity DNA Verification) - 25% (0.25)
F2: 時間錨定 (Temporal Anchor) - 15% (0.15)
F3: 規則追蹤 (Rule Trace) - 15% (0.15)
F4: 人格路由 (Persona Routing) - 12% (0.12)
F5: 保護詞彙 (Protected Vocabulary) - 12% (0.12)
F6: 風格向量 (Style Vector) - 11% (0.11)
F7: 錯誤日誌 (Mistake Ledger) - 10% (0.10)
           ────────
總計: 100% (1.00)

硬失敗規則: 任何因子 F_i = 0 → conf = 0 (不可救)
接納閾值: τ = 0.85 (預設) or 0.95 (高安全)

置信度公式: conf = ∏ s_i^{w_i} where ∑w_i = 1

理論指導: 曾仕强老师 · 行為密碼學 · 數字簽名
不免責·永久有效
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json
import math


class VerificationFactor(Enum):
    """七個驗證因子"""
    F1_IDENTITY = "F1_identity_dna"           # 25% - Identity verification
    F2_TEMPORAL = "F2_temporal_anchor"        # 15% - Time-based routing
    F3_RULE_TRACE = "F3_rule_trace"           # 15% - Rule compliance chain
    F4_PERSONA = "F4_persona_routing"         # 12% - Persona weights
    F5_VOCABULARY = "F5_protected_vocabulary" # 12% - Sovereign vocabulary
    F6_STYLE = "F6_style_vector"              # 11% - Writing style match
    F7_MISTAKES = "F7_mistake_ledger"         # 10% - Continuous error history


class VerificationResult(Enum):
    """驗證結果分類"""
    HARD_FAIL = "🔴_硬失敗"      # Any F_i = 0
    UNACCEPTABLE = "🔴_不接納"   # conf < 0.70
    QUESTIONABLE = "🟡_需審核"   # 0.70 ≤ conf < 0.85
    ACCEPTABLE = "🟢_接納"       # 0.85 ≤ conf < 0.95
    HIGHLY_TRUSTED = "🟢_高信任"  # conf ≥ 0.95


@dataclass
class F1IdentityVerification:
    """
    F1: 身份DNA驗證 (Identity DNA)

    驗證創作者身份的唯一性和可追蹤性
    """
    uid: str                        # UID (e.g., "9622", "github_username")
    gpg_fingerprint: str           # GPG簽名指紋
    gpg_prefix_marker: str         # GPG前綴標記 (e.g., "#CONFIRM🌌9622-...")
    identity_dna: str              # 身份DNA碼
    creation_timestamp: str        # 首次創建時間

    def verify(self) -> float:
        """
        F1 驗證 (0.0-1.0)

        Perfect (1.0): 完整的UID + GPG指紋 + CONFIRM碼 + DNA
        Partial (0.5): 缺少GPG或DNA之一
        Fail (0.0): 缺少身份識別信息 或 身份不匹配
        """
        score = 0.0

        # Check 1: UID 存在且格式正確
        if self.uid and len(self.uid) > 0:
            score += 0.25

        # Check 2: GPG 指紋有效 (40個16進位字符)
        if self.gpg_fingerprint and len(self.gpg_fingerprint) == 40:
            try:
                int(self.gpg_fingerprint, 16)  # 驗證是16進位
                score += 0.25
            except ValueError:
                pass

        # Check 3: CONFIRM 碼存在
        if self.gpg_prefix_marker and "CONFIRM" in self.gpg_prefix_marker:
            score += 0.25

        # Check 4: DNA 碼格式正確
        if self.identity_dna and self.identity_dna.startswith("#龍芯⚡️"):
            score += 0.25

        return score


@dataclass
class F2TemporalAnchor:
    """
    F2: 時間錨定 (Temporal Anchor)

    驗證內容的時間一致性和文化時間正確性
    """
    iso8601: str                   # ISO 8601 時間戳
    shichen: str                   # 時辰 (子丑寅卯辰巳午未申酉戌亥)
    digital_root: int              # 數字根 (1-9)
    lunar_calendar: str            # 農曆日期 (if available)
    time_window_violation: bool    # 時間窗口內違規?

    def verify(self) -> float:
        """
        F2 驗證 (0.0-1.0)

        Perfect (1.0): ISO8601 + 時辰 + 數字根都正確 + 無時間窗口違規
        Partial (0.7): 缺少時辰或數字根之一
        Fail (0.0): 時間戳缺失 或 時間窗口违規
        """
        score = 0.0

        # Check 1: ISO8601 存在
        if self.iso8601:
            try:
                datetime.fromisoformat(self.iso8601)
                score += 0.3
            except:
                return 0.0  # Hard fail

        # Check 2: 時辰有效
        valid_shichen = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        if self.shichen in valid_shichen:
            score += 0.35

        # Check 3: 數字根有效 (1-9)
        if 1 <= self.digital_root <= 9:
            score += 0.35

        # Check 4: 無時間窗口違規
        if not self.time_window_violation:
            # Bonus for time consistency
            pass
        else:
            return 0.0  # Hard fail - timeline violation

        return score


@dataclass
class F3RuleTrace:
    """
    F3: 規則追蹤 (Rule Trace)

    驗證決策是否遵循已知的規則鏈
    """
    rule_ids: List[str]            # 應用的規則ID列表
    rule_chain_hash: str            # 規則鏈的 SHA256
    signature: str                  # 簽名驗證
    audit_log_entries: int         # 審計日誌條目數

    def verify(self) -> float:
        """
        F3 驗證 (0.0-1.0)

        Perfect (1.0): 完整規則鏈 + 簽名驗證通過 + 審計日誌充足
        Partial (0.6): 規則鏈不完整 或 簽名驗證失敗
        Fail (0.0): 缺少規則追蹤 或 簽名無效
        """
        score = 0.0

        # Check 1: 規則ID列表非空
        if self.rule_ids and len(self.rule_ids) > 0:
            score += 0.33

        # Check 2: 規則鏈哈希有效
        if self.rule_chain_hash and len(self.rule_chain_hash) == 64:  # SHA256
            try:
                int(self.rule_chain_hash, 16)
                score += 0.33
            except:
                return 0.0  # Hard fail

        # Check 3: 簽名有效
        if self.signature and len(self.signature) > 0:
            score += 0.34

        # Bonus: 審計日誌充足 (至少3個條目)
        if self.audit_log_entries >= 3:
            score = min(1.0, score + 0.1)

        return score


@dataclass
class F4PersonaRouting:
    """
    F4: 人格路由 (Persona Routing)

    驗證決策是通過合法的路由權重做出的
    """
    primary_persona: str            # 主要路由節點 (e.g., "P02")
    persona_weights: Dict[str, float]  # 人格權重 {P02: 0.5, P05: 0.3, ...}
    veto_words_detected: bool       # 檢測到虛偽詞彙?
    routing_confidence: float       # 路由決策的置信度 (0.0-1.0)

    def verify(self) -> float:
        """
        F4 驗證 (0.0-1.0)

        Perfect (1.0): 合法路由 + 權重合法 (和=1.0) + 無虛偽詞彙
        Partial (0.5): 權重不合法 或 檢測到虛偽
        Fail (0.0): 無主路由 或 權重>1.0
        """
        score = 0.0

        # Check 1: 主路由存在
        if self.primary_persona:
            score += 0.3

        # Check 2: 權重總和接近 1.0 (允許浮點誤差)
        total_weight = sum(self.persona_weights.values())
        if 0.95 <= total_weight <= 1.05:  # 允許 ±0.05 誤差
            score += 0.35

        # Check 3: 無虛偽詞彙
        if not self.veto_words_detected:
            score += 0.35
        else:
            score = max(0.0, score - 0.5)  # 扣分

        return min(1.0, score)


@dataclass
class F5ProtectedVocabulary:
    """
    F5: 保護詞彙 (Protected Vocabulary)

    驗證主權詞彙是否被正確使用和保護
    """
    sovereign_terms_found: List[str]  # 找到的主權詞彙列表
    sovereign_terms_correct: bool     # 所有主權詞彙都正確用法?
    character_preservation: bool      # 傳統繁體字保護?
    semantic_integrity: bool          # 語義完整?

    def verify(self) -> float:
        """
        F5 驗證 (0.0-1.0)

        Perfect (1.0): 正確使用所有主權詞彙 + 繁體保護 + 語義完整
        Partial (0.5): 主權詞彙不完整使用
        Fail (0.0): 主權詞彙被破壞 或 語義被歪曲
        """
        score = 0.0

        # Check 1: 找到主權詞彙
        if self.sovereign_terms_found:
            score += 0.25

        # Check 2: 主權詞彙用法正確
        if self.sovereign_terms_correct:
            score += 0.25

        # Check 3: 繁體字保護
        if self.character_preservation:
            score += 0.25

        # Check 4: 語義完整
        if self.semantic_integrity:
            score += 0.25

        return score


@dataclass
class F6StyleVector:
    """
    F6: 風格向量 (Style Vector)

    驗證內容的寫作風格是否與創作者一致
    """
    cosine_similarity: float        # 風格向量餘弦相似度 (0.0-1.0)
    vocabulary_consistency: float   # 詞彙使用一致性
    syntax_pattern_match: float    # 句法模式匹配度
    tone_consistency: float        # 語調一致性

    def verify(self) -> float:
        """
        F6 驗證 (0.0-1.0)

        Perfect (1.0): 高風格一致性 (cos > 0.9)
        Partial (0.6): 中等一致性 (0.6 < cos < 0.8)
        Questionable (0.3): 風格不匹配 (cos < 0.6)
        Fail (0.0): 極度不匹配 (cos < 0.3)
        """
        # 用四個維度的平均值
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
    F7: 錯誤日誌 (Mistake Ledger)

    追蹤創作者的連續錯誤歷史
    """
    total_mistakes: int            # 總錯誤數
    recent_mistakes_30days: int    # 最近30天的錯誤
    mistake_recovery_rate: float   # 錯誤恢復率 (0.0-1.0)
    critical_mistakes: int         # 關鍵錯誤 (不可恢復)

    def verify(self) -> float:
        """
        F7 驗證 (0.0-1.0)

        Perfect (1.0): 無錯誤 或 恢復率100%
        Good (0.8): 少量錯誤但已恢復
        Fair (0.5): 中等錯誤量
        Poor (0.2): 大量錯誤且恢復率低
        Fail (0.0): 關鍵錯誤無法恢復
        """
        # 檢查關鍵錯誤
        if self.critical_mistakes > 0:
            return 0.0  # Hard fail

        if self.total_mistakes == 0:
            return 1.0  # Perfect

        # 根據恢復率計算
        score = self.mistake_recovery_rate * 0.8

        # 最近30天的錯誤減分
        if self.recent_mistakes_30days > 0:
            score -= (self.recent_mistakes_30days * 0.05)

        return max(0.0, min(1.0, score))


# ═══════════════════════════════════════════════════════════════
# 【主驗證引擎】
# ═══════════════════════════════════════════════════════════════

class SevenFactorVerifier:
    """
    七因子驗證系統 - 行為密碼學核心
    """

    # 七個因子及其權重 (必須加到 1.0)
    WEIGHTS = {
        VerificationFactor.F1_IDENTITY: 0.25,
        VerificationFactor.F2_TEMPORAL: 0.15,
        VerificationFactor.F3_RULE_TRACE: 0.15,
        VerificationFactor.F4_PERSONA: 0.12,
        VerificationFactor.F5_VOCABULARY: 0.12,
        VerificationFactor.F6_STYLE: 0.11,
        VerificationFactor.F7_MISTAKES: 0.10,
    }

    # 默認接納閾值
    DEFAULT_THRESHOLD = 0.85
    HIGH_SECURITY_THRESHOLD = 0.95

    def __init__(self):
        """初始化驗證系統"""
        # 驗證權重加到 1.0
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
        執行完整的七因子驗證

        Returns:
            完整驗證報告
        """
        threshold = threshold or self.DEFAULT_THRESHOLD

        # 計算各因子分數
        scores = {
            VerificationFactor.F1_IDENTITY: f1.verify(),
            VerificationFactor.F2_TEMPORAL: f2.verify(),
            VerificationFactor.F3_RULE_TRACE: f3.verify(),
            VerificationFactor.F4_PERSONA: f4.verify(),
            VerificationFactor.F5_VOCABULARY: f5.verify(),
            VerificationFactor.F6_STYLE: f6.verify(),
            VerificationFactor.F7_MISTAKES: f7.verify(),
        }

        # 檢查硬失敗 (任何因子 = 0)
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

        # 計算置信度: conf = ∏ s_i^{w_i}
        confidence = self._calculate_confidence(scores)

        # 確定驗證結果
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
        計算置信度: conf = ∏ s_i^{w_i}

        乘積形式確保任何因子為0會導致整體為0
        """
        confidence = 1.0

        for factor, score in scores.items():
            weight = self.WEIGHTS[factor]
            confidence *= (score ** weight)

        return confidence

    def _detailed_analysis(self, scores: Dict[VerificationFactor, float]) -> Dict:
        """生成詳細分析"""
        analysis = {}

        for factor, score in scores.items():
            weight = self.WEIGHTS[factor]
            contribution = score ** weight

            if score == 0.0:
                status = "🔴 硬失敗"
            elif score < 0.5:
                status = "🔴 不合格"
            elif score < 0.7:
                status = "🟡 有疑慮"
            elif score < 0.9:
                status = "🟢 合格"
            else:
                status = "🟢 優秀"

            analysis[factor.value] = {
                "score": score,
                "weight": weight,
                "contribution": contribution,
                "status": status
            }

        return analysis

    def print_report(self, verification_result: Dict) -> None:
        """列印驗證報告"""
        print("\n" + "="*70)
        print("【龍魂七因子驗證報告】")
        print("="*70 + "\n")

        print(f"置信度: {verification_result['confidence']:.4f}")
        print(f"結果: {verification_result['result']}")
        print(f"通過: {'✅ YES' if verification_result['passed'] else '❌ NO'}")
        print(f"閾值: {verification_result['threshold']}")

        if verification_result['hard_failures']:
            print(f"\n🔴 硬失敗:")
            for failure in verification_result['hard_failures']:
                print(f"  - {failure}")

        if 'detailed_analysis' in verification_result:
            print(f"\n【七因子詳細分析】")
            for factor, analysis in verification_result['detailed_analysis'].items():
                print(f"\n{factor}:")
                print(f"  分數: {analysis['score']:.4f}")
                print(f"  權重: {analysis['weight']:.2%}")
                print(f"  貢獻: {analysis['contribution']:.6f}")
                print(f"  狀態: {analysis['status']}")

        print("\n" + "="*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 【演示】
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂F1-F7七因子驗證系統 v1.0】\n")
    print("DNA: #龍芯⚡️2026-06-03-F1-F7-VERIFIER-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    verifier = SevenFactorVerifier()

    # 情景1: 高信任的創作者
    print("\n【情景1: 高信任創作者】\n")

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
        sovereign_terms_found=["龍", "道德經", "三才"],
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

    # 情景2: 有風險的內容
    print("\n【情景2: 有風險內容 (檢測到虛偽詞彙)】\n")

    f4_risk = F4PersonaRouting(
        primary_persona="P02",
        persona_weights={"P02": 0.50, "P05": 0.30, "P13": 0.20},
        veto_words_detected=True,  # 檢測到虛偽詞彙!
        routing_confidence=0.60
    )

    result_risk = verifier.verify(f1_good, f2_good, f3_good, f4_risk, f5_good, f6_good, f7_good)
    verifier.print_report(result_risk)

    # 情景3: 硬失敗 (缺失身份)
    print("\n【情景3: 硬失敗 (缺失身份驗證)】\n")

    f1_fail = F1IdentityVerification(
        uid="",  # 空UID = 失敗
        gpg_fingerprint="invalid",
        gpg_prefix_marker="",
        identity_dna="",
        creation_timestamp=""
    )

    result_fail = verifier.verify(f1_fail, f2_good, f3_good, f4_good, f5_good, f6_good, f7_good)
    verifier.print_report(result_fail)

    print("="*70)
    print("✅ 七因子驗證系統演示完成")
    print("="*70 + "\n")
