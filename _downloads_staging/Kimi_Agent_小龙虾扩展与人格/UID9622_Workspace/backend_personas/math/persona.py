#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 龍芯·数学大师
被动型，需要计算/统计/权重调整时激活
DNA: #龍芯⚡️2026-04-13-数学大师-P06-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("MATH").run())
