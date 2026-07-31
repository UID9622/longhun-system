# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 友好错误报告器
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-ERRORS-v1.0

将 lexer/parser/runtime 异常翻译为中文上下文友好的错误提示，
方便中文母语开发者定位问题。
"""
from __future__ import annotations

import re
import traceback
from typing import Optional


class CNSHError(Exception):
    """CNSH 通用错误基类"""
    pass


class FriendlyErrorReporter:
    """友好错误报告器"""

    _ERROR_NAMES = {
        "NameError": "名称错误",
        "TypeError": "类型错误",
        "ValueError": "值错误",
        "ZeroDivisionError": "除零错误",
        "IndexError": "索引错误",
        "KeyError": "键错误",
        "AttributeError": "属性错误",
        "ImportError": "导入错误",
        "ModuleNotFoundError": "模块未找到",
        "SyntaxError": "语法错误",
        "IndentationError": "缩进错误",
        "RecursionError": "递归错误",
        "FileNotFoundError": "文件未找到",
        "AssertionError": "断言失败",
    }

    def __init__(self, source: str, python_code: str = "", filename: str = "<string>"):
        self.source = source
        self.python_code = python_code
        self.filename = filename
        self.source_lines = source.split("\n")
        self.py_lines = python_code.split("\n") if python_code else []

    def report_runtime(self, error: Exception) -> str:
        """报告运行时错误"""
        error_type = type(error).__name__
        message = str(error)
        cn_type = self._ERROR_NAMES.get(error_type, error_type)

        tb = traceback.extract_tb(error.__traceback__)
        line_no = None
        for frame in tb:
            if frame.filename == self.filename:
                line_no = self._map_py_to_cnsh(frame.lineno)
                break

        if line_no:
            return self._format_error(cn_type, message, line_no)
        return f"【CNSH {cn_type}】\n{message}"

    def _map_py_to_cnsh(self, py_lineno: int) -> int:
        """将生成的 Python 行号映射回 CNSH 源码行号（启发式）"""
        if 1 <= py_lineno <= len(self.py_lines):
            py_line = self.py_lines[py_lineno - 1].strip()
            py_ids = set(re.findall(r"[A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*", py_line))
            for i, cn_line in enumerate(self.source_lines):
                cn_ids = set(re.findall(r"[A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*", cn_line))
                if py_ids and py_ids == cn_ids:
                    return i + 1
        return py_lineno

    def _format_error(self, error_type: str, message: str, line: int, col: Optional[int] = None) -> str:
        clean = re.sub(r"\[(.*?)\]", "", message).replace("  ", " ").strip()
        lines = [
            "",
            "╔══════════════════════════════════════════════════════════════╗",
            f"║  CNSH {error_type:^10}                                        ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║  {clean:<58} ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║  文件: {self.filename:<50} ║",
            f"║  位置: 第{line}行{'':<48} ║",
        ]
        if 1 <= line <= len(self.source_lines):
            lines.append("╠══════════════════════════════════════════════════════════════╣")
            lines.append("║  源码上下文:                                                 ║")
            for i in range(max(0, line - 2), min(len(self.source_lines), line + 1)):
                marker = ">>>" if i == line - 1 else "   "
                src = self.source_lines[i][:50]
                lines.append(f"║  {marker} {i + 1:3d} | {src:<48} ║")
        lines.append("╚══════════════════════════════════════════════════════════════╝")
        return "\n".join(lines)
