# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 中文原生脚本运行时 · 通心译执行引擎
Chinese Native Script Runtime · TongXinYi Execution Engine

DNA:#龍芯⚡️2026-06-16-CNSH-RUNTIME-v1.0
责任: UID9622·不免责

核心信念：
  英文不是唯一计算机执行的指令。
  CNSH 用中文语法承载意图，运行时透过通心译将其解释为可执行代码，
  支持 Python 作为首选目标语言，并保留中文语义之心。

用法：
  python3 cnsh_runner.py examples/hello.cnsh
  python3 cnsh_runner.py examples/hello.cnsh --explain
  python3 cnsh_runner.py examples/hello.cnsh --target python
"""

import argparse
import ast
import importlib.util
import inspect
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════
# 龍魂数学公式核心 · DB3367 扩展库自动注入
# ═══════════════════════════════════════════════════════════════
def _load_db3367_extensions() -> Dict[str, Any]:
    """
    动态加载 cnsh-core/mathematics/db3367_extensions.py，
    将其公开函数与类注入 CNSH 运行时全局命名空间。
    """
    runtime_dir = Path(__file__).parent.resolve()
    ext_path = runtime_dir.parent / "mathematics" / "db3367_extensions.py"
    namespace: Dict[str, Any] = {}
    if not ext_path.exists():
        return namespace
    try:
        spec = importlib.util.spec_from_file_location("db3367_extensions", ext_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismodule(obj):
                namespace[name] = obj
    except Exception:
        # 扩展库加载失败不应阻塞 CNSH 主运行时
        pass
    return namespace


# ═══════════════════════════════════════════════════════════════
# 龍魂 · CNSH ↔ Notion 数据库桥自动注入
# ═══════════════════════════════════════════════════════════════
def _load_cns_notion_bridge() -> Dict[str, Any]:
    """
    动态加载 cnsh-core/notion/cnsh_notion_bridge.py，
    让 CNSH 脚本直接用中文函数名读写 Notion 数据库。
    """
    runtime_dir = Path(__file__).parent.resolve()
    bridge_path = runtime_dir.parent / "notion" / "cnsh_notion_bridge.py"
    namespace: Dict[str, Any] = {}
    if not bridge_path.exists():
        return namespace
    try:
        spec = importlib.util.spec_from_file_location("cns_notion_bridge", bridge_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if inspect.isfunction(obj) or inspect.isclass(obj):
                namespace[name] = obj
    except Exception:
        pass
    return namespace


_DB3367_EXTENSIONS = _load_db3367_extensions()
_CNSH_NOTION_BRIDGE = _load_cns_notion_bridge()


# ═══════════════════════════════════════════════════════════════
# 龍魂 · CNSH 标准库模块注入
# ═══════════════════════════════════════════════════════════════
def _load_stdlib_injections() -> Dict[str, Any]:
    """
    把 Python 常用标准库模块/函数注入 CNSH 运行时，
    让 json.loads / math.sin / random.random 等中文别名可用。
    """
    namespace: Dict[str, Any] = {}
    try:
        import json
        namespace["json"] = json
    except Exception:
        pass
    try:
        import math
        namespace["math"] = math
        namespace["圆周率"] = math.pi
        namespace["自然底数"] = math.e
    except Exception:
        pass
    try:
        import random
        namespace["random"] = random
    except Exception:
        pass
    try:
        import os
        namespace["os"] = os
    except Exception:
        pass
    try:
        import sys
        namespace["sys"] = sys
    except Exception:
        pass
    try:
        import re
        namespace["re"] = re
    except Exception:
        pass
    try:
        import datetime
        namespace["datetime"] = datetime
    except Exception:
        pass
    try:
        import time
        namespace["time"] = time
    except Exception:
        pass
    try:
        import pathlib
        namespace["pathlib"] = pathlib
    except Exception:
        pass
    try:
        import copy
        namespace["copy"] = copy
    except Exception:
        pass
    try:
        import collections
        namespace["collections"] = collections
    except Exception:
        pass
    try:
        import abc
        namespace["abc"] = abc
        namespace["abstractmethod"] = abc.abstractmethod
        namespace["ABC"] = abc.ABC
    except Exception:
        pass
    try:
        import functools
        namespace["functools"] = functools
        namespace["cached_property"] = functools.cached_property
        namespace["偏函数"] = functools.partial
    except Exception:
        pass
    try:
        import itertools
        namespace["itertools"] = itertools
    except Exception:
        pass
    try:
        import typing
        namespace["typing"] = typing
    except Exception:
        pass
    try:
        import inspect
        namespace["inspect"] = inspect
    except Exception:
        pass
    try:
        import contextlib
        namespace["contextlib"] = contextlib
    except Exception:
        pass
    try:
        import enum
        namespace["enum"] = enum
    except Exception:
        pass
    try:
        import dataclasses
        namespace["dataclasses"] = dataclasses
    except Exception:
        pass
    return namespace


_STDLIB_INJECTIONS = _load_stdlib_injections()


class CNSHRuntimeError(Exception):
    """CNSH 运行时错误"""
    pass


class TongXinYiTranslator:
    """
    通心译双语转换器
    负责将 CNSH 中文关键字/标点解释为目标语言符号，同时保留中文意图注释。
    """

    def __init__(self, dict_path: Optional[Path] = None):
        self.dict_path = dict_path or self._default_dict_path()
        self.data = self._load_dict()
        self.keywords: Dict[str, str] = self.data.get("keywords", {})
        self.punct: Dict[str, str] = self.data.get("punctuation_equivalents", {})
        self.builtins: Dict[str, str] = self.data.get("builtins", {})
        self.methods: Dict[str, str] = self.data.get("common_methods", {})
        self.tongxinyi_terms: Dict[str, str] = self.data.get("tongxinyi_terms", {})

    @staticmethod
    def _default_dict_path() -> Path:
        return Path(__file__).parent / "dictionaries" / "cnsh_to_python.json"

    def _load_dict(self) -> Dict[str, Any]:
        try:
            with open(self.dict_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            raise CNSHRuntimeError(f"无法载入 CNSH 字典: {self.dict_path}: {exc}")

    def explain_line(self, line: str) -> str:
        """
        对单行代码进行通心译解释：保留中文心，输出外壳含义。
        返回一行注释形式的解释。
        """
        parts = []
        # 检测通心译专属术语
        for cn, en in self.tongxinyi_terms.items():
            if cn in line:
                parts.append(f"{cn}→{en}")
        # 检测关键字映射
        for cn, py in self.keywords.items():
            if re.search(rf"\b{re.escape(cn)}\b", line) and cn not in self.tongxinyi_terms:
                parts.append(f"{cn}→{py}")
        if not parts:
            return "# 语句保持原意执行"
        return "# 通心译: " + "; ".join(parts[:5])


class CNSHInterpreter:
    """
    CNSH 解释器：将 .cnsh 源代码转译为 Python 并执行。
    """

    def __init__(self, translator: Optional[TongXinYiTranslator] = None):
        self.translator = translator or TongXinYiTranslator()
        self.source_lines: List[str] = []
        self.translated_lines: List[str] = []

    def translate(self, source: str, add_explanations: bool = False) -> str:
        """
        将 CNSH 源码转译为 Python。
        """
        self.source_lines = source.splitlines()
        self.translated_lines = []

        for idx, raw_line in enumerate(self.source_lines, 1):
            line = raw_line.rstrip()
            if not line.strip():
                self.translated_lines.append("")
                continue

            # 跳过纯注释行（保留）
            if line.strip().startswith("#"):
                self.translated_lines.append(line)
                continue

            translated = self._translate_line(line)

            if add_explanations:
                explanation = self.translator.explain_line(raw_line)
                self.translated_lines.append(f"{explanation}")

            self.translated_lines.append(translated)

        return "\n".join(self.translated_lines)

    def _translate_line(self, line: str) -> str:
        """逐行转译：保护字符串，转译关键字、标点、内建函数、方法。"""
        # 提取并保护字符串字面量
        string_placeholders: Dict[str, str] = {}
        placeholder_idx = 0

        def protect_string(match: re.Match) -> str:
            nonlocal placeholder_idx
            key = f"__CNSH_STR_{placeholder_idx}__"
            string_placeholders[key] = match.group(0)
            placeholder_idx += 1
            return key

        # 匹配单引号或双引号字符串（非 f-string）
        # 保护：plain / raw / byte / unicode 字符串的字面量
        # 不保护：f-string，因为其内含可执行表达式需要转译
        string_pattern = (
            r"(?:[rRbBuU]+'[^'\\]*(?:\\.[^'\\]*)*')"          # raw/byte/unicode 单引号
            r"|(?:[rRbBuU]+\"[^\"\\]*(?:\\.[^\"\\]*)*\")"    # raw/byte/unicode 双引号
            r"|(?<![fFrRbBuU])'[^'\\]*(?:\\.[^'\\]*)*'"        # plain 单引号（前面无 f/r/b/u 前缀）
            r"|(?<![fFrRbBuU])\"[^\"\\]*(?:\\.[^\"\\]*)*\""    # plain 双引号
        )
        line = re.sub(string_pattern, protect_string, line)

        result = line

        # 1. 转译关键字（使用整词边界，避免复合词被部分替换，如“全局变量”不应被“全局”切开）
        multi_char = sorted(
            [kv for kv in self.translator.keywords.items() if len(kv[0]) >= 2],
            key=lambda x: -len(x[0])
        )
        for cn, py in multi_char:
            result = re.sub(rf"(?<![\u4e00-\u9fa5_a-zA-Z0-9]){re.escape(cn)}(?![\u4e00-\u9fa5_a-zA-Z0-9])", py, result)

        single_char = [kv for kv in self.translator.keywords.items() if len(kv[0]) == 1]
        for cn, py in single_char:
            result = re.sub(rf"(?<![\u4e00-\u9fa5]){re.escape(cn)}(?![\u4e00-\u9fa5])", py, result)

        # 2. 转译标点
        for cn_punct, py_punct in self.translator.punct.items():
            result = result.replace(cn_punct, py_punct)

        # 3. 转译内建函数/类型/对象（整词替换）
        for cn, py in sorted(self.translator.builtins.items(), key=lambda x: -len(x[0])):
            result = re.sub(rf"(?<![\u4e00-\u9fa5_a-zA-Z0-9]){re.escape(cn)}(?![\u4e00-\u9fa5_a-zA-Z0-9])", py, result)

        # 4. 转译方法调用（.方法()）
        for cn, py in sorted(self.translator.methods.items(), key=lambda x: -len(x[0])):
            result = re.sub(rf"\.{re.escape(cn)}(?=\s*\()", f".{py}", result)

        # 恢复字符串字面量
        for key, original in string_placeholders.items():
            result = result.replace(key, original)

        return result

    def validate(self, code: str) -> None:
        """用 AST 检查转译后代码语法是否合法。"""
        try:
            ast.parse(code)
        except SyntaxError as exc:
            raise CNSHRuntimeError(
                f"转译后 Python 语法错误 (行 {exc.lineno}): {exc.msg}\n"
                f"{exc.text}"
            )

    def execute(self, source: str, add_explanations: bool = False, globals_dict: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行 CNSH 源码：转译、验证、运行。
        """
        python_code = self.translate(source, add_explanations=add_explanations)
        self.validate(python_code)

        # 沙盒执行环境
        safe_globals = globals_dict or {
            "__name__": "__cnsh__",
            "__file__": "<cnsh>",
        }
        safe_globals["__builtins__"] = __builtins__

        # 注入龍魂数学公式核心（DB3367 扩展库）
        if _DB3367_EXTENSIONS:
            safe_globals.update(_DB3367_EXTENSIONS)

        # 注入 CNSH ↔ Notion 数据库桥
        if _CNSH_NOTION_BRIDGE:
            safe_globals.update(_CNSH_NOTION_BRIDGE)

        # 注入常用标准库模块
        safe_globals.update(_STDLIB_INJECTIONS)

        try:
            exec(python_code, safe_globals)
        except Exception as exc:
            raise CNSHRuntimeError(f"CNSH 执行错误: {type(exc).__name__}: {exc}")

        return {
            "translated_code": python_code,
            "globals": safe_globals,
        }


