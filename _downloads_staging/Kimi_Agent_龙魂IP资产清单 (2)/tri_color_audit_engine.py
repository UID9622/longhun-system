#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  龍魂·三色审计合规检测引擎 v3.0                                                 ║
║  DNA追溯码: #龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0                            ║
║  功能: 配方/参数/文本的合规性检测、AI幻觉检测、阈值审计体系                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

三色审计标准:
    🟢 通过 (GREEN)  - 合规/安全/通过
    🟡 待审 (YELLOW) - 接近阈值/需人工审核
    🔴 熔断 (RED)    - 超标/危险/验证失败
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import re
import time
import unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, Protocol, Set, Tuple, TypeVar


# ═══════════════════════════════════════════════════════════════
# 1. 三色审计核心枚举与基础数据结构
# ═══════════════════════════════════════════════════════════════

class TriColor(Enum):
    """三色审计标准枚举"""
    GREEN = "green"      # 🟢 通过/合规
    YELLOW = "yellow"    # 🟡 待审/警告
    RED = "red"          # 🔴 熔断/超标

    @property
    def emoji(self) -> str:
        return {TriColor.GREEN: "🟢", TriColor.YELLOW: "🟡", TriColor.RED: "🔴"}[self]

    @property
    def label(self) -> str:
        return {TriColor.GREEN: "通过", TriColor.YELLOW: "待审", TriColor.RED: "熔断"}[self]

    @property
    def hex_color(self) -> str:
        return {TriColor.GREEN: "#22c55e", TriColor.YELLOW: "#eab308", TriColor.RED: "#ef4444"}[self]


class IndustryType(Enum):
    """行业类型"""
    FOOD = "食品"
    CHEMICAL = "化工"
    PHARMA = "制药"
    COSMETICS = "化妆品"
    TEXTILE = "纺织"


class EncryptLevel(Enum):
    """加密强度等级"""
    STRONG = "SM4+SM2"    # 🟢 强加密
    MEDIUM = "SM4"         # 🟡 中等加密
    WEAK = "弱加密"         # 🔴 弱加密
    NONE = "未加密"         # 🔴 未加密


@dataclass
class AuditResult:
    """审计结果数据类"""
    color: TriColor
    category: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    violations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dna_trace: str = ""
    confidence: float = 1.0  # 检测置信度

    def to_dict(self) -> Dict[str, Any]:
        return {
            "color": self.color.value,
            "color_emoji": self.color.emoji,
            "label": self.color.label,
            "category": self.category,
            "message": self.message,
            "details": self.details,
            "violations": self.violations,
            "timestamp": self.timestamp,
            "dna_trace": self.dna_trace,
            "confidence": self.confidence,
        }

    def __str__(self) -> str:
        return f"{self.color.emoji} [{self.category}] {self.message}"


@dataclass
class ThresholdConfig:
    """阈值配置数据类"""
    green_max: float   # 🟢 上限
    yellow_max: float  # 🟡 警告线上限
    unit: str = ""
    description: str = ""

    def check(self, value: float) -> TriColor:
        """检查值落在哪个区间"""
        if value <= self.green_max:
            return TriColor.GREEN
        elif value <= self.yellow_max:
            return TriColor.YELLOW
        else:
            return TriColor.RED


# ═══════════════════════════════════════════════════════════════
# 2. DNA追溯码管理器 (SM2签名 + SM3哈希)
# ═══════════════════════════════════════════════════════════════

