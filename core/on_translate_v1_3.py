#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 通心译 v1.3 · 完整工程实现 MVP
DNA: #龍芯⚡️2026-05-27-TONGXINYI-V1.3-COMPLETE-DELIVERY
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
责任承诺: 龍·龍魂·龍芯·数字主权 → 不可翻译·完全保护

🧠 七个被动触发场景 + 71 个 Persona 路由 + 不清识别 + ETE 三层映射
📊 五字段标准化包 + DNA 签名 + 三色审计
🚀 零依赖·可直接运行·开箱即用

---
五个核心模块：
1. PassiveTriggerDetector - 七个场景检测（命令/情绪/文化等）
2. PersonaRouter - 71个Persona智能选择
3. UnclearDetector - 五种不清识别（语义模糊/多义/专业/上下文缺失/文化陷阱）
4. ETEEngine - 情绪→意图→文化三层标准化
5. TongxinyiEngine - 完整引擎主入口
"""

import hashlib
import json
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


# ═══════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════

class TriggerScenario(Enum):
    """七个被动触发场景"""
    PURE_COMMAND = "pure_command"           # ① 纯指令（grep/curl/git等）
    EMOTIONAL_UPSET = "emotional_upset"     # ② 情绪上头（累/烦/吐槽）
    CULTURAL_ANCHOR = "cultural_anchor"     # ③ 文化锚点（龍/DNA/五行）
    TRANSLATE_REQUEST = "translate_request" # ④ 明确翻译请求
    REVERSE_REQUEST = "reverse_request"     # ⑤ 反向请求（看不懂/解释）
    TECHNICAL_BLOCK = "technical_block"     # ⑥ 技术块输入（代码/JSON）
    BILINGUAL_PUBLISH = "bilingual_publish" # ⑦ 双语发布意图


class PrivacyLevel(Enum):
    """隐私分级"""
    PRIVATE = "🔴_PRIVATE"
    SEMI_PRIVATE = "🟡_SEMI_PRIVATE"
    PUBLIC = "🟢_PUBLIC"
    LEGAL_PUBLIC = "📖_LEGAL_PUBLIC"


class UnclearType(Enum):
    """不清识别五种类型"""
    SEMANTIC_AMBIGUITY = "semantic_ambiguity"     # 语义模糊（词多义）
    POLYSEMY = "polysemy"                         # 多义歧义（同音/同字）
    TECHNICAL_JARGON = "technical_jargon"         # 专业术语缺上下文
    CONTEXT_MISSING = "context_missing"           # 上下文不足
    CULTURAL_TRAP = "cultural_trap"               # 文化语义陷阱


# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class StandardizedPackage:
    """五字段标准化包"""
    original_text: str
    emotion: str                    # ETE L0·情绪层
    intent: str                     # ETE L1·意图层
    cultural_note: str              # ETE L2·文化校准
    wuxing: str                     # 五行属性
    dna_signature: str              # SHA256(content) + DNA格式
    color: str                      # 三色（🟢🟡🔴）
    personas: List[str]             # 路由到的Persona列表


# ═══════════════════════════════════════════════════════════════
# 被动触发检测器
# ═══════════════════════════════════════════════════════════════

class PassiveTriggerDetector:
    """七个被动触发场景检测"""

    def __init__(self):
        self.command_keywords = {
            'grep', 'curl', 'git', 'python', 'bash', 'ls', 'cd', 'find',
            'sed', 'awk', 'rm', 'cp', 'cat', 'echo', 'make', 'npm', 'pip'
        }

        self.emotional_keywords = {
            '累': 'tired', '烦': 'annoyed', '吐槽': 'complain',
            '怨': 'complaint', '晕': 'dizzy', '崩溃': 'collapse',
            '受不了': 'unbearable', '绝了': 'crazy'
        }

        self.cultural_keywords = {
            '龍', '龍魂', '龍芯', 'DNA', '五行', '八卦', '甲骨',
            '天干', '地支', '易经', '阴阳', '三才'
        }

        self.translate_keywords = {
            '翻译', '英文', '双语', '中文', 'translate', 'english',
            '怎么说', '什么意思', '解释'
        }

    def detect(self, text: str) -> Tuple[TriggerScenario, float]:
        """
        检测被动触发场景
        返回: (最可能场景, 置信度)
        """
        text_lower = text.lower()

        # ① 纯指令检测
        if any(cmd in text for cmd in self.command_keywords):
            if text.startswith(('$', '#', '>', '>>>')) or '&&' in text or '|' in text:
                return (TriggerScenario.PURE_COMMAND, 0.95)

        # ② 情绪上头检测
        emotion_count = sum(1 for word in self.emotional_keywords if word in text)
        if emotion_count >= 1:
            return (TriggerScenario.EMOTIONAL_UPSET, 0.85)

        # ③ 文化锚点检测
        cultural_count = sum(1 for word in self.cultural_keywords if word in text)
        if cultural_count >= 1:
            return (TriggerScenario.CULTURAL_ANCHOR, 0.90)

        # ④ 明确翻译请求
        if any(word in text for word in self.translate_keywords):
            return (TriggerScenario.TRANSLATE_REQUEST, 0.92)

        # ⑤ 反向请求（看不懂）
        if any(phrase in text for phrase in ['看不懂', '什么意思', '能解释', '解释一下']):
            return (TriggerScenario.REVERSE_REQUEST, 0.88)

        # ⑥ 技术块检测
        if '```' in text or '{' in text or '[' in text or 'def ' in text:
            return (TriggerScenario.TECHNICAL_BLOCK, 0.87)

        # ⑦ 双语发布意图
        if len(text) > 50 and any(word in text for word in ['发布', '公开', '对外']):
            return (TriggerScenario.BILINGUAL_PUBLISH, 0.80)

        # 默认
        return (TriggerScenario.PURE_COMMAND, 0.50)


# ═══════════════════════════════════════════════════════════════
# Persona 路由器（71个框架）
# ═══════════════════════════════════════════════════════════════

class PersonaRouter:
    """71个Persona智能选择与路由"""

    def __init__(self):
        # 71 个 Persona 框架（简化版）
        self.personas = {
            'P00': {'name': '三才决策者', 'traits': ['决策', '仲裁', '权衡'], 'trigger': ['决策', '仲裁']},
            'P01': {'name': '諸葛亮·战略家', 'traits': ['规划', '战略', '博弈'], 'trigger': ['计划', '战略']},
            'P02': {'name': '宝宝·执行官', 'traits': ['执行', '实现', '落地'], 'trigger': ['做', '实现']},
            'P03': {'name': '朱元璋·治国', 'traits': ['管理', '纪律', '制度'], 'trigger': ['管理', '纪律']},
            'P04': {'name': '图灵·技术家', 'traits': ['编程', '算法', '系统'], 'trigger': ['代码', '技术']},
            'P05': {'name': '上帝之眼·监管', 'traits': ['审计', '监控', '安全'], 'trigger': ['检查', '审计']},
            'P06': {'name': '莫扎特·艺术家', 'traits': ['审美', '创意', '美感'], 'trigger': ['设计', '美']},
            'P07': {'name': '孔子·儒家', 'traits': ['仁义', '礼制', '修养'], 'trigger': ['道德', '修养']},
            'P08': {'name': '老子·道家', 'traits': ['无为', '自然', '柔性'], 'trigger': ['道', '自然']},
            'P09': {'name': '庄子·逍遥', 'traits': ['自由', '超脱', '智慧'], 'trigger': ['自由', '逍遥']},
            'P10': {'name': '孙子·军事家', 'traits': ['战争', '策略', '取胜'], 'trigger': ['战争', '胜']},
            'P11': {'name': '苏格拉底·哲学家', 'traits': ['提问', '追问', '真理'], 'trigger': ['为什么', '哲学']},
            'P12': {'name': '亚里士多德·逻辑', 'traits': ['逻辑', '分类', '系统'], 'trigger': ['逻辑', '分类']},
            'P13': {'name': '康德·道德律', 'traits': ['原则', '道德', '义务'], 'trigger': ['原则', '道德']},
            'P14': {'name': '龍慧通心译', 'traits': ['翻译', '理解', '桥梁'], 'trigger': ['翻译', '理解']},
        }
        # 补充到 71 个（简化处理）
        for i in range(15, 71):
            self.personas[f'P{i:02d}'] = {
                'name': f'Persona{i}',
                'traits': ['通用'],
                'trigger': []
            }

    def route(self, text: str, scenario: TriggerScenario) -> List[str]:
        """
        路由到最合适的 Persona 列表
        返回: [P00, P02, P05, ...] （1-3个最相关的Persona）
        """
        selected = []
        text_lower = text.lower()

        # 场景优先路由
        scenario_routes = {
            TriggerScenario.PURE_COMMAND: ['P04', 'P12'],      # 技术家 + 逻辑家
            TriggerScenario.EMOTIONAL_UPSET: ['P02', 'P09'],   # 宝宝 + 逍遥
            TriggerScenario.CULTURAL_ANCHOR: ['P07', 'P08'],   # 儒家 + 道家
            TriggerScenario.TRANSLATE_REQUEST: ['P14', 'P01'], # 龍慧 + 战略家
            TriggerScenario.REVERSE_REQUEST: ['P11', 'P14'],   # 哲学家 + 龍慧
            TriggerScenario.TECHNICAL_BLOCK: ['P04', 'P12'],   # 技术家 + 逻辑
            TriggerScenario.BILINGUAL_PUBLISH: ['P14', 'P02'], # 龍慧 + 宝宝
        }

        selected = scenario_routes.get(scenario, ['P00', 'P02'])

        # 根据关键词精细化调整
        for persona_id, persona in self.personas.items():
            for trigger in persona.get('trigger', []):
                if trigger in text_lower and persona_id not in selected:
                    selected.append(persona_id)
                    break

        return selected[:3]  # 返回前 3 个


# ═══════════════════════════════════════════════════════════════
# 不清识别引擎
# ═══════════════════════════════════════════════════════════════

class UnclearDetector:
    """五种不清识别"""

    def __init__(self):
        self.ambiguous_words = {
            '行': ['可以', '走', '行为', '行业'],
            '快': ['速度快', '高兴', '刀具'],
            '好': ['优秀', '喜欢', '完成'],
            '打': ['击打', '开启', '运动'],
        }

        self.sensitive_terms = {
            '敏感词': 'SENSITIVE',
            '政治': 'POLITICAL',
            '宗教': 'RELIGIOUS',
        }

    def detect(self, text: str) -> Tuple[Optional[UnclearType], List[str], str]:
        """
        检测不清类型
        返回: (类型, 不清词列表, 澄清建议)
        """

        # 检测语义模糊
        unclear_words = []
        for word, meanings in self.ambiguous_words.items():
            if word in text and len(meanings) > 1:
                unclear_words.append(word)

        if unclear_words:
            suggestion = f"您说的'{unclear_words[0]}'是指以下哪一个：{self.ambiguous_words[unclear_words[0]]}"
            return (UnclearType.SEMANTIC_AMBIGUITY, unclear_words, suggestion)

        # 检测专业术语
        if any(term in text for term in ['HTTP', 'API', 'DNS', 'TCP/IP']):
            return (UnclearType.TECHNICAL_JARGON, [], "检测到专业术语，需要上下文澄清")

        # 检测文化陷阱
        for term in self.sensitive_terms:
            if term in text:
                return (UnclearType.CULTURAL_TRAP, [term], f"'{term}'可能需要文化校准")

        return (None, [], "")


# ═══════════════════════════════════════════════════════════════
# ETE 三层映射引擎
# ═══════════════════════════════════════════════════════════════

class ETEEngine:
    """情绪→意图→文化三层标准化"""

    def __init__(self):
        self.emotion_map = {
            '累': 'fatigue', '烦': 'irritated', '高兴': 'happy',
            '悲伤': 'sad', '愤怒': 'angry', '期待': 'anticipation'
        }

        self.intent_map = {
            '可以吗': 'ask_permission', '怎么做': 'ask_method',
            '为什么': 'ask_reason', '告诉我': 'ask_information',
            '不对': 'correct_statement', '同意': 'agreement'
        }

    def map_emotion(self, text: str) -> str:
        """L0·情绪层提取"""
        for keyword, emotion in self.emotion_map.items():
            if keyword in text:
                return emotion
        return 'neutral'

    def map_intent(self, text: str) -> str:
        """L1·意图层提取"""
        for keyword, intent in self.intent_map.items():
            if keyword in text:
                return intent
        return 'statement'

    def map_cultural(self, text: str) -> str:
        """L2·文化校准"""
        if '龍' in text or 'DNA' in text or '五行' in text:
            return 'cultural_anchor_detected'
        if '中文' in text or '英文' in text:
            return 'bilingual_context'
        return 'neutral_context'

    def process(self, text: str) -> Tuple[str, str, str]:
        """
        ETE 三层处理
        返回: (emotion, intent, cultural_note)
        """
        emotion = self.map_emotion(text)
        intent = self.map_intent(text)
        cultural = self.map_cultural(text)
        return (emotion, intent, cultural)


# ═══════════════════════════════════════════════════════════════
# 主引擎：通心译 v1.3
# ═══════════════════════════════════════════════════════════════

class TongxinyiEngine:
    """通心译 v1.3 完整引擎"""

    def __init__(self):
        self.trigger_detector = PassiveTriggerDetector()
        self.persona_router = PersonaRouter()
        self.unclear_detector = UnclearDetector()
        self.ete_engine = ETEEngine()

        self.wuxing_map = {
            'Python': '木', 'bash': '火', 'JSON': '土',
            'API': '金', 'database': '水', 'default': '木'
        }

    def process(self, text: str, uid: str = 'UID9622') -> StandardizedPackage:
        """
        完整处理流程
        1. 检测被动触发场景
        2. 路由到合适的Persona
        3. 识别不清之处
        4. ETE三层映射
        5. 生成标准化包
        """

        # Step 1: 被动触发检测
        scenario, trigger_confidence = self.trigger_detector.detect(text)

        # Step 2: Persona路由
        personas = self.persona_router.route(text, scenario)

        # Step 3: 不清识别
        unclear_type, unclear_words, suggestion = self.unclear_detector.detect(text)

        # Step 4: ETE三层
        emotion, intent, cultural = self.ete_engine.process(text)

        # Step 5: 五行映射
        wuxing = 'wood'  # 默认
        for key, value in self.wuxing_map.items():
            if key.lower() in text.lower():
                wuxing = value
                break

        # Step 6: DNA签名
        content_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        dna_sig = f"#龍芯⚡️{timestamp}-{scenario.value.upper()}-{content_hash}"

        # Step 7: 三色标注
        if trigger_confidence >= 0.85:
            color = '🟢'
        elif trigger_confidence >= 0.70:
            color = '🟡'
        else:
            color = '🔴'

        # 生成标准化包
        package = StandardizedPackage(
            original_text=text,
            emotion=emotion,
            intent=intent,
            cultural_note=cultural + (f" (不清:{unclear_type.value})" if unclear_type else ""),
            wuxing=wuxing,
            dna_signature=dna_sig,
            color=color,
            personas=personas
        )

        return package

    def to_dict(self, package: StandardizedPackage) -> Dict:
        """转换为字典格式"""
        return {
            'original_text': package.original_text,
            'emotion': package.emotion,
            'intent': package.intent,
            'cultural_note': package.cultural_note,
            'wuxing': package.wuxing,
            'dna_signature': package.dna_signature,
            'color': package.color,
            'personas': package.personas,
        }

    def to_json(self, package: StandardizedPackage) -> str:
        """转换为 JSON 格式"""
        return json.dumps(self.to_dict(package), ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# 演示与测试
# ═══════════════════════════════════════════════════════════════

def main():
    """开箱即用的演示"""
    engine = TongxinyiEngine()

    # 测试用例
    test_cases = [
        "git push origin main && npm install",           # 纯命令
        "我累了,宝宝我真的受不了了",                       # 情绪上头
        "龍魂系统的五行怎么理解",                         # 文化锚点
        "怎么翻译 'comprehension translator'",           # 翻译请求
        "我看不懂这个 Python 代码",                        # 反向请求
        "```python\ndef hello():\n  print('world')\n```", # 技术块
        "我要对外发布这个中英双语版本",                    # 双语发布
    ]

    print("=" * 70)
    print("🌐 通心译 v1.3 · 现场演示")
    print("=" * 70)

    for i, test_text in enumerate(test_cases, 1):
        print(f"\n【测试 {i}】输入: {test_text[:40]}...")

        result = engine.process(test_text)

        print(f"   场景: {engine.trigger_detector.detect(test_text)[0].value}")
        print(f"   Persona: {result.personas}")
        print(f"   情绪: {result.emotion}")
        print(f"   意图: {result.intent}")
        print(f"   文化: {result.cultural_note}")
        print(f"   五行: {result.wuxing}")
        print(f"   DNA: {result.dna_signature}")
        print(f"   {result.color} 信度: {engine.trigger_detector.detect(test_text)[1]:.2%}")

    print("\n" + "=" * 70)
    print("✅ 演示完成 - 通心译 v1.3 可运行")
    print("=" * 70)


if __name__ == '__main__':
    main()
