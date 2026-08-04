#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 v4.0.7 → v4.0.8 自动接力看守器
DNA: #龍芯⚡️2026-07-19-V407-V408-WATCHER-v1.0

功能：
1. 监视 v4.0.7 流水线进程或完成标记
2. v4.0.7 成功后自动启动 v4.0.8 流水线
3. 失败或超时则报警，不盲动
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
V407_PID_FILE = PROJECT / ".longhun" / "v407_pipeline.pid"
V407_MARKER = PROJECT / "models" / "longhun-v1.0" / "lora_output_v407" / "VALIDATION_PASSED"
V407_VALIDATION_REPORT = PROJECT / "models" / "longhun-v1.0" / "lora_output_v407" / "validation_reports" / "latest.json"
V408_PIPELINE = PROJECT / "bin" / "lh_v408_pipeline.py"
WATCHER_LOG = PROJECT / ".longhun" / "v407_v408_watcher.log"

POLL_INTERVAL = 60  # 秒
TIMEOUT_HOURS = 12


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    WATCHER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WATCHER_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def v407_process_alive():
    if V407_PID_FILE.exists():
        try:
            pid = int(V407_PID_FILE.read_text().strip())
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError, OSError):
            return False
    # fallback: grep current process
    result = subprocess.run(
        ["pgrep", "-f", "lh_v407_pipeline.py"],
        capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def v407_success():
    if V407_MARKER.exists():
        return True
    if V407_VALIDATION_REPORT.exists():
        try:
            report = json.loads(V407_VALIDATION_REPORT.read_text(encoding="utf-8"))
            return report.get("overall_pass", False)
        except Exception:
            pass
    return False


def start_v408():
    log("🚀 v4.0.7 完成且验证通过，启动 v4.0.8 流水线")
    log_file = PROJECT / ".longhun" / "v408_pipeline.log"
    out = open(log_file, "a", encoding="utf-8")
    subprocess.Popen(
        [sys.executable, str(V408_PIPELINE)],
        cwd=PROJECT,
        stdout=out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log(f"✅ v4.0.8 流水线已后台启动，日志: {log_file}")


def main():
    log("👁️ 启动 v4.0.7 → v4.0.8 看守器")
    log(f"轮询间隔: {POLL_INTERVAL}s | 超时: {TIMEOUT_HOURS}h")

    start = time.time()
    while True:
        elapsed_hours = (time.time() - start) / 3600
        if elapsed_hours > TIMEOUT_HOURS:
            log(f"🔴 看守超时（>{TIMEOUT_HOURS}h），退出")
            sys.exit(1)

        alive = v407_process_alive()
        if alive:
            log("⏳ v4.0.7 仍在运行，继续监视...")
            time.sleep(POLL_INTERVAL)
            continue

        # 进程已结束
        if v407_success():
            start_v408()
            sys.exit(0)
        else:
            log("🟡 v4.0.7 进程结束但未检测到成功标记，等待 5 分钟后重试")
            time.sleep(300)
            if v407_success():
                start_v408()
                sys.exit(0)
            else:
                log("🔴 v4.0.7 未成功，不启动 v4.0.8")
                sys.exit(1)


if __name__ == "__main__":
    main()
