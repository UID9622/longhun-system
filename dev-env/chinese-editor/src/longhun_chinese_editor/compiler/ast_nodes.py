#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 抽象语法树节点（brace-based 版）
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-AST-v1.0
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ASTNode:
    line: int = 1
    col: int = 1


# ========== 声明 ==========
@dataclass
class Program(ASTNode):
    decls: List[ASTNode] = field(default_factory=list)


@dataclass
class FuncDecl(ASTNode):
    name: str = ""
    params: List[Dict[str, str]] = field(default_factory=list)
    return_type: str = "空值"
    body: "Block" = field(default_factory=lambda: Block())


@dataclass
class VarDecl(ASTNode):
    name: str = ""
    vtype: str = "空值"
    init: Optional[ASTNode] = None
    is_const: bool = False


@dataclass
class ClassDecl(ASTNode):
    name: str = ""
    members: List[ASTNode] = field(default_factory=list)


# ========== 语句 ==========
@dataclass
class Block(ASTNode):
    stmts: List[ASTNode] = field(default_factory=list)


@dataclass
class IfStmt(ASTNode):
    cond: ASTNode = field(default_factory=lambda: Literal("True"))
    true_branch: Block = field(default_factory=lambda: Block())
    false_branch: Optional[ASTNode] = None  # Block 或 IfStmt（否则如果链）


@dataclass
class LoopStmt(ASTNode):
    count: ASTNode = field(default_factory=lambda: Literal("0"))
    body: Block = field(default_factory=lambda: Block())


@dataclass
class WhileStmt(ASTNode):
    cond: ASTNode = field(default_factory=lambda: Literal("True"))
    body: Block = field(default_factory=lambda: Block())


@dataclass
class ForStmt(ASTNode):
    var: str = ""
    iterable: ASTNode = field(default_factory=lambda: Call("range", [Literal("0")]))
    body: Block = field(default_factory=lambda: Block())


@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class BreakStmt(ASTNode):
    pass


@dataclass
class ContinueStmt(ASTNode):
    pass


@dataclass
class PrintStmt(ASTNode):
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class ExprStmt(ASTNode):
    expr: ASTNode = field(default_factory=lambda: Literal("None"))


# ========== 表达式 ==========
@dataclass
class Literal(ASTNode):
    value: Any = None
    kind: str = "unknown"  # number/string/bool/null


@dataclass
class Identifier(ASTNode):
    name: str = ""


@dataclass
class BinaryOp(ASTNode):
    op: str = ""
    left: ASTNode = field(default_factory=lambda: Literal("0"))
    right: ASTNode = field(default_factory=lambda: Literal("0"))


@dataclass
class UnaryOp(ASTNode):
    op: str = ""
    operand: ASTNode = field(default_factory=lambda: Literal("0"))


@dataclass
class Assignment(ASTNode):
    target: ASTNode = field(default_factory=lambda: Identifier(""))
    value: ASTNode = field(default_factory=lambda: Literal("0"))


@dataclass
class Call(ASTNode):
    name: str = ""
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class MemberAccess(ASTNode):
    obj: ASTNode = field(default_factory=lambda: Identifier(""))
    member: str = ""


@dataclass
class IndexAccess(ASTNode):
    obj: ASTNode = field(default_factory=lambda: Identifier(""))
    index: ASTNode = field(default_factory=lambda: Literal("0"))


@dataclass
class ArrayLiteral(ASTNode):
    items: List[ASTNode] = field(default_factory=list)


@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple[Any, ...]] = field(default_factory=list)


@dataclass
class ImportStmt(ASTNode):
    module: str = ""
    alias: Optional[str] = None


@dataclass
class CatchClause(ASTNode):
    exc_type: str = ""  # 空表示捕获所有异常
    body: Block = field(default_factory=lambda: Block())


@dataclass
class TryStmt(ASTNode):
    body: Block = field(default_factory=lambda: Block())
    catches: List[CatchClause] = field(default_factory=list)
    finally_body: Optional[Block] = None
