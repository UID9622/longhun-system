#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 → Rust 编译器
DNA: #龍芯⚡️2026-06-29-CNSH-COMPILER-RUST-v2.1

说明：本编译器将 CNSH 转译为 Rust，使用统一的 CnshValue 动态类型枚举，
      适合执行逻辑验证；性能敏感场景需后续静态类型增强。
"""
from typing import List, Optional, Set

from . import ast_nodes as ast
from .errors import CNSHRuntimeError


class RustCompiler:
    """CNSH → Rust 转译器"""

    INDENT = "    "

    def __init__(self):
        self.indent_level = 0
        self.module_stack: List[str] = []
        self.module_members: Set[str] = set()

    def compile(self, program: ast.Program) -> str:
        lines = [
            "// 由 CNSH v2.1 编译器自动生成",
            "use std::collections::HashMap;",
            "",
        ]
        lines.extend(self._runtime())
        lines.append("")
        lines.extend(self._stdlib())
        lines.append("")

        decl_lines: List[str] = []
        main_lines: List[str] = []
        for stmt in program.statements:
            if isinstance(stmt, (ast.FunctionDecl, ast.ModuleDecl, ast.StructDecl)):
                decl_lines.extend(self._emit(stmt))
            else:
                main_lines.extend(self._emit(stmt))
        lines.extend(decl_lines)
        lines.append("")
        lines.append("fn __cnsh_main() {")
        self.indent_level += 1
        if not main_lines:
            main_lines = ["// empty"]
        lines.extend(self._indent(main_lines))
        self.indent_level -= 1
        lines.append("}")
        lines.append("")
        lines.append("fn main() {")
        self.indent_level += 1
        lines.extend(self._indent(["__cnsh_main();"]))
        self.indent_level -= 1
        lines.append("}")
        return "\n".join(lines)

    def _runtime(self) -> List[str]:
        return [
            "#[derive(Clone, Debug)]",
            "enum CnshValue {",
            "    Number(f64),",
            "    Text(String),",
            "    Bool(bool),",
            "    Null,",
            "    List(Vec<CnshValue>),",
            "    Map(HashMap<String, CnshValue>),",
            "}",
            "",
            "impl CnshValue {",
            "    fn is_truthy(&self) -> bool {",
            "        match self {",
            "            CnshValue::Bool(b) => *b,",
            "            CnshValue::Number(n) => *n != 0.0,",
            "            CnshValue::Text(s) => !s.is_empty(),",
            "            CnshValue::List(v) => !v.is_empty(),",
            "            CnshValue::Map(m) => !m.is_empty(),",
            "            _ => false,",
            "        }",
            "    }",
            "",
            "    fn as_number(&self) -> f64 {",
            "        match self {",
            "            CnshValue::Number(n) => *n,",
            "            CnshValue::Text(s) => s.parse().unwrap_or(0.0),",
            "            CnshValue::Bool(b) => if *b { 1.0 } else { 0.0 },",
            "            _ => 0.0,",
            "        }",
            "    }",
            "",
            "    fn as_text(&self) -> String {",
            "        match self {",
            "            CnshValue::Text(s) => s.clone(),",
            "            CnshValue::Number(n) => n.to_string(),",
            "            CnshValue::Bool(b) => b.to_string(),",
            "            _ => String::new(),",
            "        }",
            "    }",
            "}",
            "",
            "fn cnsh_print(v: &CnshValue) {",
            "    match v {",
            "        CnshValue::Text(s) => print!(\"{}\", s),",
            "        CnshValue::Number(n) => print!(\"{}\", n),",
            "        CnshValue::Bool(b) => print!(\"{}\", b),",
            "        _ => print!(\"{:?}\", v),",
            "    }",
            "}",
            "",
            "fn cnsh_println(v: &CnshValue) {",
            "    cnsh_print(v);",
            "    println!();",
            "}",
            "",
            "fn cnsh_add(a: &CnshValue, b: &CnshValue) -> CnshValue {",
            "    match (a, b) {",
            "        (CnshValue::Text(x), _) | (_, CnshValue::Text(x)) => {",
            "            CnshValue::Text(format!(\"{}{}\", a.as_text(), b.as_text()))",
            "        }",
            "        _ => CnshValue::Number(a.as_number() + b.as_number()),",
            "    }",
            "}",
            "",
            "fn cnsh_sub(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Number(a.as_number() - b.as_number()) }",
            "fn cnsh_mul(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Number(a.as_number() * b.as_number()) }",
            "fn cnsh_div(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Number(a.as_number() / b.as_number()) }",
            "fn cnsh_rem(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Number(a.as_number() % b.as_number()) }",
            "",
            "fn cnsh_eq(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(format!(\"{:?}\", a) == format!(\"{:?}\", b)) }",
            "fn cnsh_ne(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(format!(\"{:?}\", a) != format!(\"{:?}\", b)) }",
            "fn cnsh_lt(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(a.as_number() < b.as_number()) }",
            "fn cnsh_gt(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(a.as_number() > b.as_number()) }",
            "fn cnsh_le(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(a.as_number() <= b.as_number()) }",
            "fn cnsh_ge(a: &CnshValue, b: &CnshValue) -> CnshValue { CnshValue::Bool(a.as_number() >= b.as_number()) }",
            "",
            "fn cnsh_len(v: &CnshValue) -> CnshValue {",
            "    match v {",
            "        CnshValue::Text(s) => CnshValue::Number(s.len() as f64),",
            "        CnshValue::List(l) => CnshValue::Number(l.len() as f64),",
            "        CnshValue::Map(m) => CnshValue::Number(m.len() as f64),",
            "        _ => CnshValue::Number(0.0),",
            "    }",
            "}",
            "",
            "fn cnsh_to_string(v: &CnshValue) -> CnshValue { CnshValue::Text(v.as_text()) }",
            "fn cnsh_to_int(v: &CnshValue) -> CnshValue { CnshValue::Number(v.as_text().parse().unwrap_or(0.0)) }",
            "fn cnsh_to_float(v: &CnshValue) -> CnshValue { CnshValue::Number(v.as_text().parse().unwrap_or(0.0)) }",
        ]

    def _stdlib(self) -> List[str]:
        return [
            "mod 龍 {",
            "    pub fn 数字根(文本: &str) -> f64 {",
            "        let mut total: u32 = 文本.chars().filter(|c| c.is_ascii_digit()).map(|c| c.to_digit(10).unwrap()).sum();",
            "        if total == 0 { return 0.0; }",
            "        while total >= 10 { total = total.to_string().chars().map(|c| c.to_digit(10).unwrap()).sum(); }",
            "        total as f64",
            "    }",
            "}",
        ]

    def _emit(self, node: ast.ASTNode) -> List[str]:
        method = getattr(self, f"_emit_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"Rust 编译器未实现节点: {type(node).__name__}")
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
        self.module_members = {s.name for s in node.body if isinstance(s, (ast.FunctionDecl, ast.VarDecl))}

        lines = [f"mod {node.name} {{", f"    // 模块 {node.name}{f' ⚖️{node.weight}' if node.weight else ''}"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["// empty"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("}")

        self.module_stack.pop()
        self.module_members = prev_members
        return lines

    def _emit_FunctionDecl(self, node: ast.FunctionDecl) -> List[str]:
        params = ", ".join(f"{p.name}: CnshValue" for p in node.params)
        name = node.name
        vis = "pub " if self.module_stack else ""
        lines = [f"{vis}fn {name}({params}) -> CnshValue {{"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["CnshValue::Null"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_VarDecl(self, node: ast.VarDecl) -> List[str]:
        rhs = self._expr(node.initializer) if node.initializer else "CnshValue::Null"
        keyword = "let" if node.is_const else "let mut"
        if self.module_stack and node.name in self.module_members:
            # 模块内变量作为 pub static? 动态初始化复杂，此处作为局部变量
            return [f"{keyword} {node.name} = {rhs};"]
        return [f"{keyword} {node.name} = {rhs};"]

    def _emit_StructDecl(self, node: ast.StructDecl) -> List[str]:
        fields = ", ".join(f"{f.name}: &CnshValue" for f in node.fields)
        lines = [f"fn {node.name}({fields}) -> CnshValue {{"]
        self.indent_level += 1
        items = ", ".join(f'("{f.name}".to_string(), {f.name}.clone())' for f in node.fields)
        lines.extend(self._indent([f'CnshValue::Map(HashMap::from([{items}]))']))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_UseStmt(self, node: ast.UseStmt) -> List[str]:
        return [f"// 使用 {' '.join(node.module_path)}"]

    def _emit_IfStmt(self, node: ast.IfStmt) -> List[str]:
        lines = [f"if {self._expr(node.condition)}.is_truthy() {{"]
        self.indent_level += 1
        then_lines = []
        for stmt in node.then_body:
            then_lines.extend(self._emit(stmt))
        if not then_lines:
            then_lines = ["// empty"]
        lines.extend(self._indent(then_lines))
        self.indent_level -= 1
        for branch in node.elif_branches:
            lines.append(f"}} else if {self._expr(branch.condition)}.is_truthy() {{")
            self.indent_level += 1
            branch_lines = []
            for stmt in branch.body:
                branch_lines.extend(self._emit(stmt))
            if not branch_lines:
                branch_lines = ["// empty"]
            lines.extend(self._indent(branch_lines))
            self.indent_level -= 1
        if node.else_body:
            lines.append("} else {")
            self.indent_level += 1
            else_lines = []
            for stmt in node.else_body:
                else_lines.extend(self._emit(stmt))
            if not else_lines:
                else_lines = ["// empty"]
            lines.extend(self._indent(else_lines))
            self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_WhileStmt(self, node: ast.WhileStmt) -> List[str]:
        lines = [f"while {self._expr(node.condition)}.is_truthy() {{"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["// empty"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_ForStmt(self, node: ast.ForStmt) -> List[str]:
        iter_expr = self._expr(node.iterable)
        lines = [f"if let CnshValue::List(__list) = {iter_expr} {{"]
        self.indent_level += 1
        lines.append(f"    for {node.var_name} in __list {{")
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["// empty"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("    }")
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_ReturnStmt(self, node: ast.ReturnStmt) -> List[str]:
        if node.value:
            return [f"return {self._expr(node.value)};"]
        return ["return CnshValue::Null;"]

    def _emit_BreakStmt(self, _) -> List[str]:
        return ["break;"]

    def _emit_ContinueStmt(self, _) -> List[str]:
        return ["continue;"]

    def _emit_ExpressionStmt(self, node: ast.ExpressionStmt) -> List[str]:
        return [f"{self._expr(node.expression)};"]

    # Rust 后端暂不支持的高级特性（给出友好错误）
    def _emit_ClassDecl(self, node: ast.ClassDecl) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 类（class），请使用 Python 后端")

    def _emit_MethodDecl(self, node: ast.MethodDecl) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 方法/异步函数，请使用 Python 后端")

    def _emit_YieldStmt(self, node: ast.YieldStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 产生（yield），请使用 Python 后端")

    def _emit_YieldFromStmt(self, node: ast.YieldFromStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 产生于（yield from），请使用 Python 后端")

    def _emit_TryStmt(self, node: ast.TryStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 尝试/捕获/最终（try/except/finally），请使用 Python 后端")

    def _emit_RaiseStmt(self, node: ast.RaiseStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 抛出（raise），请使用 Python 后端")

    def _emit_PassStmt(self, node: ast.PassStmt) -> List[str]:
        return ["// pass"]

    def _emit_WithStmt(self, node: ast.WithStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 使用（with），请使用 Python 后端")

    def _emit_AsyncWithStmt(self, node: ast.AsyncWithStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 异步使用（async with），请使用 Python 后端")

    def _emit_AsyncForStmt(self, node: ast.AsyncForStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 异步对于（async for），请使用 Python 后端")

    def _emit_EnumDecl(self, node: ast.EnumDecl) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 枚举类（enum），请使用 Python 后端")

    def _emit_EnumMember(self, node: ast.EnumMember) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 枚举成员，请使用 Python 后端")

    def _emit_DataClassDecl(self, node: ast.DataClassDecl) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 数据类（dataclass），请使用 Python 后端")

    def _emit_DataClassField(self, node: ast.DataClassField) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 数据类字段，请使用 Python 后端")

    def _emit_ImportStmt(self, node: ast.ImportStmt) -> List[str]:
        raise CNSHRuntimeError("Rust 后端暂不支持 导入（import），请使用 Python 后端")

    # ---------- 表达式 ----------

    def _expr(self, node: Optional[ast.ASTNode]) -> str:
        if node is None:
            return "CnshValue::Null".format()
        method = getattr(self, f"_expr_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"Rust 编译器未实现表达式: {type(node).__name__}")
        return method(node)

    def _expr_LiteralExpr(self, node: ast.LiteralExpr) -> str:
        if isinstance(node.value, str):
            return f'CnshValue::Text("{self._escape_string(node.value)}".to_string())'
        if isinstance(node.value, bool):
            return f"CnshValue::Bool({str(node.value).lower()})"
        if node.value is None:
            return "CnshValue::Null"
        if isinstance(node.value, float):
            return f"CnshValue::Number({node.value})"
        return f"CnshValue::Number({node.value}.0)"

    def _escape_string(self, s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")

    def _expr_IdentifierExpr(self, node: ast.IdentifierExpr) -> str:
        if self.module_stack and node.name in self.module_members:
            return f"{node.name}.clone()"
        return f"{node.name}.clone()"

    def _expr_BinaryExpr(self, node: ast.BinaryExpr) -> str:
        op = node.op
        if op == "=":
            return f"{self._expr(node.left)} = {self._expr(node.right)}"
        left = self._expr(node.left)
        right = self._expr(node.right)
        if op in ("+", "加"):
            return f"cnsh_add(&({left}), &({right}))"
        if op in ("-", "减"):
            return f"cnsh_sub(&({left}), &({right}))"
        if op in ("*", "乘"):
            return f"cnsh_mul(&({left}), &({right}))"
        if op in ("/", "除"):
            return f"cnsh_div(&({left}), &({right}))"
        if op in ("%", "取模"):
            return f"cnsh_rem(&({left}), &({right}))"
        if op in ("==", "等于"):
            return f"cnsh_eq(&({left}), &({right}))"
        if op in ("!=", "不等于"):
            return f"cnsh_ne(&({left}), &({right}))"
        if op in ("<", "小于"):
            return f"cnsh_lt(&({left}), &({right}))"
        if op in (">", "大于"):
            return f"cnsh_gt(&({left}), &({right}))"
        if op in ("<=", "小于等于"):
            return f"cnsh_le(&({left}), &({right}))"
        if op in (">=", "大于等于"):
            return f"cnsh_ge(&({left}), &({right}))"
        if op in ("&&", "且"):
            return f"CnshValue::Bool(({left}).is_truthy() && ({right}).is_truthy())"
        if op in ("||", "或"):
            return f"CnshValue::Bool(({left}).is_truthy() || ({right}).is_truthy())"
        raise CNSHRuntimeError(f"Rust 编译器未知运算符: {op}")

    def _expr_UnaryExpr(self, node: ast.UnaryExpr) -> str:
        op = node.op
        operand = self._expr(node.operand)
        if op in ("!", "非"):
            return f"CnshValue::Bool(!({operand}).is_truthy())"
        if op == "-":
            return f"CnshValue::Number(-({operand}).as_number())"
        if op == "+":
            return f"CnshValue::Number(({operand}).as_number())"
        raise CNSHRuntimeError(f"Rust 编译器未知一元运算符: {op}")

    def _expr_CallExpr(self, node: ast.CallExpr) -> str:
        # 内置函数特殊处理（避免给 Identifier 加 clone）
        if isinstance(node.callee, ast.IdentifierExpr):
            name = node.callee.name
            if name == "输出" and node.args:
                return f"cnsh_println(&({self._expr_raw(node.args[0])}))"
            if name == "长度" and node.args:
                return f"cnsh_len(&({self._expr_raw(node.args[0])}))"
            if name == "字符串" and node.args:
                return f"cnsh_to_string(&({self._expr_raw(node.args[0])}))"
            if name == "整数" and node.args:
                return f"cnsh_to_int(&({self._expr_raw(node.args[0])}))"
            if name == "小数" and node.args:
                return f"cnsh_to_float(&({self._expr_raw(node.args[0])}))"
            # 用户函数调用：直接使用函数名，不加 clone
            args = ", ".join(f"&({self._expr_raw(a)})" for a in node.args)
            return f"{name}({args})"
        callee = self._expr(node.callee)
        args = ", ".join(f"&({self._expr_raw(a)})" for a in node.args)
        return f"{callee}({args})"

    def _expr_raw(self, node: ast.ASTNode) -> str:
        """生成表达式但不自动 clone（用于取引用场景）。"""
        if isinstance(node, ast.IdentifierExpr):
            return node.name
        return self._expr(node)

    def _expr_MemberExpr(self, node: ast.MemberExpr) -> str:
        return f"{self._expr(node.object)}::{node.member}"

    def _expr_IndexExpr(self, node: ast.IndexExpr) -> str:
        obj = self._expr(node.object)
        idx = self._expr(node.index)
        return f"match (&({obj}), &({idx})) {{ (CnshValue::List(l), CnshValue::Number(i)) => l[*i as usize].clone(), (CnshValue::Map(m), CnshValue::Text(k)) => m[k].clone(), _ => CnshValue::Null }}"

    def _expr_ListExpr(self, node: ast.ListExpr) -> str:
        items = ", ".join(self._expr(e) for e in node.elements)
        return f"CnshValue::List(vec![{items}])"

    def _expr_MapExpr(self, node: ast.MapExpr) -> str:
        items = ", ".join(f"({self._expr(p.key)}.as_text(), {self._expr(p.value)})" for p in node.pairs)
        return f"CnshValue::Map(HashMap::from([{items}]))"

    def _expr_AwaitExpr(self, node: ast.AwaitExpr) -> str:
        raise CNSHRuntimeError("Rust 后端暂不支持 等待（await），请使用 Python 后端")

    def _expr_GeneratorExpr(self, node: ast.GeneratorExpr) -> str:
        raise CNSHRuntimeError("Rust 后端暂不支持 生成器表达式，请使用 Python 后端")
