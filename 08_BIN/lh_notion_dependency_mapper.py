#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 依赖关系映射器 v1.0
DNA: #龍芯⚡️丙午·乙未·乙未·申时·䷀乾-NOTION-DEPENDENCY-MAPPER-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

解析引擎间的 Python import 关系，构建依赖图。输出可用于 Notion Relation 字段。

用法:
  python3 bin/lh_notion_dependency_mapper.py              # 构建完整依赖图
  python3 bin/lh_notion_dependency_mapper.py --engine xxx # 查单个引擎依赖
  python3 bin/lh_notion_dependency_mapper.py --graph       # 输出 Graphviz DOT
  python3 bin/lh_notion_dependency_mapper.py --circular    # 检测循环依赖
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·乙未·申时·䷀乾-NOTION-DEPENDENCY-MAPPER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry_tagged.json"
# 回退到未打标版本
FALLBACK_FILE = ROOT / "data" / "notion_sync" / "engines" / "engine_registry.json"
OUTPUT_FILE = ROOT / "data" / "notion_sync" / "engines" / "dependency_graph.json"

# ── 内部模块名→路径映射 ──────────────────────────────

def _build_module_map(engine_paths: List[str]) -> Dict[str, str]:
    """构建模块名→文件路径映射"""
    module_map: Dict[str, str] = {}
    for ep in engine_paths:
        # engines/core/xxx.py → core.xxx
        # bin/xxx.py → xxx
        # 02_SKILLS/xxx/yyy.py → xxx.yyy
        p = Path(ep)
        parts = list(p.parts)
        # 去掉 .py
        stem = p.stem

        # 引擎目录下的模块
        if "engines" in parts:
            idx = parts.index("engines")
            sub = parts[idx+1:]
            if sub[-1].endswith(".py"):
                sub[-1] = stem
            mod_name = ".".join([p for p in sub if p != "__init__"])
            if mod_name:
                module_map[mod_name] = ep

        # bin 下的脚本
        if "bin" in parts:
            module_map[stem] = ep

        # 技能库
        if "01_技能庫" in parts:
            module_map[f"skills.{stem}"] = ep

    return module_map


def _extract_local_imports(content: str, module_map: Dict[str, str]) -> Set[str]:
    """提取对项目内部模块的 import"""
    local_imports: Set[str] = set()

    # from xxx import yyy
    for m in re.finditer(r'from\s+([\w.]+)\s+import', content):
        mod = m.group(1)
        if mod in module_map:
            local_imports.add(module_map[mod])
        else:
            # 尝试部分匹配
            for known_mod in module_map:
                if known_mod == mod or known_mod.startswith(mod + ".") or mod.startswith(known_mod + "."):
                    local_imports.add(module_map[known_mod])

    # import xxx (以及 import xxx as y)
    for m in re.finditer(r'^\s*import\s+([\w.]+)', content, re.MULTILINE):
        mod = m.group(1)
        if mod in module_map:
            local_imports.add(module_map[mod])

    return local_imports


def _extract_external_imports(content: str) -> List[str]:
    """提取外部依赖（第三方库）"""
    stdlib = {
        "os", "sys", "re", "json", "time", "datetime", "math", "random",
        "hashlib", "pathlib", "argparse", "typing", "collections", "itertools",
        "functools", "io", "shutil", "subprocess", "logging", "unittest",
        "ast", "csv", "enum", "glob", "threading", "multiprocessing",
        "asyncio", "socket", "http", "urllib", "xml", "html", "email",
        "sqlite3", "tempfile", "textwrap", "traceback", "warnings",
        "zipfile", "gzip", "tarfile", "base64", "struct", "copy",
        "abc", "dataclasses", "contextlib", "inspect", "types",
        "__future__", "builtins", "gc", "atexit", "signal", "pdb",
    }

    externals: Set[str] = set()
    for m in re.finditer(r'^\s*(?:from|import)\s+(\w+)', content, re.MULTILINE):
        mod = m.group(1)
        if mod not in stdlib:
            externals.add(mod)
    return sorted(externals)


