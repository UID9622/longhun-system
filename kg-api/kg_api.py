#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
龍魂知识图谱公开接口 v1.0
DNA: #龍芯⚡️2026-06-28-LONGHUN-KG-API-v1.0
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional

sys.path.insert(0, str(Path.home() / "_work"))
from formula_alignment_search import search as formula_search

from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

HOME = Path.home()
DB_PATH = HOME / ".longhun" / "global_index" / "global_index.db"
OPS_CONSOLE = HOME / "longhun-system" / "ops-console"
PAPERS_DIR = HOME / "longhun-system" / "papers"

app = FastAPI(
    title="龍魂知识图谱公开接口",
    description="LongHun Global Index Knowledge Graph Public API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def fmt_size(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def dna_for_file(file_id: int, path: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    import hashlib
    h = hashlib.blake2b(f"{ts}-{file_id}-{path}".encode(), digest_size=8).hexdigest()
    return f"#龍芯⚡️{ts}-KG-PUBLIC-F{file_id}-{h.upper()}"


@app.get("/api/knowledge/search", summary="全局索引搜索")
def knowledge_search(
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(20, ge=1, le=200),
    sort: str = Query("relevance", regex="^(relevance|date|type|size)$"),
):
    if not DB_PATH.exists():
        return {"total": 0, "results": [], "error": "索引数据库未就绪"}

    conn = get_db()
    like = f"%{q}%"
    order = {
        "relevance": "changed_at DESC",
        "date": "mtime DESC",
        "type": "SUBSTR(path, INSTR(path, '.') + 1)",
        "size": "size DESC",
    }.get(sort, "changed_at DESC")

    rows = conn.execute(
        f"""SELECT f.id, f.path, f.size, f.mtime, f.hash, f.changed_at,
                   MAX(CASE WHEN f.path LIKE ? THEN 2 ELSE 1 END) AS score
            FROM files f
            LEFT JOIN metadata m ON m.file_id = f.id
            WHERE f.accessible=1 AND (f.path LIKE ? OR m.value LIKE ?)
            GROUP BY f.id
            ORDER BY score DESC, {order}
            LIMIT ?""",
        (f"%{q}%", like, like, limit),
    ).fetchall()

    # 批量拉取命中文件的元数据（标题、摘要等）
    file_ids = [r["id"] for r in rows]
    metadata_map: dict[int, dict[str, str]] = {fid: {} for fid in file_ids}
    if file_ids:
        placeholders = ",".join("?" * len(file_ids))
        for m in conn.execute(
            f"SELECT file_id, key, value FROM metadata WHERE file_id IN ({placeholders})",
            file_ids,
        ).fetchall():
            metadata_map[m["file_id"]][m["key"]] = m["value"]

    results = []
    for r in rows:
        p = Path(r["path"])
        ext = p.suffix.lower()
        file_type = "file"
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".tiff"]:
            file_type = "image"
        elif ext in [".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg"]:
            file_type = "audio"
        elif ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
            file_type = "video"
        elif ext in [".pdf", ".doc", ".docx", ".txt", ".md", ".pages"]:
            file_type = "document"

        dna = dna_for_file(r["id"], r["path"])
        meta = metadata_map.get(r["id"], {})
        results.append({
            "id": r["id"],
            "filename": p.name,
            "path": r["path"],
            "type": file_type,
            "extension": ext,
            "size": r["size"],
            "size_human": fmt_size(r["size"] or 0),
            "mtime": datetime.fromtimestamp(r["mtime"]).isoformat() if r["mtime"] else None,
            "hash": r["hash"],
            "dna": dna,
            "trace_url": f"/api/dna/trace/{dna}",
            "metadata": meta,
        })

    return {
        "query": q,
        "total": len(results),
        "sort": sort,
        "public_access": "无需登录，可公开引用",
        "results": results,
    }


