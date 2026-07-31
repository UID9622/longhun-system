# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·戊戌·☵坎-TYPE-FIXER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · basedpyright 类型批量自愈 v1.0                     ║
║                                                                  ║
║  自动扫描并修复 reportMissingTypeArgument 错误                  ║
║  dict → dict[str, Any]  /  list → list[Any]  /  set → set[Any]  ║
║                                                                  ║
║  DNA:  #龍芯⚡️丙午·乙未·戊戌·☵坎-TYPE-FIXER-v1.0               ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_type_fixer.py            # 预览（不修改文件）
  python3 bin/lh_type_fixer.py --apply    # 执行修复
  python3 bin/lh_type_fixer.py --dry-run  # 仅显示会修改什么
  python3 bin/lh_type_fixer.py --target bin/lh_xxx.py  # 指定文件
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any


ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·乙未·戊戌·☵坎-TYPE-FIXER-v1.0"

# 跳过目录
SKIP_DIRS = {
    '__pycache__', '.git', 'venv', '.venv', '.venvs', '.venv_longhun_math', '.venv_docs',
    'node_modules', 'dist',
    'backups', '_archive', '_archived_reports', 'logs', 'logging_backup',
    'tmp', 'var', 'data', 'outputs', 'releases',
    'extensions', 'imports', 'integrated_modules', 'integrated-modules',
    'vector_db', 'vault', 'tombstone_vault', '_private',
    '.obsidian', 'memory-universe', 'brain',
    'L7_数据层', '_downloads_staging', 'downloads_archive',
}

# 裸类型 → 修复映射
BARE_TYPE_MAP: Dict[str, str] = {
    'dict': 'dict[str, Any]',
    'list': 'list[Any]',
    'tuple': 'tuple[Any, ...]',
    'set': 'set[Any]',
    'frozenset': 'frozenset[Any]',
}

# 需要添加 from __future__ import annotations 的信号模式
FUTURE_IMPORT = 'from __future__ import annotations\n'

# 需要在 typing 中添加 Any 的 signal
ANY_IMPORT_PATTERNS = [
    re.compile(r'from typing import (.+?)\n'),
    re.compile(r'from typing import (.+?)$'),
]


# ═══════════════════════════════════════════════
# AST 分析器
# ═══════════════════════════════════════════════

class TypeAnnotationVisitor(ast.NodeVisitor):
    """遍历 AST，找到所有裸类型注解"""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.issues: List[Dict[str, Any]] = []  # [{line, col, bare_type, suggested}]

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # 检查参数类型注解
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            if arg.annotation:
                self._check_annotation_node(arg.annotation)
        # 检查返回类型
        if node.returns:
            self._check_annotation_node(node.returns)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node.annotation:
            self._check_annotation_node(node.annotation)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        # 检查 subscript 内的类型（如 Dict[str, dict]）
        self._check_annotation_node(node.slice)
        self.generic_visit(node)

    def _check_annotation_node(self, node: ast.AST):
        """检查单个注解节点是否为裸类型"""
        if isinstance(node, ast.Name):
            bare = node.id
            if bare in BARE_TYPE_MAP:
                self.issues.append({
                    'line': node.lineno,
                    'col': node.col_offset,
                    'bare_type': bare,
                    'suggested': BARE_TYPE_MAP[bare],
                })
        elif isinstance(node, ast.Tuple):
            for elt in node.elts:
                self._check_annotation_node(elt)


# ═══════════════════════════════════════════════
# 修复引擎
# ═══════════════════════════════════════════════

def find_python_files(root: Path, target: str | None = None) -> List[Path]:
    """找出所有需扫描的 .py 文件"""
    if target:
        p = Path(target)
        return [p] if p.exists() and p.suffix == '.py' else []

    files = []
    for py_file in root.rglob('*.py'):
        parts = py_file.relative_to(root).parts
        if any(d in SKIP_DIRS for d in parts):
            continue
        files.append(py_file)
    return files


def analyze_file(filepath: Path) -> List[Dict[str, Any]]:
    """分析单个文件，返回裸类型注解列表"""
    try:
        source = filepath.read_text(encoding='utf-8')
    except Exception:
        return []

    try:
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, RecursionError):
        return []

    lines = source.splitlines()
    visitor = TypeAnnotationVisitor(lines)
    visitor.visit(tree)
    return visitor.issues


