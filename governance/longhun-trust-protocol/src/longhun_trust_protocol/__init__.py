#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
longhun-trust-protocol
龍魂君子协议 · 诚信评级与违约清算算法
DNA: #龍芯⚡️2026-06-26-LONGHUN-TRUST-PROTOCOL-v1.0
"""

__version__ = "1.0.0"
__dna__ = "#龍芯⚡️2026-06-26-LONGHUN-TRUST-PROTOCOL-v1.0"
__gpg__ = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

from .api import TrustProtocol
from .core import EventType, Grade, SlaughterLevel, TrustEvent, TrustProfile
from .storage import TrustStore

__all__ = [
    "__version__",
    "__dna__",
    "__gpg__",
    "TrustProtocol",
    "TrustProfile",
    "TrustEvent",
    "TrustStore",
    "Grade",
    "SlaughterLevel",
    "EventType",
]
