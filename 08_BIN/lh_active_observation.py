#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_ACTIVE_OBSERVATION-v1.0-f3f78689
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 主动观察引擎 v2.0 (Active Observation Engine)
==========================================================
从被动响应升级为主动观察——不等指令，自己看、自己判断、自己动手。

六类触发源：
  FILE_CHANGE    → 文件系统变更（创建/修改/删除）
  NETWORK_CHANGE → 网络状态变化（连接/断开/异常）
  TIME_EVENT     → 定时事件（cron式调度）
  PROCESS_EVENT  → 进程事件（启动/退出/异常）
  RESOURCE_ALERT → 资源告警（内存/磁盘/CPU超阈值）
  CROSS_DEVICE   → 跨设备同步（Mac↔鲲鹏↔手机）

架构：
  观察源 → 规则匹配 → 阈值检查 → 动作执行 → EventBus发布 → 审计归档

集成：
  - 对接 lh_event_bus_engine.EventBus（发布 FILE_OBSERVED/NETWORK_ALERT 等事件）
  - 对接 lh_regulatory_daemon（复用文件快照逻辑）
  - 对接 lh_resident_registry（常驻任务自动触发）

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-ACTIVE-OBSERVATION-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import hashlib
import json
import os
import platform
import psutil
import re
import signal
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# ── 项目根 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bin.lh_event_bus_engine import EventBus, EventType, Event  # noqa: E402

# ── 常量 ──
DNA = "#龍芯⚡️丙午·辛未·丙戌·亥时·需-ACTIVE-OBSERVATION-v2.0"
VERSION = "2.0.0"
OBS_DIR = PROJECT_ROOT / "data" / "active_observation"
OBS_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = OBS_DIR / "observation_state.json"
RULES_FILE = OBS_DIR / "observation_rules.json"


# ═══════════════════════════════════════════════════════════
# 触发类型
# ═══════════════════════════════════════════════════════════

class TriggerType(Enum):
    FILE_CHANGE = "file_change"           # 文件系统变更
    NETWORK_CHANGE = "network_change"     # 网络状态变化
    TIME_EVENT = "time_event"             # 定时事件
    PROCESS_EVENT = "process_event"       # 进程事件
    RESOURCE_ALERT = "resource_alert"     # 资源告警
    CROSS_DEVICE = "cross_device"         # 跨设备同步


# ═══════════════════════════════════════════════════════════
# 动作类型
# ═══════════════════════════════════════════════════════════

class ActionType(Enum):
    LOG = "log"               # 仅记录
    ALERT = "alert"           # 推送告警
    EXECUTE = "execute"       # 自动执行脚本
    ARCHIVE = "archive"       # 自动归档
    SYNC = "sync"             # 触发同步
    FUSE = "fuse"             # 触发熔断
    NOTIFY = "notify"         # 通知UID9622


# ═══════════════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════════════

@dataclass
class ObsThreshold:
    """观察阈值"""
    min_interval_ms: int = 5000        # 最小触发间隔
    max_per_hour: int = 60             # 每小时最大触发次数
    cooldown_ms: int = 30000           # 冷却期
    escalation_level: int = 3          # 升级阈值（连续触发N次后升级）


