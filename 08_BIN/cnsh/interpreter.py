#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 解释器 v1.1
DNA: #龍芯⚡️2026-08-31-CNSH-INTERPRETER-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 执行 CNSH 代码，支持任意符号变量 + 中文运算符 + 作用域
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

from .lexer import CNSHLexer, CNSHToken
from .var_env import CNSHVarEnv
from .dna_verify import verify_dna_header


class CNSHInterpreter:
    """CNSH 主解释器"""

    def __init__(self, config: Dict = None):
        self.env = CNSHVarEnv()
        self.config = config or {}
        self.debug = self.config.get('debug', False)
        self.strict_dna = self.config.get('strict_dna', True)

    def execute(self, source: str, filename: str = '<string>') -> Dict[str, Any]:
        """执行 CNSH 代码字符串"""
        if self.strict_dna and not verify_dna_header(source):
            raise PermissionError(
                f"[龍魂DNA校验失败] 文件 {filename} 缺少有效的 #龍芯⚡️ 签名，拒绝执行。"
            )
        lexer = CNSHLexer(source)
        tokens = lexer.tokenize()
        if self.debug:
            for t in tokens:
                if t.type != 'NEWLINE':
                    print(f"  [DEBUG] {t}")
        return self._run(tokens)

    def execute_file(self, filepath: str) -> Dict[str, Any]:
        """执行 CNSH 文件"""
        path = Path(filepath)
        if not path.exists():
            return {'error': f'文件不存在: {filepath}'}
        source = path.read_text(encoding='utf-8')
        return self.execute(source, filename=str(path))

    def _run(self, tokens: List[CNSHToken]) -> Dict[str, Any]:
        """顺序执行 token 列表"""
        i = 0
        n = len(tokens)

        def skip_newlines():
            nonlocal i
            while i < n and tokens[i].type == 'NEWLINE':
                i += 1

        while i < n:
            skip_newlines()
            if i >= n:
                break
            tok = tokens[i]

            # ── 赋值：VAR = expr ──────────────────────────
            if tok.type == 'VAR' and i + 1 < n and tokens[i + 1].type == 'ASSIGN':
                var_name = tok.value
                i += 2
                value, i = self._eval_expr(tokens, i)
                self.env.set_var(var_name, value)
                if self.debug:
                    print(f"  [DEBUG] 赋值 {var_name!r} = {value!r}")
                continue

            # ── 函数调用：IDENTIFIER(args) ────────────────
            if tok.type == 'IDENTIFIER' and i + 1 < n and tokens[i + 1].type == 'LPAREN':
                _, i = self._call_func(tokens, i)
                continue

            i += 1

        return {'env': self.env.get_env()}

    def _eval_expr(self, tokens: List[CNSHToken], start: int):
        """表达式求值（左结合，支持二元运算）"""
        n = len(tokens)
        i = start
        left, i = self._eval_primary(tokens, i)

        # 二元运算符（ASCII + 中文）
        while i < n:
            tok = tokens[i]
            if tok.type in (
                'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
                'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE',
                'AND', 'OR',
            ):
                op_tok = tok
                i += 1
                right, i = self._eval_primary(tokens, i)
                left = self.env.eval_binary(left, op_tok.type, op_tok.value, right)
            else:
                break

        return left, i

    def _eval_primary(self, tokens: List[CNSHToken], i: int):
        """基础值：变量、字面量、函数调用"""
        if i >= len(tokens):
            return None, i
        tok = tokens[i]

        if tok.type == 'NUMBER':
            val = float(tok.value) if '.' in tok.value else int(tok.value)
            return val, i + 1

        if tok.type == 'STRING':
            return tok.value, i + 1

        if tok.type == 'VAR':
            return self.env.get_var(tok.value), i + 1

        if tok.type == 'IDENTIFIER':
            # 函数调用
            if i + 1 < len(tokens) and tokens[i + 1].type == 'LPAREN':
                val, i = self._call_func(tokens, i)
                return val, i
            return None, i + 1

        if tok.type == 'LPAREN':
            val, i = self._eval_expr(tokens, i + 1)
            if i < len(tokens) and tokens[i].type == 'RPAREN':
                i += 1
            return val, i

        return None, i + 1

    def _call_func(self, tokens: List[CNSHToken], i: int):
        """函数调用 IDENTIFIER(arg1, arg2, ...)"""
        func_name = tokens[i].value
        i += 2  # 跳过 IDENTIFIER 和 LPAREN
        args = []
        while i < len(tokens) and tokens[i].type != 'RPAREN':
            if tokens[i].type == 'COMMA':
                i += 1
                continue
            val, i = self._eval_expr(tokens, i)
            args.append(val)
        if i < len(tokens) and tokens[i].type == 'RPAREN':
            i += 1
        result = self.env.call_function(func_name, *args)
        return result, i


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='🐉 CNSH 解释器 v1.1')
    parser.add_argument('file', nargs='?', help='要执行的 .cnsh 文件')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--code', type=str, help='直接执行代码字符串')
    parser.add_argument('--no-strict-dna', action='store_true', help='关闭DNA校验（开发模式）')
    args = parser.parse_args()
    config = {'debug': args.debug, 'strict_dna': not args.no_strict_dna}
    interp = CNSHInterpreter(config)
    if args.code:
        interp.execute(args.code)
    elif args.file:
        interp.execute_file(args.file)
    else:
        print('🐉 CNSH 交互模式 v1.1 | 输入 Ctrl+D 退出')
        while True:
            try:
                line = input('>> ')
                if line.strip():
                    interp.execute(line)
            except EOFError:
                break
