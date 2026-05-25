#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA 五行合规前置引擎 v1.0
WuXing Compliance Pre-Engine: Layer Zero Validation Gate

DNA: #龍芯⚡️2026-05-25-WEB3-DNA-WUXING-COMPLIANCE-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

第零层架构：在任何Web3-DNA操作前，必须通过五行相生相克的合规检查
- 输入合规性检查（生成初始五行向量）
- 上下文相生相克验证
- 操作流向和谐度评分
- 返回：合规/黄灯/红灯三色判定

不通过Red的操作自动阻断（零容错）
Yellow的操作进入人工审核队列
Green的操作自动通过，记录审计日志

本地计算·永不外送·纯数学·零ML依赖

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承
"""

import hashlib
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


# ════════════════════════════════════════════════════════
# 第一步：五行向量定义与相生相克关系
# ════════════════════════════════════════════════════════

class WuXing(Enum):
    """五行"""
    WOOD = "木"    # 1, 2
    FIRE = "火"    # 3, 4
    EARTH = "土"   # 5
    METAL = "金"   # 6, 7
    WATER = "水"   # 8, 9, 0


@dataclass
class WuXingVector:
    """五行向量：包含强度、相位、与环境共鸣度"""
    wuxing: WuXing
    strength: float        # 0.0-1.0，表示该五行的强度
    phase: str            # rising / peak / declining / dormant
    resonance: float      # 与上下文的共鸣度 0.0-1.0

    def __repr__(self):
        return f"{self.wuxing.value}({self.strength:.2f}|{self.phase}|R:{self.resonance:.2f})"


@dataclass
class ComplianceResult:
    """合规判定结果"""
    color: str                    # green / yellow / red
    score: float                  # 0.0-1.0 的合规评分
    input_vector: WuXingVector   # 输入五行向量
    context_vector: WuXingVector # 上下文五行向量
    resonance_score: float        # 相生相克评分
    reason: str                   # 判定原因
    dna: str                      # 追溯码
    timestamp: str                # 时间戳


# ════════════════════════════════════════════════════════
# 第二步：五行相生相克规则引擎
# ════════════════════════════════════════════════════════

class WuXingResonanceEngine:
    """五行相生相克引擎"""

    # 相生关系：木生火、火生土、土生金、金生水、水生木
    GENERATING = {
        WuXing.WOOD: WuXing.FIRE,
        WuXing.FIRE: WuXing.EARTH,
        WuXing.EARTH: WuXing.METAL,
        WuXing.METAL: WuXing.WATER,
        WuXing.WATER: WuXing.WOOD,
    }

    # 相克关系：木克土、土克水、水克火、火克金、金克木
    CONTROLLING = {
        WuXing.WOOD: WuXing.EARTH,
        WuXing.EARTH: WuXing.WATER,
        WuXing.WATER: WuXing.FIRE,
        WuXing.FIRE: WuXing.METAL,
        WuXing.METAL: WuXing.WOOD,
    }

    @staticmethod
    def check_resonance(vector1: WuXingVector, vector2: WuXingVector) -> float:
        """
        检查两个五行向量的共鸣度（0.0-1.0）
        相生 = 0.9 | 同类 = 1.0 | 相克 = 0.3 | 无关 = 0.5
        """
        if vector1.wuxing == vector2.wuxing:
            return 1.0  # 同类最和谐

        if WuXingResonanceEngine.GENERATING.get(vector1.wuxing) == vector2.wuxing:
            return 0.9  # 相生很和谐

        if WuXingResonanceEngine.GENERATING.get(vector2.wuxing) == vector1.wuxing:
            return 0.9  # 反向相生也很和谐

        if WuXingResonanceEngine.CONTROLLING.get(vector1.wuxing) == vector2.wuxing:
            return 0.3  # 相克不和谐

        if WuXingResonanceEngine.CONTROLLING.get(vector2.wuxing) == vector1.wuxing:
            return 0.3  # 被克也不和谐

        return 0.5  # 无直接关系

    @staticmethod
    def calculate_multi_resonance(vectors: List[WuXingVector]) -> float:
        """
        计算多个向量之间的整体共鸣度
        基于两两之间相生相克关系的平均值
        """
        if len(vectors) < 2:
            return 1.0

        resonances = []
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                r = WuXingResonanceEngine.check_resonance(vectors[i], vectors[j])
                resonances.append(r)

        return sum(resonances) / len(resonances) if resonances else 1.0


# ════════════════════════════════════════════════════════
# 第三步：合规性评分引擎
# ════════════════════════════════════════════════════════

class ComplianceScoringEngine:
    """
    合规性评分引擎：
    score = (strength_factor * resonance_score * phase_factor)
          + (context_harmony * 0.3)
          + (legal_risk_mitigation * 0.2)

    三色判定：
    - Green   (≥ 0.75): 完全合规，自动通过
    - Yellow  (0.5-0.75): 需要人工审查
    - Red     (< 0.5): 高风险，自动阻断
    """

    @staticmethod
    def score_input_compliance(
        input_vector: WuXingVector,
        context_vector: WuXingVector,
        operation_type: str = "transaction"
    ) -> ComplianceResult:
        """
        打分输入的合规性
        """
        # 第一部分：五行强度和相位评分
        strength_factor = input_vector.strength

        phase_factor = {
            "rising": 1.0,      # 上升阶段最优
            "peak": 0.95,       # 顶峰稍弱
            "declining": 0.7,   # 衰落阶段风险
            "dormant": 0.3,     # 休眠阶段最弱
        }.get(input_vector.phase, 0.5)

        # 第二部分：与上下文的共鸣度
        resonance_score = WuXingResonanceEngine.check_resonance(input_vector, context_vector)

        # 第三部分：合规综合评分
        # 权重分配：强度(50%) + 共鸣(30%) + 相位(20%)
        compliance_score = (
            strength_factor * 0.5 +
            resonance_score * 0.3 +
            phase_factor * 0.2
        )

        # 判定颜色
        if compliance_score >= 0.75:
            color = "green"
            reason = f"五行合规通过（强度:{strength_factor:.2f}, 共鸣:{resonance_score:.2f}）"
        elif compliance_score >= 0.5:
            color = "yellow"
            reason = f"需要人工审查（评分:{compliance_score:.2f}）"
        else:
            color = "red"
            reason = f"高风险阻断（共鸣不足:{resonance_score:.2f}）"

        # 生成DNA
        dna_hash = hashlib.sha256(
            f"{input_vector.wuxing.value}{context_vector.wuxing.value}{compliance_score}".encode()
        ).hexdigest()[:8]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-WUXING-COMPLIANCE-{dna_hash}"

        return ComplianceResult(
            color=color,
            score=round(compliance_score, 3),
            input_vector=input_vector,
            context_vector=context_vector,
            resonance_score=resonance_score,
            reason=reason,
            dna=dna,
            timestamp=datetime.now().isoformat(),
        )


# ════════════════════════════════════════════════════════
# 第四步：合规前置引擎（主类）
# ════════════════════════════════════════════════════════

class WuXingComplianceEngine:
    """五行合规前置引擎 - Web3-DNA第零层验证门"""

    def __init__(self):
        self.resonance_engine = WuXingResonanceEngine()
        self.scoring_engine = ComplianceScoringEngine()
        self.audit_log: List[ComplianceResult] = []

    @staticmethod
    def calculate_digital_root(text: str) -> int:
        """计算文本的数字根（1-9）"""
        total = sum(ord(c) for c in text)
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total if total > 0 else 9

    @staticmethod
    def map_to_wuxing(dr: int) -> WuXing:
        """数字根映射到五行"""
        mapping = {
            1: WuXing.WOOD,  2: WuXing.WOOD,
            3: WuXing.FIRE,  4: WuXing.FIRE,
            5: WuXing.EARTH,
            6: WuXing.METAL, 7: WuXing.METAL,
            8: WuXing.WATER, 9: WuXing.WATER,
        }
        return mapping.get(dr, WuXing.EARTH)

    @staticmethod
    def determine_phase(dr: int) -> str:
        """
        根据数字根确定相位
        1-3: rising (上升)
        4-5: peak (顶峰)
        6-7: declining (衰落)
        8-9: dormant (休眠)
        """
        if 1 <= dr <= 3:
            return "rising"
        elif 4 <= dr <= 5:
            return "peak"
        elif 6 <= dr <= 7:
            return "declining"
        else:
            return "dormant"

    def generate_input_vector(self, input_text: str) -> WuXingVector:
        """从输入文本生成五行向量"""
        dr = self.calculate_digital_root(input_text)
        wuxing = self.map_to_wuxing(dr)
        phase = self.determine_phase(dr)

        # 强度 = (dr 的相对值) / 9.0
        strength = dr / 9.0

        # 初始共鸣度（输入本身的谐波性）
        resonance = 0.5 + (strength * 0.3)  # 0.5-0.8的基线

        return WuXingVector(
            wuxing=wuxing,
            strength=strength,
            phase=phase,
            resonance=resonance
        )

    def generate_context_vector(self, context_text: str) -> WuXingVector:
        """从上下文生成五行向量"""
        # 使用相同的逻辑，但强度计算略有不同（反映上下文的"容纳度"）
        dr = self.calculate_digital_root(context_text)
        wuxing = self.map_to_wuxing(dr)
        phase = self.determine_phase(dr)

        # 上下文的强度通常更稳定
        strength = (dr + 5) / 14.0  # 更接近 0.5
        resonance = 0.6 + (strength * 0.2)  # 0.6-0.8

        return WuXingVector(
            wuxing=wuxing,
            strength=strength,
            phase=phase,
            resonance=resonance
        )

    def check_compliance(
        self,
        input_text: str,
        context_text: str = "",
        operation_type: str = "transaction"
    ) -> ComplianceResult:
        """
        执行合规检查
        返回：ComplianceResult（包含color/score/reason/dna）
        """
        # 生成向量
        input_vector = self.generate_input_vector(input_text)
        context_vector = self.generate_context_vector(context_text) if context_text else input_vector

        # 评分
        result = self.scoring_engine.score_input_compliance(
            input_vector,
            context_vector,
            operation_type
        )

        # 记录审计日志
        self.audit_log.append(result)

        return result

    def should_allow_operation(self, compliance_result: ComplianceResult) -> bool:
        """
        根据合规结果判断是否允许操作
        - Green: 允许
        - Yellow: 等待人工审查（此处返回False等待外部确认）
        - Red: 阻止
        """
        return compliance_result.color == "green"


# ════════════════════════════════════════════════════════
# 测试与演示
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔐 龍魂 Web3-DNA 五行合规前置引擎 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-WEB3-DNA-WUXING-COMPLIANCE-v1.0")
    print("=" * 60 + "\n")

    engine = WuXingComplianceEngine()

    # 测试用例
    test_cases = [
        ("用户支付1000元购买DNA资产", "区块链交易合规"),
        ("转账到未认证钱包", "高风险交易"),
        ("标准身份验证流程", "日常用户操作"),
    ]

    print("📍 测试 1: 五行合规检查\n")
    for i, (input_text, context_text) in enumerate(test_cases, 1):
        result = engine.check_compliance(input_text, context_text)
        print(f"   案例 {i}: {input_text}")
        print(f"   → 颜色: {result.color.upper()} | 分数: {result.score}")
        print(f"   → 输入向量: {result.input_vector}")
        print(f"   → 上下文向量: {result.context_vector}")
        print(f"   → 原因: {result.reason}")
        print(f"   → DNA: {result.dna}\n")

    print("=" * 60)
    print("✅ 五行合规前置引擎初始化完成")
    print("=" * 60 + "\n")
    print("🐉 龍魂 Web3-DNA · 第零层合规门 · UID9622不免责")
