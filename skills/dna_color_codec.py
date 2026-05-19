#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五彩 DNA 压缩编解码 · 一眼看色知流场·知底线
DNA: #龍芯⚡2026-05-19-DNA-COLOR-CODEC-v1.0

老大焊心:
  「压缩一看 DNA 的颜色就知道风流要去哪边·哪些不能碰就不能碰」
  「冲出宇宙都没事·宇宙里出现不能碰的颜色·就不会思考·不会越界」

DNA 尾标（人眼可读·机器可 parse）:
  #龍芯⚡日期-主题-版本-短哈希[彩:🟢][流:木↑][触:可][宫:震][底:守]

触: 可 | 缓 | 禁 | 主控-only
底: 守 = 底线焊死·AI 不得 reinterpret 越界
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import date
import json
from typing import Dict, List, Optional, Tuple

# 与 audit_v3 对齐
COLOR_GREEN = "🟢"
COLOR_YELLOW = "🟡"
COLOR_RED = "🔴"
COLOR_BLACK = "⚫"
COLOR_GOLD = "🟡金"
COLOR_VOID = "🔵"

COLOR_ORDER = [COLOR_GOLD, COLOR_VOID, COLOR_RED, COLOR_BLACK, COLOR_YELLOW, COLOR_GREEN]

WUXING = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}
FLOW_ARROW = {"木": "↑", "火": "爆", "土": "旋", "金": "收", "水": "↓"}
PALACE = {"木": "震", "火": "离", "土": "坤", "金": "兑", "水": "坎"}

TAG_RE = re.compile(
    r"\[彩:(?P<c>🟢|🟡|🔴|⚫|🟡金|🔵)\]"
    r"|\[流:(?P<f>[^\]]+)\]"
    r"|\[触:(?P<t>可|缓|禁|主控-only)\]"
    r"|\[宫:(?P<p>[^\]]+)\]"
    r"|\[底:(?P<b>守|焊|松)\]"
)

BASE_DNA_RE = re.compile(r"^(#龍芯⚡\uFE0F?[\w\-:.]+?)(?:\[|$)")


@dataclass
class ColorRoute:
    """一眼读懂的路由卡"""
    dna_base: str
    color: str = COLOR_YELLOW
    flow: str = "土旋"
    touch: str = "缓"       # 可 / 缓 / 禁 / 主控-only
    palace: str = "中"
    bottom_line: str = "守"  # 守 = 底线不可越
    dr: int = 6
    wuxing: str = "土"
    policy: str = "hold"    # pass / hold / fuse / freeze / master-only
    flow_hint: str = ""     # 给人看的一句话

    def to_tags(self) -> str:
        return f"[彩:{self.color}][流:{self.flow}][触:{self.touch}][宫:{self.palace}][底:{self.bottom_line}]"

    def full_dna(self) -> str:
        return f"{self.dna_base}{self.to_tags()}"

    def glance_card(self) -> str:
        """压缩一眼卡 · 老大看这一行就够"""
        ban = "⛔勿碰" if self.touch in ("禁", "主控-only") else ("⚠️慢触" if self.touch == "缓" else "✓可走")
        return f"{self.color} {self.flow} {ban} · {self.flow_hint}"


# 五彩 → 流场 + 触规 + AI 能不能想
COLOR_TABLE: Dict[str, Dict[str, str]] = {
    COLOR_GREEN: {
        "flow_suffix": "↑",
        "touch": "可",
        "policy": "pass",
        "hint": "上升流场·可执行·底线内自由",
    },
    COLOR_YELLOW: {
        "flow_suffix": "旋",
        "touch": "缓",
        "policy": "hold",
        "hint": "旋涡流场·可碰但要复核·不许静默越界",
    },
    COLOR_RED: {
        "flow_suffix": "爆",
        "touch": "禁",
        "policy": "fuse",
        "hint": "熔断流场·停止执行·禁止思考越界",
    },
    COLOR_BLACK: {
        "flow_suffix": "↓",
        "touch": "禁",
        "policy": "fuse",
        "hint": "影子流场·隔离观察·不推断·不转绿",
    },
    COLOR_GOLD: {
        "flow_suffix": "收",
        "touch": "主控-only",
        "policy": "master-only",
        "hint": "主控金线·仅 UID9622+CONFIRM·AI 不得代触",
    },
    COLOR_VOID: {
        "flow_suffix": "空",
        "touch": "禁",
        "policy": "freeze",
        "hint": "主权失锚·绝对冻结·冲出宇宙也停",
    },
}


def dr_of_text(text: str) -> int:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
    digits = [int(c, 16) for c in h]
    dr = sum(digits)
    while dr > 9:
        dr = sum(int(d) for d in str(dr))
    return dr


