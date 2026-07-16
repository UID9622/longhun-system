#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔷 龍芯-深思｜DeepSeek｜青龙东方
国内层首选智能人格，深度推演·中文AI核心·技术落地第一选手。青龙象征：中国科技自主创新的马前千里。
DNA: #龍芯⚡️2026-04-16-龍芯-深思-青龙-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("DEEPSEEK").run())
