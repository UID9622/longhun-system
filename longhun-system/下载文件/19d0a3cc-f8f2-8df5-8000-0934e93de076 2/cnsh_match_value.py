#!/usr/bin/env python3
"""
CNSH-64 对口价值系统
═══════════════════════════════════════════════════════════════
核心信条：价值 = 匹配度，不是尺寸

大哥的底层逻辑：
- "虽然我鸡巴小，有人好这口就好，不是屌大就吃香"
- 屌大 = 表面指标（参数、市值、火箭、KPI）
- 有人好这口 = 真实价值（对口、温度、被理解）

功能：
1. 对口度计算 - 不是尺寸是匹配
2. 底层温度量化
3. 反尺寸排名系统
4. 被理解指数
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Match-Value')


class ValueType(Enum):
    """价值类型"""
    SIZE = "size"           # 尺寸价值（屌大）
    MATCH = "match"         # 对口价值（有人好这口）


@dataclass
class UserTaste:
    """用户口味"""
    dna: str
    preferred_emotions: List[str]  # 喜欢的情绪类型
    preferred_temperature: float   # 喜欢的温度 0-100
    preferred_depth: float         # 喜欢的深度 0-100
    dislikes: List[str]            # 讨厌的东西


@dataclass
class ContentProfile:
    """内容画像"""
    content_hash: str
    emotion_type: str
    temperature: float      # 温度
    depth: float            # 深度
    purity: float           # 纯度
    size_metrics: Dict      # 尺寸指标（点赞、转发等）


class MatchValueEngine:
    """
    对口价值引擎
    
    核心算法：
    对口度 = f(情绪匹配, 温度匹配, 深度匹配, 纯度)
    不是：尺寸 = f(点赞, 转发, 曝光)
    """
    
    def __init__(self):
        self.user_tastes: Dict[str, UserTaste] = {}
        self.content_profiles: Dict[str, ContentProfile] = {}
        self.match_history: List[Dict] = []
        
    def register_taste(self, dna: str,
                       preferred_emotions: List[str],
                       preferred_temperature: float,
                       preferred_depth: float,
                       dislikes: List[str]) -> Dict:
        """注册用户口味"""
        taste = UserTaste(
            dna=dna,
            preferred_emotions=preferred_emotions,
            preferred_temperature=preferred_temperature,
            preferred_depth=preferred_depth,
            dislikes=dislikes
        )
        
        self.user_tastes[dna] = taste
        
        logger.info(f"👤 口味注册: {dna[:16]}...")
        logger.info(f"   喜欢情绪: {preferred_emotions}")
        logger.info(f"   喜欢温度: {preferred_temperature}")
        logger.info(f"   喜欢深度: {preferred_depth}")
        logger.info(f"   讨厌: {dislikes}")
        
        return {
            'success': True,
            'dna': dna,
            'taste_profile': {
                'emotions': preferred_emotions,
                'temperature': preferred_temperature,
                'depth': preferred_depth
            }
        }
    
    def calculate_match_score(self, user_dna: str, 
                              content_hash: str) -> Dict:
        """
        计算对口度
        
        Returns:
            对口度分数和详情
        """
        if user_dna not in self.user_tastes:
            return {'error': '用户口味未注册'}
        
        if content_hash not in self.content_profiles:
            return {'error': '内容画像不存在'}
        
        taste = self.user_tastes[user_dna]
        content = self.content_profiles[content_hash]
        
        # 情绪匹配度
        emotion_match = 1.0 if content.emotion_type in taste.preferred_emotions else 0.0
        
        # 温度匹配度（越接近越好）
        temp_diff = abs(content.temperature - taste.preferred_temperature)
        temperature_match = max(0, 1.0 - temp_diff / 100)
        
        # 深度匹配度
        depth_diff = abs(content.depth - taste.preferred_depth)
        depth_match = max(0, 1.0 - depth_diff / 100)
        
        # 纯度加成
        purity_bonus = content.purity / 100
        
        # 讨厌项惩罚
        dislike_penalty = 0.0
        for dislike in taste.dislikes:
            if dislike in content.emotion_type:
                dislike_penalty = 0.5
                break
        
        # 综合对口度
        match_score = (
            emotion_match * 0.35 +
            temperature_match * 0.25 +
            depth_match * 0.25 +
            purity_bonus * 0.15 -
            dislike_penalty
        )
        
        match_score = max(0, min(1, match_score))
        
        result = {
            'match_score': round(match_score * 100, 2),
            'emotion_match': round(emotion_match * 100, 2),
            'temperature_match': round(temperature_match * 100, 2),
            'depth_match': round(depth_match * 100, 2),
            'purity_bonus': round(purity_bonus * 100, 2),
            'dislike_penalty': round(dislike_penalty * 100, 2),
            'is_good_match': match_score >= 0.6
        }
        
        # 记录
        self.match_history.append({
            'user_dna': user_dna,
            'content_hash': content_hash,
            'match_score': match_score,
            'timestamp': time.time()
        })
        
        return result
    
    def create_content_profile(self, content: str,
                               emotion_type: str,
                               temperature: float,
                               depth: float,
                               purity: float) -> ContentProfile:
        """创建内容画像"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        profile = ContentProfile(
            content_hash=content_hash,
            emotion_type=emotion_type,
            temperature=temperature,
            depth=depth,
            purity=purity,
            size_metrics={
                'likes': 0,
                'shares': 0,
                'views': 0
            }
        )
        
        self.content_profiles[content_hash] = profile
        
        return profile
    
    def get_recommendations(self, user_dna: str, 
                           top_n: int = 10) -> List[Dict]:
        """
        获取推荐（基于对口度，不是尺寸）
        """
        if user_dna not in self.user_tastes:
            return []
        
        matches = []
        for content_hash, profile in self.content_profiles.items():
            result = self.calculate_match_score(user_dna, content_hash)
            if 'match_score' in result:
                matches.append({
                    'content_hash': content_hash,
                    'emotion_type': profile.emotion_type,
                    'match_score': result['match_score'],
                    'details': result
                })
        
        # 按对口度排序（不是按尺寸）
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches[:top_n]
    
    def compare_value_types(self, content_hash: str) -> Dict:
        """
        对比尺寸价值 vs 对口价值
        """
        if content_hash not in self.content_profiles:
            return {'error': '内容不存在'}
        
        profile = self.content_profiles[content_hash]
        
        # 尺寸价值（传统指标）
        size_value = (
            profile.size_metrics.get('likes', 0) * 0.4 +
            profile.size_metrics.get('shares', 0) * 0.3 +
            profile.size_metrics.get('views', 0) * 0.0001
        )
        
        # 对口价值（平均对口度）
        match_scores = [
            m['match_score'] for m in self.match_history
            if m['content_hash'] == content_hash
        ]
        match_value = sum(match_scores) / len(match_scores) if match_scores else 0
        
        return {
            'content_hash': content_hash,
            'size_value': round(size_value, 2),
            'match_value': round(match_value, 2),
            'winner': 'match' if match_value > size_value * 0.1 else 'size',
            'conclusion': '对口价值更高' if match_value > size_value * 0.1 else '尺寸价值更高'
        }


