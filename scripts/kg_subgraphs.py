#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知识图谱 · 自适应子图拆分
按页面 category 把大图拆成子图，便于独立查询、按需加载、协同调用。

DNA: #龍芯⚡️2026-06-23-LONGHUN-KG-SUBGRAPHS-v1.0
"""

import json
import os
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any

DB_PATH = Path.home() / ".longhun" / "notion_pages" / "notion_pages.db"
OUT_DIR = Path.home() / ".longhun" / "notion_pages" / "kg_subgraphs"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def build_subgraphs() -> Dict[str, Dict[str, Any]]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # 取所有页面 category
    page_cats = {
        row["id"]: row["category"]
        for row in conn.execute("SELECT id, category FROM pages WHERE status='done'")
    }

    # 统计每个 category 下的 page_id
    cat_pages = defaultdict(set)
    for pid, cat in page_cats.items():
        cat_pages[cat or "未分类"].add(pid)

    # 关系带上 category
    rel_rows = conn.execute("""
        SELECT r.*, p.category
        FROM relations r
        JOIN pages p ON r.page_id = p.id
        WHERE p.status='done'
    """).fetchall()

    cat_relations = defaultdict(list)
    for row in rel_rows:
        cat_relations[row["category"] or "未分类"].append(dict(row))

    # 实体参与哪些 category
    entity_cats = defaultdict(set)
    entity_names = {}
    for row in conn.execute("""
        SELECT e.id, e.name, e.type, p.category
        FROM entity_occurrences eo
        JOIN entities e ON eo.entity_id = e.id
        JOIN pages p ON eo.page_id = p.id
        WHERE p.status='done'
    """):
        eid, name, etype, cat = row
        entity_names[eid] = (name, etype)
        entity_cats[eid].add(cat or "未分类")

    subgraphs = {}
    for cat in sorted(cat_pages.keys()):
        rels = cat_relations.get(cat, [])
        entity_ids = set()
        for r in rels:
            entity_ids.add(r["source_id"])
            entity_ids.add(r["target_id"])

        # 只保留“主要”属于该 category 的实体（即该 category 是其最多出现 category 之一）
        # 简化：实体只要出现在该 cat 的页面里，就纳入子图
        entities = []
        for eid in entity_ids:
            if eid in entity_names:
                entities.append({
                    "id": eid,
                    "name": entity_names[eid][0],
                    "type": entity_names[eid][1],
                    "cross_categories": sorted(entity_cats.get(eid, set())),
                })

        subgraphs[cat] = {
            "category": cat,
            "page_count": len(cat_pages[cat]),
            "entity_count": len(entities),
            "relation_count": len(rels),
            "entities": entities,
            "relations": rels,
        }

    conn.close()
    return subgraphs


def export_subgraphs(subgraphs: Dict[str, Dict[str, Any]]):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = []
    for cat, data in subgraphs.items():
        safe_cat = cat.replace("/", "_").replace(" ", "_")
        file_path = OUT_DIR / f"{safe_cat}.json"
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        summary.append({
            "category": cat,
            "pages": data["page_count"],
            "entities": data["entity_count"],
            "relations": data["relation_count"],
            "file": str(file_path),
        })

    # 生成总览
    overview = {
        "total_categories": len(summary),
        "subgraphs": summary,
        "dna": "#龍芯⚡️2026-06-23-LONGHUN-KG-SUBGRAPHS-v1.0",
    }
    overview_path = OUT_DIR / "overview.json"
    overview_path.write_text(json.dumps(overview, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成 HTML 总览
    html_path = OUT_DIR / "index.html"
    rows = "\n".join(
        f"<tr><td>{s['category']}</td><td>{s['pages']}</td><td>{s['entities']}</td><td>{s['relations']}</td></tr>"
        for s in summary
    )
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>龍魂知识图谱 · 子图总览</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem; background:#0f0f0f; color:#eee; }}
table {{ border-collapse: collapse; width: 100%; margin-top:1rem; }}
th, td {{ border: 1px solid #444; padding: 0.6rem; text-align: left; }}
th {{ background: #222; }}
tr:nth-child(even) {{ background: #1a1a1a; }}
h1 {{ color: #f0c040; }}
</style>
</head>
<body>
<h1>🐉 龍魂知识图谱 · 自适应子图总览</h1>
<p>共拆分 <strong>{len(summary)}</strong> 个子图，每个子图按页面 category 独立组织。</p>
<table>
<tr><th>类别</th><th>页面数</th><th>实体数</th><th>关系数</th></tr>
{rows}
</table>
<p style="margin-top:2rem;color:#888;font-size:0.9rem;">DNA: #龍芯⚡️2026-06-23-LONGHUN-KG-SUBGRAPHS-v1.0</p>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")

    print(f"[KG子图] 已生成 {len(summary)} 个子图")
    print(f"[KG子图] 总览: {overview_path}")
    print(f"[KG子图] HTML: {html_path}")
    for s in summary[:10]:
        print(f"  - {s['category']}: {s['pages']} 页 / {s['entities']} 实体 / {s['relations']} 关系")


if __name__ == "__main__":
    subgraphs = build_subgraphs()
    export_subgraphs(subgraphs)
