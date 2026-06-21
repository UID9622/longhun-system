#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1295-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: __init__.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧬 龍魂操作日記引擎 v1.0 · 本地DNA系統

DNA:#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

核心模組:
  - operation_ledger: append-only 操作日記 + SHA-256鏈式驗證
  - dna_particle_generator: DNA粒子生成 + 身份証體系
  - habit_fingerprint_manager: F8習慣提取 + 基線建立 + SI匹配
  - cross_device_identifier: 跨設備識別 + 設備信任 + 自動同步

完整流程:
  1. 操作發生 → operation_ledger.append_operation()
  2. DNA粒子生成 → dna_particle_generator.generate_from_record()
  3. 習慣自動提取 → habit_fingerprint_manager.extract_habit_features()
  4. 跨設備識別 → cross_device_identifier.identify_user()
  5. 自動同步決策 → auto_sync_decision()

結果: 任何設備都知道是我 · 習慣認人 · DNA認話
"""

__version__ = "1.0"
__author__ = "UID9622"
__dna__ = "#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0"

import sys
from pathlib import Path

# Add parent directory to path to import core modules
_parent_dir = str(Path(__file__).parent.parent)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from core.operation_ledger import OperationLedger
from core.dna_particle_generator import DNAParticleGenerator
from core.habit_fingerprint_manager import HabitFingerprintManager
from core.cross_device_identifier import CrossDeviceIdentifier
from core.sync_engine import SyncEngine
from core.multisig_gate import MultisigGate
from core.query_tool import QueryTool

__all__ = [
    "OperationLedger",
    "DNAParticleGenerator",
    "HabitFingerprintManager",
    "CrossDeviceIdentifier",
    "SyncEngine",
    "MultisigGate",
    "QueryTool"
]
