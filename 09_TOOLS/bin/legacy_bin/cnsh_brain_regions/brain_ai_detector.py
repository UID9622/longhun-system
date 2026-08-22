#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
B2 · AI鉴定脑区 → P03 墨子/雯雯
================================
检测AI生成的伪代码、幻觉和异常模式。
评分: 伪代码分 + 幻觉分*1.5 + 命名模式分

DNA: #龍芯⚡️丙午·丙申·丙辰·未时·䷄需-BRAIN-B2-AI-DETECTOR-v1.0
"""

import re
from typing import Dict, Any, List


# ── 伪代码特征库 ──────────────────────────────────────────────────────────────

PSEUDO_CODE_PATTERNS: List[str] = [
    "TODO:",
    "TODO：",
    "FIXME",
    "HACK:",
    "PLACEHOLDER",
    "placeholder",
    "stub",
    "// ... 此处省略",
    "# ... 此处省略",
    "// 伪代码",
    "# 伪代码",
    "// pseudocode",
    "# pseudocode",
    "这裡应该调用API",
    "此处应调用",
    "假设",
    "假设",
    "// implement later",
    "# implement later",
    "// not implemented",
    "# not implemented",
]


HALLUCINATION_PATTERNS: List[str] = [
    # 不存在的库
    "from doesnotexist import",
    "import nonexistent_lib",
    "require('fake-lib')",
    # 虛构的API
    ".doSomethingThatDoesNotExist(",
    ".magicMethod(",
    # 不一致的类型
    "str_value: int = \"hello\"",
    "number = \"123\" + 456",
    # 不可能的组合
    "while True: pass  # infinite",
    "print(undefined_variable)",
]


NAMED_POORLY: List[str] = [
    "var1", "var2", "var3", "var4",
    "temp", "tmp", "temp_var",
    "x", "y", "z",  # 在复杂函数中
    "data", "result", "thing",
    "foo", "bar", "baz",
    "xxx", "test", "test1", "test2",
    "my_function", "my_class",
]


def score_pseudo_code(code: str) -> Dict[str, Any]:
    """伪代码评分"""
    hits = []
    score = 0

    for pat in PSEUDO_CODE_PATTERNS:
        if pat in code:
            hits.append(pat)
            score += 10

    return {"score": min(score, 100), "hits": hits, "count": len(hits)}


def score_hallucination(code: str) -> Dict[str, Any]:
    """幻觉检测评分"""
    hits = []
    score = 0

    for pat in HALLUCINATION_PATTERNS:
        if pat in code:
            hits.append(pat)
            score += 15

    # 检查未定义变量的使用
    definitions = set()
    usages = set()

    # 簡单的变量定义/使用检测
    for line in code.split('\n'):
        stripped = line.strip()
        # Python: var_name = ...
        m = re.match(r'^(\w+)\s*=\s*', stripped)
        if m and m.group(1) not in ('if', 'for', 'while', 'def', 'class', 'import', 'from', 'return'):
            definitions.add(m.group(1))
        # function(var_name):
        m = re.match(r'^def\s+(\w+)\s*\(([^)]*)\)', stripped)
        if m:
            params = [p.strip().split(':')[0].strip() for p in m.group(2).split(',') if p.strip()]
            definitions.update(params)

    for line in code.split('\n'):
        words = re.findall(r'\b([a-zA-Z_]\w*)\b', line)
        for w in words:
            if w not in ('if', 'else', 'elif', 'for', 'while', 'def', 'class',
                         'return', 'print', 'import', 'from', 'True', 'False',
                         'None', 'in', 'not', 'and', 'or', 'is', 'as', 'with',
                         'try', 'except', 'finally', 'raise', 'pass', 'break',
                         'continue', 'lambda', 'yield', 'global', 'nonlocal',
                         'self', 'str', 'int', 'float', 'bool', 'list', 'dict',
                         'set', 'tuple', 'type', 'len', 'range', 'str'):
                usages.add(w)

    undefined = usages - definitions
    if undefined and len(undefined) > 3:
        hits.append(f"未定义变量: {', '.join(list(undefined)[:5])}")
        score += min(len(undefined) * 3, 30)

    return {"score": min(score, 100), "hits": hits, "count": len(hits)}


def score_naming(code: str) -> Dict[str, Any]:
    """命名模式评分"""
    hits = []
    score = 0

    words = re.findall(r'\b([a-zA-Z_]\w*)\b', code)
    for name in NAMED_POORLY:
        if name in words:
            hits.append(name)
            if name in ("var1", "var2", "var3", "var4", "foo", "bar", "baz", "xxx"):
                score += 12
            elif name in ("temp", "tmp", "x", "y", "z"):
                score += 5
            else:
                score += 3

    return {"score": min(score, 100), "hits": hits, "count": len(hits)}


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B2 脑区执行入口

    綜合评估: AI生成概率 = 命名分*0.6 + 幻觉分*1.5 + 伪代码分 (上限100)
    """
    pseudo = score_pseudo_code(code)
    halluc = score_hallucination(code)
    naming = score_naming(code)

    # 加权计算
    ai_probability = naming["score"] * 0.6 + halluc["score"] * 1.5 + pseudo["score"]
    ai_probability = min(ai_probability, 100)

    # 判定级别
    if ai_probability >= 70:
        level = "🔴 高风险：极可能为AI生成或伪代码"
        recommendation = "强烈建议人工审查，拒绝自动合入"
    elif ai_probability >= 40:
        level = "🟡 中风险：可能含AI生成内容"
        recommendation = "建议人工审查後决定"
    else:
        level = "🟢 低风险：大概率为人工编写"
        recommendation = "自动流程可继续"

    # 自动激活来源追溯
    auto_activate = []
    if ai_probability >= 60:
        auto_activate.append("B3")  # 高概率 → 追溯来源

    return {
        "output_code": code,
        "auto_activate": auto_activate,
        "ai_probability": round(ai_probability, 1),
        "level": level,
        "recommendation": recommendation,
        "details": {
            "pseudo_code": pseudo,
            "hallucination": halluc,
            "naming": naming
        },
        "message": f"B2: AI概率 {ai_probability:.1f}% · {level}"
    }


if __name__ == "__main__":
    test = """
def calculate(var1):
    temp = var1 * 2
    # TODO: add validation
    result = temp + 100
    return result
"""
    r = execute(test, {}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))
