#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH → Python 转译器
DNA: #龍芯⚡️2026-06-29-CNSH-TRANSLATOR-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬CNSH-RUNNER-001 ✅

用法：
  python3 cnsh_runner.py "打印「你好」"
  python3 cnsh_runner.py test.cnsh
  python3 cnsh_runner.py --dump "打印「你好」"   # 只输出Python代码，不执行
"""

import sys
import re
import os
import hashlib
import time
from pathlib import Path

import cnsh_redlines


# ============================================================
# 1. DNA 追溯
# ============================================================

def 生成DNA(模块: str, 动作: str) -> str:
    """生成龍魂标准DNA追溯码"""
    时间戳 = time.strftime("%Y-%m-%d-%H%M%S")
    熵 = hashlib.sha256(f"{模块}-{动作}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{时间戳}-{模块}-{动作}-HASH{熵}"


# ============================================================
# 2. CNSH → Python 翻译规则
# ============================================================

# 表达式级别关键词替换（前后必须有词边界，防止破坏标识符）
CNSH_KEYWORDS = {
    # 布尔与空值
    '真': 'True',
    '假': 'False',
    '空': 'None',
    # 逻辑运算符
    '与': 'and',
    '或': 'or',
    '非': 'not',
    # 成员/身份
    '在': 'in',
    '不在': 'not in',
    '是': 'is',
    '不是': 'is not',
}

# 标准库函数映射（调用场景）
CNSH_BUILTINS = {
    # 类型转换
    '整数': 'int',
    '小数': 'float',
    '文本': 'str',
    '真假': 'bool',
    '列表': 'list',
    '映射': 'dict',
    '元组': 'tuple',
    '集合': 'set',
    # 常用函数
    '范围': 'range',
    '长度': 'len',
    '枚举': 'enumerate',
    '拉链': 'zip',
    '映射函数': 'map',
    '过滤': 'filter',
    '排序': 'sorted',
    '最大': 'max',
    '最小': 'min',
    '绝对值': 'abs',
    '四舍五入': 'round',
    '任何': 'any',
    '全部': 'all',
}

# 比较运算符（保持符号优先，但支持中文写法）
CNSH_OPERATORS = {
    '等于': '==',
    '不等于': '!=',
    '大于等于': '>=',
    '小于等于': '<=',
    '大于': '>',
    '小于': '<',
}

# 类型声明前缀：文本 变量 = "..."  →  变量 = "..."
# 整数 变量 = ...                →  变量 = int(...)
# 小数 变量 = ...                →  变量 = float(...)
# 真假 变量 = ...                →  变量 = bool(...)
# 列表 变量 = [...]              →  变量 = [...]
# 映射 变量 = {...}              →  变量 = {...}
TYPE_CAST_MAP = {
    '整数': 'int',
    '小数': 'float',
    '真假': 'bool',
}

TYPE_NAME_MAP = {
    '整数': 'int',
    '小数': 'float',
    '文本': 'str',
    '真假': 'bool',
    '列表': 'list',
    '映射': 'dict',
    '元组': 'tuple',
    '集合': 'set',
}


# 单行结构翻译规则（按优先级排序，先精确后模糊）
def translate_structure(line: str) -> str:
    """翻译单行 CNSH 结构语句"""
    s = line.strip()

    # 注释行：# 注释
    if s.startswith('#'):
        return s

    # 尝试/捕获/最终
    if re.match(r'^尝试\s*\{?', s):
        return re.sub(r'^尝试\s*\{?', 'try:', s)
    m = re.match(r'^捕获\s+(\w+)\s+(\w+)\s*\{?', s)
    if m:
        return f"except {m.group(1)} as {m.group(2)}:"
    if re.match(r'^最终\s*\{?', s):
        return re.sub(r'^最终\s*\{?', 'finally:', s)

    # 函数定义：函数 名字(参数) { / 函数 名字(参数) 返回类型 类型 {
    m = re.match(r'^函数\s+(\w+)\s*\(([^)]*)\)\s*返回类型\s+(\w+)\s*\{?', s)
    if m:
        返回类型 = TYPE_NAME_MAP.get(m.group(3), m.group(3))
        return f"def {m.group(1)}({m.group(2)}) -> {返回类型}:"
    m = re.match(r'^函数\s+(\w+)\s*\(([^)]*)\)\s*\{?', s)
    if m:
        return f"def {m.group(1)}({m.group(2)}):"

    # 控制流
    m = re.match(r'^如果〖([^〗]+)〗\s*\{?', s)
    if m:
        return f"if {translate_expression(m.group(1))}:"
    m = re.match(r'^否则如果〖([^〗]+)〗\s*\{?', s)
    if m:
        return f"elif {translate_expression(m.group(1))}:"
    if re.match(r'^否则\s*\{?', s):
        return 'else:'
    m = re.match(r'^循环〖([^〗]+)〗\s*\{?', s)
    if m:
        return f"for {translate_expression(m.group(1))}:"
    m = re.match(r'^当〖([^〗]+)〗\s*\{?', s)
    if m:
        return f"while {translate_expression(m.group(1))}:"

    # 返回 / 跳出 / 继续
    m = re.match(r'^返回\s+(.+)$', s)
    if m:
        return f"return {translate_expression(m.group(1))}"
    if s == '返回':
        return 'return'
    if s == '跳出':
        return 'break'
    if s == '继续':
        return 'continue'

    # 输入
    m = re.match(r'^输入\s+(\w+)$', s)
    if m:
        return f"{m.group(1)} = input()"
    m = re.match(r'^输入\s+(\w+)\s*「([^」]*)」$', s)
    if m:
        return f"{m.group(1)} = input(\"{m.group(2)}\")"

    # 打印：打印「...」 / 打印(表达式) / 打印 表达式
    m = re.match(r'^打印「([^」]*)」$', s)
    if m:
        return f"print(\"{m.group(1)}\")"
    m = re.match(r'^打印\s*(.+)$', s)
    if m:
        return f"print({translate_expression(m.group(1))})"

    # 类型声明：类型 变量 = 表达式
    m = re.match(r'^(整数|小数|真假)\s+(\w+)\s*=\s*(.+)$', s)
    if m:
        类型, 变量, 表达式 = m.groups()
        return f"{变量} = {TYPE_CAST_MAP[类型]}({translate_expression(表达式)})"
    m = re.match(r'^(文本|列表|映射)\s+(\w+)\s*=\s*(.+)$', s)
    if m:
        _, 变量, 表达式 = m.groups()
        return f"{变量} = {translate_expression(表达式)}"

    # 普通赋值 / 表达式语句
    return translate_expression(s)


def translate_expression(expr: str) -> str:
    """翻译表达式中的关键词和函数名"""
    # 1. 多字符运算符先替换（避免被单字符覆盖）
    for cn, py in CNSH_OPERATORS.items():
        expr = _replace_word(expr, cn, py)

    # 2. 关键词替换（真/假/空/与/或/非/在/不在/是/不是）
    # 按长度降序，避免 "不在" 被拆成 "不"+"在"
    for cn in sorted(CNSH_KEYWORDS.keys(), key=len, reverse=True):
        expr = _replace_word(expr, cn, CNSH_KEYWORDS[cn])

    # 3. 内置函数名替换（仅匹配函数调用形式：名字(）
    for cn, py in CNSH_BUILTINS.items():
        expr = re.sub(rf'(?<![\u4e00-\u9fa5\w]){re.escape(cn)}(?=\s*\()', py, expr)

    return expr


def _replace_word(text: str, word: str, replacement: str) -> str:
    """按词边界替换，不破坏标识符内部"""
    pattern = rf'(?<![\u4e00-\u9fa5\w]){re.escape(word)}(?![\u4e00-\u9fa5\w])'
    return re.sub(pattern, replacement, text)


def preprocess_strings(code: str) -> str:
    """把 CNSH 字符串「...」 预翻译成 Python 字符串 \"...\""""
    def replace_string(m):
        content = m.group(1)
        content = content.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{content}"'
    return re.sub(r'「([^」]*)」', replace_string, code)


