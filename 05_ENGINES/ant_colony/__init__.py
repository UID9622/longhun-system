#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·LACA-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂蚁群引擎 v2.0 · Ant Colony Engine
基于 LACA 论文 v1.0 的完整工程实现，深度整合龍魂系统架构

DNA: #龍芯⚡️丙午·辛未·LACA-v2.0
融合点:
  - 不动点五级 L1-L5 ← cnsh_color_fixpoint.py / cnsh_sort_fixpoint.py
  - 16人格→五大蚁群种群映射
  - 四类信息素协议 ← 七色不动点色卡颜色映射
  - 涌现质量公式 E=D^α·I^β·C^γ·V^δ ← Braket量子引擎
  - 触角总线 ← 系统事件总线
  - DNA追溯 ← 现有DNA体系

架构设计: UID9622 | 诸葛鑫 (Lucky)
主权归属: 龍魂体系 · 君子协议开源宪章
"""

__version__ = "2.0.0"
__dna__ = "#龍芯⚡️丙午·辛未·LACA-v2.0-ENGINE"

from engine.ant_colony.antenna_signal import (
    AntennaSignal,
    PheromoneType,
    PayloadType,
    SignalExpiredError,
    SignalTamperedError,
    recruit_signal,
    alert_signal,
    trail_signal,
    aggregate_signal,
)

from engine.ant_colony.pheromone_system import (
    PheromoneSystem,
    PheromoneTrail,
    calculate_recruit_priority,
    calculate_alert_escalation,
)

from engine.ant_colony.antenna_bus import (
    AntennaBus,
    ModuleRegistration,
    create_populated_bus,
)

from engine.ant_colony.fixed_point_bridge import (
    FixedPointBridge,
    ColorPheromoneMapper,
    EmergenceCalculator,
    WuxingPheromoneCoupling,
    FixedPointLevel,
)

from engine.ant_colony.runtime import (
    AntColonyRuntime,
    ColonyState,
    get_runtime,
    stop_runtime,
    ant_colony_pre_audit_hook,
    ant_colony_on_complete_hook,
    ant_colony_lifecycle_hook,
)

from engine.ant_colony.engine_bridge import (
    AntColonyEngineBridge,
    BridgeDecision,
    BridgeAudit,
    get_bridge,
)

__all__ = [
    "AntennaSignal",
    "PheromoneType",
    "PayloadType",
    "SignalExpiredError",
    "SignalTamperedError",
    "recruit_signal",
    "alert_signal",
    "trail_signal",
    "aggregate_signal",
    "PheromoneSystem",
    "PheromoneTrail",
    "calculate_recruit_priority",
    "calculate_alert_escalation",
    "AntennaBus",
    "ModuleRegistration",
    "create_populated_bus",
    "FixedPointBridge",
    "ColorPheromoneMapper",
    "EmergenceCalculator",
    "WuxingPheromoneCoupling",
    "FixedPointLevel",
    "AntColonyRuntime",
    "ColonyState",
    "get_runtime",
    "stop_runtime",
    "ant_colony_pre_audit_hook",
    "ant_colony_on_complete_hook",
    "ant_colony_lifecycle_hook",
    "AntColonyEngineBridge",
    "BridgeDecision",
    "BridgeAudit",
    "get_bridge",
]
