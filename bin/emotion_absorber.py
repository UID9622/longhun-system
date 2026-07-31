# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧽 龍魂·情绪海绵 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-EMOTION-ABSORBER-v1.0

为 lh.py 交互菜单提供安全的情绪温度检测，
不经过 shell 拼接，直接接收文本字符串。
"""

import json
from typing import Dict

# 简单关键词情绪词典（可按需扩展）
POSITIVE_WORDS = ["开心", "高兴", "棒", "喜欢", "好", "谢谢", "爱", "温暖", "加油", "感恩"]
NEGATIVE_WORDS = ["难过", "伤心", "愤怒", "恨", "失望", "痛苦", "焦虑", "压力", "恐惧", "绝望"]


def detect(text: str) -> Dict:
    """检测文本情绪温度并返回字典。"""
    if not text:
        return {
            "emotion": "空",
            "temperature": "平",
            "score": 0,
            "input_preview": "",
        }

    score = 0
    for w in POSITIVE_WORDS:
        if w in text:
            score += 1
    for w in NEGATIVE_WORDS:
        if w in text:
            score -= 1

    if score > 0:
        emotion = "积极"
        temperature = "暖"
    elif score < 0:
        emotion = "消极"
        temperature = "凉"
    else:
        emotion = "中性"
        temperature = "平"

    result = {
        "emotion": emotion,
        "temperature": temperature,
        "score": score,
        "input_preview": text[:120],
    }
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·情绪海绵")
    parser.add_argument("--text", "-t", type=str, required=True, help="待检测文本")
    args = parser.parse_args()
    print(json.dumps(detect(args.text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
