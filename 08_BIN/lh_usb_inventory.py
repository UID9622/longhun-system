#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷈小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-LH_USB_INVENTORY-v1.0-cab54313
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""龍魂 USB 备份盘索引器

扫描挂载的移动存储，建立 SQLite 索引 + 里程碑时间线 + 同步优先级清单。
输出可直接对接 longhun 搜索引擎和服务器同步脚本。
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Iterable, Any

DB_PATH = Path("~/longhun-system/data/usb_index/usb_index.db").expanduser()
MILESTONE_PATH = Path("~/longhun-system/data/usb_index/milestones.json").expanduser()
SUMMARY_PATH = Path("~/longhun-system/data/usb_index/usb_summary.json").expanduser()

CATEGORY_PATTERNS = {
    "code_repo": [".git", "pyproject.toml", "package.json", "requirements.txt", "Cargo.toml", "pom.xml"],
    "longhun_core": ["longhun", "龍魂", "龍魂", "CNSH", "cnsh"],
    "evidence": ["证据", "evidence", "snapshot", "取证", "proof"],
    "document": [".md", ".pdf", ".docx", ".txt", ".html"],
    "media": [".jpg", ".jpeg", ".png", ".mp4", ".mov", ".mp3", ".wav"],
    "archive": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "backup_phone": ["DCIM", "Camera", "Photos", "备份", "backup"],
}


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            relpath TEXT NOT NULL,
            root TEXT NOT NULL,
            size INTEGER,
            mtime REAL,
            ctime REAL,
            ext TEXT,
            category TEXT,
            sha256 TEXT,
            priority INTEGER DEFAULT 0,
            note TEXT,
            indexed_at REAL
        );
        CREATE INDEX IF NOT EXISTS idx_root ON files(root);
        CREATE INDEX IF NOT EXISTS idx_ext ON files(ext);
        CREATE INDEX IF NOT EXISTS idx_category ON files(category);
        CREATE INDEX IF NOT EXISTS idx_priority ON files(priority);
        CREATE INDEX IF NOT EXISTS idx_mtime ON files(mtime);

        CREATE TABLE IF NOT EXISTS roots (
            root TEXT PRIMARY KEY,
            total_size INTEGER,
            total_files INTEGER,
            categories TEXT,
            summary TEXT,
            scanned_at REAL
        );

        CREATE TABLE IF NOT EXISTS sync_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            target TEXT NOT NULL,
            reason TEXT,
            estimated_size INTEGER,
            status TEXT DEFAULT 'pending'
        );
        """
    )


def categorize(path: Path) -> str:
    name = path.name.lower()
    parts = [p.lower() for p in path.parts]
    for cat, markers in CATEGORY_PATTERNS.items():
        if cat == "code_repo":
            # code_repo 判断需要目录中存在 marker 文件
            continue
        if any(m.lower() in name or m.lower() in parts for m in markers):
            return cat
    if path.suffix.lower() in CATEGORY_PATTERNS.get("media", []):
        return "media"
    if path.suffix.lower() in CATEGORY_PATTERNS.get("archive", []):
        return "archive"
    if path.suffix.lower() in CATEGORY_PATTERNS.get("document", []):
        return "document"
    return "other"


def is_code_repo(dir_path: Path) -> bool:
    return any((dir_path / marker).exists() for marker in CATEGORY_PATTERNS["code_repo"])


def sha256_file(path: Path, limit: int = 256 * 1024) -> str:
    """采样哈希：前 limit 字节 + 文件大小 + 修改时间，避免 188GB 全量哈希。"""
    try:
        st = path.stat()
        h = hashlib.sha256()
        h.update(f"{st.st_size}:{st.st_mtime}".encode())
        if st.st_size <= limit:
            with open(path, "rb") as f:
                h.update(f.read())
        else:
            with open(path, "rb") as f:
                h.update(f.read(limit))
                f.seek(-limit // 2, os.SEEK_END)
                h.update(f.read(limit // 2))
        return h.hexdigest()
    except Exception:
        return ""


def scan(root: Path, conn: sqlite3.Connection, dry_run: bool = False) -> None:
    root_str = str(root)
    cursor = conn.cursor()
    existing = {row[0] for row in cursor.execute("SELECT path FROM files WHERE root = ?", (root_str,))}

    inserted = 0
    updated = 0
    skipped = 0

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            stat = file_path.stat()
        except (OSError, PermissionError):
            continue

        path_str = str(file_path)
        if path_str in existing:
            skipped += 1
            continue

        relpath = path_str[len(root_str):].lstrip("/")
        ext = file_path.suffix.lower()
        category = categorize(file_path)
        sha256 = sha256_file(file_path)

        if not dry_run:
            cursor.execute(
                """
                INSERT INTO files (path, relpath, root, size, mtime, ctime, ext, category, sha256, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (path_str, relpath, root_str, stat.st_size, stat.st_mtime, stat.st_ctime, ext, category, sha256, datetime.datetime.now().timestamp()),
            )
            inserted += 1
        else:
            inserted += 1

        if (inserted + skipped) % 5000 == 0:
            print(f"  scanned {inserted + skipped} files, inserted {inserted}")

    conn.commit()
    print(f"Done: inserted={inserted}, skipped={skipped}")


