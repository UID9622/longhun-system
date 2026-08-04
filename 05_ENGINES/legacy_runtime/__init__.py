#!/usr/bin/env python3
"""
🐉 龍魂统一引擎 · 内核包
=========================
一个引擎，多个出口。飞书/微信/Web/Telegram 共用一个内核。

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-ENGINE-CORE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

from .engine_core import LonghunEngine
from .message import Message, Response
from .registry import CapabilityRegistry

__all__ = ["LonghunEngine", "Message", "Response", "CapabilityRegistry"]
__version__ = "1.0.0"
