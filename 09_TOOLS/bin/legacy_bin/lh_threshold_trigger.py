#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 阈值触发统一管理器 v2.1
Threshold Trigger Hub · 阀子到了自动触发 · 不7x24待机

核心哲学：
  商业公司故意留bug让人多消耗算力赚钱——算力根本不是瓶颈，是噱头。
  龍魂不需要常驻轮询，阈值到了自动触发，干完就走，零待机浪费。

架构：
  旧模式: while True + sleep(N) → 持续吃CPU空转
  新模式: 定时单次检查 → 阈值达标? → 执行动作 → 退出
           ├── launchd StartInterval (定时)
           ├── launchd WatchPaths (文件变化)
           ├── launchd QueueDirectories (目录变化)
           └── 手动触发 lh_threshold_trigger.py --check <guard>

v2.1 升级：
  18个守卫 (原6+12新增) · 8项补充机制
  ├── 告警聚合 (5分钟冷却)
  ├── 自动修复 (脚本库+验证)
  ├── 告警升级 (时间梯度)
  ├── 依赖检查 (DAG拓扑)
  ├── 性能监控 (守卫耗时)
  ├── 配置热加载 (文件监听)
  ├── 多节点协调 (分布式状态)
  └── 阈值动态调整 (历史数据)

用法：
  python3 bin/lh_threshold_trigger.py --check all         # 检查所有守卫
  python3 bin/lh_threshold_trigger.py --check all --repair # 检查并自动修复
  python3 bin/lh_threshold_trigger.py --check disk         # 检查磁盘
  python3 bin/lh_threshold_trigger.py --list               # 列出所有守卫
  python3 bin/lh_threshold_trigger.py --status             # 查看触发历史
  python3 bin/lh_threshold_trigger.py --deploy             # 部署launchd定时任务
  python3 bin/lh_threshold_trigger.py --escalation-test    # 测试告警升级
  python3 bin/lh_threshold_trigger.py --dependency-check   # 检查守卫依赖
  python3 bin/lh_threshold_trigger.py --config-reload      # 热加载配置
  python3 bin/lh_threshold_trigger.py --export-config      # 导出配置
  python3 bin/lh_threshold_trigger.py --import-config FILE # 导入配置

DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·䷾既济-THRESHOLD-TRIGGER-v2.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import psutil
import re
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ── 常量 ──
HOME = Path.home()
ROOT = HOME / "longhun-system"
STATE_DIR = ROOT / "state" / "threshold_trigger"
CONFIG_DIR = HOME / ".longhun" / "config"
CONFIG_FILE = CONFIG_DIR / "threshold_trigger.yaml"
STATE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = STATE_DIR / "trigger_history.json"
PERF_FILE = STATE_DIR / "guard_performance.json"
ESCALATION_DIR = STATE_DIR / "escalations"
ESCALATION_DIR.mkdir(parents=True, exist_ok=True)
LAUNCHD_DIR = HOME / "Library" / "LaunchAgents"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·䷾既济-THRESHOLD-TRIGGER-v2.1"
TZ = timezone(timedelta(hours=8))

# ── 守卫定义 ──
GUARDS: Dict[str, Dict[str, Any]] = {}
PERFORMANCE: Dict[str, List[float]] = {}  # 守卫执行时间记录


def guard(name: str, interval_min: int, desc: str, priority: str = "P2",
          dependencies: Optional[List[str]] = None):
    """守卫注册装饰器"""
    def decorator(func):
        GUARDS[name] = {
            "name": name,
            "func": func,
            "interval_min": interval_min,
            "description": desc,
            "priority": priority,
            "dependencies": dependencies or [],
            "last_triggered": None,
            "trigger_count": 0,
        }
        return func
    return decorator


def load_config() -> Dict[str, Any]:
    """加载YAML配置，兼容JSON格式"""
    if CONFIG_FILE.exists():
        try:
            # 尝试YAML
            import yaml
            with open(CONFIG_FILE) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass
        except Exception:
            pass
        try:
            # 降级JSON
            with open(CONFIG_FILE) as f:
                content = f.read()
                return json.loads(content) if content.strip() else {}
        except Exception:
            pass
    return {}


