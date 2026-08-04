#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友好错误报告器单元测试
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-ERROR-TESTS-v1.0
"""
from longhun_chinese_editor.compiler.errors import FriendlyErrorReporter


def test_runtime_error_report():
    reporter = FriendlyErrorReporter("打印(未定义)", "print(未定义)", "<test>")
    try:
        exec("print(未定义)")
    except Exception as e:
        msg = reporter.report_runtime(e)
        assert "【CNSH" in msg
        assert "未定义" in msg or "NameError" in msg


def test_error_report_has_source_context():
    source = "整数 x = 1\n整数 y = 1 / 0\n打印(y)"
    python_code = (
        "x = 1\n"
        "y = 1 / 0\n"
        "print(y)"
    )
    reporter = FriendlyErrorReporter(source, python_code, "<test>")
    try:
        exec(compile(python_code, "<test>", "exec"))
    except Exception as e:
        msg = reporter.report_runtime(e)
        assert "第" in msg
        assert "源码上下文" in msg
