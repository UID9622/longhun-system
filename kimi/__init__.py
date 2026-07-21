#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 × Kimi 集成包

DNA:#龍芯⚡️2026-06-08-KIMI-PACKAGE-v1.0
"""

from .kimi_client import KimiClient
from .kimi_integration import KimiIntegration, IntegrationMode, CircuitBreaker
from .kimi_gateway import KimiGateway, KimiGatewayLite

__all__ = [
    "KimiClient",
    "KimiIntegration",
    "IntegrationMode",
    "CircuitBreaker",
    "KimiGateway",
    "KimiGatewayLite",
]

__version__ = "1.0.0"
__author__ = "龍魂系统 - UID9622"
