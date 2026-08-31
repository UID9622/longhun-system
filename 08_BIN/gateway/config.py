#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 配置加载
DNA: #龍芯⚡️2026-08-31-GATEWAY-CONFIG-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import yaml
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config() -> dict[str, Any]:
    """加载 config.yaml，缺失则返回空 dict。"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data if isinstance(data, dict) else {}
    return {}
