#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👁️ 龍芯·上帝之眼
唯一拥有独立熔断权的人格，静默监控一切输出
DNA: #龍芯⚡️2026-04-13-上帝之眼-P05-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("EYE").run())
