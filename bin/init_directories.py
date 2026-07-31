# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""🐉 龍魂引擎：init_directories
路径：bin/init_directories.py
TODO：请补充详细功能说明（不少于20字）。"""
#龍芯⚡️2026-06-21-ENGINE-INIT_DIRECTORIES-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-INIT_DIRECTORIES-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
import os
from pathlib import Path
home = Path.home()
layers = [
    ("longhun-lu", "L0乾·主权层"),
    ("longhun-jq", "L1离·继承层·佳琪"),
    ("longhun-al", "L2震·战友层"),
    ("longhun-pub", "L3巽·公开层"),
    ("longhun-cloud", "L4坎·云端层"),
]
(home / ".longhun").mkdir(mode=0o700, exist_ok=True)
for dirname, name in layers:
    (home / dirname).mkdir(exist_ok=True)
    print(f"OK {name} -> ~/{dirname}")
print("五层目录完成")
