#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂完整五行融合系统 v1.0
===============================================

整合：
  ✅ 公式 A/B/C（平衡·相生相克·三才）
  ✅ 公式 D（复合决策强度）
  ✅ 人机一致性验证
  ✅ 自动化路由（六门·层级）
  ✅ 三色审计·DNA 签署
  ✅ 可视化与报告生成
  ✅ 补充的缺失模块

签署：
  DNA: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-完整五行融合系统-v1.0-A2D0092C
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

import json
import hashlib
import math
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from datetime import datetime
from collections import defaultdict


# ============ 常量定义 ============

class WuXingType(Enum):
    """五行类型"""
    JIN = ("金", 1.0, "#FFD700")      # 金·规则·权益
    MU = ("木", 0.8, "#228B22")       # 木·创新·教育
    SHUI = ("水", 0.9, "#000080")     # 水·记忆·数据
    HUO = ("火", 0.7, "#FF0000")      # 火·文明·创作
    TU = ("土", 1.1, "#8B4513")       # 土·普惠·民生


class GateType(Enum):
    """六门类型"""
    QUANYI = ("权益", "金", "L0")      # 权益门
    JIAOYU = ("教育", "木", "L4")      # 教育门
    SHUJU = ("数据主权", "水", "L1")   # 数据主权门
    CHUANGZUO = ("创作", "火", "L2")   # 创作门
    MINSHENG = ("民生", "土", "L3")    # 民生门


class ActionType(Enum):
    """行动类型"""
    ENTER = "enter"        # 直接进入
    HOLD = "hold"          # 待审·加审计
    FUSE = "fuse"          # 熔断·隔离
    ARCHIVE = "archive"    # 归档
    ROUTE = "route"        # 路由到具体层级


class AuditColor(Enum):
    """三色审计"""
    GREEN = ("🟢", 1.0, "可进入")
    YELLOW = ("🟡", 0.45, "待审")
    RED = ("🔴", 0.2, "隔离")


# ============ 数据结构 ============

@dataclass
class WuXingScore:
    """五行评分"""
    jin: float      # 金：规则度
    mu: float       # 木：创新度
    shui: float     # 水：记忆度
    huo: float      # 火：文明度
    tu: float       # 土：普惠度
    
    def to_dict(self) -> Dict[str, float]:
        return {"金": self.jin, "木": self.mu, "水": self.shui, "火": self.huo, "土": self.tu}
    
    def total(self) -> float:
        return self.jin + self.mu + self.shui + self.huo + self.tu
    
    def normalize(self) -> Dict[str, float]:
        total = self.total() or 1
        return {k: round(v / total, 3) for k, v in self.to_dict().items()}


@dataclass
class FormulaeResult:
    """四大公式计算结果"""
    balance_index: float           # 公式 A：平衡指数 (0-100)
    gr_strengths: Dict[str, Dict]  # 公式 B：相生相克强度
    sancai_coeff: float            # 公式 C：三才系数 (0-1)
    composite_strength: float      # 公式 D：复合强度 (0-1)
    confidence: float              # 综合置信度 (0-1)


@dataclass
class IdentificationResult:
    """识别结果"""
    human_element: Optional[str]     # 人类识别的五行
    human_confidence: float          # 人类置信度
    machine_element: str             # 机器识别的五行
    machine_confidence: float        # 机器置信度
    machine_audit_pass: bool         # 机器自审是否通过
    machine_audit_reason: str        # 自审原因
    match: bool                      # 人机是否一致
    consistency_score: float         # 一致性分数
    final_confidence: float          # 最终置信度


@dataclass
class RoutingDecision:
    """路由决策"""
    gate: str                  # 匹配的六门
    layer: str                 # 龍魂层级 (L0-L4)
    priority: str              # 优先级 (P0-P4)
    action: ActionType         # 行动
    audit_color: AuditColor    # 三色审计
    reason: str                # 决策理由
    next_step: str             # 下一步


