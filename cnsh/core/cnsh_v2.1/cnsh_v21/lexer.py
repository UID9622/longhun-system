#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 词法分析器 (Lexer)
DNA: #龍芯⚡️2026-06-29-CNSH-LEXER-v2.1
"""
import re
from typing import List, Optional

from .tokens import Token, KEYWORDS, OPERATORS, PUNCTUATION
from .errors import CNSHLexError


class Lexer:
    """CNSH v2.1 词法分析器"""

    def __init__(self, source: str, file: Optional[str] = None):
        self.source = source
        self.file = file or "<cnsh>"
        self.tokens: List[Token] = []
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= len(self.source):
            return "\0"
        return self.source[idx]

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _add_token(self, type_: str, value: str):
        self.tokens.append(Token(type_, value, self.line, self.column, self.file))

    def _is_cjk(self, ch: str) -> bool:
        return "\u4e00" <= ch <= "\u9fff"

    def _is_id_start(self, ch: str) -> bool:
        return self._is_cjk(ch) or ch.isalpha() or ch == "_"

    def _is_id_continue(self, ch: str) -> bool:
        return self._is_id_start(ch) or ch.isdigit() or ch == "_"

    def _is_weight_char(self, ch: str) -> bool:
        return ch == "\u2696" or ch == "\u2696\ufe0f"

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self._scan_token()
        self.tokens.append(Token("EOF", "", self.line, self.column, self.file))
        return self.tokens

    def _scan_token(self):
        ch = self._peek()

        # 跳过普通空白（非换行）
        if ch in " \t\r":
            self._advance()
            return

        # 换行 -> 生成 NEWLINE
        if ch == "\n":
            self._add_token("NEWLINE", "\n")
            self._advance()
            return

        # 权重符号 ⚖️
        if self._is_weight_char(ch):
            self._add_token("WEIGHT", "⚖️")
            self._advance()
            if self._peek() == "\ufe0f":
                self._advance()
            return

        # 注释 / DNA 注释
        if ch == "#":
            self._scan_comment()
            return

        # 块注释 /* ... */
        if ch == "/" and self._peek(1) == "*":
            self._scan_block_comment()
            return

        # 字符串
        if ch in ('"', "'"):
            self._scan_string(ch)
            return

        # 数字
        if ch.isdigit():
            self._scan_number()
            return

        # 标识符 / 关键字
        if self._is_id_start(ch):
            self._scan_identifier()
            return

        # 双字符运算符
        two = self.source[self.pos : self.pos + 2]
        if two in OPERATORS:
            self._add_token(OPERATORS[two], two)
            self._advance()
            self._advance()
            return

        # 单字符运算符
        if ch in OPERATORS:
            self._add_token(OPERATORS[ch], ch)
            self._advance()
            return

        # 标点
        if ch in PUNCTUATION:
            self._add_token(PUNCTUATION[ch], ch)
            self._advance()
            return

        raise CNSHLexError(f"无法识别的字符: {ch!r}", self.line, self.column, self.file)

    def _scan_comment(self):
        start_line = self.line
        start_col = self.column
        # 消费 '#'
        self._advance()
        body = ""
        while self._peek() not in ("\n", "\0"):
            body += self._advance()
        # DNA 注释特殊标记
        stripped = body.lstrip()
        if stripped.startswith("DNA:"):
            self.tokens.append(Token("DNA_COMMENT", "#" + body, start_line, start_col, self.file))
        else:
            self.tokens.append(Token("COMMENT", "#" + body, start_line, start_col, self.file))

    def _scan_block_comment(self):
        start_line = self.line
        start_col = self.column
        body = ""
        body += self._advance()  # '/'
        body += self._advance()  # '*'
        while not (self._peek() == "*" and self._peek(1) == "/"):
            if self._peek() == "\0":
                raise CNSHLexError("未闭合的块注释", start_line, start_col, self.file)
            body += self._advance()
        body += self._advance()  # '*'
        body += self._advance()  # '/'
        self.tokens.append(Token("COMMENT", body, start_line, start_col, self.file))

    def _scan_string(self, quote: str):
        start_line = self.line
        start_col = self.column
        value = ""
        self._advance()  # 开引号
        while self._peek() != quote:
            if self._peek() == "\0" or self._peek() == "\n":
                raise CNSHLexError("未闭合的字符串", start_line, start_col, self.file)
            if self._peek() == "\\":
                self._advance()
                esc = self._advance()
                value += self._unescape(esc)
            else:
                value += self._advance()
        self._advance()  # 闭引号
        self.tokens.append(Token("STRING", value, start_line, start_col, self.file))

    @staticmethod
    def _unescape(esc: str) -> str:
        mapping = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "\"": "\"",
            "'": "'",
            "\\": "\\",
        }
        return mapping.get(esc, esc)

    def _scan_number(self):
        start_line = self.line
        start_col = self.column
        num = ""
        is_float = False
        while self._peek().isdigit():
            num += self._advance()
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            num += self._advance()
            while self._peek().isdigit():
                num += self._advance()
        token_type = "NUMBER"
        value = float(num) if is_float else int(num)
        self.tokens.append(Token(token_type, str(value), start_line, start_col, self.file))

    def _scan_identifier(self):
        start_line = self.line
        start_col = self.column
        name = ""
        # Greedy accumulate all CJK + alphanumeric chars
        while self._is_id_continue(self._peek()):
            name += self._advance()
        # 尝试拆分复合中文关键字（最长匹配优先）
        if self._is_cjk(name[0]) if name else False:
            self._emit_cjk_tokens(name, start_line, start_col)
        else:
            kind = KEYWORDS.get(name, "IDENTIFIER")
            self.tokens.append(Token(kind, name, start_line, start_col, self.file))

    def _emit_cjk_tokens(self, text: str, start_line: int, start_col: int):
        """对连续 CJK 标识符文本做关键字/标识符判定。
        连续文本作为一个整体：若整体命中关键字则输出关键字，否则输出标识符。
        这样可避免关键字前缀把复合名称（如 写入文件、全局变量）拆开。
        """
        if text in KEYWORDS:
            kind = KEYWORDS[text]
            self.tokens.append(Token(kind, text, start_line, start_col, self.file))
        else:
            self.tokens.append(Token("IDENTIFIER", text, start_line, start_col, self.file))
