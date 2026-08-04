#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH词法分析器（Lexer）

DNA:#龍芯⚡️2026-06-03-LEXER-FILE1-v1.0-FROM-JS
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

将CNSH源代码转换为Token流
直译自JavaScript版本(cnsh-compiler.js lines 99-325)

体现原则：
- 参数化: 规则可配置
- 可计算: 每个Token都有dr和hash
- 确定性: 字符级确定性匹配
"""

import hashlib
from typing import List, Optional
from .compiler_node import Token


class Lexer:
    """
    词法分析器（参数化Token识别）

    将源代码转换为Token流，每个Token携带可计算属性：
    - dr: 数字根（用于质量判定）
    - hash: SHA-256（用于去重）

    直译自JavaScript Lexer类，保持结构一致。
    """

    def __init__(self, source: str):
        """
        初始化词法分析器

        Args:
            source: CNSH源代码字符串
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def skip_whitespace(self):
        """跳过空白字符（空格、制表符、换行）"""
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch in (' ', '\t', '\r'):
                self.pos += 1
                self.column += 1
            elif ch == '\n':
                self.pos += 1
                self.line += 1
                self.column = 1
            else:
                break

    def skip_comment(self) -> bool:
        """
        跳过注释（#开头到行末）

        Returns:
            如果成功跳过注释返回True，否则False
        """
        if self.pos < len(self.source) and self.source[self.pos] == '#':
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.pos += 1
            return True
        return False

    def read_identifier(self) -> str:
        """读取标识符（支持中文）"""
        start = self.pos
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            # 中文(U+4E00-U+9FA5)或英文或数字或下划线
            if self._is_identifier_char(ch):
                self.pos += 1
                self.column += 1
            else:
                break
        return self.source[start:self.pos]

    def read_number(self) -> str:
        """读取数字（整数或浮点数）"""
        start = self.pos
        has_decimal = False

        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch.isdigit():
                self.pos += 1
                self.column += 1
            elif ch == '.' and not has_decimal:
                has_decimal = True
                self.pos += 1
                self.column += 1
            else:
                break

        return self.source[start:self.pos]

    def read_string(self, quote: str) -> str:
        """读取字符串字面量"""
        result = ''
        self.pos += 1  # 跳过开引号
        self.column += 1

        while self.pos < len(self.source):
            ch = self.source[self.pos]

            if ch == quote:
                self.pos += 1
                self.column += 1
                break
            elif ch == '\\':
                # 处理转义序列
                self.pos += 1
                self.column += 1
                if self.pos < len(self.source):
                    result += '\\' + self.source[self.pos]
                    self.pos += 1
                    self.column += 1
            else:
                result += ch
                self.pos += 1
                self.column += 1

        return result

    def next_token(self) -> Token:
        """
        读取下一个Token

        Returns:
            Token对象，包含type, value, line, column
        """
        self.skip_whitespace()

        if self.pos >= len(self.source):
            return Token(
                type='EOF',
                value=None,
                line=self.line,
                column=self.column
            )

        if self.skip_comment():
            return self.next_token()

        ch = self.source[self.pos]
        col = self.column
        line = self.line

        # 字符串（支持中文引号）
        if ch in ('"', "'", '“', '‘'):
            close_quote = '”' if ch == '“' else ('’' if ch == '‘' else ch)
            value = self.read_string(close_quote)
            return Token(
                type='STRING',
                value=value,
                line=line,
                column=col
            )

        # 数字
        if ch.isdigit():
            value = self.read_number()
            return Token(
                type='NUMBER',
                value=value,
                line=line,
                column=col
            )

        # 标识符或关键字
        if self._is_identifier_start(ch):
            value = self.read_identifier()
            token_type = 'KEYWORD' if self.is_keyword(value) else 'IDENTIFIER'
            return Token(
                type=token_type,
                value=value,
                line=line,
                column=col
            )

        # 符号
        symbols = {
            '=': 'ASSIGN',
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '%': 'MODULO',
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            '[': 'LBRACKET',
            ']': 'RBRACKET',
            '【': 'LBRACKET',
            '】': 'RBRACKET',
            ';': 'SEMICOLON',
            ',': 'COMMA',
            '.': 'DOT',
            '>': 'GT',
            '<': 'LT',
            '!': 'NOT',
            '&': 'AND',
            '|': 'OR'
        }

        if ch in symbols:
            self.pos += 1
            self.column += 1

            next_ch = self.source[self.pos] if self.pos < len(self.source) else None

            # 双字符符号
            if ch == '=' and next_ch == '=':
                self.pos += 1
                self.column += 1
                return Token(type='EQ', value='==', line=line, column=col)
            if ch == '!' and next_ch == '=':
                self.pos += 1
                self.column += 1
                return Token(type='NEQ', value='!=', line=line, column=col)
            if ch == '>' and next_ch == '=':
                self.pos += 1
                self.column += 1
                return Token(type='GTE', value='>=', line=line, column=col)
            if ch == '<' and next_ch == '=':
                self.pos += 1
                self.column += 1
                return Token(type='LTE', value='<=', line=line, column=col)
            if ch == '&' and next_ch == '&':
                self.pos += 1
                self.column += 1
                return Token(type='LOGICAL_AND', value='&&', line=line, column=col)
            if ch == '|' and next_ch == '|':
                self.pos += 1
                self.column += 1
                return Token(type='LOGICAL_OR', value='||', line=line, column=col)

            return Token(type=symbols[ch], value=ch, line=line, column=col)

        # 未知字符
        self.pos += 1
        self.column += 1
        return Token(type='UNKNOWN', value=ch, line=line, column=col)

    def is_keyword(self, word: str) -> bool:
        """检查词是否是关键字"""
        keywords = [
            '整数', '小数', '文本', '真假', '空值',
            '如果', '否则', '循环', '当', '返回', '跳出', '继续',
            '函数', '类', '结构', '返回类型', '模块', '使用',
            'DNA追溯', '三色审计',
            '熔断',
            '真', '假', '空',
            '对于', '在', '新建', '调用', '添加', '删除', '读取', '写入', '输出',
            '钩子', '全局', '局部', '常量'
        ]
        return word in keywords

    def tokenize(self) -> List[Token]:
        """
        将源代码转换为Token流

        Returns:
            Token列表（以EOF结尾）
        """
        tokens = []
        token = None

        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == 'EOF':
                break

        return tokens

    # 辅助方法
    def _is_identifier_start(self, ch: str) -> bool:
        """检查字符是否能开始标识符"""
        # 中文、英文字母、下划线
        return ch.isalpha() or ch == '_' or self._is_chinese(ch)

    def _is_identifier_char(self, ch: str) -> bool:
        """检查字符是否能在标识符中"""
        return ch.isalnum() or ch == '_' or self._is_chinese(ch)

    @staticmethod
    def _is_chinese(ch: str) -> bool:
        """检查字符是否是中文"""
        code = ord(ch)
        return 0x4e00 <= code <= 0x9fa5


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-06-03-LEXER-v1.0-FROM-JS"
__responsibility__ = "UID9622·不免责"
