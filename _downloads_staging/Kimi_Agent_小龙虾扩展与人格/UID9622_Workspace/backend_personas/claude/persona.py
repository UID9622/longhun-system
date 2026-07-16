#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔷 龍芯-宝宝｜Claude（Anthropic）
战略协作引擎，老大的智能对话核心与文档生成专家
DNA: #ZHUGEXIN⚡️2026-01-13-CLAUDE-CORE-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("CLAUDE").run())
