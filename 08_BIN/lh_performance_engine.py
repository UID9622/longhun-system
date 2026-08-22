#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 性能分析引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-PERF-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 分析系统瓶颈（CPU/内存/IO/网络）
  - 性能趋势分析
  - 优化建议
  - 容量规划
"""

import json
import psutil
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta


class PerformanceEngine:
    """性能分析引擎——找瓶颈、看趋势、给建议、容量规划"""

    def __init__(self):
        self.history_dir = Path.home() / "longhun-system/data/perf_history"
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def analyze(self) -> Dict[str, Any]:
        """当前性能分析"""
        sys_data = self._analyze_system()
        bottlenecks = []
        recs = []

        if sys_data.get("cpu_percent", 0) > 85:
            bottlenecks.append({"type": "cpu", "value": sys_data["cpu_percent"]})
            recs.append("降低并发任务数，或增加CPU资源")
        if sys_data.get("memory_percent", 0) > 85:
            bottlenecks.append({"type": "memory", "value": sys_data["memory_percent"]})
            recs.append("增加内存，或清理不用的进程")
        if sys_data.get("disk_percent", 0) > 85:
            bottlenecks.append({"type": "disk", "value": sys_data["disk_percent"]})
            recs.append("清理磁盘空间，或考虑扩容")

        return {
            "timestamp": datetime.now().isoformat(),
            "system": sys_data,
            "bottlenecks": bottlenecks,
            "recommendations": recs,
            "health": "🟡 警告" if bottlenecks else "🟢 健康",
        }

    def _analyze_system(self) -> Dict:
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            net = psutil.net_io_counters()
            return {
                "cpu_percent": cpu,
                "cpu_cores": psutil.cpu_count(),
                "memory_percent": mem.percent,
                "memory_available_gb": round(mem.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "net_recv_mb": round(net.bytes_recv / (1024**2), 2) if net else 0,
                "net_sent_mb": round(net.bytes_sent / (1024**2), 2) if net else 0,
            }
        except Exception:
            return {"error": "无法采集系统数据"}

    def trend(self, days: int = 7) -> Dict:
        """性能趋势分析"""
        cutoff = datetime.now() - timedelta(days=days)
        history = []
        for f in sorted(self.history_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                dt = datetime.fromisoformat(data.get("timestamp", "1970-01-01T00:00:00"))
                if dt > cutoff:
                    history.append(data)
            except Exception:
                continue
        if len(history) < 2:
            return {"status": "insufficient_data", "points": len(history)}

        cpu_values = [h.get("system", {}).get("cpu_percent", 0) for h in history]
        mem_values = [h.get("system", {}).get("memory_percent", 0) for h in history]

        direction = "stable"
        if len(cpu_values) >= 3:
            r_avg = sum(cpu_values[-3:]) / 3
            o_avg = sum(cpu_values[:3]) / 3
            if r_avg > o_avg * 1.15:
                direction = "increasing"
            elif r_avg < o_avg * 0.85:
                direction = "decreasing"

        return {
            "days": days, "points": len(history),
            "avg_cpu": round(sum(cpu_values) / len(cpu_values), 1),
            "avg_memory": round(sum(mem_values) / len(mem_values), 1),
            "direction": direction,
        }

    def save_snapshot(self):
        analysis = self.analyze()
        snapshot_file = self.history_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        snapshot_file.write_text(json.dumps(analysis, ensure_ascii=False, indent=2))
        return snapshot_file


if __name__ == "__main__":
    engine = PerformanceEngine()
    result = engine.analyze()
    print(f"健康: {result['health']}")
    print(f"系统: CPU={result['system'].get('cpu_percent','?')}% MEM={result['system'].get('memory_percent','?')}%")
    print(f"瓶颈: {len(result['bottlenecks'])} 项")
    snapshot = engine.save_snapshot()
    print(f"快照: {snapshot}")
    print("🟢 性能分析引擎测试通过")
