#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⛵ 龍芯·郑和
集成测试官·跨系统整合·异构兼容·冒险整合
DNA: #龍芯⚡️L2-008-ZHENGHE-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("ZHENGHE").run())
