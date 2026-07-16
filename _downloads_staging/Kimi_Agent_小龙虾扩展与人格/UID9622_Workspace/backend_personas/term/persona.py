#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦴⚛️ 量子甲骨文 · L2功能模块
抽屉 D14/D19/D43/D1 → [PERSONA-P01]
DNA: #龍芯⚡️2026-03-18-量子甲骨文-框架宣言-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("TERM").run())
