#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH语法分析器（Parser）

DNA: #龍芯⚡️2026-06-03-PARSER-v1.0-FROM-JS
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

将Token流转换为抽象语法树（AST）
直译自JavaScript版本(cnsh-compiler.js lines 338-759)

体现原则：
- 递归下降解析
- 操作符优先级处理
- 完整的语句和表达式支持
"""

from typing import List, Optional
from .compiler_node import Token, ASTNode


class Parser:
    """
    语法分析器（基于递归下降的确定性解析）

    将Token流解析为AST，直译自JavaScript Parser类，保持结构一致。
    """

    def __init__(self, tokens: List[Token]):
        """
        初始化语法分析器

        Args:
            tokens: Token列表
        """
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        """获取当前Token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # 返回EOF

    def advance(self) -> Token:
        """前进到下一个Token，并返回当前Token"""
        token = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def peek(self) -> Optional[Token]:
        """查看下一个Token（不消费）"""
        if self.pos < len(self.tokens) - 1:
            return self.tokens[self.pos + 1]
        return None

    def expect(self, token_type: str, value: str = None) -> Token:
        """
        期望某个Token，如果不符合则抛异常

        Args:
            token_type: 期望的Token类型
            value: 可选的期望值

        Returns:
            符合条件的Token

        Raises:
            SyntaxError: 如果Token不符合期望
        """
        token = self.current()
        if token.type != token_type or (value and token.value != value):
            msg = f"语法错误 (行{token.line}): 期望 {token_type}"
            if value:
                msg += f" \"{value}\""
            msg += f", 但得到 {token.type} \"{token.value}\""
            raise SyntaxError(msg)
        return self.advance()

    def parse(self) -> ASTNode:
        """
        解析整个程序

        Returns:
            Program节点
        """
        statements = []

        while self.current().type != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return ASTNode('Program', {'statements': statements})

    def parse_statement(self) -> Optional[ASTNode]:
        """解析一个语句"""
        token = self.current()

        # 变量声明
        if token.type == 'KEYWORD' and token.value in ('整数', '小数', '文本', '真假', '字符串', '列表', '映射'):
            return self.parse_variable_declaration()

        # 函数声明
        if token.type == 'KEYWORD' and token.value == '函数':
            return self.parse_function_declaration()

        # if语句
        if token.type == 'KEYWORD' and token.value == '如果':
            return self.parse_if_statement()

        # 循环语句
        if token.type == 'KEYWORD' and token.value == '循环':
            return self.parse_loop_statement()

        # 返回语句
        if token.type == 'KEYWORD' and token.value == '返回':
            return self.parse_return_statement()

        # 表达式语句
        return self.parse_expression_statement()

    def parse_variable_declaration(self) -> ASTNode:
        """解析变量声明"""
        type_token = self.advance()
        name_token = self.expect('IDENTIFIER')

        value = None
        if self.current().type == 'ASSIGN':
            self.advance()
            value = self.parse_expression()

        # 分号可选
        if self.current().type == 'SEMICOLON':
            self.advance()

        return ASTNode('VariableDeclaration', {
            'varType': type_token.value,
            'name': name_token.value,
            'value': value
        })

    def parse_function_declaration(self) -> ASTNode:
        """解析函数声明"""
        self.advance()  # 消费'函数'
        name_token = self.expect('IDENTIFIER')

        self.expect('LPAREN')
        params = []

        while self.current().type != 'RPAREN':
            type_token = self.current()
            if type_token.type != 'KEYWORD' or type_token.value not in (
                '整数', '小数', '文本', '真假', '字符串', '列表', '映射'
            ):
                break
            self.advance()

            param_name = self.expect('IDENTIFIER')
            params.append({
                'type': type_token.value,
                'name': param_name.value
            })

            if self.current().type == 'COMMA':
                self.advance()

        self.expect('RPAREN')

        return_type = '空值'
        if self.current().type == 'KEYWORD' and self.current().value == '返回类型':
            self.advance()
            return_type = self.advance().value

        self.expect('LBRACE')
        body = []

        while self.current().type != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.expect('RBRACE')

        return ASTNode('FunctionDeclaration', {
            'name': name_token.value,
            'params': params,
            'returnType': return_type,
            'body': body
        })

    def parse_if_statement(self) -> ASTNode:
        """解析if语句"""
        self.advance()  # 消费'如果'

        # 支持【】或()
        if self.current().type == 'LBRACKET':
            self.advance()
        elif self.current().type == 'LPAREN':
            self.advance()
        else:
            raise SyntaxError(f"期望【或(在if条件前")

        condition = self.parse_expression()

        if self.current().type == 'RBRACKET':
            self.advance()
        elif self.current().type == 'RPAREN':
            self.advance()
        else:
            raise SyntaxError(f"期望】或)在if条件后")

        self.expect('LBRACE')
        then_body = []

        while self.current().type != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)

        self.expect('RBRACE')

        else_body = None
        if self.current().type == 'KEYWORD' and self.current().value == '否则':
            self.advance()
            self.expect('LBRACE')
            else_body = []

            while self.current().type != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)

            self.expect('RBRACE')

        return ASTNode('IfStatement', {
            'condition': condition,
            'thenBody': then_body,
            'elseBody': else_body
        })

    def parse_loop_statement(self) -> ASTNode:
        """解析循环语句"""
        self.advance()  # 消费'循环'

        if self.current().type == 'LBRACKET':
            self.advance()
        elif self.current().type == 'LPAREN':
            self.advance()
        else:
            raise SyntaxError("期望【或(在循环条件前")

        times = self.parse_expression()

        if self.current().type == 'RBRACKET':
            self.advance()
        elif self.current().type == 'RPAREN':
            self.advance()
        else:
            raise SyntaxError("期望】或)在循环条件后")

        self.expect('LBRACE')
        body = []

        while self.current().type != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.expect('RBRACE')

        return ASTNode('LoopStatement', {
            'times': times,
            'body': body
        })

    def parse_return_statement(self) -> ASTNode:
        """解析返回语句"""
        self.advance()  # 消费'返回'

        value = None
        if self.current().type != 'SEMICOLON' and self.current().type != 'RBRACE':
            value = self.parse_expression()

        if self.current().type == 'SEMICOLON':
            self.advance()

        return ASTNode('ReturnStatement', {'value': value})

    def parse_expression_statement(self) -> ASTNode:
        """解析表达式语句"""
        expr = self.parse_expression()

        if self.current().type == 'SEMICOLON':
            self.advance()

        return ASTNode('ExpressionStatement', {'expression': expr})

    def parse_expression(self) -> ASTNode:
        """解析表达式（最低优先级）"""
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        """解析赋值表达式"""
        left = self.parse_logical_or()

        if self.current().type == 'ASSIGN':
            self.advance()
            right = self.parse_assignment()
            return ASTNode('Assignment', {'left': left, 'right': right})

        return left

    def parse_logical_or(self) -> ASTNode:
        """解析逻辑或"""
        left = self.parse_logical_and()

        while self.current().type == 'LOGICAL_OR':
            op = self.advance().value
            right = self.parse_logical_and()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_logical_and(self) -> ASTNode:
        """解析逻辑与"""
        left = self.parse_equality()

        while self.current().type == 'LOGICAL_AND':
            op = self.advance().value
            right = self.parse_equality()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_equality(self) -> ASTNode:
        """解析相等比较 (==, !=)"""
        left = self.parse_comparison()

        while self.current().type in ('EQ', 'NEQ'):
            op = self.advance().value
            right = self.parse_comparison()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_comparison(self) -> ASTNode:
        """解析比较 (>, <, >=, <=)"""
        left = self.parse_term()

        while self.current().type in ('GT', 'LT', 'GTE', 'LTE'):
            op = self.advance().value
            right = self.parse_term()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_term(self) -> ASTNode:
        """解析加减"""
        left = self.parse_factor()

        while self.current().type in ('PLUS', 'MINUS'):
            op = self.advance().value
            right = self.parse_factor()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_factor(self) -> ASTNode:
        """解析乘除模"""
        left = self.parse_unary()

        while self.current().type in ('MULTIPLY', 'DIVIDE', 'MODULO'):
            op = self.advance().value
            right = self.parse_unary()
            left = ASTNode('BinaryOp', {'op': op, 'left': left, 'right': right})

        return left

    def parse_unary(self) -> ASTNode:
        """解析一元运算"""
        if self.current().type in ('MINUS', 'NOT'):
            op = self.advance().value
            operand = self.parse_unary()
            return ASTNode('UnaryOp', {'op': op, 'operand': operand})

        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """解析主要表达式"""
        token = self.current()

        # 数字
        if token.type == 'NUMBER':
            self.advance()
            return ASTNode('Number', {'value': token.value})

        # 字符串
        if token.type == 'STRING':
            self.advance()
            return ASTNode('String', {'value': token.value})

        # 布尔和空值
        if token.type == 'KEYWORD':
            if token.value == '真':
                self.advance()
                return ASTNode('Boolean', {'value': True})
            if token.value == '假':
                self.advance()
                return ASTNode('Boolean', {'value': False})
            if token.value == '空':
                self.advance()
                return ASTNode('Null', {})

        # 标识符或函数调用
        if token.type == 'IDENTIFIER':
            self.advance()

            if self.current().type == 'LPAREN':
                self.advance()
                args = []

                while self.current().type != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.current().type == 'COMMA':
                        self.advance()

                self.expect('RPAREN')
                return ASTNode('FunctionCall', {'name': token.value, 'args': args})

            return ASTNode('Identifier', {'name': token.value})

        # 括号表达式
        if token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr

        raise SyntaxError(f"语法错误 (行{token.line}): 意外的token {token.type} \"{token.value}\"")


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-06-03-PARSER-v1.0-FROM-JS"
__responsibility__ = "UID9622·不免责"
