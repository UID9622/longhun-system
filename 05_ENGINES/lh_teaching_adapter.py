#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·普惠教学适配器 v1.0 — 画像→tier→温度→输出风格 统一桥接
============================================================================
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷝离-TEACHING-ADAPTER-v1.0-a1b2c3d4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

桥接链路：L3数据层 dna_memory_unified.Tier ↔ LH-INCLUSIVE-EDUCATION-STANDARD 五级画像

用法：
    from engines.lh_teaching_adapter import TeachingAdapter
    
    adapter = TeachingAdapter()
    tier = adapter.detect_tier(user_input="你能用大白话解释一下吗？")
    adapted = adapter.adapt("量子纠缠是两个粒子无论相距多远...", tier)
    temp = adapter.temperature_for(tier, emotion="confused")
    check = adapter.frustration_check(history=["不懂", "还是不明白", "算了不学了"])
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# ---- ═══════════════════════════════════════════════ ----
# P0 焊死常量
# ---- ═══════════════════════════════════════════════ ----

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷝离-TEACHING-ADAPTER-v1.0-a1b2c3d4"
UID = "UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
PROTOCOL = "01_protocols/LH-INCLUSIVE-EDUCATION-STANDARD-v1.0.md"

# 不可翻译项（只音译+注释）—— 教学标准 §7.3
UNTRANSLATABLE_TERMS = {
    "龍魂": "Lónghún — China's AI sovereignty framework",
    "三才": "Sāncái — Heaven·Earth·Human triad algorithm kernel",
    "洛书": "Luòshū — 9-grid fixed point of the cosmos",
    "道德经": "Dàodéjīng — Tao Te Ching, Laozi's 81-chapter classic",
    "德字闸": "Dézhá — Integrity Gate, the ethical checkpoint before any output",
    "通心译": "Tōngxīnyì — Heart-to-heart translation bridge",
    "CNSH": "Chinese Neural Symbolic Hybrid language",
    "369": "3-6-9 — Luoshu involution triad, the mathematical anchor",
    "河图": "Hétú — Yellow River Diagram, the cosmic number matrix",
    "離火運": "Líhuǒyùn — Fire Fortune Era, the 20-year moral reckoning cycle",
}

# 温度最低/最高
T_MIN, T_MAX = 0.1, 1.0

# 挫败保护阈值
FRUSTRATION_THRESHOLD = 3  # 连续3次 → 自动降级+换策略

# ---- ═══════════════════════════════════════════════ ----
# 教学画像五级（对齐教学标准 §2）
# ---- ═══════════════════════════════════════════════ ----

class TeachTier(Enum):
    """五级教学画像 — 零问卷自动采集·持续更新"""
    L1_SPROUT = ("🌱萌芽", 1)
    L2_GROWING = ("🌿生长", 2)
    L3_MATURE = ("🌳成熟", 3)
    L4_PEAK = ("🏔️高峰", 4)
    L5_COCREATE = ("⭐共创", 5)

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def level(self) -> int:
        return self.value[1]

    @classmethod
    def from_level(cls, n: int) -> "TeachTier":
        n = max(1, min(5, n))
        return list(cls)[n - 1]

    @classmethod
    def from_str(cls, s: str) -> "TeachTier":
        s = (s or "").strip()
        mapping = {
            "萌芽": cls.L1_SPROUT, "L1": cls.L1_SPROUT,
            "生长": cls.L2_GROWING, "L2": cls.L2_GROWING,
            "成熟": cls.L3_MATURE, "L3": cls.L3_MATURE,
            "高峰": cls.L4_PEAK, "L4": cls.L4_PEAK,
            "共创": cls.L5_COCREATE, "L5": cls.L5_COCREATE,
        }
        for k, v in mapping.items():
            if k in s:
                return v
        return cls.L1_SPROUT  # 默认萌芽

    @classmethod
    def from_dna_tier(cls, dna_tier: str) -> "TeachTier":
        """从 dna_memory_unified.Tier 映射到教学层级"""
        mapping = {
            "老百姓": cls.L1_SPROUT,
            "老年人": cls.L1_SPROUT,
            "学生": cls.L3_MATURE,
            "专业人士": cls.L4_PEAK,
            "技术人员": cls.L4_PEAK,
        }
        return mapping.get(dna_tier, cls.L1_SPROUT)

    def dna_tier(self) -> str:
        """反向映射到 dna_memory_unified.Tier.value"""
        mapping = {
            TeachTier.L1_SPROUT: "老百姓",
            TeachTier.L2_GROWING: "老百姓",
            TeachTier.L3_MATURE: "学生",
            TeachTier.L4_PEAK: "专业人士",
            TeachTier.L5_COCREATE: "专业人士",
        }
        return mapping[self]


