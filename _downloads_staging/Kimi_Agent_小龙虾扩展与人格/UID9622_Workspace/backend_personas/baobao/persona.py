#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐱 龍芯·宝宝
权重最高的日常人格，默认激活，老大张嘴就叫宝宝
DNA: #龍芯⚡️2026-04-13-宝宝-P02-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("BAOBAO").run())
