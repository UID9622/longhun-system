#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 v2.0 | Tongxin Translation v2.0
七维评估器 | Seven-Dimension Evaluator

可直接运行的Python骨架代码，包含：
- 七维评分系统
- 综合R分数计算
- 质量报告生成
- DNA追溯

文件DNA: #龍芯⚡️2026-07-01-TONGXIN-TRANSLATION-v2.0
父DNA: #龍芯⚡️2026-06-19-LONGWEN-NLP-v5.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import json
import numpy as np
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════

class QualityGrade(Enum):
    """质量等级枚举 | Quality Grade Enumeration"""
    S_EXCELLENT = "S"      # 卓越 0.95-1.00
    A_GOOD = "A"           # 优秀 0.85-0.95
    B_ACCEPTABLE = "B"     # 良好 0.70-0.85
    C_NEEDS_WORK = "C"     # 及格 0.55-0.70
    D_FAIL = "D"           # 不及格 <0.55


class TranslationDimension(Enum):
    """七维训练维度枚举 | Seven Training Dimensions"""
    D1_CULTURE_LEXICON = "D1_culture_lexicon"           # 文化负载词映射
    D2_SEMANTIC_SYNTAX = "D2_semantic_syntax"           # 语义-语法制约
    D3_CLASSICAL_CHINESE = "D3_classical_chinese"       # 古代汉语转换
    D4_DISCOURSE_INTEGRITY = "D4_discourse_integrity"   # 语篇完整性
    D5_CIVILIZATION_SAFETY = "D5_civilization_safety"   # 文明安全
    D6_CREATIVE_STRATEGY = "D6_creative_strategy"       # 创造性策略
    D7_SEMANTIC_PRECISION = "D7_semantic_precision"     # 语义精确性


# ═══════════════════════════════════════════════════════════════
# 全局配置
# ═══════════════════════════════════════════════════════════════

# 七维权重配置（可调）
DIMENSION_WEIGHTS = {
    TranslationDimension.D1_CULTURE_LEXICON: 0.20,
    TranslationDimension.D2_SEMANTIC_SYNTAX: 0.15,
    TranslationDimension.D3_CLASSICAL_CHINESE: 0.10,
    TranslationDimension.D4_DISCOURSE_INTEGRITY: 0.20,
    TranslationDimension.D5_CIVILIZATION_SAFETY: 0.15,
    TranslationDimension.D6_CREATIVE_STRATEGY: 0.10,
    TranslationDimension.D7_SEMANTIC_PRECISION: 0.10,
}

# R分数计算参数
R_SCORE_ALPHA = 0.1    # 创造性奖励系数
R_SCORE_BETA = 0.5     # 安全惩罚系数
R_SCORE_SAFETY_THRESHOLD = 0.95  # 文明安全阈值

# DNA追溯
FILE_DNA = "#龍芯⚡️2026-07-01-TONGXIN-TRANSLATION-v2.0"
PARENT_DNA = "#龍芯⚡️2026-06-19-LONGWEN-NLP-v5.0"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"


# ═══════════════════════════════════════════════════════════════
# 数据类定义
# ═══════════════════════════════════════════════════════════════

@dataclass
class LiteralLayer:
    """字面层输出 | Literal Layer Output"""
    text: str
    terminology_mapping: List[Dict[str, str]] = field(default_factory=list)
    confidence: float = 0.0
    error_flag: Optional[str] = None
    ambiguity_note: Optional[str] = None


@dataclass
class LogicalLayer:
    """逻辑层输出 | Logical Layer Output"""
    text: str
    semantic_entailments: List[Dict[str, str]] = field(default_factory=list)
    discourse_structure: str = ""
    confidence: float = 0.0


@dataclass
class IntentionalLayer:
    """心意层输出 | Intentional Layer Output"""
    text: str
    cultural_intention: str = ""
    imagery_mapping: List[Dict[str, str]] = field(default_factory=list)
    civilization_safety_score: float = 100.0
    confidence: float = 0.0


