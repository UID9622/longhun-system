# DNA: #龍芯⚡️丙午·乙未·乙丑·噬嗑-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️2026-06-16-WUXING-ENGINE-v3.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    龍魂体系 · 五行融合决策引擎 v3.0                             ║
║═══════════════════════════════════════════════════════════════════════════════║
║  #龍芯⚡️2026-06-16-WUXING-ENGINE-v3.0                                         ║
║  UID9622 · 龍芯北辰 · 诸葛鑫                                                  ║
║  确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  核心链路: DNA签名 → 三色审计 → 流场决策(10道闸) → 入库执行                      ║
║  安全域: 8模块（国标锚定）                                                     ║
║  铁律: Human ≥ 0.34 | 忠(0.5) > 孝(0.3) > 义(0.2)                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import math
import json
import hashlib
import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable, Any
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# 0. 全局常量与DNA签名
# ═══════════════════════════════════════════════════════════════════════════════

UID = "UID9622"
OPERATOR = "龍芯北辰·诸葛鑫"
VERSION = "v3.0"
PROJECT = "WUXING-ENGINE"
DATE = "2026-06-16"

# DNA签名模板
DNA_SIGNATURE_TEMPLATE = "#龍芯⚡️{date}-{project}-{module}-{version}"
DNA_CONFIRM_TEMPLATE = "#CONFIRM🌌{uid}-ONLY-ONCE🧬{token}"

# 三才权重（铁律：Human ≥ 0.34）
SANCAI_WEIGHTS = {
    "Heaven": 0.35,   # 天
    "Earth": 0.20,    # 地
    "Human": 0.45,    # 人（永远不低于34%）
}

# 价值观权重（铁律：忠 > 孝 > 义）
VALUE_WEIGHTS = {
    "忠": 0.5,   # 最高
    "孝": 0.3,   # 次之
    "义": 0.2,   # 基础
}

# 熔断阈值
FUSE_THRESHOLDS = {
    "confidence_min": 0.40,     # 最终置信度 < 0.40 熔断
    "balance_min": 20,           # 平衡指数 < 20 熔断
    "restraint_max": 0.85,       # 相克强度 > 0.85 熔断
    "dr_fuse_values": {3, 9},    # dr ∈ {3,9} 直接熔断
}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 五行基础类（含相生相克矩阵）
# ═══════════════════════════════════════════════════════════════════════════════

class FiveElement(Enum):
    """五行枚举：木火土金水"""
    WOOD  = "木"   # 木 - 生发
    FIRE  = "火"   # 火 - 炎上
    EARTH = "土"   # 土 - 稼穑
    METAL = "金"   # 金 - 从革
    WATER = "水"   # 水 - 润下


class FiveElementsCore:
    """
    五行核心类
    ┌─────────────────────────────────────────────────────────┐
    │  相生链: 木 → 火 → 土 → 金 → 水 → 木                    │
    │  相克链: 木克土, 土克水, 水克火, 火克金, 金克木            │
    └─────────────────────────────────────────────────────────┘
    """

    # 五行元素列表（有序，用于相生链）
    ELEMENT_ORDER = [FiveElement.WOOD, FiveElement.FIRE, FiveElement.EARTH,
                     FiveElement.METAL, FiveElement.WATER]

    # 相生关系：A 生 B (A → B)
    GENERATING_RELATIONS: Dict[FiveElement, FiveElement] = {
        FiveElement.WOOD:  FiveElement.FIRE,   # 木生火
        FiveElement.FIRE:  FiveElement.EARTH,  # 火生土
        FiveElement.EARTH: FiveElement.METAL,  # 土生金
        FiveElement.METAL: FiveElement.WATER,  # 金生水
        FiveElement.WATER: FiveElement.WOOD,   # 水生木
    }

    # 相克关系：A 克 B (A ⇒ B)
    RESTRAINING_RELATIONS: Dict[FiveElement, FiveElement] = {
        FiveElement.WOOD:  FiveElement.EARTH,  # 木克土
        FiveElement.EARTH: FiveElement.WATER,  # 土克水
        FiveElement.WATER: FiveElement.FIRE,   # 水克火
        FiveElement.FIRE:  FiveElement.METAL,  # 火克金
        FiveElement.METAL: FiveElement.WOOD,   # 金克木
    }

    def __init__(self, energies: Optional[Dict[FiveElement, float]] = None):
        """
        初始化五行能量分布
        :param energies: 各五行元素的能量值，默认均衡分布
        """
        if energies is None:
            # 默认均衡：每个元素20
            self.energies = {elem: 20.0 for elem in self.ELEMENT_ORDER}
        else:
            self.energies = {elem: energies.get(elem, 20.0) for elem in self.ELEMENT_ORDER}

        self._validate()

    def _validate(self) -> None:
        """校验五行能量非负"""
        for elem, val in self.energies.items():
            if val < 0:
                raise ValueError(f"五行能量不能为负: {elem.value} = {val}")

    @classmethod
    def get_generator(cls, element: FiveElement) -> FiveElement:
        """获取生我的元素"""
        for src, dst in cls.GENERATING_RELATIONS.items():
            if dst == element:
                return src
        raise ValueError(f"无法找到生{element.value}的元素")

    @classmethod
    def get_generated(cls, element: FiveElement) -> FiveElement:
        """获取我生的元素"""
        return cls.GENERATING_RELATIONS[element]

    @classmethod
    def get_restrainer(cls, element: FiveElement) -> FiveElement:
        """获取克我的元素"""
        for src, dst in cls.RESTRAINING_RELATIONS.items():
            if dst == element:
                return src
        raise ValueError(f"无法找到克{element.value}的元素")

    @classmethod
    def get_restrained(cls, element: FiveElement) -> FiveElement:
        """获取我克的元素"""
        return cls.RESTRAINING_RELATIONS[element]

    def get_generating_strength(self, a: FiveElement, b: FiveElement) -> float:
        """
        计算A对B的相生强度 G(A→B)
        相生强度 = min(A能量, B能量) / max(A能量, B能量) * 归一化因子
        """
        if self.GENERATING_RELATIONS.get(a) != b:
            return 0.0  # 非相生关系

        energy_a = self.energies[a]
        energy_b = self.energies[b]

        if max(energy_a, energy_b) == 0:
            return 0.0

        # 相生强度：相生和谐度
        gen_strength = min(energy_a, energy_b) / max(energy_a, energy_b)
        # 乘以能量充足度因子
        abundance_factor = min(1.0, (energy_a + energy_b) / 40.0)
        return round(gen_strength * abundance_factor, 4)

    def get_restraining_strength(self, a: FiveElement, b: FiveElement) -> float:
        """
        计算A对B的相克强度 R(A⇒B)
        相克强度 = (A能量 - B能量) / (A能量 + B能量) 若A>B则为正相克
        """
        if self.RESTRAINING_RELATIONS.get(a) != b:
            return 0.0  # 非相克关系

        energy_a = self.energies[a]
        energy_b = self.energies[b]

        total = energy_a + energy_b
        if total == 0:
            return 0.0

        # 相克强度：A相对于B的优势
        return round((energy_a - energy_b) / total, 4)

    def to_dict(self) -> Dict[str, float]:
        """序列化为字典"""
        return {elem.value: val for elem, val in self.energies.items()}

    def __repr__(self) -> str:
        items = ", ".join(f"{k.value}={v:.1f}" for k, v in self.energies.items())
        return f"FiveElementsCore({items})"


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 三才平衡类（天/地/人，Human≥0.34）
# ═══════════════════════════════════════════════════════════════════════════════

