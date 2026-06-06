#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 日志·版本·追溯系统 模块
Longhun Logging · Versioning · Tracing Module

DNA: #龍芯⚡️2026-06-07-LOGGING-MODULE-INIT-v1.0
"""

import sys
from pathlib import Path

# Import the core logging module
# The .py file doesn't have underscores in the module name, so we import it directly
core_module_path = Path(__file__).parent / 'longhun-logging-versioning-tracing-core.py'

# Dynamically import the module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "longhun_logging_core",
    str(core_module_path)
)
longhun_logging_core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(longhun_logging_core)

LogLevel = longhun_logging_core.LogLevel
OperationType = longhun_logging_core.OperationType
ChangeType = longhun_logging_core.ChangeType
LogEntry = longhun_logging_core.LogEntry
VersionRecord = longhun_logging_core.VersionRecord
SystemSnapshot = longhun_logging_core.SystemSnapshot
LonghunLogger = longhun_logging_core.LonghunLogger

__all__ = [
    'LogLevel',
    'OperationType',
    'ChangeType',
    'LogEntry',
    'VersionRecord',
    'SystemSnapshot',
    'LonghunLogger',
]

__version__ = "1.0.0"
__author__ = "UID9622"
__dna__ = "#龍芯⚡️2026-06-07-LOGGING-MODULE-INIT-v1.0"
