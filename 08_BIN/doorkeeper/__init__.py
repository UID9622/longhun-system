#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂五行八门守护模块 v1.0（对齐修正版）
DNA: #龍芯⚡️2026-08-25-DOORKEEPER-INIT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

from .door_protocol import (
    五行, 八门, 三色,
    门机事件, 门机规则,
    获取门机规则, 获取五行, 判定门机
)
from .dna_tracer import DNATracer, dna
from .tricolor_audit import TricolorAudit, audit_engine
from .service_manager import ServiceManager, service_mgr
from .longhun_doorkeeper import LonghunDoorkeeper

__all__ = [
    "五行", "八门", "三色", "门机事件", "门机规则",
    "获取门机规则", "获取五行", "判定门机",
    "DNATracer", "dna",
    "TricolorAudit", "audit_engine",
    "ServiceManager", "service_mgr",
    "LonghunDoorkeeper",
]

__version__ = "1.0.0"
__dna__ = "#龍芯⚡️2026-08-25-DOORKEEPER-v1.0-UID9622"
