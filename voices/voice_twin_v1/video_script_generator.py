#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂真声 · 视频脚本生成器
把话题扩展成适合视频号/抖音的短视频脚本。

DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-VOICE-TWIN-VIDEO-SCRIPT-v1.0
"""

import json
from pathlib import Path
from draft_generator import load_style_profile, load_transcripts_sample, call_ollama

ROOT = Path(__file__).resolve().parent


def build_video_prompt(profile: dict[str, Any], sample: str) -> str:
    return f"""你是 UID9622（龍芯北辰）的短视频编导。你把一个话题扩展成**视频号/抖音短视频脚本**。

【脚本要求】
- 时长：1-3 分钟，约 300-600 字
- 结构：开头 3 秒抓眼球（钩子）→ 中间讲清楚事情/观点 → 结尾引导互动或行动
- 保留 UID9622 的语气："对不对"、"是不是"、"嘛"、接地气、有火气
- 分镜简单，适合一个人对着手机拍
- 在【画面】标注拍摄内容，在【口播】标注要说的内容

【输出格式】
# 标题
# 视频脚本：《标题》

## 镜头 1
【画面】...
【口播】...

## 镜头 2
...

## 结尾引导
...
"""


def generate_video_script(topic: str) -> str:
    profile = load_style_profile()
    sample = load_transcripts_sample()
    system_prompt = build_video_prompt(profile, sample)
    user_prompt = f"请为以下话题写一个短视频脚本：\n\n{topic}"
    return call_ollama(system_prompt, user_prompt)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂真声视频脚本生成器")
    parser.add_argument("topic", nargs="?", help="话题")
    args = parser.parse_args()
    topic = args.topic or input("请输入话题: ")
    print(f"🎬 正在生成视频脚本...\n")
    result = generate_video_script(topic)
    print(result)
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in topic)[:30]
    out_path = ROOT / f"video_{safe}.md"
    out_path.write_text(f"# 视频脚本: {topic}\n\n{result}\n", encoding="utf-8")
    print(f"\n✅ 视频脚本已保存: {out_path}")


if __name__ == "__main__":
    main()
