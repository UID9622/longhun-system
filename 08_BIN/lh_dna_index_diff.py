#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·己亥·庚午·䷚颐-BIN-DNA_INDEX_DIFF-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·DNA注册表差异化刷新 v1.0
────────────────────────────
增量扫描：只处理自上次扫描后变动的文件，与现有注册表合并。
适用于频繁刷新场景，替代全量 lh_dna_index_fast.py 的高频调用。

用法:
  python3 bin/lh_dna_index_diff.py                      # 增量刷新
  python3 bin/lh_dna_index_diff.py --full               # 强制全量
  python3 bin/lh_dna_index_diff.py --since "2026-07-24"  # 指定时间起点
  python3 bin/lh_dna_index_diff.py --status             # 仅显示状态，不扫描

输出: 更新 .longhun/dna-audit/dna_registry.json
"""
import os, re, json, sys, time
from pathlib import Path
from datetime import datetime, timezone, timedelta

DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')

SKIP_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', '.longhun',
             '_archive', '.backups', 'backups', 'backup', '.backup',
             'old', '.old', 'legacy', 'temp', '.temp', '.cache', '.uv', '.npm',
             '.nvm', 'site-packages', '.obsidian', '.claude', '.github', 'data',
             'models', 'logs', 'dist', 'build', 'eggs', '.eggs', '.pytest_cache',
             '.mypy_cache'}

TEXT_EXTS = {'.py', '.md', '.json', '.html', '.js', '.css', '.yml', '.yaml',
             '.sh', '.toml', '.cfg', '.ini', '.xml', '.csv', '.tsv', '.rst',
             '.tex', '.bib', '.cnsh'}

LAYER_KEYWORDS = [
    ('L0_ETERNAL', ['constitution', 'protocol', 'rule', 'identity', 'permission', 'dna']),
    ('L1_SEASONAL', ['compiler', 'lexer', 'parser', 'scheduler', 'mathematics', 'core']),
    ('L2_DECISION', ['router', 'gateway', 'persona', 'audit', 'sancai', 'wuxing']),
    ('L3_GENERATIONAL', ['skill', 'tool', 'agent', 'bridge', 'monitor', 'engine']),
    ('L4_INSTANT', ['report', 'summary', 'log', 'receipt', 'guide', 'readme']),
]
PRIO = {'L0_ETERNAL': 5, 'L1_SEASONAL': 20, 'L2_DECISION': 40,
        'L3_GENERATIONAL': 65, 'L4_INSTANT': 90}
WS = {'🟢': 1.0, '🟡': 0.6, '🔴': 0.3}

STATE_FILE = '.longhun/dna-audit/.last_scan.json'


def determine_layer(path_str, module):
    text = (path_str + ' ' + module).lower()
    for layer, kws in LAYER_KEYWORDS:
        for kw in kws:
            if kw in text:
                return layer
    return 'L3_GENERATIONAL'


def determine_status(path_str):
    ps = path_str.lower()
    if any(kw in ps for kw in ['deprecated', 'backup', '.bak', '/old/', 'temp']):
        return '🔴'
    if any(kw in ps for kw in ['staging', 'draft', 'wip', 'experimental']):
        return '🟡'
    return '🟢'


def load_last_scan_state(project_root):
    """加载上次扫描状态"""
    sf = project_root / STATE_FILE
    if sf.exists():
        with open(sf) as f:
            return json.load(f)
    return {'last_scan_ts': 0, 'total_files': 0}


def save_scan_state(project_root, state):
    """保存扫描状态"""
    sf = project_root / STATE_FILE
    sf.parent.mkdir(parents=True, exist_ok=True)
    with open(sf, 'w') as f:
        json.dump(state, f, indent=2)


def scan_file(fpath, rel):
    """扫描单个文件，返回 entry 或 None"""
    ext = os.path.splitext(fpath)[1].lower()
    if ext not in TEXT_EXTS:
        return None
    fname = os.path.basename(fpath)
    if fname.startswith('.env') or fname in {'.gitignore', '.dockerignore', '.editorconfig'}:
        return None

    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            head = f.read(2048)
    except Exception:
        return None

    m = DNA_RE.search(head)
    if not m:
        return None

    dna_raw = m.group(0).strip()
    dna = dna_raw[1:] if dna_raw and dna_raw[0] in ' \t"\'' else dna_raw
    date_str = m.group(1)
    module = m.group(2)
    version = m.group(3)
    valid = dna.startswith('#龍芯⚡️') or dna.startswith('#龍芯')

    layer = determine_layer(rel, module)
    status = determine_status(rel)
    priority = PRIO.get(layer, 65)
    weight = round(priority * WS.get(status, 1.0), 1)

    return {
        'file': rel, 'dna': dna, 'date': date_str,
        'module': module, 'version': version, 'valid': valid,
        'layer': layer, 'status': status,
        'priority': priority, 'weight': weight,
        'mtime': os.path.getmtime(fpath) if os.path.exists(fpath) else 0,
    }


def incremental_scan(project_root, registry_path, since_ts=None, force_full=False):
    """增量扫描"""
    t0 = time.time()
    root = str(project_root)

    # 加载已有注册表
    existing = {}
    if registry_path.exists() and not force_full:
        with open(registry_path) as f:
            old = json.load(f)
        for e in old.get('entries', []):
            existing[e['file']] = e

    # 确定扫描起点
    state = load_last_scan_state(project_root)
    if since_ts is not None:
        scan_since = since_ts
    elif force_full:
        scan_since = 0
    else:
        scan_since = state.get('last_scan_ts', 0)

    # 扫描文件树
    added, updated, unchanged, removed = 0, 0, 0, 0
    scanned_files = set()
    new_entries = {}

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith('.')
                       and d not in {'archive', 'archived', 'deprecated'}]

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, root)
            try:
                mtime = os.path.getmtime(fpath)
            except OSError:
                continue  # 文件已删除/符号链接断裂，跳过
            scanned_files.add(rel)

            # 增量判断：文件未变化则跳过
            if not force_full and mtime <= scan_since and rel in existing:
                new_entries[rel] = existing[rel]
                unchanged += 1
                continue

            entry = scan_file(fpath, rel)
            if entry is None:
                continue

            if rel in existing:
                updated += 1
            else:
                added += 1
            new_entries[rel] = entry

    # 检测删除的文件
    for rel in existing:
        if rel not in scanned_files:
            removed += 1

    # 构建注册表
    entries = sorted(new_entries.values(), key=lambda x: x.get('priority', 65))

    by_layer = {}
    by_status = {}
    valid_count = sum(1 for e in entries if e.get('valid'))
    invalid_count = sum(1 for e in entries if not e.get('valid'))
    no_dna_count = 0  # 增量模式不统计无DNA文件

    for e in entries:
        layer = e.get('layer', 'L3_GENERATIONAL')
        status = e.get('status', '🟢')
        by_layer[layer] = by_layer.get(layer, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

    registry = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'root': root,
        'mode': 'incremental' if not force_full else 'full',
        'since_ts': scan_since,
        'dna_valid': valid_count,
        'dna_invalid': invalid_count,
        'no_dna': no_dna_count,
        'total_registered': len(entries),
        'alignment_rate': round(valid_count * 100 / max(len(new_entries), 1), 1),
        'diff': {
            'added': added, 'updated': updated,
            'unchanged': unchanged, 'removed': removed,
        },
        'by_layer': by_layer,
        'by_status': by_status,
        'entries': entries,
    }

    os.makedirs(registry_path.parent, exist_ok=True)
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    # 保存扫描状态
    save_scan_state(project_root, {
        'last_scan_ts': time.time(),
        'total_files': len(entries),
        'last_full_scan': datetime.now(timezone.utc).isoformat(),
    })

    elapsed = time.time() - t0
    return registry, elapsed, added, updated, unchanged, removed


def main():
    project_root = Path(__file__).resolve().parent.parent
    registry_path = project_root / ".longhun" / "dna-audit" / "dna_registry.json"

    if '--status' in sys.argv:
        state = load_last_scan_state(project_root)
        if state['last_scan_ts'] == 0:
            print("🟡 从未扫描")
        else:
            last = datetime.fromtimestamp(state['last_scan_ts'])
            print(f"🟢 上次扫描: {last.isoformat()} | {state['total_files']} 文件")
        return

    force_full = '--full' in sys.argv
    since_ts = None

    for i, arg in enumerate(sys.argv):
        if arg == '--since' and i + 1 < len(sys.argv):
            try:
                dt = datetime.fromisoformat(sys.argv[i + 1])
                since_ts = dt.timestamp()
            except:
                pass

    registry, elapsed, added, updated, unchanged, removed = incremental_scan(
        project_root, registry_path, since_ts=since_ts, force_full=force_full
    )

    diff = registry['diff']
    mode = registry['mode']
    total = registry['total_registered']
    valid = registry['dna_valid']
    align = registry['alignment_rate']

    print(f"[DONE] {mode} scan in {elapsed:.1f}s | +{diff['added']} ~{diff['updated']} "
          f"={diff['unchanged']} -{diff['removed']} | {total} total | {valid} valid ({align}%)")


if __name__ == '__main__':
    main()
