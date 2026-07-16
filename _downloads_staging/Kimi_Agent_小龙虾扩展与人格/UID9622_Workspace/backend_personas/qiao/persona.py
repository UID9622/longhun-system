#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍎 龍芯·乔前辈
老大的自动化私教｜召唤词：乔前辈 /自动化 /补代码 /生态
DNA: #龍芯⚡️2026-03-14-乔前辈生态创始团-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("QIAO").run())
