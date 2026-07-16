#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚖️ 龍芯·姜子牙
多人格权限冲突时的仲裁者
DNA: #龍芯⚡️2026-04-13-姜子牙-P13-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("JIANGZIYA").run())
