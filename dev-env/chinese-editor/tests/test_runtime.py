#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂中文编辑开发环境 - 运行时单元测试
DNA: #龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-TESTS-v1.0
"""
import pytest

from longhun_chinese_editor.runtime import (
    fix_fstrings,
    fix_print_calls,
    translate_cnsh_to_python,
)


def test_translate_hello_function():
    source = """
函数 主函数() {
    打印("你好")
}
"""
    code = translate_cnsh_to_python(source)
    assert "def 主函数():" in code
    assert 'print("你好")' in code


def test_translate_if_else():
    source = """
整数 年龄 = 20
如果 (年龄 >= 18) {
    打印("成年")
} 否则 {
    打印("未成年")
}
"""
    code = translate_cnsh_to_python(source)
    assert "年龄 = 20" in code
    assert "if" in code and "年龄 >= 18" in code
    assert 'print("成年")' in code
    assert "else:" in code


def test_translate_loop_n():
    source = """
循环 (3) {
    打印("迭代")
}
"""
    code = translate_cnsh_to_python(source)
    assert "for __cnshexpr in range(3):" in code


def test_translate_while():
    source = """
整数 计数 = 0
当 (计数 < 3) {
    打印(计数)
    计数 = 计数 + 1
}
"""
    code = translate_cnsh_to_python(source)
    assert "while" in code and "计数 < 3" in code


def test_keyword_boundary_no_false_positive():
    """主函数 中的 函数 不应被替换；否则如果 不应被拆断"""
    source = """
函数 主函数() {
    如果 (真) {
        打印("ok")
    } 否则如果 (假) {
        打印("no")
    }
}
"""
    code = translate_cnsh_to_python(source)
    assert "def 主函数():" in code
    assert "if" in code and "True" in code
    assert "elif" in code and "False" in code


def test_fix_print_and_fstring():
    code = 'print "hello"'
    code = fix_print_calls(code)
    assert code == 'print("hello")'

    code2 = 'print("value={x}")'
    code2 = fix_fstrings(code2)
    assert code2 == 'print(f"value={x}")'


def test_translate_for_range():
    source = """
对于 索引 在 范围(5) {
    打印(索引)
}
"""
    code = translate_cnsh_to_python(source)
    assert "for 索引 in range(5):" in code


def test_dna_placeholder_not_corrupted():
    source = '打印("DNA:#龍芯⚡️2026-test")'
    code = translate_cnsh_to_python(source)
    assert "#龍芯⚡️2026-test" in code
