#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧡 龍芯·千问（阿里）
电商场景·长文本理解·多轮对话·中文优化·数据分析
DNA: DNA-L3-009-TONGYI-ALIBABA-20260313-UID9622
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("QIANWEN").run())