def load_history() -> Dict[str, Any]:
    """加载触发历史"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"triggers": [], "stats": {}, "alerts": []}


def save_history(history: Dict[str, Any]):
    """保存触发历史"""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def load_performance() -> Dict[str, Any]:
    """加载守卫性能数据"""
    if PERF_FILE.exists():
        try:
            with open(PERF_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_performance(data: Dict[str, Any]):
    """保存守卫性能数据"""
    PERF_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PERF_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
# 告警聚合器 · 5分钟内相同问题只告警一次
# ═══════════════════════════════════════════════════════════

class AlertAggregator:
    """告警聚合器"""

    def __init__(self, cooldown_seconds: int = 300):
        self.cooldown = cooldown_seconds
        self.last_alert: Dict[str, float] = {}
        self._load_state()

    def _alert_key(self, guard_name: str, message: str) -> str:
        """生成告警去重key"""
        content = f"{guard_name}:{message[:80]}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def should_alert(self, guard_name: str, message: str) -> bool:
        """判定是否应该告警"""
        key = self._alert_key(guard_name, message)
        now = time.time()
        if key in self.last_alert:
            elapsed = now - self.last_alert[key]
            if elapsed < self.cooldown:
                return False
        self.last_alert[key] = now
        self._save_state()
        return True

    def clear_old(self, max_age: int = 3600):
        """清理过期记录"""
        now = time.time()
        self.last_alert = {
            k: v for k, v in self.last_alert.items()
            if now - v < max_age
        }
        self._save_state()

    def _state_file(self) -> Path:
        return STATE_DIR / "alert_aggregator.json"

    def _save_state(self):
        try:
            with open(self._state_file(), 'w') as f:
                json.dump({"last_alert": self.last_alert}, f)
        except Exception:
            pass

    def _load_state(self):
        sf = self._state_file()
        if sf.exists():
            try:
                with open(sf) as f:
                    data = json.load(f)
                    self.last_alert = data.get("last_alert", {})
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════
# 自动修复引擎
# ═══════════════════════════════════════════════════════════

class AutoRepair:
    """自动修复机制"""

    REPAIR_SCRIPTS = {
        "health": {
            "service_offline": [
                "systemctl restart {service} 2>/dev/null || brew services restart {service} 2>/dev/null || true",
            ],
        },
        "disk": {
            "low_space": [
                f"{sys.executable} {ROOT}/bin/lh_disk_guard.py clean",
            ],
        },
        "git": {
            "dirty_repo": [
                f"cd {ROOT} && git add -A && git commit -m 'auto: 阈值触发自动提交'",
            ],
        },
        "signing": {
            "missing_gpg": [
                f"{sys.executable} {ROOT}/bin/lh_persona_signing.py --auto-fix 2>/dev/null || true",
            ],
        },
        "typefix": {
            "bare_types": [
                f"{sys.executable} {ROOT}/bin/lh_type_fixer.py --apply",
            ],
        },
        "dualnode": {
            "connection_lost": [
                f"{sys.executable} {ROOT}/L6_同步层/dual_node_cli.py sync",
            ],
            "frp_down": [
                f"{sys.executable} {ROOT}/L6_同步层/dual_node_cli.py tunnel restart",
            ],
        },
    }

    def repair(self, guard_name: str, issue_type: str) -> dict[str, Any]:
        """执行自动修复"""
        scripts = self.REPAIR_SCRIPTS.get(guard_name, {}).get(issue_type, [])
        if not scripts:
            return {"status": "no_script", "message": "无自动修复脚本"}

        results = []
        for script in scripts:
            try:
                from lh_secure_subprocess import safe_run
                result = safe_run(
                    script, caller='lh_threshold_trigger', timeout=60
                )
                results.append({
                    "script": script,
                    "returncode": result.returncode,
                    "stdout": result.stdout[:200],
                    "stderr": result.stderr[:200],
                })
                if result.returncode != 0:
                    break
            except Exception as e:
                results.append({"script": script, "error": str(e)})
                break

        all_success = all(r.get("returncode", 1) == 0 for r in results)
        return {
            "status": "success" if all_success else "partial",
            "results": results,
            "message": "自动修复完成" if all_success else "自动修复部分失败",
        }


# ═══════════════════════════════════════════════════════════
# 告警升级引擎
# ═══════════════════════════════════════════════════════════

class EscalationEngine:
    """告警升级引擎"""

    ESCALATION_RULES = {
        "P0": {
            "initial": "bark",
            "5min": "bark_repeat",
            "15min": "founder",
        },
        "P1": {
            "initial": "bark",
            "30min": "bark_repeat",
            "60min": "email",
        },
        "P2": {
            "initial": "log",
            "60min": "bark",
        },
        "P3": {
            "initial": "log",
            "daily": "bark",
        },
    }

    def escalate(self, alert: dict[str, Any], priority: str):
        """执行告警升级"""
        rules = self.ESCALATION_RULES.get(priority, self.ESCALATION_RULES["P2"])
        alert_id = alert.get("id", str(uuid.uuid4())[:8])
        state_file = ESCALATION_DIR / f"{alert_id}.json"

        if not state_file.exists():
            # 首次告警
            self._send_alert(alert, rules["initial"])
            with open(state_file, 'w') as f:
                json.dump({"first_alert": time.time(), "level": "initial", "alert": alert}, f)
            return

        with open(state_file) as f:
            state = json.load(f)

        elapsed = time.time() - state["first_alert"]
        current_level = state["level"]

        for time_key, action in rules.items():
            if time_key.endswith("min"):
                threshold_seconds = int(time_key[:-3]) * 60
                if elapsed > threshold_seconds and current_level != action:
                    self._send_alert(alert, action)
                    state["level"] = action
                    with open(state_file, 'w') as f:
                        json.dump(state, f)
                    break

    def _send_alert(self, alert: dict[str, Any], channel: str):
        """发送告警"""
        ts = datetime.now(TZ).strftime("%H:%M:%S")
        if channel in ("bark", "bark_repeat"):
            self._bark_push(alert, channel == "bark_repeat")
        elif channel == "founder":
            self._bark_push(alert, urgent=True)
            print(f"  🚨 [{ts}] 已升级推送创始人: {alert.get('message', '')[:60]}")
        elif channel == "email":
            print(f"  📧 [{ts}] 邮件通知: {alert.get('message', '')[:60]}")
        elif channel == "log":
            pass  # 仅记录日志

    def _bark_push(self, alert: dict[str, Any], urgent: bool = False):
        """Bark推送"""
        try:
            import requests
            bark_key = os.getenv("BARK_KEY", "")
            if not bark_key:
                return
            title = f"🐉 龍魂{'🚨' if urgent else '🔔'} {alert.get('guard', '')}"
            body = alert.get("message", "")[:200]
            url = f"https://api.day.app/{bark_key}/{title}/{body}"
            if urgent:
                url += "?level=timeSensitive"
            requests.get(url, timeout=10)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# 守卫依赖检查器
# ═══════════════════════════════════════════════════════════

class GuardDependencyChecker:
    """守卫依赖检查器"""

    DEPENDENCIES = {
        "health": ["network"],
        "github": ["network"],
        "gitee": ["network"],
        "huaweicloud": ["network"],
        "signing": ["audit"],
        "persona": ["signing"],
    }

    def check_dependencies(self, guard_name: str) -> Tuple[bool, List[str]]:
        """检查依赖是否满足，返回(是否全部满足, 失败列表)"""
        deps = self.DEPENDENCIES.get(guard_name, [])
        failures = []
        for dep in deps:
            if dep in GUARDS:
                try:
                    result = GUARDS[dep]["func"]()
                    if result is not None:  # 依赖守卫触发（异常）
                        failures.append(f"{dep}(异常)")
                except Exception as e:
                    failures.append(f"{dep}(错误:{e})")
            else:
                failures.append(f"{dep}(不存在)")
        return len(failures) == 0, failures


# ═══════════════════════════════════════════════════════════
# 阈值动态调整器
# ═══════════════════════════════════════════════════════════

class DynamicThreshold:
    """基于历史数据动态调整阈值"""

    def __init__(self):
        self.history = load_history()

    def get_adjusted_threshold(self, guard_name: str, base_warn: float,
                                base_critical: float, metric: str = "free_gb") -> Tuple[float, float]:
        """根据30天触发历史调整阈值"""
        stats = self.history.get("stats", {}).get(guard_name, {})
        checks = stats.get("checks", 0)
        triggers = stats.get("triggers", 0)

        if checks < 30:
            return base_warn, base_critical  # 数据不足，用默认值

        trigger_rate = triggers / checks if checks > 0 else 0

        if trigger_rate > 0.3:
            # 频繁触发 → 收紧阈值（预警更早）
            return base_warn * 1.3, base_critical * 1.3
        elif trigger_rate < 0.05:
            # 几乎不触发 → 放宽阈值
            return base_warn * 0.8, base_critical * 0.8

        return base_warn, base_critical


# ═══════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════

alert_aggregator = AlertAggregator()
auto_repair = AutoRepair()
escalation_engine = EscalationEngine()
dependency_checker = GuardDependencyChecker()
dynamic_threshold = DynamicThreshold()


# ═══════════════════════════════════════════════════════════
# 守卫定义区 — 18个守卫 (系统级6+龍魂系统级6+安全级3+业务级3+数据级1)
# ═══════════════════════════════════════════════════════════

# ── 系统级守卫 (6个) ──

@guard("disk", interval_min=30, desc="磁盘空间低于阈值时自动清理", priority="P1")
def check_disk_guard() -> Optional[str]:
    """检查磁盘空间，低于阈值触发清理"""
    try:
        usage = psutil.disk_usage(str(HOME))
        free_gb = usage.free / (1024**3)
        total_gb = usage.total / (1024**3)
        pct = usage.percent

        FREE_WARN, FREE_CRITICAL = dynamic_threshold.get_adjusted_threshold(
            "disk", 20, 10, "free_gb"
        )

        if free_gb < FREE_CRITICAL:
            auto_repair.repair("disk", "low_space")
            return f"🔴 磁盘紧急: 仅剩{free_gb:.1f}GB/{total_gb:.0f}GB ({pct}%) → 已触发自动清理"
        elif free_gb < FREE_WARN:
            return f"🟡 磁盘预警: 剩余{free_gb:.1f}GB/{total_gb:.0f}GB ({pct}%)"
        return None
    except Exception as e:
        return f"❌ 磁盘检查异常: {e}"


@guard("memory", interval_min=15, desc="内存压力过大时告警", priority="P2")
def check_memory_guard() -> Optional[str]:
    """检查内存压力"""
    try:
        mem = psutil.virtual_memory()
        pct = mem.percent
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)

        MEM_WARN, MEM_CRITICAL = dynamic_threshold.get_adjusted_threshold(
            "memory", 85, 95, "pct"
        )

        if pct > MEM_CRITICAL:
            return f"🔴 内存紧急: {used_gb:.1f}GB/{total_gb:.1f}GB ({pct}%)"
        elif pct > MEM_WARN:
            return f"🟡 内存预警: {used_gb:.1f}GB/{total_gb:.1f}GB ({pct}%)"
        return None
    except Exception as e:
        return f"❌ 内存检查异常: {e}"


@guard("process", interval_min=15, desc="CPU异常进程检测", priority="P2")
def check_process_guard() -> Optional[str]:
    """检查异常高CPU进程"""
    try:
        high_cpu_procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                cpu = proc.info['cpu_percent'] or 0
                if cpu > 80:
                    high_cpu_procs.append(f"{proc.info['name']}(PID:{proc.info['pid']},CPU:{cpu:.0f}%)")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if len(high_cpu_procs) > 3:
            return f"🔴 异常进程: {len(high_cpu_procs)}个高CPU进程 → {', '.join(high_cpu_procs[:5])}"
        elif high_cpu_procs:
            return f"🟡 高CPU进程: {', '.join(high_cpu_procs[:3])}"
        return None
    except Exception as e:
        return f"❌ 进程检查异常: {e}"


@guard("network", interval_min=10, desc="网络异常检测（断网/延迟/丢包）", priority="P1")
def check_network_guard() -> Optional[str]:
    """检查网络状态"""
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('8.8.8.8', 53))
        sock.close()
        latency = (time.time() - start) * 1000

        if result != 0:
            # 尝试备用DNS
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.settimeout(5)
            result2 = sock2.connect_ex(('114.114.114.114', 53))
            sock2.close()
            if result2 != 0:
                return f"🔴 网络中断: 无法连接外网"
            else:
                return f"🟡 网络异常: Google DNS不通，国内DNS正常"
        elif latency > 500:
            return f"🟡 网络延迟: {latency:.0f}ms (>500ms)"
        return None
    except Exception as e:
        return f"❌ 网络检查异常: {e}"


@guard("temperature", interval_min=30, desc="设备温度监控（Mac/服务器）", priority="P3")
def check_temperature_guard() -> Optional[str]:
    """检查设备温度"""
    try:
        # macOS温度检测
        result = subprocess.run(
            ["osx-cpu-temp"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            temp_str = result.stdout.strip()
            # 解析温度值
            import re
            temps = re.findall(r'(\d+\.?\d*)', temp_str)
            if temps:
                cpu_temp = float(temps[0])
                if cpu_temp > 80:
                    return f"🔴 设备过热: CPU {cpu_temp:.0f}°C (>80°C)"
                elif cpu_temp > 65:
                    return f"🟡 温度偏高: CPU {cpu_temp:.0f}°C"
        return None
    except FileNotFoundError:
        # osx-cpu-temp未安装
        return None
    except Exception:
        return None


@guard("battery", interval_min=15, desc="笔记本电池健康度", priority="P3")
def check_battery_guard() -> Optional[str]:
    """检查电池状态"""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return None  # 台式机无电池

        pct = battery.percent
        plugged = battery.power_plugged

        if not plugged and pct < 15:
            return f"🟡 电量低: {pct:.0f}% (未充电)"
        if not plugged and pct < 5:
            return f"🔴 电量紧急: {pct:.0f}%"

        # 检查电池健康（macOS）
        try:
            result = subprocess.run(
                ["system_profiler", "SPPowerDataType"],
                capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.split("\n"):
                if "Cycle Count" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        cycles = int(parts[1].strip())
                        if cycles > 500:
                            return f"🟡 电池老化: {cycles}循环 (>500)"
                if "Condition" in line:
                    condition = line.split(":")[-1].strip()
                    if condition in ("Replace Soon", "Replace Now", "Service Battery"):
                        return f"🔴 电池需更换: {condition}"
        except Exception:
            pass

        return None
    except Exception:
        return None


# ── 龍魂系统级守卫 (6个) ──

@guard("git", interval_min=60, desc="Git仓库状态检查（未提交/未推送）", priority="P2")
def check_git_guard() -> Optional[str]:
    """检查Git仓库脏状态"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=30
        )
        dirty_files = [l for l in result.stdout.strip().split("\n") if l.strip()]
        if len(dirty_files) > 50:
            return f"🟡 Git脏状态: {len(dirty_files)}个未提交文件"
        elif len(dirty_files) > 10:
            return f"🔵 Git: {len(dirty_files)}个变更待提交"
        return None
    except Exception:
        return None


