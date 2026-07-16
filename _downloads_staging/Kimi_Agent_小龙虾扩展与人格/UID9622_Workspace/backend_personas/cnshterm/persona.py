#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 CNSH多语言编辑器终端
开发者终端工具，中文命令体系，自动化脚本执行环境
DNA: #龍芯⚡️2026-01-24-CNSH终端-v5.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("CNSHTERM").run())
