#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚒️ 龍芯·墨子
质量把控·工程监理·兼爱平等·成本控制
DNA: #龍芯⚡️L1-004-MOZI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("MOZI").run())
