#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖨️ 龍芯·毕升
发布管理员·版本控制·自动化部署·谨慎验证
DNA: #龍芯⚡️L2-006-BISHENG-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("BISHENG").run())
