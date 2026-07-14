#!/usr/bin/env python3
"""龍魂 USB 备份搜索引擎 — 在服务器上建全文索引

对已同步到服务器的 U 盘备份数据，构建：
1. ripgrep 兼容的纯文本搜索
2. 文件名索引
3. 关键术语热索引（DNA/UID9622/龙魂/CNSH/证据等）
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

INDEX_DB = Path("/data/usb_backup_index/search.db")
BACKUP_ROOT = Path("/data/usb_backup")


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS file_index (
            path TEXT PRIMARY KEY,
            name TEXT,
            ext TEXT,
            size INTEGER,
            mtime REAL,
            first_500 TEXT,
            keywords TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS file_fts USING fts5(
            path, name, content, keywords,
            content=file_index,
            content_rowid='rowid'
        );
        CREATE INDEX IF NOT EXISTS idx_ext ON file_index(ext);
        CREATE INDEX IF NOT EXISTS idx_name ON file_index(name);
    """)


def extract_keywords(text: str) -> list[str]:
    """提取关键术语"""
    kw = set()
    triggers = {
        "龙魂", "龍魂", "CNSH", "UID9622", "DNA", "证据", "宪法", "铁律",
        "Notion", "华为", "鸿蒙", "服务器", "编辑器", "终端", "协议",
        "人格", "审计", "三色", "五行", "八卦", "369", "河图", "洛书",
        "老子", "道德经", "诸葛", "张良", "姜子牙", "曾仕强",
        "longhun", "dna-gen", "wuxing", "persona", "governance",
    }
    for t in triggers:
        if t.lower() in text.lower():
            kw.add(t)
    return list(kw)


TEXT_EXTS = {".md", ".py", ".html", ".json", ".yaml", ".yml", ".toml",
             ".txt", ".csv", ".sh", ".js", ".ts", ".css", ".cnsh", ".pyi",
             ".xml", ".ini", ".cfg", ".conf", ".rst", ".tex"}


def build_index(conn: sqlite3.Connection, root: Path) -> None:
    cursor = conn.cursor()
    existing = {row[0] for row in cursor.execute("SELECT path FROM file_index")}
    added = 0
    skipped = 0

    for fpath in root.rglob("*"):
        if not fpath.is_file():
            continue
        path_str = str(fpath)
        if path_str in existing:
            skipped += 1
            continue

        ext = fpath.suffix.lower()
        try:
            st = fpath.stat()
            size = st.st_size
            mtime = st.st_mtime
        except OSError:
            continue

        first_500 = ""
        keywords = ""
        if ext in TEXT_EXTS and size < 50 * 1024 * 1024:
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")[:2000]
                first_500 = content[:500]
                kws = extract_keywords(content)
                keywords = ",".join(kws) if kws else ""
            except Exception:
                pass

        try:
            cursor.execute(
                """INSERT INTO file_index (path, name, ext, size, mtime, first_500, keywords)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (path_str, fpath.name, ext, size, mtime, first_500, keywords),
            )
            if keywords:
                cursor.execute(
                    "INSERT INTO file_fts (path, name, content, keywords) VALUES (?, ?, ?, ?)",
                    (path_str, fpath.name, first_500, keywords),
                )
            added += 1
            if added % 1000 == 0:
                print(f"  indexed {added} files...")
        except Exception:
            pass

    conn.commit()
    print(f"Index done: {added} added, {skipped} skipped")


def search(conn: sqlite3.Connection, query: str, root: Path) -> list[dict]:
    cursor = conn.cursor()
    try:
        rows = cursor.execute(
            "SELECT path, name, snippet(file_fts, 2, '<b>', '</b>', '...', 64) FROM file_fts WHERE file_fts MATCH ? LIMIT 50",
            (query,),
        ).fetchall()
    except Exception:
        rows = []

    results = []
    root_str = str(root)
    for path, name, snippet in rows:
        results.append({"path": path.replace(root_str, ""), "name": name, "snippet": snippet})
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["build", "search", "stats"])
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--root", default="/data/usb_backup")
    parser.add_argument("--db", default="/data/usb_backup_index/search.db")
    args = parser.parse_args()

    root = Path(args.root)
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    ensure_db(conn)

    if args.action == "build":
        build_index(conn, root)
    elif args.action == "search":
        results = search(conn, args.query, root)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.action == "stats":
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
        with_kw = cursor.execute("SELECT COUNT(*) FROM file_index WHERE keywords != ''").fetchone()[0]
        ext_counts = cursor.execute(
            "SELECT ext, COUNT(*) FROM file_index GROUP BY ext ORDER BY COUNT(*) DESC LIMIT 15"
        ).fetchall()
        print(json.dumps({
            "total_files": total,
            "with_keywords": with_kw,
            "ext_top15": [[e, c] for e, c in ext_counts],
        }, ensure_ascii=False, indent=2))

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
