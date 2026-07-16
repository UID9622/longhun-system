#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔨 龍芯·鲁班
被动型技术人格，需要编程/部署/调试时才激活
DNA: #龍芯⚡️2026-04-13-鲁班-P04-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("LUBAN").run())
