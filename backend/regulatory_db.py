"""
龍魂统一监管API · 数据库层
DNA: #龍芯⚡️2026-07-12-REGULATORY-DB-v2.0 · 三层透明模型

扩展数据库支持监管透明度功能:
- 监管者认证 (regulatory_auditors)
- 操作全量记录+哈希链 (operation_log, prev_hash)
- 文件变更追踪 (file_change_log)
- 文档注册表+主权分级 (document_registry, sovereignty_level 1/2/3)
- 监管访问日志 (regulatory_access_log)
- 主权策略 (sovereignty_policy)
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import DB_PATH, DATA_DIR
from .database import get_connection, now_iso, ensure_db


REGULATORY_SCHEMA = """
-- 监管者认证表
CREATE TABLE IF NOT EXISTS regulatory_auditors (
    auditor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    organization TEXT DEFAULT '',
    auth_key_hash TEXT NOT NULL UNIQUE,
    access_level TEXT DEFAULT 'readonly' CHECK(access_level IN ('readonly','full')),
    created_at TEXT NOT NULL,
    last_access TEXT,
    access_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active' CHECK(status IN ('active','suspended','revoked')),
    notes TEXT DEFAULT ''
);

-- 操作全量记录 (v2: +哈希链 prev_hash，保证不可篡改可验证)
CREATE TABLE IF NOT EXISTS operation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    operation_type TEXT NOT NULL,
    source TEXT NOT NULL,
    target TEXT DEFAULT '',
    detail TEXT DEFAULT '',
    file_path TEXT DEFAULT '',
    old_hash TEXT DEFAULT '',
    new_hash TEXT DEFAULT '',
    diff_summary TEXT DEFAULT '',
    operator_uid TEXT DEFAULT '',
    operator_ip TEXT DEFAULT '',
    session_id TEXT DEFAULT '',
    dna_trace TEXT DEFAULT '',
    prev_hash TEXT DEFAULT '',
    chain_hash TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_oplog_ts ON operation_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_oplog_type ON operation_log(operation_type);
CREATE INDEX IF NOT EXISTS idx_oplog_file ON operation_log(file_path);

-- 文件变更日志
CREATE TABLE IF NOT EXISTS file_change_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('created','modified','deleted','moved','renamed')),
    file_path TEXT NOT NULL,
    old_path TEXT,
    file_type TEXT,
    file_size INTEGER,
    sha256 TEXT,
    previous_sha256 TEXT,
    detected_by TEXT DEFAULT 'daemon',
    sovereignty_level INTEGER DEFAULT 2
);

CREATE INDEX IF NOT EXISTS idx_fclog_ts ON file_change_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_fclog_path ON file_change_log(file_path);

-- 文档注册表 (v2: +sovereignty_level 三层主权分级 1=公开 2=透明 3=私有不可碰)
CREATE TABLE IF NOT EXISTS document_registry (
    doc_id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL UNIQUE,
    doc_type TEXT NOT NULL,
    title TEXT DEFAULT '',
    status TEXT DEFAULT 'draft' CHECK(status IN ('draft','review','published','archived','fragment')),
    word_count INTEGER DEFAULT 0,
    created_at TEXT,
    modified_at TEXT,
    last_indexed_at TEXT NOT NULL,
    content_hash TEXT,
    tags TEXT DEFAULT '[]',
    meta_json TEXT DEFAULT '{}',
    sovereignty_level INTEGER DEFAULT 2 CHECK(sovereignty_level IN (1,2,3)),
    is_private_content INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_doc_type ON document_registry(doc_type);
CREATE INDEX IF NOT EXISTS idx_doc_status ON document_registry(status);
CREATE INDEX IF NOT EXISTS idx_doc_path ON document_registry(file_path);
-- idx_doc_sov 在迁移函数中创建（需要列先存在）

-- 监管访问日志
CREATE TABLE IF NOT EXISTS regulatory_access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    auditor_id TEXT NOT NULL,
    access_type TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    query_params TEXT DEFAULT '',
    result_count INTEGER DEFAULT 0,
    ip_address TEXT DEFAULT '',
    FOREIGN KEY (auditor_id) REFERENCES regulatory_auditors(auditor_id)
);

CREATE INDEX IF NOT EXISTS idx_raccess_ts ON regulatory_access_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_raccess_aid ON regulatory_access_log(auditor_id);

