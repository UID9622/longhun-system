#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 孤儿文件全文搜索工具
DNA: #龍芯⚡️2026-06-26-ORPHAN-SEARCH-v1.0
"""

import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / "_work" / "dragon_knowledge.db"


def search(query: str, limit: int = 20, project: str | None = None, topic: str | None = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    sql = """
        SELECT f.entry_id, f.file_path, f.file_name, f.title, f.description,
               f.project, f.topics, f.modified_month, f.shield_level, f.bloodline,
               snippet(device_orphan_fts, 5, '【', '】', '...', 64) AS snippet
        FROM device_orphan_fts fts
        JOIN device_orphan_files f ON fts.entry_id = f.entry_id
        WHERE device_orphan_fts MATCH ?
    """
    params = [query]
    
    if project:
        sql += " AND f.project = ?"
        params.append(project)
    if topic:
        sql += " AND f.topics LIKE ?"
        params.append(f"%{topic}%")
    
    sql += " LIMIT ?"
    params.append(limit)
    
    cur.execute(sql, params)
    rows = cur.fetchall()
    
    print(f"搜索 '{query}' 找到 {len(rows)} 个结果:\n")
    for r in rows:
        print(f"📄 {r['file_name']}")
        print(f"   路径: {r['file_path']}")
        print(f"   项目: {r['project']} | 主题: {r['topics']} | 时间: {r['modified_month']}")
        if r['snippet']:
            print(f"   摘要: {r['snippet']}")
        print()
    
    conn.close()


def list_projects():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT project, COUNT(*) as cnt FROM device_orphan_files GROUP BY project ORDER BY cnt DESC")
    print("项目分布:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
    conn.close()


def list_topics():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT topics FROM device_orphan_files")
    from collections import Counter
    counter = Counter()
    for row in cur.fetchall():
        for t in row[0].split(','):
            counter[t.strip()] += 1
    print("主题分布 TOP20:")
    for t, cnt in counter.most_common(20):
        print(f"  {t}: {cnt}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂孤儿文件全文搜索")
    parser.add_argument("query", nargs="?", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=20, help="返回数量")
    parser.add_argument("--project", help="按项目过滤")
    parser.add_argument("--topic", help="按主题过滤")
    parser.add_argument("--projects", action="store_true", help="列出所有项目")
    parser.add_argument("--topics", action="store_true", help="列出所有主题")
    args = parser.parse_args()
    
    if args.projects:
        list_projects()
    elif args.topics:
        list_topics()
    elif args.query:
        search(args.query, args.limit, args.project, args.topic)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