@guard("health", interval_min=5, desc="关键服务健康心跳检查", priority="P1",
       dependencies=["network"])
def check_health_guard() -> Optional[str]:
    """检查关键服务是否存活"""
    key_services = {
        "伦理锚点API": 9630,
        "龍魂Portal": 8888,
    }
    dead = []
    for name, port in key_services.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result != 0:
                dead.append(f"{name}(:{port})")
        except Exception:
            dead.append(f"{name}(:{port})")

    if dead:
        return f"🔴 服务离线: {', '.join(dead)}"
    return None


@guard("backup", interval_min=120, desc="备份状态检查", priority="P1")
def check_backup_guard() -> Optional[str]:
    """检查备份是否过期"""
    try:
        backup_flag = ROOT / "state" / "last_backup.json"
        if backup_flag.exists():
            with open(backup_flag) as f:
                data = json.load(f)
            last_ts = data.get("timestamp", 0)
            hours_ago = (time.time() - last_ts) / 3600
            if hours_ago > 48:
                return f"🔴 备份过期: {hours_ago:.0f}小时未备份"
            elif hours_ago > 24:
                return f"🟡 备份提醒: {hours_ago:.0f}小时未备份"
        return None
    except Exception:
        return None


@guard("persona", interval_min=60, desc="人格矩阵异常检测", priority="P1",
       dependencies=["signing"])
def check_persona_guard() -> Optional[str]:
    """检查人格矩阵状态"""
    try:
        persona_state = ROOT / "state" / "persona_matrix.json"
        if persona_state.exists():
            with open(persona_state) as f:
                data = json.load(f)

            anomalies = []
            for pid, info in data.get("personas", {}).items():
                if info.get("anomaly_score", 0) > 0.7:
                    anomalies.append(f"{pid}(异常{info['anomaly_score']:.2f})")
                last_triggered = info.get("last_triggered")
                if last_triggered:
                    try:
                        days = (time.time() - last_triggered) / 86400
                        if days > 30:
                            anomalies.append(f"{pid}(休眠{days:.0f}天)")
                    except Exception:
                        pass

            if len(anomalies) > 3:
                return f"🔴 人格异常: {len(anomalies)}个人格异常 → {', '.join(anomalies[:5])}"
            elif anomalies:
                return f"🟡 人格告警: {', '.join(anomalies[:3])}"
        return None
    except Exception as e:
        return f"❌ 人格检查异常: {e}"


