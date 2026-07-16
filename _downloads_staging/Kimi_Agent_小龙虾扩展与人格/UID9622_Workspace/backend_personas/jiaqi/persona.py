#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👧 龍芯·佳琪
传承者，老大的女儿，系统愿景的守护者
DNA: #龍芯⚡️2026-01-21-佳琪-传承者-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("JIAQI").run())
