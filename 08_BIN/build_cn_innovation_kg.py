#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
中国科技自主创新专栏 · 知识图谱生成器
源: ~/.kimi-code/skills/longhun-cn-innovation-kb/scripts/cn_innovation_kb.json
产: longhun-system/03_KNOWLEDGE_GRAPH/cn_innovation_kg.{json,md,cypher}
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from ganzhi_dna_engine import DNA生成

SRC = Path.home() / ".kimi-code/skills/longhun-cn-innovation-kb/scripts/cn_innovation_kb.json"
OUT_DIR = Path("/Users/zuimeidedeyihan/longhun-system/03_KNOWLEDGE_GRAPH")


def safe_id(text: str) -> str:
    """生成 Mermaid/Cypher 安全 ID"""
    s = re.sub(r"[^\w\u4e00-\u9fff_-]", "_", text)
    s = re.sub(r"_+", "_", s).strip("_")
    if s and s[0].isdigit():
        s = "_" + s
    return s or "_"


def parse_wuxing(dr_field: str) -> str:
    parts = [p.strip() for p in dr_field.split("·")]
    if len(parts) >= 2 and parts[1] in ("金", "木", "水", "火", "土"):
        return parts[1]
    return ""


def parse_venues(record: dict) -> list[str]:
    title = record.get("专栏标题", "")
    summary = record.get("一句话摘要", "")
    text = title + " " + summary
    venues: list[str] = []
    m = re.search(r"投稿\s+(.+?)(?:\s*·\s*英文版规划|\s*\)|$)", text)
    if m:
        raw = m.group(1).strip()
        # split on / or / with spaces, or Chinese slash
        for v in re.split(r"\s*/\s*", raw):
            v = v.strip(" ,;()")
            if v:
                venues.append(v)
    return venues


def build_graph(records: list[dict]) -> dict[str, Any]:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(nid: str, label: str, ntype: str, **props):
        if nid not in nodes:
            nodes[nid] = {"id": nid, "label": label, "type": ntype, "properties": props}

    for rec in records:
        seq = str(rec.get("文章序号", "")).strip()
        if not seq.isdigit():
            seq = str(len(nodes) + 1)
        aid = f"A{seq}"
        title = rec.get("专栏标题", "").strip() or f"未命名_{aid}"
        add_node(
            aid,
            title,
            "Article",
            状态=rec.get("状态", ""),
            重要程度=rec.get("重要程度", ""),
            DNA追溯码=rec.get("DNA追溯码", ""),
            短DNA身份码=rec.get("短DNA·身份码", ""),
            IPA=rec.get("IPA·缩写", ""),
            一句话摘要=rec.get("一句话摘要", ""),
            易经锚点=rec.get("易经锚点", ""),
            dr五行宫位=rec.get("dr·五行·宫位", ""),
            α三义=rec.get("α三义", ""),
            来源=rec.get("来源", ""),
        )

        field = rec.get("领域分类", "").strip()
        if field:
            fid = f"FIELD:{field}"
            add_node(fid, field, "Field")
            edges.append({"source": aid, "target": fid, "type": "belongs_to", "label": "属于领域"})

        status = rec.get("状态", "").strip()
        if status:
            sid = f"STATUS:{status}"
            add_node(sid, status, "Status")
            edges.append({"source": aid, "target": sid, "type": "has_status", "label": "状态"})

        importance = rec.get("重要程度", "").strip()
        if importance:
            iid = f"IMPORTANCE:{importance}"
            add_node(iid, importance, "Importance")
            edges.append({"source": aid, "target": iid, "type": "has_importance", "label": "重要程度"})

        wuxing = parse_wuxing(rec.get("dr·五行·宫位", ""))
        if wuxing:
            wid = f"WUXING:{wuxing}"
            add_node(wid, wuxing, "Wuxing")
            edges.append({"source": aid, "target": wid, "type": "has_wuxing", "label": "五行"})

        layer = rec.get("架构层级", "").strip()
        if layer:
            lid = f"LAYER:{layer}"
            add_node(lid, layer, "Layer")
            edges.append({"source": aid, "target": lid, "type": "in_layer", "label": "架构层级"})

        for persona in rec.get("人格路由", []):
            persona = persona.strip()
            if not persona:
                continue
            pid = f"PERSONA:{persona}"
            add_node(pid, persona, "Persona")
            edges.append({"source": aid, "target": pid, "type": "routed_to", "label": "人格路由"})

        for tag in rec.get("内容标签", []):
            tag = tag.strip()
            if not tag:
                continue
            tid = f"TAG:{tag}"
            add_node(tid, tag, "Tag")
            edges.append({"source": aid, "target": tid, "type": "has_tag", "label": "标签"})

        for venue in parse_venues(rec):
            vid = f"VENUE:{venue}"
            add_node(vid, venue, "Venue")
            edges.append({"source": aid, "target": vid, "type": "targets_venue", "label": "目标顶刊"})

    return {"nodes": list(nodes.values()), "edges": edges}


