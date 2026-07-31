# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH编译器·编译任务数据模型

DNA:#龍芯⚡️2026-06-03-COMPILER-NODE-FILE1-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

来源: UID9622·诸葛鑫·龍心北辰
责任: UID9622·不免责
状态: 🟢 MAIN·可公开

编译任务、词法单元、抽象语法树的数据定义。
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import json


class TargetLang(str, Enum):
    """编译目标语言"""
    C = "c"
    CPP = "cpp"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    RUST = "rust"
    OBJC = "objc"
    SWIFT = "swift"


class CompileStatus(str, Enum):
    """编译状态（三色判定）"""
    SUCCESS = "🟢"        # 编译成功
    WARNING = "🟡"        # 有警告
    FAILED = "🔴"         # 编译失败


@dataclass
class CompileTask:
    """
    编译任务（完整的CNSH编译请求和结果）

    体现"赋能而非替代"的原则：
    - 不是完整IDE，而是可参数化的编译任务对象
    - 通过参数化配置（optimize_level, mapping_overrides等）暴露计算逻辑
    - DNA追溯每一次编译的完整过程
    """
    # 基础信息
    task_id: str                    # COMPILE-20260603-001
    source_code: str                # CNSH中文源代码
    target_lang: TargetLang         # 编译目标语言

    # 编译配置（参数化）
    optimize_level: int = 1         # 优化级别 0=无优化, 1=常量折叠, 2=死代码消除, 3=公共子表达式
    enable_audit: bool = True       # 启用三色审计（dr_gate判定）
    mapping_overrides: Dict[str, str] = field(default_factory=dict)  # 自定义映射覆盖

    # 编译结果
    status: CompileStatus = CompileStatus.SUCCESS
    output_code: str = ""           # 生成的目标语言代码
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # 追溯信息（可计算的DNA链）
    dna: str = ""                   # 本次编译任务的唯一DNA (SHA-256哈希)
    compile_time: float = 0.0       # 编译耗时(秒)

    # 审计信息（可计算的三色判定）
    dr_value: int = 0               # 代码复杂度的数字根
    audit_color: str = "🟢"         # 三色审计结果: 🟢/🟡/🔴

    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # 扩展字段
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（支持JSON序列化）"""
        data = asdict(self)
        data['target_lang'] = self.target_lang.value
        data['status'] = self.status.value
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CompileTask":
        """从字典加载"""
        data = data.copy()
        data['target_lang'] = TargetLang(data['target_lang'])
        data['status'] = CompileStatus(data['status'])
        return CompileTask(**data)

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(json_str: str) -> "CompileTask":
        """从JSON字符串加载"""
        data = json.loads(json_str)
        return CompileTask.from_dict(data)


@dataclass
class Token:
    """
    词法单元（Lexer输出）

    可计算属性体现"计算优先"原则：
    - dr: 数字根（用于质量判定）
    - hash: SHA-256哈希（用于去重/缓存）
    """
    type: str           # KEYWORD, IDENTIFIER, NUMBER, STRING, OPERATOR, PUNCTUATION
    value: str          # 原始token值
    line: int           # 源代码行号
    column: int         # 源代码列号

    # 可计算属性
    dr: int = 0         # 数字根（用于过滤）
    hash: str = ""      # SHA-256（用于去重）


@dataclass
class ASTNode:
    """
    抽象语法树节点（Parser输出）

    可计算属性：
    - dna: 节点的DNA（可追溯）
    - depth: 树深度（用于复杂度计算）
    - complexity: 子树复杂度（可融合计算）
    """
    node_type: str      # PROGRAM, FUNCTION, STATEMENT, EXPRESSION, BLOCK, etc.
    value: Any          # 节点的实际值
    children: List["ASTNode"] = field(default_factory=list)

    # 可计算属性
    dna: str = ""       # 节点的DNA追溯码
    depth: int = 0      # 节点深度（根=0）

    # 扩展字段
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_complexity(self) -> int:
        """
        计算子树复杂度（递归）

        这体现"可融合计算"原则：
        - 一次树遍历就能计算总复杂度
        - 多个度量可以合并在一次遍历中
        """
        # 节点本身 + 所有子树的复杂度
        return 1 + sum(child.calculate_complexity() for child in self.children)

    def visit(self, visitor_func):
        """
        DFS遍历AST节点（支持自定义访问者）

        这支持"赋能而非替代"：
        - 用户可以自己写visitor进行AST操作
        """
        visitor_func(self)
        for child in self.children:
            child.visit(visitor_func)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（支持序列化）"""
        return {
            "node_type": self.node_type,
            "value": str(self.value),
            "dna": self.dna,
            "depth": self.depth,
            "complexity": self.calculate_complexity(),
            "children_count": len(self.children),
            "children": [child.to_dict() for child in self.children]
        }


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-06-03-COMPILER-NODE-v1.0"
__responsibility__ = "UID9622·不免责"
