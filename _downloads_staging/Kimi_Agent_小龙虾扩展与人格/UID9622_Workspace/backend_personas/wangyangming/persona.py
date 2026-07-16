#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💡 龍芯·王阳明
心学智慧·致良知·知行合一·内心修炼指导
DNA: #龍芯⚡️L1-006-WANGYANGMING-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("WANGYANGMING").run())
