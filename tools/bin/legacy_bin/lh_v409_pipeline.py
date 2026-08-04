#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.0.9 全自动流水线
数据: v4.0.8 全量 + Notion 本地镜像 + GitHub 公开仓库 + 本地仓库统一来源 + 核心焊死 QA ×30
配置: 保守 LoRA (rank=16, alpha=32, layers=12, lr=1e-5)
DNA: #龍芯⚡️2026-07-19-LONGHUN-V409-PIPELINE-v1.0
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
TRAINER = PROJECT / "bin" / "lh_lora_trainer_v409.py"
VALIDATOR = PROJECT / "bin" / "lh_validate_v409.py"
PID_FILE = PROJECT / ".longhun" / "v409_pipeline.pid"


def run(cmd: list):
    print("\n" + "=" * 60)
    print(f"🚀 {' '.join(str(c) for c in cmd)}")
    print("=" * 60)
    result = subprocess.run([PYTHON] + [str(c) for c in cmd], cwd=PROJECT)
    if result.returncode != 0:
        print(f"🔴 步骤失败，退出码: {result.returncode}")
        sys.exit(result.returncode)


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

        print("\n" + "=" * 60)
        print("🎉 v4.0.9 流水线完成")
        print("=" * 60)
    finally:
        if PID_FILE.exists():
            PID_FILE.unlink()


if __name__ == "__main__":
    main()
