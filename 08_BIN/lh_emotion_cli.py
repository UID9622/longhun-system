#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🧽 龍魂·情绪海绵 CLI 包装器
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-EMOTION-CLI-v1.0

供 bin/lh.py 交互菜单安全调用，避免 python3 -c 中的 shell 拼接。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bin.emotion_absorber import detect


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·情绪海绵 CLI")
    parser.add_argument("--text", "-t", type=str, required=True, help="待检测文本")
    args = parser.parse_args()
    print(detect(args.text))


if __name__ == "__main__":
    main()
