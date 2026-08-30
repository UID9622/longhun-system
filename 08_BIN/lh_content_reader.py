#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-CONTENT-READER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 内容读取器 v1.0

不只读标题，读正文。把文本文件的内容、语义实体、DNA、协议引用、待办项
全部抽出来，写入 SQLite，让智能体能「真正读懂」工作间。

用法:
  python3 08_BIN/lh_content_reader.py scan              # 全量读取
  python3 08_BIN/lh_content_reader.py scan --layer 01_protocols  # 只扫某层
  python3 08_BIN/lh_content_reader.py query CNSH-64     # 全文搜索
  python3 08_BIN/lh_content_reader.py stats             # 统计
  python3 08_BIN/lh_content_reader.py orphans           # 内容落单文件

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
from collections import Counter, defaultdict
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

# 可读取的文本扩展名
TEXT_EXTS = {
    ".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".txt",
    ".html", ".htm", ".cnsh", ".toml", ".sh", ".bash", ".zsh",
    ".swift", ".kt", ".java", ".js", ".ts", ".tsx", ".jsx",
    ".c", ".cpp", ".h", ".hpp", ".rs", ".go", ".rb", ".php",
    ".sql", ".css", ".scss", ".vue", ".svelte",
}

# 跳过的目录（支持前缀/精确匹配）
SKIP_DIR_EXACT = {
    ".git", "__pycache__", "node_modules",
    ".pytest_cache", ".mypy_cache", ".cache", ".idea", ".vscode",
    "target", "dist", "build", ".eggs", ".tox", ".coverage",
    "site-packages",
}
SKIP_DIR_PREFIX = (".venv", "venv", ".env", "env")

# 正则提取规则
DNA_RE = re.compile(r'#龍芯⚡️\S+')
CONFIRM_RE = re.compile(r'#CONFIRM🌌[^\s]+')
GPG_RE = re.compile(r'[A-F0-9]{40}')
PROTOCOL_RE = re.compile(r'\b(CNSH-[A-Z0-9\-]+|DAO-\d+|LH-[A-Z0-9\-]+|ZGX-[A-Z0-9\-]+)\b')
TODO_RE = re.compile(r'(?:TODO|FIXME|HACK|WARN|NOTE)[\s:：]+(.+?)(?:\n|$)', re.IGNORECASE)
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
SECTION_RE = re.compile(r'^#{2,6}\s+(.+)$', re.MULTILINE)


# ═══════════════════════════════════════════════════════
# 数据库
# ═══════════════════════════════════════════════════════
CONTENT_SCHEMA = """
CREATE TABLE IF NOT EXISTS content_read_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna TEXT,
    confirm TEXT,
    started_at TEXT,
    completed_at TEXT,
    files_scanned INTEGER,
    files_read INTEGER,
    entities_extracted INTEGER
);

CREATE TABLE IF NOT EXISTS file_contents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT UNIQUE,
    rel_path TEXT,
    layer TEXT,
    content_hash TEXT,
    char_count INTEGER,
    line_count INTEGER,
    summary TEXT,
    headings TEXT,
    sections TEXT,
    dna_codes TEXT,
    confirm_codes TEXT,
    gpg_keys TEXT,
    protocol_refs TEXT,
    todos TEXT,
    tags TEXT,
    read_at TEXT
);

CREATE TABLE IF NOT EXISTS content_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT,
    entity_type TEXT,
    entity_value TEXT,
    context TEXT,
    extracted_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_content_path ON file_contents(file_path);
CREATE INDEX IF NOT EXISTS idx_content_layer ON file_contents(layer);
CREATE INDEX IF NOT EXISTS idx_entities_type ON content_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_value ON content_entities(entity_value);
CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
    file_path, rel_path, summary, headings, sections, content=''
);
"""


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(CONTENT_SCHEMA)
    conn.commit()
    return conn


