# -*- coding: utf-8 -*-
"""三才权重（兼容层 → cnsh.algorithms.sancai）"""
from __future__ import annotations

from cnsh.algorithms.sancai import SancaiWeights, normalize_sancai_weights

normalize_sancai = normalize_sancai_weights

__all__ = ["SancaiWeights", "normalize_sancai", "normalize_sancai_weights"]
