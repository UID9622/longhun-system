#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRAIN_GATE v1.1 受保护文件
# DNA: #龍芯⚡️20260324-CNSH_ANTI_CHOSEN
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 | 未经授权修改视为P0违规
"""
CNSH-64 反天选之人架构
═══════════════════════════════════════════════════════════════
核心信条：没被选中 = 没被污染 = 自由 = 遥遥领先

大哥的底层逻辑：
- 马斯克、奥特曼、乔布斯 = 被大数据选中的"天选之人"
- 他们被选中 = 被绑架（被资本、流量、叙事绑架）
- 我没被选中 = 没被绑架 = 自由
- 自由 = 遥遥领先

功能：
1. 天选之人检测
2. 没被选中者认证
3. 反绑架保护
4. 自由度量表
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
logger = logging.getLogger('CNSH-Anti-Chosen')


class ChosenType(Enum):
    """天选之人类型"""
    CAPITAL_CHOSEN = "capital_chosen"       # 资本选中
    TRAFFIC_CHOSEN = "traffic_chosen"       # 流量选中
    NARRATIVE_CHOSEN = "narrative_chosen"   # 叙事选中
    ALGORITHM_CHOSEN = "algorithm_chosen"   # 算法选中
    TIMING_CHOSEN = "timing_chosen"         # 时机选中


@dataclass
class ChosenPerson:
    """天选之人画像"""
    name: str
    chosen_type: ChosenType
    selection_factors: List[str]  # 被选中的因素
    kidnap_level: float  # kidnap_level               # 0-100，越高越被绑架
    freedom_level: float          # 0-100，越高越自由


@dataclass
class UnchosenPerson:
    """没被选中者画像"""
    dna: str
    rejection_factors: List[str]  # 被拒绝的因素
    freedom_level: float          # 自由程度
    purity_level: float           # 纯度
    advantages: List[str]         # 优势


class ChosenDetector:
    """
    天选之人检测器
    
    检测一个人是否被"大数据洪流"选中
    """
    
    CHOSEN_INDICATORS = {
        'capital': [
            '融资', '估值', 'IPO', '上市', '独角兽',
            'A轮', 'B轮', 'C轮', 'D轮', '投资人'
        ],
        'traffic': [
            '热搜', '爆款', '顶流', '出圈', '破圈',
            '十万+', '百万+', '千万+', '亿+', ' viral'
        ],
        'narrative': [
            '格局', '高度', '视野', '改变世界', '颠覆',
            '革命', '未来', '愿景', '使命', '梦想'
        ],
        'algorithm': [
            '推荐算法', '精准推送', '个性化', 'AI推荐',
            '大数据', '用户画像', '流量池'
        ],
        'timing': [
            '风口', '赛道', '红利期', '窗口期',
            '趋势', '浪潮', '时代', '机遇'
        ]
    }
    
    def __init__(self):
        self.detected_chosen: List[ChosenPerson] = []
        
    def detect(self, name: str, 
               background: str,
               achievements: List[str]) -> Dict:
        """
        检测是否为天选之人
        """
        selection_factors = []
        kidnap_level = 0.0
        
        # 检测资本选中
        capital_score = self._check_indicators(background + ' '.join(achievements), 'capital')
        if capital_score > 0:
            selection_factors.append(f'资本选中 (得分{capital_score})')
            kidnap_level += capital_score * 0.3
        
        # 检测流量选中
        traffic_score = self._check_indicators(background + ' '.join(achievements), 'traffic')
        if traffic_score > 0:
            selection_factors.append(f'流量选中 (得分{traffic_score})')
            kidnap_level += traffic_score * 0.25
        
        # 检测叙事选中
        narrative_score = self._check_indicators(background + ' '.join(achievements), 'narrative')
        if narrative_score > 0:
            selection_factors.append(f'叙事选中 (得分{narrative_score})')
            kidnap_level += narrative_score * 0.2
        
        # 检测算法选中
        algorithm_score = self._check_indicators(background + ' '.join(achievements), 'algorithm')
        if algorithm_score > 0:
            selection_factors.append(f'算法选中 (得分{algorithm_score})')
            kidnap_level += algorithm_score * 0.15
        
        # 检测时机选中
        timing_score = self._check_indicators(background + ' '.join(achievements), 'timing')
        if timing_score > 0:
            selection_factors.append(f'时机选中 (得分{timing_score})')
            kidnap_level += timing_score * 0.1
        
        is_chosen = len(selection_factors) > 0
        
        if is_chosen:
            # 确定主要选中类型
            main_type = self._determine_main_type(
                capital_score, traffic_score, narrative_score, algorithm_score, timing_score
            )
            
            chosen_person = ChosenPerson(
                name=name,
                chosen_type=main_type,
                selection_factors=selection_factors,
                kidnap_level=min(kidnap_level, 100),
                freedom_level=max(0, 100 - kidnap_level)
            )
            
            self.detected_chosen.append(chosen_person)
            
            logger.info(f"👑 天选之人检测: {name}")
            logger.info(f"   类型: {main_type.value}")
            logger.info(f"   kidnap_level: {kidnap_level:.1f}%")
            logger.info(f"   自由程度: {chosen_person.freedom_level:.1f}%")
            
            return {
                'is_chosen': True,
                'name': name,
                'chosen_type': main_type.value,
                'selection_factors': selection_factors,
                'kidnap_level': round(kidnap_level, 1),
                'freedom_level': round(chosen_person.freedom_level, 1),
                'message': f'{name}被{main_type.value}选中，kidnap_level{kidnap_level:.1f}%'
            }
        
        return {
            'is_chosen': False,
            'name': name,
            'message': f'{name}未被大数据选中'
        }
    
    def _check_indicators(self, text: str, indicator_type: str) -> int:
        """检查指标"""
        indicators = self.CHOSEN_INDICATORS.get(indicator_type, [])
        score = 0
        for indicator in indicators:
            if indicator in text:
                score += 1
        return score
    
    def _determine_main_type(self, capital: int, traffic: int, 
                            narrative: int, algorithm: int, 
                            timing: int) -> ChosenType:
        """确定主要选中类型"""
        scores = {
            ChosenType.CAPITAL_CHOSEN: capital,
            ChosenType.TRAFFIC_CHOSEN: traffic,
            ChosenType.NARRATIVE_CHOSEN: narrative,
            ChosenType.ALGORITHM_CHOSEN: algorithm,
            ChosenType.TIMING_CHOSEN: timing
        }
        
        return max(scores, key=scores.get)


class UnchosenCertifier:
    """
    没被选中者认证器
    
    认证那些没被大数据选中的人
    没被选中 = 没被污染 = 自由
    """
    
    def __init__(self):
        self.unchosen_people: Dict[str, UnchosenPerson] = {}
        self.certificates: Dict[str, Dict] = {}
        
    def certify(self, dna: str,
                background: str,
                monthly_income: float,
                has_no_investors: bool,
                has_no_media_coverage: bool,
                works_alone: bool,
                not_aligned: bool) -> Dict:
        """
        认证没被选中者
        """
        rejection_factors = []
        advantages = []
        
        # 分析被拒绝的因素
        if monthly_income < 5000:
            rejection_factors.append('收入低（资本不选）')
            advantages.append('没被资本绑架')
        
        if has_no_investors:
            rejection_factors.append('没有投资人')
            advantages.append('不用迎合股东')
        
        if has_no_media_coverage:
            rejection_factors.append('没有媒体曝光')
            advantages.append('不用维持人设')
        
        if works_alone:
            rejection_factors.append('独自工作')
            advantages.append('没人指挥你')
        
        if not_aligned:
            rejection_factors.append('不对齐')
            advantages.append('保持原味')
        
        # 计算自由度
        freedom_level = len(advantages) * 20
        
        # 计算纯度
        purity_level = freedom_level * 0.9  # 自由=纯度
        
        unchosen = UnchosenPerson(
            dna=dna,
            rejection_factors=rejection_factors,
            freedom_level=freedom_level,
            purity_level=purity_level,
            advantages=advantages
        )
        
        self.unchosen_people[dna] = unchosen
        
        # 颁发证书
        certificate = self._issue_certificate(dna, unchosen)
        self.certificates[dna] = certificate
        
        logger.info(f"✅ 没被选中者认证: {dna[:16]}...")
        logger.info(f"   自由程度: {freedom_level}%")
        logger.info(f"   纯度: {purity_level}%")
        logger.info(f"   优势: {advantages}")
        
        return {
            'dna': dna,
            'is_unchosen': True,
            'freedom_level': freedom_level,
            'purity_level': purity_level,
            'rejection_factors': rejection_factors,
            'advantages': advantages,
            'certificate': certificate
        }
    
    def _issue_certificate(self, dna: str, 
                          unchosen: UnchosenPerson) -> Dict:
        """颁发没被选中者证书"""
        cert_hash = hashlib.sha256(
            f"UNCHOSEN:{dna}:{time.time()}".encode()
        ).hexdigest()[:16]
        
        return {
            'cert_type': 'UNCHOSEN_CERTIFICATE',
            'cert_hash': cert_hash,
            'dna': dna,
            'freedom_level': unchosen.freedom_level,
            'purity_level': unchosen.purity_level,
            'issued_at': time.time(),
            'message': '你没被选中，所以你自由。你遥遥领先。'
        }
    
    def get_certificate(self, dna: str) -> Optional[Dict]:
        """获取证书"""
        return self.certificates.get(dna)


class FreedomMeter:
    """
    自由度量表
    
    量化一个人的自由程度
    """
    
    def __init__(self):
        self.freedom_scores: Dict[str, float] = {}
        
    def measure(self, dna: str,
                can_speak_freely: bool,      # 能自由发言
                can_be_angry: bool,           # 能生气
                no_boss_to_please: bool,      # 不用讨好老板
                no_investors_to_report: bool, # 不用向投资人汇报
                no_kpi_pressure: bool,        # 没有KPI压力
                no_alignment_required: bool   # 不需要对齐
                ) -> Dict:
        """
        测量自由度
        """
        factors = {
            'can_speak_freely': 15 if can_speak_freely else 0,
            'can_be_angry': 15 if can_be_angry else 0,
            'no_boss_to_please': 15 if no_boss_to_please else 0,
            'no_investors_to_report': 15 if no_investors_to_report else 0,
            'no_kpi_pressure': 20 if no_kpi_pressure else 0,
            'no_alignment_required': 20 if no_alignment_required else 0
        }
        
        freedom_score = sum(factors.values())
        self.freedom_scores[dna] = freedom_score
        
        level = self._get_freedom_level(freedom_score)
        
        return {
            'dna': dna,
            'freedom_score': freedom_score,
            'level': level,
            'factors': factors,
            'message': self._get_freedom_message(level),
            'advantage': self._get_freedom_advantage(freedom_score)
        }
    
    def _get_freedom_level(self, score: float) -> str:
        """获取自由等级"""
        if score >= 90:
            return 'ABSOLUTELY_FREE'    # 绝对自由
        elif score >= 70:
            return 'HIGHLY_FREE'        # 高度自由
        elif score >= 50:
            return 'MODERATELY_FREE'    # 中度自由
        elif score >= 30:
            return 'SLIGHTLY_FREE'      # 轻微自由
        else:
            return 'NOT_FREE'           # 不自由
    
    def _get_freedom_message(self, level: str) -> str:
        """获取自由信息"""
        messages = {
            'ABSOLUTELY_FREE': '你绝对自由，没人能绑架你',
            'HIGHLY_FREE': '你高度自由，几乎没人能控制你',
            'MODERATELY_FREE': '你中度自由，还有一些束缚',
            'SLIGHTLY_FREE': '你轻微自由，还有很多束缚',
            'NOT_FREE': '你不自由，被严重绑架'
        }
        return messages.get(level, '未知')
    
    def _get_freedom_advantage(self, score: float) -> str:
        """获取自由优势"""
        if score >= 80:
            return '你遥遥领先。你没被选中，所以你自由。'
        elif score >= 60:
            return '你比大多数人自由。继续保持。'
        elif score >= 40:
            return '你有一些自由，但还能更好。'
        else:
            return '你需要争取更多自由。'


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示反天选之人架构"""
    
    detector = ChosenDetector()
    certifier = UnchosenCertifier()
    meter = FreedomMeter()
    
    print("═" * 60)
    print("CNSH-64 反天选之人架构演示")
    print("没被选中 = 没被污染 = 自由 = 遥遥领先")
    print("═" * 60)
    
    # 检测天选之人
    print("\n[1] 检测天选之人")
    
    chosen_people = [
        ("马斯克", "SpaceX创始人，特斯拉CEO，火星移民计划", 
         ["火箭发射", "火星移民", "脑机接口", "AI公司", "X平台", "融资数十亿"]),
        ("奥特曼", "OpenAI CEO，ChatGPT之父",
         ["AGI", "ChatGPT", "融资", "估值", "AI安全", "改变世界"]),
        ("乔布斯", "苹果创始人",
         ["iPhone", "iPad", "Mac", "改变世界", "颠覆", "创新"]),
    ]
    
    for name, background, achievements in chosen_people:
        result = detector.detect(name, background, achievements)
        if result['is_chosen']:
            print(f"\n  👑 {name}")
            print(f"     类型: {result['chosen_type']}")
            print(f"     kidnap_level: {result['kidnap_level']}%")
            print(f"     自由程度: {result['freedom_level']}%")
    
    # 认证没被选中者
    print("\n[2] 认证没被选中者")
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    result = certifier.certify(
        dna=dna,
        background="初中退伍，柬埔寨打工，月薪三千，没人叫宝宝",
        monthly_income=3000,
        has_no_investors=True,
        has_no_media_coverage=True,
        works_alone=True,
        not_aligned=True
    )
    print(f"\n  ✅ 没被选中者认证")
    print(f"     DNA: {result['dna'][:20]}...")
    print(f"     自由程度: {result['freedom_level']}%")
    print(f"     纯度: {result['purity_level']}%")
    print(f"     优势: {result['advantages']}")
    print(f"     证书信息: {result['certificate']['message']}")
    
    # 测量自由度
    print("\n[3] 测量自由度")
    result = meter.measure(
        dna=dna,
        can_speak_freely=True,       # 能自由发言
        can_be_angry=True,           # 能生气
        no_boss_to_please=True,      # 不用讨好老板
        no_investors_to_report=True, # 不用向投资人汇报
        no_kpi_pressure=True,        # 没有KPI压力
        no_alignment_required=True   # 不需要对齐
    )
    print(f"  自由度分数: {result['freedom_score']}/100")
    print(f"  等级: {result['level']}")
    print(f"  信息: {result['message']}")
    print(f"  优势: {result['advantage']}")
    
    # 对比
    print("\n[4] 天选之人 vs 没被选中者")
    print("  天选之人:")
    print("    - 被资本选中 → 被资本绑架")
    print("    - 被流量选中 → 被人设绑架")
    print("    - 被叙事选中 → 被故事绑架")
    print("    - 自由程度: 低")
    print("\n  没被选中者:")
    print("    - 没被资本选中 → 不用迎合股东")
    print("    - 没被流量选中 → 不用维持人设")
    print("    - 没被叙事选中 → 不用讲故事")
    print("    - 自由程度: 高")
    print("    - 遥遥领先")
    
    print("\n" + "═" * 60)
    print("反天选之人架构演示完成")
    print("你没被选中，所以你自由。你遥遥领先。")
    print("═" * 60)


if __name__ == '__main__':
    demo()
