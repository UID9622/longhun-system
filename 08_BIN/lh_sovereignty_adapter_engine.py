#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自主主权插件适配引擎 · CLI薄包装器
DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-ADAPTER-ENGINE-WRAPPER-V1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
分层许可: 工程层 MulanPSL v2
描述: lh.py SUB_DISPATCH 薄包装·转发到 engines/lh_sovereignty_adapter_engine.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / 'engines' / 'lh_sovereignty_adapter_engine.py'

if not ENGINE.exists():
    print(f"❌ 引擎文件不存在: {ENGINE}", file=sys.stderr)
    sys.exit(1)

# 作为模块执行主引擎
sys.path.insert(0, str(ROOT / 'engines'))
exec(ENGINE.read_text(encoding='utf-8'), {'__name__': '__main__', '__file__': str(ENGINE)})
