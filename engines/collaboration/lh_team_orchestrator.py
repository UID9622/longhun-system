#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · TeamOrchestrator v2.0（协作层别名）
DNA: #龍芯⚡️丙午·乙未·未时·☰乾-TEAM-ORCHESTRATOR-COLLAB-v2.0
创建者: 诸葛鑫（UID9622）

此文件为 engines/lh_team_orchestrator.py 的向下兼容别名。
所有功能已合入主引擎 v2.0。
"""

import sys
from pathlib import Path

SYSTEM_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_team_orchestrator import (
    # 数据模型
    RunStatus, SubTask, ConflictRecord, AfterActionReport, TeamRun,
    # 常量
    FIVE_TIER_MATRIX, FORMATION_MODES, FORMATION_ALIASES, TEAM_TEMPLATES,
    # 组件
    TaskDecomposer, ConflictDetector, AfterActionEngine,
    # 核心
    TeamOrchestrator,
    # 工具
    integration_test,
)

__all__ = [
    "RunStatus", "SubTask", "ConflictRecord", "AfterActionReport", "TeamRun",
    "FIVE_TIER_MATRIX", "FORMATION_MODES", "FORMATION_ALIASES", "TEAM_TEMPLATES",
    "TaskDecomposer", "ConflictDetector", "AfterActionEngine",
    "TeamOrchestrator",
    "integration_test",
]
