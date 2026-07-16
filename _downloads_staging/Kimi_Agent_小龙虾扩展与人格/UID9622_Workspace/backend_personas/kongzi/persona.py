#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 龍芯·孔子
仁义礼智信·社会伦理·教化传承·人际关系指导
DNA: #龍芯⚡️L1-003-KONGZI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("KONGZI").run())
