#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 递归下降语法分析器（brace-based 版）
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-PARSER-v1.0
"""
from __future__ import annotations

from typing import List, Optional, Any

from .ast_nodes import *
from .lexer import Token, TokenType


BUILTIN_CALLABLES = {"输入", "范围", "长度", "打印"}


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def _match(self, *types: TokenType) -> bool:
        return self._peek().type in types

    def _consume(self, expected: TokenType = None, value: str | None = None) -> Token:
        tok = self._peek()
        if expected and tok.type != expected:
            raise ParseError(f"期望 {expected.name}，得到 {tok} (L{tok.line}C{tok.col})")
        if value and tok.value != value:
            raise ParseError(f"期望 '{value}'，得到 '{tok.value}' (L{tok.line}C{tok.col})")
        self.pos += 1
        return tok

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            self._consume(TokenType.NEWLINE)

    def parse(self) -> Program:
        decls: List[ASTNode] = []
        while not self._match(TokenType.EOF):
            self._skip_newlines()
            if self._match(TokenType.EOF):
                break
            decls.append(self._parse_decl())
        return Program(decls=decls, line=1, col=1)

    def _parse_decl(self) -> ASTNode:
        tok = self._peek()
        if tok.type == TokenType.TYPE:
            return self._parse_var_decl()
        if tok.type == TokenType.KEYWORD:
            if tok.value == "常量":
                return self._parse_var_decl(is_const=True)
            if tok.value == "函数":
                return self._parse_func_decl()
            if tok.value == "类":
                return self._parse_class_decl()
            # 语句级关键字继续走 stmt
            return self._parse_stmt()
        return self._parse_stmt()

    def _parse_var_decl(self, is_const: bool = False) -> VarDecl:
        line, col = self._peek().line, self._peek().col
        if self._match(TokenType.KEYWORD) and self._peek().value == "常量":
            self._consume(TokenType.KEYWORD)
            is_const = True
        vtype = self._consume(TokenType.TYPE).value
        name = self._consume(TokenType.IDENT).value
        init = None
        if self._match(TokenType.OP) and self._peek().value == "=":
            self._consume(TokenType.OP)
            init = self._parse_expr()
        if self._match(TokenType.SEMI):
            self._consume(TokenType.SEMI)
        return VarDecl(name=name, vtype=vtype, init=init, is_const=is_const, line=line, col=col)

    def _parse_func_decl(self) -> FuncDecl:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "函数")
        name = self._consume(TokenType.IDENT).value
        self._consume(TokenType.LPAREN)
        params = self._parse_params()
        self._consume(TokenType.RPAREN)
        return_type = "空值"
        if self._match(TokenType.OP) and self._peek().value == "->":
            self._consume(TokenType.OP)
            return_type = self._consume(TokenType.TYPE).value
        if self._match(TokenType.KEYWORD) and self._peek().value == "返回类型":
            self._consume(TokenType.KEYWORD)
            return_type = self._consume(TokenType.TYPE).value
        body = self._parse_block()
        return FuncDecl(name=name, params=params, return_type=return_type, body=body, line=line, col=col)

    def _parse_params(self) -> List[dict[str, Any]]:
        params: List[dict[str, Any]] = []
        if self._match(TokenType.RPAREN):
            return params
        while True:
            ptype = self._consume(TokenType.TYPE).value
            pname = self._consume(TokenType.IDENT).value
            params.append({"type": ptype, "name": pname})
            if self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
            else:
                break
        return params

    def _parse_class_decl(self) -> ClassDecl:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "类")
        name = self._consume(TokenType.IDENT).value
        body = self._parse_block()
        return ClassDecl(name=name, members=body.stmts, line=line, col=col)

    def _parse_block(self) -> Block:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.LBRACE)
        stmts: List[ASTNode] = []
        while not self._match(TokenType.RBRACE):
            self._skip_newlines()
            if self._match(TokenType.RBRACE, TokenType.EOF):
                break
            stmts.append(self._parse_decl())
        self._consume(TokenType.RBRACE)
        return Block(stmts=stmts, line=line, col=col)

    def _parse_stmt(self) -> ASTNode:
        self._skip_newlines()
        tok = self._peek()
        if tok.type != TokenType.KEYWORD:
            stmt = self._parse_expr_stmt()
            if self._match(TokenType.SEMI):
                self._consume(TokenType.SEMI)
            return stmt
        if tok.value == "如果":
            return self._parse_if_stmt()
        if tok.value == "循环":
            return self._parse_loop_stmt()
        if tok.value == "当":
            return self._parse_while_stmt()
        if tok.value == "对于":
            return self._parse_for_stmt()
        if tok.value == "返回":
            return self._parse_return_stmt()
        if tok.value == "跳出":
            self._consume(TokenType.KEYWORD)
            if self._match(TokenType.SEMI):
                self._consume(TokenType.SEMI)
            return BreakStmt(line=tok.line, col=tok.col)
        if tok.value == "继续":
            self._consume(TokenType.KEYWORD)
            if self._match(TokenType.SEMI):
                self._consume(TokenType.SEMI)
            return ContinueStmt(line=tok.line, col=tok.col)
        if tok.value == "打印":
            return self._parse_print_stmt()
        if tok.value == "尝试":
            return self._parse_try_stmt()
        if tok.value == "导入":
            return self._parse_import_stmt()
        # 否则作为表达式语句
        stmt = self._parse_expr_stmt()
        if self._match(TokenType.SEMI):
            self._consume(TokenType.SEMI)
        return stmt

    def _parse_if_stmt(self) -> IfStmt:
        line, col = self._peek().line, self._peek().col
        tok = self._peek()
        if tok.value == "如果":
            self._consume(TokenType.KEYWORD, "如果")
        elif tok.value == "否则如果":
            self._consume(TokenType.KEYWORD, "否则如果")
        else:
            self._consume(TokenType.KEYWORD, "如果")
        self._consume(TokenType.LPAREN)
        cond = self._parse_expr()
        self._consume(TokenType.RPAREN)
        true_branch = self._parse_block()
        false_branch = None
        if self._match(TokenType.KEYWORD) and self._peek().value == "否则如果":
            # elif 链：false_branch 挂另一个 IfStmt
            false_branch = self._parse_if_stmt()
        elif self._match(TokenType.KEYWORD) and self._peek().value == "否则":
            self._consume(TokenType.KEYWORD)
            false_branch = self._parse_block()
        return IfStmt(cond=cond, true_branch=true_branch, false_branch=false_branch, line=line, col=col)

    def _parse_loop_stmt(self) -> LoopStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "循环")
        self._consume(TokenType.LPAREN)
        count = self._parse_expr()
        self._consume(TokenType.RPAREN)
        body = self._parse_block()
        return LoopStmt(count=count, body=body, line=line, col=col)

    def _parse_while_stmt(self) -> WhileStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "当")
        self._consume(TokenType.LPAREN)
        cond = self._parse_expr()
        self._consume(TokenType.RPAREN)
        body = self._parse_block()
        return WhileStmt(cond=cond, body=body, line=line, col=col)

    def _parse_for_stmt(self) -> ForStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "对于")
        # 可选类型: 对于 整数 索引 在 ... / 对于 索引 在 ...
        if self._match(TokenType.TYPE):
            self._consume(TokenType.TYPE)
        var = self._consume(TokenType.IDENT).value
        self._consume(TokenType.KEYWORD, "在")
        iterable: ASTNode
        if self._match(TokenType.KEYWORD) and self._peek().value == "范围":
            self._consume(TokenType.KEYWORD)
            self._consume(TokenType.LPAREN)
            end = self._parse_expr()
            self._consume(TokenType.RPAREN)
            iterable = Call(name="range", args=[end], line=line, col=col)
        else:
            iterable = self._parse_expr()
        body = self._parse_block()
        return ForStmt(var=var, iterable=iterable, body=body, line=line, col=col)

    def _parse_return_stmt(self) -> ReturnStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "返回")
        value = None
        if not (self._match(TokenType.RBRACE, TokenType.NEWLINE, TokenType.SEMI, TokenType.EOF)):
            value = self._parse_expr()
        if self._match(TokenType.SEMI):
            self._consume(TokenType.SEMI)
        return ReturnStmt(value=value, line=line, col=col)

    def _parse_print_stmt(self) -> PrintStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "打印")
        args: List[ASTNode] = []
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            if not self._match(TokenType.RPAREN):
                args.append(self._parse_expr())
                while self._match(TokenType.COMMA):
                    self._consume(TokenType.COMMA)
                    args.append(self._parse_expr())
            self._consume(TokenType.RPAREN)
        else:
            # 支持 打印 "..." 或 打印 表达式（无括号）
            args.append(self._parse_expr())
        if self._match(TokenType.SEMI):
            self._consume(TokenType.SEMI)
        return PrintStmt(args=args, line=line, col=col)

    def _parse_import_stmt(self) -> ImportStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "导入")
        if self._match(TokenType.STRING):
            module = self._consume(TokenType.STRING).value
        else:
            module = self._consume(TokenType.IDENT).value
        alias = None
        if self._match(TokenType.KEYWORD) and self._peek().value == "作为":
            self._consume(TokenType.KEYWORD)
            alias = self._consume(TokenType.IDENT).value
        if self._match(TokenType.SEMI):
            self._consume(TokenType.SEMI)
        return ImportStmt(module=module, alias=alias, line=line, col=col)

    def _parse_try_stmt(self) -> TryStmt:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "尝试")
        body = self._parse_block()
        catches: List[CatchClause] = []
        finally_body: Optional[Block] = None
        while self._match(TokenType.KEYWORD) and self._peek().value == "捕获":
            catches.append(self._parse_catch_clause())
        if self._match(TokenType.KEYWORD) and self._peek().value == "最终":
            self._consume(TokenType.KEYWORD)
            finally_body = self._parse_block()
        return TryStmt(body=body, catches=catches, finally_body=finally_body, line=line, col=col)

    def _parse_catch_clause(self) -> CatchClause:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.KEYWORD, "捕获")
        exc_type = ""
        if self._match(TokenType.LPAREN):
            self._consume(TokenType.LPAREN)
            if self._match(TokenType.IDENT):
                exc_type = self._consume(TokenType.IDENT).value
            self._consume(TokenType.RPAREN)
        body = self._parse_block()
        return CatchClause(exc_type=exc_type, body=body, line=line, col=col)

    def _parse_expr_stmt(self) -> ExprStmt:
        line, col = self._peek().line, self._peek().col
        expr = self._parse_expr()
        return ExprStmt(expr=expr, line=line, col=col)

    # ===== 表达式优先级 =====
    def _parse_expr(self) -> ASTNode:
        node = self._parse_or()
        if self._match(TokenType.OP) and self._peek().value == "=":
            line, col = node.line, node.col
            self._consume(TokenType.OP)
            return Assignment(target=node, value=self._parse_expr(), line=line, col=col)
        return node

    def _parse_or(self) -> ASTNode:
        node = self._parse_and()
        while self._match(TokenType.KEYWORD) and self._peek().value in ("或", "或者"):
            op = self._consume(TokenType.KEYWORD).value
            node = BinaryOp(op="or", left=node, right=self._parse_and(), line=node.line, col=node.col)
        return node

    def _parse_and(self) -> ASTNode:
        node = self._parse_eq()
        while self._match(TokenType.KEYWORD) and self._peek().value in ("且", "并且"):
            op = self._consume(TokenType.KEYWORD).value
            node = BinaryOp(op="and", left=node, right=self._parse_eq(), line=node.line, col=node.col)
        return node

    def _parse_eq(self) -> ASTNode:
        node = self._parse_rel()
        while self._match(TokenType.OP) and self._peek().value in ("==", "!="):
            op = self._consume(TokenType.OP).value
            node = BinaryOp(op=op, left=node, right=self._parse_rel(), line=node.line, col=node.col)
        return node

    def _parse_rel(self) -> ASTNode:
        node = self._parse_add()
        while self._match(TokenType.OP) and self._peek().value in ("<", ">", "<=", ">="):
            op = self._consume(TokenType.OP).value
            node = BinaryOp(op=op, left=node, right=self._parse_add(), line=node.line, col=node.col)
        return node

    def _parse_add(self) -> ASTNode:
        node = self._parse_mul()
        while self._match(TokenType.OP) and self._peek().value in ("+", "-"):
            op = self._consume(TokenType.OP).value
            node = BinaryOp(op=op, left=node, right=self._parse_mul(), line=node.line, col=node.col)
        return node

    def _parse_mul(self) -> ASTNode:
        node = self._parse_pow()
        while self._match(TokenType.OP) and self._peek().value in ("*", "/", "%"):
            op = self._consume(TokenType.OP).value
            node = BinaryOp(op=op, left=node, right=self._parse_pow(), line=node.line, col=node.col)
        return node

    def _parse_pow(self) -> ASTNode:
        node = self._parse_unary()
        if self._match(TokenType.OP) and self._peek().value == "**":
            op = self._consume(TokenType.OP).value
            node = BinaryOp(op=op, left=node, right=self._parse_pow(), line=node.line, col=node.col)
        return node

    def _parse_unary(self) -> ASTNode:
        if self._match(TokenType.OP) and self._peek().value in ("-", "+"):
            op = self._consume(TokenType.OP).value
            return UnaryOp(op=op, operand=self._parse_unary(), line=self._peek().line, col=self._peek().col)
        if self._match(TokenType.KEYWORD) and self._peek().value == "非":
            self._consume(TokenType.KEYWORD)
            return UnaryOp(op="not", operand=self._parse_unary(), line=self._peek().line, col=self._peek().col)
        return self._parse_postfix(self._parse_primary())

    def _parse_primary(self) -> ASTNode:
        tok = self._peek()
        if tok.type == TokenType.NUMBER:
            self._consume(TokenType.NUMBER)
            return Literal(value=tok.value, kind="number", line=tok.line, col=tok.col)
        if tok.type == TokenType.STRING:
            self._consume(TokenType.STRING)
            return Literal(value=tok.value, kind="string", line=tok.line, col=tok.col)
        if tok.type == TokenType.BOOL:
            self._consume(TokenType.BOOL)
            return Literal(value=tok.value == "真", kind="bool", line=tok.line, col=tok.col)
        if tok.type == TokenType.NULL:
            self._consume(TokenType.NULL)
            return Literal(value=None, kind="null", line=tok.line, col=tok.col)
        if tok.type == TokenType.IDENT or (tok.type == TokenType.KEYWORD and tok.value in BUILTIN_CALLABLES):
            self._consume()
            return Identifier(name=tok.value, line=tok.line, col=tok.col)
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            node = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return node
        if tok.type == TokenType.LBRACKET:
            return self._parse_array_literal()
        if tok.type == TokenType.LBRACE:
            return self._parse_dict_literal()
        raise ParseError(f"未预期的 token: {tok} (L{tok.line}C{tok.col})")

    def _parse_postfix(self, node: ASTNode) -> ASTNode:
        """处理函数调用、成员访问、索引访问"""
        while True:
            if self._match(TokenType.LPAREN):
                self._consume(TokenType.LPAREN)
                args: List[ASTNode] = []
                if not self._match(TokenType.RPAREN):
                    args.append(self._parse_expr())
                    while self._match(TokenType.COMMA):
                        self._consume(TokenType.COMMA)
                        args.append(self._parse_expr())
                self._consume(TokenType.RPAREN)
                node = Call(name=self._expr_to_name(node), args=args, line=node.line, col=node.col)
            elif self._match(TokenType.OP) and self._peek().value == ".":
                self._consume(TokenType.OP)
                member = self._consume(TokenType.IDENT).value
                node = MemberAccess(obj=node, member=member, line=node.line, col=node.col)
            elif self._match(TokenType.LBRACKET):
                self._consume(TokenType.LBRACKET)
                index = self._parse_expr()
                self._consume(TokenType.RBRACKET)
                node = IndexAccess(obj=node, index=index, line=node.line, col=node.col)
            else:
                return node

    @staticmethod
    def _expr_to_name(node: ASTNode) -> str:
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, MemberAccess):
            return f"{Parser._expr_to_name(node.obj)}.{node.member}"
        raise ParseError(f"不可调用的表达式: {node}")

    def _parse_array_literal(self) -> ArrayLiteral:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.LBRACKET)
        items: List[ASTNode] = []
        if not self._match(TokenType.RBRACKET):
            items.append(self._parse_expr())
            while self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                items.append(self._parse_expr())
        self._consume(TokenType.RBRACKET)
        return ArrayLiteral(items=items, line=line, col=col)

    def _parse_dict_literal(self) -> DictLiteral:
        line, col = self._peek().line, self._peek().col
        self._consume(TokenType.LBRACE)
        pairs: List[tuple[Any, ...]] = []
        if not self._match(TokenType.RBRACE):
            key = self._parse_expr()
            self._consume(TokenType.OP, ":")
            value = self._parse_expr()
            pairs.append((key, value))
            while self._match(TokenType.COMMA):
                self._consume(TokenType.COMMA)
                key = self._parse_expr()
                self._consume(TokenType.OP, ":")
                value = self._parse_expr()
                pairs.append((key, value))
        self._consume(TokenType.RBRACE)
        return DictLiteral(pairs=pairs, line=line, col=col)


def parse(tokens: List[Token]) -> Program:
    return Parser(tokens).parse()
