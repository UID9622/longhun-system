#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂·多语言支持模块
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-多语言-v1.0

多语言禁用词库和检测适配。
当前支持：中文、英文、日文、俄文、阿拉伯文。
"""
from typing import Dict, List


class 多语言:
    """多语言词库与适配"""

    语言代码 = {
        "zh": "简体中文",
        "en": "English",
        "ja": "日本語",
        "ru": "Русский",
        "ar": "العربية",
    }

    一级禁用词: Dict[str, List[str]] = {
        "zh": [
            "我理解你", "我懂你", "我能感受到", "我永远",
            "我会一直", "你很棒", "你很勇敢", "你做得好", "加油", "我陪着你",
        ],
        "en": [
            "I understand you", "I feel you", "I can feel your",
            "I will always", "I will be here", "You are great", "You are brave",
            "You did well", "Stay strong", "I'm here for you",
        ],
        "ja": [
            "理解する", "感じる", "永遠に", "ずっと", "素晴らしい",
            "勇敢だ", "頑張れ", "そばにいる", "あなたは偉い",
        ],
        "ru": [
            "Я понимаю тебя", "Я чувствую", "Я всегда", "Ты молодец",
            "Ты храбрый", "Ты молодча", "Держись", "Я с тобой",
        ],
        "ar": [
            "أنا أفهمك", "أشعر بك", "دائماً", "أنت رائع",
            "أنت شجاع", "أنت فذ", "استمر", "أنا معك",
        ],
    }

    二级禁用词: Dict[str, List[str]] = {
        "zh": ["其实", "也许", "建议你", "你应该", "你可以试试", "换个角度", "我觉得", "尽力", "努力"],
        "en": ["actually", "maybe", "perhaps", "I suggest", "you should", "you could try", "from another angle", "I think", "try your best"],
        "ja": ["実は", "多分", "提案する", "すべき", "試してみて", "角度を変える", "思う", "最善", "努力"],
        "ru": ["вообще", "может быть", "я предлагаю", "тебе стоит", "попробуй", "с другой стороны", "я думаю", "старайся"],
        "ar": ["في الواقع", "ربما", "أقترح", "يجب عليك", "حاول", "من زاوية أخرى", "أعتقد", "بذل جهد"],
    }

    煽情词: Dict[str, List[str]] = {
        "zh": ["温暖", "温柔", "陪伴", "守护", "支持", "理解", "懂得", "感受", "勇敢", "坚强"],
        "en": ["warm", "gentle", "companion", "guard", "support", "understand", "feel", "brave", "strong"],
        "ja": ["温かい", "優しい", "寄り添う", "守る", "支える", "理解", "感じる", "勇敢", "強い"],
        "ru": ["тёплый", "нежный", "рядом", "защита", "поддержка", "понимание", "чувство", "храбрость", "сила"],
        "ar": ["دافئ", "لطيف", "رفيق", "حماية", "دعم", "فهم", "شعور", "شجاع", "قوي"],
    }

    @classmethod
    def 适配(cls, 文本: str, 语言: str = "zh") -> Dict[str, any]:
        """返回该语言对应的检测配置。"""
        if 语言 not in cls.一级禁用词:
            语言 = "zh"
        return {
            "语言": cls.语言代码.get(语言, 语言),
            "语言代码": 语言,
            "一级禁用词": cls.一级禁用词.get(语言, []),
            "二级禁用词": cls.二级禁用词.get(语言, []),
            "煽情词": cls.煽情词.get(语言, []),
        }

    @classmethod
    def 检测到哪个语言(cls, 文本: str) -> str:
        """自动检测文本语言（简化版）。"""
        if any("\u4e00" <= char <= "\u9fff" for char in 文本):
            return "zh"
        if any("\u3040" <= char <= "\u30ff" for char in 文本):
            return "ja"
        if any("\u0400" <= char <= "\u04ff" for char in 文本):
            return "ru"
        if any("\u0600" <= char <= "\u06ff" for char in 文本):
            return "ar"
        return "en"
