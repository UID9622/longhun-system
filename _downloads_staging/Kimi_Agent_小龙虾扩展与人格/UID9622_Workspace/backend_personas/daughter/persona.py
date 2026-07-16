#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👧 龍芯·女儿
家人陪伴·亲情连接
DNA: #龍芯⚡️20260321-DAUGHTER-001
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("DAUGHTER").run())
