#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH语义分析器（Semantic Analyzer）

DNA:#龍芯⚡️2026-06-03-SEMANTIC-FILE1-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

语义分析、类型检查、作用域分析、权重指向解析

体现原则：
- 类型检查: 基于逻辑的确定性类型推导
- 作用域: 支持嵌套作用域
- 权重: 解析变量/函数权重指向
- 可扩展: 参数化的类型规则
"""

from typing import Dict, List, Optional, Any, Tuple
from .compiler_node import ASTNode


class SemanticError(Exception):
    """语义分析错误"""
    pass


class Symbol:
    """符号（变量、函数等）"""

    def __init__(self, name: str, symbol_type: str, value_type: str, weight: int = 50, scope: str = "local"):
        """
        Args:
            name: 符号名称
            symbol_type: 符号类型 ('variable', 'function', 'parameter')
            value_type: 值类型 ('整数', '小数', '文本', '布尔', '列表', '映射', '空值')
            weight: 权重值 (0-100)
            scope: 作用域 ('global', 'local', 'parameter')
        """
        self.name = name
        self.symbol_type = symbol_type
        self.value_type = value_type
        self.weight = weight
        self.scope = scope
        self.defined_at = None  # 定义位置


class Scope:
    """作用域"""

    def __init__(self, name: str, parent: Optional['Scope'] = None, weight_level: int = 0):
        """
        Args:
            name: 作用域名称
            parent: 父作用域
            weight_level: 权重级别 (0=全局, 1=模块, 2=函数等)
        """
        self.name = name
        self.parent = parent
        self.weight_level = weight_level
        self.symbols: Dict[str, Symbol] = {}
        self.children: List[Scope] = []

    def define(self, symbol: Symbol):
        """定义符号"""
        if symbol.name in self.symbols:
            raise SemanticError(f"符号 {symbol.name} 已在作用域 {self.name} 中定义")
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        """查找符号（递归向上查找）"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def add_child(self, child: 'Scope'):
        """添加子作用域"""
        self.children.append(child)


class TypeChecker:
    """类型检查器"""

    # 类型兼容性矩阵（从CNSH规范提取）
    TYPE_MAPPING = {
        '整数': 'int',
        '小数': 'float',
        '文本': 'string',
        '真假': 'bool',
        '布尔': 'bool',
        '列表': 'list',
        '数组': 'array',
        '映射': 'map',
        '向量': 'vector',
        '空值': 'void',
        '空': 'null',
    }

    # 类型兼容性规则
    COMPATIBLE = {
        'int': ['int', 'float'],
        'float': ['float'],
        'string': ['string'],
        'bool': ['bool'],
        'list': ['list'],
        'map': ['map'],
        'void': ['void'],
        'null': ['null'],
    }

    @staticmethod
    def canonicalize_type(type_name: str) -> str:
        """规范化类型名称"""
        return TypeChecker.TYPE_MAPPING.get(type_name, type_name)

    @staticmethod
    def is_compatible(from_type: str, to_type: str) -> bool:
        """检查类型兼容性"""
        from_type = TypeChecker.canonicalize_type(from_type)
        to_type = TypeChecker.canonicalize_type(to_type)

        if from_type == to_type:
            return True

        return from_type in TypeChecker.COMPATIBLE.get(to_type, [])


