#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷯井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# -*- coding: utf-8 -*-
"""#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-SYNC-SECOND-BRAIN-CLI-v1.0
Obsidian → 龍魂第二大脑 同步命令行入口
"""
import sys
import json
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from second_brain.sync import SecondBrainSync


def main():
    parser = argparse.ArgumentParser(description="同步 Obsidian vault 到龍魂第二大脑")
    parser.add_argument("--no-embed", action="store_true", help="跳过向量嵌入，仅构建 SQLite 与图谱")
    args = parser.parse_args()

    syncer = SecondBrainSync(skip_embeddings=args.no_embed)
    result = syncer.run()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
