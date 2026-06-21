#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂知识库与图谱 API · LongHun Knowledge & Graph API

公开只读接口：
  - 中央藏经阁文档检索
  - dragon_knowledge.db 代码收割记录检索
  - 公开知识图谱节点/边/一跳查询

DNA:#龍芯⚡️2026-06-19-LONGHUN-KNOWLEDGE-GRAPH-v1.0
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["knowledge"])


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = uuid.uuid4().hex[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── 路径发现 ──────────────────────────────────────────────
def _find_archive_index() -> Optional[Path]:
    candidates = [
        os.environ.get("CNSH_ARCHIVE_INDEX", ""),
        str(Path.home() / "CNSH" / "中央藏经阁索引.json"),
        "/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 7/CNSH/中央藏经阁索引.json",
        "/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 6/CNSH/中央藏经阁索引.json",
        "/root/longhun-sovereignty/CNSH/中央藏经阁索引.json",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return Path(c)
    return None


def _find_knowledge_db() -> Optional[Path]:
    candidates = [
        os.environ.get("DRAGON_KNOWLEDGE_DB", ""),
        str(Path.home() / "_work" / "dragon_knowledge.db"),
        "/root/_work/dragon_knowledge.db",
        "/Users/zuimeidedeyihan/_work/dragon_knowledge.db",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return Path(c)
    return None


_ARCHIVE_PATH: Optional[Path] = _find_archive_index()
_KNOWLEDGE_DB: Optional[Path] = _find_knowledge_db()


# ── 数据加载 ──────────────────────────────────────────────
def _load_archive() -> Dict[str, dict]:
    if not _ARCHIVE_PATH:
        return {}
    try:
        with open(_ARCHIVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("文档列表", {})
    except Exception:
        return {}


def _archive_docs_list() -> List[Dict]:
    docs = _load_archive()
    result = []
    for name, meta in docs.items():
        m = dict(meta)
        m.setdefault("id", f"doc:{name}")
        result.append(m)
    return result


def _search_knowledge_db(q: str, limit: int = 20) -> List[Dict]:
    if not _KNOWLEDGE_DB:
        return []
    rows = []
    try:
        conn = sqlite3.connect(f"file:{_KNOWLEDGE_DB}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        pattern = f"%{q}%"
        cur.execute(
            """
            SELECT code_id, file_name, file_path, file_extension, source_language,
                   theory_guide, source_url_or_path, author, dna_code, cnsh_version,
                   content_hash, substr(content_raw, 1, 300) AS content_preview
            FROM harvested_code
            WHERE file_name LIKE ? OR file_path LIKE ? OR source_language LIKE ?
                  OR theory_guide LIKE ? OR dna_code LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (pattern, pattern, pattern, pattern, pattern, limit),
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
    except Exception as e:
        return [{"error": str(e)[:200]}]
    return rows


# ── 图谱构建 ──────────────────────────────────────────────
def _build_graph() -> Dict:
    nodes: List[Dict] = []
    edges: List[Dict] = []
    node_ids = set()

    def add_node(nid: str, label: str, group: str, meta: Optional[Dict] = None):
        if nid in node_ids:
            return
        node_ids.add(nid)
        nodes.append({"id": nid, "label": label, "group": group, "meta": meta or {}})

    # 中央藏经阁文档节点 + 关键词节点
    docs = _archive_docs_list()
    keyword_docs: Dict[str, List[str]] = {}
    for doc in docs:
        did = doc.get("id", f"doc:{doc.get('名称')}")
        add_node(did, doc.get("名称", did), "doc", {
            "类别": doc.get("类别"),
            "五行": doc.get("五行"),
            "审计等级": doc.get("审计等级"),
            "DNA": doc.get("DNA"),
        })
        # 关键词
        for kw in doc.get("关键词", []):
            kid = f"kw:{kw}"
            add_node(kid, kw, "keyword")
            edges.append({"source": did, "target": kid, "relation": "has_keyword"})
            keyword_docs.setdefault(kw, []).append(did)
        # 五行
        element = doc.get("五行")
        if element:
            eid = f"element:{element}"
            add_node(eid, element, "element")
            edges.append({"source": did, "target": eid, "relation": "belongs_to"})
        # DNA 前缀聚类（取第一个 '-' 前段作为项目代号）
        dna = doc.get("DNA", "")
        if dna and "-" in dna:
            prefix = dna.split("-")[0].replace("#龍芯⚡️", "")
            pid = f"dna_prefix:{prefix}"
            add_node(pid, prefix, "dna_prefix")
            edges.append({"source": did, "target": pid, "relation": "traced_to"})

    # 文档-文档：共享关键词
    for kw, dids in keyword_docs.items():
        for i in range(len(dids)):
            for j in range(i + 1, len(dids)):
                edges.append({"source": dids[i], "target": dids[j], "relation": "shares_keyword", "keyword": kw})

    # 代码收割库节点
    if _KNOWLEDGE_DB:
        try:
            conn = sqlite3.connect(f"file:{_KNOWLEDGE_DB}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                """
                SELECT code_id, file_name, file_path, file_extension, source_language,
                       dna_code, author
                FROM harvested_code
                LIMIT 500
                """
            )
            for row in cur.fetchall():
                r = dict(row)
                cid = f"code:{r['code_id']}"
                label = r["file_name"].split("/")[-1] if r["file_name"] else cid
                add_node(cid, label, "code", {
                    "language": r.get("source_language"),
                    "extension": r.get("file_extension"),
                    "author": r.get("author"),
                    "dna": r.get("dna_code"),
                })
                # 语言节点
                lang = r.get("source_language") or (r.get("file_extension") or "").lstrip(".")
                if lang:
                    lid = f"lang:{lang}"
                    add_node(lid, lang, "language")
                    edges.append({"source": cid, "target": lid, "relation": "written_in"})
                # 作者节点
                author = r.get("author")
                if author:
                    aid = f"author:{author}"
                    add_node(aid, author, "author")
                    edges.append({"source": cid, "target": aid, "relation": "authored_by"})
            conn.close()
        except Exception:
            pass

    return {"nodes": nodes, "edges": edges}


_GRAPH_CACHE: Optional[Dict] = None


def _get_graph() -> Dict:
    global _GRAPH_CACHE
    if _GRAPH_CACHE is None:
        _GRAPH_CACHE = _build_graph()
    return _GRAPH_CACHE


# ── Pydantic 模型 ─────────────────────────────────────────
class GraphQuery(BaseModel):
    node_id: str
    depth: int = Field(1, ge=1, le=3)


class KnowledgeSearch(BaseModel):
    q: str = Field(..., min_length=1)
    limit: int = Field(20, ge=1, le=100)


# ── 路由 ──────────────────────────────────────────────────
@router.get("/archive/docs")
def archive_docs(
    q: Optional[str] = None,
    category: Optional[str] = None,
    element: Optional[str] = None,
    audit: Optional[str] = None,
):
    """中央藏经阁文档列表，支持关键词/类别/五行/审计等级过滤"""
    docs = _archive_docs_list()
    if q:
        docs = [d for d in docs if q.lower() in json.dumps(d, ensure_ascii=False).lower()]
    if category:
        docs = [d for d in docs if d.get("类别") == category]
    if element:
        docs = [d for d in docs if d.get("五行") == element]
    if audit:
        docs = [d for d in docs if d.get("审计等级") == audit]
    return {
        "dna": _dna("ARCHIVE-DOCS"),
        "timestamp": _now(),
        "count": len(docs),
        "docs": docs,
    }


@router.get("/archive/doc/{name}")
def archive_doc(name: str):
    """单篇中央藏经阁文档元数据"""
    docs = _load_archive()
    if name not in docs:
        raise HTTPException(status_code=404, detail=f"文档 {name} 不存在")
    return {
        "dna": _dna("ARCHIVE-DOC"),
        "timestamp": _now(),
        "doc": docs[name],
    }


@router.post("/knowledge/search")
def knowledge_search(req: KnowledgeSearch):
    """检索 dragon_knowledge.db 代码收割记录"""
    rows = _search_knowledge_db(req.q, req.limit)
    return {
        "dna": _dna("KNOWLEDGE-SEARCH"),
        "timestamp": _now(),
        "query": req.q,
        "count": len(rows),
        "results": rows,
    }


@router.get("/knowledge/search")
def knowledge_search_get(q: str, limit: int = 20):
    """GET 版知识检索，便于浏览器直接测试"""
    rows = _search_knowledge_db(q, limit)
    return {
        "dna": _dna("KNOWLEDGE-SEARCH"),
        "timestamp": _now(),
        "query": q,
        "count": len(rows),
        "results": rows,
    }


@router.get("/graph/nodes")
def graph_nodes():
    """知识图谱所有节点"""
    g = _get_graph()
    return {
        "dna": _dna("GRAPH-NODES"),
        "timestamp": _now(),
        "count": len(g["nodes"]),
        "nodes": g["nodes"],
    }


@router.get("/graph/edges")
def graph_edges():
    """知识图谱所有边"""
    g = _get_graph()
    return {
        "dna": _dna("GRAPH-EDGES"),
        "timestamp": _now(),
        "count": len(g["edges"]),
        "edges": g["edges"],
    }


@router.post("/graph/query")
def graph_query(req: GraphQuery):
    """从指定节点出发，查询 depth 跳内的子图"""
    g = _get_graph()
    node_set = {req.node_id}
    current = {req.node_id}
    for _ in range(req.depth):
        nxt = set()
        for e in g["edges"]:
            if e["source"] in current:
                nxt.add(e["target"])
            if e["target"] in current:
                nxt.add(e["source"])
        current = nxt
        node_set |= nxt

    sub_nodes = [n for n in g["nodes"] if n["id"] in node_set]
    sub_edges = [
        e for e in g["edges"]
        if e["source"] in node_set and e["target"] in node_set
    ]
    return {
        "dna": _dna("GRAPH-QUERY"),
        "timestamp": _now(),
        "center": req.node_id,
        "depth": req.depth,
        "node_count": len(sub_nodes),
        "edge_count": len(sub_edges),
        "nodes": sub_nodes,
        "edges": sub_edges,
    }


@router.get("/graph/stats")
def graph_stats():
    """图谱统计"""
    g = _get_graph()
    groups = {}
    for n in g["nodes"]:
        groups[n["group"]] = groups.get(n["group"], 0) + 1
    return {
        "dna": _dna("GRAPH-STATS"),
        "timestamp": _now(),
        "node_count": len(g["nodes"]),
        "edge_count": len(g["edges"]),
        "groups": groups,
    }