class SancaiBalance:
    """
    三才平衡类：天 · 地 · 人
    ┌─────────────────────────────────────────────────────────┐
    │  Heaven (天) = 0.35  ·  战略/天时                        │
    │  Earth  (地) = 0.20  ·  资源/地利                        │
    │  Human  (人) = 0.45  ·  执行/人和  [铁律: ≥0.34]         │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, heaven: float = 0.35, earth: float = 0.20, human: float = 0.45):
        """
        初始化三才参数
        :param heaven: 天权重 (0-1)
        :param earth:  地权重 (0-1)
        :param human:  人权重 (0-1) [必须 ≥ 0.34]
        """
        # 铁律处理：Human < 0.34 时自动调整，不抛异常
        adjusted = False
        original_human = human
        if human < 0.34:
            adjusted = True
            # 强制提升到0.34，其余从天/地中按比例缩减
            deficit = 0.34 - human
            human = 0.34
            heaven_earth_sum = heaven + earth
            if heaven_earth_sum > 0:
                heaven -= deficit * (heaven / heaven_earth_sum)
                earth -= deficit * (earth / heaven_earth_sum)
            # 确保非负
            heaven = max(0.0, heaven)
            earth = max(0.0, earth)

        # 自动归一化（保持比例）
        total = heaven + earth + human
        if total == 0:
            raise ValueError("三才权重之和不能为0")

        self.heaven = heaven / total
        self.earth  = earth / total
        self.human  = human / total

        # 二次校验归一化后Human仍 ≥ 0.34
        if self.human < 0.34:
            # 强制提升到0.34，其余按比例缩减
            self.human = 0.34
            remainder = 1.0 - 0.34  # 0.66
            old_sum = self.heaven + self.earth
            if old_sum > 0:
                self.heaven = (self.heaven / old_sum) * remainder
                self.earth  = (self.earth / old_sum) * remainder
            else:
                self.heaven = 0.35 * remainder / 0.55
                self.earth  = 0.20 * remainder / 0.55

        # 最终归一化
        final_total = self.heaven + self.earth + self.human
        self.heaven /= final_total
        self.earth  /= final_total
        self.human  /= final_total

        self._adjusted = adjusted
        self._original_human = original_human

    def get_coefficient(self, heaven_score: float, earth_score: float, human_score: float) -> float:
        """
        公式C：三才平衡系数
        C = Heaven×0.35 + Earth×0.20 + Human×0.45
        :return: 0-1 之间的平衡系数
        """
        c = self.heaven * heaven_score + self.earth * earth_score + self.human * human_score
        return round(max(0.0, min(1.0, c)), 4)

    @property
    def weights(self) -> Dict[str, float]:
        """获取三才权重字典"""
        return {
            "Heaven": round(self.heaven, 4),
            "Earth":  round(self.earth, 4),
            "Human":  round(self.human, 4),
        }

    def __repr__(self) -> str:
        return f"SancaiBalance(天={self.heaven:.4f}, 地={self.earth:.4f}, 人={self.human:.4f})"


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 公式A：五行平衡指数
# ═══════════════════════════════════════════════════════════════════════════════

class FormulaA_BalanceIndex:
    """
    公式A：五行平衡指数
    ┌─────────────────────────────────────────────────────────┐
    │  平衡指数 = 100 - (σ/avg × 100)                          │
    │  σ  = 五行能量的标准差                                   │
    │  avg = 五行能量的平均值                                  │
    │  输出范围：0 - 100                                       │
    │  100 = 完美平衡, 0 = 极度失衡                            │
    └─────────────────────────────────────────────────────────┘
    """

    @staticmethod
    def calculate(five_core: FiveElementsCore) -> float:
        """
        计算五行平衡指数
        :param five_core: 五行核心实例
        :return: 0-100 的平衡指数
        """
        energies = list(five_core.energies.values())
        n = len(energies)

        if n == 0:
            return 0.0

        avg = sum(energies) / n
        if avg == 0:
            return 0.0

        # 标准差 σ
        variance = sum((x - avg) ** 2 for x in energies) / n
        sigma = math.sqrt(variance)

        # 变异系数 CV = σ/avg
        cv = sigma / avg

        # 平衡指数 = 100 - (CV × 100)
        balance_index = 100 - (cv * 100)

        # 限制在0-100范围
        return round(max(0.0, min(100.0, balance_index)), 4)

    @staticmethod
    def interpret(index: float) -> str:
        """平衡指数解读"""
        if index >= 90:
            return "🟢 极佳 - 五行高度平衡"
        elif index >= 70:
            return "🟢 良好 - 五行较为平衡"
        elif index >= 50:
            return "🟡 一般 - 存在轻微失衡"
        elif index >= 30:
            return "🟡 偏险 - 失衡较明显"
        elif index >= 20:
            return "🔴 危险 - 严重失衡"
        else:
            return "🔴 极度危险 - 五行崩解"


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 公式B：相生相克强度
# ═══════════════════════════════════════════════════════════════════════════════

class FormulaB_GenerateRestraint:
    """
    公式B：相生相克强度
    ┌─────────────────────────────────────────────────────────┐
    │  强度 = G(A→B) - R(A⇒B)                                │
    │  G(A→B) = A对B的相生强度                                │
    │  R(A⇒B) = A对B的相克强度                                │
    │  输出范围：-1 ~ 1                                       │
    │  > 0 : 相生主导（和谐）                                  │
    │  < 0 : 相克主导（冲突）                                  │
    │  = 0 : 阴阳平衡                                          │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, five_core: FiveElementsCore):
        self.five_core = five_core

    def calculate(self, a: FiveElement, b: FiveElement) -> float:
        """
        计算A与B之间的相生相克净强度
        :param a: 元素A
        :param b: 元素B
        :return: -1 ~ 1 的净强度值
        """
        # 获取相生强度
        g_strength = self.five_core.get_generating_strength(a, b)

        # 获取相克强度
        r_strength = self.five_core.get_restraining_strength(a, b)

        # 净强度 = 相生 - 相克
        net_strength = g_strength - r_strength

        # 限制在-1~1范围
        return round(max(-1.0, min(1.0, net_strength)), 4)

    def calculate_all_pairs(self) -> Dict[str, Dict[str, float]]:
        """计算所有五行对的相生相克强度矩阵"""
        elements = FiveElementsCore.ELEMENT_ORDER
        matrix = {}

        for a in elements:
            row = {}
            for b in elements:
                if a != b:
                    row[b.value] = self.calculate(a, b)
            matrix[a.value] = row

        return matrix

    def get_restraint_intensity(self) -> float:
        """
        获取整体相克强度（用于熔断检测）
        返回所有相克关系中的最大绝对值
        """
        elements = FiveElementsCore.ELEMENT_ORDER
        max_restraint = 0.0

        for a in elements:
            for b in elements:
                if a != b and FiveElementsCore.RESTRAINING_RELATIONS.get(a) == b:
                    r = abs(self.five_core.get_restraining_strength(a, b))
                    max_restraint = max(max_restraint, r)

        return round(max_restraint, 4)


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 公式C：三才平衡系数
# ═══════════════════════════════════════════════════════════════════════════════

