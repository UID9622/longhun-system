#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-FACTORY-KUNPENG-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 鲲鹏联动 v1.0（v2.0 补全区块）
功能: 部署产物同步到鲲鹏服务器 + 远端健康检查
说明: SSH 优先用密钥(~/.ssh/longhun_kunpeng_ed25519)，鲲鹏 IP 与路径从
      环境变量读，不硬编码敏感信息
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .generate_dna import generate_dna

KUNPENG_HOST = os.environ.get("KUNPENG_HOST", "119.13.90.27")
KUNPENG_USER = os.environ.get("KUNPENG_USER", "root")
KUNPENG_REMOTE_DIR = os.environ.get("KUNPENG_REMOTE_DIR", "/opt/longhun/releases")
SSH_KEY = os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519")


class KunpengSync:
    """鲲鹏部署同步"""

    def __init__(self, host: str = None, user: str = None, remote_dir: str = None):
        self.host = host or KUNPENG_HOST
        self.user = user or KUNPENG_USER
        self.remote_dir = remote_dir or KUNPENG_REMOTE_DIR
        self._ssh_base = ["-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
                          "-o", "ConnectTimeout=10"]

    def _ssh(self, cmd: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["ssh", *self._ssh_base, f"{self.user}@{self.host}", cmd],
            capture_output=True, text=True, timeout=60)

    def sync(self, local_path: Path, version: str) -> Dict:
        """同步产物到鲲鹏"""
        dna = generate_dna("KUNPENG-SYNC")
        remote_target = f"{self.user}@{self.host}:{self.remote_dir}/{version}/"
        result = subprocess.run(
            ["rsync", "-az", "--delete", *self._ssh_base,
             str(local_path) + "/", remote_target],
            capture_output=True, text=True, timeout=300)

        status = "success" if result.returncode == 0 else "failed"
        return {
            "dna": dna,
            "status": status,
            "host": self.host,
            "remote": f"{self.remote_dir}/{version}",
            "stdout": result.stdout[-500:],
            "stderr": result.stderr[-500:],
            "timestamp": datetime.now().isoformat(),
        }

    def health_check(self) -> Dict:
        """鲲鹏远端健康检查"""
        dna = generate_dna("KUNPENG-HEALTH")
        result = self._ssh("uptime && free -h | head -2 && df -h / | tail -1")
        return {
            "dna": dna,
            "status": "ok" if result.returncode == 0 else "failed",
            "output": result.stdout.strip(),
            "timestamp": datetime.now().isoformat(),
        }

    def list_releases(self) -> List[str]:
        """列出鲲鹏远端发布版本"""
        result = self._ssh(f"ls -1t {self.remote_dir}/ 2>/dev/null || echo NO_RELEASES")
        if result.returncode != 0:
            return []
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return [] if lines == ["NO_RELEASES"] else lines
