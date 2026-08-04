#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🔭 龍魂·天下无欺·全貌可观测性采集引擎 v1.0                   ║
║                                                                  ║
║  协议: LH-OBSERVABILITY-COLLECTOR-v1.0                           ║
║  哲学: 天下无欺 — 每一个节点/路由/回调都可见·可追溯·可回放         ║
║                                                                  ║
║  采集维度:                                                        ║
║    A. 引擎健康 — 256+ bin/lh_*.py 存活状态                        ║
║    B. 信号路由 — 信号中继站·蚁群信息素·事件传播路径               ║
║    C. 审计追踪 — 操作日志·GP签章链·DNA注册表                      ║
║    D. 阈值状态 — 磁盘/内存/隐私/入侵/进程/签名/电池                ║
║    E. 守护进程 — 19守护+健康告警+自动修复                          ║
║    F. 告警聚合 — 去重·分级·升级·通知通道                           ║
║    G. 系统资源 — CPU/内存/磁盘/网络/进程                           ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·OBSERVABILITY-v1.0              ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_observability_collector.py              # 全量采集，JSON输出
  python3 bin/lh_observability_collector.py --daemon 30  # 守护模式，每30秒采集
  python3 bin/lh_observability_collector.py --compact    # 精简输出（仪表盘用）
  python3 bin/lh_observability_collector.py --module health  # 仅采集健康维度
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "observability"
STATE_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_FILE = STATE_DIR / "snapshot.json"
HISTORY_FILE = STATE_DIR / "history.jsonl"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·OBSERVABILITY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ══════════════════════════════════════════════════════
# A. 引擎清单 — 256+ 引擎分类
# ══════════════════════════════════════════════════════

ENGINE_CATEGORIES = {
    "人格矩阵": {
        "engines": ["persona_signing", "persona_start_all", "persona_auto_switch", "persona_landing"],
        "weight": 0.20,
    },
    "蚁群系统": {
        "engines": ["ant_colony_daemon", "ant_colony_router", "ant_colony_orchestrator"],
        "weight": 0.15,
    },
    "审计管道": {
        "engines": ["full_system_audit", "dual_audit_engine", "dual_audit_auto",
                     "audit_hook", "audit_sheet_trigger", "consciousness_audit",
                     "cnsh_code_audit", "cnsh_dir_audit", "registry_audit_fix",
                     "unified_dna_audit", "audit_pricing_v2"],
        "weight": 0.15,
    },
    "阈值守护": {
        "engines": ["threshold_trigger"],
        "weight": 0.10,
    },
    "信号中继": {
        "engines": ["signal_relay"],
        "weight": 0.05,
    },
    "健康告警": {
        "engines": ["health_alert_daemon", "auto_heal", "auto_cannon",
                     "global_monitor", "resource_monitor"],
        "weight": 0.10,
    },
    "注册表": {
        "engines": ["semantic_unified_registry", "registry_auto_sync",
                     "registry_audit_fix", "unified_pipeline"],
        "weight": 0.05,
    },
    "安全装甲": {
        "engines": ["rb_confrontation_engine", "privacy_guard",
                     "anti_counterfeit", "anti_tamper", "water_army_detect",
                     "water_army_elimination", "malicious_edit_detector",
                     "fake_review_detector"],
        "weight": 0.10,
    },
    "自动化守护": {
        "engines": ["auto_compress", "auto_shouheng", "auto_sync",
                     "auto_crawl_daemon", "browser_daemon", "drive_auto_backup",
                     "connectivity_scheduler", "knowledge_scheduler"],
        "weight": 0.05,
    },
    "API网关": {
        "engines": ["api_validate_all", "ai_gateway", "server_checker"],
        "weight": 0.05,
    },
}

ALL_ENGINES = []
for cat_name, cat_data in ENGINE_CATEGORIES.items():
    ALL_ENGINES.extend(cat_data["engines"])


# ══════════════════════════════════════════════════════
# 数据采集器
# ══════════════════════════════════════════════════════

