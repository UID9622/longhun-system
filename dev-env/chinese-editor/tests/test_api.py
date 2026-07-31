# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python API 层单元测试
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-API-TESTS-v1.0
"""
import pytest

import longhun_chinese_editor as ce


def test_compile_source():
    py = ce.compile_source('函数 加(整数 a, 整数 b) { 返回 a + b }')
    assert "def 加(a, b):" in py
    assert "return (a + b)" in py


def test_check_source_ok():
    ok, msg = ce.check_source('函数 主函数(){ 返回 0 }')
    assert ok
    assert "通过" in msg


def test_check_source_fail():
    ok, msg = ce.check_source('函数 主函数(){ 整数 }')
    assert not ok


def test_run_source():
    ns = ce.run_source('函数 主函数(){ 返回 42 }')
    assert ns["主函数"]() == 42


def test_run_source_with_namespace():
    ns = {"x": 10}
    ce.run_source('函数 主函数(){ 返回 x + 1 }', namespace=ns)
    assert ns["主函数"]() == 11


def test_legacy_translate():
    py = ce.legacy_translate('函数 主函数(){ 打印 "hello" }')
    assert "def 主函数" in py
    assert "print" in py
