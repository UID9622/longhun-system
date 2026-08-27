#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lh_google_audit.py — 去 Google 化审计扫描器
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""扫描源码中 google 域名/API/密钥调用，输出三色报告。"""

import json
import os
import re
import sys
from pathlib import Path

GOOGLE_DOMAINS = [
    'google.com', 'googleapis.com', 'gstatic.com', 'googlesource.com',
    'googleusercontent.com', 'google-analytics.com', 'googletagmanager.com',
    'googleadservices.com', 'doubleclick.net',
]
GOOGLE_API_PATTERNS = [
    r'AIza[0-9A-Za-z\-_]{35}',
    r'ya29\.[0-9A-Za-z\-_]+',
    r'client_id\s*[=:]\s*["\']?\d+-[0-9a-z]+\.apps\.googleusercontent',
]
SKIP_DIRS = {'out', 'node_modules', '.git', '.svn'}


def scan_source(src_dir, check_domains=True, check_apis=True,
                check_keys=True):
    src = Path(src_dir).expanduser().resolve()
    if not src.exists():
        return {'color': 'RED', 'error': 'dir not found: %s' % src,
                'counts': {}}

    domain_hits, api_hits, key_hits = [], [], []
    scanned = 0

    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(('.cc', '.h', '.py', '.js', '.ts',
                                   '.json', '.gn', '.gni', '.md',
                                   '.html', '.xml', '.java')):
                continue
            path = Path(root) / fname
            if '/out/' in str(path):
                continue
            try:
                text = path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            scanned += 1
            if check_domains:
                for dom in GOOGLE_DOMAINS:
                    if dom in text:
                        domain_hits.append('%s: %s' % (
                            path.relative_to(src), dom))
            if check_apis:
                for pat in GOOGLE_API_PATTERNS:
                    m = re.search(pat, text)
                    if m:
                        api_hits.append('%s: %s' % (
                            path.relative_to(src), m.group()[:20]))
            if check_keys:
                for kw in ['google_api_key', 'google_default_client_id',
                           'google_default_client_secret']:
                    if re.search(r'%s\s*=\s*["\'][^"\']+["\']' % kw, text):
                        key_hits.append('%s: %s' % (
                            path.relative_to(src), kw))

    counts = {
        'scanned_files': scanned,
        'domain_hits': len(set(domain_hits)),
        'api_hits': len(set(api_hits)),
        'key_hits': len(set(key_hits)),
    }
    total_bad = counts['domain_hits'] + counts['api_hits'] + counts['key_hits']
    if total_bad == 0:
        color = 'GREEN'
    elif total_bad <= 10:
        color = 'YELLOW'
    else:
        color = 'RED'
    return {
        'color': color,
        'counts': counts,
        'samples': (domain_hits[:5] + api_hits[:5] + key_hits[:5]),
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description='longhun google audit')
    ap.add_argument('--src', required=True)
    ap.add_argument('--check-domains', action='store_true', default=True)
    ap.add_argument('--check-apis', action='store_true', default=True)
    ap.add_argument('--check-keys', action='store_true', default=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    result = scan_source(args.src, args.check_domains,
                         args.check_apis, args.check_keys)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    counts = result['counts']
    print('[%s] google-audit' % result['color'])
    print('  scanned: %s' % counts.get('scanned_files', 0))
    print('  domains: %s' % counts.get('domain_hits', 0))
    print('  apis: %s' % counts.get('api_hits', 0))
    print('  keys: %s' % counts.get('key_hits', 0))
    for s in result.get('samples', [])[:10]:
        print('  sample: %s' % s)
    if result.get('error'):
        print('[RED] %s' % result['error'])
        sys.exit(2)
    if result['color'] != 'GREEN':
        sys.exit(1)


if __name__ == '__main__':
    main()
