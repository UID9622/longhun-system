# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-REPAIR-FILE1-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
修复模板套用后的重复标题
DNA:#龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-REPAIR-FILE1-v1.0
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

    # 找到第一个 --- 分隔线（模板 metadata 结束）
    sep_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            sep_idx = i
            break
    if sep_idx == -1 or sep_idx + 1 >= len(lines):
        return False

    # 分隔线后跳过空行，看下一个非空行是否与标题相同
    j = sep_idx + 1
    while j < len(lines) and lines[j].strip() == '':
        j += 1
    if j < len(lines) and lines[j].strip() == first:
        # 删除插入的第一行标题及其后的空行
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
    print(f'已修复重复标题：{repaired} / {len(templated)}')


if __name__ == '__main__':
    main()
