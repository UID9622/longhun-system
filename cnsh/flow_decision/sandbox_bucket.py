# -*- coding: utf-8 -*-
"""沙盒五桶分拣（简化）"""
from __future__ import annotations

from typing import Tuple


def pick_bucket(tricolor: str, privacy_mode: str, fuse: bool) -> str:
    if fuse or tricolor == "🔴":
        return "熔断桶"
    if privacy_mode == "sealed":
        return "封存桶"
    if privacy_mode == "burn":
        return "内部消化桶"
    if tricolor == "🟡":
        return "待审桶"
    return "常态归档桶"


def contribution_heat(level: str, dr: int) -> float:
    heat = 0.5 + (dr % 5) * 0.05
    if level.startswith("L0"):
        heat += 0.2
    return round(min(heat, 1.0), 3)
