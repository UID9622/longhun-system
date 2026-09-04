#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 抽象语法树节点
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-AST-v2.1
"""
from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class ASTNode:
    line: int = 0
    column: int = 0


@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class ModuleDecl(ASTNode):
    name: str = ""
    weight: Optional[int] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class FunctionDecl(ASTNode):
    name: str = ""
    params: List["Parameter"] = field(default_factory=list)
    return_type_annotation: Optional[str] = None
    weight: Optional[int] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class Parameter(ASTNode):
    name: str = ""
    type_annotation: Optional[str] = None


@dataclass
class VarDecl(ASTNode):
    name: str = ""
    initializer: Optional[ASTNode] = None
    is_const: bool = False
    type_annotation: Optional[str] = None


@dataclass
class StructDecl(ASTNode):
    name: str = ""
    fields: List["Parameter"] = field(default_factory=list)


@dataclass
class UseStmt(ASTNode):
    module_path: List[str] = field(default_factory=list)


@dataclass
class IfStmt(ASTNode):
    condition: Optional[ASTNode] = None
    then_body: List[ASTNode] = field(default_factory=list)
    elif_branches: List["ElifBranch"] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class ElifBranch(ASTNode):
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileStmt(ASTNode):
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForStmt(ASTNode):
    var_name: str = ""
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


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
class ExpressionStmt(ASTNode):
    expression: Optional[ASTNode] = None


# 表达式节点

@dataclass
class BinaryExpr(ASTNode):
    op: str = ""
    left: Optional[ASTNode] = None
    right: Optional[ASTNode] = None


@dataclass
class UnaryExpr(ASTNode):
    op: str = ""
    operand: Optional[ASTNode] = None


@dataclass
class LiteralExpr(ASTNode):
    value: Any = None


@dataclass
class IdentifierExpr(ASTNode):
    name: str = ""


@dataclass
class CallExpr(ASTNode):
    callee: Optional[ASTNode] = None
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class MemberExpr(ASTNode):
    object: Optional[ASTNode] = None
    member: str = ""


@dataclass
class IndexExpr(ASTNode):
    object: Optional[ASTNode] = None
    index: Optional[ASTNode] = None


@dataclass
class ListExpr(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class MapExpr(ASTNode):
    pairs: List["MapPair"] = field(default_factory=list)


@dataclass
class MapPair(ASTNode):
    key: Optional[ASTNode] = None
    value: Optional[ASTNode] = None


# ═══════════════════════════════════════════════════════════════
# 新增：类 / 装饰器 / 生成器 / 异步 / 上下文管理器 / 枚举 / 数据类
# ═══════════════════════════════════════════════════════════════

@dataclass
class Decorator(ASTNode):
    """装饰器 @名字(参数...)"""
    name: str = ""
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class ClassDecl(ASTNode):
    """类声明"""
    name: str = ""
    base: Optional[str] = None
    decorators: List[Decorator] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class MethodDecl(ASTNode):
    """类方法 / 函数定义（兼容运行时方言的 定义）"""
    name: str = ""
    params: List["Parameter"] = field(default_factory=list)
    return_type_annotation: Optional[str] = None
    decorators: List[Decorator] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    is_async: bool = False


@dataclass
class YieldStmt(ASTNode):
    """产生 表达式"""
    value: Optional[ASTNode] = None


@dataclass
class YieldFromStmt(ASTNode):
    """产生于 表达式"""
    value: Optional[ASTNode] = None


@dataclass
class ExceptClause(ASTNode):
    """捕获子句"""
    exc_type: Optional[str] = None
    alias: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class TryStmt(ASTNode):
    """尝试 ... 捕获 ... 最终 ..."""
    body: List[ASTNode] = field(default_factory=list)
    except_clauses: List[ExceptClause] = field(default_factory=list)
    finally_body: List[ASTNode] = field(default_factory=list)


@dataclass
class RaiseStmt(ASTNode):
    """抛出 表达式"""
    value: Optional[ASTNode] = None


@dataclass
class PassStmt(ASTNode):
    """通过"""
    pass


@dataclass
class WithItem(ASTNode):
    """with 项：上下文表达式 + 可选变量"""
    context_expr: Optional[ASTNode] = None
    var_name: Optional[str] = None


@dataclass
class WithStmt(ASTNode):
    """使用 ... 作为 ...:"""
    items: List[WithItem] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class AsyncWithStmt(ASTNode):
    """异步 使用 ... 作为 ...:"""
    items: List[WithItem] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class AsyncForStmt(ASTNode):
    """异步 对于 ... 在 ...:"""
    var_name: str = ""
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class AwaitExpr(ASTNode):
    """等待 表达式"""
    value: Optional[ASTNode] = None


@dataclass
class GeneratorExpr(ASTNode):
    """生成器表达式 (expr 对于 var 在 iterable 如果 condition)"""
    element: Optional[ASTNode] = None
    var_name: str = ""
    iterable: Optional[ASTNode] = None
    condition: Optional[ASTNode] = None


@dataclass
class EnumMember(ASTNode):
    """枚举成员"""
    name: str = ""
    value: Optional[ASTNode] = None


@dataclass
class EnumDecl(ASTNode):
    """枚举类声明"""
    name: str = ""
    base: Optional[str] = None
    unique: bool = False
    members: List[EnumMember] = field(default_factory=list)


@dataclass
class DataClassField(ASTNode):
    """数据类字段"""
    name: str = ""
    type_annotation: Optional[str] = None
    default: Optional[ASTNode] = None
    default_factory: Optional[ASTNode] = None


@dataclass
class DataClassDecl(ASTNode):
    """数据类声明"""
    name: str = ""
    decorators: List[Decorator] = field(default_factory=list)
    fields: List[DataClassField] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ImportStmt(ASTNode):
    """导入 / 从 ... 导入 ... 作为 ..."""
    module: Optional[str] = None
    names: List[str] = field(default_factory=list)
    alias: Optional[str] = None
    is_from: bool = False


# ═══════════════════════════════════════════════════════════════
# 新增：Bra-Ket 人格协作量子语法
# ═══════════════════════════════════════════════════════════════

@dataclass
class PersonaBasisDecl(ASTNode):
    """人格基态声明：人格基态 名字 { 角色: ..., 职责: ..., 权重: ... }"""
    name: str = ""
    fields: List["MapPair"] = field(default_factory=list)


@dataclass
class SystemDecl(ASTNode):
    """系统声明：系统 名字 { 人格空间: [...] }"""
    name: str = ""
    fields: List["MapPair"] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# CNSH v2.0-v2.3 新增：分支/审计/DNA/熔断/回滚/钩子/测试/路由
# ═══════════════════════════════════════════════════════════════

@dataclass
class SwitchStmt(ASTNode):
    """切换 ... { 情况 ...: ... 默认: ... }"""
    value: Optional[ASTNode] = None
    cases: List["CaseClause"] = field(default_factory=list)
    default_body: List[ASTNode] = field(default_factory=list)


@dataclass
class CaseClause(ASTNode):
    """情况 值: 语句..."""
    value: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class DNARegisterStmt(ASTNode):
    """DNA登记(信息映射)"""
    info: Optional[ASTNode] = None


@dataclass
class DNAVerifyStmt(ASTNode):
    """DNA验证(DNA码)"""
    dna_code: Optional[ASTNode] = None


@dataclass
class DNASignStmt(ASTNode):
    """DNA签章(信息)"""
    info: Optional[ASTNode] = None


@dataclass
class AbortStmt(ASTNode):
    """熔断(原因)"""
    reason: Optional[ASTNode] = None


@dataclass
class CreateRollbackStmt(ASTNode):
    """生成回滚点(标记)"""
    label: Optional[ASTNode] = None


@dataclass
class RollbackStmt(ASTNode):
    """回滚(快照ID)"""
    snapshot_id: Optional[ASTNode] = None


@dataclass
class VerifyRollbackStmt(ASTNode):
    """验证回滚(快照ID)"""
    snapshot_id: Optional[ASTNode] = None


@dataclass
class HookStmt(ASTNode):
    """钩子 名称(参数...) { ... }"""
    name: str = ""
    params: List["Parameter"] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    hook_type: str = ""  # "before" / "after" / ""


@dataclass
class TriColorAuditStmt(ASTNode):
    """三色审计(操作映射)"""
    operation: Optional[ASTNode] = None


@dataclass
class TestStmt(ASTNode):
    """测试 "名称" { ... }"""
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class AssertStmt(ASTNode):
    """断言 表达式 == 期望值"""
    actual: Optional[ASTNode] = None
    expected: Optional[ASTNode] = None


@dataclass
class ExpectStmt(ASTNode):
    """期望 表达式 == 值"""
    actual: Optional[ASTNode] = None
    expected: Optional[ASTNode] = None


@dataclass
class RouteToStmt(ASTNode):
    """路由到 人格名"""
    persona: str = ""


@dataclass
class QuantumEntangleStmt(ASTNode):
    """量子纠缠(父任务, 子任务)"""
    parent: Optional[ASTNode] = None
    child: Optional[ASTNode] = None


@dataclass
class CollapseStmt(ASTNode):
    """坍缩到(状态)"""
    state: Optional[ASTNode] = None


@dataclass
class ColdStartStmt(ASTNode):
    """冷启动"""
    pass


@dataclass
class HotStartStmt(ASTNode):
    """热启动"""
    pass


@dataclass
class ExitProgramStmt(ASTNode):
    """终止执行(退出码)"""
    code: Optional[ASTNode] = None


@dataclass
class ExportStmt(ASTNode):
    """导出 名称"""
    name: str = ""


@dataclass
class AuditStmt(ASTNode):
    """审计状态语句（已审计 / 审计中）"""
    status: str = ""  # "AUDITED" / "AUDITING"
