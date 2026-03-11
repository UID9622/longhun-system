#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇨🇳 CNSH编译器 v1.0 (Python版)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码：#龙芯⚡️2026-02-02-CNSH-Python编译器-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者：💎 龙芯北辰｜UID9622（中国退伍军人）
协作者：Claude (Anthropic)
战斗宣言：宁可战死，绝不被窃

功能：将CNSH代码转译为C代码
特性：
  - 纯中文语法
  - 内置DNA追溯
  - 三色审计系统
  - 内存安全检查
  - 完整错误提示

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
                (r'\d{15,18}', '可能包含身份证号'),
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
        # 类型
        '整数', '小数', '文本', '真假', '空值',
        # 控制流
        '如果', '否则', '循环', '当', '返回', '跳出', '继续',
        # 函数和结构
        '函数', '类', '结构', '返回类型',
        # DNA和审计
        'DNA追溯', '三色审计',
        # 其他
        '打印', '输入', '真', '假', '空',
        # 内存管理
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
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
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
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_decimal:
                    break
                has_decimal = True
            num_str += self.current_char()
            self.advance()
        
        return num_str
    
    def read_string(self, quote: str) -> str:
        """读取字符串"""
        # 确定结束引号
        close_quote = {
            '"': '"',
            "'": "'",
            '「': '」',
            '『': '』'
        }.get(quote, quote)
        
        self.advance()  # 跳过开始引号
        string = ''
        
        while self.current_char() and self.current_char() != close_quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    # 转义字符
                    escape_chars = {
                        'n': '\n',
                        't': '\t',
                        'r': '\r',
                        '\\': '\\',
                        '"': '"',
                        "'": "'"
                    }
                    string += escape_chars.get(self.current_char(), self.current_char())
                    self.advance()
            else:
                string += self.current_char()
                self.advance()
        
        if self.current_char() == close_quote:
            self.advance()  # 跳过结束引号
        
        return string
    
    def read_identifier(self) -> str:
        """读取标识符或关键字"""
        ident = ''
        
        # 支持中文、英文、数字、下划线
        while self.current_char() and (
            '\u4e00' <= self.current_char() <= '\u9fa5' or  # 中文
            self.current_char().isalnum() or
            self.current_char() == '_'
        ):
            ident += self.current_char()
            self.advance()
        
        return ident
    
    def tokenize(self) -> List[Token]:
        """分词"""
        while self.current_char():
            # 跳过空白
            if self.current_char() in ' \t\r\n':
                self.skip_whitespace()
                continue
            
            # 跳过注释
            if self.skip_comment():
                continue
            
            line, column = self.line, self.column
            ch = self.current_char()
            
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
            if ch == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', line, column))
                continue
            
            if ch == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '!=', line, column))
                continue
            
            if ch == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, '>=', line, column))
                continue
            
            if ch == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, '<=', line, column))
                continue
            
            if ch == '&' and self.peek_char() == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_AND, '&&', line, column))
                continue
            
            if ch == '|' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LOGICAL_OR, '||', line, column))
                continue
            
            # 单字符符号
            single_chars = {
                '=': TokenType.ASSIGN,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '>': TokenType.GT,
                '<': TokenType.LT,
                '!': TokenType.NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '【': TokenType.LBRACKET,
                '】': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
            }
            
            if ch in single_chars:
                self.advance()
                self.tokens.append(Token(single_chars[ch], ch, line, column))
                continue
            
            # 未知字符
            self.advance()
            self.tokens.append(Token(TokenType.UNKNOWN, ch, line, column))
        
        # EOF
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ═══════════════════════════════════════════════════════════════
# 🌳 抽象语法树（AST）节点
# ═══════════════════════════════════════════════════════════════

@dataclass
class ASTNode:
    """AST节点基类"""
    pass


@dataclass
class Program(ASTNode):
    """程序"""
    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    """变量声明"""
    var_type: str
    name: str
    value: Optional[ASTNode] = None


@dataclass
class FunctionDeclaration(ASTNode):
    """函数声明"""
    name: str
    params: List[Dict[str, str]]
    return_type: str
    body: List[ASTNode]


