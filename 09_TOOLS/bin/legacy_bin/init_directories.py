#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ENGINE-INIT_DIRECTORIES-v1.0
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
