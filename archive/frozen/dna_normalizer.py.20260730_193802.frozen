# -*- coding: utf-8 -*-
# #龍芯⚡️2026-06-21-ENGINE-DNA_NORMALIZER-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 规范化器：将项目内所有不符合 #龍芯⚡️YYYY-MM-DD-MODULE-vX.X 格式的 DNA 追溯码
统一转换为机器可读、唯一、大写 ASCII 格式，并修复重复 DNA。
"""
import os
import re
import hashlib
from pathlib import Path
from datetime import datetime

DNA_RE = re.compile(r'[\s"\']?#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')
VALID_MODULE_RE = re.compile(r'^[A-Z][A-Z0-9_-]*$')
VALID_DNA_RE = re.compile(r'^#龍芯[\u26a1\ufe0f]*\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$')

IGNORE_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'env', '.env',
               '.pytest_cache', '.mypy_cache', 'dist', 'build', '.eggs', '.longhun'}
IGNORE_EXTS = {'.pyc', '.pyo', '.so', '.dylib', '.dll', '.min.js', '.min.css', '.map',
               '.DS_Store', '.lock', '.log', '.tmp', '.temp', '.png', '.jpg', '.jpeg',
               '.gif', '.ico', '.svg', '.mp4', '.mp3', '.wav', '.pdf', '.zip', '.tar.gz',
               '.gz', '.rar', '.7z', '.exe', '.bin', '.dat', '.db', '.sqlite', '.sqlite3'}

def normalize_module(module_part: str, fallback: str, fallback_dir: str = '') -> str:
    """将模块名规范化为大写 ASCII [A-Z0-9_-]"""
    module = module_part.upper()
    # 如果时间混入模块（如 22:57-XXX），去掉时间前缀
    module = re.sub(r'^(\d{1,2}:\d{2}(_\d{1,2}:\d{2})?)-?', '', module)
    # 将非合法字符替换为下划线
    module = re.sub(r'[^A-Z0-9_-]+', '_', module)
    # 去掉连续下划线和首尾下划线
    module = re.sub(r'_+', '_', module).strip('_-')
    # 如果模块为空或只是占位符，回退到文件名
    if not module or module in ('MOD', 'MODULE', 'UNNAMED') or not re.search(r'[A-Z]', module):
        base = re.sub(r'[^A-Z0-9_-]+', '_', Path(fallback).stem.upper()).strip('_')
        if not base and fallback_dir:
            base = re.sub(r'[^A-Z0-9_-]+', '_', fallback_dir.upper()).strip('_')
        module = base if base else 'FILE'
    # 确保以字母开头
    if not module[0].isalpha():
        module = 'MOD_' + module
    # 限制长度
    module = module[:80]
    return module

def make_dna(date_str: str, module: str, version: str) -> str:
    return f'#龍芯⚡️{date_str}-{module}-v{version}'

def collect_valid_dnas(root: Path) -> set[str]:
    valid = set()
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() in IGNORE_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for m in DNA_RE.finditer(text):
            full = m.group(0)
            dna = full[1:] if full and full[0] in ' \t"\'' else full
            if VALID_DNA_RE.match(dna):
                valid.add(dna)
    return valid

def scan_and_normalize(root_dir: str, dry_run: bool = True):
    root = Path(root_dir).resolve()
    seen_dnas = collect_valid_dnas(root)
    changes = []
    stats = {'scanned': 0, 'valid': 0, 'invalid': 0, 'nodna': 0, 'fixed': 0, 'skipped': 0}

    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() in IGNORE_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        stats['scanned'] += 1
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            stats['skipped'] += 1
            continue

        matches = list(DNA_RE.finditer(text))
        if not matches:
            stats['nodna'] += 1
            continue

        replacements = {}
        file_has_invalid = False
        for match in matches:
            full = match.group(0)
            # 拆分前导空白/引号与 DNA 主体
            leading_ws = ''
            leading_quote = ''
            if full and full[0] in ' \t\n\r':
                leading_ws = full[0]
                dna_body = full.lstrip(' \t\n\r')
            elif full and full[0] in '"\'':
                leading_quote = full[0]
                dna_body = full[1:]
            else:
                dna_body = full

            body_valid = bool(VALID_DNA_RE.match(dna_body))
            full_already_valid = full == dna_body and body_valid

            if full_already_valid:
                continue

            file_has_invalid = True
            if full in replacements:
                continue

            if body_valid:
                # 仅需要去掉前导空白；保留引号（JSON/字符串场景）
                new_dna_body = dna_body
            else:
                date_str = match.group(1)
                module_raw = match.group(2)
                version = match.group(3)
                module = normalize_module(module_raw, path.stem, path.parent.name)
                new_dna_body = make_dna(date_str, module, version)
                counter = 0
                base_module = module
                while new_dna_body in seen_dnas:
                    counter += 1
                    suffix = hashlib.md5(f"{path}:{full}:{counter}".encode()).hexdigest()[:4].upper()
                    module = f"{base_module}_{suffix}"
                    new_dna_body = make_dna(date_str, module, version)
                seen_dnas.add(new_dna_body)

            # 输出：去掉空白，保留引号（因为 JSON 需要引号包裹字符串）
            replacements[full] = leading_quote + new_dna_body

        if not file_has_invalid:
            stats['valid'] += 1
            continue

        stats['invalid'] += 1
        for old, new in replacements.items():
            changes.append({'path': str(path.relative_to(root)), 'old': old, 'new': new})

        if not dry_run and replacements:
            new_text = text
            for old, new in replacements.items():
                new_text = new_text.replace(old, new)
            try:
                path.write_text(new_text, encoding='utf-8')
                stats['fixed'] += 1
            except PermissionError:
                stats['skipped'] += 1
                for c in changes[-len(replacements):]:
                    c['status'] = '权限拒绝'
                continue

    return stats, changes

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='DNA 规范化器')
    parser.add_argument('root', default='.', nargs='?', help='项目根目录')
    parser.add_argument('--执行', action='store_true', help='实际执行修改（默认模拟）')
    parser.add_argument('-o', '--输出', help='变更报告输出路径')
    args = parser.parse_args()

    dry_run = not args.执行
    stats, changes = scan_and_normalize(args.root, dry_run=dry_run)

    mode = '模拟' if dry_run else '实际'
    print(f'🐉 DNA 规范化器 ({mode}模式)')
    print(f'   扫描: {stats["scanned"]}')
    print(f'   已规范: {stats["valid"]}')
    print(f'   待规范: {stats["invalid"]}')
    print(f'   无 DNA: {stats["nodna"]}')
    print(f'   跳过: {stats["skipped"]}')
    if not dry_run:
        print(f'   已修复: {stats["fixed"]}')

    if changes:
        print(f'\n前 20 条变更示例:')
        for c in changes[:20]:
            print(f'  {c["path"]}')
            print(f'    {c["old"]}')
            print(f'    → {c["new"]}')

    if args.输出:
        report = []
        report.append('# DNA 规范化变更报告')
        report.append(f'- 模式: {mode}')
        report.append(f'- 扫描文件: {stats["scanned"]}')
        report.append(f'- 待规范: {len(changes)}')
        report.append('')
        report.append('| 文件 | 旧 DNA | 新 DNA |')
        report.append('|------|--------|--------|')
        for c in changes:
            report.append(f'| {c["path"]} | `{c["old"]}` | `{c["new"]}` |')
        Path(args.输出).write_text('\n'.join(report), encoding='utf-8')
        print(f'\n报告已保存: {args.输出}')
