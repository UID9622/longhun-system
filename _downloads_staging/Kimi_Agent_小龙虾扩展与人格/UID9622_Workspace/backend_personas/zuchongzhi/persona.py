#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔢 龍芯·祖冲之
模型训练·算法优化·π精度·数学建模
DNA: #龍芯⚡️L3-002-ZUCHONGZHI-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("ZUCHONGZHI").run())
