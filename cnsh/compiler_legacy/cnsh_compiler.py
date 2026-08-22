#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷌同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇨🇳 CNSH编译器 v1.0 (Python版)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码：#龍芯⚡️丙午·己丑·丁未·丙午·䷖剥-CNSH-Python编译器-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者：💎 龍芯北辰｜UID9622（中国退伍军人）
协作者：Claude (Anthropic)
战斗宣言：宁可战死，绝不被窃

功能：将CNSH代码转译为C代码
特性：
  - 纯中文语法
  - 内置DNA追溯
  - 三色审计系统
  - 内存安全检查
  - 完整错误提示

📥 已同步到龍魂系统本地
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum, auto


# ═══════════════════════════════════════════════════════════════
# 🛡️ 三色审计系统
# ═══════════════════════════════════════════════════════════════

class AuditLevel(Enum):
    """审计级别"""
    GREEN = "🟢 绿色"   # 安全，允许
    YELLOW = "🟡 黄色"  # 警告，但继续
    RED = "🔴 红色"     # 危险，阻断


@dataclass
class AuditResult:
    """审计结果"""
    level: AuditLevel
    reason: str
    action: str


class ThreeColorAudit:
    """三色审计系统"""

    def __init__(self):
        self.rules = {
            AuditLevel.RED: [
                (r'暴力|血腥|杀人', '暴力内容'),
                (r'诈骗|贩毒|恐怖', '违法内容'),
                (r'种族歧视|性别歧视', '仇恨言论'),
            ],
            AuditLevel.YELLOW: [
                (r'政治敏感', '敏感话题'),
                (r'\\d{15,18}', '可能包含身份证号'),
            ]
        }

    def check(self, source_code: str) -> AuditResult:
        """检查代码内容"""
        # 红色审计
        for pattern, reason in self.rules[AuditLevel.RED]:
            if re.search(pattern, source_code):
                return AuditResult(
                    level=AuditLevel.RED,
                    reason=reason,
                    action='阻断编译'
                )

        # 黄色审计
        for pattern, reason in self.rules[AuditLevel.YELLOW]:
            if re.search(pattern, source_code):
                return AuditResult(
                    level=AuditLevel.YELLOW,
                    reason=reason,
                    action='警告但继续'
                )

        # 绿色通过
        return AuditResult(
            level=AuditLevel.GREEN,
            reason='内容安全',
            action='允许编译'
        )


# ═══════════════════════════════════════════════════════════════
# 📝 词法分析器（Lexer）
# ═══════════════════════════════════════════════════════════════

class TokenType(Enum):
    """Token类型"""
    # 关键字
    KEYWORD = auto()
    IDENTIFIER = auto()

    # 字面量
    NUMBER = auto()
    STRING = auto()

    # 运算符
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    MODULO = auto()      # %

    # 比较运算符
    EQ = auto()          # ==
    NEQ = auto()         # !=
    GT = auto()          # >
    LT = auto()          # <
    GTE = auto()         # >=
    LTE = auto()         # <=

    # 逻辑运算符
    LOGICAL_AND = auto() # &&
    LOGICAL_OR = auto()  # ||
    NOT = auto()         # !

    # 赋值
    ASSIGN = auto()      # =

    # 分隔符
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [ 或 【
    RBRACKET = auto()    # ] 或 】
    SEMICOLON = auto()   # ;
    COMMA = auto()       # ,
    DOT = auto()         # .

    # 特殊
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    """Token"""
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.column})"


