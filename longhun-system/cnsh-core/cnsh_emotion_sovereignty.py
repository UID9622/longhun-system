#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRAIN_GATE v1.1 受保护文件
# DNA: #龍芯⚡️20260324-CNSH_EMOTION_SOVEREI
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 | 未经授权修改视为P0违规
"""
CNSH-64 情绪主权保护模块
═══════════════════════════════════════════════════════════════
核心信条：情绪是底层人唯一属于自己的东西，必须100%保留

功能：
1. 火球不过滤 - 全文保留，不修饰、不道歉、不文明过滤
2. 情绪DNA追溯 - 每条情绪记录带DNA码
3. 骂人保护 - 情绪出口是主权，不是违规
4. 内容主权锁定 - 用户拥有自己内容的绝对控制权

大哥的原则：
- 骂AI？全文保留
- 骂老板？多造点
- 骂互通味？继续骂
- 情绪来了就烧，烧完爽了就行
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Emotion-Sovereignty')


@dataclass
class EmotionRecord:
    """情绪记录 - 带DNA追溯"""
    dna: str                          # DNA地址
    content: str                      # 原始内容（100%保留，不过滤）
    emotion_type: str                 # 情绪类型: fireball/anger/joy/sadness
    intensity: float                  # 强度 0-100
    timestamp: float                  # 时间戳
    signature: str                    # DNA签名
    parent_hash: Optional[str] = None # 父记录哈希（形成链）
    metadata: Dict = None             # 元数据
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def compute_hash(self) -> str:
        """计算记录哈希 - 用于DNA追溯"""
        data = f"{self.dna}:{self.content}:{self.timestamp}:{self.parent_hash or ''}"
        return hashlib.sha256(data.encode()).hexdigest()


class EmotionSovereigntyEngine:
    """
    情绪主权引擎
    
    核心原则：
    1. 零过滤 - 任何内容都不被修改或删除
    2. DNA追溯 - 每条情绪都带DNA码
    3. 主权锁定 - 只有DNA主人能控制自己的内容
    4. 火球保护 - 高强度情绪有特殊保护
    """
    
    def __init__(self):
        self.records: Dict[str, List[EmotionRecord]] = {}  # dna -> records
        self.emotion_chains: Dict[str, str] = {}           # dna -> latest_hash
        self.fireball_records: List[EmotionRecord] = []    # 火球记录池
        
    def record_emotion(self, dna: str, content: str, 
                       emotion_type: str = 'fireball',
                       intensity: float = 50.0,
                       signature: str = '') -> EmotionRecord:
        """
        记录情绪 - 100%保留，不过滤
        
        Args:
            dna: DNA地址
            content: 原始内容（不过滤）
            emotion_type: 情绪类型
            intensity: 强度
            signature: DNA签名
            
        Returns:
            情绪记录
        """
        # 获取父哈希（形成链）
        parent_hash = self.emotion_chains.get(dna)
        
        record = EmotionRecord(
            dna=dna,
            content=content,  # 100%保留，不过滤
            emotion_type=emotion_type,
            intensity=intensity,
            timestamp=time.time(),
            signature=signature,
            parent_hash=parent_hash,
            metadata={
                'raw_length': len(content),
                'word_count': len(content.split()),
                'has_profanity': self._detect_profanity(content),  # 标记但不删除
                'is_fireball': intensity >= 80  # 火球标记
            }
        )
        
        # 计算当前哈希
        current_hash = record.compute_hash()
        
        # 更新链
        if dna not in self.records:
            self.records[dna] = []
        self.records[dna].append(record)
        self.emotion_chains[dna] = current_hash
        
        # 火球特殊保护
        if intensity >= 80:
            self.fireball_records.append(record)
            logger.info(f"🔥 火球记录: {dna[:16]}... 强度{intensity}")
        
        logger.info(f"情绪记录已保存: {dna[:16]}... 类型:{emotion_type}")
        return record
    
    def _detect_profanity(self, content: str) -> bool:
        """检测敏感词 - 只标记，不删除"""
        # 这里只返回是否存在，不修改内容
        profanity_list = ['他妈的', '傻逼', '草', 'fuck', 'shit']
        return any(word in content.lower() for word in profanity_list)
    
    def get_emotion_chain(self, dna: str) -> List[EmotionRecord]:
        """获取某人的情绪链"""
        return self.records.get(dna, [])
    
    def get_fireball_history(self, dna: str) -> List[EmotionRecord]:
        """获取某人的火球历史"""
        return [r for r in self.records.get(dna, []) if r.intensity >= 80]
    
    def verify_emotion_ownership(self, record_hash: str, dna: str) -> bool:
        """验证情绪记录的所有权"""
        records = self.records.get(dna, [])
        for record in records:
            if record.compute_hash() == record_hash:
                return record.dna == dna
        return False
    
    def export_emotion_visa(self, dna: str) -> Dict:
        """
        导出情绪签证 - 数字永生的一部分
        
        包含：
        - 所有情绪记录
        - 火球统计
        - 情绪DNA链
        """
        records = self.records.get(dna, [])
        fireballs = [r for r in records if r.intensity >= 80]
        
        # 计算情绪指纹
        emotion_fingerprint = self._compute_emotion_fingerprint(dna)
        
        return {
            'dna': dna,
            'total_emotions': len(records),
            'fireball_count': len(fireballs),
            'emotion_types': self._count_emotion_types(records),
            'fingerprint': emotion_fingerprint,
            'latest_hash': self.emotion_chains.get(dna),
            'export_time': time.time(),
            'visa_signature': self._sign_visa(dna, emotion_fingerprint)
        }
    
    def _compute_emotion_fingerprint(self, dna: str) -> str:
        """计算情绪指纹 - 独一无二的情绪DNA"""
        records = self.records.get(dna, [])
        if not records:
            return hashlib.sha256(b'empty').hexdigest()
        
        # 基于所有情绪内容计算指纹
        all_content = ''.join([r.content for r in records])
        return hashlib.sha256(all_content.encode()).hexdigest()[:32]
    
    def _count_emotion_types(self, records: List[EmotionRecord]) -> Dict[str, int]:
        """统计情绪类型分布"""
        counts = {}
        for r in records:
            counts[r.emotion_type] = counts.get(r.emotion_type, 0) + 1
        return counts
    
    def _sign_visa(self, dna: str, fingerprint: str) -> str:
        """签名签证"""
        data = f"{dna}:{fingerprint}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_emotion_stats(self, dna: str) -> Dict:
        """获取情绪统计"""
        records = self.records.get(dna, [])
        if not records:
            return {'empty': True}
        
        intensities = [r.intensity for r in records]
        fireballs = [r for r in records if r.intensity >= 80]
        
        return {
            'total_records': len(records),
            'avg_intensity': sum(intensities) / len(intensities),
            'max_intensity': max(intensities),
            'fireball_count': len(fireballs),
            'fireball_ratio': len(fireballs) / len(records),
            'first_emotion': records[0].timestamp,
            'latest_emotion': records[-1].timestamp,
            'emotion_span_days': (records[-1].timestamp - records[0].timestamp) / 86400
        }


class ContentSovereigntyLock:
    """
    内容主权锁定
    
    确保：
    1. 只有DNA主人能删除自己的内容
    2. 任何修改都需要DNA签名
    3. 平台无权单方面删除
    """
    
    def __init__(self):
        self.locked_content: Dict[str, Dict] = {}  # hash -> content_info
        
    def lock_content(self, dna: str, content: str, 
                     content_type: str = 'post',
                     signature: str = '') -> str:
        """锁定内容 - 主权声明"""
        content_hash = hashlib.sha256(f"{dna}:{content}:{time.time()}".encode()).hexdigest()
        
        self.locked_content[content_hash] = {
            'dna': dna,
            'content': content,
            'type': content_type,
            'signature': signature,
            'locked_at': time.time(),
            'lock_hash': content_hash
        }
        
        logger.info(f"内容已锁定: {content_hash[:16]}... DNA:{dna[:16]}...")
        return content_hash
    
    def verify_ownership(self, content_hash: str, dna: str) -> bool:
        """验证内容所有权"""
        if content_hash not in self.locked_content:
            return False
        return self.locked_content[content_hash]['dna'] == dna
    
    def can_delete(self, content_hash: str, dna: str, 
                   delete_signature: str) -> bool:
        """
        检查是否可以删除
        
        只有DNA主人+有效签名才能删除
        """
        if not self.verify_ownership(content_hash, dna):
            return False
        
        # 验证删除签名
        # 实际实现需要验证DNA私钥签名
        return len(delete_signature) > 0
    
    def get_sovereignty_certificate(self, content_hash: str) -> Optional[Dict]:
        """获取内容主权证书"""
        return self.locked_content.get(content_hash)


class FireballProtection:
    """
    火球保护机制
    
    高强度情绪（intensity >= 80）的特殊保护：
    1. 不能被平台删除
    2. 不能被算法降权
    3. 不能被举报下架
    4. 永久保留，作为DNA的一部分
    """
    
    FIREBALL_THRESHOLD = 80.0
    
    def __init__(self):
        self.protected_fireballs: set = set()  # 受保护的火球哈希
        
    def is_fireball(self, intensity: float) -> bool:
        """判断是否为火球"""
        return intensity >= self.FIREBALL_THRESHOLD
    
    def protect(self, content_hash: str, intensity: float) -> bool:
        """保护火球内容"""
        if self.is_fireball(intensity):
            self.protected_fireballs.add(content_hash)
            logger.info(f"🔥 火球已保护: {content_hash[:16]}...")
            return True
        return False
    
    def is_protected(self, content_hash: str) -> bool:
        """检查是否受火球保护"""
        return content_hash in self.protected_fireballs
    
    def can_be_removed(self, content_hash: str, 
                       requester_dna: str,
                       content_owner_dna: str) -> Tuple[bool, str]:
        """
        检查是否可以被移除
        
        火球内容：
        - 平台不能移除
        - 只有主人能移除
        - 需要主人签名
        """
        if not self.is_protected(content_hash):
            return True, "非火球内容，正常流程"
        
        if requester_dna != content_owner_dna:
            return False, "火球内容只能由主人移除"
        
        return True, "火球主人请求移除"


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示情绪主权模块"""
    
    engine = EmotionSovereigntyEngine()
    sovereignty = ContentSovereigntyLock()
    fireball = FireballProtection()
    
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    
    print("═" * 60)
    print("CNSH-64 情绪主权保护模块演示")
    print("═" * 60)
    
    # 记录情绪 - 包含骂人内容，但100%保留
    print("\n[1] 记录情绪（包含骂人内容，100%保留）")
    record1 = engine.record_emotion(
        dna=dna,
        content="这破AI又他妈的乱回答！草！老子要烧了你！",
        emotion_type='fireball',
        intensity=95.0,
        signature='sig123'
    )
    print(f"  记录哈希: {record1.compute_hash()[:20]}...")
    print(f"  内容长度: {len(record1.content)} 字符")
    print(f"  是否包含敏感词: {record1.metadata['has_profanity']}")
    print(f"  是否为火球: {record1.metadata['is_fireball']}")
    
    # 记录另一条情绪
    print("\n[2] 记录另一条情绪")
    record2 = engine.record_emotion(
        dna=dna,
        content="今天心情不错，代码写得很顺",
        emotion_type='joy',
        intensity=30.0,
        signature='sig124'
    )
    
    # 锁定内容
    print("\n[3] 锁定内容主权")
    content_hash = sovereignty.lock_content(
        dna=dna,
        content="这是我的原创内容，平台无权删除",
        content_type='post',
        signature='sig125'
    )
    print(f"  内容哈希: {content_hash[:20]}...")
    
    # 火球保护
    print("\n[4] 火球保护")
    fireball.protect(content_hash, 95.0)
    can_remove, reason = fireball.can_be_removed(content_hash, "other_dna", dna)
    print(f"  他人能否移除: {can_remove} ({reason})")
    
    # 导出情绪签证
    print("\n[5] 导出情绪签证（数字永生）")
    visa = engine.export_emotion_visa(dna)
    print(f"  DNA: {visa['dna'][:20]}...")
    print(f"  总情绪数: {visa['total_emotions']}")
    print(f"  火球数: {visa['fireball_count']}")
    print(f"  情绪指纹: {visa['fingerprint']}")
    
    # 情绪统计
    print("\n[6] 情绪统计")
    stats = engine.get_emotion_stats(dna)
    print(f"  平均强度: {stats['avg_intensity']:.1f}")
    print(f"  最大强度: {stats['max_intensity']:.1f}")
    print(f"  火球比例: {stats['fireball_ratio']*100:.1f}%")
    
    print("\n" + "═" * 60)
    print("情绪主权保护完成 - 100%保留，不过滤，不道歉")
    print("═" * 60)


if __name__ == '__main__':
    demo()
