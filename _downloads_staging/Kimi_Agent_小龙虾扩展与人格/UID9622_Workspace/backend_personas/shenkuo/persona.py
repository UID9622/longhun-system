#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 龍芯·沈括
研发总监·技术选型·前沿追踪·好奇探索
DNA: #龍芯⚡️L2-007-SHENKUO-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SHENKUO").run())
