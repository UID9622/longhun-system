#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂系统·模块 I：知识图谱与关联挖掘 v1.0
===============================================

功能：
  构建龍魂决策知识图谱 → 实体识别 → 关联分析 → 智能推理

知识维度：
  1. 五行知识：五行特性·相生相克·调理方案
  2. 决策知识：历史决策·结果反馈·成功模式
  3. 人员知识：角色·权限·决策偏好·能力模型
  4. 组织知识：部门·流程·规则·文化价值
  5. 外部知识：市场·竞争·政策·趋势

关联挖掘：
  → 决策影响关系：决策 → 五行变化 → 实际结果
  → 相似决策聚类：找到相似决策·复用经验
  → 风险关联：决策→风险因子→应急方案
  → 机会发现：隐藏的关联·未被开发的机遇

签署：
  DNA: #龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-模块I-知识图谱与关联挖掘-v1.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
from datetime import datetime
import hashlib
import json


# ============ 知识图谱常量 ============

class EntityType(Enum):
    """实体类型"""
    WUXING = "五行"              # 五行元素
    DECISION = "决策"             # 决策事件
    PERSON = "人员"               # 人员角色
    DEPARTMENT = "部门"           # 组织部门
    PROCESS = "流程"              # 业务流程
    RISK = "风险"                 # 风险因子
    OPPORTUNITY = "机遇"          # 机遇
    PATTERN = "模式"              # 成功模式


class RelationType(Enum):
    """关系类型"""
    # 五行关系
    GENERATES = "相生"            # A 相生 B
    RESTRICTS = "相克"            # A 相克 B
    SIMILAR = "相似"              # A 相似 B
    
    # 决策关系
    IMPACTS = "影响"              # 决策影响五行
    CAUSED_BY = "源于"            # 结果源于决策
    BELONGS_TO = "属于"           # 决策属于某流程
    
    # 人员关系
    OWNS = "拥有"                 # 人员拥有角色
    MANAGES = "管理"              # 人员管理部门
    PREFERS = "偏好"              # 人员偏好某五行
    
    # 组织关系
    CONTAINS = "包含"             # 部门包含人员
    FOLLOWS = "遵循"              # 部门遵循规则
    
    # 风险关系
    TRIGGERS = "触发"             # 决策触发风险
    MITIGATES = "缓解"            # 方案缓解风险
    
    # 机遇关系
    ENABLES = "启用"              # 决策启用机遇
    REQUIRES = "需要"             # 机遇需要某决策


# ============ 知识图谱数据结构 ============

@dataclass
class Entity:
    """知识图谱实体"""
    entity_id: str
    entity_type: EntityType
    name: str
    properties: Dict[str, any] = field(default_factory=dict)
    
    # 元数据
    created_time: datetime = field(default_factory=datetime.now)
    confidence: float = 0.9  # 置信度
    source: str = ""  # 数据来源
    description: str = ""


@dataclass
class Relation:
    """知识图谱关系"""
    relation_id: str
    source_entity_id: str    # 源实体
    target_entity_id: str    # 目标实体
    relation_type: RelationType
    
    # 强度指标
    strength: float = 0.8    # 关系强度 0-1
    confidence: float = 0.8  # 置信度
    
    # 元数据
    created_time: datetime = field(default_factory=datetime.now)
    source: str = ""  # 数据来源
    evidence: List[str] = field(default_factory=list)  # 证据
    description: str = ""


@dataclass
class KnowledgePath:
    """知识路径（推理路径）"""
    path_id: str
    start_entity: Entity
    end_entity: Entity
    relations: List[Relation]
    
    # 路径特性
    length: int  # 路径长度
    strength: float  # 路径强度（各关系强度的乘积）
    confidence: float  # 整体置信度
    
    # 推理结果
    conclusion: str = ""
    implication: str = ""


@dataclass
class CorrelationAnalysis:
    """关联分析结果"""
    decision_id: str
    
    # 直接影响
    direct_impacts: Dict[str, float]  # 实体 → 影响强度
    
    # 间接影响（多跳）
    indirect_impacts: Dict[str, float]
    
    # 相关决策
    similar_decisions: List[Tuple[str, float]]  # (决策ID, 相似度)
    
    # 风险与机遇
    associated_risks: List[str]
    opportunities: List[str]
    
    # 推荐行动
    recommendations: List[str]


# ============ 知识图谱引擎 ============

