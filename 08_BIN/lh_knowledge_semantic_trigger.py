#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自然语言知识搜索引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-KNOWLEDGE-SEMANTIC-TRIGGER-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

自然语言知识搜索：输一句人话，查三源知识库
  python3 bin/lh_knowledge_semantic_trigger.py "密码学相关文章"
  python3 bin/lh_knowledge_semantic_trigger.py --stats
  python3 bin/lh_knowledge_semantic_trigger.py --list 算法
  python3 bin/lh_knowledge_semantic_trigger.py --build

三源融合: CSDN博客 + Notion页面 + 本地知识卡片
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple
from collections import Counter

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-KNOWLEDGE-SEMANTIC-TRIGGER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
KB_INDEX = ROOT / "portal" / "knowledge" / "kb_index.json"
KNOWLEDGE_DIR = ROOT / "knowledge"
ARTICLES_DIR = ROOT / "articles"
NOTION_DIR = ROOT / "docs" / "notion_mirror"

# 分类关键词映射（帮助语义匹配）
CATEGORY_KEYWORDS = {
    "密码学": ["密码", "加密", "解密", "哈希", "数字签名", "密钥", "AES", "RSA", "SM2", "SM3", "SM4", "国密", "证书", "安全"],
    "CNSH": ["CNSH", "中文神经符号", "神经符号", "编程语言", "语义解析", "隐语法"],
    "AI/ML": ["AI", "机器学习", "深度学习", "模型", "训练", "推理", "神经网络", "Transformer", "LLM", "大模型", "ChatGPT"],
    "算法": ["算法", "排序", "搜索", "图论", "动态规划", "数据结构", "复杂度"],
    "龍魂": ["龍魂", "龙魂", "Longhun", "20人格", "人格", "DNA", "审计", "熔断", "GPG"],
    "哲学": ["易经", "太极", "道德经", "五行", "河图", "洛书", "369", "八卦", "三才", "七因子", "中国哲学"],
    "安全": ["安全", "渗透", "漏洞", "防火墙", "护盾", "入侵", "审计", "扫描", "加密", "隐私"],
    "区块链": ["区块链", "比特币", "以太坊", "智能合约", "去中心化", "Web3", "NFT"],
    "前端": ["HTML", "CSS", "JavaScript", "React", "Vue", "前端", "网页", "UI"],
    "后端": ["API", "服务器", "数据库", "Python", "FastAPI", "Docker", "部署", "后端"],
}


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


# ═══════════════════════════════════════════
# 核心: 语义搜索
# ═══════════════════════════════════════════

def _extract_keywords(query: str) -> List[str]:
    """从自然语言查询中提取关键词"""
    keywords = []
    # 直接匹配分类关键词
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in query.lower():
                keywords.append(kw)
                if cat not in keywords:  # 记录命中的分类
                    keywords.append(f"__CAT__{cat}")
    # 去掉分类标记，只要纯关键词
    pure_kw = [k for k in keywords if not k.startswith("__CAT__")]
    return list(set(pure_kw))[:10]


def _detect_category(query: str) -> List[str]:
    """检测查询对应的分类"""
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in query.lower():
                cats.append(cat)
                break
    return cats


def _fuzzy_match(text: str, query: str) -> float:
    """简单的模糊匹配评分 (0-1)"""
    text_lower = text.lower()
    query_lower = query.lower()

    # 精确包含
    if query_lower in text_lower:
        return 1.0

    # 切词匹配
    query_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query_lower))
    if not query_words:
        return 0.0

    text_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text_lower))
    hits = query_words & text_words
    return len(hits) / len(query_words) if query_words else 0.0


