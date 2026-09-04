#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_dna_verify.py — DNA 追溯链完整性验证
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 验证浏览器本地 DNA 链哈希连续性
# ═══════════════════════════════════════════════════════════
"""验证本地 DNA 追溯链（链式 SHA-256）完整性，全程本地，零上报。"""

import json
import os
import sqlite3
import sys


def verify_chain(db_path: str) -> dict:
    db = os.path.expanduser(db_path)
    if not os.path.exists(db):
        return {'ok': False, 'reason': f'DNA 库不存在: {db}'}

    conn = sqlite3.connect(db)
    rows = conn.execute(
        'SELECT hash, parent_hash, action, color, risk, desc, ts, uid '
        'FROM dna_chain ORDER BY id').fetchall()
    conn.close()

    if not rows:
        return {'ok': True, 'records': 0, 'reason': '空链（合法起点）'}

    import hashlib
    parent = 'GENESIS-LONGHUN'
    for (h, ph, action, color, risk, desc, ts, uid) in rows:
        payload = json.dumps(
            {'action': action, 'color': color, 'risk': risk,
             'desc': desc, 'ts': ts, 'uid': uid},
            sort_keys=True, ensure_ascii=False)
        expect = hashlib.sha256(f"{parent}{payload}".encode()).hexdigest()
        if h != expect or ph != parent:
            return {'ok': False, 'records': len(rows),
                    'reason': f'链条断裂: action={action} hash={h[:12]}',
                    'expected': expect[:12]}
        parent = h
    return {'ok': True, 'records': len(rows), 'chain_head': parent[:16]}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='龍魂DNA追溯链验证')
    ap.add_argument('--log-dir', default='~/.longhun-browser/logs/',
                    help='日志目录（兼容健康检查脚本）')
    ap.add_argument('--db', default=None,
                    help='直接指定 sqlite 库路径')
    args = ap.parse_args()

    db = args.db or os.path.join(os.path.expanduser(args.log_dir),
                                 '..', 'audit', 'dna_chain.sqlite')
    r = verify_chain(db)
    if r.get('ok'):
        print(f"[🟢] DNA追溯链: 完整 ({r.get('records', 0)} 条记录)")
        if r.get('chain_head'):
            print(f"    链头: {r['chain_head']}")
        sys.exit(0)
    else:
        print(f"[🔴] DNA追溯链: 异常！{r.get('reason')}")
        sys.exit(1)
