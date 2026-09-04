#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·AI输出归集索引引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·戊午·亥时·AI-INDEXER-V1.0-INDEX
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2（工程层·允许商业使用）

功能:
  - 扫描 ~/ai-outputs/ 下所有工具的输出
  - 建立跨工具JSON索引
  - 支持按关键词/工具/日期搜索
  - 自动去重·增量更新·统计报告
"""

import os
import json
import re
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 焊死配置
AI_OUTPUT_HUB = Path.home() / "ai-outputs"
INDEX_DIR = AI_OUTPUT_HUB / "_index"
INDEX_FILE = INDEX_DIR / "master_index.json"
STATS_FILE = INDEX_DIR / "stats.json"

# 支持的文件类型
TEXT_EXTS = {'.md', '.txt', '.py', '.js', '.ts', '.html', '.css', '.json', '.jsonl',
             '.toml', '.yaml', '.yml', '.sh', '.zsh', '.bash', '.csv', '.xml',
             '.cnsh', '.sql', '.rs', '.go', '.java', '.kt', '.swift', '.c', '.cpp', '.h'}

ASCII_BYPASS = {'.pyc', '.asc', '.sig', '.gpg', '.zip', '.tar', '.gz', '.png', '.jpg',
                '.jpeg', '.gif', '.webp', '.svg', '.mp4', '.mp3', '.wav', '.ttf', '.woff2'}


def file_hash(path: Path) -> str:
    """快速内容哈希（前8KB）"""
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read(8192)).hexdigest()[:16]
    except Exception:
        return ""


def extract_title(content: str, path: Path) -> str:
    """提取文件标题"""
    # 优先 # 标题
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()[:120]
    # 其次文件名
    return path.stem[:120]


def extract_tags(content: str) -> list:
    """提取标签关键词"""
    tags = set()
    # 从内容提取显著关键词
    patterns = [
        r'\b(DNA|GPG|CNSH|API|SDK|CLI|Docker|K8s|部署|审计|熔断|人格|协议)\b',
        r'#(\w[\w\-]+)',
        r'\[(TODO|FIXME|NOTE|HACK|WARN)\]',
    ]
    for p in patterns:
        for match in re.finditer(p, content, re.IGNORECASE):
            tag = match.group(1) if match.lastindex else match.group(0)
            tags.add(tag.lower())
    return sorted(tags)[:20]


def scan_directory(tool_dir: Path, tool_name: str) -> list:
    """扫描单个工具的产出目录"""
    entries = []
    if not tool_dir.exists():
        return entries

    for filepath in tool_dir.rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.suffix.lower() in ASCII_BYPASS:
            continue
        if filepath.name.startswith('.'):
            continue

        # 跳过索引目录自身
        if '_index' in filepath.parts:
            continue

        try:
            stat = filepath.stat()
            rel_path = str(filepath.relative_to(AI_OUTPUT_HUB))

            entry = {
                'tool': tool_name,
                'path': rel_path,
                'name': filepath.name,
                'stem': filepath.stem,
                'suffix': filepath.suffix.lower(),
                'size': stat.st_size,
                'mtime': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'content_hash': file_hash(filepath),
            }

            # 文本文件才提取标题和标签
            if filepath.suffix.lower() in TEXT_EXTS:
                # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过(后缀白名单不可靠)
                try:
                    with open(filepath, 'rb') as f:
                        if b"\x00" in f.read(8192):
                            continue
                except OSError:
                    continue
                try:
                    content = filepath.read_text(encoding='utf-8', errors='ignore')[:50000]
                    entry['title'] = extract_title(content, filepath)
                    entry['tags'] = extract_tags(content)
                    entry['char_count'] = len(content)
                    # 提取DNA
                    dna_m = re.search(r'(?:DNA|#龍芯⚡️)[：:]\s*(.+?)(?:\n|$)', content)
                    if dna_m:
                        entry['dna'] = dna_m.group(1).strip()[:80]
                except Exception:
                    entry['title'] = filepath.stem
                    entry['tags'] = []

            entries.append(entry)
        except (OSError, PermissionError):
            continue

    return entries


def build_index(force: bool = False) -> dict:
    """构建全量索引"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # 检查是否需要增量更新
    if not force and INDEX_FILE.exists():
        last_mtime = INDEX_FILE.stat().st_mtime
        if time.time() - last_mtime < 300:  # 5分钟内不重复扫
            return load_index()

    all_entries = []
    tools = {
        'codebuddy': AI_OUTPUT_HUB / 'codebuddy',
        'claude': AI_OUTPUT_HUB / 'claude',
        'kimi': AI_OUTPUT_HUB / 'kimi',
        'grok': AI_OUTPUT_HUB / 'grok',
        'copilot': AI_OUTPUT_HUB / 'copilot',
        'shared': AI_OUTPUT_HUB / '_shared',
    }

    for tool_name, tool_dir in tools.items():
        entries = scan_directory(tool_dir, tool_name)
        all_entries.extend(entries)

    # 去重（同hash同文件名=同一文件）
    seen = {}
    for e in all_entries:
        key = (e['content_hash'], e['name'])
        if key in seen:
            # 保留较新的
            if e['mtime'] > seen[key]['mtime']:
                seen[key] = e
        else:
            seen[key] = e

    unique_entries = sorted(seen.values(), key=lambda x: x['mtime'], reverse=True)

    # 统计
    stats = {
        'total_files': len(unique_entries),
        'total_size': sum(e['size'] for e in unique_entries),
        'by_tool': {},
        'by_type': {},
        'last_index': datetime.now().isoformat(),
        'recent_24h': 0,
    }
    cutoff_24h = datetime.now() - timedelta(hours=24)

    for e in unique_entries:
        stats['by_tool'][e['tool']] = stats['by_tool'].get(e['tool'], 0) + 1
        stats['by_type'][e['suffix']] = stats['by_type'].get(e['suffix'], 0) + 1
        if e['mtime'] >= cutoff_24h.isoformat():
            stats['recent_24h'] += 1

    index_data = {
        'entries': unique_entries,
        'stats': stats,
        'generated_at': datetime.now().isoformat(),
        'entry_count': len(unique_entries),
    }

    # 写索引
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    return index_data