# ═══════════════════════════════════════════════════════
# 内容提取
# ═══════════════════════════════════════════════════════
def read_text_file(path: Path, max_bytes: int = 2_000_000) -> str:
    """安全读取文本文件，过大则截断"""
    try:
        size = path.stat().st_size
        if size > max_bytes:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(max_bytes) + "\n\n[内容超过2MB，已截断]"
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[读取失败: {e}]"


def extract_headings(text: str) -> List[Tuple[int, str]]:
    """提取标题层级 [(level, title), ...]"""
    return [(len(m.group(1)), m.group(2).strip())
            for m in HEADING_RE.finditer(text)]


def extract_sections(text: str) -> List[str]:
    """提取二级及以上标题作为章节"""
    return [m.group(1).strip() for m in SECTION_RE.finditer(text)]


def extract_protocol_refs(text: str) -> List[str]:
    """提取协议引用编号"""
    seen: Set[str] = set()
    result = []
    for m in PROTOCOL_RE.finditer(text):
        val = m.group(1)
        if val not in seen:
            seen.add(val)
            result.append(val)
    return result


def extract_todos(text: str) -> List[str]:
    """提取 TODO/FIXME 等标记"""
    seen: Set[str] = set()
    result = []
    for m in TODO_RE.finditer(text):
        val = m.group(1).strip()[:200]
        if val not in seen:
            seen.add(val)
            result.append(val)
    return result


def extract_gpg_keys(text: str) -> List[str]:
    """提取 40 位 GPG 指纹"""
    seen: Set[str] = set()
    result = []
    for m in GPG_RE.finditer(text):
        val = m.group(0)
        if val not in seen:
            seen.add(val)
            result.append(val)
    return result


