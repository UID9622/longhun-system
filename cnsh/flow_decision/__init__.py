#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场决策核 v4.1·包入口
CNSH Flow Decision Core v4.1 - Package Entry

DNA: #龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1-INIT
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

from .schemas import (
    FlowDecisionNode, PersonaEnum, BucketEnum, StatusEnum,
    AuditColorEnum, WuxingEnum, VisibilityEnum, TraceModeEnum,
    LevelEnum, PalaceEnum
)
from .cnsh_flow_decision_core import CNSHFlowDecisionCore, quick_process
from .digital_root import DigitalRootCalculator, quick_dr
from .ipa_route_registry import IPARouteRegistry, get_ipa_chain_order
from .persona_collaboration import PersonaCollaborationFramework, HARDLAW_PERSONA_MAP
from .dna_chain_tracer import DNAChainTracer, DNATagPolicyValidator

__version__ = "4.1"
__author__ = "UID9622"

__all__ = [
    "FlowDecisionNode",
    "CNSHFlowDecisionCore",
    "quick_process",
    "DigitalRootCalculator",
    "quick_dr",
    "IPARouteRegistry",
    "get_ipa_chain_order",
    "PersonaCollaborationFramework",
    "HARDLAW_PERSONA_MAP",
    "DNAChainTracer",
    "DNATagPolicyValidator",
    "PersonaEnum",
    "BucketEnum",
    "StatusEnum",
    "AuditColorEnum",
    "WuxingEnum",
    "VisibilityEnum",
    "TraceModeEnum",
    "LevelEnum",
    "PalaceEnum",
]
