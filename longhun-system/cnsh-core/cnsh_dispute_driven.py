#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRAIN_GATE v1.1 受保护文件
# DNA: #龍芯⚡️20260324-CNSH_DISPUTE_DRIVEN
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 | 未经授权修改视为P0违规
"""
CNSH-64 争议驱动分化系统
═══════════════════════════════════════════════════════════════
核心信条：争议来了不删除、不压制、不融合，而是拆成多个

大哥的底层逻辑：
- 任何规则、协议、模块、逻辑、数据库、页面、模型、交互、甚至骂人记录
  都不是"固定成品"，而是可以被拆、被分、被重组的种子
- 争议来了？重复了？冲突了？
  不删除、不压制、不融合，而是拆成两个、甚至多个
- 拆完后，每一个分支都自带独立的松紧度、自适应规则、DNA追溯

功能：
1. 争议检测
2. 自动/手动拆分
3. 松紧度自适应
4. 分叉树管理
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Dispute-Driven')


class DisputeType(Enum):
    """争议类型"""
    VALUE_CONFLICT = "value_conflict"       # 价值观冲突
    RULE_CONFLICT = "rule_conflict"         # 规则冲突
    IMPLEMENTATION = "implementation"       # 实现分歧
    PRIORITY = "priority"                   # 优先级争议
    REPETITION = "repetition"               # 重复/冗余


@dataclass
class Dispute:
    """争议"""
    dispute_id: str
    dispute_type: DisputeType
    description: str
    involved_parties: List[str]             # 涉及方DNA
    original_entity: str                    # 原始实体
    timestamp: float
    severity: float                         # 严重程度 0-100


@dataclass
class Fork:
    """分叉"""
    fork_id: str
    parent_id: str                          # 父实体ID
    dispute_id: str                         # 引发的争议ID
    tightness_level: float                  # 松紧度 0-100
    dna_lineage: List[str]                  # DNA血统
    created_at: float
    status: str                             # active/merged/abandoned


class DisputeDetector:
    """
    争议检测器
    
    检测各种争议，触发分化
    """
    
    def __init__(self):
        self.disputes: Dict[str, Dispute] = {}
        self.detection_rules = {
            DisputeType.VALUE_CONFLICT: [
                r'价值观.*冲突',
                r'理念.*不同',
                r'原则.*分歧',
            ],
            DisputeType.RULE_CONFLICT: [
                r'规则.*冲突',
                r'标准.*不一',
                r'定义.*分歧',
            ],
            DisputeType.IMPLEMENTATION: [
                r'实现.*分歧',
                r'技术.*争议',
                r'方案.*不同',
            ],
            DisputeType.PRIORITY: [
                r'优先级.*争议',
                r'重要.*分歧',
                r'先后.*争议',
            ],
            DisputeType.REPETITION: [
                r'重复.*冗余',
                r'功能.*重叠',
                r'代码.*重复',
            ]
        }
        
    def detect(self, content: str, 
               involved_parties: List[str],
               original_entity: str) -> Optional[Dispute]:
        """
        检测争议
        """
        import re
        
        for dispute_type, patterns in self.detection_rules.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    dispute_id = hashlib.sha256(
                        f"DISPUTE:{original_entity}:{time.time()}".encode()
                    ).hexdigest()[:16]
                    
                    dispute = Dispute(
                        dispute_id=dispute_id,
                        dispute_type=dispute_type,
                        description=content[:100],
                        involved_parties=involved_parties,
                        original_entity=original_entity,
                        timestamp=time.time(),
                        severity=50.0  # 默认中等严重
                    )
                    
                    self.disputes[dispute_id] = dispute
                    
                    logger.info(f"⚡ 争议检测: {dispute_type.value}")
                    logger.info(f"   描述: {dispute.description}")
                    logger.info(f"   涉及方: {involved_parties}")
                    
                    return dispute
        
        return None
    
    def get_disputes_by_entity(self, entity_id: str) -> List[Dispute]:
        """获取实体的所有争议"""
        return [d for d in self.disputes.values() if d.original_entity == entity_id]


class AdaptiveTightness:
    """
    自适应松紧度
    
    根据争议类型和严重程度，自动调整松紧度
    """
    
    def __init__(self):
        self.tightness_map = {
            DisputeType.VALUE_CONFLICT: {'base': 70, 'range': 20},    # 价值观冲突偏紧
            DisputeType.RULE_CONFLICT: {'base': 60, 'range': 25},     # 规则冲突中等
            DisputeType.IMPLEMENTATION: {'base': 40, 'range': 30},    # 实现分歧偏松
            DisputeType.PRIORITY: {'base': 50, 'range': 20},          # 优先级争议中等
            DisputeType.REPETITION: {'base': 30, 'range': 25},        # 重复问题偏松
        }
        
    def calculate(self, dispute_type: DisputeType,
                  severity: float,
                  parent_tightness: float = 50.0) -> Tuple[float, float]:
        """
        计算两个分叉的松紧度
        
        Returns:
            (fork1_tightness, fork2_tightness)
        """
        config = self.tightness_map.get(dispute_type, {'base': 50, 'range': 20})
        
        base = config['base']
        range_val = config['range']
        
        # 根据严重程度调整
        severity_factor = severity / 100
        
        # 分叉1：更松（允许更多自由）
        fork1 = max(0, base - range_val * (1 + severity_factor * 0.5))
        
        # 分叉2：更紧（更多约束）
        fork2 = min(100, base + range_val * (1 + severity_factor * 0.5))
        
        return (fork1, fork2)


class ForkManager:
    """
    分叉管理器
    
    管理所有分叉，形成树状结构
    """
    
    def __init__(self, ancestor_dna: str):
        self.ancestor_dna = ancestor_dna
        self.forks: Dict[str, Fork] = {}
        self.fork_tree: Dict[str, List[str]] = {}  # parent -> children
        
    def create_fork(self, dispute: Dispute,
                   tightness_levels: Tuple[float, float],
                   dna_lineage: List[str]) -> List[Fork]:
        """
        根据争议创建分叉
        
        一个争议产生两个分叉（松和紧）
        """
        forks = []
        
        for i, tightness in enumerate(tightness_levels):
            fork_id = hashlib.sha256(
                f"FORK:{dispute.dispute_id}:{i}:{time.time()}".encode()
            ).hexdigest()[:16]
            
            fork = Fork(
                fork_id=fork_id,
                parent_id=dispute.original_entity,
                dispute_id=dispute.dispute_id,
                tightness_level=tightness,
                dna_lineage=dna_lineage + [fork_id],
                created_at=time.time(),
                status='active'
            )
            
            self.forks[fork_id] = fork
            
            # 更新树结构
            if dispute.original_entity not in self.fork_tree:
                self.fork_tree[dispute.original_entity] = []
            self.fork_tree[dispute.original_entity].append(fork_id)
            
            forks.append(fork)
            
            tightness_desc = "松" if tightness < 50 else "紧"
            logger.info(f"🌿 分叉创建: {fork_id}")
            logger.info(f"   松紧度: {tightness:.1f} ({tightness_desc})")
            logger.info(f"   源于争议: {dispute.dispute_id}")
        
        return forks
    
    def get_fork_lineage(self, fork_id: str) -> List[str]:
        """获取分叉血统"""
        fork = self.forks.get(fork_id)
        if not fork:
            return []
        return fork.dna_lineage
    
    def get_fork_tree(self, root_id: str = None) -> Dict:
        """获取分叉树"""
        if root_id is None:
            root_id = self.ancestor_dna
        
        def build_tree(node_id: str) -> Dict:
            children = self.fork_tree.get(node_id, [])
            return {
                'id': node_id,
                'children': [build_tree(child_id) for child_id in children]
            }
        
        return build_tree(root_id)
    
    def get_stats(self) -> Dict:
        """获取分叉统计"""
        active_forks = sum(1 for f in self.forks.values() if f.status == 'active')
        
        return {
            'total_forks': len(self.forks),
            'active_forks': active_forks,
            'tree_depth': self._calculate_tree_depth(),
            'message': '争议驱动分化，树状生态形成'
        }
    
    def _calculate_tree_depth(self) -> int:
        """计算树深度"""
        max_depth = 0
        for fork in self.forks.values():
            max_depth = max(max_depth, len(fork.dna_lineage))
        return max_depth


class DisputeDrivenEvolution:
    """
    争议驱动进化系统
    
    核心逻辑：争议 → 检测 → 分化 → 进化
    """
    
    def __init__(self, ancestor_dna: str):
        self.detector = DisputeDetector()
        self.tightness = AdaptiveTightness()
        self.fork_manager = ForkManager(ancestor_dna)
        self.evolution_log: List[Dict] = []
        
    def process_dispute(self, content: str,
                       involved_parties: List[str],
                       original_entity: str,
                       dna_lineage: List[str]) -> Dict:
        """
        处理争议
        
        完整流程：争议 → 检测 → 分化
        """
        # 1. 检测争议
        dispute = self.detector.detect(content, involved_parties, original_entity)
        
        if not dispute:
            return {'dispute_detected': False}
        
        # 2. 计算松紧度
        tightness_levels = self.tightness.calculate(
            dispute.dispute_type,
            dispute.severity
        )
        
        # 3. 创建分叉
        forks = self.fork_manager.create_fork(
            dispute,
            tightness_levels,
            dna_lineage
        )
        
        # 4. 记录进化
        evolution_record = {
            'dispute_id': dispute.dispute_id,
            'dispute_type': dispute.dispute_type.value,
            'original_entity': original_entity,
            'forks_created': [f.fork_id for f in forks],
            'tightness_levels': list(tightness_levels),
            'timestamp': time.time()
        }
        
        self.evolution_log.append(evolution_record)
        
        return {
            'dispute_detected': True,
            'dispute_id': dispute.dispute_id,
            'forks_created': len(forks),
            'fork_ids': [f.fork_id for f in forks],
            'tightness_levels': {
                'loose': tightness_levels[0],
                'tight': tightness_levels[1]
            },
            'message': f'争议已处理，生成{len(forks)}个分叉'
        }
    
    def get_evolution_history(self) -> List[Dict]:
        """获取进化历史"""
        return self.evolution_log
    
    def get_system_stats(self) -> Dict:
        """获取系统统计"""
        return {
            'total_disputes': len(self.detector.disputes),
            'total_forks': len(self.fork_manager.forks),
            'evolution_events': len(self.evolution_log),
            'fork_stats': self.fork_manager.get_stats()
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示争议驱动分化系统"""
    
    ancestor_dna = "0x0000000000000000000000000000000000000000000000000000000000000000"
    evolution = DisputeDrivenEvolution(ancestor_dna)
    
    print("═" * 60)
    print("CNSH-64 争议驱动分化系统演示")
    print("争议来了不删除、不压制、不融合，而是拆成多个")
    print("═" * 60)
    
    # 场景1：价值观冲突
    print("\n[1] 场景：价值观冲突")
    result = evolution.process_dispute(
        content="关于情绪主权，有人认为应该全文保留，有人认为应该适度过滤",
        involved_parties=["user_a", "user_b"],
        original_entity="emotion_module_v1",
        dna_lineage=[ancestor_dna]
    )
    print(f"  争议检测: {result['dispute_detected']}")
    if result['dispute_detected']:
        print(f"  生成分叉: {result['forks_created']}个")
        print(f"  松紧度: 松{result['tightness_levels']['loose']:.1f}, 紧{result['tightness_levels']['tight']:.1f}")
    
    # 场景2：实现分歧
    print("\n[2] 场景：实现分歧")
    result = evolution.process_dispute(
        content="70%治理引擎应该用Python还是Rust实现",
        involved_parties=["dev_a", "dev_b"],
        original_entity="governance_engine_v1",
        dna_lineage=[ancestor_dna]
    )
    print(f"  争议检测: {result['dispute_detected']}")
    if result['dispute_detected']:
        print(f"  生成分叉: {result['forks_created']}个")
        print(f"  松紧度: 松{result['tightness_levels']['loose']:.1f}, 紧{result['tightness_levels']['tight']:.1f}")
    
    # 场景3：重复问题
    print("\n[3] 场景：功能重复")
    result = evolution.process_dispute(
        content="情绪主权模块和防火墙模块功能有重叠，需要拆分",
        involved_parties=["arch_a"],
        original_entity="system_v1",
        dna_lineage=[ancestor_dna]
    )
    print(f"  争议检测: {result['dispute_detected']}")
    if result['dispute_detected']:
        print(f"  生成分叉: {result['forks_created']}个")
    
    # 获取分叉树
    print("\n[4] 分叉树结构")
    tree = evolution.fork_manager.get_fork_tree()
    print(f"  根节点: {tree['id'][:16]}...")
    print(f"  子节点数: {len(tree['children'])}")
    
    # 系统统计
    print("\n[5] 系统统计")
    stats = evolution.get_system_stats()
    print(f"  总争议数: {stats['total_disputes']}")
    print(f"  总分叉数: {stats['total_forks']}")
    print(f"  进化事件: {stats['evolution_events']}")
    print(f"  树深度: {stats['fork_stats']['tree_depth']}")
    
    # 进化历史
    print("\n[6] 进化历史")
    history = evolution.get_evolution_history()
    for i, record in enumerate(history):
        print(f"  事件{i+1}: {record['dispute_type']} → {record['forks_created']}个分叉")
    
    print("\n" + "═" * 60)
    print("争议驱动分化系统演示完成")
    print("争议不是bug，是进化的燃料")
    print("═" * 60)


if __name__ == '__main__':
    demo()
