#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 流场融合桥接引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·乙巳·壬申·午时·䷀乾-FLOW-FUSION-BRIDGE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

设计理念：
  流场是本系统唯一的物理-信息可视化观测层。
  所有可观测性引擎（审计/健康/熔断/异常/观察）通过本桥接层，
  将系统状态变化实时映射为流场扰动（源/力/涡旋/压力/冲击波）。

功能：
  1. 事件总线 — 接收所有引擎的状态事件（POST /event）
  2. 翻译层 — 引擎事件 → 流场注入类型 + 位置 + 强度
  3. 注入层 — 推送到流场引擎 :8776/inject
  4. 融合仪表盘 — 统一展示流场 + 引擎状态（/）
  5. 历史追踪 — 融合注入记录持久化
  6. 融合审计 — 谁注入·为什么·流向哪里

融合映射矩阵：
  ┌────────────────┬────────────┬──────────┬──────────────┐
  │ 源引擎         │ 事件       │ 流场注入  │ 物理含义      │
  ├────────────────┼────────────┼──────────┼──────────────┤
  │ 自我审计 🔴   │ DNA固化    │ vortex   │ 内旋阻力·僵化 │
  │ 自我审计 🟡   │ 风险预警   │ force    │ 正应力·待缓解 │
  │ 自我审计 🟢   │ 全绿通过   │ source   │ 正能量源      │
  │ 健康检查 异常  │ score<75   │ pressure │ 系统压力      │
  │ 健康检查 恢复  │ score恢复  │ anti-force│ 压力释放     │
  │ 熔断   触发    │ trip       │ shockwave│ 冲击波        │
  │ 熔断   恢复    │ reset      │ source   │ 系统复位      │
  │ 异常检测 异常  │ 资源异常   │ turbulence│ 湍流扰动     │
  │ 主动观察 变更  │ 文件/事件  │ source   │ 新信息流入    │
  │ 三色审计 🔴   │ 红线       │ vortex+  │ 强涡旋·危险   │
  │ 资源监控 高负载│ CPU/内存   │ pressure │ 资源压力      │
  └────────────────┴────────────┴──────────┴──────────────┘

用法：
  python3 bin/lh_flow_fusion_bridge.py                  # 启动桥接服务 (8777)
  python3 bin/lh_flow_fusion_bridge.py --port 8777      # 指定端口
  python3 bin/lh_flow_fusion_bridge.py --no-flow        # 不连接流场 (只记录)
  python3 bin/lh_flow_fusion_bridge.py --status         # 查看融合状态
  python3 bin/lh_flow_fusion_bridge.py --inject test    # 测试注入
  python3 bin/lh_flow_fusion_bridge.py --dashboard-only # 只启动仪表盘

API:
  POST /event       — 引擎上报事件
  GET  /state       — 融合桥接状态
  GET  /history     — 注入历史
  GET  /flow-status — 流场引擎连通状态
  GET  /            — 融合仪表盘
