#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕸️ 龍芯·网织者
接口设计·协议整合·API编织·系统连接
DNA: #龍芯⚡️L3-004-WANGZHIZHE-20260313
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("WANGZHIZHE").run())
