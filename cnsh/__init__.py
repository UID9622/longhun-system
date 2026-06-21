#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂CNSH·流場決策核集成包
CNSH Flow Decision Core Integration Package

DNA:#龍芯⚡️2026-06-06-CNSH-INTEGRATION-FILE1-v1.0
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

    from .sancai_sync import (
        SancaiSyncHub,
        IPAReceipt,
        ParticleInstruction,
        NeuralSignal,
        PalaceNode,
    )

    __version__ = "5.0"
    __all__ = [
        # v4.1 Flow Decision Core
        'FlowDecisionNode',
        'quick_process',
        'CNSHFlowDecisionCore',
        'DigitalRootCalculator',
        'IPARouteRegistry',
        'PersonaCollaborationFramework',
        'DNAChainTracer',
        # v1.0 Sancai Sync Hub
        'SancaiSyncHub',
        'IPAReceipt',
        'ParticleInstruction',
        'NeuralSignal',
        'PalaceNode',
    ]

except ImportError as e:
    # 優雅降級：如果flow_decision尚未初始化
    import warnings
    warnings.warn(f"CNSH流場決策核導入失敗: {e}。系統仍可工作，但決策功能不可用。")
    __version__ = "4.1"
    __all__ = []
