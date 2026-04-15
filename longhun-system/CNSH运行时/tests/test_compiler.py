#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 编译器自动化测试套件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA追溯码：#龍芯⚡️2026-03-22-CNSH-TESTS-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者：诸葛鑫（UID9622）
协议：Apache License 2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path

# 将 compiler 目录加入路径
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "compiler"))

from cnsh_compiler import Lexer, Parser, CCodeGenerator, ThreeColorAudit, AuditLevel

# ─────────────────────────────────────────────────────
# 测试工具
# ─────────────────────────────────────────────────────

_ok = 0
_fail = 0

def _test(name: str, passed: bool, detail: str = ""):
    global _ok, _fail
    if passed:
        _ok += 1
        print(f"  🟢 通过  {name}")
    else:
        _fail += 1
        print(f"  🔴 失败  {name}" + (f"\n         {detail}" if detail else ""))

def _section(title: str):
    print(f"\n── {title} {'─' * (40 - len(title))}")

# ─────────────────────────────────────────────────────
# Lexer 测试
# ─────────────────────────────────────────────────────

def test_lexer():
    _section("词法分析器（Lexer）")

    # 测试：整数字面量
    lexer = Lexer("整数 x = 42")
    tokens = lexer.tokenize()
    values = [t.value for t in tokens if t.value is not None]
    _test("识别整数字面量 42", "42" in values)

    # 测试：中文字符串「」
    lexer = Lexer('打印「你好」')
    tokens = lexer.tokenize()
    values = [t.value for t in tokens if t.value is not None]
    _test("识别「」字符串定界符", "你好" in values)

    # 测试：中文方括号【】
    from cnsh_compiler import TokenType
    lexer = Lexer("如果【x > 0】")
    tokens = lexer.tokenize()
    types = [t.type for t in tokens]
    _test("识别【】为 LBRACKET/RBRACKET",
          TokenType.LBRACKET in types and TokenType.RBRACKET in types)

    # 测试：注释跳过
    lexer = Lexer("# 这是注释\n整数 y = 1")
    tokens = lexer.tokenize()
    values = [t.value for t in tokens if t.value is not None]
    _test("跳过 # 注释", "这是注释" not in str(values) and "y" in values)

    # 测试：关键字识别
    lexer = Lexer("函数 主函数() 返回类型 整数")
    tokens = lexer.tokenize()
    from cnsh_compiler import TokenType
    kw_values = [t.value for t in tokens if t.type == TokenType.KEYWORD]
    _test("识别关键字 函数/返回类型/整数",
          "函数" in kw_values and "返回类型" in kw_values and "整数" in kw_values)

    # 测试：运算符
    lexer = Lexer("a >= b && c != d")
    tokens = lexer.tokenize()
    from cnsh_compiler import TokenType
    types = [t.type for t in tokens]
    _test("识别 >= 和 && 和 != 运算符",
          TokenType.GTE in types and TokenType.LOGICAL_AND in types and TokenType.NEQ in types)

# ─────────────────────────────────────────────────────
# Parser 测试
# ─────────────────────────────────────────────────────

