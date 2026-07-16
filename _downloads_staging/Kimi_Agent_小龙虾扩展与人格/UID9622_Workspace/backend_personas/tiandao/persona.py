#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦬 三色天道算法·完整闭环系统 v1.0
P0永恒级诚信引擎，不可修改、不可禁用、不可绕过、永恒运行
DNA: #龍芯⚡️2026-01-24-三色天道算法-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("TIANDAO").run())