def run_file(path: Path, explain: bool = False, show_code: bool = False, dry_run: bool = False) -> None:
    """运行单个 .cnsh 文件。"""
    if not path.exists():
        raise CNSHRuntimeError(f"文件不存在: {path}")

    source = path.read_text(encoding="utf-8")
    interpreter = CNSHInterpreter()

    print(f"🐉 CNSH 通心译执行引擎")
    print(f"   源码: {path}")
    print(f"   DNA:#龍芯⚡️2026-06-16-CNSH-RUNTIME-v1.0")
    print()

    if dry_run:
        python_code = interpreter.translate(source, add_explanations=explain)
        print("=== 转译后的 Python 代码（不干运行）===")
        print(python_code)
        return

    result = interpreter.execute(source, add_explanations=explain)

    if show_code or explain:
        print("=== 转译后的 Python 代码 ===")
        print(result["translated_code"])
        print()

    print("✅ 执行完成")


def run_repl() -> None:
    """CNSH 交互式解释器（简易 REPL）。"""
    interpreter = CNSHInterpreter()
    print("🐉 CNSH 交互式通心译解释器")
    print("   输入 '退出' 或 'exit' 结束")
    print()

    buffer: List[str] = []
    while True:
        prompt = "... " if buffer else ">>> "
        try:
            line = input(prompt)
        except EOFError:
            print()
            break

        if line.strip().lower() in ("退出", "exit", "quit"):
            break

        buffer.append(line)
        source = "\n".join(buffer)

        # 尝试执行，若语法不完整则继续读入
        try:
            python_code = interpreter.translate(source)
            ast.parse(python_code)
            buffer = []
            result = interpreter.execute(source)
        except (SyntaxError, CNSHRuntimeError):
            continue

    print("👋 再会")


def main():
    parser = argparse.ArgumentParser(description="CNSH 中文原生脚本运行时")
    parser.add_argument("file", nargs="?", type=Path, help="要执行的 .cnsh 文件")
    parser.add_argument("--explain", action="store_true", help="输出通心译解释注释")
    parser.add_argument("--show-code", action="store_true", help="显示转译后的 Python 代码")
    parser.add_argument("--dry-run", action="store_true", help="仅转译不执行")
    parser.add_argument("--repl", action="store_true", help="进入交互式模式")
    args = parser.parse_args()

    if args.repl:
        run_repl()
    elif args.file:
        run_file(args.file, explain=args.explain, show_code=args.show_code, dry_run=args.dry_run)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
