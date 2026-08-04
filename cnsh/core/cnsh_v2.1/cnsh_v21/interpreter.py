#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
CNSH v2.1 解释器（树遍历执行）
DNA: #龍芯⚡️2026-06-29-CNSH-INTERPRETER-v2.1
"""
from typing import Any, Dict, List, Optional

from . import ast_nodes as ast
from .errors import CNSHRuntimeError
from .stdlib import STDLIB, CNSHModule


class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class CNSHFunction:
    def __init__(self, decl: ast.FunctionDecl, closure: "Environment"):
        self.decl = decl
        self.closure = closure
        self.name = decl.name

    def __repr__(self) -> str:
        return f"<CNSH函数 {self.name}>"


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.values: Dict[str, Any] = {}
        self.consts: set[Any] = set()

    def define(self, name: str, value: Any, is_const: bool = False):
        self.values[name] = value
        if is_const:
            self.consts.add(name)

    def assign(self, name: str, value: Any):
        if name in self.values:
            if name in self.consts:
                raise CNSHRuntimeError(f"常量 {name} 不可重新赋值")
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise CNSHRuntimeError(f"未定义的变量: {name}")

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise CNSHRuntimeError(f"未定义的标识符: {name}")

    def contains(self, name: str) -> bool:
        if name in self.values:
            return True
        if self.parent:
            return self.parent.contains(name)
        return False


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.env = self.globals
        self._load_stdlib()
        self.last_value: Any = None
        self._braket_personas: List[Dict[str, Any]] = []

    def _load_stdlib(self):
        for name, module in STDLIB.items():
            self.globals.define(name, module)
        # 内置函数（中文别名）
        self.globals.define("输出", print)
        self.globals.define("打印", print)
        self.globals.define("输入", input)
        self.globals.define("长度", len)
        self.globals.define("类型", type)
        self.globals.define("字符串", str)
        self.globals.define("整数", int)
        self.globals.define("浮点", float)
        self.globals.define("小数", float)
        self.globals.define("列表", list)
        self.globals.define("字典", dict)
        self.globals.define("范围", range)

    def run(self, program: ast.Program) -> Any:
        for stmt in program.statements:
            self.last_value = self._execute(stmt)
        return self.last_value

    def _execute(self, node: ast.ASTNode) -> Any:
        method = getattr(self, f"_exec_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"未实现的语句类型: {type(node).__name__}")
        return method(node)

    def _exec_Program(self, node: ast.Program) -> Any:
        return self.run(node)

    def _exec_ModuleDecl(self, node: ast.ModuleDecl) -> CNSHModule:
        module = CNSHModule(node.name)
        prev = self.env
        module_env = Environment(prev)
        self.env = module_env
        try:
            for stmt in node.body:
                self._execute(stmt)
        finally:
            self.env = prev
        # 将子环境中顶层函数/变量注册为模块成员
        for name, value in module_env.values.items():
            module.register(name, value)
        self.env.define(node.name, module)
        return module

    def _exec_FunctionDecl(self, node: ast.FunctionDecl) -> CNSHFunction:
        func = CNSHFunction(node, self.env)
        self.env.define(node.name, func)
        return func

    def _exec_VarDecl(self, node: ast.VarDecl) -> Any:
        value = None
        if node.initializer:
            value = self._evaluate(node.initializer)
        self.env.define(node.name, value, is_const=node.is_const)
        return value

    def _exec_StructDecl(self, node: ast.StructDecl):
        # 简化为字典工厂函数
        def factory(**kwargs):
            return {"__类型__": node.name, **kwargs}
        factory.__name__ = node.name
        self.env.define(node.name, factory)
        return factory

    def _exec_UseStmt(self, node: ast.UseStmt) -> Any:
        path = ".".join(node.module_path)
        if path == "龍":
            return self.globals.get("龍")
        return self._exec_import_path(node.module_path)

    def _exec_ImportStmt(self, node: ast.ImportStmt) -> Any:
        if node.module == "龍":
            obj = self.globals.get("龍")
            self.env.define(node.alias or "龍", obj)
            return obj
        if node.is_from:
            return self._exec_import_from(node.module, node.names)
        return self._exec_import_path(node.module.split("."), alias=node.alias)

    def _exec_PersonaBasisDecl(self, node: ast.PersonaBasisDecl) -> Any:
        fields: Dict[str, Any] = {}
        for pair in node.fields:
            key = ""
            if isinstance(pair.key, ast.IdentifierExpr):
                key = pair.key.name
            elif isinstance(pair.key, ast.LiteralExpr):
                key = pair.key.value
            value = self._evaluate(pair.value) if pair.value else None
            fields[key] = value
        self._braket_personas.append({
            "name": node.name,
            "role": fields.get("角色", ""),
            "duty": fields.get("职责", ""),
            "weight": float(fields.get("权重", 0.5)),
        })
        return None

    def _exec_SystemDecl(self, node: ast.SystemDecl) -> Any:
        import sys
        import pathlib
        lh_root = pathlib.Path.home() / "longhun-system"
        if str(lh_root) not in sys.path:
            sys.path.insert(0, str(lh_root))
        import longhun_braket
        weights = [p.get("weight", 0.5) for p in self._braket_personas]
        engine = longhun_braket.龍魂BraKet引擎(
            personas=self._braket_personas,
            weights=weights,
            use_registry=False,
        )
        self.env.define(node.name, engine)
        return engine

    def _exec_import_path(self, module_path: List[str], alias: Optional[str] = None) -> Any:
        path = ".".join(module_path)
        if not module_path:
            raise CNSHRuntimeError("导入路径为空")
        if module_path[0] == "龍":
            obj = self.globals.get("龍")
            for part in module_path[1:]:
                if isinstance(obj, CNSHModule):
                    obj = obj.get(part)
                elif isinstance(obj, dict):
                    obj = obj[part]
                else:
                    raise CNSHRuntimeError(f"无法导入模块路径: {path}")
            self.env.define(alias or module_path[-1], obj)
            return obj
        if module_path[0] in ("Python", "python", "外部"):
            return self._import_python_module(module_path, alias=alias)
        import importlib
        try:
            mod = importlib.import_module(path)
        except Exception as exc:
            raise CNSHRuntimeError(f"导入失败: {path}: {exc}")
        self.env.define(alias or module_path[-1], mod)
        return mod

    def _exec_import_from(self, module: str, names: List[str]) -> Any:
        import importlib
        try:
            mod = importlib.import_module(module)
        except Exception as exc:
            raise CNSHRuntimeError(f"从导入失败: {module}: {exc}")
        for name in names:
            if not hasattr(mod, name):
                raise CNSHRuntimeError(f"模块 {module} 不存在成员: {name}")
            self.env.define(name, getattr(mod, name))
        return mod

    def _import_python_module(self, module_path: List[str], alias: Optional[str] = None):
        """Python FFI：导入 Python 模块并注册到当前环境。"""
        import importlib
        # module_path e.g. ['Python', 'math'] or ['外部', 'os', 'path']
        py_path = ".".join(module_path[1:])
        try:
            mod = importlib.import_module(py_path)
        except Exception as exc:
            raise CNSHRuntimeError(f"Python FFI 导入失败: {py_path}: {exc}")
        self.env.define(alias or module_path[-1], mod)
        return mod

    def _exec_IfStmt(self, node: ast.IfStmt) -> Any:
        cond = self._evaluate(node.condition)
        if self._is_truthy(cond):
            return self._execute_block(node.then_body)
        for branch in node.elif_branches:
            if self._is_truthy(self._evaluate(branch.condition)):
                return self._execute_block(branch.body)
        if node.else_body:
            return self._execute_block(node.else_body)
        return None

    def _exec_WhileStmt(self, node: ast.WhileStmt) -> Any:
        while self._is_truthy(self._evaluate(node.condition)):
            try:
                self._execute_block(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return None

    def _exec_ForStmt(self, node: ast.ForStmt) -> Any:
        iterable = self._evaluate(node.iterable)
        if not hasattr(iterable, "__iter__"):
            raise CNSHRuntimeError("对于循环需要可迭代对象")
        for item in iterable:
            self.env.define(node.var_name, item)
            try:
                self._execute_block(node.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return None

    def _exec_ReturnStmt(self, node: ast.ReturnStmt):
        value = None
        if node.value:
            value = self._evaluate(node.value)
        raise ReturnSignal(value)

    def _exec_BreakStmt(self, _):
        raise BreakSignal()

    def _exec_ContinueStmt(self, _):
        raise ContinueSignal()

    def _exec_PassStmt(self, _):
        return None

    def _exec_ExpressionStmt(self, node: ast.ExpressionStmt) -> Any:
        return self._evaluate(node.expression)

    def _execute_block(self, body: List[ast.ASTNode]) -> Any:
        result = None
        for stmt in body:
            result = self._execute(stmt)
        return result

    def _evaluate(self, node: Optional[ast.ASTNode]) -> Any:
        if node is None:
            return None
        method = getattr(self, f"_eval_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"未实现的表达式类型: {type(node).__name__}")
        return method(node)

    def _eval_LiteralExpr(self, node: ast.LiteralExpr):
        return node.value

    def _eval_IdentifierExpr(self, node: ast.IdentifierExpr):
        return self.env.get(node.name)

    def _eval_BinaryExpr(self, node: ast.BinaryExpr) -> Any:
        op = node.op
        if op == "=":
            if not isinstance(node.left, ast.IdentifierExpr):
                raise CNSHRuntimeError("赋值左侧必须是标识符")
            value = self._evaluate(node.right)
            if self.env.contains(node.left.name):
                self.env.assign(node.left.name, value)
            else:
                # 隐式变量声明：与编译目标 Python 保持一致
                self.env.define(node.left.name, value)
            return value

        left = self._evaluate(node.left)
        right = self._evaluate(node.right)

        if op in ("+", "加"):
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op in ("-", "减"):
            return left - right
        if op in ("*", "乘"):
            return left * right
        if op in ("/", "除"):
            if right == 0:
                raise CNSHRuntimeError("除零错误")
            return left / right
        if op in ("%", "取模"):
            return left % right
        if op in ("==", "等于"):
            return left == right
        if op in ("!=", "不等于"):
            return left != right
        if op in ("<", "小于"):
            return left < right
        if op in (">", "大于"):
            return left > right
        if op in ("<=", "小于等于"):
            return left <= right
        if op in (">=", "大于等于"):
            return left >= right
        if op in ("&&", "且"):
            return self._is_truthy(left) and self._is_truthy(right)
        if op in ("||", "或"):
            return self._is_truthy(left) or self._is_truthy(right)

        raise CNSHRuntimeError(f"未知运算符: {op}")

    def _eval_UnaryExpr(self, node: ast.UnaryExpr) -> Any:
        op = node.op
        operand = self._evaluate(node.operand)
        if op in ("!", "非"):
            return not self._is_truthy(operand)
        if op == "-":
            return -operand
        if op == "+":
            return +operand
        raise CNSHRuntimeError(f"未知一元运算符: {op}")

    def _eval_CallExpr(self, node: ast.CallExpr) -> Any:
        callee = self._evaluate(node.callee)
        args = [self._evaluate(a) for a in node.args]
        return self._call(callee, args)

    def _call(self, callee: Any, args: List[Any]) -> Any:
        if isinstance(callee, CNSHFunction):
            return self._call_cnsh_function(callee, args)
        if callable(callee):
            return callee(*args)
        raise CNSHRuntimeError(f"不可调用的对象: {callee!r}")

    def _call_cnsh_function(self, func: CNSHFunction, args: List[Any]) -> Any:
        if len(args) != len(func.decl.params):
            raise CNSHRuntimeError(
                f"函数 {func.decl.name} 需要 {len(func.decl.params)} 个参数，但得到 {len(args)}"
            )
        env = Environment(func.closure)
        for param, arg in zip(func.decl.params, args):
            env.define(param.name, arg)
        prev = self.env
        self.env = env
        try:
            self._execute_block(func.decl.body)
        except ReturnSignal as sig:
            return sig.value
        finally:
            self.env = prev
        return None

    def _eval_MemberExpr(self, node: ast.MemberExpr) -> Any:
        obj = self._evaluate(node.object)
        member = node.member
        if isinstance(obj, CNSHModule):
            return obj.get(member)
        if isinstance(obj, dict):
            if member not in obj:
                raise CNSHRuntimeError(f"映射中不存在键: {member}")
            return obj[member]
        if hasattr(obj, member):
            return getattr(obj, member)
        raise CNSHRuntimeError(f"对象不存在成员: {member}")

    def _eval_IndexExpr(self, node: ast.IndexExpr) -> Any:
        obj = self._evaluate(node.object)
        idx = self._evaluate(node.index)
        try:
            return obj[idx]
        except Exception as exc:
            raise CNSHRuntimeError(f"索引访问失败: {exc}")

    def _eval_ListExpr(self, node: ast.ListExpr) -> List[Any]:
        return [self._evaluate(e) for e in node.elements]

    def _eval_MapExpr(self, node: ast.MapExpr) -> Dict[Any, Any]:
        result = {}
        for pair in node.pairs:
            key = self._evaluate(pair.key)
            value = self._evaluate(pair.value)
            result[key] = value
        return result

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (list, dict, str)):
            return len(value) != 0
        return True
