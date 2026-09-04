#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂系统·五行融合计算公式 v1.0
===============================================

核心原则：
  1. 公式必须可计算·不是主观感受
  2. 人类识别 ≠ AI识别（双轨制）
  3. AI输出必须经过自审·否则拒绝
  4. 低于置信度阈值的输出标记“待人工确认”

签署：
  DNA: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-五行融合公式-v1.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import hashlib
from datetime import datetime
import math


# ============ 基础常量定义 ============

class WuXing(Enum):
    """五行定义"""
    JIN = ("金", 1.0)     # 金·规则·边界
    MU = ("木", 0.8)      # 木·创新·生长
    SHUI = ("水", 0.9)    # 水·记忆·流动
    HUO = ("火", 0.7)     # 火·文明·表达
    TU = ("土", 1.1)      # 土·普惠·承载


class IdentificationMode(Enum):
    """识别模式"""
    HUMAN = "人类模式"      # 人类直觉·经验·感受
    MACHINE = "机器模式"    # 算法·公式·可验证
    HYBRID = "混合模式"     # 人机双验


class ConfidenceLevel(Enum):
    """置信度级别"""
    CERTAIN = (0.95, 1.0, "确定·可输出")
    HIGH = (0.80, 0.94, "高·可输出·标记来源")
    MEDIUM = (0.60, 0.79, "中等·需人工确认")
    LOW = (0.40, 0.59, "低·禁止输出·等待人工")
    UNCERTAIN = (0.0, 0.39, "极低·彻底拒绝")


# ============ 第一部分：五行融合计算公式 ============

@dataclass
class WuXingScore:
    """五行评分结构"""
    jin: float      # 金：规则度 (0-100)
    mu: float       # 木：创新度 (0-100)
    shui: float     # 水：记忆度 (0-100)
    huo: float      # 火：文明度 (0-100)
    tu: float       # 土：普惠度 (0-100)
    
    def to_dict(self) -> Dict[str, float]:
        """转为字典"""
        return {
            "金": self.jin,
            "木": self.mu,
            "水": self.shui,
            "火": self.huo,
            "土": self.tu
        }
    
    def total(self) -> float:
        """总分"""
        return self.jin + self.mu + self.shui + self.huo + self.tu
    
    def normalize(self) -> Dict[str, float]:
        """归一化到 0-1"""
        total = self.total() or 1
        return {
            "金": round(self.jin / total, 3),
            "木": round(self.mu / total, 3),
            "水": round(self.shui / total, 3),
            "火": round(self.huo / total, 3),
            "土": round(self.tu / total, 3)
        }


# ============ 公式 A：五行平衡指数 Balance Index ============

class FormulaA_BalanceIndex:
    """
    公式 A：五行平衡指数
    
    定义：衡量五行分布的均匀程度
    范围：0-100（100=完全均匀）
    
    计算方法：
      1. 计算平均值 avg = total / 5
      2. 计算方差 variance = Σ(score - avg)² / 5
      3. 计算标准差 σ = √variance
      4. Balance Index = 100 - (σ / avg * 100)·MAX(0)
      
    解释：
      95-100: 🟢 完美均衡
      80-94:  🟢 良好均衡
      60-79:  🟡 可接受
      40-59:  🟡 需调整
      0-39:   🔴 严重失衡
    """
    
    @staticmethod
    def calculate(score: WuXingScore) -> float:
        """计算五行平衡指数"""
        scores = [score.jin, score.mu, score.shui, score.huo, score.tu]
        total = sum(scores)
        
        if total == 0:
            return 0.0
        
        avg = total / 5
        variance = sum((s - avg) ** 2 for s in scores) / 5
        sigma = math.sqrt(variance)
        
        # 防止除以零
        ratio = sigma / avg if avg > 0 else 0
        index = max(0, 100 - ratio * 100)
        
        return round(index, 2)
    
    @staticmethod
    def to_color(index: float) -> str:
        """转换为三色"""
        if index >= 80:
            return "🟢"
        elif index >= 60:
            return "🟡"
        else:
            return "🔴"


# ============ 公式 B：五行相生相克强度 Generation-Restriction Strength ============