def build_dependency_graph(registry_file: Optional[Path] = None) -> Dict[str, Any]:
    """构建完整依赖图"""
    # 选择注册表
    rf = registry_file or REGISTRY_FILE
    if not rf.exists():
        rf = FALLBACK_FILE
    if not rf.exists():
        _log("注册表不存在，请先运行 lh_notion_engine_discovery.py", "ERROR")
        sys.exit(1)

    with open(rf) as f:
        registry = json.load(f)

    engines = registry.get("engines", [])
    _log(f"加载 {len(engines)} 个引擎...")

    # 构建模块名→路径映射
    engine_paths = [e["path"] for e in engines]
    module_map = _build_module_map(engine_paths)
    _log(f"模块映射: {len(module_map)} 个可解析模块")

    # 分析每个引擎的依赖
    deps: List[Dict] = []
    adj: Dict[str, Set[str]] = defaultdict(set)  # 邻接表 (出边)
    in_degree: Dict[str, int] = defaultdict(int)   # 入度
    external_deps: Dict[str, List[str]] = {}

    for eng in engines:
        filepath = ROOT / eng["path"]
        if not filepath.exists():
            continue

        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            continue

        local = _extract_local_imports(content, module_map)
        external = _extract_external_imports(content)

        # 过滤自身
        local.discard(eng["path"])

        for dep_path in local:
            adj[eng["path"]].add(dep_path)
            in_degree[dep_path] += 1

        if external:
            external_deps[eng["path"]] = external

        deps.append({
            "engine": eng["name"],
            "path": eng["path"],
            "depends_on": sorted(local),
            "depends_on_count": len(local),
            "depended_by": [],  # 稍后填充
            "depended_by_count": 0,
            "external_deps": external,
            "external_count": len(external),
        })

    # 填充 depended_by（反向依赖）
    dep_by_path: Dict[str, Dict[str, Any]] = {d["path"]: d for d in deps}
    for d in deps:
        for dep_path in d["depends_on"]:
            if dep_path in dep_by_path:
                dep_by_path[dep_path]["depended_by"].append(d["path"])
                dep_by_path[dep_path]["depended_by_count"] += 1

    # 统计
    total_edges = sum(d["depends_on_count"] for d in deps)
    max_in = max((d["depended_by_count"] for d in deps), default=0)
    max_out = max((d["depends_on_count"] for d in deps), default=0)

    # 枢纽节点（被依赖最多的）
    hubs = sorted(deps, key=lambda d: -d["depended_by_count"])[:10]
    # 叶子节点（不依赖其他引擎）
    leaves = [d for d in deps if d["depends_on_count"] == 0]

    result = {
        "dna": DNA,
        "version": "1.0",
        "generated_at": _now(),
        "total_engines": len(deps),
        "total_edges": total_edges,
        "stats": {
            "max_in_degree": max_in,
            "max_out_degree": max_out,
            "avg_in_degree": round(sum(d["depended_by_count"] for d in deps) / max(len(deps), 1), 1),
            "avg_out_degree": round(sum(d["depends_on_count"] for d in deps) / max(len(deps), 1), 1),
            "hub_nodes": [h["name"] for h in hubs],
            "leaf_nodes": len(leaves),
            "engines_with_external": sum(1 for d in deps if d["external_count"] > 0),
        },
        "dependencies": deps,
        "external_dependencies": external_deps,
    }

    _log(f"依赖图完成: {len(deps)} 节点 · {total_edges} 边", "OK")
    return result


def detect_circular(graph: Dict[str, Any]) -> List[List[str]]:
    """检测循环依赖（DFS 拓扑排序变种）"""
    deps = graph["dependencies"]
    path_to_idx = {d["path"]: i for i, d in enumerate(deps)}
    adj_list: Dict[int, List[int]] = defaultdict(list)

    for d in deps:
        src_idx = path_to_idx.get(d["path"])
        if src_idx is None:
            continue
        for dep_path in d["depends_on"]:
            dst_idx = path_to_idx.get(dep_path)
            if dst_idx is not None:
                adj_list[src_idx].append(dst_idx)

    n = len(deps)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    cycles: List[List[int]] = []

    def dfs(u: int, parent: List[int]):
        color[u] = GRAY
        for v in adj_list.get(u, []):
            if color[v] == GRAY:
                # 找到循环
                cycle_start = parent.index(v) if v in parent else 0
                cycle = parent[cycle_start:] + [u]
                cycles.append(cycle)
            elif color[v] == WHITE:
                dfs(v, parent + [u])
        color[u] = BLACK

    for i in range(n):
        if color[i] == WHITE:
            dfs(i, [])

    # 转换为名称
    circular = []
    seen = set()
    for cycle in cycles:
        names = tuple(deps[i]["name"] for i in cycle)
        if names not in seen:
            seen.add(names)
            circular.append(list(names))

    return circular


