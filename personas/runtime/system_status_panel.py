#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-24-LONGHUN-STATUS-PANEL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂系统状态面板 · LongHun System Status Panel v1.0

- 三色状态指示灯（🔴 忙 / 🟡 中 / 🟢 闲）
- 高峰期自动限流保护
- 空闲时开放 DNA 追本溯源
- 模块功能地图展示

用法:
    python3 system_status_panel.py
    python3 system_status_panel.py --load 85
    python3 system_status_panel.py --module longhun_persona_hub
"""

import os
import re
import json
import time
import psutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


class 龍魂状态面板:
    DNA = "#龍芯⚡️2026-06-24-LONGHUN-STATUS-PANEL-v1.0"

    # 三色阈值
    THRESHOLDS = {
        "cpu": {"red": 80, "yellow": 50},
        "memory": {"red": 85, "yellow": 60},
        "tasks": {"red": 20, "yellow": 10},
    }

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.module_map = self._加载模块地图()

    def _加载模块地图(self) -> Dict[str, Any]:
        path = self.base_dir / "module_map.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def 系统负载(self) -> Dict[str, float]:
        """获取系统负载指标"""
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
            # 任务数用当前进程线程数估算
            tasks = len(psutil.Process().threads())
        except Exception:
            cpu, mem, load, tasks = 0.0, 0.0, 0.0, 0
        return {
            "cpu_percent": cpu,
            "memory_percent": mem,
            "system_load": load,
            "active_tasks": tasks,
            "timestamp": datetime.now().isoformat(),
        }

    def 三色状态(self, metrics: Optional[Dict] = None) -> Dict[str, Any]:
        """根据负载计算三色状态"""
        if metrics is None:
            metrics = self.系统负载()

        score = 0
        reasons = []
        t = self.THRESHOLDS

        if metrics["cpu_percent"] >= t["cpu"]["red"]:
            score = max(score, 3)
            reasons.append(f"CPU {metrics['cpu_percent']:.1f}%")
        elif metrics["cpu_percent"] >= t["cpu"]["yellow"]:
            score = max(score, 2)

        if metrics["memory_percent"] >= t["memory"]["red"]:
            score = max(score, 3)
            reasons.append(f"内存 {metrics['memory_percent']:.1f}%")
        elif metrics["memory_percent"] >= t["memory"]["yellow"]:
            score = max(score, 2)

        if metrics["active_tasks"] >= t["tasks"]["red"]:
            score = max(score, 3)
            reasons.append(f"并发任务 {metrics['active_tasks']}")
        elif metrics["active_tasks"] >= t["tasks"]["yellow"]:
            score = max(score, 2)

        if score == 3:
            color, label, emoji = "red", "高峰期 · 限流保护", "🔴"
        elif score == 2:
            color, label, emoji = "yellow", "平峰期 · 队列缓冲", "🟡"
        else:
            color, label, emoji = "green", "空闲期 · 开放溯源", "🟢"

        return {
            "color": color,
            "label": label,
            "emoji": emoji,
            "score": score,
            "reasons": reasons,
            "metrics": metrics,
        }

    def 高峰保护策略(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """根据状态给出保护策略"""
        if status["color"] == "red":
            return {
                "mode": "throttle",
                "max_concurrent": 3,
                "enable_cache": True,
                "compress_output": True,
                "show_summary_only": True,
                "dna_trace_depth": 1,
                "message": "🔴 高峰期：已启用限流，仅输出摘要，压缩传输，DNA 追溯深度限制为 1 层",
            }
        elif status["color"] == "yellow":
            return {
                "mode": "buffer",
                "max_concurrent": 8,
                "enable_cache": True,
                "compress_output": False,
                "show_summary_only": False,
                "dna_trace_depth": 3,
                "message": "🟡 平峰期：启用队列缓冲，正常输出，DNA 追溯深度 3 层",
            }
        else:
            return {
                "mode": "full",
                "max_concurrent": 16,
                "enable_cache": False,
                "compress_output": False,
                "show_summary_only": False,
                "dna_trace_depth": 10,
                "message": "🟢 空闲期：全功能开放，DNA 追本溯源至最大深度",
            }

    def 模块地图(self, query: Optional[str] = None) -> Dict[str, Any]:
        """展示模块功能地图"""
        modules = self.module_map.get("modules", {})
        if query:
            modules = {k: v for k, v in modules.items() if query.lower() in k.lower() or query.lower() in v.get("desc", "").lower()}
        return {
            "DNA": self.DNA,
            "模块总数": len(modules),
            "查询": query,
            "模块": modules,
        }

    def 完整报告(self, query: Optional[str] = None, simulated_load: Optional[float] = None) -> Dict[str, Any]:
        metrics = self.系统负载()
        if simulated_load is not None:
            metrics["cpu_percent"] = simulated_load
        status = self.三色状态(metrics)
        guard = self.高峰保护策略(status)
        mod_map = self.模块地图(query)

        return {
            "DNA": self.DNA,
            "时间": datetime.now().isoformat(),
            "状态": status,
            "保护策略": guard,
            "模块地图": mod_map,
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂系统状态面板")
    parser.add_argument("--load", "-l", type=float, help="模拟 CPU 负载百分比")
    parser.add_argument("--query", "-q", type=str, help="查询模块")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    panel = 龍魂状态面板()
    report = panel.完整报告(query=args.query, simulated_load=args.load)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = report["状态"]
        guard = report["保护策略"]
        print("=" * 60)
        print(f" {status['emoji']} 龍魂系统状态面板 · {status['label']}")
        print("=" * 60)
        print(f"   CPU: {status['metrics']['cpu_percent']:.1f}%")
        print(f"   内存: {status['metrics']['memory_percent']:.1f}%")
        print(f"   活跃任务: {status['metrics']['active_tasks']}")
        print(f"   系统负载: {status['metrics']['system_load']:.2f}")
        if status["reasons"]:
            print(f"   触发原因: {', '.join(status['reasons'])}")
        print(f"\n🛡️  {guard['message']}")
        print(f"   模式: {guard['mode']}")
        print(f"   最大并发: {guard['max_concurrent']}")
        print(f"   压缩输出: {'是' if guard['compress_output'] else '否'}")
        print(f"   DNA 追溯深度: {guard['dna_trace_depth']}")
        print("\n🗺️ 模块功能地图:")
        for name, info in report["模块地图"]["模块"].items():
            print(f"   {name}: {info.get('desc', '')}")
        print("=" * 60)


if __name__ == "__main__":
    main()
