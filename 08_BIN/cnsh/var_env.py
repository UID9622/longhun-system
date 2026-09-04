#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 变量环境 v1.1
DNA: #龍芯⚡️2026-08-31-CNSH-VAR-ENV-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 支持任意符号变量名 + 中文运算符 + 作用域堆栈
"""

import operator
from typing import Dict, Any, Optional, List


# 未定义变量哨兵：区分「变量不存在」与「变量值为 None」
_MISSING = object()


class Scope:
    """作用域（支持嵌套）"""
    def __init__(self, parent: Optional['Scope'] = None):
        self._vars: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        if name in self._vars:
            return self._vars[name]
        if self.parent:
            return self.parent.get(name)
        return _MISSING

    def set(self, name: str, value: Any):
        self._vars[name] = value

    def has(self, name: str) -> bool:
        if name in self._vars:
            return True
        return self.parent.has(name) if self.parent else False

    def flat_dict(self) -> Dict[str, Any]:
        result = {}
        if self.parent:
            result.update(self.parent.flat_dict())
        result.update(self._vars)
        return result


class CNSHVarEnv:
    """CNSH 变量环境（含作用域堆栈）"""

    # 中文 → Python operator 映射
    CN_OP_MAP = {
        '加':       operator.add,
        '减':       operator.sub,
        '乘':       operator.mul,
        '除':       operator.truediv,
        '等于':     operator.eq,
        '不等于':   operator.ne,
        '大于':     operator.gt,
        '小于':     operator.lt,
        '大于等于': operator.ge,
        '小于等于': operator.le,
        '且':       lambda a, b: bool(a) and bool(b),
        '或':       lambda a, b: bool(a) or bool(b),
    }

    # ASCII operator token → Python operator 映射
    ASCII_OP_MAP = {
        'PLUS':  operator.add,
        'MINUS': operator.sub,
        'MUL':   operator.mul,
        'DIV':   operator.truediv,
        'MOD':   operator.mod,
        'EQ':    operator.eq,
        'NEQ':   operator.ne,
        'GT':    operator.gt,
        'LT':    operator.lt,
        'GTE':   operator.ge,
        'LTE':   operator.le,
    }

    # ── DeepSeek 参考版兼容别名 ─────────────────────────
    # 参考文档 CNSHVarEnv.OP_MAP 直接暴露运算符映射，合并中文+ASCII
    OP_MAP = {**CN_OP_MAP, '+': operator.add, '-': operator.sub,
              '*': operator.mul, '/': operator.truediv, '%': operator.mod}

    def __init__(self, max_vars: Optional[int] = None):
        self._global_scope = Scope()
        self._scope_stack: List[Scope] = [self._global_scope]
        self._max_vars = max_vars  # 环境变量调优：变量数量上限
        self._functions: Dict[str, Any] = {
            '输出': self._builtin_print,
            '输入': self._builtin_input,
            '类型': lambda x: type(x).__name__,
            '长度': len,
            '整数': int,
            '浮点': float,
            '字符': str,
            '列表': list,
        }

    @property
    def var_count(self) -> int:
        """当前全局变量数量（监控指标）"""
        return len(self._global_scope._vars)

    @property
    def current_scope(self) -> Scope:
        return self._scope_stack[-1]

    def push_scope(self):
        """进入新作用域"""
        self._scope_stack.append(Scope(parent=self.current_scope))

    def pop_scope(self):
        """退出作用域"""
        if len(self._scope_stack) > 1:
            self._scope_stack.pop()

    def set_var(self, name: str, value: Any):
        """设置变量（支持任意字符名，含 # @ % ! 等）"""
        if self._max_vars is not None:
            if name not in self._global_scope._vars and self.var_count >= self._max_vars:
                raise MemoryError(
                    f"[CNSH] 变量数超限: 当前 {self.var_count} 个 ≥ 上限 {self._max_vars} 个。"
                    "请调大 CNSSH_ENV_MAX_VARS 后重试。"
                )
        self.current_scope.set(name, value)

    def get_var(self, name: str) -> Any:
        """读取变量；未定义时抛 NameError（按验证清单要求）"""
        value = self.current_scope.get(name)
        if value is _MISSING:
            raise NameError(f"未定义变量: {name}")
        return value

    def has_var(self, name: str) -> bool:
        return self.current_scope.has(name)

    def call_function(self, name: str, *args) -> Any:
        if name in self._functions:
            return self._functions[name](*args)
        raise NameError(f"未定义函数: {name}")

    def eval_binary(self, left: Any, op_type: str, op_val: str, right: Any) -> Any:
        """二元运算（中文 + ASCII 运算符）"""
        if op_val in self.CN_OP_MAP:
            return self.CN_OP_MAP[op_val](left, right)
        if op_type in self.ASCII_OP_MAP:
            return self.ASCII_OP_MAP[op_type](left, right)
        raise ValueError(f"不支持的运算符: {op_val}")

    def eval_expr(self, tokens, start: int = 0) -> tuple:
        """简易表达式求值（DeepSeek 参考版 API 兼容层）

        接收 [(type, value), ...] 二元组列表（参考版 interpreter 的调用形态），
        从左到右求值。完整表达式引擎在主解释器 CNSHInterpreter._eval_expr。
        """
        if not tokens:
            return None, start
        result = None
        i = start
        op = None
        while i < len(tokens):
            token = tokens[i]
            ttype, tval = token[0], token[1]
            if ttype == 'NUMBER':
                val = float(tval) if '.' in tval else int(tval)
            elif ttype == 'STRING':
                val = tval
            elif ttype == 'VAR':
                val = self.get_var(tval)
            elif ttype == 'IDENTIFIER':
                # 函数调用
                if i + 1 < len(tokens) and tokens[i + 1][0] == 'LPAREN':
                    func_name = tval
                    args = []
                    i += 2
                    while i < len(tokens) and tokens[i][0] != 'RPAREN':
                        if tokens[i][0] in ('NUMBER', 'STRING', 'VAR'):
                            arg_val, i = self.eval_expr(tokens, i)
                            args.append(arg_val)
                        else:
                            i += 1
                    val = self.call_function(func_name, *args)
                    result = val
                    i += 1
                    continue
                else:
                    val = None
            elif ttype in ('PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE'):
                op = ttype
                i += 1
                continue
            else:
                i += 1
                continue

            if op and result is not None:
                if op in self.ASCII_OP_MAP:
                    result = self.ASCII_OP_MAP[op](result, val)
                elif tval in self.CN_OP_MAP:
                    result = self.CN_OP_MAP[tval](result, val)
                op = None
            else:
                result = val
            i += 1
        return result, i

    def get_env(self) -> Dict[str, Any]:
        return self.current_scope.flat_dict()

    def clear(self):
        self._global_scope = Scope()
        self._scope_stack = [self._global_scope]

    # ── 内置函数 ──────────────────────────────────────────
    @staticmethod
    def _builtin_print(*args):
        print(*args)

    @staticmethod
    def _builtin_input(prompt: str = '请输入: '):
        return input(prompt)
