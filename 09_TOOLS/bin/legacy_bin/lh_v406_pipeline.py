#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.0.6 全自动流水线
数据: v3.7 + 全记忆 ingestion
配置: 保守 LoRA (rank=16, alpha=32, layers=12, lr=1e-5)
DNA: #龍芯⚡️2026-07-19-LONGHUN-V406-PIPELINE-v1.0
"""

import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
TRAINER = PROJECT / "bin" / "lh_lora_trainer_v406.py"
VALIDATOR = PROJECT / "bin" / "lh_validate_v406.py"


def run(cmd: list):
    print("\n" + "=" * 60)
    print(f"🚀 {' '.join(str(c) for c in cmd)}")
    print("=" * 60)
    result = subprocess.run([PYTHON] + [str(c) for c in cmd], cwd=PROJECT)
    if result.returncode != 0:
        print(f"🔴 步骤失败，退出码: {result.returncode}")
        sys.exit(result.returncode)


def main():
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

    print("\n" + "=" * 60)
    print("🎉 v4.0.6 流水线完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
