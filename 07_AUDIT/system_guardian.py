#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统守护者 · LongHun System Guardian

全系统检测：
  - 门户 HTTP/HTTPS 可访问性
  - DNS 解析是否正确
  - HTTPS 证书有效期
  - systemd 服务状态
  - 磁盘空间

发现异常则写入 `~/.longhun/audit/system_guardian.jsonl`，
可扩展为短信/邮件告警。

DNA:#龍芯⚡️2026-06-20-LONGHUN-SYSTEM-GUARDIAN-FILE1-v1.0
"""

import json
import shutil
import socket
import ssl
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple, Any


class 系统守护者:
    def __init__(
        self,
        域名: str = "longhun888.com",
        IP: str = "119.13.90.27",
        服务名: str = "longhun-sovereignty",
        日志路径: str = "~/.longhun/audit/system_guardian.jsonl",
        磁盘阈值: float = 90.0,
    ):
        self.域名 = 域名
        self.IP = IP
        self.服务名 = 服务名
        self.磁盘阈值 = 磁盘阈值
        self.日志路径 = Path(日志路径).expanduser()
        self.日志路径.parent.mkdir(parents=True, exist_ok=True)

    def _记录(self, report: dict[str, Any]) -> dict[str, Any]:
        with open(self.日志路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")
        return report

    def 检查HTTP(self, url: str) -> Tuple[bool, str]:
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                _ = r.read(64)
                return r.status in (200, 301, 302), f"status={r.status}"
        except Exception as e:
            return False, str(e)

    def 检查DNS(self) -> Tuple[bool, str]:
        try:
            解析 = socket.gethostbyname(self.域名)
            return 解析 == self.IP, f"resolved={解析} expected={self.IP}"
        except Exception as e:
            return False, str(e)

    def 检查证书(self) -> Tuple[bool, str]:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((self.域名, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.域名) as ssock:
                    cert = ssock.getpeercert()
                    expire = cert.get("notAfter")
                    days = self._证书剩余天数(expire)
                    return days > 7, f"expire={expire} days_left={days}"
        except Exception as e:
            return False, str(e)

    def _证书剩余天数(self, expire_str: str) -> int:
        from datetime import datetime
        fmt = "%b %d %H:%M:%S %Y %Z"
        expire = datetime.strptime(expire_str, fmt)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return max(0, (expire - now).days)

    def 检查服务(self) -> Tuple[bool, str]:
        if not shutil.which("systemctl"):
            return True, "systemctl-not-available-on-local"
        try:
            out = subprocess.run(
                ["systemctl", "is-active", self.服务名],
                capture_output=True,
                text=True,
                timeout=5,
            )
            ok = out.stdout.strip() == "active"
            return ok, out.stdout.strip()
        except Exception as e:
            return False, str(e)

    def 检查磁盘(self) -> Tuple[bool, str]:
        try:
            usage = shutil.disk_usage("/")
            percent = usage.used / usage.total * 100
            return percent < self.磁盘阈值, f"used_percent={percent:.1f}%"
        except Exception as e:
            return False, str(e)

    def 全检(self) -> dict[str, Any]:
        checks: Dict[str, Tuple[bool, str]] = {
            "portal_http": self.检查HTTP(f"http://{self.IP}/"),
            "portal_https": self.检查HTTP(f"https://{self.域名}/"),
            "api_info": self.检查HTTP(f"http://{self.IP}/api/info"),
            "dns": self.检查DNS(),
            "cert": self.检查证书(),
            "service": self.检查服务(),
            "disk": self.检查磁盘(),
        }
        overall = all(v[0] for v in checks.values())
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall": "healthy" if overall else "alert",
            "domain": self.域名,
            "ip": self.IP,
            "checks": {
                k: {"ok": v[0], "detail": v[1]} for k, v in checks.items()
            },
        }
        return self._记录(report)

    def 简报(self) -> str:
        r = self.全检()
        lines = [
            f"🐉 龍魂系统守护者 · {r['timestamp']}",
            f"整体状态: {'🟢 健康' if r['overall']=='healthy' else '🔴 告警'}",
        ]
        for k, v in r["checks"].items():
            icon = "✅" if v["ok"] else "❌"
            lines.append(f"  {icon} {k}: {v['detail']}")
        return "\n".join(lines)


if __name__ == "__main__":
    守护者 = 系统守护者()
    print(守护者.简报())
