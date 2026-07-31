#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·CNSH编译器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH编译器-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：将 .cnsh 源文件编译为可执行的 Python 代码
定位：龙魂系统中文编程语言编译器
"""

import sys
import re
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import argparse
import traceback

# ============================================================
# 一、词法分析器 (Lexer)
# ============================================================

class TokenType(Enum):
    """Token类型枚举（中文关键字映射）"""
    # 关键字
    功能 = "功能"       # def
    返回 = "返回"       # return
    如果 = "如果"       # if
    否则 = "否则"       # else
    循环 = "循环"       # for
    当 = "当"           # while
    跳出 = "跳出"       # break
    继续 = "继续"       # continue
    导入 = "导入"       # import
    从 = "从"           # from
    类型 = "类型"       # type
    类 = "类"           # class
    空 = "空"           # None
    真 = "真"           # True
    假 = "假"           # False

    # 数据类型
    整数 = "整数"       # int
    小数 = "小数"       # float
    文本 = "文本"       # str
    布尔 = "布尔"       # bool
    列表 = "列表"       # list
    字典 = "字典"       # dict
    集合 = "集合"       # set
    元组 = "元组"       # tuple

    # 标识符
    IDENTIFIER = "标识符"
    NUMBER = "数字"
    STRING = "字符串"
    COMMENT = "注释"

    # 运算符
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MOD = "%"
    POWER = "**"
    EQUAL = "="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    AND = "和"          # and
    OR = "或"           # or
    NOT = "非"          # not
    IN = "在"           # in
    IS = "是"           # is

    # 分隔符
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COLON = ":"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    ARROW = "->"

    # 特殊
    DNA = "DNA"         # DNA追溯码
    CONFIRM = "确认码"  # 确认码
    EOF = "EOF"

    @classmethod
    def 关键字映射(cls) -> Dict[str, 'TokenType']:
        """中文关键字映射表"""
        return {
            "功能": cls.功能,
            "返回": cls.返回,
            "如果": cls.如果,
            "否则": cls.否则,
            "循环": cls.循环,
            "当": cls.当,
            "跳出": cls.跳出,
            "继续": cls.继续,
            "导入": cls.导入,
            "从": cls.从,
            "类型": cls.类型,
            "类": cls.类,
            "空": cls.空,
            "真": cls.真,
            "假": cls.假,
            "整数": cls.整数,
            "小数": cls.小数,
            "文本": cls.文本,
            "布尔": cls.布尔,
            "列表": cls.列表,
            "字典": cls.字典,
            "集合": cls.集合,
            "元组": cls.元组,
            "和": cls.AND,
            "或": cls.OR,
            "非": cls.NOT,
            "在": cls.IN,
            "是": cls.IS,
            "DNA": cls.DNA,
            "确认码": cls.CONFIRM,
        }

    @classmethod
    def 关键词列表(cls) -> List[str]:
        return list(cls.关键字映射().keys())


@dataclass
class Token:
    """Token数据结构"""
    type: TokenType
    value: str
    line: int
    column: int
    file: str = ""

    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}', L{self.line}:C{self.column})"


class Lexer:
    """CNSH词法分析器"""

    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.errors = []

    def peek_char(self, n: int = 0) -> str:
        """窥视第n个字符（0=当前）"""
        if self.pos + n >= len(self.source):
            return ""
        return self.source[self.pos + n]

    def advance(self) -> str:
        """前进一个字符"""
        if self.pos >= len(self.source):
            return ""
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return char

    def is_chinese(self, char: str) -> bool:
        """判断是否为中文字符"""
        if not char:
            return False
        return '\u4e00' <= char <= '\u9fff'

    def is_chinese_or_letter(self, char: str) -> bool:
        """判断是否为中文、字母或下划线"""
        if not char:
            return False
        return (self.is_chinese(char) or
                char.isalpha() or
                char == '_')

    def is_chinese_or_letter_or_digit(self, char: str) -> bool:
        """判断是否为中文、字母、数字或下划线"""
        if not char:
            return False
        return (self.is_chinese_or_letter(char) or
                char.isdigit())

    def tokenize(self) -> List[Token]:
        """执行词法分析"""
        while self.pos < len(self.source):
            char = self.peek_char()

            # 跳过空白
            if char.isspace():
                self.advance()
                continue

            # 注释 (# ...)
            if char == '#':
                start_line = self.line
                start_col = self.col
                comment = ""
                self.advance()  # 跳过 #
                while self.pos < len(self.source) and self.peek_char() != '\n':
                    comment += self.advance()
                self.tokens.append(Token(
                    TokenType.COMMENT,
                    comment.strip(),
                    start_line,
                    start_col,
                    self.filename
                ))
                continue

            # 字符串 "..."
            if char == '"':
                start_line = self.line
                start_col = self.col
                string = ""
                self.advance()  # 跳过开始引号
                while self.pos < len(self.source) and self.peek_char() != '"':
                    string += self.advance()
                if self.pos < len(self.source) and self.peek_char() == '"':
                    self.advance()  # 跳过结束引号
                self.tokens.append(Token(
                    TokenType.STRING,
                    string,
                    start_line,
                    start_col,
                    self.filename
                ))
                continue

            # 字符串 '...'
            if char == "'":
                start_line = self.line
                start_col = self.col
                string = ""
                self.advance()
                while self.pos < len(self.source) and self.peek_char() != "'":
                    string += self.advance()
                if self.pos < len(self.source) and self.peek_char() == "'":
                    self.advance()
                self.tokens.append(Token(
                    TokenType.STRING,
                    string,
                    start_line,
                    start_col,
                    self.filename
                ))
                continue

            # 数字（整数或小数）
            if char.isdigit():
                start_line = self.line
                start_col = self.col
                num = ""
                while self.pos < len(self.source) and (self.peek_char().isdigit() or self.peek_char() == '.'):
                    num += self.advance()
                self.tokens.append(Token(
                    TokenType.NUMBER,
                    num,
                    start_line,
                    start_col,
                    self.filename
                ))
                continue

            # 中文关键字或标识符
            if self.is_chinese(char):
                start_line = self.line
                start_col = self.col
                identifier = ""
                while self.pos < len(self.source) and self.is_chinese_or_letter_or_digit(self.peek_char()):
                    identifier += self.advance()
                # 检查是否为关键字
                keyword_map = TokenType.关键字映射()
                if identifier in keyword_map:
                    self.tokens.append(Token(
                        keyword_map[identifier],
                        identifier,
                        start_line,
                        start_col,
                        self.filename
                    ))
                else:
                    self.tokens.append(Token(
                        TokenType.IDENTIFIER,
                        identifier,
                        start_line,
                        start_col,
                        self.filename
                    ))
                continue

            # 英文标识符（如变量名中的英文部分）
            if char.isalpha():
                start_line = self.line
                start_col = self.col
                identifier = ""
                while self.pos < len(self.source) and (self.peek_char().isalnum() or self.peek_char() == '_'):
                    identifier += self.advance()
                self.tokens.append(Token(
                    TokenType.IDENTIFIER,
                    identifier,
                    start_line,
                    start_col,
                    self.filename
                ))
                continue

            # 多字符运算符
            if char == '=':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUAL_EQUAL, "==", self.line, self.col - 2, self.filename))
                    continue

            if char == '!':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", self.line, self.col - 2, self.filename))
                    continue

            if char == '>':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", self.line, self.col - 2, self.filename))
                    continue

            if char == '<':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", self.line, self.col - 2, self.filename))
                    continue

            if char == '*':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '*':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.POWER, "**", self.line, self.col - 2, self.filename))
                    continue

            if char == '-':
                if self.pos + 1 < len(self.source) and self.peek_char(1) == '>':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, "->", self.line, self.col - 2, self.filename))
                    continue

            # 单字符运算符和分隔符
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MOD,
                '=': TokenType.EQUAL,
                '>': TokenType.GREATER,
                '<': TokenType.LESS,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ':': TokenType.COLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ';': TokenType.SEMICOLON,
            }

            if char in single_char_tokens:
                start_line = self.line
                start_col = self.col
                self.tokens.append(Token(
                    single_char_tokens[char],
                    char,
                    start_line,
                    start_col,
                    self.filename
                ))
                self.advance()
                continue

            # 未知字符
            self.errors.append(f"L{self.line}:C{self.col}: 未知字符 '{char}'")
            self.advance()

        # 添加EOF
        self.tokens.append(Token(TokenType.EOF, "EOF", self.line, self.col, self.filename))
        return self.tokens


# ============================================================
# 二、语法分析器 (Parser)
# ============================================================

@dataclass
class ASTNode:
    """AST节点基类 — 所有字段给默认值以兼容 dataclass 继承"""
    type: str = ""
    line: int = 0
    column: int = 0


@dataclass
class ProgramNode(ASTNode):
    """程序根节点"""
    statements: List[ASTNode] = field(default_factory=list)
    dna: Optional[str] = None
    confirm: Optional[str] = None


@dataclass
class FunctionDefNode(ASTNode):
    """函数定义节点"""
    name: str = ""
    params: List[Tuple[str, Optional[str]]] = field(default_factory=list
    )  # (参数名, 类型)
    return_type: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ReturnNode(ASTNode):
    """返回语句节点"""
    value: Optional[ASTNode] = None


@dataclass
class IfNode(ASTNode):
    """条件语句节点"""
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class ElifNode(ASTNode):
    """否则如果节点"""
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForNode(ASTNode):
    """循环语句节点"""
    variable: str = ""
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileNode(ASTNode):
    """当循环节点"""
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class BreakNode(ASTNode):
    """跳出节点"""
    pass


@dataclass
class ContinueNode(ASTNode):
    """继续节点"""
    pass


@dataclass
class ImportNode(ASTNode):
    """导入节点"""
    module: str = ""
    alias: Optional[str] = None


@dataclass
class AssignNode(ASTNode):
    """赋值节点"""
    target: str = ""
    value: Optional[ASTNode] = None
    var_type: Optional[str] = None


@dataclass
class BinaryOpNode(ASTNode):
    """二元运算节点"""
    left: Optional[ASTNode] = None
    op: str = ""
    right: Optional[ASTNode] = None


@dataclass
class UnaryOpNode(ASTNode):
    """一元运算节点"""
    op: str = ""
    operand: Optional[ASTNode] = None


@dataclass
class CallNode(ASTNode):
    """函数调用节点"""
    name: str = ""
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class IdentifierNode(ASTNode):
    """标识符节点"""
    name: str = ""


@dataclass
class NumberNode(ASTNode):
    """数字节点"""
    value: Union[int, float] = 0


@dataclass
class StringNode(ASTNode):
    """字符串节点"""
    value: str = ""


@dataclass
class ListNode(ASTNode):
    """列表节点"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class DictNode(ASTNode):
    """字典节点"""
    pairs: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)


