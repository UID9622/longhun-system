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
        return None

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

    def __init__(self):
        self._global_scope = Scope()
        self._scope_stack: List[Scope] = [self._global_scope]
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
        self.current_scope.set(name, value)

    def get_var(self, name: str) -> Any:
        return self.current_scope.get(name)

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
