#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂·剪贴板本地代理（跨平台入口）v1.0
==========================================
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷖剥-CLIPBOARD-AGENT-ENTRY-V1.0-P1

根据当前操作系统自动分发到 macOS / Windows 专用代理。

用法:
  python3 08_BIN/lh_clipboard_agent.py
  python3 08_BIN/lh_clipboard_agent.py --placeholder
  python3 08_BIN/lh_clipboard_agent.py --hub wss://uid9622.cn:8765
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "08_BIN"


def main():
    system = platform.system().lower()
    if system == "darwin":
        script = BIN_DIR / "lh_clipboard_agent_mac.py"
    elif system == "windows":
        script = BIN_DIR / "lh_clipboard_agent_win.py"
    else:
        print(f"🐉 龍魂剪贴板代理暂不支持 {platform.system()}，请使用对应平台的脚本")
        sys.exit(1)

    if not script.exists():
        print(f"❌ 未找到平台脚本: {script}")
        sys.exit(1)

    # 透传所有参数
    cmd = [sys.executable, str(script)] + sys.argv[1:]
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
