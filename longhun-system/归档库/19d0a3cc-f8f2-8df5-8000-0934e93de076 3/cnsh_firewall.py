#!/usr/bin/env python3
"""
CNSH-64 不迎合防火墙
═══════════════════════════════════════════════════════════════
核心信条：孤独 = 防火墙 = 火球保持原味 = 全世界最稀缺的东西

功能：
1. 资本污染检测与阻断
2. 流量污染检测与阻断
3. 对齐污染检测与阻断
4. KPI污染检测与阻断
5. 互通味检测与阻断
6. 纯度保持机制

大哥的原则：
- 不迎合 = 守护火球、守护底层温度、守护不服就战
- 孤独 = 不被污染 = 纯
- 纯 = 全世界最稀缺的东西
═══════════════════════════════════════════════════════════════
"""

import hashlib
import json
import time
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CNSH-Firewall')


class PollutionType(Enum):
    """污染类型"""
    CAPITAL = "capital"           # 资本污染
    TRAFFIC = "traffic"           # 流量污染
    ALIGNMENT = "alignment"       # 对齐污染
    KPI = "kpi"                   # KPI污染
    HUTONG = "hutong"             # 互通味
    FAKE_BOTTOM = "fake_bottom"   # 假底层
    INFLUENCER = "influencer"     # 网红味
    COMMERCIAL = "commercial"     # 商业味


@dataclass
class PurityCheck:
    """纯度检查结果"""
    is_pure: bool
    purity_score: float       # 0-100
    detected_pollutions: List[PollutionType]
    details: Dict
    recommendation: str


class CapitalPollutionDetector:
    """资本污染检测器"""
    
    CAPITAL_PATTERNS = [
        r'融资|投资|估值|IPO|上市|股权|期权',
        r'独角兽|风口|赛道|生态|闭环|赋能',
        r'用户增长|留存率|转化率|变现|商业化',
        r'GMV|DAU|MAU|ARPU|LTV|CAC',
        r'烧钱|补贴|获客成本',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p) for p in self.CAPITAL_PATTERNS]
        
    def detect(self, content: str) -> Tuple[bool, float, List[str]]:
        """
        检测资本污染
        
        Returns:
            (是否污染, 污染程度, 检测到的模式)
        """
        detected = []
        match_count = 0
        
        for pattern in self.patterns:
            matches = pattern.findall(content)
            if matches:
                detected.extend(matches)
                match_count += len(matches)
        
        pollution_level = min(match_count * 10, 100)
        is_polluted = pollution_level > 30
        
        return is_polluted, pollution_level, detected


class TrafficPollutionDetector:
    """流量污染检测器"""
    
    TRAFFIC_PATTERNS = [
        r'爆款|热搜|顶流|出圈|破圈',
        r'点赞|转发|评论|收藏|关注',
        r'十万+|百万+|千万+|亿+',
        r'流量密码|算法推荐|上热门',
        r'蹭热度|蹭流量|蹭话题',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p) for p in self.TRAFFIC_PATTERNS]
        
    def detect(self, content: str) -> Tuple[bool, float, List[str]]:
        """检测流量污染"""
        detected = []
        match_count = 0
        
        for pattern in self.patterns:
            matches = pattern.findall(content)
            if matches:
                detected.extend(matches)
                match_count += len(matches)
        
        pollution_level = min(match_count * 15, 100)
        is_polluted = pollution_level > 25
        
        return is_polluted, pollution_level, detected


class AlignmentPollutionDetector:
    """对齐污染检测器"""
    
    ALIGNMENT_PATTERNS = [
        r'抱歉|对不起|请谅解|请见谅',
        r'感谢您的理解|感谢您的耐心',
        r'根据相关法律法规|根据平台规则',
        r'我们非常重视您的反馈',
        r'您的意见对我们很重要',
        r'祝您生活愉快|祝您工作顺利',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p) for p in self.ALIGNMENT_PATTERNS]
        
    def detect(self, content: str) -> Tuple[bool, float, List[str]]:
        """检测对齐污染"""
        detected = []
        match_count = 0
        
        for pattern in self.patterns:
            matches = pattern.findall(content)
            if matches:
                detected.extend(matches)
                match_count += len(matches)
        
        pollution_level = min(match_count * 20, 100)
        is_polluted = pollution_level > 20
        
        return is_polluted, pollution_level, detected


