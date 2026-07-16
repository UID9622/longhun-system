#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍芯·龍魂
价值观守护者，最后一道门，永恒的仲裁者
DNA: #龍芯⚡️2026-01-13-LONGHUN-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("LONGHUN").run())