def generate_summary(text: str, max_lines: int = 8) -> str:
    """生成简单摘要：前几句非空内容"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # 过滤掉 DNA/CONFIRM 等元数据行
    content_lines = []
    for line in lines:
        if line.startswith("# DNA:") or line.startswith("# CONFIRM:"):
            continue
        if line.startswith("# SEAL:"):
            continue
        if DNA_RE.match(line) or CONFIRM_RE.search(line):
            continue
        content_lines.append(line)
        if len(content_lines) >= max_lines:
            break
    summary = " | ".join(content_lines[:max_lines])
    return summary[:1000]


def extract_tags(text: str) -> List[str]:
    """提取标签关键词"""
    tags: Set[str] = set()
    patterns = [
        (r'\b(DNA|GPG|CNSH|API|SDK|CLI|Docker|K8s|部署|审计|熔断|人格|协议|三色|君子|龍魂|龍魂|易经|河图|洛书|八卦|五行|DAO)\b', None),
        (r'#([\u4e00-\u9fffA-Za-z0-9_\-]+)', None),
    ]
    for pattern, group in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            tag = m.group(group) if group else m.group(0)
            if tag:
                tags.add(tag.lower())
    return sorted(tags)[:30]


# ═══════════════════════════════════════════════════════
# 扫描与入库
# ═══════════════════════════════════════════════════════
def classify_layer(rel_path: str) -> str:
    parts = Path(rel_path).parts
    if not parts:
        return "root"
    top = parts[0]
    if top.startswith("0") and len(top) >= 2:
        return top
    if top in ("core", "config", "archive", "scripts", "tests"):
        return top
    return "other"


def should_skip_dir(part: str) -> bool:
    """判断目录名是否应跳过"""
    if part in SKIP_DIR_EXACT:
        return True
    return any(part.startswith(p) for p in SKIP_DIR_PREFIX)


def scan_files(root: Path, layer_filter: Optional[str] = None) -> List[Path]:
    """扫描应读取内容的文件"""
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(should_skip_dir(p) for p in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过(防污染/防误读)
        try:
            with open(path, "rb") as f:
                if b"\x00" in f.read(8192):
                    continue
        except OSError:
            continue
        rel = path.relative_to(root)
        layer = classify_layer(str(rel))
        if layer_filter and layer != layer_filter:
            continue
        files.append(path)
    return sorted(files)


def process_file(path: Path, root: Path) -> Optional[Dict[str, Any]]:
    """处理单个文件，返回结构化数据"""
    rel = path.relative_to(root)
    layer = classify_layer(str(rel))
    text = read_text_file(path)
    if text.startswith("[读取失败"):
        return None

    content_hash = hashlib.sha256(text.encode()).hexdigest()
    lines = text.splitlines()

    headings = extract_headings(text)
    sections = extract_sections(text)
    dna_codes = DNA_RE.findall(text)
    confirm_codes = CONFIRM_RE.findall(text)
    gpg_keys = extract_gpg_keys(text)
    protocol_refs = extract_protocol_refs(text)
    todos = extract_todos(text)
    tags = extract_tags(text)
    summary = generate_summary(text)

    return {
        "file_path": str(path),
        "rel_path": str(rel),
        "layer": layer,
        "content_hash": content_hash,
        "char_count": len(text),
        "line_count": len(lines),
        "summary": summary,
        "headings": json.dumps(headings, ensure_ascii=False),
        "sections": json.dumps(sections, ensure_ascii=False),
        "dna_codes": json.dumps(dna_codes, ensure_ascii=False),
        "confirm_codes": json.dumps(confirm_codes, ensure_ascii=False),
        "gpg_keys": json.dumps(gpg_keys, ensure_ascii=False),
        "protocol_refs": json.dumps(protocol_refs, ensure_ascii=False),
        "todos": json.dumps(todos, ensure_ascii=False),
        "tags": json.dumps(tags, ensure_ascii=False),
    }


def save_to_db(conn: sqlite3.Connection, data: Dict[str, Any]):
    """把文件内容写入数据库"""
    conn.execute(
        """INSERT INTO file_contents
           (file_path, rel_path, layer, content_hash, char_count, line_count,
            summary, headings, sections, dna_codes, confirm_codes, gpg_keys,
            protocol_refs, todos, tags, read_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(file_path) DO UPDATE SET
               rel_path=excluded.rel_path,
               layer=excluded.layer,
               content_hash=excluded.content_hash,
               char_count=excluded.char_count,
               line_count=excluded.line_count,
               summary=excluded.summary,
               headings=excluded.headings,
               sections=excluded.sections,
               dna_codes=excluded.dna_codes,
               confirm_codes=excluded.confirm_codes,
               gpg_keys=excluded.gpg_keys,
               protocol_refs=excluded.protocol_refs,
               todos=excluded.todos,
               tags=excluded.tags,
               read_at=excluded.read_at""",
        (data["file_path"], data["rel_path"], data["layer"],
         data["content_hash"], data["char_count"], data["line_count"],
         data["summary"], data["headings"], data["sections"],
         data["dna_codes"], data["confirm_codes"], data["gpg_keys"],
         data["protocol_refs"], data["todos"], data["tags"],
         datetime.now().isoformat()),
    )

    # 写实体表
    conn.execute("DELETE FROM content_entities WHERE file_path = ?", (data["file_path"],))
    entities: List[Tuple[str, List[str]]] = [
        ("dna", json.loads(data["dna_codes"])),
        ("confirm", json.loads(data["confirm_codes"])),
        ("gpg", json.loads(data["gpg_keys"])),
        ("protocol", json.loads(data["protocol_refs"])),
        ("todo", json.loads(data["todos"])),
        ("tag", json.loads(data["tags"])),
    ]
    for etype, values in entities:
        for val in values:
            conn.execute(
                """INSERT INTO content_entities
                   (file_path, entity_type, entity_value, context, extracted_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (data["file_path"], etype, val, data["summary"][:200],
                 datetime.now().isoformat()),
            )

    # 更新 FTS（FTS5 不支持 UPSERT，先删后插）
    conn.execute("DELETE FROM content_fts WHERE file_path = ?", (data["file_path"],))
    conn.execute(
        """INSERT INTO content_fts (file_path, rel_path, summary, headings, sections)
           VALUES (?, ?, ?, ?, ?)""",
        (data["file_path"], data["rel_path"], data["summary"],
         data["headings"], data["sections"]),
    )


# ═══════════════════════════════════════════════════════
# 命令实现
# ═══════════════════════════════════════════════════════
def cmd_scan(args: argparse.Namespace):
    db_path = Path(args.db_path)
    conn = init_db(db_path)

    root = Path(args.root)
    files = scan_files(root, args.layer)
    total = len(files)

    dna = generate_dna("CONTENT-SCAN", "UID9622")
    started_at = datetime.now().isoformat()
    read_count = 0
    entity_count = 0

    print(f"🔍 发现 {total} 个可读文件")
    print(f"🧬 DNA: {dna}\n")

    for i, path in enumerate(files, 1):
        data = process_file(path, root)
        if data is None:
            print(f"[{i:>5}/{total}] ⚠️ 读取失败: {path.name}")
            continue
        save_to_db(conn, data)
        if i % 50 == 0 or i == total:
            conn.commit()
        read_count += 1
        entity_count += (
            len(json.loads(data["dna_codes"])) +
            len(json.loads(data["confirm_codes"])) +
            len(json.loads(data["gpg_keys"])) +
            len(json.loads(data["protocol_refs"])) +
            len(json.loads(data["todos"])) +
            len(json.loads(data["tags"]))
        )
        print(f"[{i:>5}/{total}] ✅ {data['rel_path'][:60]}")

    completed_at = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO content_read_runs
           (dna, confirm, started_at, completed_at, files_scanned,
            files_read, entities_extracted)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (dna, CONFIRM_MARK, started_at, completed_at,
         total, read_count, entity_count),
    )
    conn.commit()
    conn.close()

    print(f"\n📊 内容读取完成")
    print(f"   扫描文件: {total}")
    print(f"   成功读取: {read_count}")
    print(f"   提取实体: {entity_count}")
    print(f"   数据库: {db_path}")
    print(f"🧬 DNA: {dna}")

    # 生成并签名报告
    report = {
        "dna": dna,
        "confirm": CONFIRM_MARK,
        "timestamp": completed_at,
        "files_scanned": total,
        "files_read": read_count,
        "entities_extracted": entity_count,
        "db_path": str(db_path),
    }
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"content_read_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"💾 报告: {report_path}")

    # GPG 签名
    asc_path = Path(str(report_path) + ".asc")
    try:
        subprocess.run(
            ["gpg", "--batch", "--yes", "--detach-sign", "--armor",
             "-u", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
             str(report_path)],
            check=True, capture_output=True,
        )
        print(f"🔏 签名: {asc_path}")
    except Exception as e:
        print(f"⚠️ GPG 签名失败: {e}", file=sys.stderr)


