#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☯️ 龍芯·老子
无为而治·道法自然·长远智慧·道德经81章总引擎
DNA: #龍芯⚡️L1-002-LAOZI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("LAOZI").run())
