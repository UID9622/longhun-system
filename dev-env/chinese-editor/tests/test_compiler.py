#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 编译器单元测试
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-COMPILER-TESTS-v1.0
"""
import pytest

from longhun_chinese_editor.compiler.pipeline import compile_cnsh_safe
from longhun_chinese_editor.compiler.lexer import Lexer, LexerError
from longhun_chinese_editor.compiler.parser import Parser, ParseError


def _run(code: str) -> str:
    ok, result, _ = compile_cnsh_safe(code)
    assert ok, result
    return result


def test_hello_function():
    code = '''
函数 主函数() 返回类型 整数 {
  打印 "hello"
  返回 0
}
'''
    py = _run(code)
    assert "def 主函数():" in py
    assert "print(\"hello\")" in py or "print('hello')" in py
    assert "return 0" in py


def test_var_decl_and_assignment():
    code = '''
函数 主函数() {
  整数 年龄 = 25
  年龄 = 年龄 + 1
  打印 年龄
}
'''
    py = _run(code)
    assert "年龄 = 25" in py
    assert "年龄 = (年龄 + 1)" in py


def test_if_else():
    code = '''
函数 主函数() {
  整数 x = 5
  如果 (x > 3) {
    打印 "大"
  } 否则 {
    打印 "小"
  }
}
'''
    py = _run(code)
    assert "if (x > 3):" in py
    assert "else:" in py


def test_loop_and_while():
    code = '''
函数 主函数() {
  循环 (3) {
    打印 "x"
  }
  整数 i = 0
  当 (i < 2) {
    打印 i
    i = i + 1
  }
}
'''
    py = _run(code)
    assert "for __cnshexpr in range(int(3)):" in py
    assert "while (i < 2):" in py


def test_for_range():
    code = '''
函数 主函数() {
  对于 整数 i 在 范围 (3) {
    打印 i
  }
}
'''
    py = _run(code)
    assert "for i in range(3):" in py


def test_function_with_params():
    code = '''
函数 加 (整数 a, 整数 b) -> 整数 {
  返回 a + b
}
'''
    py = _run(code)
    assert "def 加(a, b):" in py
    assert "return (a + b)" in py


def test_compile_and_execute():
    code = '''
函数 主函数() 返回类型 整数 {
  整数 a = 2
  整数 b = 3
  打印 a + b
  返回 a + b
}
'''
    py = _run(code)
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == 5


def test_invalid_syntax_raises():
    code = '函数 主函数() { 整数 }'
    ok, result, err_type = compile_cnsh_safe(code)
    assert not ok
    assert err_type in ("lexer", "parser", "codegen")


def test_lexer_rejects_unclosed_string():
    with pytest.raises(LexerError):
        Lexer('文本 s = "unclosed').tokenize()


def test_parser_rejects_missing_brace():
    tokens = Lexer('函数 主函数() { 返回 0').tokenize()
    with pytest.raises(ParseError):
        Parser(tokens).parse()


def test_array_dict_and_index():
    code = '''
函数 主函数() {
  列表 arr = [1, 2, 3]
  arr[1] = 10
  字典 d = {"a": 1, "b": 2}
  返回 d["a"] + arr[1]
}
'''
    py = _run(code)
    assert "arr = [1, 2, 3]" in py
    assert "d = {" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == 11


def test_elif_chain():
    code = '''
函数 主函数() {
  整数 x = 3
  如果 (x == 1) {
    返回 "a"
  } 否则如果 (x == 2) {
    返回 "b"
  } 否则 {
    返回 "c"
  }
}
'''
    py = _run(code)
    assert "elif (x == 2):" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == "c"


def test_try_catch():
    code = '''
函数 主函数() {
  尝试 {
    整数 x = 1 / 0
  } 捕获 {
    返回 "caught"
  }
  返回 "ok"
}
'''
    py = _run(code)
    assert "try:" in py
    assert "except Exception:" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == "caught"


def test_import():
    code = '导入 "math"'
    py = _run(code)
    assert "import math" in py


def test_member_access():
    code = '''
函数 主函数() {
  文本 s = "hello"
  返回 长度(s)
}
'''
    py = _run(code)
    assert "len(s)" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == 5


def test_method_mapping():
    code = '''
函数 主函数() {
  列表 arr = [1, 2, 3]
  arr.添加(4)
  字典 d = {"a": 1}
  返回 d.获取("a") + 长度(arr)
}
'''
    py = _run(code)
    assert "arr.append(4)" in py
    assert "d.get" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == 5


def test_more_builtins():
    code = '''
函数 主函数() {
  返回 最大值([1, 5, 3])
}
'''
    py = _run(code)
    assert "max([1, 5, 3])" in py
    ns = {}
    exec(py, ns)
    assert ns["主函数"]() == 5
