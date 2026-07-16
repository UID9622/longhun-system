#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂知识图谱骨架生成器

从 notion_pages.db 提取：页面、分类、关键词、DNA 标签、页面间链接关系，
输出 JSON 图谱，供后续 Gephi / D3 / Cytoscape 可视化。

DNA: #龍芯⚡️2026-06-23-NOTION-KNOWLEDGE-GRAPH-v1.0
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone, timedelta

HOME = pathlib.Path.home()
DB_PATH = HOME / ".longhun" / "notion_pages" / "notion_pages.db"
OUT_DIR = HOME / ".longhun" / "notion_pages" / "knowledge_graph"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def build_graph(db_path: pathlib.Path) -> dict[str, Any]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    nodes: list[dict] = []
    edges: list[dict] = []
    node_ids: set[str] = set()

    def add_node(nid: str, label: str, group: str, meta: dict | None = None) -> None:
        if nid in node_ids:
            return
        node_ids.add(nid)
        nodes.append(
            {
                "id": nid,
                "label": label,
                "group": group,
                "meta": meta or {},
            }
        )

    def add_edge(source: str, target: str, relation: str, weight: float = 1.0) -> None:
        edges.append(
            {
                "source": source,
                "target": target,
                "relation": relation,
                "weight": weight,
            }
        )

    # 1. 页面节点
    rows = conn.execute(
        """
        SELECT id, title, icon, category, subcategory, notion_url,
               local_md_path, word_count, block_count, created, modified, phase, dna
        FROM pages
        WHERE status = 'done'
        """
    ).fetchall()

    page_id_set: set[str] = set()
    category_counts: defaultdict[str, int] = defaultdict(int)
    subcategory_counts: defaultdict[str, int] = defaultdict(int)

    for r in rows:
        pid = r["id"]
        page_id_set.add(pid)
        title = r["title"] or "未命名"
        category = r["category"] or "未分类"
        subcategory = r["subcategory"] or ""
        category_counts[category] += 1
        if subcategory and subcategory != category:
            subcategory_counts[subcategory] += 1

        add_node(
            f"page:{pid}",
            title,
            "page",
            {
                "page_id": pid,
                "icon": r["icon"],
                "category": category,
                "subcategory": subcategory,
                "word_count": r["word_count"],
                "block_count": r["block_count"],
                "phase": r["phase"],
                "notion_url": r["notion_url"],
                "local_md_path": r["local_md_path"],
                "created": r["created"],
                "modified": r["modified"],
                "dna": r["dna"],
            },
        )

    # 2. 分类 / 子分类节点
    for cat, count in category_counts.items():
        nid = f"cat:{cat}"
        add_node(nid, cat, "category", {"count": count})
        # 页面 -> 分类
        for r in rows:
            if (r["category"] or "未分类") == cat:
                add_edge(f"page:{r['id']}", nid, "belongs_to", 1.0)

    for sub, count in subcategory_counts.items():
        nid = f"subcat:{sub}"
        add_node(nid, sub, "subcategory", {"count": count})
        for r in rows:
            if (r["subcategory"] or "") == sub:
                add_edge(f"page:{r['id']}", nid, "belongs_to_sub", 1.0)
                # 子分类 -> 分类
                cat = r["category"] or "未分类"
                add_edge(nid, f"cat:{cat}", "sub_of", 1.0)

    # 3. 关键词节点
    kw_rows = conn.execute(
        "SELECT page_id, keyword FROM page_keywords WHERE page_id IN (SELECT id FROM pages WHERE status='done')"
    ).fetchall()
    kw_counts: defaultdict[str, int] = defaultdict(int)
    kw_links: defaultdict[str, list[str]] = defaultdict(list)
    for kr in kw_rows:
        kw = kr["keyword"]
        if not kw:
            continue
        kw_counts[kw] += 1
        kw_links[kw].append(kr["page_id"])

    for kw, count in kw_counts.items():
        if count < 2:
            continue  # 只保留共现 2 次以上的关键词，减少噪声
        nid = f"kw:{kw}"
        add_node(nid, kw, "keyword", {"count": count})
        for pid in kw_links[kw]:
            add_edge(f"page:{pid}", nid, "has_keyword", 1.0)

    # 4. DNA 标签节点
    dna_rows = conn.execute(
        "SELECT page_id, tag FROM dna_tags WHERE page_id IN (SELECT id FROM pages WHERE status='done')"
    ).fetchall()
    dna_counts: defaultdict[str, int] = defaultdict(int)
    dna_links: defaultdict[str, list[str]] = defaultdict(list)
    for dr in dna_rows:
        tag = dr["tag"]
        if not tag:
            continue
        dna_counts[tag] += 1
        dna_links[tag].append(dr["page_id"])

    for tag, count in dna_counts.items():
        nid = f"dna:{tag}"
        add_node(nid, tag, "dna_tag", {"count": count})
        for pid in dna_links[tag]:
            add_edge(f"page:{pid}", nid, "has_dna", 1.0)

    # 5. 页面间链接：从 markdown 内容中提取 Notion page_id
    notion_url_pat = re.compile(r"[0-9a-f]{32}")
    for r in rows:
        pid = r["id"]
        md_path = r["local_md_path"]
        if not md_path or not pathlib.Path(md_path).exists():
            continue
        try:
            text = pathlib.Path(md_path).read_text(encoding="utf-8")
        except Exception:
            continue
        found_ids = set(notion_url_pat.findall(text))
        for target in found_ids:
            if target != pid and target in page_id_set:
                add_edge(f"page:{pid}", f"page:{target}", "links_to", 0.8)

    conn.close()

    return {
        "meta": {
            "generated_at": now_iso(),
            "source_db": str(db_path),
            "dna": "#龍芯⚡️2026-06-23-NOTION-KNOWLEDGE-GRAPH-v1.0",
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="生成龍魂 Notion 知识图谱骨架")
    parser.add_argument("--db", type=pathlib.Path, default=DB_PATH)
    parser.add_argument("--out-dir", type=pathlib.Path, default=OUT_DIR)
    parser.add_argument("--min-kw-count", type=int, default=2)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    graph = build_graph(args.db)

    out_path = args.out_dir / "longhun_knowledge_graph.json"
    out_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    # 输出简化统计
    groups: defaultdict[str, int] = defaultdict(int)
    for n in graph["nodes"]:
        groups[n["group"]] += 1

    print(f"🕸️ 知识图谱已生成：{out_path}")
    print(f"   节点 {graph['meta']['node_count']} | 边 {graph['meta']['edge_count']}")
    print("   节点分布：")
    for g, c in sorted(groups.items()):
        print(f"     {g}: {c}")


if __name__ == "__main__":
    main()
