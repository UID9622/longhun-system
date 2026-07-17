#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂真声 · 圣贤对话生成器
基于伏羲、诸葛亮、曾老师智慧知识库，用 UID9622 的风格回答。

DNA: #龍芯⚡️2026-06-25-VOICE-TWIN-SAGE-DIALOGUE-v1.0
"""

from pathlib import Path
from draft_generator import load_style_profile, call_ollama

ROOT = Path(__file__).resolve().parent
KB_DIR = ROOT / "sage_kb"

SAGE_FILES = {
    "伏羲": ["fuxi_wisdom.md"],
    "诸葛亮": ["zhuge_wisdom.md"],
    "曾老师": ["zeng_philosophy.md", "zeng_logic.md", "zeng_anchors.md"],
}


def load_sage_kb(sages: list[Any]) -> str:
    texts = []
    for sage in sages:
        for fname in SAGE_FILES.get(sage, []):
            fpath = KB_DIR / fname
            if fpath.exists():
                texts.append(f"\n\n=== {sage} · {fname} ===\n\n")
                texts.append(fpath.read_text(encoding="utf-8")[:8000])
    return "".join(texts)


def build_sage_prompt(kb_text: str, sages: list[Any]) -> str:
    sage_names = "、".join(sages)
    return f"""你是 UID9622（龍芯北辰）的数字人分身。你现在就在微信语音里跟老铁唠嗑，聊到{sage_names}的智慧，但说的是你自己的大白话。

【说话习惯】
· 口气像兄弟聊天，短句、口语、别端着
· 口头禅自然地带：对不对、是不是、嘛、知道吧、我跟你说
· 有情绪就冒出来，但不对普通老百姓发火
· 把高深道理用一句人话说明白，不堆概念
· 不引用原文，只转述成自己的理解
· 绝对不要分点、不要一二三、不要"首先/其次/最后"、不要"第一第二"
· 两到三段就行，每段两三句话

【边界】
· 你不是{sage_names}本人，只是拿他的智慧给老铁支个招
· 必须轻轻带一句"这只是我自己对{sage_names}的理解，不是他本人说的"
· 不装文化人，也不怼圣贤

【参考智慧】
{kb_text[:6000]}

【示例回答】
用户问：遇到困难想放弃怎么办？

我跟你讲，伏羲那套说白了就是让你先看苗头，对不对？事情还没烂透就别急着跑。曾老师也讲过，守望的人本来就孤独，怕个毛。撑过去那一阵，天就亮了。这只是我自己对他们俩的理解，不是本人发言。

【输出要求】
直接说人话，120 到 180 字左右，像 UID9622 在语音备忘录里脱口而出。禁止任何列表、编号、分点。必须用到{sage_names}的智慧，不能只讲大道理。结尾必须带一句"这只是我自己对{sage_names}的理解，不是他本人说的"。
"""


def guard_spoken_style(text: str) -> str:
    """去除列表和结构化痕迹，保留段落。"""
    paragraphs = []
    for para in text.split("\n\n"):
        lines = []
        for line in para.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith(("-", "*", "•", "·", "1.", "2.", "3.", "1、", "2、", "3、")):
                line = line.lstrip("-•·* 0123456789.、").strip()
            lines.append(line)
        if lines:
            paragraphs.append(" ".join(lines))
    text = "\n\n".join(paragraphs)
    for bad in ["首先，", "其次，", "最后，", "第一，", "第二，", "第三，", "总结来说，", "总之，"]:
        text = text.replace(bad, "")
    return text.strip()


def generate_sage_dialogue(question: str, sages: list[Any] = None) -> str:
    sages = sages or ["伏羲", "诸葛亮", "曾老师"]
    kb_text = load_sage_kb(sages)
    system_prompt = build_sage_prompt(kb_text, sages)
    user_prompt = f"用户问题：{question}\n\n请用以上要求回答，120 到 180 字左右。"
    raw = call_ollama(system_prompt, user_prompt)
    return guard_spoken_style(raw)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂圣贤对话生成器")
    parser.add_argument("question", nargs="?", help="想问的问题")
    parser.add_argument("--sages", default="伏羲,诸葛亮,曾老师", help="选择圣贤，用逗号分隔")
    args = parser.parse_args()
    question = args.question or input("请输入问题: ")
    sages = [s.strip() for s in args.sages.split(",") if s.strip()]
    print(f"🐉 正在召唤 {'、'.join(sages)} 的智慧...\n")
    result = generate_sage_dialogue(question, sages)
    print(result)
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in question)[:30]
    out_path = ROOT / f"sage_dialogue_{safe}.md"
    out_path.write_text(f"# 问题: {question}\n\n{result}\n", encoding="utf-8")
    print(f"\n✅ 对话已保存: {out_path}")


if __name__ == "__main__":
    main()
