#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️20260720-V409-GUARDIAN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 v4.0.9 训练守护进程
职责：
  1. iter 2000 决策线：Val Loss > 0.767 → 切换 v4.0.8-iter1900 golden checkpoint
  2. 断电保险：电量 <15% 或 AC 断开 → 暂停训练；恢复后继续
  3. 进程守护：训练挂掉 → 从最新 checkpoint 重启
  4. 异常即时上报：Val Loss 暴涨、进程挂、电量 <15%
DNA: #龍芯⚡️20260720-V409-GUARDIAN-v1.0
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
TRAINER = PROJECT / "bin" / "lh_lora_trainer_v409.py"
VALIDATOR = PROJECT / "bin" / "lh_validate_v409.py"
LOG_DIR = PROJECT / ".longhun"
LOG_FILE = LOG_DIR / "v409_guardian.log"
FLAG_V408 = LOG_DIR / "v409_use_v408_golden"
PID_FILE = LOG_DIR / "v409_guardian.pid"

# 决策阈值
ITER_DECISION = 2000
VAL_LOSS_TARGET = 0.767
BATTERY_PAUSE_PCT = 15
BATTERY_RESUME_PCT = 20
CHECK_INTERVAL = 60  # 秒


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, level="INFO"):
    line = f"[{now()}] [{level}] {msg}"
    print(line)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def write_pid():
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def remove_pid():
    if PID_FILE.exists():
        PID_FILE.unlink()


def get_battery_status():
    """返回 (电量百分比, 是否接AC)."""
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True, text=True, timeout=5
        )
        text = result.stdout
        # 解析: "-InternalBattery-0 (id=...)\t17%; charging; ..."
        m = re.search(r'(\d+)%', text)
        pct = int(m.group(1)) if m else None
        on_ac = "AC Power" in text or "charging" in text.lower()
        return pct, on_ac
    except Exception as e:
        log(f"电量读取失败: {e}", "WARN")
        return None, None


def parse_training_log():
    """解析 training.log，返回 (latest_iter, latest_val, best_iter, best_val)."""
    log_path = PROJECT / "models" / "longhun-v1.0" / "lora_output_v409" / "training.log"
    latest_iter = 0
    latest_val = float("inf")
    best_iter = 0
    best_val = float("inf")
    if not log_path.exists():
        return latest_iter, latest_val, best_iter, best_val
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = re.search(r'Iter (\d+): Val loss ([\d.]+)', line)
            if m:
                it = int(m.group(1))
                vl = float(m.group(2))
                latest_iter = max(latest_iter, it)
                latest_val = vl
                if vl < best_val:
                    best_val = vl
                    best_iter = it
    return latest_iter, latest_val, best_iter, best_val


def find_latest_checkpoint():
    """查找 v4.0.9 adapter 目录下最新的编号 checkpoint。"""
    adapter_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v409" / "adapter_v409"
    if not adapter_dir.exists():
        return None
    checkpoints = sorted(adapter_dir.glob("*_adapters.safetensors"))
    if checkpoints:
        return checkpoints[-1]
    if (adapter_dir / "adapters.safetensors").exists():
        return adapter_dir / "adapters.safetensors"
    return None


def archive_v409_checkpoints(reason: str):
    """切换恢复源前，备份当前 v4.0.9 checkpoint。"""
    adapter_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v409" / "adapter_v409"
    if not adapter_dir.exists():
        return
    backup_dir = PROJECT / "models" / "longhun-v1.0" / "checkpoint_archive" / f"v409_before_switch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for f in adapter_dir.glob("*.safetensors"):
        shutil.copy2(f, backup_dir / f.name)
    log(f"📦 v4.0.9 checkpoint 已备份: {backup_dir} ({reason})")


def set_resume_source(source: str):
    """
    source: 'v407' | 'v408_golden' | 'latest_v409'
    通过 flag 文件告知 trainer 从哪恢复。
    """
    if source == "v408_golden":
        archive_v409_checkpoints("切换 golden checkpoint")
        FLAG_V408.write_text("golden", encoding="utf-8")
    else:
        if FLAG_V408.exists():
            FLAG_V408.unlink()
    log(f"恢复源设为: {source}")


