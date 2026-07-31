#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂计算机科学知识库嵌入式模块
DNA: #龍芯⚡️2026-07-01-LONGHUN-CS-KB-EMBED-v1.0

将增强后的 CS KB SQLite 数据库接入龍魂算法体系，提供查询、检索与统计能力。
"""

import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Optional

DNA = "#龍芯⚡️2026-07-01-LONGHUN-CS-KB-EMBED-v1.0"

DEFAULT_DB_PATH = Path("/Users/zuimeidedeyihan/longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db")

# Columns that were JSON-encoded before insertion
_JSON_COLUMNS = {"persona_route"}


def _maybe_json(value: Any) -> Any:
    """Try to parse JSON, otherwise return raw value."""
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    result = {}
    for key in row.keys():
        value = row[key]
        if key in _JSON_COLUMNS:
            result[key] = _maybe_json(value)
        else:
            result[key] = value
    return result


def load_db(db_path: Optional[str | Path] = None) -> sqlite3.Connection:
    """Open the enhanced CS KB SQLite database."""
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    if not path.exists():
        raise FileNotFoundError(f"CS KB database not found: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query_by_id(card_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[dict[str, Any]]:
    """Fetch a single knowledge card by its 知识卡片ID."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        row = conn.execute('SELECT * FROM cs_kb WHERE "card_id" = ?', (str(card_id),)).fetchone()
        return _row_to_dict(row) if row else None
    finally:
        if should_close:
            conn.close()


def query_by_category(category: str, limit: int = 50, conn: Optional[sqlite3.Connection] = None) -> list[dict[str, Any]]:
    """Return cards matching an exact 分类 value."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        rows = conn.execute(
            'SELECT * FROM cs_kb WHERE "category" = ? LIMIT ?',
            (category, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        if should_close:
            conn.close()


def query_by_status(status: str, conn: Optional[sqlite3.Connection] = None) -> list[dict[str, Any]]:
    """Return cards matching an exact 学习状态 value, e.g. '已完成'."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        rows = conn.execute('SELECT * FROM cs_kb WHERE "status" = ?', (status,)).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        if should_close:
            conn.close()


def query_by_dr(dr_str: str, conn: Optional[sqlite3.Connection] = None) -> list[dict[str, Any]]:
    """Return cards whose dr·五行·宫位 starts with the given dr_str, e.g. 'DR=3'."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        rows = conn.execute(
            'SELECT * FROM cs_kb WHERE "dr_wuxing_gong" LIKE ?',
            (f"{dr_str}%",),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        if should_close:
            conn.close()


def query_by_keyword(keyword: str, limit: int = 50, conn: Optional[sqlite3.Connection] = None) -> list[dict[str, Any]]:
    """Return cards whose name/description/context_trigger contain keyword (LIKE)."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        pattern = f"%{keyword}%"
        rows = conn.execute(
            '''SELECT * FROM cs_kb
               WHERE "name" LIKE ?
                  OR "description" LIKE ?
                  OR "context_trigger" LIKE ?
               LIMIT ?''',
            (pattern, pattern, pattern, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        if should_close:
            conn.close()


def get_formula(card_id: str, conn: Optional[sqlite3.Connection] = None) -> str:
    """Return the 算法公式 for a given card."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        row = conn.execute(
            'SELECT "formula" FROM cs_kb WHERE "card_id" = ?',
            (str(card_id),),
        ).fetchone()
        return row["formula"] if row else ""
    finally:
        if should_close:
            conn.close()


def get_routing_params(card_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[dict[str, Any]]:
    """Return parsed 路由回调参数 as a dict, or None if empty."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        row = conn.execute(
            'SELECT "routing_params" FROM cs_kb WHERE "card_id" = ?',
            (str(card_id),),
        ).fetchone()
        if not row or not row["routing_params"]:
            return None
        return json.loads(row["routing_params"])
    except Exception:
        return None
    finally:
        if should_close:
            conn.close()


def get_py_example(card_id: str, conn: Optional[sqlite3.Connection] = None) -> str:
    """Return the PY代码示例 snippet for a given card."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        row = conn.execute(
            'SELECT "py_example" FROM cs_kb WHERE "card_id" = ?',
            (str(card_id),),
        ).fetchone()
        return row["py_example"] if row else ""
    finally:
        if should_close:
            conn.close()


def search(q: str, limit: int = 20, conn: Optional[sqlite3.Connection] = None) -> list[dict[str, Any]]:
    """Full-text search across name, description and context_trigger using FTS5.

    Falls back to LIKE if FTS5 is unavailable or the query fails.
    """
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        # Try FTS5 first
        try:
            rows = conn.execute(
                '''SELECT k.* FROM cs_kb k
                   JOIN cs_kb_fts f ON k.rowid = f.rowid
                   WHERE cs_kb_fts MATCH ?
                   LIMIT ?''',
                (q, limit),
            ).fetchall()
            if rows:
                return [_row_to_dict(r) for r in rows]
        except Exception:
            pass

        # Fallback LIKE search
        pattern = f"%{q}%"
        rows = conn.execute(
            '''SELECT * FROM cs_kb
               WHERE "name" LIKE ?
                  OR "description" LIKE ?
                  OR "context_trigger" LIKE ?
               LIMIT ?''',
            (pattern, pattern, pattern, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        if should_close:
            conn.close()


def embed_summary(conn: Optional[sqlite3.Connection] = None) -> dict[str, Any]:
    """Return aggregate statistics about the embedded knowledge base."""
    should_close = conn is None
    if conn is None:
        conn = load_db()
    try:
        total = conn.execute('SELECT COUNT(*) FROM cs_kb').fetchone()[0]

        def agg(column: str) -> dict[str, int]:
            rows = conn.execute(
                f'SELECT "{column}", COUNT(*) FROM cs_kb GROUP BY "{column}"'
            ).fetchall()
            return {row[0]: row[1] for row in rows}

        def non_empty(column: str) -> int:
            return conn.execute(
                f'SELECT COUNT(*) FROM cs_kb WHERE "{column}" IS NOT NULL AND "{column}" != ""'
            ).fetchone()[0]

        return {
            "dna": DNA,
            "total_records": total,
            "by_category": agg("category"),
            "by_status": agg("status"),
            "by_architecture_layer": agg("architecture_layer"),
            "by_tri_color_audit": agg("tri_color_audit"),
            "with_formula": non_empty("formula"),
            "with_routing_params": non_empty("routing_params"),
            "with_py_example": non_empty("py_example"),
        }
    finally:
        if should_close:
            conn.close()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"龍魂 CS KB 嵌入式模块\n{DNA}\n")

    stats = embed_summary()
    print("=== 统计 ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n=== 示例查询: ID=79 逻辑回归 ===")
    card = query_by_id("79")
    if card:
        print(f"知识点: {card['name']}")
        print(f"公式: {get_formula('79')}")
        print(f"路由参数: {get_routing_params('79')}")
        print("代码示例:\n" + get_py_example("79"))

    print("\n=== 分类查询示例: 数据与人工智能 (前3条) ===")
    for r in query_by_category("数据与人工智能", limit=3):
        print(f"  [{r['card_id']}] {r['name']} | {r['status']}")

    print("\n=== 关键词搜索: '路由' (前5条) ===")
    for r in search("路由", limit=5):
        print(f"  [{r['card_id']}] {r['name']}")
