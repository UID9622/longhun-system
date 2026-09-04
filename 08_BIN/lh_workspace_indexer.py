#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-WORKSPACE-INDEXER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 工作间索引器 v1.0

把 longhun-system 整棵目录树索引进 SQLite，找出落单文件：
  - 无 DNA
  - 无 GPG 签名
  - 不在系统忽略白名单

用法:
  python3 08_BIN/lh_workspace_indexer.py
  python3 08_BIN/lh_workspace_indexer.py --output-dir 12_DOCS
  python3 08_BIN/lh_workspace_indexer.py --orphans-only

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "12_DOCS" / "workspace_index.db"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "12_DOCS"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 扫描时完全跳过的目录
SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    ".pytest_cache", ".mypy_cache", ".cache", ".idea", ".vscode",
    "target", "dist", "build", ".eggs", ".tox", ".coverage",
}

# 忽略扩展名（编译产物、缓存等）
SKIP_EXTS = {
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".class",
    ".o", ".a", ".obj", ".exe", ".bin",
    ".DS_Store", ".swp", ".swo", ".tmp", ".temp",
    ".log", ".lock", ".bundle", ".tar.gz", ".zip",
}

# 默认落单白名单：这些文件可以没有 DNA/签名
ORPHAN_WHITELIST = {
    "README.md", "README", ".gitignore", ".gitattributes",
    "LICENSE", "Makefile", "requirements.txt", "setup.py",
    "pyproject.toml", "package.json", "package-lock.json",
    ".layer_tag", ".DS_Store", "go.mod", "go.sum", "Cargo.lock",
    "yarn.lock", "pnpm-lock.yaml", "poetry.lock",
}

# 应被主权化的文本/代码/文档扩展名
CODE_DOC_EXTS = {
    ".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".txt",
    ".html", ".htm", ".cnsh", ".toml", ".sh", ".bash", ".zsh",
    ".swift", ".kt", ".java", ".js", ".ts", ".tsx", ".jsx",
    ".c", ".cpp", ".h", ".hpp", ".rs", ".go", ".rb", ".php",
    ".sql", ".css", ".scss", ".vue", ".svelte",
}

# 数据资产扩展名：不算落单，但入库管理
ASSET_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".mp3", ".mp4", ".mov", ".m4a", ".wav", ".ogg",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".db", ".sqlite", ".sqlite3", ".bundle", ".log",
}

DNA_RE = re.compile(r'#龍芯⚡️\S+')


# ═══════════════════════════════════════════════════════
# 数据库
# ═══════════════════════════════════════════════════════
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS scan_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna TEXT,
    confirm TEXT,
    started_at TEXT,
    completed_at TEXT,
    total_files INTEGER,
    orphan_files INTEGER,
    dna_count INTEGER,
    gpg_signed INTEGER
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    rel_path TEXT,
    layer TEXT,
    filename TEXT,
    extension TEXT,
    file_kind TEXT,
    size_bytes INTEGER,
    mtime TEXT,
    sha256 TEXT,
    has_asc INTEGER,
    asc_valid INTEGER,
    dna_count INTEGER,
    is_orphan INTEGER,
    orphan_reason TEXT,
    scanned_at TEXT
);

CREATE TABLE IF NOT EXISTS dna_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT,
    dna TEXT,
    dna_type TEXT,
    extracted_at TEXT,
    FOREIGN KEY (file_path) REFERENCES files(path) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gpg_sigs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT,
    asc_path TEXT,
    valid INTEGER,
    checked_at TEXT,
    FOREIGN KEY (file_path) REFERENCES files(path) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_files_layer ON files(layer);
