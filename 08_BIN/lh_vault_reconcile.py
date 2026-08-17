#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🔄 龍魂·剪贴板容器 · Neo4j 索引自检与补齐 v1.0
================================================
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷽小过-VAULT-RECONCILE-V1.0-P1

启动时扫描 06_CONTAINERS/clipboard-vault/，对比本地 Neo4j 中的 Clip 节点，
把缺失的节点/关系补齐，避免文件与图谱之间的数据漂移。

用法:
  python3 08_BIN/lh_vault_reconcile.py           # 只补齐缺失
  python3 08_BIN/lh_vault_reconcile.py --prune   # 同时清理 Neo4j 中已不存在的 Clip
"""

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
sys.path.insert(0, str(PROJECT_ROOT / "05_ENGINES"))

from ganzhi_dna_engine import DNA生成
from lh_clipboard_vault import list_vault

CST = timezone(timedelta(hours=8))
NEO4J_URL = os.environ.get("NEO4J_HTTP_URL", "http://localhost:7474/db/neo4j/tx/commit")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASSWORD", "longhun123")


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _dna() -> str:
    return DNA生成(模块="VAULT-RECONCILE", 动作="SYNC", 版本="V1.0", 级别="P1")


def _cypher_escape(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
    return f'"{s}"'


def _run_cypher(statements: List[str]) -> Dict[str, Any]:
    payload = {"statements": [{"statement": s} for s in statements]}
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
        raise RuntimeError(f"Neo4j HTTP error: {e.code} {body}")
    except Exception as e:
        raise RuntimeError(f"Neo4j unreachable: {e}")

    if result.get("errors"):
        msgs = "; ".join(str(err) for err in result["errors"][:3])
        raise RuntimeError(f"Neo4j Cypher error: {msgs}")
    return result


def _topic_id(topic: str) -> str:
    return f"VAULT-TOPIC:{hashlib.md5(topic.encode()).hexdigest()[:8]}"


def _tag_id(tag: str) -> str:
    return f"VAULT-TAG:{hashlib.md5(tag.encode()).hexdigest()[:8]}"


def _clip_node_id(content_hash: str) -> str:
    return f"CLIP:{content_hash[:16]}"


def get_existing_clip_ids() -> Set[str]:
    """查询 Neo4j 中已有的 Clip 节点 id。"""
    try:
        result = _run_cypher(["MATCH (c:Clip) RETURN c.id AS id"])
        ids: Set[str] = set()
        for res in result.get("results", []):
            for item in res.get("data", []):
                row = item.get("row", [])
                if row:
                    ids.add(row[0])
        return ids
    except Exception:
        return set()


def reconcile(prune: bool = False) -> Dict[str, Any]:
    clips = list_vault()
    existing_ids = get_existing_clip_ids()
    file_ids = {_clip_node_id(c["content_hash"]) for c in clips}

    missing = [c for c in clips if _clip_node_id(c["content_hash"]) not in existing_ids]
    orphan_ids = existing_ids - file_ids if prune else set()

    statements: List[str] = []
    topic_ids: Set[str] = set()
    tag_ids: Set[str] = set()

    for clip in missing:
        cid = _clip_node_id(clip["content_hash"])
        label = Path(clip["path"]).stem
        statements.append(
            f"MERGE (c:Clip {{id: {_cypher_escape(cid)}}}) "
            f"SET c.label = {_cypher_escape(label)}, "
            f"    c.dna = {_cypher_escape(clip['dna'])}, "
            f"    c.source = {_cypher_escape(clip['source'])}, "
            f"    c.timestamp = {_cypher_escape(clip['timestamp'])}, "
            f"    c.updated_at = {_cypher_escape(clip.get('updated_at', clip['timestamp']))}, "
            f"    c.copy_count = {clip.get('copy_count', 1)}, "
            f"    c.path = {_cypher_escape(clip['path'])}, "
            f"    c.hash = {_cypher_escape(clip['content_hash'])}"
        )

        topic = clip["topic"]
        tid = _topic_id(topic)
        if tid not in topic_ids:
            topic_ids.add(tid)
            statements.append(
                f"MERGE (t:VaultTopic {{id: {_cypher_escape(tid)}}}) "
                f"SET t.label = {_cypher_escape(topic)}"
            )
        statements.append(
            f"MATCH (c:Clip {{id: {_cypher_escape(cid)}}}), "
            f"(t:VaultTopic {{id: {_cypher_escape(tid)}}}) "
            f"MERGE (c)-[:belongs_to]->(t)"
        )

        for tag in clip.get("tags", []):
            gid = _tag_id(tag)
            if gid not in tag_ids:
                tag_ids.add(gid)
                statements.append(
                    f"MERGE (g:VaultTag {{id: {_cypher_escape(gid)}}}) "
                    f"SET g.label = {_cypher_escape(tag)}"
                )
            statements.append(
                f"MATCH (c:Clip {{id: {_cypher_escape(cid)}}}), "
                f"(g:VaultTag {{id: {_cypher_escape(gid)}}}) "
                f"MERGE (c)-[:has_tag]->(g)"
            )

    if orphan_ids:
        statements.append(
            "MATCH (c:Clip) WHERE c.id IN [" + ", ".join(_cypher_escape(i) for i in orphan_ids) + "] DETACH DELETE c"
        )

    if statements:
        _run_cypher(statements)

    return {
        "dna": _dna(),
        "timestamp": _now(),
        "total_files": len(clips),
        "neo4j_clips": len(existing_ids),
        "missing_imported": len(missing),
        "orphans_pruned": len(orphan_ids),
        "prune_enabled": prune,
    }


def main():
    parser = argparse.ArgumentParser(description="剪贴板容器 Neo4j 索引自检")
    parser.add_argument("--prune", action="store_true", help="清理 Neo4j 中已不存在的 Clip 节点")
    args = parser.parse_args()

    report = reconcile(prune=args.prune)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