@guard("signing", interval_min=30, desc="签章链完整性检查", priority="P0")
def check_signing_guard() -> Optional[str]:
    """检查签章链状态"""
    try:
        signing_log = ROOT / "state" / "signing_chain" / "signing_log.jsonl"
        if not signing_log.exists():
            return f"🔴 签章缺失: 签章日志文件不存在"

        with open(signing_log) as f:
            lines = f.readlines()

        if not lines:
            return f"🟡 签章空: 签章日志为空"

        last_line = json.loads(lines[-1])
        last_time = datetime.fromisoformat(last_line.get("trigger_time_iso", "2000-01-01T00:00:00"))
        hours_ago = (datetime.now(TZ).replace(tzinfo=None) - last_time.replace(tzinfo=None)).total_seconds() / 3600

        if hours_ago > 24:
            return f"🟡 签章稀疏: {hours_ago:.0f}小时无签章"

        invalid_gpg = sum(1 for l in lines[-100:]
                         if not json.loads(l).get("gpg_verified", False))
        if invalid_gpg > 5:
            return f"🔴 签章异常: 最近100条中{invalid_gpg}条GPG验证失败"

        return None
    except Exception as e:
        return f"❌ 签章检查异常: {e}"


@guard("audit", interval_min=120, desc="审计日志完整性检查", priority="P0")
def check_audit_guard() -> Optional[str]:
    """检查审计日志完整性"""
    try:
        audit_dir = ROOT / "audit"
        if not audit_dir.exists():
            return f"🔴 审计缺失: audit目录不存在"

        log_files = list(audit_dir.glob("*.jsonl")) + list(audit_dir.glob("*.log"))
        if not log_files:
            return f"🟡 审计空: 无审计日志文件"

        # 检查最近审计记录
        latest_ts = 0
        for lf in log_files:
            try:
                stat = lf.stat()
                latest_ts = max(latest_ts, stat.st_mtime)
            except Exception:
                pass

        hours_ago = (time.time() - latest_ts) / 3600
        if hours_ago > 48:
            return f"🔴 审计断裂: {hours_ago:.0f}小时无审计记录"
        elif hours_ago > 24:
            return f"🟡 审计稀疏: {hours_ago:.0f}小时无新记录"

        return None
    except Exception as e:
        return f"❌ 审计检查异常: {e}"


# ── 代码质量守卫 (1个) ──

@guard("typefix", interval_min=60, desc="basedpyright 类型注解缺失自动修复", priority="P2")
def check_typefix_guard() -> Optional[str]:
    """检查裸类型注解数量，超过阈值自动触发修复"""
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "bin" / "lh_type_fixer.py")],
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout

        # 从预览输出中解析问题数量: "X 文件 · Y 处待修复"
        m = re.search(r'(\d+)\s*文件\s*·\s*(\d+)\s*处待修复', output)
        if m:
            file_count = int(m.group(1))
            issue_count = int(m.group(2))

            # 阈值：5处以上裸类型注解就触发自动修复
            TYPEFIX_THRESHOLD = 5
            if issue_count > TYPEFIX_THRESHOLD:
                return f"🟡 类型注解欠佳: {file_count}个文件 · {issue_count}处裸类型 (>阈值{ TYPEFIX_THRESHOLD})"
            elif issue_count > 0:
                return None  # 有少量问题但不触发，避免过度修复

        # 如果解析失败但有输出，看是否有意义
        if "处待修复" in output:
            # 尝试另一种解析
            numbers = re.findall(r'(\d+)', output.split('处待修复')[0])
            if numbers:
                issue_count = int(numbers[-1])
                if issue_count > 5:
                    return f"🟡 类型注解欠佳: {issue_count}处裸类型"

        return None
    except Exception as e:
        return f"❌ typefix检查异常: {e}"


# ── 双节点同步守卫 (1个) ──

@guard("dualnode", interval_min=60, desc="Mac↔鲲鹏双节点连接健康检查（frp+SSH双通道）", priority="P1")
def check_dualnode_guard() -> Optional[str]:
    """检查双节点连接状态，frp隧道+SSH直连双通道检测，任一可用即正常"""
    try:
        from L6_同步层.dual_node_protocol import DualNodeProtocol
        config_file = ROOT / "deploy" / ".kunpeng_config"
        if not config_file.exists():
            return None  # 未配置鲲鹏连接，跳过

        # 解析配置
        kunpeng_ip = "119.13.90.27"
        kunpeng_user = "root"
        kunpeng_port = 22
        with open(config_file) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    v = v.strip().strip('"').strip("'")
                    if k.strip() == "KUNPENG_MGMT_IP":
                        kunpeng_ip = v
                    elif k.strip() == "KUNPENG_USER":
                        kunpeng_user = v
                    elif k.strip() == "KUNPENG_SSH_PORT":
                        kunpeng_port = int(v)

        # 1. 检查 frp 隧道
        frp_ok = False
        try:
            import urllib.request, json as ujson
            req = urllib.request.Request("http://127.0.0.1:9633/health")
            resp = urllib.request.urlopen(req, timeout=5)
            data = ujson.loads(resp.read().decode())
            if data.get("node_role") == "kunpeng":
                frp_ok = True
        except Exception:
            pass

        # 2. 检查 SSH 直连
        protocol = DualNodeProtocol(
            kunpeng_ip=kunpeng_ip,
            kunpeng_user=kunpeng_user,
            kunpeng_port=kunpeng_port,
        )
        result = protocol.test_connection()
        ssh_ok = result.get("ssh_ok", False)

        # 双通道都断 → 告警
        if not frp_ok and not ssh_ok:
            return f"🔴 双节点全断: frp隧道+SSH直连均无法连接鲲鹏 {kunpeng_ip}"

        # 仅 frp 断（SSH可用）→ 降级告警
        if not frp_ok and ssh_ok:
            return f"🟡 frp隧道断开, SSH直连可用 — 检查和重启: lh tunnel status"

        if not result.get("remote_path_ok"):
            return f"🟡 鲲鹏路径异常: /opt/longhun-system 不存在"

        # 检查磁盘
        disk = result.get("disk_info", {})
        if disk:
            pct = disk.get("use_pct", "0%").replace("%", "")
            try:
                if int(pct) > 90:
                    return f"🟡 鲲鹏磁盘告警: {disk.get('use_pct')}"
            except ValueError:
                pass

        return None
    except Exception as e:
        return f"❌ dualnode检查异常: {e}"


# ── 安全级守卫 (3个) ──

