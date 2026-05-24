# -*- coding: utf-8 -*-
"""九宫派位（简化：按 element + action 关键字）"""
from __future__ import annotations

from typing import List

PALACE_BY_ELEMENT = {
    "木": "震宫",
    "火": "离宫",
    "土": "坤宫",
    "金": "兑宫",
    "水": "坎宫",
}


def route_palaces(element: str, trace: str, action: str) -> List[str]:
    base = [PALACE_BY_ELEMENT.get(element, "中宫")]
    al = action.lower()
    if "export" in al or "外发" in action:
        base.append("乾宫")
    if "seal" in trace.lower() or "封存" in action:
        base.append("艮宫")
    return base
