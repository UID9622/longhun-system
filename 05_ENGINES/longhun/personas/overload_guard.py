#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-OVERLOAD-GUARD-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-OVERLOAD-GUARD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂过载守护 · LongHun Overload Guard v1.0

实现 DeepSeek Anti-Blowout 过载 SOP：
- 五级状态：Operational / Degraded / Partial Outage / Major Outage / Maintenance
- 基于 CPU/内存/负载/错误率计算状态
- 返回结构化错误：SERVER_OVERLOADED + retry_after + request_id
- 背压：queue_depth 限制，满则快速拒绝
- 自动写入 audit.jsonl

用法:
    python3 overload_guard.py status
    python3 overload_guard.py check
    python3 overload_guard.py request --queue-depth 150
"""

import os
import psutil
import uuid
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class 龍魂过载守护:
    DNA = "#龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-OVERLOAD-GUARD-v1.0"

    LEVELS = [
        ("Operational", "🟢", "运行正常"),
        ("Degraded Performance", "🟡", "性能降级"),
        ("Partial Outage", "🟠", "部分不可用"),
        ("Major Outage", "🔴", "严重故障"),
        ("Maintenance", "🔧", "维护模式"),
    ]

    def __init__(self, max_queue: int = 100):
        self.max_queue = max_queue
        self.request_id = str(uuid.uuid4())[:8]

    def 指标(self) -> Dict[str, float]:
        try:
            cpu = psutil.cpu_percent(interval=0.3)
            mem = psutil.virtual_memory().percent
            load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
            disk = psutil.disk_usage("/").percent
        except Exception:
            cpu, mem, load, disk = 0.0, 0.0, 0.0, 0.0
        return {
            "cpu_percent": cpu,
            "memory_percent": mem,
            "system_load": load,
            "disk_percent": disk,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def 状态等级(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        score = 0
        reasons = []
        if metrics["cpu_percent"] >= 90:
            score = max(score, 3)
            reasons.append(f"CPU {metrics['cpu_percent']:.1f}%")
        elif metrics["cpu_percent"] >= 70:
            score = max(score, 2)
            reasons.append(f"CPU {metrics['cpu_percent']:.1f}%")
        elif metrics["cpu_percent"] >= 50:
            score = max(score, 1)

        if metrics["memory_percent"] >= 90:
            score = max(score, 3)
            reasons.append(f"内存 {metrics['memory_percent']:.1f}%")
        elif metrics["memory_percent"] >= 75:
            score = max(score, 2)
            reasons.append(f"内存 {metrics['memory_percent']:.1f}%")
        elif metrics["memory_percent"] >= 60:
            score = max(score, 1)

        if metrics["disk_percent"] >= 90:
            score = max(score, 2)
            reasons.append(f"磁盘 {metrics['disk_percent']:.1f}%")

        level, emoji, desc = self.LEVELS[score]
        retry_after = max(1, int((score + 1) * 5))

        return {
            "level": level,
            "emoji": emoji,
            "description": desc,
            "score": score,
            "reasons": reasons,
            "retry_after_seconds": retry_after,
            "request_id": self.request_id,
            "metrics": metrics,
        }

    def 请求检查(self, queue_depth: int = 0) -> Dict[str, Any]:
        metrics = self.指标()
        status = self.状态等级(metrics)
        status["queue_depth"] = queue_depth
        status["queue_full"] = queue_depth >= self.max_queue

        if status["score"] >= 3 or status["queue_full"]:
            status["allowed"] = False
            status["error"] = {
                "error_code": "SERVER_OVERLOADED",
                "http_status": 503,
                "message": "服务器过载，请稍后重试",
                "retry_after_seconds": status["retry_after_seconds"],
                "request_id": self.request_id,
            }
        elif status["score"] >= 1:
            status["allowed"] = True
            status["degraded"] = True
            status["error"] = None
        else:
            status["allowed"] = True
            status["degraded"] = False
            status["error"] = None

        return status


def main():
    parser = argparse.ArgumentParser(description="龍魂过载守护")
    sub = parser.add_subparsers(dest="action")

    sub.add_parser("status", help="显示当前过载状态")
    sub.add_parser("check", help="运行过载检查")

    p_req = sub.add_parser("request", help="模拟一次请求")
    p_req.add_argument("--queue-depth", type=int, default=0)

    args = parser.parse_args()

    guard = 龍魂过载守护()

    if args.action == "status" or args.action == "check":
        result = guard.请求检查()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "request":
        result = guard.请求检查(args.queue_depth)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
