#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-JS-GEN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH → JavaScript 代码生成器（target=js 后端）
复用 08_BIN/cnsh_compiler.py 的词法/语法/AST，独立实现 JS 代码生成，零风险不碰 Python 链路。
用法:
  python3 08_BIN/cnsh.py build hello.cnsh --target js      # 统一入口
  python3 08_BIN/cnsh_jsgen.py hello.cnsh -o hello.js     # 直接调用
"""
import sys
import os
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cnsh_compiler import (Lexer, Parser, ProgramNode, FunctionDefNode, ReturnNode,
                           IfNode, ForNode, WhileNode, BreakNode, ContinueNode,
                           ImportNode, AssignNode, CallNode, IdentifierNode,
                           NumberNode, StringNode, ListNode, DictNode,
                           AttributeNode, UnaryOpNode, BinaryOpNode)

# ── JS 运行时头部（注入生成代码，提供 CNSH 内置词）──────────────────
JS_RUNTIME_HEADER = """// ═══════ CNSH Runtime (JS) · 龍魂内置词 ═══════
const CNSH = {
  打印: (...a) => console.log(...a),
  输入: () => { throw new Error('[CNSH] 输入 在 JS target 不可用（请用 Node readline 自行封装）'); },
  长度: (x) => (x == null ? 0 : (typeof x.length === 'number' ? x.length : Object.keys(x).length)),
  类型: (x) => typeof x,
  范围: (n) => Array.from({ length: n }, (_, i) => i),
  字符串: (x) => String(x),
  数字: (x) => Number(x),
  解析JSON: (s) => JSON.parse(s),
  生成JSON: (o) => JSON.stringify(o),
  列表: (...a) => [...a],
};
"""


class CNSHToJS:
    """CNSH AST → JavaScript 文本"""

    def __init__(self):
        self.lines = []
        self.indent_level = 0
        self.declared = set()  # 已声明变量（避免重复 let）

    # ── 基础工具 ─────────────────────────
    def add(self, line: str = ""):
        if line.strip():
            self.lines.append("    " * self.indent_level + line)
        else:
            self.lines.append("")

    def _expr(self, node) -> str:
        if node is None:
            return "null"
        if isinstance(node, NumberNode):
            return str(node.value)
        if isinstance(node, StringNode):
            return json.dumps(node.value, ensure_ascii=False)
        if isinstance(node, IdentifierNode):
            return {"空": "null", "真": "true", "假": "false"}.get(node.name, node.name)
        if isinstance(node, BinaryOpNode):
            l, r = self._expr(node.left), self._expr(node.right)
            return {"和": "&&", "或": "||"}.get(node.op, node.op).join([f"({l})", f"({r})"])
        if isinstance(node, UnaryOpNode):
            return {"非": "!", "负": "-", "-": "-"}.get(node.op, node.op) + f"({self._expr(node.operand)})"
        if isinstance(node, CallNode):
            args = ", ".join(self._expr(a) for a in node.args)
            if node.name in ("打印", "长度", "类型", "范围", "字符串", "数字",
                             "解析JSON", "生成JSON", "列表", "输入"):
                return f"CNSH.{node.name}({args})"
            return f"{node.name}({args})"
        if isinstance(node, ListNode):
            return "[" + ", ".join(self._expr(e) for e in node.elements) + "]"
        if isinstance(node, DictNode):
            parts = []
            for k, v in node.pairs:
                key = self._expr(k)
                if isinstance(k, StringNode):
                    key = json.dumps(k.value, ensure_ascii=False)
                parts.append(f"{key}: {self._expr(v)}")
            return "{" + ", ".join(parts) + "}"
        if isinstance(node, AttributeNode):
            return f"{self._expr(node.obj)}.{node.attr}"
        return ""

    # ── 语句生成 ─────────────────────────
    def _stmt(self, node):
        if isinstance(node, FunctionDefNode):
            params = ", ".join(p[0] for p in node.params)
            self.add(f"function {node.name}({params}) {{")
            self.indent_level += 1
            for s in node.body:
                self._stmt(s)
            self.indent_level -= 1
            self.add("}")
        elif isinstance(node, ReturnNode):
            self.add("return " + (self._expr(node.value) if node.value else "") + ";")
        elif isinstance(node, IfNode):
            self.add(f"if ({self._expr(node.condition)}) {{")
            self.indent_level += 1
            for s in node.body:
                self._stmt(s)
            self.indent_level -= 1
            if node.else_body:
                # 检查是否 否则如果 链（嵌套 IfNode）
                elifs = [s for s in node.else_body if isinstance(s, IfNode)]
                plain = [s for s in node.else_body if not isinstance(s, IfNode)]
                for st in elifs:
                    self.add(f"}} else if ({self._expr(st.condition)}) {{")
                    self.indent_level += 1
                    for s in st.body:
                        self._stmt(s)
                    self.indent_level -= 1
                if plain:
                    self.add("} else {")
                    self.indent_level += 1
                    for s in plain:
                        self._stmt(s)
                    self.indent_level -= 1
            self.add("}")
        elif isinstance(node, ForNode):
            it = self._expr(node.iterable)
            self.add(f"for (const {node.variable} of {it}) {{")
            self.indent_level += 1
            for s in node.body:
                self._stmt(s)
            self.indent_level -= 1
            self.add("}")
        elif isinstance(node, WhileNode):
            self.add(f"while ({self._expr(node.condition)}) {{")
            self.indent_level += 1
            for s in node.body:
                self._stmt(s)
            self.indent_level -= 1
            self.add("}")
        elif isinstance(node, BreakNode):
            self.add("break;")
        elif isinstance(node, ContinueNode):
            self.add("continue;")
        elif isinstance(node, ImportNode):
            self.add(f"// [CNSH import] {node.module}" + (f" as {node.alias}" if node.alias else ""))
        elif isinstance(node, AssignNode):
            decl = "let " if node.target not in self.declared else ""
            self.declared.add(node.target)
            self.add(f"{decl}{node.target} = {self._expr(node.value)};")
        elif isinstance(node, CallNode):
            self.add(self._expr(node) + ";")
        else:
            e = self._expr(node)
            if e:
                self.add(e + ";")

    # ── 主入口 ─────────────────────────
    def generate(self, ast: ProgramNode, filename: str = "<stdin>") -> str:
        self.lines = []
        self.declared = set()
        self.indent_level = 0
        self.add("// ═══════ 由 CNSH 编译器自动生成 (target=js) ═══════")
        self.add(f"// DNA: {ast.dna or '未指定'}")
        if ast.confirm:
            self.add(f"// 确认码: {ast.confirm}")
        self.add(JS_RUNTIME_HEADER.strip("\n"))
        self.add("// ═══════ 程序主体 ═══════")
        for stmt in ast.statements:
            self._stmt(stmt)
        return "\n".join(self.lines)


def compile_source(source: str, filename: str = "<stdin>") -> dict:
    """词法+语法解析 → AST → JS"""
    lexer = Lexer(source, filename)
    tokens = lexer.tokenize()
    if lexer.errors:
        return {"success": False, "errors": lexer.errors}
    parser = Parser(tokens)
    ast = parser.parse()
    if parser.errors:
        return {"success": False, "errors": parser.errors}
    gen = CNSHToJS()
    return {"success": True, "errors": [], "js_code": gen.generate(ast, filename)}


def main():
    ap = argparse.ArgumentParser(description="🐉 CNSH→JS 代码生成器 v1.0")
    ap.add_argument("input", help="CNSH 源文件 (.cnsh)")
    ap.add_argument("-o", "--output", help="输出 JS 文件 (.js)")
    args = ap.parse_args()

    src_path = Path(args.input)
    if not src_path.exists():
        print(f"❌ 文件不存在: {src_path}")
        sys.exit(1)
    source = src_path.read_text(encoding="utf-8")
    result = compile_source(source, str(src_path))
    if not result["success"]:
        print("❌ 编译失败:")
        for e in result["errors"]:
            print(f"  {e}")
        sys.exit(1)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result["js_code"] + "\n", encoding="utf-8")
        print(f"✅ JS 生成成功: {out}")
    else:
        print(result["js_code"])


if __name__ == "__main__":
    main()
