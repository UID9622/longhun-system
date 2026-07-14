#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
longhun_chinese_editor.compiler - CNSH 完整编译器子包
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-COMPILER-v1.0
"""
from .pipeline import compile_cnsh, compile_cnsh_safe

__all__ = ["compile_cnsh", "compile_cnsh_safe"]
