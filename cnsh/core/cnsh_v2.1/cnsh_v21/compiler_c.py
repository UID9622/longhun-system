#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 → C 编译器
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-COMPILER-C-v2.1

说明：教学占位编译器，生成使用 CnshValue 动态类型的 C 代码，
      支持数值/字符串/函数/if/while/for，标准库暂未接入 C。
"""
from typing import List, Optional, Set

from . import ast_nodes as ast
from .errors import CNSHRuntimeError


class CCompiler:
    """CNSH → C 转译器"""

    INDENT = "    "

    def __init__(self):
        self.indent_level = 0
        self.module_stack: List[str] = []
        self.module_members: Set[str] = set()

    def compile(self, program: ast.Program) -> str:
        lines = [
            "/* 由 CNSH v2.1 编译器自动生成 */",
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <string.h>",
            "",
        ]
        lines.extend(self._runtime())
        lines.append("")
        # 顶层声明
        decl_lines: List[str] = []
        main_lines: List[str] = []
        for stmt in program.statements:
            if isinstance(stmt, (ast.FunctionDecl, ast.ModuleDecl, ast.StructDecl)):
                decl_lines.extend(self._emit(stmt))
            else:
                main_lines.extend(self._emit(stmt))
        lines.extend(decl_lines)
        lines.append("")
        lines.append("int main(void) {")
        self.indent_level += 1
        if not main_lines:
            main_lines = ["/* empty */"]
        lines.extend(self._indent(main_lines))
        lines.extend(self._indent(["return 0;"]))
        self.indent_level -= 1
        lines.append("}")
        return "\n".join(lines)

    def _runtime(self) -> List[str]:
        return [
            "typedef enum { CNSH_NUM, CNSH_TEXT, CNSH_BOOL, CNSH_NULL } CnshType;",
            "typedef struct {",
            "    CnshType type;",
            "    double number;",
            "    char *text;",
            "    int boolean;",
            "} CnshValue;",
            "",
            "CnshValue cnsh_number(double n) { CnshValue v = {CNSH_NUM, n, NULL, 0}; return v; }",
            "CnshValue cnsh_text(const char *s) { CnshValue v = {CNSH_TEXT, 0, strdup(s), 0}; return v; }",
            "CnshValue cnsh_bool(int b) { CnshValue v = {CNSH_BOOL, 0, NULL, b}; return v; }",
            "CnshValue cnsh_null() { CnshValue v = {CNSH_NULL, 0, NULL, 0}; return v; }",
            "",
            "double cnsh_as_number(CnshValue v) {",
            "    if (v.type == CNSH_NUM) return v.number;",
            "    if (v.type == CNSH_TEXT && v.text) return atof(v.text);",
            "    return v.boolean ? 1.0 : 0.0;",
            "}",
            "",
            "const char *cnsh_as_text(CnshValue v) {",
            "    static char buf[64];",
            "    if (v.type == CNSH_TEXT) return v.text ? v.text : \"\";",
            "    if (v.type == CNSH_NUM) { snprintf(buf, sizeof(buf), \"%g\", v.number); return buf; }",
            "    return v.boolean ? \"true\" : \"false\";",
            "}",
            "",
            "int cnsh_is_truthy(CnshValue v) {",
            "    if (v.type == CNSH_BOOL) return v.boolean;",
            "    if (v.type == CNSH_NUM) return v.number != 0.0;",
            "    if (v.type == CNSH_TEXT) return v.text && v.text[0];",
            "    return 0;",
            "}",
            "",
            "void cnsh_print(CnshValue v) {",
            "    if (v.type == CNSH_TEXT) printf(\"%s\", v.text ? v.text : \"\");",
            "    else if (v.type == CNSH_NUM) printf(\"%g\", v.number);",
            "    else if (v.type == CNSH_BOOL) printf(\"%s\", v.boolean ? \"true\" : \"false\");",
            "    else printf(\"null\");",
            "}",
            "",
            "void cnsh_println(CnshValue v) { cnsh_print(v); printf(\"\\n\"); }",
            "",
            "CnshValue cnsh_add(CnshValue a, CnshValue b) {",
            "    if (a.type == CNSH_TEXT || b.type == CNSH_TEXT) {",
            "        char *buf = malloc(strlen(cnsh_as_text(a)) + strlen(cnsh_as_text(b)) + 1);",
            "        strcpy(buf, cnsh_as_text(a)); strcat(buf, cnsh_as_text(b));",
            "        CnshValue r = cnsh_text(buf); free(buf); return r;",
            "    }",
            "    return cnsh_number(cnsh_as_number(a) + cnsh_as_number(b));",
            "}",
            "CnshValue cnsh_sub(CnshValue a, CnshValue b) { return cnsh_number(cnsh_as_number(a) - cnsh_as_number(b)); }",
            "CnshValue cnsh_mul(CnshValue a, CnshValue b) { return cnsh_number(cnsh_as_number(a) * cnsh_as_number(b)); }",
            "CnshValue cnsh_div(CnshValue a, CnshValue b) { return cnsh_number(cnsh_as_number(a) / cnsh_as_number(b)); }",
            "CnshValue cnsh_rem(CnshValue a, CnshValue b) { return cnsh_number((long)cnsh_as_number(a) % (long)cnsh_as_number(b)); }",
            "",
            "CnshValue cnsh_eq(CnshValue a, CnshValue b) { return cnsh_bool(strcmp(cnsh_as_text(a), cnsh_as_text(b)) == 0); }",
            "CnshValue cnsh_ne(CnshValue a, CnshValue b) { return cnsh_bool(strcmp(cnsh_as_text(a), cnsh_as_text(b)) != 0); }",
            "CnshValue cnsh_lt(CnshValue a, CnshValue b) { return cnsh_bool(cnsh_as_number(a) < cnsh_as_number(b)); }",
            "CnshValue cnsh_gt(CnshValue a, CnshValue b) { return cnsh_bool(cnsh_as_number(a) > cnsh_as_number(b)); }",
            "CnshValue cnsh_le(CnshValue a, CnshValue b) { return cnsh_bool(cnsh_as_number(a) <= cnsh_as_number(b)); }",
            "CnshValue cnsh_ge(CnshValue a, CnshValue b) { return cnsh_bool(cnsh_as_number(a) >= cnsh_as_number(b)); }",
        ]

    def _emit(self, node: ast.ASTNode) -> List[str]:
        method = getattr(self, f"_emit_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"C 编译器未实现节点: {type(node).__name__}")
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

        lines = [f"/* 模块 {node.name}{f' ⚖️{node.weight}' if node.weight else ''} */"]
        for stmt in node.body:
            lines.extend(self._emit(stmt))

        self.module_stack.pop()
        self.module_members = prev_members
        return lines

    def _emit_FunctionDecl(self, node: ast.FunctionDecl) -> List[str]:
        params = ", ".join(f"CnshValue {p.name}" for p in node.params)
        name = node.name
        lines = [f"CnshValue {name}({params}) {{"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["return cnsh_null();"]
        elif not any(line.startswith("return ") for line in body_lines):
            body_lines.append("return cnsh_null();")
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_VarDecl(self, node: ast.VarDecl) -> List[str]:
        rhs = self._expr(node.initializer) if node.initializer else "cnsh_null()"
        return [f"CnshValue {node.name} = {rhs};"]

    def _emit_StructDecl(self, node: ast.StructDecl) -> List[str]:
        # 简化为返回文本表示
        fields = ", ".join(f"{f.name}" for f in node.fields)
        lines = [f"/* 结构体 {node.name}({fields}) */"]
        return lines

    def _emit_UseStmt(self, node: ast.UseStmt) -> List[str]:
        return [f"/* 使用 {' '.join(node.module_path)} */"]

    def _emit_IfStmt(self, node: ast.IfStmt) -> List[str]:
        lines = [f"if (cnsh_is_truthy({self._expr(node.condition)})) {{"]
        self.indent_level += 1
        then_lines = []
        for stmt in node.then_body:
            then_lines.extend(self._emit(stmt))
        if not then_lines:
            then_lines = ["/* empty */"]
        lines.extend(self._indent(then_lines))
        self.indent_level -= 1
        for branch in node.elif_branches:
            lines.append(f"}} else if (cnsh_is_truthy({self._expr(branch.condition)})) {{")
            self.indent_level += 1
            branch_lines = []
            for stmt in branch.body:
                branch_lines.extend(self._emit(stmt))
            if not branch_lines:
                branch_lines = ["/* empty */"]
            lines.extend(self._indent(branch_lines))
            self.indent_level -= 1
        if node.else_body:
            lines.append("} else {")
            self.indent_level += 1
            else_lines = []
            for stmt in node.else_body:
                else_lines.extend(self._emit(stmt))
            if not else_lines:
                else_lines = ["/* empty */"]
            lines.extend(self._indent(else_lines))
            self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_WhileStmt(self, node: ast.WhileStmt) -> List[str]:
        lines = [f"while (cnsh_is_truthy({self._expr(node.condition)})) {{"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["/* empty */"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_ForStmt(self, node: ast.ForStmt) -> List[str]:
        # 使用下标循环
        iter_expr = self._expr(node.iterable)
        var = node.var_name
        lines = [
            "{ /* for loop */",
            f"    CnshValue __iter = {iter_expr};",
            f"    /* for 循环在 C 后端中需要 List 支持，当前为占位 */",
            "}",
        ]
        return lines

    def _emit_ReturnStmt(self, node: ast.ReturnStmt) -> List[str]:
        if node.value:
            return [f"return {self._expr(node.value)};"]
        return ["return cnsh_null();"]

    def _emit_BreakStmt(self, _) -> List[str]:
        return ["break;"]

    def _emit_ContinueStmt(self, _) -> List[str]:
        return ["continue;"]

    def _emit_ExpressionStmt(self, node: ast.ExpressionStmt) -> List[str]:
        return [f"{self._expr(node.expression)};"]

    # C 后端暂不支持的高级特性（给出友好错误）
    def _emit_ClassDecl(self, node: ast.ClassDecl) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 类（class）")

    def _emit_MethodDecl(self, node: ast.MethodDecl) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 方法/异步函数")

    def _emit_YieldStmt(self, node: ast.YieldStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 产生（yield）")

    def _emit_YieldFromStmt(self, node: ast.YieldFromStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 产生于（yield from）")

    def _emit_TryStmt(self, node: ast.TryStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 尝试/捕获/最终（try/except/finally）")

    def _emit_RaiseStmt(self, node: ast.RaiseStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 抛出（raise）")

    def _emit_PassStmt(self, node: ast.PassStmt) -> List[str]:
        return ["/* pass */"]

    def _emit_WithStmt(self, node: ast.WithStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 使用（with）")

    def _emit_AsyncWithStmt(self, node: ast.AsyncWithStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 异步使用（async with）")

    def _emit_AsyncForStmt(self, node: ast.AsyncForStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 异步对于（async for）")

    def _emit_EnumDecl(self, node: ast.EnumDecl) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 枚举类（enum）")

    def _emit_EnumMember(self, node: ast.EnumMember) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 枚举成员")

    def _emit_DataClassDecl(self, node: ast.DataClassDecl) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 数据类（dataclass）")

    def _emit_DataClassField(self, node: ast.DataClassField) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 数据类字段")

    def _emit_ImportStmt(self, node: ast.ImportStmt) -> List[str]:
        raise CNSHRuntimeError("C 后端暂不支持 导入（import），请使用 Python 后端")

    # ---------- 表达式 ----------

    def _expr(self, node: Optional[ast.ASTNode]) -> str:
        if node is None:
            return "cnsh_null()"
        method = getattr(self, f"_expr_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"C 编译器未实现表达式: {type(node).__name__}")
        return method(node)

    def _expr_LiteralExpr(self, node: ast.LiteralExpr) -> str:
        if isinstance(node.value, str):
            return f'cnsh_text("{self._escape_string(node.value)}")'
        if isinstance(node.value, bool):
            return f"cnsh_bool({1 if node.value else 0})"
        if node.value is None:
            return "cnsh_null()"
        return f"cnsh_number({node.value})"

    def _escape_string(self, s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")

    def _expr_IdentifierExpr(self, node: ast.IdentifierExpr) -> str:
        return node.name

    def _expr_BinaryExpr(self, node: ast.BinaryExpr) -> str:
        op = node.op
        if op == "=":
            return f"{self._expr(node.left)} = {self._expr(node.right)}"
        left = self._expr(node.left)
        right = self._expr(node.right)
        funcs = {
            "+": "cnsh_add", "加": "cnsh_add",
            "-": "cnsh_sub", "减": "cnsh_sub",
            "*": "cnsh_mul", "乘": "cnsh_mul",
            "/": "cnsh_div", "除": "cnsh_div",
            "%": "cnsh_rem", "取模": "cnsh_rem",
            "==": "cnsh_eq", "等于": "cnsh_eq",
            "!=": "cnsh_ne", "不等于": "cnsh_ne",
            "<": "cnsh_lt", "小于": "cnsh_lt",
            ">": "cnsh_gt", "大于": "cnsh_gt",
            "<=": "cnsh_le", "小于等于": "cnsh_le",
            ">=": "cnsh_ge", "大于等于": "cnsh_ge",
        }
        if op in funcs:
            return f"{funcs[op]}({left}, {right})"
        if op in ("&&", "且"):
            return f"cnsh_bool(cnsh_is_truthy({left}) && cnsh_is_truthy({right}))"
        if op in ("||", "或"):
            return f"cnsh_bool(cnsh_is_truthy({left}) || cnsh_is_truthy({right}))"
        raise CNSHRuntimeError(f"C 编译器未知运算符: {op}")

    def _expr_UnaryExpr(self, node: ast.UnaryExpr) -> str:
        op = node.op
        operand = self._expr(node.operand)
        if op in ("!", "非"):
            return f"cnsh_bool(!cnsh_is_truthy({operand}))"
        if op == "-":
            return f"cnsh_number(-cnsh_as_number({operand}))"
        if op == "+":
            return f"cnsh_number(cnsh_as_number({operand}))"
        raise CNSHRuntimeError(f"C 编译器未知一元运算符: {op}")

    def _expr_CallExpr(self, node: ast.CallExpr) -> str:
        if isinstance(node.callee, ast.IdentifierExpr):
            name = node.callee.name
            if name == "输出" and node.args:
                return f"cnsh_println({self._expr(node.args[0])})"
            if name == "长度" and node.args:
                return f"cnsh_number(strlen(cnsh_as_text({self._expr(node.args[0])})))"
            if name in ("字符串", "整数", "小数") and node.args:
                return f"cnsh_text(cnsh_as_text({self._expr(node.args[0])}))"
            args = ", ".join(self._expr(a) for a in node.args)
            return f"{name}({args})"
        callee = self._expr(node.callee)
        args = ", ".join(self._expr(a) for a in node.args)
        return f"{callee}({args})"

    def _expr_MemberExpr(self, node: ast.MemberExpr) -> str:
        return f"/* {self._expr(node.object)}.{node.member} 未实现 */ cnsh_null()"

    def _expr_IndexExpr(self, node: ast.IndexExpr) -> str:
        return "/* 索引未实现 */ cnsh_null()"

    def _expr_ListExpr(self, node: ast.ListExpr) -> str:
        return "/* 列表未实现 */ cnsh_null()"

    def _expr_MapExpr(self, node: ast.MapExpr) -> str:
        return "/* 映射未实现 */ cnsh_null()"

    def _expr_AwaitExpr(self, node: ast.AwaitExpr) -> str:
        raise CNSHRuntimeError("C 后端暂不支持 等待（await）")

    def _expr_GeneratorExpr(self, node: ast.GeneratorExpr) -> str:
        raise CNSHRuntimeError("C 后端暂不支持 生成器表达式")
