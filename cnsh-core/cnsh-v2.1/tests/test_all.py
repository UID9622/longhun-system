# -*- coding: utf-8 -*-
"""
CNSH v2.1 测试套件
DNA: #龍芯⚡️2026-06-29-CNSH-TESTS-v2.1
"""
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cnsh_v21 import run_source, compile_to_python, compile_source, 计算数字根
from cnsh_v21.lexer import Lexer
from cnsh_v21.parser import Parser
from cnsh_v21.interpreter import Interpreter
from cnsh_v21.compiler_py import PythonCompiler
from cnsh_v21.compiler_js import JavaScriptCompiler
from cnsh_v21.compiler_c import CCompiler
from cnsh_v21.errors import CNSHError
from cnsh_v21.typechecker import TypeChecker, TypeCheckError


class TestLexer(unittest.TestCase):
    def test_hello_tokens(self):
        source = '输出("你好")'
        tokens = Lexer(source).tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(types, ["IDENTIFIER", "LPAREN", "STRING", "RPAREN", "EOF"])

    def test_operators(self):
        source = "a == b 且 c != d"
        tokens = Lexer(source).tokenize()
        values = [t.value for t in tokens if t.type not in ("EOF",)]
        self.assertEqual(values, ["a", "==", "b", "且", "c", "!=", "d"])

    def test_weight(self):
        source = "模块 示例 ⚖️100 { }"
        tokens = Lexer(source).tokenize()
        values = [t.value for t in tokens if t.type not in ("EOF",)]
        self.assertEqual(values, ["模块", "示例", "⚖️", "100", "{", "}"])


class TestParser(unittest.TestCase):
    def test_parse_function(self):
        source = """
        函数 相加(a, b) {
            返回 a + b
        }
        """
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].name, "相加")


class TestInterpreter(unittest.TestCase):
    def _capture(self, source: str):
        old = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        try:
            run_source(source)
        finally:
            sys.stdout = old
        return buf.getvalue()

    def test_arithmetic(self):
        source = '输出(1 + 2 * 3)'
        out = self._capture(source)
        self.assertIn("7", out)

    def test_if_else(self):
        source = """
        如果 (1 < 2) {
            输出("yes")
        } 否则 {
            输出("no")
        }
        """
        out = self._capture(source)
        self.assertIn("yes", out)

    def test_while(self):
        source = """
        变量 i = 0
        当 (i < 3) {
            输出(i)
            i = i + 1
        }
        """
        out = self._capture(source)
        self.assertIn("0", out)
        self.assertIn("1", out)
        self.assertIn("2", out)

    def test_for(self):
        source = """
        对于 x 在 [1, 2, 3] {
            输出(x)
        }
        """
        out = self._capture(source)
        self.assertIn("1", out)
        self.assertIn("2", out)
        self.assertIn("3", out)

    def test_function_call(self):
        source = """
        函数 平方(x) {
            返回 x * x
        }
        输出(平方(5))
        """
        out = self._capture(source)
        self.assertIn("25", out)

    def test_stdlib_math(self):
        source = '输出(龍.数学.数字根("9622"))'
        out = self._capture(source)
        self.assertIn("1", out)  # 9+6+2+2=19 -> 1+9=10 -> 1


class TestCompiler(unittest.TestCase):
    def _capture(self, source: str):
        python_code = compile_to_python(source)
        old = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        g = {"__builtins__": __builtins__}
        try:
            exec(compile(python_code, "<cnsh>", "exec"), g)
        finally:
            sys.stdout = old
        return buf.getvalue(), python_code

    def test_compile_hello(self):
        source = """
        函数 问好(名字) {
            输出("你好，" + 名字)
        }
        问好("龍魂")
        """
        out, code = self._capture(source)
        self.assertIn("你好，龍魂", out)

    def test_compile_module(self):
        source = """
        模块 工具 {
            函数 翻倍(x) {
                返回 x * 2
            }
        }
        输出(工具.翻倍(7))
        """
        out, code = self._capture(source)
        self.assertIn("14", out)