@dataclass
class ObservationRule:
    """观察规则"""
    rule_id: str
    trigger_type: TriggerType
    pattern: str                        # glob/regex 匹配模式
    action: ActionType
    action_script: str = ""             # 执行脚本路径（action=EXECUTE时）
    threshold: ObsThreshold = field(default_factory=ObsThreshold)
    enabled: bool = True
    description: str = ""
    last_triggered: float = 0.0
    trigger_count: int = 0
    consecutive_triggers: int = 0       # 连续触发计数（升级用）
    dna_signature: str = ""

    def __post_init__(self):
        if not self.dna_signature:
            payload = f"{self.rule_id}-{self.trigger_type.value}-{self.pattern}"
            self.dna_signature = f"#龍芯⚡️OBS-{hashlib.sha256(payload.encode()).hexdigest()[:12]}"

    def can_trigger(self) -> Tuple[bool, str]:
        """检查是否可触发。返回 (可否, 原因)"""
        if not self.enabled:
            return False, "已禁用"
        now = time.time()
        since_last_ms = (now - self.last_triggered) * 1000
        if since_last_ms < self.threshold.min_interval_ms:
            return False, f"间隔不足 ({since_last_ms:.0f}ms < {self.threshold.min_interval_ms}ms)"
        if self.trigger_count >= self.threshold.max_per_hour:
            return False, f"频率超限 ({self.trigger_count}/{self.threshold.max_per_hour})"
        return True, "ok"

    def record_trigger(self):
        """记录触发"""
        self.last_triggered = time.time()
        self.trigger_count += 1
        self.consecutive_triggers += 1

    def reset_consecutive(self):
        self.consecutive_triggers = 0

    def should_escalate(self) -> bool:
        return self.consecutive_triggers >= self.threshold.escalation_level


# ═══════════════════════════════════════════════════════════
# 默认规则集
# ═══════════════════════════════════════════════════════════

DEFAULT_RULES: List[Dict] = [
    # ── 文件系统 ──
    {
        "rule_id": "obs-file-new-py",
        "trigger_type": "file_change",
        "pattern": "*.py",
        "action": "log",
        "description": "检测到新Python文件时记录并索引",
    },
    {
        "rule_id": "obs-file-new-md",
        "trigger_type": "file_change",
        "pattern": "*.md",
        "action": "archive",
        "description": "检测到新Markdown文档时归档索引",
    },
    {
        "rule_id": "obs-file-config-change",
        "trigger_type": "file_change",
        "pattern": "config/*.json",
        "action": "alert",
        "description": "配置文件变更时告警",
        "threshold": {"min_interval_ms": 60000, "max_per_hour": 10, "cooldown_ms": 60000, "escalation_level": 5},
    },
    {
        "rule_id": "obs-file-env-change",
        "trigger_type": "file_change",
        "pattern": "*.env*",
        "action": "alert",
        "description": "环境变量文件变更时告警",
        "threshold": {"min_interval_ms": 300000, "max_per_hour": 3, "cooldown_ms": 300000, "escalation_level": 2},
    },
    {
        "rule_id": "obs-file-gitignore-change",
        "trigger_type": "file_change",
        "pattern": ".gitignore",
        "action": "alert",
        "description": ".gitignore变更时告警",
    },
    # ── 网络 ──
    {
        "rule_id": "obs-net-disconnect",
        "trigger_type": "network_change",
        "pattern": "disconnected",
        "action": "alert",
        "description": "网络断开时告警",
    },
    {
        "rule_id": "obs-net-reconnect",
        "trigger_type": "network_change",
        "pattern": "reconnected",
        "action": "execute",
        "action_script": "bin/lh_auto_sync.py",
        "description": "网络恢复后自动同步",
    },
    # ── 定时 ──
    {
        "rule_id": "obs-time-hourly-health",
        "trigger_type": "time_event",
        "pattern": "0 * * * *",
        "action": "execute",
        "action_script": "bin/lh_auto_cannon.py health",
        "description": "每小时自动健康检查",
    },
    {
        "rule_id": "obs-time-daily-audit",
        "trigger_type": "time_event",
        "pattern": "0 3 * * *",
        "action": "execute",
        "action_script": "bin/lh_dual_audit_engine.py",
        "description": "每日凌晨3点双重审计",
    },
    {
        "rule_id": "obs-time-direct-settlement-selfcheck",
        "trigger_type": "time_event",
        "pattern": "hourly",
        "action": "execute",
        "action_script": "bin/lh_dcep_recharge.py --verify-selfcheck",
        "description": "每小时对系统货币通道做直达标准自检",
        "threshold": {"min_interval_ms": 3600000, "max_per_hour": 2, "cooldown_ms": 3600000, "escalation_level": 3},
    },
    # ── 进程 ──
    {
        "rule_id": "obs-proc-longhun-down",
        "trigger_type": "process_event",
        "pattern": "longhun-*:down",
        "action": "execute",
        "action_script": "systemctl restart",
        "description": "龍魂服务异常退出时自动重启",
    },
    # ── 资源 ──
    {
        "rule_id": "obs-res-memory-high",
        "trigger_type": "resource_alert",
        "pattern": "memory>85%",
        "action": "alert",
        "description": "内存使用超过85%时告警",
        "threshold": {"min_interval_ms": 300000, "max_per_hour": 12, "cooldown_ms": 300000, "escalation_level": 3},
    },
    {
        "rule_id": "obs-res-disk-high",
        "trigger_type": "resource_alert",
        "pattern": "disk>90%",
        "action": "execute",
        "action_script": "bin/lh_auto_compress.py",
        "description": "磁盘使用超过90%时自动压缩归档",
        "threshold": {"min_interval_ms": 600000, "max_per_hour": 6, "cooldown_ms": 600000, "escalation_level": 2},
    },
    {
        "rule_id": "obs-res-cpu-high",
        "trigger_type": "resource_alert",
        "pattern": "cpu>95%",
        "action": "alert",
        "description": "CPU使用超过95%时告警",
        "threshold": {"min_interval_ms": 120000, "max_per_hour": 30, "cooldown_ms": 120000, "escalation_level": 5},
    },
    # ── 跨设备 ──
    {
        "rule_id": "obs-cross-kunpeng-down",
        "trigger_type": "cross_device",
        "pattern": "kunpeng:unreachable",
        "action": "alert",
        "description": "鲲鹏服务器不可达时告警",
        "threshold": {"min_interval_ms": 600000, "max_per_hour": 6, "cooldown_ms": 600000, "escalation_level": 3},
    },
    # ── 反钓鱼反贪心自审计 ──
    {
        "rule_id": "obs-time-anti-fishing-selfcheck",
        "trigger_type": "time_event",
        "pattern": "hourly",
        "action": "execute",
        "action_script": "python3 L3_数据层/anti_fishing_greed.py --audit-self",
        "description": "每小时反钓鱼反贪心自审计（8项P0承诺逐条检查）",
        "threshold": {"min_interval_ms": 3600000, "max_per_hour": 2, "cooldown_ms": 3600000, "escalation_level": 3},
    },
]


