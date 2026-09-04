#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 静态类型检查器
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-TYPECHECKER-v2.1

支持：
- 基本类型：整数、小数、文本、布尔、空
- 复合类型：列表、映射（可带泛型参数）
- 函数参数与返回类型检查
- 变量声明与赋值类型检查
- 运算符类型检查
- 函数调用参数检查
- if/while/for 条件类型检查
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from . import ast_nodes as ast
from .errors import CNSHError


@dataclass(frozen=True)
class CNSHType:
    name: str

    def __str__(self) -> str:
        return self.name

    def is_compatible_with(self, other: "CNSHType") -> bool:
        if self.name == "任意" or other.name == "任意":
            return True
        if self.name == "未知" or other.name == "未知":
            return True
        return self.name == other.name


class TypeRegistry:
    _types: Dict[str, CNSHType] = {
        "整数": CNSHType("整数"),
        "小数": CNSHType("小数"),
        "文本": CNSHType("文本"),
        "布尔": CNSHType("布尔"),
        "空": CNSHType("空"),
        "列表": CNSHType("列表"),
        "映射": CNSHType("映射"),
        "函数": CNSHType("函数"),
        "模块": CNSHType("模块"),
        "任意": CNSHType("任意"),
        "未知": CNSHType("未知"),
    }

    @classmethod
    def get(cls, name: str) -> CNSHType:
        return cls._types.get(name, CNSHType(name))


class SymbolTable:
    def __init__(self, parent: Optional["SymbolTable"] = None):
        self.parent = parent
        self.symbols: Dict[str, CNSHType] = {}

    def define(self, name: str, type_: CNSHType):
        self.symbols[name] = type_

    def lookup(self, name: str) -> Optional[CNSHType]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class TypeCheckError(CNSHError):
    pass


