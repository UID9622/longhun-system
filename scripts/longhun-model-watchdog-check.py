# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂模型看门狗双重保险检查 v1.0
DNA: #龍芯⚡️丙午·辛未·WATCHDOG-CHECK-v1.0

crontab 每5分钟调用一次，确保看门狗进程存活。
若看门狗已死，自动重启；若触发文件滞留超时，强制清理。
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

LONGHUN_ROOT = Path.home() / "longhun-system"
MODEL_DIR = LONGHUN_ROOT / "models"
SCRIPTS_DIR = LONGHUN_ROOT / "scripts"
TRIGGER_FILE = MODEL_DIR / ".retrain_trigger"
WATCHDOG_SCRIPT = SCRIPTS_DIR / "longhun-model-watchdog.py"

DNA = "UID9622-ONLY-ONCE🧬LK9X-772Z"


def main():
    pid = os.getpid()
    now = int(time.time())

    # 1. 检查是否有滞留触发文件
    if TRIGGER_FILE.exists():
        try:
            trigger = json.loads(TRIGGER_FILE.read_text())
            triggered_at = trigger.get("triggered_at", 0)
            if now - triggered_at > 600:  # 10分钟
                print(f"[{now}] ⚠️ 触发文件滞留 {now - triggered_at}s，强制清理")
                TRIGGER_FILE.unlink()
        except (json.JSONDecodeError, IOError):
            TRIGGER_FILE.unlink()
            print(f"[{now}] 🧹 清理损坏的触发文件")

    # 2. 检查看门狗进程
    try:
        result = subprocess.run(
            ["pgrep", "-f", "longhun-model-watchdog.py"],
            capture_output=True, text=True, timeout=5,
        )
        watchdog_pids = [p for p in result.stdout.strip().split("\n") if p and p != str(pid)]

        if not watchdog_pids:
            print(f"[{now}] ❌ 看门狗未运行，尝试重启...")
            subprocess.Popen(
                [sys.executable, str(WATCHDOG_SCRIPT)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            print(f"[{now}] ✅ 看门狗已重启")
        else:
            print(f"[{now}] ✅ 看门狗运行中 (PID: {', '.join(watchdog_pids)})")
    except Exception as e:
        print(f"[{now}] ⚠️ 进程检查异常: {e}")


if __name__ == "__main__":
    main()