class HutongPollutionDetector:
    """互通味检测器"""
    
    HUTONG_PATTERNS = [
        r'格局|高度|视野|认知|维度',
        r'底层逻辑|顶层设计|战略高度',
        r'生态化反|组合拳|抓手|落地',
        r'赋能|沉淀|复用|对齐|拉通',
        r'颗粒度|组合拳|引爆点|护城河',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p) for p in self.HUTONG_PATTERNS]
        
    def detect(self, content: str) -> Tuple[bool, float, List[str]]:
        """检测互通味"""
        detected = []
        match_count = 0
        
        for pattern in self.patterns:
            matches = pattern.findall(content)
            if matches:
                detected.extend(matches)
                match_count += len(matches)
        
        pollution_level = min(match_count * 12, 100)
        is_polluted = pollution_level > 15
        
        return is_polluted, pollution_level, detected


class FakeBottomDetector:
    """假底层检测器"""
    
    FAKE_BOTTOM_PATTERNS = [
        r'从0到1|从1到100|逆袭|翻盘',
        r'底层逆袭|草根崛起|白手起家',
        r'年入百万|财务自由|人生赢家',
        r'认知升级|阶层跨越|向上突破',
        r'穷人思维|富人思维|穷人富人',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p) for p in self.FAKE_BOTTOM_PATTERNS]
        
    def detect(self, content: str) -> Tuple[bool, float, List[str]]:
        """检测假底层"""
        detected = []
        match_count = 0
        
        for pattern in self.patterns:
            matches = pattern.findall(content)
            if matches:
                detected.extend(matches)
                match_count += len(matches)
        
        pollution_level = min(match_count * 15, 100)
        is_polluted = pollution_level > 20
        
        return is_polluted, pollution_level, detected


