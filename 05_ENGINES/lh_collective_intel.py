#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 协同涌现引擎 (Collective Intelligence Engine)
DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-COLLECTIVE-INTEL-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 聚合多用户/多会话访问行为，自动发现共现模式、自组织分类、最佳路径。
      单机版：把不同会话的访问日志聚合成本地群体智能。
      鲲鹏 ARM64 原生：纯 Python + SQLite。
"""

import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / ".state" / "collective_intel"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "collective.sqlite"

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-COLLECTIVE-INTEL-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cooccurrence (
            item_a TEXT,
            item_b TEXT,
            session_count INTEGER DEFAULT 0,
            total_weight REAL DEFAULT 0.0,
            last_at TEXT,
            PRIMARY KEY (item_a, item_b)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            items TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    return conn


class CollectiveIntel:
    """协同涌现引擎"""

    def __init__(self):
        self.conn = _init_db()

    def add_session(self, session_id: str, items: List[str]) -> Dict[str, Any]:
        """添加一个会话的项目共现记录"""
        if not items:
            return {"status": "empty"}
        now = now_iso()
        dedup = sorted(set(items))
        self.conn.execute(
            "INSERT OR REPLACE INTO sessions (session_id, items, created_at) VALUES (?, ?, ?)",
            (session_id, json.dumps(dedup, ensure_ascii=False), now),
        )

        # 更新共现矩阵（无序对）
        for i in range(len(dedup)):
            for j in range(i + 1, len(dedup)):
                a, b = dedup[i], dedup[j]
                if a > b:
                    a, b = b, a
                self.conn.execute(
                    """
                    INSERT INTO cooccurrence (item_a, item_b, session_count, total_weight, last_at)
                    VALUES (?, ?, 1, 1.0, ?)
                    ON CONFLICT(item_a, item_b) DO UPDATE SET
                        session_count = session_count + 1,
                        total_weight = total_weight + 1.0,
                        last_at = excluded.last_at
                    """,
                    (a, b, now),
                )
        self.conn.commit()
        return {"status": "added", "session_id": session_id, "items": len(dedup)}

    def related_items(self, item: str, limit: int = 10) -> List[Dict[str, Any]]:
        """找出与某项目高频共现的项目"""
        cursor = self.conn.execute(
            """
            SELECT item_a, item_b, session_count, total_weight FROM cooccurrence
            WHERE item_a=? OR item_b=?
            ORDER BY total_weight DESC LIMIT ?
            """,
            (item, item, limit * 2),
        )
        results = []
        seen: Set[str] = set()
        for row in cursor:
            a, b, count, weight = row
            other = b if a == item else a
            if other in seen:
                continue
            seen.add(other)
            results.append(
                {
                    "item": other,
                    "cooccurrence": count,
                    "weight": round(weight, 2),
                }
            )
            if len(results) >= limit:
                break
        return results

    def discover_clusters(self, min_support: int = 2) -> List[Dict[str, Any]]:
        """基于共现发现自组织簇（简单连通分量）"""
        cursor = self.conn.execute(
            "SELECT item_a, item_b, total_weight FROM cooccurrence WHERE session_count >= ?",
            (min_support,),
        )
        graph = defaultdict(list)
        weights: Dict[Tuple[str, str], float] = {}
        for a, b, w in cursor:
            graph[a].append(b)
            graph[b].append(a)
            weights[(min(a, b), max(a, b))] = w

        visited: Set[str] = set()
        clusters: List[Dict[str, Any]] = []
        for node in list(graph.keys()):
            if node in visited:
                continue
            stack = [node]
            comp: Set[str] = set()
            internal_weight = 0.0
            while stack:
                cur = stack.pop()
                if cur in visited:
                    continue
                visited.add(cur)
                comp.add(cur)
                for nb in graph.get(cur, []):
                    pair = (min(cur, nb), max(cur, nb))
                    internal_weight += weights.get(pair, 0)
                    if nb not in visited:
                        stack.append(nb)
            if len(comp) >= 2:
                clusters.append(
                    {
                        "id": f"cluster-{len(clusters) + 1}",
                        "size": len(comp),
                        "members": sorted(comp),
                        "internal_weight": round(internal_weight, 2),
                    }
                )
        clusters.sort(key=lambda x: -x["internal_weight"])
        return clusters

    def best_path(self, start: str, end: str) -> List[str]:
        """用 BFS 找共现图上的最佳浏览路径"""
        cursor = self.conn.execute("SELECT item_a, item_b FROM cooccurrence")
        graph = defaultdict(set)
        for a, b in cursor:
            graph[a].add(b)
            graph[b].add(a)

        if start not in graph or end not in graph:
            return []
        queue = [(start, [start])]
        visited = {start}
        while queue:
            cur, path = queue.pop(0)
            if cur == end:
                return path
            for nb in graph.get(cur, set()):
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, path + [nb]))
        return []

    def stats(self) -> Dict[str, Any]:
        c1 = self.conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        c2 = self.conn.execute("SELECT COUNT(*) FROM cooccurrence").fetchone()[0]
        return {
            "sessions": c1,
            "cooccurrence_edges": c2,
            "dna": ENGINE_DNA,
        }


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂协同涌现引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add-session", help="添加会话")
    p_add.add_argument("session_id")
    p_add.add_argument("items", nargs="+")

    p_rel = sub.add_parser("related", help="共现推荐")
    p_rel.add_argument("item")
    p_rel.add_argument("--limit", type=int, default=10)

    p_cluster = sub.add_parser("clusters", help="发现簇")
    p_cluster.add_argument("--min-support", type=int, default=2)

    p_path = sub.add_parser("path", help="最佳路径")
    p_path.add_argument("start")
    p_path.add_argument("end")

    p_stats = sub.add_parser("stats", help="统计")

    args = parser.parse_args()
    ci = CollectiveIntel()

    if args.cmd == "add-session":
        print(json.dumps(ci.add_session(args.session_id, args.items), ensure_ascii=False, indent=2))
    elif args.cmd == "related":
        print(json.dumps(ci.related_items(args.item, args.limit), ensure_ascii=False, indent=2))
    elif args.cmd == "clusters":
        print(json.dumps(ci.discover_clusters(args.min_support), ensure_ascii=False, indent=2))
    elif args.cmd == "path":
        print(json.dumps(ci.best_path(args.start, args.end), ensure_ascii=False, indent=2))
    elif args.cmd == "stats":
        print(json.dumps(ci.stats(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