def run_train():
    """启动训练子进程。"""
    log("🚀 启动 v4.0.9 训练")
    out = open(PROJECT / "models" / "longhun-v1.0" / "lora_output_v409" / "training.log", "a", encoding="utf-8")
    proc = subprocess.Popen(
        [PYTHON, str(TRAINER), "train"],
        cwd=PROJECT,
        stdout=out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log(f"   训练进程 pid={proc.pid}")
    return proc


def stop_train(proc, reason):
    """优雅停止训练。"""
    if proc is None or proc.poll() is not None:
        return None
    log(f"⏸️ 停止训练: {reason} (pid={proc.pid})")
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        log("   SIGTERM 超时，强制 SIGKILL", "WARN")
        proc.kill()
        proc.wait()
    return None


def run_fuse_export_validate():
    """训练完成后执行 fuse/export/validate。"""
    for step in ["fuse", "export"]:
        log(f"🚀 执行 {step}")
        r = subprocess.run([PYTHON, str(TRAINER), step], cwd=PROJECT)
        if r.returncode != 0:
            log(f"🔴 {step} 失败，退出码 {r.returncode}", "ERROR")
            return False
    log("🚀 执行验证")
    r = subprocess.run([PYTHON, str(VALIDATOR)], cwd=PROJECT)
    if r.returncode != 0:
        log(f"🔴 验证失败，退出码 {r.returncode}", "ERROR")
        return False
    log("🎉 v4.0.9 流水线完成")
    return True


def main():
    write_pid()
    try:
        log("=" * 60)
        log("龍魂 v4.0.9 Guardian 启动")
        log(f"决策线: iter {ITER_DECISION} Val Loss <= {VAL_LOSS_TARGET}")
        log(f"断电保险: <{BATTERY_PAUSE_PCT}% 或 AC 断开暂停，>{BATTERY_RESUME_PCT}% 且 AC 恢复继续")
        log("=" * 60)

        # 初始恢复源：v4.0.7 adapter
        set_resume_source("v407")

        proc = None
        paused_by_power = False
        decision_made = False
        training_finished = False

        while not training_finished:
            pct, on_ac = get_battery_status()
            log(f"🔋 电量={pct}% AC={on_ac}")

            # 断电保险
            if not paused_by_power and (pct is not None and pct < BATTERY_PAUSE_PCT or on_ac is False):
                proc = stop_train(proc, f"电量={pct}% AC={on_ac}，触发断电保险")
                paused_by_power = True
                log("🔴 异常即时报：训练因电量/AC 中断暂停", "ALERT")
                time.sleep(CHECK_INTERVAL)
                continue

            if paused_by_power:
                if on_ac and pct is not None and pct > BATTERY_RESUME_PCT:
                    log("🔌 供电恢复，继续训练")
                    paused_by_power = False
                    set_resume_source("latest_v409")
                    proc = run_train()
                else:
                    log(f"⏳ 等待供电恢复... 电量={pct}% AC={on_ac}")
                    time.sleep(CHECK_INTERVAL)
                    continue

            # 进程守护：训练没在跑就启动
            if proc is None or proc.poll() is not None:
                if proc is not None and proc.returncode != 0:
                    log(f"🔴 异常即时报：训练进程异常退出，code={proc.returncode}，从最新 checkpoint 重启", "ALERT")
                    set_resume_source("latest_v409")
                proc = run_train()

            # 决策线：iter 2000
            if not decision_made:
                latest_iter, latest_val, best_iter, best_val = parse_training_log()
                if latest_iter >= ITER_DECISION:
                    log(f"📊 iter {latest_iter} Val Loss={latest_val:.4f} (best={best_val:.4f}@{best_iter})")
                    if latest_val > VAL_LOSS_TARGET:
                        log(f"🔄 决策线触发：Val Loss {latest_val:.4f} > {VAL_LOSS_TARGET}，切换 v4.0.8-iter1900 golden checkpoint")
                        proc = stop_train(proc, "iter2000 决策线切换 checkpoint")
                        set_resume_source("v408_golden")
                        decision_made = True
                        proc = run_train()
                    else:
                        log(f"✅ 决策线通过：Val Loss {latest_val:.4f} <= {VAL_LOSS_TARGET}，继续 v4.0.9")
                        decision_made = True

            # Val Loss 暴涨检测（相对 best 涨 50% 以上）
            latest_iter, latest_val, best_iter, best_val = parse_training_log()
            if best_val != float("inf") and latest_val > best_val * 1.5:
                log(f"🔴 异常即时报：Val Loss 暴涨 {latest_val:.4f} vs best {best_val:.4f}", "ALERT")

            time.sleep(CHECK_INTERVAL)

        # 训练完成后 fuse/export/validate
        run_fuse_export_validate()

    except KeyboardInterrupt:
        log("🛑 Guardian 收到中断信号，停止训练", "WARN")
        if proc:
            stop_train(proc, "Guardian 中断")
    finally:
        remove_pid()


if __name__ == "__main__":
    main()
