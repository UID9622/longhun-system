#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🇨🇳 中国科技自主创新专栏 · 知识图谱 API
通过 Neo4j HTTP 接口查询本地图数据库，挂到 sovereignty/portal API 上。

端点前缀: /api/cn-innovation-kg
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated

sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/08_BIN")
from ganzhi_dna_engine import DNA生成

router = APIRouter(prefix="/api/cn-innovation-kg", tags=["cn-innovation-kg"])

NEO4J_URL = os.environ.get("NEO4J_HTTP_URL", "http://localhost:7474/db/neo4j/tx/commit")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASSWORD", "longhun123")


def _dna(prefix: str) -> str:
    return DNA生成(
        模块=f"CN-INNOVATION-KG-{prefix}",
        动作="API",
        版本="V1.0",
        级别="P1",
    )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run_cypher(statement: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """通过 Neo4j HTTP 事务端点执行 Cypher，返回行列表（每行是列名->值字典）。"""
    payload = {"statements": [{"statement": statement}]}
    if parameters:
        payload["statements"][0]["parameters"] = parameters

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        NEO4J_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{NEO4J_USER}:{NEO4J_PASS}".encode()).decode(),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")[:400]
        raise HTTPException(status_code=502, detail=f"Neo4j HTTP error: {e.code} {body}")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Neo4j unreachable: {e}")

    if result.get("errors"):
        msgs = "; ".join(str(err) for err in result["errors"][:3])
        raise HTTPException(status_code=502, detail=f"Neo4j Cypher error: {msgs}")

    rows: List[Dict[str, Any]] = []
    for res in result.get("results", []):
        columns = res.get("columns", [])
        for item in res.get("data", []):
            row = item.get("row", [])
            rows.append({col: val for col, val in zip(columns, row)})
    return rows


def _safe(value: Any) -> Any:
    """过滤 Neo4j 节点/关系中的 None 与空字符串，便于 JSON 序列化。"""
    if isinstance(value, dict):
        return {k: _safe(v) for k, v in value.items() if v not in (None, "")}
    if isinstance(value, list):
        return [_safe(v) for v in value if v not in (None, "")]
    return value


# ── Pydantic 模型 ─────────────────────────────────────────
class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1)
    limit: int = Field(20, ge=1, le=100)


class ExpandRequest(BaseModel):
    node_id: str
    depth: int = Field(1, ge=1, le=3)


# ── 路由 ──────────────────────────────────────────────────
@router.get("/stats")
def stats():
    """图谱整体统计"""
    node_rows = _run_cypher("MATCH (n) RETURN labels(n)[0] AS type, count(n) AS cnt ORDER BY cnt DESC")
    edge_rows = _run_cypher("MATCH ()-[r]->() RETURN type(r) AS rel, count(r) AS cnt ORDER BY cnt DESC")
    return {
        "dna": _dna("STATS"),
        "timestamp": _now(),
        "nodes": {r["type"]: r["cnt"] for r in node_rows},
        "edges": {r["rel"]: r["cnt"] for r in edge_rows},
    }