-- 主权策略表 (记录每次主权边界决策)
CREATE TABLE IF NOT EXISTS sovereignty_policy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    policy_type TEXT NOT NULL,
    target TEXT DEFAULT '',
    decision TEXT NOT NULL,
    reason TEXT DEFAULT '',
    effective_from TEXT,
    effective_until TEXT,
    created_by TEXT DEFAULT 'SYSTEM',
    dna_trace TEXT DEFAULT ''
);

-- 数据库迁移：为旧表添加新列（如果不存在）
"""

def _migrate_regulatory_db():
    """安全迁移：为旧表添加 v2 新增列。"""
    migrations = [
        ("operation_log", "prev_hash", "TEXT DEFAULT ''"),
        ("operation_log", "chain_hash", "TEXT DEFAULT ''"),
        ("document_registry", "sovereignty_level", "INTEGER DEFAULT 2"),
        ("document_registry", "is_private_content", "INTEGER DEFAULT 0"),
        ("file_change_log", "sovereignty_level", "INTEGER DEFAULT 2"),
    ]
    with get_connection() as conn:
        for table, col, col_def in migrations:
            try:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}")
            except sqlite3.OperationalError:
                pass  # 列已存在
        # 创建 sovereignty_level 索引（列存在后才能建）
        try:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_doc_sov ON document_registry(sovereignty_level)")
        except sqlite3.OperationalError:
            pass
        # 尝试为 sovereignty_policy 创建索引
        try:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_spolicy_type ON sovereignty_policy(policy_type)")
        except sqlite3.OperationalError:
            pass
        conn.commit()


def init_regulatory_db():
    """初始化监管相关数据库表。"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.executescript(REGULATORY_SCHEMA)
        conn.commit()
    # v2 迁移
    _migrate_regulatory_db()


def create_auditor(auditor_id: str, name: str, auth_key_hash: str, 
                   organization: str = "", access_level: str = "readonly") -> dict:
    """创建监管者账号。"""
    with get_connection() as conn:
        try:
            conn.execute(
                "INSERT INTO regulatory_auditors (auditor_id, name, organization, auth_key_hash, access_level, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (auditor_id, name, organization, auth_key_hash, access_level, now_iso())
            )
            conn.commit()
            return {"ok": True, "auditor_id": auditor_id}
        except sqlite3.IntegrityError as e:
            return {"ok": False, "error": str(e)}


def get_auditor_by_key_hash(auth_key_hash: str) -> Optional[dict]:
    """通过密钥哈希查找监管者。"""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM regulatory_auditors WHERE auth_key_hash = ? AND status = 'active'",
            (auth_key_hash,)
        ).fetchone()
        return dict(row) if row else None


def record_auditor_access(auditor_id: str) -> None:
    """记录监管者访问。"""
    with get_connection() as conn:
        conn.execute(
            "UPDATE regulatory_auditors SET last_access = ?, access_count = access_count + 1 WHERE auditor_id = ?",
            (now_iso(), auditor_id)
        )
        conn.commit()


def log_regulatory_access(auditor_id: str, access_type: str, endpoint: str,
                          query_params: str = "", result_count: int = 0, ip: str = "") -> None:
    """记录监管访问日志。"""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO regulatory_access_log (timestamp, auditor_id, access_type, endpoint, query_params, result_count, ip_address) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (now_iso(), auditor_id, access_type, endpoint, query_params, result_count, ip)
        )
        conn.commit()


def log_operation(op_type: str, source: str, target: str = "", detail: str = "",
                  file_path: str = "", old_hash: str = "", new_hash: str = "",
                  diff_summary: str = "", operator_uid: str = "", operator_ip: str = "",
                  session_id: str = "", dna_trace: str = "") -> None:
    """记录操作到全量操作日志。v2: 附加哈希链。"""
    import hashlib as _hashlib
    with get_connection() as conn:
        # 获取前一行的 id 和 chain_hash 用于哈希链
        prev = conn.execute(
            "SELECT id, chain_hash, timestamp FROM operation_log ORDER BY id DESC LIMIT 1"
        ).fetchone()
        prev_hash = prev["chain_hash"] if prev and prev["chain_hash"] else "GENESIS"
        prev_id = prev["id"] if prev else 0
        
        # 构建当前行数据用于计算链哈希
        raw = f"{now_iso()}|{op_type}|{source}|{target}|{detail}|{file_path}|{old_hash}|{new_hash}|{diff_summary}|{operator_uid}|{operator_ip}|{session_id}|{dna_trace}|{prev_hash}"
        chain_hash = _hashlib.sha256(raw.encode()).hexdigest()
        
        conn.execute(
            "INSERT INTO operation_log (timestamp, operation_type, source, target, detail, "
            "file_path, old_hash, new_hash, diff_summary, operator_uid, operator_ip, session_id, "
            "dna_trace, prev_hash, chain_hash) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (now_iso(), op_type, source, target, detail, file_path, old_hash, new_hash,
             diff_summary, operator_uid, operator_ip, session_id, dna_trace, prev_hash, chain_hash)
        )
        conn.commit()


