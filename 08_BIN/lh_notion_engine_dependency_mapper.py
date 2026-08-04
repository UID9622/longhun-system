#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎依赖映射器 v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-DEPENDENCY-MAPPER-v1.0-BAD75C7E
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-DEPENDENCY-MAPPER-v1.0-BAD75C7E"
SCHEMA_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
REGISTRY_FILE = OUTPUT_DIR / "engine_registry.json"
DEPENDENCY_GRAPH_FILE = OUTPUT_DIR / "dependency_graph.json"
DOT_FILE = OUTPUT_DIR / "engine_dependency_graph.dot"

# 视为项目内部源码目录的前缀
INTERNAL_PREFIXES = ("engines/", "bin/", "01_技能庫/")


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "MAP": "🕸️"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _is_internal_path(path: str) -> bool:
    """判断路径是否位于项目内部源码目录"""
    path_lower = path.lower().replace("\\", "/")
    return any(path_lower.startswith(p) for p in INTERNAL_PREFIXES)


def build_name_index(engines: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """建立模块名到引擎条目的索引（去重时保留第一个）"""
    index: Dict[str, Dict[str, Any]] = {}
    for eng in engines:
        name = eng.get("name", "")
        if name and name not in index:
            index[name] = eng
    return index


def classify_imports(engines: List[Dict[str, Any]]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, List[str]]]:
    """区分每个引擎的内部依赖与外部依赖，返回 (internal_deps, external_deps, unresolved_deps)"""
    name_index = build_name_index(engines)
    internal_deps: Dict[str, List[str]] = defaultdict(list)
    external_deps: Dict[str, List[str]] = defaultdict(list)
    unresolved_deps: Dict[str, List[str]] = defaultdict(list)

    for eng in engines:
        src_name = eng.get("name", "")
        imports = eng.get("imports", [])
        for imp in imports:
            imp_lower = imp.lower()
            # 内部依赖：导入名与某个引擎的 name 匹配
            if imp_lower in name_index and imp_lower != src_name:
                internal_deps[src_name].append(imp_lower)
            else:
                # 尝试从导入名推断是否是项目内部模块（lh_ 或 CNSH_ 前缀）
                if imp_lower.startswith("lh_") or imp_lower.startswith("cnsh_") or imp_lower.startswith("CNSH_"):
                    unresolved_deps[src_name].append(imp_lower)
                else:
                    external_deps[src_name].append(imp_lower)

    return dict(internal_deps), dict(external_deps), dict(unresolved_deps)


def build_dependency_graph(engines: List[Dict[str, Any]]) -> Dict[str, Any]:
    """构建依赖图"""
    _log("开始构建依赖图...", "MAP")

    internal_deps, external_deps, unresolved_deps = classify_imports(engines)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    # 出度 / 入度统计
    out_degree: Dict[str, int] = defaultdict(int)
    in_degree: Dict[str, int] = defaultdict(int)

    for eng in engines:
        name = eng.get("name", "")
        path = eng.get("path", "")
        node = {
            "id": eng.get("id"),
            "name": name,
            "path": path,
            "category": eng.get("category"),
            "subcategory": eng.get("subcategory"),
            "type": eng.get("type"),
            "is_internal_source": _is_internal_path(path),
        }
        nodes.append(node)

        for dep in internal_deps.get(name, []):
            edges.append({
                "source": name,
                "target": dep,
                "type": "internal",
            })
            out_degree[name] += 1
            in_degree[dep] += 1

        for dep in external_deps.get(name, []):
            edges.append({
                "source": name,
                "target": dep,
                "type": "external",
            })

    # 孤立文件：无内部出边且无内部入边
    isolated: List[Dict[str, Any]] = []
    for eng in engines:
        name = eng.get("name", "")
        if out_degree.get(name, 0) == 0 and in_degree.get(name, 0) == 0:
            isolated.append({
                "id": eng.get("id"),
                "name": name,
                "path": eng.get("path"),
                "reason": "无内部依赖出边也无内部依赖入边",
            })

    # 外部依赖聚合统计
    external_counter: Dict[str, int] = defaultdict(int)
    for deps in external_deps.values():
        for dep in deps:
            external_counter[dep] += 1

    graph = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "total_engines": len(engines),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "internal_edge_count": sum(out_degree.values()),
        "isolated_count": len(isolated),
        "nodes": nodes,
        "edges": edges,
        "isolated": isolated,
        "external_dependency_top": sorted(external_counter.items(), key=lambda x: -x[1])[:30],
        "unresolved_internal": {k: v for k, v in unresolved_deps.items() if v},
    }

    _log(
        f"依赖图构建完成: {len(nodes)} 节点 · {len(edges)} 边 · {len(isolated)} 孤立文件",
        "OK",
    )
    return graph