def _list_articles_core(
    field: Optional[str] = None,
    tag: Optional[str] = None,
    status: Optional[str] = None,
    persona: Optional[str] = None,
    venue: Optional[str] = None,
    wuxing: Optional[str] = None,
    layer: Optional[str] = None,
    importance: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """论文列表核心逻辑（纯 Python，避免 FastAPI Query 对象混入 Cypher 参数）。"""
    where_clauses: List[str] = []
    params: Dict[str, Any] = {}

    if q:
        where_clauses.append(
            "(toLower(a.label) CONTAINS toLower($q) OR toLower(a.一句话摘要) CONTAINS toLower($q) OR toLower(a.IPA) CONTAINS toLower($q))"
        )
        params["q"] = q

    def add_filter(rel_type: str, node_label: str, param_name: str, value: Optional[str]):
        nonlocal where_clauses, params
        if value:
            where_clauses.append(
                f"EXISTS {{ MATCH (a)-[:{rel_type}]->(b:{node_label}) WHERE b.label = ${param_name} }}"
            )
            params[param_name] = value

    add_filter("belongs_to", "Field", "field", field)
    add_filter("has_tag", "Tag", "tag", tag)
    add_filter("has_status", "Status", "status", status)
    add_filter("routed_to", "Persona", "persona", persona)
    add_filter("targets_venue", "Venue", "venue", venue)
    add_filter("has_wuxing", "Wuxing", "wuxing", wuxing)
    add_filter("in_layer", "Layer", "layer", layer)
    add_filter("has_importance", "Importance", "importance", importance)

    where_str = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    cypher = f"""
        MATCH (a:Article)
        {where_str}
        RETURN a.id AS id, a.label AS title, a.状态 AS status, a.重要程度 AS importance,
               a.IPA AS ipa, a.一句话摘要 AS summary, a.易经锚点 AS yijing
        ORDER BY a.id
        SKIP $offset LIMIT $limit
    """
    params["offset"] = int(offset)
    params["limit"] = int(limit)
    rows = _run_cypher(cypher, params)
    return {
        "dna": _dna("ARTICLES-LIST"),
        "timestamp": _now(),
        "count": len(rows),
        "offset": int(offset),
        "limit": int(limit),
        "articles": [_safe(r) for r in rows],
    }


@router.get("/articles")
def list_articles(
    field: Optional[str] = None,
    tag: Optional[str] = None,
    status: Optional[str] = None,
    persona: Optional[str] = None,
    venue: Optional[str] = None,
    wuxing: Optional[str] = None,
    layer: Optional[str] = None,
    importance: Optional[str] = None,
    q: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """论文列表，支持多维度过滤与关键词搜索"""
    return _list_articles_core(
        field=field, tag=tag, status=status, persona=persona, venue=venue,
        wuxing=wuxing, layer=layer, importance=importance, q=q,
        limit=limit, offset=offset,
    )


@router.get("/article/{article_id}")
def article_detail(article_id: str):
    """单篇论文详情 + 一跳邻居"""
    rows = _run_cypher(
        """
        MATCH (a:Article {id: $id})
        OPTIONAL MATCH (a)-[r]->(b)
        RETURN a.id AS id, a.label AS title, a.状态 AS status, a.重要程度 AS importance,
               a.IPA AS ipa, a.一句话摘要 AS summary, a.易经锚点 AS yijing,
               a.DNA追溯码 AS dna, a.短DNA身份码 AS short_dna, a.dr五行宫位 AS dr,
               a.α三义 AS alpha, a.来源 AS source,
               collect({rel: type(r), target: b.id, target_label: b.label, target_type: labels(b)[0]}) AS neighbors
        """,
        {"id": article_id},
    )
    if not rows:
        raise HTTPException(status_code=404, detail=f"论文 {article_id} 不存在")
    row = rows[0]
    row["neighbors"] = [n for n in row["neighbors"] if n["target"]]
    return {
        "dna": _dna("ARTICLE-DETAIL"),
        "timestamp": _now(),
        "article": _safe(row),
    }


@router.post("/search")
def search(req: SearchRequest):
    """全文关键词搜索论文"""
    return _list_articles_core(q=req.q, limit=req.limit)


@router.get("/search")
def search_get(q: str, limit: int = 20):
    """GET 版搜索，便于浏览器直接测试"""
    return _list_articles_core(q=q, limit=limit)


@router.get("/facets")
def facets():
    """所有维度分面及计数（领域、标签、人格、顶刊、五行、架构层级、状态、重要程度）"""
    queries = {
        "fields": ("belongs_to", "Field"),
        "tags": ("has_tag", "Tag"),
        "personas": ("routed_to", "Persona"),
        "venues": ("targets_venue", "Venue"),
        "wuxings": ("has_wuxing", "Wuxing"),
        "layers": ("in_layer", "Layer"),
        "statuses": ("has_status", "Status"),
        "importances": ("has_importance", "Importance"),
    }
    result: Dict[str, List[Dict[str, Any]]] = {}
    for key, (rel, label) in queries.items():
        rows = _run_cypher(
            f"""
            MATCH (a:Article)-[:{rel}]->(b:{label})
            RETURN b.label AS label, count(a) AS cnt
            ORDER BY cnt DESC
            """
        )
        result[key] = _safe(rows)
    return {
        "dna": _dna("FACETS"),
        "timestamp": _now(),
        "facets": result,
    }


@router.get("/field/{field_label}")
def field_articles(field_label: str):
    """某个领域下的所有论文"""
    return _list_articles_core(field=field_label)


@router.get("/tag/{tag_label}")
def tag_articles(tag_label: str):
    """某个标签下的所有论文"""
    return _list_articles_core(tag=tag_label)


@router.get("/persona/{persona_label}")
def persona_articles(persona_label: str):
    """某个人格路由下的所有论文"""
    return _list_articles_core(persona=persona_label)


@router.get("/venue/{venue_label}")
def venue_articles(venue_label: str):
    """某个顶刊目标下的所有论文"""
    return _list_articles_core(venue=venue_label)


@router.post("/expand")
def expand(req: ExpandRequest):
    """从指定节点出发扩展 depth 跳子图"""
    # 使用 Neo4j 的 apoc.path.subgraphAll 需要 APOC；这里用简单路径查询 depth<=N
    depth = int(req.depth)
    rows = _run_cypher(
        f"""
        MATCH (start)
        WHERE start.id = $node_id
        OPTIONAL MATCH path = (start)-[*1..{depth}]->(n)
        WITH start, collect(DISTINCT n) AS nodes, collect(DISTINCT last(relationships(path))) AS rels
        RETURN start.id AS center_id, start.label AS center_label,
               [x IN nodes | {{id: x.id, label: x.label, type: labels(x)[0]}}] AS nodes,
               [r IN rels | {{source: startNode(r).id, target: endNode(r).id, type: type(r)}}] AS edges
        """,
        {"node_id": req.node_id},
    )
    if not rows:
        raise HTTPException(status_code=404, detail=f"节点 {req.node_id} 不存在")
    row = rows[0]
    # 合并中心节点
    all_nodes = {row["center_id"]: {"id": row["center_id"], "label": row["center_label"]}}
    for n in row["nodes"]:
        if n and n["id"]:
            all_nodes[n["id"]] = n
    return {
        "dna": _dna("GRAPH-EXPAND"),
        "timestamp": _now(),
        "center": req.node_id,
        "depth": req.depth,
        "node_count": len(all_nodes),
        "edge_count": len(row["edges"]),
        "nodes": list(all_nodes.values()),
        "edges": [e for e in row["edges"] if e],
    }


@router.get("/expand")
def expand_get(node_id: str, depth: int = 1):
    """GET 版子图扩展"""
    return expand(ExpandRequest(node_id=node_id, depth=depth))