def render_dot(graph: Dict[str, Any]) -> str:
    """渲染 Graphviz DOT 格式"""
    dot = "digraph 龍魂引擎依赖图 {\n"
    dot += '  rankdir=LR;\n  node [shape=box, style=filled, fillcolor="#1a1a2e", fontcolor="#e6c87c"];\n'
    dot += '  edge [color="#4a4a6e"];\n\n'

    for d in graph["dependencies"]:
        name = d["engine"]
        dot += f'  "{name}" [label="{name}"];\n'
        for dep_path in d["depends_on"]:
            # 找到依赖名称
            dep_name = dep_path.split("/")[-1].replace(".py", "")
            dot += f'  "{name}" -> "{dep_name}";\n'

    dot += "}\n"
    return dot


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


# ── 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 依赖关系映射器")
    parser.add_argument("--engine", type=str, help="查询单个引擎依赖")
    parser.add_argument("--graph", action="store_true", help="输出 Graphviz DOT 格式")
    parser.add_argument("--circular", action="store_true", help="检测循环依赖")
    parser.add_argument("--save", action="store_true", help="保存依赖图到文件")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    graph = build_dependency_graph()

    if args.engine:
        for d in graph["dependencies"]:
            if d["engine"] == args.engine:
                print(f"\n📦 {d['engine']}")
                print(f"   路径: {d['path']}")
                print(f"   依赖 ({d['depends_on_count']}):")
                for dep in d["depends_on"]:
                    print(f"     → {dep}")
                print(f"   被依赖 ({d['depended_by_count']}):")
                for dep in d["depended_by"]:
                    print(f"     ← {dep}")
                print(f"   外部依赖 ({d['external_count']}):")
                for ext in d["external_deps"]:
                    print(f"     · {ext}")
                return
        _log(f"未找到引擎: {args.engine}", "ERROR")
        return

    if args.circular:
        circular = detect_circular(graph)
        if circular:
            _log(f"发现 {len(circular)} 个循环依赖:", "WARN")
            for i, cycle in enumerate(circular, 1):
                print(f"  {i}. {' → '.join(cycle)}")
        else:
            _log("未发现循环依赖", "OK")
        return

    if args.graph:
        dot = render_dot(graph)
        print(dot)
        return

    # 默认：显示摘要
    stats = graph["stats"]
    print(f"📊 依赖图统计")
    print(f"   节点: {graph['total_engines']}")
    print(f"   边: {graph['total_edges']}")
    print(f"   最大入度: {stats['max_in_degree']} (最大被依赖)")
    print(f"   最大出度: {stats['max_out_degree']} (最大依赖数)")
    print(f"   平均入度: {stats['avg_in_degree']}")
    print(f"   平均出度: {stats['avg_out_degree']}")
    print(f"   叶子节点: {stats['leaf_nodes']} 个")
    print(f"   有外部依赖: {stats['engines_with_external']} 个")
    print(f"\n🏛️  枢纽节点 (被依赖最多):")
    for i, h in enumerate(graph["dependencies"]):
        if h["name"] in stats["hub_nodes"]:
            hb = "█" * max(1, h["depended_by_count"] // 2)
            print(f"  {h['name']:24s} 入度:{h['depended_by_count']:3d} 出度:{h['depends_on_count']:2d}  {hb}")

    if args.save:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(graph, f, ensure_ascii=False, indent=2)
        _log(f"依赖图已保存: {OUTPUT_FILE}", "OK")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
