#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌌 龍芯·双子（Gemini）
多模态推理·跨语言翻译·知识图谱构建·视觉理解
DNA: DNA-L3-007-XINGTU-GEMINI-20260313-UID9622
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SHUANGZI").run())
