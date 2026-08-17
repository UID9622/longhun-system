#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 情绪与噪点检测模块
识别用户输入中的情绪化表达、错别字、不专业用语

DNA: #龍芯⚡️丙午·丙申·壬戌·辰时-EMOTION-DETECT-UID9622
"""

import re
from typing import Dict, List, Tuple


class EmotionNoiseDetector:
    """情绪与噪点检测器"""

    # 情绪关键词 (用于触发纠偏，但不输出安慰)
    EMOTION_KEYWORDS = [
        "生气", "愤怒", "烦", "无语", "郁闷", "恼火", "暴躁",
        "靠", "操", "我靠", "我去", "什么鬼", "搞什么", "他妈",
        "不行", "太差", "烂", "垃圾", "废物", "坑",
        "崩溃", "绝望", "无奈", "晕", "晕死", "头大",
        "烦死了", "累死了", "气死了", "急死了", "恨死",
        "赶紧", "快点", "马上", "立刻", "现在",
        "怎么搞的", "怎么回事", "什么情况", "又出问题",
    ]

    # 不专业用词 (口语化、不精确)
    UNPROFESSIONAL_KEYWORDS = [
        "那个", "这个", "就是", "嗯", "啊", "哦", "哎",
        "好吧", "算了", "就这样", "随便", "都行",
        "一堆", "一堆堆", "一大堆", "一点点",
        "随便搞搞", "差不多就行",
    ]

    # 常见错别字映射 (错误写法 -> 正确写法)
    TYPO_MAP = {
        "登陆": "登录",
        "帐号": "账号",
        "秘码": "密码",
        "搜素": "搜索",
        "提价": "提交",
        "接受": "接收",
        "反应": "反映",
        "计画": "计划",
        "分折": "分析",
        "配值": "配置",
        "部属": "部署",
        "班本": "版本",
        "跟新": "更新",
        "安转": "安装",
        "下栽": "下载",
        "上穿": "上传",
        "册除": "删除",
        "复志": "复制",
        "沾贴": "粘贴",
        "保荐": "保存",
        "遍历": "遍历",
        "调式": "调试",
        "除错": "调试",
        "网制": "网关",
        "路游": "路由",
        "结口": "接口",
    }

    # 情绪强度加权
    EMOTION_INTENSITY = {
        "他妈": 3, "操": 3, "垃圾": 3, "废物": 3,
        "崩溃": 3, "绝望": 3, "愤怒": 3,
        "烦死了": 2, "气死了": 2, "急死了": 2, "无语": 2,
        "赶紧": 1, "快点": 1, "马上": 1, "立刻": 1,
    }

    @classmethod
    def detect_emotion(cls, text: str) -> Tuple[bool, List[str], int]:
        """检测情绪化表达，返回 (是否含情绪, 关键词列表, 强度总分)"""
        detected = [kw for kw in cls.EMOTION_KEYWORDS if kw in text]
        intensity = sum(cls.EMOTION_INTENSITY.get(kw, 1) for kw in detected)
        return len(detected) > 0, detected, intensity

    @classmethod
    def detect_unprofessional(cls, text: str) -> Tuple[bool, List[str]]:
        """检测不专业用词"""
        detected = [kw for kw in cls.UNPROFESSIONAL_KEYWORDS if kw in text]
        return len(detected) > 0, detected

    @classmethod
    def correct_typos(cls, text: str) -> str:
        """纠正常见错别字"""
        corrected = text
        for wrong, right in cls.TYPO_MAP.items():
            corrected = corrected.replace(wrong, right)
        return corrected

    @classmethod
    def clean_noise(cls, text: str) -> str:
        """去除明显口语化前缀/后缀"""
        # 去除句首的 嗯/啊/哦/哎
        text = re.sub(r"^[嗯啊哦哎]+[,，]?", "", text)
        # 去除句末的 吧/啊/哦/嗯
        text = re.sub(r"[,，]?[吧啊哦嗯]+$", "", text)
        return text.strip()

    @classmethod
    def detect_noise(cls, text: str) -> Dict:
        """综合检测噪点"""
        has_emotion, emotions, intensity = cls.detect_emotion(text)
        has_unpro, unpro = cls.detect_unprofessional(text)
        corrected = cls.correct_typos(text)
        cleaned = cls.clean_noise(corrected)
        has_typo = corrected != text or cleaned != corrected

        return {
            "has_emotion": has_emotion,
            "emotions": emotions,
            "emotion_intensity": intensity,
            "has_unprofessional": has_unpro,
            "unprofessional_words": unpro,
            "has_typo": has_typo,
            "corrected_text": cleaned,
            "original_text": text,
        }


# 测试
if __name__ == "__main__":
    test_texts = [
        "这个功能怎么搞的，烦死了，赶紧帮我修复一下",
        "登录不上去了，靠，什么情况",
        "接收邮件设置有问题，请分析",
        "好无语啊，这个配置怎么又出问题了",
        "搜素功能用不了",
    ]
    for t in test_texts:
        result = EmotionNoiseDetector.detect_noise(t)
        print(f"输入: {t}")
        print(f"  情绪: {result['emotions']} (强度 {result['emotion_intensity']})")
        print(f"  错别字修正: {result['corrected_text']}")
        print()
