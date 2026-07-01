#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 标签变量字典 | CNSH Tag Variables
DNA: #龍芯⚡️2026-07-01-CNSH-TAG-VARIABLES-v1.0

将龍魂标签体系暴露为 CNSH 风格的变量名，支持中文键。
用于在 CNSH 脚本/配置中引用龍魂标签。
"""

from typing import Any, Dict, Optional

# DNA常量
DNA = "#龍芯⚡️2026-07-01-CNSH-TAG-VARIABLES-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# ═══════════════════════════════════════════════════════════════
# CNSH 标签变量主表
# ═══════════════════════════════════════════════════════════════

CNSH_TAG_VARS: Dict[str, Dict[str, Any]] = {
    # ── 五行 ──
    "$五行.金": {"type": "五行", "element": "金", "unicode": "\u91d1", "color": "#FFFFFF", "code": "METAL"},
    "$五行.木": {"type": "五行", "element": "木", "unicode": "\u6728", "color": "#228B22", "code": "WOOD"},
    "$五行.水": {"type": "五行", "element": "水", "unicode": "\u6c34", "color": "#1E90FF", "code": "WATER"},
    "$五行.火": {"type": "五行", "element": "火", "unicode": "\u706b", "color": "#DC143C", "code": "FIRE"},
    "$五行.土": {"type": "五行", "element": "土", "unicode": "\u571f", "color": "#8B4513", "code": "EARTH"},

    "$五行.金旺": {"type": "五行状态", "element": "金", "state": "旺", "symbol": "\u91d1\U0001f525", "desc": "金旺·鼎盛", "hex": "#FFD700", "code": "METAL_PEAK"},
    "$五行.火旺": {"type": "五行状态", "element": "火", "state": "旺", "symbol": "\u706b\U0001f480", "desc": "火旺·炽烈", "hex": "#8B0000", "code": "FIRE_PEAK"},
    "$五行.水旺": {"type": "五行状态", "element": "水", "state": "旺", "symbol": "\u6c34\U0001f30a", "desc": "水旺·奔流", "hex": "#00008B", "code": "WATER_PEAK"},
    "$五行.木旺": {"type": "五行状态", "element": "木", "state": "旺", "symbol": "\u6728\U0001f333", "desc": "木旺·繁茂", "hex": "#006400", "code": "WOOD_PEAK"},
    "$五行.土旺": {"type": "五行状态", "element": "土", "state": "旺", "symbol": "\u571f\U0001f3d4", "desc": "土旺·稳重", "hex": "#8B4513", "code": "EARTH_PEAK"},

    # ── 八卦 ──
    "$八卦.乾": {"type": "八卦", "gua": "乾", "unicode_char": "\u4e7e", "unicode_trigram": "\u2630", "element": "金", "color": "#FFD700", "code": "QIAN"},
    "$八卦.坤": {"type": "八卦", "gua": "坤", "unicode_char": "\u5764", "unicode_trigram": "\u2637", "element": "土", "color": "#8B4513", "code": "KUN"},
    "$八卦.震": {"type": "八卦", "gua": "震", "unicode_char": "\u9707", "unicode_trigram": "\u2633", "element": "木", "color": "#228B22", "code": "ZHEN"},
    "$八卦.巽": {"type": "八卦", "gua": "巽", "unicode_char": "\u5dfd", "unicode_trigram": "\u2634", "element": "木", "color": "#32CD32", "code": "XUN"},
    "$八卦.坎": {"type": "八卦", "gua": "坎", "unicode_char": "\u574e", "unicode_trigram": "\u2635", "element": "水", "color": "#1E90FF", "code": "KAN"},
    "$八卦.离": {"type": "八卦", "gua": "离", "unicode_char": "\u79bb", "unicode_trigram": "\u2632", "element": "火", "color": "#DC143C", "code": "LI"},
    "$八卦.艮": {"type": "八卦", "gua": "艮", "unicode_char": "\u826e", "unicode_trigram": "\u2636", "element": "土", "color": "#696969", "code": "GEN"},
    "$八卦.兑": {"type": "八卦", "gua": "兑", "unicode_char": "\u5151", "unicode_trigram": "\u2631", "element": "金", "color": "#FFD700", "code": "DUI"},

    # ── 甲骨文 ──
    "$甲骨文.启": {"type": "甲骨文", "char": "启", "unicode": "\u542f", "tag": "START", "color": "#00C853"},
    "$甲骨文.止": {"type": "甲骨文", "char": "止", "unicode": "\u6b62", "tag": "STOP", "color": "#FF1744"},
    "$甲骨文.行": {"type": "甲骨文", "char": "行", "unicode": "\u884c", "tag": "RUN", "color": "#2979FF"},
    "$甲骨文.成": {"type": "甲骨文", "char": "成", "unicode": "\u6210", "tag": "SUCCESS", "color": "#00C853"},
    "$甲骨文.败": {"type": "甲骨文", "char": "败", "unicode": "\u8d25", "tag": "FAIL", "color": "#D50000"},
    "$甲骨文.喜": {"type": "甲骨文", "char": "喜", "unicode": "\u559c", "tag": "JOY", "color": "#FFEA00"},
    "$甲骨文.怒": {"type": "甲骨文", "char": "怒", "unicode": "\u6012", "tag": "ANGER", "color": "#DD2C00"},
    "$甲骨文.爱": {"type": "甲骨文", "char": "爱", "unicode": "\u7231", "tag": "LOVE", "color": "#FF4081"},
    "$甲骨文.信": {"type": "甲骨文", "char": "信", "unicode": "\u4fe1", "tag": "TRUST", "color": "#0091EA"},
    "$甲骨文.王": {"type": "甲骨文", "char": "王", "unicode": "\u738b", "tag": "CORE", "color": "#FFD700"},
    "$甲骨文.民": {"type": "甲骨文", "char": "民", "unicode": "\u6c11", "tag": "EDGE", "color": "#9E9E9E"},

    # ── 状态 ──
    "$状态.通行": {"type": "三色状态", "color": "green", "emoji": "🟢", "label": "通行", "desc": "绿色通行，可直接执行"},
    "$状态.待审": {"type": "三色状态", "color": "yellow", "emoji": "🟡", "label": "待审", "desc": "黄色待审，需要确认"},
    "$状态.熔断": {"type": "三色状态", "color": "red", "emoji": "🔴", "label": "熔断", "desc": "红色熔断，停止执行"},

    # ── 龍魂核心 ──
    "$龍魂.标签总数": {"type": "常量", "value": 112},
    "$龍魂.DNA": {"type": "常量", "value": "#龍芯⚡️2026-07-01-LONGHUN-TAG-SYSTEM-v1.0"},
    "$龍魂.UID": {"type": "常量", "value": "UID9622"},
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


def expand_all() -> Dict[str, Dict[str, Any]]:
    """返回全部 CNSH 标签变量的副本"""
    return dict(CNSH_TAG_VARS)


def main():
    print("=" * 50)
    print("CNSH 标签变量字典")
    print(f"DNA: {DNA}")
    print("=" * 50)

    print("\n变量示例:")
    for name in ["$五行.金旺", "$八卦.乾", "$甲骨文.成", "$状态.通行"]:
        value = lookup(name)
        print(f"  {name}: {value}")

    print(f"\n总变量数: {len(CNSH_TAG_VARS)}")
    print(f"Emoji 映射数: {len(EMOJI_TO_LONGHUN)}")


if __name__ == "__main__":
    main()