def mermaid_escape(text: str) -> str:
    text = text.replace('"', "'")
    text = text.replace("\n", " ")
    return text.strip()


def build_markdown(graph: dict[str, Any], dna: str) -> str:
    nodes = {n["id"]: n for n in graph["nodes"]}
    stats = Counter(n["type"] for n in graph["nodes"])
    edge_stats = Counter(e["type"] for e in graph["edges"])

    # Top fields/personas/tags
    top_fields = Counter(
        nodes[e["target"]]["label"] for e in graph["edges"] if e["type"] == "belongs_to"
    ).most_common(10)
    top_personas = Counter(
        nodes[e["target"]]["label"] for e in graph["edges"] if e["type"] == "routed_to"
    ).most_common(10)
    top_tags = Counter(
        nodes[e["target"]]["label"] for e in graph["edges"] if e["type"] == "has_tag"
    ).most_common(10)
    top_venues = Counter(
        nodes[e["target"]]["label"] for e in graph["edges"] if e["type"] == "targets_venue"
    ).most_common(10)

    lines: list[str] = []
    lines.append("# 🇨🇳 中国科技自主创新专栏 · 知识图谱")
    lines.append("")
    lines.append(f"**DNA**: `{dna}`")
    lines.append(f"**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`")
    lines.append("")
    lines.append("## 图谱统计")
    lines.append("")
    lines.append("| 指标 | 数量 |")
    lines.append("|:---:|---:|")
    lines.append(f"| 节点总数 | {len(graph['nodes'])} |")
    lines.append(f"| 边总数 | {len(graph['edges'])} |")
    for t, c in sorted(stats.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} 节点 | {c} |")
    lines.append("")
    lines.append("### 边类型分布")
    lines.append("")
    lines.append("| 边类型 | 数量 |")
    lines.append("|:---:|---:|")
    for t, c in sorted(edge_stats.items(), key=lambda x: -x[1]):
        lines.append(f"| `{t}` | {c} |")
    lines.append("")

    def stat_block(title: str, items: list[tuple[str, int]]):
        lines.append(f"### {title}")
        lines.append("")
        if not items:
            lines.append("*暂无数据*")
        else:
            for name, c in items:
                lines.append(f"- **{name}** · {c} 篇")
        lines.append("")

    stat_block("领域分布 TOP10", top_fields)
    stat_block("人格路由 TOP10", top_personas)
    stat_block("高频标签 TOP10", top_tags)
    stat_block("顶刊目标 TOP10", top_venues)

    # Mermaid: Field -> Article overview
    lines.append("## 领域-论文关系图")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    field_edges = [e for e in graph["edges"] if e["type"] == "belongs_to"]
    field_ids = sorted({e["target"] for e in field_edges})
    article_ids = sorted({e["source"] for e in field_edges})
    for fid in field_ids:
        label = mermaid_escape(nodes[fid]["label"])
        lines.append(f'  {safe_id(fid)}["{label}"]')
    for aid in article_ids:
        label = mermaid_escape(f"{aid}: {nodes[aid]['label'][:26]}")
        lines.append(f'  {aid}["{label}"]')
    for e in field_edges:
        lines.append(f"  {safe_id(e['target'])} --> {e['source']}")
    lines.append("```")
    lines.append("")

    # Mermaid: Persona routing overview
    lines.append("## 人格路由图")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    p_edges = [e for e in graph["edges"] if e["type"] == "routed_to"]
    p_ids = sorted({e["target"] for e in p_edges})
    a_ids = sorted({e["source"] for e in p_edges})
    for pid in p_ids:
        label = mermaid_escape(nodes[pid]["label"])
        lines.append(f'  {safe_id(pid)}["{label}"]')
    for aid in a_ids:
        label = mermaid_escape(f"{aid}: {nodes[aid]['label'][:22]}")
        lines.append(f'  {aid}["{label}"]')
    for e in p_edges:
        lines.append(f"  {e['source']} --> {safe_id(e['target'])}")
    lines.append("```")
    lines.append("")

    # Article list
    lines.append("## 论文节点清单")
    lines.append("")
    lines.append("| 节点ID | 专栏标题 | 领域 | 状态 | 重要程度 |")
    lines.append("|:---|:---|:---|:---|:---|")
    articles = [n for n in graph["nodes"] if n["type"] == "Article"]
    articles.sort(key=lambda x: x["id"])
    for a in articles:
        # find field/status/importance from edges
        field = ""
        status = ""
        importance = ""
        for e in graph["edges"]:
            if e["source"] != a["id"]:
                continue
            if e["type"] == "belongs_to":
                field = nodes[e["target"]]["label"]
            elif e["type"] == "has_status":
                status = nodes[e["target"]]["label"]
            elif e["type"] == "has_importance":
                importance = nodes[e["target"]]["label"]
        title = a["label"].replace("|", "｜")
        lines.append(f"| {a['id']} | {title} | {field} | {status} | {importance} |")
    lines.append("")

    lines.append("---")
    lines.append("> 来源: `.kimi-code/skills/longhun-cn-innovation-kb/scripts/cn_innovation_kb.json`")
    lines.append("> 协议: CC BY-NC-SA 4.0（思想层） / MulanPSL v2（工程层）")
    lines.append("")
    return "\n".join(lines)


