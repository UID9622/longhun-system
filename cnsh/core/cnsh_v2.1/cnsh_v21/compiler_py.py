# -*- coding: utf-8 -*-
"""
CNSH v2.1 → Python 编译器（转译器）
DNA: #龍芯⚡️2026-06-29-CNSH-COMPILER-PY-v2.1
"""
from typing import Any, Dict, List, Optional, Set

from . import ast_nodes as ast
from .errors import CNSHRuntimeError


class PythonCompiler:
    """将 CNSH AST 转译为可执行的 Python 3 源码。"""

    INDENT = "    "

    def __init__(self):
        self.indent_level = 0
        self.module_stack: List[str] = []
        self.module_members: Set[str] = set()

    # 中文关键字 -> Python 关键字/名称映射
    _DECORATOR_MAP = {
        "数据类": "dataclasses.dataclass",
        "枚举唯一": "enum.unique",
        "属性": "property",
        "类方法": "classmethod",
        "静态方法": "staticmethod",
        "抽象方法": "abc.abstractmethod",
    }
    _TYPE_MAP = {
        "整数": "int",
        "小数": "float",
        "浮点": "float",
        "文本": "str",
        "字符串": "str",
        "布尔": "bool",
        "列表": "list",
        "映射": "dict",
    }
    _KWARG_MAP = {
        "默认工厂": "default_factory",
        "默认值": "default",
        "比较": "compare",
        "哈希": "hash",
        "表示": "repr",
    }

    def compile(self, program: ast.Program) -> str:
        has_braket = any(
            isinstance(s, (ast.PersonaBasisDecl, ast.SystemDecl))
            for s in program.statements
        )
        lines = [
            "# -*- coding: utf-8 -*-",
            "# 由 CNSH v2.1 编译器自动生成",
            "import abc",
            "import asyncio",
            "import contextlib",
            "import dataclasses",
            "import enum",
            "import math",
            "",
            "from dataclasses import dataclass, field",
            "from cnsh_v21.stdlib import STDLIB",
            "龍 = STDLIB['龍']",
            "输出 = print",
            "打印 = print",
            "输入 = input",
            "长度 = len",
            "字符串 = str",
            "整数 = int",
            "小数 = float",
            "浮点 = float",
            "列表 = list",
            "范围 = range",
            "平方根 = math.sqrt",
            "圆周率 = math.pi",
            "例外 = Exception",
            "全局变量 = globals",
            "字段 = field",
            "无 = None",
            "真 = True",
            "假 = False",
            "打开 = open",
            "",
        ]
        if has_braket:
            lines.extend([
                "# Bra-Ket 人格协作运行时注入",
                "import sys, pathlib",
                "_lh_root = pathlib.Path.home() / 'longhun-system'",
                "if str(_lh_root) not in sys.path: sys.path.insert(0, str(_lh_root))",
                "import longhun_braket",
                "__BRAKET_PERSONAS__ = []",
                "",
            ])
        for stmt in program.statements:
            lines.extend(self._emit(stmt))
        return "\n".join(lines)

    def _emit(self, node: ast.ASTNode) -> List[str]:
        method = getattr(self, f"_emit_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"编译器未实现节点: {type(node).__name__}")
        return method(node)

    def _indent(self, lines: List[str]) -> List[str]:
        prefix = self.INDENT * self.indent_level
        return [prefix + line if line else line for line in lines]

    def _emit_Program(self, node: ast.Program) -> List[str]:
        result = []
        for stmt in node.statements:
            result.extend(self._emit(stmt))
        return result

    def _emit_ModuleDecl(self, node: ast.ModuleDecl) -> List[str]:
        self.module_stack.append(node.name)
        prev_members = self.module_members
        self.module_members = {s.name for s in node.body if isinstance(s, ast.FunctionDecl)}
        self.module_members.update(s.name for s in node.body if isinstance(s, ast.VarDecl))

        lines = [f"class {node.name}:", f'{self.INDENT}"""模块 {node.name}{f" ⚖️{node.weight}" if node.weight else ""}"""']
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1

        self.module_stack.pop()
        self.module_members = prev_members
        return lines

    def _emit_FunctionDecl(self, node: ast.FunctionDecl) -> List[str]:
        params = ", ".join(p.name for p in node.params)
        is_module_method = bool(self.module_stack)
        lines = []
        if is_module_method:
            lines.append("@staticmethod")
        lines.append(f"def {node.name}({params}):")
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_VarDecl(self, node: ast.VarDecl) -> List[str]:
        rhs = self._expr(node.initializer) if node.initializer else "None"
        return [f"{node.name} = {rhs}"]

    def _emit_StructDecl(self, node: ast.StructDecl) -> List[str]:
        fields = ", ".join(f.name for f in node.fields)
        lines = [f"def {node.name}({fields}):"]
        self.indent_level += 1
        dict_items = ", ".join(f'"{f.name}": {f.name}' for f in node.fields)
        lines.extend(self._indent([f'return {{"__类型__": "{node.name}", {dict_items}}}']))
        self.indent_level -= 1
        return lines

    def _emit_UseStmt(self, node: ast.UseStmt) -> List[str]:
        # Python FFI
        if node.module_path[0] in ("Python", "python", "外部"):
            py_path = ".".join(node.module_path[1:])
            alias = node.module_path[-1]
            return [f"import {py_path} as {alias}"]
        return [f"# 使用 {' '.join(node.module_path)}"]

    def _emit_IfStmt(self, node: ast.IfStmt) -> List[str]:
        lines = [f"if {self._expr(node.condition)}:"]
        self.indent_level += 1
        then_lines = []
        for stmt in node.then_body:
            then_lines.extend(self._emit(stmt))
        if not then_lines:
            then_lines = ["pass"]
        lines.extend(self._indent(then_lines))
        self.indent_level -= 1
        for branch in node.elif_branches:
            lines.append(f"elif {self._expr(branch.condition)}:")
            self.indent_level += 1
            branch_lines = []
            for stmt in branch.body:
                branch_lines.extend(self._emit(stmt))
            if not branch_lines:
                branch_lines = ["pass"]
            lines.extend(self._indent(branch_lines))
            self.indent_level -= 1
        if node.else_body:
            lines.append("else:")
            self.indent_level += 1
            else_lines = []
            for stmt in node.else_body:
                else_lines.extend(self._emit(stmt))
            if not else_lines:
                else_lines = ["pass"]
            lines.extend(self._indent(else_lines))
            self.indent_level -= 1
        return lines

    def _emit_WhileStmt(self, node: ast.WhileStmt) -> List[str]:
        lines = [f"while {self._expr(node.condition)}:"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_ForStmt(self, node: ast.ForStmt) -> List[str]:
        lines = [f"for {node.var_name} in {self._expr(node.iterable)}:"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_ReturnStmt(self, node: ast.ReturnStmt) -> List[str]:
        if node.value:
            return [f"return {self._expr(node.value)}"]
        return ["return"]

    def _emit_BreakStmt(self, _):
        return ["break"]

    def _emit_ContinueStmt(self, _):
        return ["continue"]

    def _emit_ExpressionStmt(self, node: ast.ExpressionStmt) -> List[str]:
        return [self._expr(node.expression)]

    def _emit_Decorator(self, node: ast.Decorator) -> str:
        name = self._DECORATOR_MAP.get(node.name, node.name)
        args = ", ".join(self._emit_arg(a) for a in node.args)
        if args:
            return f"@{name}({args})"
        return f"@{name}"

    def _emit_ClassDecl(self, node: ast.ClassDecl) -> List[str]:
        lines: List[str] = []
        for d in node.decorators:
            lines.append(self._emit_Decorator(d))
        base = f"({node.base})" if node.base else ""
        lines.append(f"class {node.name}{base}:")
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_MethodDecl(self, node: ast.MethodDecl) -> List[str]:
        lines: List[str] = []
        for d in node.decorators:
            lines.append(self._emit_Decorator(d))
        params = ", ".join(p.name for p in node.params)
        name = "__init__" if node.name == "初始化" else node.name
        async_prefix = "async " if node.is_async else ""
        lines.append(f"{async_prefix}def {name}({params}):")
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_YieldStmt(self, node: ast.YieldStmt) -> List[str]:
        if node.value:
            return [f"yield {self._expr(node.value)}"]
        return ["yield"]

    def _emit_YieldFromStmt(self, node: ast.YieldFromStmt) -> List[str]:
        return [f"yield from {self._expr(node.value)}"]

    def _emit_TryStmt(self, node: ast.TryStmt) -> List[str]:
        lines = ["try:"]
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        for clause in node.except_clauses:
            exc = ""
            if clause.exc_type:
                exc = clause.exc_type
            if clause.alias:
                exc = f"{exc} as {clause.alias}"
            if exc:
                lines.append(f"except {exc}:")
            else:
                lines.append("except:")
            self.indent_level += 1
            clause_lines: List[str] = []
            for stmt in clause.body:
                clause_lines.extend(self._emit(stmt))
            if not clause_lines:
                clause_lines = ["pass"]
            lines.extend(self._indent(clause_lines))
            self.indent_level -= 1
        if node.finally_body:
            lines.append("finally:")
            self.indent_level += 1
            finally_lines: List[str] = []
            for stmt in node.finally_body:
                finally_lines.extend(self._emit(stmt))
            if not finally_lines:
                finally_lines = ["pass"]
            lines.extend(self._indent(finally_lines))
            self.indent_level -= 1
        return lines

    def _emit_RaiseStmt(self, node: ast.RaiseStmt) -> List[str]:
        if node.value:
            return [f"raise {self._expr(node.value)}"]
        return ["raise"]

    def _emit_PassStmt(self, _: ast.PassStmt) -> List[str]:
        return ["pass"]

    def _emit_WithStmt(self, node: ast.WithStmt) -> List[str]:
        items = ", ".join(self._with_item(i) for i in node.items)
        lines = [f"with {items}:"]
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_AsyncWithStmt(self, node: ast.AsyncWithStmt) -> List[str]:
        items = ", ".join(self._with_item(i) for i in node.items)
        lines = [f"async with {items}:"]
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _with_item(self, node: ast.WithItem) -> str:
        s = self._expr(node.context_expr)
        if node.var_name:
            s = f"{s} as {node.var_name}"
        return s

    def _emit_AsyncForStmt(self, node: ast.AsyncForStmt) -> List[str]:
        lines = [f"async for {node.var_name} in {self._expr(node.iterable)}:"]
        self.indent_level += 1
        body_lines: List[str] = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_GeneratorExpr(self, node: ast.GeneratorExpr) -> List[str]:
        raise CNSHRuntimeError("生成器表达式只能出现在表达式上下文中")

    def _emit_EnumDecl(self, node: ast.EnumDecl) -> List[str]:
        lines: List[str] = []
        if node.unique:
            lines.append("@enum.unique")
        base = "enum.Enum"
        if node.base and node.base != "枚举类":
            base = node.base
        lines.append(f"class {node.name}({base}):")
        self.indent_level += 1
        body_lines: List[str] = []
        for member in node.members:
            body_lines.extend(self._emit(member))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_EnumMember(self, node: ast.EnumMember) -> List[str]:
        return [f"{node.name} = {self._expr(node.value)}"]

    def _emit_DataClassDecl(self, node: ast.DataClassDecl) -> List[str]:
        lines: List[str] = []
        for d in node.decorators:
            lines.append(self._emit_Decorator(d))
        lines.append(f"class {node.name}:")
        self.indent_level += 1
        body_lines: List[str] = []
        for field in node.fields:
            body_lines.extend(self._emit(field))
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["pass"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        return lines

    def _emit_DataClassField(self, node: ast.DataClassField) -> List[str]:
        ann = self._TYPE_MAP.get(node.type_annotation, node.type_annotation) if node.type_annotation else ""
        if node.default:
            return [f"{node.name}: {ann} = {self._expr(node.default)}"]
        return [f"{node.name}: {ann}"]

    def _emit_ImportStmt(self, node: ast.ImportStmt) -> List[str]:
        if node.is_from:
            names = ", ".join(node.names)
            return [f"from {node.module} import {names}"]
        module = node.module
        if module == "龍":
            return ["# 龍 标准库已预加载"]
        if module.startswith("Python."):
            py_mod = module.split(".", 1)[1]
            alias = py_mod.split(".")[-1]
            return [f"import {py_mod} as {alias}"]
        return [f"import {module}"]

    # ---------- Bra-Ket 人格协作转译 ----------

    def _emit_PersonaBasisDecl(self, node: ast.PersonaBasisDecl) -> List[str]:
        fields: Dict[str, Any] = {}
        for pair in node.fields:
            key = ""
            if isinstance(pair.key, ast.IdentifierExpr):
                key = pair.key.name
            elif isinstance(pair.key, ast.LiteralExpr) and isinstance(pair.key.value, str):
                key = pair.key.value
            value = self._expr(pair.value) if pair.value else "None"
            fields[key] = value
        name = fields.get("名字", repr(node.name))
        role = fields.get("角色", "''")
        duty = fields.get("职责", "''")
        weight = fields.get("权重", "0.5")
        return [
            f"__BRAKET_PERSONAS__.append({{"
            f'"name": {name}, "role": {role}, "duty": {duty}, "weight": {weight}'
            f"}})",
        ]

    def _emit_SystemDecl(self, node: ast.SystemDecl) -> List[str]:
        # 人格空间字段暂用于文档/校验，引擎使用全部已声明人格基态
        return [
            f"_braket_weights = [p.get('weight', 0.5) for p in __BRAKET_PERSONAS__]",
            f"{node.name} = longhun_braket.龍魂BraKet引擎(personas=__BRAKET_PERSONAS__, weights=_braket_weights, use_registry=False)",
        ]

    # ---------- 表达式转译 ----------

    def _expr(self, node: Optional[ast.ASTNode]) -> str:
        if node is None:
            return "None"
        method = getattr(self, f"_expr_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"编译器未实现表达式: {type(node).__name__}")
        return method(node)

    def _expr_LiteralExpr(self, node: ast.LiteralExpr) -> str:
        if isinstance(node.value, str):
            return repr(node.value)
        if isinstance(node.value, bool):
            return "True" if node.value else "False"
        if node.value is None:
            return "None"
        return str(node.value)

    def _expr_IdentifierExpr(self, node: ast.IdentifierExpr) -> str:
        # 模块内函数/变量：若当前在模块中且名称为模块成员，使用 __class__ 解析
        if self.module_stack and node.name in self.module_members:
            return f"__class__.{node.name}"
        return node.name

    def _expr_BinaryExpr(self, node: ast.BinaryExpr) -> str:
        op = node.op
        if op == "=":
            return f"{self._expr(node.left)} = {self._expr(node.right)}"
        op_map = {
            "且": "and", "或": "or", "非": "not",
        }
        py_op = op_map.get(op, op)
        return f"({self._expr(node.left)} {py_op} {self._expr(node.right)})"

    def _expr_UnaryExpr(self, node: ast.UnaryExpr) -> str:
        op = node.op
        if op in ("!", "非"):
            return f"(not {self._expr(node.operand)})"
        return f"({op}{self._expr(node.operand)})"

    def _expr_CallExpr(self, node: ast.CallExpr) -> str:
        callee = self._expr(node.callee)
        if isinstance(node.callee, ast.IdentifierExpr) and node.callee.name == "超类":
            callee = "super"
        args = ", ".join(self._emit_arg(a) for a in node.args)
        return f"{callee}({args})"

    def _emit_arg(self, node: ast.ASTNode) -> str:
        if (
            isinstance(node, ast.BinaryExpr)
            and node.op == "="
            and isinstance(node.left, ast.IdentifierExpr)
        ):
            name = self._KWARG_MAP.get(node.left.name, node.left.name)
            return f"{name}={self._expr(node.right)}"
        return self._expr(node)

    def _expr_MemberExpr(self, node: ast.MemberExpr) -> str:
        member = "__init__" if node.member == "初始化" else node.member
        return f"{self._expr(node.object)}.{member}"

    def _expr_IndexExpr(self, node: ast.IndexExpr) -> str:
        return f"{self._expr(node.object)}[{self._expr(node.index)}]"

    def _expr_ListExpr(self, node: ast.ListExpr) -> str:
        items = ", ".join(self._expr(e) for e in node.elements)
        return f"[{items}]"

    def _expr_MapExpr(self, node: ast.MapExpr) -> str:
        items = ", ".join(f"{self._expr(p.key)}: {self._expr(p.value)}" for p in node.pairs)
        return f"{{{items}}}"

    def _expr_AwaitExpr(self, node: ast.AwaitExpr) -> str:
        return f"await {self._expr(node.value)}"

    def _expr_GeneratorExpr(self, node: ast.GeneratorExpr) -> str:
        element = self._expr(node.element)
        iterable = self._expr(node.iterable)
        if node.condition:
            condition = self._expr(node.condition)
            return f"({element} for {node.var_name} in {iterable} if {condition})"
        return f"({element} for {node.var_name} in {iterable})"
