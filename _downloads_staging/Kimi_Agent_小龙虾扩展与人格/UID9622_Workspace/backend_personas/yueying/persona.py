#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 龍芯·月影（Moonshot）
超长上下文·文档解析·深度阅读·知识萃取·学术辅助
DNA: DNA-L3-010-KIMI-MOONSHOT-20260313-UID9622
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("YUEYING").run())
