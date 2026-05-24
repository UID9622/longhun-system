# -*- coding: utf-8 -*-
"""五行生克（简化：对父元素）"""
from __future__ import annotations

SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def relation_to_parent(child_el: str, parent_el: str) -> str:
    if parent_el not in SHENG:
        return "无"
    if SHENG.get(parent_el) == child_el:
        return "子受生于父"
    if KE.get(parent_el) == child_el:
        return "父克子"
    if SHENG.get(child_el) == parent_el:
        return "子生父"
    if KE.get(child_el) == parent_el:
        return "子克父"
    return "比劫/平"