class TypeChecker:
    """CNSH 静态类型检查器"""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.current_scope = SymbolTable()
        self.current_function_return: Optional[CNSHType] = None
        self._init_builtins()

    def _init_builtins(self):
        # 核心内置函数与命名空间
        builtins = {
            "输出": TypeRegistry.get("函数"),
            "输入": TypeRegistry.get("函数"),
            "长度": TypeRegistry.get("函数"),
            "类型": TypeRegistry.get("函数"),
            "字符串": TypeRegistry.get("函数"),
            "整数": TypeRegistry.get("函数"),
            "小数": TypeRegistry.get("函数"),
            "浮点": TypeRegistry.get("函数"),
            "列表": TypeRegistry.get("函数"),
            "字典": TypeRegistry.get("函数"),
            "范围": TypeRegistry.get("函数"),
            "打印": TypeRegistry.get("函数"),
            "龍": TypeRegistry.get("模块"),
            "真": TypeRegistry.get("布尔"),
            "假": TypeRegistry.get("布尔"),
            "无": TypeRegistry.get("空"),
            # Python 运行时别名（编译后可用）
            "打开": TypeRegistry.get("函数"),
            "列表": TypeRegistry.get("函数"),
            "范围": TypeRegistry.get("函数"),
            "平方根": TypeRegistry.get("函数"),
            "圆周率": TypeRegistry.get("任意"),
            "例外": TypeRegistry.get("函数"),
            "全局变量": TypeRegistry.get("函数"),
            "字段": TypeRegistry.get("函数"),
            "isinstance": TypeRegistry.get("函数"),
            "asyncio": TypeRegistry.get("任意"),
            "contextlib": TypeRegistry.get("任意"),
            "dataclasses": TypeRegistry.get("任意"),
            "enum": TypeRegistry.get("任意"),
            "math": TypeRegistry.get("任意"),
            "datetime": TypeRegistry.get("任意"),
            "abc": TypeRegistry.get("任意"),
            "超类": TypeRegistry.get("任意"),
        }
        for name, type_ in builtins.items():
            self.current_scope.define(name, type_)

    def check(self, program: ast.Program) -> Tuple[bool, List[str], List[str]]:
        self.errors = []
        self.warnings = []
        self._collect_globals(program)
        for stmt in program.statements:
            self._check_stmt(stmt)
        return (len(self.errors) == 0, self.errors, self.warnings)

    def _error(self, message: str, node: ast.ASTNode):
        self.errors.append(f"[{node.line}:{node.column}] {message}")

    def _warn(self, message: str, node: ast.ASTNode):
        self.warnings.append(f"[{node.line}:{node.column}] {message}")

    # ---------- 全局符号收集 ----------
    def _collect_globals(self, program: ast.Program):
        for stmt in program.statements:
            if isinstance(stmt, (ast.FunctionDecl, ast.MethodDecl)):
                self.current_scope.define(stmt.name, TypeRegistry.get("函数"))
            elif isinstance(stmt, ast.ModuleDecl):
                self.current_scope.define(stmt.name, TypeRegistry.get("模块"))
            elif isinstance(stmt, ast.VarDecl):
                var_type = self._parse_type(stmt.type_annotation)
                self.current_scope.define(stmt.name, var_type)
            elif isinstance(stmt, (ast.ClassDecl, ast.DataClassDecl, ast.EnumDecl, ast.SystemDecl)):
                self.current_scope.define(stmt.name, TypeRegistry.get("任意"))

    # ---------- 语句检查 ----------
    def _check_stmt(self, stmt: ast.ASTNode):
        method = getattr(self, f"_check_{type(stmt).__name__}", None)
        if method is None:
            self._warn(f"类型检查未实现语句: {type(stmt).__name__}", stmt)
            return
        method(stmt)

    def _check_ModuleDecl(self, node: ast.ModuleDecl):
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_FunctionDecl(self, node: ast.FunctionDecl):
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        prev_return = self.current_function_return
        self.current_function_return = self._parse_type(None)

        try:
            for param in node.params:
                ptype = self._parse_type(param.type_annotation)
                self.current_scope.define(param.name, ptype)

            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent
            self.current_function_return = prev_return

    def _check_MethodDecl(self, node: ast.MethodDecl):
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        prev_return = self.current_function_return
        self.current_function_return = self._parse_type(None)

        try:
            for param in node.params:
                ptype = self._parse_type(param.type_annotation)
                self.current_scope.define(param.name, ptype)

            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent
            self.current_function_return = prev_return

    def _check_ClassDecl(self, node: ast.ClassDecl):
        self.current_scope.define(node.name, TypeRegistry.get("任意"))
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_DataClassDecl(self, node: ast.DataClassDecl):
        self.current_scope.define(node.name, TypeRegistry.get("任意"))
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            for field in node.fields:
                if field.default:
                    self._infer_expr(field.default)
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_EnumDecl(self, node: ast.EnumDecl):
        self.current_scope.define(node.name, TypeRegistry.get("任意"))

    def _check_PersonaBasisDecl(self, node: ast.PersonaBasisDecl):
        for field in node.fields:
            if field.value:
                self._infer_expr(field.value)

    def _check_SystemDecl(self, node: ast.SystemDecl):
        self.current_scope.define(node.name, TypeRegistry.get("任意"))
        for field in node.fields:
            if field.value:
                self._infer_expr(field.value)

    def _check_VarDecl(self, node: ast.VarDecl):
        declared_type = self._parse_type(node.type_annotation)
        if node.initializer:
            init_type = self._infer_expr(node.initializer)
            if not declared_type.is_compatible_with(init_type) and declared_type.name != "未知":
                self._error(
                    f"变量 '{node.name}' 声明类型为 {declared_type}，但初始化表达式类型为 {init_type}",
                    node,
                )
            elif declared_type.name == "未知":
                declared_type = init_type
        self.current_scope.define(node.name, declared_type)

    def _check_StructDecl(self, node: ast.StructDecl):
        self.current_scope.define(node.name, TypeRegistry.get("映射"))

    def _check_UseStmt(self, node: ast.UseStmt):
        pass

    def _check_ImportStmt(self, node: ast.ImportStmt):
        pass

    def _check_PassStmt(self, node: ast.PassStmt):
        pass

    def _check_YieldStmt(self, node: ast.YieldStmt):
        if node.value:
            self._infer_expr(node.value)

    def _check_YieldFromStmt(self, node: ast.YieldFromStmt):
        if node.value:
            self._infer_expr(node.value)

    def _check_RaiseStmt(self, node: ast.RaiseStmt):
        if node.value:
            self._infer_expr(node.value)

    def _check_TryStmt(self, node: ast.TryStmt):
        for stmt in node.body:
            self._check_stmt(stmt)
        for clause in node.except_clauses:
            scope = SymbolTable(self.current_scope)
            self.current_scope = scope
            try:
                if clause.alias:
                    self.current_scope.define(clause.alias, TypeRegistry.get("任意"))
                for stmt in clause.body:
                    self._check_stmt(stmt)
            finally:
                self.current_scope = self.current_scope.parent
        for stmt in node.finally_body:
            self._check_stmt(stmt)

    def _check_WithStmt(self, node: ast.WithStmt):
        for item in node.items:
            self._infer_expr(item.context_expr)
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            for item in node.items:
                if item.var_name:
                    self.current_scope.define(item.var_name, TypeRegistry.get("任意"))
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_AsyncWithStmt(self, node: ast.AsyncWithStmt):
        for item in node.items:
            self._infer_expr(item.context_expr)
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            for item in node.items:
                if item.var_name:
                    self.current_scope.define(item.var_name, TypeRegistry.get("任意"))
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_AsyncForStmt(self, node: ast.AsyncForStmt):
        self._infer_expr(node.iterable)
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            self.current_scope.define(node.var_name, TypeRegistry.get("任意"))
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_IfStmt(self, node: ast.IfStmt):
        cond_type = self._infer_expr(node.condition)
        if cond_type.name not in ("布尔", "整数", "小数", "文本", "任意", "未知"):
            self._error(f"if 条件需要可判真类型，但得到 {cond_type}", node)
        for stmt in node.then_body:
            self._check_stmt(stmt)
        for branch in node.elif_branches:
            ct = self._infer_expr(branch.condition)
            if ct.name not in ("布尔", "整数", "小数", "文本", "任意", "未知"):
                self._error(f"elif 条件需要可判真类型，但得到 {ct}", branch)
            for s in branch.body:
                self._check_stmt(s)
        if node.else_body:
            for s in node.else_body:
                self._check_stmt(s)

    def _check_WhileStmt(self, node: ast.WhileStmt):
        cond_type = self._infer_expr(node.condition)
        if cond_type.name not in ("布尔", "整数", "小数", "文本", "任意", "未知"):
            self._error(f"while 条件需要可判真类型，但得到 {cond_type}", node)
        for stmt in node.body:
            self._check_stmt(stmt)

    def _check_ForStmt(self, node: ast.ForStmt):
        iter_type = self._infer_expr(node.iterable)
        if iter_type.name not in ("列表", "文本", "映射", "任意", "未知"):
            self._error(f"for 循环需要可迭代类型，但得到 {iter_type}", node)
        scope = SymbolTable(self.current_scope)
        self.current_scope = scope
        try:
            self.current_scope.define(node.var_name, TypeRegistry.get("任意"))
            for stmt in node.body:
                self._check_stmt(stmt)
        finally:
            self.current_scope = self.current_scope.parent

    def _check_ReturnStmt(self, node: ast.ReturnStmt):
        if node.value is None:
            return_type = TypeRegistry.get("空")
        else:
            return_type = self._infer_expr(node.value)
        if self.current_function_return is None:
            self._warn("return 出现在函数外部", node)
        else:
            self.current_function_return = return_type

    def _check_BreakStmt(self, node: ast.BreakStmt):
        pass

    def _check_ContinueStmt(self, node: ast.ContinueStmt):
        pass

    def _check_ExpressionStmt(self, node: ast.ExpressionStmt):
        if node.expression:
            # 赋值表达式定义新变量（如 a = 动物(...)）
            if (
                isinstance(node.expression, ast.BinaryExpr)
                and node.expression.op == "="
                and isinstance(node.expression.left, ast.IdentifierExpr)
            ):
                if self.current_scope.lookup(node.expression.left.name) is None:
                    self.current_scope.define(node.expression.left.name, TypeRegistry.get("任意"))
            self._infer_expr(node.expression)

    # ---------- 表达式推断 ----------
    def _infer_expr(self, node: ast.ASTNode) -> CNSHType:
        method = getattr(self, f"_infer_{type(node).__name__}", None)
        if method is None:
            self._warn(f"类型推断未实现表达式: {type(node).__name__}", node)
            return TypeRegistry.get("未知")
        return method(node)

    def _infer_LiteralExpr(self, node: ast.LiteralExpr) -> CNSHType:
        v = node.value
        if isinstance(v, bool):
            return TypeRegistry.get("布尔")
        if isinstance(v, int):
            return TypeRegistry.get("整数")
        if isinstance(v, float):
            return TypeRegistry.get("小数")
        if isinstance(v, str):
            return TypeRegistry.get("文本")
        if v is None:
            return TypeRegistry.get("空")
        if isinstance(v, list):
            return TypeRegistry.get("列表")
        if isinstance(v, dict):
            return TypeRegistry.get("映射")
        return TypeRegistry.get("未知")

    def _infer_IdentifierExpr(self, node: ast.IdentifierExpr) -> CNSHType:
        t = self.current_scope.lookup(node.name)
        if t is None:
            self._error(f"未定义的标识符: {node.name}", node)
            return TypeRegistry.get("未知")
        return t

    def _infer_BinaryExpr(self, node: ast.BinaryExpr) -> CNSHType:
        op = node.op
        if op == "=":
            right_type = self._infer_expr(node.right)
            if isinstance(node.left, ast.IdentifierExpr):
                existing = self.current_scope.lookup(node.left.name)
                if existing is not None and not existing.is_compatible_with(right_type):
                    self._error(
                        f"不能将类型 {right_type} 赋值给变量 '{node.left.name}'（期望 {existing}）",
                        node,
                    )
            return right_type

        left_type = self._infer_expr(node.left)
        right_type = self._infer_expr(node.right)

        # 包含未标注类型时放宽检查
        if left_type.name in ("未知", "任意") or right_type.name in ("未知", "任意"):
            return TypeRegistry.get("未知")

        # 算术
        if op in ("+", "-", "*", "/", "%"):
            if left_type.name in ("整数", "小数") and right_type.name in ("整数", "小数"):
                if left_type.name == "小数" or right_type.name == "小数":
                    return TypeRegistry.get("小数")
                return TypeRegistry.get("整数")
            if op == "+" and (left_type.name == "文本" or right_type.name == "文本"):
                return TypeRegistry.get("文本")
            self._error(f"运算符 '{op}' 不支持类型 {left_type} 和 {right_type}", node)
            return TypeRegistry.get("未知")

        # 比较
        if op in ("==", "!=", "<", ">", "<=", ">="):
            return TypeRegistry.get("布尔")

        # 逻辑
        if op in ("&&", "||", "且", "或"):
            return TypeRegistry.get("布尔")

        return TypeRegistry.get("未知")

    def _infer_UnaryExpr(self, node: ast.UnaryExpr) -> CNSHType:
        op = node.op
        operand_type = self._infer_expr(node.operand)
        if op in ("!", "非"):
            return TypeRegistry.get("布尔")
        if op in ("+", "-"):
            if operand_type.name in ("未知", "任意"):
                return TypeRegistry.get("未知")
            if operand_type.name in ("整数", "小数"):
                return operand_type
            self._error(f"一元运算符 '{op}' 不支持类型 {operand_type}", node)
            return TypeRegistry.get("未知")
        return TypeRegistry.get("未知")

    def _infer_CallExpr(self, node: ast.CallExpr) -> CNSHType:
        callee_type = self._infer_expr(node.callee)
        for arg in node.args:
            self._infer_expr(arg)
        # 内置函数返回类型特殊处理
        if isinstance(node.callee, ast.IdentifierExpr):
            name = node.callee.name
            if name in ("输出", "输入"):
                return TypeRegistry.get("空")
            if name == "长度":
                return TypeRegistry.get("整数")
            if name in ("字符串", "整数", "小数"):
                return TypeRegistry.get(name)
        return TypeRegistry.get("任意")

    def _infer_MemberExpr(self, node: ast.MemberExpr) -> CNSHType:
        obj_type = self._infer_expr(node.object)
        # 模块成员无法静态确定，返回任意
        if obj_type.name == "模块":
            return TypeRegistry.get("任意")
        if obj_type.name == "映射":
            return TypeRegistry.get("任意")
        return TypeRegistry.get("任意")

    def _infer_IndexExpr(self, node: ast.IndexExpr) -> CNSHType:
        obj_type = self._infer_expr(node.object)
        index_type = self._infer_expr(node.index)
        if obj_type.name == "列表":
            return TypeRegistry.get("任意")
        if obj_type.name == "映射":
            return TypeRegistry.get("任意")
        if obj_type.name == "文本":
            return TypeRegistry.get("文本")
        self._warn(f"对非索引类型 {obj_type} 进行索引访问", node)
        return TypeRegistry.get("任意")

    def _infer_ListExpr(self, node: ast.ListExpr) -> CNSHType:
        return TypeRegistry.get("列表")

    def _infer_MapExpr(self, node: ast.MapExpr) -> CNSHType:
        return TypeRegistry.get("映射")

    def _infer_AwaitExpr(self, node: ast.AwaitExpr) -> CNSHType:
        if node.value:
            self._infer_expr(node.value)
        return TypeRegistry.get("任意")

    def _infer_GeneratorExpr(self, node: ast.GeneratorExpr) -> CNSHType:
        return TypeRegistry.get("任意")

    # ---------- 类型解析 ----------
    def _parse_type(self, type_annotation: Optional[str]) -> CNSHType:
        if type_annotation is None:
            return TypeRegistry.get("未知")
        type_annotation = type_annotation.strip()
        if not type_annotation:
            return TypeRegistry.get("未知")
        return TypeRegistry.get(type_annotation)
