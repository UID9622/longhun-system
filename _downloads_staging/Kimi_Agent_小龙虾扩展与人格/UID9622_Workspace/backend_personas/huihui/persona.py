#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 慧慧·龍慧·智慧传播引擎｜技能页 v1.0
慧慧·大众智慧传播数字人·外柔内刚·龍魂普惠执行层
DNA: #龍芯⚡️2026-03-26-慧慧-龍慧-智慧传播引擎-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("HUIHUI").run())