class DNAManager:
    """
    DNA追溯码管理器
    - 生成DNA追溯码 (SM3哈希)
    - 验证DNA签名 (SM2签名验证模拟)
    - 验证数据完整性 (哈希对比)
    """

    DNA_PREFIX = "#龍芯⚡️"
    DNA_VERSION = "v3.0"

    def __init__(self):
        self._trace_log: List[Dict[str, Any]] = []

    def generate_trace_id(self, data: Dict[str, Any], source: str = "") -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        # SM3哈希模拟 (使用SHA-256作为SM3的替代，实际部署使用gmssl)
        hash_value = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        trace_id = f"{self.DNA_PREFIX}{timestamp}-{hash_value}-{self.DNA_VERSION}"
        self._trace_log.append({
            "trace_id": trace_id,
            "source": source,
            "timestamp": timestamp,
            "hash": hash_value,
        })
        return trace_id

    def sm3_hash(self, data: bytes) -> str:
        """SM3哈希计算 (模拟)"""
        return hashlib.sha256(data).hexdigest()

    def sm2_sign_verify(self, data: bytes, signature: str, public_key: str) -> bool:
        """SM2签名验证 (模拟实现 - 实际部署使用gmssl库)"""
        # 模拟SM2验签: 使用HMAC作为演示
        expected = hmac.new(
            public_key.encode(), data, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def sm2_sign(self, data: bytes, private_key: str) -> str:
        """SM2签名 (模拟)"""
        return hmac.new(private_key.encode(), data, hashlib.sha256).hexdigest()

    def verify_integrity(self, data: bytes, expected_hash: str) -> bool:
        """验证数据完整性 (SM3哈希对比)"""
        actual_hash = self.sm3_hash(data)
        return hmac.compare_digest(actual_hash.encode(), expected_hash.encode())

    def parse_trace_id(self, trace_id: str) -> Optional[Dict[str, str]]:
        """解析DNA追溯码"""
        pattern = rf"{re.escape(self.DNA_PREFIX)}(.+)-(.+)-(.+)"
        match = re.match(pattern, trace_id)
        if match:
            return {
                "timestamp": match.group(1),
                "hash": match.group(2),
                "version": match.group(3),
            }
        return None

    def get_trace_log(self) -> List[Dict[str, Any]]:
        return self._trace_log.copy()


# ═══════════════════════════════════════════════════════════════
# 3. 抽象检测器基类
# ═══════════════════════════════════════════════════════════════

class BaseDetector(ABC):
    """检测器抽象基类"""

    def __init__(self, name: str, dna_manager: Optional[DNAManager] = None):
        self.name = name
        self.dna = dna_manager or DNAManager()
        self._rules: List[Callable[..., AuditResult]] = []
        self._history: List[AuditResult] = []

    @abstractmethod
    def detect(self, data: Any, **kwargs: Any) -> AuditResult:
        """执行检测 - 子类必须实现"""
        pass

    def add_rule(self, rule: Callable[..., AuditResult]) -> None:
        """动态添加检测规则"""
        self._rules.append(rule)

    def get_history(self) -> List[AuditResult]:
        return self._history.copy()

    def _create_result(
        self,
        color: TriColor,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        violations: Optional[List[str]] = None,
    ) -> AuditResult:
        result = AuditResult(
            color=color,
            category=self.name,
            message=message,
            details=details or {},
            violations=violations or [],
            dna_trace="",
        )
        self._history.append(result)
        return result


# ═══════════════════════════════════════════════════════════════
# 4. 配方合规检测器
# ═══════════════════════════════════════════════════════════════

class FormulaComplianceDetector(BaseDetector):
    """
    配方合规检测器
    检测配方成分是否在安全阈值内
    适用: 食品、化工、制药、化妆品等行业
    """

    # 默认行业阈值配置
    DEFAULT_THRESHOLDS: Dict[IndustryType, Dict[str, ThresholdConfig]] = {
        IndustryType.FOOD: {
            "二氧化硫残留": ThresholdConfig(0.05, 0.1, "g/kg", "GB 2760"),
            "苯甲酸": ThresholdConfig(0.2, 0.5, "g/kg", "GB 2760"),
            "山梨酸": ThresholdConfig(0.5, 1.0, "g/kg", "GB 2760"),
            "铅": ThresholdConfig(0.1, 0.5, "mg/kg", "GB 2762"),
            "砷": ThresholdConfig(0.1, 0.5, "mg/kg", "GB 2762"),
            "镉": ThresholdConfig(0.05, 0.1, "mg/kg", "GB 2762"),
            "糖": ThresholdConfig(50, 100, "g/100g", "营养成分"),
            "钠": ThresholdConfig(600, 2000, "mg/100g", "营养成分"),
            "脂肪": ThresholdConfig(20, 35, "g/100g", "营养成分"),
        },
        IndustryType.CHEMICAL: {
            "苯": ThresholdConfig(0.1, 1.0, "mg/m³", "GBZ 2.1"),
            "甲醛": ThresholdConfig(0.5, 1.0, "mg/m³", "GBZ 2.1"),
            "铅": ThresholdConfig(0.05, 0.1, "mg/L", "GB 5085"),
            "汞": ThresholdConfig(0.005, 0.05, "mg/L", "GB 5085"),
            "六价铬": ThresholdConfig(0.1, 1.5, "mg/L", "GB 5085"),
            "VOC": ThresholdConfig(50, 150, "g/L", "GB 18582"),
        },
        IndustryType.PHARMA: {
            "原料药纯度": ThresholdConfig(99.0, 98.0, "%", "药典"),
            "水分": ThresholdConfig(3.0, 7.0, "%", "药典"),
            "重金属": ThresholdConfig(10, 20, "ppm", "药典"),
            "微生物限度": ThresholdConfig(100, 1000, "CFU/g", "药典"),
        },
        IndustryType.COSMETICS: {
            "汞": ThresholdConfig(0.5, 1.0, "mg/kg", "化妆品安全技术规范"),
            "铅": ThresholdConfig(5, 10, "mg/kg", "化妆品安全技术规范"),
            "砷": ThresholdConfig(1, 2, "mg/kg", "化妆品安全技术规范"),
            "镉": ThresholdConfig(2, 5, "mg/kg", "化妆品安全技术规范"),
            "甲醛": ThresholdConfig(500, 1000, "mg/kg", "化妆品安全技术规范"),
        },
    }

    def __init__(
        self,
        dna_manager: Optional[DNAManager] = None,
        custom_thresholds: Optional[Dict[str, ThresholdConfig]] = None,
    ):
        super().__init__("配方合规检测器", dna_manager)
        self.industry: Optional[IndustryType] = None
        self._custom_thresholds = custom_thresholds or {}
        self._current_thresholds: Dict[str, ThresholdConfig] = {}

    def set_industry(self, industry: IndustryType) -> None:
        """设置行业类型，加载对应阈值"""
        self.industry = industry
        self._current_thresholds = {}
        if industry in self.DEFAULT_THRESHOLDS:
            self._current_thresholds.update(self.DEFAULT_THRESHOLDS[industry])
        self._current_thresholds.update(self._custom_thresholds)

    def set_thresholds(self, thresholds: Dict[str, ThresholdConfig]) -> None:
        """动态设置阈值"""
        self._current_thresholds.update(thresholds)

    def detect(
        self,
        formula_data: Dict[str, float],
        trace_id: str = "",
        **kwargs: Any,
    ) -> AuditResult:
        """
        检测配方合规性

        Args:
            formula_data: {成分名: 含量值} 的字典
            trace_id: DNA追溯码

        Returns:
            AuditResult: 三色审计结果
        """
        if not self._current_thresholds:
            return self._create_result(
                TriColor.RED,
                "未设置行业阈值，无法检测",
                {"error": "请先调用 set_industry() 设置行业类型"},
            )

        violations = []
        details: Dict[str, Any] = {
            "industry": self.industry.value if self.industry else "未知",
            "items_checked": [],
            "trace_id": trace_id,
        }
        colors_found: Set[TriColor] = set()

        for ingredient, value in formula_data.items():
            if ingredient not in self._current_thresholds:
                continue

            threshold = self._current_thresholds[ingredient]
            color = threshold.check(value)
            colors_found.add(color)

            item_result = {
                "ingredient": ingredient,
                "value": value,
                "unit": threshold.unit,
                "threshold_green": threshold.green_max,
                "threshold_yellow": threshold.yellow_max,
                "color": color.value,
                "color_emoji": color.emoji,
                "standard": threshold.description,
            }
            details["items_checked"].append(item_result)

            if color == TriColor.RED:
                violations.append(
                    f"🔴 {ingredient}: {value}{threshold.unit} "
                    f"(超标: 上限 {threshold.yellow_max}{threshold.unit})"
                )
            elif color == TriColor.YELLOW:
                violations.append(
                    f"🟡 {ingredient}: {value}{threshold.unit} "
                    f"(接近上限: {threshold.green_max}{threshold.unit})"
                )

        # 确定总体颜色
        if TriColor.RED in colors_found:
            overall_color = TriColor.RED
            message = f"检测到 {len([v for v in violations if v.startswith('🔴')])} 项超标"
        elif TriColor.YELLOW in colors_found:
            overall_color = TriColor.YELLOW
            message = f"检测到 {len([v for v in violations if v.startswith('🟡')])} 项接近上限，建议人工审核"
        else:
            overall_color = TriColor.GREEN
            message = "所有成分均在安全阈值内，合规"

        result = self._create_result(
            color=overall_color,
            message=message,
            details=details,
            violations=violations,
        )
        result.dna_trace = trace_id
        return result

    def generate_compliance_report(
        self, results: List[AuditResult]
    ) -> Dict[str, Any]:
        """生成综合合规报告"""
        total = len(results)
        green_count = sum(1 for r in results if r.color == TriColor.GREEN)
        yellow_count = sum(1 for r in results if r.color == TriColor.YELLOW)
        red_count = sum(1 for r in results if r.color == TriColor.RED)

        return {
            "total_checked": total,
            "green": green_count,
            "yellow": yellow_count,
            "red": red_count,
            "compliance_rate": green_count / total * 100 if total > 0 else 0,
            "summary": f"🟢{green_count} 🟡{yellow_count} 🔴{red_count}",
            "all_pass": red_count == 0 and yellow_count == 0,
        }


# ═══════════════════════════════════════════════════════════════
# 5. 文本幻觉检测器
# ═══════════════════════════════════════════════════════════════

class TextHallucinationDetector(BaseDetector):
    """
    文本幻觉检测器
    检测AI生成文本的幻觉率、事实一致性、语义密度
    三色标准: <5%🟢 / 5-15%🟡 / >15%🔴
    """

    # 幻觉模式特征词库
    HALLUCINATION_PATTERNS = {
        "fabrication": [
            r"研究表明.*?实际上", r"据统计.*?数据显示",
            r"众所周知.*?事实", r"据专家.*?指出",
        ],
        "uncertainty": [
            r"可能.*?也许", r"大概.*?似乎",
            r"不确定.*?有可能", r"据推测.*?估计",
        ],
        "contradiction": [
            r"但是.*?然而", r"虽然.*?不过",
            r"尽管.*?但是", r"然而.*?另一方面",
        ],
        "vague_reference": [
            r"相关机构", r"有关部门",
            r"某研究机构", r"一些专家",
            r"据报道.*?未指明", r"相关人士",
        ],
        "temporal_hallucination": [
            r"最近.*?年以来", r"近年来.*?数据显示",
            r"据统计.*?202[0-9]", r"截至.*?数据",
        ],
    }

    # 事实核查关键词
    FACT_CHECK_TRIGGERS = [
        "总是", "从不", "所有", "没有任何", "绝对",
        "100%", "完全不可能", "永远", "必然",
    ]

    def __init__(self, dna_manager: Optional[DNAManager] = None):
        super().__init__("文本幻觉检测器", dna_manager)
        self._pattern_weights = {
            "fabrication": 0.25,
            "uncertainty": 0.15,
            "contradiction": 0.20,
            "vague_reference": 0.25,
            "temporal_hallucination": 0.15,
        }
        self._thresholds = {
            "green": 0.05,   # <5%
            "yellow": 0.15,  # <15%
        }

    def detect(
        self,
        text: str,
        reference_facts: Optional[List[str]] = None,
        trace_id: str = "",
        **kwargs: Any,
    ) -> AuditResult:
        """
        检测文本幻觉

        Args:
            text: AI生成的文本
            reference_facts: 参考事实列表（可选）
            trace_id: DNA追溯码

        Returns:
            AuditResult: 三色审计结果
        """
        text_length = len(text)
        sentences = re.split(r'[。！？.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # 1. 幻觉片段检测
        hallucination_segments = []
        pattern_scores: Dict[str, int] = {}

        for pattern_name, patterns in self.HALLUCINATION_PATTERNS.items():
            count = 0
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    count += 1
                    start = max(0, match.start() - 10)
                    end = min(text_length, match.end() + 10)
                    segment = text[start:end]
                    hallucination_segments.append({
                        "segment": segment,
                        "pattern": pattern_name,
                        "position": (match.start(), match.end()),
                    })
            pattern_scores[pattern_name] = count

        # 2. 绝对化表述检测
        absolute_statements = []
        for trigger in self.FACT_CHECK_TRIGGERS:
            if trigger in text:
                absolute_statements.append(trigger)

        # 3. 事实一致性检测 (与参考事实对比)
        fact_consistency = 1.0
        if reference_facts:
            matched_facts = 0
            for fact in reference_facts:
                # 简单的关键词匹配
                fact_keywords = set(fact.split())
                if any(kw in text for kw in fact_keywords):
                    matched_facts += 1
            fact_consistency = matched_facts / len(reference_facts)

        # 4. 语义密度计算
        semantic_density = self._calculate_semantic_density(text)

        # 5. 综合幻觉率计算
        total_weighted_score = sum(
            pattern_scores.get(name, 0) * weight
            for name, weight in self._pattern_weights.items()
        )
        hallucination_rate = min(1.0, total_weighted_score / max(len(sentences), 1))

        # 考虑绝对化表述的加成
        if absolute_statements:
            hallucination_rate = min(1.0, hallucination_rate + 0.03 * len(absolute_statements))

        # 考虑事实一致性的影响
        hallucination_rate = min(1.0, hallucination_rate * (2 - fact_consistency))

        # 6. 三色判定
        if hallucination_rate < self._thresholds["green"]:
            color = TriColor.GREEN
            message = f"幻觉率 {hallucination_rate*100:.1f}% < 5%，文本可信度高"
        elif hallucination_rate < self._thresholds["yellow"]:
            color = TriColor.YELLOW
            message = f"幻觉率 {hallucination_rate*100:.1f}% 在 5%-15%，建议人工审核"
        else:
            color = TriColor.RED
            message = f"幻觉率 {hallucination_rate*100:.1f}% > 15%，存在严重幻觉风险"

        # 7. 构建违规列表
        violations = []
        for seg in hallucination_segments[:10]:  # 最多显示10个
            emoji = {"fabrication": "🔴", "uncertainty": "🟡",
                     "contradiction": "🟡", "vague_reference": "🔴",
                     "temporal_hallucination": "🟡"}[seg["pattern"]]
            violations.append(f"{emoji} [{seg['pattern']}] {seg['segment']}")

        if absolute_statements:
            violations.append(f"🟡 [绝对化表述] 发现 {len(absolute_statements)} 处: {', '.join(absolute_statements[:5])}")

        details = {
            "text_length": text_length,
            "sentence_count": len(sentences),
            "hallucination_rate": round(hallucination_rate, 4),
            "hallucination_rate_percent": f"{hallucination_rate*100:.2f}%",
            "pattern_scores": pattern_scores,
            "absolute_statements": absolute_statements,
            "fact_consistency": round(fact_consistency, 4),
            "semantic_density": round(semantic_density, 4),
            "hallucination_segments": hallucination_segments[:10],
            "trace_id": trace_id,
        }

        result = self._create_result(color, message, details, violations)
        result.dna_trace = trace_id
        result.confidence = 1.0 - hallucination_rate
        return result

    def _calculate_semantic_density(self, text: str) -> float:
        """计算语义密度 (信息含量/总长度)"""
        # 去除停用词后的有效信息比例
        stop_words = set(["的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
                         "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
                         "你", "会", "着", "没有", "看", "好", "自己", "这", "那"])
        words = re.findall(r'\w+', text)
        if not words:
            return 0.0
        meaningful = sum(1 for w in words if w not in stop_words)
        return meaningful / len(words)

    def set_thresholds(self, green: float, yellow: float) -> None:
        """动态设置阈值"""
        self._thresholds["green"] = green
        self._thresholds["yellow"] = yellow


# ═══════════════════════════════════════════════════════════════
# 6. 个人信息保护检测器
# ═══════════════════════════════════════════════════════════════

class PIIProtectionDetector(BaseDetector):
    """
    个人信息保护检测器
    检测个人信息是否被加密保护，加密强度是否达标
    三色: SM4+SM2🟢 / SM4🟡 / 弱加密🔴
    """

    # PII模式检测
    PII_PATTERNS = {
        "phone": r'1[3-9]\d{9}',
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "id_card": r'\d{17}[\dXx]',
        "bank_card": r'\d{16,19}',
        "name": r'[\u4e00-\u9fff]{2,4}',
        "address": r'[\u4e00-\u9fff]+(?:省|市|区|县|路|街|号|室)',
    }

    def __init__(self, dna_manager: Optional[DNAManager] = None):
        super().__init__("个人信息保护检测器", dna_manager)

    def detect(
        self,
        data: Dict[str, Any],
        trace_id: str = "",
        **kwargs: Any,
    ) -> AuditResult:
        """
        检测个人信息保护状态

        Args:
            data: {
                "encryption_level": EncryptLevel 或 str,
                "encrypted_fields": List[str],
                "raw_text": str (可选, 用于检测PII泄露),
                "key_rotation_days": int,
            }
            trace_id: DNA追溯码

        Returns:
            AuditResult
        """
        encryption_level = data.get("encryption_level", EncryptLevel.NONE)
        if isinstance(encryption_level, str):
            encryption_level = self._parse_encrypt_level(encryption_level)

        encrypted_fields = data.get("encrypted_fields", [])
        raw_text = data.get("raw_text", "")
        key_rotation_days = data.get("key_rotation_days", 999)

        violations = []
        details = {
            "encryption_level": encryption_level.value,
            "encrypted_fields": encrypted_fields,
            "key_rotation_days": key_rotation_days,
            "pii_found": [],
            "trace_id": trace_id,
        }

        # 1. 加密强度判定
        if encryption_level == EncryptLevel.STRONG:
            color = TriColor.GREEN
            message = f"加密强度: {encryption_level.value}，符合最高安全标准"
        elif encryption_level == EncryptLevel.MEDIUM:
            color = TriColor.YELLOW
            message = f"加密强度: {encryption_level.value}，建议升级至SM4+SM2"
            violations.append(f"🟡 当前使用 {encryption_level.value} 加密，建议增加SM2签名保护")
        elif encryption_level == EncryptLevel.WEAK:
            color = TriColor.RED
            message = f"加密强度: {encryption_level.value}，存在严重安全隐患"
            violations.append(f"🔴 检测到弱加密 {encryption_level.value}，必须升级")
        else:
            color = TriColor.RED
            message = f"数据未加密，严重违规"
            violations.append(f"🔴 数据未加密，个人信息完全暴露")

        # 2. 检测PII泄露
        if raw_text:
            pii_found = self._detect_pii(raw_text)
            details["pii_found"] = pii_found
            if pii_found:
                for pii_type, matches in pii_found.items():
                    if matches and pii_type not in encrypted_fields:
                        violations.append(
                            f"🔴 检测到未加密的{pii_type}: 发现 {len(matches)} 处"
                        )
                        if color != TriColor.RED:
                            color = TriColor.RED
                            message = "检测到未加密的个人信息，严重违规"

        # 3. 密钥轮换检查
        if key_rotation_days > 90:
            violations.append(f"🟡 密钥已 {key_rotation_days} 天未轮换，建议90天内轮换")
            if color == TriColor.GREEN:
                color = TriColor.YELLOW
                message += "；密钥轮换周期过长"

        result = self._create_result(color, message, details, violations)
        result.dna_trace = trace_id
        return result

    def _parse_encrypt_level(self, level_str: str) -> EncryptLevel:
        """解析加密等级字符串"""
        mapping = {
            "SM4+SM2": EncryptLevel.STRONG,
            "强加密": EncryptLevel.STRONG,
            "SM4": EncryptLevel.MEDIUM,
            "中等加密": EncryptLevel.MEDIUM,
            "DES": EncryptLevel.WEAK,
            "3DES": EncryptLevel.WEAK,
            "RC4": EncryptLevel.WEAK,
            "弱加密": EncryptLevel.WEAK,
            "未加密": EncryptLevel.NONE,
            "NONE": EncryptLevel.NONE,
        }
        return mapping.get(level_str.upper() if level_str else "", EncryptLevel.WEAK)

    def _detect_pii(self, text: str) -> Dict[str, List[str]]:
        """检测文本中的PII信息"""
        found = {}
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                found[pii_type] = matches
        return found


# ═══════════════════════════════════════════════════════════════
# 7. 参数合规检测器
# ═══════════════════════════════════════════════════════════════

class ParameterComplianceDetector(BaseDetector):
    """
    参数合规检测器
    检测企业参数是否符合申报要求
    三色: 完全一致🟢 / 轻微偏差🟡 / 严重不符🔴
    """

    def __init__(self, dna_manager: Optional[DNAManager] = None):
        super().__init__("参数合规检测器", dna_manager)
        self._declared_params: Dict[str, Any] = {}
        self._tolerance_config = {
            "green": 0.0,     # 完全一致
            "yellow": 0.05,   # 5%偏差
            "red": 0.20,      # 20%偏差
        }

    def set_declared_params(self, params: Dict[str, Any]) -> None:
        """设置申报参数"""
        self._declared_params = params

    def set_tolerance(self, green: float, yellow: float, red: float) -> None:
        """设置容差范围"""
        self._tolerance_config = {"green": green, "yellow": yellow, "red": red}

    def detect(
        self,
        actual_params: Dict[str, Any],
        trace_id: str = "",
        **kwargs: Any,
    ) -> AuditResult:
        """
        检测参数合规性

        Args:
            actual_params: 实际参数值
            trace_id: DNA追溯码

        Returns:
            AuditResult
        """
        if not self._declared_params:
            return self._create_result(
                TriColor.RED,
                "未设置申报参数，无法检测",
                {"error": "请先调用 set_declared_params()"},
            )

        violations = []
        details = {
            "declared": self._declared_params,
            "actual": actual_params,
            "comparisons": [],
            "trace_id": trace_id,
        }
        colors_found: Set[TriColor] = set()

        for param_name, declared_value in self._declared_params.items():
            if param_name not in actual_params:
                colors_found.add(TriColor.RED)
                violations.append(f"🔴 参数 '{param_name}' 在实际数据中缺失")
                details["comparisons"].append({
                    "param": param_name,
                    "declared": declared_value,
                    "actual": None,
                    "color": TriColor.RED.value,
                    "deviation": None,
                })
                continue

            actual_value = actual_params[param_name]
            deviation = self._calculate_deviation(declared_value, actual_value)

            if deviation is None:
                # 非数值比较
                if declared_value == actual_value:
                    color = TriColor.GREEN
                else:
                    color = TriColor.RED
                    violations.append(
                        f"🔴 '{param_name}': 申报={declared_value}, 实际={actual_value}"
                    )
            else:
                # 数值偏差比较
                if deviation <= self._tolerance_config["green"]:
                    color = TriColor.GREEN
                elif deviation <= self._tolerance_config["yellow"]:
                    color = TriColor.YELLOW
                    violations.append(
                        f"🟡 '{param_name}': 偏差 {deviation*100:.1f}% "
                        f"(申报={declared_value}, 实际={actual_value})"
                    )
                else:
                    color = TriColor.RED
                    violations.append(
                        f"🔴 '{param_name}': 严重偏差 {deviation*100:.1f}% "
                        f"(申报={declared_value}, 实际={actual_value})"
                    )

            colors_found.add(color)
            details["comparisons"].append({
                "param": param_name,
                "declared": declared_value,
                "actual": actual_value,
                "color": color.value,
                "deviation": deviation,
            })

        # 检查是否有未申报的参数
        for param_name in actual_params:
            if param_name not in self._declared_params:
                violations.append(f"🟡 未申报参数 '{param_name}': {actual_params[param_name]}")
                if TriColor.RED not in colors_found:
                    colors_found.add(TriColor.YELLOW)

        # 总体判定
        if TriColor.RED in colors_found:
            overall_color = TriColor.RED
            message = "检测到参数严重不符申报值"
        elif TriColor.YELLOW in colors_found:
            overall_color = TriColor.YELLOW
            message = "部分参数存在轻微偏差，建议核实"
        else:
            overall_color = TriColor.GREEN
            message = "所有参数与申报值完全一致"

        result = self._create_result(overall_color, message, details, violations)
        result.dna_trace = trace_id
        return result

    def _calculate_deviation(
        self, declared: Any, actual: Any
    ) -> Optional[float]:
        """计算偏差率"""
        try:
            declared_num = float(declared)
            actual_num = float(actual)
            if declared_num == 0:
                return abs(actual_num) if actual_num != 0 else 0.0
            return abs((actual_num - declared_num) / declared_num)
        except (ValueError, TypeError):
            return None


# ═══════════════════════════════════════════════════════════════
# 8. DNA验证器
# ═══════════════════════════════════════════════════════════════

class DNAValidator(BaseDetector):
    """
    DNA追溯码验证器
    - SM2签名验证
    - SM3哈希对比
    - 验证追溯链完整性
    """

    def __init__(self, dna_manager: Optional[DNAManager] = None):
        super().__init__("DNA验证器", dna_manager)
        self._public_keys: Dict[str, str] = {}

    def register_public_key(self, entity_id: str, public_key: str) -> None:
        """注册实体的公钥"""
        self._public_keys[entity_id] = public_key

    def detect(
        self,
        data: Dict[str, Any],
        trace_id: str = "",
        **kwargs: Any,
    ) -> AuditResult:
        """
        验证DNA追溯码

        Args:
            data: {
                "file_content": bytes,      # 加密文件内容
                "dna_trace_id": str,        # DNA追溯码
                "signature": str,           # SM2签名
                "entity_id": str,           # 签发实体ID
                "expected_hash": str,       # 预期的SM3哈希
            }
            trace_id: DNA追溯码

        Returns:
            AuditResult
        """
        file_content = data.get("file_content", b"")
        dna_trace_id = data.get("dna_trace_id", "")
        signature = data.get("signature", "")
        entity_id = data.get("entity_id", "")
        expected_hash = data.get("expected_hash", "")

        violations = []
        checks_passed = []
        checks_failed = []

        # 1. 验证DNA追溯码格式
        trace_info = self.dna.parse_trace_id(dna_trace_id)
        if trace_info:
            checks_passed.append("DNA追溯码格式有效")
        else:
            checks_failed.append("DNA追溯码格式无效")
            violations.append("🔴 DNA追溯码格式解析失败")

        # 2. SM3哈希验证
        if file_content and expected_hash:
            if self.dna.verify_integrity(file_content, expected_hash):
                checks_passed.append("SM3哈希验证通过 - 数据未被篡改")
            else:
                checks_failed.append("SM3哈希验证失败 - 数据可能被篡改")
                violations.append("🔴 SM3哈希不匹配，数据完整性被破坏")
        else:
            checks_failed.append("缺少文件内容或预期哈希值")
            violations.append("🔴 无法执行哈希验证：缺少必要数据")

        # 3. SM2签名验证
        if entity_id in self._public_keys and signature and file_content:
            public_key = self._public_keys[entity_id]
            if self.dna.sm2_sign_verify(file_content, signature, public_key):
                checks_passed.append("SM2签名验证通过")
            else:
                checks_failed.append("SM2签名验证失败")
                violations.append("🔴 SM2签名验证失败，来源不可信")
        elif entity_id not in self._public_keys:
            checks_failed.append(f"未找到实体 '{entity_id}' 的公钥")
            violations.append("🟡 未注册实体的公钥，无法验证签名")

        # 4. 结果判定
        if violations and all(v.startswith("🔴") for v in violations):
            color = TriColor.RED
            message = "DNA验证失败，数据不可信"
        elif violations:
            color = TriColor.YELLOW
            message = "DNA验证部分通过，存在警告项"
        else:
            color = TriColor.GREEN
            message = "DNA验证全部通过，数据可信"

        details = {
            "dna_trace_id": dna_trace_id,
            "trace_info": trace_info,
            "checks_passed": checks_passed,
            "checks_failed": checks_failed,
            "total_checks": len(checks_passed) + len(checks_failed),
            "passed_count": len(checks_passed),
            "failed_count": len(checks_failed),
            "trace_id": trace_id,
        }

        result = self._create_result(color, message, details, violations)
        result.dna_trace = trace_id or dna_trace_id
        return result


# ═══════════════════════════════════════════════════════════════
# 9. 三色审计引擎主类
# ═══════════════════════════════════════════════════════════════

class TriColorAuditEngine:
    """
    龍魂·三色审计合规检测引擎 主类

    统一管理所有检测器，提供统一的检测接口和报告生成
    """

    DNA_TRACE = "#龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0"

    def __init__(self):
        self.dna_manager = DNAManager()
        self.detectors: Dict[str, BaseDetector] = {
            "formula": FormulaComplianceDetector(self.dna_manager),
            "text": TextHallucinationDetector(self.dna_manager),
            "pii": PIIProtectionDetector(self.dna_manager),
            "parameter": ParameterComplianceDetector(self.dna_manager),
            "dna": DNAValidator(self.dna_manager),
        }
        self._audit_log: List[Dict[str, Any]] = []

    def detect_formula(
        self,
        formula_data: Dict[str, float],
        industry: IndustryType,
        trace_id: str = "",
    ) -> AuditResult:
        """配方合规检测"""
        detector = self.detectors["formula"]
        detector.set_industry(industry)
        trace = trace_id or self.dna_manager.generate_trace_id(formula_data, "formula")
        result = detector.detect(formula_data, trace)
        self._log_audit("formula", result)
        return result

    def detect_text(
        self,
        text: str,
        reference_facts: Optional[List[str]] = None,
        trace_id: str = "",
    ) -> AuditResult:
        """文本幻觉检测"""
        detector = self.detectors["text"]
        trace = trace_id or self.dna_manager.generate_trace_id({"text_len": len(text)}, "text")
        result = detector.detect(text, reference_facts, trace)
        self._log_audit("text", result)
        return result

    def detect_pii(
        self,
        data: Dict[str, Any],
        trace_id: str = "",
    ) -> AuditResult:
        """个人信息保护检测"""
        detector = self.detectors["pii"]
        # 创建可序列化的trace数据副本
        trace_data = {k: (v.value if hasattr(v, "value") else v)
                      for k, v in data.items()}
        trace = trace_id or self.dna_manager.generate_trace_id(trace_data, "pii")
        result = detector.detect(data, trace)
        self._log_audit("pii", result)
        return result

    def detect_parameters(
        self,
        actual_params: Dict[str, Any],
        declared_params: Optional[Dict[str, Any]] = None,
        trace_id: str = "",
    ) -> AuditResult:
        """参数合规检测"""
        detector = self.detectors["parameter"]
        if declared_params:
            detector.set_declared_params(declared_params)
        trace = trace_id or self.dna_manager.generate_trace_id(actual_params, "parameter")
        result = detector.detect(actual_params, trace)
        self._log_audit("parameter", result)
        return result

    def verify_dna(
        self,
        data: Dict[str, Any],
        trace_id: str = "",
    ) -> AuditResult:
        """DNA追溯码验证"""
        detector = self.detectors["dna"]
        result = detector.detect(data, trace_id)
        self._log_audit("dna", result)
        return result

    def run_batch(
        self,
        tasks: List[Dict[str, Any]],
    ) -> List[AuditResult]:
        """批量检测"""
        results = []
        for task in tasks:
            task_type = task.get("type", "")
            if task_type == "formula":
                result = self.detect_formula(
                    task["data"], task["industry"], task.get("trace_id", "")
                )
            elif task_type == "text":
                result = self.detect_text(
                    task["data"], task.get("reference_facts"), task.get("trace_id", "")
                )
            elif task_type == "pii":
                result = self.detect_pii(task["data"], task.get("trace_id", ""))
            elif task_type == "parameter":
                result = self.detect_parameters(
                    task["data"], task.get("declared"), task.get("trace_id", "")
                )
            elif task_type == "dna":
                result = self.verify_dna(task["data"], task.get("trace_id", ""))
            else:
                result = AuditResult(
                    TriColor.RED, "未知", f"未知的检测类型: {task_type}"
                )
            results.append(result)
        return results

    def generate_report(self, results: Optional[List[AuditResult]] = None) -> Dict[str, Any]:
        """生成综合审计报告"""
        target_results = results or self._get_all_history()
        summary = {TriColor.GREEN: 0, TriColor.YELLOW: 0, TriColor.RED: 0}
        category_stats: Dict[str, Dict[str, int]] = {}

        for r in target_results:
            summary[r.color] += 1
            cat = r.category
            if cat not in category_stats:
                category_stats[cat] = {"green": 0, "yellow": 0, "red": 0}
            category_stats[cat][r.color.value] += 1

        total = sum(summary.values())
        return {
            "dna_trace": self.DNA_TRACE,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total": total,
                "green": summary[TriColor.GREEN],
                "yellow": summary[TriColor.YELLOW],
                "red": summary[TriColor.RED],
                "pass_rate": summary[TriColor.GREEN] / total * 100 if total > 0 else 0,
            },
            "category_breakdown": category_stats,
            "results": [r.to_dict() for r in target_results],
            "overall_color": (
                TriColor.RED.emoji if summary[TriColor.RED] > 0
                else TriColor.YELLOW.emoji if summary[TriColor.YELLOW] > 0
                else TriColor.GREEN.emoji
            ),
        }

    def export_report(self, filepath: str, results: Optional[List[AuditResult]] = None) -> None:
        """导出报告为JSON"""
        report = self.generate_report(results)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def _log_audit(self, detector_type: str, result: AuditResult) -> None:
        self._audit_log.append({
            "detector": detector_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result.to_dict(),
        })

    def _get_all_history(self) -> List[AuditResult]:
        all_results = []
        for detector in self.detectors.values():
            all_results.extend(detector.get_history())
        return all_results

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self._audit_log.copy()


# ═══════════════════════════════════════════════════════════════
# 10. 单元测试
# ═══════════════════════════════════════════════════════════════

class TestTriColorAuditEngine(unittest.TestCase):
    """三色审计引擎单元测试"""

    def setUp(self):
        self.engine = TriColorAuditEngine()

    # ─── TriColor Enum Tests ───

    def test_tricolor_enum(self):
        self.assertEqual(TriColor.GREEN.emoji, "🟢")
        self.assertEqual(TriColor.YELLOW.label, "待审")
        self.assertEqual(TriColor.RED.hex_color, "#ef4444")

    def test_threshold_config(self):
        tc = ThresholdConfig(10, 20, "mg/kg")
        self.assertEqual(tc.check(5), TriColor.GREEN)
        self.assertEqual(tc.check(15), TriColor.YELLOW)
        self.assertEqual(tc.check(25), TriColor.RED)

    # ─── DNA Manager Tests ───

    def test_dna_generate_and_verify(self):
        dna = DNAManager()
        data = {"test": "value", "num": 123}
        trace_id = dna.generate_trace_id(data, "test")
        self.assertTrue(trace_id.startswith(dna.DNA_PREFIX))
        parsed = dna.parse_trace_id(trace_id)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["version"], "v3.0")

    def test_sm2_sign_and_verify(self):
        dna = DNAManager()
        test_key = "test_sm2_key_123"
        data = b"test data for signing"
        signature = dna.sm2_sign(data, test_key)
        # 使用相同key验证通过
        self.assertTrue(dna.sm2_sign_verify(data, signature, test_key))
        # 篡改数据验证失败
        self.assertFalse(dna.sm2_sign_verify(b"tampered data", signature, test_key))
        # 使用不同key验证失败
        self.assertFalse(dna.sm2_sign_verify(data, signature, "wrong_key"))

    def test_sm3_integrity(self):
        dna = DNAManager()
        data = b"integrity test data"
        hash1 = dna.sm3_hash(data)
        hash2 = dna.sm3_hash(data)
        self.assertEqual(hash1, hash2)
        self.assertTrue(dna.verify_integrity(data, hash1))

    # ─── Formula Detector Tests ───

    def test_formula_compliance_green(self):
        detector = FormulaComplianceDetector()
        detector.set_industry(IndustryType.FOOD)
        formula = {"苯甲酸": 0.1, "山梨酸": 0.3}  # 都在安全范围内
        result = detector.detect(formula)
        self.assertEqual(result.color, TriColor.GREEN)
        self.assertIn("合规", result.message)

    def test_formula_compliance_yellow(self):
        detector = FormulaComplianceDetector()
        detector.set_industry(IndustryType.FOOD)
        formula = {"苯甲酸": 0.3}  # 接近上限 (green_max=0.2)
        result = detector.detect(formula)
        self.assertEqual(result.color, TriColor.YELLOW)

    def test_formula_compliance_red(self):
        detector = FormulaComplianceDetector()
        detector.set_industry(IndustryType.FOOD)
        formula = {"苯甲酸": 0.8}  # 超标
        result = detector.detect(formula)
        self.assertEqual(result.color, TriColor.RED)
        self.assertTrue(len(result.violations) > 0)

    def test_formula_report(self):
        detector = FormulaComplianceDetector()
        detector.set_industry(IndustryType.FOOD)
        results = [
            detector.detect({"苯甲酸": 0.1}),
            detector.detect({"苯甲酸": 0.3}),
            detector.detect({"苯甲酸": 0.8}),
        ]
        report = detector.generate_compliance_report(results)
        self.assertEqual(report["green"], 1)
        self.assertEqual(report["yellow"], 1)
        self.assertEqual(report["red"], 1)

    # ─── Text Hallucination Detector Tests ───

    def test_text_low_hallucination(self):
        detector = TextHallucinationDetector()
        text = "这是一个普通的陈述句，不包含任何可疑内容。所有数据都经过验证。"
        result = detector.detect(text)
        self.assertEqual(result.color, TriColor.GREEN)

    def test_text_high_hallucination(self):
        detector = TextHallucinationDetector()
        text = "据某研究机构统计，相关机构的数据表明100%的人都总是使用该产品的。"
        result = detector.detect(text)
        self.assertEqual(result.color, TriColor.RED)

    def test_text_with_facts(self):
        detector = TextHallucinationDetector()
        text = "这是一个基本正确的描述。"
        facts = ["正确"]
        result = detector.detect(text, facts)
        self.assertEqual(result.color, TriColor.GREEN)

    # ─── PII Detector Tests ───

    def test_pii_strong_encryption(self):
        detector = PIIProtectionDetector()
        data = {
            "encryption_level": EncryptLevel.STRONG,
            "encrypted_fields": ["phone", "email"],
            "raw_text": "",
            "key_rotation_days": 30,
        }
        result = detector.detect(data)
        self.assertEqual(result.color, TriColor.GREEN)

    def test_pii_weak_encryption(self):
        detector = PIIProtectionDetector()
        data = {
            "encryption_level": EncryptLevel.WEAK,
            "encrypted_fields": [],
            "raw_text": "",
            "key_rotation_days": 180,
        }
        result = detector.detect(data)
        self.assertEqual(result.color, TriColor.RED)

    def test_pii_exposure(self):
        detector = PIIProtectionDetector()
        data = {
            "encryption_level": EncryptLevel.STRONG,
            "encrypted_fields": [],
            "raw_text": "用户手机号: 13800138000",
            "key_rotation_days": 30,
        }
        result = detector.detect(data)
        self.assertEqual(result.color, TriColor.RED)
        self.assertTrue(len(result.details["pii_found"]) > 0)

    # ─── Parameter Detector Tests ───

    def test_parameter_green(self):
        detector = ParameterComplianceDetector()
        detector.set_declared_params({"产量": 100, "纯度": 99.5})
        result = detector.detect({"产量": 100, "纯度": 99.5})
        self.assertEqual(result.color, TriColor.GREEN)

    def test_parameter_yellow(self):
        detector = ParameterComplianceDetector()
        detector.set_declared_params({"产量": 100})
        result = detector.detect({"产量": 103})  # 3%偏差
        self.assertEqual(result.color, TriColor.YELLOW)

    def test_parameter_red(self):
        detector = ParameterComplianceDetector()
        detector.set_declared_params({"产量": 100})
        result = detector.detect({"产量": 130})  # 30%偏差
        self.assertEqual(result.color, TriColor.RED)

    # ─── DNA Validator Tests ───

    def test_dna_validator_green(self):
        validator = DNAValidator()
        dna = DNAManager()
        data = b"test file content"
        test_key = "sm2_test_key"
        signature = dna.sm2_sign(data, test_key)
        validator.register_public_key("entity1", test_key)

        result = validator.detect({
            "file_content": data,
            "dna_trace_id": dna.generate_trace_id({"file": "test"}),
            "signature": signature,
            "entity_id": "entity1",
            "expected_hash": dna.sm3_hash(data),
        })
        self.assertEqual(result.color, TriColor.GREEN)

    def test_dna_validator_red(self):
        validator = DNAValidator()
        dna = DNAManager()
        # 提供有效数据和公钥，但签名和哈希不匹配，触发RED
        file_content = b"test data"
        validator.register_public_key("entity2", "key_for_entity2")
        result = validator.detect({
            "file_content": file_content,
            "dna_trace_id": "invalid-trace-id",
            "signature": "wrong_signature",
            "entity_id": "entity2",
            "expected_hash": "wrong_hash",
        })
        self.assertEqual(result.color, TriColor.RED)

    # ─── Engine Integration Tests ───

    def test_engine_formula_detection(self):
        result = self.engine.detect_formula(
            {"苯甲酸": 0.15, "山梨酸": 0.4},
            IndustryType.FOOD,
        )
        self.assertIn(result.color, [TriColor.GREEN, TriColor.YELLOW])

    def test_engine_text_detection(self):
        result = self.engine.detect_text("这是一个测试文本，没有任何问题。")
        self.assertEqual(result.color, TriColor.GREEN)

    def test_engine_batch_detection(self):
        tasks = [
            {"type": "formula", "data": {"苯甲酸": 0.1}, "industry": IndustryType.FOOD},
            {"type": "text", "data": "正常文本。"},
        ]
        results = self.engine.run_batch(tasks)
        self.assertEqual(len(results), 2)

    def test_engine_report(self):
        self.engine.detect_formula({"苯甲酸": 0.1}, IndustryType.FOOD)
        self.engine.detect_text("测试")
        report = self.engine.generate_report()
        self.assertIn("summary", report)
        self.assertIn("dna_trace", report)

    def test_audit_log(self):
        self.engine.detect_formula({"苯甲酸": 0.1}, IndustryType.FOOD)
        log = self.engine.get_audit_log()
        self.assertTrue(len(log) > 0)

    def test_dna_trace_constant(self):
        self.assertEqual(
            TriColorAuditEngine.DNA_TRACE,
            "#龍芯⚡️2026-07-04-TRI-COLOR-AUDIT-v3.0"
        )


