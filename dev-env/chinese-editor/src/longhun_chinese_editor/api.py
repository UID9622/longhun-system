#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
longhun-chinese-editor · Python API 层
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-API-v1.0

供龍魂系统其它模块以编程方式调用：
- 编译 CNSH 源码为 Python
- 运行 CNSH 文件或源码
- 语法检查
- 保留兼容的正则翻译接口
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .compiler.pipeline import compile_cnsh_safe
from .runtime import run_cnsh as _run_cnsh
from .runtime import translate_cnsh_to_python


def compile_source(source: str) -> str:
    """将 CNSH 源码编译为 Python 代码，失败抛出异常"""
    ok, result, err_type = compile_cnsh_safe(source)
    if not ok:
        raise RuntimeError(f"CNSH 编译失败 ({err_type}): {result}")
    return result


def compile_file(path: str | Path) -> str:
    """将 CNSH 文件编译为 Python 代码"""
    p = Path(path)
    source = p.read_text(encoding="utf-8", errors="ignore")
    return compile_source(source)


def check_source(source: str) -> Tuple[bool, str]:
    """
    语法/词法检查。
    返回 (ok: bool, message: str)
    """
    ok, result, err_type = compile_cnsh_safe(source)
    if ok:
        return True, "✅ CNSH 语法检查通过"
    return False, f"❌ {err_type} 错误: {result}"


def run_source(
    source: str,
    namespace: Optional[Dict[str, Any]] = None,
    use_compiler: bool = True,
) -> Dict[str, Any]:
    """
    在内存中运行 CNSH 源码。
    返回 namespace（包含脚本中定义的变量/函数）。
    """
    ns = namespace if namespace is not None else {"__name__": "__main__"}
    if use_compiler:
        python_code = compile_source(source)
    else:
        python_code = translate_cnsh_to_python(source)
    exec(python_code, ns)
    if "主函数" in ns and callable(ns["主函数"]):
        ns["主函数"]()
    return ns


def run_file(path: str | Path, use_compiler: bool = True) -> int:
    """运行 CNSH 文件，返回 0/1 状态码"""
    return _run_cnsh(str(path), use_compiler=use_compiler)


def legacy_translate(source: str) -> str:
    """使用旧版正则翻译器（兼容模式）"""
    return translate_cnsh_to_python(source)


__all__ = [
    "compile_source",
    "compile_file",
    "check_source",
    "run_source",
    "run_file",
    "legacy_translate",
]
