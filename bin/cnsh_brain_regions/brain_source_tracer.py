#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-BRAIN_SOURCE_TRACER-v1.0-08b25d3f
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
B3 · 来源追溯脑区 → P18 凤凰
================================
提取代码指纹，追踪来源，构建追溯链。

四种指纹:
  1. 语法指纹: 缩进、命名、括号风格
  2. 算法指纹: 控制流模式、复杂度
  3. DNA指纹: #ZHUGEXIN⚡️ / #龙芯⚡️ 识别
  4. 语义哈希: 内容结构哈希

DNA: #龙芯⚡️丙午·丙申·丙辰·未时·需-BRAIN-B3-SOURCE-TRACER-v1.0
"""

import re
import hashlib
from typing import Dict, Any, List, Optional


def extract_syntax_fingerprint(code: str) -> Dict[str, Any]:
    """提取语法指纹"""
    lines = code.split('\n')
    non_empty = [l for l in lines if l.strip()]

    # 缩进风格
    indent_chars = []
    for l in non_empty:
        stripped = l.lstrip()
        if stripped != l:
            indent = l[:len(l) - len(stripped)]
            indent_chars.append(indent)

    tab_count = sum(1 for i in indent_chars if '\t' in i)
    space_count = sum(1 for i in indent_chars if i.startswith('  '))
    indent_style = "tabs" if tab_count > space_count else "spaces"

    # 括号风格
    has_brace_same_line = any('{' in l and not l.strip().startswith('{') for l in non_empty)
    has_brace_new_line = any(l.strip() == '{' for l in non_empty)

    # 命名风格
    snake_case = sum(1 for l in non_empty if re.search(r'\b[a-z]+_[a-z]+\b', l))
    camelCase = sum(1 for l in non_empty if re.search(r'\b[a-z]+[A-Z][a-z]+\b', l))
    PascalCase = sum(1 for l in non_empty if re.search(r'\b[A-Z][a-z]+[A-Z][a-z]+\b', l))

    naming = "snake_case" if snake_case > camelCase else "camelCase" if camelCase > PascalCase else "mixed"

    return {
        "indent_style": indent_style,
        "indent_count": len(indent_chars),
        "brace_same_line": has_brace_same_line,
        "brace_new_line": has_brace_new_line,
        "naming_style": naming,
        "snake_case_count": snake_case,
        "camelCase_count": camelCase,
        "PascalCase_count": PascalCase
    }


def extract_algo_fingerprint(code: str) -> Dict[str, Any]:
    """提取算法指纹"""
    lines = code.split('\n')

    loop_count = 0
    condition_count = 0
    recursion = False

    loop_patterns = [
        r'\bfor\b', r'\bwhile\b', r'\bforeach\b',
        r'\.forEach\(', r'\.map\(', r'^loop\b'
    ]
    condition_patterns = [r'\bif\b', r'\belse\b', r'\belif\b', r'\bswitch\b', r'\bcase\b']

    for line in lines:
        for pat in loop_patterns:
            if re.search(pat, line, re.IGNORECASE):
                loop_count += 1
        for pat in condition_patterns:
            if re.search(pat, line, re.IGNORECASE):
                condition_count += 1

    # 复杂度估算
    cyclomatic = 1 + condition_count + loop_count

    return {
        "loop_count": loop_count,
        "condition_count": condition_count,
        "cyclomatic_complexity": cyclomatic,
        "complexity_level": "低" if cyclomatic <= 5 else "中" if cyclomatic <= 10 else "高"
    }


def extract_dna_fingerprint(code: str) -> Optional[str]:
    """提取DNA追溯码"""
    patterns = [r'#ZHUGEXIN⚡️[^\n]+', r'#龙芯⚡️[^\n]+', r'DNA[：:]\s*[^\n]+']
    for pat in patterns:
        m = re.search(pat, code)
        if m:
            return m.group(0).strip()
    return None


def compute_semantic_hash(code: str) -> str:
    """计算语义哈希"""
    # 去除空白和註釋後哈希
    normalized = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    normalized = re.sub(r'//.*$', '', normalized, flags=re.MULTILINE)
    normalized = re.sub(r'\s+', '', normalized)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B3 脑区执行入口
    """
    syntax_fp = extract_syntax_fingerprint(code)
    algo_fp = extract_algo_fingerprint(code)
    dna_fp = extract_dna_fingerprint(code)
    semantic_hash = compute_semantic_hash(code)

    trace_chain = {
        "syntax_fingerprint": syntax_fp,
        "algorithm_fingerprint": algo_fp,
        "dna_fingerprint": dna_fp,
        "semantic_hash": semantic_hash,
        "source_matches": [],  # 来源匹配结果（需外部API）
        "trace_level": "🟢 本地指纹" if dna_fp else "🟡 无DNA·仅指纹"
    }

    has_dna = dna_fp is not None

    return {
        "output_code": code,
        "auto_activate": [],
        "trace_chain": trace_chain,
        "has_dna": has_dna,
        "dna_code": dna_fp,
        "message": f"B3: 来源追溯完成 · {'有DNA' if has_dna else '无DNA·本地指纹'} · hash={semantic_hash}"
    }


if __name__ == "__main__":
    test = """
#龙芯⚡️丙午·丙申-EXAMPLE-ABCD1234
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)
"""
    r = execute(test, {}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))
