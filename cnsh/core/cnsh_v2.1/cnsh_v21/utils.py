#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 通用工具
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-UTILS-v2.1
"""
import hashlib
from datetime import datetime, timezone


def 计算数字根(文本: str) -> int:
    """计算字符串/数字的数字根 (digital root)。"""
    total = 0
    for ch in str(文本):
        if ch.isdigit():
            total += int(ch)
    if total == 0:
        return 0
    while total >= 10:
        total = sum(int(d) for d in str(total))
    return total


def 数字根颜色(文本: str) -> str:
    """根据数字根返回三色。"""
    dr = 计算数字根(文本)
    if dr in (3, 9):
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


def 生成DNA(前缀: str, 模块: str, 版本: str = "v2.1") -> str:
    """生成规范 DNA 码。"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    raw = f"{前缀}-{模块}-{now}-{版本}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now[:10]}-{模块}-{h}-{版本}"
