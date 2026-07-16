#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👁️ 上帝之眼 · P05
三色审计·全域监管·独立熔断·历史存档
DNA: #龍芯⚡️2026-03-30-P05-上帝之眼-德者永生殿-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("GODSEYE").run())