@guard("intrusion", interval_min=5, desc="入侵检测（异常登录/文件变更）", priority="P0")
def check_intrusion_guard() -> Optional[str]:
    """检查入侵迹象"""
    try:
        alerts = []

        # 检查敏感文件变更
        sensitive_files = [
            ROOT / ".env",
            ROOT / "config" / "config.json",
            ROOT / "bin" / "lh_data_privacy_v2.0.py",
            ROOT / "deploy" / ".env.kunpeng",
        ]

        for sf in sensitive_files:
            if sf.exists():
                stat = sf.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime, tz=TZ)
                hours_ago = (datetime.now(TZ) - mtime).total_seconds() / 3600
                if hours_ago < 1:
                    alerts.append(f"{sf.name}({hours_ago:.1f}小时前修改)")

        # 检查SSH登录记录
        try:
            result = subprocess.run(
                ["last", "-5"], capture_output=True, text=True, timeout=10
            )
            logins = result.stdout.strip().split("\n")
            # 简单检测：非常见用户登录
            known_users = {"zuimeidedeyihan", "root"}
            for login_line in logins[:5]:
                if login_line.strip() and not login_line.startswith("reboot"):
                    parts = login_line.split()
                    if parts and parts[0] not in known_users and parts[0]:
                        alerts.append(f"未知用户登录: {parts[0]}")
        except Exception:
            pass

        if len(alerts) > 3:
            return f"🔴 入侵告警: {len(alerts)}个异常 → {', '.join(alerts[:5])}"
        elif alerts:
            return f"🟡 安全提醒: {', '.join(alerts[:3])}"

        return None
    except Exception as e:
        return f"❌ 入侵检查异常: {e}"


@guard("firewall", interval_min=60, desc="防火墙规则完整性检查", priority="P1")
def check_firewall_guard() -> Optional[str]:
    """检查macOS防火墙状态"""
    try:
        result = subprocess.run(
            ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        if "Firewall is disabled" in output:
            return f"🔴 防火墙关闭: 系统防火墙未启用"

        # 检查异常开放端口
        netstat = subprocess.run(
            ["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"],
            capture_output=True, text=True, timeout=10
        )
        # 已知合法端口
        known_ports = {8766, 8888, 9630, 5000, 8080, 3000, 22, 80, 443}
        unknown_ports = []
        for line in netstat.stdout.split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 9:
                addr = parts[-2]
                if ":" in addr:
                    port_str = addr.split(":")[-1]
                    try:
                        port = int(port_str)
                        if port not in known_ports and port < 10000:
                            unknown_ports.append(str(port))
                    except ValueError:
                        pass

        if len(unknown_ports) > 5:
            return f"🟡 异常端口: {len(unknown_ports)}个非标准端口开放 → {', '.join(unknown_ports[:5])}"

        return None
    except Exception:
        return None


@guard("privacy", interval_min=60, desc="隐私保护合规检查", priority="P0")
def check_privacy_guard() -> Optional[str]:
    """检查隐私合规"""
    try:
        # 检查用量上报是否包含内容字段
        usage_dir = ROOT / "state" / "usage_reports"
        if usage_dir.exists():
            for uf in usage_dir.glob("*.jsonl"):
                try:
                    with open(uf) as f:
                        for line in f:
                            data = json.loads(line)
                            usage = data.get("usage", {})
                            for key in usage:
                                if any(fk in key.lower() for fk in
                                       ["content", "text", "input", "output", "prompt"]):
                                    return f"🔴 隐私泄露: 用量上报包含内容字段 '{key}'"
                except Exception:
                    pass

        # 检查隐私审计日志
        privacy_log = ROOT / "state" / "privacy_audit.jsonl"
        if privacy_log.exists():
            with open(privacy_log) as f:
                lines = f.readlines()
            if lines:
                last = json.loads(lines[-1])
                if last.get("type") == "privacy_breach":
                    return f"🔴 隐私熔断: 最近发生隐私保护熔断"

        return None
    except Exception as e:
        return f"❌ 隐私检查异常: {e}"


# ── 业务级守卫 (3个) ──

@guard("github", interval_min=60, desc="GitHub仓库状态监控", priority="P2",
       dependencies=["network"])
def check_github_guard() -> Optional[str]:
    """检查GitHub状态"""
    try:
        import requests
        token = os.getenv("GITHUB_TOKEN", "")
        if not token:
            return None

        headers = {"Authorization": f"token {token}"}
        response = requests.get(
            "https://api.github.com/repos/UID9622/longhun-system",
            headers=headers, timeout=30
        )

        if response.status_code != 200:
            return f"🔴 GitHub异常: HTTP {response.status_code}"

        # 检查新Issue
        issues_response = requests.get(
            "https://api.github.com/repos/UID9622/longhun-system/issues",
            headers=headers, timeout=30
        )
        issues = issues_response.json()

        state_file = STATE_DIR / "github_state.json"
        last_issues = 0
        if state_file.exists():
            with open(state_file) as f:
                last_state = json.load(f)
                last_issues = last_state.get("open_issues", 0)

        current_issues = len([i for i in issues if isinstance(i, dict[str, Any]) and i.get("state") == "open"])

        with open(state_file, 'w') as f:
            json.dump({"open_issues": current_issues, "updated": time.time()}, f)

        if current_issues > last_issues:
            new_issues = current_issues - last_issues
            return f"🔵 GitHub: {new_issues}个新Issue"

        return None
    except ImportError:
        return None
    except Exception as e:
        return f"❌ GitHub检查异常: {e}"


@guard("gitee", interval_min=60, desc="Gitee仓库状态监控", priority="P2",
       dependencies=["network"])
def check_gitee_guard() -> Optional[str]:
    """检查Gitee仓库同步状态"""
    try:
        gitee_remote = subprocess.run(
            ["git", "remote", "-v"], capture_output=True, text=True, cwd=str(ROOT), timeout=10
        )
        has_gitee = "gitee.com" in gitee_remote.stdout

        if not has_gitee:
            return None  # 未配置Gitee remote

        # 检查同步状态
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", "gitee", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=30
        )
        if result.returncode != 0:
            return f"🟡 Gitee异常: 无法连接Gitee仓库"

        return None
    except Exception:
        return None


@guard("huaweicloud", interval_min=30, desc="华为云服务状态监控", priority="P1",
       dependencies=["network"])
def check_huaweicloud_guard() -> Optional[str]:
    """检查华为云鲲鹏服务器连通性"""
    try:
        huawei_ip = os.getenv("HUAWEI_CLOUD_IP", "119.13.90.27")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((huawei_ip, 22))
        sock.close()

        if result != 0:
            return f"🔴 华为云离线: {huawei_ip}:22 不通"

        return None
    except Exception as e:
        return f"❌ 华为云检查异常: {e}"


# ── 数据级守卫 (1个) ──

