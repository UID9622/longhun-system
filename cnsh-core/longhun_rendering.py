#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂渲染模块 | LongHun Rendering Engine
DNA: #龍芯⚡️2026-07-01-LONGHUN-RENDERING-v1.0

无外部依赖，纯标准库实现。
功能：渲染龍魂标签、emoji、CNSH变量、页面头部、三色状态。
支持 html 与 markdown 两种风格。
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# DNA常量
DNA = "#龍芯⚡️2026-07-01-LONGHUN-RENDERING-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# 尝试复用 longhun-tags 数据
_TAGS_PATH = Path(__file__).resolve().parent.parent / "skills" / "longhun-tags" / "scripts"
if str(_TAGS_PATH) not in sys.path:
    sys.path.insert(0, str(_TAGS_PATH))

try:
    from longhun_tags import LongHunTagSystem
except Exception:
    LongHunTagSystem = None  # type: ignore

# 基础变量映射（避免依赖失败时仍可用）
CNSH_VAR_FALLBACK: Dict[str, Dict[str, Any]] = {
    "$五行.金旺": {"symbol": "金🔥", "desc": "金旺·鼎盛", "color": "#FFD700"},
    "$五行.木旺": {"symbol": "木🌳", "desc": "木旺·繁茂", "color": "#006400"},
    "$五行.水旺": {"symbol": "水🌊", "desc": "水旺·奔流", "color": "#00008B"},
    "$五行.火旺": {"symbol": "火💀", "desc": "火旺·炽烈", "color": "#8B0000"},
    "$五行.土旺": {"symbol": "土🏔️", "desc": "土旺·稳重", "color": "#8B4513"},
    "$八卦.乾": {"symbol": "☰", "desc": "乾·正位", "color": "#FFD700"},
    "$八卦.坤": {"symbol": "☷", "desc": "坤·正位", "color": "#8B4513"},
    "$状态.通行": {"symbol": "🟢", "desc": "绿色通行", "color": "#00C853"},
    "$状态.待审": {"symbol": "🟡", "desc": "黄色待审", "color": "#FFC107"},
    "$状态.熔断": {"symbol": "🔴", "desc": "红色熔断", "color": "#D50000"},
}

TRI_COLOR_STATES = {
    "green": {"emoji": "🟢", "label": "通行", "hex": "#00C853"},
    "yellow": {"emoji": "🟡", "label": "待审", "hex": "#FFC107"},
    "red": {"emoji": "🔴", "label": "熔断", "hex": "#D50000"},
}


def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def render_tag(tag_code: str, style: str = "html") -> str:
    """
    渲染龍魂标签

    style:
      - html:  <span style="color:#..." title="...">symbol desc</span>
      - md:    🟢 金旺·鼎盛
      - text:  金旺·鼎盛
    """
    tag: Optional[Dict[str, Any]] = None
    if LongHunTagSystem is not None:
        tag = LongHunTagSystem().get_tag(tag_code)

    if tag:
        label = tag.get("desc") or tag.get("label") or tag.get("char", tag_code)
        color = tag.get("hex") or tag.get("color", "#333333")
        symbol = tag.get("symbol") or tag.get("unicode", "")
        title = tag.get("usage", label)
    else:
        label = tag_code
        color = "#333333"
        symbol = ""
        title = ""

    text = f"{symbol} {label}".strip() if symbol and symbol not in label else label

    if style == "html":
        return f'<span style="color:{color};font-weight:bold" title="{title}">{text}</span>'
    elif style == "md":
        return f"`{text}`"
    return text


def render_emoji(emoji: str, style: str = "html") -> str:
    """
    将西方 emoji 渲染为 龍魂标签
    """
    tag_code = None
    if LongHunTagSystem is not None:
        resolved = LongHunTagSystem().resolve_emoji(emoji)
        if resolved:
            tag_code = resolved.get("龍魂标签")

    if tag_code:
        return render_tag(tag_code, style)

    # fallback
    fallback = {
        "🔥": "火·旺", "✅": "成", "❌": "败", "🚨": "火·囚",
        "🟢": "$状态.通行", "🟡": "$状态.待审", "🔴": "$状态.熔断",
    }.get(emoji)
    if fallback:
        return render_tag(fallback, style)
    return emoji


def render_cnsh_var(var_name: str, value: Any = None, style: str = "html") -> str:
    """
    渲染 CNSH 变量
    """
    meta: Optional[Dict[str, Any]] = None
    if LongHunTagSystem is not None:
        try:
            from cnsh_tag_variables import lookup
            meta = lookup(var_name)
        except Exception:
            pass

    if meta is None:
        meta = CNSH_VAR_FALLBACK.get(var_name)

    if meta is None:
        display = f"{var_name}={value}" if value is not None else var_name
        return display

    symbol = meta.get("symbol", "")
    desc = meta.get("desc", var_name)
    color = meta.get("color", "#333333")
    text = f"{symbol} {desc}".strip() if symbol else desc

    if style == "html":
        return f'<span style="color:{color};font-weight:bold" title="{var_name}">{text}</span>'
    elif style == "md":
        return text
    return desc


def render_page_header(title: str, dna: str) -> str:
    """
    渲染页面头部（HTML）
    """
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 40px; background: #f9f9f9; }}
  .lh-header {{ background: linear-gradient(135deg, #8B0000, #FFD700); color: white; padding: 24px; border-radius: 12px; }}
  .lh-header h1 {{ margin: 0; font-size: 28px; }}
  .lh-dna {{ font-family: monospace; margin-top: 8px; opacity: 0.9; }}
</style>
</head>
<body>
<div class="lh-header">
  <h1>{title}</h1>
  <div class="lh-dna">{dna}</div>
</div>
</body>
</html>"""


def render_tri_color(status: str, style: str = "html") -> str:
    """
    渲染三色状态
    status: green / yellow / red 或 通行/待审/熔断
    """
    status_map = {
        "green": "green", "通行": "green", "🟢": "green",
        "yellow": "yellow", "待审": "yellow", "🟡": "yellow",
        "red": "red", "熔断": "red", "🔴": "red",
    }
    state = status_map.get(status, status)
    info = TRI_COLOR_STATES.get(state, TRI_COLOR_STATES["green"])

    text = f"{info['emoji']} {info['label']}"
    if style == "html":
        return f'<span style="color:{info["hex"]};font-weight:bold" title="三色状态:{state}">{text}</span>'
    elif style == "md":
        return text
    return text


def main():
    print("=" * 60)
    print("龍魂渲染模块 | LongHun Rendering Engine")
    print(f"DNA: {DNA}")
    print("=" * 60)

    print("\n[1] 标签渲染")
    for style in ["html", "md", "text"]:
        print(f"  {style:5}: {render_tag('火·旺', style)}")

    print("\n[2] Emoji 渲染")
    for emoji in ["🔥", "✅", "🚨"]:
        print(f"  {emoji} -> {render_emoji(emoji, 'text')}")
        print(f"        {render_emoji(emoji, 'html')}")

    print("\n[3] CNSH 变量渲染")
    for var in ["$五行.金旺", "$状态.通行", "$八卦.乾"]:
        print(f"  {var} -> {render_cnsh_var(var, style='text')}")

    print("\n[4] 三色状态")
    for status in ["green", "yellow", "red"]:
        print(f"  {status}: {render_tri_color(status, 'text')}")

    print("\n[5] 页面头部（片段）")
    header = render_page_header("龍魂标签面板", DNA)
    print(header[:300] + "...")


if __name__ == "__main__":
    main()