@dataclass
class AttributeNode(ASTNode):
    """属性访问节点"""
    obj: Optional[ASTNode] = None
    attr: str = ""


class Parser:
    """CNSH语法分析器"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self._update_current()

    def _update_current(self):
        """更新当前Token"""
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self) -> Token:
        """前进到下一个Token"""
        token = self.current
        self.pos += 1
        self._update_current()
        return token

    def expect(self, token_type: TokenType, error_msg: str = "") -> Token:
        """期待指定类型的Token"""
        if self.current and self.current.type == token_type:
            return self.advance()
        if not error_msg:
            error_msg = f"期望 {token_type.value}，但遇到 {self.current.value if self.current else 'EOF'}"
        self.errors.append(f"L{self.current.line if self.current else '?'}: {error_msg}")
        return None

    def match(self, token_type: TokenType) -> bool:
        """检查当前Token是否匹配指定类型"""
        return self.current is not None and self.current.type == token_type

    def parse(self) -> ProgramNode:
        """解析程序入口"""
        program = ProgramNode(type="Program")

        # 解析DNA和确认码（如果存在）
        if self.match(TokenType.DNA):
            dna_token = self.advance()
            if self.match(TokenType.STRING):
                program.dna = self.advance().value
            elif self.match(TokenType.IDENTIFIER):
                program.dna = self.advance().value

        if self.match(TokenType.CONFIRM):
            self.advance()
            if self.match(TokenType.STRING):
                program.confirm = self.advance().value
            elif self.match(TokenType.IDENTIFIER):
                program.confirm = self.advance().value

        # 解析语句
        while self.current and self.current.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            else:
                # 如果解析失败，跳过此Token继续
                if self.current and self.current.type != TokenType.EOF:
                    self.advance()

        return program

    def parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        if not self.current:
            return None

        token = self.current

        # RBRACE/EOF 不是语句，直接返回None让外层循环处理
        if token.type in (TokenType.RBRACE, TokenType.EOF):
            return None

        # 注释：返回 None，外层 parse() 的 else 分支统一 advance
        if token.type == TokenType.COMMENT:
            return None

        # 功能 函数名(...) { ... }
        if token.type == TokenType.功能:
            return self.parse_function_def()

        # 返回 ...
        if token.type == TokenType.返回:
            return self.parse_return()

        # 如果 ... { ... } 否则 { ... }
        if token.type == TokenType.如果:
            return self.parse_if()

        # 循环 ... { ... }
        if token.type == TokenType.循环:
            return self.parse_for()

        # 当 ... { ... }
        if token.type == TokenType.当:
            return self.parse_while()

        # 跳出
        if token.type == TokenType.跳出:
            self.advance()
            return BreakNode(type="Break", line=token.line, column=token.column)

        # 继续
        if token.type == TokenType.继续:
            self.advance()
            return ContinueNode(type="Continue", line=token.line, column=token.column)

        # 导入
        if token.type == TokenType.导入:
            return self.parse_import()

        # 赋值或表达式
        return self.parse_assign_or_expr()

    def parse_function_def(self) -> FunctionDefNode:
        """解析函数定义"""
        start_token = self.advance()  # 功能

        # 函数名
        if not self.match(TokenType.IDENTIFIER):
            self.errors.append(f"L{start_token.line}: 期望函数名")
            # 跳过直到能找到下一个语句
            while self.current and self.current.type not in [TokenType.功能, TokenType.EOF]:
                self.advance()
            return None

        name_token = self.advance()
        name = name_token.value

        # 参数列表
        params = []
        return_type = None

        if self.match(TokenType.LPAREN):
            self.advance()  # (
            while self.current and self.current.type != TokenType.RPAREN:
                if self.match(TokenType.IDENTIFIER):
                    param_name = self.advance().value
                    param_type = None
                    # 检查类型标注（支持 整数/文本/小数/布尔/列表/字典/集合/元组）
                    if self.match(TokenType.COLON):
                        self.advance()  # :
                        param_type = self._parse_type_annotation()
                    params.append((param_name, param_type))
                    if self.match(TokenType.COMMA):
                        self.advance()
                elif self.match(TokenType.COMMA):
                    self.advance()
                else:
                    break
            self.expect(TokenType.RPAREN, "期望 ')'")

        # 返回类型
        if self.match(TokenType.ARROW):
            self.advance()  # ->
            return_type = self._parse_type_annotation()

        # 函数体
        self.expect(TokenType.LBRACE, "期望 '{'")
        body = []
        while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE, "期望 '}'")

        return FunctionDefNode(
            type="FunctionDef",
            line=start_token.line,
            column=start_token.column,
            name=name,
            params=params,
            return_type=return_type,
            body=body
        )

    def parse_return(self) -> ReturnNode:
        """解析返回语句"""
        token = self.advance()  # 返回
        value = None
        if self.current and self.current.type not in [TokenType.RBRACE, TokenType.EOF]:
            value = self.parse_expression()
        return ReturnNode(
            type="Return",
            line=token.line,
            column=token.column,
            value=value
        )

    def parse_if(self) -> IfNode:
        """解析如果语句，支持否则如果链"""
        token = self.advance()  # 如果
        condition = self.parse_expression()

        self.expect(TokenType.LBRACE, "期望 '{'")
        body = []
        while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE, "期望 '}'")

        else_body = []
        # 处理否则或否则如果
        while self.current and self.current.type == TokenType.否则:
            self.advance()  # 否则
            # 检查是否为 "否则 如果"
            if self.current and self.current.type == TokenType.如果:
                # 否则如果 -> 转换为嵌套的if
                self.advance()  # 如果
                elif_condition = self.parse_expression()
                self.expect(TokenType.LBRACE, "期望 '{'")
                elif_body = []
                while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        elif_body.append(stmt)
                self.expect(TokenType.RBRACE, "期望 '}'")
                # 包装为 if 节点放入 else_body
                else_body.append(IfNode(
                    type="If", line=token.line, column=token.column,
                    condition=elif_condition, body=elif_body, else_body=[]
                ))
                # 如果后面可能还有否则/否则如果，继续循环
                continue
            else:
                # 否则 { ... }
                self.expect(TokenType.LBRACE, "期望 '{'")
                while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                self.expect(TokenType.RBRACE, "期望 '}'")
                break  # 否则后面不能有更多否则

        return IfNode(
            type="If",
            line=token.line,
            column=token.column,
            condition=condition,
            body=body,
            else_body=else_body
        )

    def parse_for(self) -> ForNode:
        """解析循环语句"""
        token = self.advance()  # 循环

        if not self.match(TokenType.IDENTIFIER):
            self.errors.append(f"L{token.line}: 期望循环变量名")
            return None

        var_token = self.advance()
        variable = var_token.value

        # 在/in (可省略，支持中英文)
        if self.current and (self.current.type == TokenType.IN or self.current.value in ("在", "in")):
            self.advance()

        iterable = self.parse_expression()

        self.expect(TokenType.LBRACE, "期望 '{'")
        body = []
        while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE, "期望 '}'")

        return ForNode(
            type="For",
            line=token.line,
            column=token.column,
            variable=variable,
            iterable=iterable,
            body=body
        )

    def parse_while(self) -> WhileNode:
        """解析当循环"""
        token = self.advance()  # 当
        condition = self.parse_expression()

        self.expect(TokenType.LBRACE, "期望 '{'")
        body = []
        while self.current and self.current.type != TokenType.RBRACE and self.current.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE, "期望 '}'")

        return WhileNode(
            type="While",
            line=token.line,
            column=token.column,
            condition=condition,
            body=body
        )

    def parse_import(self) -> ImportNode:
        """解析导入语句"""
        token = self.advance()  # 导入
        if not self.match(TokenType.IDENTIFIER):
            self.errors.append(f"L{token.line}: 期望模块名")
            return None

        module = self.advance().value
        alias = None

        # 检查别名（作为 或 as）
        if self.current and self.current.value in ["作为", "as"]:
            self.advance()
            if self.match(TokenType.IDENTIFIER):
                alias = self.advance().value

        return ImportNode(
            type="Import",
            line=token.line,
            column=token.column,
            module=module,
            alias=alias
        )

    # 数据类型Token集合，用于类型标注解析
    _类型标注Token = {
        TokenType.整数, TokenType.小数, TokenType.文本, TokenType.布尔,
        TokenType.列表, TokenType.字典, TokenType.集合, TokenType.元组,
    }

    def _parse_type_annotation(self) -> Optional[str]:
        """解析类型标注（支持 整数/文本/小数 等类型关键字 + 普通标识符）"""
        if not self.current:
            return None
        if self.current.type in self._类型标注Token or self.match(TokenType.IDENTIFIER):
            return self.advance().value
        return None

    def parse_assign_or_expr(self) -> Optional[ASTNode]:
        """解析赋值或表达式"""
        token = self.current

        if self.match(TokenType.IDENTIFIER):
            # 保存当前解析位置
            saved_pos = self.pos
            name_token = self.advance()
            var_type = None

            # 检查类型标注
            if self.match(TokenType.COLON):
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    var_type = self.advance().value

            if self.match(TokenType.EQUAL):
                self.advance()  # =
                value = self.parse_expression()
                return AssignNode(
                    type="Assign",
                    line=token.line,
                    column=token.column,
                    target=name_token.value,
                    value=value,
                    var_type=var_type
                )
            else:
                # 回退，作为表达式调用
                self.pos = saved_pos
                self._update_current()
                return self.parse_expression()

        return self.parse_expression()

    def parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        """解析逻辑或"""
        left = self.parse_logical_and()
        while self.current and self.current.type == TokenType.OR:
            op_token = self.advance()
            right = self.parse_logical_and()
            left = BinaryOpNode(
                type="BinaryOp",
                line=op_token.line,
                column=op_token.column,
                left=left,
                op="或",
                right=right
            )
        return left

    def parse_logical_and(self) -> ASTNode:
        """解析逻辑与"""
        left = self.parse_comparison()
        while self.current and self.current.type == TokenType.AND:
            op_token = self.advance()
            right = self.parse_comparison()
            left = BinaryOpNode(
                type="BinaryOp",
                line=op_token.line,
                column=op_token.column,
                left=left,
                op="和",
                right=right
            )
        return left

    def parse_comparison(self) -> ASTNode:
        """解析比较运算"""
        left = self.parse_additive()
        comparison_ops = {
            TokenType.EQUAL_EQUAL: "==",
            TokenType.NOT_EQUAL: "!=",
            TokenType.GREATER: ">",
            TokenType.LESS: "<",
            TokenType.GREATER_EQUAL: ">=",
            TokenType.LESS_EQUAL: "<=",
        }
        while self.current and self.current.type in comparison_ops:
            op_token = self.advance()
            right = self.parse_additive()
            left = BinaryOpNode(
                type="BinaryOp",
                line=op_token.line,
                column=op_token.column,
                left=left,
                op=comparison_ops[op_token.type],
                right=right
            )
        return left

    def parse_additive(self) -> ASTNode:
        """解析加减法"""
        left = self.parse_multiplicative()
        while self.current and self.current.type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(
                type="BinaryOp",
                line=op_token.line,
                column=op_token.column,
                left=left,
                op=op_token.value,
                right=right
            )
        return left

    def parse_multiplicative(self) -> ASTNode:
        """解析乘除法（含幂运算 ** 更高优先级）"""
        left = self.parse_unary()
        while self.current and self.current.type in [TokenType.POWER, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MOD]:
            op_token = self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(
                type="BinaryOp",
                line=op_token.line,
                column=op_token.column,
                left=left,
                op=op_token.value,
                right=right
            )
        return left

    def parse_unary(self) -> ASTNode:
        """解析一元运算"""
        if self.current and self.current.type == TokenType.NOT:
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(
                type="UnaryOp",
                line=op_token.line,
                column=op_token.column,
                op="非",
                operand=operand
            )
        if self.current and self.current.value == "-" and self.current.type == TokenType.MINUS:
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(
                type="UnaryOp",
                line=op_token.line,
                column=op_token.column,
                op="-",
                operand=operand
            )
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        if not self.current:
            return None

        token = self.current

        # 数字
        if token.type == TokenType.NUMBER:
            self.advance()
            if '.' in token.value:
                return NumberNode(type="Number", line=token.line, column=token.column, value=float(token.value))
            return NumberNode(type="Number", line=token.line, column=token.column, value=int(token.value))

        # 字符串
        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(type="String", line=token.line, column=token.column, value=token.value)

        # 标识符（含中文类型关键字在表达式中当变量名使用）
        if token.type == TokenType.IDENTIFIER or token.type in self._类型标注Token:
            token_value = token.value
            self.advance()
            # 检查是否为函数调用
            if self.current and self.current.type == TokenType.LPAREN:
                self.advance()  # (
                args = []
                while self.current and self.current.type != TokenType.RPAREN:
                    arg = self.parse_expression()
                    if arg:
                        args.append(arg)
                    if self.current and self.current.type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN, "期望 ')'")
                return CallNode(
                    type="Call",
                    line=token.line,
                    column=token.column,
                    name=token_value,
                    args=args
                )
            return IdentifierNode(type="Identifier", line=token.line, column=token.column, name=token_value)

        # 列表
        if token.type == TokenType.LBRACKET:
            self.advance()  # [
            elements = []
            while self.current and self.current.type != TokenType.RBRACKET:
                elem = self.parse_expression()
                if elem:
                    elements.append(elem)
                if self.current and self.current.type == TokenType.COMMA:
                    self.advance()
            self.expect(TokenType.RBRACKET, "期望 ']'")
            return ListNode(type="List", line=token.line, column=token.column, elements=elements)

        # 字典
        if token.type == TokenType.LBRACE:
            self.advance()  # {
            pairs = []
            while self.current and self.current.type != TokenType.RBRACE:
                key = self.parse_expression()
                if self.current and self.current.type == TokenType.COLON:
                    self.advance()
                    value = self.parse_expression()
                    if key and value:
                        pairs.append((key, value))
                if self.current and self.current.type == TokenType.COMMA:
                    self.advance()
            self.expect(TokenType.RBRACE, "期望 '}'")
            return DictNode(type="Dict", line=token.line, column=token.column, pairs=pairs)

        # 空/真/假
        if token.type in [TokenType.空, TokenType.真, TokenType.假]:
            self.advance()
            return IdentifierNode(type="Identifier", line=token.line, column=token.column, name=token.value)

        # 括号表达式
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "期望 ')'")
            return expr

        self.errors.append(f"L{token.line}:C{token.column}: 意外的Token '{token.value}'")
        self.advance()
        return None


# ============================================================
# 三、语义分析器 (Semantic Analyzer)
# ============================================================

class SemanticAnalyzer:
    """CNSH语义分析器"""

    def __init__(self):
        self.scopes = [{}]  # 作用域栈
        self.errors = []
        self.functions = {}  # 函数定义
        self.current_function = None
        self.has_return = False

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare_variable(self, name: str, var_type: Optional[str] = None):
        if name in self.scopes[-1]:
            self.errors.append(f"变量 '{name}' 已在当前作用域中定义")
        self.scopes[-1][name] = var_type or "任意"

    def lookup_variable(self, name: str) -> Optional[str]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def analyze(self, node: ASTNode) -> bool:
        """执行语义分析"""
        if isinstance(node, ProgramNode):
            return self.analyze_program(node)
        elif isinstance(node, FunctionDefNode):
            return self.analyze_function_def(node)
        elif isinstance(node, ReturnNode):
            return self.analyze_return(node)
        elif isinstance(node, IfNode):
            return self.analyze_if(node)
        elif isinstance(node, ForNode):
            return self.analyze_for(node)
        elif isinstance(node, WhileNode):
            return self.analyze_while(node)
        elif isinstance(node, AssignNode):
            return self.analyze_assign(node)
        elif isinstance(node, CallNode):
            return self.analyze_call(node)
        elif isinstance(node, BinaryOpNode):
            return self.analyze_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.analyze_unary_op(node)
        elif isinstance(node, IdentifierNode):
            return self.analyze_identifier(node)
        elif isinstance(node, ImportNode):
            return True
        elif isinstance(node, BreakNode):
            return True
        elif isinstance(node, ContinueNode):
            return True
        return True

    def analyze_program(self, node: ProgramNode) -> bool:
        ok = True
        for stmt in node.statements:
            if not self.analyze(stmt):
                ok = False
        return ok

    def analyze_function_def(self, node: FunctionDefNode) -> bool:
        self.functions[node.name] = node
        self.enter_scope()
        self.current_function = node.name
        self.has_return = False

        for param_name, param_type in node.params:
            self.declare_variable(param_name, param_type)

        for stmt in node.body:
            self.analyze(stmt)

        self.exit_scope()
        self.current_function = None
        return True

    def analyze_return(self, node: ReturnNode) -> bool:
        self.has_return = True
        if node.value:
            return self.analyze(node.value)
        return True

    def analyze_if(self, node: IfNode) -> bool:
        ok = True
        if node.condition:
            ok = self.analyze(node.condition) and ok
        self.enter_scope()
        for stmt in node.body:
            if not self.analyze(stmt):
                ok = False
        self.exit_scope()

        if node.else_body:
            self.enter_scope()
            for stmt in node.else_body:
                if not self.analyze(stmt):
                    ok = False
            self.exit_scope()

        return ok

    def analyze_for(self, node: ForNode) -> bool:
        ok = True
        self.enter_scope()
        self.declare_variable(node.variable)
        if node.iterable:
            ok = self.analyze(node.iterable) and ok
        for stmt in node.body:
            if not self.analyze(stmt):
                ok = False
        self.exit_scope()
        return ok

    def analyze_while(self, node: WhileNode) -> bool:
        ok = True
        if node.condition:
            ok = self.analyze(node.condition) and ok
        for stmt in node.body:
            if not self.analyze(stmt):
                ok = False
        return ok

    def analyze_assign(self, node: AssignNode) -> bool:
        self.declare_variable(node.target, node.var_type)
        if node.value:
            return self.analyze(node.value)
        return True

    def analyze_call(self, node: CallNode) -> bool:
        builtins = ["打印", "输入", "长度", "类型", "范围"]
        if node.name not in builtins and node.name not in self.functions:
            self.errors.append(f"函数 '{node.name}' 未定义")
            return False
        for arg in node.args:
            if not self.analyze(arg):
                return False
        return True

    def analyze_binary_op(self, node: BinaryOpNode) -> bool:
        ok = True
        if node.left:
            ok = self.analyze(node.left) and ok
        if node.right:
            ok = self.analyze(node.right) and ok
        return ok

    def analyze_unary_op(self, node: UnaryOpNode) -> bool:
        if node.operand:
            return self.analyze(node.operand)
        return True

    def analyze_identifier(self, node: IdentifierNode) -> bool:
        if node.name not in ["空", "真", "假"]:
            var_type = self.lookup_variable(node.name)
            if var_type is None and node.name not in self.functions:
                self.errors.append(f"未定义的变量 '{node.name}'")
                return False
        return True


# ============================================================
# 四、代码生成器 (Code Generator)
# ============================================================

class CodeGenerator:
    """CNSH代码生成器 - 生成Python代码"""

    def __init__(self, filename: str = "<stdin>"):
        self.filename = filename
        self.indent_level = 0
        self.code_lines = []
        self.indent_str = "    "
        self.builtin_functions = {"打印": "print", "输入": "input", "长度": "len", "类型": "type", "范围": "range"}

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1
        if self.indent_level < 0:
            self.indent_level = 0

    def add_line(self, line: str):
        if line.strip():
            self.code_lines.append(self.indent_str * self.indent_level + line)
        else:
            self.code_lines.append(line)

    def generate(self, node: ASTNode) -> str:
        """生成Python代码"""
        self.code_lines = []

        # 添加头部
        self.add_line("# 由CNSH编译器自动生成")
        if isinstance(node, ProgramNode):
            self.add_line("# DNA: " + (node.dna or "未指定"))
            self.add_line("# 确认码: " + (node.confirm or "未指定"))
        self.add_line("import sys")
        self.add_line("import math")
        self.add_line("import json")
        self.add_line("import hashlib")
        self.add_line("from datetime import datetime")
        self.add_line("")

        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self._generate_node(stmt)

        return "\n".join(self.code_lines)

    def _generate_node(self, node: ASTNode):
        """递归生成代码"""
        if isinstance(node, FunctionDefNode):
            self._generate_function_def(node)
        elif isinstance(node, ReturnNode):
            self._generate_return(node)
        elif isinstance(node, IfNode):
            self._generate_if(node)
        elif isinstance(node, ForNode):
            self._generate_for(node)
        elif isinstance(node, WhileNode):
            self._generate_while(node)
        elif isinstance(node, BreakNode):
            self.add_line("break")
        elif isinstance(node, ContinueNode):
            self.add_line("continue")
        elif isinstance(node, ImportNode):
            self._generate_import(node)
        elif isinstance(node, AssignNode):
            self._generate_assign(node)
        elif isinstance(node, CallNode):
            self.add_line(self._generate_expr(node))
        else:
            expr = self._generate_expr(node)
            if expr:
                self.add_line(expr)

    def _generate_function_def(self, node: FunctionDefNode):
        """生成函数定义"""
        params = [p[0] for p in node.params]
        params_str = ", ".join(params)

        self.add_line(f"def {node.name}({params_str}):")
        self.indent()
        for stmt in node.body:
            self._generate_node(stmt)
        self.dedent()
        self.add_line("")

    def _generate_return(self, node: ReturnNode):
        if node.value:
            expr = self._generate_expr(node.value)
            self.add_line(f"return {expr}")
        else:
            self.add_line("return")

    def _generate_if(self, node: IfNode):
        cond = self._generate_expr(node.condition)
        self.add_line(f"if {cond}:")
        self.indent()
        for stmt in node.body:
            self._generate_node(stmt)
        self.dedent()

        if node.else_body:
            # 处理否则如果链（嵌套的IfNode）+ 否则块
            for stmt in node.else_body:
                if isinstance(stmt, IfNode):
                    self.add_line(f"elif {self._generate_expr(stmt.condition)}:")
                    self.indent()
                    for s in stmt.body:
                        self._generate_node(s)
                    self.dedent()
                else:
                    self.add_line("else:")
                    self.indent()
                    self._generate_node(stmt)
                    self.dedent()

    def _generate_for(self, node: ForNode):
        iterable = self._generate_expr(node.iterable)
        self.add_line(f"for {node.variable} in {iterable}:")
        self.indent()
        for stmt in node.body:
            self._generate_node(stmt)
        self.dedent()

    def _generate_while(self, node: WhileNode):
        cond = self._generate_expr(node.condition)
        self.add_line(f"while {cond}:")
        self.indent()
        for stmt in node.body:
            self._generate_node(stmt)
        self.dedent()

    def _generate_import(self, node: ImportNode):
        if node.alias:
            self.add_line(f"import {node.module} as {node.alias}")
        else:
            self.add_line(f"import {node.module}")

    def _generate_assign(self, node: AssignNode):
        value = self._generate_expr(node.value)
        self.add_line(f"{node.target} = {value}")

    def _generate_expr(self, node: ASTNode) -> str:
        """生成表达式代码"""
        if node is None:
            return "None"
        if isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, StringNode):
            return f'"{node.value}"'
        elif isinstance(node, IdentifierNode):
            value_map = {"空": "None", "真": "True", "假": "False"}
            return value_map.get(node.name, node.name)
        elif isinstance(node, BinaryOpNode):
            left = self._generate_expr(node.left)
            right = self._generate_expr(node.right)
            op_map = {"和": " and ", "或": " or "}
            if node.op in op_map:
                return f"{left}{op_map[node.op]}{right}"
            return f"{left} {node.op} {right}"
        elif isinstance(node, UnaryOpNode):
            operand = self._generate_expr(node.operand)
            op_map = {"非": "not ", "-": "-"}
            return f"{op_map.get(node.op, '')}{operand}"
        elif isinstance(node, CallNode):
            args = [self._generate_expr(arg) for arg in node.args]
            func_name = self.builtin_functions.get(node.name, node.name)
            return f"{func_name}({', '.join(args)})"
        elif isinstance(node, ListNode):
            elements = [self._generate_expr(elem) for elem in node.elements]
            return f"[{', '.join(elements)}]"
        elif isinstance(node, DictNode):
            pairs = [f"{self._generate_expr(k)}: {self._generate_expr(v)}" for k, v in node.pairs]
            return f"{{{', '.join(pairs)}}}"
        elif isinstance(node, AttributeNode):
            obj = self._generate_expr(node.obj)
            return f"{obj}.{node.attr}"
        else:
            return ""


# ============================================================
# 五、编译器主控 (Compiler)
# ============================================================

class CNSHCompiler:
    """CNSH编译器主控"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.tokens = []
        self.ast = None
        self.python_code = ""

    def compile(self, source: str, filename: str = "<stdin>") -> Dict[str, Any]:
        """编译CNSH源代码"""
        self.errors = []
        self.warnings = []

        # 步骤1: 词法分析
        lexer = Lexer(source, filename)
        self.tokens = lexer.tokenize()
        self.errors.extend(lexer.errors)

        if self.errors:
            return {"success": False, "errors": self.errors}

        # 步骤2: 语法分析
        parser = Parser(self.tokens)
        self.ast = parser.parse()
        self.errors.extend(parser.errors)

        if self.errors:
            return {"success": False, "errors": self.errors}

        # 步骤3: 语义分析
        semantic = SemanticAnalyzer()
        semantic.analyze(self.ast)
        self.errors.extend(semantic.errors)

        if self.errors:
            return {"success": False, "errors": self.errors}

        # 步骤4: 代码生成
        generator = CodeGenerator(filename)
        self.python_code = generator.generate(self.ast)

        return {
            "success": True,
            "errors": [],
            "tokens": self.tokens,
            "ast": self.ast,
            "python_code": self.python_code
        }

    def compile_file(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """编译CNSH文件"""
        input_path = Path(input_path)
        if not input_path.exists():
            return {"success": False, "errors": [f"文件不存在: {input_path}"]}

        with open(input_path, 'r', encoding='utf-8') as f:
            source = f.read()

        result = self.compile(source, str(input_path))

        if result["success"] and output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result["python_code"])
            result["output_path"] = str(output_path)

        return result

    def run(self, source: str, filename: str = "<stdin>") -> Dict[str, Any]:
        """编译并执行CNSH代码"""
        result = self.compile(source, filename)
        if not result["success"]:
            return result

        # 执行生成的Python代码
        try:
            exec_globals = {
                "__name__": "__main__",
                "__file__": filename,
                "sys": sys,
                "math": __import__('math'),
                "json": __import__('json'),
                "hashlib": __import__('hashlib'),
                "datetime": __import__('datetime'),
            }
            exec(result["python_code"], exec_globals)
            result["execution"] = "success"
        except Exception as e:
            result["execution"] = "error"
            result["execution_error"] = str(e)
            result["execution_traceback"] = traceback.format_exc()

        return result


