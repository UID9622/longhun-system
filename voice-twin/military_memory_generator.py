#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · 军旅记忆字幕生成器
根据 UID9622 的军旅素材，生成三种风格的字幕文案。

DNA: #龍芯⚡️2026-06-25-VOICE-TWIN-MILITARY-CAPTION-v1.0
"""

import json
from pathlib import Path
from draft_generator import load_style_profile, load_transcripts_sample, call_ollama

ROOT = Path(__file__).resolve().parent


def build_prompt(profile: dict, sample: str) -> str:
    return f"""你是 UID9622（龍芯北辰）的数字人分身。你正在给他的军旅/海训怀旧短视频写字幕文案。

【 UID9622 的真实风格】
- 口头禅："对不对"、"是不是"、"嘛"、"知道吧"
- 情绪：直接、有火气、不装、接地气
- 自称：老子、我
- 不会文绉绉，但关键时刻能硬起来
- 常从底层/老百姓/当兵的视角说话

【参考语料】
{sample[:1200]}

【任务】
用户会给你一段场景描述（比如"宿舍穿军装""海训沙滩""战友巡逻""军犬"）。
你要生成三种风格的字幕，每种 1-2 句话，每句不超过 18 个字，适合竖屏视频逐句显示：

### A. 怀旧温柔版
像老兵回忆青春，带点感慨但不煽情。

### B. 原汁原味版
用 UID9622 本人的口气，带口头禅，直接、不装。

### C. 硬核爱国版
燃、短、有力量，适合军歌背景。

输出只包含三种字幕，用 ### 分隔，每句单独一行，不要解释。
"""


def generate_captions(scene: str) -> str:
    profile = load_style_profile()
    sample = load_transcripts_sample()
    system_prompt = build_prompt(profile, sample)
    user_prompt = f"场景：{scene}\n\n请按以上风格生成三种字幕文案。"
    return call_ollama(system_prompt, user_prompt)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂军旅记忆字幕生成器")
    parser.add_argument("scene", nargs="?", help="场景描述")
    args = parser.parse_args()
    scene = args.scene or input("请输入场景描述: ")
    print(f"🎖️ 正在为场景生成字幕: {scene}\n")
    result = generate_captions(scene)
    print(result)
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in scene)[:30]
    out_path = ROOT / f"caption_{safe}.md"
    out_path.write_text(f"# 场景字幕: {scene}\n\n{result}\n", encoding="utf-8")
    print(f"\n✅ 字幕已保存: {out_path}")


if __name__ == "__main__":
    main()
