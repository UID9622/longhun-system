#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
B4 · CNSH翻译脑区 → P04 鲁班
================================
将解析後的代码转换为CNSH格式。
对接已有 cnsh_translator_engine_v2.0.py。

DNA: #龍芯⚡️丙午·丙申·丙辰·未时·需-BRAIN-B4-CNSH-TRANSLATOR-v1.0
"""

import re
import os
import sys
from typing import Dict, Any


# ── 类型映射表 ────────────────────────────────────────────────────────────────

TYPE_MAP: Dict[str, str] = {
    # Python → CNSH
    "int": "整数",
    "float": "小数",
    "str": "文本",
    "bool": "真假",
    "list": "列表",
    "dict": "字典",
    "tuple": "元组",
    "set": "集合",
    "None": "空值",
    "bytes": "字节",
    # C/C++ → CNSH
    "int": "整数",
    "double": "小数",
    "char*": "文本",
    "bool": "真假",
    "void": "空值",
    # JavaScript → CNSH
    "number": "数字",
    "string": "文本",
    "boolean": "真假",
    "undefined": "未定义",
    "null": "空",
}

KEYWORD_MAP: Dict[str, str] = {
    # Python
    "def": "函数",
    "class": "类型",
    "if": "如果",
    "elif": "否则如果",
    "else": "否则",
    "for": "遍历",
    "while": "当",
    "return": "返回",
    "import": "导入",
    "from": "从",
    "try": "尝试",
    "except": "捕获",
    "finally": "最终",
    "raise": "抛出",
    "pass": "跳过",
    "break": "跳出",
    "continue": "继续",
    "yield": "产出",
    "lambda": "匿名函数",
    "with": "使用",
    "as": "作为",
    "print": "打印",
    "len": "长度",
    "range": "范围",
    "True": "真",
    "False": "假",
}


def translate_python_to_cnsh(code: str) -> str:
    """Python → CNSH 基基翻译"""
    lines = code.split('\n')
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append(line)
            continue

        # 获取縮进
        indent = line[:len(line) - len(stripped)]

        # 翻译关键词
        translated = stripped
        for en, cn in KEYWORD_MAP.items():
            translated = re.sub(r'\b' + en + r'\b', cn, translated)

        # 翻译函数定义: 函数 名称(参数):
        translated = re.sub(
            r'^函数\s+(\w+)\s*\((.*?)\)',
            r'函数 \1(参数 \2)',
            translated
        )

        # 翻译变量賦值中的类型註解
        for en, cn in TYPE_MAP.items():
            translated = translated.replace(f": {en}", f"类型 {cn}")

        result.append(indent + translated)

    return '\n'.join(result)


def translate_cpp_to_cnsh(code: str) -> str:
    """C/C++ → CNSH 基基翻译"""
    cpp_keywords = {
        "int": "整数", "float": "小数", "double": "小数",
        "char": "字符", "void": "空值", "bool": "真假",
        "return": "返回", "if": "如果", "else": "否则",
        "for": "遍历", "while": "当", "class": "类型",
        "public": "公开", "private": "私有", "protected": "保护",
        "const": "常量", "static": "静态", "virtual": "虚",
        "include": "导入", "using": "使用", "namespace": "命名空间",
        "struct": "结构", "enum": "枚举",
        "cout": "输出", "cin": "输入", "printf": "打印",
    }

    lines = code.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        indent = line[:len(line) - len(stripped)]
        translated = stripped
        for en, cn in cpp_keywords.items():
            translated = re.sub(r'\b' + en + r'\b', cn, translated)
        result.append(indent + translated)
    return '\n'.join(result)


def translate_js_to_cnsh(code: str) -> str:
    """JavaScript/TypeScript → CNSH 基基翻译"""
    js_keywords = {
        "function": "函数", "const": "常量", "let": "变量", "var": "变量",
        "if": "如果", "else": "否则", "for": "遍历", "while": "当",
        "return": "返回", "class": "类型", "new": "新建",
        "import": "导入", "export": "导出", "from": "从",
        "try": "尝试", "catch": "捕获", "throw": "抛出",
        "async": "异步", "await": "等待",
        "console.log": "打印",
        "true": "真", "false": "假",
        "null": "空值", "undefined": "未定义",
    }

    lines = code.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        indent = line[:len(line) - len(stripped)]
        translated = stripped
        for en, cn in js_keywords.items():
            translated = re.sub(r'\b' + en + r'\b', cn, translated)
        result.append(indent + translated)
    return '\n'.join(result)


TRANSLATORS = {
    "python": translate_python_to_cnsh,
    "javascript": translate_js_to_cnsh,
    "typescript": translate_js_to_cnsh,
    "cpp": translate_cpp_to_cnsh,
    "c": translate_cpp_to_cnsh,
}


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B4 脑区执行入口
    """
    language = features.get("language", "unknown")

    translator = TRANSLATORS.get(language)
    if translator:
        cnsh_code = translator(code)
        translated = cnsh_code != code
    else:
        # 嘗试导入现有翻译引擎
        cnsh_code = code
        translated = False
        try:
            # 嘗试加载现有的 cnsh_translator_engine
            engine_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "cnsh-editor", "cnsh_translator_engine_v2.0.py"
            )
            if os.path.exists(engine_path):
                sys.path.insert(0, os.path.dirname(engine_path))
                # 使用现有引擎会更完整，这裡僅标记
                sys.path.pop(0)
        except Exception:
            pass

    auto_activate = ["B7"]  # 翻译完成後自动激活质量检查

    return {
        "output_code": cnsh_code,
        "auto_activate": auto_activate,
        "translated": translated,
        "language": language,
        "message": f"B4: {'已翻译 ' + language + ' → CNSH' if translated else language + ' 暂无CNSH转换器·保留原码'}"
    }


if __name__ == "__main__":
    test = """
def calculate_price(quantity, unit_price):
    total = quantity * unit_price
    if total > 100:
        return total * 0.9
    return total
"""
    r = execute(test, {"language": "python"}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))
    print("\n--- CNSH 输出 ---")
    print(r["output_code"])