class TestJSCompiler(unittest.TestCase):
    def _capture(self, source: str):
        import io
        import sys
        import subprocess
        import tempfile
        from pathlib import Path
        js_code = compile_source(source, target="javascript")
        tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
        tmp.write(js_code)
        tmp.close()
        try:
            result = subprocess.run(["node", tmp.name], capture_output=True, text=True, check=True)
            return result.stdout, js_code
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    def test_js_hello(self):
        source = """
        函数 问好(名字) { 输出("你好，" + 名字) }
        问好("龍魂")
        """
        out, _ = self._capture(source)
        self.assertIn("你好，龍魂", out)

    def test_js_fib(self):
        source = """
        函数 斐波那契(n) {
            如果 (n <= 1) { 返回 n }
            返回 斐波那契(n - 1) + 斐波那契(n - 2)
        }
        输出(斐波那契(10))
        """
        out, _ = self._capture(source)
        self.assertIn("55", out)


class TestCCompiler(unittest.TestCase):
    def _capture(self, source: str):
        import io
        import subprocess
        import tempfile
        from pathlib import Path
        c_code = compile_source(source, target="c")
        tmp = tempfile.NamedTemporaryFile("w", suffix=".c", delete=False, encoding="utf-8")
        tmp.write(c_code)
        tmp.close()
        exe = tmp.name.replace(".c", "")
        try:
            subprocess.run(["gcc", tmp.name, "-o", exe, "-lm"], check=True)
            result = subprocess.run([exe], capture_output=True, text=True, check=True)
            return result.stdout, c_code
        finally:
            Path(tmp.name).unlink(missing_ok=True)
            Path(exe).unlink(missing_ok=True)

    def test_c_hello(self):
        source = """
        函数 问好(名字) {
            输出("你好，" + 名字)
        }
        问好("龍魂")
        """
        out, _ = self._capture(source)
        self.assertIn("你好，龍魂", out)

    def test_c_fib(self):
        source = """
        函数 斐波那契(n) {
            如果 (n <= 1) { 返回 n }
            返回 斐波那契(n - 1) + 斐波那契(n - 2)
        }
        输出(斐波那契(10))
        """
        out, _ = self._capture(source)
        self.assertIn("55", out)


class TestRustCompiler(unittest.TestCase):
    def test_rust_code_generation(self):
        source = """
        函数 斐波那契(n) {
            如果 (n <= 1) { 返回 n }
            返回 斐波那契(n - 1) + 斐波那契(n - 2)
        }
        输出(斐波那契(10))
        """
        rust_code = compile_source(source, target="rust")
        self.assertIn("enum CnshValue", rust_code)
        self.assertIn("fn 斐波那契", rust_code)
        self.assertIn("fn main()", rust_code)


class TestCrypto(unittest.TestCase):
    def test_sm4_roundtrip(self):
        from cnsh_v21.crypto import sm4_encrypt, sm4_decrypt
        plain = "CNSH 龍魂主权不可侵犯 UID9622"
        key = "我的密钥"
        cipher = sm4_encrypt(plain, key)
        self.assertNotEqual(cipher, plain)
        self.assertEqual(sm4_decrypt(cipher, key), plain)

    def test_sm4_different_keys_fail(self):
        from cnsh_v21.crypto import sm4_encrypt, sm4_decrypt, CNSHCryptoError
        plain = "secret"
        cipher = sm4_encrypt(plain, "key1")
        with self.assertRaises((CNSHCryptoError, UnicodeDecodeError)):
            sm4_decrypt(cipher, "key2")

    def test_gpg_sign_verify(self):
        from cnsh_v21.crypto import gpg_sign, gpg_verify
        data = "龍魂审计日志：登录事件"
        sig = gpg_sign(data)
        self.assertTrue(gpg_verify(data, sig))

    def test_gpg_verify_tampered_data(self):
        from cnsh_v21.crypto import gpg_sign, gpg_verify
        data = "原始数据"
        sig = gpg_sign(data)
        self.assertFalse(gpg_verify("篡改数据", sig))