def build_cypher(graph: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("// 中国科技自主创新专栏 · Neo4j 导入脚本")
    lines.append("// 自动generated，勿手写")
    lines.append("")
    # Create articles first
    for n in graph["nodes"]:
        if n["type"] != "Article":
            continue
        props = {k: v for k, v in n["properties"].items() if v}
        prop_str = ", ".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in props.items())
        lines.append(f"CREATE (:{n['type']} {{id: {json.dumps(n['id'])}, label: {json.dumps(n['label'], ensure_ascii=False)}{', ' + prop_str if prop_str else ''}}}); ")
    # Merge other nodes
    for n in graph["nodes"]:
        if n["type"] == "Article":
            continue
        lines.append(
            f"MERGE (:{n['type']} {{id: {json.dumps(n['id'])}, label: {json.dumps(n['label'], ensure_ascii=False)}}});"
        )
    # Edges
    for e in graph["edges"]:
        lines.append(
            f"MATCH (a {{id: {json.dumps(e['source'])}}}), (b {{id: {json.dumps(e['target'])}}}) "
            f"CREATE (a)-[:{e['type']} {{label: {json.dumps(e['label'], ensure_ascii=False)}}}]->(b);"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(SRC, "r", encoding="utf-8") as f:
        records = json.load(f)

    graph = build_graph(records)

    dna = DNA生成(
        模块="KNOWLEDGE-GRAPH-CN-INNOVATION",
        动作="BUILD",
        版本="V1.0",
        级别="P1",
        内容锚点="中国科技自主创新专栏知识图谱",
    )

    kg = {
        "meta": {
            "title": "🇨🇳 中国科技自主创新专栏 · 知识图谱",
            "source": str(SRC),
            "dna": dna,
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "node_count": len(graph["nodes"]),
            "edge_count": len(graph["edges"]),
        },
        "schema": {
            "node_types": ["Article", "Field", "Tag", "Status", "Importance", "Wuxing", "Persona", "Layer", "Venue"],
            "edge_types": [
                "belongs_to",
                "has_tag",
                "has_status",
                "has_importance",
                "has_wuxing",
                "routed_to",
                "in_layer",
                "targets_venue",
            ],
        },
        **graph,
    }

    json_path = OUT_DIR / "cn_innovation_kg.json"
    md_path = OUT_DIR / "cn_innovation_kg.md"
    cypher_path = OUT_DIR / "cn_innovation_kg.cypher"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(kg, f, ensure_ascii=False, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(build_markdown(graph, dna))

    with open(cypher_path, "w", encoding="utf-8") as f:
        f.write(build_cypher(graph))

    print(f"🟢 知识图谱已生成")
    print(f"   JSON   : {json_path}")
    print(f"   Markdown: {md_path}")
    print(f"   Cypher : {cypher_path}")
    print(f"   DNA    : {dna}")
    print(f"   节点   : {len(graph['nodes'])}  边 : {len(graph['edges'])}")


if __name__ == "__main__":
    main()
