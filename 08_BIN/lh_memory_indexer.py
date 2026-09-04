#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷯井-MEMORY-INDEXER-v1.0-7a3f001c
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 将所有每日日志编入统一索引 → ~/.longhun/memory_index.json
"""
龍魂·记忆索引器 v1.0
────────────────────────────
扫描 .codebuddy/memory/ 下所有每日日志（YYYY-MM-DD.md），提取：
  - 日期、标题、DNA码、关键词、内容摘要
  - 存入 ~/.longhun/memory_index.json
  - 记忆API启动时自动加载，查询时先查索引再回源

用法:
  python3 bin/lh_memory_indexer.py              # 增量构建索引
  python3 bin/lh_memory_indexer.py --force      # 强制重建全量索引
  python3 bin/lh_memory_indexer.py --stats      # 仅输出统计
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 常量 ──────────────────────────────────────────
CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DAILY_LOG_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
MEMORY_FILE = DAILY_LOG_DIR / "MEMORY.md"
INDEX_FILE = Path.home() / ".longhun" / "memory_index.json"
INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── 关键词提取正则 ────────────────────────────────
RE_HEADING = re.compile(r'^#{1,4}\s+(.+?)$', re.MULTILINE)
RE_DNA = re.compile(r'(?:DNA|#龍芯|dna)[：:]\s*(#[^\n]{10,80})', re.IGNORECASE)
RE_BOLD = re.compile(r'\*\*(.+?)\*\*')
RE_DATE_IN_TITLE = re.compile(r'^#\s*(\d{4}-\d{2}-\d{2})')

# 停用词（不提取为关键词）
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '他', '她', '它', '们', '那', '什么', '怎么', '哪', '为什么',
    '可以', '这个', '那个', '还', '被', '把', '让', '与', '或', '从', '而', '且',
    '但', '所以', '因为', '如果', '虽然', '然而', '然后', '之后', '之前', '已经',
    '进行', '使用', '通过', '需要', '应该', '可能', '能够', '对于', '关于', '一些',
    '每个', '所有', '任何', '其他', '其中', '之后', '现在', '目前', '当前',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
    'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
}


def extract_keywords(text: str, max_kw: int = 20) -> List[str]:
    """从文本中提取关键词（标题 + 加粗 + 长词过滤停用词）"""
    keywords = []

    # 提取标题
    for m in RE_HEADING.finditer(text):
        kw = m.group(1).strip()
        # 去掉开头的数字编号
        kw = re.sub(r'^\d+[\.\、\)）]\s*', '', kw)
        if len(kw) >= 2 and kw not in STOP_WORDS:
            keywords.append(kw)

    # 提取加粗文本
    for m in RE_BOLD.finditer(text):
        kw = m.group(1).strip()
        if len(kw) >= 3 and kw not in STOP_WORDS and kw not in keywords:
            keywords.append(kw)

    # 提取长词（4字以上中文词组）
    words = re.findall(r'[\u4e00-\u9fff]{4,}', text)
    seen = set(keywords)
    for w in words:
        if w not in seen and w not in STOP_WORDS:
            keywords.append(w)
            seen.add(w)
            if len(keywords) >= max_kw:
                break

    # 只保留独特的、有意义的
    unique = []
    seen = set()
    for kw in keywords:
        kw_clean = kw.strip().lower()
        if kw_clean not in seen and len(kw_clean) >= 2:
            unique.append(kw)
            seen.add(kw_clean)

    return unique[:max_kw]


def extract_title(text: str, filename_stem: str) -> str:
    """提取日志标题：第一行 > 第一个 ## 标题 > 文件名日期"""
    lines = text.strip().split('\n')
    # 尝试第一行（# 标题）
    if lines and lines[0].startswith('# '):
        return lines[0][2:].strip()
    # 尝试第一个二级标题
    for line in lines:
        if line.startswith('## '):
            return line[3:].strip()
    return f"每日日志 {filename_stem}"


def extract_dnas(text: str) -> List[str]:
    """提取所有 DNA 码"""
    dnas = []
    for m in RE_DNA.finditer(text):
        dna = m.group(1).strip()
        if len(dna) > 10:
            dnas.append(dna)
    return dnas


def get_content_preview(text: str, max_chars: int = 300) -> str:
    """生成内容摘要（跳过标题行）"""
    lines = text.strip().split('\n')
    content_lines = []
    for line in lines:
        stripped = line.strip()
        # 跳过纯标题行和分隔线
        if stripped.startswith('#') or stripped.startswith('---') or stripped.startswith('==='):
            if not content_lines:
                continue
        content_lines.append(line)
    preview = '\n'.join(content_lines[:10]).strip()
    if len(preview) > max_chars:
        preview = preview[:max_chars] + '...'
    return preview


def index_file(filepath: Path) -> Dict[str, Any]:
    """索引单个日志文件"""
    text = filepath.read_text(encoding='utf-8')
    stem = filepath.stem  # YYYY-MM-DD

    title = extract_title(text, stem)
    keywords = extract_keywords(text)
    dnas = extract_dnas(text)
    preview = get_content_preview(text)
    size_bytes = len(text.encode('utf-8'))

    # 计算内容哈希
    content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    return {
        "date": stem,
        "title": title,
        "file": str(filepath.relative_to(PROJECT_ROOT)),
        "keywords": keywords,
        "dnas": dnas,
        "preview": preview,
        "size_kb": round(size_bytes / 1024, 1),
        "content_hash": content_hash,
    }


