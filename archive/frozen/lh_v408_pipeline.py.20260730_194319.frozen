#!/usr/bin/env python3
#龍芯⚡️2026-07-19-LONGHUN-V408-PIPELINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.0.8 全自动流水线
数据: v4.0.7 + 八卦阵 v1.1 + 道德经定锚 v1.1 + 水军显化 v1.2 + 焊死核心 QA ×30
配置: 保守 LoRA (rank=16, alpha=32, layers=12, lr=1e-5)
DNA: #龍芯⚡️2026-07-19-LONGHUN-V408-PIPELINE-v1.0
"""

import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
TRAINER = PROJECT / "bin" / "lh_lora_trainer_v408.py"
VALIDATOR = PROJECT / "bin" / "lh_validate_v408.py"
NEXT_WATCHER = PROJECT / "bin" / "lh_v408_to_v409_watcher.py"
PID_FILE = PROJECT / ".longhun" / "v408_pipeline.pid"


def run(cmd: list):
    print("\n" + "=" * 60)
    print(f"🚀 {' '.join(str(c) for c in cmd)}")
    print("=" * 60)
    result = subprocess.run([PYTHON] + [str(c) for c in cmd], cwd=PROJECT)
    if result.returncode != 0:
        print(f"🔴 步骤失败，退出码: {result.returncode}")
        sys.exit(result.returncode)


def start_next_watcher():
    """v4.0.8 验证通过后，启动 v4.0.8 → v4.0.9 自动接力看守器。"""
    print("\n" + "=" * 60)
    print("🚀 v4.0.8 完成，启动 v4.0.9 接力看守器")
    print("=" * 60)
    log_file = PROJECT / ".longhun" / "v408_v409_watcher.log"
    out = open(log_file, "a", encoding="utf-8")
    subprocess.Popen(
        [PYTHON, str(NEXT_WATCHER)],
        cwd=PROJECT,
        stdout=out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    print(f"✅ v4.0.9 接力看守器已后台启动，日志: {log_file}")


def main():
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    try:
        steps = [
            [TRAINER, "setup"],
            [TRAINER, "prepare"],
            [TRAINER, "train"],
            [TRAINER, "fuse"],
            [TRAINER, "export"],
            [VALIDATOR],
        ]
        for step in steps:
            run(step)

        start_next_watcher()

        print("\n" + "=" * 60)
        print("🎉 v4.0.8 流水线完成")
        print("=" * 60)
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()


if __name__ == "__main__":
    main()
