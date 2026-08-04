#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️2026-06-21-ENGINE-DNA_PYTHON_FILLER-v1.0
# 文件名: dna_python_filler.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给未带 DNA 的 Python 脚本批量补充 DNA 追溯码。
跳过第三方、缓存、虚拟环境等目录。
"""
import os
import re
import hashlib
from pathlib import Path
from datetime import datetime

DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')
VALID_DNA_RE = re.compile(r'^#龍芯[\u26a1\ufe0f]*\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$')

IGNORE_DIR_NAMES = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'env', '.env',
                    '.pytest_cache', '.mypy_cache', 'dist', 'build', '.eggs', '.longhun',
                    '.agents', '.kimi-code', '.lmstudio', '.npm', '.nvm', '.cache', '.uv'}
IGNORE_PATH_PARTS = {'site-packages', '/venv', 'virtualenv', 'lib/python'}


def should_ignore(path: Path) -> bool:
    text = str(path).lower()
    for part in IGNORE_PATH_PARTS:
        if part in text:
            return True
    for part in path.parts:
        if part in IGNORE_DIR_NAMES:
            return True
    return False


def collect_existing_dnas(root: Path) -> set[str]:
    dnas = set()
    for path in root.rglob('*.py'):
        if should_ignore(path):
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


def make_dna(module: str, used: set[str]) -> str:
    date_str = datetime.now().strftime('%Y-%m-%d')
    base = f'#龍芯⚡️{date_str}-ENGINE-{module}-v1.0'
    if base not in used:
        used.add(base)
        return base
    counter = 0
    while True:
        counter += 1
        suffix = hashlib.md5(f'{module}:{counter}'.encode()).hexdigest()[:4].upper()
        candidate = f'#龍芯⚡️{date_str}-ENGINE-{module}_{suffix}-v1.0'
        if candidate not in used:
            used.add(candidate)
            return candidate


def add_dna_to_python(root_dir: str, dry_run: bool = True, max_files: int = 0):
    root = Path(root_dir).resolve()
    used = collect_existing_dnas(root)
    stats = {'scanned': 0, 'has_dna': 0, 'added': 0, 'skipped': 0, 'errors': 0}
    changes = []

    for path in root.rglob('*.py'):
        if should_ignore(path):
            continue
        stats['scanned'] += 1
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            stats['errors'] += 1
            continue

        if DNA_RE.search(text):
            stats['has_dna'] += 1
            continue

        if max_files > 0 and stats['added'] >= max_files:
            stats['skipped'] += 1
            continue

        module = normalize_module(path.stem)
        dna = make_dna(module, used)
        rel = str(path.relative_to(root))

        # 在文件头部插入 DNA 注释
        new_text = f'# {dna}\n# 文件名: {path.name}\n\n{text}'

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
    parser = argparse.ArgumentParser(description='Python 脚本 DNA 填充器')
    parser.add_argument('root', default='.', nargs='?', help='项目根目录')
    parser.add_argument('--执行', action='store_true', help='实际执行')
    parser.add_argument('--最大数量', type=int, default=0, help='最大填充数量 (0=无限制)')
    parser.add_argument('-o', '--输出', help='变更报告输出路径')
    args = parser.parse_args()

    dry_run = not args.执行
    stats, changes = add_dna_to_python(args.root, dry_run=dry_run, max_files=args.最大数量)

    mode = '模拟' if dry_run else '实际'
    print(f'🐉 Python DNA 填充器 ({mode}模式)')
    print(f'   扫描: {stats["scanned"]}')
    print(f'   已有 DNA: {stats["has_dna"]}')
    print(f'   {"待填充" if dry_run else "已填充"}: {stats["added"]}')
    print(f'   跳过/限制: {stats["skipped"]}')
    print(f'   错误/权限: {stats["errors"]}')

    if changes:
        print(f'\n前 20 条:')
        for c in changes[:20]:
            print(f'  {c["path"]} -> {c["dna"]}')

    if args.输出:
        lines = [f'# Python DNA 填充报告 ({mode})', f'扫描: {stats["scanned"]}', f'已有: {stats["has_dna"]}', f'填充: {stats["added"]}', '']
        lines.append('| 文件 | DNA |')
        lines.append('|------|-----|')
        for c in changes:
            lines.append(f'| {c["path"]} | `{c["dna"]}` |')
        Path(args.输出).write_text('\n'.join(lines), encoding='utf-8')
        print(f'\n报告已保存: {args.输出}')
