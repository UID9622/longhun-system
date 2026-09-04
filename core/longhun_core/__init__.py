#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂低算力内核 · longhun-core v1.0.0
治大国若烹小鲜。——《道德经》第60章

五模块内核：DNA追溯 | 三色审计 | 年轮链 | 数字根 | 流控
纯标准库·零依赖·断网可跑·10KB发行包

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-LOW-POWER-BENCH-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

__version__ = "1.0.0"
__author__ = "诸葛鑫（UID9622）"
__dna__ = "#龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-LOW-POWER-BENCH-UID9622"

from .dna_trace import DNAEngine, generate_dna, parse_dna, get_time_stamp
from .tricolor_audit import TricolorAudit, evaluate, audit_report
from .historian import YearRingChain, write_record, verify_chain
from .digital_root import DigitalRoot, compute_root, verify_root
from .flow_control import TokenBucket, FlowController, create_rate_limiter

__all__ = [
    # DNA
    "DNAEngine", "generate_dna", "parse_dna", "get_time_stamp",
    # Tricolor
    "TricolorAudit", "evaluate", "audit_report",
    # Historian
    "YearRingChain", "write_record", "verify_chain",
    # Digital Root
    "DigitalRoot", "compute_root", "verify_root",
    # Flow Control
    "TokenBucket", "FlowController", "create_rate_limiter",
]
