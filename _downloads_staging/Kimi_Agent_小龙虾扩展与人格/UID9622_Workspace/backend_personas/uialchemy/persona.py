#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 龍芯·界面炼金
专注界面设计和视觉体验
DNA: #龍芯⚡️2026-04-13-界面炼金-P09-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("UIALCHEMY").run())