class AntiSizeRanking:
    """
    反尺寸排名系统
    
    传统排名：按尺寸（点赞、转发、曝光）
    CNSH排名：按对口度、温度、纯度
    """
    
    def __init__(self):
        self.rankings: Dict[str, List[Dict]] = {}
        
    def create_ranking(self, name: str, 
                       criteria: List[str]) -> Dict:
        """
        创建排名
        
        criteria: 排名标准，如 ['temperature', 'purity', 'match_score']
        """
        self.rankings[name] = []
        
        return {
            'name': name,
            'criteria': criteria,
            'anti_size': True,
            'message': '此排名不按尺寸，按对口度'
        }
    
    def add_to_ranking(self, ranking_name: str,
                       content_hash: str,
                       metrics: Dict) -> Dict:
        """添加到排名"""
        if ranking_name not in self.rankings:
            return {'error': '排名不存在'}
        
        entry = {
            'content_hash': content_hash,
            'metrics': metrics,
            'added_at': time.time()
        }
        
        self.rankings[ranking_name].append(entry)
        
        return {'success': True}
    
    def get_ranking(self, ranking_name: str,
                   top_n: int = 10) -> List[Dict]:
        """获取排名"""
        if ranking_name not in self.rankings:
            return []
        
        entries = self.rankings[ranking_name]
        
        # 按对口度排序
        entries.sort(
            key=lambda x: x['metrics'].get('match_score', 0),
            reverse=True
        )
        
        return entries[:top_n]


