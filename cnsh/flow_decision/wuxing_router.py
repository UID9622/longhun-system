# -*- coding: utf-8 -*-
"""dr → 五行（语义映射 P4）"""
from __future__ import annotations

DR_TO_ELEMENT = {
    1: "木",
    2: "木",
    3: "火",
    4: "火",
    5: "土",
    6: "金",
    7: "金",
    8: "水",
    9: "水",
    0: "土",
}


def element_for_dr(dr: int) -> str:
    return DR_TO_ELEMENT.get(dr % 10, "土")
