# -*- coding: utf-8 -*-
"""
CNSH v2.1 → Objective-C 编译器
DNA: #龍芯⚡️2026-07-06-CNSH-COMPILER-OBJC-v2.1

说明：CNSH → Objective-C 编译器后端（🟡 待实现）。
      生成使用 Foundation 框架的 Objective-C 代码。
      支持消息传递、Category、Protocol、Block、ARC 等 ObjC 特性。
      Apple Developer: fireroot.lad@outlook.com
"""
from typing import List, Optional, Set

from . import ast_nodes as ast
from .errors import CNSHRuntimeError


class ObjcCompiler:
    """CNSH → Objective-C 转译器"""

    INDENT = "    "

    def __init__(self):
        self.indent_level = 0
        self.module_stack: List[str] = []
        self.module_members: Set[str] = set()

    def compile(self, program: ast.Program) -> str:
        raise NotImplementedError(
            "CNSH → Objective-C 编译器后端待实现。\n"
            "目标: clang + Foundation，支持消息传递/Category/Protocol/Block/ARC。\n"
            "Apple Developer: fireroot.lad@outlook.com\n"
            "预计交付: v3.0 (2026-Q3)"
        )
