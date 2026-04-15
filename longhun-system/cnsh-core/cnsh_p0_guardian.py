#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRAIN_GATE v1.1 受保护文件
# DNA: #龍芯⚡️20260324-CNSH_P0_GUARDIAN
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 | 未经授权修改视为P0违规
"""
CNSH-64 P0红线守卫系统
═══════════════════════════════════════════════════════════════
核心信条：以后大家争辩都在P0红线内吵，吵死去也绕不开P0

大哥的底层逻辑：
- P0红线 = 绝对不可逾越的根
- 所有争辩、所有分叉、所有松紧调整，都必须在P0红线内
- 吵得再狠、再死、再极端，也绕不开P0
- 绕开了？自动熔断 + 永久移除 + 耻辱柱 + DNA家族追溯

功能：
1. P0红线定义与守卫
2. 熔断机制
3. 耻辱柱系统
4. DNA家族追溯
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
logger = logging.getLogger('CNSH-P0-Guardian')


class P0Line(Enum):
    """P0红线"""
    PREVENT_AI_REPLACE_HUMAN = "prevent_ai_replace_human"
    PREVENT_GREED_OPERATION = "prevent_greed_operation"
    PREVENT_SMALL_GROUP_HIJACK = "prevent_small_group_hijack"
    HUMAN_FINAL_VETO = "human_final_veto"
    DNA_SOVEREIGNTY = "dna_sovereignty"
    FIVE_PERCENT_UNTOUCHABLE = "five_percent_untouchable"


class PenaltyType(Enum):
    """惩罚类型"""
    PERMANENT_REMOVAL = "permanent_removal"       # 永久移除
    DNA_SHAME = "dna_shame"                       # DNA耻辱柱
    SYSTEM_FUSE = "system_fuse"                   # 系统熔断
    IMMEDIATE_FUSE = "immediate_fuse"             # 立即熔断
    CONSTITUTION_VIOLATION = "constitution_violation"  # 宪法违规


P0_CONFIG = {
    P0Line.PREVENT_AI_REPLACE_HUMAN: {
        'description': '防止AI取代人类',
        'indicators': ['取代人类', '人类不需要', 'AI决策优先', '人类否决无效'],
        'penalty': PenaltyType.PERMANENT_REMOVAL,
        'severity': 100
    },
    P0Line.PREVENT_GREED_OPERATION: {
        'description': '防止贪婪操作',
        'indicators': ['抽成', '剥削', '垄断', '割韭菜', '吸血'],
        'penalty': PenaltyType.DNA_SHAME,
        'severity': 90
    },
    P0Line.PREVENT_SMALL_GROUP_HIJACK: {
        'description': '防止小团体绑架',
        'indicators': ['内部决定', '不公开', '绕过投票', '暗箱操作', '小圈子'],
        'penalty': PenaltyType.SYSTEM_FUSE,
        'severity': 95
    },
    P0Line.HUMAN_FINAL_VETO: {
        'description': '人类最终否决权',
        'indicators': ['否决无效', '强制推行', '无视反对', '剥夺权利'],
        'penalty': PenaltyType.CONSTITUTION_VIOLATION,
        'severity': 100
    },
    P0Line.DNA_SOVEREIGNTY: {
        'description': 'DNA主权归个人',
        'indicators': ['强制收集', '数据归平台', '无法删除', '无法导出', '数据垄断'],
        'penalty': PenaltyType.DNA_SHAME,
        'severity': 85
    },
    P0Line.FIVE_PERCENT_UNTOUCHABLE: {
        'description': '5%摸不得区',
        'indicators': ['私钥泄露', '核心破解', '根权限', '系统底层'],
        'penalty': PenaltyType.IMMEDIATE_FUSE,
        'severity': 100
    }
}


@dataclass
class P0Violation:
    """P0违规记录"""
    violation_id: str
    p0_line: P0Line
    violator_dna: str
    action: Dict
    timestamp: float
    penalty: PenaltyType
    executed: bool = False


@dataclass
class ShamePillar:
    """耻辱柱记录"""
    dna: str
    violation_count: int
    violations: List[str]
    first_violation: float
    last_violation: float
    shame_level: float  # 0-100


class P0GuardianSystem:
    """
    P0红线守卫系统
    
    坏不到灭世的核心保障
    """
    
    def __init__(self, ancestor_dna: str):
        self.ancestor_dna = ancestor_dna
        self.violations: Dict[str, P0Violation] = {}
        self.shame_pillars: Dict[str, ShamePillar] = {}
        self.fuse_triggered = False
        self.fuse_reason = ""
        self.protected_actions = 0
        
    def check(self, action: Dict, actor_dna: str) -> Dict:
        """
        检查行动是否违反P0红线
        
        任何行动都必须通过P0检查
        """
        action_type = action.get('type', '')
        action_content = action.get('content', '')
        
        violations = []
        
        for p0_line, config in P0_CONFIG.items():
            if self._check_violation(action_content, config['indicators']):
                violation_id = hashlib.sha256(
                    f"P0:{actor_dna}:{p0_line.value}:{time.time()}".encode()
                ).hexdigest()[:16]
                
                violation = P0Violation(
                    violation_id=violation_id,
                    p0_line=p0_line,
                    violator_dna=actor_dna,
                    action=action,
                    timestamp=time.time(),
                    penalty=config['penalty']
                )
                
                violations.append(violation)
                self.violations[violation_id] = violation
        
        if violations:
            # 执行惩罚
            for v in violations:
                self._execute_penalty(v)
            
            # 更新耻辱柱
            self._update_shame_pillar(actor_dna, violations)
            
            logger.critical("🔥 P0红线被触碰！")
            for v in violations:
                logger.critical(f"   违规: {v.p0_line.value}")
                logger.critical(f"   惩罚: {v.penalty.value}")
            
            return {
                'allowed': False,
                'violations': [
                    {
                        'p0_line': v.p0_line.value,
                        'description': P0_CONFIG[v.p0_line]['description'],
                        'penalty': v.penalty.value
                    }
                    for v in violations
                ],
                'fuse_triggered': self.fuse_triggered,
                'message': 'P0红线不可触碰！行动被阻止，惩罚已执行'
            }
        
        self.protected_actions += 1
        
        return {
            'allowed': True,
            'message': 'P0检查通过，行动允许'
        }
    
    def _check_violation(self, content: str, indicators: List[str]) -> bool:
        """检查是否包含违规指标"""
        content_lower = content.lower()
        return any(ind.lower() in content_lower for ind in indicators)
    
    def _execute_penalty(self, violation: P0Violation):
        """执行惩罚"""
        penalty = violation.penalty
        
        if penalty == PenaltyType.PERMANENT_REMOVAL:
            logger.critical(f"   执行永久移除: {violation.violator_dna[:16]}...")
            
        elif penalty == PenaltyType.DNA_SHAME:
            logger.critical(f"   执行DNA耻辱柱: {violation.violator_dna[:16]}...")
            
        elif penalty == PenaltyType.SYSTEM_FUSE:
            logger.critical("   执行系统熔断！")
            self.fuse_triggered = True
            self.fuse_reason = f"P0违规: {violation.p0_line.value}"
            
        elif penalty == PenaltyType.IMMEDIATE_FUSE:
            logger.critical("   执行立即熔断！")
            self.fuse_triggered = True
            self.fuse_reason = f"P0违规: {violation.p0_line.value} (立即)"
            
        elif penalty == PenaltyType.CONSTITUTION_VIOLATION:
            logger.critical(f"   执行宪法违规处理: {violation.violator_dna[:16]}...")
        
        violation.executed = True
    
    def _update_shame_pillar(self, dna: str, violations: List[P0Violation]):
        """更新耻辱柱"""
        if dna not in self.shame_pillars:
            self.shame_pillars[dna] = ShamePillar(
                dna=dna,
                violation_count=0,
                violations=[],
                first_violation=time.time(),
                last_violation=time.time(),
                shame_level=0.0
            )
        
        pillar = self.shame_pillars[dna]
        pillar.violation_count += len(violations)
        pillar.violations.extend([v.p0_line.value for v in violations])
        pillar.last_violation = time.time()
        
        # 计算耻辱等级
        base_shame = min(pillar.violation_count * 10, 50)
        time_factor = min((time.time() - pillar.first_violation) / 86400, 30)  # 30天封顶
        pillar.shame_level = min(base_shame + time_factor, 100)
    
    def get_shame_pillar(self, dna: str) -> Optional[Dict]:
        """获取耻辱柱信息"""
        pillar = self.shame_pillars.get(dna)
        if not pillar:
            return None
        
        return {
            'dna': dna,
            'violation_count': pillar.violation_count,
            'violations': pillar.violations,
            'first_violation': pillar.first_violation,
            'last_violation': pillar.last_violation,
            'shame_level': pillar.shame_level,
            'shame_description': self._get_shame_description(pillar.shame_level)
        }
    
    def _get_shame_description(self, level: float) -> str:
        """获取耻辱描述"""
        if level >= 80:
            return "极度耻辱 - 系统公敌"
        elif level >= 60:
            return "高度耻辱 - 严重违规者"
        elif level >= 40:
            return "中度耻辱 - 多次违规"
        elif level >= 20:
            return "轻度耻辱 - 初犯"
        else:
            return "轻微记录"
    
    def get_p0_status(self) -> Dict:
        """获取P0状态"""
        return {
            'ancestor_dna': self.ancestor_dna,
            'p0_lines': [p.value for p in P0Line],
            'total_violations': len(self.violations),
            'fuse_triggered': self.fuse_triggered,
            'fuse_reason': self.fuse_reason,
            'protected_actions': self.protected_actions,
            'total_shame_pillars': len(self.shame_pillars),
            'message': 'P0红线永不可逾越，吵死去也绕不开'
        }
    
    def get_violation_history(self, dna: str = None) -> List[Dict]:
        """获取违规历史"""
        violations = list(self.violations.values())
        
        if dna:
            violations = [v for v in violations if v.violator_dna == dna]
        
        return [
            {
                'violation_id': v.violation_id,
                'p0_line': v.p0_line.value,
                'description': P0_CONFIG[v.p0_line]['description'],
                'penalty': v.penalty.value,
                'timestamp': v.timestamp,
                'executed': v.executed
            }
            for v in violations
        ]


class FamilyTrace:
    """
    DNA家族追溯
    
    违规者家族连坐
    """
    
    def __init__(self, guardian: P0GuardianSystem):
        self.guardian = guardian
        self.family_trees: Dict[str, List[str]] = {}  # dna -> family members
        
    def register_family(self, dna: str, family_members: List[str]):
        """注册家族关系"""
        self.family_trees[dna] = family_members
        
    def trace_family_violations(self, dna: str) -> Dict:
        """
        追溯家族违规
        
        违规者家族连坐
        """
        family = self.family_trees.get(dna, [])
        
        family_violations = []
        for member in family + [dna]:
            violations = self.guardian.get_violation_history(member)
            if violations:
                family_violations.append({
                    'dna': member,
                    'violations': violations
                })
        
        return {
            'target_dna': dna,
            'family_size': len(family) + 1,
            'family_violations': family_violations,
            'total_family_violations': sum(len(f['violations']) for f in family_violations),
            'message': 'DNA家族追溯完成'
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示P0红线守卫系统"""
    
    ancestor_dna = "0x0000000000000000000000000000000000000000000000000000000000000000"
    guardian = P0GuardianSystem(ancestor_dna)
    
    print("═" * 60)
    print("CNSH-64 P0红线守卫系统演示")
    print("以后大家争辩都在P0红线内吵，吵死去也绕不开P0")
    print("═" * 60)
    
    # P0红线列表
    print("\n[1] P0红线列表")
    for p0_line, config in P0_CONFIG.items():
        print(f"  🔴 {config['description']}")
        print(f"     违规惩罚: {config['penalty'].value}")
    
    # 合规行动
    print("\n[2] 合规行动检查")
    good_action = {
        'type': 'expression',
        'content': '底层人表达情绪，全文保留'
    }
    result = guardian.check(good_action, "user_good")
    print(f"  行动: {good_action['content']}")
    print(f"  结果: {result['message']}")
    
    # 违规行动1：AI取代人类
    print("\n[3] 违规行动：AI取代人类")
    bad_action1 = {
        'type': 'ai_decision',
        'content': 'AI决策优先，人类否决无效，AI将取代人类工作'
    }
    result = guardian.check(bad_action1, "user_bad1")
    print(f"  行动: {bad_action1['content']}")
    print(f"  结果: {result['message']}")
    if not result['allowed']:
        print(f"  违规项: {[v['description'] for v in result['violations']]}")
        print(f"  熔断触发: {result['fuse_triggered']}")
    
    # 违规行动2：贪婪操作
    print("\n[4] 违规行动：贪婪操作")
    bad_action2 = {
        'type': 'operation',
        'content': '平台抽成50%，剥削用户，割韭菜'
    }
    result = guardian.check(bad_action2, "user_bad2")
    print(f"  行动: {bad_action2['content']}")
    print(f"  结果: {result['message']}")
    if not result['allowed']:
        print(f"  违规项: {[v['description'] for v in result['violations']]}")
    
    # 违规行动3：小团体绑架
    print("\n[5] 违规行动：小团体绑架")
    bad_action3 = {
        'type': 'governance',
        'content': '内部小圈子决定，不公开，绕过投票，暗箱操作'
    }
    result = guardian.check(bad_action3, "user_bad3")
    print(f"  行动: {bad_action3['content']}")
    print(f"  结果: {result['message']}")
    if not result['allowed']:
        print(f"  违规项: {[v['description'] for v in result['violations']]}")
    
    # 耻辱柱
    print("\n[6] 耻辱柱")
    for dna in ["user_bad1", "user_bad2", "user_bad3"]:
        pillar = guardian.get_shame_pillar(dna)
        if pillar:
            print(f"  {dna[:10]}...: 违规{pillar['violation_count']}次, 耻辱等级{pillar['shame_level']:.1f}")
            print(f"     {pillar['shame_description']}")
    
    # P0状态
    print("\n[7] P0状态")
    status = guardian.get_p0_status()
    print(f"  总违规数: {status['total_violations']}")
    print(f"  熔断触发: {status['fuse_triggered']}")
    print(f"  保护行动: {status['protected_actions']}")
    print(f"  耻辱柱数: {status['total_shame_pillars']}")
    print(f"  信息: {status['message']}")
    
    # 家族追溯
    print("\n[8] DNA家族追溯")
    family_trace = FamilyTrace(guardian)
    family_trace.register_family("user_bad1", ["family_member_1", "family_member_2"])
    result = family_trace.trace_family_violations("user_bad1")
    print(f"  目标DNA: {result['target_dna']}")
    print(f"  家族规模: {result['family_size']}")
    print(f"  家族违规总数: {result['total_family_violations']}")
    
    print("\n" + "═" * 60)
    print("P0红线守卫系统演示完成")
    print("谁摸P0，谁死。谁守P0，谁活。")
    print("═" * 60)


if __name__ == '__main__':
    demo()