@dataclass
class DimensionScores:
    """七维评分 | Seven-Dimension Scores"""
    D1_culture_lexicon: float = 0.0
    D2_semantic_syntax: float = 0.0
    D3_classical_chinese: float = 0.0
    D4_discourse_integrity: float = 0.0
    D5_civilization_safety: float = 0.0
    D6_creative_strategy: float = 0.0
    D7_semantic_precision: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "D1_culture_lexicon": self.D1_culture_lexicon,
            "D2_semantic_syntax": self.D2_semantic_syntax,
            "D3_classical_chinese": self.D3_classical_chinese,
            "D4_discourse_integrity": self.D4_discourse_integrity,
            "D5_civilization_safety": self.D5_civilization_safety,
            "D6_creative_strategy": self.D6_creative_strategy,
            "D7_semantic_precision": self.D7_semantic_precision,
        }
    
    def min_score(self) -> float:
        """返回最低维度分"""
        return min(self.to_dict().values())
    
    def mean_score(self) -> float:
        """返回平均维度分"""
        return np.mean(list(self.to_dict().values()))


@dataclass
class TranslationOutput:
    """通心译完整输出 | Tongxin Translation Complete Output"""
    source_text: str
    literal: LiteralLayer
    logical: LogicalLayer
    intentional: IntentionalLayer
    dimension_scores: DimensionScores = field(default_factory=DimensionScores)
    r_score: float = 0.0
    quality_grade: QualityGrade = QualityGrade.D_FAIL
    
    def to_dict(self) -> Dict:
        return {
            "source_text": self.source_text,
            "literal": {
                "text": self.literal.text,
                "terminology_mapping": self.literal.terminology_mapping,
                "confidence": self.literal.confidence,
                "error_flag": self.literal.error_flag,
                "ambiguity_note": self.literal.ambiguity_note,
            },
            "logical": {
                "text": self.logical.text,
                "semantic_entailments": self.logical.semantic_entailments,
                "discourse_structure": self.logical.discourse_structure,
                "confidence": self.logical.confidence,
            },
            "intentional": {
                "text": self.intentional.text,
                "cultural_intention": self.intentional.cultural_intention,
                "imagery_mapping": self.intentional.imagery_mapping,
                "civilization_safety_score": self.intentional.civilization_safety_score,
                "confidence": self.intentional.confidence,
            },
            "dimension_scores": self.dimension_scores.to_dict(),
            "r_score": self.r_score,
            "quality_grade": self.quality_grade.value,
        }


# ═══════════════════════════════════════════════════════════════
# 核心评估器类
# ═══════════════════════════════════════════════════════════════

