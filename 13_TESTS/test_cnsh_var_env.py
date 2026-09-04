#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 变量环境测试 v1.3
DNA: #龍芯⚡️2026-08-31-CNSH-TEST-v1.3-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / '08_BIN'))
from cnsh.lexer import CNSHLexer
from cnsh.var_env import CNSHVarEnv
from cnsh.interpreter import CNSHInterpreter, load_config_from_env
from cnsh.dna_verify import verify_dna_header, verify_dna_file

DNA_PREFIX = """#!/usr/bin/env cnsh
// DNA: #龍芯⚡️2026-08-31-TEST-INLINE-v1.0-UID9622
"""


class TestLexer(unittest.TestCase):

    def test_symbol_vars(self):
        """变量名含任意符号"""
        code = DNA_PREFIX + '$#var = 100\n$@data = "hello"\n${#special!} = 3.14'
        tokens = CNSHLexer(code).tokenize()
        var_names = [t.value for t in tokens if t.type == 'VAR']
        self.assertIn('#var', var_names)
        self.assertIn('@data', var_names)
        self.assertIn('#special!', var_names)

    def test_comment_ignored(self):
        """注释不产生token"""
        code = '// 这是注释\n/* 块注释 */$x = 1'
        tokens = [t for t in CNSHLexer(code).tokenize() if t.type not in ('NEWLINE',)]
        types = [t.type for t in tokens]
        self.assertNotIn('COMMENT', types)
        self.assertIn('VAR', types)

    def test_chinese_op_priority(self):
        """中文运算符优先长串匹配（大于等于 不拆成 大于+等于）"""
        code = '$a 大于等于 $b'
        tokens = [t for t in CNSHLexer(code).tokenize() if t.type != 'NEWLINE']
        op_tokens = [t for t in tokens if t.value == '大于等于']
        self.assertEqual(len(op_tokens), 1)
        self.assertEqual(op_tokens[0].type, 'GTE')


class TestVarEnv(unittest.TestCase):

    def test_any_symbol_var(self):
        env = CNSHVarEnv()
        env.set_var('#龍芯⚡️9622', 'locked')
        self.assertEqual(env.get_var('#龍芯⚡️9622'), 'locked')

    def test_cn_operators(self):
        env = CNSHVarEnv()
        self.assertEqual(env.eval_binary(10, 'PLUS', '加', 5), 15)
        self.assertEqual(env.eval_binary(10, 'MUL', '乘', 3), 30)
        self.assertTrue(env.eval_binary(10, 'GT', '大于', 5))
        self.assertTrue(env.eval_binary(10, 'GTE', '大于等于', 10))

    def test_scope_stack(self):
        env = CNSHVarEnv()
        env.set_var('x', 1)
        env.push_scope()
        env.set_var('x', 99)
        self.assertEqual(env.get_var('x'), 99)
        env.pop_scope()
        self.assertEqual(env.get_var('x'), 1)


class TestInterpreter(unittest.TestCase):

    def _make_interp(self):
        return CNSHInterpreter({'debug': False, 'strict_dna': False})

    def test_assignment(self):
        interp = self._make_interp()
        interp.execute('$#var = 100\n$@data = "hello"')
        self.assertEqual(interp.env.get_var('#var'), 100)
        self.assertEqual(interp.env.get_var('@data'), 'hello')

    def test_long_form(self):
        interp = self._make_interp()
        interp.execute('${#special with spaces} = "ok"')
        self.assertEqual(interp.env.get_var('#special with spaces'), 'ok')

    def test_cn_arithmetic(self):
        interp = self._make_interp()
        interp.execute('$a = 10\n$b = 5\n$c = $a 加 $b')
        self.assertEqual(interp.env.get_var('c'), 15)

    def test_builtin_print(self):
        import io
        from contextlib import redirect_stdout
        interp = self._make_interp()
        interp.execute('$#var = 100')
        buf = io.StringIO()
        with redirect_stdout(buf):
            interp.execute('输出($#var)')
        self.assertIn('100', buf.getvalue())


class TestUndefinedVar(unittest.TestCase):
    """验证清单：未定义变量引用抛出异常"""

    def test_undefined_var_raises(self):
        interp = CNSHInterpreter({'strict_dna': False})
        with self.assertRaises(NameError):
            interp.execute('$y = $#not_defined')
        with self.assertRaises(NameError):
            interp.execute('$a = 1\n$b = $a 加 $missing')

    def test_defined_var_ok(self):
        interp = CNSHInterpreter({'strict_dna': False})
        interp.execute('$#defined = 42')
        self.assertEqual(interp.env.get_var('#defined'), 42)


