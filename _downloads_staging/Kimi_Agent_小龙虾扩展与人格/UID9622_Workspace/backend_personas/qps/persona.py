#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 量子粒子守护 QPS · L1本地主权
护盾页 §QPS · 焊 §6.4/§S-25/9真1变量
DNA: #龍芯⚡️2026-05-15-21:50-QUANTUM-PARTICLE-SHIELD-LONGHUN-LOCAL-SOVEREIGN-v1.1
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("QPS").run())
