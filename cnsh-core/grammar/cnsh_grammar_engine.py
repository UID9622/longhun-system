#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 中文语法库底层引擎 v1.0

提供：词法分析、语法分析（AST）、DNA 校验、三色审计、CNSH→Python 转译。
DNA:#龍芯⚡️2026-06-29-CNSH-GRAMMAR-ENGINE-FILE1-v1-UID9622
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════════════════
DNA = "#龍芯⚡️2026-06-29-CNSH-GRAMMAR-ENGINE-v1-UID9622"

DNA_PATTERN = re.compile(
    r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Za-z0-9_\-]+"
)
CONFIRM_PATTERN = re.compile(
    r"#CONFIRM🌌9622-ONLY-ONCE🧬[A-Z0-9]+-[A-Z0-9]+"
)
ETERNAL_PATTERN = re.compile(
    r"#ZHUGEXIN⚡️\d{4}-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
)

# ═══════════════════════════════════════════════════════════════════════════
# 关键字映射（中文 + 英文别名 → 统一 token）
# ═══════════════════════════════════════════════════════════════════════════
KEYWORDS: Dict[str, str] = {
    # 控制流
    "如果": "IF", "if": "IF",
    "否则": "ELSE", "else": "ELSE",
    "否则如果": "ELIF", "elif": "ELIF", "else if": "ELIF",
    "当": "WHILE", "while": "WHILE",
    "对于": "FOR", "for": "FOR",
    "在": "IN", "in": "IN",
    "返回": "RETURN", "return": "RETURN",
    "跳出": "BREAK", "break": "BREAK",
    "继续": "CONTINUE", "continue": "CONTINUE",
    # 数据类型
    "字符串": "STRING_T", "string": "STRING_T",
    "整数": "INT_T", "integer": "INT_T",
    "浮点数": "FLOAT_T", "float": "FLOAT_T",
    "布尔": "BOOL_T", "boolean": "BOOL_T",
    "列表": "LIST_T", "list": "LIST_T",
    "映射": "MAP_T", "map": "MAP_T",
    "空": "NULL", "null": "NULL",
    "真": "TRUE", "true": "TRUE",
    "假": "FALSE", "false": "FALSE",
    # 龍魂专属
    "三色审计": "TRI_AUDIT", "tri_color_audit": "TRI_AUDIT",
    "DNA追溯": "DNA_TRACE", "dna_trace": "DNA_TRACE",
    "熔断": "ABORT", "abort": "ABORT",
    "回滚": "ROLLBACK", "rollback": "ROLLBACK",
    "钩子": "HOOK", "hook": "HOOK",
    "尝试": "TRY", "try": "TRY",
    "捕获": "CATCH", "catch": "CATCH",
    "最终": "FINALLY", "finally": "FINALLY",
    "定义": "DEF", "def": "DEF",
    "类": "CLASS", "class": "CLASS",
    "导入": "IMPORT", "import": "IMPORT",
}

PREFIX_WEIGHTS: Dict[str, int] = {
    "龍_": 100,
    "系统_": 80, "核心_": 80, "引擎_": 80,
    "模块_": 60, "用户_": 60, "数据_": 60,
    "辅助_": 40, "临时_": 40,
    "扩展_": 20, "访客_": 20,
}

# 繁体龍保护
SIMPLIFIED_DRAGON = re.compile(r"(?<!龍)龙(?!魂)")


# ═══════════════════════════════════════════════════════════════════════════
# Token / Lexer
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Token:
    type: str
    value: Any
    line: int
    col: int


