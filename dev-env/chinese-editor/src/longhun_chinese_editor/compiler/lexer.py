#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 词法分析器（brace-based 版）
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-LEXER-v1.0

为 longhun-chinese-editor 提供真正的词法分析，支持当前 CNSH 示例使用的
大括号块结构、中文关键字、中文标识符。
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class TokenType(Enum):
    KEYWORD = auto()   # 函数/如果/否则/循环/当/对于/返回/打印/类/导入/常量
    TYPE = auto()      # 整数/小数/文本/真假/空值
    BOOL = auto()      # 真/假
    NULL = auto()      # 空
    IDENT = auto()     # 标识符
    NUMBER = auto()    # 数字
    STRING = auto()    # 字符串
    OP = auto()        # 运算符
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LBRACE = auto()    # {
    RBRACE = auto()    # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    SEMI = auto()      # ;
    COMMA = auto()     # ,
    ARROW = auto()     # ->
    NEWLINE = auto()   # 换行
    EOF = auto()       # 结束
    UNKNOWN = auto()   # 未知


KEYWORDS: Dict[str, TokenType] = {
    # 控制流
    "函数": TokenType.KEYWORD,
    "类": TokenType.KEYWORD,
    "结构": TokenType.KEYWORD,
    "如果": TokenType.KEYWORD,
    "否则": TokenType.KEYWORD,
    "否则如果": TokenType.KEYWORD,
    "循环": TokenType.KEYWORD,
    "当": TokenType.KEYWORD,
    "对于": TokenType.KEYWORD,
    "在": TokenType.KEYWORD,
    "范围": TokenType.KEYWORD,
    "返回": TokenType.KEYWORD,
    "跳出": TokenType.KEYWORD,
    "继续": TokenType.KEYWORD,
    "打印": TokenType.KEYWORD,
    "输入": TokenType.KEYWORD,
    "导入": TokenType.KEYWORD,
    "导出": TokenType.KEYWORD,
    "返回类型": TokenType.KEYWORD,
    "常量": TokenType.KEYWORD,
    "静态": TokenType.KEYWORD,
    "异步": TokenType.KEYWORD,
    "等待": TokenType.KEYWORD,
    "尝试": TokenType.KEYWORD,
    "捕获": TokenType.KEYWORD,
    "最终": TokenType.KEYWORD,
    "作为": TokenType.KEYWORD,
    # 字面量
    "真": TokenType.BOOL,
    "假": TokenType.BOOL,
    "空": TokenType.NULL,
    # 类型
    "整数": TokenType.TYPE,
    "小数": TokenType.TYPE,
    "文本": TokenType.TYPE,
    "真假": TokenType.TYPE,
    "空值": TokenType.TYPE,
    "列表": TokenType.TYPE,
    "字典": TokenType.TYPE,
}

TYPES = {"整数", "小数", "文本", "真假", "空值", "列表", "字典"}

OPS = {
    "**": "**",
    "+=": "+=",
    "-=": "-=",
    "*=": "*=",
    "/=": "/=",
    "==": "==",
    "!=": "!=",
    "<=": "<=",
    ">=": ">=",
    "<<": "<<",
    ">>": ">>",
    "&&": "and",
    "||": "or",
    "->": "->",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "%": "%",
    "=": "=",
    "<": "<",
    ">": ">",
    ":": ":",
    ".": ".",
    "!": "not",
    "&": "&",
    "|": "|",
    "^": "^",
    "~": "~",
}

CHINESE_OPS = {
    "且": "and",
    "并且": "and",
    "或": "or",
    "或者": "or",
    "非": "not",
    "不大于": "<=",
    "不小于": ">=",
    "等于": "==",
    "不等于": "!=",
}

PUNCTUATION = {
    "（": "(", "）": ")",
    "【": "(", "】": ")",
    "｛": "{", "｝": "}",
    "；": ";", "，": ",",
    "：": ":",
    "“": '"', "”": '"',
    "‘": "'", "’": "'",
}


@dataclass
class Token:
    type: TokenType
    value: str
    line: int = 1
    col: int = 1

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}C{self.col})"


class LexerError(Exception):
    pass


