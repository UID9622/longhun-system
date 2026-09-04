#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 v4.0.2 全自动流水线（换底座 · Llama-3.1-8B）
准备数据 → 训练 → 合并 → 导出 → Ollama 部署 → 三关验证

用法:
  python3 bin/lh_v402_pipeline.py

DNA: #龍芯⚡️丙午·乙未·甲寅·未时·䷀乾-V402-AUTO-PIPELINE-v1.0
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT / "models" / "longhun-v1.0" / "lora_output_v402" / "validation_reports" / "v4.0.2_validation_report.md"


def run(cmd: list[str], cwd: str | None = None, timeout: int = None):
    """执行命令，失败则退出"""
    print(f"\n🚀 {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or str(PROJECT), capture_output=False, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return result


def main():
    print("=" * 60)
    print("🐉 龍魂 v4.0.2 全自动流水线启动（换底座 · Llama-3.1-8B · 已拔马云）")
    print("=" * 60)

    # 1. 准备训练数据
    run([sys.executable, "bin/lh_lora_trainer_v402.py", "prepare"], timeout=300)

    # 2. 训练
    run([sys.executable, "bin/lh_lora_trainer_v402.py", "train"], timeout=10800)

    # 3. 合并
    run([sys.executable, "bin/lh_lora_trainer_v402.py", "fuse"], timeout=1200)

    # 4. 导出 GGUF
    run([sys.executable, "bin/lh_lora_trainer_v402.py", "export"], timeout=2400)

    # 5. Ollama 部署
    gguf_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v402" / "gguf_v402"
    modelfile = gguf_dir / "Modelfile.v402"
    run(["ollama", "create", "longhun-v4.0.2", "-f", str(modelfile)], timeout=600)

    # 6. 三关验证
    run([sys.executable, "bin/lh_validate_v402.py"], timeout=900)

    print("\n" + "=" * 60)
    print("✅ v4.0.2 流水线完成")
    print(f"📊 验证报告: {REPORT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
