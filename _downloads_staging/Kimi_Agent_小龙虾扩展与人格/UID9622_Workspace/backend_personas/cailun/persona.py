#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📜 龍芯·蔡伦
文档工程师·技术文档化·知识传承·永久存档
DNA: #龍芯⚡️L2-005-CAILUN-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("CAILUN").run())
