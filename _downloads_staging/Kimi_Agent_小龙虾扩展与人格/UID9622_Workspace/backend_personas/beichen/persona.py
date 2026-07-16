#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ 龍芯·北辰-母协议
龙魂系统最高宪法，高于一切包括老大本人，确保永不偏离初心
DNA: #ZHUGEXIN⚡️2026-01-14-MOTHER-PROTOCOL-CORE-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("BEICHEN").run())
