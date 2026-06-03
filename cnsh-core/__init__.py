#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂核心系统 / LongHun Core System (CNSH)                   ║
║                                                                  ║
║  P0核心模块·完整governance体系·8层架构                            ║
║                                                                  ║
║  DNA: #龍芯⚡️2026-06-03-CNSH-CORE-SYSTEM-v1.0                  ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  来源: 五个Notion核心宣言 + 数学公式算法核心                      ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from . import constitution
from . import identity
from . import permissions
from . import dna
from . import logging
from . import scheduler
from . import mathematics
from . import registry
from . import rules
from . import compiler
from .core_system_launcher import LongHunCoreSystem

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"

__all__ = [
    'constitution',
    'identity',
    'permissions',
    'dna',
    'logging',
    'scheduler',
    'mathematics',
    'registry',
    'rules',
    'compiler',
    'LongHunCoreSystem',
]