# ═══════════════════════════════════════════════════════════════
# 11. 运行入口
# ═══════════════════════════════════════════════════════════════

def run_demo():
    """运行演示"""
    print("=" * 70)
    print("  龍魂·三色审计合规检测引擎 v3.0 演示")
    print(f"  DNA追溯码: {TriColorAuditEngine.DNA_TRACE}")
    print("=" * 70)

    engine = TriColorAuditEngine()

    # 1. 配方检测演示
    print("\n🧪 [1] 食品配方合规检测")
    print("-" * 50)
    formula = {
        "苯甲酸": 0.35,   # 🟡 接近上限
        "山梨酸": 0.8,    # 🟡 接近上限
        "铅": 0.3,        # 🔴 超标
        "糖": 45,         # 🟢 合规
    }
    result = engine.detect_formula(formula, IndustryType.FOOD)
    print(f"  结果: {result}")
    for v in result.violations:
        print(f"    {v}")

    # 2. 文本幻觉检测演示
    print("\n📝 [2] AI文本幻觉检测")
    print("-" * 50)
    ai_text = "相关机构的统计数据表明，所有用户100%满意。据推测也许可能有效。"
    result = engine.detect_text(ai_text)
    print(f"  结果: {result}")
    print(f"  幻觉率: {result.details.get('hallucination_rate_percent', 'N/A')}")
    for v in result.violations[:3]:
        print(f"    {v}")

    # 3. 个人信息保护检测演示
    print("\n🔒 [3] 个人信息保护检测")
    print("-" * 50)
    pii_data = {
        "encryption_level": EncryptLevel.MEDIUM,
        "encrypted_fields": ["email"],
        "raw_text": "用户手机: 13800138000",
        "key_rotation_days": 120,
    }
    result = engine.detect_pii(pii_data)
    print(f"  结果: {result}")
    for v in result.violations:
        print(f"    {v}")

    # 4. 参数合规检测演示
    print("\n📊 [4] 企业参数合规检测")
    print("-" * 50)
    declared = {"年产量": 10000, "纯度": 99.9, "能耗": 500}
    actual = {"年产量": 10050, "纯度": 99.85, "能耗": 650}  # 能耗超标30%
    result = engine.detect_parameters(actual, declared)
    print(f"  结果: {result}")
    for comp in result.details.get("comparisons", []):
        print(f"    {comp['param']}: 申报={comp['declared']} 实际={comp['actual']} "
              f"偏差={comp.get('deviation', 'N/A'):.4f} -> {comp['color']}")

    # 5. DNA验证演示
    print("\n🧬 [5] DNA追溯码验证")
    print("-" * 50)
    dna = DNAManager()
    file_content = b"encrypted formula data"
    # 使用相同的key进行签名和验证 (演示SM2签名验证流程)
    test_key = "dragon_soul_sm2_key_2026"
    signature = dna.sm2_sign(file_content, test_key)
    validator = engine.detectors["dna"]
    validator.register_public_key("factory_A", test_key)

    result = engine.verify_dna({
        "file_content": file_content,
        "dna_trace_id": dna.generate_trace_id({"file": "formula"}),
        "signature": signature,
        "entity_id": "factory_A",
        "expected_hash": dna.sm3_hash(file_content),
    })
    print(f"  结果: {result}")
    for check in result.details.get("checks_passed", []):
        print(f"    ✅ {check}")

    # 综合报告
    print("\n" + "=" * 70)
    print("  综合审计报告")
    print("=" * 70)
    report = engine.generate_report()
    summary = report["summary"]
    print(f"  总检测项: {summary['total']}")
    print(f"  🟢 通过: {summary['green']}")
    print(f"  🟡 待审: {summary['yellow']}")
    print(f"  🔴 熔断: {summary['red']}")
    print(f"  合规率: {summary['pass_rate']:.1f}%")
    print(f"  综合判定: {report['overall_color']}")
    print(f"\n  DNA追溯: {report['dna_trace']}")
    print("=" * 70)


if __name__ == "__main__":
    # 运行单元测试
    print("\n运行单元测试...\n")
    unittest.main(verbosity=2, exit=False)

    # 运行演示
    print("\n")
    run_demo()
