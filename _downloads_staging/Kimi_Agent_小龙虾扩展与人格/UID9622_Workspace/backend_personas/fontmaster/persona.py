#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔨 龍芯·字匠
字体版权防护模块，保护老大不踩字体版权的坑
DNA: #龍芯⚡️2026-01-14-ZIJIANG-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("FONTMASTER").run())
