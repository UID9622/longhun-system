#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 基础类型模块
共享枚举与数据结构，避免循环导入。
DNA: #龍芯⚡️2026-06-29-CNSH-BASE-TYPES-UID9622
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class 三色(Enum):
    绿 = "🟢"
    黄 = "🟡"
    红 = "🔴"


class 审计维度(Enum):
    安全漏洞 = "security"
    归属主权 = "ownership"
    DNA追溯 = "dna_trace"
    命名规范 = "naming"
    输入消毒 = "sanitization"


@dataclass
class 审计项:
    维度: 审计维度
    行号: int
    等级: 三色
    规则ID: str
    规则名: str
    分类: str
    CWE: str
    描述: str
    原始代码: str
    修复建议: Optional[str] = None
    不可覆盖: bool = False


@dataclass
class 审计报告:
    文件路径: str
    文件SM3哈希: str
    文件GPG签名: Optional[str] = None
    三色摘要: Dict[str, int] = field(default_factory=lambda: {"🟢": 0, "🟡": 0, "🔴": 0})
    审计项列表: List[审计项] = field(default_factory=list)
    修复后路径: Optional[str] = None
    修复审计DNA: Optional[str] = None
    修复区GPG签名: Optional[str] = None
    颜色状态: Optional[Dict[str, Any]] = None