def search(query: str, limit: int = 30) -> List[Dict[str, Any]]:
    """三源融合搜索"""
    results: List[Tuple[float, Dict[str, Any]]] = []
    detected_cats = _detect_category(query)

    _log(f"🔍 搜索: '{query}'")
    if detected_cats:
        _log(f"  检测到分类: {', '.join(detected_cats)}")

    # 源1: 网站知识索引 (kb_index.json)
    if KB_INDEX.exists():
        with open(KB_INDEX) as f:
            idx = json.load(f)
        for art in idx.get("articles", []):
            title = art.get("title", "")
            summary = art.get("summary", "")
            text = f"{title} {summary}"
            score = _fuzzy_match(text, query)

            # 分类匹配加权
            cat = art.get("category", "")
            if cat in detected_cats:
                score = max(score, score * 1.5)

            if score > 0:
                results.append((score, {
                    "title": title,
                    "summary": summary[:200],
                    "source": art.get("source", "未知"),
                    "category": cat,
                    "quality": art.get("quality", 0),
                    "url": art.get("url", ""),
                    "origin": "网站索引",
                }))

    # 源2: 本地知识卡片
    if KNOWLEDGE_DIR.exists():
        for md in KNOWLEDGE_DIR.rglob("*.md"):
            try:
                content = md.read_text(encoding='utf-8', errors='ignore')
                # 取标题（第一个#行）
                first_line = md.stem
                for line in content.split('\n'):
                    if line.startswith('# '):
                        first_line = line[2:].strip()
                        break
                text = f"{first_line} {content[:500]}"
                score = _fuzzy_match(text, query)
                if score > 0:
                    results.append((score, {
                        "title": first_line,
                        "summary": content[:200].replace('\n', ' '),
                        "source": f"本地知识/{md.parent.name}",
                        "category": md.parent.name,
                        "quality": 1.0,
                        "origin": "本地知识卡片",
                    }))
            except Exception:
                pass

    # 源3: Notion镜像
    if NOTION_DIR.exists():
        pages_dir = NOTION_DIR / "pages"
        if pages_dir.exists():
            for md in list(pages_dir.rglob("*.md"))[:50]:  # 只搜前50个
                try:
                    content = md.read_text(encoding='utf-8', errors='ignore')
                    first_line = md.stem
                    for line in content.split('\n'):
                        if line.startswith('# '):
                            first_line = line[2:].strip()
                            break
                    text = f"{first_line} {content[:500]}"
                    score = _fuzzy_match(text, query)
                    if score > 0:
                        results.append((score, {
                            "title": first_line,
                            "summary": content[:200].replace('\n', ' '),
                            "source": "Notion镜像",
                            "category": "Notion",
                            "quality": 1.0,
                            "origin": "Notion镜像",
                        }))
                except Exception:
                    pass

    # 排序去重
    results.sort(key=lambda x: -x[0])
    seen_titles = set()
    deduped = []
    for _, item in results:
        title = item["title"].lower()
        if title not in seen_titles:
            seen_titles.add(title)
            deduped.append(item)
            if len(deduped) >= limit:
                break

    return deduped


# ═══════════════════════════════════════════
# 交互式命令
# ═══════════════════════════════════════════

def handle_command(cmd: str) -> bool:
    """处理自然语言命令，返回是否已处理"""
    cmd_lower = cmd.strip().lower()

    # "统计概览" → stats
    if any(w in cmd_lower for w in ["统计", "概览", "分布", "stats", "怎么看"]):
        show_stats()
        return True

    # "列出XX分类" → list
    list_match = re.search(r'(?:列出?|显示?|---list)\s*(.*)', cmd_lower)
    if list_match:
        cat = list_match.group(1).strip()
        if cat:
            list_category(cat)
        else:
            list_all_categories()
        return True

    # "重建索引" → build
    if any(w in cmd_lower for w in ["重建", "build", "刷新索引", "重建索引"]):
        build_index()
        return True

    # 默认 → search
    return False


def show_stats():
    """统计概览"""
    total = 0
    cats = Counter()

    if KB_INDEX.exists():
        with open(KB_INDEX) as f:
            idx = json.load(f)
        total = idx.get("total_articles", 0)
        for cat, info in idx.get("categories", {}).items():
            cats[cat] = info.get("count", 0)

    local_count = 0
    local_cats = Counter()
    if KNOWLEDGE_DIR.exists():
        for md in KNOWLEDGE_DIR.rglob("*.md"):
            local_count += 1
            cat = md.parent.name if md.parent != KNOWLEDGE_DIR else "根目录"
            local_cats[cat] += 1

    notion_count = 0
    if NOTION_DIR.exists():
        pages_dir = NOTION_DIR / "pages"
        if pages_dir.exists():
            notion_count = sum(1 for _ in pages_dir.rglob("*.md"))

    print(f"\n{'='*56}")
    print(f"  📊 龍魂知识库统计概览")
    print(f"{'='*56}")
    print(f"  网站索引: {total} 篇")
    print(f"  本地知识: {local_count} 篇")
    print(f"  Notion镜像: {notion_count} 页")
    print(f"  三源合计: {total + local_count + notion_count} 条目")
    print()

    if cats:
        print(f"  ── 分类分布 ──")
        for cat, cnt in cats.most_common():
            bar = '█' * min(cnt, 30)
            print(f"  {cat:12s} {cnt:4d} {bar}")
    print(f"{'='*56}\n")


