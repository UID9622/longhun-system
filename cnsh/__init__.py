#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂CNSH·流場決策核集成包
CNSH Flow Decision Core Integration Package

DNA: #龍芯⚡️2026-06-06-CNSH-INTEGRATION-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

責任: UID9622·不免責
"""

try:
    from .flow_decision import (
        FlowDecisionNode,
        quick_process,
        CNSHFlowDecisionCore,
        DigitalRootCalculator,
        IPARouteRegistry,
        PersonaCollaborationFramework,
        DNAChainTracer,
    )

    __version__ = "4.1"
    __all__ = [
        'FlowDecisionNode',
        'quick_process',
        'CNSHFlowDecisionCore',
        'DigitalRootCalculator',
        'IPARouteRegistry',
        'PersonaCollaborationFramework',
        'DNAChainTracer',
    ]

except ImportError as e:
    # 優雅降級：如果flow_decision尚未初始化
    import warnings
    warnings.warn(f"CNSH流場決策核導入失敗: {e}。系統仍可工作，但決策功能不可用。")
    __version__ = "4.1"
    __all__ = []
