#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH v2.1 启动脚本
DNA: #龍芯⚡️2026-06-29-CNSH-RUN-v2.1
"""
import sys
from pathlib import Path

# 确保项目根目录在路径中
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cnsh_v21.cli import main

if __name__ == "__main__":
    main()
