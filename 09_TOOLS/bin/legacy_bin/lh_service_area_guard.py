#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 · 服务区训练守护进程
DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-SERVICE-AREA-GUARD-v1.0

功能：
1. 调用 macOS caffeinate 防止训练时系统休眠
2. 每分钟监控电池电量与电源状态
3. 高温/低电量/断电时日志告警（不自动停止，由老大决策）
4. 训练完成后自动退出
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT / ".longhun" / "service_area_guard.log"
PID_FILE = PROJECT / ".longhun" / "v407_pipeline.pid"
V408_PID_FILE = PROJECT / ".longhun" / "v408_pipeline.pid"
V407_DONE = PROJECT / "models" / "longhun-v1.0" / "lora_output_v407" / "VALIDATION_PASSED"
V408_DONE = PROJECT / "models" / "longhun-v1.0" / "lora_output_v408" / "VALIDATION_PASSED"

POLL_INTERVAL = 30  # 秒
BATTERY_LOW_THRESHOLD = 25  # %


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_battery_info():
    """返回 (电量百分比, 是否连接电源, 是否正在充电, 剩余时间估算)"""
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True, text=True, timeout=5
        )
        text = result.stdout
        # 示例："Now drawing from 'Battery Power'\n -InternalBattery-0 (id=...)  68%; discharging; 2:30 remaining"
        pct_match = re.search(r"(\d+)%", text)
        pct = int(pct_match.group(1)) if pct_match else -1
        ac_connected = "AC Power" in text or "charging" in text.lower()
        charging = "charging" in text.lower() and "discharging" not in text.lower()
        return pct, ac_connected, charging, text.strip()
    except Exception as e:
        return -1, False, False, f"读取失败: {e}"


def training_running():
    """只要 v4.0.7 或 v4.0.8 任一 Pipeline 在跑，就认为训练进行中"""
    for pf in [PID_FILE, V408_PID_FILE]:
        if pf.exists():
            try:
                pid = int(pf.read_text().strip())
                os.kill(pid, 0)
                return True
            except Exception:
                pass
    # fallback: grep process
    result = subprocess.run(
        ["pgrep", "-f", "lh_v40[78]_pipeline.py"],
        capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def training_done():
    return V408_DONE.exists() or (V407_DONE.exists() and not training_running())


def main():
    log("🛡️ 服务区训练守护进程启动")
    log("功能：防休眠 + 电池监控 + 训练完成自动退出")

    # 启动 caffeinate 子进程，防止空闲休眠（不影响显示器睡眠）
    caffeinate = subprocess.Popen(
        ["caffeinate", "-i", "-w", str(os.getpid())],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    log(f"☕ caffeinate 已启动（PID {caffeinate.pid}），系统不会进入空闲睡眠")

    warned_low_battery = False

    try:
        while True:
            pct, ac, charging, raw = get_battery_info()
            status = f"🔋 {pct}%"
            if ac:
                status += " ⚡接电源"
            elif charging:
                status += " 🔌充电中"
            else:
                status += " 🔋电池供电"

            if pct > 0 and pct < BATTERY_LOW_THRESHOLD and not ac:
                if not warned_low_battery:
                    log(f"🚨 低电量告警：{pct}%，未接电源！建议接入电源或保存模型后暂停")
                    warned_low_battery = True
            else:
                warned_low_battery = False

            if not training_running():
                if V408_DONE.exists():
                    log("✅ v4.0.8 验证已通过，训练全部完成，守护退出")
                    break
                if V407_DONE.exists():
                    log("✅ v4.0.7 验证已通过，等待 v4.0.8 启动...")
                else:
                    log("⚠️ 未检测到训练进程，继续监视...")

            log(status)
            time.sleep(POLL_INTERVAL)
    finally:
        caffeinate.terminate()
        log("🛑 服务区守护进程退出")


if __name__ == "__main__":
    main()
