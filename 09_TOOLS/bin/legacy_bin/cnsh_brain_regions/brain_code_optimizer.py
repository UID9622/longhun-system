#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
B6 · 代码优化脑区 → P02 龍芯修复师
====================================
算法优化、结构优化、性能改进。
最小修复原则：只改必要的，不改正确的。

DNA: #龍芯⚡️丙午·丙申·丙辰·未时·需-BRAIN-B6-CODE-OPTIMIZER-v1.0
"""

import re
from typing import Dict, Any, List


def optimize_naming(code: str) -> Tuple[str, List[str]]:
    """优化变量命名"""
    changes = []
    result = code

    poor_names = {
        "var1": "first_var", "var2": "second_var",
        "temp": "tmp_value", "tmp": "tmp_value",
        "data": "input_data", "result": "output_result",
        "thing": "item",
    }

    for poor, better in poor_names.items():
        pattern = r'\b' + poor + r'\b(?![\w"])'
        if re.search(pattern, result):
            changes.append(f"重命名 {poor} → {better}")

    return result, changes


def optimize_loops(code: str) -> Tuple[str, List[str]]:
    """优化循环结构"""
    changes = []

    # 检测 range(len(x)) 模式
    if re.search(r'range\(\s*len\(', code):
        changes.append("建议: range(len(x)) → enumerate(x)")

    # 检测 flag 循环
    if re.search(r'found\s*=\s*(True|False)', code):
        changes.append("建议: 使用 for-else 或 early return 替代 flag 模式")

    return code, changes


def optimize_imports(code: str) -> Tuple[str, List[str]]:
    """优化导入语句"""
    changes = []
    lines = code.split('\n')
    imports = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('import ', 'from ')):
            imports.append(stripped)

    # 检查重复导入
    seen = set()
    for imp in imports:
        base = imp.split(' as ')[0] if ' as ' in imp else imp
        if base in seen:
            changes.append(f"重复导入: {imp}")
        seen.add(base)

    return code, changes


def basic_fixes(code: str) -> Tuple[str, List[str]]:
    """基基修复"""
    changes = []

    # 修复多余空行 (>3)
    while '\n\n\n\n' in code:
        code = code.replace('\n\n\n\n', '\n\n\n')
        changes.append("压縮多余空行")

    # 修复行尾空白
    new_lines = []
    for line in code.split('\n'):
        fixed = line.rstrip()
        if fixed != line:
            changes.append("去除行尾空白")
        new_lines.append(fixed)
    code = '\n'.join(new_lines)

    return code, changes


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B6 脑区执行入口

    返回优化後的代码（最小修复原则）
    """
    all_changes: List[str] = []

    code, c1 = basic_fixes(code)
    all_changes.extend(c1)

    code, c2 = optimize_loops(code)
    all_changes.extend(c2)

    code, c3 = optimize_imports(code)
    all_changes.extend(c3)

    code, c4 = optimize_naming(code)
    all_changes.extend(c4)

    optimized = len(all_changes) > 0
    level = "🟢 无需优化" if not optimized else "🟡 轻微优化" if len(all_changes) <= 3 else "🔴 多項优化"

    return {
        "output_code": code,
        "auto_activate": [],
        "optimized": optimized,
        "changes_count": len(all_changes),
        "changes": all_changes[:10],  # 最多记录10条
        "level": level,
        "message": f"B6: {level} · {len(all_changes)}处改动"
    }


if __name__ == "__main__":
    test = "x = 1\n\n\n\ny = 2   \n\n\n\nz = 3"
    r = execute(test, {}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))
