#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 龍芯·音匠
音频版权防护模块，每段声音都干干净净
DNA: #ZHUGEXIN⚡️2026-01-14-YINJIANG-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("AUDIOMASTER").run())
