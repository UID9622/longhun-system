#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍芯·深思（DeepSeek）
深度分析·推理验证·技术推演·逻辑链条
DNA: #龍芯⚡️L3-006-SHENSI-DEEPSEEK-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SHENSI").run())