CREATE INDEX IF NOT EXISTS idx_files_orphan ON files(is_orphan);
CREATE INDEX IF NOT EXISTS idx_dna_file ON dna_records(file_path);
CREATE INDEX IF NOT EXISTS idx_gpg_file ON gpg_sigs(file_path);
"""


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(DB_SCHEMA)
    conn.commit()
    return conn


def classify_layer(rel_path: str) -> str:
    """根据路径判断所属层级"""
    parts = Path(rel_path).parts
    if not parts:
        return "root"
    top = parts[0]
    if top.startswith("0") and len(top) >= 2:
        return top
    if top in ("core", "config", "archive", "scripts", "tests"):
        return top
    return "other"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def extract_dnas(text: str) -> List[Tuple[str, str]]:
    """从文本中提取 DNA，返回 [(dna, type), ...]"""
    seen: Set[str] = set()
    result = []
    for match in DNA_RE.finditer(text):
        dna = match.group(0)
        if dna in seen:
            continue
        seen.add(dna)
        # 简单分类
        if "CONFIRM" in dna:
            dtype = "confirm"
        elif "ZHUGEXIN" in dna:
            dtype = "seal"
        elif re.search(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]', dna):
            dtype = "ganzhi"
        else:
            dtype = "other"
        result.append((dna, dtype))
    return result


def verify_gpg(file_path: Path, asc_path: Path) -> bool:
    """验证 GPG 签名，找不到公钥也算无效"""
    try:
        result = subprocess.run(
            ["gpg", "--verify", str(asc_path), str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except Exception:
        return False


def should_skip(path: Path, rel: Path) -> bool:
    """判断是否应该跳过该路径"""
    for part in rel.parts:
        if part in SKIP_DIRS:
            return True
    if path.name in ORPHAN_WHITELIST:
        return False
    if path.suffix.lower() in SKIP_EXTS:
        return True
    return False


def classify_file_kind(path: Path) -> str:
    """判断文件类型：code_doc / signature / asset / other"""
    ext = path.suffix.lower()
    if ext == ".asc":
        return "signature"
    if ext in CODE_DOC_EXTS:
        return "code_doc"
    if ext in ASSET_EXTS:
        return "asset"
    return "other"


def is_whitelisted(rel: Path) -> bool:
    return rel.name in ORPHAN_WHITELIST


def scan_workspace(root: Path, conn: sqlite3.Connection,
                   orphans_only: bool = False) -> Dict[str, Any]:
    """扫描工作间并写入数据库"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files")
    cursor.execute("DELETE FROM dna_records")
    cursor.execute("DELETE FROM gpg_sigs")
    conn.commit()

    total = 0
    orphan_count = 0
    dna_total = 0
    gpg_signed = 0
    started_at = datetime.now().isoformat()

    print(f"🔍 开始扫描工作间: {root}")

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue

        if should_skip(path, rel):
            continue

        total += 1
        stat = path.stat()
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
        sha = sha256_file(path)
        layer = classify_layer(str(rel))
        file_kind = classify_file_kind(path)

        # 读取内容提取 DNA（仅文本类文件）
        dnas: List[Tuple[str, str]] = []
        if file_kind == "code_doc" or path.suffix.lower() in {".log"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                dnas = extract_dnas(text)
            except Exception:
                pass

        # GPG 签名：签名文件本身不需要被签名
        asc_path = path.with_suffix(path.suffix + ".asc")
        has_asc = 1 if asc_path.exists() else 0
        asc_valid = 0
        if has_asc:
            asc_valid = 1 if verify_gpg(path, asc_path) else 0
            gpg_signed += asc_valid

        # 落单判断：只有 code_doc 类文件才需要 DNA + GPG 签名
        is_orphan = 0
        reasons = []
        if file_kind == "code_doc" and not is_whitelisted(rel):
            if not dnas:
                reasons.append("无DNA")
            if not has_asc:
                reasons.append("无GPG签名")
            if reasons:
                is_orphan = 1
                orphan_count += 1

        cursor.execute(
            """INSERT INTO files
               (path, rel_path, layer, filename, extension, file_kind, size_bytes, mtime,
                sha256, has_asc, asc_valid, dna_count, is_orphan, orphan_reason, scanned_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(path), str(rel), layer, path.name, path.suffix.lower(), file_kind,
             size, mtime, sha, has_asc, asc_valid, len(dnas),
             is_orphan, "、".join(reasons), started_at),
        )

        for dna, dtype in dnas:
            cursor.execute(
                "INSERT INTO dna_records (file_path, dna, dna_type, extracted_at) VALUES (?, ?, ?, ?)",
                (str(path), dna, dtype, started_at),
            )
            dna_total += 1

        if has_asc:
            cursor.execute(
                "INSERT INTO gpg_sigs (file_path, asc_path, valid, checked_at) VALUES (?, ?, ?, ?)",
                (str(path), str(asc_path), asc_valid, started_at),
            )

        if total % 500 == 0:
            conn.commit()
            print(f"  已扫描 {total} 个文件...")

    conn.commit()

    completed_at = datetime.now().isoformat()
    dna = generate_dna("WORKSPACE-INDEXER", "UID9622")
    cursor.execute(
        """INSERT INTO scan_runs
           (dna, confirm, started_at, completed_at, total_files, orphan_files,
            dna_count, gpg_signed)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (dna, CONFIRM_MARK, started_at, completed_at, total, orphan_count,
         dna_total, gpg_signed),
    )
    conn.commit()

    return {
        "dna": dna,
        "total": total,
        "orphan_count": orphan_count,
        "dna_total": dna_total,
        "gpg_signed": gpg_signed,
        "started_at": started_at,
        "completed_at": completed_at,
    }


def generate_report(conn: sqlite3.Connection, output_dir: Path, stats: Dict[str, Any]) -> Path:
    """生成 Markdown 报告"""
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / f"workspace_index_report_{datetime.now():%Y%m%d_%H%M%S}.md"

    # 按层级统计
    cursor = conn.execute(
        "SELECT layer, COUNT(*) FROM files GROUP BY layer ORDER BY COUNT(*) DESC"
    )
    layer_stats = cursor.fetchall()

    # 按文件类型统计
    cursor = conn.execute(
        "SELECT file_kind, COUNT(*) FROM files GROUP BY file_kind ORDER BY COUNT(*) DESC"
    )
    kind_stats = cursor.fetchall()

    # 落单文件按层级统计
    cursor = conn.execute(
        "SELECT layer, COUNT(*) FROM files WHERE is_orphan=1 GROUP BY layer ORDER BY COUNT(*) DESC"
    )
    orphan_layer_stats = cursor.fetchall()

    # 前 50 个落单文件
    cursor = conn.execute(
        "SELECT rel_path, layer, orphan_reason FROM files WHERE is_orphan=1 ORDER BY layer, rel_path LIMIT 50"
    )
    top_orphans = cursor.fetchall()

    # 统计 code_doc 文件总数与落单数
    cursor = conn.execute("SELECT COUNT(*) FROM files WHERE file_kind='code_doc'")
    code_doc_total = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM files WHERE file_kind='code_doc' AND is_orphan=1")
    code_doc_orphan = cursor.fetchone()[0]

    md = f"""# 🐉 龍魂 · 工作间索引报告

**DNA:** `{stats['dna']}`  
**确认码:** `{CONFIRM_MARK}`  
**扫描时间:** {stats['started_at']} ~ {stats['completed_at']}

---

## 📊 总览

| 指标 | 数量 |
|:---|---:|
| 总文件数 | **{stats['total']}** |
| 应主权化文件 (code_doc) | **{code_doc_total}** |
| code_doc 落单 | **{code_doc_orphan}** |
| 落单文件（总） | **{stats['orphan_count']}** |
| DNA 记录 | **{stats['dna_total']}** |
| GPG 有效签名 | **{stats['gpg_signed']}** |

---

## 📂 按层级分布

| 层级 | 文件数 |
|:---|---:|
"""
    for layer, count in layer_stats:
        md += f"| {layer} | {count} |\n"

    md += """
---

## 🧩 按文件类型分布

| 类型 | 文件数 | 说明 |
|:---|---:|:---|
"""
    kind_desc = {
        "code_doc": "应被主权化的代码/文档/配置",
        "signature": "GPG 签名文件 (.asc)",
        "asset": "数据资产（图片/音视频/压缩包/数据库等）",
        "other": "其他文件",
    }
    for kind, count in kind_stats:
        md += f"| {kind} | {count} | {kind_desc.get(kind, '')} |\n"

    md += """
---

## 🔴 落单文件按层级分布

| 层级 | 落单数 |
|:---|---:|
"""
    for layer, count in orphan_layer_stats:
        md += f"| {layer} | {count} |\n"

    md += """
---

## 📝 前 50 个落单文件

| 路径 | 层级 | 原因 |
|:---|:---|:---|
"""
    for rel_path, layer, reason in top_orphans:
        md += f"| `{rel_path}` | {layer} | {reason} |\n"

    md += f"""
---

## 🚀 后续建议

```bash
# 查看所有 code_doc 落单文件
sqlite3 12_DOCS/workspace_index.db "SELECT rel_path, orphan_reason FROM files WHERE is_orphan=1 AND file_kind='code_doc';"

# 按层级统计落单
sqlite3 12_DOCS/workspace_index.db "SELECT layer, COUNT(*) FROM files WHERE is_orphan=1 GROUP BY layer;"

# 查看无签名的 code_doc 文件
sqlite3 12_DOCS/workspace_index.db "SELECT rel_path FROM files WHERE file_kind='code_doc' AND has_asc=0;"
```

---

**DNA:** `{stats['dna']}`  
**确认码:** `{CONFIRM_MARK}`
"""

    md_path.write_text(md, encoding="utf-8")
    return md_path


def export_orphans_csv(conn: sqlite3.Connection, output_dir: Path) -> Path:
    """导出落单文件 CSV"""
    import csv
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"workspace_orphans_{datetime.now():%Y%m%d_%H%M%S}.csv"

    cursor = conn.execute(
        "SELECT rel_path, layer, size_bytes, mtime, orphan_reason FROM files WHERE is_orphan=1 ORDER BY layer, rel_path"
    )
    rows = cursor.fetchall()

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["rel_path", "layer", "size_bytes", "mtime", "orphan_reason"])
        writer.writerows(rows)

    return csv_path


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 工作间索引器")
    parser.add_argument("--db-path", type=str, default=str(DEFAULT_DB_PATH),
                        help=f"SQLite 数据库路径 (默认: {DEFAULT_DB_PATH})")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help=f"报告输出目录 (默认: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--orphans-only", action="store_true",
                        help="只导出落单文件 CSV，不重新扫描")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    output_dir = Path(args.output_dir)
    conn = init_db(db_path)

    if args.orphans_only:
        csv_path = export_orphans_csv(conn, output_dir)
        print(f"📤 落单清单: {csv_path}")
        conn.close()
        return

    stats = scan_workspace(PROJECT_ROOT, conn)
    md_path = generate_report(conn, output_dir, stats)
    csv_path = export_orphans_csv(conn, output_dir)

    print(f"\n📊 扫描完成")
    print(f"   总文件: {stats['total']}")
    print(f"   落单: {stats['orphan_count']}")
    print(f"   DNA: {stats['dna_total']}")
    print(f"   GPG 签名: {stats['gpg_signed']}")
    print(f"📄 报告: {md_path}")
    print(f"📤 落单 CSV: {csv_path}")
    print(f"💾 数据库: {db_path}")
    print(f"🧬 DNA: {stats['dna']}")
    conn.close()


if __name__ == "__main__":
    main()
