#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🕸️ 龍魂·剪贴板容器 → 知识图谱导入器 v1.0
============================================
DNA: #龍芯⚡️丙午·丙申·庚申·子时·䷃蒙-VAULT-TO-KG-V1.0-P1

把 06_CONTAINERS/clipboard-vault/ 里的 markdown 剪贴项，
增量导入本地 Neo4j 知识图谱，形成可查询的 Clip/VaultTopic/VaultTag 子图。

用法:
  python3 08_BIN/lh_vault_to_kg.py --dry-run    # 预览要导入的内容
  python3 08_BIN/lh_vault_to_kg.py              # 真正导入 Neo4j
  python3 08_BIN/lh_vault_to_kg.py --clear      # 清空已有 Vault 子图后重导
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

import yaml
from ganzhi_dna_engine import DNA生成

CST = timezone(timedelta(hours=8))
VAULT_ROOT = PROJECT_ROOT / "06_CONTAINERS" / "clipboard-vault"
INBOX_DIR = VAULT_ROOT / "inbox"

NEO4J_URL = os.environ.get("NEO4J_HTTP_URL", "http://localhost:7474/db/neo4j/tx/commit")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASSWORD", "longhun123")


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _dna() -> str:
    return DNA生成(模块="VAULT-TO-KG", 动作="IMPORT", 版本="V1.0", 级别="P1")


def _parse_frontmatter(text: str) -> Optional[Dict[str, Any]]:
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    raw = m.group(1)
    try:
        return yaml.safe_load(raw) or {}
    except Exception:
        try:
            return json.loads(raw) or {}
        except Exception:
            return None


def _cypher_escape(value: Any) -> str:
    """把字符串转义为 Cypher 字符串字面量。"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    # 双引号转义，换行转义
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
    return f'"{s}"'


def _run_cypher(statements: List[str]) -> Dict[str, Any]:
    """批量执行 Cypher 语句。"""
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


def _clip_id(content_hash: str) -> str:
    return f"CLIP:{content_hash[:16]}"


def _topic_id(topic: str) -> str:
    return f"VAULT-TOPIC:{hashlib.md5(topic.encode()).hexdigest()[:8]}"


def _tag_id(tag: str) -> str:
    return f"VAULT-TAG:{hashlib.md5(tag.encode()).hexdigest()[:8]}"


def load_clips() -> List[Dict[str, Any]]:
    """加载 vault 中所有剪贴项。"""
    clips: List[Dict[str, Any]] = []
    for md_file in sorted(INBOX_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        if meta is None:
            continue
        content_hash = meta.get("content_hash", "")
        if not content_hash:
            content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        clips.append({
            "id": _clip_id(content_hash),
            "path": str(md_file.relative_to(PROJECT_ROOT)),
            "dna": meta.get("dna", ""),
            "source": meta.get("source", "clipboard"),
            "topic": meta.get("topic", "未分类"),
            "tags": meta.get("tags", []),
            "timestamp": meta.get("timestamp", ""),
            "content_hash": content_hash,
            "parent_dna": meta.get("parent_dna", []),
        })
    return clips


def build_cypher(clips: List[Dict[str, Any]]) -> List[str]:
    """为所有 Clip 生成 MERGE/CREATE Cypher。"""
    statements: List[str] = []
    topic_ids: set = set()
    tag_ids: set = set()

    for clip in clips:
        cid = clip["id"]
        label = Path(clip["path"]).stem
        updated_at = clip.get("updated_at", clip["timestamp"])
        copy_count = clip.get("copy_count", 1)
        statements.append(
            f"MERGE (c:Clip {{id: {_cypher_escape(cid)}}}) "
            f"SET c.label = {_cypher_escape(label)}, "
            f"    c.dna = {_cypher_escape(clip['dna'])}, "
            f"    c.source = {_cypher_escape(clip['source'])}, "
            f"    c.timestamp = {_cypher_escape(clip['timestamp'])}, "
            f"    c.updated_at = {_cypher_escape(updated_at)}, "
            f"    c.copy_count = {copy_count}, "
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
            tag_id = _tag_id(tag)
            if tag_id not in tag_ids:
                tag_ids.add(tag_id)
                statements.append(
                    f"MERGE (g:VaultTag {{id: {_cypher_escape(tag_id)}}}) "
                    f"SET g.label = {_cypher_escape(tag)}"
                )
            statements.append(
                f"MATCH (c:Clip {{id: {_cypher_escape(cid)}}}), "
                f"(g:VaultTag {{id: {_cypher_escape(tag_id)}}}) "
                f"MERGE (c)-[:has_tag]->(g)"
            )

    return statements


def stats() -> Dict[str, int]:
    try:
        result = _run_cypher([
            "MATCH (c:Clip) RETURN count(c) AS cnt",
            "MATCH (t:VaultTopic) RETURN count(t) AS cnt",
            "MATCH (g:VaultTag) RETURN count(g) AS cnt",
            "MATCH ()-[r:VAULT_DERIVED]->() RETURN count(r) AS cnt",
        ])
        counts = []
        for res in result.get("results", []):
            rows = res.get("data", [])
            counts.append(rows[0]["row"][0] if rows else 0)
        return {
            "clips": counts[0] if len(counts) > 0 else 0,
            "topics": counts[1] if len(counts) > 1 else 0,
            "tags": counts[2] if len(counts) > 2 else 0,
            "derived": counts[3] if len(counts) > 3 else 0,
        }
    except Exception:
        return {"clips": 0, "topics": 0, "tags": 0, "derived": 0}


def main():
    parser = argparse.ArgumentParser(description="剪贴板容器 → 知识图谱导入器")
    parser.add_argument("--dry-run", action="store_true", help="只生成 Cypher，不执行")
    parser.add_argument("--clear", action="store_true", help="先清空 Vault 子图再导入")
    parser.add_argument("--output", type=str, help="导出 Cypher 到文件")
    args = parser.parse_args()

    clips = load_clips()
    if not clips:
        print("🟡 容器中没有剪贴项，无需导入")
        return

    print(f"📦 加载到 {len(clips)} 条剪贴项")

    statements = build_cypher(clips)
    print(f"🧬 生成 {len(statements)} 条 Cypher 语句")

    if args.output:
        Path(args.output).write_text("\n;\n".join(statements) + ";\n", encoding="utf-8")
        print(f"💾 Cypher 已导出到 {args.output}")

    if args.dry_run:
        print("\n--- 前 5 条 Cypher 预览 ---")
        for s in statements[:5]:
            print(s)
        print("...")
        print("\n🟡 dry-run 模式，未写入 Neo4j")
        return

    if args.clear:
        print("🧹 清空已有 Vault 子图...")
        _run_cypher(["MATCH (c:Clip) DETACH DELETE c", "MATCH (t:VaultTopic) DETACH DELETE t", "MATCH (g:VaultTag) DETACH DELETE g"])

    print("🚀 导入 Neo4j...")
    _run_cypher(statements)

    after = stats()
    report = {
        "dna": _dna(),
        "timestamp": _now(),
        "imported_clips": len(clips),
        "cypher_statements": len(statements),
        "neo4j_stats": after,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