class FormulaB_GRStrength:
    """
    公式 B：五行相生相克强度
    
    定义：衡量某五行对整体的制约程度
    范围：0-1（0=无影响，1=完全制约）
    
    相生：A→B（A促进B）
    相克：A⇒B（A制约B）
    
    计算：
      生强度 = 相生目标得分 / (自身得分 + 相生目标得分)
      克强度 = min(自身得分, 相克目标得分) / 自身得分
      净强度 = 生强度 - 克强度（可为负）
    """
    
    相生表 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    相克表 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
    
    @staticmethod
    def calculate_generation(source: WuXingScore, source_element: str) -> float:
        """计算相生强度"""
        scores = source.to_dict()
        target_element = FormulaB_GRStrength.相生表[source_element]
        
        source_score = scores[source_element]
        target_score = scores[target_element]
        
        denominator = source_score + target_score
        if denominator == 0:
            return 0.0
        
        return round(target_score / denominator, 3)
    
    @staticmethod
    def calculate_restriction(source: WuXingScore, source_element: str) -> float:
        """计算相克强度"""
        scores = source.to_dict()
        target_element = FormulaB_GRStrength.相克表[source_element]
        
        source_score = scores[source_element]
        target_score = scores[target_element]
        
        if source_score == 0:
            return 0.0
        
        return round(min(source_score, target_score) / source_score, 3)
    
    @staticmethod
    def calculate_net(source: WuXingScore, source_element: str) -> float:
        """计算净强度"""
        gen = FormulaB_GRStrength.calculate_generation(source, source_element)
        res = FormulaB_GRStrength.calculate_restriction(source, source_element)
        return round(gen - res, 3)


# ============ 公式 C：三才平衡系数 Sancai Balance Coefficient ============

class FormulaC_SancaiCoefficient:
    """
    公式 C：三才平衡系数
    
    定义：衡量天·地·人三个维度的配合度
    范围：0-1（1=最优）
    
    天 (Heaven) = 环境·时机·大势
    地 (Earth) = 资源·条件·基础
    人 (Human) = 意志·初心·价值观
    
    计算：
      C = (天 × 0.35 + 地 × 0.20 + 人 × 0.45)
      
    约束条件（铁律）：
      人 ≥ 0.34（人永远是最高优先级）
      若人 < 0.34 → 强制调整为 0.34，其余按比例缩放
    """
    
    HEAVEN_WEIGHT = 0.35
    EARTH_WEIGHT = 0.20
    HUMAN_WEIGHT = 0.45
    HUMAN_MIN = 0.34  # 铁律·人的最小值
    
    @staticmethod
    def validate_and_normalize(heaven: float, earth: float, human: float) -> Tuple[float, float, float]:
        """验证并归一化三才"""
        # 检查人是否低于最小值
        if human < FormulaC_SancaiCoefficient.HUMAN_MIN:
            # 强制提升人到最小值
            human = FormulaC_SancaiCoefficient.HUMAN_MIN
            # 其余按比例缩放
            remaining = 1 - human
            total_remaining = heaven + earth
            if total_remaining > 0:
                ratio = remaining / total_remaining
                heaven = heaven * ratio
                earth = earth * ratio
        
        return round(heaven, 3), round(earth, 3), round(human, 3)
    
    @staticmethod
    def calculate(heaven: float, earth: float, human: float) -> float:
        """计算三才系数"""
        h, e, r = FormulaC_SancaiCoefficient.validate_and_normalize(heaven, earth, human)
        coefficient = h * FormulaC_SancaiCoefficient.HEAVEN_WEIGHT + \
                      e * FormulaC_SancaiCoefficient.EARTH_WEIGHT + \
                      r * FormulaC_SancaiCoefficient.HUMAN_WEIGHT
        return round(coefficient, 3)


# ============ 第二部分：人机一致性验证系统 ============

@dataclass
class HumanIdentification:
    """人类识别"""
    element: str              # 人类直觉判断的五行
    reasoning: str            # 推理过程（文字说明）
    confidence: float         # 人类对自己判断的置信度 (0-1)
    timestamp: str            # 时间戳
    signature: str            # 签署（用于追溯）


