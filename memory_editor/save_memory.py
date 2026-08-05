#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐲 龙魂记忆编辑器 · 命令行保存工具 v3.1
DNA: #龍芯⚡️2026-08-05-CLI-SAVE-UID9622
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2

用法:
    python3 save_memory.py "我的记忆内容"
    python3 save_memory.py "我的记忆内容" --category scene_memory --tags "项目A, 重要"
    python3 save_memory.py --file memo.txt --category atomic_facts
    python3 save_memory.py --list
    python3 save_memory.py --search "决策模式"

依赖: Python 3.8+
许可: MulanPSL v2
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, date
from pathlib import Path

# ═══════════════ 配置 ═══════════════
DNA_PREFIX = "#龍芯⚡️"
UID = "UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
MEMORY_DIR = Path.home() / "Desktop" / "龍魂系统·本地知识库" / "記憶"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = MEMORY_DIR / "index.json"

BASE_DATE = date(1984, 2, 2)  # 甲子日基准

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 五虎遁：年干 -> 正月（寅月）月干索引
TIGER_BASE = {
    '甲': 2, '乙': 4, '丙': 6, '丁': 8, '戊': 0,
    '己': 2, '庚': 4, '辛': 6, '壬': 8, '癸': 0,
}
# 五鼠遁：日干 -> 子时（00:00-01:00）时干索引
MOUSE_BASE = {
    '甲': 0, '乙': 2, '丙': 4, '丁': 6, '戊': 8,
    '己': 0, '庚': 2, '辛': 4, '壬': 6, '癸': 8,
}

CATEGORIES = {
    "atomic_facts":   {"icon": "🔬", "label": "原子事实"},
    "scene_memory":   {"icon": "🎬", "label": "场景记忆"},
    "global_overview": {"icon": "🌍", "label": "全局概览"},
    "chat_history":   {"icon": "💬", "label": "原始会话"},
}


# ═══════════════ 天干地支四柱 ═══════════════
def year_ganzhi(dt: datetime):
    y = dt.year
    return STEMS[(y - 4) % 10], BRANCHES[(y - 4) % 12]


def month_ganzhi(dt: datetime):
    y_stem, _ = year_ganzhi(dt)
    m = dt.month
    # 公历近似：1月=寅，2月=卯，...，12月=丑
    branch_idx = (m + 1) % 12
    stem_idx = (TIGER_BASE[y_stem] + m - 1) % 10
    return STEMS[stem_idx], BRANCHES[branch_idx]


def day_ganzhi(dt: datetime):
    d = dt.date()
    diff = (d - BASE_DATE).days
    idx = diff % 60
    return STEMS[idx % 10], BRANCHES[idx % 12]


def hour_ganzhi(dt: datetime):
    d_stem, _ = day_ganzhi(dt)
    h = dt.hour
    branch_idx = ((h + 1) // 2) % 12
    stem_idx = (MOUSE_BASE[d_stem] + branch_idx) % 10
    return STEMS[stem_idx], BRANCHES[branch_idx]


def sizhu(dt: datetime) -> str:
    ys, yb = year_ganzhi(dt)
    ms, mb = month_ganzhi(dt)
    ds, db = day_ganzhi(dt)
    hs, hb = hour_ganzhi(dt)
    return f"{ys}{yb}{ms}{mb}{ds}{db}{hs}{hb}"


# ═══════════════ 工具函数 ═══════════════
def generate_dna() -> str:
    """生成基于天干地支四柱的 DNA 追溯码。"""
    now = datetime.now(timezone.utc)
    gz = sizhu(now)
    rand = os.urandom(2).hex().upper()
    return f"{DNA_PREFIX}{gz}-MEMORY-{rand}-{UID}"


def digital_root(text: str) -> int:
    total = sum(ord(c) for c in text)
    while total >= 10:
        total = sum(int(d) for d in str(total))
    return total


def extract_keywords(text: str, max_n: int = 5):
    stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '也', '他', '这', '中', '大',
                 '来', '上', '个', '们', '说', '要', '去', '你', '会', '着', '好', '自己', '那', '什么',
                 '怎么', '为什么', '可以', '没有', '不是', '已经', '一个', '非常', '真的', '还是', '但是',
                 '因为', '所以', '如果', '可能', '这样', '那样', '把', '被', '让', '到', '对', '为', '与',
                 '而', '之', '其', '以', '及', '或', '但', '啊', '呢', '吧', '吗', '嘛', '哦', '嗯'}
    words = [w for w in __import__('re').split('[\\s,，.。！!？?、；;：:（）()\\n\\r\\t""''《》<>【】\\[\\]]+', text)
             if len(w) >= 2 and w not in stopwords]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:max_n]]


def parse_tags(raw: str):
    return [t.strip() for t in raw.replace('，', ',').replace('；', ';').split(',') if t.strip()]


