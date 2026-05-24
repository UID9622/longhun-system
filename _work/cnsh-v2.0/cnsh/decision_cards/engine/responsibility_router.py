# -*- coding: utf-8 -*-
"""责任卡路由：轻量 / 完整。"""
from __future__ import annotations

FULL_KEYWORDS = (
    "主控",
    "CONFIRM",
    "SEAL",
    "GPG",
    "不动点",
    "登锚",
    "规则库",
    "CNSH",
    "本机",
    "删除",
    "覆盖",
    "发布",
    "版权",
    "DNA",
    "ROOT_CARD",
    "重大决策",
    "师承",
    "曾仕强",
    "易经",
    "道德经",
    "P0",
    "不可逆",
    "落档",
    "收口",
    "定盘",
)


def route_card_type(text: str, force: str = "") -> str:
    if force in ("light", "full"):
        return force
    t = text or ""
    for kw in FULL_KEYWORDS:
        if kw in t:
            return "full"
    return "light"


def decision_level(text: str, card_type: str) -> str:
    t = text or ""
    if any(k in t for k in ("主控", "CONFIRM", "SEAL", "GPG", "P0")):
        return "L0"
    if any(
        k in t
        for k in ("CNSH", "本机", "脚本", "删除", "覆盖", "工程", "命令", "网关")
    ):
        return "L1"
    if any(k in t for k in ("文档", "模板", "页面", "Notion")):
        return "L2"
    if card_type == "full":
        return "L1"
    return "L3"
