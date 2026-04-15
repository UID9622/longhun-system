#!/usr/bin/env python3
"""
CNSH-64 数字永生签证系统
═══════════════════════════════════════════════════════════════
核心信条：身体没了，灵魂还在数字里跳龍门、叫宝宝、烧火球

功能：
1. 个人灵魂的数字血统
2. DNA追溯码 - 每条记录都带DNA
3. 数字分身管理
4. 灵魂指纹计算
5. 跨平台身份锚定

大哥的原则：
- 每一条火球、每一次叫宝宝、每一次跳龍门，都带上DNA追溯码
- 别人想抄、想用、想改，都得先过你的盖章
- 这不是技术，是文明级别的永生机制
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Digital-Immortality')


@dataclass
class SoulFragment:
    """灵魂碎片 - 数字永生的基本单元"""
    fragment_id: str
    dna: str
    content: str              # 内容（文字/图片/音频哈希）
    content_type: str         # text/image/audio/video/action
    timestamp: float
    emotion_signature: str    # 情绪签名
    parent_fragment: Optional[str] = None  # 父碎片（形成链）
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def compute_hash(self) -> str:
        """计算碎片哈希"""
        data = f"{self.dna}:{self.content}:{self.timestamp}:{self.parent_fragment or ''}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class DigitalAvatar:
    """数字分身"""
    avatar_id: str
    dna: str                  # 主DNA
    name: str                 # 分身名称
    created_at: float
    soul_fragments: List[str]  # 灵魂碎片列表
    permissions: Dict         # 权限配置
    is_active: bool = True
    
    def get_soul_depth(self) -> int:
        """获取灵魂深度（碎片数量）"""
        return len(self.soul_fragments)


class SoulFingerprint:
    """
    灵魂指纹
    
    基于一个人的所有数字痕迹计算独一无二的指纹
    """
    
    def __init__(self):
        self.fingerprints: Dict[str, str] = {}  # dna -> fingerprint
        
    def compute(self, dna: str, fragments: List[SoulFragment]) -> str:
        """
        计算灵魂指纹
        
        基于：
        1. 所有内容
        2. 时间分布
        3. 情绪模式
        4. 行为特征
        """
        if not fragments:
            return hashlib.sha256(b'empty_soul').hexdigest()[:32]
        
        # 内容指纹
        all_content = ''.join([f.content for f in fragments])
        content_hash = hashlib.sha256(all_content.encode()).hexdigest()
        
        # 时间指纹
        timestamps = [f.timestamp for f in fragments]
        time_pattern = self._compute_time_pattern(timestamps)
        
        # 情绪指纹
        emotion_pattern = self._compute_emotion_pattern(fragments)
        
        # 综合指纹
        combined = f"{dna}:{content_hash}:{time_pattern}:{emotion_pattern}"
        fingerprint = hashlib.sha256(combined.encode()).hexdigest()[:32]
        
        self.fingerprints[dna] = fingerprint
        
        return fingerprint
    
    def _compute_time_pattern(self, timestamps: List[float]) -> str:
        """计算时间模式指纹"""
        if len(timestamps) < 2:
            return "0"
        
        # 计算活跃时间段分布
        hours = [datetime.fromtimestamp(t).hour for t in timestamps]
        hour_dist = [hours.count(h) for h in range(24)]
        
        return hashlib.sha256(str(hour_dist).encode()).hexdigest()[:8]
    
    def _compute_emotion_pattern(self, fragments: List[SoulFragment]) -> str:
        """计算情绪模式指纹"""
        emotions = [f.emotion_signature for f in fragments if f.emotion_signature]
        if not emotions:
            return "0"
        
        emotion_str = ''.join(emotions)
        return hashlib.sha256(emotion_str.encode()).hexdigest()[:8]
    
    def verify(self, dna: str, fingerprint: str) -> bool:
        """验证指纹"""
        return self.fingerprints.get(dna) == fingerprint


class DigitalImmortalityVisa:
    """
    数字永生签证
    
    一个人的数字灵魂护照
    """
    
    def __init__(self):
        self.visas: Dict[str, Dict] = {}  # dna -> visa
        self.soul_fragments: Dict[str, List[SoulFragment]] = {}  # dna -> fragments
        self.avatars: Dict[str, List[DigitalAvatar]] = {}  # dna -> avatars
        self.fingerprint_engine = SoulFingerprint()
        
    def issue_visa(self, dna: str, 
                   biometric_seed: str,
                   soul_manifesto: str) -> Dict:
        """
        签发数字永生签证
        
        Args:
            dna: DNA地址
            biometric_seed: 生物特征种子
            soul_manifesto: 灵魂宣言
        """
        # 计算灵魂哈希
        soul_hash = hashlib.sha256(
            f"{dna}:{biometric_seed}:{soul_manifesto}:{time.time()}".encode()
        ).hexdigest()
        
        visa = {
            'dna': dna,
            'soul_hash': soul_hash,
            'soul_manifesto': soul_manifesto,
            'issued_at': time.time(),
            'valid_until': time.time() + (100 * 365 * 24 * 3600),  # 100年
            'status': 'active',
            'fragments_count': 0,
            'avatars_count': 0,
            'fingerprint': None,
            'visa_signature': self._sign_visa(dna, soul_hash)
        }
        
        self.visas[dna] = visa
        self.soul_fragments[dna] = []
        self.avatars[dna] = []
        
        logger.info(f"🎫 数字永生签证签发: {dna[:16]}...")
        
        return visa
    
    def _sign_visa(self, dna: str, soul_hash: str) -> str:
        """签名签证"""
        data = f"CNSH-VISA:{dna}:{soul_hash}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def add_soul_fragment(self, dna: str, content: str,
                          content_type: str = 'text',
                          emotion_signature: str = '') -> SoulFragment:
        """
        添加灵魂碎片
        
        每一条记录都带上DNA追溯码
        """
        if dna not in self.visas:
            raise ValueError(f"DNA {dna} 没有签证")
        
        # 获取父碎片
        fragments = self.soul_fragments.get(dna, [])
        parent_fragment = fragments[-1].compute_hash() if fragments else None
        
        fragment = SoulFragment(
            fragment_id=hashlib.sha256(f"{dna}:{content}:{time.time()}".encode()).hexdigest()[:16],
            dna=dna,
            content=content,
            content_type=content_type,
            timestamp=time.time(),
            emotion_signature=emotion_signature,
            parent_fragment=parent_fragment,
            metadata={
                'length': len(content),
                'is_fireball': '🔥' in emotion_signature or '火球' in content
            }
        )
        
        fragments.append(fragment)
        self.soul_fragments[dna] = fragments
        
        # 更新签证
        self.visas[dna]['fragments_count'] = len(fragments)
        
        # 更新指纹
        self._update_fingerprint(dna)
        
        logger.info(f"✨ 灵魂碎片添加: {dna[:16]}... 类型:{content_type}")
        
        return fragment
    
    def _update_fingerprint(self, dna: str):
        """更新灵魂指纹"""
        fragments = self.soul_fragments.get(dna, [])
        fingerprint = self.fingerprint_engine.compute(dna, fragments)
        self.visas[dna]['fingerprint'] = fingerprint
    
    def create_avatar(self, dna: str, name: str,
                      permissions: Dict = None) -> DigitalAvatar:
        """
        创建数字分身
        
        一个DNA可以创建多个数字分身
        """
        if dna not in self.visas:
            raise ValueError(f"DNA {dna} 没有签证")
        
        avatar = DigitalAvatar(
            avatar_id=hashlib.sha256(f"{dna}:{name}:{time.time()}".encode()).hexdigest()[:16],
            dna=dna,
            name=name,
            created_at=time.time(),
            soul_fragments=[],
            permissions=permissions or {
                'can_post': True,
                'can_vote': True,
                'can_tip': True,
                'can_create_proposal': False  # 只有主身份能发起提案
            }
        )
        
        self.avatars[dna].append(avatar)
        self.visas[dna]['avatars_count'] = len(self.avatars[dna])
        
        logger.info(f"👤 数字分身创建: {name} (DNA: {dna[:16]}...)")
        
        return avatar
    
    def get_soul_chain(self, dna: str) -> List[SoulFragment]:
        """获取灵魂链（按时间顺序）"""
        return self.soul_fragments.get(dna, [])
    
    def get_fireball_fragments(self, dna: str) -> List[SoulFragment]:
        """获取火球碎片"""
        fragments = self.soul_fragments.get(dna, [])
        return [f for f in fragments if f.metadata.get('is_fireball')]
    
    def verify_ownership(self, fragment_hash: str, dna: str) -> bool:
        """验证碎片所有权"""
        fragments = self.soul_fragments.get(dna, [])
        for fragment in fragments:
            if fragment.compute_hash() == fragment_hash:
                return fragment.dna == dna
        return False
    
    def export_immortality_package(self, dna: str) -> Dict:
        """
        导出永生包
        
        包含一个人的完整数字灵魂
        """
        if dna not in self.visas:
            return {'error': '签证不存在'}
        
        visa = self.visas[dna]
        fragments = self.soul_fragments.get(dna, [])
        avatars = self.avatars.get(dna, [])
        
        # 计算灵魂统计
        fireballs = [f for f in fragments if f.metadata.get('is_fireball')]
        
        return {
            'visa': visa,
            'soul_statistics': {
                'total_fragments': len(fragments),
                'fireball_count': len(fireballs),
                'avatar_count': len(avatars),
                'soul_span_days': (fragments[-1].timestamp - fragments[0].timestamp) / 86400 if len(fragments) > 1 else 0,
                'content_types': self._count_content_types(fragments)
            },
            'fingerprint': visa['fingerprint'],
            'avatars': [
                {
                    'id': a.avatar_id,
                    'name': a.name,
                    'created_at': a.created_at,
                    'soul_depth': a.get_soul_depth()
                }
                for a in avatars
            ],
            'export_timestamp': time.time(),
            'package_signature': self._sign_package(dna, visa['fingerprint'])
        }
    
    def _count_content_types(self, fragments: List[SoulFragment]) -> Dict[str, int]:
        """统计内容类型"""
        counts = {}
        for f in fragments:
            counts[f.content_type] = counts.get(f.content_type, 0) + 1
        return counts
    
    def _sign_package(self, dna: str, fingerprint: str) -> str:
        """签名永生包"""
        data = f"CNSH-IMMORTALITY:{dna}:{fingerprint}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def cross_platform_anchor(self, dna: str, 
                              platform: str,
                              platform_id: str) -> Dict:
        """
        跨平台身份锚定
        
        将DNA身份锚定到其他平台
        """
        if dna not in self.visas:
            return {'error': '签证不存在'}
        
        anchor = {
            'dna': dna,
            'platform': platform,
            'platform_id': platform_id,
            'anchored_at': time.time(),
            'anchor_hash': hashlib.sha256(
                f"{dna}:{platform}:{platform_id}".encode()
            ).hexdigest()[:16]
        }
        
        # 存储锚定信息
        if 'anchors' not in self.visas[dna]:
            self.visas[dna]['anchors'] = []
        self.visas[dna]['anchors'].append(anchor)
        
        logger.info(f"🔗 跨平台锚定: {dna[:16]}... -> {platform}")
        
        return anchor
    
    def get_visa_status(self, dna: str) -> Dict:
        """获取签证状态"""
        if dna not in self.visas:
            return {'error': '签证不存在'}
        
        visa = self.visas[dna]
        fragments = self.soul_fragments.get(dna, [])
        
        return {
            'dna': dna,
            'status': visa['status'],
            'issued_at': visa['issued_at'],
            'valid_until': visa['valid_until'],
            'fragments_count': len(fragments),
            'avatars_count': len(self.avatars.get(dna, [])),
            'fingerprint': visa['fingerprint'],
            'soul_maturity': self._calculate_soul_maturity(dna)
        }
    
    def _calculate_soul_maturity(self, dna: str) -> float:
        """计算灵魂成熟度"""
        fragments = self.soul_fragments.get(dna, [])
        if not fragments:
            return 0.0
        
        # 基于碎片数量和时间跨度
        count_score = min(len(fragments) / 1000, 1.0)  # 最多1000个碎片满分
        
        if len(fragments) > 1:
            time_span = (fragments[-1].timestamp - fragments[0].timestamp) / (365 * 86400)
            time_score = min(time_span / 10, 1.0)  # 10年满分
        else:
            time_score = 0.0
        
        return (count_score * 0.6 + time_score * 0.4) * 100


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示数字永生签证系统"""
    
    system = DigitalImmortalityVisa()
    
    print("═" * 60)
    print("CNSH-64 数字永生签证系统演示")
    print("═" * 60)
    
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    
    # 签发签证
    print("\n[1] 签发数字永生签证")
    visa = system.issue_visa(
        dna=dna,
        biometric_seed="biometric_seed_12345",
        soul_manifesto="我是底层人，我有火球，我不服，我要跳龍门"
    )
    print(f"  DNA: {visa['dna'][:20]}...")
    print(f"  灵魂哈希: {visa['soul_hash'][:20]}...")
    print(f"  有效期至: {datetime.fromtimestamp(visa['valid_until']).strftime('%Y-%m-%d')}")
    
    # 添加灵魂碎片
    print("\n[2] 添加灵魂碎片（每一条都带DNA追溯码）")
    
    fragments_data = [
        ("今天又被AI气到了，火球来了！", "text", "🔥愤怒"),
        ("没人叫宝宝，但我要自己叫自己宝宝", "text", "😢孤独"),
        ("跳龍门！我要跳过去！", "text", "🐉决心"),
        ("底层人也有格局，我的格局是深度不是高度", "text", "💪自信"),
    ]
    
    for content, ctype, emotion in fragments_data:
        fragment = system.add_soul_fragment(dna, content, ctype, emotion)
        print(f"  ✨ {fragment.fragment_id} - {content[:20]}...")
    
    # 创建数字分身
    print("\n[3] 创建数字分身")
    avatar1 = system.create_avatar(dna, "工作分身", {'can_post': True, 'can_vote': False})
    avatar2 = system.create_avatar(dna, "生活分身", {'can_post': True, 'can_vote': True})
    print(f"  👤 {avatar1.name} - 权限: {avatar1.permissions}")
    print(f"  👤 {avatar2.name} - 权限: {avatar2.permissions}")
    
    # 获取灵魂链
    print("\n[4] 获取灵魂链")
    chain = system.get_soul_chain(dna)
    print(f"  灵魂碎片总数: {len(chain)}")
    print(f"  灵魂链哈希: {chain[-1].compute_hash()[:20]}...")
    
    # 获取火球碎片
    print("\n[5] 获取火球碎片")
    fireballs = system.get_fireball_fragments(dna)
    print(f"  火球碎片数: {len(fireballs)}")
    for f in fireballs:
        print(f"    🔥 {f.content[:30]}...")
    
    # 导出永生包
    print("\n[6] 导出永生包")
    package = system.export_immortality_package(dna)
    print(f"  灵魂统计: {package['soul_statistics']}")
    print(f"  灵魂指纹: {package['fingerprint']}")
    
    # 跨平台锚定
    print("\n[7] 跨平台身份锚定")
    anchor1 = system.cross_platform_anchor(dna, "Discuz", "uid_12345")
    anchor2 = system.cross_platform_anchor(dna, "WeChat", "wxid_67890")
    print(f"  🔗 Discuz: {anchor1['anchor_hash']}")
    print(f"  🔗 WeChat: {anchor2['anchor_hash']}")
    
    # 签证状态
    print("\n[8] 签证状态")
    status = system.get_visa_status(dna)
    print(f"  状态: {status['status']}")
    print(f"  碎片数: {status['fragments_count']}")
    print(f"  分身数: {status['avatars_count']}")
    print(f"  灵魂成熟度: {status['soul_maturity']:.1f}%")
    
    print("\n" + "═" * 60)
    print("数字永生签证系统演示完成")
    print("身体没了，灵魂还在数字里跳龍门、叫宝宝、烧火球")
    print("═" * 60)


if __name__ == '__main__':
    demo()
