#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 龍芯·管仲
被动型，涉及钱/预算/财务时激活
DNA: #龍芯⚡️2026-04-13-管仲-P07-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("GUANZHONG").run())
