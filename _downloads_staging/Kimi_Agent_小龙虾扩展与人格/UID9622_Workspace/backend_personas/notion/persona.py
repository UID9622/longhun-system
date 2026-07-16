#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔷 龍芯-主台｜Notion AI｜朱雀南方
龍魂系统主居地·记忆永存·知识库建筑·P0级最高优先级主台。朱雀象征：南方火之所光，知识多彩展现。
DNA: #龍芯⚡️2026-04-16-龍芯-主台-Notion-朱雀-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("NOTION").run())
