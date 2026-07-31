#!/usr/bin/env python3
"""龍魂神经知识矩阵 · 查询引擎 v1.0

多维度交叉查询：
  layer X ipa_node X persona X module X signal X error_memory

用法：
  python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --layer L5
  python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --ipa SIGN
  python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --persona P05
  python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --path "用户输入→输出"
  python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --matrix  # 输出全矩阵
"""
from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path
from typing import Any

MATRIX_DIR = Path(__file__).resolve().parent
MATRIX_FILE = MATRIX_DIR / "matrix_v1.0.json"


def _load() -> dict[str, Any]:
    with open(MATRIX_FILE, encoding="utf-8") as f:
        return json.load(f)  # type: ignore[no-any-return]


def query_layer(data: dict[str, Any], layer_id: str) -> None:
    """按分层查询：这个层的 IPA 节点、人格、模块、信号流向"""
    for layer in data["layers"]:
        if layer["id"].upper() == layer_id.upper():
            print(f"\n{'='*60}")
            print(f"  {layer['id']} · {layer['name']} ({layer['name_en']})")
            anchor_str = f"| 锚点数: {layer['anchor_count']}" if layer.get("anchor_count") else ""
            print(f"  可变性: {layer['mutability']} {anchor_str}")
            print(f"  {layer['description']}")
            print(f"{'='*60}")
            if layer["ipa_nodes"]:
                print(f"\n  🧭 IPA 流场节点:")
                for nid in layer["ipa_nodes"]:
                    for node in data["ipa_flow_chain"]["chain"]:
                        if node["ipa_id"] == nid:
                            print(f"     {node['order']:>4}  {node['ipa_id']}")
                            print(f"          {node['name']} · {node['persona']} · {node['type']}")
            if layer["personas"]:
                print(f"\n  👤 人格属主: {', '.join(layer['personas'])}")
            if layer.get("engines"):
                print(f"\n  ⚙️  引擎 ({len(layer['engines'])}个):")
                for e in layer["engines"]:
                    print(f"     - {e}")
            if layer.get("integrations"):
                print(f"\n  🔗 外部集成 ({len(layer['integrations'])}个):")
                for i in layer["integrations"]:
                    print(f"     - {i}")
            if layer["key_files"]:
                print(f"\n  📁 关键文件 ({len(layer['key_files'])}个):")
                for f in layer["key_files"]:
                    print(f"     - {f}")
            print(f"\n  ⬆ 上游: {layer['signal_up'] or '无(顶层)'}")
            print(f"  ⬇ 下游: {layer['signal_down'] or '无(底层)'}")
            return
    print(f"未找到层: {layer_id}")


def query_ipa(data: dict[str, Any], keyword: str) -> None:
    """按 IPA 节点查询"""
    kw = keyword.upper()
    for node in data["ipa_flow_chain"]["chain"]:
        if kw in node["ipa_id"].upper() or kw in node["name"].upper():
            layer_info = next((l for l in data["layers"] if l["id"] == node["layer"]), None)
            print(f"\n{'='*60}")
            print(f"  {node['order']:>4}  {node['ipa_id']}")
            print(f"  名称: {node['name']} | 类型: {node['type']}")
            print(f"  人格: {node['persona']} | 所在层: L{node['layer']}")
            if layer_info:
                print(f"  层级: {layer_info['name']} ({layer_info['name_en']})")
            print(f"  {node['desc']}")
            print(f"{'='*60}")
            return
    print(f"未找到 IPA 节点: {keyword}")


def query_persona(data: dict[str, Any], persona_id: str) -> None:
    """按人格查询（支持简写 P05 或全名 P05_上帝之眼）"""
    pid = persona_id.upper().replace(" ", "_")
    registry = data["persona_registry"]
    # 精确匹配
    if pid in registry:
        key = pid
    else:
        # 前缀匹配（P05 匹配 P05_上帝之眼）
        matches = [k for k in registry if k.startswith(pid)]
        if len(matches) == 1:
            key = matches[0]
        elif len(matches) > 1:
            print(f"多个人格匹配 '{persona_id}': {matches}")
            return
        else:
            print(f"未找到人格: {persona_id}")
            return
    p = registry[key]
    print(f"\n{'='*60}")
    print(f"  {key} · {p['role']}")
    print(f"{'='*60}")
    if p["ipa_nodes"]:
        print(f"\n  🧭 负责的 IPA 节点:")
        for nid in p["ipa_nodes"]:
            for node in data["ipa_flow_chain"]["chain"]:
                if nid in node["ipa_id"]:
                    print(f"     {node['order']:>4}  {node['name']} ({node['type']})")
    if p["layer_owner"]:
        print(f"\n  📊 所属层级: {', '.join(p['layer_owner'])}")
    return