class Lexer:
    """CNSH 词法分析器（brace-based）"""

    def __init__(self, source: str):
        self.source = self._normalize(source)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []

    def _normalize(self, source: str) -> str:
        for ch, repl in PUNCTUATION.items():
            source = source.replace(ch, repl)
        return source

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _skip_whitespace(self) -> None:
        while self._peek() in " \t\r":
            self._advance()

    def _skip_comment(self) -> bool:
        if self._peek() == "#":
            while self._peek() not in ("\n", "\0"):
                self._advance()
            return True
        return False

    def _read_string(self) -> Token:
        quote = self._peek()
        start_line, start_col = self.line, self.col
        self._advance()
        value = ""
        while self._peek() not in (quote, "\n", "\0"):
            if self._peek() == "\\":
                self._advance()
                esc = self._advance()
                value += {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}.get(esc, esc)
            else:
                value += self._advance()
        if self._peek() != quote:
            raise LexerError(f"未闭合字符串 L{start_line}C{start_col}")
        self._advance()
        return Token(TokenType.STRING, value, start_line, start_col)

    def _read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ""
        has_dot = False
        while self._peek().isdigit() or (self._peek() == "." and not has_dot):
            if self._peek() == ".":
                if self._peek(1) == ".":
                    break
                has_dot = True
            value += self._advance()
        if self._peek() in "eE":
            value += self._advance()
            if self._peek() in "+-":
                value += self._advance()
            while self._peek().isdigit():
                value += self._advance()
        return Token(TokenType.NUMBER, value, start_line, start_col)

    def _read_ident_or_keyword(self) -> Token:
        start_line, start_col = self.line, self.col
        value = ""
        while self._peek().isalnum() or self._peek() == "_" or ("\u4e00" <= self._peek() <= "\u9fff"):
            value += self._advance()
        # 优先匹配较长的中文关键字（否则如果）
        if value in KEYWORDS:
            return Token(KEYWORDS[value], value, start_line, start_col)
        return Token(TokenType.IDENT, value, start_line, start_col)

    def _read_operator(self) -> Token:
        start_line, start_col = self.line, self.col
        # 双字符
        two = self._peek() + self._peek(1)
        if two in OPS:
            self._advance()
            self._advance()
            return Token(TokenType.OP, OPS[two], start_line, start_col)
        # 单字符
        ch = self._advance()
        return Token(TokenType.OP, OPS.get(ch, ch), start_line, start_col)

    def tokenize(self) -> List[Token]:
        while True:
            self._skip_whitespace()
            if self._skip_comment():
                continue
            ch = self._peek()
            line, col = self.line, self.col
            if ch == "\0":
                self.tokens.append(Token(TokenType.EOF, "", line, col))
                break
            if ch == "\n":
                self.tokens.append(Token(TokenType.NEWLINE, "\n", line, col))
                self._advance()
                continue
            if ch in ('"', "'"):
                self.tokens.append(self._read_string())
            elif ch.isdigit():
                self.tokens.append(self._read_number())
            elif ch.isalpha() or ch == "_" or ("\u4e00" <= ch <= "\u9fff"):
                self.tokens.append(self._read_ident_or_keyword())
            elif ch == "(":
                self.tokens.append(Token(TokenType.LPAREN, ch, line, col)); self._advance()
            elif ch == ")":
                self.tokens.append(Token(TokenType.RPAREN, ch, line, col)); self._advance()
            elif ch == "{":
                self.tokens.append(Token(TokenType.LBRACE, ch, line, col)); self._advance()
            elif ch == "}":
                self.tokens.append(Token(TokenType.RBRACE, ch, line, col)); self._advance()
            elif ch == "[":
                self.tokens.append(Token(TokenType.LBRACKET, ch, line, col)); self._advance()
            elif ch == "]":
                self.tokens.append(Token(TokenType.RBRACKET, ch, line, col)); self._advance()
            elif ch == ";":
                self.tokens.append(Token(TokenType.SEMI, ch, line, col)); self._advance()
            elif ch == ",":
                self.tokens.append(Token(TokenType.COMMA, ch, line, col)); self._advance()
            elif ch in "+-*/%=<>!&|^~:.":
                self.tokens.append(self._read_operator())
            else:
                self.tokens.append(Token(TokenType.UNKNOWN, ch, line, col))
                self._advance()
        # 合并相邻 NEWLINE 为单个
        compact: List[Token] = []
        for tok in self.tokens:
            if tok.type == TokenType.NEWLINE and compact and compact[-1].type == TokenType.NEWLINE:
                continue
            compact.append(tok)
        return compact


def tokenize(source: str) -> List[Token]:
    return Lexer(source).tokenize()