def fix_file(filepath: Path, issues: List[Dict[str, Any]], apply: bool = False) -> str:
    """修复文件中的裸类型注解，返回 diff 描述"""
    source = filepath.read_text(encoding='utf-8')
    lines = source.split('\n')
    modified = False
    needs_any_import = False
    needs_annotations_import = False
    report_lines: List[str] = []

    # 从后往前处理，避免行号偏移
    sorted_issues = sorted(issues, key=lambda x: (-x['line'], -x['col']))

    for issue in sorted_issues:
        line_idx = issue['line'] - 1
        if line_idx >= len(lines):
            continue
        line = lines[line_idx]

        # 只在类型注解位置替换（避免替换注释/字符串中的字面量）
        # 策略：整行扫描，在裸类型出现的位置做替换
        bare = issue['bare_type']
        suggested = issue['suggested']

        # 用正则精确匹配类型注解中的裸类型（跟在 : 或 -> 或 [ 后）
        # 匹配模式: 前面是空格/: 后面是空格/,/)/-
        col = issue['col']
        before = line[:col]
        at_bare = line[col:col + len(bare)]
        after = line[col + len(bare):]

        if at_bare == bare:
            # 确认边界（前后都不是字母/数字）
            before_ok = not before or not before[-1].isalnum()
            after_ok = not after or not after[0].isalnum()
            if before_ok and after_ok:
                line = before + suggested + after
                lines[line_idx] = line
                modified = True
                needs_any_import = True
                report_lines.append(f"  L{issue['line']}: {bare} → {suggested}")

    if not modified:
        return ''

    # 检查是否需要添加 from __future__ import annotations
    has_future = any('from __future__ import annotations' in l for l in lines)
    if not has_future and needs_any_import:
        needs_annotations_import = True
        # 找到第一个非注释/非空行，在上面插入
        insert_pos = 0
        for i, l in enumerate(lines):
            stripped = l.strip()
            if stripped and not stripped.startswith('#!') and not stripped.startswith('# -*-'):
                # 跳过 encoding 声明和 shebang
                if stripped.startswith('#') and ('coding' in stripped or 'encoding' in stripped):
                    continue
                insert_pos = i
                break
        lines.insert(insert_pos, 'from __future__ import annotations')
        # 跳过可能紧接的空行
        report_lines.insert(0, '  + from __future__ import annotations')

    # 检查是否需要添加 Any 到 typing import
    if needs_any_import:
        has_any = any('Any' in re.findall(r'from typing import (.+)', l)[0] if re.findall(r'from typing import (.+)', l) else ''
                      for l in lines if 'from typing import' in l)
        if not has_any:
            for i, l in enumerate(lines):
                if 'from typing import' in l:
                    # 在该行末尾加 , Any
                    lines[i] = l.rstrip() + ', Any'
                    report_lines.append('  + Any (typing import)')
                    break

    new_source = '\n'.join(lines)
    if new_source.endswith('\n'):
        pass  # keep original ending style
    else:
        new_source += '\n'

    if apply:
        filepath.write_text(new_source, encoding='utf-8')

    return '\n'.join(report_lines)


# ═══════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════

def main():
    args = sys.argv[1:]
    apply_mode = '--apply' in args
    target_file = None

    for i, a in enumerate(args):
        if a in ('--target', '-t') and i + 1 < len(args):
            target_file = args[i + 1]
        elif a.startswith('--target='):
            target_file = a.split('=', 1)[1]

    files = find_python_files(ROOT, target_file)

    total_issues = 0
    total_fixed = 0

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🏥 龍魂 · basedpyright 类型自愈 v1.0                      ║
║  {DNA}
║  模式: {'🔧 执行修复' if apply_mode else '👀 预览（不修改文件）'}
║  文件: {len(files)} 个 .py
╚══════════════════════════════════════════════════════════════╝
""")

    for fp in files:
        issues = analyze_file(fp)
        if not issues:
            continue

        rel = fp.relative_to(ROOT)
        report = fix_file(fp, issues, apply=apply_mode)
        if report:
            total_issues += len(issues)
            total_fixed += 1
            print(f"📄 {rel}")
            print(report)
            print()

    print(f"{'═'*60}")
    if apply_mode:
        print(f"  ✅ 修复完成: {total_fixed} 文件 · {total_issues} 处类型注解")
    else:
        print(f"  👀 预览完成: {total_fixed} 文件 · {total_issues} 处待修复")
        if total_issues > 0:
            print(f"  💡 执行 'python3 bin/lh_type_fixer.py --apply' 来应用修复")
    print(f"{'═'*60}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
