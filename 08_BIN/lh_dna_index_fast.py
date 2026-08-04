#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-24-BIN-DNA_INDEX_FAST-v2.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
#龍芯⚡️2026-07-24-BIN-DNA_INDEX_FAST-v2.2
DNA快速索引 v2.2 — 文件DNA + 行为DNA标签双轨扫描·os.walk剪枝·流式输出
v2.2新增: 行为DNA标签扫描(7F-*/MODE-*/EVT-*/EMO-*/AUTH-L*)纳入注册表
"""
import os, re, json, sys, time
from pathlib import Path
from datetime import datetime, timezone

DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')

# ━━ v2.2: 行为DNA标签正则 ━━
BEHAVIOR_LABEL_RE = re.compile(
    r'(?:'
    r'7F-[PFTCERAXYZ]-[^\s,，\n]+|'      # 七因子
    r'MODE-[^\s,，\n]+|'                  # 行为模式
    r'EVT-[^\s,，\n]+|'                   # 事件类型
    r'EMO-[^\s,，\n]+|'                   # 情绪标签
    r'T-[^\s,，\n]+|'                      # 审计周期
    r'SPACE-[^\s,，\n]+|'                 # 空间层级
    r'AUTH-L\d-[^\s,，\n]+'               # 数据主权
    r')'
)

SKIP_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', '.longhun',
             '_archive', '.backups', 'backups', 'backup', '.backup', 'backup_*',
             'old', '.old', 'legacy', 'temp', '.temp', '.cache', '.uv', '.npm',
             '.nvm', 'site-packages', '.obsidian', '.claude', '.github', 'data',
             'models', 'logs', 'dist', 'build', 'eggs', '.eggs', '.pytest_cache',
             '.mypy_cache', '.obsidian'}

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

PRIO = {'L0_ETERNAL': 5, 'L1_SEASONAL': 20, 'L2_DECISION': 40,
        'L3_GENERATIONAL': 65, 'L4_INSTANT': 90}
WS = {'🟢': 1.0, '🟡': 0.6, '🔴': 0.3}

def main():
    t0 = time.time()
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    outfile = sys.argv[2] if len(sys.argv) > 2 else '.longhun/dna-audit/dna_registry.json'
    root = os.path.abspath(root)

    entries = []
    by_layer = {}
    by_status = {}
    scanned = valid_count = invalid_count = no_dna_count = behavior_count = 0
    behavior_by_type = {}  # v2.2: 行为标签分类统计
    last_report = t0

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Prune skip dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith('.')
                       and d not in {'archive', 'archived', 'deprecated'}]

        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in TEXT_EXTS:
                continue
            if fname.startswith('.env') or fname in {'.gitignore', '.dockerignore', '.editorconfig'}:
                continue

            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, root)
            scanned += 1

            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    # Only read first 2KB for DNA match (it's always near top)
                    head = f.read(2048)
            except Exception:
                continue

            m = DNA_RE.search(head)
            if not m:
                no_dna_count += 1
                continue

            dna_raw = m.group(0).strip()
            dna = dna_raw[1:] if dna_raw and dna_raw[0] in ' \t"\'' else dna_raw
            date_str = m.group(1)
            module = m.group(2)
            version = m.group(3)

            # Simple validity check
            valid = dna.startswith('#龍芯⚡️') or dna.startswith('#龍芯')
            if valid:
                valid_count += 1
            else:
                invalid_count += 1

            layer = determine_layer(rel, module)
            status = determine_status(rel)
            priority = PRIO.get(layer, 65)
            weight = round(priority * WS.get(status, 1.0), 1)

            # ━━ v2.2: 提取行为DNA标签 ━━
            behavior_labels = []
            # 在已读取的前2KB中扫描
            for m_behavior in BEHAVIOR_LABEL_RE.finditer(head):
                behavior_labels.append(m_behavior.group(0))
            if behavior_labels:
                behavior_count += len(behavior_labels)

            entry = {
                'file': rel, 'dna': dna, 'date': date_str,
                'module': module, 'version': version, 'valid': valid,
                'layer': layer, 'status': status,
                'priority': priority, 'weight': weight,
            }
            if behavior_labels:
                entry['behavior_labels'] = behavior_labels
                # 分类统计
                for label in behavior_labels:
                    if label.startswith('7F-'):
                        behavior_by_type['七因子'] = behavior_by_type.get('七因子', 0) + 1
                    elif label.startswith('MODE-'):
                        behavior_by_type['行为模式'] = behavior_by_type.get('行为模式', 0) + 1
                    elif label.startswith('EVT-'):
                        behavior_by_type['事件类型'] = behavior_by_type.get('事件类型', 0) + 1
                    elif label.startswith('EMO-'):
                        behavior_by_type['情绪标签'] = behavior_by_type.get('情绪标签', 0) + 1
                    elif label.startswith('AUTH-L'):
                        behavior_by_type['数据主权'] = behavior_by_type.get('数据主权', 0) + 1
                    elif label.startswith('T-'):
                        behavior_by_type['审计周期'] = behavior_by_type.get('审计周期', 0) + 1
                    elif label.startswith('SPACE-'):
                        behavior_by_type['空间层级'] = behavior_by_type.get('空间层级', 0) + 1

            entries.append(entry)
            by_layer[layer] = by_layer.get(layer, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        # Progress report every 5s
        now = time.time()
        if now - last_report > 5:
            print(f"  [DNA-IDX] scanned={scanned} dna={valid_count} dir={dirpath[-60:]}", flush=True)
            last_report = now

    elapsed = time.time() - t0
    behavior_info = f" | 🧬行为标签: {behavior_count}" if behavior_count > 0 else ""
    print(f"\n[DONE] {scanned} files in {elapsed:.1f}s | DNA: {valid_count} valid + {invalid_count} invalid | {no_dna_count} without DNA{behavior_info}", flush=True)

    registry = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'root': root,
        'scanned': scanned,
        'dna_valid': valid_count,
        'dna_invalid': invalid_count,
        'no_dna': no_dna_count,
        'total_registered': len(entries),
        'alignment_rate': round(valid_count * 100 / max(scanned, 1), 1),
        'by_layer': by_layer,
        'by_status': by_status,
        # v2.2: 行为DNA统计
        'behavior_labels_total': behavior_count,
        'behavior_by_type': behavior_by_type,
        'entries': entries,
    }

    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    size_mb = os.path.getsize(outfile) / (1024*1024)
    print(f"[WRITTEN] {outfile} ({size_mb:.1f}MB)", flush=True)

if __name__ == '__main__':
    main()
