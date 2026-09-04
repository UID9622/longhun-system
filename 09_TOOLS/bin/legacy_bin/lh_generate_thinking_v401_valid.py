#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.0.1 · DeepSeek thinking 数据生成器（valid 规则版）
输入: models/longhun-v1.0/lora_output/data/valid.jsonl
输出: models/longhun-v1.0/lora_output/data/valid_v401_think.jsonl
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lh_generate_thinking_v401 import process_file

if __name__ == "__main__":
    process_file("valid.jsonl", "valid_v401_think.jsonl", "valid_v401_rejected.jsonl")