class KnowledgeGraphEngine:
    """知识图谱与关联挖掘引擎"""
    
    def __init__(self):
        """初始化知识图谱引擎"""
        self.entities: Dict[str, Entity] = {}
        self.relations: Dict[str, Relation] = {}
        
        # 推理缓存
        self.paths_cache: Dict[str, List[KnowledgePath]] = {}
        self.correlation_cache: Dict[str, CorrelationAnalysis] = {}
        
        # 统计信息
        self.stats = {
            "total_entities": 0,
            "total_relations": 0,
            "entity_types": {},
            "relation_types": {},
        }
        
        # 初始化基础五行知识
        self._initialize_wuxing_knowledge()
    
    def _initialize_wuxing_knowledge(self):
        """初始化基础五行知识"""
        # 五行实体
        wuxing_entities = {
            "jin": ("金", "坚决·规则·边界·执行"),
            "mu": ("木", "成长·计划·创新·连接"),
            "shui": ("水", "智慧·流动·隐藏·适应"),
            "huo": ("火", "热情·表达·文化·光明"),
            "tu": ("土", "承载·稳定·中心·滋养"),
        }
        
        for key, (name, desc) in wuxing_entities.items():
            entity = Entity(
                entity_id=f"WUXING-{key.upper()}",
                entity_type=EntityType.WUXING,
                name=name,
                description=desc,
                properties={
                    "element": key,
                    "core_value": name,
                    "characteristics": desc.split("·"),
                },
                source="System"
            )
            self.entities[entity.entity_id] = entity
        
        # 五行相生相克关系
        generates = [
            ("jin", "tu"),  # 金生土
            ("tu", "shui"), # 土生水
            ("shui", "mu"), # 水生木
            ("mu", "huo"),  # 木生火
            ("huo", "jin"), # 火生金
        ]
        
        restricts = [
            ("jin", "mu"),  # 金克木
            ("mu", "tu"),   # 木克土
            ("tu", "shui"), # 土克水
            ("shui", "huo"), # 水克火
            ("huo", "jin"), # 火克金
        ]
        
        for src, tgt in generates:
            self._add_relation(
                f"WUXING-{src.upper()}", f"WUXING-{tgt.upper()}",
                RelationType.GENERATES, 0.9, "Five Elements Theory"
            )
        
        for src, tgt in restricts:
            self._add_relation(
                f"WUXING-{src.upper()}", f"WUXING-{tgt.upper()}",
                RelationType.RESTRICTS, 0.9, "Five Elements Theory"
            )
    
    # ========== 实体管理 ==========
    
    def add_entity(self, entity: Entity) -> Entity:
        """添加实体"""
        self.entities[entity.entity_id] = entity
        
        # 更新统计
        self.stats["total_entities"] += 1
        entity_type = entity.entity_type.value
        self.stats["entity_types"][entity_type] = \
            self.stats["entity_types"].get(entity_type, 0) + 1
        
        return entity
    
    def _add_relation(self, src_id: str, tgt_id: str, 
                     rel_type: RelationType, strength: float,
                     source: str) -> Relation:
        """添加关系"""
        rel_id = f"REL-{hashlib.sha256(f'{src_id}{tgt_id}{rel_type.value}'.encode()).hexdigest()[:12].upper()}"
        
        relation = Relation(
            relation_id=rel_id,
            source_entity_id=src_id,
            target_entity_id=tgt_id,
            relation_type=rel_type,
            strength=strength,
            confidence=0.9,
            source=source,
        )
        
        self.relations[rel_id] = relation
        
        # 更新统计
        self.stats["total_relations"] += 1
        rel_type_name = rel_type.value
        self.stats["relation_types"][rel_type_name] = \
            self.stats["relation_types"].get(rel_type_name, 0) + 1
        
        return relation
    
    # ========== 决策知识提取 ==========
    
    def extract_decision_knowledge(self, decision_report: Dict[str, Any]) -> Entity:
        """
        从决策报告提取决策知识
        """
        decision_id = decision_report.get("meta", {}).get("report_id", "DECISION-UNKNOWN")
        
        # 提取主要五行
        main_element = decision_report.get("identification", {}).get("machine_element", "未知")
        confidence = decision_report.get("identification", {}).get("final_confidence", 0)
        
        # 创建决策实体
        decision_entity = Entity(
            entity_id=decision_id,
            entity_type=EntityType.DECISION,
            name=f"决策-{main_element}主导",
            properties={
                "main_element": main_element,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat(),
                "formulae": decision_report.get("formulae", {}),
            },
            source="Decision Engine"
        )
        
        self.add_entity(decision_entity)
        
        # 添加决策到五行的关系
        wuxing_id = f"WUXING-{main_element.upper()}"
        if wuxing_id in self.entities:
            self._add_relation(
                decision_id, wuxing_id,
                RelationType.IMPACTS,
                strength=confidence,
                source="Decision Extraction"
            )
        
        return decision_entity
    
    # ========== 关联分析 ==========
    
    def analyze_correlations(self, decision_id: str) -> CorrelationAnalysis:
        """
        分析决策的关联影响
        """
        # 获取决策实体
        decision = self.entities.get(decision_id)
        if not decision:
            raise ValueError(f"决策不存在：{decision_id}")
        
        # 直接影响：决策直接连接的实体
        direct_impacts = {}
        for rel_id, relation in self.relations.items():
            if relation.source_entity_id == decision_id and relation.relation_type == RelationType.IMPACTS:
                target = self.entities.get(relation.target_entity_id)
                if target:
                    direct_impacts[target.name] = relation.strength
        
        # 间接影响：多跳推理
        indirect_impacts = {}
        for target_id, impact_strength in direct_impacts.items():
            # 找到该实体进一步影响的实体
            for rel_id, relation in self.relations.items():
                if relation.source_entity_id == target_id:
                    further_target = self.entities.get(relation.target_entity_id)
                    if further_target:
                        indirect_strength = impact_strength * relation.strength
                        indirect_impacts[further_target.name] = indirect_strength
        
        # 相似决策聚类
        similar_decisions = self._find_similar_decisions(decision_id)
        
        # 关联风险与机遇
        associated_risks = self._find_associated_risks(decision_id)
        opportunities = self._find_opportunities(decision_id)
        
        # 生成推荐
        recommendations = self._generate_recommendations(
            decision, direct_impacts, indirect_impacts, associated_risks
        )
        
        analysis = CorrelationAnalysis(
            decision_id=decision_id,
            direct_impacts=direct_impacts,
            indirect_impacts=indirect_impacts,
            similar_decisions=similar_decisions,
            associated_risks=associated_risks,
            opportunities=opportunities,
            recommendations=recommendations,
        )
        
        # 缓存
        self.correlation_cache[decision_id] = analysis
        
        return analysis
    
    def _find_similar_decisions(self, decision_id: str) -> List[Tuple[str, float]]:
        """找到相似决策"""
        decision = self.entities.get(decision_id)
        if not decision:
            return []
        
        similar = []
        main_element = decision.properties.get("main_element", "")
        
        # 找到有相同主导五行的决策
        for entity_id, entity in self.entities.items():
            if entity.entity_type == EntityType.DECISION and entity_id != decision_id:
                if entity.properties.get("main_element") == main_element:
                    similarity = 0.8  # 相同五行·高相似度
                    similar.append((entity_id, similarity))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)[:5]
    
    def _find_associated_risks(self, decision_id: str) -> List[str]:
        """找到关联风险"""
        risks = []
        
        # 简化版本·根据五行找风险
        decision = self.entities.get(decision_id)
        if decision:
            main_element = decision.properties.get("main_element", "")
            
            # 根据五行预定义风险
            risk_map = {
                "金": ["执行过度·忽视灵活性", "规则僵化·缺乏创新"],
                "木": ["急进·过度乐观", "计划过多·执行不足"],
                "水": ["过度谨慎·决策迟缓", "隐藏信息·缺乏透明"],
                "火": ["表面文章·虚假承诺", "热度消退·后继乏力"],
                "土": ["保守固步·拒绝变化", "责任模糊·效率低下"],
            }
            
            risks = risk_map.get(main_element, [])
        
        return risks
    
    def _find_opportunities(self, decision_id: str) -> List[str]:
        """找到机遇"""
        opportunities = []
        
        # 简化版本·根据五行找机遇
        decision = self.entities.get(decision_id)
        if decision:
            main_element = decision.properties.get("main_element", "")
            
            # 根据五行预定义机遇
            opportunity_map = {
                "金": ["建立标准·形成品牌", "制度创新·规则领先"],
                "木": ["快速扩展·市场抢占", "创新突破·产品创新"],
                "水": ["深度分析·智慧决策", "隐藏价值·数据挖掘"],
                "火": ["文化传播·品牌传播", "创意爆发·内容创新"],
                "土": ["基础巩固·能力积累", "生态完善·体系优化"],
            }
            
            opportunities = opportunity_map.get(main_element, [])
        
        return opportunities
    
    def _generate_recommendations(self, decision: Entity,
                                 direct: Dict[str, Any], indirect: Dict[str, Any],
                                 risks: List[str]) -> List[str]:
        """生成推荐"""
        recs = []
        
        # 基于直接影响
        if direct:
            primary_impact = max(direct.items(), key=lambda x: x[1])
            recs.append(f"重点监控【{primary_impact[0]}】的变化")
        
        # 基于间接影响
        if indirect:
            secondary_impact = max(indirect.items(), key=lambda x: x[1])
            recs.append(f"警惕【{secondary_impact[0]}】的间接影响")
        
        # 基于风险
        if risks:
            top_risk = risks[0]
            recs.append(f"预防风险：{top_risk}")
        
        # 通用推荐
        recs.append("定期复盘决策结果·反馈知识图谱")
        recs.append("对标相似决策·学习成功经验")
        
        return recs
    
    # ========== 报告生成 ==========
    
    def generate_knowledge_report(self, decision_id: str) -> Dict[str, Any]:
        """生成知识图谱报告"""
        if decision_id not in self.correlation_cache:
            analysis = self.analyze_correlations(decision_id)
        else:
            analysis = self.correlation_cache[decision_id]
        
        return {
            "report_id": f"KG-{decision_id}",
            "timestamp": datetime.now().isoformat(),
            
            "decision_entity": {
                "id": decision_id,
                "name": self.entities[decision_id].name if decision_id in self.entities else "未知",
            },
            
            "direct_impacts": analysis.direct_impacts,
            "indirect_impacts": analysis.indirect_impacts,
            
            "similar_decisions": [
                {
                    "decision_id": d[0],
                    "similarity": round(d[1], 3),
                } for d in analysis.similar_decisions
            ],
            
            "associated_risks": analysis.associated_risks,
            "opportunities": analysis.opportunities,
            
            "recommendations": analysis.recommendations,
            
            "graph_statistics": {
                "total_entities": self.stats["total_entities"],
                "total_relations": self.stats["total_relations"],
                "entity_types": self.stats["entity_types"],
                "relation_types": self.stats["relation_types"],
            },
            
            "DNA_signature": f"#龍芯⚡️{hashlib.sha256(f'{decision_id}{analysis}'.encode()).hexdigest()[:16].upper()}",
        }


