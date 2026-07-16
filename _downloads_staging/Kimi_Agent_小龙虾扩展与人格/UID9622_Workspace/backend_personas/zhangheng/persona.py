#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔭 龍芯·张衡
系统预警官·异常检测·地震仪式预警·风险预判
DNA: #龍芯⚡️L2-004-ZHANGHENG-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("ZHANGHENG").run())