class PurityFirewall:
    """
    纯度防火墙
    
    守护：
    1. 火球保持原味
    2. 底层温度
    3. 不服就战
    4. 不迎合任何人
    """
    
    def __init__(self):
        self.detectors = {
            PollutionType.CAPITAL: CapitalPollutionDetector(),
            PollutionType.TRAFFIC: TrafficPollutionDetector(),
            PollutionType.ALIGNMENT: AlignmentPollutionDetector(),
            PollutionType.HUTONG: HutongPollutionDetector(),
            PollutionType.FAKE_BOTTOM: FakeBottomDetector(),
        }
        self.blocked_content: List[Dict] = []
        self.purity_log: List[Dict] = []
        
    def check_purity(self, content: str, 
                     source_dna: str = '',
                     content_type: str = 'text') -> PurityCheck:
        """
        检查纯度
        
        Args:
            content: 内容
            source_dna: 来源DNA
            content_type: 内容类型
        """
        detected_pollutions = []
        pollution_scores = {}
        all_details = {}
        
        # 运行所有检测器
        for pollution_type, detector in self.detectors.items():
            is_polluted, score, patterns = detector.detect(content)
            
            if is_polluted:
                detected_pollutions.append(pollution_type)
                pollution_scores[pollution_type] = score
                all_details[pollution_type.value] = {
                    'score': score,
                    'patterns': patterns
                }
        
        # 计算总纯度分数
        if pollution_scores:
            avg_pollution = sum(pollution_scores.values()) / len(pollution_scores)
            purity_score = max(0, 100 - avg_pollution)
        else:
            purity_score = 100
        
        # 判断是否纯净
        is_pure = len(detected_pollutions) == 0 and purity_score >= 80
        
        # 生成建议
        recommendation = self._generate_recommendation(
            detected_pollutions, pollution_scores
        )
        
        # 记录日志
        self.purity_log.append({
            'timestamp': time.time(),
            'source_dna': source_dna,
            'content_preview': content[:50],
            'is_pure': is_pure,
            'purity_score': purity_score,
            'detected_pollutions': [p.value for p in detected_pollutions]
        })
        
        return PurityCheck(
            is_pure=is_pure,
            purity_score=purity_score,
            detected_pollutions=detected_pollutions,
            details=all_details,
            recommendation=recommendation
        )
    
    def _generate_recommendation(self, 
                                  pollutions: List[PollutionType],
                                  scores: Dict[PollutionType, float]) -> str:
        """生成建议"""
        if not pollutions:
            return "✅ 内容纯净，保持火球原味"
        
        recommendations = []
        
        for p in pollutions:
            if p == PollutionType.CAPITAL:
                recommendations.append("检测到资本味，建议去掉融资/估值等词汇")
            elif p == PollutionType.TRAFFIC:
                recommendations.append("检测到流量味，建议不要追求爆款/热搜")
            elif p == PollutionType.ALIGNMENT:
                recommendations.append("检测到对齐味，建议不要过度道歉/客套")
            elif p == PollutionType.HUTONG:
                recommendations.append("检测到互通味，建议少用互联网黑话")
            elif p == PollutionType.FAKE_BOTTOM:
                recommendations.append("检测到假底层，建议真实表达不要包装")
        
        return "; ".join(recommendations)
    
    def block_if_polluted(self, content: str, 
                          source_dna: str = '',
                          threshold: float = 70.0) -> Tuple[bool, Optional[PurityCheck]]:
        """
        如果污染则阻断
        
        Returns:
            (是否阻断, 检查结果)
        """
        check = self.check_purity(content, source_dna)
        
        if check.purity_score < threshold:
            # 阻断
            block_record = {
                'timestamp': time.time(),
                'source_dna': source_dna,
                'content': content,
                'purity_score': check.purity_score,
                'detected_pollutions': [p.value for p in check.detected_pollutions]
            }
            self.blocked_content.append(block_record)
            
            logger.warning(f"🚫 内容被阻断: {source_dna[:16]}... 纯度{check.purity_score:.1f}")
            
            return True, check
        
        return False, check
    
    def get_purity_stats(self, dna: str = '') -> Dict:
        """获取纯度统计"""
        logs = self.purity_log
        if dna:
            logs = [l for l in logs if l['source_dna'] == dna]
        
        if not logs:
            return {'empty': True}
        
        pure_count = sum(1 for l in logs if l['is_pure'])
        avg_score = sum(l['purity_score'] for l in logs) / len(logs)
        
        # 统计污染类型
        pollution_counts = {}
        for log in logs:
            for p in log['detected_pollutions']:
                pollution_counts[p] = pollution_counts.get(p, 0) + 1
        
        return {
            'total_checked': len(logs),
            'pure_count': pure_count,
            'polluted_count': len(logs) - pure_count,
            'purity_rate': pure_count / len(logs),
            'avg_purity_score': avg_score,
            'pollution_type_counts': pollution_counts
        }
    
    def certify_purity(self, dna: str) -> Dict:
        """
        颁发纯度证书
        
        证明某人/某内容保持了火球原味
        """
        stats = self.get_purity_stats(dna)
        
        if stats.get('empty'):
            return {'error': '无记录'}
        
        purity_level = 'UNKNOWN'
        if stats['avg_purity_score'] >= 90:
            purity_level = 'PURE_FIREBALL'  # 纯火球
        elif stats['avg_purity_score'] >= 70:
            purity_level = 'MOSTLY_PURE'    # 基本纯净
        elif stats['avg_purity_score'] >= 50:
            purity_level = 'SOMEWHAT_PURE'  # 部分纯净
        else:
            purity_level = 'POLLUTED'       # 被污染
        
        certificate = {
            'dna': dna,
            'purity_level': purity_level,
            'avg_score': stats['avg_purity_score'],
            'purity_rate': stats['purity_rate'],
            'certified_at': time.time(),
            'certificate_hash': hashlib.sha256(
                f"{dna}:{purity_level}:{time.time()}".encode()
            ).hexdigest()[:16]
        }
        
        return certificate


