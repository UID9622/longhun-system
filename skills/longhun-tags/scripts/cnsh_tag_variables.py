#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
CNSH 标签变量字典 | CNSH Tag Variables
DNA: #龍芯⚡️2026-07-01-CNSH-TAG-VARIABLES-v1.1

将龍魂标签体系暴露为 CNSH 风格的变量名，支持中文键。
用于在 CNSH 脚本/配置中引用龍魂标签。

v1.1 新增：
- $文化.{五行}.生克 / $文化.{五行}.生成
- $视觉.{五行}.{生/旺/休/囚/base/dark} 及对应 design token
- cultural_note(var)  helper
"""

from typing import Any, Dict, Optional

# 复用 longhun-tags 的色板与文化解释（同目录，无外部依赖）
from longhun_tags import COLOR_PALETTE, WUXING_CULTURAL_NOTES

# DNA常量
DNA = "#龍芯⚡️2026-07-01-CNSH-TAG-VARIABLES-v1.1"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

_ELEMENT_TOKEN_PREFIX = {"金": "gold", "木": "wood", "水": "water", "火": "fire", "土": "earth"}
_STATE_KEY = {"生": "light", "旺": "peak", "休": "rest", "囚": "trap"}

# ═══════════════════════════════════════════════════════════════
# CNSH 标签变量主表
# ═══════════════════════════════════════════════════════════════

CNSH_TAG_VARS: Dict[str, Dict[str, Any]] = {
    # ── 五行 ──
    "$五行.金": {"type": "五行", "element": "金", "unicode": "金", "color": COLOR_PALETTE["金"]["base"], "code": "METAL"},
    "$五行.木": {"type": "五行", "element": "木", "unicode": "木", "color": COLOR_PALETTE["木"]["base"], "code": "WOOD"},
    "$五行.水": {"type": "五行", "element": "水", "unicode": "水", "color": COLOR_PALETTE["水"]["base"], "code": "WATER"},
    "$五行.火": {"type": "五行", "element": "火", "unicode": "火", "color": COLOR_PALETTE["火"]["base"], "code": "FIRE"},
    "$五行.土": {"type": "五行", "element": "土", "unicode": "土", "color": COLOR_PALETTE["土"]["base"], "code": "EARTH"},

    "$五行.金旺": {"type": "五行状态", "element": "金", "state": "旺", "symbol": "金🔥", "desc": "金旺·鼎盛", "hex": COLOR_PALETTE["金"]["peak"], "code": "METAL_PEAK"},
    "$五行.火旺": {"type": "五行状态", "element": "火", "state": "旺", "symbol": "火💀", "desc": "火旺·炽烈", "hex": COLOR_PALETTE["火"]["peak"], "code": "FIRE_PEAK"},
    "$五行.水旺": {"type": "五行状态", "element": "水", "state": "旺", "symbol": "水🌊", "desc": "水旺·奔流", "hex": COLOR_PALETTE["水"]["peak"], "code": "WATER_PEAK"},
    "$五行.木旺": {"type": "五行状态", "element": "木", "state": "旺", "symbol": "木🌳", "desc": "木旺·繁茂", "hex": COLOR_PALETTE["木"]["peak"], "code": "WOOD_PEAK"},
    "$五行.土旺": {"type": "五行状态", "element": "土", "state": "旺", "symbol": "土🏔", "desc": "土旺·稳重", "hex": COLOR_PALETTE["土"]["peak"], "code": "EARTH_PEAK"},

    # ── 八卦 ──
    "$八卦.乾": {"type": "八卦", "gua": "乾", "unicode_char": "乾", "unicode_trigram": "☰", "element": "金", "color": COLOR_PALETTE["金"]["base"], "code": "QIAN"},
    "$八卦.坤": {"type": "八卦", "gua": "坤", "unicode_char": "坤", "unicode_trigram": "☷", "element": "土", "color": COLOR_PALETTE["土"]["base"], "code": "KUN"},
    "$八卦.震": {"type": "八卦", "gua": "震", "unicode_char": "震", "unicode_trigram": "☳", "element": "木", "color": COLOR_PALETTE["木"]["base"], "code": "ZHEN"},
    "$八卦.巽": {"type": "八卦", "gua": "巽", "unicode_char": "巽", "unicode_trigram": "☴", "element": "木", "color": COLOR_PALETTE["木"]["base"], "code": "XUN"},
    "$八卦.坎": {"type": "八卦", "gua": "坎", "unicode_char": "坎", "unicode_trigram": "☵", "element": "水", "color": COLOR_PALETTE["水"]["base"], "code": "KAN"},
    "$八卦.离": {"type": "八卦", "gua": "离", "unicode_char": "离", "unicode_trigram": "☲", "element": "火", "color": COLOR_PALETTE["火"]["base"], "code": "LI"},
    "$八卦.艮": {"type": "八卦", "gua": "艮", "unicode_char": "艮", "unicode_trigram": "☶", "element": "土", "color": COLOR_PALETTE["土"]["base"], "code": "GEN"},
    "$八卦.兑": {"type": "八卦", "gua": "兑", "unicode_char": "兑", "unicode_trigram": "☱", "element": "金", "color": COLOR_PALETTE["金"]["base"], "code": "DUI"},

    # ── 甲骨文 ──
    "$甲骨文.启": {"type": "甲骨文", "char": "启", "unicode": "启", "tag": "START", "color": "#00C853"},
    "$甲骨文.止": {"type": "甲骨文", "char": "止", "unicode": "止", "tag": "STOP", "color": "#FF1744"},
    "$甲骨文.行": {"type": "甲骨文", "char": "行", "unicode": "行", "tag": "RUN", "color": "#2979FF"},
    "$甲骨文.成": {"type": "甲骨文", "char": "成", "unicode": "成", "tag": "SUCCESS", "color": "#00C853"},
    "$甲骨文.败": {"type": "甲骨文", "char": "败", "unicode": "败", "tag": "FAIL", "color": "#D50000"},
    "$甲骨文.喜": {"type": "甲骨文", "char": "喜", "unicode": "喜", "tag": "JOY", "color": "#FFEA00"},
    "$甲骨文.怒": {"type": "甲骨文", "char": "怒", "unicode": "怒", "tag": "ANGER", "color": "#DD2C00"},
    "$甲骨文.爱": {"type": "甲骨文", "char": "爱", "unicode": "爱", "tag": "LOVE", "color": "#FF4081"},
    "$甲骨文.信": {"type": "甲骨文", "char": "信", "unicode": "信", "tag": "TRUST", "color": "#0091EA"},
    "$甲骨文.王": {"type": "甲骨文", "char": "王", "unicode": "王", "tag": "CORE", "color": "#FFD700"},
    "$甲骨文.民": {"type": "甲骨文", "char": "民", "unicode": "民", "tag": "EDGE", "color": "#9E9E9E"},

    # ── 状态 ──
    "$状态.通行": {"type": "三色状态", "color": "green", "emoji": "🟢", "label": "通行", "desc": "绿色通行，可直接执行"},
    "$状态.待审": {"type": "三色状态", "color": "yellow", "emoji": "🟡", "label": "待审", "desc": "黄色待审，需要确认"},
    "$状态.熔断": {"type": "三色状态", "color": "red", "emoji": "🔴", "label": "熔断", "desc": "红色熔断，停止执行"},

    # ── 龍魂核心 ──
    "$龍魂.标签总数": {"type": "常量", "value": 112},
    "$龍魂.DNA": {"type": "常量", "value": "#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.1"},
    "$龍魂.UID": {"type": "常量", "value": "UID9622"},
}

# 自动生成 $视觉.* 与 $文化.* 变量
for _elem, _palette in COLOR_PALETTE.items():
    _prefix = _ELEMENT_TOKEN_PREFIX[_elem]
    # 状态色
    for _state, _key in _STATE_KEY.items():
        CNSH_TAG_VARS[f"$视觉.{_elem}.{_state}"] = {
            "type": "视觉",
            "element": _elem,
            "state": _state,
            "hex": _palette[_key],
            "token": f"--lh-{_prefix}-{_key}",
        }
    # 基础/暗色
    CNSH_TAG_VARS[f"$视觉.{_elem}.base"] = {"type": "视觉", "element": _elem, "hex": _palette["base"], "token": f"--lh-{_prefix}-base"}
    CNSH_TAG_VARS[f"$视觉.{_elem}.dark"] = {"type": "视觉", "element": _elem, "hex": _palette["dark"], "token": f"--lh-{_prefix}-dark"}

    # 文化解释
    CNSH_TAG_VARS[f"$文化.{_elem}.生克"] = {
        "type": "文化",
        "element": _elem,
        "aspect": "生克",
        "note": WUXING_CULTURAL_NOTES[_elem]["生克"],
    }
    CNSH_TAG_VARS[f"$文化.{_elem}.生成"] = {
        "type": "文化",
        "element": _elem,
        "aspect": "生成",
        "note": WUXING_CULTURAL_NOTES[_elem]["生成"],
    }

# 西方 emoji -> 龍魂标签代码映射
EMOJI_TO_LONGHUN: Dict[str, str] = {
    "🔥": "火·旺",
    "🌱": "木·生",
    "🌳": "木·旺",
    "💧": "水·生",
    "🌊": "水·旺",
    "⚡": "震·动",
    "🛡️": "坎·正",
    "🚨": "火·囚",
    "✅": "成",
    "❌": "败",
    "⏳": "等",
    "🚀": "震·动",
    "💀": "死",
    "⭐": "星",
    "🔒": "水·囚",
    "📊": "思",
    "❤️": "爱",
    "💔": "哀",
    "😡": "怒",
    "😊": "喜",
    "🧑‍💻": "思",
    "🏗️": "土·生",
    "🎯": "上",
}


def lookup(var_name: str) -> Optional[Dict[str, Any]]:
    """
    查询 CNSH 标签变量

    示例:
        lookup("$五行.金旺") -> {...}
        lookup("$状态.通行") -> {...}
    """
    return CNSH_TAG_VARS.get(var_name)


def cultural_note(var_name: str) -> Optional[str]:
    """
    返回文化解释文本

    示例:
        cultural_note("$文化.金.生克") -> "金曰从革..."
    """
    entry = CNSH_TAG_VARS.get(var_name)
    if entry and entry.get("type") == "文化":
        return entry.get("note")
    return None


def expand_all() -> Dict[str, Dict[str, Any]]:
    """返回全部 CNSH 标签变量的副本"""
    return dict(CNSH_TAG_VARS)


def main():
    print("=" * 50)
    print("CNSH 标签变量字典")
    print(f"DNA: {DNA}")
    print("=" * 50)

    print("\n变量示例:")
    for name in ["$五行.金旺", "$八卦.乾", "$甲骨文.成", "$状态.通行",
                 "$文化.金.生克", "$视觉.水.囚"]:
        value = lookup(name)
        print(f"  {name}: {value}")

    print("\n文化解释 helper:")
    print(f"  cultural_note('$文化.木.生成'): {cultural_note('$文化.木.生成')}")

    print(f"\n总变量数: {len(CNSH_TAG_VARS)}")
    print(f"Emoji 映射数: {len(EMOJI_TO_LONGHUN)}")


if __name__ == "__main__":
    main()
