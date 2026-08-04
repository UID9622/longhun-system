#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 v4.0.5 全自动流水线（升容量 · Yi-1.5-9B-Chat）
DNA: #龍芯⚡️丙午·乙未·甲寅·未时·乾-V405-AUTO-PIPELINE-v1.0
"""

import subprocess, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "validation_reports" / "v4.0.5_validation_report.md"


def run(cmd: list[str], cwd: str | None = None, timeout: int = None):
    print(f"\n🚀 {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or str(PROJECT), capture_output=False, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return result


def main():
    print("=" * 60)
    print("🐉 龍魂 v4.0.5 全自动流水线启动（Yi-1.5-9B-Chat · rank=64 · layers=24）")
    print("=" * 60)

    run([sys.executable, "bin/lh_lora_trainer_v405.py", "setup"], timeout=2400)
    run([sys.executable, "bin/lh_lora_trainer_v405.py", "prepare"], timeout=300)
    run([sys.executable, "bin/lh_lora_trainer_v405.py", "train"], timeout=21600)
    run([sys.executable, "bin/lh_lora_trainer_v405.py", "fuse"], timeout=1200)
    run([sys.executable, "bin/lh_lora_trainer_v405.py", "export"], timeout=2400)

    gguf_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v405" / "gguf_v405"
    modelfile = gguf_dir / "Modelfile.v405"
    run(["ollama", "create", "longhun-v4.0.5", "-f", str(modelfile)], timeout=600)

    run([sys.executable, "bin/lh_validate_v405.py"], timeout=900)

    print("\n" + "=" * 60)
    print("✅ v4.0.5 流水线完成")
    print(f"📊 验证报告: {REPORT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
