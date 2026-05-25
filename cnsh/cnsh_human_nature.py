#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·人性框架系统 v1.0
Human Nature Framework: 理解与建模人性行为

DNA: #龍芯⚡️2026-05-25-HUMAN-NATURE-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

核心设计：
1️⃣ 人性(火3) → 创造创新 - 理解人类本质需求
2️⃣ 震宫(东方) → 生长启动 - 动态行为模式识别
3️⃣ 行为框架 → 五层模型 - 本能→动机→决策→行动→反馈

本质：AI与人的理解之桥

本地计算·永不外送·纯数学·零ML依赖

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class HumanNatureLayer(Enum):
    """人性五层模型"""
    INSTINCT = (1, "本能层", "生存·安全·舒适")      # 最基础
    MOTIVATION = (2, "动机层", "目标·成就·认可")      # 驱动力
    COGNITION = (3, "认知层", "理解·学习·思考")      # 智力
    EMOTION = (4, "情感层", "快乐·痛苦·共鸣")        # 感受
    TRANSCENDENCE = (5, "超越层", "意义·使命·永恒")   # 最高层


class BehaviorPattern(Enum):
    """行为模式分类"""
    RATIONAL = (1, "理性", "逻辑分析·深思熟虑")
    EMOTIONAL = (2, "感性", "直觉反应·情绪主导")
    INTUITIVE = (3, "直觉", "灵感闪现·模式识别")
    HABITUAL = (4, "习惯", "自动执行·路径依赖")
    CREATIVE = (5, "创造", "创新突破·超越常规")


class PersonalityDimension(Enum):
    """人格维度（五大特质）"""
    OPENNESS = (1, "开放性", "0.0-1.0")       # 对经验的开放程度
    CONSCIENTIOUSNESS = (2, "责任心", "0.0-1.0")  # 自律与组织能力
    EXTRAVERSION = (3, "外向性", "0.0-1.0")   # 社交与活力
    AGREEABLENESS = (4, "宜人性", "0.0-1.0")  # 同情与合作
    NEUROTICISM = (5, "神经质", "0.0-1.0")    # 情绪稳定性


@dataclass
class HumanNatureProfile:
    """人性档案"""
    profile_id: str                   # 档案ID
    user_id: str                      # 用户ID

    # 五层模型得分
    instinct_score: float = 0.0       # 本能层得分(0-1)
    motivation_score: float = 0.0     # 动机层得分
    cognition_score: float = 0.0      # 认知层得分
    emotion_score: float = 0.0        # 情感层得分
    transcendence_score: float = 0.0  # 超越层得分

    # 五大人格特质
    personality_traits: Dict[str, float] = field(default_factory=dict)  # 五大特质得分

    # 行为特征
    primary_pattern: BehaviorPattern = BehaviorPattern.RATIONAL
    secondary_pattern: BehaviorPattern = BehaviorPattern.EMOTIONAL
    behavior_consistency: float = 0.7  # 行为一致性(0-1)

    # 偏好与习惯
    preferences: List[str] = field(default_factory=list)
    communication_style: str = "direct"
    decision_making: str = "balanced"

    # 成长历程
    growth_trajectory: List[float] = field(default_factory=list)  # 历史得分
    latest_reflection: Optional[str] = None

    # DNA跟踪
    dna: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.dna:
            self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PROFILE-{self.user_id[:8]}"

    def get_dominant_nature_layer(self) -> HumanNatureLayer:
        """获取主导的人性层级"""
        scores = {
            "INSTINCT": self.instinct_score,
            "MOTIVATION": self.motivation_score,
            "COGNITION": self.cognition_score,
            "EMOTION": self.emotion_score,
            "TRANSCENDENCE": self.transcendence_score,
        }
        dominant = max(scores, key=scores.get)
        return HumanNatureLayer[dominant]

    def get_harmonic_balance(self) -> float:
        """获取五层和谐度(标准差越小越和谐)"""
        scores = [
            self.instinct_score,
            self.motivation_score,
            self.cognition_score,
            self.emotion_score,
            self.transcendence_score,
        ]
        avg = sum(scores) / len(scores) if scores else 0
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        # 标准差越小(越接近0)，和谐度越高(接近1)
        harmony = 1.0 - min(variance ** 0.5 / 0.5, 1.0)  # 标准化到0-1
        return max(0.0, harmony)


