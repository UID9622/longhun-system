#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 交互式解释器（REPL）v1.1
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-REPL-v1.1

支持命令：
    .帮助 / .help      显示帮助
    .退出 / .quit     退出 REPL
    .代码 / .py       显示上次转译的 Python 代码
    .令牌 / .tokens   显示上次分词结果
    .DNA              显示系统 DNA
"""
from __future__ import annotations

import sys
from typing import Any, Dict

from .compiler.errors import FriendlyErrorReporter
from .compiler.lexer import Lexer, LexerError
from .compiler.pipeline import compile_cnsh_safe


WELCOME = r"""
╔══════════════════════════════════════════════════════════════════╗
║           龍魂 CNSH 交互式解释器 v1.1                             ║
║     用中文写代码，让编程回归母语                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  帮助: .帮助    退出: .退出   查看代码: .代码   查看令牌: .令牌   ║
╚══════════════════════════════════════════════════════════════════╝
""".strip()

HELP = """
【CNSH REPL 命令】
  .帮助 / .help      显示此帮助
  .退出 / .quit      退出 REPL（或 Ctrl+D / Ctrl+C）
  .代码 / .py        显示最后一次转译的 Python 代码
  .令牌 / .tokens    显示最后一次分词结果
  .DNA               显示系统 DNA 标识

【示例】
  >>> 打印("你好，世界！")
  >>> 函数 平方(x) { 返回 x * x }
  >>> 对于 i 在 范围(5) { 打印(i) }
""".strip()

PROMPT = "CNSH> "
CONTINUE_PROMPT = "...   "


class CNSHREPL:
    def __init__(self):
        self.globals: Dict[str, Any] = {"__name__": "__repl__"}
        self.last_python = ""
        self.last_tokens = []
        self.buffer = ""
        self.in_multiline = False

    def run(self) -> int:
        print(WELCOME)
        while True:
            try:
                line = input(CONTINUE_PROMPT if self.in_multiline else PROMPT)
            except (EOFError, KeyboardInterrupt):
                print("\n👋 再见")
                return 0

            if not self.in_multiline and line.startswith("."):
                if self._handle_command(line):
                    continue

            if self.in_multiline:
                if line.strip() == "":
                    self._execute(self.buffer)
                    self._reset_buffer()
                else:
                    self.buffer += "\n" + line
                    if self._is_structurally_complete(self.buffer):
                        self._execute(self.buffer)
                        self._reset_buffer()
                continue

            if line.strip() == "":
                continue

            if self._needs_multiline(line):
                self.in_multiline = True
                self.buffer = line
                continue

            self._execute(line)
        return 0

    def _reset_buffer(self) -> None:
        self.buffer = ""
        self.in_multiline = False

    def _handle_command(self, cmd: str) -> bool:
        cmd = cmd.strip().lower()
        if cmd in (".退出", ".quit", ".q"):
            print("👋 再见")
            sys.exit(0)
        if cmd in (".帮助", ".help", ".h"):
            print(HELP)
            return True
        if cmd in (".代码", ".code", ".py"):
            if self.last_python:
                print("\n【转译后的 Python 代码】")
                print("-" * 40)
                for i, l in enumerate(self.last_python.split("\n"), 1):
                    print(f"  {i:3d} | {l}")
                print("-" * 40)
            else:
                print("【尚无代码】")
            return True
        if cmd in (".令牌", ".tokens", ".tok"):
            if self.last_tokens:
                print("\n【分词结果】")
                print("-" * 40)
                for t in self.last_tokens:
                    print(f"  {t.type.name:<16} {t.value!r:<20} L{t.line}:{t.col}")
                print("-" * 40)
            else:
                print("【尚无分词结果】")
            return True
        if cmd == ".dna":
            print("#龍芯⚡️2026-06-26-LONGHUN-CNSH-REPL-v1.1")
            return True
        return False

    def _needs_multiline(self, line: str) -> bool:
        s = line.strip()
        if s.endswith(":") or s.endswith("{"):
            return True
        return (
            s.count("(") > s.count(")")
            or s.count("[") > s.count("]")
            or s.count("{") > s.count("}")
        )

    def _is_structurally_complete(self, text: str) -> bool:
        return (
            text.count("{") == text.count("}")
            and text.count("(") == text.count(")")
            and text.count("[") == text.count("]")
        )

    def _execute(self, source: str) -> None:
        try:
            tokens = Lexer(source, "<repl>").tokenize()
            self.last_tokens = tokens
        except LexerError as e:
            print(f"【词法错误】{e}")
            return

        ok, result, err_type = compile_cnsh_safe(source)
        if not ok:
            print(f"【{err_type} 错误】{result}")
            return

        self.last_python = result
        try:
            exec(result, self.globals)
        except Exception as e:
            reporter = FriendlyErrorReporter(source, result, "<repl>")
            print(reporter.report_runtime(e))


def repl_loop() -> int:
    return CNSHREPL().run()