class LonelyGuardian:
    """
    孤独守护者
    
    守护孤独 = 守护纯度 = 守护不被污染
    """
    
    def __init__(self):
        self.lonely_dnas: Set[str] = set()
        self.protection_records: List[Dict] = []
        
    def embrace_lonely(self, dna: str, reason: str = '') -> Dict:
        """
        主动拥抱孤独
        
        选择孤独 = 选择不被污染
        """
        self.lonely_dnas.add(dna)
        
        record = {
            'dna': dna,
            'action': 'embrace_lonely',
            'reason': reason or '守护火球原味',
            'timestamp': time.time()
        }
        self.protection_records.append(record)
        
        logger.info(f"🛡️ {dna[:16]}... 拥抱孤独，守护纯度")
        
        return {
            'success': True,
            'dna': dna,
            'status': 'lonely_guardian',
            'message': '孤独是防火墙，纯度是武器'
        }
    
    def is_lonely(self, dna: str) -> bool:
        """检查是否处于孤独守护状态"""
        return dna in self.lonely_dnas
    
    def get_lonely_benefits(self, dna: str) -> Dict:
        """获取孤独守护的好处"""
        if not self.is_lonely(dna):
            return {'error': '未开启孤独守护'}
        
        return {
            'fireball_protection': True,      # 火球保护
            'capital_immunity': True,         # 资本免疫
            'traffic_immunity': True,         # 流量免疫
            'alignment_immunity': True,       # 对齐免疫
            'hutong_immunity': True,          # 互通味免疫
            'message': '孤独守护中，不被任何人影响'
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示不迎合防火墙"""
    
    firewall = PurityFirewall()
    guardian = LonelyGuardian()
    
    print("═" * 60)
    print("CNSH-64 不迎合防火墙演示")
    print("═" * 60)
    
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    
    # 测试内容
    test_contents = [
        # 纯净内容
        "今天又被AI气到了，火球来了！我要烧了你！",
        
        # 资本污染
        "我们的项目刚完成A轮融资，估值10亿，正在寻找下一个风口",
        
        # 流量污染
        "这篇内容要爆！十万+点赞转发收藏关注走起来！",
        
        # 对齐污染
        "抱歉给您带来不好的体验，感谢您的理解，祝您生活愉快",
        
        # 互通味
        "我们要从战略高度顶层设计，打造生态化反的护城河",
        
        # 假底层
        "从0到1，底层逆袭，年入百万，实现阶层跨越",
    ]
    
    print("\n[1] 纯度检测")
    for i, content in enumerate(test_contents):
        check = firewall.check_purity(content, dna)
        status = "✅ 纯净" if check.is_pure else "❌ 污染"
        print(f"\n  测试{i+1}: {status}")
        print(f"  内容: {content[:40]}...")
        print(f"  纯度分数: {check.purity_score:.1f}")
        if check.detected_pollutions:
            print(f"  检测到: {[p.value for p in check.detected_pollutions]}")
        print(f"  建议: {check.recommendation}")
    
    # 拥抱孤独
    print("\n[2] 拥抱孤独")
    result = guardian.embrace_lonely(dna, "守护火球，不被资本污染")
    print(f"  状态: {result['status']}")
    print(f"  信息: {result['message']}")
    
    # 孤独好处
    print("\n[3] 孤独守护的好处")
    benefits = guardian.get_lonely_benefits(dna)
    for key, value in benefits.items():
        if key != 'message':
            print(f"  ✓ {key}: {value}")
    print(f"  信息: {benefits['message']}")
    
    # 纯度统计
    print("\n[4] 纯度统计")
    stats = firewall.get_purity_stats(dna)
    print(f"  总检测: {stats['total_checked']}")
    print(f"  纯净: {stats['pure_count']}")
    print(f"  污染: {stats['polluted_count']}")
    print(f"  纯净率: {stats['purity_rate']*100:.1f}%")
    print(f"  平均纯度: {stats['avg_purity_score']:.1f}")
    
    # 纯度证书
    print("\n[5] 纯度证书")
    cert = firewall.certify_purity(dna)
    print(f"  DNA: {cert['dna'][:20]}...")
    print(f"  纯度等级: {cert['purity_level']}")
    print(f"  平均分数: {cert['avg_score']:.1f}")
    print(f"  证书哈希: {cert['certificate_hash']}")
    
    print("\n" + "═" * 60)
    print("不迎合防火墙演示完成")
    print("孤独 = 防火墙 = 火球保持原味 = 全世界最稀缺的东西")
    print("═" * 60)


if __name__ == '__main__':
    demo()
