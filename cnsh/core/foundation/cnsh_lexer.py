#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 CNSH 词法分析器
将中文代码解析为Token流

DNA: #龍芯⚡️丙午·丙申·辛酉·庚寅·䷥睽-LEXER-UID9622
"""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


# ============================================================
# Token类型定义
# ============================================================

class TokenType(Enum):
    # 中文关键字
    KEYWORD_FUNCTION = auto()
    KEYWORD_CLASS = auto()
    KEYWORD_IF = auto()
    KEYWORD_ELSE = auto()
    KEYWORD_ELIF = auto()
    KEYWORD_FOR = auto()
    KEYWORD_WHILE = auto()
    KEYWORD_RETURN = auto()
    KEYWORD_IMPORT = auto()
    KEYWORD_FROM = auto()
    KEYWORD_TRUE = auto()
    KEYWORD_FALSE = auto()
    KEYWORD_NONE = auto()
    KEYWORD_AND = auto()
    KEYWORD_OR = auto()
    KEYWORD_NOT = auto()
    KEYWORD_IN = auto()
    KEYWORD_IS = auto()
    KEYWORD_WITH = auto()
    KEYWORD_AS = auto()
    KEYWORD_TRY = auto()
    KEYWORD_EXCEPT = auto()
    KEYWORD_FINALLY = auto()
    KEYWORD_RAISE = auto()
    KEYWORD_YIELD = auto()
    KEYWORD_ASYNC = auto()
    KEYWORD_AWAIT = auto()
    KEYWORD_LAMBDA = auto()
    KEYWORD_GLOBAL = auto()
    KEYWORD_NONLOCAL = auto()
    KEYWORD_DEL = auto()
    KEYWORD_PASS = auto()
    KEYWORD_BREAK = auto()
    KEYWORD_CONTINUE = auto()

    # 类型关键字
    KEYWORD_INT = auto()
    KEYWORD_STR = auto()
    KEYWORD_LIST = auto()
    KEYWORD_DICT = auto()
    KEYWORD_TUPLE = auto()
    KEYWORD_SET = auto()
    KEYWORD_BOOL = auto()
    KEYWORD_FLOAT = auto()

    # 内置函数
    BUILTIN_PRINT = auto()
    BUILTIN_LEN = auto()
    BUILTIN_TYPE = auto()
    BUILTIN_RANGE = auto()
    BUILTIN_ENUMERATE = auto()
    BUILTIN_ZIP = auto()
    BUILTIN_MAP = auto()
    BUILTIN_FILTER = auto()
    BUILTIN_SUM = auto()
    BUILTIN_MAX = auto()
    BUILTIN_MIN = auto()
    BUILTIN_SORTED = auto()
    BUILTIN_REVERSED = auto()
    BUILTIN_OPEN = auto()

    # 标识符/变量名
    IDENTIFIER = auto()

    # 字面量
    STRING = auto()
    NUMBER = auto()

    # 操作符
    OPERATOR_PLUS = auto()
    OPERATOR_MINUS = auto()
    OPERATOR_MUL = auto()
    OPERATOR_DIV = auto()
    OPERATOR_EQ = auto()
    OPERATOR_GT = auto()
    OPERATOR_LT = auto()
    OPERATOR_GE = auto()
    OPERATOR_LE = auto()
    OPERATOR_NE = auto()
    OPERATOR_AND = auto()
    OPERATOR_OR = auto()
    OPERATOR_NOT = auto()

    # 分隔符
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    # 注释
    COMMENT = auto()

    # EOF
    EOF = auto()


@dataclass
class Token:
    """Token数据结构"""
    type: TokenType
    value: str
    line: int
    column: int


# ============================================================
# 词法解析器
# ============================================================

class CNSHLexer:
    """CNSH词法解析器"""

    KEYWORD_MAP = {
        "函数": TokenType.KEYWORD_FUNCTION,
        "类": TokenType.KEYWORD_CLASS,
        "如果": TokenType.KEYWORD_IF,
        "否则": TokenType.KEYWORD_ELSE,
        "否则如果": TokenType.KEYWORD_ELIF,
        "循环": TokenType.KEYWORD_FOR,
        "当": TokenType.KEYWORD_WHILE,
        "返回": TokenType.KEYWORD_RETURN,
        "导入": TokenType.KEYWORD_IMPORT,
        "从": TokenType.KEYWORD_FROM,
        "真": TokenType.KEYWORD_TRUE,
        "假": TokenType.KEYWORD_FALSE,
        "空": TokenType.KEYWORD_NONE,
        "且": TokenType.KEYWORD_AND,
        "或": TokenType.KEYWORD_OR,
        "非": TokenType.KEYWORD_NOT,
        "在": TokenType.KEYWORD_IN,
        "是": TokenType.KEYWORD_IS,
        "使用": TokenType.KEYWORD_WITH,
        "作为": TokenType.KEYWORD_AS,
        "尝试": TokenType.KEYWORD_TRY,
        "捕获": TokenType.KEYWORD_EXCEPT,
        "最终": TokenType.KEYWORD_FINALLY,
        "抛出": TokenType.KEYWORD_RAISE,
        "生成": TokenType.KEYWORD_YIELD,
        "异步": TokenType.KEYWORD_ASYNC,
        "等待": TokenType.KEYWORD_AWAIT,
        "匿名函数": TokenType.KEYWORD_LAMBDA,
        "全局": TokenType.KEYWORD_GLOBAL,
        "非局部": TokenType.KEYWORD_NONLOCAL,
        "删除": TokenType.KEYWORD_DEL,
        "通过": TokenType.KEYWORD_PASS,
        "跳出": TokenType.KEYWORD_BREAK,
        "继续": TokenType.KEYWORD_CONTINUE,
        # 类型
        "整数": TokenType.KEYWORD_INT,
        "文本": TokenType.KEYWORD_STR,
        "列表": TokenType.KEYWORD_LIST,
        "字典": TokenType.KEYWORD_DICT,
        "元组": TokenType.KEYWORD_TUPLE,
        "集合": TokenType.KEYWORD_SET,
        "布尔": TokenType.KEYWORD_BOOL,
        "浮点": TokenType.KEYWORD_FLOAT,
        # 内置函数
        "输出": TokenType.BUILTIN_PRINT,
        "长度": TokenType.BUILTIN_LEN,
        "类型": TokenType.BUILTIN_TYPE,
        "区间": TokenType.BUILTIN_RANGE,
        "枚举": TokenType.BUILTIN_ENUMERATE,
        "压缩": TokenType.BUILTIN_ZIP,
        "映射": TokenType.BUILTIN_MAP,
        "过滤": TokenType.BUILTIN_FILTER,
        "求和": TokenType.BUILTIN_SUM,
        "最大值": TokenType.BUILTIN_MAX,
        "最小值": TokenType.BUILTIN_MIN,
        "排序": TokenType.BUILTIN_SORTED,
        "反转": TokenType.BUILTIN_REVERSED,
        "打开": TokenType.BUILTIN_OPEN,
    }

    OPERATOR_MAP = {
        "+": TokenType.OPERATOR_PLUS,
        "-": TokenType.OPERATOR_MINUS,
        "*": TokenType.OPERATOR_MUL,
        "/": TokenType.OPERATOR_DIV,
        "=": TokenType.OPERATOR_EQ,
        ">": TokenType.OPERATOR_GT,
        "<": TokenType.OPERATOR_LT,
        ">=": TokenType.OPERATOR_GE,
        "<=": TokenType.OPERATOR_LE,
        "!=": TokenType.OPERATOR_NE,
        "&&": TokenType.OPERATOR_AND,
        "||": TokenType.OPERATOR_OR,
        "!": TokenType.OPERATOR_NOT,
    }

    SEPARATOR_MAP = {
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        ":": TokenType.COLON,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        ";": TokenType.SEMICOLON,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]

    def tokenize(self) -> List[Token]:
        """执行词法分析"""
        while self.pos < len(self.source):
            char = self.source[self.pos]

            if char == " ":
                self._advance()
                continue

            if char == "\n":
                self._handle_newline()
                continue

            if char == "#":
                self._handle_comment()
                continue

            if char in ['"', "'", '"', '"', ''', ''']:
                self._handle_string(char)
                continue

            if char.isdigit():
                self._handle_number()
                continue

            if self._is_identifier_char(char):
                self._handle_identifier()
                continue

            two_char = self.source[self.pos:self.pos + 2]
            if two_char in self.OPERATOR_MAP:
                self._add_token(self.OPERATOR_MAP[two_char], two_char)
                self._advance()
                self._advance()
                continue

            if char in self.OPERATOR_MAP:
                self._add_token(self.OPERATOR_MAP[char], char)
                self._advance()
                continue

            if char in self.SEPARATOR_MAP:
                self._add_token(self.SEPARATOR_MAP[char], char)
                self._advance()
                continue

            # 未知字符：跳过
            self._advance()

        self._add_token(TokenType.EOF, "")
        return self.tokens

    def _advance(self):
        """前进一个字符"""
        char = self.source[self.pos]
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def _peek(self, offset: int = 1) -> str:
        """预览字符"""
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return ""

    def _add_token(self, token_type: TokenType, value: str):
        """添加Token"""
        self.tokens.append(Token(token_type, value, self.line, self.column))

    def _handle_newline(self):
        """处理换行与缩进"""
        self._add_token(TokenType.NEWLINE, "\n")
        self._advance()

        indent = 0
        while self.pos < len(self.source) and self.source[self.pos] == " ":
            indent += 1
            self._advance()

        if indent > self.indent_stack[-1]:
            self._add_token(TokenType.INDENT, " " * (indent - self.indent_stack[-1]))
            self.indent_stack.append(indent)
        elif indent < self.indent_stack[-1]:
            while self.indent_stack[-1] > indent:
                self._add_token(TokenType.DEDENT, "")
                self.indent_stack.pop()

    def _handle_comment(self):
        """处理注释"""
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != "\n":
            self._advance()
        comment_text = self.source[start:self.pos]
        self._add_token(TokenType.COMMENT, comment_text)

    def _handle_string(self, quote_char: str):
        """处理字符串"""
        start = self.pos
        self._advance()
        while self.pos < len(self.source) and self.source[self.pos] != quote_char:
            if self.source[self.pos] == "\\":
                self._advance()
            self._advance()
        if self.pos < len(self.source):
            self._advance()  # 跳过结束引号
        string_text = self.source[start:self.pos]
        self._add_token(TokenType.STRING, string_text)

    def _handle_number(self):
        """处理数字"""
        start = self.pos
        while self.pos < len(self.source) and (
            self.source[self.pos].isdigit() or self.source[self.pos] == "."
        ):
            self._advance()
        number_text = self.source[start:self.pos]
        self._add_token(TokenType.NUMBER, number_text)

    def _handle_identifier(self):
        """处理标识符 (中文或英文)"""
        start = self.pos
        while self.pos < len(self.source) and self._is_identifier_char(self.source[self.pos]):
            self._advance()
        ident = self.source[start:self.pos]

        if ident in self.KEYWORD_MAP:
            self._add_token(self.KEYWORD_MAP[ident], ident)
        else:
            self._add_token(TokenType.IDENTIFIER, ident)

    def _handle_operator(self):
        """处理操作符（备用）"""
        two_char = self.source[self.pos : self.pos + 2]
        if two_char in self.OPERATOR_MAP:
            self._add_token(self.OPERATOR_MAP[two_char], two_char)
            self._advance()
            self._advance()
            return
        char = self.source[self.pos]
        if char in self.OPERATOR_MAP:
            self._add_token(self.OPERATOR_MAP[char], char)
            self._advance()

    def _is_identifier_char(self, char: str) -> bool:
        """判断是否是标识符字符 (中文/英文/数字/下划线)"""
        cjk_ranges = [
            (0x4E00, 0x9FFF),
            (0x3400, 0x4DBF),
            (0x20000, 0x2A6DF),
            (0x2A700, 0x2B73F),
            (0x2B740, 0x2B81F),
            (0x2B820, 0x2CEAF),
            (0x2CEB0, 0x2EBEF),
            (0x30000, 0x3134F),
        ]
        code = ord(char)
        for start, end in cjk_ranges:
            if start <= code <= end:
                return True
        return char.isalnum() or char == "_"


# ============================================================
# 测试
# ============================================================


def test_lexer():
    """测试词法分析器"""
    code = """
    函数 计算折扣(原价, 折扣率):
        返回 原价 * 折扣率

    类 商品:
        函数 初始化(名称, 价格):
            这个.名称 = 名称
            这个.价格 = 价格
    """

    lexer = CNSHLexer(code)
    tokens = lexer.tokenize()

    print("🐉 CNSH 词法分析结果")
    print("=" * 50)
    for token in tokens:
        print(f"{token.type.name:25} {token.value!r:25} [{token.line}:{token.column}]")
    return tokens


if __name__ == "__main__":
    test_lexer()
