#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lh_browser_audit_middleware.py — 浏览器操作三色审计中间件
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 原则: 审计记录只写本地，永不上报
"""浏览器操作三色审计中间件。每次关键操作自动触发，本地DNA链记录。"""

import hashlib
import json
import os
import sqlite3
import time

RED_VETO_ACTIONS = [
    'upload_to_external',
    'send_telemetry',
    'access_user_keychain',
    'read_private_keys',
    'modify_hosts_file',
    'disable_audit',
]


def tri_color_audit(impact, uncertainty, boundary):
    """三色判定: 红>60 / 黄>25 / 绿其余。Risk=影响x不确定x越界。"""
    risk = float(impact) * float(uncertainty) * float(boundary)
    if risk >= 60:
        return ('RED', round(risk, 2))
    if risk >= 25:
        return ('YELLOW', round(risk, 2))
    return ('GREEN', round(risk, 2))


class BrowserAuditMiddleware:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser(
            '~/.longhun-browser/audit/dna_chain.sqlite')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS dna_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_hash TEXT,
            action TEXT,
            color TEXT,
            risk REAL,
            desc TEXT,
            ts REAL,
            uid TEXT,
            hash TEXT UNIQUE
        )''')
        conn.commit()
        conn.close()

    def _get_last_hash(self):
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            'SELECT hash FROM dna_chain ORDER BY id DESC LIMIT 1').fetchone()
        conn.close()
        return row[0] if row else 'GENESIS-LONGHUN'

    def _write_local(self, entry, child_hash):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            'INSERT OR REPLACE INTO dna_chain '
            '(parent_hash, action, color, risk, desc, ts, uid, hash) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (entry['parent_hash'], entry['action'], entry['color'],
             entry['risk'], entry['desc'], entry['ts'],
             entry['uid'], child_hash))
        conn.commit()
        conn.close()

    def audit(self, action, context=None):
        context = context or {}
        if action in RED_VETO_ACTIONS:
            self._log_dna(action, 'RED', 999, 'veto')
            return ('RED', 999, False)
        impact = float(context.get('impact', 1))
        uncertainty = float(context.get('uncertainty', 1))
        boundary = float(context.get('boundary_cross', 1))
        color, risk = tri_color_audit(impact, uncertainty, boundary)
        executable = color != 'RED'
        self._log_dna(action, color, risk, context.get('description', ''))
        return (color, risk, executable)

    def _log_dna(self, action, color, risk, desc):
        entry = {
            'action': action, 'color': color, 'risk': float(risk),
            'desc': desc, 'ts': time.time(), 'uid': 'local_only',
        }
        parent_hash = self._get_last_hash()
        payload = json.dumps(
            {k: v for k, v in entry.items()},
            sort_keys=True, ensure_ascii=False)
        entry['parent_hash'] = parent_hash
        child_hash = hashlib.sha256(
            (parent_hash + payload).encode()).hexdigest()
        self._write_local(entry, child_hash)

    def stats(self):
        conn = sqlite3.connect(self.db_path)
        total = conn.execute('SELECT COUNT(*) FROM dna_chain').fetchone()[0]
        green = conn.execute(
            "SELECT COUNT(*) FROM dna_chain WHERE color='GREEN'").fetchone()[0]
        yellow = conn.execute(
            "SELECT COUNT(*) FROM dna_chain WHERE color='YELLOW'").fetchone()[0]
        red = conn.execute(
            "SELECT COUNT(*) FROM dna_chain WHERE color='RED'").fetchone()[0]
        conn.close()
        return {'total': total, 'green': green, 'yellow': yellow,
                'red': red, 'external_requests': 0}

    def verify_chain(self):
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            'SELECT hash, parent_hash, action, color, risk, desc, ts, uid '
            'FROM dna_chain ORDER BY id').fetchall()
        conn.close()
        parent = 'GENESIS-LONGHUN'
        for (h, ph, action, color, risk, desc, ts, uid) in rows:
            payload = json.dumps(
                {'action': action, 'color': color, 'risk': risk,
                 'desc': desc, 'ts': ts, 'uid': uid},
                sort_keys=True, ensure_ascii=False)
            expect = hashlib.sha256(
                (parent + payload).encode()).hexdigest()
            if h != expect or ph != parent:
                return False
            parent = h
        return True


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='longhun browser audit middleware')
    ap.add_argument('--action', default='test_action')
    ap.add_argument('--impact', type=float, default=1)
    ap.add_argument('--uncertainty', type=float, default=1)
    ap.add_argument('--boundary', type=float, default=1)
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--stats', action='store_true')
    args = ap.parse_args()

    mw = BrowserAuditMiddleware()
    if args.verify:
        print('dna-chain:', 'OK' if mw.verify_chain() else 'BROKEN')
    elif args.stats:
        print(json.dumps(mw.stats(), ensure_ascii=False, indent=2))
    else:
        color, risk, ok = mw.audit(
            args.action,
            {'impact': args.impact, 'uncertainty': args.uncertainty,
             'boundary_cross': args.boundary})
        print(color, 'risk=%s' % risk, 'executable=%s' % ok)