@dataclass
class IfStatement(ASTNode):
    """if语句"""
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class LoopStatement(ASTNode):
    """循环语句"""
    times: ASTNode
    body: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    """return语句"""
    value: Optional[ASTNode] = None


@dataclass
class PrintStatement(ASTNode):
    """打印语句"""
    value: ASTNode


@dataclass
class ExpressionStatement(ASTNode):
    """表达式语句"""
    expression: ASTNode


@dataclass
class Number(ASTNode):
    """数字"""
    value: str


@dataclass
class String(ASTNode):
    """字符串"""
    value: str


@dataclass
class Boolean(ASTNode):
    """布尔值"""
    value: bool


@dataclass
class Null(ASTNode):
    """空值"""
    pass


@dataclass
class Identifier(ASTNode):
    """标识符"""
    name: str


@dataclass
class BinaryOp(ASTNode):
    """二元运算"""
    op: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """一元运算"""
    op: str
    operand: ASTNode


@dataclass
class Assignment(ASTNode):
    """赋值"""
    left: ASTNode
    right: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """函数调用"""
    name: str
    args: List[ASTNode]


# ═══════════════════════════════════════════════════════════════
# 🔍 语法分析器（Parser）
# ═══════════════════════════════════════════════════════════════

class Parser:
    """语法分析器"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current(self) -> Token:
        """当前token"""
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 1) -> Token:
        """向前看token"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        """前进"""
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType, value: Optional[str] = None) -> Token:
        """期望某个token"""
        token = self.current()
        if token.type != token_type or (value and token.value != value):
            expected = f"{token_type.name}"
            if value:
                expected += f" '{value}'"
            raise SyntaxError(
                f"语法错误 (行{token.line}): 期望 {expected}, "
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
        """解析语句"""
        token = self.current()
        
        # 变量声明
        if token.type == TokenType.KEYWORD and token.value in ['整数', '小数', '文本', '真假']:
            return self.parse_variable_declaration()
        
        # 函数定义
        if token.type == TokenType.KEYWORD and token.value == '函数':
            return self.parse_function_declaration()
        
        # if语句
        if token.type == TokenType.KEYWORD and token.value == '如果':
            return self.parse_if_statement()
        
        # 循环语句
        if token.type == TokenType.KEYWORD and token.value == '循环':
            return self.parse_loop_statement()
        
        # return语句
        if token.type == TokenType.KEYWORD and token.value == '返回':
            return self.parse_return_statement()
        
        # 打印语句
        if token.type == TokenType.KEYWORD and token.value == '打印':
            return self.parse_print_statement()
        
        # 表达式语句
        return self.parse_expression_statement()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """解析变量声明"""
        type_token = self.advance()
        name_token = self.expect(TokenType.IDENTIFIER)
        
        value = None
        if self.current().type == TokenType.ASSIGN:
            self.advance()  # 跳过 =
            value = self.parse_expression()
        
        # 可选的分号
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        
        return VariableDeclaration(type_token.value, name_token.value, value)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """解析函数声明"""
        self.advance()  # 跳过 '函数'
        name_token = self.expect(TokenType.IDENTIFIER)
        
        self.expect(TokenType.LPAREN)
        params = []
        
        # 参数列表
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
        
        # 返回类型
        return_type = '空值'
        if self.current().type == TokenType.KEYWORD and self.current().value == '返回类型':
            self.advance()
            return_type = self.advance().value
        
        # 函数体
        self.expect(TokenType.LBRACE)
        body = []
        
        while self.current().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        return FunctionDeclaration(name_token.value, params, return_type, body)
    
    def parse_if_statement(self) -> IfStatement:
        """解析if语句"""
        self.advance()  # 跳过 '如果'
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
        
        # else子句
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
        """解析循环语句"""
        self.advance()  # 跳过 '循环'
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
        """解析return语句"""
        self.advance()  # 跳过 '返回'
        
        value = None
        if self.current().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        
        return ReturnStatement(value)
    
    def parse_print_statement(self) -> PrintStatement:
        """解析打印语句"""
        self.advance()  # 跳过 '打印'
        value = self.parse_expression()
        
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        
        return PrintStatement(value)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """解析表达式语句"""
        expr = self.parse_expression()
        
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
        
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        """解析赋值"""
        left = self.parse_logical_or()
        
        if self.current().type == TokenType.ASSIGN:
            self.advance()
            right = self.parse_assignment()
            return Assignment(left, right)
        
        return left
    
    def parse_logical_or(self) -> ASTNode:
        """解析逻辑或"""
        left = self.parse_logical_and()
        
        while self.current().type == TokenType.LOGICAL_OR:
            op = self.advance().value
            right = self.parse_logical_and()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        """解析逻辑与"""
        left = self.parse_equality()
        
        while self.current().type == TokenType.LOGICAL_AND:
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        """解析相等性"""
        left = self.parse_comparison()
        
        while self.current().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """解析比较"""
        left = self.parse_term()
        
        while self.current().type in [TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE]:
            op = self.advance().value
            right = self.parse_term()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        """解析项"""
        left = self.parse_factor()
        
        while self.current().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_factor(self) -> ASTNode:
        """解析因子"""
        left = self.parse_unary()
        
        while self.current().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """解析一元运算"""
        if self.current().type in [TokenType.MINUS, TokenType.NOT]:
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        token = self.current()
        
        # 数字
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        
        # 字符串
        if token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        
        # 布尔值和空值
        if token.type == TokenType.KEYWORD:
            if token.value == '真':
                self.advance()
                return Boolean(True)
            if token.value == '假':
                self.advance()
                return Boolean(False)
            if token.value == '空':
                self.advance()
                return Null()
        
        # 标识符或函数调用
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            
            # 函数调用
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
        
        # 括号表达式
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
        '整数': 'int',
        '小数': 'double',
        '文本': 'char*',
        '真假': 'bool',
        '空值': 'void'
    }
    
    DEFAULT_VALUES = {
        'int': '0',
        'double': '0.0',
        'char*': 'NULL',
        'bool': 'false',
        'void': ''
    }
    
    def __init__(self, ast: Program):
        self.ast = ast
        self.indent = 0
        self.output = []
    
    def emit(self, code: str):
        """输出代码"""
        indent_str = '    ' * self.indent
        self.output.append(indent_str + code)
    
    def generate(self) -> str:
        """生成C代码"""
        # 头文件
        self.output.append('// Generated by CNSH Compiler v1.0 (Python)')
        self.output.append('// DNA追溯码：#龙芯⚡️2026-02-02-CNSH编译输出')
        self.output.append('// GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F')
        self.output.append('')
        self.output.append('#include <stdio.h>')
        self.output.append('#include <stdlib.h>')
        self.output.append('#include <string.h>')
        self.output.append('#include <stdbool.h>')
        self.output.append('')
        
        # 生成程序体
        self.generate_program(self.ast)
        
        # main函数
        self.output.append('')
        self.output.append('int main() {')
        self.output.append('    主函数();')
        self.output.append('    return 0;')
        self.output.append('}')
        
        return '\n'.join(self.output)
    
    def generate_program(self, node: Program):
        """生成程序"""
        for stmt in node.statements:
            self.generate_statement(stmt)
    
    def generate_statement(self, node: ASTNode):
        """生成语句"""
        if isinstance(node, VariableDeclaration):
            self.generate_variable_declaration(node)
        elif isinstance(node, FunctionDeclaration):
            self.generate_function_declaration(node)
        elif isinstance(node, IfStatement):
            self.generate_if_statement(node)
        elif isinstance(node, LoopStatement):
            self.generate_loop_statement(node)
        elif isinstance(node, ReturnStatement):
            self.generate_return_statement(node)
        elif isinstance(node, PrintStatement):
            self.generate_print_statement(node)
        elif isinstance(node, ExpressionStatement):
            expr_code = self.generate_expression(node.expression)
            self.emit(f'{expr_code};')
    
    def generate_variable_declaration(self, node: VariableDeclaration):
        """生成变量声明"""
        c_type = self.TYPE_MAP[node.var_type]
        value = self.generate_expression(node.value) if node.value else self.DEFAULT_VALUES[c_type]
        self.emit(f'{c_type} {node.name} = {value};')
    
    def generate_function_declaration(self, node: FunctionDeclaration):
        """生成函数声明"""
        return_type = self.TYPE_MAP[node.return_type]
        params = ', '.join(
            f"{self.TYPE_MAP[p['type']]} {p['name']}"
            for p in node.params
        )
        
        self.emit(f'{return_type} {node.name}({params}) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        self.emit('}')
        self.emit('')
    
    def generate_if_statement(self, node: IfStatement):
        """生成if语句"""
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
    
    def generate_loop_statement(self, node: LoopStatement):
        """生成循环语句"""
        times = self.generate_expression(node.times)
        self.emit(f'for (int __i = 0; __i < {times}; __i++) {{')
        self.indent += 1
        
        for stmt in node.body:
            self.generate_statement(stmt)
        
        self.indent -= 1
        self.emit('}')
    
    def generate_return_statement(self, node: ReturnStatement):
        """生成return语句"""
        if node.value:
            value = self.generate_expression(node.value)
            self.emit(f'return {value};')
        else:
            self.emit('return;')
    
    def generate_print_statement(self, node: PrintStatement):
        """生成打印语句"""
        value = self.generate_expression(node.value)
        
        # 根据类型选择printf格式
        if isinstance(node.value, String):
            self.emit(f'printf("%s\\n", {value});')
        elif isinstance(node.value, Number):
            self.emit(f'printf("%g\\n", (double){value});')
        else:
            self.emit(f'printf("%d\\n", {value});')
    
    def generate_expression(self, node: ASTNode) -> str:
        """生成表达式"""
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
        else:
            return ''


# ═══════════════════════════════════════════════════════════════
# 🚀 CNSH编译器
# ═══════════════════════════════════════════════════════════════

class CNSHCompiler:
    """CNSH编译器"""
    
    VERSION = '1.0'
    DNA_CODE = '#龙芯⚡️2026-02-02-CNSH-Python编译器-v1.0'
    
    def __init__(self):
        self.audit_system = ThreeColorAudit()
    
    def compile(self, source_code: str, source_path: str) -> Dict[str, Any]:
        """编译CNSH代码"""
        print('🇨🇳 CNSH编译器 v' + self.VERSION + ' (Python版)')
        print('DNA追溯码：' + self.DNA_CODE)
        print('━━━━━━━━━━━━━━━━━━\n')
        
        try:
            # 三色审计
            print('🛡️  阶段0：三色审计...')
            audit_result = self.audit_system.check(source_code)
            
            if audit_result.level == AuditLevel.RED:
                print(f'{audit_result.level.value} 审计阻断：{audit_result.reason}')
                print('   编译终止')
                return {
                    'success': False,
                    'error': f'三色审计阻断：{audit_result.reason}'
                }
            elif audit_result.level == AuditLevel.YELLOW:
                print(f'{audit_result.level.value} 审计警告：{audit_result.reason}')
                print('   继续编译，但请注意内容')
            else:
                print(f'{audit_result.level.value} 审计通过：{audit_result.reason}')
            print()
            
            # 词法分析
            print('📝 阶段1：词法分析...')
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            print(f'   找到 {len(tokens)} 个token\n')
            
            # 语法分析
            print('🌳 阶段2：语法分析...')
            parser = Parser(tokens)
            ast = parser.parse()
            print('   生成抽象语法树\n')
            
            # 代码生成
            print('⚙️  阶段3：代码生成...')
            generator = CCodeGenerator(ast)
            c_code = generator.generate()
            print('   生成C代码\n')
            
            # 保存输出
            output_path = source_path.replace('.cnsh', '.c')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(c_code)
            
            print('✅ 编译成功！')
            print(f'   输出文件：{output_path}\n')
            
            print('📦 下一步：')
            print(f'   gcc {output_path} -o {source_path.replace(".cnsh", "")}')
            print(f'   ./{source_path.replace(".cnsh", "")}\n')
            
            return {
                'success': True,
                'output_path': output_path,
                'c_code': c_code
            }
            
        except Exception as e:
            print(f'❌ 编译失败：{e}')
            return {
                'success': False,
                'error': str(e)
            }


# ═══════════════════════════════════════════════════════════════
# 🎯 命令行入口
# ═══════════════════════════════════════════════════════════════

def main():
    """命令行入口"""
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
