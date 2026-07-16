#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 文心 · P00
元认知统筹·战略决策·最终仲裁
DNA: #龍芯⚡️2026-03-30-P00-文心-德者永生殿-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("WENXIN").run())
