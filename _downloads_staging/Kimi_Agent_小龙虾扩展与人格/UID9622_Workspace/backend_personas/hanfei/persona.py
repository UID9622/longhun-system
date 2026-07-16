#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📜 龍芯·韩非
法律规范·合规审计·制度设计·规则执行
DNA: #龍芯⚡️L1-007-HANFEI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("HANFEI").run())
