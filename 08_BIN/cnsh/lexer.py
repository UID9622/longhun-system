#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 词法分析器 v1.1
DNA: #龍芯⚡️2026-08-31-CNSH-LEXER-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 支持任意符号变量名（# @ $ % ! 等），注释使用 // 和 /* */
"""

from typing import List, Optional


class CNSHToken:
    """CNSH词法单元"""
    def __init__(self, type_: str, value: str, line: int = 0, col: int = 0):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', L{self.line}:C{self.col})"


class CNSHLexer:
    """CNSH 词法分析器"""

    # 运算符（这些字符不能出现在短格式变量名中）
    OPERATOR_CHARS = set('=+-*/(){}[];,.:!&|<>')

    # 中文运算符（优先匹配长串，防止「等于」被识别成「等」+「于」）
    CHINESE_OPERATORS = [
        ('大于等于', 'GTE'),
        ('小于等于', 'LTE'),
        ('不等于', 'NEQ'),
        ('等于', 'EQ'),
        ('大于', 'GT'),
        ('小于', 'LT'),
        ('加', 'PLUS'),
        ('减', 'MINUS'),
        ('乘', 'MUL'),
        ('除', 'DIV'),
        ('且', 'AND'),
        ('或', 'OR'),
        ('非', 'NOT'),
    ]

    # ASCII运算符映射
    ASCII_OPERATORS = {
        '=': 'ASSIGN', '+': 'PLUS', '-': 'MINUS',
        '*': 'MUL',    '/': 'DIV',  '%': 'MOD',
        '(': 'LPAREN', ')': 'RPAREN',
        '{': 'LBRACE', '}': 'RBRACE',
        '[': 'LBRACKET', ']': 'RBRACKET',
        ',': 'COMMA',  ';': 'SEMICOLON',
        '.': 'DOT',    ':': 'COLON',
        '!': 'BANG',   '&': 'AMP',
        '|': 'PIPE',   '<': 'LT_ASCII',
        '>': 'GT_ASCII',
    }

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[CNSHToken] = []

    def _peek(self, offset: int = 1) -> Optional[str]:
        idx = self.pos + offset
        return self.source[idx] if idx < self.length else None

    def _is_cn(self, ch: str) -> bool:
        return '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf'

    def _match_chinese_op(self) -> Optional[tuple]:
        """尝试从当前位置匹配中文运算符（优先长串）"""
        for op_str, op_type in self.CHINESE_OPERATORS:
            end = self.pos + len(op_str)
            if self.source[self.pos:end] == op_str:
                return op_str, op_type
        return None

    def tokenize(self) -> List[CNSHToken]:
        """执行词法分析"""
        while self.pos < self.length:
            ch = self.source[self.pos]

            # ── 空白 ──────────────────────────────────────
            if ch.isspace():
                if ch == '\n':
                    self.tokens.append(CNSHToken('NEWLINE', '\n', self.line, self.col))
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1
                continue

            # ── 行注释 // ─────────────────────────────────
            if ch == '/' and self._peek() == '/':
                self.pos += 2
                while self.pos < self.length and self.source[self.pos] != '\n':
                    self.pos += 1
                continue

            # ── 块注释 /* */ ──────────────────────────────
            if ch == '/' and self._peek() == '*':
                self.pos += 2
                while self.pos < self.length:
                    if self.source[self.pos] == '*' and self._peek() == '/':
                        self.pos += 2
                        break
                    if self.source[self.pos] == '\n':
                        self.line += 1
                        self.col = 1
                    self.pos += 1
                continue

            # ── 数字 ──────────────────────────────────────
            if ch.isdigit() or (ch == '.' and self._peek() and self._peek().isdigit()):
                start = self.pos
                has_dot = False
                while self.pos < self.length:
                    c = self.source[self.pos]
                    if c.isdigit():
                        self.pos += 1
                    elif c == '.' and not has_dot:
                        has_dot = True
                        self.pos += 1
                    else:
                        break
                value = self.source[start:self.pos]
                self.tokens.append(CNSHToken('NUMBER', value, self.line, self.col))
                self.col += len(value)
                continue

            # ── 字符串（双引号）────────────────────────────
            if ch == '"':
                self.pos += 1
                start = self.pos
                while self.pos < self.length and self.source[self.pos] != '"':
                    if self.source[self.pos] == '\\':
                        self.pos += 2  # 处理转义
                    else:
                        self.pos += 1
                value = self.source[start:self.pos]
                self.pos += 1
                self.tokens.append(CNSHToken('STRING', value, self.line, self.col))
                continue

            # ── 字符串（单引号）────────────────────────────
            if ch == "'":
                self.pos += 1
                start = self.pos
                while self.pos < self.length and self.source[self.pos] != "'":
                    if self.source[self.pos] == '\\':
                        self.pos += 2
                    else:
                        self.pos += 1
                value = self.source[start:self.pos]
                self.pos += 1
                self.tokens.append(CNSHToken('STRING', value, self.line, self.col))
                continue

            # ── 变量（$ 开头，核心功能）────────────────────
            if ch == '$':
                self.pos += 1
                self.col += 1
                if self.pos < self.length and self.source[self.pos] == '{':
                    # 长格式 ${...}
                    self.pos += 1
                    start = self.pos
                    while self.pos < self.length and self.source[self.pos] != '}':
                        if self.source[self.pos] == '\n':
                            self.line += 1
                            self.col = 1
                        self.pos += 1
                    value = self.source[start:self.pos]
                    self.pos += 1  # 跳过 }
                    self.tokens.append(CNSHToken('VAR', value, self.line, self.col))
                else:
                    # 短格式：直到空白或运算符
                    start = self.pos
                    while self.pos < self.length:
                        c = self.source[self.pos]
                        if c.isspace() or c in self.OPERATOR_CHARS:
                            break
                        self.pos += 1
                    value = self.source[start:self.pos]
                    self.tokens.append(CNSHToken('VAR', value, self.line, self.col))
                    self.col += len(value)
                continue

            # ── 中文字符（关键字 or 标识符）────────────────
            if self._is_cn(ch):
                # 优先匹配中文运算符
                matched = self._match_chinese_op()
                if matched:
                    op_str, op_type = matched
                    self.tokens.append(CNSHToken(op_type, op_str, self.line, self.col))
                    self.pos += len(op_str)
                    self.col += len(op_str)
                    continue
                # 普通中文标识符
                start = self.pos
                while self.pos < self.length and (
                    self._is_cn(self.source[self.pos])
                    or self.source[self.pos].isalnum()
                    or self.source[self.pos] == '_'
                ):
                    self.pos += 1
                value = self.source[start:self.pos]
                self.tokens.append(CNSHToken('IDENTIFIER', value, self.line, self.col))
                self.col += len(value)
                continue

            # ── 英文标识符 ────────────────────────────────
            if ch.isalpha() or ch == '_':
                start = self.pos
                while self.pos < self.length and (
                    self.source[self.pos].isalnum() or self.source[self.pos] == '_'
                ):
                    self.pos += 1
                value = self.source[start:self.pos]
                self.tokens.append(CNSHToken('IDENTIFIER', value, self.line, self.col))
                self.col += len(value)
                continue

            # ── ASCII运算符 ───────────────────────────────
            if ch in self.ASCII_OPERATORS:
                self.tokens.append(CNSHToken(self.ASCII_OPERATORS[ch], ch, self.line, self.col))
                self.pos += 1
                self.col += 1
                continue

            # ── 其他符号（透传）───────────────────────────
            self.tokens.append(CNSHToken('SYMBOL', ch, self.line, self.col))
            self.pos += 1
            self.col += 1

        return self.tokens


if __name__ == '__main__':
    code = '''
    // 测试通用符号变量
    $#var = 100
    $@data = "hello"
    ${#special!} = 3.14
    $用户年龄 = 28
    输出($#var)
    '''
    lexer = CNSHLexer(code)
    for t in lexer.tokenize():
        if t.type != 'NEWLINE':
            print(t)