def translate_cnsh(code: str) -> str:
    """翻译整个 CNSH 脚本"""
    code = preprocess_strings(code)
    lines = code.split('\n')
    result = []
    indent = 0

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        # 保留空行
        if not stripped:
            result.append('')
            continue

        # 保留注释行
        if stripped.startswith('#'):
            result.append('    ' * indent + stripped)
            continue

        # 块结束
        if stripped == '}':
            indent = max(0, indent - 1)
            continue

        # 内联块切换：} 否则 {
        m = re.match(r'^}\s*否则\s*\{$', stripped)
        if m:
            indent = max(0, indent - 1)
            result.append('    ' * indent + 'else:')
            indent += 1
            continue

        # 内联块切换：} 否则如果〖条件〗{
        m = re.match(r'^}\s*否则如果〖([^〗]+)〗\s*\{$', stripped)
        if m:
            indent = max(0, indent - 1)
            result.append('    ' * indent + 'elif ' + translate_expression(m.group(1)) + ':')
            indent += 1
            continue

        # 块开始（行尾带 {）
        if stripped.endswith('{'):
            stmt = stripped[:-1].strip()
            translated = translate_structure(stmt)
            result.append('    ' * indent + translated)
            indent += 1
            continue

        # 普通语句
        translated = translate_structure(stripped)
        result.append('    ' * indent + translated)

    return '\n'.join(result)


def execute_cnsh(source: str, dump_only: bool = False):
    """执行 CNSH 代码（先过红线熔断检查）"""
    py_code = translate_cnsh(source)
    py_code = '\n'.join(line for line in py_code.split('\n') if line.strip() != '')

    # 红线熔断检查：扫描 CNSH 源码与生成代码
    熔断器 = cnsh_redlines.红线熔断器()
    检查结果 = 熔断器.熔断检查(source + "\n" + py_code)
    if 检查结果["触发"]:
        print("🔴 龍魂 CNSH 红线熔断")
        print(熔断器.报告(检查结果))
        print("\n龍魂系统 AI 拒绝执行包含红线词组的 CNSH 代码。")
        sys.exit(1)

    if dump_only:
        print(py_code)
        return py_code

    dna = 生成DNA('CNSH-TRANSLATOR', 'EXECUTE')
    print("🐉 龙魂 CNSH → Python")
    print(f"   {dna}")
    print("-" * 40)
    print(py_code)
    print("-" * 40)

    # 创建独立命名空间执行，避免污染全局
    namespace = {'__name__': '__cnsh__'}
    exec(py_code, namespace)
    return py_code


# ============================================================
# 3. CLI 入口
# ============================================================

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    dump_only = False
    if args[0] == '--dump':
        dump_only = True
        args = args[1:]
        if not args:
            print("用法: python3 cnsh_runner.py --dump \"打印「你好」\"")
            return

    arg = args[0]

    # 文件模式
    if arg.endswith('.cnsh'):
        path = Path(arg)
        if not path.exists():
            path = Path.home() / arg
        if not path.exists():
            print(f"❌ 找不到文件: {arg}")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            execute_cnsh(f.read(), dump_only=dump_only)
        return

    # 直接执行 CNSH 代码
    execute_cnsh(arg, dump_only=dump_only)


if __name__ == "__main__":
    main()