def load_index() -> dict:
    """加载已有索引"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'entries': [], 'stats': {}, 'entry_count': 0}


def search_index(query: str, tool: Optional[str] = None, limit: int = 30) -> list:
    """搜索索引"""
    index = build_index()
    results = []
    q = query.lower()

    for e in index.get('entries', []):
        if tool and e['tool'] != tool:
            continue

        score = 0
        # 标题匹配
        if 'title' in e and q in e.get('title', '').lower():
            score += 10
        # 文件名匹配
        if q in e['name'].lower():
            score += 8
        # 标签匹配
        if q in [t.lower() for t in e.get('tags', [])]:
            score += 5
        # 路径匹配
        if q in e['path'].lower():
            score += 3
        # DNA匹配
        if 'dna' in e and q in e.get('dna', '').lower():
            score += 7

        if score > 0:
            e['_score'] = score
            results.append(e)

    return sorted(results, key=lambda x: x['_score'], reverse=True)[:limit]


def get_stats() -> dict:
    """获取统计信息"""
    if STATS_FILE.exists():
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return build_index()['stats']


def print_report(stats: dict):
    """打印归集报告"""
    print("╔══════════════════════════════════════╗")
    print("║   🐉 AI产出归集索引 · 状态报告       ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  总文件数:  {stats.get('total_files', 0):>6}                  ║")
    total_mb = stats.get('total_size', 0) / (1024 * 1024)
    print(f"║  总大小:    {total_mb:>6.1f} MB              ║")
    print(f"║  24h新增:   {stats.get('recent_24h', 0):>6}                  ║")
    print(f"║  索引时间:  {stats.get('last_index', 'N/A')[:19]}   ║")
    print("╠══════════════════════════════════════╣")
    print("║  按工具分布:                         ║")
    for tool, count in sorted(stats.get('by_tool', {}).items()):
        bar = "█" * min(count, 20)
        print(f"║    {tool:<12} {count:>4} {bar} ║")
    print("╠══════════════════════════════════════╣")
    print("║  按类型分布 (Top 8):                 ║")
    for ext, count in sorted(stats.get('by_type', {}).items(), key=lambda x: -x[1])[:8]:
        print(f"║    {ext:<12} {count:>4}                  ║")
    print("╚══════════════════════════════════════╝")


# ── CLI入口 ──

def main():
    import argparse
    parser = argparse.ArgumentParser(description='龍魂·AI产出归集索引引擎')
    sub = parser.add_subparsers(dest='action', help='操作')

    # build
    sub.add_parser('build', help='构建/更新索引')
    p_build = sub.add_parser('force', help='强制重建索引')

    # search
    p_search = sub.add_parser('search', help='搜索索引')
    p_search.add_argument('query', help='搜索关键词')
    p_search.add_argument('--tool', '-t', help='限定工具: codebuddy/claude/kimi/grok')
    p_search.add_argument('--limit', '-n', type=int, default=20, help='返回条数')

    # stats
    sub.add_parser('stats', help='查看统计')

    # report
    sub.add_parser('report', help='打印完整报告')

    # scan (输出路径 → 归集)
    p_scan = sub.add_parser('scan', help='扫描并归集指定目录')
    p_scan.add_argument('source', help='源目录路径')
    p_scan.add_argument('--tool', '-t', required=True, help='工具名')

    args = parser.parse_args()

    if args.action == 'search':
        results = search_index(args.query, args.tool, args.limit)
        if not results:
            print(f"🔍 未找到匹配 '{args.query}' 的结果")
            return
        print(f"🔍 搜索 '{args.query}' — {len(results)} 条结果:\n")
        for i, r in enumerate(results, 1):
            tool_icon = {'codebuddy': '🧠', 'claude': '🤖', 'kimi': '🔮',
                         'grok': '⚡', 'copilot': '👾', 'shared': '📦'}.get(r['tool'], '📄')
            title = r.get('title', r['name'])[:80]
            print(f"  {i:2}. {tool_icon} [{r['tool']}] {title}")
            print(f"      📁 {r['path']}")
            if 'dna' in r:
                print(f"      🧬 {r['dna']}")
            if 'tags' in r and r['tags']:
                print(f"      🏷️  {', '.join(r['tags'][:8])}")
            print()

    elif args.action == 'stats':
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))

    elif args.action == 'report':
        print_report(get_stats())

    elif args.action == 'scan':
        source = Path(args.source).expanduser().resolve()
        dest = AI_OUTPUT_HUB / args.tool
        dest.mkdir(parents=True, exist_ok=True)
        import shutil
        copied = 0
        for f in source.rglob("*"):
            if f.is_file() and f.suffix.lower() in TEXT_EXTS:
                rel = f.relative_to(source)
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or f.stat().st_mtime > target.stat().st_mtime:
                    shutil.copy2(f, target)
                    copied += 1
        print(f"✅ 从 {args.tool} 归集 {copied} 个文件 → {dest}")
        build_index(force=True)

    else:
        # 默认：构建+报告
        index = build_index()
        print_report(index['stats'])


if __name__ == '__main__':
    main()