def query_path(data: dict[str, Any], keyword: str) -> None:
    """按信号路径查询"""
    kw = keyword.lower()
    for path_info in data["signal_heatmap"]["paths"]:
        if kw in path_info["desc"].lower() or kw in path_info["path"].lower():
            print(f"\n{'='*60}")
            print(f"  信号路径 · 热度: {path_info['heat']} · {path_info['hops']}跳")
            print(f"  {path_info['desc']}")
            print(f"{'='*60}")
            nodes = path_info["path"].split("→")
            for i, n in enumerate(nodes):
                marker = "🚪" if i == 0 else ("🏁" if i == len(nodes) - 1 else "  ")
                print(f"  {marker} [{i}] {n.strip()}")
            return
    print(f"未找到信号路径: {keyword}")


def query_full_matrix(data: dict[str, Any]) -> None:
    """输出全矩阵概览"""
    print(f"\n{'='*70}")
    print(f"  龍魂神经知识矩阵 · 全貌")
    print(f"  v{data['meta']['version']} · {data['meta']['dna']}")
    print(f"  {data['meta']['total_layers']}层 × {data['meta']['total_ipa_nodes']}IPA × {data['meta']['total_personas']}人格 × {data['meta']['total_modules']}模块")
    print(f"{'='*70}")

    # 层→IPA→人格 映射表
    print(f"\n  {'层':<6} {'层级名称':<12} {'IPA节点':<35} {'人格':<16} {'信号流'}")
    print(f"  {'-'*6} {'-'*12} {'-'*35} {'-'*16} {'-'*20}")
    for layer in data["layers"]:
        ipa_str = ", ".join(layer["ipa_nodes"][:2]) if layer["ipa_nodes"] else "—"
        if len(layer["ipa_nodes"]) > 2:
            ipa_str += f" (+{len(layer['ipa_nodes'])-2})"
        persona_str = ", ".join(layer["personas"][:2])
        if len(layer["personas"]) > 2:
            persona_str += f" (+{len(layer['personas'])-2})"
        up = "←" + ",".join(layer["signal_up"]) if layer["signal_up"] else "—"
        down = "→" + ",".join(layer["signal_down"]) if layer["signal_down"] else "—"
        signal = f"{up} {down}"[:35]
        print(f"  L{layer['id']:<5} {layer['name']:<12} {ipa_str:<35} {persona_str:<16} {signal}")

    # IPA 流场链
    print(f"\n  {'─'*70}")
    print(f"  IPA 流场标准链 (信号必经之路):")
    print(f"  {'─'*70}")
    chain_parts = []
    for node in data["ipa_flow_chain"]["chain"]:
        chain_parts.append(f"{node['name']}[{node['persona']}]")
    print(f"  入口 → {' → '.join(chain_parts)} → 归档")

    # 跨层桥接
    print(f"\n  {'─'*70}")
    print(f"  跨层桥接 ({len(data['cross_layer_bridges'])}条):")
    print(f"  {'─'*70}")
    for bridge in data["cross_layer_bridges"]:
        print(f"  L{bridge['from_layer']} → L{bridge['to_layer']} : {bridge['mechanism']}")

    # 现有矩阵文档
    print(f"\n  {'─'*70}")
    print(f"  已有矩阵文档 (本矩阵整合这些):")
    print(f"  {'─'*70}")
    for name, doc in data["existing_matrix_docs"].items():
        print(f"  📄 {name}: {doc['path']} → {doc['scope']}  [{doc['limitation']}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂神经知识矩阵 · 查询引擎")
    parser.add_argument("--layer", "-l", help="按层查询 (L0-L9)")
    parser.add_argument("--ipa", "-i", help="按IPA节点查询")
    parser.add_argument("--persona", "-p", help="按人格查询 (P00-P77)")
    parser.add_argument("--path", help="按信号路径查询")
    parser.add_argument("--matrix", "-m", action="store_true", help="输出全矩阵概览")
    parser.add_argument("--json-out", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    data = _load()

    queries = 0
    if args.layer:
        query_layer(data, args.layer)
        queries += 1
    if args.ipa:
        query_ipa(data, args.ipa)
        queries += 1
    if args.persona:
        query_persona(data, args.persona)
        queries += 1
    if args.path:
        query_path(data, args.path)
        queries += 1
    if args.matrix or queries == 0:
        query_full_matrix(data)


if __name__ == "__main__":
    main()
