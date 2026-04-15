#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notion_page_registry.py · Notion页面注册表 · app.py接口层 v1.0
DNA: #龍芯⚡️2026-04-07-NOTION-PAGE-REGISTRY-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

用途: app.py及任何模块调用Notion页面时的统一入口
数据源: ~/longhun-system/notion-index/notion_pages.json（30核心页面）

调用方式:
  from notion_page_registry import find_page, get_page_id, get_palace_pages

  page = find_page("草日志")
  # → {"id": "b35faf46...", "title": "...", "url": "...", "palace": 4, ...}

  pid = get_page_id("主控")
  # → "2507125a..."

  pages = get_palace_pages(8)  # 8宫·艮·算法维
  # → [{"title": "三才算法...", ...}, ...]
"""

import json
import re
from pathlib import Path
from typing import Optional

# ══════════════════════════════════════════════
# 数据加载
# ══════════════════════════════════════════════

_REGISTRY_PATH = Path.home() / "longhun-system" / "notion-index" / "notion_pages.json"
_REGISTRY: dict = {}
_PAGES: list = []

def _load():
    global _REGISTRY, _PAGES
    if _REGISTRY:
        return  # 已加载
    try:
        with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
            _REGISTRY = json.load(f)
        _PAGES = _REGISTRY.get("pages", [])
    except FileNotFoundError:
        _PAGES = []
    except Exception as e:
        print(f"[注册表] 加载失败: {e}")
        _PAGES = []

# ══════════════════════════════════════════════
# 核心查找函数
# ══════════════════════════════════════════════

def find_page(query: str) -> Optional[dict]:
    """
    模糊搜索页面·返回最佳匹配。
    匹配优先级: title全匹配 > title包含 > keywords包含 > purpose包含
    """
    _load()
    q = query.lower()

    # 1. 标题精确匹配
    for p in _PAGES:
        if q == p.get("title", "").lower():
            return p

    # 2. 标题包含
    candidates = []
    for p in _PAGES:
        title = p.get("title", "").lower()
        if q in title:
            candidates.append((len(q) / max(len(title), 1), p))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    # 3. keywords包含
    for p in _PAGES:
        for kw in p.get("keywords", []):
            if q in kw.lower() or kw.lower() in q:
                return p

    # 4. purpose包含
    for p in _PAGES:
        if q in p.get("purpose", "").lower():
            return p

    return None

def get_page_id(query: str) -> Optional[str]:
    """快捷函数·只返回页面ID（短格式）"""
    page = find_page(query)
    return page["id"] if page else None

def get_page_url(query: str) -> Optional[str]:
    """快捷函数·只返回Notion URL"""
    page = find_page(query)
    return page["url"] if page else None

def get_palace_pages(palace: int) -> list:
    """返回指定洛书宫位的所有页面"""
    _load()
    return [p for p in _PAGES if p.get("palace") == palace]

def get_all_pages() -> list:
    """返回所有注册页面"""
    _load()
    return list(_PAGES)

def get_palace_summary() -> dict:
    """返回九宫分布统计"""
    _load()
    summary = _REGISTRY.get("palace_summary", {})
    if not summary:
        from collections import Counter
        counts = Counter(p.get("palace") for p in _PAGES)
        summary = {str(k): v for k, v in counts.items()}
    return summary

def search_pages(query: str, limit: int = 5) -> list:
    """
    全文搜索·返回最多limit条结果（按相关度排序）
    """
    _load()
    q = query.lower()
    scored = []
    for p in _PAGES:
        score = 0
        title = p.get("title", "").lower()
        if q in title:
            score += 10
        for kw in p.get("keywords", []):
            if q in kw.lower():
                score += 3
        if q in p.get("purpose", "").lower():
            score += 2
        for tag in p.get("tags", []):
            if q in tag.lower():
                score += 1
        if score > 0:
            scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:limit]]

# ══════════════════════════════════════════════
# 快捷常量（高频页面直接引用）
# ══════════════════════════════════════════════

class Pages:
    """常用页面ID常量（从notion_pages.json加载）"""

    @classmethod
    def _get(cls, query):
        return get_page_id(query)

    # P0核心
    SHIELD_V13       = "6c03f9adafd94ce8bf98f8439eb9dbbf"  # 护盾v1.3
    AI_MAIN_CONTROL  = "2d87125a9c9f802889e2e18002f7cf4f"  # AI主控操作台
    MAIN_CONTROL     = "2507125a9c9f80d2b214c07deced0f0f"  # 主控操作台

    # 核心算法
    SANCAI_ENGINE    = "a1821c71"  # 三才流场·MCP自适应引擎 v4.0
    SANCAI_ALGO      = "9046e804"  # 三才算法·龍魂系统统一算法根基

    # 日志/草日志
    DIARY            = "b35faf46-2bc0-42aa-9de5-192520180728"

    # 规则中心
    RULES_CENTER     = "16e2a2e5-1334-450a-a5a6-bdf742b97ade"

# ══════════════════════════════════════════════
# CLI测试入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    _load()
    total = len(_PAGES)
    print(f"\n📚 Notion页面注册表 v1.0 · 共{total}页")
    print(f"DNA: #龍芯⚡️2026-04-07-NOTION-PAGE-REGISTRY-v1.0")
    print("=" * 60)

    queries = sys.argv[1:] or ["三才", "草日志", "护盾", "主控", "元宇宙", "指令集"]

    for q in queries:
        page = find_page(q)
        if page:
            print(f"\n✅ [{q}] → {page['title'][:40]}")
            print(f"   ID: {page['id']} | 宫: {page['palace']}宫 | URL: {page['url'][:50]}")
        else:
            print(f"\n❌ [{q}] 未找到")

    print(f"\n九宫分布: {get_palace_summary()}")
    print(f"\n🟢 注册表就绪 · 数据源: {_REGISTRY_PATH}")