# ═══════════════ 存储 ═══════════════
def load_index() -> list:
    if not INDEX_PATH.exists():
        return []
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_index(index: list):
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def save_memory(content: str, category: str, tags: list):
    if not content.strip():
        print("❌ 内容为空")
        return None

    now = datetime.now(timezone.utc)
    dna = generate_dna()
    timestamp = now.isoformat()
    date_str = now.strftime("%Y-%m-%d")
    file_id = now.strftime("%Y%m%d_%H%M%S")
    root = digital_root(content)
    keywords = extract_keywords(content)

    file_path = MEMORY_DIR / f"記憶_{file_id}_{date_str}_{UID}.cnsh.md"
    meta = CATEGORIES.get(category, {"icon": "❓", "label": category})

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""---
DNA: {dna}
确认码: {CONFIRM}
创建时间: {timestamp}
数字根: {root}
分类: {meta['icon']} {meta['label']}
标签: {'、'.join(tags)}
关键词: {'、'.join(keywords)}
---
{content.strip()}
""")

    index = load_index()
    index.insert(0, {
        "id": f"mem_{file_id}",
        "dna": dna,
        "timestamp": timestamp,
        "date": date_str,
        "digital_root": root,
        "category": category,
        "tags": tags,
        "keywords": keywords,
        "file": str(file_path.name),
        "preview": content[:100] + ("..." if len(content) > 100 else ""),
    })
    save_index(index)

    print(f"✅ 记忆已保存: {file_path}")
    print(f"🧬 DNA: {dna}")
    print(f"🔢 数字根: {root}")
    print(f"📂 分类: {meta['icon']} {meta['label']}")
    if tags:
        print(f"🏷️  标签: {', '.join(tags)}")
    return file_path


def list_memories(category: str = None, limit: int = 20):
    index = load_index()
    if category:
        index = [e for e in index if e.get("category") == category]
    return index[:limit]


def search_memories(query: str, limit: int = 20):
    index = load_index()
    q = query.lower()
    results = []
    for e in index:
        haystack = " ".join([
            e.get("preview", ""),
            *e.get("tags", []),
            *e.get("keywords", []),
            e.get("dna", ""),
        ]).lower()
        if q in haystack:
            results.append(e)
        if len(results) >= limit:
            break
    return results


def format_memory(e: dict, idx: int = None) -> str:
    meta = CATEGORIES.get(e.get("category", ""), {"icon": "❓", "label": e.get("category", "未知")})
    tags_str = ", ".join(f"#{t}" for t in e.get("tags", []))
    preview = e.get("preview", "")
    dna_short = (e.get("dna") or e.get("id", ""))[-24:]

    lines = []
    head = f"[{idx}] " if idx is not None else ""
    lines.append(f"── {head}{meta['icon']} {meta['label']} ──")
    lines.append(f"  🧬 DNA: {dna_short}")
    lines.append(f"  📅 {e.get('timestamp', '?')[:19]}")
    if tags_str:
        lines.append(f"  🏷️  {tags_str}")
    lines.append(f"  📝 {preview}")
    return "\n".join(lines)


# ═══════════════ 主入口 ═══════════════
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龙魂记忆编辑器 · CLI 保存工具（天干地支 DNA 版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 save_memory.py "今天学习了五行调度算法"
  python3 save_memory.py "修复了审计模块的Bug" --category atomic_facts --tags "bug修复, 审计"
  python3 save_memory.py --file memo.txt --category chat_history --tags "对话记录"
  python3 save_memory.py --list
  python3 save_memory.py --list --category scene_memory
  python3 save_memory.py --search "五行调度"
        """,
    )

    parser.add_argument("content", nargs="?", default=None, help="记忆内容（不提供时从 stdin 读取）")
    parser.add_argument("--file", "-f", default=None, help="从文件读取记忆内容")
    parser.add_argument("--category", "-c", default=None, choices=list(CATEGORIES.keys()),
                        help="记忆分类（默认: 不限）")
    parser.add_argument("--tags", "-t", default="", help="标签，逗号分隔（如: 项目A, 重要）")
    parser.add_argument("--list", "-l", action="store_true", help="列出最近的记忆")
    parser.add_argument("--search", "-s", default=None, help="搜索记忆内容")
    parser.add_argument("--limit", "-n", type=int, default=20, help="列出/搜索的最大条数（默认: 20）")
    parser.add_argument("--json", "-j", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    # ── 列表模式 ──
    if args.list:
        memories = list_memories(args.category, args.limit)
        if args.json:
            print(json.dumps(memories, ensure_ascii=False, indent=2))
        else:
            if not memories:
                print("📭 暂无记忆。")
            for i, m in enumerate(memories, 1):
                print(format_memory(m, i))
        return

    # ── 搜索模式 ──
    if args.search:
        results = search_memories(args.search, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            if not results:
                print(f"🔍 未找到匹配 '{args.search}' 的记忆。")
            for i, m in enumerate(results, 1):
                print(format_memory(m, i))
        return

    # ── 保存模式 ──
    if args.file:
        try:
            content = Path(args.file).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
    elif args.content:
        content = args.content
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
        else:
            print("❌ 请提供记忆内容，或通过管道输入。")
            print("   用法: python3 save_memory.py \"记忆内容\"")
            print("   或: echo \"记忆内容\" | python3 save_memory.py")
            sys.exit(1)

    if not content or not content.strip():
        print("❌ 记忆内容不能为空。")
        sys.exit(1)

    tags = parse_tags(args.tags)
    category = args.category or "atomic_facts"
    save_memory(content, category, tags)


if __name__ == "__main__":
    main()