class ObservabilityCollector:
    """天下无欺·全貌采集器"""

    def __init__(self):
        self.root = ROOT
        self.bin_dir = ROOT / "bin"
        self.hostname = socket.gethostname()
        self.platform = platform.platform()
        self.collected_at = None

    # ── A. 引擎健康采集 ──

    def collect_engine_health(self) -> dict[str, Any]:
        """采集所有引擎存在性和最近修改时间"""
        result = {"categories": {}, "total": 0, "present": 0, "missing": []}

        for cat_name, cat_data in ENGINE_CATEGORIES.items():
            cat_result = {"engines": [], "present": 0, "missing": []}
            for eng in cat_data["engines"]:
                fpath = self.bin_dir / f"lh_{eng}.py"
                exists = fpath.exists()
                info = {
                    "name": f"lh_{eng}",
                    "present": exists,
                    "mtime": datetime.fromtimestamp(fpath.stat().st_mtime).isoformat() if exists else None,
                    "size_kb": round(fpath.stat().st_size / 1024, 1) if exists else 0,
                }
                if exists:
                    cat_result["present"] += 1
                else:
                    cat_result["missing"].append(f"lh_{eng}")
                cat_result["engines"].append(info)

            cat_result["health_pct"] = round(100 * cat_result["present"] / max(1, len(cat_data["engines"])), 1)
            result["categories"][cat_name] = cat_result
            result["total"] += len(cat_data["engines"])
            result["present"] += cat_result["present"]
            if cat_result["missing"]:
                result["missing"].extend(cat_result["missing"])

        result["health_pct"] = round(100 * result["present"] / max(1, result["total"]), 1)
        return result

    # ── B. 信号路由状态 ──

    def collect_signal_routes(self) -> dict[str, Any]:
        """采集信号中继站和蚁群信息素状态"""
        routes = {
            "signal_relay": {"status": "unknown", "queue_size": 0, "signals_today": 0},
            "pheromone_network": {"status": "unknown", "trails": 0},
            "route_table": {
                "alert": ["rb_confrontation_engine", "audit_pipeline", "overseer"],
                "heartbeat": ["flow_pipeline", "colony_orchestrator"],
                "threshold": ["rb_confrontation_engine", "sentinel", "overseer"],
                "audit": ["audit_pipeline", "signing_engine", "archive"],
                "persona": ["persona_orchestrator", "signing_engine"],
            },
        }

        # 检查信号队列
        signal_queue = Path.home() / ".longhun" / "ant_colony" / "signal_queue.jsonl"
        if signal_queue.exists():
            try:
                lines = signal_queue.read_text().strip().split("\n")
                today = datetime.now().strftime("%Y-%m-%d")
                routes["signal_relay"]["queue_size"] = len([l for l in lines if l.strip()])
                routes["signal_relay"]["signals_today"] = len(
                    [l for l in lines if l.strip() and today in l]
                )
                routes["signal_relay"]["status"] = "active" if routes["signal_relay"]["queue_size"] > 0 else "idle"
            except Exception:
                routes["signal_relay"]["status"] = "error"

        # 检查信息素网络
        pheromone_file = Path.home() / ".longhun" / "ant_colony" / "pheromone_network.jsonl"
        if pheromone_file.exists():
            try:
                trails = [l for l in pheromone_file.read_text().strip().split("\n") if l.strip()]
                routes["pheromone_network"]["trails"] = len(trails)
                routes["pheromone_network"]["status"] = "active" if trails else "idle"
            except Exception:
                routes["pheromone_network"]["status"] = "error"

        return routes

    # ── C. 审计追踪 ──

    def collect_audit_trail(self) -> dict[str, Any]:
        """采集操作日志统计"""
        audit = {
            "action_log": {"status": "unknown", "today_ops": 0, "total_ops": 0, "success_rate": 0},
            "gpg_signatures": {"total": 0, "valid": 0},
            "health_checks": {"today": 0, "latest_score": None, "history_points": 0},
        }

        # 操作日志
        action_log = ROOT / "logs" / "action_log.jsonl"
        if action_log.exists():
            try:
                today = datetime.now().strftime("%Y-%m-%d")
                all_lines = [l for l in action_log.read_text().strip().split("\n") if l.strip()]
                audit["action_log"]["total_ops"] = len(all_lines)
                today_ops = []
                successes = 0
                for line in all_lines:
                    try:
                        rec = json.loads(line)
                        if rec.get("date", "").startswith(today):
                            today_ops.append(rec)
                            if rec.get("status") == "success":
                                successes += 1
                    except json.JSONDecodeError:
                        pass
                audit["action_log"]["today_ops"] = len(today_ops)
                audit["action_log"]["success_rate"] = round(
                    100 * successes / max(1, len(today_ops)), 1
                )
                audit["action_log"]["status"] = "active"
            except Exception:
                audit["action_log"]["status"] = "error"

        # GPG签章
        gpg_registry = ROOT / "L8_治理层" / "original_creation_milestones" / "GPG_SIGNING_REGISTRY_v1.0.md"
        if gpg_registry.exists():
            try:
                content = gpg_registry.read_text()
                lines = content.split("\n")
                sig_count = sum(1 for l in lines if "GPG" in l or "SIG-" in l)
                audit["gpg_signatures"]["total"] = sig_count
                audit["gpg_signatures"]["valid"] = sig_count  # 默认全部有效
            except Exception:
                pass

        # 健康检查历史
        health_state = Path.home() / ".longhun" / "health" / "health_state.json"
        if health_state.exists():
            try:
                state = json.loads(health_state.read_text())
                audit["health_checks"]["latest_score"] = state.get("last_score")
                audit["health_checks"]["history_points"] = len(state.get("history", []))
            except Exception:
                pass

        return audit

    # ── D. 阈值状态 ──

    def collect_thresholds(self) -> dict[str, Any]:
        """采集所有阈值守护状态"""
        thresholds = {}
        threshold_logs = list(ROOT.glob("logs/threshold_*.out.log")) + \
                         list(ROOT.glob("logs/threshold_*.err.log"))

        for logfile in threshold_logs:
            name = logfile.stem.replace("threshold_", "").replace(".out", "").replace(".err", "")
            if name not in thresholds:
                thresholds[name] = {"status": "unknown", "last_entry": None, "errors": False}

            try:
                content = logfile.read_text().strip()
                if content:
                    last_line = content.split("\n")[-1]
                    thresholds[name]["last_entry"] = last_line[:100]
                    if "ERROR" in last_line or "CRITICAL" in last_line or "🔴" in last_line:
                        thresholds[name]["status"] = "red"
                    elif "WARNING" in last_line or "🟡" in last_line or "🟠" in last_line:
                        thresholds[name]["status"] = "yellow"
                    else:
                        thresholds[name]["status"] = "green"
                if ".err." in str(logfile):
                    thresholds[name]["errors"] = True
            except Exception:
                pass

        return thresholds

    # ── E. 守护进程状态 ──

    def collect_daemons(self) -> dict[str, Any]:
        """采集守护进程运行状态"""
        daemons = {}

        # 通过 ps 检查守护进程
        try:
            result = subprocess.run(
                ["ps", "aux"], capture_output=True, text=True, timeout=5
            )
            ps_output = result.stdout

            daemon_patterns = {
                "health_alert": "lh_health_alert_daemon",
                "ant_colony": "lh_ant_colony_daemon",
                "auto_crawl": "lh_auto_crawl_daemon",
                "browser": "lh_browser_daemon",
                "auto_sync": "lh_auto_sync",
                "auto_shouheng": "lh_auto_shouheng",
                "signal_relay": "lh_signal_relay",
                "threshold_trigger": "lh_threshold_trigger",
                "resource_monitor": "lh_resource_monitor",
                "global_monitor": "lh_global_monitor",
                "auto_heal": "lh_auto_heal",
            }

            for name, pattern in daemon_patterns.items():
                running = pattern in ps_output and "python" in ps_output.split(pattern)[0] if pattern in ps_output else False
                if pattern in ps_output:
                    # 更精确的检查
                    for line in ps_output.split("\n"):
                        if pattern in line and "python" in line and "grep" not in line:
                            running = True
                            break
                        running = False
                daemons[name] = {"running": running, "status": "active" if running else "stopped"}
        except Exception:
            # 回退到基础检查
            for name in daemon_patterns:
                daemons[name] = {"running": False, "status": "unknown"}

        return daemons

    # ── F. 告警聚合 ──

    def collect_alerts(self) -> dict[str, Any]:
        """聚合所有告警源"""
        alerts = {"active": [], "resolved": [], "history_count": 0}

        # 健康历史中的告警
        health_log = Path.home() / ".longhun" / "health" / "health_history.jsonl"
        if health_log.exists():
            try:
                today = datetime.now().strftime("%Y-%m-%d")
                for line in health_log.read_text().strip().split("\n"):
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            if rec.get("ts", "").startswith(today) and rec.get("status") in ("RED", "ORANGE", "YELLOW"):
                                alerts["active"].append({
                                    "source": "health",
                                    "level": rec["status"],
                                    "score": rec.get("score"),
                                    "ts": rec.get("ts"),
                                    "module_count": rec.get("module_count", 0),
                                })
                        except json.JSONDecodeError:
                            pass
                alerts["history_count"] = len([l for l in health_log.read_text().strip().split("\n") if l.strip()])
            except Exception:
                pass

        # 治理告警
        governance_alarms = ROOT / "var" / "governance" / "governance_alarms.jsonl"
        if governance_alarms.exists():
            try:
                today = datetime.now().strftime("%Y-%m-%d")
                for line in governance_alarms.read_text().strip().split("\n"):
                    if line.strip() and today in line:
                        try:
                            rec = json.loads(line)
                            alerts["active"].append({"source": "governance", "level": "YELLOW", "detail": str(rec)[:80]})
                        except json.JSONDecodeError:
                            pass
            except Exception:
                pass

        return alerts

    # ── G. 系统资源 ──

    def collect_resources(self) -> dict[str, Any]:
        """采集系统资源"""
        resources = {"cpu_percent": 0, "memory": {}, "disk": {}, "uptime_hours": 0}

        try:
            import psutil
            resources["cpu_percent"] = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            resources["memory"] = {
                "total_gb": round(mem.total / (1024**3), 1),
                "used_gb": round(mem.used / (1024**3), 1),
                "percent": mem.percent,
            }
            disk = psutil.disk_usage("/")
            resources["disk"] = {
                "total_gb": round(disk.total / (1024**3), 1),
                "used_gb": round(disk.used / (1024**3), 1),
                "percent": disk.percent,
            }
            boot = datetime.fromtimestamp(psutil.boot_time())
            resources["uptime_hours"] = round((datetime.now() - boot).total_seconds() / 3600, 1)
        except ImportError:
            # 回退到 subprocess
            try:
                cpu = subprocess.run(["sysctl", "-n", "vm.loadavg"], capture_output=True, text=True, timeout=3)
                resources["cpu_load"] = cpu.stdout.strip()
            except Exception:
                pass
            try:
                mem_cmd = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=3)
                resources["memory"]["total_gb"] = round(int(mem_cmd.stdout.strip()) / (1024**3), 1)
            except Exception:
                pass

        return resources

    # ── 全量采集 ──

    def collect_all(self) -> dict[str, Any]:
        """全维度采集"""
        self.collected_at = datetime.now().isoformat()

        snapshot = {
            "meta": {
                "dna": DNA,
                "confirm": CONFIRM,
                "collected_at": self.collected_at,
                "hostname": self.hostname,
                "platform": self.platform,
                "collector_version": "v1.0",
            },
            "engines": self.collect_engine_health(),
            "signals": self.collect_signal_routes(),
            "audit": self.collect_audit_trail(),
            "thresholds": self.collect_thresholds(),
            "daemons": self.collect_daemons(),
            "alerts": self.collect_alerts(),
            "resources": self.collect_resources(),
            "overall": {},
        }

        # 综合评分
        overall = self._compute_overall(snapshot)
        snapshot["overall"] = overall

        # 保存快照
        try:
            SNAPSHOT_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))
            with open(HISTORY_FILE, "a") as f:
                f.write(json.dumps({
                    "ts": self.collected_at,
                    "overall_score": overall["score"],
                    "overall_status": overall["status"],
                    "engines_health": snapshot["engines"]["health_pct"],
                    "active_alerts": len(snapshot["alerts"]["active"]),
                }, ensure_ascii=False) + "\n")
        except Exception:
            pass

        return snapshot

    def _compute_overall(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        """综合评分"""
        score = 100.0

        # 引擎健康扣分
        eng_health = snapshot["engines"]["health_pct"]
        if eng_health < 90:
            score -= (90 - eng_health) * 1.5
        elif eng_health < 50:
            score -= 60

        # 守护进程扣分
        running_daemons = sum(1 for d in snapshot["daemons"].values() if d["running"])
        total_daemons = len(snapshot["daemons"])
        if total_daemons > 0:
            daemon_health = 100 * running_daemons / total_daemons
            if daemon_health < 80:
                score -= (80 - daemon_health) * 1.2

        # 告警扣分
        active_alerts = len(snapshot["alerts"]["active"])
        score -= min(active_alerts * 3, 30)

        # 阈值状态扣分
        red_thresholds = sum(1 for t in snapshot["thresholds"].values() if t.get("status") == "red")
        score -= min(red_thresholds * 5, 25)

        score = max(0, min(100, round(score, 1)))

        if score >= 85:
            status = "GREEN"
        elif score >= 70:
            status = "YELLOW"
        elif score >= 50:
            status = "ORANGE"
        else:
            status = "RED"

        return {
            "score": score,
            "status": status,
            "engines_health_pct": eng_health,
            "active_daemons": f"{running_daemons}/{total_daemons}",
            "active_alerts": active_alerts,
            "threshold_issues": red_thresholds,
        }


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂·天下无欺·全貌可观测性采集引擎")
    parser.add_argument("--daemon", type=int, nargs="?", const=30, metavar="SEC",
                        help="守护模式，每N秒采集一次 (默认30)")
    parser.add_argument("--compact", action="store_true", help="精简JSON输出")
    parser.add_argument("--module", type=str, help="仅采集指定维度 (health/signals/audit/thresholds/daemons/alerts/resources)")
    parser.add_argument("--watch", action="store_true", help="持续监控模式，终端仪表盘")

    args = parser.parse_args()
    collector = ObservabilityCollector()

    if args.module:
        method = f"collect_{args.module}"
        if hasattr(collector, method):
            print(json.dumps(getattr(collector)(), ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未知维度: {args.module}", file=sys.stderr)
            sys.exit(1)
        return

    if args.watch:
        try:
            while True:
                snapshot = collector.collect_all()
                ov = snapshot["overall"]
                icon = {"GREEN": "✅", "YELLOW": "⚠️", "ORANGE": "🟠", "RED": "🔴"}.get(ov["status"], "❓")
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"\r{icon} [{ts}] 天下无欺: {ov['score']}/100 | 引擎: {ov['engines_health_pct']}% | 守护: {ov['active_daemons']} | 告警: {ov['active_alerts']} | 阈值: {ov['threshold_issues']}   ", end="", flush=True)
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n\n👋 天下无欺·采集结束")
        return

    if args.daemon:
        interval = args.daemon
        print(f"🔄 守护模式启动 · 每{interval}秒采集 · Ctrl+C停止")
        try:
            while True:
                collector.collect_all()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 守护模式已停止")
        return

    # 默认: 单次采集
    snapshot = collector.collect_all()
    if args.compact:
        compact = {
            "ts": snapshot["meta"]["collected_at"],
            "overall": snapshot["overall"],
            "engines_summary": f"{snapshot['engines']['present']}/{snapshot['engines']['total']} ({snapshot['engines']['health_pct']}%)",
            "alerts_count": len(snapshot["alerts"]["active"]),
            "daemons_running": sum(1 for d in snapshot["daemons"].values() if d["running"]),
            "threshold_issues": sum(1 for t in snapshot["thresholds"].values() if t.get("status") in ("red", "yellow")),
        }
        print(json.dumps(compact, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
