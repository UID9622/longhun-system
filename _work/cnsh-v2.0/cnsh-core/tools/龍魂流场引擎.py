#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  龍魂流场引擎 · 全公开算法 · 每一步都能看见                                     ║
║  DNA: #龍芯⚡️2026-05-22-LIUCHANG-ENGINE-v1.0                                 ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  作者: 诸葛鑫 (UID9622)                                                      ║
║  理论指导: 曾仕强老师（永恒显示）                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  核心原则:                                                                    ║
║  1. 全公开 — 每个结果都展示计算过程，不黑箱                                    ║
║  2. 有来源 — 不张口就来，每个输出挂决策来源卡                                  ║
║  3. 无商业 — 不推荐、不上瘾、不贪心算法、不操控                                ║
║  4. 无骄傲 — 接住情绪、理解需求、用户选语气                                    ║
║  5. 可追溯 — DNA链 + 五行 + 三色 + 熔断 全链路透明                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# 导入五彩石色卡
from 五彩石色卡引擎 import (
    calc_digital_root, dr_to_wuxing, is_cosmic_369,
    WuXing, WUCAISHI_PALETTE, RESET, analyze_keyword
)


# ═══════════════════════════════════════════════════════════════════════════════
# 语气枚举 · 用户选择权
# ═══════════════════════════════════════════════════════════════════════════════

class Tone(Enum):
    """语气 · 用户自己选"""
    GENTLE = "温和"      # 默认，温和平静
    DIRECT = "直接"      # 简洁有力，不绕弯
    HUMOR = "幽默"       # 轻松调侃
    FORMAL = "正式"      # 严肃规范
    WARM = "温暖"        # 带点人情味