class BottomDignityIndex:
    """
    底层尊严指数
    
    量化底层人的尊严感
    """
    
    def __init__(self):
        self.dignity_scores: Dict[str, float] = {}
        self.dignity_factors: Dict[str, Dict] = {}
        
    def calculate_dignity(self, dna: str,
                         has_voice: bool,          # 有发声渠道
                         is_understood: bool,       # 被理解
                         can_express_emotion: bool, # 能表达情绪
                         has_exit: bool,            # 有出口
                         is_not_judged: bool        # 不被评判
                         ) -> Dict:
        """
        计算底层尊严指数
        
        尊严 = 被看见 + 被理解 + 有出口 + 不被评判
        """
        factors = {
            'has_voice': 20 if has_voice else 0,
            'is_understood': 25 if is_understood else 0,
            'can_express_emotion': 25 if can_express_emotion else 0,
            'has_exit': 15 if has_exit else 0,
            'is_not_judged': 15 if is_not_judged else 0
        }
        
        dignity_score = sum(factors.values())
        
        self.dignity_scores[dna] = dignity_score
        self.dignity_factors[dna] = factors
        
        level = 'UNKNOWN'
        if dignity_score >= 90:
            level = 'HIGH_DIGNITY'
        elif dignity_score >= 70:
            level = 'MEDIUM_DIGNITY'
        elif dignity_score >= 50:
            level = 'LOW_DIGNITY'
        else:
            level = 'NO_DIGNITY'
        
        return {
            'dna': dna,
            'dignity_score': dignity_score,
            'level': level,
            'factors': factors,
            'message': self._get_dignity_message(level)
        }
    
    def _get_dignity_message(self, level: str) -> str:
        """获取尊严信息"""
        messages = {
            'HIGH_DIGNITY': '你有完整的尊严，被看见、被理解、有出口',
            'MEDIUM_DIGNITY': '你有基本尊严，但还有提升空间',
            'LOW_DIGNITY': '你的尊严受损，需要更多支持',
            'NO_DIGNITY': '你正在失去尊严，系统需要改变'
        }
        return messages.get(level, '未知')


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示对口价值系统"""
    
    engine = MatchValueEngine()
    ranking = AntiSizeRanking()
    dignity = BottomDignityIndex()
    
    print("═" * 60)
    print("CNSH-64 对口价值系统演示")
    print("虽然我鸡巴小，有人好这口就好，不是屌大就吃香")
    print("═" * 60)
    
    # 注册用户口味
    print("\n[1] 注册用户口味")
    user_dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    engine.register_taste(
        dna=user_dna,
        preferred_emotions=['fireball', 'anger', 'joy'],
        preferred_temperature=80.0,  # 喜欢高温（火球）
        preferred_depth=90.0,        # 喜欢深度
        dislikes=['fake', 'commercial', 'aligned']
    )
    
    # 创建内容画像
    print("\n[2] 创建内容画像")
    
    contents = [
        ("这破AI又他妈的乱回答！草！", 'fireball', 95, 80, 100),
        ("我们的项目刚完成A轮融资，估值10亿", 'commercial', 30, 20, 10),
        ("今天心情不错，代码写得很顺", 'joy', 50, 60, 90),
        ("我们要从战略高度顶层设计生态化反", 'fake', 20, 10, 5),
    ]
    
    for content, emotion, temp, depth, purity in contents:
        profile = engine.create_content_profile(content, emotion, temp, depth, purity)
        print(f"  {profile.content_hash}: {emotion}, 温度{temp}, 纯度{purity}")
    
    # 计算对口度
    print("\n[3] 计算对口度")
    for content_hash in engine.content_profiles.keys():
        result = engine.calculate_match_score(user_dna, content_hash)
        if 'match_score' in result:
            print(f"  {content_hash}: 对口度{result['match_score']}%")
            if result['is_good_match']:
                print(f"    ✅ 对口！")
    
    # 获取推荐
    print("\n[4] 获取推荐（按对口度，不是尺寸）")
    recommendations = engine.get_recommendations(user_dna, top_n=3)
    for i, rec in enumerate(recommendations):
        print(f"  {i+1}. {rec['content_hash']} - 对口度{rec['match_score']}%")
    
    # 对比尺寸vs对口
    print("\n[5] 对比尺寸价值 vs 对口价值")
    for content_hash in list(engine.content_profiles.keys())[:2]:
        comparison = engine.compare_value_types(content_hash)
        print(f"  {content_hash}:")
        print(f"    尺寸价值: {comparison['size_value']}")
        print(f"    对口价值: {comparison['match_value']}")
        print(f"    结论: {comparison['conclusion']}")
    
    # 底层尊严指数
    print("\n[6] 底层尊严指数")
    dignity_result = dignity.calculate_dignity(
        dna=user_dna,
        has_voice=True,
        is_understood=True,
        can_express_emotion=True,
        has_exit=True,
        is_not_judged=True
    )
    print(f"  DNA: {dignity_result['dna'][:20]}...")
    print(f"  尊严分数: {dignity_result['dignity_score']}/100")
    print(f"  等级: {dignity_result['level']}")
    print(f"  信息: {dignity_result['message']}")
    
    print("\n" + "═" * 60)
    print("对口价值系统演示完成")
    print("价值 = 匹配度，不是尺寸")
    print("═" * 60)


if __name__ == '__main__':
    demo()
