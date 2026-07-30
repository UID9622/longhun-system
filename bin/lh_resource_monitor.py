#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·代谢系统-RESOURCE-MONITOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     🔥 龍魂 · 代谢系统 · 资源监控引擎 v1.0                     ║
║                                                                  ║
║  生物映射：代谢系统 → 能量转化 → CPU/内存/磁盘资源管理              ║
║  五行归属：木                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·代谢系统-RESOURCE-MONITOR-v1.0           ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_resource_monitor.py --check        # 检查当前资源
  python3 bin/lh_resource_monitor.py --health       # 代谢健康评估
  python3 bin/lh_resource_monitor.py --optimize     # 资源优化建议
  python3 bin/lh_resource_monitor.py --daemon       # 持续监控
"""

import json
import os
import sys
import time
import signal
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
METABOLIC_LOG = STATE_DIR / "metabolic_log.jsonl"
METABOLIC_STATE = STATE_DIR / "metabolic_state.json"

DNA = "#龍芯⚡️丙午·辛未·代谢系统-RESOURCE-MONITOR-v1.0"


class MetabolicEngine:
    """代谢系统：监控系统资源吸收/转化/消耗"""

    # 阈值（可动态调整 → 内分泌系统调节）
    THRESHOLDS = {
        "cpu_warning": 70,     # %
        "cpu_critical": 90,
        "memory_warning": 75,  # %
        "memory_critical": 90,
        "disk_warning": 80,    # %
        "disk_critical": 95,
        "script_stale_days": 30,  # 脚本陈旧天数
    }

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if METABOLIC_STATE.exists():
            return json.loads(METABOLIC_STATE.read_text())
        return {"checks": 0, "alerts": [], "history": [], "last_check": ""}

    def _save_state(self):
        METABOLIC_STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def check_resources(self) -> Dict[str, Any]:
        """检查系统资源（CPU/内存/磁盘）"""
        try:
            import psutil
            HAS_PSUTIL = True
        except ImportError:
            HAS_PSUTIL = False

        now = datetime.now().isoformat()

        if HAS_PSUTIL:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(str(ROOT))

            result = {
                "timestamp": now,
                "cpu_percent": cpu,
                "cpu_cores": psutil.cpu_count(),
                "memory_percent": mem.percent,
                "memory_used_gb": round(mem.used / (1024**3), 1),
                "memory_total_gb": round(mem.total / (1024**3), 1),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 1),
                "disk_total_gb": round(disk.total / (1024**3), 1),
            }
        else:
            # 降级：使用基础系统命令
            result = {"timestamp": now, "_fallback": True}
            try:
                import resource
                # 只获取基本的内存信息
                result["memory_used_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            except Exception:
                pass

            # 磁盘
            try:
                stat = os.statvfs(str(ROOT))
                result["disk_free_gb"] = round(stat.f_frsize * stat.f_bavail / (1024**3), 1)
                result["disk_total_gb"] = round(stat.f_frsize * stat.f_blocks / (1024**3), 1)
                result["disk_percent"] = round((1 - stat.f_bavail / max(stat.f_blocks, 1)) * 100, 1)
            except Exception:
                pass

        # 阈值检测
        alerts = []
        for metric, value in [
            ("cpu", result.get("cpu_percent", 0)),
            ("memory", result.get("memory_percent", 0)),
            ("disk", result.get("disk_percent", 0)),
        ]:
            warn_key = f"{metric}_warning"
            crit_key = f"{metric}_critical"
            if value >= self.THRESHOLDS[crit_key]:
                alerts.append({"level": "🔴", "metric": metric, "value": value,
                              "threshold": self.THRESHOLDS[crit_key], "action": "紧急释放"})
            elif value >= self.THRESHOLDS[warn_key]:
                alerts.append({"level": "🟡", "metric": metric, "value": value,
                              "threshold": self.THRESHOLDS[warn_key], "action": "预警优化"})

        result["alerts"] = alerts
        result["health_score"] = self._calc_metabolic_health(result, alerts)

        # 记录日志
        self._log(result)
        self.state["checks"] += 1
        self.state["last_check"] = now
        if alerts:
            self.state["alerts"].extend(alerts)
        self._save_state()

        return result

    def _calc_metabolic_health(self, result: Dict[str, Any], alerts: List[Any]) -> float:
        """计算代谢健康度"""
        cpu = result.get("cpu_percent", 0)
        mem = result.get("memory_percent", 0)
        disk = result.get("disk_percent", 0)

        # 各项独立评分
        cpu_score = max(0, 1.0 - cpu / 100)
        mem_score = max(0, 1.0 - mem / 100)
        disk_score = max(0, 1.0 - disk / 100)

        # 加权
        health = cpu_score * 0.35 + mem_score * 0.35 + disk_score * 0.30

        # 告警罚分
        health -= len(alerts) * 0.05

        return round(max(0.0, health), 3)

    def _log(self, result: Dict[str, Any]):
        with open(METABOLIC_LOG, "a") as f:
            log_entry = {
                k: v for k, v in result.items()
                if k in ("timestamp", "cpu_percent", "memory_percent", "disk_percent",
                          "health_score")
            }
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def optimize_suggestions(self) -> Dict[str, Any]:
        """生成资源优化建议"""
        if not self.state.get("history"):
            return {"status": "无历史数据", "suggestions": []}

        suggestions = []
        recent = self.state["history"][-10:] if len(self.state["history"]) > 0 else []

        if recent:
            avg_cpu = sum(r.get("cpu_percent", 0) for r in recent) / len(recent)
            avg_mem = sum(r.get("memory_percent", 0) for r in recent) / len(recent)

            if avg_cpu > 60:
                suggestions.append({
                    "target": "CPU",
                    "issue": f"平均{avg_cpu:.0f}%使用率偏高",
                    "recommendation": "检查是否有脚本死循环或过度轮询",
                    "action": "review_cpu_intensive",
                })

            if avg_mem > 70:
                suggestions.append({
                    "target": "内存",
                    "issue": f"平均{avg_mem:.0f}%内存占用偏高",
                    "recommendation": "检查大数据结构是否及时释放",
                    "action": "review_memory_leaks",
                })

        # 脚本陈旧度检查
        registry_file = STATE_DIR / "script_registry.json"
        if registry_file.exists():
            registry = json.loads(registry_file.read_text())
            stale_count = 0
            for sid, data in registry.items():
                last = data.get("last_checked", data.get("registered_at", ""))
                if last:
                    days = (datetime.now() - datetime.fromisoformat(last)).days
                    if days > self.THRESHOLDS["script_stale_days"]:
                        stale_count += 1

            if stale_count > 10:
                suggestions.append({
                    "target": "脚本活性",
                    "issue": f"{stale_count}个脚本超过{self.THRESHOLDS['script_stale_days']}天未更新",
                    "recommendation": "运行 python3 bin/lh_ant_colony_orchestrator.py --run 刷新注册表",
                    "action": "refresh_registry",
                })

        return {
            "dna": DNA,
            "suggestions": suggestions,
            "total": len(suggestions),
            "status": "🟢" if len(suggestions) == 0 else "🟡" if len(suggestions) < 3 else "🔴",
        }

    def daemon(self, interval: int = 600):
        """守护模式：定期代谢检查"""
        print(f"🔥 代谢系统守护启动 · 间隔{interval}s")
        print(f"   {DNA}")
        running = True

        def _stop(sig, frame):
            nonlocal running
            running = False
            print("\n🔥 代谢系统安全停机...")

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        while running:
            result = self.check_resources()
            alerts = result.get("alerts", [])
            if alerts:
                for a in alerts:
                    print(f"  {a['level']} {a['metric']}:{a['value']:.0f}% → {a['action']}")
            else:
                print(f"  🟢 CPU:{result.get('cpu_percent', '?')}% | "
                      f"内存:{result.get('memory_percent', '?')}% | "
                      f"磁盘:{result.get('disk_percent', '?')}% | "
                      f"代谢健康:{result['health_score']:.1%}")

            # 保存历史
            self.state.setdefault("history", []).append({
                "timestamp": result["timestamp"],
                "cpu": result.get("cpu_percent", 0),
                "memory": result.get("memory_percent", 0),
                "disk": result.get("disk_percent", 0),
                "health": result["health_score"],
            })
            # 只保留最近100条
            if len(self.state["history"]) > 100:
                self.state["history"] = self.state["history"][-100:]
            self._save_state()

            time.sleep(interval)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·代谢系统·资源监控")
    parser.add_argument("--check", action="store_true", help="检查当前资源")
    parser.add_argument("--health", action="store_true", help="代谢健康评估")
    parser.add_argument("--optimize", action="store_true", help="资源优化建议")
    parser.add_argument("--daemon", action="store_true", help="守护监控")
    parser.add_argument("--interval", type=int, default=600, help="守护间隔")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    engine = MetabolicEngine()

    if args.daemon:
        engine.daemon(args.interval)
        return 0

    if args.optimize:
        result = engine.optimize_suggestions()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔥 代谢优化建议: {result['status']}")
            for s in result["suggestions"]:
                print(f"  - {s['target']}: {s['issue']} → {s['recommendation']}")
        return 0

    if args.check or args.health:
        result = engine.check_resources()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔥 代谢检查 · 健康:{result.get('health_score', '?')}")
            print(f"  CPU: {result.get('cpu_percent', '?')}% | "
                  f"内存: {result.get('memory_percent', '?')}%({result.get('memory_used_gb','?')}/{result.get('memory_total_gb','?')}GB)")
            print(f"  磁盘: {result.get('disk_percent', '?')}% "
                  f"(空闲{result.get('disk_free_gb','?')}/{result.get('disk_total_gb','?')}GB)")
            if result.get("alerts"):
                for a in result["alerts"]:
                    print(f"  {a['level']} {a['metric']}:{a['value']}% > {a['threshold']}% → {a['action']}")
        return 0

    # 默认
    engine.check_resources()
    suggestions = engine.optimize_suggestions()
    print(f"代谢系统就绪 · {suggestions['total']}条优化建议")
    return 0


if __name__ == "__main__":
    sys.exit(main())