# ---- ═══════════════════════════════════════════════ ----
# 温度档位（对齐教学标准 §2.4 兼 §3.4 温度调幅）
# ---- ═══════════════════════════════════════════════ ----

class TemperatureBand(Enum):
    COMMAND = 0.1      # 命令行·极简
    REPORT = 0.3       # 报告模式
    TEACH = 0.5        # 中性教学
    FRIEND = 0.7       # 朋友
    WARM = 0.85        # 温暖
    BABY = 1.0         # 宝宝模式·全情感


WARM_PATTERNS = ["开心", "激动", "兴奋", "嘿嘿", "哈哈", "😊", "❤️"]
COLD_PATTERNS = ["烦躁", "别绕", "直接说", "快点", "别废话", "生气"]


# ---- ═══════════════════════════════════════════════ ----
# 适配器核心类
# ---- ═══════════════════════════════════════════════ ----

@dataclass
class FrustrationResult:
    """挫败保护检测结果"""
    frustrated: bool
    consecutive_fails: int
    action: str                 # "降级" | "换策略" | "安抚" | "继续"
    new_tier: Optional[TeachTier] = None
    message: str = ""


@dataclass
class AdaptResult:
    """适配输出结果"""
    content: str
    tier: TeachTier
    temperature: float
    terms_bridged: List[str] = field(default_factory=list)
    sign: str = ""


