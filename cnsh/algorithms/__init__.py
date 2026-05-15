# -*- coding: utf-8 -*-
"""龍魂算法公式库（从 longhun-algorithms-cnsh-v1.0.md 搬回可执行层）"""
from cnsh.algorithms.sancai import (
    CANONICAL_SOURCE,
    SancaiDecision,
    SancaiWeights,
    compute_sancai_decision,
    normalize_sancai_weights,
    sancai_complete_check,
    sancai_flow_theta,
)

__all__ = [
    "CANONICAL_SOURCE",
    "SancaiDecision",
    "SancaiWeights",
    "compute_sancai_decision",
    "normalize_sancai_weights",
    "sancai_complete_check",
    "sancai_flow_theta",
]
