# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 本地运行时 · 中文母语脚本执行器
DNA: #龍芯⚡️2026-06-26-LONGHUN-CNSH-RUNTIME-v3.1

基于缩进推断块结构，将 CNSH 中文关键字翻译为 Python 后执行。
本版本已吸入 CNSH 编译器框架 v1.0/v2.0 主干语法规范。
"""
import re
from pathlib import Path

try:
    from .compiler.errors import FriendlyErrorReporter
    from .compiler.pipeline import compile_cnsh_safe
except Exception:  # pragma: no cover - 防御性导入
    compile_cnsh_safe = None
    FriendlyErrorReporter = None


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
        leading = line[: len(line) - len(line.lstrip())]
        rest = line.lstrip()
        rest = re.sub(r"^(" + "|".join(TYPE_MAP.keys()) + r")\b\s+", "", rest)
        line = leading + rest
        line = re.sub(r"\b(" + "|".join(TYPE_MAP.keys()) + r")\b\s+(\w+)", r"\2", line)
        out.append(line)
    return "\n".join(out)


def translate_cnsh_to_python(source: str) -> str:
    """将 CNSH 源码翻译为 Python"""
    source = normalize_punctuation(source)
    source = strip_type_declarations(source)

    def map_return_type(m):
        t = m.group(1)
        return f"-> {TYPE_MAP.get(t, t)}:"

    source = re.sub(r"返回类型\s+(\w+)\s*\{", map_return_type, source)

    placeholders = {}
    placeholder_id = 0

    def make_placeholder(text):
        nonlocal placeholder_id
        key = f"__CNSH_PLACEHOLDER_{placeholder_id}__"
        placeholder_id += 1
        placeholders[key] = text
        return key

    def protect_string(m):
        return make_placeholder(m.group(0))

    source = re.sub(r'"(?:[^"\\]|\\.)*"', protect_string, source)
    source = re.sub(r"'(?:[^'\\]|\\.)*'", protect_string, source)

    def protect_dna(m):
        return make_placeholder(m.group(0))

    source = re.sub(r"#龍芯⚡️[^\s]*", protect_dna, source)
    source = re.sub(r"#CONFIRM[^\s]*", protect_dna, source)
    source = re.sub(r"#ZHUGEXIN[^\s]*", protect_dna, source)

    def transform_loop(m):
        expr = m.group(1).strip()
        return f"for __cnshexpr in range({expr}): {{"

    source = re.sub(
        r"(?<![\u4e00-\u9fa5A-Za-z0-9])循环\s*\(([^)]+)\)\s*\{", transform_loop, source
    )

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

    def replace_keyword(src, cn, py):
        pat = (
            r"(?<![\u4e00-\u9fa5A-Za-z0-9])"
            + re.escape(cn)
            + r"(?![\u4e00-\u9fa5A-Za-z0-9])"
        )
        return re.sub(pat, py, src)

    for cn, py in sorted(keywords, key=lambda x: len(x[0]), reverse=True):
        source = replace_keyword(source, cn, py)

    for key, val in placeholders.items():
        source = source.replace(key, val)

    raw_lines = source.splitlines()

    indent_stack = [0]
    virtual_lines = []
    for raw in raw_lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("##"):
            virtual_lines.append((raw, -1, stripped))
            continue

        close_count = 0
        tmp = stripped
        while tmp.endswith("}"):
            tmp = tmp[:-1].rstrip()
            close_count += 1

        open_count = 0
        tmp2 = tmp
        while tmp2.endswith("{"):
            tmp2 = tmp2[:-1].rstrip()
            open_count += 1

        for _ in range(close_count):
            if len(indent_stack) > 1:
                indent_stack.pop()

        base_indent = len(raw) - len(raw.lstrip())
        virtual_indent = indent_stack[-1] + base_indent

        if re.match(r"\s*(if|for|while|def|elif)\b", tmp2) and not tmp2.rstrip().endswith(":"):
            tmp2 = tmp2.rstrip() + ":"

        virtual_lines.append((" " * virtual_indent + tmp2, virtual_indent, tmp2))

        for _ in range(open_count):
            indent_stack.append(indent_stack[-1] + 4)

    py_lines = []
    block_indents = [-1]

    for raw, indent, stripped in virtual_lines:
        if indent == -1:
            py_lines.append(raw)
            continue

        if not stripped:
            continue

        if stripped.startswith("}"):
            stripped = stripped.lstrip("}").strip()
            if not stripped:
                continue

        if stripped.startswith("else") or stripped.startswith("elif"):
            if not stripped.endswith(":"):
                stripped += ":"
            if len(block_indents) > 1:
                block_indents.pop()
            logical_indent = len(block_indents) - 1
            py_lines.append("    " * logical_indent + stripped)
            block_indents.append(indent)
            continue

        while len(block_indents) > 1 and indent <= block_indents[-1]:
            block_indents.pop()

        logical_indent = len(block_indents) - 1
        py_lines.append("    " * logical_indent + stripped)

        if stripped.endswith(":"):
            block_indents.append(indent)

    cleaned_lines = [line for line in py_lines if line.strip()]

    return "\n".join(cleaned_lines)


def fix_print_calls(code: str) -> str:
    """修复 print"..." / print "..." 为 print(...)"""
    code = re.sub(r'print\s*"([^"]*)"', r'print("\1")', code)
    code = re.sub(r"print\s*'([^']*)'", r'print("\1")', code)
    return code


def fix_fstrings(code: str) -> str:
    """把 CNSH 的 print '{变量}' 转换为 Python f-string"""

    def make_fstring(m):
        inner = m.group(1)
        if re.search(r"\{[A-Za-z_\u4e00-\u9fa5][A-Za-z0-9_\u4e00-\u9fa5]*\}", inner):
            return f'print(f"{inner}")'
        return f'print("{inner}")'

    code = re.sub(r'print\("([^"]*)"\)', make_fstring, code)
    return code


def _exec_python_code(python_code: str, dry_run: bool = False, label: str = "", source: str = "") -> int:
    if dry_run:
        print(f"📝 生成的 Python 代码 ({label}):")
        print(python_code)
        return 0

    try:
        namespace = {"__name__": "__main__"}
        exec(python_code, namespace)
        if "主函数" in namespace and callable(namespace["主函数"]):
            namespace["主函数"]()
        print("-" * 40)
        print("✅ CNSH 脚本执行完成")
        return 0
    except Exception as e:
        if FriendlyErrorReporter is not None:
            reporter = FriendlyErrorReporter(source, python_code, "<cnshexec>")
            print(reporter.report_runtime(e))
        else:
            print(f"❌ 执行错误: {e}")
        print("\n生成的 Python 代码:")
        print(python_code)
        return 1


def run_cnsh_compiler(file_path: str, dry_run: bool = False) -> int:
    """使用完整 CNSH 编译器（lexer/parser/codegen）运行脚本"""
    p = Path(file_path)
    if not p.exists():
        print(f"❌ 文件不存在: {file_path}")
        return 1
    if compile_cnsh_safe is None:
        print("⚠️ 编译器未加载，退回正则翻译器")
        return run_cnsh_legacy(file_path, dry_run=dry_run)

    source = p.read_text(encoding="utf-8", errors="ignore")
    print(f"🐉 运行 CNSH 脚本（编译器模式）: {p.name}")
    print("-" * 40)

    ok, result, err_type = compile_cnsh_safe(source)
    if not ok:
        print(f"⚠️ 编译器 {err_type} 阶段失败: {result}")
        print("🔄 自动退回正则翻译器执行...\n")
        return run_cnsh_legacy(file_path, dry_run=dry_run)

    return _exec_python_code(result, dry_run=dry_run, label="编译器", source=source)


def run_cnsh_legacy(file_path: str, dry_run: bool = False) -> int:
    """使用原有正则翻译器运行脚本"""
    p = Path(file_path)
    if not p.exists():
        print(f"❌ 文件不存在: {file_path}")
        return 1

    source = p.read_text(encoding="utf-8", errors="ignore")
    print(f"🐉 运行 CNSH 脚本（兼容模式）: {p.name}")
    print("-" * 40)

    python_code = translate_cnsh_to_python(source)
    python_code = fix_print_calls(python_code)
    python_code = fix_fstrings(python_code)

    return _exec_python_code(python_code, dry_run=dry_run, label="兼容模式", source=source)


def run_cnsh(file_path: str, dry_run: bool = False, use_compiler: bool = True) -> int:
    """运行 CNSH 脚本，默认使用完整编译器，失败自动退回正则翻译器"""
    if use_compiler:
        return run_cnsh_compiler(file_path, dry_run=dry_run)
    return run_cnsh_legacy(file_path, dry_run=dry_run)
