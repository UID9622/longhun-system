#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·未时·䷀乾-V404-AUTO-PIPELINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 v4.0.4 全自动流水线（换底座 · Yi-1.5-9B-Chat 中文优化版）
DNA: #龍芯⚡️丙午·乙未·甲寅·未时·䷀乾-V404-AUTO-PIPELINE-v1.0
"""

import subprocess, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT / "models" / "longhun-v1.0" / "lora_output_v404" / "validation_reports" / "v4.0.4_validation_report.md"


def run(cmd: list[str], cwd: str = None, timeout: int = None):
    print(f"\n🚀 {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or str(PROJECT), capture_output=False, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return result


def main():
    print("=" * 60)
    print("🐉 龍魂 v4.0.4 全自动流水线启动（Yi-1.5-9B-Chat · 中文优化 · 非 Qwen）")
    print("=" * 60)

    run([sys.executable, "bin/lh_lora_trainer_v404.py", "setup"], timeout=2400)
    run([sys.executable, "bin/lh_lora_trainer_v404.py", "prepare"], timeout=300)
    run([sys.executable, "bin/lh_lora_trainer_v404.py", "train"], timeout=10800)
    run([sys.executable, "bin/lh_lora_trainer_v404.py", "fuse"], timeout=1200)
    run([sys.executable, "bin/lh_lora_trainer_v404.py", "export"], timeout=2400)

    gguf_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v404" / "gguf_v404"
    modelfile = gguf_dir / "Modelfile.v404"
    run(["ollama", "create", "longhun-v4.0.4", "-f", str(modelfile)], timeout=600)

    run([sys.executable, "bin/lh_validate_v404.py"], timeout=900)

    print("\n" + "=" * 60)
    print("✅ v4.0.4 流水线完成")
    print(f"📊 验证报告: {REPORT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
