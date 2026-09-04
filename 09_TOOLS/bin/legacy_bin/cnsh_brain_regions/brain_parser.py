#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
B1 · 多语言解析脑区 → P07 开源守门
====================================
解析多种编程语言的AST，提取语法特征。
支援: Python, JavaScript, TypeScript, Java, C/C++, Go, Rust

DNA: #龍芯⚡️丙午·丙申·丙辰·未时·䷄需-BRAIN-B1-PARSER-v1.0
"""

import re
from typing import Dict, Any, List, Optional


def detect_language(code: str) -> str:
    """检测代码语言"""
    patterns = {
        "python":     [r"^def\s+\w+\s*\(.*\):", r"^import\s+\w+", r"^from\s+\w+\s+import", r"self\."],
        "javascript": [r"^function\s+\w+\s*\(.*\)\s*\{", r"^const\s+\w+\s*=", r"=>\s*\{", r"console\.log"],
        "typescript": [r":\s*string\b", r":\s*number\b", r"interface\s+\w+", r"^export\s+(interface|type|class)"],
        "java":       [r"public\s+class\s+\w+", r"private\s+\w+\s+\w+", r"System\.out\.print"],
        "cpp":        [r"#include\s*<", r"std::\w+", r"int\s+main\s*\(", r"->\s*\w+"],
        "go":         [r"^func\s+\w+\s*\(.*\)", r"^package\s+\w+", r"fmt\.\w+", r"defer\s+"],
        "rust":       [r"^fn\s+\w+\s*\(.*\)", r"let\s+mut\s+", r"^use\s+\w+::", r"impl\s+\w+"]
    }

    scores = {}
    for lang, pats in patterns.items():
        s = sum(1 for p in pats if re.search(p, code, re.MULTILINE))
        if s > 0:
            scores[lang] = s

    if not scores:
        return "unknown"
    return max(scores, key=scores.get)


def extract_functions(code: str, language: str) -> List[Dict[str, Any]]:
    """提取函数定义"""
    functions = []
    lines = code.split('\n')

    patterns = {
        "python":     r"def\s+(\w+)\s*\((.*?)\)",
        "javascript": r"function\s+(\w+)\s*\((.*?)\)",
        "go":         r"func\s+(\w+)\s*\((.*?)\)",
        "rust":       r"fn\s+(\w+)\s*\((.*?)\)",
        "cpp":        r"(\w+)\s+(\w+)\s*\((.*?)\)",
    }

    if language in patterns:
        for line in lines:
            m = re.search(patterns[language], line)
            if m:
                name = m.group(1) if language != "cpp" else m.group(2)
                params = m.group(2) if language != "cpp" else m.group(3)
                functions.append({"name": name, "params": params, "line": line.strip()})

    return functions


def extract_variables(code: str, language: str) -> List[str]:
    """提取变量声明"""
    variables = []

    var_patterns = {
        "python":     [r"^(\w+)\s*=\s*"],
        "javascript": [r"^(?:const|let|var)\s+(\w+)\s*="],
        "typescript": [r"^(?:const|let|var)\s+(\w+)\s*(?::\s*\w+\s*)?="],
    }

    if language in var_patterns:
        for line in code.split('\n'):
            for pat in var_patterns.get(language, []):
                m = re.search(pat, line)
                if m:
                    variables.append(m.group(1))

    return list(set(variables))


def simple_ast(code: str, language: str) -> Dict[str, Any]:
    """簡易AST结构提取"""
    lines = code.split('\n')
    return {
        "total_lines": len(lines),
        "non_empty_lines": len([l for l in lines if l.strip()]),
        "comment_lines": len([l for l in lines if l.strip().startswith(("#", "//", "/*", "*"))]),
        "functions": extract_functions(code, language),
        "variables": extract_variables(code, language),
        "imports": extract_imports(code, language)
    }


def extract_imports(code: str, language: str) -> List[str]:
    """提取导入语句"""
    imports = []
    for line in code.split('\n'):
        stripped = line.strip()
        if language == "python" and stripped.startswith(("import ", "from ")):
            imports.append(stripped)
        elif language in ("javascript", "typescript") and stripped.startswith(("import ", "require(")):
            imports.append(stripped)
        elif language in ("cpp", "c") and stripped.startswith("#include"):
            imports.append(stripped)
        elif language == "go" and stripped.startswith("import"):
            imports.append(stripped)
        elif language == "rust" and stripped.startswith("use "):
            imports.append(stripped)
    return imports


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B1 脑区执行入口

    返回:
        {
            "output_code": str,          # 输出代码
            "auto_activate": List[str],  # 需要自动激活的脑区
            "parsed": Dict[str, Any],              # 解析结果
            "message": str               # 状态訊息
        }
    """
    language = detect_language(code)
    if language == "unknown":
        return {
            "output_code": code,
            "auto_activate": [],
            "parsed": {"language": "unknown", "error": "无法识别语言"},
            "message": "B1: 无法识别编程语言，跳过解析"
        }

    ast = simple_ast(code, language)

    # 自动激活规则：发现伪代码嫌疑
    auto_activate = []
    if any("TODO" in l for l in code.split('\n')):
        auto_activate.append("B2")  # AI鉴定
    if ast["imports"] and len(ast["imports"]) > 5:
        pass  # 多导入不一定是问题

    return {
        "output_code": code,
        "auto_activate": auto_activate,
        "parsed": {
            "language": language,
            "ast_summary": ast
        },
        "message": f"B1: 识别语言 {language}，{ast['total_lines']}行，{len(ast['functions'])}个函数"
    }


if __name__ == "__main__":
    test_code = """
def hello(name: str) -> str:
    return f"Hello, {name}"

def main():
    print(hello("World"))
"""
    result = execute(test_code, {}, 0, 0)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
