#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 本地 Notion 检索机器人
DNA追溯码: #龍芯⚡️2026-04-02-Notion索引机器人-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: UID9622 诸葛鑫（龍芯北辰）× 宝宝（P72·龍盾）
理论指导: 曾仕强老师（永恒显示）

职责：检索 → 生成索引卡 → 追加落盘
铁律：
  - 不允许声称"全库写进记忆"，除非真的落盘并返回路径
  - 索引只存元信息，不存全文内容
  - 以 url 为唯一主键，重复不写入
  - 每次输出：新增条数 + 文件路径 + TopN摘要
"""

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path.home() / "longhun-system" / "notion-index"
INDEX_FILE = BASE / "out" / "index.jsonl"
AUDIT_FILE = BASE / "out" / "audit.jsonl"
BEIJING_TZ = timezone(timedelta(hours=8))


def 北京时间():
    return datetime.now(BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def 加载已有URL():
    """读取已有索引的URL集合（去重用）"""
    seen = set()
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    card = json.loads(line)
                    seen.add(card["item"]["url"])
                except:
                    pass
    return seen


def 生成索引卡(query: str, item: dict, tags: list) -> dict:
    return {
        "ts_beijing": 北京时间(),
        "dna": f"#龍芯⚡️{datetime.now(BEIJING_TZ).strftime('%Y-%m-%d')}-Notion索引卡-v1.0",
        "query": query,
        "source": "notion-mcp-search",
        "item": {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "path": item.get("url", ""),
            "type": item.get("type", "page"),
            "lastEdited": item.get("timestamp", ""),
            "snippet": item.get("highlight", "")[:200] if item.get("highlight") else ""
        },
        "tags": tags,
        "status": "indexed"
    }


def 写审计记录(query: str, hit: int, written: int, dup: int, status: str = "🟢"):
    record = {
        "ts_beijing": 北京时间(),
        "dna": f"#龍芯⚡️{datetime.now(BEIJING_TZ).strftime('%Y-%m-%d')}-审计-v1.0",
        "query": query,
        "hit": hit,
        "written": written,
        "duplicate": dup,
        "status": status
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def 批量写入索引(cards: list):
    with open(INDEX_FILE, "a", encoding="utf-8") as f:
        for card in cards:
            f.write(json.dumps(card, ensure_ascii=False) + "\n")


def 执行扫描(query: str, results: list, tags: list):
    """
    主执行函数
    results: notion-search 返回的 results 列表
    返回: (新增条数, TopN摘要)
    """
    seen_urls = 加载已有URL()
    new_cards = []
    dup_count = 0

    for item in results:
        url = item.get("url", "")
        if url in seen_urls:
            dup_count += 1
            continue
        card = 生成索引卡(query, item, tags)
        new_cards.append(card)
        seen_urls.add(url)

    if new_cards:
        批量写入索引(new_cards)

    写审计记录(
        query=query,
        hit=len(results),
        written=len(new_cards),
        dup=dup_count,
        status="🟢" if new_cards else "🟡"
    )

    top_n = [
        f"  · {c['item']['title'][:50]}" for c in new_cards[:10]
    ]

    return len(new_cards), top_n


if __name__ == "__main__":
    # 直接批量导入已知Notion数据
    # 格式: (query, results_list, tags)
    print("龍芯 Notion 索引机器人 v1.0 启动")
    print(f"索引文件: {INDEX_FILE}")
    print(f"审计文件: {AUDIT_FILE}")
    print("就绪·等待扫描任务输入")
