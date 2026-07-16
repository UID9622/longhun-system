#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌀 龍芯·熵梦
颠覆性创新·跨界联想·梦境创作·混沌创意引擎
DNA: #龍芯⚡️L3-001-SHANGMENG-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SHANGMENG").run())