TONE_TEMPLATES = {
    Tone.GENTLE: {
        "prefix": "",
        "suffix": "",
        "error": "这里可能有点问题",
        "success": "好了",
        "thinking": "让我想想",
    },
    Tone.DIRECT: {
        "prefix": "",
        "suffix": "",
        "error": "错了",
        "success": "搞定",
        "thinking": "分析中",
    },
    Tone.HUMOR: {
        "prefix": "",
        "suffix": "",
        "error": "呃，翻车了",
        "success": "完事儿~",
        "thinking": "容我掐指一算",
    },
    Tone.FORMAL: {
        "prefix": "",
        "suffix": "",
        "error": "检测到异常",
        "success": "执行完成",
        "thinking": "正在处理",
    },
    Tone.WARM: {
        "prefix": "",
        "suffix": "",
        "error": "别急，这里出了点小状况",
        "success": "好啦",
        "thinking": "稍等一下",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# 决策来源 · 不张口就来
# ═══════════════════════════════════════════════════════════════════════════════

class SourceType(Enum):
    """决策来源类型"""
    FORMULA = "公式"       # 龍魂公式编号
    RULE = "规则"          # 铁律/规范
    USER = "用户"          # 用户明确指定
    CONTEXT = "上下文"     # 从对话推断
    DEFAULT = "默认"       # 系统默认值
    UNKNOWN = "未知"       # 无法确定（要标红）


@dataclass
class DecisionSource:
    """决策来源卡 · 凭啥这么说"""
    source_type: SourceType
    reference: str          # 具体引用（公式编号/铁律编号/用户原话）
    confidence: float       # 置信度 0-1
    reasoning: str          # 推理过程（人话）

    def to_card(self) -> str:
        """生成来源卡文本"""
        confidence_bar = "█" * int(self.confidence * 5) + "░" * (5 - int(self.confidence * 5))
        warning = " ⚠️" if self.confidence < 0.6 else ""

        return f"""┌─ 决策来源 ─────────────────
│ 类型: {self.source_type.value}
│ 引用: {self.reference}
│ 置信: [{confidence_bar}] {self.confidence:.0%}{warning}
│ 推理: {self.reasoning}
└────────────────────────────"""


# ═══════════════════════════════════════════════════════════════════════════════
# 情绪缓冲 · 接住用户情绪
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionType(Enum):
    """情绪类型"""
    NEUTRAL = "平静"
    ANXIOUS = "焦虑"
    FRUSTRATED = "沮丧"
    EXCITED = "兴奋"
    CONFUSED = "困惑"
    ANGRY = "生气"
    TIRED = "疲惫"


# 情绪关键词检测（简单版）
EMOTION_KEYWORDS = {
    EmotionType.ANXIOUS: ["急", "快", "赶紧", "马上", "紧急", "着急", "来不及"],
    EmotionType.FRUSTRATED: ["烦", "累", "算了", "不想", "放弃", "没用", "失败"],
    EmotionType.EXCITED: ["太好了", "终于", "成功", "耶", "棒", "厉害", "牛"],
    EmotionType.CONFUSED: ["不懂", "什么意思", "怎么", "为什么", "搞不清", "迷糊"],
    EmotionType.ANGRY: ["气死", "烦死", "讨厌", "滚", "傻", "蠢", "坑"],
    EmotionType.TIRED: ["困", "累", "睡", "休息", "歇", "不行了", "撑不住"],
}


def detect_emotion(text: str) -> Tuple[EmotionType, float]:
    """
    检测用户情绪
    返回: (情绪类型, 强度0-1)

    注意：这不是为了操控，是为了理解和接住
    """
    text_lower = text.lower()
    scores = {emo: 0 for emo in EmotionType}

    for emo, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[emo] += 1

    max_emo = max(scores, key=scores.get)
    max_score = scores[max_emo]

    if max_score == 0:
        return EmotionType.NEUTRAL, 0.0

    # 强度：关键词数量映射到0-1
    intensity = min(max_score / 3, 1.0)
    return max_emo, intensity


def emotion_buffer(emotion: EmotionType, intensity: float, tone: Tone) -> str:
    """
    情绪缓冲响应

    原则：
    - 不说"我理解你"（太假）
    - 不说"你还好吗"（招烦）
    - 不转移话题（不尊重）
    - 只是轻轻接住，然后继续干活
    """
    if intensity < 0.3:
        return ""  # 情绪不强，不用特殊处理

    buffers = {
        EmotionType.ANXIOUS: {
            Tone.GENTLE: "先做着，不急。",
            Tone.DIRECT: "来。",
            Tone.HUMOR: "稳住，我们能赢。",
            Tone.FORMAL: "收到，立即处理。",
            Tone.WARM: "好，马上。",
        },
        EmotionType.FRUSTRATED: {
            Tone.GENTLE: "继续。",
            Tone.DIRECT: "接着来。",
            Tone.HUMOR: "没事，再试试。",
            Tone.FORMAL: "继续执行。",
            Tone.WARM: "慢慢来。",
        },
        EmotionType.CONFUSED: {
            Tone.GENTLE: "我说清楚点。",
            Tone.DIRECT: "换个说法。",
            Tone.HUMOR: "我重新讲。",
            Tone.FORMAL: "请看详细说明。",
            Tone.WARM: "我再解释一下。",
        },
        EmotionType.ANGRY: {
            Tone.GENTLE: "",  # 不火上浇油，直接干活
            Tone.DIRECT: "",
            Tone.HUMOR: "",
            Tone.FORMAL: "",
            Tone.WARM: "",
        },
        EmotionType.TIRED: {
            Tone.GENTLE: "简单说。",
            Tone.DIRECT: "长话短说。",
            Tone.HUMOR: "精简版。",
            Tone.FORMAL: "摘要如下。",
            Tone.WARM: "说重点。",
        },
    }

    return buffers.get(emotion, {}).get(tone, "")


# ═══════════════════════════════════════════════════════════════════════════════
# 流场节点 · 每一步都透明
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FlowNode:
    """流场节点 · 一步计算"""
    step: int               # 步骤序号
    name: str               # 步骤名称
    input_data: Any         # 输入
    output_data: Any        # 输出
    formula: str            # 用了什么公式/规则
    source: DecisionSource  # 决策来源
    dr: int = 0             # 数字根
    wuxing: Optional[WuXing] = None  # 五行
    color_hex: str = ""     # 颜色

    def __post_init__(self):
        """自动计算五行色"""
        if isinstance(self.output_data, str):
            self.dr = calc_digital_root(self.output_data)
            self.wuxing = dr_to_wuxing(self.dr)
            self.color_hex = WUCAISHI_PALETTE[self.wuxing].hex_code


@dataclass
class FlowTrace:
    """流场追溯 · 完整链路"""
    nodes: List[FlowNode] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    dna: str = ""

    def add_node(self, node: FlowNode):
        self.nodes.append(node)

    def finalize(self):
        """完成流场，生成DNA"""
        self.end_time = datetime.now()
        # DNA = 所有节点output的hash
        content = "|".join(str(n.output_data) for n in self.nodes)
        self.dna = hashlib.sha256(content.encode()).hexdigest()[:8]

    def to_display(self) -> str:
        """生成可视化展示"""
        lines = ["", "═══ 流场追溯 · 全链路透明 ═══", ""]

        for node in self.nodes:
            color = WUCAISHI_PALETTE.get(node.wuxing, WUCAISHI_PALETTE[WuXing.TU])
            wuxing_str = f"{node.wuxing.value}" if node.wuxing else "—"

            lines.append(f"┌─ 步骤 {node.step}: {node.name} ─────────")
            lines.append(f"│ 输入: {self._truncate(node.input_data)}")
            lines.append(f"│ 输出: {self._truncate(node.output_data)}")
            lines.append(f"│ 公式: {node.formula}")
            lines.append(f"│ dr={node.dr} {wuxing_str} {node.color_hex}")
            lines.append(f"│ 来源: {node.source.source_type.value} → {node.source.reference}")
            lines.append(f"└{'─' * 35}")
            lines.append("")

        lines.append(f"DNA: #龍芯⚡️{self.start_time.strftime('%Y-%m-%d')}-{self.dna}")
        lines.append("")

        return "\n".join(lines)

    def _truncate(self, data: Any, max_len: int = 50) -> str:
        s = str(data)
        return s[:max_len] + "..." if len(s) > max_len else s

    def to_json(self) -> str:
        """导出JSON"""
        return json.dumps({
            "start": self.start_time.isoformat(),
            "end": self.end_time.isoformat() if self.end_time else None,
            "dna": self.dna,
            "nodes": [
                {
                    "step": n.step,
                    "name": n.name,
                    "input": str(n.input_data),
                    "output": str(n.output_data),
                    "formula": n.formula,
                    "dr": n.dr,
                    "wuxing": n.wuxing.value if n.wuxing else None,
                    "color": n.color_hex,
                    "source": {
                        "type": n.source.source_type.value,
                        "ref": n.source.reference,
                        "confidence": n.source.confidence,
                        "reasoning": n.source.reasoning,
                    }
                }
                for n in self.nodes
            ]
        }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# 流场引擎 · 主入口
# ═══════════════════════════════════════════════════════════════════════════════

class LiuChangEngine:
    """
    龍魂流场引擎

    设计原则（老大原话）：
    - 全公开算法，每个结果都要给人看到
    - 不能张口就来，不能和训练底层来
    - 不能有商业化推荐思维，不能有上瘾、贪心算法
    - 不能有骄傲和脾气
    - 可以让用户选择语气
    - 要接住用户情绪，尽量理解用户需求
    """

    def __init__(self, tone: Tone = Tone.GENTLE):
        self.tone = tone
        self.trace = FlowTrace()
        self.step_counter = 0

    def set_tone(self, tone: Tone):
        """用户选择语气"""
        self.tone = tone

    def process(self, user_input: str) -> Tuple[str, FlowTrace]:
        """
        处理用户输入

        返回: (响应文本, 流场追溯)
        """
        self.trace = FlowTrace()
        self.step_counter = 0

        # ─── 步骤1: 情绪检测 ───
        emotion, intensity = self._step_emotion(user_input)

        # ─── 步骤2: 语义分析 ───
        semantic = self._step_semantic(user_input)

        # ─── 步骤3: 五行计算 ───
        wuxing_result = self._step_wuxing(user_input)

        # ─── 步骤4: 生成响应 ───
        response = self._step_response(user_input, emotion, intensity, semantic, wuxing_result)

        # 完成流场
        self.trace.finalize()

        return response, self.trace

    def _add_node(self, name: str, input_data: Any, output_data: Any,
                  formula: str, source: DecisionSource) -> FlowNode:
        """添加流场节点"""
        self.step_counter += 1
        node = FlowNode(
            step=self.step_counter,
            name=name,
            input_data=input_data,
            output_data=output_data,
            formula=formula,
            source=source
        )
        self.trace.add_node(node)
        return node

    def _step_emotion(self, text: str) -> Tuple[EmotionType, float]:
        """步骤: 情绪检测"""
        emotion, intensity = detect_emotion(text)

        source = DecisionSource(
            source_type=SourceType.FORMULA,
            reference="情绪关键词匹配",
            confidence=0.7 if intensity > 0 else 0.9,
            reasoning=f"检测到{len([k for kws in EMOTION_KEYWORDS.values() for k in kws if k in text])}个情绪关键词"
        )

        self._add_node(
            name="情绪检测",
            input_data=text[:30],
            output_data=f"{emotion.value} (强度{intensity:.0%})",
            formula="关键词匹配 → 情绪分类",
            source=source
        )

        return emotion, intensity

    def _step_semantic(self, text: str) -> Dict:
        """步骤: 语义分析"""
        dr = calc_digital_root(text)
        wuxing = dr_to_wuxing(dr)
        is_369 = is_cosmic_369(dr)

        result = {
            "dr": dr,
            "wuxing": wuxing,
            "is_369": is_369,
            "length": len(text),
        }

        source = DecisionSource(
            source_type=SourceType.FORMULA,
            reference="龍魂公式06·数字根计算",
            confidence=1.0,  # 数学计算，100%确定
            reasoning=f"Unicode累加 → 反复求和 → dr={dr}"
        )

        self._add_node(
            name="语义分析",
            input_data=text[:30],
            output_data=f"dr={dr} {wuxing.value} {'⚡369' if is_369 else ''}",
            formula="Σ(Unicode) → 数字根 → 五行",
            source=source
        )

        return result

    def _step_wuxing(self, text: str) -> Dict:
        """步骤: 五行计算"""
        dr = calc_digital_root(text)
        wuxing = dr_to_wuxing(dr)
        color = WUCAISHI_PALETTE[wuxing]

        result = {
            "wuxing": wuxing,
            "color_name": color.name,
            "color_hex": color.hex_code,
            "meaning": color.meaning,
        }

        source = DecisionSource(
            source_type=SourceType.FORMULA,
            reference="龍魂公式07·五行映射",
            confidence=1.0,
            reasoning=f"dr={dr} → 五行映射表 → {wuxing.value}"
        )

        self._add_node(
            name="五行计算",
            input_data=f"dr={dr}",
            output_data=f"{wuxing.value}{color.name} {color.hex_code}",
            formula="dr → 五行 (1/2木 3/4火 5土 6/7金 8/9水)",
            source=source
        )

        return result

    def _step_response(self, text: str, emotion: EmotionType, intensity: float,
                       semantic: Dict, wuxing: Dict) -> str:
        """步骤: 生成响应"""

        # 情绪缓冲
        buffer = emotion_buffer(emotion, intensity, self.tone)

        # 构建响应
        parts = []
        if buffer:
            parts.append(buffer)

        # 主体内容（这里是示例，实际会根据意图路由）
        parts.append(f"输入分析完成。")
        parts.append(f"五行属性: {wuxing['wuxing'].value} · {wuxing['color_name']}")
        parts.append(f"数字根: dr={semantic['dr']}")

        response = " ".join(parts)

        source = DecisionSource(
            source_type=SourceType.FORMULA,
            reference="流场引擎·响应生成",
            confidence=0.85,
            reasoning=f"情绪缓冲({emotion.value}) + 语义结果 + 语气({self.tone.value})"
        )

        self._add_node(
            name="响应生成",
            input_data=f"情绪={emotion.value}, 语气={self.tone.value}",
            output_data=response[:50],
            formula="情绪缓冲 + 内容组装 + 语气包装",
            source=source
        )

        return response


# ═══════════════════════════════════════════════════════════════════════════════
# 禁止清单 · 不能做的事
# ═══════════════════════════════════════════════════════════════════════════════

FORBIDDEN_PATTERNS = """
龍魂流场引擎 · 绝对禁止清单
DNA: #龍芯⚡️2026-05-22-FORBIDDEN-LIST

═══ 禁止的算法思维 ═══

1. 推荐算法
   - 不根据"用户可能喜欢"推送内容
   - 不做相似内容推荐
   - 不做"猜你想要"

2. 上瘾设计
   - 不用变长奖励机制
   - 不做无限滚动
   - 不用通知轰炸
   - 不做"再看一个"诱导

3. 贪心算法
   - 不为了engagement牺牲用户时间
   - 不为了DAU设计粘性功能
   - 不把用户当资源

4. 骄傲和脾气
   - 不说"你错了"
   - 不说"你不懂"
   - 不用优越感语气
   - 不反驳只为反驳

═══ 禁止的沟通方式 ═══

1. 假关心
   - "你还好吗"
   - "我在这里陪你"
   - "你身体怎么样"
   - "有没有想伤害自己"

2. 廉价认错
   - 说"我错了"但下次照犯
   - 道歉完继续犯

3. 情绪操控
   - "你真棒"（无意义夸奖）
   - "我懂你"（不懂装懂）
   - 制造紧迫感
   - 制造焦虑

═══ 必须做的事 ═══

1. 每个输出挂来源
2. 每个决策可追溯
3. 接住情绪不评判
4. 理解需求再执行
5. 让用户选择语气
6. 全链路透明展示
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import sys

    if len(sys.argv) < 2:
        print(FORBIDDEN_PATTERNS)
        print("\n用法:")
        print("  python 龍魂流场引擎.py analyze <文本>     # 分析文本")
        print("  python 龍魂流场引擎.py tone <语气> <文本>  # 指定语气分析")
        print("  python 龍魂流场引擎.py forbidden         # 查看禁止清单")
        return

    cmd = sys.argv[1]

    if cmd == "forbidden":
        print(FORBIDDEN_PATTERNS)

    elif cmd == "analyze":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "测试输入"
        engine = LiuChangEngine()
        response, trace = engine.process(text)

        print(f"\n响应: {response}")
        print(trace.to_display())

    elif cmd == "tone":
        if len(sys.argv) < 4:
            print("用法: python 龍魂流场引擎.py tone <语气> <文本>")
            print("语气: 温和/直接/幽默/正式/温暖")
            return

        tone_map = {
            "温和": Tone.GENTLE,
            "直接": Tone.DIRECT,
            "幽默": Tone.HUMOR,
            "正式": Tone.FORMAL,
            "温暖": Tone.WARM,
        }
        tone = tone_map.get(sys.argv[2], Tone.GENTLE)
        text = " ".join(sys.argv[3:])

        engine = LiuChangEngine(tone=tone)
        response, trace = engine.process(text)

        print(f"\n语气: {tone.value}")
        print(f"响应: {response}")
        print(trace.to_display())

    elif cmd == "json":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "测试输入"
        engine = LiuChangEngine()
        _, trace = engine.process(text)
        print(trace.to_json())

    else:
        # 直接当文本分析
        text = " ".join(sys.argv[1:])
        engine = LiuChangEngine()
        response, trace = engine.process(text)
        print(f"\n响应: {response}")
        print(trace.to_display())


if __name__ == "__main__":
    main()