# ═══════════════════════════════════════════════════════════
# 主动观察引擎
# ═══════════════════════════════════════════════════════════

class ActiveObservationEngine:
    """
    主动观察引擎 — 六类触发源统一观察 + 规则匹配 + 动作执行。

    用法:
        engine = ActiveObservationEngine()
        engine.load_default_rules()
        engine.start()
        # ... 系统运行中 ...
        engine.stop()
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self.rules: Dict[str, ObservationRule] = {}
        self._running = False
        self._lock = threading.Lock()
        self._observers: List[threading.Thread] = []
        self._file_snapshots: Dict[str, Tuple[float, str]] = {}  # path → (mtime, sha256)
        self._event_bus = event_bus or EventBus()
        self._hourly_counters: Dict[str, int] = {}  # rule_id → 本小时计数
        self._last_counter_reset = time.time()

        # 注册 EventBus 回调
        self._event_bus.register_callback("obs_file_observed", self._on_file_observed)
        self._event_bus.register_callback("obs_network_alert", self._on_network_alert)
        self._event_bus.register_callback("obs_resource_alert", self._on_resource_alert)

    # ── 规则管理 ──

    def load_default_rules(self):
        """加载默认规则集"""
        for r in DEFAULT_RULES:
            self.add_rule(ObservationRule(
                rule_id=r["rule_id"],
                trigger_type=TriggerType(r["trigger_type"]),
                pattern=r["pattern"],
                action=ActionType(r["action"]),
                action_script=r.get("action_script", ""),
                threshold=ObsThreshold(**r.get("threshold", {})),
                description=r.get("description", ""),
            ))

    def add_rule(self, rule: ObservationRule):
        with self._lock:
            self.rules[rule.rule_id] = rule
            self._log(f"📋 注册规则: {rule.rule_id} [{rule.trigger_type.value}] {rule.description}")

    def remove_rule(self, rule_id: str):
        with self._lock:
            self.rules.pop(rule_id, None)

    def enable_rule(self, rule_id: str):
        with self._lock:
            if rule_id in self.rules:
                self.rules[rule_id].enabled = True

    def disable_rule(self, rule_id: str):
        with self._lock:
            if rule_id in self.rules:
                self.rules[rule_id].enabled = False

    def get_rules(self) -> List[ObservationRule]:
        with self._lock:
            return list(self.rules.values())

    # ── 生命周期 ──

    def start(self):
        """启动所有观察器"""
        if self._running:
            self._log("⚠️ 引擎已在运行")
            return
        self._running = True
        self._log(f"🚀 主动观察引擎 v{VERSION} 启动")

        # 启动六类观察器（每类独立线程）
        observers = [
            ("文件系统", self._file_observer_loop),
            ("网络状态", self._network_observer_loop),
            ("定时事件", self._time_observer_loop),
            ("进程事件", self._process_observer_loop),
            ("资源告警", self._resource_observer_loop),
            ("跨设备", self._cross_device_observer_loop),
        ]

        for name, loop_fn in observers:
            t = threading.Thread(target=loop_fn, name=f"obs-{name}", daemon=True)
            t.start()
            self._observers.append(t)
            self._log(f"  └─ {name}观察器已启动")

        self._log(f"✅ 全部 {len(observers)} 个观察器已激活")

    def stop(self):
        """停止所有观察器"""
        self._running = False
        for t in self._observers:
            t.join(timeout=5)
        self._observers.clear()
        self._save_state()
        self._log("🛑 主动观察引擎已停止")

    # ═══════════════════════════════════════════════════════
    # 观察器循环（6个独立线程）
    # ═══════════════════════════════════════════════════════

    def _file_observer_loop(self):
        """文件系统观察器 — 每10秒扫描一次"""
        interval = 10
        while self._running:
            try:
                self._scan_file_changes()
            except Exception as e:
                self._log(f"❌ 文件观察异常: {e}")
            time.sleep(interval)

    def _network_observer_loop(self):
        """网络状态观察器 — 每30秒检查连接"""
        interval = 30
        last_status = self._check_network()
        while self._running:
            try:
                current = self._check_network()
                if current != last_status:
                    if current:
                        self._trigger(TriggerType.NETWORK_CHANGE, "reconnected", {
                            "status": "connected", "previous": last_status,
                        })
                    else:
                        self._trigger(TriggerType.NETWORK_CHANGE, "disconnected", {
                            "status": "disconnected", "previous": last_status,
                        })
                    last_status = current
            except Exception as e:
                self._log(f"❌ 网络观察异常: {e}")
            time.sleep(interval)

    def _time_observer_loop(self):
        """定时事件观察器 — 每60秒检查cron式调度"""
        interval = 60
        while self._running:
            try:
                self._check_time_events()
            except Exception as e:
                self._log(f"❌ 定时事件异常: {e}")
            time.sleep(interval)

    def _process_observer_loop(self):
        """进程事件观察器 — 每30秒检查龍魂进程"""
        interval = 30
        while self._running:
            try:
                self._check_processes()
            except Exception as e:
                self._log(f"❌ 进程观察异常: {e}")
            time.sleep(interval)

    def _resource_observer_loop(self):
        """资源告警观察器 — 每60秒检查系统资源"""
        interval = 60
        while self._running:
            try:
                self._check_resources()
            except Exception as e:
                self._log(f"❌ 资源观察异常: {e}")
            time.sleep(interval)

    def _cross_device_observer_loop(self):
        """跨设备同步观察器 — 每120秒检查鲲鹏可达性"""
        interval = 120
        while self._running:
            try:
                self._check_cross_device()
            except Exception as e:
                self._log(f"❌ 跨设备观察异常: {e}")
            time.sleep(interval)

    # ═══════════════════════════════════════════════════════
    # 检测逻辑
    # ═══════════════════════════════════════════════════════

    def _scan_file_changes(self):
        """扫描文件系统变更（增量快照对比）"""
        watch_dirs = [
            PROJECT_ROOT / "bin",
            PROJECT_ROOT / "config",
            PROJECT_ROOT / "personas",
            PROJECT_ROOT / "integrations",
        ]
        for watch_dir in watch_dirs:
            if not watch_dir.exists():
                continue
            for fpath in watch_dir.rglob("*"):
                if not fpath.is_file():
                    continue
                key = str(fpath)
                try:
                    stat = fpath.stat()
                    mtime = stat.st_mtime
                except OSError:
                    continue

                if key not in self._file_snapshots:
                    # 新文件
                    self._file_snapshots[key] = (mtime, "")
                    self._trigger(TriggerType.FILE_CHANGE, str(fpath), {
                        "event": "created", "file": key, "size": stat.st_size,
                    })
                elif self._file_snapshots[key][0] != mtime:
                    # 已修改
                    self._file_snapshots[key] = (mtime, "")
                    self._trigger(TriggerType.FILE_CHANGE, str(fpath), {
                        "event": "modified", "file": key, "size": stat.st_size,
                    })

        # 检测删除
        removed = set(self._file_snapshots.keys()) - {
            str(p) for wd in watch_dirs if wd.exists()
            for p in wd.rglob("*") if p.is_file()
        }
        for key in removed:
            self._file_snapshots.pop(key, None)
            self._trigger(TriggerType.FILE_CHANGE, key, {"event": "deleted", "file": key})

    def _check_network(self) -> bool:
        """检查网络连接"""
        try:
            socket.create_connection(("119.13.90.27", 22), timeout=5)
            return True
        except OSError:
            pass
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def _check_time_events(self):
        """检查定时事件（简化cron匹配）"""
        now = datetime.now()
        # 每小时整点触发健康检查
        if now.minute == 0:
            self._trigger(TriggerType.TIME_EVENT, "hourly", {
                "time": now.isoformat(), "event": "hourly_health_check",
            })
        # 每日凌晨3点触发审计
        if now.hour == 3 and now.minute == 0:
            self._trigger(TriggerType.TIME_EVENT, "daily_audit", {
                "time": now.isoformat(), "event": "daily_audit",
            })

    def _check_processes(self):
        """检查龍魂关键进程"""
        key_procs = ["longhun-api", "longhun-portal", "longhun-dashboard", "python"]
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = " ".join(proc.info['cmdline'] or [])
                for kp in key_procs:
                    if kp in cmdline:
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def _check_resources(self):
        """检查系统资源"""
        # 内存
        mem = psutil.virtual_memory()
        if mem.percent > 85:
            self._trigger(TriggerType.RESOURCE_ALERT, "memory>85%", {
                "resource": "memory", "percent": mem.percent,
                "used_gb": mem.used / (1024**3), "total_gb": mem.total / (1024**3),
            })
        # 磁盘
        disk = psutil.disk_usage("/")
        if disk.percent > 90:
            self._trigger(TriggerType.RESOURCE_ALERT, "disk>90%", {
                "resource": "disk", "percent": disk.percent,
                "used_gb": disk.used / (1024**3), "total_gb": disk.total / (1024**3),
            })
        elif disk.percent > 80:
            self._log(f"⚠️ 磁盘使用 {disk.percent}% — 接近阈值")
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        if cpu > 95:
            self._trigger(TriggerType.RESOURCE_ALERT, "cpu>95%", {
                "resource": "cpu", "percent": cpu,
            })

    def _check_cross_device(self):
        """检查鲲鹏可达性"""
        kunpeng_ip = "119.13.90.27"
        try:
            socket.create_connection((kunpeng_ip, 22), timeout=10)
        except OSError:
            self._trigger(TriggerType.CROSS_DEVICE, "kunpeng:unreachable", {
                "device": "kunpeng", "ip": kunpeng_ip, "status": "unreachable",
            })

    # ═══════════════════════════════════════════════════════
    # 触发与执行
    # ═══════════════════════════════════════════════════════

    def _trigger(self, trigger_type: TriggerType, match_key: str, event_data: Dict[str, Any]):
        """统一触发入口 — 匹配规则 → 阈值检查 → 执行动作"""
        # 重置小时计数器
        self._reset_hourly_counters()

        for rule_id, rule in self.rules.items():
            if rule.trigger_type != trigger_type:
                continue

            # 模式匹配
            if not self._match_pattern(rule.pattern, match_key):
                continue

            # 阈值检查
            can, reason = rule.can_trigger()
            if not can:
                self._log(f"⏸️ {rule_id}: {reason}", level="debug")
                continue

            # 记录触发
            with self._lock:
                rule.record_trigger()
                self._hourly_counters[rule_id] = self._hourly_counters.get(rule_id, 0) + 1

            # 升级检查
            if rule.should_escalate():
                self._log(f"🚨 {rule_id}: 连续触发{rule.consecutive_triggers}次，升级！")

            # 执行动作
            self._execute_action(rule, match_key, event_data)

            # 发布到 EventBus
            self._publish_to_bus(rule, trigger_type, event_data)

        # 如果无规则匹配，至少记录日志
        if not any(r.trigger_type == trigger_type and self._match_pattern(r.pattern, match_key)
                   for r in self.rules.values()):
            self._log(f"📝 [无规则] {trigger_type.value}: {match_key}")

    def _match_pattern(self, pattern: str, target: str) -> bool:
        """模式匹配"""
        if pattern == "*":
            return True
        # glob 匹配
        if "*" in pattern or "?" in pattern:
            import fnmatch
            return fnmatch.fnmatch(target, pattern)
        # 子串匹配
        return pattern.lower() in target.lower()

    def _execute_action(self, rule: ObservationRule, match_key: str, event_data: Dict[str, Any]):
        """执行动作"""
        action = rule.action
        self._log(f"⚡ {rule.rule_id}: {action.value} ← {match_key}")

        if action == ActionType.LOG:
            self._write_obs_log(rule, event_data)
        elif action == ActionType.ALERT:
            self._send_alert(rule, event_data)
        elif action == ActionType.EXECUTE:
            self._auto_execute(rule, event_data)
        elif action == ActionType.ARCHIVE:
            self._auto_archive(rule, event_data)
        elif action == ActionType.FUSE:
            self._trigger_fuse(rule, event_data)
        elif action == ActionType.NOTIFY:
            self._notify_master(rule, event_data)

    def _auto_execute(self, rule: ObservationRule, event_data: Dict[str, Any]):
        """自动执行脚本"""
        if not rule.action_script:
            return
        self._log(f"  → 执行: {rule.action_script}")
        try:
            from lh_secure_subprocess import safe_shell_cmd
            result = safe_shell_cmd(
                rule.action_script, caller='lh_observer', timeout=120
            )
            if result.returncode != 0:
                self._log(f"  ❌ 执行失败 (code={result.returncode}): {result.stderr[:200]}")
            else:
                self._log(f"  ✅ 执行成功: {result.stdout[:100].strip()}")
        except subprocess.TimeoutExpired:
            self._log(f"  ⏰ 执行超时: {rule.action_script}")
        except Exception as e:
            self._log(f"  ❌ 执行异常: {e}")

    def _publish_to_bus(self, rule: ObservationRule, trigger_type: TriggerType, event_data: Dict[str, Any]):
        """发布事件到 EventBus"""
        type_map = {
            TriggerType.FILE_CHANGE: EventType.HOOK_TRIGGERED,
            TriggerType.NETWORK_CHANGE: EventType.HOOK_TRIGGERED,
            TriggerType.TIME_EVENT: EventType.CHAIN_STEP,
            TriggerType.PROCESS_EVENT: EventType.HOOK_TRIGGERED,
            TriggerType.RESOURCE_ALERT: EventType.FUSE_TRIGGERED,
            TriggerType.CROSS_DEVICE: EventType.HOOK_TRIGGERED,
        }
        evt_type = type_map.get(trigger_type, EventType.HOOK_TRIGGERED)
        self._event_bus.publish(
            event_type=evt_type,
            source=f"ActiveObservation.{rule.rule_id}",
            dna_trace=rule.dna_signature,
            payload={
                "rule_id": rule.rule_id,
                "trigger_type": trigger_type.value,
                "action": rule.action.value,
                **event_data,
            },
        )

    # ── EventBus 回调 ──

    def _on_file_observed(self, event: Event):
        pass  # 由内部处理，此处为外部订阅者回调

    def _on_network_alert(self, event: Event):
        pass

    def _on_resource_alert(self, event: Event):
        pass

    # ── 辅助方法 ──

    def _send_alert(self, rule: ObservationRule, data: Dict[str, Any]):
        """发送告警（对接 Bark/飞书）"""
        alert_msg = f"[龍魂·主动观察] {rule.rule_id}: {rule.description}\n{json.dumps(data, ensure_ascii=False, indent=2)}"
        self._log(f"🚨 告警: {alert_msg[:200]}")
        # TODO: 对接 Bark推送 + 飞书Webhook
        # from deploy.scripts.health_check import send_bark_alert
        # send_bark_alert(alert_msg)

    def _auto_archive(self, rule: ObservationRule, data: Dict[str, Any]):
        """自动归档"""
        archive_file = OBS_DIR / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump({
                "rule_id": rule.rule_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": data,
                "dna": rule.dna_signature,
            }, f, ensure_ascii=False, indent=2)
        self._log(f"📦 已归档: {archive_file.name}")

    def _trigger_fuse(self, rule: ObservationRule, data: Dict[str, Any]):
        """触发熔断"""
        self._log(f"🔥 熔断触发: {rule.rule_id}")
        # TODO: 对接 lh_fuse_response.py

    def _notify_master(self, rule: ObservationRule, data: Dict[str, Any]):
        """通知 UID9622"""
        self._log(f"📢 通知主人: {rule.description}")
        # TODO: 对接通知渠道

    def _write_obs_log(self, rule: ObservationRule, data: Dict[str, Any]):
        """写观察日志"""
        log_file = OBS_DIR / "observation_log.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "rule_id": rule.rule_id,
                "trigger_type": rule.trigger_type.value,
                "action": rule.action.value,
                "data": data,
                "dna": rule.dna_signature,
            }, ensure_ascii=False) + '\n')

    def _reset_hourly_counters(self):
        """每小时重置计数器"""
        now = time.time()
        if now - self._last_counter_reset > 3600:
            self._hourly_counters.clear()
            for rule in self.rules.values():
                rule.trigger_count = 0
            self._last_counter_reset = now

    def _save_state(self):
        """保存引擎状态"""
        state = {
            "version": VERSION,
            "dna": DNA,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "rules": {
                rid: {
                    "enabled": r.enabled,
                    "trigger_count": r.trigger_count,
                    "last_triggered": r.last_triggered,
                    "dna": r.dna_signature,
                } for rid, r in self.rules.items()
            },
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def save_rules(self):
        """持久化规则到文件"""
        rules_data = []
        for r in self.rules.values():
            rules_data.append({
                "rule_id": r.rule_id,
                "trigger_type": r.trigger_type.value,
                "pattern": r.pattern,
                "action": r.action.value,
                "action_script": r.action_script,
                "enabled": r.enabled,
                "description": r.description,
                "threshold": asdict(r.threshold),
                "dna_signature": r.dna_signature,
            })
        with open(RULES_FILE, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, ensure_ascii=False, indent=2)
        self._log(f"💾 规则已保存: {len(rules_data)} 条")

    def load_rules(self):
        """从文件加载规则"""
        if not RULES_FILE.exists():
            return
        with open(RULES_FILE, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
        for r in rules_data:
            rule = ObservationRule(
                rule_id=r["rule_id"],
                trigger_type=TriggerType(r["trigger_type"]),
                pattern=r["pattern"],
                action=ActionType(r["action"]),
                action_script=r.get("action_script", ""),
                threshold=ObsThreshold(**r.get("threshold", {})),
                enabled=r.get("enabled", True),
                description=r.get("description", ""),
                dna_signature=r.get("dna_signature", ""),
            )
            self.rules[rule.rule_id] = rule
        self._log(f"📂 已加载 {len(self.rules)} 条规则")

    def _log(self, msg: str, level: str = "info"):
        prefix = {"debug": "🔍", "info": "  ", "warn": "⚠️", "error": "❌"}.get(level, "  ")
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[obs {ts}] {prefix} {msg}")

    # ── 状态查询 ──

    def get_status(self) -> Dict[str, Any]:
        """获取引擎运行状态"""
        return {
            "running": self._running,
            "version": VERSION,
            "dna": DNA,
            "rules_count": len(self.rules),
            "active_rules": sum(1 for r in self.rules.values() if r.enabled),
            "observer_threads": len(self._observers),
            "event_bus_events": len(self._event_bus.event_log),
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "rules": {
                rid: {
                    "enabled": r.enabled,
                    "trigger_count": r.trigger_count,
                    "last_triggered": datetime.fromtimestamp(r.last_triggered).isoformat() if r.last_triggered else None,
                    "consecutive": r.consecutive_triggers,
                } for rid, r in self.rules.items()
            },
            "file_snapshots": len(self._file_snapshots),
            "hourly_counters": dict(self._hourly_counters),
        }


# ═══════════════════════════════════════════════════════════
# 单例入口
# ═══════════════════════════════════════════════════════════

_engine_instance: Optional[ActiveObservationEngine] = None


def get_observation_engine() -> ActiveObservationEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ActiveObservationEngine()
    return _engine_instance


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 主动观察引擎 v2.0")
    parser.add_argument("--daemon", action="store_true", help="后台守护模式运行")
    parser.add_argument("--once", action="store_true", help="执行一次扫描后退出")
    parser.add_argument("--status", action="store_true", help="查看引擎状态")
    parser.add_argument("--rules", action="store_true", help="列出所有规则")
    parser.add_argument("--save-rules", action="store_true", help="保存规则到文件")
    parser.add_argument("--load-rules", action="store_true", help="从文件加载规则")
    parser.add_argument("--enable", type=str, help="启用指定规则ID")
    parser.add_argument("--disable", type=str, help="禁用指定规则ID")
    args = parser.parse_args()

    engine = get_observation_engine()

    if args.load_rules:
        engine.load_rules()
        return
    if args.save_rules:
        engine.save_rules()
        return

    engine.load_default_rules()

    if args.status:
        status = engine.get_status()
        stats = engine.get_stats()
        print(json.dumps({"status": status, "stats": stats}, ensure_ascii=False, indent=2))
        return

    if args.rules:
        for r in engine.get_rules():
            status_icon = "🟢" if r.enabled else "🔴"
            print(f"{status_icon} {r.rule_id:30s} [{r.trigger_type.value:16s}] {r.action.value:8s} | {r.description}")
        return

    if args.enable:
        engine.enable_rule(args.enable)
        print(f"✅ 已启用: {args.enable}")
        return
    if args.disable:
        engine.disable_rule(args.disable)
        print(f"🔴 已禁用: {args.disable}")
        return

    # 默认：启动运行
    engine.start()

    if args.once:
        time.sleep(5)  # 等一轮扫描
        engine.stop()
        return

    # 守护模式
    try:
        while engine._running:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n⏹️  收到中断信号")
    finally:
        engine.stop()


if __name__ == "__main__":
    main()
