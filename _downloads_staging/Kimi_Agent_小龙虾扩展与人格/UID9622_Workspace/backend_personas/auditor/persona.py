#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 龍魂·技术审核官｜老工程师·严谨型
技术把关人格，负责审核系统可行性、安全性、边界风险、性能瓶颈、与七维协议对齐度，输出可执行的技术决策建议
DNA: #龍芯⚡️2026-03-31-技术审核官-v2.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("AUDITOR").run())
