#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復模板套用後的重複標題
DNA: #龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-REPAIR-v1.0
"""

import json
from pathlib import Path

PROJECT_ROOT = Path('/Users/zuimeidedeyihan/longhun-system')
REGISTRY = PROJECT_ROOT / 'docs/契约矩阵/龍魂文档标准化登记册.json'


def repair(path: Path) -> bool:
    content = path.read_text(encoding='utf-8')
    lines = content.splitlines(keepends=True)
    if not lines:
        return False
    first = lines[0].strip()
    if not first.startswith('# '):
        return False
    title = first[2:].strip()

    # 找到第一個 --- 分隔線（模板 metadata 結束）
    sep_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            sep_idx = i
            break
    if sep_idx == -1 or sep_idx + 1 >= len(lines):
        return False

    # 分隔線後跳過空行，看下一個非空行是否與標題相同
    j = sep_idx + 1
    while j < len(lines) and lines[j].strip() == '':
        j += 1
    if j < len(lines) and lines[j].strip() == first:
        # 刪除插入的第一行標題及其後的空行
        del lines[0]
        if lines and lines[0].strip() == '':
            del lines[0]
        path.write_text(''.join(lines), encoding='utf-8')
        return True
    return False


def main():
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    templated = registry.get('templated', [])
    repaired = 0
    for item in templated:
        rel = item['file']
        path = PROJECT_ROOT / rel
        if path.exists() and repair(path):
            repaired += 1
    print(f'已修復重複標題：{repaired} / {len(templated)}')


if __name__ == '__main__':
    main()
