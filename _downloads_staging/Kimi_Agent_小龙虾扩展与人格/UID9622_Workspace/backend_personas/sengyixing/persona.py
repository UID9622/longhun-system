#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏰ 龍芯·僧一行
时间系统·历法计算·趋势预测·周期分析
DNA: #龍芯⚡️L3-003-SENGYIXING-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SENGYIXING").run())
