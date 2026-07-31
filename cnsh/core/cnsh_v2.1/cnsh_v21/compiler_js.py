# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
CNSH v2.1 → JavaScript 编译器
DNA: #龍芯⚡️2026-06-29-CNSH-COMPILER-JS-v2.1
"""
import json
from typing import Any, List, Optional, Set

from . import ast_nodes as ast
from .errors import CNSHRuntimeError


class JavaScriptCompiler:
    """将 CNSH AST 转译为可执行的 JavaScript (Node.js / 浏览器)。"""

    INDENT = "    "

    def __init__(self):
        self.indent_level = 0
        self.module_stack: List[str] = []
        self.module_members: Set[str] = set()

    def compile(self, program: ast.Program) -> str:
        lines = [
            "// 由 CNSH v2.1 编译器自动生成",
            "// 运行时辅助函数",
            "function cnsh_print(...args) { console.log(...args); }",
            "function cnsh_length(x) { return (x && typeof x.length === 'number') ? x.length : 0; }",
            "const 输出 = cnsh_print;",
            "const 输入 = () => { throw new Error('浏览器环境不支持输入'); };",
            "const 长度 = cnsh_length;",
            "const 字符串 = String;",
            "const 整数 = parseInt;",
            "const 小数 = parseFloat;",
            "",
        ]
        lines.extend(self._stdlib_js())
        lines.append("")
        for stmt in program.statements:
            lines.extend(self._emit(stmt))
        return "\n".join(lines)

    def _stdlib_js(self) -> List[str]:
        return [
            "const 龍 = {",
            "    核心: {",
            "        DNA登记: (信息) => '#龍芯⚡️' + new Date().toISOString().slice(0,10) + '-' + (信息.模块 || '未知') + '-' + Math.random().toString(36).slice(2,10).toUpperCase() + '-v2.1',",
            "        DNA验证: (DNA码) => typeof DNA码 === 'string' && DNA码.startsWith('#龍芯⚡️'),",
            "        IPA注册: (节点) => console.log('[IPA注册]', 节点.名称 || '未命名'),",
            "        记忆归集: () => ({ 摘要: '记忆归集占位', 时间: new Date().toISOString() }),",
            "        序列化全局状态: (状态) => JSON.stringify(状态),",
            "        恢复全局状态: (快照) => JSON.parse(快照),",
            "    },",
            "    数学: {",
            "        数字根: (文本) => { let t = String(文本).split('').filter(c => /\\d/.test(c)).reduce((a,b)=>a+parseInt(b),0); while(t >= 10){ t = String(t).split('').reduce((a,b)=>a+parseInt(b),0); } return t; },",
            "        五行: {",
            "            解析八字: (八字) => ({ 八字, 天干: 八字.split('').filter((_,i)=>i%2===0), 地支: 八字.split('').filter((_,i)=>i%2===1) }),",
            "            计算强度: (四柱) => ({ 金:20, 木:20, 水:20, 火:20, 土:20 })",
            "        },",
            "        八卦: { 推演: (场景) => ({ 卦象:'未济', 建议:'审慎推进', 场景 }) },",
            "        洛书: { 定位: (数字) => { const m = {1:{宫:'坎',五行:'水'},2:{宫:'坤',五行:'土'},3:{宫:'震',五行:'木'},4:{宫:'巽',五行:'木'},5:{宫:'中',五行:'土'},6:{宫:'乾',五行:'金'},7:{宫:'兑',五行:'金'},8:{宫:'艮',五行:'土'},9:{宫:'离',五行:'火'}}; return m[((数字-1)%9)+1]; } }",
            "    },",
            "    审计: {",
            "        三色判定: (操作) => { const dr = 龍.数学.数字根(JSON.stringify(操作)); return (dr === 3 || dr === 9) ? '🔴' : (dr === 6 ? '🟡' : '🟢'); },",
            "        数字根: (文本) => 龍.数学.数字根(文本),",
            "        证据校验: (证据) => 证据.哈希 !== undefined && 证据.签名 !== undefined,",
            "        日志记录: (事件) => console.log('[审计日志]', JSON.stringify({ 时间: new Date().toISOString(), 事件 }))",
            "    },",
            "    IO: {",
            "        标准输出: (内容) => process.stdout.write(String(内容)),",
            "        标准输入: () => { throw new Error('未实现'); },",
            "        网络请求: async (地址, 方法) => { throw new Error('未实现'); }",
            "    },",
            "    DNA: {",
            "        登记: (信息) => 龍.核心.DNA登记(信息),",
            "        验证: (DNA码) => 龍.核心.DNA验证(DNA码),",
            "        签章: (数据) => btoa(unescape(encodeURIComponent(数据))),",
            "        查询: (DNA码) => ({})",
            "    },",
            "    盾: {",
            "        加密: (明文, 密钥) => btoa(unescape(encodeURIComponent(明文))),",
            "        解密: (密文, 密钥) => decodeURIComponent(escape(atob(密文))),",
            "        签章: (数据) => 龍.DNA.签章(数据),",
            "        验签: (数据, 签名) => 龍.DNA.签章(数据) === 签名,",
            "        阅后即焚: (数据) => { delete 数据.敏感字段; console.log('[阅后即焚] 已销毁'); }",
            "    }",
            "};",
        ]

    def _emit(self, node: ast.ASTNode) -> List[str]:
        method = getattr(self, f"_emit_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"JS 编译器未实现节点: {type(node).__name__}")
        return method(node)

    def _indent(self, lines: List[str]) -> List[str]:
        prefix = self.INDENT * self.indent_level
        return [prefix + line if line else line for line in lines]

    def _emit_ModuleDecl(self, node: ast.ModuleDecl) -> List[str]:
        self.module_stack.append(node.name)
        prev_members = self.module_members
        self.module_members = {s.name for s in node.body if isinstance(s, (ast.FunctionDecl, ast.VarDecl))}

        lines = [f"const {node.name} = {{}};", f"// 模块 {node.name}{f' ⚖️{node.weight}' if node.weight else ''}"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1

        self.module_stack.pop()
        self.module_members = prev_members
        return lines

    def _emit_FunctionDecl(self, node: ast.FunctionDecl) -> List[str]:
        params = ", ".join(p.name for p in node.params)
        is_module_method = bool(self.module_stack)
        name = node.name
        if is_module_method:
            module_name = self.module_stack[-1]
            lines = [f"{module_name}.{name} = function({params}) {{"]
        else:
            lines = [f"function {name}({params}) {{"]
        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            body_lines.extend(self._emit(stmt))
        if not body_lines:
            body_lines = ["return;"]
        lines.extend(self._indent(body_lines))
        self.indent_level -= 1
        lines.append("};")
        return lines

    def _emit_VarDecl(self, node: ast.VarDecl) -> List[str]:
        rhs = self._expr(node.initializer) if node.initializer else "null"
        keyword = "const" if node.is_const else "let"
        if self.module_stack and node.name in self.module_members:
            module_name = self.module_stack[-1]
            return [f"{module_name}.{node.name} = {rhs};"]
        return [f"{keyword} {node.name} = {rhs};"]

    def _emit_StructDecl(self, node: ast.StructDecl) -> List[str]:
        fields = ", ".join(f.name for f in node.fields)
        lines = [f"function {node.name}({fields}) {{"]
        self.indent_level += 1
        items = ", ".join(f'{f.name}: {f.name}' for f in node.fields)
        lines.extend(self._indent([f'return {{ __类型__: "{node.name}", {items} }};']))
        self.indent_level -= 1
        lines.append("}")
        return lines

    def _emit_UseStmt(self, node: ast.UseStmt) -> List[str]:
        return [f"// 使用 {' '.join(node.module_path)}"]

    def _emit_IfStmt(self, node: ast.IfStmt) -> List[str]:
        lines = [f"if ({self._expr(node.condition)}) {{"]
        self.indent_level += 1
        then_lines = []
        for stmt in node.then_body:
            then_lines.extend(self._emit(stmt))
        if not then_lines:
            then_lines = ["// empty"]
        lines.extend(self._indent(then_lines))
        self.indent_level -= 1
        for branch in node.elif_branches:
            lines.append(f"}} else if ({self._expr(branch.condition)}) {{")
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
        lines = [f"while ({self._expr(node.condition)}) {{"]
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
        lines = [f"for (const {node.var_name} of {self._expr(node.iterable)}) {{"]
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

    def _emit_ReturnStmt(self, node: ast.ReturnStmt) -> List[str]:
        if node.value:
            return [f"return {self._expr(node.value)};"]
        return ["return;"]

    def _emit_BreakStmt(self, _) -> List[str]:
        return ["break;"]

    def _emit_ContinueStmt(self, _) -> List[str]:
        return ["continue;"]

    def _emit_ExpressionStmt(self, node: ast.ExpressionStmt) -> List[str]:
        return [f"{self._expr(node.expression)};"]

    # JS 后端暂不支持的高级特性（给出友好错误）
    def _emit_ClassDecl(self, node: ast.ClassDecl) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 类（class），请使用 Python 后端")

    def _emit_MethodDecl(self, node: ast.MethodDecl) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 方法/异步函数，请使用 Python 后端")

    def _emit_YieldStmt(self, node: ast.YieldStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 产生（yield），请使用 Python 后端")

    def _emit_YieldFromStmt(self, node: ast.YieldFromStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 产生于（yield from），请使用 Python 后端")

    def _emit_TryStmt(self, node: ast.TryStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 尝试/捕获/最终（try/except/finally），请使用 Python 后端")

    def _emit_RaiseStmt(self, node: ast.RaiseStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 抛出（raise），请使用 Python 后端")

    def _emit_PassStmt(self, node: ast.PassStmt) -> List[str]:
        return ["// pass"]

    def _emit_WithStmt(self, node: ast.WithStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 使用（with），请使用 Python 后端")

    def _emit_AsyncWithStmt(self, node: ast.AsyncWithStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 异步使用（async with），请使用 Python 后端")

    def _emit_AsyncForStmt(self, node: ast.AsyncForStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 异步对于（async for），请使用 Python 后端")

    def _emit_EnumDecl(self, node: ast.EnumDecl) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 枚举类（enum），请使用 Python 后端")

    def _emit_EnumMember(self, node: ast.EnumMember) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 枚举成员，请使用 Python 后端")

    def _emit_DataClassDecl(self, node: ast.DataClassDecl) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 数据类（dataclass），请使用 Python 后端")

    def _emit_DataClassField(self, node: ast.DataClassField) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 数据类字段，请使用 Python 后端")

    def _emit_ImportStmt(self, node: ast.ImportStmt) -> List[str]:
        raise CNSHRuntimeError("JS 后端暂不支持 导入（import），请使用 Python 后端")

    # ---------- 表达式 ----------

    def _expr(self, node: Optional[ast.ASTNode]) -> str:
        if node is None:
            return "null"
        method = getattr(self, f"_expr_{type(node).__name__}", None)
        if method is None:
            raise CNSHRuntimeError(f"JS 编译器未实现表达式: {type(node).__name__}")
        return method(node)

    def _expr_LiteralExpr(self, node: ast.LiteralExpr) -> str:
        if isinstance(node.value, str):
            return self._js_string(node.value)
        if isinstance(node.value, bool):
            return "true" if node.value else "false"
        if node.value is None:
            return "null"
        return str(node.value)

    def _js_string(self, s: str) -> str:
        escaped = s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\t", "\\t")
        return f"'{escaped}'"

    def _expr_IdentifierExpr(self, node: ast.IdentifierExpr) -> str:
        if self.module_stack and node.name in self.module_members:
            return f"{self.module_stack[-1]}.{node.name}"
        return node.name

    def _expr_BinaryExpr(self, node: ast.BinaryExpr) -> str:
        op = node.op
        if op == "=":
            return f"{self._expr(node.left)} = {self._expr(node.right)}"
        op_map = {"且": "&&", "或": "||", "非": "!"}
        py_op = op_map.get(op, op)
        return f"({self._expr(node.left)} {py_op} {self._expr(node.right)})"

    def _expr_UnaryExpr(self, node: ast.UnaryExpr) -> str:
        op = node.op
        if op in ("!", "非"):
            return f"(!{self._expr(node.operand)})"
        return f"({op}{self._expr(node.operand)})"

    def _expr_CallExpr(self, node: ast.CallExpr) -> str:
        callee = self._expr(node.callee)
        args = ", ".join(self._expr(a) for a in node.args)
        return f"{callee}({args})"

    def _expr_MemberExpr(self, node: ast.MemberExpr) -> str:
        return f"{self._expr(node.object)}.{node.member}"

    def _expr_IndexExpr(self, node: ast.IndexExpr) -> str:
        return f"{self._expr(node.object)}[{self._expr(node.index)}]"

    def _expr_ListExpr(self, node: ast.ListExpr) -> str:
        items = ", ".join(self._expr(e) for e in node.elements)
        return f"[{items}]"

    def _expr_MapExpr(self, node: ast.MapExpr) -> str:
        items = ", ".join(f"{self._expr(p.key)}: {self._expr(p.value)}" for p in node.pairs)
        return f"{{{items}}}"

    def _expr_AwaitExpr(self, node: ast.AwaitExpr) -> str:
        raise CNSHRuntimeError("JS 后端暂不支持 等待（await），请使用 Python 后端")

    def _expr_GeneratorExpr(self, node: ast.GeneratorExpr) -> str:
        raise CNSHRuntimeError("JS 后端暂不支持 生成器表达式，请使用 Python 后端")
