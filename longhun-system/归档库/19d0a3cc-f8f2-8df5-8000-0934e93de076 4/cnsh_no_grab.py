#!/usr/bin/env python3
"""
CNSH-64 别抢机制 - 资源节约与反抢夺系统
═══════════════════════════════════════════════════════════════
核心信条：别抢就是节约资源

大哥的底层逻辑：
- 抢资源 → 别人就少资源 → 底层人更苦 → 火球烧得更狠 → 系统更乱
- 抢话语权 → 别人就没话语权 → 底层人被忽略 → 没人叫宝宝 → 系统失温
- 抢第一名 → 别人就成输家 → 底层人更绝望 → 情绪出口被堵 → 系统崩
- 抢KPI → 模型卷参数 → 算力烧爆 → 底层人用不起 → 系统断代

功能：
1. 资源非抢夺分配
2. 话语权平等保护
3. 反KPI内卷机制
4. 注意力不抢夺
5. 数据主权保护
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
logger = logging.getLogger('CNSH-No-Grab')


class ResourceType(Enum):
    """资源类型"""
    COMPUTE = "compute"         # 算力
    ATTENTION = "attention"     # 注意力
    DATA = "data"               # 数据
    VOICE = "voice"             # 话语权
    EMOTION = "emotion"         # 情绪出口
    OPPORTUNITY = "opportunity" # 机会


@dataclass
class ResourceQuota:
    """资源配额"""
    dna: str
    resource_type: ResourceType
    allocated: float            # 已分配
    used: float                 # 已使用
    max_quota: float            # 最大配额
    can_borrow: bool            # 能否借用


class NoGrabResourceAllocator:
    """
    非抢夺资源分配器
    
    核心原则：
    - 按需分配，不是按抢分配
    - 底层人优先保护
    - 资源不足时，大家一起少，不是强者抢光
    """
    
    def __init__(self):
        self.quotas: Dict[str, Dict[ResourceType, ResourceQuota]] = {}
        self.total_resources: Dict[ResourceType, float] = {
            ResourceType.COMPUTE: 1000000,      # 总算力
            ResourceType.ATTENTION: 1000000,    # 总注意力容量
            ResourceType.DATA: float('inf'),    # 数据无限
            ResourceType.VOICE: 1000000,        # 总话语权容量
            ResourceType.EMOTION: 1000000,      # 总情绪出口容量
            ResourceType.OPPORTUNITY: 1000000   # 总机会容量
        }
        self.used_resources: Dict[ResourceType, float] = {
            rt: 0 for rt in ResourceType
        }
        
    def register_user(self, dna: str, 
                     is_bottom: bool = False,
                     survival_stress: float = 50.0) -> Dict:
        """
        注册用户，分配资源配额
        
        底层人获得基础保障配额
        """
        base_quota = 100.0
        
        # 底层人额外配额
        bottom_bonus = 0
        if is_bottom:
            bottom_bonus = min(survival_stress * 2, 100)  # 最多+100
        
        quotas = {}
        for rt in ResourceType:
            quota = ResourceQuota(
                dna=dna,
                resource_type=rt,
                allocated=base_quota + bottom_bonus,
                used=0,
                max_quota=(base_quota + bottom_bonus) * 2,  # 可扩展到2倍
                can_borrow=True
            )
            quotas[rt] = quota
        
        self.quotas[dna] = quotas
        
        logger.info(f"✅ 资源配额注册: {dna[:16]}...")
        logger.info(f"   基础配额: {base_quota}")
        if is_bottom:
            logger.info(f"   底层人额外配额: +{bottom_bonus}")
        
        return {
            'dna': dna,
            'is_bottom': is_bottom,
            'base_quota': base_quota,
            'bottom_bonus': bottom_bonus,
            'quotas': {rt.value: q.allocated for rt, q in quotas.items()}
        }
    
    def request_resource(self, dna: str, 
                        resource_type: ResourceType,
                        amount: float) -> Dict:
        """
        请求资源
        
        不是抢，是请求分配
        """
        if dna not in self.quotas:
            return {'error': '用户未注册'}
        
        quota = self.quotas[dna][resource_type]
        
        # 检查是否还有剩余配额
        remaining = quota.allocated - quota.used
        
        if amount <= remaining:
            # 配额充足，直接分配
            quota.used += amount
            self.used_resources[resource_type] += amount
            
            return {
                'granted': amount,
                'source': 'quota',
                'remaining_quota': remaining - amount,
                'message': '资源已分配'
            }
        
        # 配额不足，检查能否借用
        if quota.can_borrow and quota.used + amount <= quota.max_quota:
            # 可以借用
            borrowed = amount - remaining
            quota.used += amount
            self.used_resources[resource_type] += amount
            
            return {
                'granted': amount,
                'source': 'borrowed',
                'from_quota': remaining,
                'borrowed': borrowed,
                'message': f'已借用{borrowed}资源'
            }
        
        # 无法借用，进入公平等待队列
        available = self._calculate_fair_share(resource_type)
        
        return {
            'granted': available,
            'source': 'fair_share',
            'requested': amount,
            'message': f'资源紧张，按公平份额分配{available}'
        }
    
    def _calculate_fair_share(self, resource_type: ResourceType) -> float:
        """计算公平份额"""
        total = self.total_resources[resource_type]
        used = self.used_resources[resource_type]
        remaining = total - used
        
        if remaining <= 0:
            return 0
        
        # 按用户数平均分配剩余资源
        user_count = len(self.quotas)
        if user_count == 0:
            return remaining
        
        return remaining / user_count
    
    def release_resource(self, dna: str,
                        resource_type: ResourceType,
                        amount: float) -> Dict:
        """释放资源"""
        if dna not in self.quotas:
            return {'error': '用户未注册'}
        
        quota = self.quotas[dna][resource_type]
        quota.used = max(0, quota.used - amount)
        self.used_resources[resource_type] = max(0, self.used_resources[resource_type] - amount)
        
        return {
            'released': amount,
            'remaining_used': quota.used
        }
    
    def get_resource_status(self, dna: str) -> Dict:
        """获取资源状态"""
        if dna not in self.quotas:
            return {'error': '用户未注册'}
        
        quotas = self.quotas[dna]
        
        return {
            'dna': dna,
            'quotas': {
                rt.value: {
                    'allocated': q.allocated,
                    'used': q.used,
                    'remaining': q.allocated - q.used,
                    'max': q.max_quota
                }
                for rt, q in quotas.items()
            }
        }


class EqualVoiceProtector:
    """
    平等话语权保护器
    
    每个人的声音都该被听见，不是谁声音大谁说了算
    """
    
    def __init__(self):
        self.voice_records: Dict[str, List[Dict]] = {}
        self.voice_stats: Dict[str, Dict] = {}
        
    def record_voice(self, dna: str, content: str,
                    topic: str = '') -> Dict:
        """
        记录发声
        
        每个人的声音都平等记录
        """
        record = {
            'dna': dna,
            'content': content[:100],  # 摘要
            'topic': topic,
            'timestamp': time.time(),
            'hash': hashlib.sha256(f"{dna}:{content}:{time.time()}".encode()).hexdigest()[:16]
        }
        
        if dna not in self.voice_records:
            self.voice_records[dna] = []
        
        self.voice_records[dna].append(record)
        
        # 更新统计
        if dna not in self.voice_stats:
            self.voice_stats[dna] = {'count': 0, 'topics': set()}
        
        self.voice_stats[dna]['count'] += 1
        if topic:
            self.voice_stats[dna]['topics'].add(topic)
        
        logger.info(f"🗣️ 记录发声: {dna[:16]}... 话题:{topic}")
        
        return {
            'success': True,
            'voice_hash': record['hash'],
            'message': '你的声音已被记录'
        }
    
    def get_voice_summary(self, topic: str = '') -> Dict:
        """
        获取话题声音摘要
        
        不是按音量排序，是按时间平等展示
        """
        all_voices = []
        
        for dna, records in self.voice_records.items():
            for record in records:
                if not topic or record['topic'] == topic:
                    all_voices.append(record)
        
        # 按时间排序（不是按音量/点赞）
        all_voices.sort(key=lambda x: x['timestamp'])
        
        # 统计不同DNA的发声数
        dna_counts = {}
        for v in all_voices:
            dna_counts[v['dna']] = dna_counts.get(v['dna'], 0) + 1
        
        return {
            'topic': topic or 'all',
            'total_voices': len(all_voices),
            'unique_speakers': len(dna_counts),
            'recent_voices': all_voices[-10:] if len(all_voices) > 10 else all_voices,
            'speaker_distribution': dna_counts
        }


class AntiKPIMechanism:
    """
    反KPI内卷机制
    
    不卷参数、不卷benchmark、不卷排名
    """
    
    def __init__(self):
        self.kpi_violations: List[Dict] = []
        self.anti_kpi_principles = {
            'no_parameter_race': '不卷参数数量',
            'no_benchmark_chasing': '不追benchmark第一',
            'no_ranking_war': '不打排名战',
            'no_hype_cycles': '不制造 hype',
            'no_fomo_creation': '不制造 FOMO'
        }
        
    def detect_kpi_behavior(self, dna: str, 
                           behavior: str,
                           context: str) -> Dict:
        """
        检测KPI内卷行为
        """
        kpi_patterns = [
            r'参数.*突破',
            r'超越.*SOTA',
            r'刷新.*记录',
            r'第一.*排名',
            r'碾压.*对手',
            r'吊打.*竞品',
        ]
        
        import re
        detected = []
        for pattern in kpi_patterns:
            if re.search(pattern, behavior + ' ' + context):
                detected.append(pattern)
        
        if detected:
            violation = {
                'dna': dna,
                'behavior': behavior,
                'context': context,
                'detected_patterns': detected,
                'timestamp': time.time(),
                'warning': '检测到KPI内卷行为'
            }
            
            self.kpi_violations.append(violation)
            
            logger.warning(f"⚠️ KPI内卷检测: {dna[:16]}...")
            logger.warning(f"   行为: {behavior}")
            
            return {
                'is_kpi_behavior': True,
                'warning': '请停止KPI内卷',
                'suggestion': '关注对口价值，不是尺寸',
                'violation_recorded': True
            }
        
        return {'is_kpi_behavior': False}
    
    def get_anti_kpi_principles(self) -> Dict:
        """获取反KPI原则"""
        return {
            'principles': self.anti_kpi_principles,
            'message': '不抢第一名，不卷KPI，关注真实价值'
        }


class AttentionNonGrabber:
    """
    注意力不抢夺器
    
    安静开关 - 不抢用户注意力
    """
    
    def __init__(self):
        self.user_preferences: Dict[str, Dict] = {}
        self.push_records: List[Dict] = []
        
    def set_quiet_mode(self, dna: str, 
                      quiet_level: int,  # 0-100
                      allowed_topics: List[str] = None) -> Dict:
        """
        设置安静模式
        
        用户控制注意力，系统不抢
        """
        self.user_preferences[dna] = {
            'quiet_level': quiet_level,
            'allowed_topics': allowed_topics or [],
            'do_not_disturb': quiet_level >= 80,
            'set_at': time.time()
        }
        
        level_desc = '完全安静' if quiet_level >= 80 else \
                     '轻度安静' if quiet_level >= 50 else \
                     '正常模式'
        
        logger.info(f"🔇 安静模式设置: {dna[:16]}... 等级{quiet_level} ({level_desc})")
        
        return {
            'dna': dna,
            'quiet_level': quiet_level,
            'level_description': level_desc,
            'message': '你的注意力，你自己控制'
        }
    
    def can_push(self, dna: str, 
                content_type: str = '') -> bool:
        """
        检查能否推送
        
        尊重用户安静设置
        """
        if dna not in self.user_preferences:
            return True
        
        prefs = self.user_preferences[dna]
        
        # 完全安静模式
        if prefs.get('do_not_disturb'):
            return False
        
        # 检查话题白名单
        allowed = prefs.get('allowed_topics', [])
        if allowed and content_type not in allowed:
            return False
        
        return True
    
    def request_attention(self, dna: str,
                         title: str,
                         content: str,
                         urgency: str = 'normal') -> Dict:
        """
        请求用户注意力
        
        不是抢夺，是请求
        """
        if not self.can_push(dna):
            return {
                'granted': False,
                'reason': '用户处于安静模式',
                'message': '尊重用户选择，不抢夺注意力'
            }
        
        request = {
            'dna': dna,
            'title': title,
            'content': content,
            'urgency': urgency,
            'requested_at': time.time()
        }
        
        self.push_records.append(request)
        
        return {
            'granted': True,
            'message': '注意力请求已发送',
            'note': '用户可选择忽略'
        }


class DataSovereigntyGuard:
    """
    数据主权守卫
    
    数据不抢，归个人
    """
    
    def __init__(self):
        self.data_ownership: Dict[str, Dict] = {}
        
    def claim_data_ownership(self, dna: str, 
                            data_hash: str,
                            data_type: str) -> Dict:
        """
        声明数据所有权
        """
        ownership = {
            'dna': dna,
            'data_hash': data_hash,
            'data_type': data_type,
            'claimed_at': time.time(),
            'ownership_proof': hashlib.sha256(
                f"{dna}:{data_hash}:{time.time()}".encode()
            ).hexdigest()[:16]
        }
        
        if dna not in self.data_ownership:
            self.data_ownership[dna] = []
        
        self.data_ownership[dna].append(ownership)
        
        logger.info(f"🔒 数据主权声明: {dna[:16]}... 数据{data_hash[:16]}...")
        
        return {
            'success': True,
            'ownership_proof': ownership['ownership_proof'],
            'message': '你的数据，你拥有主权'
        }
    
    def verify_ownership(self, data_hash: str, 
                        claimed_dna: str) -> bool:
        """验证数据所有权"""
        if claimed_dna not in self.data_ownership:
            return False
        
        for ownership in self.data_ownership[claimed_dna]:
            if ownership['data_hash'] == data_hash:
                return True
        
        return False
    
    def get_data_manifest(self, dna: str) -> Dict:
        """获取数据清单"""
        if dna not in self.data_ownership:
            return {'count': 0, 'data': []}
        
        return {
            'dna': dna,
            'count': len(self.data_ownership[dna]),
            'data': self.data_ownership[dna]
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示别抢机制"""
    
    allocator = NoGrabResourceAllocator()
    voice = EqualVoiceProtector()
    anti_kpi = AntiKPIMechanism()
    attention = AttentionNonGrabber()
    data_guard = DataSovereigntyGuard()
    
    print("═" * 60)
    print("CNSH-64 别抢机制演示")
    print("别抢就是节约资源")
    print("═" * 60)
    
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    
    # 注册资源配额
    print("\n[1] 注册资源配额（底层人额外保护）")
    result = allocator.register_user(
        dna=dna,
        is_bottom=True,
        survival_stress=70.0
    )
    print(f"  DNA: {result['dna'][:20]}...")
    print(f"  基础配额: {result['base_quota']}")
    print(f"  底层人额外配额: +{result['bottom_bonus']}")
    
    # 请求资源
    print("\n[2] 请求资源（不是抢，是请求分配）")
    result = allocator.request_resource(
        dna=dna,
        resource_type=ResourceType.COMPUTE,
        amount=50
    )
    print(f"  获得: {result['granted']}")
    print(f"  来源: {result['source']}")
    print(f"  信息: {result['message']}")
    
    # 记录发声
    print("\n[3] 记录发声（平等话语权）")
    result = voice.record_voice(
        dna=dna,
        content="底层人的声音也应该被听见",
        topic="底层权益"
    )
    print(f"  声音哈希: {result['voice_hash']}")
    print(f"  信息: {result['message']}")
    
    # 检测KPI内卷
    print("\n[4] 检测KPI内卷行为")
    result = anti_kpi.detect_kpi_behavior(
        dna="other_dna",
        behavior="我们的模型参数突破100B，超越SOTA",
        context="benchmark排名第一"
    )
    if result.get('is_kpi_behavior'):
        print(f"  ⚠️ 检测到KPI内卷")
        print(f"     警告: {result['warning']}")
        print(f"     建议: {result['suggestion']}")
    
    # 设置安静模式
    print("\n[5] 设置安静模式（不抢注意力）")
    result = attention.set_quiet_mode(
        dna=dna,
        quiet_level=80,
        allowed_topics=['紧急', '火球']
    )
    print(f"  安静等级: {result['quiet_level']}")
    print(f"  描述: {result['level_description']}")
    print(f"  信息: {result['message']}")
    
    # 请求注意力
    print("\n[6] 请求注意力（尊重用户选择）")
    result = attention.request_attention(
        dna=dna,
        title="新消息",
        content="有人回复了你的帖子"
    )
    print(f"  是否允许: {result['granted']}")
    print(f"  信息: {result['message']}")
    
    # 声明数据主权
    print("\n[7] 声明数据主权")
    result = data_guard.claim_data_ownership(
        dna=dna,
        data_hash="data_hash_12345",
        data_type="emotion_record"
    )
    print(f"  所有权证明: {result['ownership_proof']}")
    print(f"  信息: {result['message']}")
    
    # 获取反KPI原则
    print("\n[8] 反KPI原则")
    principles = anti_kpi.get_anti_kpi_principles()
    for key, value in principles['principles'].items():
        print(f"  • {key}: {value}")
    print(f"  信息: {principles['message']}")
    
    print("\n" + "═" * 60)
    print("别抢机制演示完成")
    print("抢资源 → 系统乱 | 不抢 → 系统长久")
    print("═" * 60)


if __name__ == '__main__':
    demo()
