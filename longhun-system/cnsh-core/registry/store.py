"""
CNSH L3 Registry Store — SQLite 持久化层

数据库路径：~/.longhun/registry.db
两张表：
  registry_entries   — 所有条目（私域+公域）
  ext_registry       — 扩展快查索引（视图）

Author: 诸葛鑫 (UID9622)
"""

import sqlite3
import os
import time
from typing import Optional, List

from .entry import RegistryEntry, Scope

DB_PATH = os.path.expanduser("~/.longhun/registry.db")


# ── 连接 ──────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── 初始化 ────────────────────────────────────────────────────────

def init_db():
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS registry_entries (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_code     TEXT UNIQUE NOT NULL,
                scope        TEXT NOT NULL,
                owner_gpg    TEXT DEFAULT '',
                timestamp    REAL DEFAULT 0,
                content_hash TEXT DEFAULT '',
                prev_entry   TEXT DEFAULT '',
                ext_id       TEXT DEFAULT '',
                ext_type     TEXT DEFAULT '',
                handler_path TEXT DEFAULT '',
                version      TEXT DEFAULT '1.0.0',
                description  TEXT DEFAULT '',
                gpg_sig      TEXT DEFAULT '',
                active       INTEGER DEFAULT 1,
                entry_hash   TEXT DEFAULT '',
                created_at   REAL DEFAULT 0
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ext_id   ON registry_entries(ext_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_scope    ON registry_entries(scope)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_active   ON registry_entries(active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts       ON registry_entries(timestamp)")
        conn.commit()


# ── 写入 ──────────────────────────────────────────────────────────

def save_entry(entry: RegistryEntry) -> RegistryEntry:
    """保存/覆盖条目，自动计算 entry_hash"""
    entry.entry_hash = entry.compute_entry_hash()
    with _get_conn() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO registry_entries
            (dna_code, scope, owner_gpg, timestamp, content_hash, prev_entry,
             ext_id, ext_type, handler_path, version, description, gpg_sig,
             active, entry_hash, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            entry.dna_code, entry.scope.value, entry.owner_gpg, entry.timestamp,
            entry.content_hash, entry.prev_entry, entry.ext_id, entry.ext_type,
            entry.handler_path, entry.version, entry.description, entry.gpg_sig,
            int(entry.active), entry.entry_hash, entry.created_at,
        ))
        conn.commit()
    return entry


def deactivate_entry(dna_code: str) -> bool:
    """停用条目（不删除，保留DNA）"""
    with _get_conn() as conn:
        c = conn.execute(
            "UPDATE registry_entries SET active=0 WHERE dna_code=?", (dna_code,)
        )
        conn.commit()
        return c.rowcount > 0


# ── 查询 ──────────────────────────────────────────────────────────

def lookup_ext(ext_id: str) -> Optional[RegistryEntry]:
    """按 ext_id 查找最新激活的扩展处理器"""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM registry_entries WHERE ext_id=? AND active=1 ORDER BY created_at DESC LIMIT 1",
            (ext_id,)
        ).fetchone()
    return _row_to_entry(row) if row else None


def lookup_dna(dna_code: str) -> Optional[RegistryEntry]:
    """按 DNA 码查找条目"""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM registry_entries WHERE dna_code=?",
            (dna_code,)
        ).fetchone()
    return _row_to_entry(row) if row else None


def list_extensions(ext_type: str = "", active_only: bool = True, limit: int = 100) -> List[RegistryEntry]:
    """列出扩展条目"""
    sql = "SELECT * FROM registry_entries WHERE ext_id != ''"
    params = []
    if active_only:
        sql += " AND active=1"
    if ext_type:
        sql += " AND ext_type=?"
        params.append(ext_type.upper())
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with _get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_entry(r) for r in rows]


def list_public_entries(limit: int = 50) -> List[RegistryEntry]:
    """列出最新公域条目（用于链审计）"""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM registry_entries WHERE scope='PUBLIC' ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [_row_to_entry(r) for r in rows]


def get_latest_public_dna() -> str:
    """获取最新公域条目的 DNA 码，用于构建 prev_entry（链式）"""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT dna_code FROM registry_entries WHERE scope='PUBLIC' ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
    return row["dna_code"] if row else "GENESIS"


# ── 链追溯 ────────────────────────────────────────────────────────

def get_chain(dna_code: str, max_depth: int = 20) -> List[RegistryEntry]:
    """沿 prev_entry 向前追溯，返回链条（从新到旧）"""
    chain = []
    current = dna_code
    seen = set()
    while current and current != "GENESIS" and len(chain) < max_depth:
        if current in seen:
            break
        seen.add(current)
        entry = lookup_dna(current)
        if not entry:
            break
        chain.append(entry)
        current = entry.prev_entry
    return chain


# ── 链完整性验证 ──────────────────────────────────────────────────

def verify_chain() -> dict:
    """验证整个注册表的哈希完整性"""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM registry_entries ORDER BY timestamp ASC"
        ).fetchall()
    entries = [_row_to_entry(r) for r in rows]

    broken = []
    for e in entries:
        expected = e.compute_entry_hash()
        if e.entry_hash and e.entry_hash != expected:
            broken.append({
                "dna_code": e.dna_code,
                "scope":    str(e.scope),
                "reason":   "hash_mismatch",
                "stored":   e.entry_hash[:16],
                "expected": expected[:16],
            })

    return {
        "total":          len(entries),
        "public_count":   sum(1 for e in entries if e.scope == Scope.PUBLIC or e.scope.value == "PUBLIC"),
        "private_count":  sum(1 for e in entries if e.scope == Scope.PRIVATE or e.scope.value == "PRIVATE"),
        "broken":         len(broken),
        "integrity":      "🟢 完整" if not broken else "🔴 链条受损",
        "broken_entries": broken,
    }


# ── 内部转换 ──────────────────────────────────────────────────────

def _row_to_entry(row) -> RegistryEntry:
    # 兼容旧数据中 "Scope.PRIVATE" 格式
    raw_scope = row["scope"] or "PRIVATE"
    if "." in raw_scope:
        raw_scope = raw_scope.split(".")[-1]
    return RegistryEntry(
        dna_code     = row["dna_code"],
        scope        = Scope(raw_scope),
        owner_gpg    = row["owner_gpg"] or "",
        timestamp    = float(row["timestamp"] or 0),
        content_hash = row["content_hash"] or "",
        prev_entry   = row["prev_entry"] or "",
        ext_id       = row["ext_id"] or "",
        ext_type     = row["ext_type"] or "",
        handler_path = row["handler_path"] or "",
        version      = row["version"] or "1.0.0",
        description  = row["description"] or "",
        gpg_sig      = row["gpg_sig"] or "",
        active       = bool(row["active"]),
        entry_hash   = row["entry_hash"] or "",
        created_at   = float(row["created_at"] or 0),
    )


# 启动时初始化
init_db()
