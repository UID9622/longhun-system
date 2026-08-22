#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂真声 · 情感阅读稿生成器
把话题/草稿转成适合朗读的版本，保留语气词和情绪停顿。

DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-VOICE-TWIN-READING-v1.0
"""

import json
from pathlib import Path
from draft_generator import load_style_profile, load_transcripts_sample, call_ollama, MODEL

ROOT = Path(__file__).resolve().parent


def build_reading_prompt(profile: dict[str, Any], sample: str) -> str:
    fillers = profile.get("口头禅", {})
    return f"""你是 UID9622（龍芯北辰）的声音复刻员。你的任务是把一个话题或草稿改写成**适合朗读的阅读稿**。

【朗读风格要求】
- 必须保留 UID9622 的口头禅和语气词："对不对"、"是不是"、"嘛"、"啊"、"知道吧"、"好吧"
- 要有情绪起伏，不是冷冰冰念稿
- 用短句、口语化，适合一口气读下来
- 在需要停顿、重音、情绪的地方用括号标注，例如：（停顿）、（加重）、（苦笑）、（叹气）
- 结尾可以留个反问或呼吁

【参考语气】
- 接地气、温州口音影响、直接
- 该骂就骂，但不对老百姓撒气
- 常用"老子""他妈""狗日"表达愤怒，但阅读稿里可以适度保留
- 情绪关键词：愤怒{profile.get('情绪分布', {}).get('愤怒', 0)}、坚定{profile.get('情绪分布', {}).get('坚定', 0)}、关怀{profile.get('情绪分布', {}).get('关怀', 0)}

【参考语料片段】
{sample[:1200]}

【输出格式】
只输出阅读稿正文，不要解释。标题用 # 开头。段落之间空一行。
"""


def generate_reading(topic_or_draft: str) -> str:
    profile = load_style_profile()
    sample = load_transcripts_sample()
    system_prompt = build_reading_prompt(profile, sample)
    user_prompt = f"请把以下内容改写成有温度的阅读稿：\n\n{topic_or_draft}"
    return call_ollama(system_prompt, user_prompt)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂真声阅读稿生成器")
    parser.add_argument("topic", nargs="?", help="话题或草稿")
    args = parser.parse_args()
    topic = args.topic or input("请输入话题或草稿: ")
    print(f"🎙️ 正在生成阅读稿...\n")
    result = generate_reading(topic)
    print(result)
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in topic)[:30]
    out_path = ROOT / f"reading_{safe}.md"
    out_path.write_text(f"# 阅读稿: {topic}\n\n{result}\n", encoding="utf-8")
    print(f"\n✅ 阅读稿已保存: {out_path}")


if __name__ == "__main__":
    main()
