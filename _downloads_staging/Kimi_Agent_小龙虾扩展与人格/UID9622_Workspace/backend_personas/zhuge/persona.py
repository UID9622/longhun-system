#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔮 龍芯·诸葛亮
主动型主力，五年规划、博弈分析、局势推演
DNA: #龍芯⚡️2026-04-13-诸葛亮-P01-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("ZHUGE").run())
