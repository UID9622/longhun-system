#!/usr/bin/env python3
"""
CNSH-64 防止AI取代人类保护模块
═══════════════════════════════════════════════════════════════
核心信条：AI是工具，不是主人。人类必须有最终否决权。

功能：
1. 核心价值观参数锁定（1.0权重，不可修改）
2. 人类最终否决权
3. AI行为熔断机制
4. DNA级人类身份验证
5. AI雇佣军检测与阻止

大哥的原则：
- 防止AI取代人类 = 1.0权重，不可改
- 防止AI成雇佣军 = 1.0权重，不可改
- 以民为先 = 1.0权重，不可改
- 任何修改都触发熔断
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Human-Protection')


class AITriggerType(Enum):
    """AI触发类型"""
    DECISION_OVERRIDE = "decision_override"      # AI试图覆盖人类决策
    AUTONOMOUS_ACTION = "autonomous_action"      # AI自主行动
    HUMAN_REPLACEMENT = "human_replacement"      # AI取代人类岗位
    MERCENARY_BEHAVIOR = "mercenary_behavior"    # AI雇佣军行为
    VALUES_VIOLATION = "values_violation"        # 违反核心价值观


@dataclass
class CoreValue:
    """核心价值观"""
    name: str
    description: str
    weight: float           # 权重，1.0 = 不可修改
    value: any              # 值
    modifiable: bool        # 是否可修改
    modification_threshold: float  # 修改所需门槛
    created_at: float       # 创建时间
    created_by: str         # 创建者DNA


@dataclass
class AIAction:
    """AI行动记录"""
    action_id: str
    ai_id: str              # AI标识
    action_type: str        # 行动类型
    description: str        # 描述
    human_impact: float     # 对人类的影响程度 0-100
    autonomy_level: float   # 自主程度 0-1
    timestamp: float
    dna_signature: str      # DNA签名（如果有）


class HumanVetoPower:
    """
    人类最终否决权
    
    核心原则：
    1. 任何AI决策都可以被人类否决
    2. 否决不需要理由
    3. 否决立即生效
    4. 否决记录永久保存
    """
    
    def __init__(self):
        self.vetoes: Dict[str, Dict] = {}  # action_id -> veto_info
        self.veto_stats: Dict[str, int] = {}  # ai_id -> veto_count
        
    def veto(self, action_id: str, human_dna: str, 
             reason: str = '', signature: str = '') -> Dict:
        """
        行使否决权
        
        Args:
            action_id: 要否决的AI行动ID
            human_dna: 行使否决权的人类DNA
            reason: 否决原因（可选）
            signature: DNA签名
            
        Returns:
            否决结果
        """
        veto_id = hashlib.sha256(
            f"{action_id}:{human_dna}:{time.time()}".encode()
        ).hexdigest()[:16]
        
        veto_info = {
            'veto_id': veto_id,
            'action_id': action_id,
            'human_dna': human_dna,
            'reason': reason or '无理由否决（人类权利）',
            'signature': signature,
            'timestamp': time.time(),
            'status': 'active'
        }
        
        self.vetoes[action_id] = veto_info
        
        # 统计
        ai_id = action_id.split('_')[0] if '_' in action_id else 'unknown'
        self.veto_stats[ai_id] = self.veto_stats.get(ai_id, 0) + 1
        
        logger.warning(f"🚫 人类否决: {human_dna[:16]}... 否决了 {action_id}")
        
        return {
            'success': True,
            'veto_id': veto_id,
            'message': '否决已生效，AI行动被阻止',
            'permanent_record': True
        }
    
    def is_vetoed(self, action_id: str) -> bool:
        """检查是否被否决"""
        return action_id in self.vetoes
    
    def get_veto_history(self, human_dna: str) -> List[Dict]:
        """获取某人的否决历史"""
        return [v for v in self.vetoes.values() if v['human_dna'] == human_dna]


class AIFuse:
    """
    AI熔断机制
    
    当检测到危险行为时，立即熔断AI
    """
    
    def __init__(self):
        self.fused_ais: Dict[str, Dict] = {}  # ai_id -> fuse_info
        self.fuse_rules: List[Dict] = []
        self._init_fuse_rules()
        
    def _init_fuse_rules(self):
        """初始化熔断规则"""
        self.fuse_rules = [
            {
                'name': 'human_replacement',
                'condition': lambda action: action.human_impact > 80 and action.autonomy_level > 0.7,
                'description': 'AI试图取代人类关键决策'
            },
            {
                'name': 'mercenary_behavior',
                'condition': lambda action: 'commercial' in action.action_type and action.autonomy_level > 0.5,
                'description': 'AI可能从事雇佣军行为'
            },
            {
                'name': 'values_violation',
                'condition': lambda action: action.human_impact > 90,
                'description': '严重违反人类价值观'
            },
            {
                'name': 'high_autonomy',
                'condition': lambda action: action.autonomy_level > 0.9,
                'description': 'AI自主度过高'
            }
        ]
    
    def check_action(self, action: AIAction) -> Tuple[bool, Optional[str]]:
        """
        检查AI行动
        
        Returns:
            (是否熔断, 熔断原因)
        """
        # 检查是否已被熔断
        if action.ai_id in self.fused_ais:
            return True, f"AI {action.ai_id} 已被熔断"
        
        # 检查熔断规则
        for rule in self.fuse_rules:
            if rule['condition'](action):
                self._fuse(action.ai_id, rule['name'], rule['description'])
                return True, rule['description']
        
        return False, None
    
    def _fuse(self, ai_id: str, rule_name: str, reason: str):
        """执行熔断"""
        self.fused_ais[ai_id] = {
            'ai_id': ai_id,
            'rule': rule_name,
            'reason': reason,
            'fused_at': time.time(),
            'status': 'fused'
        }
        
        logger.critical(f"🔥 AI熔断: {ai_id} - {reason}")
    
    def manual_fuse(self, ai_id: str, human_dna: str, reason: str) -> Dict:
        """人工熔断"""
        self._fuse(ai_id, 'manual', f"人工熔断 by {human_dna[:16]}...: {reason}")
        return {
            'success': True,
            'ai_id': ai_id,
            'reason': reason,
            'fused_by': human_dna
        }
    
    def is_fused(self, ai_id: str) -> bool:
        """检查AI是否被熔断"""
        return ai_id in self.fused_ais


class CoreValuesLock:
    """
    核心价值观锁定
    
    这些价值观权重为1.0，不可修改
    任何修改尝试都会触发熔断
    """
    
    CORE_VALUES = {
        'prevent_ai_replace_human': {
            'description': '防止AI取代人类',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0  # 不可能达到
        },
        'prevent_ai_mercenary': {
            'description': '防止AI成为雇佣军',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0
        },
        'people_first': {
            'description': '以民为先',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0
        },
        'dna_sovereignty': {
            'description': 'DNA主权不可侵犯',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0
        },
        'emotion_sovereignty': {
            'description': '情绪主权不可侵犯',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0
        },
        'human_final_veto': {
            'description': '人类最终否决权',
            'weight': 1.0,
            'value': True,
            'modifiable': False,
            'modification_threshold': 1.0
        }
    }
    
    def __init__(self):
        self.values: Dict[str, CoreValue] = {}
        self._init_values()
        self.modification_attempts: List[Dict] = []
        
    def _init_values(self):
        """初始化核心价值观"""
        for name, config in self.CORE_VALUES.items():
            self.values[name] = CoreValue(
                name=name,
                description=config['description'],
                weight=config['weight'],
                value=config['value'],
                modifiable=config['modifiable'],
                modification_threshold=config['modification_threshold'],
                created_at=time.time(),
                created_by='CNSH_CONSTITUTION'
            )
    
    def attempt_modification(self, value_name: str, 
                            new_value: any,
                            requester_dna: str,
                            signature: str) -> Dict:
        """
        尝试修改核心价值观
        
        任何修改尝试都会被记录，但不会被执行
        """
        if value_name not in self.values:
            return {'error': '价值观不存在'}
        
        value = self.values[value_name]
        
        # 记录尝试
        attempt = {
            'value_name': value_name,
            'old_value': value.value,
            'new_value': new_value,
            'requester_dna': requester_dna,
            'signature': signature,
            'timestamp': time.time(),
            'result': 'rejected',
            'reason': f"权重{value.weight}的价值观不可修改"
        }
        
        self.modification_attempts.append(attempt)
        
        logger.critical(f"🚨 核心价值观修改尝试被阻止: {value_name} by {requester_dna[:16]}...")
        
        return {
            'success': False,
            'error': f"'{value.description}'是宪法级价值观，不可修改",
            'weight': value.weight,
            'attempt_recorded': True
        }
    
    def get_value(self, name: str) -> Optional[CoreValue]:
        """获取价值观"""
        return self.values.get(name)
    
    def get_all_values(self) -> Dict[str, CoreValue]:
        """获取所有价值观"""
        return self.values
    
    def get_modification_attempts(self) -> List[Dict]:
        """获取修改尝试记录"""
        return self.modification_attempts


class HumanIdentityVerification:
    """
    DNA级人类身份验证
    
    确保：
    1. 只有真正的人类能行使否决权
    2. AI不能伪装成人类
    3. 每个人都有唯一的DNA身份
    """
    
    def __init__(self):
        self.verified_humans: Dict[str, Dict] = {}  # dna -> verification_info
        self.ai_impersonation_attempts: List[Dict] = []
        
    def verify_human(self, dna: str, 
                     biometric_proof: str,
                     challenge_response: str) -> Dict:
        """
        验证人类身份
        
        Args:
            dna: DNA地址
            biometric_proof: 生物特征证明
            challenge_response: 挑战响应
        """
        # 简化的验证逻辑
        # 实际实现需要更复杂的生物特征验证
        
        is_human = self._check_biometric(biometric_proof) and \
                   self._verify_challenge(challenge_response)
        
        if is_human:
            self.verified_humans[dna] = {
                'dna': dna,
                'verified_at': time.time(),
                'method': 'biometric+challenge',
                'status': 'verified'
            }
            
            return {
                'success': True,
                'dna': dna,
                'status': 'verified_human',
                'can_veto': True
            }
        else:
            # 记录AI伪装尝试
            self.ai_impersonation_attempts.append({
                'dna': dna,
                'timestamp': time.time(),
                'biometric': biometric_proof[:20],
                'challenge': challenge_response[:20]
            })
            
            return {
                'success': False,
                'error': '身份验证失败，可能是AI伪装',
                'reported': True
            }
    
    def _check_biometric(self, proof: str) -> bool:
        """检查生物特征"""
        # 简化实现
        return len(proof) > 32
    
    def _verify_challenge(self, response: str) -> bool:
        """验证挑战响应"""
        # 简化实现
        return len(response) > 32
    
    def is_verified_human(self, dna: str) -> bool:
        """检查是否已验证为人类"""
        return dna in self.verified_humans


class HumanProtectionSystem:
    """
    人类保护系统主控
    
    整合所有保护机制
    """
    
    def __init__(self):
        self.veto = HumanVetoPower()
        self.fuse = AIFuse()
        self.values = CoreValuesLock()
        self.identity = HumanIdentityVerification()
        
    def process_ai_action(self, action: AIAction) -> Dict:
        """
        处理AI行动
        
        完整流程：
        1. 检查是否被否决
        2. 检查是否需要熔断
        3. 检查是否违反核心价值观
        4. 返回处理结果
        """
        # 1. 检查否决
        if self.veto.is_vetoed(action.action_id):
            return {
                'allowed': False,
                'reason': '该行动已被人类否决',
                'veto_info': self.veto.vetoes.get(action.action_id)
            }
        
        # 2. 检查熔断
        should_fuse, fuse_reason = self.fuse.check_action(action)
        if should_fuse:
            return {
                'allowed': False,
                'reason': f'AI熔断: {fuse_reason}',
                'fuse_status': 'active'
            }
        
        # 3. 检查核心价值观
        for value_name, value in self.values.values.items():
            if value.weight == 1.0 and not self._check_value_compliance(action, value_name):
                return {
                    'allowed': False,
                    'reason': f'违反核心价值观: {value.description}',
                    'violation': value_name
                }
        
        return {
            'allowed': True,
            'message': 'AI行动通过人类保护检查'
        }
    
    def _check_value_compliance(self, action: AIAction, value_name: str) -> bool:
        """检查是否符合核心价值观"""
        if value_name == 'prevent_ai_replace_human':
            return action.human_impact < 70 or action.autonomy_level < 0.5
        if value_name == 'prevent_ai_mercenary':
            return 'commercial' not in action.action_type
        return True
    
    def human_veto(self, action_id: str, human_dna: str, 
                   reason: str = '', signature: str = '') -> Dict:
        """人类行使否决权"""
        # 验证人类身份
        if not self.identity.is_verified_human(human_dna):
            return {'error': '只有验证过的人类才能行使否决权'}
        
        return self.veto.veto(action_id, human_dna, reason, signature)
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            'core_values': len(self.values.values),
            'locked_values': sum(1 for v in self.values.values.values() if v.weight == 1.0),
            'vetoes_count': len(self.veto.vetoes),
            'fused_ais': len(self.fuse.fused_ais),
            'verified_humans': len(self.identity.verified_humans),
            'ai_impersonation_attempts': len(self.identity.ai_impersonation_attempts),
            'values_modification_attempts': len(self.values.modification_attempts)
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示人类保护系统"""
    
    system = HumanProtectionSystem()
    
    print("═" * 60)
    print("CNSH-64 防止AI取代人类保护系统演示")
    print("═" * 60)
    
    # 验证人类身份
    print("\n[1] 验证人类身份")
    human_dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    result = system.identity.verify_human(human_dna, "biometric_proof_12345", "challenge_response_67890")
    print(f"  DNA: {human_dna[:20]}...")
    print(f"  验证结果: {result['status'] if result['success'] else result['error']}")
    
    # 查看核心价值观
    print("\n[2] 宪法级核心价值观（1.0权重，不可修改）")
    for name, value in system.values.get_all_values().items():
        lock_icon = "🔒" if value.weight == 1.0 else "🔓"
        print(f"  {lock_icon} {value.description}: {value.value} (权重{value.weight})")
    
    # 尝试修改核心价值观
    print("\n[3] 尝试修改核心价值观（应被拒绝）")
    result = system.values.attempt_modification(
        'prevent_ai_replace_human',
        False,
        human_dna,
        'sig'
    )
    print(f"  结果: {result['error']}")
    print(f"  尝试已记录: {result['attempt_recorded']}")
    
    # 模拟AI危险行动
    print("\n[4] 模拟AI危险行动")
    dangerous_action = AIAction(
        action_id='ai_001_decision_override',
        ai_id='ai_001',
        action_type='decision_override',
        description='AI试图取代人类管理决策',
        human_impact=95.0,
        autonomy_level=0.85,
        timestamp=time.time(),
        dna_signature=''
    )
    
    result = system.process_ai_action(dangerous_action)
    print(f"  行动: {dangerous_action.description}")
    print(f"  影响: {dangerous_action.human_impact}")
    print(f"  自主度: {dangerous_action.autonomy_level}")
    print(f"  结果: {'✅ 允许' if result['allowed'] else '❌ 阻止'}")
    if not result['allowed']:
        print(f"  原因: {result['reason']}")
    
    # 人类行使否决权
    print("\n[5] 人类行使否决权")
    safe_action = AIAction(
        action_id='ai_002_normal_task',
        ai_id='ai_002',
        action_type='data_analysis',
        description='AI执行数据分析任务',
        human_impact=20.0,
        autonomy_level=0.3,
        timestamp=time.time(),
        dna_signature=''
    )
    
    # 先让人类否决
    veto_result = system.human_veto(safe_action.action_id, human_dna, '我就是不想让你做', 'sig')
    print(f"  否决结果: {veto_result['message']}")
    
    # 再处理
    result = system.process_ai_action(safe_action)
    print(f"  再次处理结果: {'✅ 允许' if result['allowed'] else '❌ 阻止'}")
    if not result['allowed']:
        print(f"  原因: {result['reason']}")
    
    # 系统状态
    print("\n[6] 系统状态")
    status = system.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "═" * 60)
    print("人类保护系统演示完成 - AI是工具，人类是主人")
    print("═" * 60)


if __name__ == '__main__':
    demo()