class TestOptimizer(unittest.TestCase):
    def _capture(self, source: str, optimize_level: int = 3):
        old = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        try:
            run_source(source, optimize_level=optimize_level)
        finally:
            sys.stdout = old
        return buf.getvalue()

    def test_constant_folding(self):
        source = '输出(1 + 2 * 3)'
        out = self._capture(source)
        self.assertIn("7", out)

    def test_dead_code_elimination(self):
        source = """
        如果 (假) {
            输出("dead")
        } 否则 {
            输出("alive")
        }
        """
        out = self._capture(source)
        self.assertNotIn("dead", out)
        self.assertIn("alive", out)

    def test_expression_simplification(self):
        source = """
        变量 x = 5
        输出(x * 1 + 0)
        """
        out = self._capture(source)
        self.assertIn("5", out)


class TestFFI(unittest.TestCase):
    def _capture(self, source: str):
        old = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        try:
            run_source(source)
        finally:
            sys.stdout = old
        return buf.getvalue()

    def test_python_math(self):
        source = """
        导入 Python.math
        输出(math.sqrt(1764))
        """
        out = self._capture(source)
        self.assertIn("42.0", out)

    def test_python_datetime(self):
        source = """
        导入 Python.datetime
        输出(datetime.datetime(2026, 1, 1).year)
        """
        out = self._capture(source)
        self.assertIn("2026", out)


class TestUtils(unittest.TestCase):
    def test_digital_root(self):
        self.assertEqual(计算数字根("9622"), 1)
        self.assertEqual(计算数字根("12345"), 6)


class TestTypeChecker(unittest.TestCase):
    def _check(self, source: str):
        tokens = Lexer(source).tokenize()
        tree = Parser(tokens).parse()
        return TypeChecker().check(tree)

    def test_valid_types(self):
        source = """
        变量 计数: 整数 = 10
        变量 价格: 小数 = 19.99
        变量 名字: 文本 = "龍魂"
        变量 激活: 布尔 = 真
        函数 相加(a: 整数, b: 整数) -> 整数 {
            返回 a + b
        }
        输出(相加(计数, 2))
        """
        ok, errors, _ = self._check(source)
        self.assertTrue(ok, errors)

    def test_type_mismatch_in_var_decl(self):
        source = "变量 x: 整数 = \"文本\""
        ok, errors, _ = self._check(source)
        self.assertFalse(ok)
        self.assertTrue(any("整数" in e and "文本" in e for e in errors))

    def test_assignment_type_error(self):
        source = """
        变量 x: 整数 = 1
        x = "错误"
        """
        ok, errors, _ = self._check(source)
        self.assertFalse(ok)
        self.assertTrue(any("错误" in e or "文本" in e for e in errors))

    def test_undefined_identifier(self):
        source = "输出(未定义变量)"
        ok, errors, _ = self._check(source)
        self.assertFalse(ok)
        self.assertTrue(any("未定义" in e for e in errors))

    def test_arithmetic_type_error(self):
        source = "输出(\"文本\" - 1)"
        ok, errors, _ = self._check(source)
        self.assertFalse(ok)
        self.assertTrue(any("运算符" in e for e in errors))

    def test_strict_mode_raises(self):
        source = "变量 x: 整数 = \"文本\""
        with self.assertRaises(TypeCheckError):
            run_source(source, strict_types=True, type_check=True)

    def test_no_type_check_runs(self):
        source = "变量 x: 整数 = \"文本\"\n输出(x)"
        # 不开启类型检查时仍能解释执行
        try:
            run_source(source, type_check=False)
        except CNSHError:
            self.fail("禁用类型检查时应允许执行")