class SemanticAnalyzer:
    """语义分析器"""

    def __init__(self):
        """初始化语义分析器"""
        self.global_scope = Scope('global', weight_level=0)
        self.current_scope = self.global_scope
        self.errors: List[SemanticError] = []
        self.warnings: List[str] = []

    def analyze(self, ast: ASTNode) -> Tuple[bool, List[str], List[str]]:
        """
        分析AST

        Args:
            ast: 抽象语法树根节点

        Returns:
            (成功, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        try:
            self._analyze_node(ast)
        except SemanticError as e:
            self.errors.append(str(e))

        return len(self.errors) == 0, self.errors, self.warnings

    def _get(self, node: ASTNode, key: str, default=None):
        """从ASTNode的value字典获取属性"""
        if isinstance(node.value, dict):
            return node.value.get(key, default)
        return default

    def _analyze_node(self, node: ASTNode):
        """分析单个节点"""
        if not isinstance(node, ASTNode):
            return

        node_type = node.node_type

        if node_type == 'Program':
            self._analyze_program(node)
        elif node_type == 'FunctionDeclaration':
            self._analyze_function_declaration(node)
        elif node_type == 'VariableDeclaration':
            self._analyze_variable_declaration(node)
        elif node_type == 'IfStatement':
            self._analyze_if_statement(node)
        elif node_type == 'LoopStatement':
            self._analyze_loop_statement(node)
        elif node_type == 'ReturnStatement':
            self._analyze_return_statement(node)
        elif node_type == 'ExpressionStatement':
            self._analyze_expression_statement(node)
        elif node_type == 'Assignment':
            self._analyze_assignment(node)
        elif node_type == 'BinaryOp':
            self._analyze_binary_op(node)
        elif node_type == 'FunctionCall':
            self._analyze_function_call(node)
        elif node_type == 'Identifier':
            self._analyze_identifier(node)

    def _analyze_program(self, node: ASTNode):
        """分析程序"""
        statements = self._get(node, 'statements', [])
        for stmt in statements:
            self._analyze_node(stmt)

    def _analyze_function_declaration(self, node: ASTNode):
        """分析函数声明"""
        name = self._get(node, 'name')
        params = self._get(node, 'params', [])
        return_type = self._get(node, 'returnType', '空值')
        body = self._get(node, 'body', [])

        # 定义函数符号
        symbol = Symbol(name, 'function', return_type, weight=80)
        try:
            self.current_scope.define(symbol)
        except SemanticError as e:
            self.errors.append(str(e))

        # 创建函数作用域
        func_scope = Scope(f"func_{name}", parent=self.current_scope, weight_level=1)
        self.current_scope.add_child(func_scope)
        old_scope = self.current_scope
        self.current_scope = func_scope

        # 定义参数
        for param in params:
            param_symbol = Symbol(
                param.get('name'),
                'parameter',
                param.get('type'),
                scope='parameter'
            )
            try:
                self.current_scope.define(param_symbol)
            except SemanticError as e:
                self.errors.append(str(e))

        # 分析函数体
        for stmt in body:
            self._analyze_node(stmt)

        # 恢复作用域
        self.current_scope = old_scope

    def _analyze_variable_declaration(self, node: ASTNode):
        """分析变量声明"""
        var_type = self._get(node, 'varType')
        name = self._get(node, 'name')
        value = self._get(node, 'value')

        # 定义变量符号
        symbol = Symbol(name, 'variable', var_type)
        try:
            self.current_scope.define(symbol)
        except SemanticError as e:
            self.errors.append(str(e))

        # 检查初始化值的类型
        if value:
            # 分析初始化值表达式（检查未定义变量等）
            self._analyze_node(value)
            value_type = self._infer_type(value)
            if value_type and not TypeChecker.is_compatible(value_type, var_type):
                self.warnings.append(
                    f"变量 {name} 类型不匹配: "
                    f"期望 {var_type} 但得到 {value_type}"
                )

    def _analyze_if_statement(self, node: ASTNode):
        """分析if语句"""
        condition = self._get(node, 'condition')
        then_body = self._get(node, 'thenBody', [])
        else_body = self._get(node, 'elseBody')

        # 检查条件类型
        if condition:
            cond_type = self._infer_type(condition)
            if cond_type and cond_type != '布尔':
                self.warnings.append(
                    f"if条件应为布尔类型，但得到 {cond_type}"
                )

        # 创建if块作用域
        if_scope = Scope('if_block', parent=self.current_scope, weight_level=1)
        self.current_scope.add_child(if_scope)
        old_scope = self.current_scope
        self.current_scope = if_scope

        # 分析then分支
        for stmt in then_body:
            self._analyze_node(stmt)

        self.current_scope = old_scope

        # 分析else分支
        if else_body:
            else_scope = Scope('else_block', parent=self.current_scope, weight_level=1)
            self.current_scope.add_child(else_scope)
            old_scope = self.current_scope
            self.current_scope = else_scope

            for stmt in else_body:
                self._analyze_node(stmt)

            self.current_scope = old_scope

    def _analyze_loop_statement(self, node: ASTNode):
        """分析循环语句"""
        times = self._get(node, 'times')
        body = self._get(node, 'body', [])

        # 创建循环块作用域
        loop_scope = Scope('loop_block', parent=self.current_scope, weight_level=1)
        self.current_scope.add_child(loop_scope)
        old_scope = self.current_scope
        self.current_scope = loop_scope

        # 分析循环体
        for stmt in body:
            self._analyze_node(stmt)

        self.current_scope = old_scope

    def _analyze_return_statement(self, node: ASTNode):
        """分析返回语句"""
        value = self._get(node, 'value')
        if value:
            # 分析返回值表达式（检查未定义变量等）
            self._analyze_node(value)

    def _analyze_expression_statement(self, node: ASTNode):
        """分析表达式语句"""
        expr = self._get(node, 'expression')
        if expr:
            self._analyze_node(expr)

    def _analyze_assignment(self, node: ASTNode):
        """分析赋值"""
        left = self._get(node, 'left')
        right = self._get(node, 'right')

        # 检查左值是否是变量
        if left and left.node_type == 'Identifier':
            var_name = self._get(left, 'name')
            symbol = self.current_scope.lookup(var_name)
            if not symbol:
                self.errors.append(f"变量 {var_name} 未定义")
                return

            # 分析右值表达式
            if right:
                self._analyze_node(right)

            # 检查右值类型
            right_type = self._infer_type(right)
            if right_type and not TypeChecker.is_compatible(right_type, symbol.value_type):
                self.warnings.append(
                    f"赋值类型不匹配: 变量 {var_name} 期望 {symbol.value_type} "
                    f"但得到 {right_type}"
                )

    def _analyze_binary_op(self, node: ASTNode):
        """分析二元操作"""
        left = self._get(node, 'left')
        right = self._get(node, 'right')
        op = self._get(node, 'op')

        if left:
            self._analyze_node(left)
        if right:
            self._analyze_node(right)

    def _analyze_function_call(self, node: ASTNode):
        """分析函数调用"""
        name = self._get(node, 'name')
        args = self._get(node, 'args', [])

        # 检查函数是否存在
        func_symbol = self.current_scope.lookup(name)
        if not func_symbol:
            self.warnings.append(f"函数 {name} 未找到（可能是内置函数）")
            return

        if func_symbol.symbol_type != 'function':
            self.errors.append(f"{name} 不是一个函数")

        # 分析参数
        for arg in args:
            self._analyze_node(arg)

    def _analyze_identifier(self, node: ASTNode):
        """分析标识符"""
        name = self._get(node, 'name')
        symbol = self.current_scope.lookup(name)
        if not symbol:
            self.errors.append(f"未定义的标识符: {name}")

    def _infer_type(self, node: Optional[ASTNode]) -> Optional[str]:
        """推导表达式类型"""
        if not node:
            return None

        node_type = node.node_type

        if node_type == 'Number':
            # 简单启发式：整数vs浮点
            value = str(self._get(node, 'value', ''))
            return '小数' if '.' in value else '整数'

        elif node_type == 'String':
            return '文本'

        elif node_type == 'Boolean':
            return '布尔'

        elif node_type == 'Null':
            return '空值'

        elif node_type == 'Identifier':
            name = self._get(node, 'name')
            symbol = self.current_scope.lookup(name)
            return symbol.value_type if symbol else None

        elif node_type == 'BinaryOp':
            op = self._get(node, 'op')
            left_type = self._infer_type(self._get(node, 'left'))
            right_type = self._infer_type(self._get(node, 'right'))

            # 比较和逻辑操作返回布尔
            if op in ('==', '!=', '<', '>', '<=', '>=', '&&', '||'):
                return '布尔'

            # 算术操作
            if op in ('+', '-', '*', '/', '%'):
                if left_type == '文本' and op == '+':
                    return '文本'
                elif left_type in ('整数', '小数') and right_type in ('整数', '小数'):
                    return '小数' if '小数' in (left_type, right_type) else '整数'

            return left_type

        elif node_type == 'UnaryOp':
            op = self._get(node, 'op')
            operand_type = self._infer_type(self._get(node, 'operand'))

            if op == '!':
                return '布尔'

            return operand_type

        elif node_type == 'FunctionCall':
            # 简化：假设返回int
            return '整数'

        elif node_type == 'Assignment':
            return self._infer_type(self._get(node, 'right'))

        return None


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-06-03-SEMANTIC-v1.0"
__responsibility__ = "UID9622·不免责"
