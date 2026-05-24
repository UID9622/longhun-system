# -*- coding: utf-8 -*-
"""
本地痕迹挖宝 · 只读 · 路径/元数据入库（明文内容不入主表）
DNA: #龍芯⚡️2026-05-16-08:10-FOOTPRINT-MINER-v1.0
"""
from __future__ import annotations

import hashlib
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

HOME = Path.home()

# 命中即跳过登记（路径级·不展开内容）
FORBIDDEN_SUBSTR = ("军事机密", "国防绝密", "核武器", "绝密", "机密")

TARGETS: Dict[str, List[Path]] = {
    "豆包": [
        HOME / "Library/Application Support/Doubao",
        HOME / "Library/Caches/com.bytedance.doubao",
    ],
    "通义": [
        HOME / "Library/Application Support/Tongyi",
        HOME / "Library/Caches/com.alibaba.tongyi",
    ],
    "文心": [
        HOME / "Library/Application Support/Wenxin",
        HOME / "Library/Caches/com.baidu.wenxin",
    ],
    "Kimi": [HOME / "Library/Application Support/Kimi"],
    "智谱": [
        HOME / "Library/Application Support/Zhipu",
        HOME / "Library/Caches/com.zhipuai",
    ],
    "DeepSeek": [HOME / "Library/Application Support/DeepSeek"],
}

MAX_FILE_BYTES = 10_000_000
MAX_FILES_PER_PRODUCT = 4000
DEFAULT_DB = REPO_ROOT / "tools/h_weapon_100k/db/footprint.db"


def _path_safe(p: Path) -> bool:
    s = str(p)
    return not any(x in s for x in FORBIDDEN_SUBSTR)


def _iter_files(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        return
    try:
        for f in root.rglob("*"):
            if f.is_file() and f.stat().st_size <= MAX_FILE_BYTES:
                yield f
    except (OSError, PermissionError):
        return


def scan_target(name: str, paths: List[Path]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for p in paths:
        if not _path_safe(p):
            continue
        for f in _iter_files(p):
            if not _path_safe(f):
                continue
            if len(found) >= MAX_FILES_PER_PRODUCT:
                return found
            try:
                st = f.stat()
            except OSError:
                continue
            ph = hashlib.sha256(str(f).encode("utf-8")).hexdigest()[:32]
            found.append(
                {
                    "hash": ph,
                    "product": name,
                    "path": str(f),
                    "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
                }
            )
    return found


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS footprints (
            hash TEXT PRIMARY KEY,
            product TEXT,
            path TEXT,
            size INTEGER,
            mtime TEXT,
            scan_ts TEXT
        );
        """
    )
    return conn


def main() -> None:
    db_path = DEFAULT_DB
    conn = init_db(db_path)
    total = 0
    now = datetime.now(timezone.utc).isoformat()
    for name, paths in TARGETS.items():
        items = scan_target(name, paths)
        print(f"  {name}: {len(items)} 个文件（上限 {MAX_FILES_PER_PRODUCT}）", flush=True)
        for it in items:
            conn.execute(
                "INSERT OR IGNORE INTO footprints VALUES (?,?,?,?,?,?)",
                (it["hash"], it["product"], it["path"], it["size"], it["mtime"], now),
            )
            total += 1
        conn.commit()
    conn.close()
    print(f"入库 {total} 条 · {db_path}", flush=True)


if __name__ == "__main__":
    main()