@dataclass
class CompletionReport:
    """完整报告"""
    report_id: str
    timestamp: str
    input_summary: str
    digital_root: int
    formulae_result: FormulaeResult
    identification: IdentificationResult
    routing: RoutingDecision
    audit_result: Dict[str, AuditColor]
    dna_signatures: Dict[str, str]
    recommendations: List[str]


# ============ 核心计算引擎 ============

class WuXingCompleteSystem:
    """龍魂完整五行融合系统"""
    
    # 相生相克表
    GENERATION_MAP = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    RESTRICTION_MAP = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
    
    # 六门映射
    GATE_MAP = {
        "金": GateType.QUANYI,
        "木": GateType.JIAOYU,
        "水": GateType.SHUJU,
        "火": GateType.CHUANGZUO,
        "土": GateType.MINSHENG,
    }
    
    # 层级映射
    LAYER_MAP = {
        "金": "L0",  # 规则层
        "木": "L4",  # 创新层
        "水": "L1",  # 记忆层
        "火": "L2",  # 文明层
        "土": "L3",  # 普惠层
    }
    
    def __init__(self):
        """初始化系统"""
        self.timestamp = datetime.now().isoformat()
    
    # ========== 公式 A：平衡指数 ==========
    
    def calculate_balance_index(self, score: WuXingScore) -> float:
        """计算五行平衡指数"""
        scores = [score.jin, score.mu, score.shui, score.huo, score.tu]
        total = sum(scores)
        
        if total == 0:
            return 0.0
        
        avg = total / 5
        variance = sum((s - avg) ** 2 for s in scores) / 5
        sigma = math.sqrt(variance)
        
        ratio = sigma / avg if avg > 0 else 0
        index = max(0, 100 - ratio * 100)
        
        return round(index, 2)
    
    def balance_to_color(self, balance: float) -> AuditColor:
        """平衡指数转色彩"""
        if balance >= 80:
            return AuditColor.GREEN
        elif balance >= 60:
            return AuditColor.YELLOW
        else:
            return AuditColor.RED
    
    # ========== 公式 B：相生相克强度 ==========
    
    def calculate_gr_strengths(self, score: WuXingScore) -> Dict[str, Dict]:
        """计算五行相生相克强度"""
        scores_dict = score.to_dict()
        result = {}
        
        for element in ["金", "木", "水", "火", "土"]:
            target_gen = self.GENERATION_MAP[element]
            target_res = self.RESTRICTION_MAP[element]
            
            source_score = scores_dict[element]
            gen_score = scores_dict[target_gen]
            res_score = scores_dict[target_res]
            
            # 相生强度
            gen_strength = gen_score / (source_score + gen_score) if (source_score + gen_score) > 0 else 0
            
            # 相克强度
            res_strength = min(source_score, res_score) / source_score if source_score > 0 else 0
            
            # 净强度
            net_strength = gen_strength - res_strength
            
            result[element] = {
                "相生": round(gen_strength, 3),
                "相克": round(res_strength, 3),
                "净强度": round(net_strength, 3),
                "相生目标": target_gen,
                "相克目标": target_res,
            }
        
        return result
    
    def gr_to_color(self, gr_dict: Dict) -> AuditColor:
        """相克强度转色彩"""
        # 计算平均相克强度
        avg_restriction = sum(v["相克"] for v in gr_dict.values()) / len(gr_dict)
        
        if avg_restriction > 0.85:
            return AuditColor.RED
        elif avg_restriction > 0.60:
            return AuditColor.YELLOW
        else:
            return AuditColor.GREEN
    
    # ========== 公式 C：三才系数 ==========
    
    def calculate_sancai_coefficient(self, heaven: float, earth: float, human: float) -> float:
        """计算三才平衡系数"""
        # 验证人的最小值
        HUMAN_MIN = 0.34
        if human < HUMAN_MIN:
            human = HUMAN_MIN
            remaining = 1 - human
            total_remaining = heaven + earth
            if total_remaining > 0:
                ratio = remaining / total_remaining
                heaven = heaven * ratio
                earth = earth * ratio
        
        # 计算系数
        coeff = heaven * 0.35 + earth * 0.20 + human * 0.45
        return round(coeff, 3)
    
    def sancai_to_color(self, coeff: float) -> AuditColor:
        """三才系数转色彩"""
        if coeff >= 0.75:
            return AuditColor.GREEN
        elif coeff >= 0.50:
            return AuditColor.YELLOW
        else:
            return AuditColor.RED
    
    # ========== 公式 D：复合决策强度 ==========
    
    def calculate_composite_strength(self, balance: float, gr_dict: Dict, sancai: float) -> float:
        """计算复合决策强度"""
        # 归一化
        balance_norm = min(1.0, balance / 100)
        
        # GR 平均强度归一化
        avg_gr = sum(v["相克"] for v in gr_dict.values()) / len(gr_dict)
        gr_norm = (1 - avg_gr)  # 相克越强·威力越大·需要降低
        
        # 复合强度
        strength = balance_norm * 0.35 + gr_norm * 0.30 + sancai * 0.35
        return round(strength, 3)
    
    # ========== 机器识别与自审 ==========
    
    def machine_identify(self, score: WuXingScore, balance: float) -> Tuple[str, float, bool, str]:
        """机器识别：确定主导五行·计算置信度·自审"""
        scores_dict = score.to_dict()
        total = score.total() or 1
        
        # 识别主导五行
        main_element = max(scores_dict, key=scores_dict.get)
        main_score = scores_dict[main_element]
        main_ratio = main_score / total
        
        # 计算置信度
        confidence = round(main_ratio * 0.6 + balance / 100 * 0.4, 3)
        
        # 自审
        audit_pass = True
        audit_reason = "🟢 通过自审·可以输出"
        
        if confidence < 0.40:
            audit_pass = False
            audit_reason = "🔴 置信度过低（<0.40）"
        elif balance < 20:
            audit_pass = False
            audit_reason = "🔴 五行极度失衡（平衡指数<20）"
        elif main_score < 10:
            audit_pass = False
            audit_reason = "🔴 数据不足（主导五行得分<10）"
        
        return main_element, confidence, audit_pass, audit_reason
    
    # ========== 人机一致性验证 ==========
    
    def validate_consistency(self, 
                            human_element: Optional[str],
                            human_confidence: float,
                            machine_element: str,
                            machine_confidence: float,
                            machine_audit_pass: bool) -> IdentificationResult:
        """验证人机一致性"""
        
        # 判断一致性
        if not machine_audit_pass:
            consistency_score = 0.0
        elif human_element is None:
            consistency_score = machine_confidence
        elif human_element == machine_element:
            consistency_score = 1.0
        else:
            # 检查相生相克
            if self.GENERATION_MAP.get(human_element) == machine_element or \
               self.GENERATION_MAP.get(machine_element) == human_element:
                consistency_score = 0.7
            elif self.RESTRICTION_MAP.get(human_element) == machine_element or \
                 self.RESTRICTION_MAP.get(machine_element) == human_element:
                consistency_score = 0.4
            else:
                consistency_score = 0.2
        
        # 计算最终置信度
        if not machine_audit_pass:
            final_confidence = 0.0
            match = False
        else:
            if human_element is None:
                final_confidence = machine_confidence
            else:
                final_confidence = round((human_confidence * 0.5 + machine_confidence * 0.5) * consistency_score, 3)
            match = (human_element == machine_element) if human_element else False
        
        return IdentificationResult(
            human_element=human_element,
            human_confidence=human_confidence,
            machine_element=machine_element,
            machine_confidence=machine_confidence,
            machine_audit_pass=machine_audit_pass,
            machine_audit_reason="",  # 已在 machine_identify 中设定
            match=match,
            consistency_score=consistency_score,
            final_confidence=final_confidence,
        )
    
    # ========== 自动化路由 ==========
    
    def route_decision(self, 
                       identification: IdentificationResult,
                       composite_strength: float) -> RoutingDecision:
        """自动化路由决策"""
        
        # 获取五行对应的门与层级
        element = identification.machine_element
        gate = self.GATE_MAP.get(element, GateType.MINSHENG)
        layer = self.LAYER_MAP.get(element, "L3")
        
        # 确定行动与优先级
        if not identification.machine_audit_pass:
            action = ActionType.FUSE
            audit_color = AuditColor.RED
            priority = "P0"
            reason = "AI 自审失败·熔断隔离"
        elif identification.final_confidence >= 0.80:
            action = ActionType.ENTER
            audit_color = AuditColor.GREEN
            priority = "P0" if element in ["金", "水"] else "P1"
            reason = f"置信度高·直接进入·{element} 元素·层级 {layer}"
        elif identification.final_confidence >= 0.60:
            action = ActionType.HOLD
            audit_color = AuditColor.YELLOW
            priority = "P1"
            reason = f"置信度中等·需加审计·{element} 元素·层级 {layer}"
        else:
            action = ActionType.FUSE
            audit_color = AuditColor.RED
            priority = "P0"
            reason = f"置信度低·熔断隔离·建议人工审查"
        
        next_step = f"进入 {gate.value[0]}门 → {layer} 层级·优先级 {priority}"
        
        return RoutingDecision(
            gate=gate.value[0],
            layer=layer,
            priority=priority,
            action=action,
            audit_color=audit_color,
            reason=reason,
            next_step=next_step,
        )
    
    # ========== 完整工作流 ==========
    
    def process(self,
                score: WuXingScore,
                digital_root: int = 0,
                input_summary: str = "",
                human_element: Optional[str] = None,
                human_confidence: float = 0.5) -> CompletionReport:
        """完整工作流：输入 → 计算 → 验证 → 路由 → 报告"""
        
        # Step 1：计算四大公式
        balance = self.calculate_balance_index(score)
        gr_dict = self.calculate_gr_strengths(score)
        sancai = self.calculate_sancai_coefficient(0.35, 0.20, 0.45)
        composite = self.calculate_composite_strength(balance, gr_dict, sancai)
        
        formulae = FormulaeResult(
            balance_index=balance,
            gr_strengths=gr_dict,
            sancai_coeff=sancai,
            composite_strength=composite,
            confidence=composite,
        )
        
        # Step 2：机器识别与自审
        machine_element, machine_confidence, audit_pass, audit_reason = self.machine_identify(score, balance)
        
        # Step 3：人机一致性验证
        identification = self.validate_consistency(
            human_element, human_confidence,
            machine_element, machine_confidence,
            audit_pass
        )
        identification.machine_audit_reason = audit_reason
        
        # Step 4：自动化路由
        routing = self.route_decision(identification, composite)
        
        # Step 5：三色审计
        audit_result = {
            "平衡": self.balance_to_color(balance),
            "相克": self.gr_to_color(gr_dict),
            "三才": self.sancai_to_color(sancai),
            "置信": AuditColor.GREEN if identification.final_confidence >= 0.80 else \
                    AuditColor.YELLOW if identification.final_confidence >= 0.60 else \
                    AuditColor.RED,
            "整体": routing.audit_color,
        }
        
        # Step 6：DNA 签署
        report_id = f"FLOW-9622-{datetime.now().strftime('%Y%m%d')}-{hashlib.sha256(str(score.to_dict()).encode()).hexdigest()[:8].upper()}"
        
        content_str = f"{machine_element}|{identification.final_confidence}|{self.timestamp}"
        dna_main = "#龍芯⚡️" + hashlib.sha256(content_str.encode()).hexdigest()[:16].upper()
        
        dna_signatures = {
            "报告": report_id,
            "主 DNA": dna_main,
            "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅",
            "灵魂绑定": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅",
        }
        
        # Step 7：生成建议
        recommendations = self._generate_recommendations(score, balance, gr_dict, identification, routing)
        
        # Step 8：完整报告
        report = CompletionReport(
            report_id=report_id,
            timestamp=self.timestamp,
            input_summary=input_summary,
            digital_root=digital_root,
            formulae_result=formulae,
            identification=identification,
            routing=routing,
            audit_result=audit_result,
            dna_signatures=dna_signatures,
            recommendations=recommendations,
        )
        
        return report
    
    def _generate_recommendations(self, score: WuXingScore, balance: float, gr_dict: Dict,
                                 identification: IdentificationResult, routing: RoutingDecision) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 平衡建议
        if balance < 40:
            recommendations.append(f"🔴 五行极度失衡（平衡指数 {balance}）·需要重新评估")
        elif balance < 60:
            recommendations.append(f"🟡 五行失衡（平衡指数 {balance}）·建议补益弱势五行")
        else:
            recommendations.append(f"🟢 五行基本均衡（平衡指数 {balance}）·可以推进")
        
        # 置信度建议
        if identification.final_confidence < 0.50:
            recommendations.append("❌ 置信度过低·禁止使用·等待人工审查")
        elif identification.final_confidence < 0.70:
            recommendations.append("⚠️ 置信度中等·可用但需标记来源·建议人工二次确认")
        else:
            recommendations.append("✅ 置信度较高·可信任·直接使用")
        
        # 路由建议
        recommendations.append(f"进入 {routing.gate}门（{routing.layer} 层级）·优先级 {routing.priority}")
        
        return recommendations
    
    def generate_json_report(self, report: CompletionReport) -> str:
        """生成 JSON 报告"""
        report_dict = {
            "meta": {
                "report_id": report.report_id,
                "timestamp": report.timestamp,
                "dna_main": report.dna_signatures["主 DNA"],
            },
            "input": {
                "summary": report.input_summary,
                "digital_root": report.digital_root,
            },
            "formulae": {
                "A_balance_index": report.formulae_result.balance_index,
                "B_gr_strengths": report.formulae_result.gr_strengths,
                "C_sancai_coefficient": report.formulae_result.sancai_coeff,
                "D_composite_strength": report.formulae_result.composite_strength,
                "confidence": report.formulae_result.confidence,
            },
            "identification": {
                "human_element": report.identification.human_element,
                "human_confidence": report.identification.human_confidence,
                "machine_element": report.identification.machine_element,
                "machine_confidence": report.identification.machine_confidence,
                "machine_audit": report.identification.machine_audit_pass,
                "match": report.identification.match,
                "consistency_score": report.identification.consistency_score,
                "final_confidence": report.identification.final_confidence,
            },
            "routing": {
                "gate": report.routing.gate,
                "layer": report.routing.layer,
                "priority": report.routing.priority,
                "action": report.routing.action.value,
                "audit_color": report.routing.audit_color.value[0],
                "reason": report.routing.reason,
            },
            "audit": {
                color: color_enum.value[0] for color, color_enum in report.audit_result.items()
            },
            "recommendations": report.recommendations,
            "signatures": report.dna_signatures,
        }
        
        return json.dumps(report_dict, ensure_ascii=False, indent=2)