class Lexer:
    """CNSH 词法分析器"""

    TOKEN_SPEC = [
        ("COMMENT", r"#.*"),
        ("STRING", r"'[^'\n]*'|\"[^\"\n]*\""),
        ("NUMBER", r"\d+\.\d+|\d+"),
        ("OP", r"==|!=|<=|>=|=>|->|\+\+|--|\*\*|//|[-+*/%=<>!&|]"),
        ("ASSIGN", r":"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("LBRACKET", r"\["),
        ("RBRACKET", r"\]"),
        ("COMMA", r","),
        ("DOT", r"\."),
        ("NEWLINE", r"\n"),
        ("SKIP", r"[ \t\r]+"),
        ("IDENT", r"[\u4e00-\u9fa5A-Za-z_][\u4e00-\u9fa5A-Za-z0-9_]*"),
        ("MISMATCH", r"."),
    ]

    TOK_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        line = 1
        col = 1
        for mo in re.finditer(self.TOK_REGEX, self.source):
            kind = mo.lastgroup
            value = mo.group()
            if kind in ("SKIP", "COMMENT"):
                col += len(value)
                continue
            if kind == "NEWLINE":
                line += 1
                col = 1
                continue
            if kind == "MISMATCH":
                raise SyntaxError(f"非法字符 {value!r} 在行 {line} 列 {col}")
            if kind == "IDENT" and value in KEYWORDS:
                kind = KEYWORDS[value]
            self.tokens.append(Token(kind, value, line, col))
            col += len(value)
        self.tokens.append(Token("EOF", "", line, col))
        return self.tokens


# ═══════════════════════════════════════════════════════════════════════════
# AST 节点
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class ASTNode:
    type: str
    line: int
    meta: Dict[str, Any] = field(default_factory=dict)


class Parser:
    """简易递归下降语法分析器，支持 CNSH 子集"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, token_type: str) -> Token:
        tok = self.current()
        if tok.type != token_type:
            raise SyntaxError(f"期望 {token_type}，得到 {tok.type} ({tok.value}) 在行 {tok.line}")
        return self.advance()

    def parse(self) -> List[ASTNode]:
        stmts: List[ASTNode] = []
        while self.current().type != "EOF":
            stmts.append(self.stmt())
        return stmts

    def stmt(self) -> ASTNode:
        tok = self.current()
        if tok.type == "DEF":
            return self.parse_def()
        if tok.type == "CLASS":
            return self.parse_class()
        if tok.type == "IF":
            return self.parse_if()
        if tok.type == "WHILE":
            return self.parse_while()
        if tok.type == "FOR":
            return self.parse_for()
        if tok.type == "RETURN":
            return self.parse_return()
        if tok.type == "TRY":
            return self.parse_try()
        if tok.type == "TRI_AUDIT":
            return self.parse_tri_audit()
        if tok.type == "DNA_TRACE":
            return self.parse_dna_trace()
        if tok.type == "ABORT":
            self.advance()
            return ASTNode("abort", tok.line)
        if tok.type == "ROLLBACK":
            self.advance()
            return ASTNode("rollback", tok.line)
        if tok.type == "IMPORT":
            return self.parse_import()
        return self.parse_assignment_or_expr()

    def parse_def(self) -> ASTNode:
        line = self.advance().line
        name = self.expect("IDENT").value
        self.expect("LPAREN")
        params = self.parse_params()
        self.expect("RPAREN")
        self.expect("LBRACE")
        body = self.block()
        return ASTNode("def", line, {"name": name, "params": params, "body": body})

    def parse_class(self) -> ASTNode:
        line = self.advance().line
        name = self.expect("IDENT").value
        self.expect("LBRACE")
        body = self.block()
        return ASTNode("class", line, {"name": name, "body": body})

    def parse_params(self) -> List[str]:
        params: List[str] = []
        if self.current().type == "IDENT":
            params.append(self.advance().value)
            while self.current().type == "COMMA":
                self.advance()
                params.append(self.expect("IDENT").value)
        return params

    def parse_if(self) -> ASTNode:
        line = self.advance().line
        cond = self.expr()
        self.expect("LBRACE")
        then_body = self.block()
        else_body: List[ASTNode] = []
        if self.current().type == "ELSE":
            self.advance()
            self.expect("LBRACE")
            else_body = self.block()
        elif self.current().type == "ELIF":
            else_body = [self.parse_if()]
        return ASTNode("if", line, {"cond": cond, "then": then_body, "else": else_body})

    def parse_while(self) -> ASTNode:
        line = self.advance().line
        cond = self.expr()
        self.expect("LBRACE")
        body = self.block()
        return ASTNode("while", line, {"cond": cond, "body": body})

    def parse_for(self) -> ASTNode:
        line = self.advance().line
        var = self.expect("IDENT").value
        self.expect("IN")
        iterable = self.expr()
        self.expect("LBRACE")
        body = self.block()
        return ASTNode("for", line, {"var": var, "iter": iterable, "body": body})

    def parse_return(self) -> ASTNode:
        line = self.advance().line
        value = None
        if self.current().type not in ("EOF", "RBRACE"):
            value = self.expr()
        return ASTNode("return", line, {"value": value})

    def parse_try(self) -> ASTNode:
        line = self.advance().line
        self.expect("LBRACE")
        try_body = self.block()
        catch_var = "error"
        catch_body: List[ASTNode] = []
        if self.current().type == "CATCH":
            self.advance()
            if self.current().type == "IDENT":
                catch_var = self.advance().value
            self.expect("LBRACE")
            catch_body = self.block()
        finally_body: List[ASTNode] = []
        if self.current().type == "FINALLY":
            self.advance()
            self.expect("LBRACE")
            finally_body = self.block()
        return ASTNode("try", line, {
            "try": try_body, "catch_var": catch_var,
            "catch": catch_body, "finally": finally_body,
        })

    def parse_tri_audit(self) -> ASTNode:
        line = self.advance().line
        expr_node = self.expr()
        return ASTNode("tri_audit", line, {"expr": expr_node})

    def parse_dna_trace(self) -> ASTNode:
        line = self.advance().line
        target = self.expr()
        return ASTNode("dna_trace", line, {"target": target})

    def parse_import(self) -> ASTNode:
        line = self.advance().line
        names = [self.expect("IDENT").value]
        while self.current().type == "COMMA":
            self.advance()
            names.append(self.expect("IDENT").value)
        return ASTNode("import", line, {"names": names})

    def parse_assignment_or_expr(self) -> ASTNode:
        left = self.expr()
        tok = self.current()
        if tok.type == "ASSIGN" or (tok.type == "OP" and tok.value == "="):
            self.advance()
            right = self.expr()
            return ASTNode("assign", tok.line, {"left": left, "right": right})
        return ASTNode("expr_stmt", tok.line, {"expr": left})

    def expr(self) -> Any:
        return self.comp()

    def _op(self, ops: set) -> bool:
        tok = self.current()
        return tok.type == "OP" and tok.value in ops

    def comp(self) -> Any:
        left = self.add()
        while self._op({"==", "!=", "<", ">", "<=", ">="}):
            op = self.advance().value
            right = self.add()
            left = ASTNode("binop", left.line, {"op": op, "left": left, "right": right})
        return left

    def add(self) -> Any:
        left = self.mul()
        while self._op({"+", "-"}):
            op = self.advance().value
            right = self.mul()
            left = ASTNode("binop", left.line, {"op": op, "left": left, "right": right})
        return left

    def mul(self) -> Any:
        left = self.atom()
        while self._op({"*", "/", "%"}):
            op = self.advance().value
            right = self.atom()
            left = ASTNode("binop", left.line, {"op": op, "left": left, "right": right})
        return left

    def parse_args(self) -> List[Any]:
        args: List[Any] = []
        if self.current().type != "RPAREN":
            args.append(self.expr())
            while self.current().type == "COMMA":
                self.advance()
                args.append(self.expr())
        return args

    def atom(self) -> Any:
        tok = self.current()
        if tok.type in ("NUMBER", "STRING", "TRUE", "FALSE", "NULL"):
            self.advance()
            return ASTNode("literal", tok.line, {"value": tok.value})
        if tok.type == "IDENT":
            line = tok.line
            self.advance()
            node: Any = ASTNode("ident", line, {"name": tok.value})
            # 方法/属性访问 / 函数调用
            while self.current().type == "DOT":
                self.advance()
                attr = self.expect("IDENT").value
                node = ASTNode("attr", line, {"obj": node, "attr": attr})
                if self.current().type == "LPAREN":
                    self.advance()
                    args = self.parse_args()
                    self.expect("RPAREN")
                    node = ASTNode("call", line, {"func": node, "args": args})
            if self.current().type == "LPAREN":
                self.advance()
                args = self.parse_args()
                self.expect("RPAREN")
                node = ASTNode("call", line, {"func": node, "args": args})
            return node
        if tok.type == "LPAREN":
            self.advance()
            node = self.expr()
            self.expect("RPAREN")
            return node
        if tok.type == "LBRACKET":
            self.advance()
            items: List[Any] = []
            if self.current().type != "RBRACKET":
                items.append(self.expr())
                while self.current().type == "COMMA":
                    self.advance()
                    items.append(self.expr())
            self.expect("RBRACKET")
            return ASTNode("list", tok.line, {"items": items})
        if tok.type == "LBRACE":
            self.advance()
            pairs: List[Tuple[str, Any]] = []
            if self.current().type != "RBRACE":
                key = self.expect("IDENT").value
                self.expect("ASSIGN")
                val = self.expr()
                pairs.append((key, val))
                while self.current().type == "COMMA":
                    self.advance()
                    key = self.expect("IDENT").value
                    self.expect("ASSIGN")
                    val = self.expr()
                    pairs.append((key, val))
            self.expect("RBRACE")
            return ASTNode("map", tok.line, {"pairs": pairs})
        raise SyntaxError(f"意外 token {tok.type} ({tok.value}) 在行 {tok.line}")

    def block(self) -> List[ASTNode]:
        body: List[ASTNode] = []
        while self.current().type != "RBRACE" and self.current().type != "EOF":
            body.append(self.stmt())
        self.expect("RBRACE")
        return body


# ═══════════════════════════════════════════════════════════════════════════
# DNA / 三色 / 文化主权审计
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class AuditItem:
    level: str  # 🟢 🟡 🔴
    dimension: str
    line: int
    message: str
    rule_id: str = ""


class CNSHAuditor:
    """CNSH 代码审计器：DNA、文化主权、权重、三色"""

    def __init__(self, source: str, ast: List[ASTNode]):
        self.source = source
        self.ast = ast
        self.items: List[AuditItem] = []

    def audit(self) -> Dict[str, Any]:
        self.check_header()
        self.check_dna()
        self.check_simplified_dragon()
        self.check_weight_prefix()
        self.check_forgidden_funcs()
        return {
            "dna": DNA,
            "items": [{"level": i.level, "dimension": i.dimension, "line": i.line, "message": i.message, "rule_id": i.rule_id} for i in self.items],
            "score": self._score(),
        }

    def check_header(self):
        lines = self.source.splitlines()
        has_dna = any(DNA_PATTERN.search(l) for l in lines[:20])
        has_confirm = any(CONFIRM_PATTERN.search(l) for l in lines[:20])
        has_creator = any("创建者" in l or "Author" in l for l in lines[:20])
        if not has_dna:
            self.items.append(AuditItem("🔴", "DNA追溯", 1, "缺少标准 DNA 追溯码"))
        if not has_creator:
            self.items.append(AuditItem("🟡", "归属权", 1, "缺少创建者/Author 声明"))
        if has_dna and has_creator:
            self.items.append(AuditItem("🟢", "文件头", 1, "文件头合规"))

    def check_dna(self):
        dnas = DNA_PATTERN.findall(self.source)
        for d in dnas:
            if "UID9622" not in d and "龍芯" not in d:
                self.items.append(AuditItem("🟡", "DNA追溯", 1, f"DNA 未含 UID9622/龍芯: {d}"))

    def check_simplified_dragon(self):
        for i, line in enumerate(self.source.splitlines(), 1):
            if "龙" in line and not SIMPLIFIED_DRAGON.search(line):
                continue
            if "龙" in line:
                self.items.append(AuditItem("🔴", "文化主权", i, "发现简体「龙」字，应使用繁体「龍」"))

    def check_weight_prefix(self):
        for node in self.ast:
            if node.type == "def":
                name: str = node.meta.get("name", "")
                for prefix, weight in PREFIX_WEIGHTS.items():
                    if name.startswith(prefix):
                        self.items.append(AuditItem("🟢", "权重指向", node.line, f"函数 {name} 前缀权重 {weight}"))
                        break

    def check_forgidden_funcs(self):
        forbidden = {"eval": "直接执行字符串代码", "exec": "执行任意代码"}
        for node in self.ast:
            if node.type == "expr_stmt":
                expr = node.meta.get("expr")
                if isinstance(expr, ASTNode) and expr.type == "ident" and expr.meta.get("name") in forbidden:
                    self.items.append(AuditItem("🔴", "安全漏洞", node.line, f"调用 {expr.meta['name']}：{forbidden[expr.meta['name']]}", "CNSH-R001"))

    def _score(self) -> str:
        reds = sum(1 for i in self.items if i.level == "🔴")
        yellows = sum(1 for i in self.items if i.level == "🟡")
        if reds:
            return "🔴"
        if yellows:
            return "🟡"
        return "🟢"


# ═══════════════════════════════════════════════════════════════════════════
# CNSH → Python 转译器（子集）
# ═══════════════════════════════════════════════════════════════════════════
class PythonTranspiler:
    """把 CNSH AST 转译成 Python 代码"""

    def __init__(self, ast: List[ASTNode]):
        self.ast = ast
        self.indent = 0

    def transpile(self) -> str:
        lines = [
            "# -*- coding: utf-8 -*-",
            f"# 由 CNSH 语法引擎自动生成",
            f"# DNA: {DNA}",
            "",
        ]
        for node in self.ast:
            lines.extend(self.gen(node))
        return "\n".join(lines)

    def gen(self, node: ASTNode) -> List[str]:
        if node.type == "def":
            name = node.meta["name"]
            params = ", ".join(node.meta["params"])
            header = f"def {name}({params}):"
            body = [self._line(self.gen(s)) for s in node.meta["body"]]
            if not body:
                body = [self._line("pass")]
            return [header] + body
        if node.type == "class":
            name = node.meta["name"]
            header = f"class {name}:"
            body = [self._line(self.gen(s)) for s in node.meta["body"]]
            if not body:
                body = [self._line("pass")]
            return [header] + body
        if node.type == "if":
            cond = self._expr(node.meta["cond"])
            lines = [f"if {cond}:"]
            lines += [self._line(self.gen(s)) for s in node.meta["then"]]
            if node.meta["else"]:
                if len(node.meta["else"]) == 1 and node.meta["else"][0].type == "if":
                    lines.append("else:")
                    lines += [self._line(self.gen(node.meta["else"][0]))]
                else:
                    lines.append("else:")
                    lines += [self._line(self.gen(s)) for s in node.meta["else"]]
            return lines
        if node.type == "while":
            cond = self._expr(node.meta["cond"])
            lines = [f"while {cond}:"]
            lines += [self._line(self.gen(s)) for s in node.meta["body"]]
            return lines
        if node.type == "for":
            var = node.meta["var"]
            it = self._expr(node.meta["iter"])
            lines = [f"for {var} in {it}:"]
            lines += [self._line(self.gen(s)) for s in node.meta["body"]]
            return lines
        if node.type == "return":
            val = node.meta.get("value")
            return [f"return {self._expr(val)}" if val else "return"]
        if node.type == "try":
            lines = ["try:"]
            lines += [self._line(self.gen(s)) for s in node.meta["try"]]
            cv = node.meta.get("catch_var", "error")
            lines.append(f"except Exception as {cv}:")
            lines += [self._line(self.gen(s)) for s in node.meta["catch"]]
            if node.meta.get("finally"):
                lines.append("finally:")
                lines += [self._line(self.gen(s)) for s in node.meta["finally"]]
            return lines
        if node.type == "assign":
            left = self._expr(node.meta["left"])
            right = self._expr(node.meta["right"])
            return [f"{left} = {right}"]
        if node.type == "expr_stmt":
            return [self._expr(node.meta["expr"])]
        if node.type == "tri_audit":
            expr = self._expr(node.meta["expr"])
            return [f"# 三色审计: {expr}"]
        if node.type == "dna_trace":
            target = self._expr(node.meta["target"])
            return [f"# DNA追溯: {target}"]
        if node.type == "abort":
            return ["raise SystemExit('CNSH 熔断')"]
        if node.type == "rollback":
            return ["# CNSH 回滚"]
        return [f"# 未转译节点 {node.type}"]

    def _line(self, content: List[str]) -> str:
        return "    " + "\n    ".join(content)

    def _expr(self, node: Any) -> str:
        if isinstance(node, ASTNode):
            if node.type == "literal":
                return str(node.meta["value"])
            if node.type == "ident":
                return node.meta["name"]
            if node.type == "binop":
                left = self._expr(node.meta["left"])
                right = self._expr(node.meta["right"])
                return f"{left} {node.meta['op']} {right}"
            if node.type == "list":
                items = ", ".join(self._expr(i) for i in node.meta["items"])
                return f"[{items}]"
            if node.type == "map":
                pairs = ", ".join(f"{k!r}: {self._expr(v)}" for k, v in node.meta["pairs"])
                return f"{{{pairs}}}"
            if node.type == "attr":
                obj = self._expr(node.meta["obj"])
                return f"{obj}.{node.meta['attr']}"
            if node.type == "call":
                func = self._expr(node.meta["func"])
                args = ", ".join(self._expr(a) for a in node.meta["args"])
                return f"{func}({args})"
        return str(node)


# ═══════════════════════════════════════════════════════════════════════════
# 顶层引擎
# ═══════════════════════════════════════════════════════════════════════════
class CNSHEngine:
    """CNSH 语法引擎统一入口"""

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.ast: List[ASTNode] = []
        self.audit_report: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self) -> Dict[str, Any]:
        try:
            lexer = Lexer(self.source)
            self.tokens = lexer.tokenize()
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            auditor = CNSHAuditor(self.source, self.ast)
            self.audit_report = auditor.audit()
        except Exception as e:
            self.errors.append(str(e))
        return self.report()

    def report(self) -> Dict[str, Any]:
        return {
            "dna": DNA,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "token_count": len(self.tokens),
            "ast_nodes": len(self.ast),
            "audit": self.audit_report,
            "errors": self.errors,
            "status": "🟢" if not self.errors and self.audit_report.get("score") == "🟢" else "🟡" if not self.errors else "🔴",
        }

    def to_python(self) -> Optional[str]:
        if not self.ast:
            return None
        return PythonTranspiler(self.ast).transpile()


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════
def main(argv: List[str] = sys.argv) -> int:
    if len(argv) < 2:
        print("用法: python3 cnsh_grammar_engine.py <file.cnsh> [--py]")
        return 1
    path = Path(argv[1])
    source = path.read_text(encoding="utf-8")
    engine = CNSHEngine(source)
    report = engine.run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if "--py" in argv:
        py_code = engine.to_python()
        if py_code:
            out = path.with_suffix(".cnsh.py")
            out.write_text(py_code, encoding="utf-8")
            print(f"\n已转译: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
