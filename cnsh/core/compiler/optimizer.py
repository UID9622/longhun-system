#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
CNSH优化器（Optimizer）

DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-OPTIMIZER-FILE1-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

编译优化：常量折叠、死代码消除、表达式简化

体现原则：
- 可融合的数学变换
- 确定性优化（可追溯）
- 可选的优化级别 (0-3)
"""

from typing import Dict, List, Optional, Any, Tuple
from .compiler_node import ASTNode


class OptimizerError(Exception):
    """优化错误"""
    pass


class Optimizer:
    """代码优化器"""

    def __init__(self, level: int = 1):
        """
        初始化优化器

        Args:
            level: 优化级别
                0: 无优化
                1: 常量折叠（默认）
                2: + 死代码消除
                3: + 表达式简化
        """
        if not 0 <= level <= 3:
            raise ValueError(f"优化级别应该在 0-3 之间，得到 {level}")
        self.level = level
        self.optimizations_applied = []

    def optimize(self, ast: ASTNode) -> ASTNode:
        """
        优化 AST

        Args:
            ast: 抽象语法树

        Returns:
            优化后的 AST
        """
        if self.level == 0:
            return ast

        self.optimizations_applied = []

        try:
            # Level 1: 常量折叠
            if self.level >= 1:
                ast = self._constant_folding(ast)

            # Level 2: 死代码消除
            if self.level >= 2:
                ast = self._dead_code_elimination(ast)

            # Level 3: 表达式简化
            if self.level >= 3:
                ast = self._expression_simplification(ast)

            return ast

        except Exception as e:
            raise OptimizerError(f"优化失败: {str(e)}")

    # ═══════════════════════════════════════════════════════════════
    # 【优化 Pass 1：常量折叠】
    # ═══════════════════════════════════════════════════════════════

    def _constant_folding(self, node: ASTNode) -> ASTNode:
        """
        常量折叠：在编译时计算常量表达式

        例如：1 + 2 → 3
        """
        if not isinstance(node, ASTNode):
            return node

        # 递归处理子节点
        if hasattr(node, 'children') and node.children:
            for i, child in enumerate(node.children):
                node.children[i] = self._constant_folding(child)

        # 处理 node.value 中的子节点
        if isinstance(node.value, dict):
            for key, value in list(node.value.items()):
                if isinstance(value, ASTNode):
                    node.value[key] = self._constant_folding(value)
                elif isinstance(value, list):
                    node.value[key] = [
                        self._constant_folding(item) if isinstance(item, ASTNode) else item
                        for item in value
                    ]

        # 尝试常量折叠这个节点
        if node.node_type == 'BinaryOp':
            return self._fold_binary_op(node)
        elif node.node_type == 'UnaryOp':
            return self._fold_unary_op(node)

        return node

    def _fold_binary_op(self, node: ASTNode) -> ASTNode:
        """折叠二元运算"""
        left = self._get(node, 'left')
        right = self._get(node, 'right')
        op = self._get(node, 'op')

        # 只有两个操作数都是常量时才能折叠
        if not self._is_constant(left) or not self._is_constant(right):
            return node

        try:
            left_val = self._get_constant_value(left)
            right_val = self._get_constant_value(right)

            # 算术运算
            if op == '+':
                result = left_val + right_val
            elif op == '-':
                result = left_val - right_val
            elif op == '*':
                result = left_val * right_val
            elif op == '/':
                if right_val == 0:
                    return node  # 避免除以零
                result = left_val / right_val
            elif op == '%':
                if right_val == 0:
                    return node
                result = left_val % right_val
            # 比较运算
            elif op == '==':
                result = left_val == right_val
            elif op == '!=':
                result = left_val != right_val
            elif op == '<':
                result = left_val < right_val
            elif op == '>':
                result = left_val > right_val
            elif op == '<=':
                result = left_val <= right_val
            elif op == '>=':
                result = left_val >= right_val
            # 逻辑运算
            elif op == '&&':
                result = left_val and right_val
            elif op == '||':
                result = left_val or right_val
            else:
                return node

            # 创建新的常量节点
            result_type = left.node_type
            result_node = ASTNode(result_type, {'value': result})
            self.optimizations_applied.append(f"常量折叠: {op}")
            return result_node

        except Exception:
            return node

    def _fold_unary_op(self, node: ASTNode) -> ASTNode:
        """折叠一元运算"""
        operand = self._get(node, 'operand')
        op = self._get(node, 'op')

        if not self._is_constant(operand):
            return node

        try:
            val = self._get_constant_value(operand)

            if op == '-':
                result = -val
            elif op == '!':
                result = not val
            else:
                return node

            result_type = 'Boolean' if op == '!' else operand.node_type
            result_node = ASTNode(result_type, {'value': result})
            self.optimizations_applied.append(f"一元常量折叠: {op}")
            return result_node

        except Exception:
            return node

    # ═══════════════════════════════════════════════════════════════
    # 【优化 Pass 2：死代码消除】
    # ═══════════════════════════════════════════════════════════════

    def _dead_code_elimination(self, node: ASTNode) -> ASTNode:
        """
        死代码消除

        移除不可达的代码或未使用的变量
        """
        if node.node_type == 'Program':
            statements = self._get(node, 'statements', [])
            alive_statements = []

            for stmt in statements:
                # 优化每个语句
                stmt = self._constant_folding(stmt)

                # 移除 always-false if 语句的 then 分支
                if stmt.node_type == 'IfStatement':
                    condition = self._get(stmt, 'condition')
                    if self._is_false_condition(condition):
                        # 如果有 else，保留 else；否则删除
                        else_body = self._get(stmt, 'elseBody')
                        if else_body:
                            # 将 else 体替换为顶级语句
                            for s in else_body:
                                alive_statements.append(s)
                            self.optimizations_applied.append("死代码消除: 移除 false if")
                        else:
                            self.optimizations_applied.append("死代码消除: 移除 false if")
                        continue

                alive_statements.append(stmt)

            if len(alive_statements) < len(statements):
                node.value['statements'] = alive_statements

        return node

    def _is_false_condition(self, node: ASTNode) -> bool:
        """检查条件是否总是 false"""
        if node.node_type == 'Boolean':
            return self._get(node, 'value') is False
        return False

    # ═══════════════════════════════════════════════════════════════
    # 【优化 Pass 3：表达式简化】
    # ═══════════════════════════════════════════════════════════════

    def _expression_simplification(self, node: ASTNode) -> ASTNode:
        """
        表达式简化

        例如：x + 0 → x，x * 1 → x，x && true → x 等
        """
        if not isinstance(node, ASTNode):
            return node

        # 递归处理子节点
        if hasattr(node, 'children') and node.children:
            for i, child in enumerate(node.children):
                node.children[i] = self._expression_simplification(child)

        # 处理 node.value 中的子节点
        if isinstance(node.value, dict):
            for key, value in list(node.value.items()):
                if isinstance(value, ASTNode):
                    node.value[key] = self._expression_simplification(value)
                elif isinstance(value, list):
                    node.value[key] = [
                        self._expression_simplification(item) if isinstance(item, ASTNode) else item
                        for item in value
                    ]

        # 简化二元运算
        if node.node_type == 'BinaryOp':
            return self._simplify_binary_op(node)

        return node

    def _simplify_binary_op(self, node: ASTNode) -> ASTNode:
        """简化二元运算"""
        left = self._get(node, 'left')
        right = self._get(node, 'right')
        op = self._get(node, 'op')

        # x + 0 → x
        if op == '+':
            if self._is_zero(right):
                self.optimizations_applied.append("表达式简化: x + 0")
                return left
            if self._is_zero(left):
                self.optimizations_applied.append("表达式简化: 0 + x")
                return right

        # x - 0 → x
        if op == '-' and self._is_zero(right):
            self.optimizations_applied.append("表达式简化: x - 0")
            return left

        # x * 1 → x，x * 0 → 0
        if op == '*':
            if self._is_one(right):
                self.optimizations_applied.append("表达式简化: x * 1")
                return left
            if self._is_one(left):
                self.optimizations_applied.append("表达式简化: 1 * x")
                return right
            if self._is_zero(left) or self._is_zero(right):
                self.optimizations_applied.append("表达式简化: x * 0")
                return ASTNode('Number', {'value': 0})

        # x / 1 → x
        if op == '/' and self._is_one(right):
            self.optimizations_applied.append("表达式简化: x / 1")
            return left

        # x && true → x，x && false → false
        if op == '&&':
            if self._is_true_condition(right):
                self.optimizations_applied.append("表达式简化: x && true")
                return left
            if self._is_false_condition(right):
                self.optimizations_applied.append("表达式简化: x && false")
                return right

        # x || false → x，x || true → true
        if op == '||':
            if self._is_false_condition(right):
                self.optimizations_applied.append("表达式简化: x || false")
                return left
            if self._is_true_condition(right):
                self.optimizations_applied.append("表达式简化: x || true")
                return right

        return node

    def _is_true_condition(self, node: ASTNode) -> bool:
        """检查条件是否总是 true"""
        if node.node_type == 'Boolean':
            return self._get(node, 'value') is True
        return False

    # ═══════════════════════════════════════════════════════════════
    # 【辅助方法】
    # ═══════════════════════════════════════════════════════════════

    def _get(self, node: ASTNode, key: str, default=None):
        """从 ASTNode 获取属性"""
        if isinstance(node.value, dict):
            return node.value.get(key, default)
        return default

    def _is_constant(self, node: ASTNode) -> bool:
        """检查节点是否是常量"""
        if not isinstance(node, ASTNode):
            return False
        return node.node_type in ('Number', 'String', 'Boolean', 'Null')

    def _get_constant_value(self, node: ASTNode) -> Any:
        """获取常量值"""
        if node.node_type == 'Number':
            val = self._get(node, 'value')
            return float(val) if '.' in str(val) else int(val)
        elif node.node_type == 'String':
            return self._get(node, 'value', '')
        elif node.node_type == 'Boolean':
            return self._get(node, 'value', False)
        elif node.node_type == 'Null':
            return None
        return None

    def _is_zero(self, node: ASTNode) -> bool:
        """检查是否为 0"""
        if self._is_constant(node):
            val = self._get_constant_value(node)
            return val == 0
        return False

    def _is_one(self, node: ASTNode) -> bool:
        """检查是否为 1"""
        if self._is_constant(node):
            val = self._get_constant_value(node)
            return val == 1
        return False

    def get_optimization_report(self) -> Dict[str, Any]:
        """获取优化报告"""
        return {
            'level': self.level,
            'optimizations_applied': self.optimizations_applied,
            'total_optimizations': len(self.optimizations_applied)
        }


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-OPTIMIZER-v1.0"
__responsibility__ = "UID9622·不免责"