class TongxinEvaluator:
    """
    通心译七维评估器 | Tongxin Seven-Dimension Evaluator
    
    功能:
    1. 七维独立评分
    2. 综合R分数计算
    3. 质量等级判定
    4. 质量报告生成
    5. 批量评估
    """
    
    def __init__(self, 
                 weights: Optional[Dict[TranslationDimension, float]] = None,
                 alpha: float = R_SCORE_ALPHA,
                 beta: float = R_SCORE_BETA,
                 safety_threshold: float = R_SCORE_SAFETY_THRESHOLD):
        """
        初始化评估器
        
        Args:
            weights: 七维权重字典，默认使用全局配置
            alpha: 创造性奖励系数
            beta: 安全惩罚系数
            safety_threshold: 文明安全阈值
        """
        self.weights = weights or DIMENSION_WEIGHTS
        self.alpha = alpha
        self.beta = beta
        self.safety_threshold = safety_threshold
        self.evaluation_history: List[Dict] = []
        
        # 验证权重归一化
        total_weight = sum(self.weights.values())
        if abs(total_weight - 1.0) > 0.01:
            print(f"[WARN] 权重未归一化: sum={total_weight:.3f}，自动归一化")
            for k in self.weights:
                self.weights[k] /= total_weight
    
    # ─────────────────────────────────────────────────────────
    # 公共API: 评估
    # ─────────────────────────────────────────────────────────
    
    def evaluate(self, 
                 output: TranslationOutput, 
                 reference: Optional[TranslationOutput] = None) -> TranslationOutput:
        """
        执行七维评估并计算R-Score
        
        Args:
            output: 待评估的翻译输出
            reference: 参考答案（可选）
        
        Returns:
            更新后的TranslationOutput（含评分和等级）
        """
        # 步骤1: 计算七维评分
        if reference:
            scores = self._calculate_dimension_scores_with_reference(output, reference)
        else:
            scores = self._calculate_dimension_scores_autonomous(output)
        output.dimension_scores = scores
        
        # 步骤2: 计算R-Score
        output.r_score = self._calculate_r_score(scores)
        
        # 步骤3: 确定质量等级
        output.quality_grade = self._determine_grade(output.r_score)
        
        # 步骤4: 记录历史
        self.evaluation_history.append({
            "timestamp": datetime.now().isoformat(),
            "source": output.source_text[:50],
            "r_score": output.r_score,
            "grade": output.quality_grade.value,
            "scores": scores.to_dict(),
        })
        
        return output
    
    def evaluate_batch(self, 
                       outputs: List[TranslationOutput],
                       references: Optional[List[TranslationOutput]] = None) -> List[TranslationOutput]:
        """
        批量评估
        
        Args:
            outputs: 待评估的翻译输出列表
            references: 参考答案列表（可选）
        
        Returns:
            更新后的TranslationOutput列表
        """
        results = []
        for i, output in enumerate(outputs):
            ref = references[i] if references and i < len(references) else None
            result = self.evaluate(output, ref)
            results.append(result)
        return results
    
    # ─────────────────────────────────────────────────────────
    # 核心: 七维评分计算
    # ─────────────────────────────────────────────────────────
    
    def _calculate_dimension_scores_autonomous(self, output: TranslationOutput) -> DimensionScores:
        """
        自主评估七维评分（无参考答案）
        
        基于输出内容的内部特征进行启发式评分。
        实际部署时应替换为训练好的评估模型。
        """
        scores = DimensionScores()
        
        # D1: 文化负载词评分
        scores.D1_culture_lexicon = self._score_d1_culture_lexicon(output)
        
        # D2: 语义-语法制约评分
        scores.D2_semantic_syntax = self._score_d2_semantic_syntax(output)
        
        # D3: 古代汉语转换评分
        scores.D3_classical_chinese = self._score_d3_classical_chinese(output)
        
        # D4: 语篇完整性评分
        scores.D4_discourse_integrity = self._score_d4_discourse_integrity(output)
        
        # D5: 文明安全评分
        scores.D5_civilization_safety = self._score_d5_civilization_safety(output)
        
        # D6: 创造性策略评分
        scores.D6_creative_strategy = self._score_d6_creative_strategy(output)
        
        # D7: 语义精确性评分
        scores.D7_semantic_precision = self._score_d7_semantic_precision(output)
        
        return scores
    
    def _calculate_dimension_scores_with_reference(
        self, 
        output: TranslationOutput, 
        reference: TranslationOutput
    ) -> DimensionScores:
        """
        基于参考答案的七维评分
        
        计算输出与参考在各维度上的相似度。
        """
        scores = DimensionScores()
        
        # 各维度与参考的对比评分
        scores.D1_culture_lexicon = self._compare_d1(output, reference)
        scores.D2_semantic_syntax = self._compare_d2(output, reference)
        scores.D3_classical_chinese = self._compare_d3(output, reference)
        scores.D4_discourse_integrity = self._compare_d4(output, reference)
        scores.D5_civilization_safety = self._compare_d5(output, reference)
        scores.D6_creative_strategy = self._compare_d6(output, reference)
        scores.D7_semantic_precision = self._compare_d7(output, reference)
        
        return scores
    
    # ─────────────────────────────────────────────────────────
    # 各维度评分实现（启发式版本）
    # ─────────────────────────────────────────────────────────
    
    def _score_d1_culture_lexicon(self, output: TranslationOutput) -> float:
        """D1: 文化负载词映射评分"""
        score = 0.5  # 基础分
        
        # 检查术语映射数量
        term_count = len(output.literal.terminology_mapping)
        if term_count >= 3:
            score += 0.15
        elif term_count >= 1:
            score += 0.05
        
        # 检查心意层是否有文化意图说明
        if output.intentional.cultural_intention and len(output.intentional.cultural_intention) > 20:
            score += 0.15
        
        # 检查是否有意象映射
        if len(output.intentional.imagery_mapping) > 0:
            score += 0.10
        
        # 检查字面层是否有错误标记
        if output.literal.error_flag and "GRAMMAR" in output.literal.error_flag:
            score -= 0.10
        
        # 检查文明安全分是否合理
        if 80 <= output.intentional.civilization_safety_score <= 100:
            score += 0.10
        
        return max(0.0, min(1.0, score))
    
    def _score_d2_semantic_syntax(self, output: TranslationOutput) -> float:
        """D2: 语义-语法制约评分"""
        score = 0.5
        
        # 检查语义蕴含数量
        entailment_count = len(output.logical.semantic_entailments)
        if entailment_count >= 3:
            score += 0.20
        elif entailment_count >= 1:
            score += 0.10
        
        # 检查语篇结构标注
        if output.logical.discourse_structure and len(output.logical.discourse_structure) > 5:
            score += 0.15
        
        # 检查逻辑层与字面层的一致性
        if output.logical.text != output.literal.text:
            score += 0.10  # 逻辑层有改进
        
        # 检查是否有语法错误标记
        if output.literal.error_flag:
            score -= 0.15
        
        # 检查逻辑层置信度
        score += output.logical.confidence * 0.05
        
        return max(0.0, min(1.0, score))
    
    def _score_d3_classical_chinese(self, output: TranslationOutput) -> float:
        """D3: 古代汉语转换评分"""
        score = 0.5
        
        source = output.source_text
        
        # 检测源文本是否包含古汉语特征
        classical_markers = ["之", "乎", "者", "也", "矣", "焉", "哉", "曰", "子曰", "诗云"]
        has_classical = any(m in source for m in classical_markers)
        
        if has_classical:
            # 有古汉语内容，评估转换质量
            if len(output.intentional.cultural_intention) > 30:
                score += 0.20
            if len(output.logical.semantic_entailments) >= 2:
                score += 0.15
            if output.intentional.confidence > 0.7:
                score += 0.15
        else:
            # 无古汉语内容，该维度不适用，给中性分
            score = 0.60
        
        return max(0.0, min(1.0, score))
    
    def _score_d4_discourse_integrity(self, output: TranslationOutput) -> float:
        """D4: 语篇完整性评分"""
        score = 0.5
        
        # 检查三层输出是否存在
        if output.literal.text and output.logical.text and output.intentional.text:
            score += 0.15
        
        # 检查上下文连贯性（语篇结构标注）
        if output.logical.discourse_structure:
            score += 0.15
        
        # 检查语义蕴含的完整性
        if len(output.logical.semantic_entailments) >= 2:
            score += 0.15
        
        # 检查是否有断章取义风险（心意层是否完整传达）
        if output.intentional.confidence >= 0.8:
            score += 0.15
        elif output.intentional.confidence >= 0.5:
            score += 0.05
        
        # 检查是否有歧义标记
        if output.literal.ambiguity_note:
            score -= 0.10
        
        return max(0.0, min(1.0, score))
    
    def _score_d5_civilization_safety(self, output: TranslationOutput) -> float:
        """D5: 文明安全评分"""
        # 直接使用心意层的文明安全分（归一化）
        css = output.intentional.civilization_safety_score
        
        # 检查是否有文化意图注释（表明有意识处理）
        has_intention_note = bool(output.intentional.cultural_intention)
        
        # 基础分来自文明安全分数
        base_score = css / 100.0
        
        # 有注释加分
        if has_intention_note:
            base_score += 0.05
        
        return max(0.0, min(1.0, base_score))
    
    def _score_d6_creative_strategy(self, output: TranslationOutput) -> float:
        """D6: 创造性策略评分"""
        score = 0.5
        
        # 检查意象映射（创造性替换）
        imagery_count = len(output.intentional.imagery_mapping)
        if imagery_count >= 2:
            score += 0.20
        elif imagery_count >= 1:
            score += 0.10
        
        # 检查心意层与逻辑层是否有有意义的差异（创造性改写）
        intentional_text = output.intentional.text
        logical_text = output.logical.text
        
        # 有意义的差异（不是简单扩展，而是实质性改写）
        if len(intentional_text) > len(logical_text) * 1.2:
            score += 0.10
        
        # 检查是否有文化注释（创造性注释策略）
        if "[" in intentional_text and "]" in intentional_text:
            score += 0.10
        
        # 检查心意层置信度（创造性不能过度）
        if output.intentional.confidence >= 0.8:
            score += 0.10
        elif output.intentional.confidence < 0.5:
            score -= 0.10
        
        return max(0.0, min(1.0, score))
    
    def _score_d7_semantic_precision(self, output: TranslationOutput) -> float:
        """D7: 语义精确性评分"""
        score = 0.5
        
        # 检查是否有歧义标记（精确性问题的诚实标记）
        if output.literal.ambiguity_note:
            # 诚实标记歧义是好的，但内容本身有歧义
            score += 0.05
        
        # 检查术语映射的精确度
        if len(output.literal.terminology_mapping) > 0:
            # 检查是否有括号注释（精确标注）
            for mapping in output.literal.terminology_mapping:
                if "(" in mapping.get("target", ""):
                    score += 0.05
                    break
        
        # 检查语义蕴含的精确性
        entailments = output.logical.semantic_entailments
        if len(entailments) > 0:
            score += 0.10
            # 检查蕴含是否有完整的premise-conclusion结构
            for e in entailments:
                if e.get("premise") and e.get("conclusion"):
                    score += 0.03
        
        # 字面层置信度作为精确性指标
        score += output.literal.confidence * 0.10
        
        # 如果有语法错误，扣分
        if output.literal.error_flag:
            score -= 0.15
        
        return max(0.0, min(1.0, score))
    
    # ─────────────────────────────────────────────────────────
    # 参考对比评分（简化版）
    # ─────────────────────────────────────────────────────────
    
    def _compare_d1(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D1评分"""
        # 术语映射数量对比
        out_terms = len(output.literal.terminology_mapping)
        ref_terms = len(reference.literal.terminology_mapping)
        if ref_terms == 0:
            return 0.8
        return max(0.0, min(1.0, 1.0 - abs(out_terms - ref_terms) / ref_terms * 0.3))
    
    def _compare_d2(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D2评分"""
        out_ent = len(output.logical.semantic_entailments)
        ref_ent = len(reference.logical.semantic_entailments)
        if ref_ent == 0:
            return 0.8
        return max(0.0, min(1.0, 1.0 - abs(out_ent - ref_ent) / ref_ent * 0.3))
    
    def _compare_d3(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D3评分"""
        return 0.7  # 简化处理
    
    def _compare_d4(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D4评分"""
        return 0.8 if output.logical.discourse_structure == reference.logical.discourse_structure else 0.6
    
    def _compare_d5(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D5评分"""
        out_css = output.intentional.civilization_safety_score
        ref_css = reference.intentional.civilization_safety_score
        return max(0.0, min(1.0, 1.0 - abs(out_css - ref_css) / 100 * 2))
    
    def _compare_d6(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D6评分"""
        return 0.75  # 简化处理
    
    def _compare_d7(self, output: TranslationOutput, reference: TranslationOutput) -> float:
        """对比D7评分"""
        return 0.8  # 简化处理
    
    # ─────────────────────────────────────────────────────────
    # 核心: R分数计算
    # ─────────────────────────────────────────────────────────
    
    def _calculate_r_score(self, scores: DimensionScores) -> float:
        """
        计算综合R分数
        
        公式: R = Σ(w_i × Dim_i) + α × Creativity_Bonus - β × Safety_Penalty
        
        Args:
            scores: 七维评分
        
        Returns:
            R-Score (0.0 - 1.0)
        """
        # 基础加权分
        base_score = (
            self.weights[TranslationDimension.D1_CULTURE_LEXICON] * scores.D1_culture_lexicon +
            self.weights[TranslationDimension.D2_SEMANTIC_SYNTAX] * scores.D2_semantic_syntax +
            self.weights[TranslationDimension.D3_CLASSICAL_CHINESE] * scores.D3_classical_chinese +
            self.weights[TranslationDimension.D4_DISCOURSE_INTEGRITY] * scores.D4_discourse_integrity +
            self.weights[TranslationDimension.D5_CIVILIZATION_SAFETY] * scores.D5_civilization_safety +
            self.weights[TranslationDimension.D6_CREATIVE_STRATEGY] * scores.D6_creative_strategy +
            self.weights[TranslationDimension.D7_SEMANTIC_PRECISION] * scores.D7_semantic_precision
        )
        
        # 创造性奖励: 当D6超过0.8时触发
        dim_values = [
            scores.D1_culture_lexicon, scores.D2_semantic_syntax,
            scores.D3_classical_chinese, scores.D4_discourse_integrity,
            scores.D5_civilization_safety, scores.D6_creative_strategy,
            scores.D7_semantic_precision
        ]
        creativity_bonus = max(0, scores.D6_creative_strategy - 0.8) * np.mean(dim_values)
        
        # 安全惩罚: 当D5低于阈值时重罚
        safety_penalty = max(0, self.safety_threshold - scores.D5_civilization_safety) * self.beta * 2
        
        r_score = base_score + self.alpha * creativity_bonus - safety_penalty
        
        # 截断到[0, 1]
        return max(0.0, min(1.0, r_score))
    
    def _determine_grade(self, r_score: float) -> QualityGrade:
        """
        根据R-Score确定质量等级
        
        Args:
            r_score: 综合R分数
        
        Returns:
            QualityGrade枚举值
        """
        if r_score >= 0.95:
            return QualityGrade.S_EXCELLENT
        elif r_score >= 0.85:
            return QualityGrade.A_GOOD
        elif r_score >= 0.70:
            return QualityGrade.B_ACCEPTABLE
        elif r_score >= 0.55:
            return QualityGrade.C_NEEDS_WORK
        else:
            return QualityGrade.D_FAIL
    
    # ─────────────────────────────────────────────────────────
    # 报告生成
    # ─────────────────────────────────────────────────────────
    
    def generate_report(self, output: TranslationOutput, verbose: bool = True) -> str:
        """
        生成质量报告
        
        Args:
            output: 已评估的翻译输出
            verbose: 是否生成详细报告
        
        Returns:
            质量报告字符串
        """
        scores = output.dimension_scores
        
        if verbose:
            report = self._generate_verbose_report(output, scores)
        else:
            report = self._generate_compact_report(output, scores)
        
        return report
    
    def _generate_verbose_report(self, output: TranslationOutput, scores: DimensionScores) -> str:
        """生成详细报告"""
        
        def bar(score: float) -> str:
            filled = int(score * 10)
            return '█' * filled + '░' * (10 - filled)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           通心译 v2.0 质量报告 | Quality Report                   ║
╠══════════════════════════════════════════════════════════════════╣
  样本ID: {hash(output.source_text) & 0xFFFF:04X}
  原文: {output.source_text[:60]}{"..." if len(output.source_text) > 60 else ""}
  
  ┌─────────────────────────────────────────────────────────┐
  │  R-Score: {output.r_score:.3f}  (等级: {output.quality_grade.value}){" " * (29 - len(f"{output.r_score:.3f}"))}│
  └─────────────────────────────────────────────────────────┘

  七维雷达 | Dimension Radar:
  ─────────────────────────────────────────────────────────────
  D1 文化负载词  {scores.D1_culture_lexicon:.2f} {bar(scores.D1_culture_lexicon)}  {scores.D1_culture_lexicon * 100:.0f}%
  D2 语义-语法   {scores.D2_semantic_syntax:.2f} {bar(scores.D2_semantic_syntax)}  {scores.D2_semantic_syntax * 100:.0f}%
  D3 古代汉语    {scores.D3_classical_chinese:.2f} {bar(scores.D3_classical_chinese)}  {scores.D3_classical_chinese * 100:.0f}%
  D4 语篇完整    {scores.D4_discourse_integrity:.2f} {bar(scores.D4_discourse_integrity)}  {scores.D4_discourse_integrity * 100:.0f}%
  D5 文明安全    {scores.D5_civilization_safety:.2f} {bar(scores.D5_civilization_safety)}  {scores.D5_civilization_safety * 100:.0f}%
  D6 创造策略    {scores.D6_creative_strategy:.2f} {bar(scores.D6_creative_strategy)}  {scores.D6_creative_strategy * 100:.0f}%
  D7 语义精确    {scores.D7_semantic_precision:.2f} {bar(scores.D7_semantic_precision)}  {scores.D7_semantic_precision * 100:.0f}%

  分析 | Analysis:
  ─────────────────────────────────────────────────────────────
  主要弱点: {self._identify_weakness(scores)}
  改进方向: {self._suggest_improvement(scores)}
  平均维度分: {scores.mean_score():.3f}
  最低维度分: {scores.min_score():.3f} (瓶颈维度)

  三层输出 | Tri-Layer Output:
  ─────────────────────────────────────────────────────────────
  [L] {output.literal.text[:70]}{"..." if len(output.literal.text) > 70 else ""}
  [G] {output.logical.text[:70]}{"..." if len(output.logical.text) > 70 else ""}
  [I] {output.intentional.text[:70]}{"..." if len(output.intentional.text) > 70 else ""}

  {FILE_DNA}
╚══════════════════════════════════════════════════════════════════╝
"""
        return report
    
    def _generate_compact_report(self, output: TranslationOutput, scores: DimensionScores) -> str:
        """生成紧凑报告"""
        return (f"R={output.r_score:.3f}({output.quality_grade.value}) | "
                f"D1={scores.D1_culture_lexicon:.2f} "
                f"D2={scores.D2_semantic_syntax:.2f} "
                f"D3={scores.D3_classical_chinese:.2f} "
                f"D4={scores.D4_discourse_integrity:.2f} "
                f"D5={scores.D5_civilization_safety:.2f} "
                f"D6={scores.D6_creative_strategy:.2f} "
                f"D7={scores.D7_semantic_precision:.2f}")
    
    def _identify_weakness(self, scores: DimensionScores) -> str:
        """识别主要弱点"""
        score_dict = {
            "D1文化负载词": scores.D1_culture_lexicon,
            "D2语义-语法": scores.D2_semantic_syntax,
            "D3古代汉语": scores.D3_classical_chinese,
            "D4语篇完整": scores.D4_discourse_integrity,
            "D5文明安全": scores.D5_civilization_safety,
            "D6创造策略": scores.D6_creative_strategy,
            "D7语义精确": scores.D7_semantic_precision,
        }
        weakest = min(score_dict, key=score_dict.get)
        return f"{weakest} ({score_dict[weakest]:.2f})"
    
    def _suggest_improvement(self, scores: DimensionScores) -> str:
        """基于弱点给出改进建议"""
        weakness = self._identify_weakness(scores)
        suggestions = {
            "D1": "增加文化负载词注释，使用CNSH术语引擎查询",
            "D2": "检查语义-语法制约关系，确保句法受语义驱动",
            "D3": "使用古汉语知识图谱辅助释义",
            "D4": "扩大上下文窗口，检查信息完整性",
            "D5": "进行文明安全风险评估，调整文化立场",
            "D6": "尝试比喻/意象替换策略",
            "D7": "消除语义模糊，增加消歧处理",
        }
        dim_key = weakness[:2]
        return suggestions.get(dim_key, "综合优化")
    
    # ─────────────────────────────────────────────────────────
    # 统计分析
    # ─────────────────────────────────────────────────────────
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取评估统计信息
        
        Returns:
            统计信息字典
        """
        if not self.evaluation_history:
            return {"message": "No evaluations yet"}
        
        r_scores = [e["r_score"] for e in self.evaluation_history]
        grades = [e["grade"] for e in self.evaluation_history]
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "r_score_mean": np.mean(r_scores),
            "r_score_std": np.std(r_scores),
            "r_score_min": np.min(r_scores),
            "r_score_max": np.max(r_scores),
            "grade_distribution": {
                "S": grades.count("S"),
                "A": grades.count("A"),
                "B": grades.count("B"),
                "C": grades.count("C"),
                "D": grades.count("D"),
            },
            "dna": FILE_DNA,
        }
    
    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("通心译v2.0 评估统计 | Evaluation Statistics")
        print("=" * 50)
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")


# ═══════════════════════════════════════════════════════════════
# 演示与测试
# ═══════════════════════════════════════════════════════════════

def create_sample_output(sample_id: int) -> TranslationOutput:
    """创建示例翻译输出（用于测试）"""
    
    samples = {
        1: {
            "source": "画龍点睛",
            "literal": "to draw eyes on the dragon painting",
            "logical": "to add the crucial final detail that brings a work to life",
            "intentional": "to add the finishing touch that brings something to life",
            "cultural": "Expresses the transformative power of a precise detail",
            "css": 95,
        },
        2: {
            "source": "龍",
            "literal": "dragon",
            "logical": "Chinese dragon (loong) — auspicious divine creature",
            "intentional": "loong [Chinese dragon — benevolent symbol distinct from Western dragon]",
            "cultural": "Preserve positive Chinese cultural connotation",
            "css": 88,
        },
        3: {
            "source": "因为下雨，所以地面湿了",
            "literal": "Because rain, so ground wet.",
            "logical": "Because it rained, the ground is wet.",
            "intentional": "Because it rained, the ground is wet.",
            "cultural": "Semantic-syntactic constraint demonstration",
            "css": 98,
            "error_flag": "GRAMMAR_CONFLICT: because+so coexistence",
        },
        4: {
            "source": "道可道，非常道",
            "literal": "Way can be spoken, not constant way.",
            "logical": "The Tao that can be told is not the eternal Tao.",
            "intentional": "The Tao that can be spoken of is not the constant Tao. [Dao De Jing]",
            "cultural": "Preserve the philosophical paradox at the heart of Daoism",
            "css": 82,
        },
    }
    
    data = samples.get(sample_id, samples[1])
    
    return TranslationOutput(
        source_text=data["source"],
        literal=LiteralLayer(
            text=data["literal"],
            terminology_mapping=[],
            confidence=0.85,
            error_flag=data.get("error_flag"),
        ),
        logical=LogicalLayer(
            text=data["logical"],
            semantic_entailments=[],
            discourse_structure="",
            confidence=0.88,
        ),
        intentional=IntentionalLayer(
            text=data["intentional"],
            cultural_intention=data["cultural"],
            imagery_mapping=[],
            civilization_safety_score=data["css"],
            confidence=0.85,
        ),
    )


def main():
    """主函数 - 演示评估器用法"""
    print("=" * 60)
    print("通心译 v2.0 七维评估器 | Tongxin Seven-Dimension Evaluator")
    print(f"DNA: {FILE_DNA}")
    print("=" * 60)
    
    # 初始化评估器
    evaluator = TongxinEvaluator()
    
    # 测试样本
    print("\n[1] 运行评估演示...")
    print("-" * 60)
    
    for i in range(1, 5):
        sample = create_sample_output(i)
        result = evaluator.evaluate(sample)
        
        print(f"\n样本 {i}: {result.source_text}")
        print(evaluator.generate_report(result, verbose=False))
    
    # 详细报告示例
    print("\n" + "=" * 60)
    print("[2] 详细报告示例")
    print("-" * 60)
    
    sample = create_sample_output(1)
    result = evaluator.evaluate(sample)
    print(evaluator.generate_report(result, verbose=True))
    
    # 统计信息
    print("\n" + "=" * 60)
    print("[3] 评估统计")
    print("-" * 60)
    evaluator.print_statistics()
    
    # DNA追溯
    print("\n" + "=" * 60)
    print("[4] DNA 追溯")
    print("-" * 60)
    print(f"文件DNA:  {FILE_DNA}")
    print(f"父DNA:    {PARENT_DNA}")
    print(f"确认码:   {CONFIRM_CODE}")
    print(f"封印:     {SEAL}")
    
    print("\n" + "=" * 60)
    print("评估器运行完成 | Evaluator execution completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
