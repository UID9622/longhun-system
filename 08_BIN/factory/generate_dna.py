#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-FACTORY-DNA-UID9622
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · DNA 生成器 v1.0
用途: 全自动工厂各流水线统一生成 DNA 追溯码
安全: 使用 SHA-256（系统禁 MD5/SHA-1/DES）
"""

import hashlib
import time
from datetime import datetime

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "FACTORY") -> str:
    """生成 DNA 追溯码: #龍芯⚡️YYYY-MM-DD-SUFFIX-HASH8-UID"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(
        f"{suffix}{timestamp}{time.time()}{UID}".encode()
    ).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{rand}-{UID}"