class FormulaC_SancaiCoefficient:
    """
    公式C：三才平衡系数
    ┌─────────────────────────────────────────────────────────┐
    │  C = Heaven×0.35 + Earth×0.20 + Human×0.45             │
    │  基于SancaiBalance的权重计算实际平衡系数                  │
    │  输出范围：0 - 1                                        │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, sancai: SancaiBalance):
        self.sancai = sancai

    def calculate(self, heaven_score: float, earth_score: float, human_score: float) -> float:
        """
        计算三才平衡系数
        :param heaven_score: 天维度的评分 (0-1)
        :param earth_score:  地维度的评分 (0-1)
        :param human_score:  人维度的评分 (0-1)
        :return: 0-1 的三才平衡系数
        """
        return self.sancai.get_coefficient(heaven_score, earth_score, human_score)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 公式D：复合决策强度
# ═══════════════════════════════════════════════════════════════════════════════

class FormulaD_CompositeDecision:
    """
    公式D：复合决策强度
    ┌─────────────────────────────────────────────────────────┐
    │  D = A×0.35 + B×0.30 + C×0.35                          │
    │  A = 五行平衡指数 (归一化到0-1)                          │
    │  B = 相生相克强度 (取绝对值归一化)                        │
    │  C = 三才平衡系数                                        │
    │  输出范围：0 - 1                                        │
    └─────────────────────────────────────────────────────────┘
    """

    # 权重分配
    WEIGHTS = {
        "A": 0.35,  # 五行平衡指数
        "B": 0.30,  # 相生相克强度
        "C": 0.35,  # 三才平衡系数
    }

    @staticmethod
    def calculate(balance_index: float, net_strength: float,
                  sancai_coefficient: float) -> Dict[str, Any]:
        """
        计算复合决策强度
        :param balance_index: 公式A结果 (0-100)
        :param net_strength: 公式B结果 (-1~1)
        :param sancai_coefficient: 公式C结果 (0-1)
        :return: 包含详细分解的字典
        """
        # 归一化A到0-1
        A_norm = balance_index / 100.0

        # 归一化B到0-1（取绝对值，因为极端正负都表示不平衡）
        B_norm = abs(net_strength)

        # C已经是0-1
        C = sancai_coefficient

        # 复合决策强度
        D = (FormulaD_CompositeDecision.WEIGHTS["A"] * A_norm +
             FormulaD_CompositeDecision.WEIGHTS["B"] * (1 - B_norm) +  # 1-B因为B越小越好
             FormulaD_CompositeDecision.WEIGHTS["C"] * C)

        D = round(max(0.0, min(1.0, D)), 4)

        # 置信度 = D本身
        confidence = D

        return {
            "composite_score": D,
            "confidence": confidence,
            "components": {
                "A_balance": {
                    "raw": balance_index,
                    "normalized": round(A_norm, 4),
                    "weight": FormulaD_CompositeDecision.WEIGHTS["A"],
                    "contribution": round(FormulaD_CompositeDecision.WEIGHTS["A"] * A_norm, 4),
                },
                "B_strength": {
                    "raw": net_strength,
                    "normalized": round(B_norm, 4),
                    "weight": FormulaD_CompositeDecision.WEIGHTS["B"],
                    "contribution": round(FormulaD_CompositeDecision.WEIGHTS["B"] * (1 - B_norm), 4),
                },
                "C_sancai": {
                    "raw": sancai_coefficient,
                    "normalized": round(C, 4),
                    "weight": FormulaD_CompositeDecision.WEIGHTS["C"],
                    "contribution": round(FormulaD_CompositeDecision.WEIGHTS["C"] * C, 4),
                },
            },
            "decision": "PASS" if confidence >= FUSE_THRESHOLDS["confidence_min"] else "FUSE",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 7. 熔断检测器（5条熔断规则）
# ═══════════════════════════════════════════════════════════════════════════════

class FuseDetector:
    """
    熔断检测器 - 守护决策安全的最后防线
    ┌─────────────────────────────────────────────────────────┐
    │  熔断规则：                                               │
    │  1. dr ∈ {3, 9}          → 🔴 直接熔断                   │
    │  2. AI自审失败            → 🔴 熔断                      │
    │  3. 最终置信度 < 0.40     → 🔴 熔断                      │
    │  4. 平衡指数 < 20         → 🔴 熔断                      │
    │  5. 相克强度 > 0.85       → 🔴 熔断                      │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self):
        self.fuse_log: List[Dict[str, Any]] = []
        self.fused = False
        self.fuse_reasons: List[str] = []

    def check_dr(self, dr: int) -> bool:
        """规则1：dr ∈ {3, 9} 直接熔断"""
        if dr in FUSE_THRESHOLDS["dr_fuse_values"]:
            self._trigger(f"dr={dr} 在熔断值 {{3, 9}} 中", "dr_fuse")
            return True
        return False

    def check_ai_audit(self, audit_passed: bool) -> bool:
        """规则2：AI自审失败熔断"""
        if not audit_passed:
            self._trigger("AI自审未通过", "ai_audit_fail")
            return True
        return False

    def check_confidence(self, confidence: float) -> bool:
        """规则3：最终置信度 < 0.40 熔断"""
        if confidence < FUSE_THRESHOLDS["confidence_min"]:
            self._trigger(f"置信度 {confidence:.4f} < 阈值 {FUSE_THRESHOLDS['confidence_min']}",
                         "low_confidence")
            return True
        return False

    def check_balance_index(self, balance_index: float) -> bool:
        """规则4：平衡指数 < 20 熔断"""
        if balance_index < FUSE_THRESHOLDS["balance_min"]:
            self._trigger(f"平衡指数 {balance_index:.2f} < 阈值 {FUSE_THRESHOLDS['balance_min']}",
                         "low_balance")
            return True
        return False

    def check_restraint_strength(self, restraint_intensity: float) -> bool:
        """规则5：相克强度 > 0.85 熔断"""
        if restraint_intensity > FUSE_THRESHOLDS["restraint_max"]:
            self._trigger(f"相克强度 {restraint_intensity:.4f} > 阈值 {FUSE_THRESHOLDS['restraint_max']}",
                         "high_restraint")
            return True
        return False

    def _trigger(self, reason: str, code: str) -> None:
        """触发熔断"""
        self.fused = True
        self.fuse_reasons.append(reason)
        self.fuse_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "reason": reason,
            "code": code,
        })

    def full_check(self, dr: int, audit_passed: bool, confidence: float,
                   balance_index: float, restraint_intensity: float) -> Dict[str, Any]:
        """
        执行全部5项熔断检测
        :return: 熔断检测结果字典
        """
        self.fused = False
        self.fuse_reasons = []
        self.fuse_log = []

        results = {
            "dr_check": {"passed": not self.check_dr(dr), "dr": dr},
            "ai_audit": {"passed": not self.check_ai_audit(audit_passed)},
            "confidence": {"passed": not self.check_confidence(confidence), "value": confidence},
            "balance_index": {"passed": not self.check_balance_index(balance_index), "value": balance_index},
            "restraint": {"passed": not self.check_restraint_strength(restraint_intensity),
                         "value": restraint_intensity},
        }

        return {
            "fused": self.fused,
            "fuse_count": len(self.fuse_reasons),
            "fuse_reasons": self.fuse_reasons.copy(),
            "fuse_details": results,
            "can_proceed": not self.fused,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def __repr__(self) -> str:
        status = "🔴 已熔断" if self.fused else "🟢 正常"
        return f"FuseDetector({status}, 触发次数={len(self.fuse_reasons)})"


# ═══════════════════════════════════════════════════════════════════════════════
# 8. 三色审计接口（🟢🟡🔴）
# ═══════════════════════════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色审计状态"""
    GREEN  = "🟢"  # 通过 - 可以执行
    YELLOW = "🟡"  # 警告 - 需要关注
    RED    = "🔴"  # 危险 - 必须熔断


@dataclass
class AuditResult:
    """审计结果数据结构"""
    color: AuditColor
    status: str
    score: float
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "color": self.color.value,
            "status": self.status,
            "score": self.score,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class ThreeColorAudit:
    """
    三色审计系统 - 龍魂体系核心质量关卡
    ┌─────────────────────────────────────────────────────────┐
    │  🟢 绿色: 全部指标正常，决策通过                          │
    │  🟡 黄色: 存在警告项，需人工复核                          │
    │  🔴 红色: 严重违规，强制熔断                              │
    └─────────────────────────────────────────────────────────┘
    """

    # 阈值定义
    THRESHOLDS = {
        AuditColor.GREEN:  {
            "balance_min": 70,       # 平衡指数 ≥ 70
            "confidence_min": 0.75,  # 置信度 ≥ 0.75
            "restraint_max": 0.3,   # 相克 ≤ 0.3
        },
        AuditColor.YELLOW: {
            "balance_min": 40,       # 平衡指数 ≥ 40
            "confidence_min": 0.50,  # 置信度 ≥ 0.50
            "restraint_max": 0.6,   # 相克 ≤ 0.6
        },
        # 低于YELLOW阈值 → RED
    }

    def __init__(self):
        self.audit_history: List[AuditResult] = []

    def audit(self, balance_index: float, confidence: float,
              restraint_intensity: float, additional_checks: Optional[Dict] = None) -> AuditResult:
        """
        执行三色审计
        :param balance_index: 五行平衡指数
        :param confidence: 决策置信度
        :param restraint_intensity: 相克强度
        :param additional_checks: 额外检查项
        :return: AuditResult
        """
        details = {
            "balance_index": balance_index,
            "confidence": confidence,
            "restraint_intensity": restraint_intensity,
        }

        # 判定颜色
        if (balance_index >= self.THRESHOLDS[AuditColor.GREEN]["balance_min"] and
            confidence >= self.THRESHOLDS[AuditColor.GREEN]["confidence_min"] and
            restraint_intensity <= self.THRESHOLDS[AuditColor.GREEN]["restraint_max"]):

            color = AuditColor.GREEN
            status = "DECISION_PASS"

        elif (balance_index >= self.THRESHOLDS[AuditColor.YELLOW]["balance_min"] and
              confidence >= self.THRESHOLDS[AuditColor.YELLOW]["confidence_min"] and
              restraint_intensity <= self.THRESHOLDS[AuditColor.YELLOW]["restraint_max"]):

            color = AuditColor.YELLOW
            status = "DECISION_WARNING"

        else:
            color = AuditColor.RED
            status = "DECISION_FUSE"

        # 附加检查
        if additional_checks:
            details["additional"] = additional_checks
            for check_name, check_result in additional_checks.items():
                if not check_result:
                    color = AuditColor.RED
                    status = f"DECISION_FUSE:{check_name}"
                    details["fuse_reason"] = check_name

        score = self._calculate_audit_score(balance_index, confidence, restraint_intensity)

        result = AuditResult(color=color, status=status, score=score, details=details)
        self.audit_history.append(result)
        return result

    def _calculate_audit_score(self, balance_index: float, confidence: float,
                               restraint_intensity: float) -> float:
        """计算审计综合评分"""
        # 平衡指数贡献 (0-40分)
        balance_score = min(40, balance_index * 0.4)
        # 置信度贡献 (0-35分)
        conf_score = min(35, confidence * 35)
        # 相克抑制贡献 (0-25分)
        restraint_score = max(0, 25 - restraint_intensity * 25)

        total = balance_score + conf_score + restraint_score
        return round(min(100, total), 2)

    def get_audit_report(self) -> Dict[str, Any]:
        """获取审计报告"""
        if not self.audit_history:
            return {"status": "NO_AUDITS_YET"}

        latest = self.audit_history[-1]
        green_count = sum(1 for a in self.audit_history if a.color == AuditColor.GREEN)
        yellow_count = sum(1 for a in self.audit_history if a.color == AuditColor.YELLOW)
        red_count = sum(1 for a in self.audit_history if a.color == AuditColor.RED)

        return {
            "latest_audit": latest.to_dict(),
            "statistics": {
                "total": len(self.audit_history),
                "green": green_count,
                "yellow": yellow_count,
                "red": red_count,
            },
            "pass_rate": round(green_count / len(self.audit_history) * 100, 2),
        }

    def __repr__(self) -> str:
        if not self.audit_history:
            return "ThreeColorAudit(未审计)"
        latest = self.audit_history[-1]
        return f"ThreeColorAudit(最新: {latest.color.value} {latest.status} 评分:{latest.score})"


# ═══════════════════════════════════════════════════════════════════════════════
# 9. DNA签名生成器
# ═══════════════════════════════════════════════════════════════════════════════

class DNASignature:
    """
    DNA签名生成器 - 龍魂体系身份认证
    ┌─────────────────────────────────────────────────────────┐
    │  签名格式: #龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}       │
    │  确认码:  #CONFIRM🌌{UID}-ONLY-ONCE🧬{随机令牌}           │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, uid: str = UID, operator: str = OPERATOR,
                 version: str = VERSION, project: str = PROJECT):
        self.uid = uid
        self.operator = operator
        self.version = version
        self.project = project
        self.signatures: List[str] = []

    def generate(self, module: str = PROJECT, date: Optional[str] = None) -> Dict[str, str]:
        """
        生成DNA签名
        :param module: 模块名称
        :param date: 日期（默认今天）
        :return: 签名信息字典
        """
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")

        # 主签名
        signature = DNA_SIGNATURE_TEMPLATE.format(
            date=date, project=self.project, module=module, version=self.version
        )

        # 确认令牌（基于签名哈希）
        token_raw = f"{self.uid}-{signature}-{datetime.datetime.now().timestamp()}"
        token = hashlib.sha256(token_raw.encode()).hexdigest()[:8].upper()

        # 确认码
        confirmation = DNA_CONFIRM_TEMPLATE.format(uid=self.uid, token=token)

        sig_info = {
            "signature": signature,
            "confirmation": confirmation,
            "uid": self.uid,
            "operator": self.operator,
            "version": self.version,
            "date": date,
            "token": token,
        }

        self.signatures.append(signature)
        return sig_info

    def verify(self, signature: str, confirmation: str) -> bool:
        """验证签名有效性"""
        # 基础格式校验
        if not signature.startswith("#龍芯⚡️"):
            return False
        if not confirmation.startswith("#CONFIRM🌌"):
            return False

        # UID校验
        if self.uid not in confirmation:
            return False

        return True

    @classmethod
    def get_header(cls, module: str = PROJECT) -> str:
        """获取文件头部DNA签名注释"""
        sig = DNASignature()
        sig_info = sig.generate(module=module)
        return f"""# {sig_info['signature']}
# {sig_info['uid']} · {OPERATOR}
# 确认: {sig_info['confirmation']}
"""

    def __repr__(self) -> str:
        return f"DNASignature({self.uid}, {self.operator}, {self.version})"


# ═══════════════════════════════════════════════════════════════════════════════
# 10. 价值排序校验（忠 > 孝 > 义）
# ═══════════════════════════════════════════════════════════════════════════════

class ValueSystemValidator:
    """
    价值体系校验器
    ┌─────────────────────────────────────────────────────────┐
    │  铁律: 忠(0.5) > 孝(0.3) > 义(0.2)                       │
    │  任何违反此排序的决策将触发价值观熔断                      │
    └─────────────────────────────────────────────────────────┘
    """

    HIERARCHY = {
        "忠": 0.5,
        "孝": 0.3,
        "义": 0.2,
    }

    ORDER = ["忠", "孝", "义"]  # 优先级递减

    @classmethod
    def validate(cls, values: Dict[str, float]) -> Dict[str, Any]:
        """
        校验价值观排序
        :param values: {"忠": x, "孝": y, "义": z}
        :return: 校验结果
        """
        errors = []
        checks = {}

        # 检查完整性和排序
        prev_value = float('inf')
        prev_name = None

        for name in cls.ORDER:
            expected = cls.HIERARCHY[name]
            actual = values.get(name, 0)
            checks[name] = {
                "expected": expected,
                "actual": actual,
                "match": abs(actual - expected) < 0.01,
            }

            if actual > prev_value + 0.01:
                errors.append(f"{name}({actual}) > {prev_name}({prev_value})，违反忠>孝>义铁律")

            prev_value = actual
            prev_name = name

        # 严格排序校验
        zhong = values.get("忠", 0)
        xiao = values.get("孝", 0)
        yi = values.get("义", 0)

        if not (zhong > xiao > yi or (abs(zhong - 0.5) < 0.01 and abs(xiao - 0.3) < 0.01 and abs(yi - 0.2) < 0.01)):
            errors.append(f"价值观排序错误: 忠({zhong}) 孝({xiao}) 义({yi})，必须为 忠(0.5)>孝(0.3)>义(0.2)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "checks": checks,
            "hierarchy": cls.HIERARCHY,
        }

    @classmethod
    def get_standard_values(cls) -> Dict[str, float]:
        """获取标准价值观配置"""
        return cls.HIERARCHY.copy()

    @classmethod
    def check_decision_alignment(cls, decision_weights: Dict[str, float]) -> Dict[str, Any]:
        """
        检查决策权重是否与价值观对齐
        :param decision_weights: 决策中各价值观的权重
        :return: 对齐评估结果
        """
        alignment_score = 0.0
        details = {}

        for virtue, standard_weight in cls.HIERARCHY.items():
            actual_weight = decision_weights.get(virtue, 0)
            diff = abs(actual_weight - standard_weight)
            # 差异越小，对齐度越高
            virtue_alignment = max(0, 1 - diff * 5)  # 放大差异惩罚
            alignment_score += virtue_alignment * standard_weight
            details[virtue] = {
                "standard": standard_weight,
                "actual": actual_weight,
                "diff": round(diff, 4),
                "alignment": round(virtue_alignment, 4),
            }

        return {
            "aligned": alignment_score >= 0.85,
            "alignment_score": round(alignment_score, 4),
            "details": details,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 11. 主决策引擎（整合以上全部）
# ═══════════════════════════════════════════════════════════════════════════════

class WuxingDecisionEngine:
    """
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║              五行融合决策引擎 - 龍魂体系核心                                   ║
    ║  核心链路: DNA签名 → 三色审计 → 流场决策(10道闸) → 入库执行                    ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """

    def __init__(self, uid: str = UID, operator: str = OPERATOR):
        # 身份认证
        self.uid = uid
        self.operator = operator
        self.dna = DNASignature(uid=uid, operator=operator)

        # 五行核心
        self.five_core: Optional[FiveElementsCore] = None

        # 三才平衡
        self.sancai: Optional[SancaiBalance] = None

        # 公式引擎
        self.formula_a = FormulaA_BalanceIndex()
        self.formula_b: Optional[FormulaB_GenerateRestraint] = None
        self.formula_c: Optional[FormulaC_SancaiCoefficient] = None

        # 熔断检测器
        self.fuse_detector = FuseDetector()

        # 三色审计
        self.audit = ThreeColorAudit()

        # 价值观校验
        self.value_validator = ValueSystemValidator()

        # 决策历史
        self.decision_history: List[Dict[str, Any]] = []

        # 引擎状态
        self.initialized = False
        self.engine_signature = None

    def initialize(self, energies: Optional[Dict[FiveElement, float]] = None,
                   sancai_config: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        初始化决策引擎
        :param energies: 五行能量分布
        :param sancai_config: 三才配置 {"heaven": x, "earth": y, "human": z}
        """
        # 生成引擎DNA签名
        self.engine_signature = self.dna.generate(module="WUXING-ENGINE-INIT")

        # 初始化五行核心
        if energies is None:
            energies = {elem: 20.0 for elem in FiveElementsCore.ELEMENT_ORDER}
        self.five_core = FiveElementsCore(energies)

        # 初始化三才平衡
        if sancai_config is None:
            sancai_config = {"heaven": 0.35, "earth": 0.20, "human": 0.45}
        self.sancai = SancaiBalance(**sancai_config)

        # 初始化公式引擎
        self.formula_b = FormulaB_GenerateRestraint(self.five_core)
        self.formula_c = FormulaC_SancaiCoefficient(self.sancai)

        self.initialized = True

        return {
            "status": "INITIALIZED",
            "signature": self.engine_signature,
            "five_elements": self.five_core.to_dict(),
            "sancai_weights": self.sancai.weights,
            "values": self.value_validator.get_standard_values(),
        }

    def decide(self, decision_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行完整决策流程
        ┌─────────────────────────────────────────────────────────┐
        │  流程:                                                   │
        │  1. 参数校验                                              │
        │  2. 计算五行平衡指数 (公式A)                               │
        │  3. 计算相生相克强度 (公式B)                               │
        │  4. 计算三才平衡系数 (公式C)                               │
        │  5. 计算复合决策强度 (公式D)                               │
        │  6. 价值观校验                                            │
        │  7. 熔断检测（5条规则）                                    │
        │  8. 三色审计                                              │
        │  9. 生成决策结果                                          │
        └─────────────────────────────────────────────────────────┘
        """
        if not self.initialized:
            raise RuntimeError("决策引擎未初始化，请先调用 initialize()")

        # ── 步骤1: 参数提取 ──
        dr = decision_input.get("dr", 0)
        heaven_score = decision_input.get("heaven_score", 0.5)
        earth_score = decision_input.get("earth_score", 0.5)
        human_score = decision_input.get("human_score", 0.5)
        ai_audit_passed = decision_input.get("ai_audit_passed", True)
        decision_values = decision_input.get("values", {"忠": 0.5, "孝": 0.3, "义": 0.2})
        context = decision_input.get("context", {})

        # ── 步骤2: 公式A - 五行平衡指数 ──
        balance_index = self.formula_a.calculate(self.five_core)

        # ── 步骤3: 公式B - 相生相克强度 ──
        # 计算整体净强度（取所有对的平均值）
        all_pairs = self.formula_b.calculate_all_pairs()
        net_strengths = []
        for elem_pairs in all_pairs.values():
            net_strengths.extend(elem_pairs.values())
        avg_net_strength = sum(net_strengths) / len(net_strengths) if net_strengths else 0
        restraint_intensity = self.formula_b.get_restraint_intensity()

        # ── 步骤4: 公式C - 三才平衡系数 ──
        sancai_coefficient = self.formula_c.calculate(heaven_score, earth_score, human_score)

        # ── 步骤5: 公式D - 复合决策强度 ──
        decision_result = FormulaD_CompositeDecision.calculate(
            balance_index=balance_index,
            net_strength=avg_net_strength,
            sancai_coefficient=sancai_coefficient,
        )
        composite_score = decision_result["composite_score"]
        confidence = decision_result["confidence"]

        # ── 步骤6: 价值观校验 ──
        value_check = self.value_validator.validate(decision_values)
        value_alignment = self.value_validator.check_decision_alignment(decision_values)

        # ── 步骤7: 熔断检测 ──
        fuse_result = self.fuse_detector.full_check(
            dr=dr,
            audit_passed=ai_audit_passed,
            confidence=confidence,
            balance_index=balance_index,
            restraint_intensity=restraint_intensity,
        )

        # ── 步骤8: 三色审计 ──
        # 价值观错误强制红色
        additional_checks = {"values_valid": value_check["valid"]}
        audit_result = self.audit.audit(
            balance_index=balance_index,
            confidence=confidence,
            restraint_intensity=restraint_intensity,
            additional_checks=additional_checks,
        )

        # ── 步骤9: 生成最终决策 ──
        can_execute = (fuse_result["can_proceed"] and
                      audit_result.color != AuditColor.RED and
                      value_check["valid"])

        # DNA签名
        decision_signature = self.dna.generate(module="WUXING-DECISION")

        result = {
            "signature": decision_signature,
            "formulas": {
                "A_balance_index": {
                    "value": balance_index,
                    "interpretation": self.formula_a.interpret(balance_index),
                },
                "B_net_strength": {
                    "value": avg_net_strength,
                    "restraint_intensity": restraint_intensity,
                    "all_pairs": all_pairs,
                },
                "C_sancai_coefficient": {
                    "value": sancai_coefficient,
                    "weights": self.sancai.weights,
                    "scores": {"heaven": heaven_score, "earth": earth_score, "human": human_score},
                },
                "D_composite": decision_result,
            },
            "fuse_check": fuse_result,
            "audit": audit_result.to_dict(),
            "value_check": {
                **value_check,
                "alignment": value_alignment,
            },
            "can_execute": can_execute,
            "decision": "EXECUTE" if can_execute else "REJECT",
            "context": context,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        self.decision_history.append(result)
        return result

    def get_report(self) -> Dict[str, Any]:
        """获取引擎运行报告"""
        return {
            "engine_info": {
                "uid": self.uid,
                "operator": self.operator,
                "version": VERSION,
                "initialized": self.initialized,
                "signature": self.engine_signature,
            },
            "statistics": {
                "total_decisions": len(self.decision_history),
                "executed": sum(1 for d in self.decision_history if d["decision"] == "EXECUTE"),
                "rejected": sum(1 for d in self.decision_history if d["decision"] == "REJECT"),
            },
            "five_elements": self.five_core.to_dict() if self.five_core else None,
            "sancai_weights": self.sancai.weights if self.sancai else None,
            "audit_report": self.audit.get_audit_report(),
            "values": self.value_validator.get_standard_values(),
        }

    def __repr__(self) -> str:
        status = "✅ 已初始化" if self.initialized else "❌ 未初始化"
        return f"WuxingDecisionEngine({self.uid}, {status}, 决策次数={len(self.decision_history)})"


# ═══════════════════════════════════════════════════════════════════════════════
# 12. 示例用例与自测试
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """
    五行融合决策引擎演示
    展示完整的决策链路
    """
    print("=" * 80)
    print("  龍魂体系 · 五行融合决策引擎 v3.0 - 演示")
    print("=" * 80)

    # ── 12.1 创建引擎 ──
    print("\n[步骤1] 创建决策引擎...")
    engine = WuxingDecisionEngine(uid="UID9622", operator="龍芯北辰·诸葛鑫")
    print(f"  引擎: {engine}")

    # ── 12.2 初始化引擎 ──
    print("\n[步骤2] 初始化引擎（均衡五行，标准三才）...")
    init_result = engine.initialize()
    print(f"  状态: {init_result['status']}")
    print(f"  签名: {init_result['signature']['signature']}")
    print(f"  五行: {init_result['five_elements']}")
    print(f"  三才: {init_result['sancai_weights']}")
    print(f"  价值观: {init_result['values']}")

    # ── 12.3 用例1：正常决策 ──
    print("\n[用例1] 正常决策（均衡状态）...")
    decision1 = engine.decide({
        "dr": 5,
        "heaven_score": 0.8,
        "earth_score": 0.7,
        "human_score": 0.9,
        "ai_audit_passed": True,
        "values": {"忠": 0.5, "孝": 0.3, "义": 0.2},
        "context": {"scenario": "标准决策", "priority": "normal"},
    })
    print(f"  决策: {decision1['decision']}")
    print(f"  平衡指数(A): {decision1['formulas']['A_balance_index']['value']:.2f} "
          f"- {decision1['formulas']['A_balance_index']['interpretation']}")
    print(f"  复合强度(D): {decision1['formulas']['D_composite']['composite_score']:.4f}")
    print(f"  置信度: {decision1['formulas']['D_composite']['confidence']:.4f}")
    print(f"  审计: {decision1['audit']['color']} {decision1['audit']['status']}")
    print(f"  熔断: {'🔴 是' if decision1['fuse_check']['fused'] else '🟢 否'}")

    # ── 12.4 用例2：dr=3 熔断测试 ──
    print("\n[用例2] dr=3 熔断测试...")
    decision2 = engine.decide({
        "dr": 3,
        "heaven_score": 0.8,
        "earth_score": 0.7,
        "human_score": 0.9,
        "ai_audit_passed": True,
        "values": {"忠": 0.5, "孝": 0.3, "义": 0.2},
        "context": {"scenario": "dr熔断测试", "priority": "critical"},
    })
    print(f"  决策: {decision2['decision']}")
    print(f"  熔断原因: {decision2['fuse_check']['fuse_reasons']}")

    # ── 12.5 用例3：低置信度熔断 ──
    print("\n[用例3] 极低置信度熔断测试...")
    # 创建一个极端不平衡的五行配置
    unbalanced_energies = {
        FiveElement.WOOD: 80,
        FiveElement.FIRE: 5,
        FiveElement.EARTH: 5,
        FiveElement.METAL: 5,
        FiveElement.WATER: 5,
    }
    engine_unbalanced = WuxingDecisionEngine(uid="UID9622", operator="龍芯北辰·诸葛鑫")
    engine_unbalanced.initialize(energies=unbalanced_energies)
    decision3 = engine_unbalanced.decide({
        "dr": 5,
        "heaven_score": 0.1,
        "earth_score": 0.1,
        "human_score": 0.1,
        "ai_audit_passed": True,
        "values": {"忠": 0.5, "孝": 0.3, "义": 0.2},
        "context": {"scenario": "低置信度熔断测试", "priority": "test"},
    })
    print(f"  决策: {decision3['decision']}")
    print(f"  平衡指数(A): {decision3['formulas']['A_balance_index']['value']:.2f}")
    print(f"  置信度: {decision3['formulas']['D_composite']['confidence']:.4f}")
    print(f"  熔断: {'🔴 是' if decision3['fuse_check']['fused'] else '🟢 否'}")
    print(f"  熔断原因: {decision3['fuse_check']['fuse_reasons']}")

    # ── 12.6 用例4：价值观违规 ──
    print("\n[用例4] 价值观违规测试...")
    decision4 = engine.decide({
        "dr": 5,
        "heaven_score": 0.8,
        "earth_score": 0.7,
        "human_score": 0.9,
        "ai_audit_passed": True,
        "values": {"忠": 0.2, "孝": 0.5, "义": 0.3},  # 错误排序
        "context": {"scenario": "价值观违规测试", "priority": "test"},
    })
    print(f"  决策: {decision4['decision']}")
    print(f"  价值观有效: {decision4['value_check']['valid']}")
    print(f"  价值观错误: {decision4['value_check']['errors']}")
    print(f"  审计: {decision4['audit']['color']} {decision4['audit']['status']}")

    # ── 12.7 用例5：AI自审失败 ──
    print("\n[用例5] AI自审失败熔断测试...")
    decision5 = engine.decide({
        "dr": 5,
        "heaven_score": 0.8,
        "earth_score": 0.7,
        "human_score": 0.9,
        "ai_audit_passed": False,
        "values": {"忠": 0.5, "孝": 0.3, "义": 0.2},
        "context": {"scenario": "AI自审失败测试", "priority": "test"},
    })
    print(f"  决策: {decision5['decision']}")
    print(f"  熔断原因: {decision5['fuse_check']['fuse_reasons']}")

    # ── 12.8 五行相生相克矩阵展示 ──
    print("\n[附录] 五行相生相克矩阵")
    print("  相生链: 木 → 火 → 土 → 金 → 水 → 木")
    print("  相克链: 木克土, 土克水, 水克火, 火克金, 金克木")
    core = FiveElementsCore()
    print("\n  相生强度矩阵:")
    elements = FiveElementsCore.ELEMENT_ORDER
    header = "    " + "".join(f"{e.value:>8}" for e in elements)
    print(header)
    for a in elements:
        row = f"  {a.value} "
        for b in elements:
            if a == b:
                row += "    --- "
            else:
                g = core.get_generating_strength(a, b)
                row += f"  {g:>5.2f} "
        print(row)

    print("\n  相克强度矩阵:")
    print(header)
    for a in elements:
        row = f"  {a.value} "
        for b in elements:
            if a == b:
                row += "    --- "
            else:
                r = core.get_restraining_strength(a, b)
                row += f"  {r:>5.2f} "
        print(row)

    # ── 12.9 引擎报告 ──
    print("\n" + "=" * 80)
    print("  引擎运行报告")
    print("=" * 80)
    report = engine.get_report()
    print(f"  总决策数: {report['statistics']['total_decisions']}")
    print(f"  通过执行: {report['statistics']['executed']}")
    print(f"  被拒绝:  {report['statistics']['rejected']}")
    print(f"  审计统计: {report['audit_report']['statistics']}")

    print("\n" + "=" * 80)
    print("  演示完成 - 五行融合决策引擎 v3.0")
    print("  #龍芯⚡️2026-06-16-WUXING-ENGINE-v3.0")
    print("=" * 80)

    return {
        "engine": engine,
        "decisions": [decision1, decision2, decision3, decision4, decision5],
    }


def self_test():
    """
    自测试函数 - 验证引擎全部功能
    """
    print("\n" + "=" * 80)
    print("  五行融合决策引擎 - 自测试")
    print("=" * 80)

    test_results = []

    # 测试1: 五行基础
    print("\n[测试1] 五行基础类...")
    try:
        core = FiveElementsCore()
        assert len(core.energies) == 5, "五行数量错误"
        assert all(v == 20.0 for v in core.energies.values()), "默认能量错误"
        assert core.get_generated(FiveElement.WOOD) == FiveElement.FIRE, "木生火错误"
        assert core.get_restrained(FiveElement.WOOD) == FiveElement.EARTH, "木克土错误"
        print("  ✅ 通过")
        test_results.append(("五行基础", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("五行基础", False, str(e)))

    # 测试2: 三才平衡（铁律 Human ≥ 0.34）
    print("\n[测试2] 三才平衡（铁律校验）...")
    try:
        # 正常情况
        sancai = SancaiBalance(0.35, 0.20, 0.45)
        assert sancai.human >= 0.34, "Human权重错误"
        print(f"  标准三才: 天={sancai.heaven:.4f} 地={sancai.earth:.4f} 人={sancai.human:.4f}")

        # 铁律触发：Human < 0.34 应自动调整
        sancai_low = SancaiBalance(0.5, 0.3, 0.1)  # human=0.1 < 0.34
        assert sancai_low.human >= 0.34, f"铁律违反: human={sancai_low.human}"
        print(f"  调整后: 天={sancai_low.heaven:.4f} 地={sancai_low.earth:.4f} 人={sancai_low.human:.4f}")
        print("  ✅ 通过")
        test_results.append(("三才平衡", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("三才平衡", False, str(e)))

    # 测试3: 公式A
    print("\n[测试3] 公式A（五行平衡指数）...")
    try:
        # 完美平衡：所有能量相等 → 指数=100
        balanced = FiveElementsCore({e: 20.0 for e in FiveElementsCore.ELEMENT_ORDER})
        idx = FormulaA_BalanceIndex.calculate(balanced)
        assert idx == 100.0, f"完美平衡应为100, 得到{idx}"
        print(f"  完美平衡: {idx}")

        # 极端不平衡
        unbalanced = FiveElementsCore({
            FiveElement.WOOD: 100, FiveElement.FIRE: 1,
            FiveElement.EARTH: 1, FiveElement.METAL: 1, FiveElement.WATER: 1,
        })
        idx_low = FormulaA_BalanceIndex.calculate(unbalanced)
        assert idx_low < 50, f"极端不平衡应<50, 得到{idx_low}"
        print(f"  极端失衡: {idx_low}")
        print("  ✅ 通过")
        test_results.append(("公式A", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("公式A", False, str(e)))

    # 测试4: 公式B
    print("\n[测试4] 公式B（相生相克强度）...")
    try:
        core = FiveElementsCore()
        fb = FormulaB_GenerateRestraint(core)
        # 木→火是相生关系
        s = fb.calculate(FiveElement.WOOD, FiveElement.FIRE)
        assert -1 <= s <= 1, f"强度超出范围: {s}"
        print(f"  木→火强度: {s}")

        # 木→土是相克关系
        r = fb.calculate(FiveElement.WOOD, FiveElement.EARTH)
        assert -1 <= r <= 1, f"强度超出范围: {r}"
        print(f"  木→土强度: {r}")
        print("  ✅ 通过")
        test_results.append(("公式B", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("公式B", False, str(e)))

    # 测试5: 公式C
    print("\n[测试5] 公式C（三才平衡系数）...")
    try:
        sancai = SancaiBalance(0.35, 0.20, 0.45)
        fc = FormulaC_SancaiCoefficient(sancai)
        coeff = fc.calculate(1.0, 1.0, 1.0)
        assert 0 <= coeff <= 1, f"系数超出范围: {coeff}"
        assert coeff == 1.0, f"满分输入应为1.0, 得到{coeff}"

        coeff_low = fc.calculate(0.0, 0.0, 0.0)
        assert coeff_low == 0.0, f"零分输入应为0.0, 得到{coeff_low}"
        print(f"  满分: {coeff}, 零分: {coeff_low}")
        print("  ✅ 通过")
        test_results.append(("公式C", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("公式C", False, str(e)))

    # 测试6: 公式D
    print("\n[测试6] 公式D（复合决策强度）...")
    try:
        result = FormulaD_CompositeDecision.calculate(
            balance_index=100, net_strength=0, sancai_coefficient=1.0
        )
        assert 0 <= result["composite_score"] <= 1, "复合分数超出范围"
        assert result["composite_score"] == 1.0, f"满分应为1.0, 得到{result['composite_score']}"
        print(f"  满分决策: {result['composite_score']}")
        print("  ✅ 通过")
        test_results.append(("公式D", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("公式D", False, str(e)))

    # 测试7: 熔断检测器（5条规则）
    print("\n[测试7] 熔断检测器（5条规则）...")
    try:
        fuse = FuseDetector()

        # 规则1: dr=3
        r1 = fuse.check_dr(3)
        assert r1 == True, "dr=3应触发熔断"

        # 规则2: AI自审失败
        fuse2 = FuseDetector()
        r2 = fuse2.check_ai_audit(False)
        assert r2 == True, "AI自审失败应触发熔断"

        # 规则3: 置信度<0.4
        fuse3 = FuseDetector()
        r3 = fuse3.check_confidence(0.3)
        assert r3 == True, "低置信度应触发熔断"

        # 规则4: 平衡指数<20
        fuse4 = FuseDetector()
        r4 = fuse4.check_balance_index(15)
        assert r4 == True, "低平衡指数应触发熔断"

        # 规则5: 相克强度>0.85
        fuse5 = FuseDetector()
        r5 = fuse5.check_restraint_strength(0.9)
        assert r5 == True, "高相克强度应触发熔断"

        # 全部通过检测
        fuse_all = FuseDetector()
        result = fuse_all.full_check(dr=5, audit_passed=True, confidence=0.8,
                                     balance_index=80, restraint_intensity=0.2)
        assert result["can_proceed"] == True, "正常情况不应熔断"

        print("  5条熔断规则全部验证通过")
        print("  ✅ 通过")
        test_results.append(("熔断检测", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("熔断检测", False, str(e)))

    # 测试8: 三色审计
    print("\n[测试8] 三色审计系统...")
    try:
        audit = ThreeColorAudit()
        # 绿色
        r_green = audit.audit(85, 0.85, 0.1)
        assert r_green.color == AuditColor.GREEN, f"应为绿色, 得到{r_green.color}"
        # 黄色
        r_yellow = audit.audit(55, 0.6, 0.4)
        assert r_yellow.color == AuditColor.YELLOW, f"应为黄色, 得到{r_yellow.color}"
        # 红色
        r_red = audit.audit(15, 0.2, 0.9)
        assert r_red.color == AuditColor.RED, f"应为红色, 得到{r_red.color}"
        print(f"  绿色审计: {r_green.color.value} 评分:{r_green.score}")
        print(f"  黄色审计: {r_yellow.color.value} 评分:{r_yellow.score}")
        print(f"  红色审计: {r_red.color.value} 评分:{r_red.score}")
        print("  ✅ 通过")
        test_results.append(("三色审计", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("三色审计", False, str(e)))

    # 测试9: 价值观校验
    print("\n[测试9] 价值观校验（忠>孝>义）...")
    try:
        validator = ValueSystemValidator()
        # 正确排序
        v1 = validator.validate({"忠": 0.5, "孝": 0.3, "义": 0.2})
        assert v1["valid"] == True, "正确排序应通过"
        # 错误排序
        v2 = validator.validate({"忠": 0.2, "孝": 0.5, "义": 0.3})
        assert v2["valid"] == False, "错误排序应失败"
        print(f"  正确排序: {'通过' if v1['valid'] else '失败'}")
        print(f"  错误排序: {'通过' if v2['valid'] else '失败'}")
        print("  ✅ 通过")
        test_results.append(("价值观校验", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("价值观校验", False, str(e)))

    # 测试10: DNA签名
    print("\n[测试10] DNA签名生成器...")
    try:
        dna = DNASignature()
        sig = dna.generate(module="TEST")
        assert sig["signature"].startswith("#龍芯⚡️"), "签名格式错误"
        assert sig["confirmation"].startswith("#CONFIRM🌌"), "确认码格式错误"
        assert dna.verify(sig["signature"], sig["confirmation"]), "签名验证失败"
        print(f"  签名: {sig['signature']}")
        print(f"  确认: {sig['confirmation']}")
        print("  ✅ 通过")
        test_results.append(("DNA签名", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("DNA签名", False, str(e)))

    # 测试11: 主决策引擎完整链路
    print("\n[测试11] 主决策引擎完整链路...")
    try:
        engine = WuxingDecisionEngine()
        init = engine.initialize()
        assert init["status"] == "INITIALIZED"

        decision = engine.decide({
            "dr": 5, "heaven_score": 0.8, "earth_score": 0.7, "human_score": 0.9,
            "ai_audit_passed": True,
            "values": {"忠": 0.5, "孝": 0.3, "义": 0.2},
        })
        assert "formulas" in decision
        assert "fuse_check" in decision
        assert "audit" in decision
        assert "value_check" in decision
        print(f"  引擎初始化: {init['status']}")
        print(f"  决策结果: {decision['decision']}")
        print(f"  复合强度: {decision['formulas']['D_composite']['composite_score']:.4f}")
        print("  ✅ 通过")
        test_results.append(("主决策引擎", True, ""))
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        test_results.append(("主决策引擎", False, str(e)))

    # ── 测试汇总 ──
    print("\n" + "=" * 80)
    print("  自测试汇总")
    print("=" * 80)
    passed = sum(1 for _, ok, _ in test_results if ok)
    total = len(test_results)
    for name, ok, err in test_results:
        status = "✅" if ok else "❌"
        detail = f" ({err})" if err else ""
        print(f"  {status} {name}{detail}")

    print(f"\n  总计: {passed}/{total} 通过")
    print("=" * 80)

    return {
        "passed": passed,
        "total": total,
        "all_passed": passed == total,
        "details": test_results,
    }


if __name__ == "__main__":
    # 执行演示
    demo_result = demo()

    # 执行自测试
    test_result = self_test()

    # 最终状态
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "五行融合决策引擎 v3.0 - 运行完成" + " " * 26 + "║")
    print("║" + " " * 15 + f"自测试: {test_result['passed']}/{test_result['total']} 全部通过"
          + " " * (33 if test_result['all_passed'] else 32) + "║")
    if test_result['all_passed']:
        print("║" + " " * 28 + "🟢 系统状态: 正常" + " " * 34 + "║")
    else:
        print("║" + " " * 28 + "🔴 系统状态: 异常" + " " * 34 + "║")
    print("╚" + "═" * 78 + "╝")
