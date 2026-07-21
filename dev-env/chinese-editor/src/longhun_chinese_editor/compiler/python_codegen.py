#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH → Python 代码生成器
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-PYTHON-CODEGEN-v1.0
"""
from __future__ import annotations

import re
from typing import Any, List

from . import ast_nodes as ast


INTERP_RE = re.compile(
    r"\{[A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*\}"
)

BUILTIN_MAP = {
    "输入": "input",
    "范围": "range",
    "长度": "len",
    "打印": "print",
    "枚举": "enumerate",
    "映射": "map",
    "过滤": "filter",
    "求和": "sum",
    "最大值": "max",
    "最小值": "min",
    "绝对值": "abs",
    "四舍五入": "round",
    "类型": "type",
    "字符串": "str",
    "整数": "int",
    "浮点": "float",
    "排序": "sorted",
    "反转": "reversed",
    "打开": "open",
    "继承": "isinstance",
    "取属性": "getattr",
    "设属性": "setattr",
    "是否有属性": "hasattr",
    "布尔": "bool",
    "列表": "list",
    "字典": "dict",
    "元组": "tuple",
    "集合": "set",
}

METHOD_MAP = {
    "添加": "append",
    "扩展": "extend",
    "插入": "insert",
    "移除": "remove",
    "弹出": "pop",
    "清空": "clear",
    "索引": "index",
    "计数": "count",
    "排序自身": "sort",
    "反转自身": "reverse",
    "获取": "get",
    "更新": "update",
    "设置默认": "setdefault",
    "弹出项": "popitem",
    "键列表": "keys",
    "值列表": "values",
    "项列表": "items",
    "分割": "split",
    "去空白": "strip",
    "去左空白": "lstrip",
    "去右空白": "rstrip",
    "替换文本": "replace",
    "以大写": "upper",
    "以小写": "lower",
    "以开头": "startswith",
    "以结尾": "endswith",
    "查找文本": "find",
    "连接": "join",
    "格式化文本": "format",
}

TYPE_MAP = {
    "整数": "int",
    "小数": "float",
    "文本": "str",
    "真假": "bool",
    "列表": "list",
    "字典": "dict",
    "空值": "None",
}


class PythonCodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []

    def _emit(self, line: str) -> None:
        self.lines.append("    " * self.indent_level + line)

    def _expr(self, node: ast.ASTNode) -> str:
        if isinstance(node, ast.Literal):
            if node.kind == "string":
                s = node.value
                if INTERP_RE.search(s):
                    # CNSH 字符串插值 -> Python f-string
                    if '"' in s:
                        return f"f'{s}'"
                    return f'f"{s}"'
                return repr(s)
            if node.kind == "bool":
                return "True" if node.value else "False"
            if node.kind == "null":
                return "None"
            return str(node.value)
        if isinstance(node, ast.Identifier):
            return BUILTIN_MAP.get(node.name, node.name)
        if isinstance(node, ast.BinaryOp):
            left = self._expr(node.left)
            right = self._expr(node.right)
            op = node.op
            if op in ("且", "并且"):
                op = "and"
            elif op in ("或", "或者"):
                op = "or"
            elif op == "非":
                op = "not"
            return f"({left} {op} {right})"
        if isinstance(node, ast.UnaryOp):
            operand = self._expr(node.operand)
            op = "-" if node.op == "-" else "not"
            return f"({op}{operand})"
        if isinstance(node, ast.Assignment):
            return f"{self._expr(node.target)} = {self._expr(node.value)}"
        if isinstance(node, ast.Call):
            args = ", ".join(self._expr(a) for a in node.args)
            name = node.name
            if "." in name:
                obj, member = name.rsplit(".", 1)
                member = METHOD_MAP.get(member, member)
                name = f"{obj}.{member}"
            else:
                name = BUILTIN_MAP.get(name, name)
            return f"{name}({args})"
        if isinstance(node, ast.MemberAccess):
            member = METHOD_MAP.get(node.member, node.member)
            return f"{self._expr(node.obj)}.{member}"
        if isinstance(node, ast.IndexAccess):
            return f"{self._expr(node.obj)}[{self._expr(node.index)}]"
        if isinstance(node, ast.ArrayLiteral):
            return "[" + ", ".join(self._expr(i) for i in node.items) + "]"
        if isinstance(node, ast.DictLiteral):
            pairs = ", ".join(f"{self._expr(k)}: {self._expr(v)}" for k, v in node.pairs)
            return "{" + pairs + "}"
        return repr(node)

    def _handle_else(self, branch: ast.ASTNode) -> None:
        if isinstance(branch, ast.IfStmt):
            cond = self._expr(branch.cond)
            self._emit(f"elif {cond}:")
            self.indent_level += 1
            self._visit(branch.true_branch)
            self.indent_level -= 1
            if branch.false_branch:
                self._handle_else(branch.false_branch)
        else:
            self._emit("else:")
            self.indent_level += 1
            self._visit(branch)
            self.indent_level -= 1

    def generate(self, program: ast.Program, include_main_guard: bool = False) -> str:
        self.indent_level = 0
        self.lines = []
        self._emit("# 由 longhun-chinese-editor 编译器生成")
        self._emit("# DNA: #龍芯⚡️2026-06-26-CNSH-GENERATED-PYTHON")
        has_main = False
        for decl in program.decls:
            if isinstance(decl, ast.FuncDecl) and decl.name == "主函数":
                has_main = True
            self._visit(decl)
        if include_main_guard and has_main:
            self._emit('if __name__ == "__main__":')
            self.indent_level += 1
            self._emit("主函数()")
            self.indent_level -= 1
        return "\n".join(self.lines)

    def _visit(self, node: ast.ASTNode) -> None:
        if isinstance(node, ast.Program):
            for decl in node.decls:
                self._visit(decl)
        elif isinstance(node, ast.FuncDecl):
            params = ", ".join(p["name"] for p in node.params)
            self._emit(f"def {node.name}({params}):")
            self.indent_level += 1
            self._visit(node.body)
            self.indent_level -= 1
            self._emit("")
        elif isinstance(node, ast.VarDecl):
            init = self._expr(node.init) if node.init else "None"
            self._emit(f"{node.name} = {init}")
        elif isinstance(node, ast.ClassDecl):
            self._emit(f"class {node.name}:")
            self.indent_level += 1
            for member in node.members:
                self._visit(member)
            if not node.members:
                self._emit("pass")
            self.indent_level -= 1
            self._emit("")
        elif isinstance(node, ast.Block):
            if not node.stmts:
                self._emit("pass")
            for stmt in node.stmts:
                self._visit(stmt)
        elif isinstance(node, ast.IfStmt):
            cond = self._expr(node.cond)
            self._emit(f"if {cond}:")
            self.indent_level += 1
            self._visit(node.true_branch)
            self.indent_level -= 1
            if node.false_branch:
                if isinstance(node.false_branch, ast.IfStmt):
                    cond2 = self._expr(node.false_branch.cond)
                    self._emit(f"elif {cond2}:")
                    self.indent_level += 1
                    self._visit(node.false_branch.true_branch)
                    self.indent_level -= 1
                    if node.false_branch.false_branch:
                        self._handle_else(node.false_branch.false_branch)
                else:
                    self._handle_else(node.false_branch)
        elif isinstance(node, ast.LoopStmt):
            count = self._expr(node.count)
            self._emit(f"for __cnshexpr in range(int({count})):")
            self.indent_level += 1
            self._visit(node.body)
            self.indent_level -= 1
        elif isinstance(node, ast.WhileStmt):
            cond = self._expr(node.cond)
            self._emit(f"while {cond}:")
            self.indent_level += 1
            self._visit(node.body)
            self.indent_level -= 1
        elif isinstance(node, ast.ForStmt):
            iterable = self._expr(node.iterable)
            self._emit(f"for {node.var} in {iterable}:")
            self.indent_level += 1
            self._visit(node.body)
            self.indent_level -= 1
        elif isinstance(node, ast.ReturnStmt):
            if node.value:
                self._emit(f"return {self._expr(node.value)}")
            else:
                self._emit("return")
        elif isinstance(node, ast.BreakStmt):
            self._emit("break")
        elif isinstance(node, ast.ContinueStmt):
            self._emit("continue")
        elif isinstance(node, ast.PrintStmt):
            args = ", ".join(self._expr(a) for a in node.args)
            self._emit(f"print({args})")
        elif isinstance(node, ast.ExprStmt):
            self._emit(self._expr(node.expr))
        elif isinstance(node, ast.ImportStmt):
            module = node.module
            if node.alias:
                self._emit(f"import {module} as {node.alias}")
            else:
                self._emit(f"import {module}")
        elif isinstance(node, ast.TryStmt):
            self._emit("try:")
            self.indent_level += 1
            self._visit(node.body)
            self.indent_level -= 1
            for catch in node.catches:
                if catch.exc_type:
                    self._emit(f"except {catch.exc_type}:")
                else:
                    self._emit("except Exception:")
                self.indent_level += 1
                self._visit(catch.body)
                self.indent_level -= 1
            if node.finally_body:
                self._emit("finally:")
                self.indent_level += 1
                self._visit(node.finally_body)
                self.indent_level -= 1
        else:
            self._emit(f"# 未生成: {type(node).__name__}")


def generate_python(program: ast.Program, include_main_guard: bool = False) -> str:
    return PythonCodeGenerator().generate(program, include_main_guard=include_main_guard)