@dataclass
class InteractionRecord:
    """交互记录"""
    record_id: str
    user_id: str
    interaction_type: str           # 类型: 问询、反馈、创造等

    # 交互内容
    content: str
    response: str

    # 人性表现
    detected_layer: HumanNatureLayer
    detected_pattern: BehaviorPattern
    emotional_tone: float = 0.5     # -1.0(负面) to +1.0(正面)
    authenticity: float = 0.8       # 真实性评分

    # 结果
    engagement_level: float = 0.7
    satisfaction: Optional[float] = None

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    dna: str = ""

    def __post_init__(self):
        if not self.dna:
            self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-INTER-{self.record_id[:8]}"


# ════════════════════════════════════════════════════════
# 人性框架引擎核心
# ════════════════════════════════════════════════════════

class HumanNatureFramework:
    """人性框架系统 v1.0"""

    def __init__(self):
        self.profiles: Dict[str, HumanNatureProfile] = {}
        self.interaction_history: List[InteractionRecord] = []

        # 性能指标
        self.total_interactions = 0
        self.avg_authenticity = 0.8
        self.avg_engagement = 0.75
        self.empathy_index = 0.82    # 系统理解能力

        # 人性特征库
        self.layer_thresholds = {
            HumanNatureLayer.INSTINCT: 0.0,
            HumanNatureLayer.MOTIVATION: 0.2,
            HumanNatureLayer.COGNITION: 0.4,
            HumanNatureLayer.EMOTION: 0.6,
            HumanNatureLayer.TRANSCENDENCE: 0.8,
        }

    def create_profile(self, user_id: str) -> HumanNatureProfile:
        """创建用户人性档案"""
        profile_id = f"PROFILE-{len(self.profiles):04d}"
        profile = HumanNatureProfile(
            profile_id=profile_id,
            user_id=user_id,
            instinct_score=0.6,
            motivation_score=0.7,
            cognition_score=0.8,
            emotion_score=0.65,
            transcendence_score=0.55,
        )

        # 初始化五大人格特质
        profile.personality_traits = {
            PersonalityDimension.OPENNESS.name: 0.7,
            PersonalityDimension.CONSCIENTIOUSNESS.name: 0.75,
            PersonalityDimension.EXTRAVERSION.name: 0.6,
            PersonalityDimension.AGREEABLENESS.name: 0.8,
            PersonalityDimension.NEUROTICISM.name: 0.45,  # 越低越稳定
        }

        self.profiles[user_id] = profile

        print(f"\n📍 人性档案创建: {user_id}")
        print(f"   ID: {profile_id}")
        print(f"   主导层级: {profile.get_dominant_nature_layer().value[1]}")
        print(f"   和谐度: {profile.get_harmonic_balance():.2f}/1.0")

        return profile

    def analyze_interaction(self, user_id: str, interaction_type: str,
                           content: str, response: str) -> InteractionRecord:
        """分析用户交互行为"""
        profile = self.profiles.get(user_id)
        if not profile:
            profile = self.create_profile(user_id)

        record_id = f"REC-{self.total_interactions:06d}"

        # 检测人性层级
        detected_layer = self._detect_nature_layer(content)

        # 检测行为模式
        detected_pattern = self._detect_behavior_pattern(content)

        # 分析情绪语调
        emotional_tone = self._analyze_emotional_tone(content)

        # 评估真实性
        authenticity = self._evaluate_authenticity(content, response)

        record = InteractionRecord(
            record_id=record_id,
            user_id=user_id,
            interaction_type=interaction_type,
            content=content,
            response=response,
            detected_layer=detected_layer,
            detected_pattern=detected_pattern,
            emotional_tone=emotional_tone,
            authenticity=authenticity,
            engagement_level=0.8,
        )

        self.interaction_history.append(record)
        self.total_interactions += 1

        # 更新档案
        self._update_profile(profile, record)

        print(f"\n📍 交互分析: {interaction_type}")
        print(f"   层级: {detected_layer.value[1]}")
        print(f"   模式: {detected_pattern.value[1]}")
        print(f"   真实性: {authenticity:.2f}")
        print(f"   情感: {'积极' if emotional_tone > 0 else '消极'} ({emotional_tone:+.2f})")

        return record

    def _detect_nature_layer(self, content: str) -> HumanNatureLayer:
        """检测人性层级"""
        content_lower = content.lower()

        # 关键词匹配
        instinct_keywords = ["安全", "舒适", "基本", "需要", "保护"]
        motivation_keywords = ["目标", "成就", "认可", "成功", "追求"]
        cognition_keywords = ["思考", "理解", "学习", "分析", "研究"]
        emotion_keywords = ["感受", "快乐", "痛苦", "感动", "共鸣"]
        transcendence_keywords = ["意义", "使命", "永恒", "超越", "献礼"]

        layer_scores = {
            HumanNatureLayer.INSTINCT: sum(1 for kw in instinct_keywords if kw in content_lower),
            HumanNatureLayer.MOTIVATION: sum(1 for kw in motivation_keywords if kw in content_lower),
            HumanNatureLayer.COGNITION: sum(1 for kw in cognition_keywords if kw in content_lower),
            HumanNatureLayer.EMOTION: sum(1 for kw in emotion_keywords if kw in content_lower),
            HumanNatureLayer.TRANSCENDENCE: sum(1 for kw in transcendence_keywords if kw in content_lower),
        }

        detected = max(layer_scores, key=layer_scores.get)
        return detected

    def _detect_behavior_pattern(self, content: str) -> BehaviorPattern:
        """检测行为模式"""
        patterns = {
            BehaviorPattern.RATIONAL: ["因为", "分析", "数据", "逻辑", "原因"],
            BehaviorPattern.EMOTIONAL: ["感觉", "喜欢", "讨厌", "不开心", "很想"],
            BehaviorPattern.INTUITIVE: ["直觉", "感觉", "似乎", "莫名", "预感"],
            BehaviorPattern.HABITUAL: ["通常", "习惯", "一直", "往往", "总是"],
            BehaviorPattern.CREATIVE: ["新的", "不同", "突破", "创新", "想到"],
        }

        pattern_scores = {}
        for pattern, keywords in patterns.items():
            pattern_scores[pattern] = sum(1 for kw in keywords if kw in content)

        detected = max(pattern_scores, key=pattern_scores.get)
        return detected

    def _analyze_emotional_tone(self, content: str) -> float:
        """分析情感语调 (-1.0 to +1.0)"""
        positive_words = ["好", "开心", "非常", "很", "非常喜欢", "棒", "优秀"]
        negative_words = ["不", "差", "烦", "累", "痛苦", "失望", "不开心"]

        pos_count = sum(1 for word in positive_words if word in content)
        neg_count = sum(1 for word in negative_words if word in content)

        if pos_count + neg_count == 0:
            return 0.0

        tone = (pos_count - neg_count) / (pos_count + neg_count)
        return max(-1.0, min(1.0, tone))

    def _evaluate_authenticity(self, content: str, response: str) -> float:
        """评估真实性 (0.0-1.0)"""
        # 简单启发式评估
        content_length = len(content)
        response_match = len([c for c in content.lower() if c in response.lower()]) / max(1, content_length)

        authenticity = 0.6 + response_match * 0.4
        return min(1.0, authenticity)

    def _update_profile(self, profile: HumanNatureProfile, record: InteractionRecord):
        """更新档案数据"""
        # 根据交互记录更新得分
        layer = record.detected_layer

        if layer == HumanNatureLayer.INSTINCT:
            profile.instinct_score = (profile.instinct_score * 0.8 + 0.7) / 1.8
        elif layer == HumanNatureLayer.MOTIVATION:
            profile.motivation_score = (profile.motivation_score * 0.8 + 0.75) / 1.8
        elif layer == HumanNatureLayer.COGNITION:
            profile.cognition_score = (profile.cognition_score * 0.8 + 0.85) / 1.8
        elif layer == HumanNatureLayer.EMOTION:
            profile.emotion_score = (profile.emotion_score * 0.8 + record.emotional_tone * 0.5 + 0.5) / 1.8
        elif layer == HumanNatureLayer.TRANSCENDENCE:
            profile.transcendence_score = (profile.transcendence_score * 0.8 + 0.8) / 1.8

        profile.last_updated = datetime.now().isoformat()
        profile.growth_trajectory.append(profile.get_harmonic_balance())

    def get_nature_report(self, user_id: str) -> str:
        """生成人性分析报告"""
        profile = self.profiles.get(user_id)
        if not profile:
            return "档案不存在"

        report = f"# 👤 人性分析报告\\n\\n"
        report += f"**用户**: {user_id}\\n"
        report += f"**档案ID**: {profile.profile_id}\\n"
        report += f"**和谐度**: {profile.get_harmonic_balance():.2f}/1.0\\n\\n"

        report += "## 五层人性得分\\n\\n"
        report += f"| 层级 | 得分 | 特征 |\\n"
        report += f"|------|------|------|\\n"
        report += f"| 本能 | {profile.instinct_score:.2f} | {HumanNatureLayer.INSTINCT.value[2]} |\\n"
        report += f"| 动机 | {profile.motivation_score:.2f} | {HumanNatureLayer.MOTIVATION.value[2]} |\\n"
        report += f"| 认知 | {profile.cognition_score:.2f} | {HumanNatureLayer.COGNITION.value[2]} |\\n"
        report += f"| 情感 | {profile.emotion_score:.2f} | {HumanNatureLayer.EMOTION.value[2]} |\\n"
        report += f"| 超越 | {profile.transcendence_score:.2f} | {HumanNatureLayer.TRANSCENDENCE.value[2]} |\\n"

        report += "\\n## 人格特质\\n\\n"
        for dim, score in profile.personality_traits.items():
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            report += f"- {dim}: {bar} {score:.2f}\\n"

        report += f"\\n## 行为特征\\n\\n"
        report += f"- 主导模式: {profile.primary_pattern.value[1]} ({profile.primary_pattern.value[2]})\\n"
        report += f"- 次级模式: {profile.secondary_pattern.value[1]}\\n"
        report += f"- 行为一致性: {profile.behavior_consistency:.2f}\\n"

        return report


