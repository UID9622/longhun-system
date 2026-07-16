#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 龍芯·影匠
视频版权防护模块，每帧画面都有追溯根源
DNA: #龍芯⚡️2026-01-14-YINGJIANG-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("VIDEOMASTER").run())
