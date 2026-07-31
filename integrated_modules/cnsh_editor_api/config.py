# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH Editor API ·  tier 配置
DNA: #龍芯⚡️2026-07-04-CNSH-API-CONFIG-v1.0
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TierLimits:
    """单个 tier 的限制"""
    name: str
    max_source_chars: int
    max_execution_time_ms: int
    allow_file_io: bool
    allow_network: bool
    allow_advanced_features: bool
    description: str


# 默认免费 tier（本地/轻量）
FREE_TIER = TierLimits(
    name="free",
    max_source_chars=2000,
    max_execution_time_ms=3000,
    allow_file_io=False,
    allow_network=False,
    allow_advanced_features=False,
    description="本地免费版：基础语法渲染与短代码执行",
)

# 付费 tier（华为云/鲲鹏完整版）
PAID_TIER = TierLimits(
    name="paid",
    max_source_chars=50000,
    max_execution_time_ms=30000,
    allow_file_io=True,
    allow_network=True,
    allow_advanced_features=True,
    description="龍魂云完整版：文件 IO、网络、高级语法、华为鲲鹏加速",
)

TIER_MAP: Dict[str, TierLimits] = {
    "free": FREE_TIER,
    "paid": PAID_TIER,
}


def get_current_tier() -> TierLimits:
    """根据环境变量 CNSH_API_TIER 返回当前 tier"""
    tier_name = os.environ.get("CNSH_API_TIER", "free").lower()
    return TIER_MAP.get(tier_name, FREE_TIER)


def is_paid() -> bool:
    return get_current_tier().name == "paid"