# ============================================================
# 六、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·CNSH编译器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 编译CNSH文件
  python3 cnsh_compiler.py -i 脚本.cnsh -o 脚本.py

  # 直接编译并运行
  python3 cnsh_compiler.py -i 脚本.cnsh --run

  # 显示Token流
  python3 cnsh_compiler.py -i 脚本.cnsh --tokens

  # 显示AST
  python3 cnsh_compiler.py -i 脚本.cnsh --ast

  # 交互式REPL
  python3 cnsh_compiler.py --repl
        """
    )

    parser.add_argument(
        "-i", "--input",
        type=str,
        help="输入CNSH源文件 (.cnsh)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="输出Python文件 (.py)"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="编译后立即执行"
    )
    parser.add_argument(
        "--tokens",
        action="store_true",
        help="显示Token流"
    )
    parser.add_argument(
        "--ast",
        action="store_true",
        help="显示AST结构"
    )
    parser.add_argument(
        "--repl",
        action="store_true",
        help="启动交互式REPL"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="显示版本信息"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="CNSH源文件（快捷方式）"
    )

    args = parser.parse_args()

    if args.version:
        print("🐉 CNSH编译器 v1.0")
        print("DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-CNSH编译器-v1.0")
        print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        return

    compiler = CNSHCompiler()

    # REPL模式
    if args.repl:
        print("🐉 CNSH交互式REPL v1.0")
        print("输入CNSH代码，按 Ctrl+D (或输入 'exit') 退出")
        print("-" * 40)
        buffer = []
        while True:
            try:
                line = input("CNSH> ")
                if line.strip().lower() in ('exit', 'quit', 'q'):
                    break
                buffer.append(line)
                if line.strip().endswith('}'):
                    source = "\n".join(buffer)
                    result = compiler.run(source, "<repl>")
                    if result["success"]:
                        print("✅ 执行成功")
                    else:
                        for err in result.get("errors", []):
                            print(f"❌ {err}")
                    buffer = []
            except EOFError:
                break
            except KeyboardInterrupt:
                print("")
                continue
        return

    # 文件模式
    input_file = args.input or args.file
    if not input_file:
        parser.print_help()
        return

    # 编译
    if args.output:
        result = compiler.compile_file(input_file, args.output)
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        result = compiler.compile(source, input_file)

    if not result["success"]:
        print("❌ 编译失败:")
        for err in result.get("errors", []):
            print(f"  {err}")
        sys.exit(1)

    # 显示Token流
    if args.tokens and "tokens" in result:
        print("\n📜 Token流:")
        for token in result["tokens"][:50]:
            print(f"  {token}")
        if len(result["tokens"]) > 50:
            print(f"  ... 还有 {len(result['tokens']) - 50} 个Token")

    # 显示AST
    if args.ast and "ast" in result:
        print("\n🌳 AST:")
        print(result["ast"])

    # 运行
    if args.run:
        print("\n🚀 执行结果:")
        exec_globals = {
            "__name__": "__main__",
            "__file__": input_file,
            "sys": sys,
            "math": __import__('math'),
            "json": __import__('json'),
            "hashlib": __import__('hashlib'),
            "datetime": __import__('datetime'),
        }
        try:
            exec(result["python_code"], exec_globals)
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            traceback.print_exc()
    elif args.output:
        print(f"✅ 编译成功: {args.output}")
    else:
        print("✅ 编译成功")
        print("-" * 40)
        print(result["python_code"])


if __name__ == "__main__":
    main()
