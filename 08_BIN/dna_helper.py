#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·DNA 助手 v1.0 · 供 voice/vision/agent 调用的轻量封装
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷗复-DNA-HELPER-v1.0-CB002
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
三色: 🟢 对齐主引擎·修表后重签

说明:
  - 本助手基于 bin/lh_dna_ref_impl.py（零依赖参考实现，算法与主引擎 lh_dna_generator.py 逐字段一致）
  - DNA 格式: #龍芯⚡️四柱干支·卦-类别-动作-哈希8（确定性 sha256(title)[:8]，可复现）
  - 自动写记忆: 追加到 .codebuddy/memory/YYYY-MM-DD.md（跨会话记忆体系，非根目录 MEMORY.md）
  - 调用方: voice_input.py / vision_input.py / 各 Agent 引擎
"""

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))

from lh_dna_ref_impl import generate

MEMORY_DIR = ROOT / ".codebuddy" / "memory"


def make_dna(title: str, category: str = "system", action: str = "generate",
             date_str=None, hours=None) -> str:
    """生成完整 DNA 字符串（确定性：同一 title/日期/时辰 → 同一 DNA）"""
    result = generate(title=title, category=category, action=action,
                      date_str=date_str, hours=hours)
    return result["dna_string"]


def make_dna_full(title: str, category: str = "system", action: str = "generate",
                  date_str=None, hours=None) -> dict:
    """生成完整 DNA 记录（字典：dna_string/ganzhi/hexagram/title_hash/digital_root）"""
    return generate(title=title, category=category, action=action,
                    date_str=date_str, hours=hours)


def append_with_dna(text: str, source: str = "system", category: str = "system",
                    action: str = "记录", silent: bool = False) -> str:
    """
    写入 .codebuddy/memory/YYYY-MM-DD.md，自动附带 DNA 追溯

    参数:
        text: 要记录的内容（长度 >0 且不以 ERROR 开头才写）
        source: 来源标识（voice/vision/agent/system）
        category: DNA 分类
        action: DNA 动作
        silent: 静默模式（不打印）

    返回:
        DNA 字符串（失败返回空串）
    """
    if not text or text.startswith("ERROR"):
        return ""

    result = generate(title=text[:40], category=category, action=action)
    dna_string = result["dna_string"]

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")

    entry = (
        f"\n- **[{ts}] [{source}]**\n"
        f"  {text}\n"
        f"  DNA: {dna_string} · 卦{result['hexagram_symbol']}{result['hexagram_name']} · "
        f"数字根{result['digital_root']}\n"
    )

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    daily = MEMORY_DIR / f"{today}.md"
    with open(daily, "a", encoding="utf-8") as f:
        f.write(entry)

    if not silent:
        print(f"📝 已写入 {daily.name} (DNA: {dna_string})")

    return dna_string


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂 DNA 助手")
    parser.add_argument("--text", default="测试记忆", help="要记录的内容")
    parser.add_argument("--source", default="test", help="来源标识")
    parser.add_argument("--category", default="system", help="DNA 分类")
    parser.add_argument("--action", default="记录", help="DNA 动作")
    parser.add_argument("--dna-only", action="store_true", help="只生成不落盘")
    args = parser.parse_args()

    if args.dna_only:
        print(make_dna(args.text, args.category, args.action))
    else:
        dna = append_with_dna(args.text, args.source, args.category, args.action)
        print(f"✅ DNA: {dna}")