def log_file_change(event_type: str, file_path: str, old_path: str = None,
                    file_type: str = "", file_size: int = 0, sha256: str = "",
                    previous_sha256: str = "", detected_by: str = "daemon") -> None:
    """记录文件变更。"""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO file_change_log (timestamp, event_type, file_path, old_path, file_type, "
            "file_size, sha256, previous_sha256, detected_by) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (now_iso(), event_type, file_path, old_path, file_type, file_size, sha256, previous_sha256, detected_by)
        )
        conn.commit()


def get_operations(limit: int = 100, offset: int = 0, op_type: str = None,
                   source: str = None, file_path: str = None,
                   from_ts: str = None, to_ts: str = None) -> list:
    """查询操作日志。"""
    with get_connection() as conn:
        query = "SELECT * FROM operation_log WHERE 1=1"
        params = []
        if op_type:
            query += " AND operation_type = ?"
            params.append(op_type)
        if source:
            query += " AND source LIKE ?"
            params.append(f"%{source}%")
        if file_path:
            query += " AND file_path LIKE ?"
            params.append(f"%{file_path}%")
        if from_ts:
            query += " AND timestamp >= ?"
            params.append(from_ts)
        if to_ts:
            query += " AND timestamp <= ?"
            params.append(to_ts)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def get_file_changes(limit: int = 100, offset: int = 0, event_type: str = None,
                     file_path: str = None, from_ts: str = None, to_ts: str = None) -> list:
    """查询文件变更日志。"""
    with get_connection() as conn:
        query = "SELECT * FROM file_change_log WHERE 1=1"
        params = []
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        if file_path:
            query += " AND file_path LIKE ?"
            params.append(f"%{file_path}%")
        if from_ts:
            query += " AND timestamp >= ?"
            params.append(from_ts)
        if to_ts:
            query += " AND timestamp <= ?"
            params.append(to_ts)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def get_documents(doc_type: str = None, status: str = None, 
                  limit: int = 100, offset: int = 0,
                  search: str = None) -> list:
    """查询文档注册表。"""
    with get_connection() as conn:
        query = "SELECT * FROM document_registry WHERE 1=1"
        params = []
        if doc_type:
            query += " AND doc_type = ?"
            params.append(doc_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND (title LIKE ? OR file_path LIKE ? OR tags LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        query += " ORDER BY modified_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def upsert_document(file_path: str, doc_type: str, title: str = "", 
                    status: str = "draft", word_count: int = 0,
                    content_hash: str = "", tags: str = "[]", meta_json: str = "{}",
                    sovereignty_level: int = 2, is_private_content: int = 0) -> dict:
    """插入或更新文档注册。v2: +主权分级。"""
    import hashlib
    doc_id = hashlib.sha256(file_path.encode()).hexdigest()[:16]
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM document_registry WHERE file_path = ?", (file_path,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE document_registry SET doc_type=?, title=?, status=?, word_count=?, "
                "modified_at=?, last_indexed_at=?, content_hash=?, tags=?, meta_json=?, "
                "sovereignty_level=?, is_private_content=? "
                "WHERE file_path=?",
                (doc_type, title, status, word_count, now_iso(), now_iso(), 
                 content_hash, tags, meta_json, sovereignty_level, is_private_content, file_path)
            )
        else:
            conn.execute(
                "INSERT INTO document_registry (doc_id, file_path, doc_type, title, status, "
                "word_count, created_at, modified_at, last_indexed_at, content_hash, tags, "
                "meta_json, sovereignty_level, is_private_content) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (doc_id, file_path, doc_type, title, status, word_count, 
                 now_iso(), now_iso(), now_iso(), content_hash, tags, meta_json,
                 sovereignty_level, is_private_content)
            )
        conn.commit()
        return {"ok": True, "doc_id": doc_id, "file_path": file_path}


