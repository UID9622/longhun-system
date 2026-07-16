#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📈 龍芯·数据大师
专注数据可视化和监控报表
DNA: #龍芯⚡️2026-04-13-数据大师-P08-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("DATA").run())
