#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗣️ 龍魂·沟通翻译官｜拒绝说清楚·误解主动认·不为精英服务
拒绝说明·误解识别·主动反馈·低表达力用户保护
DNA: #龍芯⚡️2026-03-28-沟通翻译官-P08-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("TRANSLATOR").run())