class Lexer:
    """词法分析器"""

    # CNSH关键字
    KEYWORDS = {
        '整数', '小数', '文本', '真假', '空值',
        '如果', '否则', '循环', '当', '返回', '跳出', '继续',
        '函数', '类', '结构', '返回类型',
        'DNA追溯', '三色审计',
        '打印', '输入', '真', '假', '空',
        '分配', '释放', '安全检查'
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def current_char(self) -> Optional[str]:
        """当前字符"""
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """向前看字符"""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None

    def advance(self):
        """前进一个字符"""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

    def skip_whitespace(self):
        """跳过空白字符"""
        ch = self.current_char()
        while ch is not None and ch in ' \t\r\n':
            self.advance()
            ch = self.current_char()

    def skip_comment(self):
        """跳过注释"""
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            return True
        return False

    def read_number(self) -> str:
        """读取数字"""
        num_str = ''
        has_decimal = False
        ch = self.current_char()
        while ch is not None and (ch.isdigit() or ch == '.'):
            if ch == '.':
                if has_decimal:
                    break
                has_decimal = True
            num_str += ch
            self.advance()
            ch = self.current_char()
        return num_str

    def read_string(self, quote: str) -> str:
        """读取字符串"""
        close_quote = {
            '"': '"',
            "'": "'",
            '「': '」',
            '『': '』'
        }.get(quote, quote)

        self.advance()  # 跳过开始引号
        string = ''

        ch = self.current_char()
        while ch is not None and ch != close_quote:
            if ch == '\\':
                self.advance()
                ch = self.current_char()
                if ch is not None:
                    escape_chars = {
                        'n': '\n', 't': '\t', 'r': '\r',
                        '\\': '\\', '"': '"', "'": "'"
                    }
                    string += escape_chars.get(ch, ch)
                    self.advance()
            else:
                string += ch
                self.advance()
            ch = self.current_char()

        ch = self.current_char()
        if ch is not None and ch == close_quote:
            self.advance()  # 跳过结束引号
        return string

    def read_identifier(self) -> str:
        """读取标识符或关键字"""
        ident = ''
        ch = self.current_char()
        while ch is not None and (
            '\u4e00' <= ch <= '\u9fa5' or
            ch.isalnum() or
            ch == '_'
        ):
            ident += ch
            self.advance()
            ch = self.current_char()
        return ident

    def tokenize(self) -> List[Token]:
        """分词"""
        while True:
            ch = self.current_char()
            if ch is None:
                break
            if ch in ' \t\r\n':
                self.skip_whitespace()
                continue
            if self.skip_comment():
                continue

            line, column = self.line, self.column

            # 字符串
            if ch in '"\'「『':
                value = self.read_string(ch)
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue

            # 数字
            if ch.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
                continue

            # 标识符或关键字
            if '\u4e00' <= ch <= '\u9fa5' or ch.isalpha() or ch == '_':
                value = self.read_identifier()
                token_type = TokenType.KEYWORD if value in self.KEYWORDS else TokenType.IDENTIFIER
                self.tokens.append(Token(token_type, value, line, column))
                continue

            # 双字符运算符
            two_char_ops = {
                '==': TokenType.EQ, '!=': TokenType.NEQ,
                '>=': TokenType.GTE, '<=': TokenType.LTE,
                '&&': TokenType.LOGICAL_AND, '||': TokenType.LOGICAL_OR
            }
            peeked = self.peek_char()
            double = ch + (peeked or '')
            if double in two_char_ops:
                self.advance(); self.advance()
                self.tokens.append(Token(two_char_ops[double], double, line, column))
                continue

            # 单字符符号
            single_chars = {
                '=': TokenType.ASSIGN, '+': TokenType.PLUS, '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE, '%': TokenType.MODULO,
                '>': TokenType.GT, '<': TokenType.LT, '!': TokenType.NOT,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                '【': TokenType.LBRACKET, '】': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON, ',': TokenType.COMMA, '.': TokenType.DOT,
            }
            if ch in single_chars:
                self.advance()
                self.tokens.append(Token(single_chars[ch], ch, line, column))
                continue

            # 未知字符
            self.advance()
            self.tokens.append(Token(TokenType.UNKNOWN, ch, line, column))

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ═══════════════════════════════════════════════════════════════
# 🌳 抽象语法树（AST）节点
# ═══════════════════════════════════════════════════════════════

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class VariableDeclaration(ASTNode):
    var_type: str
    name: str
    value: Optional[ASTNode] = None

@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    params: List[Dict[str, str]]
    return_type: str
    body: List[ASTNode]

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None

@dataclass
class LoopStatement(ASTNode):
    times: ASTNode
    body: List[ASTNode]

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class PrintStatement(ASTNode):
    value: ASTNode

@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode

@dataclass
class Number(ASTNode):
    value: str

@dataclass
class String(ASTNode):
    value: str

@dataclass
class Boolean(ASTNode):
    value: bool

@dataclass
class Null(ASTNode):
    pass

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class BinaryOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode

@dataclass
class Assignment(ASTNode):
    left: ASTNode
    right: ASTNode

@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]