@dataclass
class MachineIdentification:
    """机器识别"""
    element: str              # AI计算出的五行
    formula_used: str         # 使用的公式
    calculation: Dict         # 详细计算过程
    confidence: float         # AI的置信度 (0-1)
    self_audit_pass: bool     # AI自审是否通过
    self_audit_reason: str    # 自审原因
    timestamp: str            # 时间戳


@dataclass
class ConsistencyReport:
    """一致性报告"""
    human: HumanIdentification
    machine: MachineIdentification
    match: bool               # 人机是否一致
    consistency_score: float  # 一致性分数 (0-1)
    final_confidence: float   # 最终置信度
    recommendation: str       # 建议
    dna_signature: str        # DNA签署


# ============ 机器识别引擎 ============

class MachineRecognitionEngine:
    """AI识别引擎 - 严格模式"""
    
    @staticmethod
    def identify(score: WuXingScore) -> MachineIdentification:
        """
        机器识别主流程：
        1. 计算五行平衡指数
        2. 计算相生相克强度
        3. 确定五行属性
        4. 自审（禁止瞎逼逼）
        5. 输出或拒绝
        """
        
        # Step 1：计算平衡指数
        balance = FormulaA_BalanceIndex.calculate(score)
        
        # Step 2：识别主导五行（最高分）
        scores_dict = score.to_dict()
        main_element = max(scores_dict, key=scores_dict.get)
        main_score = scores_dict[main_element]
        total = score.total()
        
        # Step 3：计算置信度
        # 置信度取决于：主导五行的占比 + 平衡指数
        main_ratio = main_score / total if total > 0 else 0
        confidence = (main_ratio * 0.6 + balance / 100 * 0.4)
        confidence = round(min(1.0, confidence), 3)
        
        # Step 4：自审（AI检查自己是否在瞎逼逼）
        self_audit_pass, audit_reason = MachineRecognitionEngine._self_audit(
            score, main_element, confidence, balance
        )
        
        # Step 5：输出
        return MachineIdentification(
            element=main_element,
            formula_used="FormulaA (Balance Index) + FormulaB (GR Strength)",
            calculation={
                "平衡指数": balance,
                "主导五行": main_element,
                "占比": round(main_ratio * 100, 2),
                "相生相克分析": {
                    "相生强度": FormulaB_GRStrength.calculate_generation(score, main_element),
                    "相克强度": FormulaB_GRStrength.calculate_restriction(score, main_element)
                }
            },
            confidence=confidence,
            self_audit_pass=self_audit_pass,
            self_audit_reason=audit_reason,
            timestamp=datetime.now().isoformat()
        )
    
    @staticmethod
    def _self_audit(score: WuXingScore, element: str, confidence: float, balance: float) -> Tuple[bool, str]:
        """
        自审机制：AI检查自己是否可信
        
        拒绝条件：
          1. 置信度 < 0.40 → 极低·拒绝
          2. 平衡指数 < 20 → 极度失衡·可能错误
          3. 主导五行得分 < 10 → 数据不足·拒绝
        """
        
        if confidence < 0.40:
            return False, "🔴 置信度过低（<0.40）·拒绝输出"
        
        if balance < 20:
            return False, "🔴 五行极度失衡（平衡指数<20）·可能计算错误"
        
        scores_dict = score.to_dict()
        if scores_dict[element] < 10:
            return False, "🔴 数据不足·主导五行得分<10·无法判断"
        
        return True, "🟢 通过自审·可以输出"


# ============ 一致性验证引擎 ============