def build_index(force: bool = False) -> Dict[str, Any]:
    """构建全量索引"""
    # 加载现有索引（增量模式）
    existing: Dict[str, Any] = {}
    if not force and INDEX_FILE.exists():
        try:
            existing = json.loads(INDEX_FILE.read_text(encoding='utf-8'))
        except Exception:
            existing = {}

    existing_entries = existing.get("entries", {})

    # 扫描每日日志
    log_files = sorted(DAILY_LOG_DIR.glob("20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"))
    entries: Dict[str, Dict[str, Any]] = {}
    new_count = 0
    updated_count = 0

    for fp in log_files:
        stem = fp.stem
        entry = index_file(fp)

        if not force and stem in existing_entries:
            # 增量模式：检查是否需要更新
            old = existing_entries[stem]
            if old.get("content_hash") == entry["content_hash"] and old.get("size_kb") == entry["size_kb"]:
                entries[stem] = old  # 复用旧条目
                continue
            updated_count += 1
        elif stem not in existing_entries:
            new_count += 1

        entries[stem] = entry

    # 统计
    total_kw = sum(len(e["keywords"]) for e in entries.values())
    total_dnas = sum(len(e["dnas"]) for e in entries.values())

    # 构建关键词倒排索引
    kw_index: Dict[str, List[str]] = {}
    for date_str, entry in entries.items():
        for kw in entry["keywords"]:
            kw_lower = kw.lower()
            if kw_lower not in kw_index:
                kw_index[kw_lower] = []
            if date_str not in kw_index[kw_lower]:
                kw_index[kw_lower].append(date_str)

    result = {
        "version": "1.0.0",
        "dna": "#龍芯⚡️丙午·乙未·辛酉·甲午·䷯井-MEMORY-INDEXER-v1.0-7a3f001c",
        "built_at": datetime.now(CST).isoformat(),
        "total_files": len(entries),
        "total_keywords": total_kw,
        "total_dnas": total_dnas,
        "new": new_count,
        "updated": updated_count,
        "unchanged": len(entries) - new_count - updated_count,
        "keyword_index": kw_index,
        "entries": entries,
    }

    # 写盘
    INDEX_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


def show_stats(index: Dict[str, Any]):
    """打印统计信息"""
    print(f"\n╔══════════════════════════════════════════╗")
    print(f"║  龍魂·记忆索引器 v1.0                     ║")
    print(f"╠══════════════════════════════════════════╣")
    print(f"║  索引文件: {len(index['entries'])} 个日志")
    print(f"║  关键词:   {index['total_keywords']} 个")
    print(f"║  DNA码:    {index['total_dnas']} 个")
    print(f"║  新增:     {index['new']}  更新: {index['updated']}  未变: {index['unchanged']}")
    print(f"║  输出:     {INDEX_FILE}")
    print(f"╚══════════════════════════════════════════╝")

    # 日期范围
    dates = sorted(index['entries'].keys())
    if dates:
        print(f"\n  日期范围: {dates[0]} ~ {dates[-1]}")

    # TOP 10 关键词
    kw_count = sorted(index['keyword_index'].items(), key=lambda x: len(x[1]), reverse=True)[:10]
    if kw_count:
        print(f"\n  TOP 10 关键词（按出现频率）:")
        for kw, dates_list in kw_count:
            print(f"    {kw}: {len(dates_list)} 天")

    print()


def search_index(query: str, index: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """在索引中搜索（供记忆API调用）"""
    if index is None:
        if not INDEX_FILE.exists():
            return []
        index = json.loads(INDEX_FILE.read_text(encoding='utf-8'))

    results = []
    q_lower = query.lower()
    entries = index.get("entries", {})
    kw_index = index.get("keyword_index", {})

    # 对每个条目打分
    for date_str, entry in entries.items():
        score = 0
        matched_kws = []

        # 关键词匹配
        for kw in entry.get("keywords", []):
            if q_lower in kw.lower() or kw.lower() in q_lower:
                score += 2
                matched_kws.append(kw)

        # 标题匹配
        if q_lower in entry.get("title", "").lower():
            score += 5
            matched_kws.append(f"[标题] {entry['title']}")

        # 内容摘要匹配
        if q_lower in entry.get("preview", "").lower():
            score += 1

        # DNA 匹配
        for dna in entry.get("dnas", []):
            if q_lower in dna.lower():
                score += 3
                matched_kws.append(f"[DNA] {dna[:40]}...")

        if score > 0:
            results.append({
                "date": date_str,
                "title": entry.get("title", ""),
                "file": entry.get("file", ""),
                "score": score,
                "matched_keywords": matched_kws[:5],
                "preview": entry.get("preview", "")[:200],
                "dnas": entry.get("dnas", [])[:3],
            })

    # 按分数降序
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ── CLI ──────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·记忆索引器 v1.0")
    parser.add_argument("--force", action="store_true", help="强制重建全量索引")
    parser.add_argument("--stats", action="store_true", help="仅输出统计")
    parser.add_argument("--search", type=str, help="搜索关键词")
    args = parser.parse_args()

    if args.search:
        idx = json.loads(INDEX_FILE.read_text(encoding='utf-8')) if INDEX_FILE.exists() else {}
        results = search_index(args.search, idx)
        print(f"\n搜索: {args.search} → {len(results)} 条结果\n")
        for r in results[:10]:
            print(f"  [{r['date']}] [分数:{r['score']}] {r['title']}")
            print(f"    匹配: {', '.join(r.get('matched_keywords', []))}")
            print(f"    文件: {r['file']}")
            print()
    else:
        result = build_index(force=args.force)
        show_stats(result)
