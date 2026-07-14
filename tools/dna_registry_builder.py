# #龍芯⚡️2026-06-21-ENGINE-DNA_REGISTRY_BUILDER-v1.0
# 文件名: dna_registry_builder.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DNA→权重/层级/状态 全局注册表生成器
扫描项目内所有带 DNA 标记的文件，按路径与类型分配层级、权重、状态，
生成统一注册表，供 lh6 status、审计器、路由系统调用。
"""
import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')
VALID_DNA_RE = re.compile(r'^#龍芯[\u26a1\ufe0f]*\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$')

IGNORE_DIR_EXACT = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'env',
                      '.env', '.pytest_cache', '.mypy_cache', 'dist', 'build',
                      '.eggs', '.longhun', '_archive', 'archive', 'archived',
                      '.backups', 'backups', 'backup', '.backup', 'old', '.old',
                      'legacy', 'deprecated', 'temp', '.temp', '.cache', '.uv',
                      '.npm', '.nvm', 'site-packages', '.obsidian', '.claude',
                      '.github'}
IGNORE_DIR_SUBSTR = {'venv', 'virtualenv', 'site-packages', 'backup', 'archive',
                     '.bak', 'deprecated', 'egg-info'}
IGNORE_EXTS = {'.pyc', '.pyo', '.so', '.dylib', '.dll', '.min.js', '.min.css', '.map',
               '.DS_Store', '.lock', '.log', '.tmp', '.temp', '.png', '.jpg', '.jpeg',
               '.gif', '.ico', '.svg', '.mp4', '.mp3', '.wav', '.pdf', '.zip', '.tar.gz',
               '.gz', '.rar', '.7z', '.exe', '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
               '.bak', '.backup', '.old', '.orig', '.rej', '.coverage', '.protocol_checksum'}

# 层级关键词映射（路径或模块名匹配）
LAYER_RULES = [
    ('L0_ETERNAL', ['constitution', 'protocol', 'rule', 'identity', 'permission', 'dna', 'logging', 'vault', 'charter']),
    ('L1_SEASONAL', ['compiler', 'lexer', 'parser', 'codegen', 'scheduler', 'rule_engine', 'mathematics', 'core']),
    ('L2_DECISION', ['flow_decision', 'router', 'gateway', 'persona', 'audit', 'sancai', 'wuxing', 'palace']),
    ('L3_GENERATIONAL', ['skill', 'tool', 'agent', 'launcher', 'editor', 'bridge', 'monitor', 'multimodal', 'vision', 'voice']),
    ('L4_INSTANT', ['report', 'summary', 'log', 'receipt', 'digest', 'status', 'readme', 'guide', 'quickstart']),
]

# 状态规则
STATUS_RULES = [
    ('🔴', ['_DEPRECATED', '_archive', 'backup', '.bak', 'old', 'temp']),
    ('🟡', ['staging', 'draft', 'wip', 'experiment', 'review']),
    ('🟢', []),  # 默认
]


def determine_layer(path: Path, module: str) -> str:
    text = (str(path) + ' ' + module).lower()
    for layer, keywords in LAYER_RULES:
        for kw in keywords:
            if kw in text:
                return layer
    return 'L3_GENERATIONAL'


def determine_status(path: Path) -> str:
    text = str(path).lower()
    for status, keywords in STATUS_RULES:
        for kw in keywords:
            if kw in text:
                return status
    return '🟢'


def priority_from_layer(layer: str) -> int:
    return {
        'L0_ETERNAL': 5,
        'L1_SEASONAL': 20,
        'L2_DECISION': 40,
        'L3_GENERATIONAL': 65,
        'L4_INSTANT': 90,
    }.get(layer, 65)


def weight_from_status(status: str) -> float:
    return {'🟢': 1.0, '🟡': 0.6, '🔴': 0.3}.get(status, 1.0)


def build_registry(root_dir: str, output_path: str):
    root = Path(root_dir).resolve()
    entries = []
    dna_index = {}
    stats = {'total': 0, 'valid_dna': 0, 'invalid_dna': 0, 'nodna': 0,
             'by_layer': {}, 'by_status': {}}

    IGNORE_NAMES = {'.gitignore', '.dockerignore', '.coverage', '.protocol_checksum',
                    '.editorconfig', '.gitattributes', '.prettierrc', '.eslintrc',
                    '.babelrc', '.nvmrc', '.python-version', '.tool-versions'}
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() in IGNORE_EXTS:
            continue
        name = path.name.lower()
        if name in IGNORE_NAMES or name.startswith('.env') or name == '.ds_store':
            continue
        parts = [p.lower() for p in path.parts]
        if any(p in IGNORE_DIR_EXACT for p in parts):
            continue
        if any(any(sub in p for sub in IGNORE_DIR_SUBSTR) for p in parts):
            continue
        stats['total'] += 1
        rel = str(path.relative_to(root))
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue

        matches = list(DNA_RE.finditer(text))
        if not matches:
            stats['nodna'] += 1
            continue

        # 取第一个 DNA 作为文件主 DNA
        first = matches[0]
        dna = first.group(0)
        dna_body = dna[1:] if dna and dna[0] in ' \t"\'' else dna
        date_str = first.group(1)
        module = first.group(2)
        version = first.group(3)
        valid = bool(VALID_DNA_RE.match(dna_body))

        if valid:
            stats['valid_dna'] += 1
        else:
            stats['invalid_dna'] += 1

        layer = determine_layer(path, module)
        status = determine_status(path)
        priority = priority_from_layer(layer)
        weight = round(priority * weight_from_status(status), 1)

        entry = {
            'file': rel,
            'dna': dna_body,
            'date': date_str,
            'module': module,
            'version': version,
            'valid': valid,
            'layer': layer,
            'status': status,
            'priority': priority,
            'weight': weight,
            'size': path.stat().st_size,
            'mtime': path.stat().st_mtime,
        }
        entries.append(entry)
        dna_index[dna_body] = entry

        stats['by_layer'][layer] = stats['by_layer'].get(layer, 0) + 1
        stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

    registry = {
        'generated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'root': str(root),
        'total_files': stats['total'],
        'registered_files': len(entries),
        'valid_dna': stats['valid_dna'],
        'invalid_dna': stats['invalid_dna'],
        'no_dna': stats['nodna'],
        'alignment_rate': round(stats['valid_dna'] / stats['total'] * 100, 1) if stats['total'] else 0,
        'by_layer': stats['by_layer'],
        'by_status': stats['by_status'],
        'entries': entries,
        'dna_index': dna_index,
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    return registry


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='DNA 全局注册表生成器')
    parser.add_argument('root', default='.', nargs='?', help='项目根目录')
    parser.add_argument('-o', '--输出', default='.longhun/dna-audit/dna_registry.json', help='输出 JSON 路径')
    args = parser.parse_args()

    reg = build_registry(args.root, args.输出)
    print(f'🐉 DNA 全局注册表已生成: {args.输出}')
    print(f'   扫描文件: {reg["total_files"]}')
    print(f'   已注册:   {reg["registered_files"]}')
    print(f'   有效 DNA: {reg["valid_dna"]}')
    print(f'   无效 DNA: {reg["invalid_dna"]}')
    print(f'   无 DNA:   {reg["no_dna"]}')
    print(f'   对齐率:   {reg["alignment_rate"]}%')
    print(f'   层级分布: {reg["by_layer"]}')
    print(f'   状态分布: {reg["by_status"]}')
