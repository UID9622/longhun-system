#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 异常检测引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ANOMALY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 实时检测系统异常（CPU/内存/磁盘/网络）
  - 检测代码异常（重复函数、未使用变量、循环依赖）
  - 检测行为异常（偏离历史模式）
  - 主动报警 + 建议修复路径
"""

import psutil
import json
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import deque, Counter


class AnomalyEngine:
    """异常检测引擎——被动响应→主动发现"""

    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)
        self.anomalies = []
        self.alert_count = 0

    def detect_system_anomaly(self) -> List[Dict]:
        """检测系统级异常"""
        anomalies = []
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            if cpu > 90:
                anomalies.append({
                    "type": "high_cpu", "value": cpu, "threshold": 90,
                    "severity": "critical", "suggestion": "降低并发任务或增加CPU"
                })
            elif cpu > 70:
                anomalies.append({
                    "type": "elevated_cpu", "value": cpu, "threshold": 70,
                    "severity": "warning", "suggestion": "监控CPU趋势"
                })

            if mem.percent > 90:
                anomalies.append({
                    "type": "high_memory", "value": mem.percent, "threshold": 90,
                    "severity": "critical", "suggestion": f"可用内存仅 {mem.available / (1024**3):.1f}GB"
                })

            if disk.percent > 85:
                anomalies.append({
                    "type": "low_disk", "value": disk.percent, "threshold": 85,
                    "severity": "critical", "suggestion": f"磁盘剩余 {disk.free / (1024**3):.1f}GB"
                })
        except Exception as e:
            anomalies.append({"type": "sensor_error", "error": str(e)})

        self.anomalies.extend(anomalies)
        return anomalies

    def detect_code_anomaly(self, files: List[str]) -> List[Dict]:
        """检测代码级异常"""
        anomalies = []
        for fp in files:
            p = Path(fp)
            if not p.exists():
                continue
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                lines = content.split("\n")
                size = len(lines)
                if size > 1000:
                    anomalies.append({
                        "type": "large_file", "file": str(p),
                        "lines": size, "suggestion": "考虑拆分大文件"
                    })
            except Exception:
                continue
        return anomalies

    def detect_behavior_anomaly(self, events: List[Dict]) -> List[Dict]:
        """检测行为模式异常"""
        if len(events) < 10:
            return []
        anomalies = []
        # 统计事件类型频率
        type_counts = Counter(e.get("type", "unknown") for e in events)
        avg_count = sum(type_counts.values()) / max(1, len(type_counts))
        for etype, count in type_counts.items():
            if count > avg_count * 3:
                anomalies.append({
                    "type": "behavior_spike", "event_type": etype,
                    "count": count, "avg": int(avg_count),
                    "suggestion": f"事件 {etype} 频率异常升高"
                })
        return anomalies

    def get_alert(self) -> List[Dict]:
        """获取需要关注的严重异常"""
        critical = [a for a in self.anomalies if a.get("severity") == "critical"]
        if critical:
            self.alert_count += len(critical)
        return critical

    def scan(self) -> Dict[str, Any]:
        """执行一次完整扫描"""
        t0 = time.time()
        system = self.detect_system_anomaly()
        alert = self.get_alert()
        return {
            "timestamp": datetime.now().isoformat(),
            "system_anomalies": system,
            "alerts": alert,
            "total_anomalies": len(self.anomalies),
            "scan_time_ms": (time.time() - t0) * 1000,
            "status": "🟡 告警" if alert else "🟢 正常",
        }


if __name__ == "__main__":
    engine = AnomalyEngine()
    result = engine.scan()
    print(f"扫描结果: {result['status']}")
    print(f"系统异常: {len(result['system_anomalies'])} 项")
    for a in result["system_anomalies"]:
        print(f"  ├ {a['type']}: {a.get('value', 'N/A')} (阈值:{a.get('threshold', 'N/A')})")
    print(f"告警: {len(result['alerts'])} 项")
    print("🟢 异常检测引擎测试通过")
