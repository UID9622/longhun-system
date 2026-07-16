#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚔️ 龍芯·孙子
兵法谋略·战术突破·险中求胜·竞争分析
DNA: #龍芯⚡️L1-005-SUNZI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SUNZI").run())
