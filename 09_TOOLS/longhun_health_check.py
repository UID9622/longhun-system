#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂服务健康检查 · 自动重启
DNA: #龍芯⚡️2026-07-05-LONGHUN-HEALTH-CHECK-v1.0

用法：
  python3 longhun_health_check.py          # 检查一次并打印报告
  python3 longhun_health_check.py --watch  # 持续守护（每 30 秒检查）
  python3 longhun_health_check.py --fix    # 发现失败时自动调用补全服务脚本
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

HOME = Path.home()
ROOT = HOME / "longhun-system"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
FIX_SCRIPT = ROOT / "tools" / "补全服务.sh"
STARTER_SCRIPT = ROOT / "tools" / "start_longhun888_services.sh"


@dataclass
class ServiceCheck:
    name: str
    port: int
    host: str = "127.0.0.1"
    path: str = "/"
    critical: bool = True  # 失败时是否触发重启


SERVICES: List[ServiceCheck] = [
    ServiceCheck("longhun888 门户", 8777, path="/web/CNSH_龍魂操作台v4.0.html"),
    ServiceCheck("CNSH 编辑器 API", 18000, path="/docs"),
    ServiceCheck("L0 道德经伦理锚定", 9630, path="/stats"),
    ServiceCheck("龍魂对话 L0", 9635, path="/health"),
    ServiceCheck("v10 API", 18100, path="/health"),
    ServiceCheck("操作台 p0-controls", 9622, path="/"),
    ServiceCheck("卦象审计", 9623, path="/"),
    ServiceCheck("龍之心语", 9624, path="/health"),
    ServiceCheck("龍魂脑干", 9625, path="/health"),
]


def probe_tcp(check: ServiceCheck, timeout: float = 2.0) -> bool:
    """TCP 端口连通性探测（不依赖 HTTP/CORS）。"""
    try:
        with socket.create_connection((check.host, check.port), timeout=timeout):
            return True
    except Exception:
        return False


def run_fix() -> bool:
    """调用补全脚本尝试恢复服务。"""
    print("🔧 尝试自动修复：调用补全服务脚本...")
    try:
        result = subprocess.run(
            ["bash", str(FIX_SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        # 将输出写入日志
        (LOG_DIR / "health-check-fix.out.log").write_text(result.stdout, encoding="utf-8")
        (LOG_DIR / "health-check-fix.err.log").write_text(result.stderr, encoding="utf-8")
        return result.returncode == 0
    except Exception as e:
        print(f"🔴 自动修复失败: {e}")
        return False


def check_all(fix: bool = False) -> Dict[str, any]:
    results: List[Dict] = []
    failed_critical: List[ServiceCheck] = []

    for svc in SERVICES:
        ok = probe_tcp(svc)
        status = "✅" if ok else "🔴"
        results.append({
            "name": svc.name,
            "port": svc.port,
            "ok": ok,
            "critical": svc.critical,
        })
        print(f"{status} {svc.name:<20} :{svc.port}  {'可达' if ok else '不可达'}")
        if not ok and svc.critical:
            failed_critical.append(svc)

    summary = {
        "total": len(SERVICES),
        "ok": sum(1 for r in results if r["ok"]),
        "failed": len(failed_critical),
        "details": results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }

    if failed_critical:
        print(f"\n⚠️  {len(failed_critical)} 个核心服务不可达")
        if fix:
            if run_fix():
                print("✅ 自动修复脚本已执行，等待服务恢复...")
                time.sleep(5)
                # 重新检查失败的
                still_failed = [s for s in failed_critical if not probe_tcp(s)]
                if not still_failed:
                    print("✅ 服务已全部恢复")
                else:
                    print(f"🔴 仍有 {len(still_failed)} 个服务未恢复")
            else:
                print("🔴 自动修复未成功")
    else:
        print("\n✅ 所有核心服务正常")

    # 写入 JSON 日志
    (LOG_DIR / "health-check-latest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def watch_loop(interval: int = 30, fix: bool = False):
    print(f"🛡️ 进入守护模式，每 {interval} 秒检查一次（按 Ctrl+C 退出）")
    while True:
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        check_all(fix=fix)
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="龍魂服务健康检查")
    parser.add_argument("--watch", action="store_true", help="持续守护模式")
    parser.add_argument("--fix", action="store_true", help="失败时自动修复")
    parser.add_argument("--interval", type=int, default=30, help="守护模式检查间隔（秒）")
    args = parser.parse_args()

    if args.watch:
        watch_loop(interval=args.interval, fix=args.fix)
    else:
        check_all(fix=args.fix)


if __name__ == "__main__":
    main()
