#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-SELF-MONITOR-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 工厂自监控 v1.0
功能: 工厂自身健康检查（磁盘/内存/进程/网络）
注意: 关键进程名单与实际服务对齐，端口探测式判定（未监听=warning 不硬断）
"""

import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    import psutil
except ImportError:
    psutil = None

# 实际服务进程（与 systemd/launchd 对齐，缺失时仅 warning 提示）
KEY_PROCESSES = ["lh_auto_factory", "lh_knowledge_graph_v2", "lh_memory_load"]
# 实际服务端口（探测式: 开放=ok, 未开放=warning 注明）
KEY_PORTS = [8767, 8771, 9631]


class SelfMonitor:
    """工厂自监控"""

    def __init__(self, factory_root: Path):
        self.factory_root = factory_root
        self.last_check: Dict = {}
        self.check_history: List[Dict] = []

    def check(self) -> Dict:
        """执行自检"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "disk": self._check_disk(),
            "memory": self._check_memory(),
            "process": self._check_process(),
            "network": self._check_network(),
            "overall": "healthy",
        }

        # 整体判定
        sections = [results["disk"], results["memory"], results["process"], results["network"]]
        if any(s.get("status") == "critical" for s in sections):
            results["overall"] = "critical"
        elif any(s.get("status") == "warning" for s in sections):
            results["overall"] = "warning"

        self.last_check = results
        self.check_history.append(results)
        return results

    def _check_disk(self) -> Dict:
        """检查磁盘"""
        if psutil is None:
            return {"status": "warning", "message": "psutil 未安装，跳过磁盘检查"}
        percent = psutil.disk_usage(self.factory_root).percent
        if percent > 90:
            return {"status": "critical", "percent": percent, "message": f"磁盘使用率 {percent}%"}
        if percent > 75:
            return {"status": "warning", "percent": percent, "message": f"磁盘使用率 {percent}%"}
        return {"status": "ok", "percent": percent}

    def _check_memory(self) -> Dict:
        """检查内存"""
        if psutil is None:
            return {"status": "warning", "message": "psutil 未安装，跳过内存检查"}
        percent = psutil.virtual_memory().percent
        if percent > 90:
            return {"status": "critical", "percent": percent, "message": f"内存使用率 {percent}%"}
        if percent > 75:
            return {"status": "warning", "percent": percent, "message": f"内存使用率 {percent}%"}
        return {"status": "ok", "percent": percent}

    def _check_process(self) -> Dict:
        """检查关键进程"""
        if psutil is None:
            return {"status": "warning", "message": "psutil 未安装，跳过进程检查"}
        running = []
        for proc in psutil.process_iter(["name"]):
            try:
                running.append(proc.info["name"] or "")
            except Exception:
                continue
        missing = [p for p in KEY_PROCESSES if not any(p in r for r in running)]
        if missing:
            return {"status": "warning", "missing": missing, "message": f"未发现进程: {missing}"}
        return {"status": "ok"}

    def _check_network(self) -> Dict:
        """检查关键端口（探测式: 未开放只记 warning 注明，不硬断）"""
        open_ports, closed_ports = [], []
        for port in KEY_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                if sock.connect_ex(("127.0.0.1", port)) == 0:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
            except Exception:
                closed_ports.append(port)
            finally:
                sock.close()
        if closed_ports:
            return {"status": "warning", "open": open_ports, "closed": closed_ports,
                    "message": f"未监听端口: {closed_ports}"}
        return {"status": "ok", "open": open_ports}