"""

import os
import sys
import json
import time
import hashlib
import datetime
import argparse
import sqlite3
import threading
import http.server
import urllib.request
import urllib.error
import socketserver
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from collections import deque, defaultdict
from enum import Enum
import math

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_CORE = "丙午·乙巳·壬申·午时·☰乾-FLOW-FUSION-BRIDGE-v1.0"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "flow_fusion.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 流场引擎地址
FLOW_ENGINE_URL = "http://127.0.0.1:8776"

# ============================================================
# 事件类型枚举
# ============================================================

class EventSource(str, Enum):
    SELF_AUDIT = "self_audit"       # 自我审计引擎
    HEALTH_CHECK = "health_check"   # 健康检查
    HEALTH_ALERT = "health_alert"   # 健康告警守护
    FUSE_CONTROL = "fuse_control"   # 熔断控制
    ANOMALY_DETECT = "anomaly_detect"  # 异常检测
    ACTIVE_OBSERVE = "active_observe"  # 主动观察
    THREE_COLOR_AUDIT = "three_color_audit"  # 三色审计
    RESOURCE_MONITOR = "resource_monitor"    # 资源监控
    ANTI_TAMPER = "anti_tamper"     # 防篡改
    VULN_DETECT = "vuln_detect"     # 漏洞检测
    CIRCUIT_BREAKER = "circuit_breaker"  # 四级熔断
    AUTO_HEAL = "auto_heal"         # 自愈扫描
    SYSTEM = "system"               # 系统级事件
    KNOWLEDGE_GAIN = "knowledge_gain"   # 知识获取
    PERSONA_SWITCH = "persona_switch"   # 人格切换
    TASK_COMPLETE = "task_complete"     # 任务完成
    MISTAKE_LEDGER = "mistake_ledger"   # 记错本
    DNA_VERIFY = "dna_verify"           # DNA验证

class FlowInjectionType(str, Enum):
    FORCE = "force"         # 定向力·推拉
    SOURCE = "source"       # 源·新增物质/能量
    VORTEX = "vortex"       # 涡旋·旋转/内卷
    PRESSURE = "pressure"   # 压力·压缩/负荷
    SHOCKWAVE = "shockwave" # 冲击波·突发事件
    TURBULENCE = "turbulence"  # 湍流·局部混乱
    ANTI_FORCE = "anti_force"  # 反力·恢复/释放

# ============================================================
# 翻译矩阵：引擎事件 → 流场注入
# ============================================================

# 流场坐标系定义（归一化 0-1）
POSITIONS = {
    "center":       (0.5, 0.5),   # 中心·内核
    "top":          (0.5, 0.05),  # 顶部·云端/外部
    "bottom":       (0.5, 0.95),  # 底部·基础设施
    "left":         (0.05, 0.5),  # 左·历史/过去
    "right":        (0.95, 0.5),  # 右·未来/演进
    "top_left":     (0.15, 0.15),
    "top_right":    (0.85, 0.15),
    "bottom_left":  (0.15, 0.85),
    "bottom_right": (0.85, 0.85),
    "mid_left":     (0.25, 0.5),
    "mid_right":    (0.75, 0.5),
}

# 翻译矩阵核心
TRANSLATION_MATRIX = {
    # ─── 自我审计 ───
    (EventSource.SELF_AUDIT, "dna_risk_high"):     (FlowInjectionType.VORTEX, "center", 0.85),
    (EventSource.SELF_AUDIT, "dna_risk_medium"):   (FlowInjectionType.FORCE, "center", 0.50),
    (EventSource.SELF_AUDIT, "dna_risk_low"):      (FlowInjectionType.SOURCE, "mid_right", 0.30),
    (EventSource.SELF_AUDIT, "p0_risk_high"):      (FlowInjectionType.VORTEX, "center", 0.90),
    (EventSource.SELF_AUDIT, "p0_risk_medium"):    (FlowInjectionType.FORCE, "top", 0.55),
    (EventSource.SELF_AUDIT, "p0_risk_low"):       (FlowInjectionType.SOURCE, "mid_right", 0.25),
    (EventSource.SELF_AUDIT, "protocol_risk_high"):(FlowInjectionType.TURBULENCE, "bottom_right", 0.80),
    (EventSource.SELF_AUDIT, "protocol_risk_medium"):(FlowInjectionType.FORCE, "bottom", 0.50),
    (EventSource.SELF_AUDIT, "protocol_risk_low"): (FlowInjectionType.SOURCE, "bottom_right", 0.30),

    # ─── 健康检查 ───
    (EventSource.HEALTH_CHECK, "critical"):        (FlowInjectionType.PRESSURE, "center", 0.95),
    (EventSource.HEALTH_CHECK, "warning"):         (FlowInjectionType.PRESSURE, "top", 0.65),
    (EventSource.HEALTH_CHECK, "ok"):              (FlowInjectionType.SOURCE, "mid_right", 0.20),
    (EventSource.HEALTH_CHECK, "recovered"):       (FlowInjectionType.ANTI_FORCE, "center", 0.60),

    # ─── 健康告警守护 ───
    (EventSource.HEALTH_ALERT, "p0_alert"):        (FlowInjectionType.SHOCKWAVE, "center", 0.95),
    (EventSource.HEALTH_ALERT, "p1_alert"):        (FlowInjectionType.PRESSURE, "center", 0.75),
    (EventSource.HEALTH_ALERT, "warning"):         (FlowInjectionType.FORCE, "top", 0.50),

    # ─── 熔断控制 ───
    (EventSource.FUSE_CONTROL, "trip"):            (FlowInjectionType.SHOCKWAVE, "center", 1.0),
    (EventSource.FUSE_CONTROL, "soft_block"):      (FlowInjectionType.PRESSURE, "center", 0.70),
    (EventSource.FUSE_CONTROL, "reset"):           (FlowInjectionType.SOURCE, "center", 0.50),
    (EventSource.FUSE_CONTROL, "block_domain"):    (FlowInjectionType.FORCE, "top", 0.60),

    # ─── 异常检测 ───
    (EventSource.ANOMALY_DETECT, "cpu_high"):      (FlowInjectionType.TURBULENCE, "bottom_left", 0.60),
    (EventSource.ANOMALY_DETECT, "mem_high"):      (FlowInjectionType.TURBULENCE, "bottom", 0.60),
    (EventSource.ANOMALY_DETECT, "disk_high"):     (FlowInjectionType.TURBULENCE, "bottom_right", 0.60),
    (EventSource.ANOMALY_DETECT, "code_anomaly"):  (FlowInjectionType.VORTEX, "mid_left", 0.55),
    (EventSource.ANOMALY_DETECT, "behavior_anomaly"):(FlowInjectionType.SHOCKWAVE, "center", 0.75),

    # ─── 主动观察 ───
    (EventSource.ACTIVE_OBSERVE, "file_change"):   (FlowInjectionType.SOURCE, "mid_left", 0.25),
    (EventSource.ACTIVE_OBSERVE, "network_change"):(FlowInjectionType.SOURCE, "top", 0.30),
    (EventSource.ACTIVE_OBSERVE, "process_event"): (FlowInjectionType.SOURCE, "bottom", 0.25),

    # ─── 三色审计 ───
    (EventSource.THREE_COLOR_AUDIT, "red"):        (FlowInjectionType.VORTEX, "center", 0.90),
    (EventSource.THREE_COLOR_AUDIT, "yellow"):     (FlowInjectionType.FORCE, "mid_right", 0.45),
    (EventSource.THREE_COLOR_AUDIT, "green"):      (FlowInjectionType.SOURCE, "right", 0.20),

    # ─── 资源监控 ───
    (EventSource.RESOURCE_MONITOR, "cpu_high"):    (FlowInjectionType.PRESSURE, "bottom_left", 0.65),
    (EventSource.RESOURCE_MONITOR, "mem_high"):    (FlowInjectionType.PRESSURE, "bottom", 0.65),
    (EventSource.RESOURCE_MONITOR, "disk_high"):   (FlowInjectionType.PRESSURE, "bottom_right", 0.60),

    # ─── 熔断(四级) ───
    (EventSource.CIRCUIT_BREAKER, "l0_trigger"):   (FlowInjectionType.SHOCKWAVE, "center", 1.0),
    (EventSource.CIRCUIT_BREAKER, "l1_trigger"):   (FlowInjectionType.PRESSURE, "center", 0.85),
    (EventSource.CIRCUIT_BREAKER, "l2_trigger"):   (FlowInjectionType.FORCE, "center", 0.60),
    (EventSource.CIRCUIT_BREAKER, "l3_trigger"):   (FlowInjectionType.FORCE, "top", 0.40),

    # ─── 自愈扫描 ───
    (EventSource.AUTO_HEAL, "service_down"):       (FlowInjectionType.TURBULENCE, "bottom", 0.70),
    (EventSource.AUTO_HEAL, "service_restart"):    (FlowInjectionType.SOURCE, "bottom", 0.40),
    (EventSource.AUTO_HEAL, "health_report"):      (FlowInjectionType.SOURCE, "mid_right", 0.20),

    # ─── 知识获取 ───
    (EventSource.KNOWLEDGE_GAIN, "new_knowledge"): (FlowInjectionType.SOURCE, "left", 0.35),
    (EventSource.KNOWLEDGE_GAIN, "learned"):       (FlowInjectionType.SOURCE, "top_left", 0.30),
    (EventSource.KNOWLEDGE_GAIN, "discovered"):    (FlowInjectionType.VORTEX, "mid_left", 0.40),

    # ─── 人格切换 ───
    (EventSource.PERSONA_SWITCH, "activate"):      (FlowInjectionType.SOURCE, "mid_right", 0.35),
    (EventSource.PERSONA_SWITCH, "deactivate"):    (FlowInjectionType.ANTI_FORCE, "mid_right", 0.30),
    (EventSource.PERSONA_SWITCH, "conflict"):      (FlowInjectionType.VORTEX, "center", 0.55),

    # ─── 任务完成 ───
    (EventSource.TASK_COMPLETE, "success"):        (FlowInjectionType.ANTI_FORCE, "right", 0.35),
    (EventSource.TASK_COMPLETE, "partial"):        (FlowInjectionType.SOURCE, "bottom_right", 0.25),
    (EventSource.TASK_COMPLETE, "failed"):         (FlowInjectionType.TURBULENCE, "bottom_right", 0.50),

    # ─── 记错本 ───
    (EventSource.MISTAKE_LEDGER, "recorded"):      (FlowInjectionType.SOURCE, "mid_left", 0.30),
    (EventSource.MISTAKE_LEDGER, "reviewed"):      (FlowInjectionType.FORCE, "mid_left", 0.40),
    (EventSource.MISTAKE_LEDGER, "fixed"):         (FlowInjectionType.ANTI_FORCE, "mid_left", 0.45),

    # ─── DNA验证 ───
    (EventSource.DNA_VERIFY, "pass"):              (FlowInjectionType.SOURCE, "center", 0.25),
    (EventSource.DNA_VERIFY, "fail"):              (FlowInjectionType.VORTEX, "center", 0.80),
    (EventSource.DNA_VERIFY, "renew"):             (FlowInjectionType.FORCE, "center", 0.50),

    # ─── 搜索引擎(Mac:9631 · 鲲鹏:9631) ───
    ("search_engine", "search_executed"):          (FlowInjectionType.SOURCE, "top_right", 0.25),
    ("search_engine", "cache_hit"):                (FlowInjectionType.SOURCE, "top_right", 0.15),
    ("search_engine", "cache_miss"):               (FlowInjectionType.FORCE, "top_right", 0.20),

    # ─── 量子卦象API(Mac:9000 · 鲲鹏:9000) ───
    ("quantum_api", "hexagram_computed"):          (FlowInjectionType.VORTEX, "top", 0.40),
    ("quantum_api", "hamming_calculated"):         (FlowInjectionType.SOURCE, "top", 0.35),

    # ─── 思维管线(Mac:9630 · 鲲鹏:9630) ───
    ("think_pipeline", "decision_made"):           (FlowInjectionType.FORCE, "mid_right", 0.30),
    ("think_pipeline", "card_recorded"):           (FlowInjectionType.SOURCE, "mid_right", 0.20),

    # ─── Notion对话桥(Mac:8779) ───
    ("notion_bridge", "sync_complete"):            (FlowInjectionType.SOURCE, "left", 0.25),
    ("notion_bridge", "rag_queried"):              (FlowInjectionType.FORCE, "left", 0.20),

    # ─── 天线八闸(Mac:8769 · 鲲鹏:8769) ───
    ("antenna_8gate", "route_executed"):           (FlowInjectionType.SOURCE, "top", 0.30),
    ("antenna_8gate", "ant_colony_pulse"):         (FlowInjectionType.VORTEX, "top", 0.45),
    ("antenna_8gate", "bagua_routed"):             (FlowInjectionType.FORCE, "top_left", 0.35),

    # ─── 知识中枢(Mac:8766 · 鲲鹏:8766) ───
    ("knowledge_harvester", "harvested"):          (FlowInjectionType.SOURCE, "left", 0.30),
    ("knowledge_harvester", "indexed"):            (FlowInjectionType.SOURCE, "top_left", 0.25),
    ("knowledge_harvester", "quality_filtered"):   (FlowInjectionType.FORCE, "left", 0.20),

    # ─── 观澜API(Mac:8770) ───
    ("guanlan_api", "observing"):                  (FlowInjectionType.SOURCE, "top", 0.20),
    ("guanlan_api", "ripple_detected"):            (FlowInjectionType.VORTEX, "top", 0.35),

    # ─── 安全网关(Mac:9623 · 鲲鹏:9623) ───
    ("security_gateway", "request_blocked"):       (FlowInjectionType.SHOCKWAVE, "center", 0.65),
    ("security_gateway", "request_passed"):        (FlowInjectionType.SOURCE, "mid_right", 0.15),
    ("security_gateway", "threat_detected"):       (FlowInjectionType.VORTEX, "center", 0.75),

    # ─── 后端主服务(Mac:9622 · 鲲鹏:9622) ───
    ("backend_main", "request_served"):            (FlowInjectionType.SOURCE, "bottom", 0.15),
    ("backend_main", "api_slow"):                  (FlowInjectionType.FORCE, "bottom", 0.40),

    # ─── 对话伦理服务(Mac:9635) ───
    ("dialogue_ethics", "dialogue_complete"):      (FlowInjectionType.SOURCE, "mid_right", 0.20),
    ("dialogue_ethics", "ethics_check_pass"):      (FlowInjectionType.SOURCE, "right", 0.15),
    ("dialogue_ethics", "ethics_check_block"):     (FlowInjectionType.SHOCKWAVE, "center", 0.70),

    # ─── 统一记忆(鲲鹏:8773) ───
    ("memory_api", "memory_write"):                (FlowInjectionType.SOURCE, "left", 0.25),
    ("memory_api", "memory_read"):                 (FlowInjectionType.SOURCE, "left", 0.15),
    ("memory_api", "memory_conflict"):             (FlowInjectionType.VORTEX, "left", 0.50),

    # ─── 视频索引(鲲鹏:8788) ───
    ("video_index", "indexed"):                    (FlowInjectionType.SOURCE, "bottom_left", 0.25),
    ("video_index", "thumbnail_generated"):        (FlowInjectionType.SOURCE, "bottom_left", 0.20),

    # ─── 门户API(鲲鹏:8789) ───
    ("portal_api", "api_hit"):                     (FlowInjectionType.SOURCE, "bottom", 0.15),
    ("portal_api", "kb_browsed"):                  (FlowInjectionType.SOURCE, "bottom_left", 0.20),

    # ─── DeepSeek执行器(鲲鹏:9453) ───
    ("deepseek_executor", "model_called"):         (FlowInjectionType.FORCE, "top_right", 0.35),
    ("deepseek_executor", "streaming"):            (FlowInjectionType.SOURCE, "top_right", 0.25),
    ("deepseek_executor", "rate_limited"):         (FlowInjectionType.PRESSURE, "top_right", 0.50),

    # ─── Ollama本地模型(双端:11434) ───
    ("ollama", "model_inference"):                 (FlowInjectionType.FORCE, "bottom_left", 0.30),
    ("ollama", "model_loaded"):                    (FlowInjectionType.SOURCE, "bottom_left", 0.20),

    # ─── 流场引擎自身(鲲鹏:8776) ───
    ("flow_engine", "frame_tick"):                 (FlowInjectionType.SOURCE, "center", 0.10),
    ("flow_engine", "anomaly_generated"):          (FlowInjectionType.VORTEX, "center", 0.55),
    ("flow_engine", "vortex_detected"):            (FlowInjectionType.VORTEX, "mid_left", 0.45),

    # ─── 保险柜(鲲鹏:8780) ───
    ("vault", "key_access"):                       (FlowInjectionType.FORCE, "center", 0.40),
    ("vault", "audit_log"):                        (FlowInjectionType.SOURCE, "center", 0.20),

    # ─── 记忆同步(鲲鹏:8787) ───
    ("memory_sync", "synced"):                     (FlowInjectionType.SOURCE, "left", 0.25),
    ("memory_sync", "conflict_resolved"):          (FlowInjectionType.ANTI_FORCE, "left", 0.35),

    # ─── 如意API(鲲鹏:8778) ───
    ("ruyi_api", "orchestrate"):                   (FlowInjectionType.FORCE, "top", 0.30),
    ("ruyi_api", "skill_dispatched"):              (FlowInjectionType.SOURCE, "top", 0.25),

    # ─── 纳米视觉(鲲鹏:9625) ───
    ("nano_vision", "detected"):                   (FlowInjectionType.SOURCE, "top_right", 0.20),

    # ─── 共生体矩阵(鲲鹏:9627) ───
    ("symbiote_matrix", "pulse"):                  (FlowInjectionType.VORTEX, "bottom", 0.40),

    # ─── 健康API(鲲鹏:9636) ───
    ("health_api", "check"):                       (FlowInjectionType.SOURCE, "mid_right", 0.15),

    # ─── 路径规划(鲲鹏:9650/9651) ───
    ("pathfinder", "route_found"):                 (FlowInjectionType.SOURCE, "right", 0.25),
    ("pathfinder", "dead_end"):                    (FlowInjectionType.TURBULENCE, "right", 0.40),

    # ─── 激活API(鲲鹏:9656/9657) ───
    ("activation_api", "activated"):               (FlowInjectionType.SOURCE, "bottom_left", 0.25),

    # ─── 裁判API(鲲鹏:9666) ───
    ("judge_api", "verdict"):                      (FlowInjectionType.FORCE, "center", 0.35),

    # ─── 审计即服务(鲲鹏:8771) ───
    ("audit_service", "audit_pass"):               (FlowInjectionType.SOURCE, "mid_right", 0.20),
    ("audit_service", "audit_block"):              (FlowInjectionType.SHOCKWAVE, "center", 0.70),
    ("audit_service", "gate_check"):               (FlowInjectionType.FORCE, "mid_right", 0.35),

    # ─── 通用集成测试 ───
    ("integration", "health_check"):               (FlowInjectionType.SOURCE, "center", 0.15),
    ("integration", "full_sync"):                  (FlowInjectionType.FORCE, "center", 0.40),
}

# ============================================================
# 数据库
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fusion_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT DEFAULT 'info',
            data TEXT,
            flow_injection_type TEXT,
            flow_position TEXT,
            flow_strength REAL,
            injection_success INTEGER DEFAULT 0,
            injection_response TEXT,
            dna_trace TEXT NOT NULL,
            tricolor TEXT DEFAULT '🟡',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engine_heartbeats (
            engine_name TEXT PRIMARY KEY,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'unknown',
            version TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fusion_state (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def gen_dna(module: str, action: str) -> str:
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = hashlib.md5(f"{module}{now}{action}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now}-{module}-{action}-{suffix}"

# ============================================================
# 融合桥接核心
# ============================================================

class FlowFusionBridge:
    def __init__(self, flow_url: str = FLOW_ENGINE_URL, connect_flow: bool = True):
        self.flow_url = flow_url
        self.connect_flow = connect_flow
        self.flow_connected = False
        if not DB_PATH.exists():
            init_db()
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.event_queue = deque(maxlen=1000)
        self.injection_log = deque(maxlen=500)
        self.engine_status = defaultdict(lambda: {"last_seen": None, "status": "unknown"})

        # 检查流场连通性
        if self.connect_flow:
            self._check_flow_connection()

    def _check_flow_connection(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.flow_url}/state")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                self.flow_connected = True
                return True
        except Exception:
            self.flow_connected = False
            return False

    def translate_event(self, source: str, event_type: str, severity: str = "info") -> Dict:
        """将引擎事件翻译为流场注入参数"""
        key = (source, event_type)
        default = (FlowInjectionType.SOURCE, "center", 0.15)

        injection_type, pos_name, base_strength = TRANSLATION_MATRIX.get(key, default)

        # 严重等级修正强度
        severity_mult = {"critical": 1.3, "high": 1.15, "medium": 1.0, "low": 0.7, "info": 0.5}
        strength = min(1.0, base_strength * severity_mult.get(severity, 1.0))

        # 获取坐标
        pos_x, pos_y = POSITIONS.get(pos_name, POSITIONS["center"])

        return {
            "type": injection_type.value,
            "x": pos_x,
            "y": pos_y,
            "strength": round(strength, 3),
            "radius": 0.05 + strength * 0.15,
            "source": source,
            "event": event_type,
        }

    def inject_to_flow(self, injection: Dict) -> Dict:
        """将翻译后的注入参数推送到流场引擎"""
        if not self.connect_flow:
            return {"success": False, "error": "flow_disabled", "injection": injection}

        # 构建流场API请求体
        payload = {
            "type": injection.get("type", "source"),
            "x": injection.get("x", 0.5),
            "y": injection.get("y", 0.5),
            "strength": injection.get("strength", 0.3),
            "radius": injection.get("radius", 0.1),
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.flow_url}/inject",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode())
                self.flow_connected = True
                return {"success": True, "flow_response": result, "injection": injection}
        except urllib.error.URLError as e:
            self.flow_connected = False
            return {"success": False, "error": f"flow_unreachable: {e}", "injection": injection}
        except Exception as e:
            return {"success": False, "error": str(e), "injection": injection}

    def process_event(self, source: str, event_type: str,
                      severity: str = "info",
                      data: Optional[Dict] = None,
                      inject: bool = True) -> Dict:
        """核心处理流程：接收事件 → 翻译 → 注入流场 → 记录"""
        # 翻译
        injection = self.translate_event(source, event_type, severity)

        # 注入流场
        injection_result = {}
        if inject:
            injection_result = self.inject_to_flow(injection)

        # 记录
        dna = gen_dna("FUSION", source)
        success = 1 if injection_result.get("success") else 0
        tricolor = self._map_severity_to_tricolor(severity)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO fusion_events
            (source, event_type, severity, data, flow_injection_type,
             flow_position, flow_strength, injection_success, injection_response, dna_trace, tricolor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            source, event_type, severity,
            json.dumps(data or {}, ensure_ascii=False),
            injection.get("type"), f"({injection.get('x')},{injection.get('y')})",
            injection.get("strength"), success,
            json.dumps(injection_result, ensure_ascii=False) if injection_result else None,
            dna, tricolor
        ))

        # 更新引擎心跳
        cursor.execute('''
            INSERT INTO engine_heartbeats (engine_name, last_seen, status)
            VALUES (?, datetime('now'), ?)
            ON CONFLICT(engine_name) DO UPDATE SET
                last_seen = datetime('now'), status = ?
        ''', (source, severity, severity))

        self.conn.commit()

        # 事件入队
        event_record = {
            "source": source, "event": event_type, "severity": severity,
            "injection": injection, "success": success,
            "tricolor": tricolor, "dna": dna,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.event_queue.appendleft(event_record)
        self.injection_log.appendleft(event_record)

        return event_record

    def _map_severity_to_tricolor(self, severity: str) -> str:
        mapping = {"critical": "🔴", "high": "🔴", "medium": "🟡", "low": "🟢", "info": "🟢"}
        return mapping.get(severity, "🟡")

    def get_state(self) -> Dict:
        """获取融合桥接当前状态"""
        cursor = self.conn.cursor()

        # 引擎心跳统计
        cursor.execute("SELECT engine_name, last_seen, status FROM engine_heartbeats")
        heartbeats = [dict(row) for row in cursor.fetchall()]

        # 近期事件
        cursor.execute('''
            SELECT source, event_type, severity, flow_injection_type,
                   flow_strength, tricolor, created_at
            FROM fusion_events
            ORDER BY id DESC LIMIT 20
        ''')
        recent = [dict(row) for row in cursor.fetchall()]

        # 注入成功率
        cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN injection_success=1 THEN 1 ELSE 0 END) as success
            FROM fusion_events
            WHERE created_at > datetime('now', '-1 hour')
        ''')
        stats_row = cursor.fetchone()
        stats = dict(stats_row) if stats_row else {"total": 0, "success": 0}
        total = stats.get("total", 0)
        success = stats.get("success", 0)
        success_rate = round(success / total * 100, 1) if total > 0 else 100.0

        # 流场连通状态
        self._check_flow_connection()

        return {
            "bridge": "flow_fusion_v1.0",
            "flow_connected": self.flow_connected,
            "flow_url": self.flow_url,
            "recent_events": recent,
            "engine_heartbeats": heartbeats,
            "injection_success_rate_1h": f"{success_rate}% ({success}/{total})",
            "queue_size": len(self.event_queue),
            "dna": DNA_CORE,
        }

    def get_history(self, limit: int = 100) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM fusion_events ORDER BY id DESC LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()

# ============================================================
# HTTP API 服务器
# ============================================================

FUSION_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂操作台 · 流场融合 v2.0</title>
<style>
:root{
  --bg0:#030310;--bg1:#070720;--bg2:#0b0b2e;--bg3:#0f0f3a;
  --bd:#1c1c55;--bd2:#2a2a6a;
  --gold:#d4af37;--goldb:#ffd700;--goldd:#6a4e0e;
  --red:#ff3355;--redg:rgba(255,51,85,.18);
  --yel:#ffcc00;--yelg:rgba(255,204,0,.15);
  --grn:#00ff88;--grng:rgba(0,255,136,.14);
  --cyn:#00d4ff;--cynl:rgba(0,212,255,.12);
  --pur:#7b2dff;--purs:#a855f7;
  --tp:#e8e0f8;--ts:#6868a8;--td:#2e2e66;
  --nav-w:220px;--right-w:280px;--hdr-h:48px;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden}
body{background:var(--bg0);color:var(--tp);font-family:'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;font-size:13px;display:flex;flex-direction:column}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:2px}

/* HEADER */
#hdr{height:var(--hdr-h);flex-shrink:0;background:var(--bg1);border-bottom:1px solid var(--bd);display:flex;align-items:center;padding:0 16px;gap:14px;position:relative;z-index:100}
#hdr-logo{font-size:16px;font-weight:900;white-space:nowrap;background:linear-gradient(135deg,var(--gold),var(--goldb),var(--purs));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
#hdr-dna{font:10px 'JetBrains Mono',monospace;color:var(--goldd);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hdr-badge{display:flex;align-items:center;gap:6px;padding:3px 10px;border-radius:3px;font:10px 'JetBrains Mono',monospace;white-space:nowrap;flex-shrink:0}
.hdr-badge.grn{background:var(--grng);color:var(--grn);border:1px solid rgba(0,255,136,.3)}
.hdr-badge.red{background:var(--redg);color:var(--red);border:1px solid rgba(255,51,85,.3)}
.hdr-badge.uid{background:rgba(212,175,55,.1);color:var(--gold);border:1px solid rgba(212,175,55,.3)}
.hdr-badge.live{background:rgba(0,212,255,.08);color:var(--cyn);border:1px solid rgba(0,212,255,.25)}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.dot.grn{background:var(--grn);box-shadow:0 0 6px var(--grn)}
.dot.red{background:var(--red);box-shadow:0 0 6px var(--red)}
.dot.yel{background:var(--yel);box-shadow:0 0 6px var(--yel)}
.dot.pulse{animation:blink 1.6s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

/* BODY */
#body{flex:1;display:flex;overflow:hidden}

/* LEFT NAV */
#nav{width:var(--nav-w);flex-shrink:0;background:var(--bg1);border-right:1px solid var(--bd);overflow-y:auto;display:flex;flex-direction:column}
.nav-section{padding:10px 0}
.nav-section-title{padding:6px 14px;font:10px 'JetBrains Mono',monospace;color:var(--goldd);letter-spacing:2px;text-transform:uppercase}
.nav-item{display:flex;align-items:center;gap:8px;padding:6px 14px;cursor:pointer;border-left:2px solid transparent;transition:all .15s;color:var(--ts);font-size:12px}
.nav-item:hover{background:rgba(255,255,255,.03);color:var(--tp);border-left-color:var(--gold)}
.nav-item.active{background:rgba(212,175,55,.06);color:var(--gold);border-left-color:var(--gold)}
.nav-item .ni-icon{font-size:13px;flex-shrink:0;width:18px;text-align:center}
.nav-item .ni-badge{margin-left:auto;padding:1px 5px;border-radius:2px;font:9px 'JetBrains Mono',monospace;background:var(--bd);color:var(--ts);flex-shrink:0}
.nav-item .ni-badge.live{background:var(--grng);color:var(--grn)}
.nav-item .ni-badge.warn{background:var(--yelg);color:var(--yel)}

/* MAIN */
#main{flex:1;display:flex;flex-direction:column;overflow:hidden}
#tabs{display:flex;align-items:center;gap:0;background:var(--bg1);border-bottom:1px solid var(--bd);padding:0 16px;flex-shrink:0;overflow-x:auto}
.tab{padding:10px 18px;font:12px 'JetBrains Mono',monospace;cursor:pointer;border-bottom:2px solid transparent;color:var(--ts);white-space:nowrap;transition:all .15s}
.tab:hover{color:var(--tp)}
.tab.active{color:var(--gold);border-bottom-color:var(--gold)}
#panels{flex:1;overflow:hidden;position:relative}
.panel{position:absolute;inset:0;overflow-y:auto;padding:0;display:none}
.panel.active{display:block}
.pad{padding:20px}

/* RIGHT SIDEBAR */
#right{width:var(--right-w);flex-shrink:0;background:var(--bg1);border-left:1px solid var(--bd);overflow-y:auto;display:flex;flex-direction:column;gap:0}
.rbox{border-bottom:1px solid var(--bd);padding:14px}
.rbox-title{font:10px 'JetBrains Mono',monospace;color:var(--goldd);letter-spacing:2px;margin-bottom:10px}

/* CARDS */
.card{background:var(--bg2);border:1px solid var(--bd);border-radius:6px;padding:14px;margin-bottom:12px;position:relative}
.card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;border-radius:3px 0 0 3px}
.card.gold::before{background:var(--gold)}
.card.red::before{background:var(--red)}
.card.grn::before{background:var(--grn)}
.card.yel::before{background:var(--yel)}
.card.cyn::before{background:var(--cyn)}
.card.pur::before{background:var(--pur)}
.card-title{font-size:12px;font-weight:700;margin-bottom:8px;color:var(--tp)}
.card-body{font-size:11px;color:var(--ts);line-height:1.9}
.card-mono{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--ts);line-height:2}

/* METRICS */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:16px}
.metric{background:var(--bg2);border:1px solid var(--bd);border-radius:6px;padding:14px;text-align:center;position:relative}
.metric::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--gold);opacity:.4}
.metric .value{font:22px 'JetBrains Mono',monospace;font-weight:900;color:var(--gold)}
.metric .label{font:9px 'JetBrains Mono',monospace;color:var(--ts);margin-top:6px;letter-spacing:1px}
.metric.red .value{color:var(--red)}
.metric.grn .value{color:var(--grn)}
.metric.cyn .value{color:var(--cyn)}

/* FLOW CANVAS */
#flow-canvas-wrap{position:relative;background:var(--bg0);border:1px solid var(--bd);border-radius:6px;overflow:hidden}
#flowCanvas{display:block;width:100%;height:360px;cursor:crosshair}
.flow-overlay{position:absolute;bottom:0;left:0;right:0;padding:12px 16px;background:linear-gradient(0deg,rgba(3,3,16,.95),transparent);display:flex;gap:20px;align-items:flex-end;pointer-events:none}
.flow-stat{text-align:center}
.flow-stat-val{font:18px 'JetBrains Mono',monospace;font-weight:900}
.flow-stat-lbl{font:9px 'JetBrains Mono',monospace;color:var(--td);letter-spacing:1px}
.heaven .flow-stat-val{color:var(--cyn)}.earth .flow-stat-val{color:var(--grn)}.human .flow-stat-val{color:var(--gold)}

/* TABLES / LISTS */
.data-list{font-size:11px}
.row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--bd);color:var(--ts)}
.row:last-child{border-bottom:none}
.row .source{color:var(--cyn);min-width:110px}
.row .type{color:var(--purs);min-width:90px}
.row .val{font-family:'JetBrains Mono',monospace;color:var(--tp)}
.row .time{margin-left:auto;font:10px 'JetBrains Mono',monospace;color:var(--td)}
.row .dot-inline{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.matrix-table{width:100%;border-collapse:collapse;font-size:10px;margin-top:8px}
.matrix-table th{background:var(--bg3);color:var(--gold);padding:6px 8px;text-align:left;font-family:'JetBrains Mono',monospace}
.matrix-table td{padding:5px 8px;border-bottom:1px solid var(--bd);color:var(--ts)}
.matrix-table .vortex{color:#f88}.matrix-table .source{color:#8f8}.matrix-table .pressure{color:#ff88}.matrix-table .shockwave{color:#f44}.matrix-table .force{color:#88f}.matrix-table .turbulence{color:#fa8}

/* LUOSHU */
.luoshu-mini{display:grid;grid-template-columns:repeat(3,28px);gap:3px}
.lu-cell{width:28px;height:28px;display:flex;align-items:center;justify-content:center;font:11px 'JetBrains Mono',monospace;border:1px solid var(--bd);color:rgba(0,212,255,.6)}
.lu-cell.center{border-color:var(--goldd);color:var(--gold);background:rgba(212,175,55,.06)}

/* TRICOLOR */
.tri-bar{height:4px;border-radius:2px;background:var(--bg2);overflow:hidden;margin-top:6px;display:flex}
.tri-seg{height:100%}
.tri-legend{display:flex;gap:12px;margin-top:8px;font:10px 'JetBrains Mono',monospace;color:var(--ts)}

/* LOG */
#ws-log{height:120px;overflow-y:auto;background:var(--bg0);border:1px solid var(--bd);border-radius:4px;padding:8px;font:10px 'JetBrains Mono',monospace;color:var(--ts);line-height:1.8}
.log-line{margin-bottom:2px}
.log-line .ts{color:var(--td)}
.log-line .grn{color:var(--grn)}.log-line .yel{color:var(--yel)}.log-line .red{color:var(--red)}.log-line .cyn{color:var(--cyn)}

/* RESPONSIVE */
@media(max-width:1100px){#right{display:none}#nav{width:180px}}
@media(max-width:800px){#nav{display:none}}
</style>
</head>
<body>
<div id="hdr">
  <div id="hdr-logo">🐉 龍魂操作台 · 流场融合 v2.0</div>
  <div id="hdr-dna">DNA: #龍芯⚡️丙午·乙巳·壬申·午时·☰乾-FLOW-FUSION-BRIDGE-v2.0</div>
  <div class="hdr-badge uid"><span>UID</span>9622</div>
  <div class="hdr-badge grn" id="hdrFlow"><span class="dot grn pulse"></span>流场在线</div>
  <div class="hdr-badge live" id="hdrWs"><span class="dot yel"></span>WS: 连接中</div>
  <div class="hdr-badge" id="hdrTime" style="color:var(--ts)">--:--:--</div>
</div>
<div id="body">
  <nav id="nav">
    <div class="nav-section">
      <div class="nav-section-title">OPERATION</div>
      <div class="nav-item active" data-panel="overview"><span class="ni-icon">◈</span>总览面板<span class="ni-badge live">LIVE</span></div>
      <div class="nav-item" data-panel="flow"><span class="ni-icon">🌊</span>流场可视化</div>
      <div class="nav-item" data-panel="events"><span class="ni-icon">📋</span>注入事件<span class="ni-badge" id="navEventCount">0</span></div>
      <div class="nav-item" data-panel="engines"><span class="ni-icon">⚙️</span>引擎心跳</div>
      <div class="nav-item" data-panel="anomalies"><span class="ni-icon">⚠️</span>异常预警<span class="ni-badge warn" id="navAnomalyCount">0</span></div>
      <div class="nav-item" data-panel="matrix"><span class="ni-icon">🗺️</span>翻译矩阵</div>
    </div>
    <div class="nav-section">
      <div class="nav-section-title">SYSTEM</div>
      <div class="nav-item" onclick="location.href='http://127.0.0.1:8776/'" title="流场引擎 8776"><span class="ni-icon">🐉</span>流场引擎</div>
      <div class="nav-item" onclick="location.href='http://127.0.0.1:8779/'" title="统一控制台 8779"><span class="ni-icon">🧠</span>知识中枢</div>
    </div>
  </nav>

  <main id="main">
    <div id="tabs">
      <div class="tab active" data-panel="overview">总览</div>
      <div class="tab" data-panel="flow">流场</div>
      <div class="tab" data-panel="events">事件</div>
      <div class="tab" data-panel="engines">引擎</div>
      <div class="tab" data-panel="anomalies">异常</div>
      <div class="tab" data-panel="matrix">矩阵</div>
    </div>
    <div id="panels">
      <!-- OVERVIEW -->
      <div class="panel active" id="panel-overview">
        <div class="pad">
          <div class="metrics">
            <div class="metric"><div class="value" id="mtTotal">0</div><div class="label">总注入次数</div></div>
            <div class="metric"><div class="value" id="mtSuccess">100%</div><div class="label">注入成功率(1h)</div></div>
            <div class="metric"><div class="value" id="mtEngines">0</div><div class="label">活跃引擎</div></div>
            <div class="metric grn"><div class="value" id="mtFlow">在线</div><div class="label">流场连通</div></div>
            <div class="metric cyn"><div class="value" id="mtQueue">0</div><div class="label">队列中</div></div>
            <div class="metric red"><div class="value" id="mtAnomaly">0</div><div class="label">当前异常</div></div>
          </div>
          <div id="flow-canvas-wrap">
            <canvas id="flowCanvas" width="800" height="360"></canvas>
            <div class="flow-overlay">
              <div class="flow-stat heaven"><div class="flow-stat-val" id="statParticles">0</div><div class="flow-stat-lbl">粒子数</div></div>
              <div class="flow-stat earth"><div class="flow-stat-val" id="statFrame">0</div><div class="flow-stat-lbl">帧数</div></div>
              <div class="flow-stat human"><div class="flow-stat-val" id="statVortices">0</div><div class="flow-stat-lbl">涡旋</div></div>
              <div class="breath-bar-wrap" style="flex:1;align-self:center">
                <div class="flow-stat-lbl">流场活跃度</div>
                <div style="height:4px;background:var(--bg2);border-radius:2px;overflow:hidden"><div id="breathFill" style="height:100%;width:0%;background:linear-gradient(90deg,var(--cyn),var(--gold));border-radius:2px;transition:width .3s"></div></div>
              </div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">
            <div class="card cyn"><div class="card-title">📋 最近注入事件</div><div class="card-body data-list" id="overviewEvents">加载中...</div></div>
            <div class="card pur"><div class="card-title">⚙️ 引擎心跳</div><div class="card-body data-list" id="overviewEngines">加载中...</div></div>
          </div>
        </div>
      </div>

      <!-- FLOW -->
      <div class="panel" id="panel-flow">
        <div style="padding:16px;height:100%;display:flex;flex-direction:column">
          <div id="flow-canvas-wrap" style="flex:1">
            <canvas id="flowCanvasBig" width="1000" height="600" style="width:100%;height:100%"></canvas>
          </div>
          <div style="display:flex;gap:16px;margin-top:12px">
            <div class="card grn" style="flex:1"><div class="card-title">点击注入</div><div class="card-body">在画布任意位置点击，可注入一个 source 扰动点。双击注入 vortex 涡旋。</div></div>
            <div class="card yel" style="flex:1"><div class="card-title">颜色含义</div><div class="card-body">青色=速度场 · 金色=高密度区 · 红色=异常/冲击波 · 紫色=涡旋核心</div></div>
          </div>
        </div>
      </div>

      <!-- EVENTS -->
      <div class="panel" id="panel-events">
        <div class="pad">
          <div class="card gold"><div class="card-title">📡 实时事件流 <span style="font-size:11px;color:var(--ts)">(最近50条)</span></div><div class="card-body data-list" id="eventsList">加载中...</div></div>
        </div>
      </div>

      <!-- ENGINES -->
      <div class="panel" id="panel-engines">
        <div class="pad">
          <div class="card pur"><div class="card-title">⚙️ 引擎心跳</div><div class="card-body data-list" id="enginesList">加载中...</div></div>
        </div>
      </div>

      <!-- ANOMALIES -->
      <div class="panel" id="panel-anomalies">
        <div class="pad">
          <div class="card red"><div class="card-title">⚠️ 异常预警 <span style="font-size:11px;color:var(--ts)">(WebSocket 实时推送)</span></div><div class="card-body data-list" id="anomaliesList">暂无异常</div></div>
        </div>
      </div>

      <!-- MATRIX -->
      <div class="panel" id="panel-matrix">
        <div class="pad">
          <div class="card gold"><div class="card-title">🗺️ 事件 → 流场 翻译矩阵</div>
            <table class="matrix-table"><thead><tr><th>源引擎</th><th>事件</th><th>流场注入</th><th>位置</th><th>强度</th></tr></thead><tbody id="matrixBody"></tbody></table>
          </div>
        </div>
      </div>
    </div>
  </main>

  <aside id="right">
    <div class="rbox">
      <div class="rbox-title">TRICOLOR 三色相位</div>
      <div class="card grn"><div class="card-title">🟢 通过</div><div class="card-body" id="triGreenCount">0 条注入</div></div>
      <div class="card yel"><div class="card-title">🟡 待核</div><div class="card-body" id="triYellowCount">0 条注入</div></div>
      <div class="card red"><div class="card-title">🔴 红线</div><div class="card-body" id="triRedCount">0 条注入</div></div>
      <div class="tri-bar"><div class="tri-seg" id="barGreen" style="background:var(--grn);width:33%"></div><div class="tri-seg" id="barYellow" style="background:var(--yel);width:33%"></div><div class="tri-seg" id="barRed" style="background:var(--red);width:34%"></div></div>
    </div>
    <div class="rbox">
      <div class="rbox-title">LUOSHU 洛书九宫</div>
      <div style="display:flex;justify-content:center"><div class="luoshu-mini">
        <div class="lu-cell">4</div><div class="lu-cell">9</div><div class="lu-cell">2</div>
        <div class="lu-cell">3</div><div class="lu-cell center">5</div><div class="lu-cell">7</div>
        <div class="lu-cell">8</div><div class="lu-cell">1</div><div class="lu-cell">6</div>
      </div></div>
      <div class="card-mono" style="margin-top:10px">369 不动点: sn=369 · log=5.911 · perm=108</div>
    </div>
    <div class="rbox">
      <div class="rbox-title">LIVE LOG</div>
      <div id="ws-log"><div class="log-line"><span class="ts">--</span> 等待实时数据...</div></div>
    </div>
  </aside>
</div>

<script>
const BRIDGE_URL = window.location.origin;
const FLOW_URL = 'http://127.0.0.1:8776';
let ws = null;
let anomalies = [];
let flowState = null;
let particles = [];

// ---------- TABS / NAV ----------
function switchPanel(name){
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item[data-panel], .tab').forEach(el=>el.classList.remove('active'));
  document.getElementById('panel-'+name).classList.add('active');
  document.querySelectorAll('[data-panel="'+name+'"]').forEach(el=>el.classList.add('active'));
}
document.querySelectorAll('.nav-item[data-panel], .tab').forEach(el=>{
  el.addEventListener('click',()=>switchPanel(el.dataset.panel));
});

// ---------- TIME ----------
function updateTime(){
  const now = new Date();
  document.getElementById('hdrTime').textContent = now.toLocaleTimeString('zh-CN',{hour12:false});
}
setInterval(updateTime,1000); updateTime();

// ---------- LOG ----------
function log(msg,cls='cyn'){
  const box = document.getElementById('ws-log');
  const ts = new Date().toLocaleTimeString('zh-CN',{hour12:false});
  const line = document.createElement('div'); line.className='log-line';
  line.innerHTML = '<span class="ts">'+ts+'</span> <span class="'+cls+'">'+msg+'</span>';
  box.prepend(line);
  if(box.children.length>60) box.lastChild.remove();
}

// ---------- WEBSOCKET TO FLOW ENGINE ----------
function connectWs(){
  const wsUrl = 'ws://127.0.0.1:8776/ws';
  ws = new WebSocket(wsUrl);
  const hdr = document.getElementById('hdrWs');
  ws.onopen = ()=>{ hdr.innerHTML='<span class="dot grn pulse"></span>WS: 在线'; log('流场 WS 已连接','grn'); };
  ws.onmessage = (ev)=>{
    try{
      const data = JSON.parse(ev.data);
      if(data.type==='anomaly'){
        anomalies.unshift(...data.data);
        anomalies = anomalies.slice(0,20);
        log('收到异常推送: '+data.data.length+' 条','red');
        renderAnomalies();
      }
    }catch(e){}
  };
  ws.onclose = ()=>{ hdr.innerHTML='<span class="dot red"></span>WS: 断开'; log('流场 WS 断开，5秒后重连','red'); setTimeout(connectWs,5000); };
  ws.onerror = ()=>{ hdr.innerHTML='<span class="dot red"></span>WS: 错误'; };
}
connectWs();

// ---------- FETCH STATE ----------
async function fetchState(){
  try{
    const r = await fetch(BRIDGE_URL+'/state');
    const state = await r.json();
    renderBridge(state);
    await fetchFlowState();
  }catch(e){
    document.getElementById('hdrFlow').innerHTML='<span class="dot red"></span>流场离线';
    document.getElementById('hdrFlow').className='hdr-badge red';
    log('桥接状态获取失败','red');
  }
}
async function fetchFlowState(){
  try{
    const r = await fetch(FLOW_URL+'/state');
    flowState = await r.json();
    document.getElementById('hdrFlow').innerHTML='<span class="dot grn pulse"></span>流场在线';
    document.getElementById('hdrFlow').className='hdr-badge grn';
    renderFlow(flowState);
  }catch(e){
    document.getElementById('hdrFlow').innerHTML='<span class="dot red"></span>流场离线';
    document.getElementById('hdrFlow').className='hdr-badge red';
  }
}

// ---------- RENDER BRIDGE ----------
function renderBridge(state){
  const recent = state.recent_events || [];
  document.getElementById('mtTotal').textContent = recent.length;
  document.getElementById('mtSuccess').textContent = state.injection_success_rate_1h || '100%';
  document.getElementById('mtQueue').textContent = state.queue_size || 0;
  document.getElementById('mtEngines').textContent = (state.engine_heartbeats || []).filter(e=>e.status!=='unknown').length;
  document.getElementById('mtFlow').textContent = state.flow_connected ? '在线' : '离线';
  document.getElementById('mtAnomaly').textContent = anomalies.length;
  document.getElementById('navEventCount').textContent = recent.length;
  document.getElementById('navAnomalyCount').textContent = anomalies.length;

  // events
  const evHtml = recent.slice(0,12).map(e=>{
    const col = e.tricolor==='🔴'?'red':e.tricolor==='🟢'?'grn':'yel';
    return '<div class="row"><span class="dot-inline" style="background:var(--'+col+')"></span><span class="source">'+e.source+'</span><span class="type">'+e.event_type+'</span><span class="time">'+(e.created_at||'').slice(11,19)+'</span></div>';
  }).join('') || '<div class="row">无事件</div>';
  document.getElementById('eventsList').innerHTML = evHtml;
  document.getElementById('overviewEvents').innerHTML = evHtml;

  // engines
  const eng = state.engine_heartbeats || [];
  const engHtml = eng.slice(0,10).map(e=>{
    const cls = e.status==='ok'?'grn':e.status==='critical'?'red':'yel';
    return '<div class="row"><span class="dot-inline" style="background:var(--'+cls+')"></span><span class="source">'+e.engine_name+'</span><span class="val">'+e.status+'</span><span class="time">'+(e.last_seen||'').slice(11,19)+'</span></div>';
  }).join('') || '<div class="row">无心跳记录</div>';
  document.getElementById('enginesList').innerHTML = engHtml;
  document.getElementById('overviewEngines').innerHTML = engHtml;

  // tricolor counts
  const g = recent.filter(e=>e.tricolor==='🟢').length;
  const y = recent.filter(e=>e.tricolor==='🟡').length;
  const r = recent.filter(e=>e.tricolor==='🔴').length;
  const total = Math.max(1,g+y+r);
  document.getElementById('triGreenCount').textContent = g+' 条注入';
  document.getElementById('triYellowCount').textContent = y+' 条注入';
  document.getElementById('triRedCount').textContent = r+' 条注入';
  document.getElementById('barGreen').style.width = (g/total*100)+'%';
  document.getElementById('barYellow').style.width = (y/total*100)+'%';
  document.getElementById('barRed').style.width = (r/total*100)+'%';

  // matrix
  const matrix = [
    ['自我审计','dna_risk_high','vortex','center','0.85'],['自我审计','p0_risk_high','vortex','center','0.90'],
    ['健康检查','critical','pressure','center','0.95'],['熔断控制','trip','shockwave','center','1.00'],
    ['三色审计','red','vortex','center','0.90'],['异常检测','behavior_anomaly','shockwave','center','0.75'],
    ['知识获取','new_knowledge','source','left','0.35'],['人格切换','activate','source','mid_right','0.35'],
    ['任务完成','success','anti_force','right','0.35'],['记错本','recorded','source','mid_left','0.30'],
    ['DNA验证','fail','vortex','center','0.80'],['主动观察','file_change','source','mid_left','0.25'],
    ['资源监控','cpu_high','pressure','bottom_left','0.65']
  ];
  document.getElementById('matrixBody').innerHTML = matrix.map(m=>
    '<tr><td>'+m[0]+'</td><td>'+m[1]+'</td><td class="'+m[2]+'">'+m[2]+'</td><td>'+m[3]+'</td><td>'+m[4]+'</td></tr>'
  ).join('');
}

function renderAnomalies(){
  document.getElementById('mtAnomaly').textContent = anomalies.length;
  document.getElementById('navAnomalyCount').textContent = anomalies.length;
  const html = anomalies.slice(0,15).map(a=>
    '<div class="row"><span class="source">'+(a.type||'anomaly')+'</span><span class="type">'+(a.severity||'info')+'</span><span class="time">'+(a.timestamp||'').slice(11,19)+'</span></div>'
  ).join('') || '<div class="row">暂无异常</div>';
  document.getElementById('anomaliesList').innerHTML = html;
}

// ---------- FLOW VISUALIZATION ----------
function initParticles(){
  particles = [];
  for(let i=0;i<120;i++){
    particles.push({x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.003,vy:(Math.random()-.5)*.003,life:Math.random()});
  }
}
initParticles();

function renderFlow(state){
  if(!state) return;
  document.getElementById('statParticles').textContent = state.particles || 0;
  document.getElementById('statFrame').textContent = state.frame_count || 0;
  const vortices = (state.vortices || []).length;
  document.getElementById('statVortices').textContent = vortices;
  const activity = Math.min(100, (state.particles||0)/2 + vortices*10 + (state.pressure_points||[]).length*5);
  document.getElementById('breathFill').style.width = activity+'%';
}

function drawFlow(){
  const cvs = document.getElementById('flowCanvas');
  if(!cvs) return;
  const ctx = cvs.getContext('2d');
  const w = cvs.width, h = cvs.height;
  ctx.fillStyle = 'rgba(3,3,16,0.25)';
  ctx.fillRect(0,0,w,h);

  // grid
  ctx.strokeStyle = 'rgba(28,28,85,0.5)'; ctx.lineWidth = 1;
  for(let i=0;i<=w;i+=40){ ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,h);ctx.stroke(); }
  for(let i=0;i<=h;i+=40){ ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(w,i);ctx.stroke(); }

  // particles
  particles.forEach(p=>{
    p.x += p.vx; p.y += p.vy;
    if(p.x<0||p.x>1) p.vx *= -1;
    if(p.y<0||p.y>1) p.vy *= -1;
    p.life += 0.01;
    const px = p.x*w, py = p.y*h;
    ctx.beginPath();
    ctx.arc(px,py,1.5,0,Math.PI*2);
    ctx.fillStyle = 'rgba(0,212,255,'+(0.4+Math.sin(p.life)*0.3)+')';
    ctx.fill();
  });

  // draw anomalies / vortices from state
  if(flowState && flowState.vortices){
    flowState.vortices.forEach(v=>{
      const x = v.x*w, y = v.y*h;
      ctx.beginPath();
      ctx.arc(x,y,8+v.strength*20,0,Math.PI*2);
      ctx.strokeStyle = 'rgba(255,51,85,0.5)';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }

  // flow sources
  if(flowState && flowState.sources){
    flowState.sources.forEach(s=>{
      const x = s.x*w, y = s.y*h;
      ctx.beginPath();
      ctx.arc(x,y,4+s.strength*15,0,Math.PI*2);
      ctx.fillStyle = 'rgba(212,175,55,0.3)';
      ctx.fill();
    });
  }

  requestAnimationFrame(drawFlow);
}

// big canvas interaction
const bigCvs = document.getElementById('flowCanvasBig');
if(bigCvs){
  bigCvs.addEventListener('click', async (e)=>{
    const rect = bigCvs.getBoundingClientRect();
    const x = (e.clientX-rect.left)/rect.width;
    const y = (e.clientY-rect.top)/rect.height;
    try{
      await fetch(FLOW_URL+'/inject',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'source',x,y,strength:0.4,radius:0.1})});
      log('已注入 source @ '+x.toFixed(2)+','+y.toFixed(2),'grn');
    }catch(err){ log('注入失败','red'); }
  });
  bigCvs.addEventListener('dblclick', async (e)=>{
    const rect = bigCvs.getBoundingClientRect();
    const x = (e.clientX-rect.left)/rect.width;
    const y = (e.clientY-rect.top)/rect.height;
    try{
      await fetch(FLOW_URL+'/inject',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'vortex',x,y,strength:0.6,radius:0.12})});
      log('已注入 vortex @ '+x.toFixed(2)+','+y.toFixed(2),'yel');
    }catch(err){ log('注入失败','red'); }
  });
}

// sync small canvas size
function resizeCanvas(){
  const cvs = document.getElementById('flowCanvas');
  if(cvs && cvs.parentElement){
    cvs.width = cvs.parentElement.clientWidth;
    cvs.height = 360;
  }
}
window.addEventListener('resize',resizeCanvas);
resizeCanvas();
drawFlow();

// ---------- LOOP ----------
fetchState();
setInterval(fetchState,3000);
log('操作台已加载','cyn');
</script>
</body>
</html>"""