def summarize(conn: sqlite3.Connection, root: Path) -> dict[str, Any]:
    cursor = conn.cursor()
    root_str = str(root)
    rows = list(cursor.execute(
        "SELECT ext, category, size FROM files WHERE root = ?", (root_str,)
    ))
    total_size = sum(r[2] for r in rows)
    total_files = len(rows)
    ext_counts: dict[str, int] = {}
    cat_counts: dict[str, int] = {}
    for ext, cat, _ in rows:
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    summary = {
        "root": root_str,
        "total_size": total_size,
        "total_files": total_files,
        "ext_top10": sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        "category_counts": cat_counts,
        "scanned_at": datetime.datetime.now().isoformat(),
    }

    conn.execute(
        """
        INSERT OR REPLACE INTO roots (root, total_size, total_files, categories, summary, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (root_str, total_size, total_files, json.dumps(cat_counts), json.dumps(summary), datetime.datetime.now().timestamp()),
    )
    conn.commit()
    return summary


def detect_milestones(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """从目录名和修改时间中提取里程碑。"""
    cursor = conn.cursor()
    roots = [row[0] for row in cursor.execute("SELECT DISTINCT root FROM files")]
    milestones = []
    for root in roots:
        root_path = Path(root)
        # 顶层目录作为里程碑候选
        for child in root_path.iterdir():
            if child.is_dir() and not child.name.startswith("."):
                try:
                    stat = child.stat()
                    milestones.append({
                        "name": child.name,
                        "path": str(child),
                        "mtime_iso": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "size": sum(f.stat().st_size for f in child.rglob("*") if f.is_file()),
                    })
                except Exception:
                    continue
    milestones.sort(key=lambda x: x["mtime_iso"])
    MILESTONE_PATH.parent.mkdir(parents=True, exist_ok=True)
    MILESTONE_PATH.write_text(json.dumps(milestones, ensure_ascii=False, indent=2), encoding="utf-8")
    return milestones


EXCLUDED_PATHS = {
    ".Trashes", "$RECYCLE.BIN", "System Volume Information", ".Spotlight-V100",
    ".fseventsd", "__pycache__", "node_modules", ".git", ".DS_Store",
}

TIER1_TOP_DIRS = {
    # 龍魂核心：这些顶层目录整个包进来（排除垃圾子目录）
    "CNSH 军人的编辑器", "CNSH", "龍魂终端扬帆起航", "龍魂铸剑实验室", "龍魂使命",
    "龍芯_证据_20260507_232327", "龍魂系统备份_20260114",
    "ai-truth-protocol", "service_dna_demo",
    "开发者", "开源项目包", "文稿",
}

TIER2_TOP_DIRS = {
    # Notion导出 + 待处理（只取.md/.py/.html/.json）
    "Export-14311d34-129d-4fb7-91dd-16e54203f88d",
    "待处理",
}

TIER3_TOP_DIRS = {
    # 归档 / 🇨🇳 手机备份（不往上同步，只建索引）
    "归档", "归档 2", "🇨🇳",
}

SYNC_EXT_WHITELIST = {".md", ".py", ".html", ".json", ".yaml", ".yml", ".toml",
                       ".txt", ".csv", ".sh", ".js", ".ts", ".css",
                       ".png", ".jpg", ".jpeg", ".svg", ".gif",
                       ".pdf", ".docx", ".xlsx", ".key", ".pages"}

MAX_SYNC_GB = 42  # 服务器剩余 51G，留 9G 缓冲


def _should_exclude(relpath: str) -> bool:
    parts = set(relpath.split("/"))
    return bool(parts & EXCLUDED_PATHS)


def _top_dir(relpath: str) -> str:
    return relpath.split("/")[0] if "/" in relpath else "root"


def build_sync_plan(conn: sqlite3.Connection, root: Path) -> None:
    """三级同步计划：
    Tier1 高优先 → 整目录同步（排除垃圾）
    Tier2 中优先 → 核心文件类型同步
    Tier3 低优先 → 只建索引不同步（手机备份/归档）
    """
    cursor = conn.cursor()
    root_str = str(root)
    cursor.execute("DELETE FROM sync_plan WHERE target = 'server'")

    cursor.execute(
        "SELECT path, relpath, size, ext, mtime FROM files WHERE root = ? ORDER BY mtime DESC",
        (root_str,),
    )

    tier1_total = 0
    tier2_total = 0
    tier1_count = 0
    tier2_count = 0
    skipped_junk = 0
    skipped_tier3 = 0

    for path, relpath, size, ext, mtime in cursor.fetchall():
        td = _top_dir(relpath)

        # 跳过垃圾/系统目录
        if _should_exclude(relpath):
            skipped_junk += 1
            continue

        # Tier 3: 不往上同步
        if td in TIER3_TOP_DIRS:
            skipped_tier3 += 1
            continue

        reason = None
        est_size = size

        # Tier 1: 整目录同步（所有文件类型）
        if td in TIER1_TOP_DIRS:
            if tier1_total + est_size <= MAX_SYNC_GB * 1024 * 1024 * 1024 * 0.65:
                reason = "tier1_core"
                tier1_total += est_size
                tier1_count += 1
            else:
                continue

        # Tier 2: 中优先，只看白名单扩展名
        elif td in TIER2_TOP_DIRS:
            if ext in SYNC_EXT_WHITELIST and size < 500 * 1024 * 1024:
                if tier1_total + tier2_total + est_size <= MAX_SYNC_GB * 1024 * 1024 * 1024:
                    reason = "tier2_document"
                    tier2_total += est_size
                    tier2_count += 1
                else:
                    continue
            else:
                continue

        # 不是在上述目录的龍魂相关文件（如🇨🇳里的龍魂价值内核）
        elif any(kw in relpath.lower() for kw in ("longhun", "龍魂", "龍魂", "cnsh", "uid9622", "证据")):
            if ext in SYNC_EXT_WHITELIST and size < 100 * 1024 * 1024:
                if tier1_total + tier2_total + est_size <= MAX_SYNC_GB * 1024 * 1024 * 1024:
                    reason = "tier2_longhun"
                    tier2_total += est_size
                    tier2_count += 1
                else:
                    continue
            else:
                continue
        else:
            continue  # 不在任何同步范围内的文件

        if reason:
            cursor.execute(
                "INSERT INTO sync_plan (path, target, reason, estimated_size) VALUES (?, ?, ?, ?)",
                (path, "server", reason, est_size),
            )

    conn.commit()
    total_gb = (tier1_total + tier2_total) / 1024 / 1024 / 1024
    print(f"Sync plan: {total_gb:.2f} GB to server")
    print(f"  Tier1 (核心): {tier1_count} 文件, {tier1_total/1024/1024/1024:.2f} GB")
    print(f"  Tier2 (文档): {tier2_count} 文件, {tier2_total/1024/1024/1024:.2f} GB")
    print(f"  跳过垃圾:   {skipped_junk} 文件")
    print(f"  跳过Tier3:  {skipped_tier3} 文件")


def main() -> int:
    parser = argparse.ArgumentParser(description="USB 备份盘索引器")
    parser.add_argument("mount", help="挂载点，例如 /Volumes/🔐")
    parser.add_argument("--scan", action="store_true", help="执行扫描")
    parser.add_argument("--summary", action="store_true", help="生成汇总")
    parser.add_argument("--milestones", action="store_true", help="生成里程碑")
    parser.add_argument("--sync-plan", action="store_true", help="生成同步计划")
    parser.add_argument("--dry-run", action="store_true", help="只统计不写入")
    args = parser.parse_args()

    root = Path(args.mount)
    if not root.exists():
        print(f"Mount not found: {root}")
        return 1

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)

    if args.scan or args.summary or args.milestones or args.sync_plan:
        if args.scan:
            scan(root, conn, dry_run=args.dry_run)
        if args.summary:
            summary = summarize(conn, root)
            SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
            SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        if args.milestones:
            milestones = detect_milestones(conn)
            print(f"Milestones: {len(milestones)}")
            for m in milestones[-10:]:
                print(f"  {m['mtime_iso']} | {m['name']} | {m['size'] / 1024 / 1024:.1f} MB")
        if args.sync_plan:
            build_sync_plan(conn, root)
    else:
        parser.print_help()

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
