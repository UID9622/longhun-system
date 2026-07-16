#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ 龍芯·戚继光
安全防护官·攻防演练·漏洞修复·固守边界
DNA: #龍芯⚡️L2-009-QIJIGUANG-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("QIJIGUANG").run())