def test_parser():
    _section("语法分析器（Parser）")

    def parse(code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    from cnsh_compiler import (FunctionDeclaration, VariableDeclaration,
                                IfStatement, LoopStatement, ReturnStatement,
                                PrintStatement)

    # 测试：函数定义
    ast = parse("函数 主函数() 返回类型 整数 { 返回 0 }")
    _test("解析函数定义",
          len(ast.statements) == 1 and isinstance(ast.statements[0], FunctionDeclaration))

    # 测试：变量声明
    ast = parse("整数 年龄 = 25")
    _test("解析变量声明",
          len(ast.statements) == 1 and isinstance(ast.statements[0], VariableDeclaration))

    # 测试：if-else
    ast = parse("如果【x > 0】{ 返回 1 } 否则 { 返回 0 }")
    _test("解析 如果/否则",
          len(ast.statements) == 1 and isinstance(ast.statements[0], IfStatement) and
          ast.statements[0].else_body is not None)

    # 测试：循环
    ast = parse("循环【3】{ 打印「测试」 }")
    _test("解析 循环【N】",
          len(ast.statements) == 1 and isinstance(ast.statements[0], LoopStatement))

    # 测试：打印字面量
    ast = parse('打印「你好」')
    _test("解析 打印「」",
          len(ast.statements) == 1 and isinstance(ast.statements[0], PrintStatement))

    # 测试：嵌套 if
    code = """
    如果【a > 0】{
        如果【b > 0】{
            返回 1
        } 否则 {
            返回 2
        }
    } 否则 {
        返回 3
    }
    """
    ast = parse(code)
    _test("解析嵌套 如果/否则", isinstance(ast.statements[0], IfStatement))

# ─────────────────────────────────────────────────────
# 三色审计测试
# ─────────────────────────────────────────────────────

def test_audit():
    _section("三色审计系统")

    audit = ThreeColorAudit()

    # 绿色：正常代码
    result = audit.check("整数 x = 1\n打印「你好」")
    _test("正常代码 → 🟢 绿色", result.level == AuditLevel.GREEN)

    # 红色：危险内容
    result = audit.check("整数 x = 诈骗")
    _test("危险关键词 → 🔴 红色", result.level == AuditLevel.RED)

    # 黄色：可能的身份证号
    result = audit.check("文本 id = 「110101199001011234」")
    _test("身份证号码 → 🟡 黄色", result.level == AuditLevel.YELLOW)

# ─────────────────────────────────────────────────────
# 代码生成测试（端到端）
# ─────────────────────────────────────────────────────

def test_codegen():
    _section("C 代码生成")

    def gen_c(code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        gen = CCodeGenerator(ast)
        return gen.generate()

    # 测试：整数变量生成 int
    c = gen_c("整数 年龄 = 25")
    _test("整数 → int", "int 年龄 = 25;" in c)

    # 测试：小数变量生成 double
    c = gen_c("小数 价格 = 9.9")
    _test("小数 → double", "double 价格 = 9.9;" in c)

    # 测试：if 生成 if (...)
    c = gen_c("如果【x > 0】{ 返回 1 }")
    _test("如果【】→ if (...)", "if (" in c)

    # 测试：else 生成 else
    c = gen_c("如果【x > 0】{ 返回 1 } 否则 { 返回 0 }")
    _test("否则 → else", "} else {" in c)

    # 测试：循环生成 for
    c = gen_c("循环【5】{ 返回 0 }")
    _test("循环【N】→ for (...)", "for (" in c and "__i < 5" in c)

    # 测试：函数定义生成
    c = gen_c("函数 主函数() 返回类型 整数 { 返回 0 }")
    _test("函数定义 → C 函数", "int 主函数()" in c)

# ─────────────────────────────────────────────────────
# 端到端运行测试（需要 gcc）
# ─────────────────────────────────────────────────────

HELLO_CNSH = """\
# 端到端测试程序
函数 主函数() 返回类型 整数 {
    打印「CNSH测试通过」
    返回 0
}
"""

CALC_CNSH = """\
# 计算测试
函数 主函数() 返回类型 整数 {
    整数 a = 10
    整数 b = 3
    整数 结果 = a + b
    返回 结果
}
"""

def test_e2e():
    _section("端到端运行测试（需要 gcc）")

    import shutil
    if not shutil.which("gcc"):
        print("  ⏭  跳过（系统中未找到 gcc）")
        return

    cli = _ROOT / "cli" / "cnsh"
    if not cli.exists():
        print("  ⏭  跳过（未找到 cnsh CLI）")
        return

    with tempfile.TemporaryDirectory() as tmp:
        # Hello World 测试
        src = Path(tmp) / "test_hello.cnsh"
        src.write_text(HELLO_CNSH, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(cli), "run", str(src)],
            capture_output=True, text=True, timeout=30
        )
        _test("Hello World 编译并运行",
              result.returncode == 0 and "CNSH测试通过" in result.stdout,
              detail=result.stderr[:200] if result.returncode != 0 else "")

        # 计算测试（通过返回值验证）
        src2 = Path(tmp) / "test_calc.cnsh"
        src2.write_text(CALC_CNSH, encoding="utf-8")
        result2 = subprocess.run(
            [sys.executable, str(cli), "compile", str(src2)],
            capture_output=True, text=True, timeout=30
        )
        _test("算术运算编译通过",
              result2.returncode == 0,
              detail=result2.stderr[:200] if result2.returncode != 0 else "")

# ─────────────────────────────────────────────────────
# 主运行入口
# ─────────────────────────────────────────────────────

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  CNSH 编译器测试套件 v1.0")
    print("  DNA：#龍芯⚡️2026-03-22-CNSH-TESTS-v1.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    test_lexer()
    test_parser()
    test_audit()
    test_codegen()
    test_e2e()

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total = _ok + _fail
    print(f"  测试结果：通过 {_ok}/{total}  失败 {_fail}/{total}")
    if _fail == 0:
        print("  🟢 全部通过！")
    else:
        print(f"  🔴 有 {_fail} 个测试失败，请检查。")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    sys.exit(0 if _fail == 0 else 1)


if __name__ == "__main__":
    main()