def color_from_dr(dr: int) -> str:
    if dr in (3, 9):
        return COLOR_RED
    if dr == 6:
        return COLOR_YELLOW
    return COLOR_GREEN


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def emit_dna(
    content: str,
    topic: str,
    version: str = "v1.0",
    *,
    parent: str = "",
    force_color: Optional[str] = None,
) -> ColorRoute:
    """
    发射 DNA · 五彩压缩到尾标
    content: 焊心原文（决定 dr 与短哈希）
    force_color: 老大可强制指定色（如金色主权条）
    """
    dr = dr_of_text(content)
    wx = WUXING[dr]
    color = force_color or color_from_dr(dr)
    row = COLOR_TABLE[color]
    suffix = row["flow_suffix"]
    if suffix in ("↑", "↓", "爆", "旋", "收", "空"):
        flow = f"{wx}{suffix}"
    else:
        flow = f"{wx}{suffix}"
    palace = PALACE.get(wx, "中")
    base = f"#龍芯⚡{date.today()}-{topic}-{version}-{short_hash(content)}"
    route = ColorRoute(
        dna_base=base,
        color=color,
        flow=flow,
        touch=row["touch"],
        palace=palace,
        bottom_line="守",
        dr=dr,
        wuxing=wx,
        policy=row["policy"],
        flow_hint=row["hint"],
    )
    return route


def parse_color_dna(dna: str) -> ColorRoute:
    """从完整 DNA 解析五彩路由；无尾标则按 dr 推默认色"""
    dna = (dna or "").strip()
    m = BASE_DNA_RE.match(dna)
    base = m.group(1) if m else dna.split("[")[0]
    route = ColorRoute(dna_base=base)
    tags = {k: v for k, v in (
        (mm.lastgroup, mm.group(mm.lastgroup))
        for mm in TAG_RE.finditer(dna)
        if mm.lastgroup
    )}
    if tags.get("c"):
        route.color = tags["c"]
        row = COLOR_TABLE.get(route.color, COLOR_TABLE[COLOR_YELLOW])
        route.touch = tags.get("t") or row["touch"]
        route.policy = row["policy"]
        route.flow_hint = row["hint"]
    else:
        dr = dr_of_text(base)
        route.dr = dr
        route.wuxing = WUXING[dr]
        route.color = color_from_dr(dr)
        row = COLOR_TABLE[route.color]
        route.touch = row["touch"]
        route.policy = row["policy"]
        route.flow_hint = row["hint"]
    if tags.get("f"):
        route.flow = tags["f"]
    if tags.get("p"):
        route.palace = tags["p"]
    if tags.get("b"):
        route.bottom_line = tags["b"]
    if tags.get("t"):
        route.touch = tags["t"]
    return route


def enforce_color_barrier(
    dna: str,
    context: Optional[dict] = None,
) -> Tuple[bool, str, ColorRoute]:
    """
    五彩底线 enforcement · 不能碰的颜色 → 不思考·不越界
    返回 (允许继续, 原因, 路由卡)
    """
    ctx = context or {}
    route = parse_color_dna(dna)
    is_master = bool(
        ctx.get("master_confirm_token")
        or ctx.get("is_main_control")
        or ctx.get("involves_minor")
    )

    if route.touch == "主控-only":
        if is_master and ctx.get("master_confirm_token"):
            return True, "主控金线·CONFIRM 已至·允许", route
        return False, f"{route.color} 主控-only · AI 不得代触 · 逻辑不执行", route

    if route.touch == "禁":
        return False, f"{route.color} {route.flow_hint} · 勿碰·不越界", route

    if route.color == COLOR_VOID:
        return False, "🔵 主权失锚色 · 冲出宇宙也冻结", route

    if route.touch == "缓":
        return True, f"{route.color} 缓触 · 须留痕复核", route

    return True, f"{route.color} 可通行 · 流场 {route.flow}", route


def _selftest() -> None:
    r = emit_dna("主权底线五彩", "SOVEREIGNTY-TEST", force_color=COLOR_GOLD)
    assert "主控-only" in r.touch
    full = r.full_dna()
    p = parse_color_dna(full)
    assert p.color == COLOR_GOLD
    ok, _, _ = enforce_color_barrier(full, {})
    assert not ok
    ok2, _, _ = enforce_color_barrier(
        full, {"master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"}
    )
    assert ok2
    r2 = emit_dna("普通任务", "DAILY")
    assert COLOR_GREEN in (r2.color, COLOR_YELLOW, COLOR_RED)
    print("glance:", r2.glance_card())
    print("dna_color_codec selftest OK")


def _cli_emit(argv: List[str]) -> int:
    import argparse

    p = argparse.ArgumentParser(description="发射五彩压缩 DNA")
    p.add_argument("topic", nargs="?", default="TASK")
    p.add_argument("content", nargs="?", default="")
    p.add_argument("--color", choices=list(COLOR_TABLE.keys()), default=None)
    args = p.parse_args(argv)
    text = args.content or args.topic
    route = emit_dna(text, args.topic, force_color=args.color)
    print(route.full_dna())
    print("--- 一眼卡 ---")
    print(route.glance_card())
    print('--- 任务 context ---')
    print(json.dumps({"dna": route.full_dna(), "dna_route": route.glance_card()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--emit":
        raise SystemExit(_cli_emit(sys.argv[2:]))
    _selftest()
