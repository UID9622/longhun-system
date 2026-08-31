#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH DNA签名验证模块 v1.1
DNA: #龍芯⚡️2026-08-31-CNSH-DNA-VERIFY-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 验证所有进入龍魂系统的文件是否含有合法DNA签名
"""

import re
from pathlib import Path
from typing import Optional

# 标准DNA格式正则
# 格式：#龍芯⚡️{YYYY-MM-DD}-{项目段}-{版本号}-UID9622
DNA_PATTERN = re.compile(
    r'#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9_-]+-v\d+\.\d+-UID9622'
)

GPG_FINGERPRINT = 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'


def verify_dna_header(source: str) -> bool:
    """
    检查source中是否含有合法龍芯DNA签名。
    规则：前30行内必须出现至少一个符合格式的DNA标签。
    """
    lines = source.splitlines()[:30]
    header = '\n'.join(lines)
    return bool(DNA_PATTERN.search(header))


def verify_dna_file(filepath: str) -> dict:
    """校验文件DNA签名，返回详细结果"""
    path = Path(filepath)
    if not path.exists():
        return {'ok': False, 'reason': f'文件不存在: {filepath}'}
    source = path.read_text(encoding='utf-8')
    matches = DNA_PATTERN.findall(source)
    if not matches:
        return {
            'ok': False,
            'reason': '未找到合法龍芯DNA签名',
            'file': str(path),
            'hint': '格式: #龍芯⚡️YYYY-MM-DD-{项目}-{版本}-UID9622'
        }
    return {
        'ok': True,
        'file': str(path),
        'signatures': matches,
        'count': len(matches)
    }


def batch_verify(directory: str, suffix: str = '.py') -> list:
    """批量校验目录下所有文件"""
    results = []
    for fp in Path(directory).rglob(f'*{suffix}'):
        results.append(verify_dna_file(str(fp)))
    return results


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description='🐉 龍魂DNA签名验证器')
    parser.add_argument('target', help='文件或目录路径')
    parser.add_argument('--suffix', default='.py')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    target = Path(args.target)
    if target.is_dir():
        results = batch_verify(str(target), args.suffix)
        ok_count = sum(1 for r in results if r['ok'])
        fail_count = len(results) - ok_count
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                status = '✅' if r['ok'] else '❌'
                print(f"{status} {r.get('file', '?')}")
            print(f"\n总计: {ok_count}通过 / {fail_count}失败")
    else:
        r = verify_dna_file(str(target))
        print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else r)
