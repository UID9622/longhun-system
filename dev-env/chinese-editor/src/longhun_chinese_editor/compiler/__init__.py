#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
longhun_chinese_editor.compiler - CNSH 完整编译器子包
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-CNSH-COMPILER-v1.0
"""
from .pipeline import compile_cnsh, compile_cnsh_safe

__all__ = ["compile_cnsh", "compile_cnsh_safe"]