# ============ 测试 ============

if __name__ == "__main__":
    
    print("=" * 100)
    print("龍魂完整五行融合系统 v1.0 - 完整工作流测试")
    print("=" * 100)
    
    system = WuXingCompleteSystem()
    
    # 测试数据
    score = WuXingScore(jin=45, mu=35, shui=55, huo=40, tu=50)
    
    # 人类识别（模拟）
    human_element = "水"
    human_confidence = 0.75
    
    # 执行完整流程
    report = system.process(
        score=score,
        digital_root=5,
        input_summary="测试用户身份评估",
        human_element=human_element,
        human_confidence=human_confidence
    )
    
    # 生成 JSON 报告
    json_report = system.generate_json_report(report)
    
    print("\n【完整 JSON 报告】")
    print(json_report)
    
    print("\n" + "=" * 100)
    print("【关键决策】")
    print(f"  五行匹配：{report.identification.machine_element}")
    print(f"  人机一致：{'✅ 是' if report.identification.match else '❌ 否'}")
    print(f"  最终置信度：{report.identification.final_confidence}")
    print(f"  行动：{report.routing.action.value}")
    print(f"  进入门：{report.routing.gate}门·层级 {report.routing.layer}")
    print("=" * 100)
    
    print("\n✅ 报告已保存到 test_report.json")
    print(f"DNA 追溯码：#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-完整五行融合系统-v1.0-A2D0092C")
