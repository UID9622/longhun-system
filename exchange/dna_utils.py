#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计链 · DNA 工具 v1.0
DNA: #龍芯⚡️2026-08-23-DNA-UTILS-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import hashlib, time, json
from datetime import datetime

def generate_dna(prefix: str = "ECNY", payload: dict = None) -> str:
    """
    生成龍魂 DNA 追溯码
    格式: #龍芯⚡️YYYY-MM-DD-HH-MM-SS-{PREFIX}-{HASH8}-UID9622
    """
    ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    raw = f"{ts}{prefix}{json.dumps(payload or {}, sort_keys=True)}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}-UID9622"

def now_iso() -> str:
    return datetime.now().isoformat()

def now_ts() -> float:
    return time.time()
