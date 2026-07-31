# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 REPL 交互式解释器
DNA: #龍芯⚡️2026-06-29-CNSH-REPL-v2.1
"""
import sys

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import CNSHError


def run_repl():
    print("🐉 CNSH v2.1 交互式解释器")
    print("   输入 :help 查看帮助，:quit 或 :exit 退出")
    print()

    interpreter = Interpreter()
    buffer: list[str] = []

    while True:
        prompt = "... " if buffer else ">>> "
        try:
            line = input(prompt)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            buffer.clear()
            continue

        stripped = line.strip()
        if not buffer and stripped in (":quit", ":exit", "退出", "exit", "quit"):
            print("👋 再会")
            break
        if not buffer and stripped == ":help":
            print("帮助：")
            print("  :help          显示帮助")
            print("  :quit / :exit  退出 REPL")
            print("  多行输入：以 '{' 或 '(' 开头后未闭合，继续输入即可")
            continue

        buffer.append(line)
        source = "\n".join(buffer)

        # 简单启发：若仍有未闭合括号，继续读
        if not _looks_complete(source):
            continue

        try:
            tokens = Lexer(source, file="<repl>").tokenize()
            ast = Parser(tokens).parse()
            result = interpreter.run(ast)
            if result is not None:
                print(f"=> {result!r}")
            buffer.clear()
        except CNSHError as exc:
            print(exc)
            buffer.clear()
        except Exception as exc:
            print(f"⚠️ 意外错误: {exc}")
            buffer.clear()


def _looks_complete(source: str) -> bool:
    """简单判断源码是否可能完整。"""
    open_braces = source.count("{") - source.count("}")
    open_parens = source.count("(") - source.count(")")
    open_brackets = source.count("[") - source.count("]")
    return open_braces <= 0 and open_parens <= 0 and open_brackets <= 0
