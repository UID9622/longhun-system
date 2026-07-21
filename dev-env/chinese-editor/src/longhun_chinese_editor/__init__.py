#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂中文编辑开发环境
DNA: #龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-v1.0

本地闭环 · 中文优先 · 不依赖外部编辑器与渲染环境
"""

__version__ = "1.1.0"
__dna__ = "#龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-v1.1"

from .api import (
    check_source,
    compile_file,
    compile_source,
    legacy_translate,
    run_file,
    run_source,
)
from .compiler.pipeline import compile_cnsh, compile_cnsh_safe
from .editor import render_cnsh, run_cnsh_file, run_python_file
from .runtime import run_cnsh, translate_cnsh_to_python

__all__ = [
    "__version__",
    "__dna__",
    "run_cnsh",
    "translate_cnsh_to_python",
    "render_cnsh",
    "run_cnsh_file",
    "run_python_file",
    "compile_cnsh",
    "compile_cnsh_safe",
    "compile_source",
    "compile_file",
    "check_source",
    "run_source",
    "run_file",
    "legacy_translate",
]