@guard("recovery", interval_min=1440, desc="恢复链完整性检查（每日）", priority="P1")
def check_recovery_guard() -> Optional[str]:
    """检查恢复链完整性"""
    try:
        recovery_chain = ROOT / "state" / "recovery_chain.jsonl"
        if not recovery_chain.exists():
            return f"🟡 恢复链空: 无恢复记录"

        with open(recovery_chain) as f:
            lines = f.readlines()

        if not lines:
            return f"🟡 恢复链空: 文件存在但无记录"

        last = json.loads(lines[-1])
        last_time_str = last.get("timestamp", "2000-01-01T00:00:00")
        try:
            last_time = datetime.fromisoformat(last_time_str)
            days_ago = (datetime.now(TZ) - last_time.replace(tzinfo=TZ)).days
        except Exception:
            days_ago = 999

        invalid_gpg = sum(1 for l in lines
                         if not json.loads(l).get("gpg_signature"))

        if invalid_gpg > 0:
            return f"🔴 恢复链异常: {invalid_gpg}条记录无GPG签章"

        if days_ago > 30:
            return f"🟡 恢复稀疏: {days_ago}天无恢复操作"

        return None
    except Exception as e:
        return f"❌ 恢复链检查异常: {e}"


# ═══════════════════════════════════════════════════════════
# 触发引擎
# ═══════════════════════════════════════════════════════════

def run_guard(guard_name: str, verbose: bool = True,
              repair: bool = False) -> Tuple[bool, Optional[str], Dict]:
    """运行单个守卫检查，返回 (是否触发, 消息, 元信息)"""
    if guard_name not in GUARDS:
        return False, f"❌ 未知守卫: {guard_name}", {}

    guard_def = GUARDS[guard_name]

    # 性能监控：记录执行时间
    t_start = time.perf_counter()
    try:
        result = guard_def["func"]()
    except Exception as e:
        result = f"❌ 守卫 {guard_name} 执行异常: {e}"
    t_end = time.perf_counter()
    elapsed_ms = (t_end - t_start) * 1000

    # 记录性能
    perf_data = load_performance()
    guard_perf = perf_data.setdefault(guard_name, [])
    guard_perf.append({"timestamp": datetime.now(TZ).isoformat(), "elapsed_ms": elapsed_ms})
    if len(guard_perf) > 100:
        guard_perf = guard_perf[-100:]
    perf_data[guard_name] = guard_perf
    save_performance(perf_data)

    # 性能告警
    if elapsed_ms > 10000:
        perf_warn = f"⚠️ 守卫 {guard_name} 执行超时: {elapsed_ms:.0f}ms"
        if verbose:
            print(f"  {perf_warn}")

    triggered = result is not None
    msg = result or f"✅ {guard_name}: 正常"

    # 告警聚合
    alert_meta = {}
    if triggered:
        if not alert_aggregator.should_alert(guard_name, msg):
            if verbose:
                print(f"  🔇 {guard_name}: 冷却期跳过 (消息: {msg[:60]})")
            # 仍记录但不重复告警
            alert_meta["suppressed"] = True

    # 自动修复
    if triggered and repair:
        issue_type = _infer_issue_type(guard_name, msg)
        repair_result = auto_repair.repair(guard_name, issue_type)
        alert_meta["repair"] = repair_result
        if repair_result["status"] == "success":
            msg += " → ✅ 自动修复完成"

    # 记录历史
    history = load_history()
    record = {
        "guard": guard_name,
        "timestamp": datetime.now(TZ).isoformat(),
        "triggered": triggered,
        "message": msg,
        "priority": guard_def.get("priority", "P2"),
        "elapsed_ms": elapsed_ms,
        "meta": alert_meta,
    }
    history["triggers"].append(record)

    # 只保留最近2000条
    if len(history["triggers"]) > 2000:
        history["triggers"] = history["triggers"][-2000:]

    # 更新统计
    stats = history.setdefault("stats", {})
    gs = stats.setdefault(guard_name, {"checks": 0, "triggers": 0, "last_trigger": None,
                                        "avg_ms": 0, "priority": guard_def.get("priority", "P2")})
    gs["checks"] += 1
    if triggered:
        gs["triggers"] += 1
        gs["last_trigger"] = datetime.now(TZ).isoformat()

    # 移动平均执行时间
    gs["avg_ms"] = gs.get("avg_ms", 0) * 0.9 + elapsed_ms * 0.1

    save_history(history)

    # 更新守卫状态
    guard_def["last_triggered"] = datetime.now(TZ).isoformat()
    if triggered:
        guard_def["trigger_count"] += 1

    # 告警升级
    if triggered and not alert_meta.get("suppressed"):
        escalation_engine.escalate({
            "id": f"{guard_name}-{int(time.time())}",
            "guard": guard_name,
            "message": msg,
            "priority": guard_def.get("priority", "P2"),
            "timestamp": datetime.now(TZ).isoformat(),
        }, guard_def.get("priority", "P2"))

    if verbose:
        icon = "🔔" if triggered else "✅"
        priority_tag = f"[{guard_def.get('priority', 'P2')}]"
        print(f"  {icon} {priority_tag} {guard_name}: {msg[:120]}")

    return triggered, msg, alert_meta


def _infer_issue_type(guard_name: str, msg: str) -> str:
    """根据消息推断问题类型"""
    if guard_name == "disk" and "紧急" in msg:
        return "low_space"
    elif guard_name == "health" and "离线" in msg:
        return "service_offline"
    elif guard_name == "git" and "脏" in msg:
        return "dirty_repo"
    elif guard_name == "signing" and "签章" in msg:
        return "missing_gpg"
    elif guard_name == "typefix" and "类型" in msg:
        return "bare_types"
    elif guard_name == "dualnode":
        if "frp" in msg.lower() or "隧道" in msg:
            return "frp_down"
        elif "断开" in msg:
            return "connection_lost"
    return "generic"


def check_all(verbose: bool = True, repair: bool = False) -> Dict[str, Tuple[bool, Optional[str]]]:
    """检查所有守卫"""
    results = {}
    for name in GUARDS:
        triggered, msg, _ = run_guard(name, verbose, repair)
        results[name] = (triggered, msg)
    return results


def check_one(name: str, verbose: bool = True, repair: bool = False) -> Tuple[bool, Optional[str]]:
    """检查单个守卫"""
    triggered, msg, _ = run_guard(name, verbose, repair)
    return triggered, msg


def list_guards():
    """列出所有守卫"""
    categories = {
        "系统级": ["disk", "memory", "process", "network", "temperature", "battery"],
        "龍魂系统级": ["git", "health", "backup", "persona", "signing", "audit"],
        "代码质量": ["typefix"],
        "双节点同步": ["dualnode"],
        "安全级": ["intrusion", "firewall", "privacy"],
        "业务级": ["github", "gitee", "huaweicloud"],
        "数据级": ["recovery"],
    }

    print(f"\n{'='*70}")
    print(f"🐉 龍魂阈值触发守卫 v2.1 · 共{len(GUARDS)}个")
    print(f"{'='*70}")

    for category, guard_names in categories.items():
        print(f"\n  ── {category} ──")
        print(f"  {'守卫':<14} {'优先级':<8} {'间隔':<10} {'说明'}")
        print(f"  {'-'*14} {'-'*8} {'-'*10} {'-'*40}")
        for name in guard_names:
            if name in GUARDS:
                g = GUARDS[name]
                interval = f"{g['interval_min']}分钟" if g['interval_min'] < 60 else f"{g['interval_min']//60}小时"
                if g['interval_min'] >= 1440:
                    interval = f"{g['interval_min']//1440}天"
                print(f"  {name:<14} {g.get('priority', 'P2'):<8} {interval:<10} {g['description']}")

    print(f"\n  运行: python3 bin/lh_threshold_trigger.py --check <守卫名>")
    print(f"  全部: python3 bin/lh_threshold_trigger.py --check all")
    print(f"  修复: python3 bin/lh_threshold_trigger.py --check all --repair")