@app.get("/api/dna/trace/{dna_code}", summary="DNA入侵追溯")
def dna_trace(dna_code: str):
    if not DB_PATH.exists():
        raise HTTPException(status_code=503, detail="索引数据库未就绪")

    conn = get_db()
    file_id = None

    # 解析 KG-PUBLIC DNA 中的文件ID: #龍芯⚡️...-KG-PUBLIC-F{file_id}-{hash}
    m = re.search(r"-KG-PUBLIC-F(\d+)-", dna_code)
    if m:
        file_id = int(m.group(1))

    file_match = None
    if file_id:
        rows = conn.execute("SELECT * FROM files WHERE id=? LIMIT 1", (file_id,)).fetchall()
        if rows:
            r = rows[0]
            file_match = {
                "id": r["id"],
                "path": r["path"],
                "size": r["size"],
                "size_human": fmt_size(r["size"] or 0),
                "mtime": datetime.fromtimestamp(r["mtime"]).isoformat() if r["mtime"] else None,
                "indexed_at": datetime.fromtimestamp(r["indexed_at"]).isoformat() if r["indexed_at"] else None,
                "hash": r["hash"],
                "hash_algorithm": r["hash_algo"],
            }

    # 同时查询 events 表中的真实 DNA 记录
    event_rows = conn.execute(
        "SELECT * FROM events WHERE dna=? ORDER BY timestamp DESC LIMIT 10",
        (dna_code,),
    ).fetchall()
    related = []
    for r in event_rows:
        related.append({
            "timestamp": datetime.fromtimestamp(r["timestamp"]).isoformat(),
            "event_type": r["event_type"],
            "path": r["path"],
            "details": r["details"],
        })

    # 如果 events 中有路径但 file_id 没命中，用路径补查
    if not file_match and related and related[0].get("path"):
        path = related[0]["path"]
        rows = conn.execute("SELECT * FROM files WHERE path=? LIMIT 1", (path,)).fetchall()
        if rows:
            r = rows[0]
            file_match = {
                "id": r["id"],
                "path": r["path"],
                "size": r["size"],
                "size_human": fmt_size(r["size"] or 0),
                "mtime": datetime.fromtimestamp(r["mtime"]).isoformat() if r["mtime"] else None,
                "indexed_at": datetime.fromtimestamp(r["indexed_at"]).isoformat() if r["indexed_at"] else None,
                "hash": r["hash"],
                "hash_algorithm": r["hash_algo"],
            }

    # 查找近期关联事件（同一文件路径）
    history = []
    if file_match:
        assoc = conn.execute(
            "SELECT event_type, timestamp, details FROM events WHERE path=? ORDER BY timestamp DESC LIMIT 10",
            (file_match["path"],),
        ).fetchall()
        history = [
            {"event_type": a["event_type"],
             "timestamp": datetime.fromtimestamp(a["timestamp"]).isoformat(),
             "details": a["details"]} for a in assoc
        ]

    return {
        "dna": dna_code,
        "traceable": file_match is not None,
        "public_citation": f"https://longhun888.com:8088/api/dna/trace/{dna_code}",
        "embed_code": f'<iframe src="https://longhun888.com:8088/api/dna/trace/{dna_code}" width="100%" height="300"></iframe>',
        "file": file_match,
        "related_events": related,
        "history": history,
    }


def _parse_paper_meta(path: Path) -> dict:
    text = path.stem
    # 尝试提取日期 2024-01 / 202401 / 2024
    dates = re.findall(r"(20\d{2})[-_ ]?(0[1-9]|1[0-2])[-_ ]?([0-2][0-9]|3[01])?", text)
    year = dates[0][0] if dates else str(datetime.fromtimestamp(path.stat().st_mtime).year)
    month = dates[0][1] if dates else None

    # 主题关键词简单推断
    topics = []
    topic_keywords = {
        "CNSH": "CNSH中文原生",
        "Riemann": "黎曼猜想",
        "riemann": "黎曼猜想",
        "AI": "人工智能",
        "ai": "人工智能",
        "区块链": "区块链",
        "web3": "Web3",
        "DNA": "DNA追溯",
        " sovereignty": "主权体系",
        "主权": "主权体系",
        "六壬": "六壬",
        "易经": "易经",
        "论文": "学术论文",
        "顶刊": "顶刊投稿",
        "Review": "文献综述",
    }
    for kw, topic in topic_keywords.items():
        if kw in text:
            topics.append(topic)
    if not topics:
        topics.append("未分类")

    # 作者推断：文件名中 "_by_xxx" 或 "-作者-"
    authors = []
    m = re.search(r"[ _]by[ _]([^_\-]+)", text, re.IGNORECASE)
    if m:
        authors.append(m.group(1))
    m = re.search(r"作者[ _\-]*([^_\-]+)", text)
    if m:
        authors.append(m.group(1))
    if not authors:
        authors.append("UID9622")

    return {
        "filename": path.name,
        "title": text.replace("_", " ").replace("-", " ").strip(),
        "authors": authors,
        "year": year,
        "month": month,
        "topics": list(set(topics)),
        "path": str(path),
        "size": path.stat().st_size,
        "size_human": fmt_size(path.stat().st_size),
        "mtime": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
    }