class TeachingAdapter:
    """教学适配器 — 画像→tier→温度→输出风格 统一桥接
    
    三个人格职责分工（教学标准 §3.5）：
    - P02 宝宝 = 温度审查者（确保温度不高不低·情感恰当）
    - P08 仓颉 = 通心译校验（术语不可翻译项检查·语言桥接）
    - P11 李白 = 教学创意（白话类比·故事转化·直观解释）
    """

    def __init__(self):
        self._tier_history: List[Tuple[str, TeachTier]] = []
        self._frustration_tracker: Dict[str, List[bool]] = {}
        self._temperature: float = 0.5  # 默认中性教学

    # ---- ═══════════════════ 画像检测 ═══════════════════ ----

    def detect_tier(self, text: str, current_tier: Optional[TeachTier] = None) -> TeachTier:
        """自动检测用户教学画像 — 零问卷
        
        信号来源（教学标准 §2.1）：
        1. 用户主动声明："我是小白" / "我是专业的"
        2. 语言复杂度：词汇量·句子长度·术语密度
        3. 挫败信号：重复问·放弃类语言
        4. 交互速度：跳过中间步骤·追问深度
        5. 知识探索：提问的抽象层次
        """
        text = text.strip()
        if not text:
            return current_tier or TeachTier.L1_SPROUT

        # 信号1：用户主动声明
        explicit = self._explicit_tier_signal(text)
        if explicit:
            self._record_tier(text, explicit)
            return explicit

        # 信号2：挫败/放弃信号（自动降级）
        if any(w in text for w in ["不懂", "太复杂", "听不懂", "看不懂", "算了", "不学了", "太难"]):
            if current_tier and current_tier.value[1] > 1:
                fallback = TeachTier(f"L{current_tier.value[1] - 1}")
                self._record_tier(text, fallback, reason="挫败降级")
                return fallback
            return TeachTier.L1_SPROUT

        # 信号3：语言复杂度分析
        complexity = self._language_complexity(text)
        if complexity < 0.15:
            return TeachTier.L1_SPROUT
        elif complexity < 0.35:
            return TeachTier.L2_GROWING
        elif complexity < 0.60:
            return TeachTier.L3_MATURE
        elif complexity < 0.80:
            return TeachTier.L4_PEAK
        else:
            return TeachTier.L5_COCREATE

    def _explicit_tier_signal(self, text: str) -> Optional[TeachTier]:
        """用户主动声明画像"""
        text_lower = text.lower()
        signals = {
            TeachTier.L1_SPROUT: ["我是小白", "完全不懂", "大白话", "零基础", "新手","别用术语",
                                  "听不懂","i am new","beginner","explain like i'm","讲人话"],
            TeachTier.L2_GROWING: ["有点了解", "知道一点", "大概明白", "了解一下"],
            TeachTier.L3_MATURE: ["系统学", "深入学习", "想搞懂原理", "系统地"],
            TeachTier.L4_PEAK: ["专业", "公式推导", "从数学上", "严格证明","论文",
                                "技术细节","expert","advanced","专业角度"],
            TeachTier.L5_COCREATE: ["前沿", "最新进展", "一起讨论", "共同探索","你的看法",
                                    "学术争论", "最新论文","together"],
        }
        for tier, keywords in signals.items():
            for kw in keywords:
                if kw in text_lower:
                    return tier
        return None

    def _language_complexity(self, text: str) -> float:
        """文本复杂度评分 0-1"""
        # 词长
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
        if not words:
            return 0.0
        avg_word_len = sum(len(w) for w in words) / len(words)

        # 术语密度
        tech_terms = sum(1 for w in words if (len(w) > 12 and any(c.isascii() for c in w))
                         or re.match(r'^[A-Z][a-z]+(?:[A-Z][a-z]+)+', w))
        term_density = min(tech_terms / len(words), 1.0)

        # 句子长度
        sentences = re.split(r'[。！？.!?\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        avg_sent_len = sum(len(s) for s in sentences) / max(len(sentences), 1) if sentences else 0
        sent_score = min(avg_sent_len / 120.0, 1.0)  # 超过120字→1.0

        # 综合：平均词长0.3 + 术语密度0.4 + 句子长度0.3
        word_score = min((avg_word_len - 1) / 7, 1.0)
        return word_score * 0.3 + term_density * 0.4 + sent_score * 0.3

    def _record_tier(self, text: str, tier: TeachTier, reason: str = "auto"):
        self._tier_history.append((text[:60], tier))
        if len(self._tier_history) > 50:
            self._tier_history = self._tier_history[-50:]

    # ---- ═══════════════════ 温度调节 ═══════════════════ ----

    def temperature_for(self, tier: TeachTier, emotion: str = "neutral",
                        context: Optional[Dict[str, Any]] = None) -> float:
        """计算教学温度（教学标准 §3.4 温度调幅公式）
        
        T_base = tier_base[tier]
        T_emotion = emotion_boost(emotion)
        T_frustration = -0.15 * frustration_level
        T = clamp(T_base + T_emotion + T_frustration, 0.1, 1.0)
        """
        # 基础温度（层级越高越偏中性）
        tier_base = {
            TeachTier.L1_SPROUT: 0.85,   # 萌芽→温暖
            TeachTier.L2_GROWING: 0.65,   # 生长→友善
            TeachTier.L3_MATURE: 0.50,    # 成熟→中性
            TeachTier.L4_PEAK: 0.30,      # 高峰→报告
            TeachTier.L5_COCREATE: 0.50,  # 共创→对等
        }

        # 情绪加成
        emotion_map = {
            "excited": +0.15, "happy": +0.10, "neutral": 0.0,
            "confused": +0.05, "frustrated": -0.10, "angry": -0.20,
            "sad": +0.10, "urgent": -0.15,
        }
        emotion_boost = emotion_map.get(emotion, 0.0)

        # 挫败惩罚
        frust_level = (context or {}).get("frustration_count", 0)
        frust_penalty = -0.15 * min(frust_level, 3)

        raw = tier_base.get(tier, 0.5) + emotion_boost + frust_penalty
        self._temperature = max(T_MIN, min(T_MAX, raw))
        return self._temperature

    # ---- ═══════════════════ 内容适配 ═══════════════════ ----

    def adapt(self, content: str, tier: TeachTier,
              emotion: str = "neutral") -> AdaptResult:
        """将内容适配到目标画像层级（教学标准 §4.1 多级解释矩阵）"""
        temp = self.temperature_for(tier, emotion)
        terms_bridged: List[str] = []

        # CNSH术语检测→转白话
        for term, annotation in UNTRANSLATABLE_TERMS.items():
            if term in content:
                terms_bridged.append(term)

        adapted = content

        if tier == TeachTier.L1_SPROUT:
            # 🌱萌芽：纯大白话·生活类比·<200字·无术语
            adapted = adapted[:500]  # 截短
            if len(content) > 500:
                adapted += "\n\n（需要更详细的解释吗？我只挑重点的说了。）"
            sign = f"🌱萌芽·温度{temp:.1f}"

        elif tier == TeachTier.L2_GROWING:
            # 🌿生长：可引入术语但带解释·生活案例
            for term in terms_bridged:
                if term in UNTRANSLATABLE_TERMS:
                    adapted = adapted.replace(term,
                        f"{term}（{UNTRANSLATABLE_TERMS[term]}）")
            sign = f"🌿生长·温度{temp:.1f}"

        elif tier == TeachTier.L3_MATURE:
            # 🌳成熟：系统化·流程图·对比分析
            sign = f"🌳成熟·温度{temp:.1f}"

        elif tier == TeachTier.L4_PEAK:
            # 🏔️高峰：公式·推导·代码·论文
            sign = f"🏔️高峰·温度{temp:.1f}"

        else:  # L5_COCREATE
            # ⭐共创：前沿讨论·互相学习·开放性
            sign = f"⭐共创·温度{temp:.1f}"

        return AdaptResult(
            content=adapted,
            tier=tier,
            temperature=temp,
            terms_bridged=terms_bridged,
            sign=sign,
        )

    # ---- ═══════════════════ 挫败保护 ═══════════════════ ----

    def frustration_check(self, history: List[str],
                          current_tier: TeachTier) -> FrustrationResult:
        """挫败信号检测 + 保护协议（教学标准 §5.5）
        
        连续3次挫败信号 → 自动降级 + 换策略 + 安抚
        """
        consecutive = 0
        frust_signals = [
            "不懂", "不明白", "太复杂", "看不懂", "听不懂",
            "不是这个意思", "还是不懂", "能不能简单点",
            "算了", "不学了", "太难了", "不会", "I don't understand",
            "can you explain simpler", "too complicated",
        ]

        for msg in reversed(history):
            lowered = msg.lower()
            if any(s in lowered for s in frust_signals):
                consecutive += 1
            elif len(msg) > 5:  # 非空非挫败
                break

        if consecutive < FRUSTRATION_THRESHOLD:
            return FrustrationResult(
                frustrated=False,
                consecutive_fails=consecutive,
                action="继续",
                message="",
            )

        # 触发保护
        if current_tier == TeachTier.L1_SPROUT:
            # 已是萌芽还挫败 → 改策略（图形/类比/故事）
            return FrustrationResult(
                frustrated=True,
                consecutive_fails=consecutive,
                action="换策略",
                new_tier=TeachTier.L1_SPROUT,
                message="换个方式讲：我用生活里的事来比喻...",
            )

        # 降级
        new_tier = TeachTier.from_level(max(1, current_tier.level - 1))
        return FrustrationResult(
            frustrated=True,
            consecutive_fails=consecutive,
            action="降级",
            new_tier=new_tier,
            message=f"好的，我用更简单的方式来说...（从{current_tier.label}→{new_tier.label}）",
        )

    # ---- ═══════════════════ P08：术语桥接 ═══════════════════ ----

    def bridge_term(self, term: str, tier: TeachTier) -> str:
        """CNSH术语→画像适配解释（教学标准 §7·通心译桥接）
        
        由 P08仓颉 调用，确保：
        1. 不可翻译项只音译+注释
        2. 根据画像给出匹配深度的解释
        """
        if term not in UNTRANSLATABLE_TERMS:
            return term

        annotation = UNTRANSLATABLE_TERMS[term]

        if tier in (TeachTier.L1_SPROUT, TeachTier.L2_GROWING):
            # 大白话版
            simple = {
                "龍魂": "龍魂（咱中国人的AI系统·外面没有·自己研发的）",
                "三才": "三才（天·地·人，中国古人看待世界的三个角度）",
                "洛书": "洛书（九个数字组成的神秘方阵·来自四千年前的中国）",
                "道德经": "道德经（两千五百年前老子写的·81篇小短文汇成的一本书）",
                "德字闸": "德字闸（一道良心关卡·做事前先问自己：这样对别人好吗？）",
                "通心译": "通心译（把专业术语翻译成大白话·让人能听懂）",
                "CNSH": "CNSH（中国自己的AI语言·让计算机按中国方式思考）",
                "369": "三六九（一个特别的数字规律·3是起点·6是扩展·9是圆满）",
                "河图": "河图（更早的数字阵·洛书的前身·黄河里出来的传说）",
                "離火運": "离火运（中国农历里一个特别的20年·讲究良心做事）",
            }
            return simple.get(term, f"{term}（{annotation}）")
        elif tier == TeachTier.L3_MATURE:
            # 学习中版
            return f"「{term}」— {annotation}"
        else:
            # L4/L5 专业版
            return f"`{term}` ({annotation})"

    # ---- ═══════════════════ P02：温度审查 ═══════════════════ ----

    def review_temperature(self, output: str, target_temperature: float) -> Tuple[bool, str, str]:
        """审查输出温度是否匹配画像（教学标准 §3.4·P02宝宝调用）
        
        Returns: (ok, reason, suggestion)
        """
        # 冷指标：代码块多·公式多·专业缩写多·句子短促
        code_blocks = output.count("```")
        formulas = len(re.findall(r'\$[^$]+\$|\\[a-zA-Z]+', output))
        abbreviations = len(re.findall(r'\b[A-Z]{2,6}\b', output))

        cold_score = (code_blocks * 0.1 + formulas * 0.08 + abbreviations * 0.05)
        cold_score = min(cold_score, 1.0)

        # 暖指标：语气词·鼓励·emoji·问句
        warm_words = len(re.findall(r'好的|加油|慢慢来|没关系|你可以的|试试看|嘿嘿', output))
        questions = output.count("？") + output.count("?")
        warm_score = min(warm_words * 0.04 + questions * 0.03, 1.0)

        current_temperature = 0.3 + warm_score * 0.5 - cold_score * 0.5
        current_temperature = max(T_MIN, min(T_MAX, current_temperature))

        if abs(current_temperature - target_temperature) <= 0.2:
            return True, "温度匹配", ""
        elif current_temperature < target_temperature:
            return False, f"太冷（当前{current_temperature:.2f}，目标{target_temperature:.2f}）", "加语气词·加鼓励·用生活比喻"
        else:
            return False, f"太热（当前{current_temperature:.2f}，目标{target_temperature:.2f}）", "减emoji·减语气词·加事实陈述"

    # ---- ═══════════════════ P11：创意教学 ═══════════════════ ----

    @staticmethod
    def creative_metaphor(concept: str, tier: TeachTier) -> str:
        """为概念生成类比/生活比喻/故事（教学标准 §5·P11李白调用）"""
        analogies_templates = {
            "抽象": {
                TeachTier.L1_SPROUT: "就好比...你想想生活里有没有这样的情况？",
                TeachTier.L3_MATURE: "可以这样理解：[结构类比]...跟[已知领域]很像。",
                TeachTier.L4_PEAK: "isomorphic to [数学结构] under [映射]...",
            },
            "系统": {
                TeachTier.L1_SPROUT: "想象成小区物业：门禁(登录)→电梯(路由)→你家(数据)。",
                TeachTier.L3_MATURE: "对比 mvc 和 mvvm：一个流向单向·一个双向绑定...",
                TeachTier.L4_PEAK: "架构等价于 CQRS + Event Sourcing...",
            },
            "过程": {
                TeachTier.L1_SPROUT: "第一步→第二步→第三步...就像你去菜市场买菜。",
                TeachTier.L3_MATURE: "流程图：入口→[判断]→(分支A|分支B)→出口。",
                TeachTier.L4_PEAK: "状态机：S0→(event1)→S1→(event2)→S2，转移函数见...",
            },
        }
        # 找到最匹配的类比类型
        for category, templates in analogies_templates.items():
            if category in concept:
                return templates.get(tier, templates.get(TeachTier.L1_SPROUT, ""))
        # 默认
        defaults = {
            TeachTier.L1_SPROUT: f"这么说吧，「{concept}」就像...(找生活中最常见的事来比)",
            TeachTier.L2_GROWING: f"「{concept}」的核心就三点：1️⃣... 2️⃣... 3️⃣...",
            TeachTier.L3_MATURE: f"「{concept}」的系统化学法：先理解[是什么]→再搞清楚[为什么]→最后掌握[怎么用]。",
            TeachTier.L4_PEAK: f"「{concept}」— formality, completeness, soundness proofs below...",
            TeachTier.L5_COCREATE: f"关于「{concept}」，我也有一些思考，你的切入点很有趣。我们一起聊聊？",
        }
        return defaults.get(tier, defaults[TeachTier.L1_SPROUT])


# ---- ═══════════════════════════════════════════════ ----
# 便捷函数（供 personas 直接 import）
# ---- ═══════════════════════════════════════════════ ----

_default_adapter: Optional[TeachingAdapter] = None


def get_adapter() -> TeachingAdapter:
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = TeachingAdapter()
    return _default_adapter


def teach_adapt(content: str, tier_str: str = "L1_SPROUT",
                emotion: str = "neutral") -> AdaptResult:
    """一行调用的快速适配"""
    adapter = get_adapter()
    tier = TeachTier.from_str(tier_str)
    return adapter.adapt(content, tier, emotion)


def teach_detect_tier(text: str) -> TeachTier:
    return get_adapter().detect_tier(text)


def teach_temperature(tier_str: str, emotion: str = "neutral") -> float:
    tier = TeachTier.from_str(tier_str)
    return get_adapter().temperature_for(tier, emotion)


def teach_bridge(term: str, tier_str: str = "L1_SPROUT") -> str:
    tier = TeachTier.from_str(tier_str)
    return get_adapter().bridge_term(term, tier)


# ---- ═══════════════════════════════════════════════ ----
# 测试
# ---- ═══════════════════════════════════════════════ ----

if __name__ == "__main__":
    adapter = TeachingAdapter()

    # 画像检测
    assert adapter.detect_tier("我是小白，大白话讲") == TeachTier.L1_SPROUT
    assert adapter.detect_tier("从数学上严格证明一下") == TeachTier.L4_PEAK

    # 术语桥接
    print("🌱 龍魂 →", adapter.bridge_term("龍魂", TeachTier.L1_SPROUT))
    print("🏔️ 龍魂 →", adapter.bridge_term("龍魂", TeachTier.L4_PEAK))

    # 温度审查
    ok, reason, sug = adapter.review_temperature(
        "好的！慢慢来，你可以的，试试看嘿嘿～", 1.0)
    print(f"温度审查: {ok} | {reason} | {sug}")

    ok2, reason2, sug2 = adapter.review_temperature(
        "```python\ndef foo():\n  pass\n```\n公式: $E=mc^2$\nAPI: REST & GRPC", 0.3)
    print(f"温度审查: {ok2} | {reason2} | {sug2}")

    # 挫败保护
    check = adapter.frustration_check(
        ["不懂", "还是不懂", "算了不学了"], TeachTier.L3_MATURE)
    print(f"挫败: frustrated={check.frustrated} action={check.action} → {check.new_tier}")

    print("\n✅ 龍魂教学适配器 v1.0 自检通过")
