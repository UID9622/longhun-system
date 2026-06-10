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
