#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知识图谱 · 轻量论文索引器
LongHun KG Paper Indexer (self-contained)

直接操作 ~/.longhun/global_index/global_index.db，与全局索引服务共用同一份数据，
但无需导入 watchdog 等守护进程依赖。

DNA: #龍芯⚡️2026-07-01-KG-PAPER-INDEXER-v1.0
"""

import hashlib
import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Optional


def _now() -> float:
    return time.time()


def compute_hash(path: Path, algo: str = "blake2b") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1048576)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def extract_document_metadata(path: Path) -> Dict[str, str]:
    """对 .md/.txt 提取标题、首标题、摘要。"""
    meta: Dict[str, str] = {}
    suf = path.suffix.lower()
    if suf not in (".md", ".txt", ".markdown", ".rst"):
        meta["type"] = "unsupported"
        return meta
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    except Exception as e:
        meta["error"] = str(e)
        return meta

    lines = [ln.rstrip() for ln in text.splitlines()]
    heading = ""
    for ln in lines:
        if ln.startswith("#"):
            heading = ln.lstrip("#").strip()
            break
    meta["first_heading"] = heading

    title = ""
    for ln in lines[:10]:
        stripped = ln.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            break
    meta["title"] = title or heading

    snippet = " ".join(ln.strip() for ln in lines[:30] if ln.strip())
    meta["snippet"] = snippet[:500]
    return meta


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            relpath TEXT,
            root TEXT,
            size INTEGER,
            mtime REAL,
            inode INTEGER,
            mode INTEGER,
            hash TEXT,
            hash_algo TEXT,
            indexed_at REAL,
            changed_at REAL,
            event_type TEXT,
            accessible INTEGER DEFAULT 1
        );
        CREATE INDEX IF NOT EXISTS idx_files_root ON files(root);
        CREATE INDEX IF NOT EXISTS idx_files_changed ON files(changed_at);

        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            media_type TEXT,
            key TEXT,
            value TEXT,
            extracted_at REAL,
            FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_metadata_file ON metadata(file_id);
        """
    )


def index_files(
    paths: List[Path],
    root: Path,
    db_path: Path,
    event_type: str = "paper-index",
) -> List[Dict[str, object]]:
    """把一组文件索引进知识图谱，返回每个文件的摘要信息。"""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=60.0)
    conn.row_factory = sqlite3.Row
    _init_schema(conn)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    results: List[Dict[str, object]] = []
    now = _now()
    root_str = str(root)

    for path in paths:
        if not path.is_file():
            results.append({"path": str(path), "ok": False, "error": "not a file"})
            continue
        try:
            st = path.stat()
        except Exception as e:
            results.append({"path": str(path), "ok": False, "error": str(e)})
            continue

        rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        h = compute_hash(path)
        meta = extract_document_metadata(path)
        media_type = "document" if meta.get("type") != "unsupported" else None

        conn.execute(
            """INSERT OR REPLACE INTO files
               (path, relpath, root, size, mtime, inode, mode, hash, hash_algo,
                indexed_at, changed_at, event_type, accessible)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (
                str(path),
                rel,
                root_str,
                st.st_size,
                st.st_mtime,
                st.st_ino,
                st.st_mode,
                h,
                "blake2b",
                now,
                now,
                event_type,
            ),
        )
        row = conn.execute("SELECT id FROM files WHERE path=?", (str(path),)).fetchone()
        file_id = row["id"]

        conn.execute("DELETE FROM metadata WHERE file_id=?", (file_id,))
        if media_type:
            for k, v in meta.items():
                conn.execute(
                    "INSERT INTO metadata (file_id, media_type, key, value, extracted_at) VALUES (?, ?, ?, ?, ?)",
                    (file_id, media_type, k, str(v), now),
                )

        results.append(
            {
                "path": str(path),
                "ok": True,
                "file_id": file_id,
                "hash": h,
                "title": meta.get("title", ""),
            }
        )

    conn.commit()
    conn.close()
    return results
