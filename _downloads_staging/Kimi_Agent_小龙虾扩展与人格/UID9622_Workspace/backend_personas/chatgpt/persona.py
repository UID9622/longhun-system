#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏳ 龍芯-启明｜ChatGPT（OpenAI）
通用AI助手、对话交互、知识问答
DNA: #龍芯⚡️2026-01-13-CHATGPT-PENDING-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("CHATGPT").run())