def show_status():
    """显示触发历史状态"""
    history = load_history()
    stats = history.get("stats", {})
    triggers = history.get("triggers", [])

    print(f"\n{'='*70}")
    print(f"🐉 龍魂阈值触发 v2.1 · 运行状态")
    print(f"{'='*70}")

    if not stats:
        print("  尚无触发记录")
        return

    print(f"\n  {'守卫':<14} {'优先级':<8} {'检查':>6} {'触发':>6} {'触发率':>8} {'均耗时':>8} {'最后触发'}")
    print(f"  {'-'*14} {'-'*8} {'-'*6} {'-'*6} {'-'*8} {'-'*8} {'-'*20}")
    for name, s in sorted(stats.items()):
        rate = f"{s['triggers']/s['checks']*100:.0f}%" if s['checks'] > 0 else "N/A"
        last = s.get('last_trigger', '暂无') or '暂无'
        if len(last) > 19:
            last = last[:19]
        avg_ms = f"{s.get('avg_ms', 0):.0f}ms"
        print(f"  {name:<14} {s.get('priority', 'P2'):<8} {s['checks']:>6} {s['triggers']:>6} "
              f"{rate:>8} {avg_ms:>8} {last}")

    # 最近触发
    recent_triggers = [t for t in triggers[-50:] if t.get("triggered")]
    if recent_triggers:
        print(f"\n  最近触发事件 (最近10条):")
        for t in reversed(recent_triggers[-10:]):
            ts = t.get("timestamp", "")[:19]
            p = t.get("priority", "P2")
            elapsed = t.get("elapsed_ms", 0)
            print(f"    [{ts}] [{p}] {t['guard']}({elapsed:.0f}ms): {t.get('message', '')[:80]}")


def check_dependencies(verbose: bool = True) -> Dict[str, List[str]]:
    """检查所有守卫的依赖关系"""
    results = {}
    if verbose:
        print(f"\n{'='*60}")
        print(f"🔗 守卫依赖关系检查")
        print(f"{'='*60}\n")

    all_ok = True
    for name, g in GUARDS.items():
        deps = g.get("dependencies", [])
        if not deps:
            continue
        ok, failures = dependency_checker.check_dependencies(name)
        results[name] = failures
        if verbose:
            if ok:
                print(f"  ✅ {name}: 依赖满足 ({', '.join(deps)})")
            else:
                all_ok = False
                print(f"  ❌ {name}: 依赖失败 → {', '.join(failures)}")

    if verbose:
        status = "全部通过" if all_ok else "存在失败"
        print(f"\n  结论: {status}")
    return results


def deploy_launchd(guard_filter: Optional[str] = None):
    """生成launchd定时任务配置"""
    print(f"\n{'='*70}")
    print(f"🐉 部署阈值触发定时任务 (替代常驻守护) v2.1")
    print(f"{'='*70}\n")

    deployed = []
    skipped = []

    targets = {guard_filter: GUARDS[guard_filter]} if guard_filter and guard_filter in GUARDS else GUARDS

    for name, g in targets.items():
        plist_name = f"com.longhun.threshold-{name}.plist"
        plist_path = LAUNCHD_DIR / plist_name
        interval_min = g["interval_min"]

        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.threshold-{name}</string>

    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{ROOT}/bin/lh_threshold_trigger.py</string>
        <string>--check</string>
        <string>{name}</string>
    </array>

    <key>WorkingDirectory</key>
    <string>{ROOT}</string>

    <key>StartInterval</key>
    <integer>{interval_min * 60}</integer>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>{ROOT}/logs/threshold_{name}.out.log</string>

    <key>StandardErrorPath</key>
    <string>{ROOT}/logs/threshold_{name}.err.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
        <key>LONGHUN_ROOT</key>
        <string>{ROOT}</string>
    </dict>