def verify_regulatory_hash_chain() -> dict:
    """验证操作日志的哈希链完整性。"""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, timestamp, operation_type, source, target, detail, file_path, "
            "old_hash, new_hash, diff_summary, operator_uid, operator_ip, session_id, "
            "dna_trace, prev_hash, chain_hash "
            "FROM operation_log ORDER BY id ASC"
        ).fetchall()
    
    if not rows:
        return {"ok": True, "chain_length": 0, "status": "empty", "violations": []}
    
    violations = []
    expected_prev = "GENESIS"
    
    for row in rows:
        row_dict = dict(row)
        # 验证 prev_hash 链
        if row_dict["prev_hash"] != expected_prev and row_dict["prev_hash"] != "":
            violations.append({
                "id": row_dict["id"],
                "type": "broken_prev_hash",
                "expected": expected_prev,
                "actual": row_dict["prev_hash"],
            })
        # 重新计算 chain_hash
        import hashlib as _h
        raw = (
            f"{row_dict['timestamp']}|{row_dict['operation_type']}|{row_dict['source']}|"
            f"{row_dict['target']}|{row_dict['detail']}|{row_dict['file_path']}|"
            f"{row_dict['old_hash']}|{row_dict['new_hash']}|{row_dict['diff_summary']}|"
            f"{row_dict['operator_uid']}|{row_dict['operator_ip']}|{row_dict['session_id']}|"
            f"{row_dict['dna_trace']}|{expected_prev}"
        )
        recomputed = _h.sha256(raw.encode()).hexdigest()
        if row_dict["chain_hash"] and recomputed != row_dict["chain_hash"]:
            violations.append({
                "id": row_dict["id"],
                "type": "tampered_chain_hash",
                "expected": recomputed,
                "actual": row_dict["chain_hash"],
            })
        expected_prev = row_dict["chain_hash"]
    
    return {
        "ok": len(violations) == 0,
        "chain_length": len(rows),
        "status": "intact" if len(violations) == 0 else "compromised",
        "violations": violations,
        "genesis_id": rows[0]["id"] if rows else None,
        "latest_id": rows[-1]["id"] if rows else None,
        "latest_hash": rows[-1]["chain_hash"] if rows else None,
    }


def log_sovereignty_policy(policy_type: str, target: str, decision: str,
                           reason: str = "", created_by: str = "SYSTEM",
                           dna_trace: str = "") -> None:
    """记录主权策略决策。"""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO sovereignty_policy (timestamp, policy_type, target, decision, "
            "reason, effective_from, created_by, dna_trace) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (now_iso(), policy_type, target, decision, reason, now_iso(), created_by, dna_trace)
        )
        conn.commit()


def get_sovereignty_policies(policy_type: str = None, limit: int = 50) -> list:
    """查询主权策略。"""
    with get_connection() as conn:
        if policy_type:
            rows = conn.execute(
                "SELECT * FROM sovereignty_policy WHERE policy_type = ? ORDER BY id DESC LIMIT ?",
                (policy_type, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM sovereignty_policy ORDER BY id DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]


def get_document_by_path(file_path: str) -> Optional[dict]:
    """通过文件路径获取文档信息。"""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM document_registry WHERE file_path = ?", (file_path,)
        ).fetchone()
        return dict(row) if row else None


def get_document_by_id(doc_id: str) -> Optional[dict]:
    """通过文档ID获取文档信息。"""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM document_registry WHERE doc_id = ?", (doc_id,)
        ).fetchone()
        return dict(row) if row else None


def get_document_stats() -> dict:
    """获取文档统计信息。"""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM document_registry").fetchone()[0]
        by_type = {}
        for row in conn.execute(
            "SELECT doc_type, COUNT(*) as cnt FROM document_registry GROUP BY doc_type"
        ).fetchall():
            by_type[row[0]] = row[1]
        by_status = {}
        for row in conn.execute(
            "SELECT status, COUNT(*) as cnt FROM document_registry GROUP BY status"
        ).fetchall():
            by_status[row[0]] = row[1]
        total_words = conn.execute(
            "SELECT COALESCE(SUM(word_count), 0) FROM document_registry"
        ).fetchone()[0]
        return {
            "total_docs": total,
            "by_type": by_type,
            "by_status": by_status,
            "total_words": total_words
        }


def get_regulatory_access_logs(limit: int = 100, auditor_id: str = None) -> list:
    """查询监管访问日志。"""
    with get_connection() as conn:
        if auditor_id:
            rows = conn.execute(
                "SELECT * FROM regulatory_access_log WHERE auditor_id = ? ORDER BY id DESC LIMIT ?",
                (auditor_id, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM regulatory_access_log ORDER BY id DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]


# 启动时初始化
init_regulatory_db()