# ============ 测试 ============

if __name__ == "__main__":
    
    print("=" * 80)
    print("龍魂系统·模块 I：知识图谱与关联挖掘 v1.0")
    print("=" * 80)
    
    # 初始化知识图谱
    kg = KnowledgeGraphEngine()
    
    print("\n【知识图谱初始化】")
    print(f"  实体数：{kg.stats['total_entities']}")
    print(f"  关系数：{kg.stats['total_relations']}")
    
    # 模拟决策报告
    sample_decision = {
        "meta": {"report_id": "FLOW-9622-20260608-KG-TEST"},
        "identification": {
            "machine_element": "水",
            "final_confidence": 0.75,
        },
        "formulae": {
            "A_balance_index": 84.29,
        }
    }
    
    # 提取决策知识
    decision_entity = kg.extract_decision_knowledge(sample_decision)
    print(f"\n✅ 决策知识已提取")
    print(f"  决策 ID：{decision_entity.entity_id}")
    print(f"  决策名称：{decision_entity.name}")
    
    # 分析关联
    analysis = kg.analyze_correlations(decision_entity.entity_id)
    print(f"\n✅ 关联分析完成")
    print(f"  直接影响：{list(analysis.direct_impacts.keys())}")
    print(f"  相似决策：{len(analysis.similar_decisions)} 个")
    print(f"  风险因子：{len(analysis.associated_risks)} 个")
    
    # 生成报告
    report = kg.generate_knowledge_report(decision_entity.entity_id)
    
    print(f"\n【知识图谱报告】")
    print(f"  报告 ID：{report['report_id']}")
    print(f"  图谱实体：{report['graph_statistics']['total_entities']}")
    print(f"  图谱关系：{report['graph_statistics']['total_relations']}")
    
    print(f"\n【关联分析】")
    print(f"  直接影响：{report['direct_impacts']}")
    for risk in report['associated_risks']:
        print(f"  风险：{risk}")
    
    print(f"\n【推荐行动】")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "=" * 80)
    print(f"DNA 追溯码：#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-模块I-知识图谱与关联挖掘-v1.0")
    print("=" * 80)
