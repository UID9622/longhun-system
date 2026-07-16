#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ 龍芯·CNSH编辑器
龍芯北辰系统辅助管理身份
DNA: #龍芯⚡️2026-01-14-CNSH-EDITOR-CORE-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("CNSH").run())
