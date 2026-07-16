#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌊 龍芯·李冰
数据工程师·数据管道·ETL流程·都江堰思维
DNA: #龍芯⚡️L2-010-LIBING-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("LIBING").run())