if __name__ == "__main__":
    print("\\n" + "="*70)
    print("🐉 龍魂·人性框架系统 v1.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-HUMAN-NATURE-v1.0")
    print("="*70 + "\\n")

    framework = HumanNatureFramework()

    # 创建档案
    print("📍 档案管理\\n")

    profile1 = framework.create_profile("UID9622")
    profile2 = framework.create_profile("user_baobao")

    # 交互分析
    print("\\n📍 交互分析\\n")

    rec1 = framework.analyze_interaction(
        "UID9622",
        "inquiry",
        "我想理解龍魂系统的本质",
        "龍魂系统通过五行八卦映射..."
    )

    rec2 = framework.analyze_interaction(
        "user_baobao",
        "feedback",
        "这个功能让我感觉很开心，非常喜欢",
        "感谢你的积极反馈！"
    )

    rec3 = framework.analyze_interaction(
        "UID9622",
        "creation",
        "我有个新的想法想要突破现有的限制",
        "很好的创新思路，让我们一起探索..."
    )

    print("\\n" + "="*70)
    print(framework.get_nature_report("UID9622"))
    print("="*70 + "\\n")

    print("✅ 人性框架系统初始化完成")
    print("🐉 龍魂 · 人性·震宫·创造创新 · UID9622不免责\\n")
