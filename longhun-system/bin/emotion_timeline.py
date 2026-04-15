#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 · 诸葛鑫（龍芯北辰）
DNA追溯码: #龍芯⚡️2026-04-02-情绪时间线-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）

职责：第四步 · 情绪时间线
输入：用户文本
输出：情绪标签 + 写入 emotion_log.jsonl + 返回近5条情绪历史
"""

import json, os, re
from datetime import datetime

EMOTION_LOG = os.path.expanduser("~/longhun-system/logs/emotion_log.jsonl")

# 6种情绪及关键词
EMOTION_RULES = [
    ("顿悟", ["明白了", "懂了", "原来", "豁然", "开窍", "通了", "对对对", "就是这个"]),
    ("开心", ["嘿嘿", "哈哈", "棒", "爽", "好耶", "太好了", "厉害", "牛", "666"]),
    ("愤怒", ["妈的", "操", "气死", "烦死", "草", "恼火", "垃圾", "滚"]),
    ("崩溃", ["崩了", "完了", "撑不住", "不行了", "救命", "受不了", "绝望"]),
    ("焦虑", ["怎么办", "急", "担心", "怕", "慌", "来不及", "出问题"]),
    ("平静", ["好的", "嗯", "继续", "行", "知道了", "收到", "了解"]),
]

EMOTION_EMOJI = {
    "开心": "😊", "崩溃": "😤", "顿悟": "✨",
    "平静": "😌", "愤怒": "🤬", "焦虑": "😰",
}


def 检测情绪(text: str) -> str:
    """从文本检测情绪，返回情绪标签"""
    text_lower = text.lower()
    scores = {}
    for emotion, keywords in EMOTION_RULES:
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[emotion] = score
    if not scores:
        return "平静"
    return max(scores, key=scores.get)


def 记录情绪(text: str, source: str = "user") -> dict:
    """检测情绪并写入日志"""
    emotion = 检测情绪(text)
    record = {
        "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "emotion": emotion,
        "emoji": EMOTION_EMOJI.get(emotion, "😌"),
        "source": source,
        "snippet": text[:80],
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-情绪-{emotion}",
    }
    os.makedirs(os.path.dirname(EMOTION_LOG), exist_ok=True)
    with open(EMOTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def 读取近期情绪(n: int = 5) -> list:
    """读取最近N条情绪记录"""
    if not os.path.exists(EMOTION_LOG):
        return []
    records = []
    with open(EMOTION_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records[-n:]


def 情绪简报(records: list) -> str:
    """生成情绪时间线简报，供system prompt注入"""
    if not records:
        return ""
    parts = [f"{r['emoji']}{r['emotion']}({r['ts'][11:16]})" for r in records]
    trend = " → ".join(parts)
    latest = records[-1]
    return (
        f"【情绪时间线·近{len(records)}条】{trend}\n"
        f"当前情绪：{latest['emoji']}{latest['emotion']}"
    )


if __name__ == "__main__":
    tests = ["嘿嘿通了", "妈的又报错", "原来如此，懂了！", "嗯继续", "怎么办急死了"]
    print("=" * 40)
    for t in tests:
        r = 记录情绪(t)
        print(f"  输入: {t[:20]!r} → {r['emoji']}{r['emotion']}")
    print("\n近期情绪：")
    records = 读取近期情绪()
    print(" ", 情绪简报(records))