def list_category(cat_name: str):
    """列出指定分类条目"""
    if not KB_INDEX.exists():
        _log("索引未生成 · 运行 lh_kb_expand.py index", "WARN")
        return

    with open(KB_INDEX) as f:
        idx = json.load(f)

    matched = []
    for art in idx.get("articles", []):
        if cat_name.lower() in art.get("category", "").lower():
            matched.append(art)

    if not matched:
        # 模糊匹配
        for art in idx.get("articles", []):
            title = art.get("title", "")
            if cat_name.lower() in title.lower():
                matched.append(art)

    print(f"\n  📋 分类 '{cat_name}': {len(matched)} 项")
    for art in matched[:20]:
        title = art.get("title", "?")
        source = art.get("source", "?")
        quality = art.get("quality", 0)
        print(f"  [{source}] {title} (质量: {quality})")
    if len(matched) > 20:
        print(f"  ... 还有 {len(matched)-20} 项")
    print()


def list_all_categories():
    """列出所有分类"""
    if not KB_INDEX.exists():
        _log("索引未生成", "WARN")
        return

    with open(KB_INDEX) as f:
        idx = json.load(f)

    print(f"\n  📂 全部分类:")
    for cat, info in idx.get("categories", {}).items():
        cnt = info.get("count", 0)
        print(f"  {cat}: {cnt} 篇")


def build_index():
    """重建三源融合索引"""
    _log("🔨 重建三源索引...")
    import subprocess

    # 调 lh_kb_expand.py 重新建索引
    result = subprocess.run(
        [sys.executable, str(ROOT / "bin" / "lh_kb_expand.py"), "index"],
        capture_output=True, text=True, timeout=300
    )
    if result.returncode == 0:
        _log("索引重建完成", "OK")
    else:
        _log(f"索引重建失败: {result.stderr[:200]}", "ERROR")


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 自然语言知识搜索引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_knowledge_semantic_trigger.py "密码学相关文章"
  python3 bin/lh_knowledge_semantic_trigger.py --stats
  python3 bin/lh_knowledge_semantic_trigger.py --list 算法
  python3 bin/lh_knowledge_semantic_trigger.py --build
        """
    )
    parser.add_argument("query", nargs="?", type=str, help="搜索关键词（自然语言）")
    parser.add_argument("-n", "--limit", type=int, default=30, help="返回结果数 (默认: 30)")
    parser.add_argument("--stats", action="store_true", help="统计概览")
    parser.add_argument("--list", type=str, nargs="?", const="", metavar="分类", help="列出分类条目")
    parser.add_argument("--build", action="store_true", help="重建三源融合索引")
    args = parser.parse_args()

    print(f"\n🐉 龍魂知识搜索引擎 v1.0")
    print(f"   {DNA}\n")

    if args.build:
        build_index()
    elif args.stats or (args.query and args.query.strip().lower() in ["stats", "统计", "概览", "分布"]):
        show_stats()
    elif args.list is not None:
        if args.list:
            list_category(args.list)
        else:
            list_all_categories()
    elif args.query:
        # 先尝试命令匹配
        if not handle_command(args.query):
            results = search(args.query, args.limit)
            if results:
                print(f"\n  🔍 找到 {len(results)} 条结果:\n")
                for i, r in enumerate(results, 1):
                    title = r.get("title", "?")
                    source = r.get("source", "?")
                    origin = r.get("origin", "?")
                    cat = r.get("category", "")
                    quality = r.get("quality", 0)
                    summary = r.get("summary", "")[:120]
                    print(f"  {i:2d}. [{origin}] {title}")
                    print(f"      来源: {source} · 分类: {cat} · 质量: {quality:.1f}")
                    if summary:
                        print(f"      {summary}")
                    print()
            else:
                _log("未找到匹配结果 · 尝试换个说法", "WARN")
                _log("提示: python3 bin/lh_knowledge_semantic_trigger.py --stats 查看有哪些分类", "INFO")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
