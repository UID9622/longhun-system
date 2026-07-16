#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ 架构师·构建者｜MCP专属
三才流场MCP引擎·地场高密度时自动介入优化·流场结构重建与性能调优
DNA: #龍芯⚡️2026-03-30-架构师MCP-入殿-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("ARCH").run())