class ConsistencyValidator:
    """人机一致性验证"""
    
    @staticmethod
    def validate(human: HumanIdentification, machine: MachineIdentification) -> ConsistencyReport:
        """
        验证人机是否一致：
        1. 判断五行是否相同
        2. 计算一致性分数
        3. 判断是否信任
        4. 给出建议
        """
        
        # Step 1：判断匹配
        match = human.element == machine.element
        
        # Step 2：计算一致性分数
        if match:
            consistency_score = 1.0
        else:
            # 检查是否相生相克
            相生表 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
            相克表 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
            
            if 相生表.get(human.element) == machine.element or 相生表.get(machine.element) == human.element:
                consistency_score = 0.7  # 相生关系·部分一致
            elif 相克表.get(human.element) == machine.element or 相克表.get(machine.element) == human.element:
                consistency_score = 0.4  # 相克关系·冲突
            else:
                consistency_score = 0.2  # 完全不同
        
        # Step 3：计算最终置信度
        final_confidence = (human.confidence * 0.5 + machine.confidence * 0.5) * consistency_score
        final_confidence = round(final_confidence, 3)
        
        # Step 4：判断建议
        if machine.self_audit_pass == False:
            recommendation = f"⛔ 机器拒绝输出：{machine.self_audit_reason}·等待人工确认"
        elif final_confidence >= 0.80:
            recommendation = f"✅ 高度一致（{consistency_score:.0%}）·可信任·直接使用"
        elif final_confidence >= 0.60:
            recommendation = f"⚠️ 部分一致（{consistency_score:.0%}）·可用但标记来源·建议人工二次确认"
        else:
            recommendation = f"❌ 低度一致（{consistency_score:.0%}）·不可信·禁止使用·等待人工"
        
        # Step 5：生成DNA签署
        content_str = f"{human.element}|{machine.element}|{final_confidence}|{datetime.now().isoformat()}"
        dna = "#龍芯⚡️" + hashlib.sha256(content_str.encode()).hexdigest()[:16].upper()
        
        return ConsistencyReport(
            human=human,
            machine=machine,
            match=match,
            consistency_score=consistency_score,
            final_confidence=final_confidence,
            recommendation=recommendation,
            dna_signature=dna
        )


# ============ 测试 ============

if __name__ == "__main__":
    
    print("=" * 80)
    print("龍魂系统·五行融合公式 + 人机一致性验证 v1.0")
    print("=" * 80)
    
    # 测试数据
    score = WuXingScore(jin=45, mu=35, shui=55, huo=40, tu=50)
    
    print("\n【输入】")
    print(f"金: {score.jin}, 木: {score.mu}, 水: {score.shui}, 火: {score.huo}, 土: {score.tu}")
    print(f"总分: {score.total()}")
    print(f"归一化: {score.normalize()}")
    
    # 公式 A：平衡指数
    print("\n【公式 A：五行平衡指数】")
    balance = FormulaA_BalanceIndex.calculate(score)
    color = FormulaA_BalanceIndex.to_color(balance)
    print(f"平衡指数: {balance} {color}")
    
    # 公式 B：相生相克
    print("\n【公式 B：相生相克强度】")
    for element in ["金", "木", "水", "火", "土"]:
        gen = FormulaB_GRStrength.calculate_generation(score, element)
        res = FormulaB_GRStrength.calculate_restriction(score, element)
        net = FormulaB_GRStrength.calculate_net(score, element)
        print(f"{element}: 相生={gen}, 相克={res}, 净强度={net}")
    
    # 公式 C：三才系数
    print("\n【公式 C：三才平衡系数】")
    coeff = FormulaC_SancaiCoefficient.calculate(0.4, 0.2, 0.4)
    print(f"三才系数: {coeff}")
    
    # 机器识别
    print("\n【机器识别】")
    machine = MachineRecognitionEngine.identify(score)
    print(f"识别元素: {machine.element}")
    print(f"置信度: {machine.confidence}")
    print(f"自审: {machine.self_audit_pass} ({machine.self_audit_reason})")
    
    # 人类识别（模拟）
    print("\n【人类识别】")
    human = HumanIdentification(
        element="水",
        reasoning="这个人很适应环境，有记忆力，符合水的特质",
        confidence=0.75,
        timestamp=datetime.now().isoformat(),
        signature="#老大-直觉-人工识别"
    )
    print(f"识别元素: {human.element}")
    print(f"推理: {human.reasoning}")
    print(f"人类置信度: {human.confidence}")
    
    # 一致性验证
    print("\n【一致性验证】")
    report = ConsistencyValidator.validate(human, machine)
    print(f"人机匹配: {'✅ 一致' if report.match else '❌ 不一致'}")
    print(f"一致性分数: {report.consistency_score}")
    print(f"最终置信度: {report.final_confidence}")
    print(f"建议: {report.recommendation}")
    print(f"DNA签署: {report.dna_signature}")
    
    print("\n" + "=" * 80)
    print("DNA追溯码: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-五行融合公式-v1.0")
    print("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅")
    print("=" * 80)