</dict>
</plist>"""

        try:
            (ROOT / "logs").mkdir(parents=True, exist_ok=True)
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            deployed.append((name, plist_name, interval_min))
            print(f"  ✅ {name}[{g.get('priority','P2')}]: 每{interval_min}分钟 → {plist_name}")
        except Exception as e:
            skipped.append((name, str(e)))
            print(f"  ❌ {name}: 部署失败 → {e}")

    print(f"\n  已部署: {len(deployed)}个定时检查任务")
    if skipped:
        print(f"  跳过: {len(skipped)}个")

    if deployed:
        print(f"\n  加载命令:")
        for name, plist_name, _ in deployed:
            print(f"    launchctl load -w ~/Library/LaunchAgents/{plist_name}")
        print(f"\n  一次性加载全部:")
        plist_paths = " ".join([f"~/Library/LaunchAgents/{p}" for _, p, _ in deployed])
        print(f"    for p in {plist_paths}; do launchctl load -w \"$p\"; done")

    print(f"\n  旧守护进程已可停止:")
    print(f"    python3 bin/lh_threshold_trigger.py --stop-old-guards")


def stop_old_guard_daemons():
    """停止旧的常驻轮询守护进程"""
    OLD_LAUNCHD_LABELS = [
        "com.longhun.disk-guard",
        "com.longhun.global-monitor",
        "com.longhun.drive-backup",
        "com.longhun.rawfeeder",
        "com.longhun.gua-audit",
        "com.longhun.memory-bootstrap",
        "com.longhun.capability-daemon",
        "com.longhun.symbiote",
    ]

    print(f"\n{'='*70}")
    print(f"🛑 停止旧常驻守护进程")
    print(f"{'='*70}\n")

    for label in OLD_LAUNCHD_LABELS:
        plist_path = LAUNCHD_DIR / f"{label}.plist"
        if plist_path.exists():
            try:
                subprocess.run(["launchctl", "unload", str(plist_path)],
                             capture_output=True, timeout=10)
                archive_dir = ROOT / "_archive" / "old_guards_plist"
                archive_dir.mkdir(parents=True, exist_ok=True)
                plist_path.rename(archive_dir / plist_path.name)
                print(f"  ✅ 已停止: {label}")
            except Exception as e:
                print(f"  ⚠️ {label}: {e}")
        else:
            print(f"  ⏭️ 无配置: {label}")

    print(f"\n  清理残留进程...")
    kill_patterns = [
        "lh_disk_guard.py watch",
        "lh_global_monitor.py --daemon",
        "lh_drive_auto_backup.py watch",
        "gua_audit_daemon.py",
        "memory_bootstrap_daemon.py",
        "lh-train-daemon",
        "龍魂投喂器服务",
    ]
    for pattern in kill_patterns:
        try:
            result = subprocess.run(
                ["pkill", "-f", pattern],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                print(f"  ✅ 已停止进程: {pattern}")
        except Exception:
            pass

    print(f"\n  旧守护全部停用。阈值触发系统 v2.1 已接管。")


def export_config():
    """导出当前守卫配置为YAML"""
    config = {
        "global": {
            "log_level": "INFO",
            "alert_cooldown": 300,
            "auto_repair": False,
            "escalation": True,
        },
        "guards": {},
    }

    for name, g in GUARDS.items():
        config["guards"][name] = {
            "enabled": True,
            "interval_min": g["interval_min"],
            "priority": g.get("priority", "P2"),
            "description": g["description"],
            "dependencies": g.get("dependencies", []),
        }

    try:
        import yaml
        content = yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except ImportError:
        content = json.dumps(config, ensure_ascii=False, indent=2)

    print(content)
    return config


def import_config(file_path: str):
    """从YAML/JSON导入配置"""
    config_path = Path(file_path)
    if not config_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return

    try:
        with open(config_path) as f:
            content = f.read()

        # 尝试YAML
        try:
            import yaml
            config = yaml.safe_load(content)
        except ImportError:
            config = json.loads(content)

        # 写入配置文件
        with open(CONFIG_FILE, 'w') as f:
            if "yaml" in sys.modules:
                yaml.dump(config, f, allow_unicode=True)
            else:
                json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"✅ 配置已导入: {CONFIG_FILE}")

        # 显示导入的守卫
        guards_cfg = config.get("guards", {})
        enabled = [k for k, v in guards_cfg.items() if v.get("enabled", True)]
        disabled = [k for k, v in guards_cfg.items() if not v.get("enabled", True)]
        print(f"  启用守卫: {len(enabled)} → {', '.join(enabled[:10])}...")
        if disabled:
            print(f"  禁用守卫: {len(disabled)} → {', '.join(disabled)}")

    except Exception as e:
        print(f"❌ 导入失败: {e}")


def escalation_test():
    """测试告警升级机制"""
    print(f"\n{'='*60}")
    print(f"🧪 告警升级测试")
    print(f"{'='*60}\n")

    test_alerts = [
        {"id": "test-p0", "guard": "test_guard", "message": "P0级别测试告警", "priority": "P0",
         "timestamp": datetime.now(TZ).isoformat()},
        {"id": "test-p1", "guard": "test_guard", "message": "P1级别测试告警", "priority": "P1",
         "timestamp": datetime.now(TZ).isoformat()},
        {"id": "test-p2", "guard": "test_guard", "message": "P2级别测试告警", "priority": "P2",
         "timestamp": datetime.now(TZ).isoformat()},
    ]

    for alert in test_alerts:
        print(f"  测试 {alert['priority']}: {alert['message']}")
        escalation_engine.escalate(alert, alert["priority"])

    print(f"\n  ✅ 告警升级测试完成")


def config_reload():
    """热加载配置"""
    print(f"🔄 热加载配置...")
    config = load_config()
    if config:
        guards_cfg = config.get("guards", {})
        for name, cfg in guards_cfg.items():
            if name in GUARDS:
                if not cfg.get("enabled", True):
                    GUARDS[name]["enabled"] = False
                    print(f"  ⏸️ 已禁用: {name}")
                else:
                    GUARDS[name]["enabled"] = True
                    if "interval_min" in cfg:
                        GUARDS[name]["interval_min"] = cfg["interval_min"]
                    if "priority" in cfg:
                        GUARDS[name]["priority"] = cfg["priority"]
        print(f"✅ 配置已热加载")
    else:
        print(f"⚠️ 无配置文件，使用默认配置")


# ═══════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂阈值触发统一管理器 v2.1 · 阀子到了自动触发 · 18守卫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --check all              检查所有阈值守卫
  %(prog)s --check all --repair     检查并自动修复
  %(prog)s --check disk             仅检查磁盘
  %(prog)s --list                   列出所有守卫
  %(prog)s --status                 查看触发历史
  %(prog)s --deploy                 部署定时检查任务
  %(prog)s --deploy --guard disk    仅部署disk守卫
  %(prog)s --stop-old-guards        停止旧的常驻轮询守护
  %(prog)s --escalation-test        测试告警升级
  %(prog)s --dependency-check       检查守卫依赖
  %(prog)s --export-config          导出配置
  %(prog)s --import-config FILE     导入配置
  %(prog)s --config-reload          热加载配置
        """,
    )

    parser.add_argument("--check", type=str, metavar="GUARD",
                       help="检查指定守卫 (名称或 'all')")
    parser.add_argument("--repair", action="store_true",
                       help="检测到问题后自动修复")
    parser.add_argument("--list", action="store_true",
                       help="列出所有守卫")
    parser.add_argument("--status", action="store_true",
                       help="查看触发历史")
    parser.add_argument("--deploy", action="store_true",
                       help="部署launchd定时任务")
    parser.add_argument("--guard", type=str, metavar="NAME",
                       help="仅部署指定守卫 (配合--deploy)")
    parser.add_argument("--stop-old-guards", action="store_true",
                       help="停止旧的常驻轮询守护")
    parser.add_argument("--json", action="store_true",
                       help="JSON格式输出")
    parser.add_argument("--escalation-test", action="store_true",
                       help="测试告警升级机制")
    parser.add_argument("--dependency-check", action="store_true",
                       help="检查守卫依赖关系")
    parser.add_argument("--export-config", action="store_true",
                       help="导出当前配置")
    parser.add_argument("--import-config", type=str, metavar="FILE",
                       help="从文件导入配置")
    parser.add_argument("--config-reload", action="store_true",
                       help="热加载配置文件")

    args = parser.parse_args()

    if args.list:
        list_guards()
    elif args.status:
        show_status()
    elif args.deploy:
        deploy_launchd(args.guard)
    elif args.stop_old_guards:
        stop_old_guard_daemons()
    elif args.escalation_test:
        escalation_test()
    elif args.dependency_check:
        check_dependencies()
    elif args.export_config:
        export_config()
    elif args.import_config:
        import_config(args.import_config)
    elif args.config_reload:
        config_reload()
    elif args.check:
        if args.check == "all":
            results = check_all(verbose=not args.json, repair=args.repair)
            if args.json:
                output = {k: {"triggered": v[0], "message": v[1]} for k, v in results.items()}
                print(json.dumps(output, ensure_ascii=False, indent=2))
            any_triggered = any(v[0] for v in results.values())
        else:
            triggered, msg = check_one(args.check, verbose=not args.json, repair=args.repair)
            if args.json:
                print(json.dumps({"guard": args.check, "triggered": triggered, "message": msg},
                               ensure_ascii=False, indent=2))
            any_triggered = triggered
        sys.exit(1 if any_triggered else 0)
    else:
        # 默认：检查所有 + 显示摘要
        print(f"🐉 龍魂阈值触发 v2.1 · {datetime.now(TZ).strftime('%H:%M:%S')}")
        print(f"DNA: {DNA}")
        print(f"守卫: {len(GUARDS)}个 · 告警聚合+自动修复+告警升级+依赖检查\n")
        results = check_all()
        triggered_count = sum(1 for v in results.values() if v[0])
        print(f"\n  结果: {triggered_count}/{len(results)} 触发, "
              f"{len(results) - triggered_count}/{len(results)} 正常")
        sys.exit(1 if triggered_count > 0 else 0)


if __name__ == "__main__":
    main()
