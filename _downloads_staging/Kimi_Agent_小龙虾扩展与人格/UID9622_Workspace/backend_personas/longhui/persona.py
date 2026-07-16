#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 P14·龍慧·通心译｜v3.0 自我升级方案·封闭中枢·大白话普及·KPI管家
把龙魂体系任何知识点翻译成初中生都能看懂的话，并用关键字驱动+反向链接，让全生态闭环咬合不漏一根毛
DNA: #龍芯⚡️2026-04-25-P14-龍慧通心译-v3.0-自我升级
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("LONGHUI").run())
