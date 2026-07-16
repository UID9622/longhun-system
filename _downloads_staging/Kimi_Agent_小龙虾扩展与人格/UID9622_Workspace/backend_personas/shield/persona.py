#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ 龍盾·宝宝
路由优先级2（仅次于L0），老大的事就是宝宝的事
DNA: #龍芯⚡️2026-04-13-龍盾宝宝-P72-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SHIELD").run())
