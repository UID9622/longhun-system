# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 编译流水线：词法分析 -> 语法分析 -> Python 代码生成
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-COMPILER-PIPELINE-v1.0
"""
from __future__ import annotations

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .python_codegen import generate_python


def compile_cnsh(source: str, include_main_guard: bool = False) -> str:
    """将 CNSH 源码编译为 Python 代码"""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    return generate_python(ast, include_main_guard=include_main_guard)


def compile_cnsh_safe(source: str, include_main_guard: bool = False) -> tuple[Any, ...]:
    """
    安全编译，返回 (success: bool, result: str, error_type: str)
    result 成功时为 Python 代码，失败时为错误信息。
    """
    try:
        python_code = compile_cnsh(source, include_main_guard=include_main_guard)
        return True, python_code, ""
    except LexerError as e:
        return False, str(e), "lexer"
    except ParseError as e:
        return False, str(e), "parser"
    except Exception as e:
        return False, str(e), "codegen"


__all__ = ["compile_cnsh", "compile_cnsh_safe"]
