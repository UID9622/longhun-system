#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂CNSH编译器 (P1-3)

DNA: #龍芯⚡️2026-06-03-CNSH-COMPILER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

核心模块·计算逻辑赋能层·可参数化编译

导出接口：
- CompileTask - 编译任务数据模型
- Token - 词法单元
- ASTNode - 抽象语法树节点
- TargetLang - 目标语言枚举
- CompileStatus - 编译状态（三色）
- Lexer - 词法分析器
- Parser - 语法分析器
- ThreeColorAudit - 三色审计系统
- DNATracer - DNA追溯系统
"""

from .compiler_node import (
    CompileTask,
    Token,
    ASTNode,
    TargetLang,
    CompileStatus,
)

from .lexer import Lexer
from .parser import Parser
from .audit import ThreeColorAudit, DNATracer
from .semantic import SemanticAnalyzer, SemanticError
from .codegen import CodeGenerator, CodeGenError

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"

__all__ = [
    'CompileTask',
    'Token',
    'ASTNode',
    'TargetLang',
    'CompileStatus',
    'Lexer',
    'Parser',
    'ThreeColorAudit',
    'DNATracer',
    'SemanticAnalyzer',
    'SemanticError',
    'CodeGenerator',
    'CodeGenError',
]
