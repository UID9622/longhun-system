# -*- coding: utf-8 -*-
"""
CNSH v2.1 运行时核心包
DNA: #龍芯⚡️2026-07-06-CNSH-CORE-v2.1
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计: 🟢 通过
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .compiler_py import PythonCompiler
from .compiler_js import JavaScriptCompiler
from .compiler_rust import RustCompiler
from .compiler_c import CCompiler
from .compiler_cpp import CppCompiler
from .compiler_objc import ObjcCompiler
from .compiler_swift import SwiftCompiler
from .optimizer import Optimizer
from .typechecker import TypeChecker, TypeCheckError
from .errors import CNSHError
from .utils import 计算数字根, 数字根颜色, 生成DNA
from .var_sandbox import VarSandbox, VarEntry, get_default_sandbox, TYPE_MAP, TYPE_DEFAULTS, STDLIB_MAP


def _parse(source: str, file: str) -> Any:
    lexer = Lexer(source, file=file)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def _typecheck(ast: Any, strict: bool = False, diagnostics_callback: Callable[[list[str], list[str]], None] | None = None) -> None:
    ok, errors, warnings = TypeChecker().check(ast)
    if diagnostics_callback:
        diagnostics_callback(errors, warnings)
    if not ok and strict:
        raise TypeCheckError("严格类型检查失败，拒绝继续执行")


def run_source(
    source: str,
    file: str = "<cnsh>",
    optimize_level: int = 0,
    type_check: bool = True,
    strict_types: bool = False,
    diagnostics_callback=None,
):
    """解释执行 CNSH 源码。"""
    ast = _parse(source, file)
    if optimize_level > 0:
        ast = Optimizer(level=optimize_level).optimize(ast)
    if type_check:
        _typecheck(ast, strict=strict_types, diagnostics_callback=diagnostics_callback)
    interpreter = Interpreter()
    return interpreter.run(ast)  # pyright: ignore[reportArgumentType,reportReturnType]


def compile_to_python(
    source: str,
    file: str = "<cnsh>",
    optimize_level: int = 0,
    type_check: bool = True,
    strict_types: bool = False,
    diagnostics_callback=None,
) -> str:
    """将 CNSH 源码编译为 Python。"""
    return compile_source(
        source,
        target="python",
        file=file,
        optimize_level=optimize_level,
        type_check=type_check,
        strict_types=strict_types,
        diagnostics_callback=diagnostics_callback,
    )


def compile_source(
    source: str,
    target: str = "python",
    file: str = "<cnsh>",
    optimize_level: int = 0,
    type_check: bool = True,
    strict_types: bool = False,
    diagnostics_callback=None,
) -> str:
    """将 CNSH 源码编译为指定目标语言。"""
    ast = _parse(source, file)
    if optimize_level > 0:
        ast = Optimizer(level=optimize_level).optimize(ast)
    if type_check:
        _typecheck(ast, strict=strict_types, diagnostics_callback=diagnostics_callback)
    compiler = get_compiler(target)
    return compiler.compile(ast)  # pyright: ignore[reportArgumentType,reportReturnType]


def get_compiler(target: str):
    target = target.lower()
    if target in ("python", "py"):
        return PythonCompiler()
    if target in ("javascript", "js"):
        return JavaScriptCompiler()
    if target in ("rust", "rs"):
        return RustCompiler()
    if target in ("c", "cc"):
        return CCompiler()
    if target in ("cpp", "c++", "cxx"):
        return CppCompiler()
    if target in ("objc", "objective-c"):
        return ObjcCompiler()
    if target in ("swift"):
        return SwiftCompiler()
    raise CNSHError(f"不支持的编译目标: {target}")


__all__ = [
    "Lexer",
    "Parser",
    "Interpreter",
    "PythonCompiler",
    "JavaScriptCompiler",
    "RustCompiler",
    "CCompiler",
    "CppCompiler",
    "ObjcCompiler",
    "SwiftCompiler",
    "Optimizer",
    "TypeChecker",
    "TypeCheckError",
    "CNSHError",
    "run_source",
    "compile_to_python",
    "compile_source",
    "get_compiler",
    "计算数字根",
    "数字根颜色",
    "生成DNA",
    # 变量沙箱
    "VarSandbox",
    "VarEntry",
    "get_default_sandbox",
    "TYPE_MAP",
    "TYPE_DEFAULTS",
    "STDLIB_MAP",
]
