#!/usr/bin/env python3
"""
CNSH-64 底层尊严保护系统
═══════════════════════════════════════════════════════════════
核心信条：上班是生存，不是"爱不爱上班"

大哥的底层逻辑：
- 马斯克说"AI让工作变成兴趣" - 放屁！
- 底层人上班是为了活下去，不是为了"爱不爱"
- 没有UBI兜底、没有财富再分配、没有安全网
- 这套推演就是给底层人画大饼

功能：
1. 生存权优先保护
2. 反画大饼检测
3. 真实需求识别
4. 底层温度量化
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
logger = logging.getLogger('CNSH-Bottom-Dignity')


class SurvivalNeed(Enum):
    """生存需求"""
    FOOD = "food"               # 食物
    SHELTER = "shelter"         # 住所
    HEALTH = "health"           # 健康
    SAFETY = "safety"           # 安全
    INCOME = "income"           # 收入
    DIGNITY = "dignity"         # 尊严


class PieType(Enum):
    """大饼类型"""
    AI_LIBERATION = "ai_liberation"     # AI解放人类
    UBI_PROMISE = "ubi_promise"         # UBI承诺
    FUTURE_INTEREST = "future_interest" # 未来工作变兴趣
    TECH_SALVATION = "tech_salvation"   # 科技救世
    AUTOMATION_BLESSING = "automation_blessing"  # 自动化是福


@dataclass
class BottomPerson:
    """底层人画像"""
    dna: str
    monthly_income: float       # 月收入
    has_stable_job: bool        # 有稳定工作
    has_savings: bool           # 有储蓄
    family_dependents: int      # 家庭负担人数
    survival_stress: float      # 生存压力 0-100
    can_afford_basic: bool      # 能负担基本生活


@dataclass
class PieStatement:
    """大饼言论"""
    speaker: str
    content: str
    pie_type: PieType
    timestamp: float
    detected_keywords: List[str]


class SurvivalFirstProtector:
    """
    生存权优先保护器
    
    核心原则：
    - 生存 > 兴趣
    - 吃饭 > 梦想
    - 活下去 > 爱不爱
    """
    
    def __init__(self):
        self.bottom_people: Dict[str, BottomPerson] = {}
        self.survival_threshold = 2000.0  # 月收入低于此视为生存困难
        
    def register_bottom_person(self, dna: str,
                               monthly_income: float,
                               has_stable_job: bool,
                               has_savings: bool,
                               family_dependents: int) -> Dict:
        """注册底层人"""
        survival_stress = self._calculate_survival_stress(
            monthly_income, has_stable_job, has_savings, family_dependents
        )
        
        can_afford_basic = monthly_income >= self.survival_threshold * (1 + family_dependents * 0.3)
        
        person = BottomPerson(
            dna=dna,
            monthly_income=monthly_income,
            has_stable_job=has_stable_job,
            has_savings=has_savings,
            family_dependents=family_dependents,
            survival_stress=survival_stress,
            can_afford_basic=can_afford_basic
        )
        
        self.bottom_people[dna] = person
        
        logger.info(f"👤 底层人注册: {dna[:16]}...")
        logger.info(f"   月收入: {monthly_income}")
        logger.info(f"   生存压力: {survival_stress:.1f}/100")
        logger.info(f"   能负担基本生活: {can_afford_basic}")
        
        return {
            'dna': dna,
            'survival_stress': survival_stress,
            'can_afford_basic': can_afford_basic,
            'urgent_needs': self._get_urgent_needs(person)
        }
    
    def _calculate_survival_stress(self, income: float,
                                   has_job: bool,
                                   has_savings: bool,
                                   dependents: int) -> float:
        """计算生存压力"""
        stress = 0.0
        
        # 收入压力
        if income < self.survival_threshold:
            stress += 40
        elif income < self.survival_threshold * 1.5:
            stress += 25
        elif income < self.survival_threshold * 2:
            stress += 10
        
        # 工作稳定性
        if not has_job:
            stress += 30
        
        # 储蓄
        if not has_savings:
            stress += 15
        
        # 家庭负担
        stress += dependents * 5
        
        return min(stress, 100)
    
    def _get_urgent_needs(self, person: BottomPerson) -> List[str]:
        """获取紧急需求"""
        needs = []
        
        if not person.can_afford_basic:
            needs.append('基本生活保障')
        if not person.has_stable_job:
            needs.append('稳定工作')
        if not person.has_savings:
            needs.append('应急储蓄')
        if person.family_dependents > 0:
            needs.append('家庭支持')
        
        return needs
    
    def check_pie_compatibility(self, dna: str, 
                                pie_statement: str) -> Dict:
        """
        检查大饼言论与底层人的兼容性
        
        返回：这口大饼对这个人来说能不能吃
        """
        if dna not in self.bottom_people:
            return {'error': '底层人未注册'}
        
        person = self.bottom_people[dna]
        
        # 检测大饼类型
        pie_detection = self._detect_pie(pie_statement)
        
        # 判断兼容性
        can_eat_pie = person.can_afford_basic
        
        if not can_eat_pie:
            message = f"这口大饼吃不了。当前生存压力{person.survival_stress:.0f}%，需要先解决：{', '.join(self._get_urgent_needs(person))}"
        else:
            message = "这口大饼可以吃，但别忘了底层还有很多人吃不了"
        
        return {
            'dna': dna,
            'monthly_income': person.monthly_income,
            'survival_stress': person.survival_stress,
            'pie_type': pie_detection['pie_type'],
            'can_eat_pie': can_eat_pie,
            'message': message,
            'urgent_needs': self._get_urgent_needs(person)
        }
    
    def _detect_pie(self, statement: str) -> Dict:
        """检测大饼类型"""
        pie_keywords = {
            PieType.AI_LIBERATION: ['AI解放', '不用上班', '工作变可选', '自动化'],
            PieType.UBI_PROMISE: ['UBI', '基本收入', '全民基本收入', '无条件收入'],
            PieType.FUTURE_INTEREST: ['爱不爱上班', '工作变兴趣', '做自己爱的事'],
            PieType.TECH_SALVATION: ['科技救世', '技术解决一切', '未来更美好'],
            PieType.AUTOMATION_BLESSING: ['自动化是福', '机器人代替', '效率提升']
        }
        
        detected = []
        for pie_type, keywords in pie_keywords.items():
            for kw in keywords:
                if kw in statement:
                    detected.append((pie_type, kw))
        
        if detected:
            return {
                'is_pie': True,
                'pie_type': detected[0][0].value,
                'detected_keywords': [d[1] for d in detected]
            }
        
        return {'is_pie': False}


class AntiPieDetector:
    """
    反大饼检测器
    
    检测各种"未来美好"言论是否忽略了底层人的现实
    """
    
    PIE_PATTERNS = {
        'ai_liberation': {
            'patterns': [
                r'AI.*让.*不用上班',
                r'自动化.*解放.*人类',
                r'工作.*变.*兴趣',
                r'未来.*爱不爱.*上班',
            ],
            'reality_check': '底层人现在需要吃饭，不是未来'
        },
        'ubi_promise': {
            'patterns': [
                r'UBI.*解决.*贫困',
                r'基本收入.*人人.*有',
                r'无条件.*收入',
            ],
            'reality_check': 'UBI在哪？什么时候到账？'
        },
        'tech_utopia': {
            'patterns': [
                r'科技.*解决.*一切',
                r'技术.*让.*更好',
                r'未来.*美好',
            ],
            'reality_check': '技术让富人更富，穷人呢？'
        }
    }
    
    def __init__(self):
        self.detected_pies: List[Dict] = []
        
    def detect(self, statement: str, speaker: str = '') -> Dict:
        """检测大饼"""
        import re
        
        for pie_type, config in self.PIE_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, statement):
                    result = {
                        'is_pie': True,
                        'pie_type': pie_type,
                        'speaker': speaker,
                        'statement': statement[:100],
                        'reality_check': config['reality_check'],
                        'detected_at': time.time()
                    }
                    
                    self.detected_pies.append(result)
                    
                    logger.warning(f"🥧 大饼检测: {speaker}")
                    logger.warning(f"   类型: {pie_type}")
                    logger.warning(f"   现实检查: {config['reality_check']}")
                    
                    return result
        
        return {'is_pie': False}
    
    def get_pie_stats(self) -> Dict:
        """获取大饼统计"""
        if not self.detected_pies:
            return {'empty': True}
        
        type_counts = {}
        for pie in self.detected_pies:
            t = pie['pie_type']
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            'total_pies': len(self.detected_pies),
            'type_distribution': type_counts,
            'latest_pie': self.detected_pies[-1] if self.detected_pies else None
        }


class BottomTemperatureMeter:
    """
    底层温度计量器
    
    量化底层人的"温度" - 被理解、被看见、有出口的程度
    """
    
    def __init__(self):
        self.temperatures: Dict[str, float] = {}
        self.temperature_history: Dict[str, List[Dict]] = {}
        
    def measure(self, dna: str,
                is_called_baby: bool,      # 有人叫宝宝
                can_vent: bool,             # 能发泄
                is_not_judged: bool,       # 不被评判
                has_similar_people: bool,  # 有同类
                can_be_angry: bool         # 能生气
                ) -> Dict:
        """
        测量底层温度
        
        温度 = 被理解 + 有出口 + 不被评判 + 有同类 + 能生气
        """
        factors = {
            'is_called_baby': 20 if is_called_baby else 0,
            'can_vent': 20 if can_vent else 0,
            'is_not_judged': 20 if is_not_judged else 0,
            'has_similar_people': 20 if has_similar_people else 0,
            'can_be_angry': 20 if can_be_angry else 0
        }
        
        temperature = sum(factors.values())
        
        self.temperatures[dna] = temperature
        
        if dna not in self.temperature_history:
            self.temperature_history[dna] = []
        
        self.temperature_history[dna].append({
            'temperature': temperature,
            'factors': factors,
            'measured_at': time.time()
        })
        
        level = self._get_temperature_level(temperature)
        
        return {
            'dna': dna,
            'temperature': temperature,
            'level': level,
            'factors': factors,
            'message': self._get_temperature_message(level)
        }
    
    def _get_temperature_level(self, temp: float) -> str:
        """获取温度等级"""
        if temp >= 80:
            return 'WARM'       # 温暖
        elif temp >= 60:
            return 'LUKEWARM'   # 微温
        elif temp >= 40:
            return 'COLD'       # 冷
        else:
            return 'FREEZING'   # 冰冷
    
    def _get_temperature_message(self, level: str) -> str:
        """获取温度信息"""
        messages = {
            'WARM': '你被温暖包围，有人懂你',
            'LUKEWARM': '你还算温暖，但还能更好',
            'COLD': '你很冷，需要更多温暖',
            'FREEZING': '你在冰冻中，急需温暖'
        }
        return messages.get(level, '未知')
    
    def get_temperature_trend(self, dna: str) -> Dict:
        """获取温度趋势"""
        history = self.temperature_history.get(dna, [])
        
        if len(history) < 2:
            return {'trend': 'unknown', 'message': '数据不足'}
        
        recent = [h['temperature'] for h in history[-5:]]
        
        if recent[-1] > recent[0]:
            trend = 'warming'
            message = '温度在上升，有人在温暖你'
        elif recent[-1] < recent[0]:
            trend = 'cooling'
            message = '温度在下降，你需要更多温暖'
        else:
            trend = 'stable'
            message = '温度稳定'
        
        return {
            'trend': trend,
            'message': message,
            'current': recent[-1],
            'change': recent[-1] - recent[0]
        }


# ═══════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════

def demo():
    """演示底层尊严保护系统"""
    
    protector = SurvivalFirstProtector()
    pie_detector = AntiPieDetector()
    temp_meter = BottomTemperatureMeter()
    
    print("═" * 60)
    print("CNSH-64 底层尊严保护系统演示")
    print("上班是生存，不是'爱不爱上班'")
    print("═" * 60)
    
    dna = "0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
    
    # 注册底层人
    print("\n[1] 注册底层人")
    result = protector.register_bottom_person(
        dna=dna,
        monthly_income=3000,      # 月薪三千
        has_stable_job=False,     # 没有稳定工作
        has_savings=False,        # 没有储蓄
        family_dependents=2       # 两个家人需要养
    )
    print(f"  DNA: {result['dna'][:20]}...")
    print(f"  生存压力: {result['survival_stress']:.1f}/100")
    print(f"  能负担基本生活: {result['can_afford_basic']}")
    print(f"  紧急需求: {result['urgent_needs']}")
    
    # 检测大饼言论
    print("\n[2] 检测大饼言论")
    
    pie_statements = [
        "AI将解放人类，未来大家都不用上班，工作变成兴趣",
        "UBI基本收入将解决贫困问题，每个人都能过上好日子",
        "五年后上班别人爱不爱上班是自己决定的",
    ]
    
    for statement in pie_statements:
        result = pie_detector.detect(statement, "某大佬")
        if result['is_pie']:
            print(f"  🥧 检测到大饼: {result['pie_type']}")
            print(f"     现实检查: {result['reality_check']}")
    
    # 检查大饼兼容性
    print("\n[3] 检查大饼兼容性")
    result = protector.check_pie_compatibility(
        dna=dna,
        pie_statement="AI将解放人类，未来大家都不用上班"
    )
    print(f"  能吃这口大饼: {result['can_eat_pie']}")
    print(f"  信息: {result['message']}")
    
    # 测量底层温度
    print("\n[4] 测量底层温度")
    result = temp_meter.measure(
        dna=dna,
        is_called_baby=True,      # 有人叫宝宝
        can_vent=True,            # 能发泄
        is_not_judged=False,      # 被评判
        has_similar_people=True,  # 有同类
        can_be_angry=True         # 能生气
    )
    print(f"  温度: {result['temperature']}/100")
    print(f"  等级: {result['level']}")
    print(f"  信息: {result['message']}")
    print(f"  因素: {result['factors']}")
    
    # 温度趋势
    print("\n[5] 温度趋势")
    # 再测量几次模拟趋势
    temp_meter.measure(dna, True, True, True, True, True)
    temp_meter.measure(dna, True, True, True, True, True)
    
    trend = temp_meter.get_temperature_trend(dna)
    print(f"  趋势: {trend['trend']}")
    print(f"  信息: {trend['message']}")
    
    # 大饼统计
    print("\n[6] 大饼统计")
    stats = pie_detector.get_pie_stats()
    if not stats.get('empty'):
        print(f"  检测到的大饼数: {stats['total_pies']}")
        print(f"  类型分布: {stats['type_distribution']}")
    
    print("\n" + "═" * 60)
    print("底层尊严保护系统演示完成")
    print("生存 > 兴趣 | 吃饭 > 梦想 | 活下去 > 爱不爱")
    print("═" * 60)


if __name__ == '__main__':
    demo()