def _cite_apa(p: dict) -> str:
    authors = ", ".join(p["authors"])
    return f"{authors} ({p['year']}). {p['title']}. 龍魂知识图谱. {p['path']}"


def _cite_mla(p: dict) -> str:
    authors = ", ".join(p["authors"])
    return f'"{p["title"]}." 龍魂知识图谱, {p["year"]}, {p["path"]}.'


def _cite_gb(p: dict) -> str:
    authors = ", ".join(p["authors"])
    return f"[{1}] {authors}. {p['title']}[R]. 龍魂知识图谱, {p['year']}."


@app.get("/api/knowledge/classify", summary="论文分类与引用")
def knowledge_classify(
    topic: Optional[str] = Query(None, description="按主题过滤"),
    year: Optional[str] = Query(None, description="按年份过滤"),
    author: Optional[str] = Query(None, description="按作者过滤"),
):
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    papers = []
    for p in PAPERS_DIR.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            meta = _parse_paper_meta(p)
            papers.append(meta)

    # 过滤
    if topic:
        papers = [p for p in papers if topic in p["topics"]]
    if year:
        papers = [p for p in papers if p["year"] == year]
    if author:
        papers = [p for p in papers if any(author.lower() in a.lower() for a in p["authors"])]

    # 分类统计
    by_topic = {}
    by_year = {}
    for p in papers:
        for t in p["topics"]:
            by_topic[t] = by_topic.get(t, 0) + 1
        by_year[p["year"]] = by_year.get(p["year"], 0) + 1

    # 添加引用格式和公开URL
    enriched = []
    for p in papers:
        p = dict(p)
        p["citations"] = {
            "apa": _cite_apa(p),
            "mla": _cite_mla(p),
            "gb_t_7714": _cite_gb(p),
        }
        p["public_url"] = f"/api/knowledge/search?q={p['filename']}"
        enriched.append(p)

    return {
        "total": len(enriched),
        "papers_dir": str(PAPERS_DIR),
        "classifications": {
            "by_topic": by_topic,
            "by_year": by_year,
        },
        "public_access": "无需登录，可公开引用",
        "papers": enriched,
    }


@app.get("/api/knowledge/formula/search", summary="公式对准表向量检索")
def formula_search_api(
    q: str = Query(..., description="公式关键词"),
    top: int = Query(5, ge=1, le=20),
):
    results = formula_search(q, top_k=top)
    return {
        "query": q,
        "total": len(results),
        "module_id": "formula_alignment_v1_6",
        "dna": dna_for_file(0, f"formula-search-{q}"),
        "public_access": "无需登录，可公开引用",
        "results": results,
    }


@app.get("/api/health", summary="服务健康检查")
def health():
    db_ok = DB_PATH.exists()
    return {
        "status": "ok" if db_ok else "degraded",
        "dna": dna_for_file(0, "health-check"),
        "database_ready": db_ok,
        "timestamp": datetime.now().isoformat(),
    }


# 静态文件：ops-console
if OPS_CONSOLE.exists():
    app.mount("/ops", StaticFiles(directory=str(OPS_CONSOLE), html=True), name="ops-console")


@app.get("/", response_class=HTMLResponse)
def root():
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>龍魂知识图谱 API</title></head>
<body style="font-family:sans-serif;max-width:800px;margin:40px auto;line-height:1.8">
<h1>🐉 龍魂知识图谱公开接口</h1>
<p>DNA: #龍芯⚡️2026-06-28-LONGHUN-KG-API-v1.0</p>
<h2>公开端点</h2>
<ul>
<li><code>GET /api/knowledge/search?q={关键词}&limit=20&sort=relevance</code></li>
<li><code>GET /api/dna/trace/{dna_code}</code></li>
<li><code>GET /api/knowledge/classify?topic=&year=&author=</code></li>
<li><code>GET /api/knowledge/formula/search?q={关键词}&top=5</code></li>
<li><code>GET /api/health</code></li>
<li><a href="/ops/index.html">龍魂操作台</a></li>
</ul>
<p>所有接口公开访问，无需登录，可引用。</p>
</body>
</html>"""
