#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 AST 优化器
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-OPTIMIZER-v2.1

自动优化能力：
- 常量折叠（Constant Folding）
- 死代码消除（Dead Code Elimination）
- 表达式化简（Expression Simplification）
"""
from copy import copy
from typing import List, Optional, Any

from . import ast_nodes as ast


class Optimizer:
    """CNSH AST 优化器"""

    def __init__(self, level: int = 2):
        """
        level:
          0 - 不优化
          1 - 常量折叠
          2 - 常量折叠 + 表达式化简
          3 - 以上 + 死代码消除
        """
        self.level = level
        self.stats = {
            "常量折叠": 0,
            "表达式化简": 0,
            "死代码消除": 0,
        }

    def optimize(self, node: ast.ASTNode) -> ast.ASTNode:
        if self.level <= 0:
            return node
        return self._opt(node)

    def report(self) -> dict[str, Any]:
        return dict(self.stats)

    # ---------- 节点分发 ----------
    def _opt(self, node: ast.ASTNode) -> ast.ASTNode:
        method = getattr(self, f"_opt_{type(node).__name__}", None)
        if method is None:
            return node
        return method(node)

    def _opt_Program(self, node: ast.Program) -> ast.Program:
        node.statements = self._opt_stmt_list(node.statements)
        return node

    def _opt_ModuleDecl(self, node: ast.ModuleDecl) -> ast.ModuleDecl:
        node.body = self._opt_stmt_list(node.body)
        return node

    def _opt_FunctionDecl(self, node: ast.FunctionDecl) -> ast.FunctionDecl:
        node.body = self._opt_stmt_list(node.body)
        return node

    def _opt_VarDecl(self, node: ast.VarDecl) -> ast.VarDecl:
        if node.initializer:
            node.initializer = self._opt(node.initializer)
        return node

    def _opt_StructDecl(self, node: ast.StructDecl) -> ast.StructDecl:
        return node

    def _opt_UseStmt(self, node: ast.UseStmt) -> ast.UseStmt:
        return node

    def _opt_IfStmt(self, node: ast.IfStmt) -> ast.ASTNode:
        node.condition = self._opt(node.condition)

        if self.level >= 3:
            cond = self._as_constant(node.condition)
            if cond is not None:
                if self._is_truthy_literal(cond):
                    self.stats["死代码消除"] += 1
                    return self._flatten_block(node.then_body)
                else:
                    # 否则分支可能命中
                    for branch in node.elif_branches:
                        branch.condition = self._opt(branch.condition)
                        c = self._as_constant(branch.condition)
                        if c is not None and self._is_truthy_literal(c):
                            self.stats["死代码消除"] += 1
                            return self._flatten_block(branch.body)
                        if c is not None:
                            continue
                    if node.else_body:
                        self.stats["死代码消除"] += 1
                        return self._flatten_block(node.else_body)
                    self.stats["死代码消除"] += 1
                    return ast.ExpressionStmt(expression=ast.LiteralExpr(value=None))

        node.then_body = self._opt_stmt_list(node.then_body)
        for branch in node.elif_branches:
            branch.body = self._opt_stmt_list(branch.body)
        if node.else_body:
            node.else_body = self._opt_stmt_list(node.else_body)
        return node

    def _opt_WhileStmt(self, node: ast.WhileStmt) -> ast.WhileStmt:
        node.condition = self._opt(node.condition)
        if self.level >= 3:
            cond = self._as_constant(node.condition)
            if cond is not None and not self._is_truthy_literal(cond):
                self.stats["死代码消除"] += 1
                return ast.ExpressionStmt(expression=ast.LiteralExpr(value=None))
        node.body = self._opt_stmt_list(node.body)
        return node

    def _opt_ForStmt(self, node: ast.ForStmt) -> ast.ForStmt:
        node.iterable = self._opt(node.iterable)
        node.body = self._opt_stmt_list(node.body)
        return node

    def _opt_ReturnStmt(self, node: ast.ReturnStmt) -> ast.ReturnStmt:
        if node.value:
            node.value = self._opt(node.value)
        return node

    def _opt_BreakStmt(self, node: ast.BreakStmt) -> ast.BreakStmt:
        return node

    def _opt_ContinueStmt(self, node: ast.ContinueStmt) -> ast.ContinueStmt:
        return node

    def _opt_ExpressionStmt(self, node: ast.ExpressionStmt) -> ast.ExpressionStmt:
        if node.expression:
            node.expression = self._opt(node.expression)
        return node

    # ---------- 表达式优化 ----------
    def _opt_BinaryExpr(self, node: ast.BinaryExpr) -> ast.ASTNode:
        node.left = self._opt(node.left)
        node.right = self._opt(node.right)

        # 常量折叠
        folded = self._fold_constant(node)
        if folded is not None:
            self.stats["常量折叠"] += 1
            return folded

        # 表达式化简
        if self.level >= 2:
            simplified = self._simplify_expression(node)
            if simplified is not None:
                self.stats["表达式化简"] += 1
                return simplified

        return node

    def _opt_UnaryExpr(self, node: ast.UnaryExpr) -> ast.ASTNode:
        node.operand = self._opt(node.operand)
        folded = self._fold_unary(node)
        if folded is not None:
            self.stats["常量折叠"] += 1
            return folded
        if self.level >= 2:
            simplified = self._simplify_unary(node)
            if simplified is not None:
                self.stats["表达式化简"] += 1
                return simplified
        return node

    def _opt_LiteralExpr(self, node: ast.LiteralExpr) -> ast.LiteralExpr:
        return node

    def _opt_IdentifierExpr(self, node: ast.IdentifierExpr) -> ast.IdentifierExpr:
        return node

    def _opt_CallExpr(self, node: ast.CallExpr) -> ast.CallExpr:
        node.callee = self._opt(node.callee)
        node.args = [self._opt(a) for a in node.args]
        return node

    def _opt_MemberExpr(self, node: ast.MemberExpr) -> ast.MemberExpr:
        node.object = self._opt(node.object)
        return node

    def _opt_IndexExpr(self, node: ast.IndexExpr) -> ast.IndexExpr:
        node.object = self._opt(node.object)
        node.index = self._opt(node.index)
        return node

    def _opt_ListExpr(self, node: ast.ListExpr) -> ast.ListExpr:
        node.elements = [self._opt(e) for e in node.elements]
        return node

    def _opt_MapExpr(self, node: ast.MapExpr) -> ast.MapExpr:
        for pair in node.pairs:
            pair.key = self._opt(pair.key)
            pair.value = self._opt(pair.value)
        return node

    # ---------- 辅助方法 ----------
    def _opt_stmt_list(self, stmts: List[ast.ASTNode]) -> List[ast.ASTNode]:
        result = []
        for stmt in stmts:
            optimized = self._opt(stmt)
            # 死代码消除后可能产生无意义的空表达式语句，可过滤
            if isinstance(optimized, ast.ExpressionStmt) and isinstance(optimized.expression, ast.LiteralExpr):
                continue
            result.append(optimized)
        return result

    def _flatten_block(self, stmts: List[ast.ASTNode]) -> ast.ASTNode:
        optimized = self._opt_stmt_list(stmts)
        if len(optimized) == 1:
            return optimized[0]
        # 多块无法作为单语句返回，保留为一个 Program 或 block 表达式？
        # 为简化，返回 Program（解释器可运行）
        return ast.Program(statements=optimized)

    def _as_constant(self, node: ast.ASTNode) -> Optional[ast.LiteralExpr]:
        if isinstance(node, ast.LiteralExpr):
            return node
        return None

    @staticmethod
    def _is_truthy_literal(lit: ast.LiteralExpr) -> bool:
        v = lit.value
        if v is None:
            return False
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            return len(v) > 0
        if isinstance(v, (list, dict)):
            return len(v) > 0
        return True

    def _fold_constant(self, node: ast.BinaryExpr) -> Optional[ast.LiteralExpr]:
        left = self._as_constant(node.left)
        right = self._as_constant(node.right)
        if left is None or right is None:
            return None
        a, b = left.value, right.value
        op = node.op
        try:
            if op == "+":
                return ast.LiteralExpr(value=a + b)
            if op == "-":
                return ast.LiteralExpr(value=a - b)
            if op == "*":
                return ast.LiteralExpr(value=a * b)
            if op == "/":
                return ast.LiteralExpr(value=a / b)
            if op == "%":
                return ast.LiteralExpr(value=a % b)
            if op == "==":
                return ast.LiteralExpr(value=a == b)
            if op == "!=":
                return ast.LiteralExpr(value=a != b)
            if op == "<":
                return ast.LiteralExpr(value=a < b)
            if op == ">":
                return ast.LiteralExpr(value=a > b)
            if op == "<=":
                return ast.LiteralExpr(value=a <= b)
            if op == ">=":
                return ast.LiteralExpr(value=a >= b)
            if op in ("&&", "且"):
                return ast.LiteralExpr(value=self._is_truthy_literal(left) and self._is_truthy_literal(right))
            if op in ("||", "或"):
                return ast.LiteralExpr(value=self._is_truthy_literal(left) or self._is_truthy_literal(right))
        except Exception:
            return None
        return None

    def _fold_unary(self, node: ast.UnaryExpr) -> Optional[ast.LiteralExpr]:
        operand = self._as_constant(node.operand)
        if operand is None:
            return None
        v = operand.value
        op = node.op
        if op in ("!", "非"):
            return ast.LiteralExpr(value=not self._is_truthy_literal(operand))
        if op == "-" and isinstance(v, (int, float)):
            return ast.LiteralExpr(value=-v)
        if op == "+" and isinstance(v, (int, float)):
            return ast.LiteralExpr(value=+v)
        return None

    def _simplify_expression(self, node: ast.BinaryExpr) -> Optional[ast.ASTNode]:
        op = node.op
        left = node.left
        right = node.right

        def is_zero(n):
            return isinstance(n, ast.LiteralExpr) and n.value == 0

        def is_one(n):
            return isinstance(n, ast.LiteralExpr) and n.value == 1

        def is_true(n):
            return isinstance(n, ast.LiteralExpr) and n.value is True

        def is_false(n):
            return isinstance(n, ast.LiteralExpr) and n.value is False

        if op in ("+",):
            if is_zero(left):
                return right
            if is_zero(right):
                return left
        if op == "-":
            if is_zero(right):
                return left
        if op in ("*",):
            if is_one(left):
                return right
            if is_one(right):
                return left
            if is_zero(left) or is_zero(right):
                return ast.LiteralExpr(value=0)
        if op == "/":
            if is_one(right):
                return left
        if op in ("&&", "且"):
            if is_true(left):
                return right
            if is_true(right):
                return left
            if is_false(left) or is_false(right):
                return ast.LiteralExpr(value=False)
        if op in ("||", "或"):
            if is_false(left):
                return right
            if is_false(right):
                return left
            if is_true(left) or is_true(right):
                return ast.LiteralExpr(value=True)
        return None

    def _simplify_unary(self, node: ast.UnaryExpr) -> Optional[ast.ASTNode]:
        op = node.op
        operand = node.operand
        if op in ("!", "非") and isinstance(operand, ast.UnaryExpr) and operand.op in ("!", "非"):
            return operand.operand
        return None
