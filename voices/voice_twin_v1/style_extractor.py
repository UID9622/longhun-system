#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂真声 · 风格提取器
从语音转写文本中提取 UID9622 的表达风格特征。

DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-VOICE-TWIN-STYLE-EXTRACTOR-v1.0
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent
TRANSCRIPTS = ROOT / "all-transcripts.txt"
PROFILE_PATH = ROOT / "style_profile.json"

# 情绪词库
EMOTION_WORDS = {
    "愤怒": ["操", "他妈", "狗日", "妈逼", "去他妈", "老子", "骂", "火", "气", "憋屈", "恶心", "恨"],
    "讽刺": ["呵呵", "哈哈哈", "好厉害", "完美", "真是", "牛逼"],
    "坚定": ["绝对", "一定", "必须", "不跪", "不会", "永远", "永不"],
    "孤独": ["没人懂", "一个人", "寂寞", "孤独", "没人"],
    "关怀": ["人民", "老百姓", "底层", "孩子", "后代", "传承"],
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_sentences(text: str) -> List[str]:
    # 语音转写缺少标点，按多种断句点切分
    # 1. 先按常见停顿词切分
    breakers = r"(对不对|是不是|知道吧|是吧|对吧|你說呢|我說|我覺得|其實|但是|不過|所以呢|反正|哎呀|哎呦|那個|這個|媽的|他媽的)"
    parts = re.split(breakers, text)
    chunks = []
    current = ""
    for p in parts:
        current += p
        if len(current) > 40:
            chunks.append(current.strip())
            current = ""
    if current:
        chunks.append(current.strip())
    
    # 2. 再按标点精分
    result = []
    for chunk in chunks:
        result.extend([s.strip() for s in re.split(r"[。！？\n,，;；]", chunk) if s.strip()])
    return [r for r in result if len(r) > 3]


def extract_profanity(text: str) -> List[str]:
    patterns = [r"他妈", r"妈逼", r"狗日", r"操", r"去他妈", r"老子", r"日", r"逼"]
    found = []
    for p in patterns:
        found.extend(re.findall(p, text))
    return found


def extract_style_features(text: str) -> Dict[str, Any]:
    sentences = split_sentences(text)
    words = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    bigrams = [words[i] + words[i + 1] for i in range(len(words) - 1)]
    
    # 高频词
    word_freq = Counter(words).most_common(50)
    bigram_freq = Counter(bigrams).most_common(30)
    
    # 句子长度
    sent_lengths = [len(s) for s in sentences]
    avg_sent_len = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0
    
    # 粗话比例
    profanity = extract_profanity(text)
    profanity_ratio = len(profanity) / len(words) if words else 0
    
    # 情绪分布
    emotion_scores = {}
    for emotion, keywords in EMOTION_WORDS.items():
        score = sum(text.count(k) for k in keywords)
        emotion_scores[emotion] = score
    
    # 常见开头
    starters = [s[:4] for s in sentences if len(s) >= 4]
    starter_freq = Counter(starters).most_common(20)
    
    # 口头禅
    filler_patterns = [r"对不对", r"是不是", r"知道吧", r"是吧", r"嘛", r"哎呀", r"他妈的", r"怎么说呢"]
    fillers = {p: len(re.findall(p, text)) for p in filler_patterns}
    
    return {
        "总字数": len(text),
        "句子数": len(sentences),
        "平均句长": round(avg_sent_len, 1),
        "粗话词数": len(profanity),
        "粗话比例": round(profanity_ratio, 4),
        "高频词": word_freq,
        "高频双词": bigram_freq,
        "情绪分布": emotion_scores,
        "常见句首": starter_freq,
        "口头禅": fillers,
    }


def main():
    text = load_text(TRANSCRIPTS)
    features = extract_style_features(text)
    PROFILE_PATH.write_text(json.dumps(features, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 风格特征已提取: {PROFILE_PATH}")
    print(f"   总字数: {features['总字数']}")
    print(f"   句子数: {features['句子数']}")
    print(f"   平均句长: {features['平均句长']}")
    print(f"   粗话比例: {features['粗话比例']:.2%}")
    print(f"   情绪分布: {features['情绪分布']}")


if __name__ == "__main__":
    main()
