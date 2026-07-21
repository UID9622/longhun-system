#!/usr/bin/env python3
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