class TestEnvConfig(unittest.TestCase):
    """环境变量调优参数（文档§四-3）"""

    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in (
            'CNSSH_ENV_ALLOW_SYMBOLS', 'CNSSH_ENV_STRICT_DNA',
            'CNSSH_ENV_CACHE_SIZE', 'CNSSH_ENV_MAX_VARS',
        )}

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_env_bool(self):
        os.environ['CNSSH_ENV_STRICT_DNA'] = 'false'
        cfg = load_config_from_env({})
        self.assertFalse(cfg['strict_dna'])

    def test_env_cache_size(self):
        os.environ['CNSSH_ENV_CACHE_SIZE'] = '8'
        cfg = load_config_from_env({})
        self.assertEqual(cfg['cache_size'], 8)

    def test_env_max_vars(self):
        os.environ['CNSSH_ENV_MAX_VARS'] = '3'
        interp = CNSHInterpreter({'strict_dna': False})
        interp.execute('$a = 1\n$b = 2\n$c = 3')
        with self.assertRaises(MemoryError):
            interp.execute('$d = 4')

    def test_legacy_prefix(self):
        """兼容 CNSH_ENV_* 旧前缀"""
        os.environ['CNSH_ENV_ALLOW_SYMBOLS'] = 'true'
        cfg = load_config_from_env({})
        self.assertTrue(cfg['allow_symbols'])


class TestCache(unittest.TestCase):
    """AST缓存（文档§三-3 优化方向）"""

    def test_cache_hit(self):
        interp = CNSHInterpreter({'strict_dna': False, 'cache_size': 8})
        code = '$#x = 1\n$#y = 2'
        interp.execute(code)
        interp.execute(code)  # 第二次应命中缓存
        self.assertEqual(interp.stats['parse_count'], 1)
        self.assertEqual(interp.stats['cache_hits'], 1)

    def test_cache_disabled(self):
        interp = CNSHInterpreter({'strict_dna': False, 'cache_size': 0})
        code = '$#x = 1'
        interp.execute(code)
        interp.execute(code)
        self.assertEqual(interp.stats['cache_hits'], 0)


class TestDeepSeekCompat(unittest.TestCase):
    """DeepSeek 参考版 API 兼容（深度集成验收）"""

    def test_cnssh_lexer_alias(self):
        """三S类名 CNSSHLexer 与 CNSHLexer 等价"""
        from cnsh import CNSSHLexer
        self.assertIs(CNSSHLexer, CNSHLexer)
        code = '''
        $#var = 100
        $@data = "hello"
        ${#special!} = 3.14
        '''
        lexer = CNSSHLexer(code)
        var_names = [t.value for t in lexer.tokenize() if t.type == 'VAR']
        self.assertIn('#var', var_names)
        self.assertIn('@data', var_names)
        self.assertIn('#special!', var_names)

    def test_eval_expr_compat(self):
        """参考版 eval_expr API（tuple 列表形态）"""
        env = CNSHVarEnv()
        env.set_var('#a', 10)
        env.set_var('#b', 5)
        val, _ = env.eval_expr([('VAR', '#a'), ('PLUS', '加'), ('VAR', '#b')])
        self.assertEqual(val, 15)

    def test_op_map_compat(self):
        """参考版 OP_MAP 属性（中文+ASCII 合并）"""
        self.assertIn('加', CNSHVarEnv.OP_MAP)
        self.assertIn('+', CNSHVarEnv.OP_MAP)

    def test_interp_eval_expr_compat(self):
        """参考版解释器用 eval_expr 求值（文档§3.2 调用形态）"""
        interp = CNSHInterpreter({'strict_dna': False})
        interp.execute('$#a = 10\n$#b = 5')
        lexer = CNSHLexer('$#a 加 $#b')
        tokens = [(t.type, t.value) for t in lexer.tokenize() if t.type != 'NEWLINE']
        val, _ = interp.env.eval_expr(tokens)
        self.assertEqual(val, 15)


class TestDNAVerify(unittest.TestCase):

    def test_valid_dna(self):
        source = '// #龍芯⚡️2026-08-31-TEST-v1.0-UID9622\n$x = 1'
        self.assertTrue(verify_dna_header(source))

    def test_invalid_dna_simplified(self):
        """简体龙不合法"""
        source = '// #龙芯⚡️2026-08-31-TEST-v1.0-UID9622\n$x = 1'
        self.assertFalse(verify_dna_header(source))

    def test_invalid_dna_no_uid(self):
        """缺少UID9622后缀不合法"""
        source = '// #龍芯⚡️2026-08-31-TEST-v1.0\n$x = 1'
        self.assertFalse(verify_dna_header(source))


if __name__ == '__main__':
    unittest.main(verbosity=2)
