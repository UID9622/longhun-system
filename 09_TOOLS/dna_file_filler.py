#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️2026-06-21-ENGINE-DNA_FILE_FILLER-v1.0
# 文件名: dna_file_filler.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给项目内合理文件批量补充 DNA 追溯码。
跳过第三方、缓存、虚拟环境、二进制、日志、环境配置等。
"""
import os
import re
import hashlib
from pathlib import Path
from datetime import datetime

DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')

IGNORE_DIR_NAMES = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'env', '.env',
                    '.pytest_cache', '.mypy_cache', 'dist', 'build', '.eggs', '.longhun',
                    '.agents', '.kimi-code', '.lmstudio', '.npm', '.nvm', '.cache', '.uv',
                    '.playwright-mcp', '.obsidian', '.claude', '.backups', '.github'}
IGNORE_PATH_PARTS = {'site-packages', '/venv', 'virtualenv', 'lib/python', '/.cache/',
                     'releases/v5.1/staging/baobao-guardian/backend/venv',
                     'cnsh-core/ai-tools/operation_log_engine/venv_notion'}

# 允许处理的扩展名（文本/项目文件）
ALLOWED_EXTS = {'.md', '.json', '.txt', '.cnsh', '.bak', '.yml', '.yaml', '.toml', '.rst',
                '.js', '.ts', '.html', '.css', '.sh', '.fish', '.csh', '.ps1'}
# 无扩展名但可处理的白名单文件名
ALLOWED_NOEXT_NAMES = {'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'Makefile',
                       'Dockerfile', 'requirements', 'Pipfile', ' Brewfile'}

PREFIX_MAP = {
    '.md': 'DOC', '.json': 'CONFIG', '.txt': 'TEXT', '.cnsh': 'CNSH',
    '.bak': 'ARCHIVE', '.yml': 'CONFIG', '.yaml': 'CONFIG', '.toml': 'CONFIG',
    '.rst': 'DOC', '.js': 'UI', '.ts': 'UI', '.html': 'UI', '.css': 'UI',
    '.sh': 'TOOL', '.fish': 'TOOL', '.csh': 'TOOL', '.ps1': 'TOOL',
}


def should_ignore(path: Path) -> bool:
    text = str(path).lower()
    for part in IGNORE_PATH_PARTS:
        if part.lower() in text:
            return True
    for part in path.parts:
        if part in IGNORE_DIR_NAMES:
            return True
    return False


def collect_existing_dnas(root: Path) -> set[str]:
    dnas = set()
    for path in root.rglob('*'):
        if not path.is_file() or should_ignore(path):
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for m in DNA_RE.finditer(text):
            body = m.group(0)
            body = body[1:] if body and body[0] in ' \t"\'' else body
            dnas.add(body)
    return dnas


def normalize_module(name: str) -> str:
    module = re.sub(r'[^A-Z0-9_-]+', '_', name.upper()).strip('_')
    if not module or not module[0].isalpha():
        module = 'MOD_' + module if module else 'FILE'
    return module[:60]


def make_dna(prefix: str, module: str, used: set[str]) -> str:
    date_str = datetime.now().strftime('%Y-%m-%d')
    base = f'#龍芯⚡️{date_str}-{prefix}-{module}-v1.0'
    if base not in used:
        used.add(base)
        return base
    counter = 0
    while True:
        counter += 1
        suffix = hashlib.md5(f'{prefix}:{module}:{counter}'.encode()).hexdigest()[:4].upper()
        candidate = f'#龍芯⚡️{date_str}-{prefix}-{module}_{suffix}-v1.0'
        if candidate not in used:
            used.add(candidate)
            return candidate


def get_comment_prefix(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {'.sh', '.fish', '.csh', '.yaml', '.yml', '.toml', '.cnsh'}:
        return '# '
    if ext in {'.md', '.txt', '.rst', '.bak', ''}:
        return ''
    if ext == '.json':
        return ''  # JSON 不插入注释，放在值里
    if ext in {'.js', '.ts', '.css', '.html'}:
        return '// '
    return '# '


def insert_dna(text: str, dna: str, path: Path) -> str:
    ext = path.suffix.lower()
    comment = get_comment_prefix(path)
    if ext == '.json':
        # 在 JSON 顶部插入一个带 DNA 的伪字段
        stripped = text.lstrip()
        if stripped.startswith('{'):
            return '{"_dna": "' + dna + '",\n' + stripped[1:]
        if stripped.startswith('['):
            return '[\n{"_dna": "' + dna + '"},' + stripped[1:]
        return dna + '\n' + text
    if comment:
        return comment + dna + '\n' + text
    return dna + '\n' + text


def add_dna_to_files(root_dir: str, dry_run: bool = True, max_files: int = 0):
    root = Path(root_dir).resolve()
    used = collect_existing_dnas(root)
    stats = {'scanned': 0, 'has_dna': 0, 'added': 0, 'skipped': 0, 'ignored': 0, 'errors': 0}
    changes = []

    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if should_ignore(path):
            stats['ignored'] += 1
            continue

        ext = path.suffix.lower()
        name = path.name
        is_allowed = (ext in ALLOWED_EXTS or
                      (not ext and name.split('.')[0].upper() in {n.upper() for n in ALLOWED_NOEXT_NAMES}))
        if not is_allowed:
            stats['ignored'] += 1
            continue

        stats['scanned'] += 1
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            stats['errors'] += 1
            continue

        if DNA_RE.search(text):
            stats['has_dna'] += 1
            continue

        if max_files > 0 and stats['added'] >= max_files:
            stats['skipped'] += 1
            continue

        prefix = PREFIX_MAP.get(ext, 'FILE')
        module = normalize_module(path.stem)
        dna = make_dna(prefix, module, used)
        rel = str(path.relative_to(root))
        new_text = insert_dna(text, dna, path)

        if not dry_run:
            try:
                path.write_text(new_text, encoding='utf-8')
                stats['added'] += 1
            except PermissionError:
                stats['errors'] += 1
                continue
        else:
            stats['added'] += 1

        changes.append({'path': rel, 'dna': dna})

    return stats, changes


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='项目文件 DNA 填充器')
    parser.add_argument('root', default='.', nargs='?', help='项目根目录')
    parser.add_argument('--执行', action='store_true', help='实际执行')
    parser.add_argument('--最大数量', type=int, default=0, help='最大填充数量')
    parser.add_argument('-o', '--输出', help='变更报告路径')
    args = parser.parse_args()

    dry_run = not args.执行
    stats, changes = add_dna_to_files(args.root, dry_run=dry_run, max_files=args.最大数量)

    mode = '模拟' if dry_run else '实际'
    print(f'🐉 文件 DNA 填充器 ({mode}模式)')
    print(f'   扫描: {stats["scanned"]}  忽略: {stats["ignored"]}')
    print(f'   已有 DNA: {stats["has_dna"]}')
    print(f'   {"待填充" if dry_run else "已填充"}: {stats["added"]}')
    print(f'   跳过/限制: {stats["skipped"]}')
    print(f'   错误/权限: {stats["errors"]}')

    if changes:
        print(f'\n前 20 条:')
        for c in changes[:20]:
            print(f'  {c["path"]} -> {c["dna"]}')

    if args.输出:
        lines = [f'# 文件 DNA 填充报告 ({mode})',
                 f'扫描: {stats["scanned"]}  忽略: {stats["ignored"]}',
                 f'已有: {stats["has_dna"]}  填充: {stats["added"]}', '']
        lines.append('| 文件 | DNA |')
        lines.append('|------|-----|')
        for c in changes:
            lines.append(f'| {c["path"]} | `{c["dna"]}` |')
        Path(args.输出).write_text('\n'.join(lines), encoding='utf-8')
        print(f'\n报告已保存: {args.输出}')
