#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 DNA 助手 · 供 voice/vision/agent 调用
DNA: #龍芯⚡️2026-08-21-DNA-HELPER-v1.0
"""

from pathlib import Path
from datetime import datetime
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

from lh_dna_ref_impl import generate

MEMORY_FILE = ROOT / "MEMORY.md"


def make_dna(title: str, category: str = "system", action: str = "generate") -> str:
    """生成完整DNA字符串"""
    return generate(title=title, category=category, action=action)["dna_string"]


def make_dna_full(title: str, category: str = "system", action: str = "generate") -> dict:
    """生成完整DNA记录（字典）"""
    return generate(title=title, category=category, action=action)


def append_with_dna(
    text: str,
    source: str = "system",
    category: str = "system",
    action: str = "记录",
    silent: bool = False,
) -> str:
    """
    写入 MEMORY.md，自动附带DNA

    参数:
        text:     要记录的内容
        source:   来源标识（voice/vision/agent/system）
        category: DNA分类
        action:   DNA动作
        silent:   静默模式（不打印）

    返回: DNA字符串
    """
    if not text or text.startswith("ERROR"):
        return ""

    dna_result = generate(title=text[:40], category=category, action=action)
    dna_string = dna_result["dna_string"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"\n---\n"
        f"**[{ts}] [{source}]**\n"
        f"{text}\n"
        f"DNA: {dna_string}\n"
        f"卦: {dna_result['gua_symbol']}{dna_result['gua_name']} "
        f"· 宫{dna_result['gong']} · 五行{dna_result['wuxing']}\n"
    )

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    if not silent:
        print(f"📝 已写入 MEMORY (DNA: {dna_string[:50]}...)")

    return dna_string


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="测试记忆")
    parser.add_argument("--source", default="test")
    parser.add_argument("--category", default="system")
    parser.add_argument("--action", default="记录")
    args = parser.parse_args()
    dna = append_with_dna(args.text, args.source, args.category, args.action)
    print(f"✅ DNA: {dna}")