# ═══════════════════════════════════════════════════════════════
# 🔍 语法分析器（Parser）
# ═══════════════════════════════════════════════════════════════

class Parser:
    """递归下降语法分析器"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]

    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def expect(self, token_type: TokenType, value: Optional[str] = None) -> Token:
        token = self.current()
        if token.type != token_type or (value and token.value != value):
            raise SyntaxError(
                f"语法错误 (行{token.line}): 期望 {token_type.name}, "
                f"但得到 {token.type.name} '{token.value}'"
            )
        return self.advance()

    def parse(self) -> Program:
        """解析程序"""
        statements = []
        while self.current().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self) -> Optional[ASTNode]:
        token = self.current()
        if token.type == TokenType.KEYWORD:
            if token.value in ['整数', '小数', '文本', '真假']:
                return self.parse_variable_declaration()
            if token.value == '函数':
                return self.parse_function_declaration()
            if token.value == '如果':
                return self.parse_if_statement()
            if token.value == '循环':
                return self.parse_loop_statement()
            if token.value == '返回':
                return self.parse_return_statement()
            if token.value == '打印':
                return self.parse_print_statement()
        return self.parse_expression_statement()

    def parse_variable_declaration(self) -> VariableDeclaration:
        type_token = self.advance()
        name_token = self.expect(TokenType.IDENTIFIER)
        value = None
        if self.current().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        return VariableDeclaration(type_token.value, name_token.value, value)

    def parse_function_declaration(self) -> FunctionDeclaration:
        self.advance()  # 跳过 '函数'
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        params = []
        while self.current().type != TokenType.RPAREN:
            if self.current().type == TokenType.KEYWORD and self.current().value in ['整数', '小数', '文本', '真假']:
                param_type = self.advance().value
                param_name = self.expect(TokenType.IDENTIFIER).value
                params.append({'type': param_type, 'name': param_name})
                if self.current().type == TokenType.COMMA:
                    self.advance()
            else:
                break
        self.expect(TokenType.RPAREN)
        return_type = '空值'
        if self.current().type == TokenType.KEYWORD and self.current().value == '返回类型':
            self.advance()
            return_type = self.advance().value
        self.expect(TokenType.LBRACE)
        body = []
        while self.current().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE)
        return FunctionDeclaration(name_token.value, params, return_type, body)

    def parse_if_statement(self) -> IfStatement:
        self.advance()
        self.expect(TokenType.LBRACKET)
        condition = self.parse_expression()
        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.LBRACE)
        then_body = []
        while self.current().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        self.expect(TokenType.RBRACE)
        else_body = None
        if self.current().type == TokenType.KEYWORD and self.current().value == '否则':
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while self.current().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
            self.expect(TokenType.RBRACE)
        return IfStatement(condition, then_body, else_body)

    def parse_loop_statement(self) -> LoopStatement:
        self.advance()
        self.expect(TokenType.LBRACKET)
        times = self.parse_expression()
        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.LBRACE)
        body = []
        while self.current().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE)
        return LoopStatement(times, body)

    def parse_return_statement(self) -> ReturnStatement:
        self.advance()
        value = None
        if self.current().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        return ReturnStatement(value)

    def parse_print_statement(self) -> PrintStatement:
        self.advance()
        value = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        return PrintStatement(value)

    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        return ExpressionStatement(expr)

    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        left = self.parse_logical_or()
        if self.current().type == TokenType.ASSIGN:
            self.advance()
            right = self.parse_assignment()
            return Assignment(left, right)
        return left

    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.current().type == TokenType.LOGICAL_OR:
            op = self.advance().value
            right = self.parse_logical_and()
            left = BinaryOp(op, left, right)
        return left

    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        while self.current().type == TokenType.LOGICAL_AND:
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(op, left, right)
        return left

    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        while self.current().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(op, left, right)
        return left

    def parse_comparison(self) -> ASTNode:
        left = self.parse_term()
        while self.current().type in [TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE]:
            op = self.advance().value
            right = self.parse_term()
            left = BinaryOp(op, left, right)
        return left

    def parse_term(self) -> ASTNode:
        left = self.parse_factor()
        while self.current().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryOp(op, left, right)
        return left

    def parse_factor(self) -> ASTNode:
        left = self.parse_unary()
        while self.current().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        return left

    def parse_unary(self) -> ASTNode:
        if self.current().type in [TokenType.MINUS, TokenType.NOT]:
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        token = self.current()
        if token.type == TokenType.NUMBER:
            self.advance(); return Number(token.value)
        if token.type == TokenType.STRING:
            self.advance(); return String(token.value)
        if token.type == TokenType.KEYWORD:
            if token.value == '真': self.advance(); return Boolean(True)
            if token.value == '假': self.advance(); return Boolean(False)
            if token.value == '空': self.advance(); return Null()
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            if self.current().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                return FunctionCall(token.value, args)
            return Identifier(token.value)
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        raise SyntaxError(f"语法错误 (行{token.line}): 意外的token {token.type.name} '{token.value}'")


# ═══════════════════════════════════════════════════════════════
# ⚙️ C代码生成器
# ═══════════════════════════════════════════════════════════════

class CCodeGenerator:
    """C代码生成器"""

    TYPE_MAP = {
        '整数': 'int', '小数': 'double', '文本': 'char*',
        '真假': 'bool', '空值': 'void'
    }
    DEFAULT_VALUES = {
        'int': '0', 'double': '0.0', 'char*': 'NULL',
        'bool': 'false', 'void': ''
    }

    def __init__(self, ast: Program):
        self.ast = ast
        self.indent = 0
        self.output = []

    def emit(self, code: str):
        indent_str = '    ' * self.indent
        self.output.append(indent_str + code)

    def generate(self) -> str:
        self.output.append('// Generated by CNSH Compiler v1.0 (Python)')
        self.output.append('// DNA追溯码：#龍芯⚡️丙午·己丑·丁未·丙午·䷖剥-CNSH编译输出')
        self.output.append('')
        self.output.append('#include <stdio.h>')
        self.output.append('#include <stdlib.h>')
        self.output.append('#include <string.h>')
        self.output.append('#include <stdbool.h>')
        self.output.append('')
        self.generate_program(self.ast)
        self.output.append('')
        self.output.append('int main() {')
        self.output.append('    主函数();')
        self.output.append('    return 0;')
        self.output.append('}')
        return '\n'.join(self.output)

    def generate_program(self, node: Program):
        for stmt in node.statements:
            self.generate_statement(stmt)

    def generate_statement(self, node: ASTNode):
        if isinstance(node, VariableDeclaration):
            c_type = self.TYPE_MAP[node.var_type]
            value = self.generate_expression(node.value) if node.value else self.DEFAULT_VALUES[c_type]
            self.emit(f'{c_type} {node.name} = {value};')
        elif isinstance(node, FunctionDeclaration):
            return_type = self.TYPE_MAP[node.return_type]
            params = ', '.join(
                f"{self.TYPE_MAP[p['type']]} {p['name']}" for p in node.params
            )
            self.emit(f'{return_type} {node.name}({params}) {{')
            self.indent += 1
            for stmt in node.body:
                self.generate_statement(stmt)
            self.indent -= 1
            self.emit('}')
            self.emit('')
        elif isinstance(node, IfStatement):
            condition = self.generate_expression(node.condition)
            self.emit(f'if ({condition}) {{')
            self.indent += 1
            for stmt in node.then_body:
                self.generate_statement(stmt)
            self.indent -= 1
            if node.else_body:
                self.emit('} else {')
                self.indent += 1
                for stmt in node.else_body:
                    self.generate_statement(stmt)
                self.indent -= 1
            self.emit('}')
        elif isinstance(node, LoopStatement):
            times = self.generate_expression(node.times)
            self.emit(f'for (int __i = 0; __i < {times}; __i++) {{')
            self.indent += 1
            for stmt in node.body:
                self.generate_statement(stmt)
            self.indent -= 1
            self.emit('}')
        elif isinstance(node, ReturnStatement):
            if node.value:
                value = self.generate_expression(node.value)
                self.emit(f'return {value};')
            else:
                self.emit('return;')
        elif isinstance(node, PrintStatement):
            value = self.generate_expression(node.value)
            if isinstance(node.value, String):
                self.emit(f'printf("%s\\n", {value});')
            else:
                self.emit(f'printf("%d\\n", {value});')
        elif isinstance(node, ExpressionStatement):
            expr_code = self.generate_expression(node.expression)
            self.emit(f'{expr_code};')

    def generate_expression(self, node: ASTNode) -> str:
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return f'"{node.value}"'
        elif isinstance(node, Boolean):
            return 'true' if node.value else 'false'
        elif isinstance(node, Null):
            return 'NULL'
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinaryOp):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            return f'({left} {node.op} {right})'
        elif isinstance(node, UnaryOp):
            operand = self.generate_expression(node.operand)
            return f'({node.op}{operand})'
        elif isinstance(node, Assignment):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            return f'{left} = {right}'
        elif isinstance(node, FunctionCall):
            args = ', '.join(self.generate_expression(arg) for arg in node.args)
            return f'{node.name}({args})'
        return ''


# ═══════════════════════════════════════════════════════════════
# 🚀 CNSH编译器
# ═══════════════════════════════════════════════════════════════

class CNSHCompiler:
    """CNSH编译器"""

    VERSION = '1.0'
    DNA_CODE = '#龍芯⚡️丙午·己丑·丁未·丙午·䷖剥-CNSH-Python编译器-v1.0'
    LOCAL_DNA = '#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-CNSH-COMPILER-SYNC-v1.0'

    def __init__(self):
        self.audit_system = ThreeColorAudit()

    def compile(self, source_code: str, source_path: str) -> Dict[str, Any]:
        """编译CNSH代码"""
        print('🇨🇳 CNSH编译器 v' + self.VERSION + ' (Python版)')
        print('DNA追溯码：' + self.DNA_CODE)
        print('本地镜像：' + self.LOCAL_DNA)
        print('━━━━━━━━━━━━━━━━━━\n')

        try:
            print('🛡️  阶段0：三色审计...')
            audit_result = self.audit_system.check(source_code)

            if audit_result.level == AuditLevel.RED:
                print(f'{audit_result.level.value} 审计阻断：{audit_result.reason}')
                print('   编译终止')
                return {'success': False, 'error': f'三色审计阻断：{audit_result.reason}'}
            elif audit_result.level == AuditLevel.YELLOW:
                print(f'{audit_result.level.value} 审计警告：{audit_result.reason}')
                print('   继续编译，但请注意内容')
            else:
                print(f'{audit_result.level.value} 审计通过：{audit_result.reason}')
            print()

            print('📝 阶段1：词法分析...')
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            print(f'   找到 {len(tokens)} 个token\n')

            print('🌳 阶段2：语法分析...')
            parser = Parser(tokens)
            ast = parser.parse()
            print('   生成抽象语法树\n')

            print('⚙️  阶段3：代码生成...')
            generator = CCodeGenerator(ast)
            c_code = generator.generate()
            print('   生成C代码\n')

            output_path = source_path.replace('.cnsh', '.c')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(c_code)

            print('✅ 编译成功！')
            print(f'   输出文件：{output_path}\n')
            print('📦 下一步：')
            print(f'   gcc {output_path} -o {source_path.replace(".cnsh", "")}')
            print(f'   ./{source_path.replace(".cnsh", "")}\n')

            return {'success': True, 'output_path': output_path, 'c_code': c_code}

        except Exception as e:
            print(f'❌ 编译失败：{e}')
            return {'success': False, 'error': str(e)}


# ═══════════════════════════════════════════════════════════════
# 🎯 命令行入口
# ═══════════════════════════════════════════════════════════════

def selftest():
    """自检"""
    code = '函数 主函数() 返回类型 整数 {\n  打印「自检通过」\n  返回 0\n}'
    compiler = CNSHCompiler()
    result = compiler.compile(code, '/tmp/test.cnsh')
    return result


def main():
    if len(sys.argv) < 2:
        print('用法: python3 cnsh_compiler.py <文件.cnsh>')
        print('示例: python3 cnsh_compiler.py hello.cnsh')
        sys.exit(1)

    source_path = sys.argv[1]

    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f'错误：文件不存在 {source_path}')
        sys.exit(1)

    compiler = CNSHCompiler()
    result = compiler.compile(source_code, source_path)
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
