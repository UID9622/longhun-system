# -*- coding: utf-8 -*-
"""
CNSH v2.1 Token 定义
DNA: #龍芯⚡️2026-06-29-CNSH-TOKENS-v2.1
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    line: int
    column: int
    file: Optional[str] = None

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r}, L{self.line}, C{self.column})"


# Token 类型常量
TOKEN_TYPES = {
    # 字面量
    "NUMBER": "NUMBER",
    "STRING": "STRING",
    "BOOLEAN": "BOOLEAN",
    "NULL": "NULL",
    # 关键字
    "KEYWORD": "KEYWORD",
    # 标识符
    "IDENTIFIER": "IDENTIFIER",
    # 运算符
    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "STAR": "STAR",
    "SLASH": "SLASH",
    "PERCENT": "PERCENT",
    "ASSIGN": "ASSIGN",
    "EQ": "EQ",
    "NE": "NE",
    "LT": "LT",
    "GT": "GT",
    "LE": "LE",
    "GE": "GE",
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",
    # 标点
    "LPAREN": "LPAREN",
    "RPAREN": "RPAREN",
    "LBRACE": "LBRACE",
    "RBRACE": "RBRACE",
    "LBRACKET": "LBRACKET",
    "RBRACKET": "RBRACKET",
    "COMMA": "COMMA",
    "SEMICOLON": "SEMICOLON",
    "COLON": "COLON",
    "DOT": "DOT",
    "WEIGHT": "WEIGHT",
    "ARROW": "ARROW",
    "AT": "AT",
    "NEWLINE": "NEWLINE",
    "EOF": "EOF",
    "COMMENT": "COMMENT",
    "DNA_COMMENT": "DNA_COMMENT",
    # 新增关键字类型
    "CLASS": "CLASS",
    "DEF": "DEF",
    "SELF": "SELF",
    "SUPER": "SUPER",
    "YIELD": "YIELD",
    "YIELD_FROM": "YIELD_FROM",
    "ASYNC": "ASYNC",
    "AWAIT": "AWAIT",
    "WITH": "WITH",
    "AS": "AS",
    "TRY": "TRY",
    "EXCEPT": "EXCEPT",
    "FINALLY": "FINALLY",
    "RAISE": "RAISE",
    "PASS": "PASS",
    "IMPORT": "IMPORT",
    "FROM": "FROM",
    "ENUM": "ENUM",
    "UNIQUE": "UNIQUE",
    "DATACLASS": "DATACLASS",
    "FIELD": "FIELD",
    "DEFAULT_FACTORY": "DEFAULT_FACTORY",
    "PROPERTY": "PROPERTY",
    "CLASSMETHOD": "CLASSMETHOD",
    "STATICMETHOD": "STATICMETHOD",
    "ABSTRACTMETHOD": "ABSTRACTMETHOD",
    # Bra-Ket 人格协作关键字
    "PERSONA_BASIS": "PERSONA_BASIS",
    "SYSTEM": "SYSTEM",
}


# 关键字映射
KEYWORDS = {
    "模块": "MODULE",
    "函数": "FUNCTION",
    "定义": "DEF",
    "类": "CLASS",
    "自己": "SELF",
    "超类": "SUPER",
    "变量": "VAR",
    "常量": "CONST",
    "结构体": "STRUCT",
    "返回": "RETURN",
    "如果": "IF",
    "否则如果": "ELIF",
    "否则": "ELSE",
    "循环": "LOOP",
    "当": "WHILE",
    "对于": "FOR",
    "异步": "ASYNC",
    "等待": "AWAIT",
    "中断": "BREAK",
    "继续": "CONTINUE",
    "使用": "WITH",
    "作为": "AS",
    "导入": "IMPORT",
    "从": "FROM",
    "尝试": "TRY",
    "捕获": "EXCEPT",
    "最终": "FINALLY",
    "抛出": "RAISE",
    "通过": "PASS",
    "产生": "YIELD",
    "产生于": "YIELD_FROM",
    "真": "TRUE",
    "假": "FALSE",
    "空": "NULL",
    # 龍魂专属装饰器/类型关键字
    "枚举类": "ENUM",
    "枚举唯一": "UNIQUE",
    "数据类": "DATACLASS",
    "字段": "FIELD",
    "默认工厂": "DEFAULT_FACTORY",
    "属性": "PROPERTY",
    "类方法": "CLASSMETHOD",
    "静态方法": "STATICMETHOD",
    "抽象方法": "ABSTRACTMETHOD",
    # Bra-Ket 人格协作关键字
    "人格基态": "PERSONA_BASIS",
    "系统": "SYSTEM",
    # 中文运算符别名
    "且": "AND",
    "或": "OR",
    "非": "NOT",
}


# 运算符字符映射
OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "%": "PERCENT",
    "=": "ASSIGN",
    "==": "EQ",
    "!=": "NE",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
    "&&": "AND",
    "||": "OR",
    "!": "NOT",
    "->": "ARROW",
}


# 单字符标点
PUNCTUATION = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ",": "COMMA",
    ";": "SEMICOLON",
    ":": "COLON",
    ".": "DOT",
    "@": "AT",
}