def render_dot(graph: Dict[str, Any]) -> str:
    """渲染 Graphviz DOT 图（仅内部依赖）"""
    lines = [
        "// 🐉 龍魂 Notion 引擎依赖图",
        f"// DNA: {DNA}",
        f"// 生成时间: {graph['generated_at']}",
        "digraph LonghunEngineDependencyGraph {",
        '  rankdir="LR";',
        '  node [shape=box, fontname="Helvetica"];',
        '  edge [fontname="Helvetica", fontsize=10];',
        "",
    ]

    for node in graph["nodes"]:
        name = node["name"]
        label = f"{name}\\n({node.get('category', '')})"
        if node.get("is_internal_source"):
            lines.append(f'  "{name}" [label="{label}", style=filled, fillcolor="#E8F4FD"];')
        else:
            lines.append(f'  "{name}" [label="{label}"];')

    lines.append("")

    for edge in graph["edges"]:
        if edge["type"] == "internal":
            lines.append(f'  "{edge["source"]}" -> "{edge["target"]}";')

    lines.append("}")
    return "\n".join(lines)


def save_outputs(graph: Dict[str, Any], dot_content: str, dry_run: bool):
    """保存依赖图和 DOT 文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if dry_run:
        _log(f"[DRY-RUN] 不写入文件: {DEPENDENCY_GRAPH_FILE}", "SKIP")
        _log(f"[DRY-RUN] 不写入文件: {DOT_FILE}", "SKIP")
        return

    with open(DEPENDENCY_GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {DEPENDENCY_GRAPH_FILE}", "OK")

    with open(DOT_FILE, "w", encoding="utf-8") as f:
        f.write(dot_content)
    _log(f"已保存: {DOT_FILE}", "OK")


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎依赖映射器")
    parser.add_argument("--registry", type=Path, default=REGISTRY_FILE,
                        help="输入注册表路径 (默认: data/notion_sync/engines/engine_registry.json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅打印结果，不保存文件")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    if not args.registry.exists():
        _log(f"注册表不存在: {args.registry}", "ERROR")
        sys.exit(1)

    with open(args.registry, "r", encoding="utf-8") as f:
        registry = json.load(f)

    engines = registry.get("engines", [])
    if not engines:
        _log("注册表为空", "WARN")
        sys.exit(0)

    graph = build_dependency_graph(engines)
    dot_content = render_dot(graph)

    print("\n📊 依赖图统计:")
    print(f"  引擎总数: {graph['total_engines']}")
    print(f"  节点数: {graph['total_nodes']}")
    print(f"  边数: {graph['total_edges']}")
    print(f"  内部边数: {graph['internal_edge_count']}")
    print(f"  孤立文件数: {graph['isolated_count']}")
    print(f"\n🔝 外部依赖 Top 10:")
    for dep, cnt in graph["external_dependency_top"][:10]:
        print(f"  {dep}: {cnt}")

    if graph["isolated"]:
        print(f"\n🚧 孤立文件示例 (前 10):")
        for item in graph["isolated"][:10]:
            print(f"  - {item['name']} ({item['path']})")

    save_outputs(graph, dot_content, args.dry_run)

    if args.dry_run:
        _log("DRY-RUN 模式完成，未写入任何文件", "OK")
    else:
        _log("完成", "OK")


if __name__ == "__main__":
    main()