class TestPythonCompilerAdvanced(unittest.TestCase):
    def _capture(self, source: str):
        python_code = compile_to_python(source)
        old = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        g = {"__builtins__": __builtins__}
        try:
            exec(compile(python_code, "<cnsh>", "exec"), g)
        finally:
            sys.stdout = old
        return buf.getvalue(), python_code

    def test_class_inheritance_and_decorators(self):
        source = """
        类 动物 {
            定义 初始化(自己, 名字) {
                自己.名字 = 名字
            }
            定义 叫声(自己) {
                返回 "声音:" + 自己.名字
            }
        }
        类 狗(动物) {
            定义 初始化(自己, 名字, 品种) {
                超类().初始化(名字)
                自己.品种 = 品种
            }
            定义 叫声(自己) {
                返回 自己.名字 + "(" + 自己.品种 + ")"
            }
        }
        类 方 {
            定义 初始化(自己, 边) {
                自己.边 = 边
            }
            @属性
            定义 面积(自己) {
                返回 自己.边 * 自己.边
            }
        }
        d = 狗("阿黄", "土狗")
        输出(d.叫声())
        s = 方(4)
        输出("面积=" + 字符串(s.面积))
        """
        out, _ = self._capture(source)
        self.assertIn("阿黄(土狗)", out)
        self.assertIn("面积=16", out)

    def test_generators(self):
        source = """
        定义 计数(最大) {
            n = 0
            当 n < 最大 {
                产生 n
                n = n + 1
            }
        }
        输出(列表(计数(3)))
        平方 = (x * x 对于 x 在 范围(5) 如果 x > 1)
        输出(列表(平方))
        """
        out, _ = self._capture(source)
        self.assertIn("[0, 1, 2]", out)
        self.assertIn("[4, 9, 16]", out)

    def test_try_except(self):
        source = """
        定义 出错() {
            抛出 例外("bad")
        }
        尝试 {
            出错()
        } 捕获 例外 作为 e {
            输出("捕获:" + 字符串(e))
        }
        """
        out, _ = self._capture(source)
        self.assertIn("捕获:bad", out)

    def test_enum_and_dataclass(self):
        source = """
        枚举唯一
        类 状态码(枚举类) {
            成功 = 200
            失败 = 500
        }
        输出(状态码.成功.name)
        输出(字符串(状态码.成功.value))

        数据类
        类 用户 {
            名字: 字符串
            年龄: 整数 = 0
        }
        u = 用户("老大", 年龄=30)
        输出(u.名字 + "," + 字符串(u.年龄))
        """
        out, _ = self._capture(source)
        self.assertIn("成功", out)
        self.assertIn("200", out)
        self.assertIn("老大,30", out)

    def test_async_await_with(self):
        source = """
        异步 定义 主函数() {
            使用 打开("/tmp/cnsh_async_test.txt", "w") 作为 f {
                f.write("hello")
            }
            信号量 = asyncio.Semaphore(1)
            异步 使用 信号量 {
                等待 asyncio.sleep(0.01)
                输出("async with ok")
            }
        }
        asyncio.run(主函数())
        """
        out, _ = self._capture(source)
        self.assertIn("async with ok", out)

    def test_braket_persona_collaboration(self):
        source = """
        人格基态 诸葛亮 {
            角色: "推演态",
            职责: "战略推演",
            权重: 0.15
        }
        人格基态 管仲 {
            角色: "财务态",
            职责: "财务核算",
            权重: 0.10
        }
        系统 龍魂BraKet {
            人格空间: [诸葛亮, 管仲]
        }
        任务 = "帮我做财务分析"
        测量结果 = 龍魂BraKet.测量(任务)
        演化态 = 测量结果.酉演化(时间=1.0)
        概率分布 = 演化态.协作概率()
        审计 = 演化态.三色审计()
        输出("场景:" + 测量结果.场景)
        输出("主执行人格:" + 概率分布[0].名字)
        输出("审计:" + 审计.状态)
        """
        out, code = self._capture(source)
        self.assertIn("场景:", out)
        self.assertIn("主执行人格:", out)
        self.assertIn("审计:", out)


if __name__ == "__main__":
    unittest.main()
