# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH编译器核心（Main Compiler）

DNA:#龍芯⚡️2026-06-03-COMPILER-CORE-FILE1-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

编排五层流水线：Lexer → Parser → Semantic → Optimizer → CodeGen
支持参数化配置和完整的编译任务管理

体现原则：
- 五层流水线编排
- 参数化配置
- 完整的错误处理
- DNA追溯和三色审计集成
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .compiler_node import ASTNode, CompileTask, TargetLang, CompileStatus
from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer, SemanticError
from .codegen import CodeGenerator, CodeGenError
from .optimizer import Optimizer, OptimizerError
from .audit import ThreeColorAudit, DNATracer


class CompileError(Exception):
    """编译错误"""
    pass


class CNSHCompiler:
    """CNSH 编译器核心"""

    def __init__(self, optimize_level: int = 1):
        """
        初始化编译器

        Args:
            optimize_level: 优化级别 (0-3)
        """
        self.optimize_level = optimize_level
        self.audit = ThreeColorAudit()
        self.dna_tracer = DNATracer()
        self.compile_history: List[Dict[str, Any]] = []

    def compile(self, task: CompileTask) -> CompileTask:
        """
        编译 CNSH 源代码

        五层流水线：
        1. 词法分析 (Lexer)
        2. 语法分析 (Parser)
        3. 语义分析 (Semantic)
        4. 优化 (Optimizer)
        5. 代码生成 (CodeGen)

        Args:
            task: 编译任务

        Returns:
            完成的编译任务
        """
        start_time = time.time()

        try:
            # 【阶段0：三色审计】
            if task.enable_audit:
                audit_result = self.audit.check(task.source_code)
                if audit_result['级别'] == '红色':
                    task.status = CompileStatus.FAILED
                    task.errors.append(f"安全审计失败: {audit_result['原因']}")
                    task.compile_time = time.time() - start_time
                    self._log_compile(task)
                    return task

            # 【阶段1：词法分析】
            tokens = self._lexical_analysis(task.source_code)

            # 【阶段2：语法分析】
            ast = self._syntax_analysis(tokens)

            # 【阶段3：语义分析】
            self._semantic_analysis(ast, task)
            if not task.status == CompileStatus.SUCCESS:
                task.compile_time = time.time() - start_time
                self._log_compile(task)
                return task

            # 【阶段4：优化】
            ast = self._optimization(ast)

            # 【阶段5：代码生成】
            output_code = self._code_generation(ast, task.target_lang)

            # 填充结果
            task.output_code = output_code
            task.status = CompileStatus.SUCCESS

            # 生成 DNA
            task.dna = self.dna_tracer.generate(
                task.source_code,
                "cnsh_compile",
                "v1.0"
            )

            # 记录编译时间
            task.compile_time = time.time() - start_time

            # 记录编译历史
            self._log_compile(task)

            return task

        except Exception as e:
            task.status = CompileStatus.FAILED
            task.errors.append(f"编译失败: {type(e).__name__}: {str(e)}")
            task.compile_time = time.time() - start_time
            self._log_compile(task)
            return task

    # ═══════════════════════════════════════════════════════════════
    # 【五层流水线阶段】
    # ═══════════════════════════════════════════════════════════════

    def _lexical_analysis(self, source: str) -> List[Any]:
        """
        阶段1：词法分析

        Args:
            source: CNSH 源代码

        Returns:
            Token 列表
        """
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            return tokens
        except Exception as e:
            raise CompileError(f"词法分析失败: {str(e)}")

    def _syntax_analysis(self, tokens: List[Any]) -> ASTNode:
        """
        阶段2：语法分析

        Args:
            tokens: Token 列表

        Returns:
            AST 根节点
        """
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            return ast
        except Exception as e:
            raise CompileError(f"语法分析失败: {str(e)}")

    def _semantic_analysis(self, ast: ASTNode, task: CompileTask):
        """
        阶段3：语义分析

        Args:
            ast: 抽象语法树
            task: 编译任务（用于存储错误）
        """
        try:
            analyzer = SemanticAnalyzer()
            success, errors, warnings = analyzer.analyze(ast)

            if errors:
                task.errors.extend(errors)
            if warnings:
                task.warnings.extend(warnings)

            if not success:
                task.status = CompileStatus.FAILED
            elif warnings:
                task.status = CompileStatus.WARNING

        except Exception as e:
            raise CompileError(f"语义分析失败: {str(e)}")

    def _optimization(self, ast: ASTNode) -> ASTNode:
        """
        阶段4：优化

        Args:
            ast: 抽象语法树

        Returns:
            优化后的 AST
        """
        try:
            optimizer = Optimizer(self.optimize_level)
            optimized_ast = optimizer.optimize(ast)
            return optimized_ast
        except Exception as e:
            raise CompileError(f"优化失败: {str(e)}")

    def _code_generation(self, ast: ASTNode, target_lang: TargetLang) -> str:
        """
        阶段5：代码生成

        Args:
            ast: 抽象语法树
            target_lang: 目标语言

        Returns:
            生成的目标语言代码
        """
        try:
            codegen = CodeGenerator(target_lang)
            output = codegen.generate(ast)
            return output
        except Exception as e:
            raise CompileError(f"代码生成失败: {str(e)}")

    # ═══════════════════════════════════════════════════════════════
    # 【日志和历史】
    # ═══════════════════════════════════════════════════════════════

    def _log_compile(self, task: CompileTask):
        """记录编译任务到历史"""
        record = {
            'task_id': task.task_id,
            'source_code': task.source_code[:100],  # 前100个字符
            'target_lang': task.target_lang.value,
            'status': task.status.value,
            'compile_time': task.compile_time,
            'error_count': len(task.errors),
            'warning_count': len(task.warnings),
            'dna': task.dna,
            'timestamp': datetime.now().isoformat()
        }
        self.compile_history.append(record)

    def get_compile_history(self) -> List[Dict[str, Any]]:
        """获取编译历史"""
        return self.compile_history

    # ═══════════════════════════════════════════════════════════════
    # 【自检函数】
    # ═══════════════════════════════════════════════════════════════

    def selftest(self) -> Tuple[bool, List[str]]:
        """
        自检函数

        Returns:
            (成功, 错误列表)
        """
        errors = []

        # 测试代码
        test_code = "整数 x = 10; 返回 x + 1;"

        try:
            # 测试完整编译流程
            task = CompileTask(
                task_id="SELFTEST-001",
                source_code=test_code,
                target_lang=TargetLang.PYTHON,
                optimize_level=1,
                enable_audit=True
            )

            result = self.compile(task)

            if result.status == CompileStatus.FAILED:
                errors.append(f"自检编译失败: {result.errors}")
            elif not result.output_code:
                errors.append("自检编译没有生成输出代码")
            elif not result.dna:
                errors.append("自检编译没有生成 DNA")

        except Exception as e:
            errors.append(f"自检异常: {str(e)}")

        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════
# 【全局单例】
# ═══════════════════════════════════════════════════════════════

_GLOBAL_COMPILER = None


def get_cnsh_compiler(optimize_level: int = 1) -> CNSHCompiler:
    """获取全局编译器实例（单例）"""
    global _GLOBAL_COMPILER
    if _GLOBAL_COMPILER is None:
        _GLOBAL_COMPILER = CNSHCompiler(optimize_level)
    return _GLOBAL_COMPILER


def reset_cnsh_compiler():
    """重置全局编译器实例"""
    global _GLOBAL_COMPILER
    _GLOBAL_COMPILER = None


# ═══════════════════════════════════════════════════════════════
# 【DNA追溯信息】
# ═══════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-06-03-COMPILER-CORE-v1.0"
__responsibility__ = "UID9622·不免责"
