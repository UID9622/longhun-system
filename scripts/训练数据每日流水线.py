#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 训练数据每日流水线
一键运行：收集 → 标注 → 质检 → 报告。
DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-DAILY-PIPELINE-v1.0
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SCRIPTS = HOME / "longhun-system" / "scripts"


def _运行(脚本名: str) -> int:
    路径 = SCRIPTS / 脚本名
    print(f"\n▶️ 执行: {脚本名}")
    result = subprocess.run([sys.executable, str(路径)])
    return result.returncode


def main():
    print("🐉 启动龍魂训练数据每日流水线")
    print(f"DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-DAILY-PIPELINE-v1.0")
    print(f"时间: {datetime.now(timezone.utc).isoformat()}\n")

    steps = [
        "收集反馈.py",
        "标注数据.py",
        "质量检查.py",
        "生成数据报告.py",
    ]

    失败 = 0
    for step in steps:
        rc = _运行(step)
        if rc != 0:
            失败 += 1
            print(f"🔴 {step} 失败，返回码 {rc}")

    if 失败 == 0:
        print("\n🟢 流水线全部完成")
    else:
        print(f"\n🟡 流水线完成，{失败} 个步骤失败")

    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    报告 = HOME / "longhun-system" / "data" / "training" / "reports" / f"training_report_{日期}.md"
    if 报告.exists():
        print(f"   查看报告: {报告}")


if __name__ == "__main__":
    main()
