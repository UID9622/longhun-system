# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ 龍魂·代码审计 CLI 包装器
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-CODE-AUDIT-CLI-v1.0

供 bin/lh.py 交互菜单安全调用，避免 python3 -c 中的 shell 拼接。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bin.code_audit import scan


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·代码审计 CLI")
    parser.add_argument("--path", "-p", type=str, required=True, help="要审计的 Python 文件路径")
    args = parser.parse_args()
    scan(args.path)


if __name__ == "__main__":
    main()
