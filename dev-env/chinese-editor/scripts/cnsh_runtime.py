# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 本地运行时 · 中文母语脚本执行器
DNA: #龍芯⚡️2026-06-26-DEVENV-CNSH-RUNTIME-v3.0

基于缩进推断块结构，将 CNSH 中文关键字翻译为 Python 后执行。
本版本已吸入 CNSH 编译器框架 v1.0/v2.0 主干语法规范。
"""
import argparse
import re
from pathlib import Path


TYPE_MAP = {
    "整数": "int",
    "小数": "float",
    "文本": "str",
    "真假": "bool",
    "列表": "list",
    "字典": "dict",
    "空值": "None",
}

BOOL_MAP = {"真": "True", "假": "False"}


def normalize_punctuation(source: str) -> str:
    """中文标点符号标准化为英文"""
    replacements = {
        chr(8220): chr(34), chr(8221): chr(34),  # "" -> "
        chr(8216): chr(39), chr(8217): chr(39),  # '' -> '
        chr(65288): chr(40), chr(65289): chr(41),  # （） -> ()
        chr(12300): chr(34), chr(12301): chr(34),  # 「」 -> "
        chr(12302): chr(34), chr(12303): chr(34),  # 『』 -> "
        "【": "(", "】": ")",
        "｛": "{", "｝": "}",
        "；": ";", "，": ",",
        "：": ":", "。": ".",
    }
    for ch, repl in replacements.items():
        source = source.replace(ch, repl)
    return source


def strip_type_declarations(source: str) -> str:
    """移除 CNSH 变量/参数类型声明前缀，但保留函数返回类型声明"""
    lines = source.splitlines()
    out = []
    for line in lines:
        # 保留返回类型关键字本身，但函数参数中的类型仍需剥离
        # 行首的类型声明："整数 年龄 = ..." -> "年龄 = ..."（保留原缩进）
        leading = line[:len(line) - len(line.lstrip())]
        rest = line.lstrip()
        rest = re.sub(r"^(" + "|".join(TYPE_MAP.keys()) + r")\b\s+", "", rest)
        line = leading + rest
        # 函数参数中的类型声明："(整数 a, 文本 b)" -> "(a, b)"
        line = re.sub(r"\b(" + "|".join(TYPE_MAP.keys()) + r")\b\s+(\w+)", r"\2", line)
        out.append(line)
    return "\n".join(out)


def translate_cnsh_to_python(source: str) -> str:
    """将 CNSH 源码翻译为 Python"""
    source = normalize_punctuation(source)

    # 在关键字替换前先把类型声明（变量声明）剥离，避免"整数 数字"干扰后续语法
    source = strip_type_declarations(source)

    # 返回类型：必须在 strip_type_declarations 之后，避免"返回类型 整数"中的"整数"被误删
    def map_return_type(m):
        t = m.group(1)
        return f"-> {TYPE_MAP.get(t, t)}:"
    source = re.sub(r"返回类型\s+(\w+)\s*\{", map_return_type, source)

    # 用占位符方式保护字符串与 DNA 后再做关键字映射
    placeholders = {}
    placeholder_id = 0

    def make_placeholder(text):
        nonlocal placeholder_id
        key = f"__CNSH_PLACEHOLDER_{placeholder_id}__"
        placeholder_id += 1
        placeholders[key] = text
        return key

    # 保护字符串字面量
    def protect_string(m):
        return make_placeholder(m.group(0))
    source = re.sub(r'"(?:[^"\\]|\\.)*"', protect_string, source)
    source = re.sub(r"'(?:[^'\\]|\\.)*'", protect_string, source)

    # 保护 DNA 追溯码
    def protect_dna(m):
        return make_placeholder(m.group(0))
    source = re.sub(r"#龍芯⚡️[^\s]*", protect_dna, source)
    source = re.sub(r"#CONFIRM[^\s]*", protect_dna, source)
    source = re.sub(r"#ZHUGEXIN[^\s]*", protect_dna, source)

    # 循环【n】{ ... } 是固定次数循环，翻译为 for __cnshexpr in range(n)
    def transform_loop(m):
        expr = m.group(1).strip()
        return f"for __cnshexpr in range({expr}): {{"
    source = re.sub(r"(?<![\u4e00-\u9fa5A-Za-z0-9])循环\s*\(([^)]+)\)\s*\{", transform_loop, source)

    # 关键字映射（注意顺序：先处理较长的词和特殊符号）
    keywords = [
        ("函数", "def"),
        ("返回", "return"),
        ("如果", "if"),
        ("否则如果", "elif"),
        ("否则", "else"),
        ("当", "while"),
        ("对于", "for"),
        ("在", "in"),
        ("范围", "range"),
        ("打印", "print"),
        ("跳出", "break"),
        ("继续", "continue"),
        ("并且", "and"),
        ("或者", "or"),
        ("非", "not"),
        ("不大于", "<="),
        ("不小于", ">="),
        ("等于", "=="),
        ("不等于", "!="),
        ("真", "True"),
        ("假", "False"),
        ("空", "None"),
    ]

    # 关键字替换：按长度降序避免"否则如果"被拆成"否则"+"如果"
    # 使用前后边界，避免误伤中文标识符（如"主函数"中的"函数"）
    def replace_keyword(src, cn, py):
        # 边界只考虑中文/字母/数字；占位符以非单词字符开头，因此关键字后跟字符串占位符也能被替换
        pat = r"(?<![\u4e00-\u9fa5A-Za-z0-9])" + re.escape(cn) + r"(?![\u4e00-\u9fa5A-Za-z0-9])"
        return re.sub(pat, py, src)

    for cn, py in sorted(keywords, key=lambda x: len(x[0]), reverse=True):
        source = replace_keyword(source, cn, py)

    # 恢复占位符
    for key, val in placeholders.items():
        source = source.replace(key, val)

    # 按 {} 块结构推断 Python 缩进
    raw_lines = source.splitlines()

    indent_stack = [0]
    virtual_lines = []
    for raw in raw_lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("##"):
            virtual_lines.append((raw, -1, stripped))
            continue

        # 统计行尾的 } 数量（可能形如 "} 否则 {"）
        close_count = 0
        tmp = stripped
        while tmp.endswith("}"):
            tmp = tmp[:-1].rstrip()
            close_count += 1

        # 统计行尾的 { 数量
        open_count = 0
        tmp2 = tmp
        while tmp2.endswith("{"):
            tmp2 = tmp2[:-1].rstrip()
            open_count += 1

        # 先处理 close（当前行结束旧块），再处理 open（当前行开始新块）
        for _ in range(close_count):
            if len(indent_stack) > 1:
                indent_stack.pop()

        base_indent = len(raw) - len(raw.lstrip())
        # 虚拟缩进：当前块缩进 + 原始行缩进
        virtual_indent = indent_stack[-1] + base_indent

        # 给 if / for / while / def / elif 行尾补冒号（CNSH 块用 {} 而非冒号）
        if re.match(r"\s*(if|for|while|def|elif)\b", tmp2) and not tmp2.rstrip().endswith(":"):
            tmp2 = tmp2.rstrip() + ":"

        virtual_lines.append((" " * virtual_indent + tmp2, virtual_indent, tmp2))

        for _ in range(open_count):
            indent_stack.append(indent_stack[-1] + 4)

    # 基于虚拟缩进生成 Python 缩进
    py_lines = []
    block_indents = [-1]

    for raw, indent, stripped in virtual_lines:
        if indent == -1:
            py_lines.append(raw)
            continue

        if not stripped:
            continue

        # 清理行首可能残留的 }
        if stripped.startswith("}"):
            stripped = stripped.lstrip("}").strip()
            if not stripped:
                continue

        # else/elif 与上层的 if/for/while/def 同层
        if stripped.startswith("else") or stripped.startswith("elif"):
            if not stripped.endswith(":"):
                stripped += ":"
            if len(block_indents) > 1:
                block_indents.pop()
            logical_indent = len(block_indents) - 1
            py_lines.append("    " * logical_indent + stripped)
            # else 分支本身开启一个新块，供后续语句缩进
            block_indents.append(indent)
            continue

        while len(block_indents) > 1 and indent <= block_indents[-1]:
            block_indents.pop()

        logical_indent = len(block_indents) - 1
        py_lines.append("    " * logical_indent + stripped)

        if stripped.endswith(":"):
            block_indents.append(indent)

    # 移除空行
    cleaned_lines = [line for line in py_lines if line.strip()]

    return "\n".join(cleaned_lines)


def fix_print_calls(code: str) -> str:
    """修复 print"..." / print "..." 为 print(...)"""
    # 匹配 print 后紧跟双引号字符串（允许前导空白）
    code = re.sub(r'print\s*"([^"]*)"', r'print("\1")', code)
    code = re.sub(r"print\s*'([^']*)'", r'print("\1")', code)
    return code


def fix_fstrings(code: str) -> str:
    """把 CNSH 的 print '...{变量}...' 转换为 Python f-string"""
    # 将 print("...{xxx}...") 转换为 print(f"...{xxx}...")
    def make_fstring(m):
        inner = m.group(1)
        # 简单判断内部是否有 {变量} 模式
        if re.search(r"\{[A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*\}", inner):
            return f'print(f"{inner}")'
        return f'print("{inner}")'
    code = re.sub(r'print\("([^"]*)"\)', make_fstring, code)
    return code


def run_cnsh(file_path: str, dry_run: bool = False):
    p = Path(file_path)
    if not p.exists():
        print(f"❌ 文件不存在: {file_path}")
        return 1

    source = p.read_text(encoding="utf-8", errors="ignore")
    print(f"🐉 运行 CNSH 脚本: {p.name}")
    print("-" * 40)

    python_code = translate_cnsh_to_python(source)
    python_code = fix_print_calls(python_code)
    python_code = fix_fstrings(python_code)

    if dry_run:
        print("📝 生成的 Python 代码:")
        print(python_code)
        return 0

    try:
        namespace = {"__name__": "__main__"}
        exec(python_code, namespace)
        # CNSH 约定：如果定义了 主函数，自动调用它
        if "主函数" in namespace and callable(namespace["主函数"]):
            namespace["主函数"]()
        print("-" * 40)
        print("✅ CNSH 脚本执行完成")
        return 0
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        print("\n生成的 Python 代码:")
        print(python_code)
        return 1


def main():
    parser = argparse.ArgumentParser(description="CNSH 本地运行时")
    parser.add_argument("file", help="CNSH 脚本文件路径")
    parser.add_argument("--dry-run", action="store_true", help="只输出翻译后的 Python 代码，不执行")
    args = parser.parse_args()
    return run_cnsh(args.file, args.dry_run)


if __name__ == "__main__":
    import sys
    sys.exit(main())