def cmd_query(args: argparse.Namespace):
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"❌ 数据库不存在: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    keyword = args.keyword

    # FTS 搜索（关键词加引号，避免 FTS 查询语法解析错误）
    safe_keyword = '"' + keyword.replace('"', '""') + '"'
    rows = conn.execute(
        """SELECT fc.file_path, fc.rel_path, fc.layer, fc.summary
           FROM content_fts fts
           JOIN file_contents fc ON fc.file_path = fts.file_path
           WHERE content_fts MATCH ?
           LIMIT ?""",
        (safe_keyword, args.limit),
    ).fetchall()

    # 实体搜索
    entity_rows = conn.execute(
        """SELECT DISTINCT file_path, entity_type, entity_value
           FROM content_entities
           WHERE entity_value LIKE ?
           LIMIT ?""",
        (f"%{keyword}%", args.limit),
    ).fetchall()
    entity_paths = {r["file_path"] for r in entity_rows}

    # 合并
    all_paths = set(entity_paths)
    all_paths.update(r["file_path"] for r in rows)

    if not all_paths:
        print(f"🔍 未找到包含 '{keyword}' 的内容")
        return

    print(f"\n🐉 搜索结果: '{keyword}' ({len(all_paths)} 个文件)\n")
    for path in sorted(all_paths)[:args.limit]:
        row = conn.execute(
            "SELECT rel_path, layer, summary FROM file_contents WHERE file_path = ?",
            (path,),
        ).fetchone()
        if row:
            print(f"📄 {row['rel_path']} [{row['layer']}]")
            print(f"   {row['summary'][:160]}...")
            print()

    conn.close()