class FusionHTTPHandler(http.server.BaseHTTPRequestHandler):
    bridge: FlowFusionBridge = None

    def log_message(self, format, *args):
        pass  # 静默日志

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._send_html(FUSION_DASHBOARD_HTML)
        elif self.path == "/state":
            self._send_json(self.bridge.get_state())
        elif self.path == "/history":
            self._send_json(self.bridge.get_history(100))
        elif self.path == "/flow-status":
            connected = self.bridge._check_flow_connection()
            self._send_json({"flow_connected": connected, "flow_url": self.bridge.flow_url})
        elif self.path == "/health":
            self._send_json({"status": "ok", "service": "flow-fusion-bridge", "port": 8777,
                "dna": "丙午·乙巳·壬申·午时·☰乾-FLOW-FUSION-BRIDGE-v1.0"})
        elif self.path == "/ping":
            self._send_json({"pong": True, "time": datetime.datetime.now().isoformat()})
        elif self.path == "/events":
            events = list(self.bridge.event_queue)[:50]
            self._send_json(events)
        else:
            self._send_json({"error": "not_found"}, 404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid_json"}, 400)
            return

        if self.path == "/event":
            source = data.get("source", "unknown")
            event_type = data.get("event_type", "unknown")
            severity = data.get("severity", "info")
            event_data = data.get("data")
            no_inject = data.get("no_inject", False)

            result = self.bridge.process_event(
                source, event_type, severity, event_data,
                inject=not no_inject
            )
            self._send_json(result)

        elif self.path == "/batch-event":
            events = data.get("events", [])
            results = []
            for evt in events:
                r = self.bridge.process_event(
                    evt.get("source", "unknown"),
                    evt.get("event_type", "unknown"),
                    evt.get("severity", "info"),
                    evt.get("data"),
                    inject=not evt.get("no_inject", False)
                )
                results.append(r)
            self._send_json({"results": results, "count": len(results)})

        else:
            self._send_json({"error": "not_found"}, 404)

# ============================================================
# 命令行接口
# ============================================================

def print_banner(port: int, flow_connected: bool):
    print(f"""
{'='*55}
🐉 龍魂 · 流场融合桥接引擎 v1.0
{'='*55}
  API:     http://127.0.0.1:{port}
  仪表盘:  http://localhost:{port}/
  流场:    {FLOW_ENGINE_URL} {'✅ 已连通' if flow_connected else '❌ 未连通'}
{'='*55}
  DNA:     #龍芯⚡️{DNA_CORE}
  CONFIRM: {CONFIRM}
  GPG:     {GPG[:32]}...
{'='*55}
  流场融合 · 全引擎观测 · 统一物理映射
  所有引擎通过此桥注入流场 · 可视化系统健康
{'='*55}
""")

def run_server(port: int = 8777, connect_flow: bool = True):
    bridge = FlowFusionBridge(connect_flow=connect_flow)
    FusionHTTPHandler.bridge = bridge
    print_banner(port, bridge.flow_connected)

    server = socketserver.ThreadingTCPServer(("127.0.0.1", port), FusionHTTPHandler)
    server.daemon_threads = True
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 融合桥接 · 龍魂不息")
        bridge.close()
        server.shutdown()

def status_report():
    bridge = FlowFusionBridge()
    state = bridge.get_state()
    print(json.dumps(state, ensure_ascii=False, indent=2))
    bridge.close()

def test_inject(source: str = "system", event: str = "test"):
    bridge = FlowFusionBridge()
    result = bridge.process_event(source, event, "info")
    print(f"✅ 测试注入: {source}/{event}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    bridge.close()

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 流场融合桥接引擎")
    parser.add_argument("--port", type=int, default=8777, help="桥接服务端口 (默认8777)")
    parser.add_argument("--no-flow", action="store_true", help="不连接流场 (只记录事件)")
    parser.add_argument("--status", action="store_true", help="查看融合状态")
    parser.add_argument("--inject", type=str, nargs="?", const="test", help="测试注入")
    parser.add_argument("--flow-url", type=str, default=FLOW_ENGINE_URL, help="流场引擎地址")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    if args.status:
        status_report()
    elif args.inject:
        test_inject("system", args.inject)
    else:
        run_server(port=args.port, connect_flow=not args.no_flow)

if __name__ == "__main__":
    main()
