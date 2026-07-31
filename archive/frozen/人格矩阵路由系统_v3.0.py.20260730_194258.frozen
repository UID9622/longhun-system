#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 龍魂体系 · 人格矩阵路由系统 v3.0
 Dragon Soul Persona Matrix Router System v3.0
================================================================================
DNA签名: #龍芯⚡️2026-06-16-PERSONA-ROUTER-v3.0
UID:      UID9622
身份:     龍芯北辰 · 诸葛鑫
确认码:   #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

五大元知: 军事(MIL) · 历史(HIS) · 哲学(PHI) · 经济(ECO) · 政治(POL)
价值优先级: 忠(0.5) > 孝(0.3) > 义(0.2) > 信 > 和

系统架构:
  ┌─────────────────────────────────────────────────────────────┐
  │                 人格矩阵路由系统 v3.0                         │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
  │  │ 情境解析器 │ │ 权重分配器 │ │ 价值校准器 │ │ 约束检查器 │       │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
  │  │ 情报修正器 │ │ 归一化引擎 │ │ 路由生成器 │ │ 审计追踪器 │       │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
  │  │ 反馈校准器 │ │ DNA签名器 │ │ 人格引擎  │ │ 元知基座  │       │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
  └─────────────────────────────────────────────────────────────┘
================================================================================
"""

from __future__ import annotations

import re
import hashlib
import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any, Set
from datetime import datetime
from collections import deque, defaultdict
import json
import math


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 五大元知枚举与基础类定义
# ═══════════════════════════════════════════════════════════════════════════════

class MetaCognition(Enum):
    """五大元知枚举 - 龍魂体系核心维度"""
    MIL = "军事"    # 态势感知 · 资源调配 · 果断执行
    HIS = "历史"    # 周期识别 · 模式匹配 · 经验复用
    PHI = "哲学"    # 本质追问 · 价值排序 · 逻辑推演
    ECO = "经济"    # 成本核算 · ROI · 边际分析
    POL = "政治"    # 利益博弈 · 联盟构建 · 叙事操控

    @property
    def dna_anchor(self) -> str:
        """获取DNA锚定标识"""
        anchors = {
            MetaCognition.MIL: "#MIL⚡️UID9622",
            MetaCognition.HIS: "#HIS⚡️UID9622",
            MetaCognition.PHI: "#PHI⚡️UID9622",
            MetaCognition.ECO: "#ECO⚡️UID9622",
            MetaCognition.POL: "#POL⚡️UID9622",
        }
        return anchors[self]

    @property
    def core_traits(self) -> Tuple[str, ...]:
        """获取核心特质"""
        traits = {
            MetaCognition.MIL: ("态势感知", "资源调配", "果断执行"),
            MetaCognition.HIS: ("周期识别", "模式匹配", "经验复用"),
            MetaCognition.PHI: ("本质追问", "价值排序", "逻辑推演"),
            MetaCognition.ECO: ("成本核算", "ROI分析", "边际分析"),
            MetaCognition.POL: ("利益博弈", "联盟构建", "叙事操控"),
        }
        return traits[self]

    @property
    def activation_conditions(self) -> Tuple[str, ...]:
        """获取激活条件"""
        conditions = {
            MetaCognition.MIL: ("紧急", "竞争", "生存威胁"),
            MetaCognition.HIS: ("战略", "长期", "未知情境"),
            MetaCognition.PHI: ("原则", "伦理", "架构设计"),
            MetaCognition.ECO: ("资源分配", "投资", "效率"),
            MetaCognition.POL: ("协作", "公共", "影响力"),
        }
        return conditions[self]


class ValuePriority(Enum):
    """五大价值优先级 - 龍魂伦理基座"""
    ZHONG = ("忠", 0.50, MetaCognition.MIL, 1.2)   # 忠 → MIL×1.2
    XIAO = ("孝", 0.30, MetaCognition.HIS, 1.1)     # 孝 → HIS×1.1
    YI = ("义", 0.20, MetaCognition.PHI, 1.3)       # 义 → PHI×1.3
    XIN = ("信", 0.15, MetaCognition.ECO, 1.2)      # 信 → ECO×1.2
    HE = ("和", 0.15, MetaCognition.POL, 1.3)       # 和 → POL×1.3

    def __init__(self, cn_name: str, weight: float, meta: MetaCognition, multiplier: float):
        self.cn_name = cn_name
        self.base_weight = weight
        self.target_meta = meta
        self.calibration_multiplier = multiplier

    @classmethod
    def get_calibration_map(cls) -> Dict[MetaCognition, float]:
        """获取价值校准映射表"""
        return {
            v.target_meta: v.calibration_multiplier
            for v in cls
        }


class SituationType(Enum):
    """六种情境类型 - 用于自动路由识别"""
    EMERGENCY = "紧急响应"      # → 军事主导
    ARCHITECTURE = "架构设计"    # → 哲学主导
    RESOURCE = "资源优化"       # → 经济主导
    COLLABORATION = "协作影响"   # → 政治主导
    STRATEGIC = "战略规划"      # → 历史主导
    BALANCED = "均衡模式"       # → 均衡型


class RouteType(Enum):
    """六种决策路由模板类型"""
    MILITARY_DOMINANT = "军事主导型"       # 紧急响应模式
    PHILOSOPHY_DOMINANT = "哲学主导型"      # 架构设计模式
    ECONOMY_DOMINANT = "经济主导型"         # 资源优化模式
    POLITICAL_DOMINANT = "政治主导型"       # 协作影响模式
    HISTORICAL_DOMINANT = "历史主导型"      # 战略规划模式
    BALANCED = "均衡型"                   # 默认模式

    @property
    def primary_meta(self) -> MetaCognition:
        """获取该路由的主导元知"""
        mapping = {
            RouteType.MILITARY_DOMINANT: MetaCognition.MIL,
            RouteType.PHILOSOPHY_DOMINANT: MetaCognition.PHI,
            RouteType.ECONOMY_DOMINANT: MetaCognition.ECO,
            RouteType.POLITICAL_DOMINANT: MetaCognition.POL,
            RouteType.HISTORICAL_DOMINANT: MetaCognition.HIS,
            RouteType.BALANCED: None,
        }
        return mapping[self]


class AuditLevel(Enum):
    """三色审计等级"""
    GREEN = ("🟢", "正常", "系统运行正常，路由决策在预期范围内")
    YELLOW = ("🟡", "警告", "检测到异常模式，建议人工复核")
    RED = ("🔴", "严重", "严重偏离，触发安全保护机制")

    def __init__(self, emoji: str, level: str, description: str):
        self.emoji = emoji
        self.level = level
        self.description = description


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 核心数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MetaProfile:
    """元知画像 - 单个元知的完整状态"""
    meta: MetaCognition
    base_score: float = 0.20          # 基础分数
    calibrated_score: float = 0.20    # 校准后分数
    historical_avg: float = 0.20      # 历史平均值
    confidence: float = 1.0           # 置信度 0-1
    activation_count: int = 0         # 激活次数
    last_activated: Optional[datetime] = None

    def __post_init__(self):
        if self.calibrated_score == 0.20 and self.base_score != 0.20:
            self.calibrated_score = self.base_score

    @property
    def effectiveness(self) -> float:
        """计算效能指数"""
        if self.activation_count == 0:
            return 0.5
        return min(1.0, self.calibrated_score * self.confidence)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meta": self.meta.value,
            "meta_en": self.meta.name,
            "base_score": round(self.base_score, 4),
            "calibrated_score": round(self.calibrated_score, 4),
            "confidence": round(self.confidence, 4),
            "activation_count": self.activation_count,
            "effectiveness": round(self.effectiveness, 4),
        }


@dataclass
class SituationContext:
    """情境上下文 - 用于解析和路由决策"""
    situation_type: SituationType
    description: str
    urgency: float = 0.5           # 紧急度 0-1
    complexity: float = 0.5        # 复杂度 0-1
    ambiguity: float = 0.5         # 模糊度 0-1
    stakeholders: int = 1          # 利益相关方数量
    time_pressure: float = 0.5     # 时间压力 0-1
    resource_scarcity: float = 0.5 # 资源稀缺性 0-1
    keywords: List[str] = field(default_factory=list)
    raw_input: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "situation_type": self.situation_type.value if isinstance(self.situation_type, SituationType) else self.situation_type,
            "description": self.description,
            "urgency": self.urgency,
            "complexity": self.complexity,
            "ambiguity": self.ambiguity,
            "stakeholders": self.stakeholders,
            "time_pressure": self.time_pressure,
            "resource_scarcity": self.resource_scarcity,
            "keywords": self.keywords,
        }


@dataclass
class RouteDecision:
    """路由决策结果"""
    route_type: RouteType
    meta_weights: Dict[MetaCognition, float]
    primary_meta: MetaCognition
    secondary_meta: MetaCognition
    confidence: float
    situation_context: SituationContext
    value_calibration_applied: Dict[str, float]
    audit_level: AuditLevel
    dna_signature: str
    timestamp: datetime = field(default_factory=datetime.now)
    reasoning: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route_type": self.route_type.value,
            "primary_meta": self.primary_meta.name if self.primary_meta else "BALANCED",
            "secondary_meta": self.secondary_meta.name if self.secondary_meta else "BALANCED",
            "confidence": round(self.confidence, 4),
            "audit_level": f"{self.audit_level.emoji} {self.audit_level.level}",
            "dna_signature": self.dna_signature,
            "timestamp": self.timestamp.isoformat(),
            "meta_weights": {k.name: round(v, 4) for k, v in self.meta_weights.items()},
            "value_calibration": self.value_calibration_applied,
            "reasoning": self.reasoning,
        }


@dataclass
class AuditRecord:
    """审计记录"""
    timestamp: datetime
    level: AuditLevel
    module: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"[{self.level.emoji}] {self.timestamp.strftime('%H:%M:%S')} | {self.module} | {self.message}"


@dataclass
class FeedbackRecord:
    """反馈记录 - 用于校准回路"""
    timestamp: datetime
    decision_signature: str
    outcome_score: float           # 实际结果评分 0-1
    expected_score: float          # 预期评分 0-1
    deviation: float               # 偏差
    adjustment_applied: Dict[str, float]


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 情境解析器（自动识别情境类型）
# ═══════════════════════════════════════════════════════════════════════════════

class SituationParser:
    """
    情境解析器 - 龍魂体系第一感知层
    负责解析输入文本/上下文，自动识别情境类型
    """

    # 关键词映射表 - 用于情境识别
    KEYWORD_MAP: Dict[SituationType, List[str]] = {
        SituationType.EMERGENCY: [
            "紧急", "危机", "威胁", "攻击", "防御", "立即", "马上", "危险",
            "失效", "崩溃", "故障", "入侵", "破坏", "抢救", "应急",
            "urgent", "emergency", "crisis", "attack", "defend", "immediate",
            "threat", "danger", "critical", "failure", "crash", "breach"
        ],
        SituationType.ARCHITECTURE: [
            "架构", "设计", "原则", "哲学", "本质", "逻辑", "框架", "系统",
            "结构", "模型", "范式", "伦理", "道德", "价值", "标准",
            "architecture", "design", "principle", "philosophy", "essence",
            "framework", "structure", "paradigm", "ethics", "pattern"
        ],
        SituationType.RESOURCE: [
            "资源", "成本", "预算", "投资", "收益", "ROI", "效率", "优化",
            "价格", "费用", "利润", "亏损", "节约", "配置", "分配",
            "resource", "cost", "budget", "invest", "return", "efficiency",
            "optimize", "price", "profit", "loss", "allocate", "margin"
        ],
        SituationType.COLLABORATION: [
            "协作", "合作", "利益", "联盟", "谈判", "沟通", "共识",
            "团队", "组织", "公关", "影响", "说服", "调解", "共赢",
            "collaborate", "cooperate", "stakeholder", "alliance", "negotiate",
            "consensus", "team", "organization", "influence", "persuade"
        ],
        SituationType.STRATEGIC: [
            "战略", "规划", "长期", "未来", "趋势", "历史", "周期",
            "模式", "经验", "教训", "预测", "布局", "愿景", "使命",
            "strategy", "plan", "long-term", "future", "trend", "cycle",
            "pattern", "lesson", "forecast", "vision", "roadmap"
        ],
    }

    # 情境特征规则 - 用于量化评估
    SITUATION_RULES: Dict[SituationType, Callable[[SituationContext], float]] = {
        SituationType.EMERGENCY: lambda ctx: (
            ctx.urgency * 0.4 + ctx.time_pressure * 0.3 +
            (1 - ctx.resource_scarcity) * 0.2 + min(ctx.stakeholders / 10, 1.0) * 0.1
        ),
        SituationType.ARCHITECTURE: lambda ctx: (
            ctx.complexity * 0.35 + ctx.ambiguity * 0.25 +
            (1 - ctx.urgency) * 0.2 + min(ctx.stakeholders / 5, 1.0) * 0.2
        ),
        SituationType.RESOURCE: lambda ctx: (
            ctx.resource_scarcity * 0.4 + ctx.complexity * 0.2 +
            (1 - ctx.urgency) * 0.2 + min(ctx.stakeholders / 8, 1.0) * 0.2
        ),
        SituationType.COLLABORATION: lambda ctx: (
            min(ctx.stakeholders / 5, 1.0) * 0.4 + (1 - ctx.urgency) * 0.25 +
            ctx.complexity * 0.2 + ctx.ambiguity * 0.15
        ),
        SituationType.STRATEGIC: lambda ctx: (
            (1 - ctx.urgency) * 0.35 + ctx.complexity * 0.25 +
            ctx.ambiguity * 0.2 + (1 - ctx.time_pressure) * 0.2
        ),
    }

    def __init__(self):
        self._parser_stats: Dict[str, int] = defaultdict(int)
        self._last_parsed: Optional[SituationContext] = None

    def parse(self, input_text: str, **context_kwargs) -> SituationContext:
        """
        解析输入文本，识别情境类型

        Args:
            input_text: 待解析的输入文本
            **context_kwargs: 额外的上下文参数

        Returns:
            SituationContext: 解析后的情境上下文
        """
        # 关键词提取
        keywords = self._extract_keywords(input_text)

        # 情境评分
        scores = self._score_situations(input_text, keywords)

        # 确定主导情境
        situation_type = max(scores, key=scores.get)

        # 如果所有分数都低，归为均衡型
        if scores[situation_type] < 0.3:
            situation_type = SituationType.BALANCED

        # 量化参数
        params = self._quantify_params(input_text, situation_type, keywords, scores)
        params.update(context_kwargs)

        context = SituationContext(
            situation_type=situation_type,
            description=input_text[:200],
            keywords=keywords,
            raw_input=input_text,
            **params
        )

        self._last_parsed = context
        self._parser_stats[situation_type.value] += 1

        return context

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        text_lower = text.lower()
        found_keywords = []

        for sit_type, keywords in self.KEYWORD_MAP.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    found_keywords.append(kw)

        return list(set(found_keywords))

    def _score_situations(self, text: str, keywords: List[str]) -> Dict[SituationType, float]:
        """对各种情境类型进行评分"""
        scores = {st: 0.0 for st in SituationType if st != SituationType.BALANCED}
        text_lower = text.lower()

        for sit_type, kw_list in self.KEYWORD_MAP.items():
            score = 0.0
            for kw in kw_list:
                count = text_lower.count(kw.lower())
                # 中文关键词权重更高
                weight = 1.5 if any('\u4e00' <= c <= '\u9fff' for c in kw) else 1.0
                score += count * weight
            scores[sit_type] = min(1.0, score / max(len(kw_list) * 0.3, 1.0))

        return scores

    def _quantify_params(self, text: str, sit_type: SituationType,
                         keywords: List[str], scores: Dict[SituationType, float]) -> Dict[str, float]:
        """量化情境参数"""
        # 基于文本特征计算各项参数
        text_lower = text.lower()

        # 紧急度
        urgency_keywords = ["紧急", "立即", "马上", "urgent", "immediate", "now", "asap"]
        urgency = min(1.0, sum(1 for kw in urgency_keywords if kw in text_lower) * 0.25 + 0.3)

        # 复杂度（文本长度、专业术语密度）
        complexity = min(1.0, len(text) / 500 + len(keywords) * 0.05)

        # 模糊度（不确定性词汇）
        ambiguity_keywords = ["可能", "大概", "不确定", "也许", "或许", "maybe", "perhaps", "uncertain"]
        ambiguity = min(1.0, sum(1 for kw in ambiguity_keywords if kw in text_lower) * 0.2)

        # 利益相关方
        stakeholder_keywords = ["团队", "部门", "公司", "客户", "用户", "合作", "team", "client", "partner"]
        stakeholders = max(1, sum(1 for kw in stakeholder_keywords if kw in text_lower) * 2)

        # 时间压力
        time_keywords = [" deadline", "期限", "截止", "限期", "倒计时", "timeout"]
        time_pressure = min(1.0, sum(1 for kw in time_keywords if kw in text_lower) * 0.3 + urgency * 0.5)

        # 资源稀缺
        resource_keywords = ["预算", "有限", "不足", "缺乏", "紧缺", "limited", "scarce", "budget"]
        resource_scarcity = min(1.0, sum(1 for kw in resource_keywords if kw in text_lower) * 0.25 + 0.2)

        return {
            "urgency": urgency,
            "complexity": complexity,
            "ambiguity": ambiguity,
            "stakeholders": min(stakeholders, 20),
            "time_pressure": time_pressure,
            "resource_scarcity": resource_scarcity,
        }

    @property
    def parse_stats(self) -> Dict[str, int]:
        """获取解析统计"""
        return dict(self._parser_stats)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 权重初分配器
# ═══════════════════════════════════════════════════════════════════════════════

class WeightDistributor:
    """
    权重初分配器 - 龍魂体系资源调配层
    基于情境类型和元知画像进行初始权重分配
    """

    # 基础权重模板 - 6种路由类型的初始权重分布
    BASE_TEMPLATES: Dict[RouteType, Dict[MetaCognition, float]] = {
        RouteType.MILITARY_DOMINANT: {
            MetaCognition.MIL: 0.45,
            MetaCognition.HIS: 0.15,
            MetaCognition.PHI: 0.10,
            MetaCognition.ECO: 0.15,
            MetaCognition.POL: 0.15,
        },
        RouteType.PHILOSOPHY_DOMINANT: {
            MetaCognition.MIL: 0.10,
            MetaCognition.HIS: 0.15,
            MetaCognition.PHI: 0.45,
            MetaCognition.ECO: 0.15,
            MetaCognition.POL: 0.15,
        },
        RouteType.ECONOMY_DOMINANT: {
            MetaCognition.MIL: 0.10,
            MetaCognition.HIS: 0.15,
            MetaCognition.PHI: 0.15,
            MetaCognition.ECO: 0.45,
            MetaCognition.POL: 0.15,
        },
        RouteType.POLITICAL_DOMINANT: {
            MetaCognition.MIL: 0.10,
            MetaCognition.HIS: 0.15,
            MetaCognition.PHI: 0.10,
            MetaCognition.ECO: 0.20,
            MetaCognition.POL: 0.45,
        },
        RouteType.HISTORICAL_DOMINANT: {
            MetaCognition.MIL: 0.15,
            MetaCognition.HIS: 0.45,
            MetaCognition.PHI: 0.15,
            MetaCognition.ECO: 0.10,
            MetaCognition.POL: 0.15,
        },
        RouteType.BALANCED: {
            MetaCognition.MIL: 0.20,
            MetaCognition.HIS: 0.20,
            MetaCognition.PHI: 0.20,
            MetaCognition.ECO: 0.20,
            MetaCognition.POL: 0.20,
        },
    }

    # 情境类型到路由类型的映射
    SITUATION_ROUTE_MAP: Dict[SituationType, RouteType] = {
        SituationType.EMERGENCY: RouteType.MILITARY_DOMINANT,
        SituationType.ARCHITECTURE: RouteType.PHILOSOPHY_DOMINANT,
        SituationType.RESOURCE: RouteType.ECONOMY_DOMINANT,
        SituationType.COLLABORATION: RouteType.POLITICAL_DOMINANT,
        SituationType.STRATEGIC: RouteType.HISTORICAL_DOMINANT,
        SituationType.BALANCED: RouteType.BALANCED,
    }

    def __init__(self, meta_profiles: Optional[Dict[MetaCognition, MetaProfile]] = None):
        self.meta_profiles = meta_profiles or {}
        self._distribution_history: deque = deque(maxlen=100)

    def distribute(self, situation: SituationContext,
                   meta_profiles: Optional[Dict[MetaCognition, MetaProfile]] = None) -> Tuple[RouteType, Dict[MetaCognition, float]]:
        """
        基于情境进行权重初分配

        Returns:
            (路由类型, 元知权重映射)
        """
        profiles = meta_profiles or self.meta_profiles

        # 确定路由类型
        route_type = self.SITUATION_ROUTE_MAP.get(situation.situation_type, RouteType.BALANCED)

        # 获取基础模板
        base_weights = self.BASE_TEMPLATES[route_type].copy()

        # 根据情境参数微调
        adjusted_weights = self._adjust_by_context(base_weights, situation)

        # 根据元知画像调整
        if profiles:
            adjusted_weights = self._adjust_by_profiles(adjusted_weights, profiles)

        self._distribution_history.append({
            "timestamp": datetime.now(),
            "situation": situation.situation_type.value,
            "route": route_type.value,
            "weights": adjusted_weights.copy(),
        })

        return route_type, adjusted_weights

    def _adjust_by_context(self, weights: Dict[MetaCognition, float],
                          situation: SituationContext) -> Dict[MetaCognition, float]:
        """根据情境参数微调权重"""
        adjusted = weights.copy()

        # 紧急度提升MIL权重
        if situation.urgency > 0.7:
            adjusted[MetaCognition.MIL] += 0.05
            adjusted[MetaCognition.PHI] -= 0.025
            adjusted[MetaCognition.HIS] -= 0.025

        # 复杂度提升PHI权重
        if situation.complexity > 0.7:
            adjusted[MetaCognition.PHI] += 0.05
            adjusted[MetaCognition.ECO] -= 0.025
            adjusted[MetaCognition.POL] -= 0.025

        # 资源稀缺提升ECO权重
        if situation.resource_scarcity > 0.7:
            adjusted[MetaCognition.ECO] += 0.05
            adjusted[MetaCognition.MIL] -= 0.025
            adjusted[MetaCognition.POL] -= 0.025

        # 多利益方提升POL权重
        if situation.stakeholders > 5:
            adjusted[MetaCognition.POL] += 0.05
            adjusted[MetaCognition.MIL] -= 0.025
            adjusted[MetaCognition.PHI] -= 0.025

        # 长期规划提升HIS权重
        if situation.urgency < 0.3 and situation.complexity > 0.5:
            adjusted[MetaCognition.HIS] += 0.05
            adjusted[MetaCognition.MIL] -= 0.025
            adjusted[MetaCognition.ECO] -= 0.025

        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}

        return adjusted

    def _adjust_by_profiles(self, weights: Dict[MetaCognition, float],
                           profiles: Dict[MetaCognition, MetaProfile]) -> Dict[MetaCognition, float]:
        """根据元知画像效能调整权重"""
        adjusted = weights.copy()

        for meta, profile in profiles.items():
            if meta in adjusted:
                # 高置信度和效能的元知获得权重加成
                effectiveness_boost = (profile.effectiveness - 0.5) * 0.1
                adjusted[meta] = max(0.05, adjusted[meta] + effectiveness_boost)

        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}

        return adjusted


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 价值校准器（忠孝义信和）
# ═══════════════════════════════════════════════════════════════════════════════

class ValueCalibrator:
    """
    价值校准器 - 龍魂体系伦理校准层
    基于五大价值（忠孝义信和）对元知权重进行伦理校准
    """

    # 价值校准规则
    CALIBRATION_RULES: Dict[str, Tuple[MetaCognition, float]] = {
        "忠": (MetaCognition.MIL, 1.2),   # 忠 → MIL×1.2
        "孝": (MetaCognition.HIS, 1.1),   # 孝 → HIS×1.1
        "义": (MetaCognition.PHI, 1.3),   # 义 → PHI×1.3
        "信": (MetaCognition.ECO, 1.2),   # 信 → ECO×1.2
        "和": (MetaCognition.POL, 1.3),   # 和 → POL×1.3
    }

    # 价值优先级权重
    VALUE_PRIORITY: Dict[str, float] = {
        "忠": 0.50,
        "孝": 0.30,
        "义": 0.20,
        "信": 0.15,
        "和": 0.15,
    }

    def __init__(self, active_values: Optional[List[str]] = None):
        # 默认激活所有价值
        self.active_values = active_values or list(self.VALUE_PRIORITY.keys())
        self._calibration_history: deque = deque(maxlen=100)

    def calibrate(self, weights: Dict[MetaCognition, float],
                  value_override: Optional[Dict[str, float]] = None) -> Tuple[Dict[MetaCognition, float], Dict[str, float]]:
        """
        对权重进行价值校准

        Args:
            weights: 待校准的元知权重
            value_override: 可覆盖默认价值优先级

        Returns:
            (校准后的权重, 应用的校准值)
        """
        calibrated = weights.copy()
        applied_calibration = {}

        # 确定当前使用的价值优先级
        value_priority = value_override or self.VALUE_PRIORITY

        for value_name, (target_meta, multiplier) in self.CALIBRATION_RULES.items():
            if value_name not in self.active_values:
                continue

            priority_weight = value_priority.get(value_name, 0.1)

            # 计算校准系数：优先级越高，校准影响越大
            # 基础校准 = (multiplier - 1) * priority_weight * 2
            calibration_factor = 1.0 + (multiplier - 1.0) * priority_weight * 2

            if target_meta in calibrated:
                old_value = calibrated[target_meta]
                calibrated[target_meta] *= calibration_factor
                applied_calibration[f"{value_name}→{target_meta.name}"] = calibration_factor

        # 归一化
        total = sum(calibrated.values())
        if total > 0:
            calibrated = {k: v / total for k, v in calibrated.items()}

        self._calibration_history.append({
            "timestamp": datetime.now(),
            "input_weights": weights.copy(),
            "output_weights": calibrated.copy(),
            "applied": applied_calibration.copy(),
        })

        return calibrated, applied_calibration

    def set_active_values(self, values: List[str]):
        """设置当前激活的价值维度"""
        valid_values = set(self.CALIBRATION_RULES.keys())
        self.active_values = [v for v in values if v in valid_values]

    def get_value_report(self) -> Dict[str, Any]:
        """获取价值校准报告"""
        return {
            "active_values": self.active_values,
            "calibration_rules": {
                k: {"target": v[0].name, "multiplier": v[1]}
                for k, v in self.CALIBRATION_RULES.items()
            },
            "value_priority": self.VALUE_PRIORITY,
            "history_count": len(self._calibration_history),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 资源约束检查器
# ═══════════════════════════════════════════════════════════════════════════════

class ResourceConstraintChecker:
    """
    资源约束检查器 - 龍魂体系资源边界层
    检查决策是否在可用资源约束范围内
    """

    # 每种路由类型对应的资源需求基线
    RESOURCE_BASELINE: Dict[RouteType, Dict[str, float]] = {
        RouteType.MILITARY_DOMINANT: {
            "compute": 0.8, "time": 0.3, "data": 0.6,
            "human": 0.4, "risk_tolerance": 0.8,
        },
        RouteType.PHILOSOPHY_DOMINANT: {
            "compute": 0.6, "time": 0.8, "data": 0.7,
            "human": 0.3, "risk_tolerance": 0.3,
        },
        RouteType.ECONOMY_DOMINANT: {
            "compute": 0.5, "time": 0.5, "data": 0.8,
            "human": 0.4, "risk_tolerance": 0.4,
        },
        RouteType.POLITICAL_DOMINANT: {
            "compute": 0.4, "time": 0.6, "data": 0.7,
            "human": 0.8, "risk_tolerance": 0.3,
        },
        RouteType.HISTORICAL_DOMINANT: {
            "compute": 0.5, "time": 0.9, "data": 0.9,
            "human": 0.3, "risk_tolerance": 0.2,
        },
        RouteType.BALANCED: {
            "compute": 0.5, "time": 0.5, "data": 0.5,
            "human": 0.5, "risk_tolerance": 0.5,
        },
    }

    def __init__(self, available_resources: Optional[Dict[str, float]] = None):
        # 默认可用资源
        self.available_resources = available_resources or {
            "compute": 1.0, "time": 1.0, "data": 1.0,
            "human": 1.0, "risk_tolerance": 1.0,
        }
        self._violation_count = 0

    def check(self, route_type: RouteType,
              weights: Dict[MetaCognition, float]) -> Tuple[bool, Dict[str, Any]]:
        """
        检查资源约束

        Returns:
            (是否通过, 约束报告)
        """
        baseline = self.RESOURCE_BASELINE.get(route_type, self.RESOURCE_BASELINE[RouteType.BALANCED])

        violations = []
        warnings = []
        resource_score = 1.0

        for resource_type, required in baseline.items():
            available = self.available_resources.get(resource_type, 1.0)
            utilization = required / max(available, 0.01)

            if utilization > 1.0:
                violations.append({
                    "resource": resource_type,
                    "required": required,
                    "available": available,
                    "gap": utilization - 1.0,
                })
                resource_score *= 0.8
            elif utilization > 0.8:
                warnings.append({
                    "resource": resource_type,
                    "utilization": utilization,
                })
                resource_score *= 0.95

        passed = len(violations) == 0

        if not passed:
            self._violation_count += 1

        report = {
            "passed": passed,
            "resource_score": round(resource_score, 4),
            "violations": violations,
            "warnings": warnings,
            "total_violations": self._violation_count,
        }

        return passed, report

    def adjust_for_constraints(self, route_type: RouteType,
                                weights: Dict[MetaCognition, float]) -> Dict[MetaCognition, float]:
        """根据资源约束调整权重"""
        passed, report = self.check(route_type, weights)

        if passed:
            return weights

        adjusted = weights.copy()

        # 如果存在资源不足，降低高消耗元知的权重
        for violation in report["violations"]:
            if violation["resource"] == "compute":
                # 降低MIL和PHI权重（高计算需求）
                adjusted[MetaCognition.MIL] *= 0.95
                adjusted[MetaCognition.PHI] *= 0.95
            elif violation["resource"] == "time":
                # 降低HIS和PHI权重（长时间需求）
                adjusted[MetaCognition.HIS] *= 0.95
                adjusted[MetaCognition.PHI] *= 0.95
            elif violation["resource"] == "human":
                # 降低POL权重（高人力需求）
                adjusted[MetaCognition.POL] *= 0.95

        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}

        return adjusted


# ═══════════════════════════════════════════════════════════════════════════════
# 7. 情报修正器
# ═══════════════════════════════════════════════════════════════════════════════

class IntelligenceCorrector:
    """
    情报修正器 - 龍魂体系情报融合层
    基于实时情报和历史数据对权重进行修正
    """

    def __init__(self, intelligence_buffer_size: int = 50):
        self.intelligence_buffer: deque = deque(maxlen=intelligence_buffer_size)
        self.meta_effectiveness_history: Dict[MetaCognition, deque] = {
            meta: deque(maxlen=20) for meta in MetaCognition
        }
        self._correction_stats = {"total_corrections": 0, "avg_magnitude": 0.0}

    def add_intelligence(self, source: str, intel_type: str,
                        content: Dict[str, Any], confidence: float = 0.5):
        """添加情报到缓冲区"""
        self.intelligence_buffer.append({
            "timestamp": datetime.now(),
            "source": source,
            "type": intel_type,
            "content": content,
            "confidence": confidence,
        })

    def correct(self, weights: Dict[MetaCognition, float],
                situation: SituationContext) -> Tuple[Dict[MetaCognition, float], Dict[str, Any]]:
        """
        基于情报对权重进行修正

        Returns:
            (修正后的权重, 修正报告)
        """
        corrected = weights.copy()
        correction_details = {}

        # 分析近期情报趋势
        intel_summary = self._summarize_intelligence()

        # 基于情报调整权重
        for meta in MetaCognition:
            meta_intel = intel_summary.get(meta.name, {})
            if meta_intel:
                trend = meta_intel.get("trend", 0.0)
                confidence = meta_intel.get("confidence", 0.5)

                # 趋势修正
                correction = trend * confidence * 0.1
                if meta in corrected:
                    old_value = corrected[meta]
                    corrected[meta] = max(0.05, min(0.8, corrected[meta] + correction))
                    correction_details[meta.name] = {
                        "old": round(old_value, 4),
                        "new": round(corrected[meta], 4),
                        "correction": round(correction, 4),
                        "trend": round(trend, 4),
                    }

        # 基于历史效能修正
        for meta in MetaCognition:
            history = self.meta_effectiveness_history[meta]
            if len(history) >= 5:
                recent_avg = sum(list(history)[-5:]) / 5
                if recent_avg < 0.3:
                    # 效能低下，降低权重
                    corrected[meta] *= 0.95
                    correction_details.setdefault(meta.name, {}).update(
                        {"efficiency_penalty": 0.95}
                    )
                elif recent_avg > 0.8:
                    # 效能优秀，提升权重
                    corrected[meta] *= 1.05
                    correction_details.setdefault(meta.name, {}).update(
                        {"efficiency_bonus": 1.05}
                    )

        # 归一化
        total = sum(corrected.values())
        if total > 0:
            corrected = {k: v / total for k, v in corrected.items()}

        # 统计
        magnitude = sum(abs(correction_details.get(m.name, {}).get("correction", 0))
                       for m in MetaCognition) / max(len(correction_details), 1)
        self._correction_stats["total_corrections"] += 1
        self._correction_stats["avg_magnitude"] = (
            (self._correction_stats["avg_magnitude"] * (self._correction_stats["total_corrections"] - 1) + magnitude)
            / self._correction_stats["total_corrections"]
        )

        return corrected, {
            "details": correction_details,
            "intelligence_count": len(self.intelligence_buffer),
            "magnitude": round(magnitude, 4),
        }

    def _summarize_intelligence(self) -> Dict[str, Dict[str, float]]:
        """汇总情报趋势"""
        summary = defaultdict(lambda: {"trend": 0.0, "confidence": 0.0, "count": 0})

        for intel in self.intelligence_buffer:
            content = intel.get("content", {})
            for meta_name, score in content.items():
                if isinstance(score, (int, float)):
                    summary[meta_name]["trend"] += score
                    summary[meta_name]["confidence"] += intel.get("confidence", 0.5)
                    summary[meta_name]["count"] += 1

        # 平均化
        for meta_name in summary:
            count = summary[meta_name]["count"]
            if count > 0:
                summary[meta_name]["trend"] /= count
                summary[meta_name]["confidence"] /= count

        return dict(summary)

    def record_outcome(self, meta: MetaCognition, effectiveness: float):
        """记录元知应用效果"""
        self.meta_effectiveness_history[meta].append(effectiveness)


# ═══════════════════════════════════════════════════════════════════════════════
# 8. 归一化引擎
# ═══════════════════════════════════════════════════════════════════════════════

class NormalizationEngine:
    """
    归一化引擎 - 龍魂体系标准化层
    对元知权重进行多策略归一化
    """

    class Strategy(Enum):
        SOFTMAX = "softmax"
        LINEAR = "linear"
        POWER = "power"
        ENTROPY_BALANCED = "entropy_balanced"

    def __init__(self, strategy: Strategy = Strategy.ENTROPY_BALANCED,
                 temperature: float = 1.0):
        self.strategy = strategy
        self.temperature = temperature
        self._normalization_count = 0

    def normalize(self, weights: Dict[MetaCognition, float],
                  target_entropy: Optional[float] = None) -> Dict[MetaCognition, float]:
        """
        归一化权重

        Args:
            weights: 待归一化的权重
            target_entropy: 目标熵值（用于熵平衡策略）

        Returns:
            归一化后的权重
        """
        if not weights:
            return {meta: 0.20 for meta in MetaCognition}

        # 确保所有元知都有权重
        complete_weights = {meta: weights.get(meta, 0.01) for meta in MetaCognition}

        if self.strategy == self.Strategy.SOFTMAX:
            result = self._softmax_normalize(complete_weights)
        elif self.strategy == self.Strategy.LINEAR:
            result = self._linear_normalize(complete_weights)
        elif self.strategy == self.Strategy.POWER:
            result = self._power_normalize(complete_weights)
        elif self.strategy == self.Strategy.ENTROPY_BALANCED:
            result = self._entropy_balanced_normalize(complete_weights, target_entropy)
        else:
            result = self._linear_normalize(complete_weights)

        self._normalization_count += 1
        return result

    def _softmax_normalize(self, weights: Dict[MetaCognition, float]) -> Dict[MetaCognition, float]:
        """Softmax归一化"""
        values = list(weights.values())
        max_val = max(values)

        # 数值稳定性处理
        exp_values = [math.exp((v - max_val) / self.temperature) for v in values]
        sum_exp = sum(exp_values)

        if sum_exp == 0:
            return {meta: 0.20 for meta in MetaCognition}

        keys = list(weights.keys())
        return {keys[i]: exp_values[i] / sum_exp for i in range(len(keys))}

    def _linear_normalize(self, weights: Dict[MetaCognition, float]) -> Dict[MetaCognition, float]:
        """线性归一化"""
        total = sum(weights.values())
        if total == 0:
            return {meta: 0.20 for meta in MetaCognition}
        return {k: v / total for k, v in weights.items()}

    def _power_normalize(self, weights: Dict[MetaCognition, float]) -> Dict[MetaCognition, float]:
        """幂归一化 - 增强高权重，抑制低权重"""
        powered = {k: v ** (1 / self.temperature) for k, v in weights.items()}
        total = sum(powered.values())
        if total == 0:
            return {meta: 0.20 for meta in MetaCognition}
        return {k: v / total for k, v in powered.items()}

    def _entropy_balanced_normalize(self, weights: Dict[MetaCognition, float],
                                    target_entropy: Optional[float] = None) -> Dict[MetaCognition, float]:
        """
        熵平衡归一化 - 保持一定多样性
        避免某个元知权重过高，保持系统灵活性
        """
        # 先线性归一化
        linear = self._linear_normalize(weights)

        # 目标熵：默认ln(5)/2 ≈ 0.805（5个等概率选项的一半熵）
        target = target_entropy or math.log(5) / 2

        # 计算当前熵
        current_entropy = -sum(v * math.log(max(v, 1e-10)) for v in linear.values())

        if current_entropy < target:
            # 熵太低（太集中），需要增加多样性
            # 向均匀分布混合
            uniform = {meta: 0.20 for meta in MetaCognition}
            mix_ratio = min(0.3, (target - current_entropy) / math.log(5))
            balanced = {
                meta: linear[meta] * (1 - mix_ratio) + uniform[meta] * mix_ratio
                for meta in MetaCognition
            }
            return self._linear_normalize(balanced)

        return linear

    def calculate_entropy(self, weights: Dict[MetaCognition, float]) -> float:
        """计算权重的信息熵"""
        return -sum(v * math.log(max(v, 1e-10)) for v in weights.values() if v > 0)





# ═══════════════════════════════════════════════════════════════════════════════
# 9. 路由生成器（6种决策路由模板）
# ═══════════════════════════════════════════════════════════════════════════════

class RouteGenerator:
    """
    路由生成器 - 龍魂体系决策输出层
    基于6种模板生成决策路由
    """

    # 路由模板定义
    TEMPLATES: Dict[RouteType, Dict[str, Any]] = {
        RouteType.MILITARY_DOMINANT: {
            "name": "军事主导型 · 紧急响应模式",
            "description": "以军事元知为主导，快速响应紧急情境",
            "decision_pattern": "感知→评估→执行→反馈",
            "time_horizon": "短期",
            "risk_profile": "高风险容忍",
            "primary_meta": MetaCognition.MIL,
            "traits": ["快速决策", "果断执行", "资源集中", "目标导向"],
            "activation_threshold": 0.35,
        },
        RouteType.PHILOSOPHY_DOMINANT: {
            "name": "哲学主导型 · 架构设计模式",
            "description": "以哲学元知为主导，深度思考架构和原则",
            "decision_pattern": "追问→分析→推演→验证",
            "time_horizon": "中长期",
            "risk_profile": "低风险容忍",
            "primary_meta": MetaCognition.PHI,
            "traits": ["本质思考", "逻辑严密", "价值排序", "系统思维"],
            "activation_threshold": 0.30,
        },
        RouteType.ECONOMY_DOMINANT: {
            "name": "经济主导型 · 资源优化模式",
            "description": "以经济元知为主导，优化资源配置和效率",
            "decision_pattern": "评估→比较→优化→监控",
            "time_horizon": "中短期",
            "risk_profile": "中等风险容忍",
            "primary_meta": MetaCognition.ECO,
            "traits": ["成本意识", "ROI导向", "边际分析", "效率优先"],
            "activation_threshold": 0.30,
        },
        RouteType.POLITICAL_DOMINANT: {
            "name": "政治主导型 · 协作影响模式",
            "description": "以政治元知为主导，构建联盟和影响叙事",
            "decision_pattern": "识别→联盟→协商→共识",
            "time_horizon": "中长期",
            "risk_profile": "中等风险容忍",
            "primary_meta": MetaCognition.POL,
            "traits": ["利益平衡", "联盟构建", "叙事操控", "关系管理"],
            "activation_threshold": 0.30,
        },
        RouteType.HISTORICAL_DOMINANT: {
            "name": "历史主导型 · 战略规划模式",
            "description": "以历史元知为主导，基于周期和模式进行战略规划",
            "decision_pattern": "回溯→匹配→推演→布局",
            "time_horizon": "长期",
            "risk_profile": "低风险容忍",
            "primary_meta": MetaCognition.HIS,
            "traits": ["周期识别", "模式匹配", "经验复用", "前瞻布局"],
            "activation_threshold": 0.30,
        },
        RouteType.BALANCED: {
            "name": "均衡型 · 默认模式",
            "description": "五大元知均衡发挥，适用于一般性情境",
            "decision_pattern": "感知→分析→协商→决策",
            "time_horizon": "灵活",
            "risk_profile": "均衡",
            "primary_meta": None,
            "traits": ["多维平衡", "灵活适应", "综合考量", "动态调整"],
            "activation_threshold": 0.20,
        },
    }

    def __init__(self):
        self._route_history: deque = deque(maxlen=100)
        self._template_stats: Dict[RouteType, int] = {rt: 0 for rt in RouteType}

    def generate(self, route_type: RouteType,
                 weights: Dict[MetaCognition, float],
                 situation: SituationContext,
                 confidence: float = 0.5) -> Dict[str, Any]:
        """
        生成路由决策详情

        Returns:
            完整的路由决策信息
        """
        template = self.TEMPLATES[route_type]

        # 确定主次元知
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        primary_meta = sorted_weights[0][0]
        secondary_meta = sorted_weights[1][0] if len(sorted_weights) > 1 else sorted_weights[0][0]

        # 构建决策路径
        decision_path = self._build_decision_path(route_type, weights, situation)

        route = {
            "route_type": route_type.value,
            "route_type_enum": route_type.name,
            "template": template,
            "meta_weights": {k.name: round(v, 4) for k, v in weights.items()},
            "primary_meta": primary_meta.name,
            "secondary_meta": secondary_meta.name,
            "confidence": round(confidence, 4),
            "decision_path": decision_path,
            "recommended_actions": self._generate_actions(route_type, situation),
            "risk_assessment": self._assess_risk(route_type, weights, situation),
            "timestamp": datetime.now().isoformat(),
        }

        self._route_history.append(route)
        self._template_stats[route_type] += 1

        return route

    def _build_decision_path(self, route_type: RouteType,
                             weights: Dict[MetaCognition, float],
                             situation: SituationContext) -> List[Dict[str, str]]:
        """构建决策路径"""
        paths = {
            RouteType.MILITARY_DOMINANT: [
                {"step": "1", "phase": "态势感知", "meta": "MIL", "action": "快速评估威胁等级"},
                {"step": "2", "phase": "资源评估", "meta": "ECO", "action": "盘点可用资源"},
                {"step": "3", "phase": "果断决策", "meta": "MIL", "action": "制定应急方案"},
                {"step": "4", "phase": "执行监控", "meta": "MIL", "action": "执行并追踪效果"},
            ],
            RouteType.PHILOSOPHY_DOMINANT: [
                {"step": "1", "phase": "本质追问", "meta": "PHI", "action": "深入分析根本问题"},
                {"step": "2", "phase": "价值排序", "meta": "PHI", "action": "明确优先级和原则"},
                {"step": "3", "phase": "逻辑推演", "meta": "PHI", "action": "构建逻辑框架"},
                {"step": "4", "phase": "架构验证", "meta": "HIS", "action": "历史模式验证"},
            ],
            RouteType.ECONOMY_DOMINANT: [
                {"step": "1", "phase": "成本评估", "meta": "ECO", "action": "全面成本核算"},
                {"step": "2", "phase": "ROI分析", "meta": "ECO", "action": "投资回报计算"},
                {"step": "3", "phase": "边际优化", "meta": "ECO", "action": "寻找最优配置点"},
                {"step": "4", "phase": "效率监控", "meta": "ECO", "action": "持续效率追踪"},
            ],
            RouteType.POLITICAL_DOMINANT: [
                {"step": "1", "phase": "利益识别", "meta": "POL", "action": "梳理利益格局"},
                {"step": "2", "phase": "联盟构建", "meta": "POL", "action": "寻找合作伙伴"},
                {"step": "3", "phase": "协商谈判", "meta": "POL", "action": "达成共识方案"},
                {"step": "4", "phase": "叙事推动", "meta": "POL", "action": "推动方案落地"},
            ],
            RouteType.HISTORICAL_DOMINANT: [
                {"step": "1", "phase": "历史回溯", "meta": "HIS", "action": "检索相似历史情境"},
                {"step": "2", "phase": "模式匹配", "meta": "HIS", "action": "识别周期性模式"},
                {"step": "3", "phase": "经验复用", "meta": "HIS", "action": "提取历史经验"},
                {"step": "4", "phase": "前瞻布局", "meta": "HIS", "action": "制定长期规划"},
            ],
            RouteType.BALANCED: [
                {"step": "1", "phase": "多维感知", "meta": "ALL", "action": "全面收集信息"},
                {"step": "2", "phase": "综合分析", "meta": "ALL", "action": "多维度评估"},
                {"step": "3", "phase": "协商平衡", "meta": "POL", "action": "寻找平衡点"},
                {"step": "4", "phase": "动态决策", "meta": "ALL", "action": "灵活调整执行"},
            ],
        }
        return paths.get(route_type, paths[RouteType.BALANCED])

    def _generate_actions(self, route_type: RouteType,
                          situation: SituationContext) -> List[str]:
        """生成推荐行动"""
        actions_map = {
            RouteType.MILITARY_DOMINANT: [
                "立即启动应急响应机制",
                "集中关键资源到核心任务",
                "建立快速反馈回路",
                "设定明确的执行时间节点",
            ],
            RouteType.PHILOSOPHY_DOMINANT: [
                "深入分析问题的本质和根因",
                "明确核心原则和约束条件",
                "构建系统性的分析框架",
                "进行多轮逻辑验证",
            ],
            RouteType.ECONOMY_DOMINANT: [
                "开展全面的成本效益分析",
                "评估多种方案的ROI",
                "优化资源配置方案",
                "建立效率和效果监控指标",
            ],
            RouteType.POLITICAL_DOMINANT: [
                "梳理所有利益相关方诉求",
                "识别潜在的联盟和阻力",
                "设计共赢方案",
                "准备有说服力的叙事材料",
            ],
            RouteType.HISTORICAL_DOMINANT: [
                "研究相似历史情境和结果",
                "识别当前所处的周期阶段",
                "借鉴成功和失败的经验",
                "制定分阶段的长期规划",
            ],
            RouteType.BALANCED: [
                "全面收集各方面信息",
                "综合评估多种因素",
                "寻求多方共识",
                "保持灵活的调整空间",
            ],
        }
        return actions_map.get(route_type, actions_map[RouteType.BALANCED])

    def _assess_risk(self, route_type: RouteType,
                     weights: Dict[MetaCognition, float],
                     situation: SituationContext) -> Dict[str, Any]:
        """风险评估"""
        # 集中度风险（单一元知权重过高）
        max_weight = max(weights.values())
        concentration_risk = max_weight ** 2  # 赫芬达尔指数简化版

        # 情境风险
        situation_risk = (situation.urgency * 0.3 + situation.complexity * 0.3 +
                         situation.ambiguity * 0.4)

        # 路由类型风险系数
        route_risk_factor = {
            RouteType.MILITARY_DOMINANT: 0.7,
            RouteType.PHILOSOPHY_DOMINANT: 0.3,
            RouteType.ECONOMY_DOMINANT: 0.5,
            RouteType.POLITICAL_DOMINANT: 0.5,
            RouteType.HISTORICAL_DOMINANT: 0.3,
            RouteType.BALANCED: 0.4,
        }

        total_risk = (concentration_risk * 0.3 + situation_risk * 0.4 +
                     route_risk_factor.get(route_type, 0.5) * 0.3)

        risk_level = "低风险"
        if total_risk > 0.7:
            risk_level = "高风险"
        elif total_risk > 0.4:
            risk_level = "中等风险"

        return {
            "total_risk": round(total_risk, 4),
            "risk_level": risk_level,
            "concentration_risk": round(concentration_risk, 4),
            "situation_risk": round(situation_risk, 4),
            "route_risk": route_risk_factor.get(route_type, 0.5),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 10. 三色审计接口（🟢🟡🔴）
# ═══════════════════════════════════════════════════════════════════════════════

class TriColorAuditor:
    """
    三色审计器 - 龍魂体系质量监督层
    🟢 正常 | 🟡 警告 | 🔴 严重
    """

    # 审计阈值
    THRESHOLDS = {
        "weight_deviation": {"yellow": 0.15, "red": 0.30},
        "confidence": {"yellow": 0.60, "red": 0.40},
        "entropy": {"yellow": 0.50, "red": 0.30},
        "risk_score": {"yellow": 0.60, "red": 0.80},
        "consecutive_same_route": {"yellow": 5, "red": 10},
    }

    def __init__(self):
        self.audit_log: deque = deque(maxlen=200)
        self.route_sequence: deque = deque(maxlen=50)
        self._audit_counts = {"🟢": 0, "🟡": 0, "🔴": 0}

    def audit(self, decision: RouteDecision) -> AuditLevel:
        """
        对路由决策进行审计

        Returns:
            AuditLevel: 审计等级
        """
        findings = []
        score = 0  # 0=正常, 1=警告, 2=严重

        # 1. 检查权重偏差
        weights = decision.meta_weights
        max_weight = max(weights.values())
        min_weight = min(weights.values())
        deviation = max_weight - min_weight

        if deviation > self.THRESHOLDS["weight_deviation"]["red"]:
            findings.append(f"权重偏差过大: {deviation:.2f} (主导: {decision.primary_meta.name})")
            score = max(score, 2)
        elif deviation > self.THRESHOLDS["weight_deviation"]["yellow"]:
            findings.append(f"权重偏差需注意: {deviation:.2f}")
            score = max(score, 1)

        # 2. 检查置信度
        if decision.confidence < self.THRESHOLDS["confidence"]["red"]:
            findings.append(f"置信度过低: {decision.confidence:.2f}")
            score = max(score, 2)
        elif decision.confidence < self.THRESHOLDS["confidence"]["yellow"]:
            findings.append(f"置信度偏低: {decision.confidence:.2f}")
            score = max(score, 1)

        # 3. 检查熵值（多样性）
        entropy = -sum(w * math.log(max(w, 1e-10)) for w in weights.values())
        if entropy < self.THRESHOLDS["entropy"]["red"]:
            findings.append(f"决策多样性严重不足: 熵={entropy:.3f}")
            score = max(score, 2)
        elif entropy < self.THRESHOLDS["entropy"]["yellow"]:
            findings.append(f"决策多样性偏低: 熵={entropy:.3f}")
            score = max(score, 1)

        # 4. 检查路由序列单调性
        self.route_sequence.append(decision.route_type)
        consecutive = self._count_consecutive_same()
        if consecutive >= self.THRESHOLDS["consecutive_same_route"]["red"]:
            findings.append(f"连续{consecutive}次相同路由，可能陷入模式固化")
            score = max(score, 2)
        elif consecutive >= self.THRESHOLDS["consecutive_same_route"]["yellow"]:
            findings.append(f"连续{consecutive}次相同路由，建议引入多样性")
            score = max(score, 1)

        # 确定审计等级
        if score == 2:
            level = AuditLevel.RED
        elif score == 1:
            level = AuditLevel.YELLOW
        else:
            level = AuditLevel.GREEN

        self._audit_counts[level.emoji] += 1

        # 记录审计
        record = AuditRecord(
            timestamp=datetime.now(),
            level=level,
            module="TriColorAuditor",
            message="; ".join(findings) if findings else "系统运行正常",
            details={
                "deviation": round(deviation, 4),
                "confidence": round(decision.confidence, 4),
                "entropy": round(entropy, 4),
                "consecutive_same": consecutive,
                "score": score,
            }
        )
        self.audit_log.append(record)

        return level

    def audit_with_report(self, decision: RouteDecision) -> Tuple[AuditLevel, Dict[str, Any]]:
        """审计并生成详细报告"""
        level = self.audit(decision)

        report = {
            "audit_level": f"{level.emoji} {level.level}",
            "level_description": level.description,
            "timestamp": datetime.now().isoformat(),
            "audit_counts": self._audit_counts.copy(),
            "recent_log": [str(r) for r in list(self.audit_log)[-10:]],
        }

        return level, report

    def _count_consecutive_same(self) -> int:
        """统计连续相同路由的次数"""
        if not self.route_sequence:
            return 0
        last = self.route_sequence[-1]
        count = 0
        for rt in reversed(self.route_sequence):
            if rt == last:
                count += 1
            else:
                break
        return count

    def get_audit_summary(self) -> Dict[str, Any]:
        """获取审计汇总"""
        total = sum(self._audit_counts.values())
        if total == 0:
            total = 1
        return {
            "total_audits": total,
            "green_count": self._audit_counts["🟢"],
            "yellow_count": self._audit_counts["🟡"],
            "red_count": self._audit_counts["🔴"],
            "green_ratio": round(self._audit_counts["🟢"] / total, 4),
            "yellow_ratio": round(self._audit_counts["🟡"] / total, 4),
            "red_ratio": round(self._audit_counts["🔴"] / total, 4),
            "health_status": "健康" if self._audit_counts["🔴"] == 0 else
                           "需关注" if self._audit_counts["🔴"] / total < 0.1 else "告警",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 11. DNA签名生成器
# ═══════════════════════════════════════════════════════════════════════════════

class DNASignatureGenerator:
    """
    DNA签名生成器 - 龍魂体系身份认证层
    为每个决策生成唯一的DNA签名
    """

    # 系统标识
    SYSTEM_ID = "UID9622"
    SYSTEM_NAME = "龍芯北辰"
    SYSTEM_ALIAS = "诸葛鑫"

    def __init__(self):
        self._signature_count = 0

    def generate(self, decision: RouteDecision,
                 module: str = "PERSONA-ROUTER",
                 version: str = "v3.0") -> str:
        """
        生成DNA签名

        格式: #龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}-{UID}-{哈希}
        """
        self._signature_count += 1
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H%M%S")

        # 构建签名基础数据
        sig_data = {
            "uid": self.SYSTEM_ID,
            "date": date_str,
            "time": time_str,
            "module": module,
            "version": version,
            "route": decision.route_type.name,
            "primary": decision.primary_meta.name if decision.primary_meta else "BAL",
            "seq": self._signature_count,
        }

        # 生成哈希
        hash_input = f"{self.SYSTEM_ID}{date_str}{time_str}{decision.route_type.name}{random.random()}"
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:8].upper()

        # 组合签名
        signature = (
            f"#龍芯⚡️{date_str}-{module}-{version} "
            f"#{self.SYSTEM_ID}·{self.SYSTEM_NAME}·{self.SYSTEM_ALIAS} "
            f"#ROUTE:{decision.route_type.name} "
            f"#META:{decision.primary_meta.name if decision.primary_meta else 'BALANCED'} "
            f"#{hash_digest}"
        )

        return signature

    def generate_confirm_code(self, decision: RouteDecision) -> str:
        """生成确认码"""
        hash_input = (
            f"CONFIRM{self.SYSTEM_ID}{decision.route_type.name}"
            f"{decision.primary_meta.name if decision.primary_meta else 'BAL'}"
            f"{datetime.now().isoformat()}"
        )
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:12].upper()
        return f"#CONFIRM🌌{self.SYSTEM_ID}-ONLY-ONCE🧬{hash_digest}"

    def generate_meta_anchor(self, meta: MetaCognition) -> str:
        """生成元知DNA锚定"""
        return meta.dna_anchor

    def get_system_identity(self) -> Dict[str, str]:
        """获取系统身份信息"""
        return {
            "uid": self.SYSTEM_ID,
            "name": self.SYSTEM_NAME,
            "alias": self.SYSTEM_ALIAS,
            "full_identity": f"{self.SYSTEM_ID} · {self.SYSTEM_NAME} · {self.SYSTEM_ALIAS}",
            "version": "v3.0",
            "signature_count": str(self._signature_count),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 12. 反馈回路校准器
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackCalibrator:
    """
    反馈回路校准器 - 龍魂体系进化层
    基于实际结果反馈持续校准系统参数
    """

    def __init__(self, learning_rate: float = 0.1,
                 calibration_decay: float = 0.95):
        self.learning_rate = learning_rate
        self.calibration_decay = calibration_decay
        self.feedback_history: deque = deque(maxlen=100)
        self.meta_calibration_bias: Dict[MetaCognition, float] = {
            meta: 0.0 for meta in MetaCognition
        }
        self.value_calibration_bias: Dict[str, float] = {
            "忠": 0.0, "孝": 0.0, "义": 0.0, "信": 0.0, "和": 0.0
        }
        self._total_feedback = 0
        self._avg_outcome = 0.5

    def add_feedback(self, decision: RouteDecision, outcome_score: float,
                    notes: str = "") -> Dict[str, Any]:
        """
        添加反馈并执行校准

        Args:
            decision: 原始决策
            outcome_score: 实际结果评分 0-1
            notes: 备注

        Returns:
            校准报告
        """
        expected = decision.confidence
        deviation = outcome_score - expected

        feedback = FeedbackRecord(
            timestamp=datetime.now(),
            decision_signature=decision.dna_signature,
            outcome_score=outcome_score,
            expected_score=expected,
            deviation=deviation,
            adjustment_applied={},
        )

        # 应用校准
        adjustments = self._apply_calibration(decision, deviation, outcome_score)
        feedback.adjustment_applied = adjustments

        self.feedback_history.append(feedback)
        self._total_feedback += 1

        # 更新平均结果
        self._avg_outcome = (
            (self._avg_outcome * (self._total_feedback - 1) + outcome_score)
            / self._total_feedback
        )

        return {
            "deviation": round(deviation, 4),
            "adjustments": adjustments,
            "meta_bias": {k.name: round(v, 4) for k, v in self.meta_calibration_bias.items()},
            "value_bias": self.value_calibration_bias.copy(),
            "avg_outcome": round(self._avg_outcome, 4),
            "total_feedback": self._total_feedback,
        }

    def _apply_calibration(self, decision: RouteDecision,
                          deviation: float, outcome_score: float) -> Dict[str, float]:
        """应用校准调整"""
        adjustments = {}

        # 调整主导元知的偏差
        primary = decision.primary_meta
        if primary and abs(deviation) > 0.1:
            adjustment = self.learning_rate * deviation
            self.meta_calibration_bias[primary] += adjustment
            adjustments[f"meta_{primary.name}"] = round(adjustment, 4)

            # 衰减其他元知的偏差
            for meta in MetaCognition:
                if meta != primary:
                    self.meta_calibration_bias[meta] *= self.calibration_decay

        # 如果结果很差，调整价值校准
        if outcome_score < 0.3:
            # 降低当前激活价值的权重
            for value, applied in decision.value_calibration_applied.items():
                value_name = value.split("→")[0] if "→" in value else value
                if value_name in self.value_calibration_bias:
                    penalty = -self.learning_rate * 0.5
                    self.value_calibration_bias[value_name] += penalty
                    adjustments[f"value_{value_name}"] = round(penalty, 4)

        return adjustments

    def get_calibration_state(self) -> Dict[str, Any]:
        """获取当前校准状态"""
        return {
            "meta_bias": {k.name: round(v, 4) for k, v in self.meta_calibration_bias.items()},
            "value_bias": self.value_calibration_bias.copy(),
            "learning_rate": self.learning_rate,
            "decay": self.calibration_decay,
            "total_feedback": self._total_feedback,
            "avg_outcome": round(self._avg_outcome, 4),
            "recent_deviation": (
                round(list(self.feedback_history)[-1].deviation, 4)
                if self.feedback_history else 0
            ),
        }

    def apply_bias_to_weights(self, weights: Dict[MetaCognition, float]) -> Dict[MetaCognition, float]:
        """将偏差应用到权重"""
        adjusted = weights.copy()

        for meta, bias in self.meta_calibration_bias.items():
            if meta in adjusted and abs(bias) > 0.01:
                adjusted[meta] *= (1 + bias)

        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: max(0.01, v / total) for k, v in adjusted.items()}

        return adjusted


# ═══════════════════════════════════════════════════════════════════════════════
# 13. 主人格矩阵引擎（整合层）
# ═══════════════════════════════════════════════════════════════════════════════

class PersonaMatrixEngine:
    """
    主人格矩阵引擎 - 龍魂体系核心控制器
    整合所有子系统，执行7步叠加算法
    """

    # 7步叠加算法步骤
    ALGORITHM_STEPS = [
        "情境解析",
        "权重初分配",
        "价值校准",
        "资源约束",
        "情报修正",
        "归一化",
        "路由生成",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化主人格矩阵引擎

        Args:
            config: 可选的配置字典
        """
        self.config = config or {}
        self._init_time = datetime.now()

        # 初始化五大元知画像
        self.meta_profiles: Dict[MetaCognition, MetaProfile] = {
            meta: MetaProfile(meta=meta, base_score=0.20)
            for meta in MetaCognition
        }

        # 初始化所有子系统
        self.situation_parser = SituationParser()
        self.weight_distributor = WeightDistributor(self.meta_profiles)
        self.value_calibrator = ValueCalibrator(
            active_values=self.config.get("active_values", ["忠", "孝", "义", "信", "和"])
        )
        self.constraint_checker = ResourceConstraintChecker(
            available_resources=self.config.get("resources")
        )
        self.intelligence_corrector = IntelligenceCorrector(
            intelligence_buffer_size=self.config.get("intel_buffer_size", 50)
        )
        self.normalization_engine = NormalizationEngine(
            strategy=NormalizationEngine.Strategy.ENTROPY_BALANCED,
            temperature=self.config.get("temperature", 1.0)
        )
        self.route_generator = RouteGenerator()
        self.auditor = TriColorAuditor()
        self.dna_generator = DNASignatureGenerator()
        self.feedback_calibrator = FeedbackCalibrator(
            learning_rate=self.config.get("learning_rate", 0.1),
            calibration_decay=self.config.get("calibration_decay", 0.95)
        )

        # 状态追踪
        self._execution_count = 0
        self._step_execution_log: deque = deque(maxlen=100)
        self._decision_history: deque = deque(maxlen=200)

    def process(self, input_text: str, **kwargs) -> RouteDecision:
        """
        主处理流程 - 7步叠加算法

        Args:
            input_text: 输入文本/指令
            **kwargs: 额外参数
                - situation_override: 强制指定情境类型
                - route_override: 强制指定路由类型
                - value_override: 覆盖价值优先级
                - bypass_audit: 是否跳过审计

        Returns:
            RouteDecision: 路由决策结果
        """
        self._execution_count += 1
        step_log = {"sequence": self._execution_count, "steps": {}}

        # ═══════════════════════════════════════════════════════════
        # 步骤1: 情境解析
        # ═══════════════════════════════════════════════════════════
        situation_override = kwargs.get("situation_override")
        if situation_override and isinstance(situation_override, SituationType):
            situation = SituationContext(
                situation_type=situation_override,
                description=input_text[:200],
                raw_input=input_text,
            )
        else:
            situation = self.situation_parser.parse(input_text)

        step_log["steps"]["1_situation"] = {
            "type": situation.situation_type.value if isinstance(situation.situation_type, SituationType) else str(situation.situation_type),
            "urgency": round(situation.urgency, 3),
            "complexity": round(situation.complexity, 3),
        }

        # ═══════════════════════════════════════════════════════════
        # 步骤2: 权重初分配
        # ═══════════════════════════════════════════════════════════
        route_override = kwargs.get("route_override")
        if route_override and isinstance(route_override, RouteType):
            base_weights = RouteGenerator.TEMPLATES[route_override]
            route_type = route_override
            weights = {
                MetaCognition.MIL: base_weights.get("primary_meta") == MetaCognition.MIL and 0.45 or 0.15,
                MetaCognition.HIS: base_weights.get("primary_meta") == MetaCognition.HIS and 0.45 or 0.15,
                MetaCognition.PHI: base_weights.get("primary_meta") == MetaCognition.PHI and 0.45 or 0.15,
                MetaCognition.ECO: base_weights.get("primary_meta") == MetaCognition.ECO and 0.45 or 0.15,
                MetaCognition.POL: base_weights.get("primary_meta") == MetaCognition.POL and 0.45 or 0.15,
            }
            # 重新映射均衡型
            if route_type == RouteType.BALANCED:
                weights = {meta: 0.20 for meta in MetaCognition}
            else:
                # 正确设置主导元知权重
                weights = RouteGenerator.TEMPLATES[route_type]  # This needs fixing
                # Actually use proper template weights
                weights = self.weight_distributor.BASE_TEMPLATES[route_type].copy()
        else:
            route_type, weights = self.weight_distributor.distribute(situation, self.meta_profiles)

        step_log["steps"]["2_weights"] = {k.name: round(v, 4) for k, v in weights.items()}

        # ═══════════════════════════════════════════════════════════
        # 步骤3: 价值校准（忠孝义信和）
        # ═══════════════════════════════════════════════════════════
        value_override = kwargs.get("value_override")
        weights, calibration_applied = self.value_calibrator.calibrate(weights, value_override)

        step_log["steps"]["3_calibration"] = calibration_applied

        # ═══════════════════════════════════════════════════════════
        # 步骤4: 资源约束
        # ═══════════════════════════════════════════════════════════
        weights = self.constraint_checker.adjust_for_constraints(route_type, weights)
        passed, constraint_report = self.constraint_checker.check(route_type, weights)

        step_log["steps"]["4_constraint"] = {
            "passed": passed,
            "resource_score": constraint_report.get("resource_score", 1.0),
        }

        # ═══════════════════════════════════════════════════════════
        # 步骤5: 情报修正
        # ═══════════════════════════════════════════════════════════
        weights, correction_report = self.intelligence_corrector.correct(weights, situation)

        step_log["steps"]["5_intelligence"] = {
            "correction_magnitude": correction_report.get("magnitude", 0),
            "intel_count": correction_report.get("intelligence_count", 0),
        }

        # ═══════════════════════════════════════════════════════════
        # 步骤6: 归一化
        # ═══════════════════════════════════════════════════════════
        weights = self.normalization_engine.normalize(weights)
        final_entropy = self.normalization_engine.calculate_entropy(weights)

        step_log["steps"]["6_normalize"] = {
            "entropy": round(final_entropy, 4),
            "final_weights": {k.name: round(v, 4) for k, v in weights.items()},
        }

        # ═══════════════════════════════════════════════════════════
        # 确定主次元知
        # ═══════════════════════════════════════════════════════════
        sorted_meta = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        primary_meta = sorted_meta[0][0]
        secondary_meta = sorted_meta[1][0]

        # ═══════════════════════════════════════════════════════════
        # 步骤7: 路由生成
        # ═══════════════════════════════════════════════════════════
        # 计算置信度
        confidence = self._calculate_confidence(weights, situation, calibration_applied)

        # 生成路由详情
        route_details = self.route_generator.generate(
            route_type, weights, situation, confidence
        )

        step_log["steps"]["7_route"] = {
            "route_type": route_type.value,
            "confidence": round(confidence, 4),
        }

        # ═══════════════════════════════════════════════════════════
        # 生成DNA签名
        # ═══════════════════════════════════════════════════════════
        dna_signature = self.dna_generator.generate(
            RouteDecision(
                route_type=route_type,
                meta_weights=weights,
                primary_meta=primary_meta,
                secondary_meta=secondary_meta,
                confidence=confidence,
                situation_context=situation,
                value_calibration_applied=calibration_applied,
                audit_level=AuditLevel.GREEN,
                dna_signature="",
            )
        )

        # ═══════════════════════════════════════════════════════════
        # 构建决策结果
        # ═══════════════════════════════════════════════════════════
        decision = RouteDecision(
            route_type=route_type,
            meta_weights=weights,
            primary_meta=primary_meta,
            secondary_meta=secondary_meta,
            confidence=confidence,
            situation_context=situation,
            value_calibration_applied=calibration_applied,
            audit_level=AuditLevel.GREEN,  # 临时，后面会更新
            dna_signature=dna_signature,
            timestamp=datetime.now(),
            reasoning=self._generate_reasoning(route_type, primary_meta, weights, situation),
        )

        # ═══════════════════════════════════════════════════════════
        # 三色审计
        # ═══════════════════════════════════════════════════════════
        if not kwargs.get("bypass_audit", False):
            audit_level, audit_report = self.auditor.audit_with_report(decision)
            decision.audit_level = audit_level
            step_log["audit"] = audit_report

        # ═══════════════════════════════════════════════════════════
        # 更新元知画像
        # ═══════════════════════════════════════════════════════════
        self._update_meta_profiles(decision)

        # ═══════════════════════════════════════════════════════════
        # 记录执行日志
        # ═══════════════════════════════════════════════════════════
        self._step_execution_log.append(step_log)
        self._decision_history.append(decision)

        return decision

    def _calculate_confidence(self, weights: Dict[MetaCognition, float],
                             situation: SituationContext,
                             calibration_applied: Dict[str, float]) -> float:
        """计算决策置信度"""
        # 基于权重集中度
        max_weight = max(weights.values())
        weight_confidence = max_weight  # 主导元知权重越高越有信心

        # 基于情境清晰度
        clarity = 1.0 - situation.ambiguity

        # 基于校准一致性
        calibration_consistency = 1.0 - min(len(calibration_applied) * 0.1, 0.3)

        # 综合置信度
        confidence = (weight_confidence * 0.4 + clarity * 0.35 +
                     calibration_consistency * 0.25)

        return min(1.0, max(0.1, confidence))

    def _generate_reasoning(self, route_type: RouteType,
                           primary_meta: MetaCognition,
                           weights: Dict[MetaCognition, float],
                           situation: SituationContext) -> str:
        """生成决策推理说明"""
        meta_weights_str = ", ".join(
            f"{meta.name}={weight:.2f}" for meta, weight in
            sorted(weights.items(), key=lambda x: x[1], reverse=True)
        )

        reasoning = (
            f"基于情境解析[{situation.situation_type.value}]，"
            f"系统选择{route_type.value}，"
            f"主导元知为{primary_meta.value}({primary_meta.name})。"
            f"最终权重分布: {meta_weights_str}。"
            f"紧急度={situation.urgency:.2f}, "
            f"复杂度={situation.complexity:.2f}。"
        )

        return reasoning

    def _update_meta_profiles(self, decision: RouteDecision):
        """更新元知画像"""
        for meta, weight in decision.meta_weights.items():
            profile = self.meta_profiles[meta]
            profile.activation_count += 1
            profile.last_activated = datetime.now()
            # 更新历史平均值
            n = profile.activation_count
            profile.historical_avg = (profile.historical_avg * (n - 1) + weight) / n
            profile.calibrated_score = weight
            profile.confidence = decision.confidence

    def provide_feedback(self, decision_signature: str, outcome_score: float,
                        notes: str = "") -> Optional[Dict[str, Any]]:
        """
        提供反馈以校准系统

        Args:
            decision_signature: 决策签名
            outcome_score: 结果评分 0-1
            notes: 备注

        Returns:
            校准报告
        """
        # 查找对应的决策
        decision = None
        for d in self._decision_history:
            if d.dna_signature == decision_signature:
                decision = d
                break

        if decision is None:
            # 使用最近的决策
            if self._decision_history:
                decision = self._decision_history[-1]
            else:
                return None

        return self.feedback_calibrator.add_feedback(decision, outcome_score, notes)

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "system_identity": self.dna_generator.get_system_identity(),
            "init_time": self._init_time.isoformat(),
            "execution_count": self._execution_count,
            "meta_profiles": {k.name: v.to_dict() for k, v in self.meta_profiles.items()},
            "audit_summary": self.auditor.get_audit_summary(),
            "feedback_state": self.feedback_calibrator.get_calibration_state(),
            "value_calibrator_state": self.value_calibrator.get_value_report(),
            "recent_decisions": len(self._decision_history),
        }

    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取决策历史"""
        return [d.to_dict() for d in list(self._decision_history)[-limit:]]

    def get_meta_profile_report(self) -> Dict[str, Any]:
        """获取元知画像报告"""
        return {
            "profiles": {k.name: v.to_dict() for k, v in self.meta_profiles.items()},
            "dominant_meta": max(self.meta_profiles.items(), key=lambda x: x[1].calibrated_score)[0].name,
            "most_active": max(self.meta_profiles.items(), key=lambda x: x[1].activation_count)[0].name,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 14. 示例用例与系统演示
# ═══════════════════════════════════════════════════════════════════════════════

def demo_military_scenario():
    """演示：军事主导型 - 紧急响应场景"""
    print("\n" + "=" * 70)
    print(" 🎖️ 演示1: 军事主导型 - 紧急响应场景")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "系统遭受不明攻击，核心服务响应延迟超过阈值，"
        "需要立即启动应急响应，隔离受影响的节点，恢复服务正常运行。"
        "攻击源可能来自多个IP地址，情况紧急。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"⭐ 主导元知: {decision.primary_meta.value} ({decision.primary_meta.name})")
    print(f"⭐ 次要元知: {decision.secondary_meta.value} ({decision.secondary_meta.name})")
    print(f"📊 置信度: {decision.confidence:.4f}")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🔬 DNA签名: {decision.dna_signature[:80]}...")
    print(f"🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_philosophy_scenario():
    """演示：哲学主导型 - 架构设计场景"""
    print("\n" + "=" * 70)
    print(" 📐 演示2: 哲学主导型 - 架构设计场景")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "需要重新设计系统的核心架构，明确各模块的职责边界和交互协议。"
        "要从第一性原理出发，理清系统的本质需求，建立清晰的逻辑层次。"
        "设计应遵循单一职责原则和开闭原则，确保系统的可扩展性和可维护性。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"⭐ 主导元知: {decision.primary_meta.value} ({decision.primary_meta.name})")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_economy_scenario():
    """演示：经济主导型 - 资源优化场景"""
    print("\n" + "=" * 70)
    print(" 💰 演示3: 经济主导型 - 资源优化场景")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "本季度预算有限，需要在多个项目之间进行资源分配。"
        "项目A预期ROI为150%，项目B为80%，项目C为200%但风险较高。"
        "需要优化资源配置，在预算约束下最大化整体回报。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"⭐ 主导元知: {decision.primary_meta.value} ({decision.primary_meta.name})")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_political_scenario():
    """演示：政治主导型 - 协作影响场景"""
    print("\n" + "=" * 70)
    print(" 🤝 演示4: 政治主导型 - 协作影响场景")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "需要协调技术团队、产品团队和业务团队三方合作推进新功能上线。"
        "各方对优先级有不同看法，需要通过协商达成共识，"
        "构建联盟推动项目顺利进行，同时平衡各方利益。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"⭐ 主导元知: {decision.primary_meta.value} ({decision.primary_meta.name})")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_historical_scenario():
    """演示：历史主导型 - 战略规划场景"""
    print("\n" + "=" * 70)
    print(" 📜 演示5: 历史主导型 - 战略规划场景")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "回顾过去三年的市场周期变化，分析行业趋势和发展规律。"
        "基于历史数据预测未来一年的发展方向，"
        "制定长期战略规划，布局下一个增长周期。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"⭐ 主导元知: {decision.primary_meta.value} ({decision.primary_meta.name})")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_balanced_scenario():
    """演示：均衡型 - 默认模式"""
    print("\n" + "=" * 70)
    print(" ⚖️ 演示6: 均衡型 - 默认模式")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    input_text = (
        "今天的日常任务安排，需要处理一些常规的工作事项。"
        "没有特别紧急的事情，按照正常流程推进即可。"
    )

    decision = engine.process(input_text)

    print(f"\n📋 输入: {input_text[:60]}...")
    print(f"\n🎯 情境类型: {decision.situation_context.situation_type.value}")
    print(f"🧭 路由类型: {decision.route_type.value}")
    print(f"\n📐 元知权重分布:")
    for meta, weight in sorted(decision.meta_weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 40)
        print(f"   {meta.name} ({meta.value}): {weight:.4f} {bar}")
    print(f"\n🎨 审计状态: {decision.audit_level.emoji} {decision.audit_level.level}")

    return engine, decision


def demo_feedback_calibration():
    """演示：反馈回路校准"""
    print("\n" + "=" * 70)
    print(" 🔄 演示7: 反馈回路校准机制")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    # 执行一系列决策
    scenarios = [
        "紧急安全漏洞需要立即修补",
        "系统架构需要重新设计",
        "预算分配需要优化",
        "团队间需要协调合作",
        "制定长期技术路线图",
    ]

    print("\n📋 执行5次决策...")
    decisions = []
    for i, text in enumerate(scenarios):
        decision = engine.process(text)
        decisions.append(decision)
        print(f"   决策{i+1}: {decision.route_type.value} | "
              f"主导: {decision.primary_meta.name} | "
              f"置信度: {decision.confidence:.3f}")

    # 提供反馈
    print("\n📝 提供反馈校准...")
    for i, decision in enumerate(decisions):
        # 模拟不同的结果
        outcome = [0.9, 0.4, 0.8, 0.3, 0.7][i]
        report = engine.provide_feedback(decision.dna_signature, outcome)
        if report:
            print(f"   反馈{i+1}: 结果={outcome:.1f}, 偏差={report['deviation']:+.3f}")

    # 查看校准状态
    state = engine.feedback_calibrator.get_calibration_state()
    print(f"\n📊 校准状态:")
    print(f"   总反馈次数: {state['total_feedback']}")
    print(f"   平均结果: {state['avg_outcome']:.4f}")
    print(f"   元知偏差: {state['meta_bias']}")

    return engine


def demo_full_system_report():
    """演示：完整系统报告"""
    print("\n" + "=" * 70)
    print(" 📊 演示8: 完整系统报告")
    print("=" * 70)

    engine = PersonaMatrixEngine()

    # 执行多种场景
    scenarios = [
        ("紧急安全漏洞需要立即修补！", SituationType.EMERGENCY),
        ("重新设计核心架构，明确模块职责", SituationType.ARCHITECTURE),
        ("优化预算分配，提高投资回报率", SituationType.RESOURCE),
        ("协调多方合作，达成共识方案", SituationType.COLLABORATION),
        ("分析历史趋势，制定长期战略", SituationType.STRATEGIC),
        ("日常任务安排", SituationType.BALANCED),
    ]

    for text, sit_type in scenarios:
        engine.process(text, situation_override=sit_type)

    # 系统状态
    status = engine.get_system_status()
    print("\n🏛️ 系统身份信息:")
    for k, v in status["system_identity"].items():
        print(f"   {k}: {v}")

    print(f"\n📈 执行统计:")
    print(f"   总执行次数: {status['execution_count']}")

    print(f"\n🧠 元知画像:")
    for meta_name, profile in status["meta_profiles"].items():
        print(f"   {meta_name}: 激活{profile['activation_count']}次, "
              f"历史均值={profile['historical_avg']:.4f}")

    print(f"\n🎨 审计汇总:")
    audit = status["audit_summary"]
    print(f"   总计: {audit['total_audits']}")
    print(f"   🟢 正常: {audit['green_count']} ({audit['green_ratio']*100:.1f}%)")
    print(f"   🟡 警告: {audit['yellow_count']} ({audit['yellow_ratio']*100:.1f}%)")
    print(f"   🔴 严重: {audit['red_count']} ({audit['red_ratio']*100:.1f}%)")
    print(f"   健康状态: {audit['health_status']}")

    print(f"\n🔄 反馈校准:")
    fb = status["feedback_state"]
    print(f"   总反馈: {fb['total_feedback']}")
    print(f"   平均结果: {fb['avg_outcome']:.4f}")

    return engine


# ═══════════════════════════════════════════════════════════════════════════════
# 15. 主入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print(" 🐉 龍魂体系 · 人格矩阵路由系统 v3.0 启动")
    print("=" * 70)
    print(f"系统: UID9622 · 龍芯北辰 · 诸葛鑫")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"五大元知: 军事(MIL) · 历史(HIS) · 哲学(PHI) · 经济(ECO) · 政治(POL)")
    print(f"价值优先级: 忠(0.5) > 孝(0.3) > 义(0.2) > 信(0.15) > 和(0.15)")
    print("=" * 70)

    # 运行所有演示
    demo_military_scenario()
    demo_philosophy_scenario()
    demo_economy_scenario()
    demo_political_scenario()
    demo_historical_scenario()
    demo_balanced_scenario()
    demo_feedback_calibration()
    demo_full_system_report()

    print("\n" + "=" * 70)
    print(" ✅ 所有演示完成 - 人格矩阵路由系统 v3.0 运行正常")
    print("=" * 70)