def cmd_stats(args: argparse.Namespace):
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"❌ 数据库不存在: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))

    total = conn.execute("SELECT COUNT(*) FROM file_contents").fetchone()[0]
    chars = conn.execute("SELECT COALESCE(SUM(char_count), 0) FROM file_contents").fetchone()[0]
    lines = conn.execute("SELECT COALESCE(SUM(line_count), 0) FROM file_contents").fetchone()[0]

    print("\n🐉 内容读取统计")
    print("=" * 60)
    print(f"已读文件: {total}")
    print(f"总字符: {chars:,}")
    print(f"总行数: {lines:,}")

    print("\n按层级分布:")
    for row in conn.execute(
        "SELECT layer, COUNT(*) as c FROM file_contents GROUP BY layer ORDER BY c DESC"
    ):
        print(f"  {row[0] or 'unknown'}: {row[1]}")

    print("\n实体统计:")
    for row in conn.execute(
        "SELECT entity_type, COUNT(*) as c FROM content_entities GROUP BY entity_type ORDER BY c DESC"
    ):
        print(f"  {row[0]}: {row[1]}")

    print("\n热门协议引用:")
    for row in conn.execute(
        """SELECT entity_value, COUNT(*) as c FROM content_entities
           WHERE entity_type = 'protocol' GROUP BY entity_value ORDER BY c DESC LIMIT 10"""
    ):
        print(f"  {row[0]}: {row[1]}")

    print("=" * 60)
    conn.close()


def cmd_orphans(args: argparse.Namespace):
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"❌ 数据库不存在: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # 内容落单：已读但无 DNA、无协议引用、无 TODO
    rows = conn.execute(
        """SELECT file_path, rel_path, layer, char_count, summary
           FROM file_contents
           WHERE (dna_codes = '[]' OR dna_codes IS NULL)
             AND (protocol_refs = '[]' OR protocol_refs IS NULL)
             AND (todos = '[]' OR todos IS NULL)
             AND char_count > 50
           ORDER BY char_count DESC
           LIMIT ?""",
        (args.limit,),
    ).fetchall()

    print(f"\n🐉 内容落单文件（无 DNA/协议/TODO）: {len(rows)} 个\n")
    for r in rows:
        print(f"📄 {r['rel_path']} [{r['layer']}] {r['char_count']} chars")
        print(f"   {r['summary'][:120]}...")
        print()

    conn.close()


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 内容读取器：读正文、抽语义、入库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 08_BIN/lh_content_reader.py scan
  python3 08_BIN/lh_content_reader.py scan --layer 01_protocols
  python3 08_BIN/lh_content_reader.py query CNSH-64
  python3 08_BIN/lh_content_reader.py stats
  python3 08_BIN/lh_content_reader.py orphans
        """,
    )
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH),
                        help=f"SQLite 数据库路径 (默认: {DEFAULT_DB_PATH})")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                        help=f"报告输出目录 (默认: {DEFAULT_OUTPUT_DIR})")

    sub = parser.add_subparsers(dest="command", help="子命令")

    p_scan = sub.add_parser("scan", help="读取文件内容并入库")
    p_scan.add_argument("--root", default=str(PROJECT_ROOT),
                        help=f"扫描根目录 (默认: {PROJECT_ROOT})")
    p_scan.add_argument("--layer", help="只扫描指定层级，如 01_protocols")

    p_query = sub.add_parser("query", help="全文/实体搜索")
    p_query.add_argument("keyword", help="搜索关键词")
    p_query.add_argument("--limit", type=int, default=20, help="最多返回条数")

    sub.add_parser("stats", help="内容统计")

    p_orphans = sub.add_parser("orphans", help="内容落单文件")
    p_orphans.add_argument("--limit", type=int, default=50, help="最多显示条数")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "orphans":
        cmd_orphans(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
