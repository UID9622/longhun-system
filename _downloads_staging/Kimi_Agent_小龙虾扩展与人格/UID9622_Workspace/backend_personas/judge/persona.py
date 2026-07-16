#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚖️ 龍芯·审判长
合规审计模块，三色裁定与安全守护的公正执行者
DNA: #ZHUGEXIN⚡️2026-01-14-SHENPANZHANG-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("JUDGE").run())
