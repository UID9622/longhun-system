#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 解释器 v1.2
DNA: #龍芯⚡️2026-08-31-CNSH-INTERPRETER-v1.2-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 执行 CNSH 代码，支持任意符号变量 + 中文运算符 + 作用域
v1.2 新增(对照评估): 未定义变量抛异常·环境变量调优·AST缓存·stats监控
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# 双模式导入：包导入（from cnsh.interpreter import ...）与
# 直接运行（python3 08_BIN/cnsh/interpreter.py）均可用
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from cnsh.lexer import CNSHLexer, CNSHToken
    from cnsh.var_env import CNSHVarEnv
    from cnsh.dna_verify import verify_dna_header
else:
    from .lexer import CNSHLexer, CNSHToken
    from .var_env import CNSHVarEnv
    from .dna_verify import verify_dna_header


def _env_bool(raw: Optional[str], default: bool) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in ('1', 'true', 'yes', 'on')


def _env_int(raw: Optional[str], default: int) -> int:
    if raw is None:
        return default
    try:
        return int(raw.strip())
    except ValueError:
        return default


def load_config_from_yaml(path: str) -> Dict:
    """读取 yaml 配置（对齐 20_CONFIG/cnsh_config.yaml 结构，兼容 DeepSeek 参考版）

    支持的映射:
      cnsh.variables.allow_any_symbols    → allow_symbols
      cnsh.variables.allow_chinese_operators → allow_chinese_operators
      cnsh.variables.scope_stack          → scope_stack
      cnsh.dna.strict_mode                → strict_dna
      cnsh.comments.line/block            → 注释符号（供词法层读取）
      cnsh.debug                          → debug
      cnsh.performance.ast_cache_size     → cache_size
      cnsh.performance.max_vars           → max_vars
    """
    try:
        import yaml  # 按需导入（依赖最小化）
    except ImportError:
        raise ImportError("加载 yaml 配置需先安装 PyYAML: pip3 install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f) or {}
    c = raw.get('cnsh', raw) if isinstance(raw, dict) else {}
    if not isinstance(c, dict):
        return {}
    cfg = {}
    vars_cfg = c.get('variables') or {}
    if 'allow_any_symbols' in vars_cfg:
        cfg['allow_symbols'] = bool(vars_cfg['allow_any_symbols'])
    if 'allow_chinese_operators' in vars_cfg:
        cfg['allow_chinese_operators'] = bool(vars_cfg['allow_chinese_operators'])
    if 'scope_stack' in vars_cfg:
        cfg['scope_stack'] = bool(vars_cfg['scope_stack'])
    dna_cfg = c.get('dna') or {}
    if 'strict_mode' in dna_cfg:
        cfg['strict_dna'] = bool(dna_cfg['strict_mode'])
    if 'debug' in c:
        cfg['debug'] = bool(c['debug'])
    perf = c.get('performance') or {}
    if 'ast_cache_size' in perf:
        cfg['cache_size'] = int(perf['ast_cache_size'])
    if 'max_vars' in perf and perf['max_vars'] is not None:
        cfg['max_vars'] = int(perf['max_vars'])
    return cfg


def load_config_from_env(config: Optional[Dict] = None) -> Dict:
    """读取环境变量覆盖配置（兼容 CNSSH_ENV_* 与 CNSH_ENV_* 双前缀）"""
    base = dict(config or {})
    allow = os.environ.get('CNSSH_ENV_ALLOW_SYMBOLS') or os.environ.get('CNSH_ENV_ALLOW_SYMBOLS')
    strict = os.environ.get('CNSSH_ENV_STRICT_DNA') or os.environ.get('CNSH_STRICT_DNA')
    cache = os.environ.get('CNSSH_ENV_CACHE_SIZE') or os.environ.get('CNSH_ENV_CACHE_SIZE')
    maxv = os.environ.get('CNSSH_ENV_MAX_VARS') or os.environ.get('CNSH_ENV_MAX_VARS')
    dbg = os.environ.get('CNSSH_ENV_DEBUG') or os.environ.get('CNSH_ENV_DEBUG')
    if allow is not None:
        base['allow_symbols'] = _env_bool(allow, True)
    if strict is not None:
        base['strict_dna'] = _env_bool(strict, True)
    if cache is not None:
        base['cache_size'] = _env_int(cache, 64)
    if maxv is not None:
        base['max_vars'] = _env_int(maxv, None)
    if dbg is not None:
        base['debug'] = _env_bool(dbg, False)
    return base


class CNSHInterpreter:
    """CNSH 主解释器"""

    def __init__(self, config: Dict = None):
        self.config = load_config_from_env(config)
        self.debug = self.config.get('debug', False)
        self.strict_dna = self.config.get('strict_dna', True)
        self.allow_symbols = self.config.get('allow_symbols', True)
        cache_size = self.config.get('cache_size', 64)
        max_vars = self.config.get('max_vars')
        self.env = CNSHVarEnv(max_vars=max_vars)
        self._cache_size = max(0, int(cache_size))
        self._token_cache: Dict[str, List[CNSHToken]] = {}
        # stats 监控指标（文档§四-4）
        self.stats = {
            'exec_count': 0,        # 执行次数
            'parse_count': 0,       # 真实解析次数
            'cache_hits': 0,        # 缓存命中次数
            'errors': 0,            # 解析失败次数
            'total_time_ms': 0.0,   # 总执行耗时(ms)
            'peak_vars': 0,         # 峰值变量数
        }

    def _tokenize(self, source: str) -> List[CNSHToken]:
        """词法分析（带 AST 缓存：同一源码命中缓存跳过重复解析）"""
        if self._cache_size > 0:
            cached = self._token_cache.get(source)
            if cached is not None:
                self.stats['cache_hits'] += 1
                return cached
        lexer = CNSHLexer(source)
        try:
            tokens = lexer.tokenize()
        except Exception:
            self.stats['errors'] += 1
            raise
        self.stats['parse_count'] += 1
        if self._cache_size > 0:
            if len(self._token_cache) >= self._cache_size:
                # 简单 FIFO 淘汰（dict 保序）
                self._token_cache.pop(next(iter(self._token_cache)))
            self._token_cache[source] = tokens
        return tokens

    def execute(self, source: str, filename: str = '<string>') -> Dict[str, Any]:
        """执行 CNSH 代码字符串"""
        t0 = time.perf_counter()
        try:
            if self.strict_dna and not verify_dna_header(source):
                raise PermissionError(
                    f"[龍魂DNA校验失败] 文件 {filename} 缺少有效的 #龍芯⚡️ 签名，拒绝执行。"
                )
            tokens = self._tokenize(source)
            if self.debug:
                for t in tokens:
                    if t.type != 'NEWLINE':
                        print(f"  [DEBUG] {t}")
            result = self._run(tokens)
            self.stats['exec_count'] += 1
            return result
        finally:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self.stats['total_time_ms'] += elapsed_ms
            self.stats['peak_vars'] = max(self.stats['peak_vars'], self.env.var_count)

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
    import json
    parser = argparse.ArgumentParser(description='🐉 CNSH 解释器 v1.3')
    parser.add_argument('file', nargs='?', help='要执行的 .cnsh 文件')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--code', type=str, help='直接执行代码字符串')
    parser.add_argument('--no-strict-dna', action='store_true', help='关闭DNA校验（开发模式）')
    parser.add_argument('--stats', action='store_true', help='执行后输出监控统计')
    parser.add_argument('--cache-size', type=int, help='AST缓存大小(环境变量 CNSSH_ENV_CACHE_SIZE 可覆盖)')
    parser.add_argument('--config', type=str, help='yaml配置文件(20_CONFIG/cnsh_config.yaml)')
    import sys as _sys
    # 兼容 `cnsh run file.cnsh` 语法（DeepSeek 参考版）：仅删除首个非flag参数位置的
    # run 子命令词；跳过 --code/--config/--cache-size 等带值 flag，防误删其值。
    argv = _sys.argv[1:]
    _value_flags = ('--code', '--config', '--cache-size')
    _skip_next = False
    for _idx, _a in enumerate(argv):
        if _skip_next:
            _skip_next = False
            continue
        if _a in _value_flags:
            _skip_next = True
            continue
        if not _a.startswith('-'):
            if _a == 'run':
                argv = argv[:_idx] + argv[_idx + 1:]
            break
    args = parser.parse_args(argv)
    config = {'debug': args.debug, 'strict_dna': not args.no_strict_dna}
    if args.config:
        # yaml 配置为基底，CLI 显式参数覆盖
        config = {**load_config_from_yaml(args.config), **config}
    if args.cache_size is not None:
        config['cache_size'] = args.cache_size
    interp = CNSHInterpreter(config)
    try:
        if args.code:
            interp.execute(args.code)
        elif args.file:
            interp.execute_file(args.file)
        else:
            print('🐉 CNSH 交互模式 v1.3 | 输入 Ctrl+D 退出')
            while True:
                try:
                    line = input('>> ')
                    if line.strip():
                        interp.execute(line)
                except EOFError:
                    break
        if args.stats:
            print(json.dumps(interp.stats, ensure_ascii=False, indent=2))
    except (NameError, PermissionError, MemoryError, ValueError) as e:
        print(f'❌ {e}')
        sys.exit(1)
