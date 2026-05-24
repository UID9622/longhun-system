# -*- coding: utf-8 -*-
"""三色闸：结合 dr、L0、auto_execute（§6.1 7-9）"""
from __future__ import annotations


def audit_color(dr: int, auto_execute: bool, level: str) -> str:
    if level.startswith("L0"):
        return "🟡"
    if dr in (3, 9) and auto_execute:
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


def map_result_status(color: str) -> str:
    if color == "🔴":
        return "fuse"
    if color == "🟡":
        return "hold"
    return "enter"
