#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 同步官·数据管理员｜MCP专属
三才流场MCP引擎·Notion健康探测·同步失败背压队列管理·自适应频率探测
DNA: #龍芯⚡️2026-03-30-同步官MCP-入殿-v1.0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.persona_engine import PersonaEngine

if __name__ == "__main__":
    sys.exit(PersonaEngine("SYNC").run())
