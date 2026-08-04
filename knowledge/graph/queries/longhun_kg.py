#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知识图谱查询引擎 (LongHun Knowledge Graph Engine)
=====================================================
为龍魂系统(UID9622)构建的轻量级知识图谱查询引擎。

功能:
  - list   : 列出节点（支持类型/层级/状态过滤）
  - show   : 显示节点详情与关联节点
  - path   : BFS 查找两节点间最短路径
  - state  : 查看节点状态历史
  - export : 导出 Mermaid 格式关系图
  - transition: 应用状态转换（含联动更新）

依赖: Python 3.8+ 标准库 only
"""

import json
import os
import sys
import argparse
from collections import deque, defaultdict

# ═══════════════════════════════════════════════════════════════
#  ANSI 颜色常量
# ═══════════════════════════════════════════════════════════════
C = {
    "reset":    "\033[0m",
    "bold":     "\033[1m",
    "dim":      "\033[2m",
    "red":      "\033[91m",
    "green":    "\033[92m",
    "yellow":   "\033[93m",
    "blue":     "\033[94m",
    "magenta":  "\033[95m",
    "cyan":     "\033[96m",
    "white":    "\033[97m",
    "bg_red":   "\033[41m",
    "bg_green": "\033[42m",
    "bg_blue":  "\033[44m",
}


def color(text, *codes):
    """为文本添加 ANSI 颜色"""
    if not sys.stdout.isatty():
        return text
    return "".join(C.get(c, "") for c in codes) + text + C["reset"]


# ═══════════════════════════════════════════════════════════════
#  LongHunGraph 核心类
# ═══════════════════════════════════════════════════════════════
class LongHunGraph:
    """龍魂知识图谱查询引擎"""

    def __init__(self, data_dir):
        """
        加载 nodes/edges/states JSON 文件
        若目录不存在，使用内建测试数据
        """
        self.data_dir = data_dir
        self.nodes = {}
        self.edges = []
        self.state_machine = {}
        self.state_history = defaultdict(list)
        self._adj_out = defaultdict(list)   # source -> [(target, edge_dict), ...]
        self._adj_in  = defaultdict(list)   # target -> [(source, edge_dict), ...]

        if data_dir and os.path.isdir(data_dir):
            self._load_from_dir(data_dir)
        else:
            self._load_builtin()

        self._build_index()

    # ── 数据加载 ───────────────────────────────────────────
    def _load_from_dir(self, data_dir):
        """从指定目录加载 JSON 数据文件
        
        支持两种目录结构:
        1. 扁平结构: data_dir/nodes.json, data_dir/edges.json, data_dir/states.json
        2. 分层结构: data_dir/nodes/all_nodes.json, data_dir/edges/all_edges.json, data_dir/states/state_machine.json
        """
        # 尝试分层结构（龍魂标准结构）
        nodes_path = os.path.join(data_dir, "nodes", "all_nodes.json")
        edges_path = os.path.join(data_dir, "edges", "all_edges.json")
        states_path = os.path.join(data_dir, "states", "state_machine.json")
        history_path = os.path.join(data_dir, "states", "state_history.json")
        
        # 回退到扁平结构
        if not os.path.isfile(nodes_path):
            nodes_path = os.path.join(data_dir, "nodes.json")
        if not os.path.isfile(edges_path):
            edges_path = os.path.join(data_dir, "edges.json")
        if not os.path.isfile(states_path):
            states_path = os.path.join(data_dir, "states.json")

        # 检查关键文件
        key_files = [(nodes_path, "nodes"), (edges_path, "edges")]
        for p, name in key_files:
            if not os.path.isfile(p):
                print(color(f"[WARN] 未找到 {name} 数据 ({p})，回退到内建测试数据", "yellow"), file=sys.stderr)
                self._load_builtin()
                return

        with open(nodes_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            # 支持 {metadata, nodes: [...]} 或 [...] 格式
            node_list = raw.get("nodes", []) if isinstance(raw, dict) else raw
            # 适配不同字段名: node_id/id, node_type/type/category, dna/dna_trace, state/status
            self.nodes = {}
            for n in node_list:
                nid = n.get("node_id", n.get("id", "unknown"))
                # 适配多种字段名格式
                node_type = n.get("node_type", n.get("type", n.get("category", "unknown")))
                dna_val = n.get("dna", "")
                if not dna_val or not isinstance(dna_val, str):
                    dna_val = n.get("dna_trace", "")
                self.nodes[nid] = {
                    "id": nid,
                    "node_id": nid,
                    "type": node_type,
                    "node_type": node_type,
                    "name": n.get("name", n.get("display", nid)),
                    "desc": n.get("description", n.get("desc", "")),
                    "description": n.get("description", n.get("desc", "")),
                    "layer": n.get("layer", "unknown"),
                    "state": n.get("state", n.get("status", "active")),
                    "dna": dna_val,
                    "properties": n.get("properties", {}),
                    "version": n.get("version", "v1.0"),
                    "created_at": n.get("created_at", ""),
                    "updated_at": n.get("updated_at", ""),
                }

        with open(edges_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            edge_list = raw.get("edges", []) if isinstance(raw, dict) else raw
            self.edges = []
            for e in edge_list:
                self.edges.append({
                    "edge_id": e.get("edge_id", e.get("id", "")),
                    "source": e.get("source", e.get("from", "")),
                    "target": e.get("target", e.get("to", "")),
                    "relation": e.get("relation", e.get("type", "")),
                    "description": e.get("description", e.get("desc", "")),
                    "dna": e.get("dna", e.get("dna_trace", "")),
                    "properties": e.get("properties", {}),
                })

        with open(states_path, "r", encoding="utf-8") as f:
            self.state_machine = json.load(f)

        if os.path.isfile(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self.state_history = defaultdict(list, json.load(f))
        else:
            self.state_history = defaultdict(list, {})

    def _load_builtin(self):
        """加载内建测试数据"""
        self.nodes = {
            "LH9622": {"id": "LH9622", "node_id": "LH9622", "type": "system", "node_type": "system", "name": "龍魂系统", "layer": "core", "state": "active", "desc": "龍魂系统核心本体", "dna": "#龍芯⚡️2026-06-27-LHKG-BUILTIN-v1.0", "properties": {}, "version": "v1.0", "created_at": "", "updated_at": ""},
        }
        self.edges = []
        self.state_machine = {
            "states": ["active", "pending", "suspended", "terminated", "overridden", "merged"],
            "transitions": {
                "active": ["pending", "suspended", "terminated", "overridden"],
                "pending": ["active", "suspended", "terminated"],
                "suspended": ["active", "pending", "terminated"],
                "terminated": [],
                "overridden": ["active", "terminated"],
                "merged": [],
            }
        }
        self.state_history = defaultdict(list)

    def _build_index(self):
        """构建邻接索引"""
        self._adj_out.clear()
        self._adj_in.clear()
        for e in self.edges:
            src = e.get("source", "")
            tgt = e.get("target", "")
            if src and tgt:
                self._adj_out[src].append((tgt, e))
                self._adj_in[tgt].append((src, e))

    # ── list ───────────────────────────────────────────────
    def list_nodes(self, node_type=None, layer=None, state=None):
        """列出节点，支持按类型 / 层级 / 状态过滤"""
        results = []
        for nid, n in self.nodes.items():
            if node_type and n.get("type") != node_type:
                continue
            if layer and n.get("layer") != layer:
                continue
            if state and n.get("state") != state:
                continue
            results.append(n)
        return results

    # ── show ───────────────────────────────────────────────
    def show_node(self, node_id):
        """显示节点详情 + 关联节点"""
        node = self.nodes.get(node_id)
        if not node:
            return {"error": f"节点 {node_id} 不存在"}

        related = {
            "outgoing": [],
            "incoming": [],
        }
        for tgt, e in self._adj_out.get(node_id, []):
            related["outgoing"].append({"target": tgt, "relation": e.get("relation", ""), "description": e.get("description", "")})
        for src, e in self._adj_in.get(node_id, []):
            related["incoming"].append({"source": src, "relation": e.get("relation", ""), "description": e.get("description", "")})

        return {"node": node, "related": related}

    # ── path ───────────────────────────────────────────────
    def find_path(self, source, target):
        """BFS 查找两节点间最短路径"""
        if source not in self.nodes:
            return None
        if target not in self.nodes:
            return None
        if source == target:
            return [source]

        visited = {source}
        queue = deque([(source, [source])])

        while queue:
            current, path = queue.popleft()
            for nxt, _ in self._adj_out.get(current, []):
                if nxt == target:
                    return path + [nxt]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))
        return None

    # ── state ──────────────────────────────────────────────
    def get_state_history(self, node_id):
        """获取节点状态历史"""
        if node_id not in self.nodes:
            return {"error": f"节点 {node_id} 不存在"}
        history = self.state_history.get(node_id, [])
        return {"node": node_id, "current_state": self.nodes[node_id].get("state"), "history": history}

    # ── export ─────────────────────────────────────────────
    def export_mermaid(self, output_path, layer_filter=None):
        """导出 Mermaid 格式关系图"""
        lines = ["graph TD"]
        lines.append("")

        # 按层级分组
        layers = defaultdict(list)
        for nid, n in self.nodes.items():
            l = n.get("layer", "unknown").upper()
            layers[l].append(n)

        # 定义层级颜色
        layer_colors = {
            "SOVEREIGNTY": "fill:#DC2626,color:#fff",
            "GOVERNANCE": "fill:#2563EB,color:#fff",
            "MECHANISM": "fill:#16A34A,color:#fff",
            "FOUNDATION": "fill:#4B5563,color:#fff",
            "UNKNOWN": "fill:#cccccc,color:#333",
        }

        # 输出子图
        for layer_name, node_list in sorted(layers.items()):
            if layer_filter and layer_name.lower() != layer_filter.lower():
                continue
            lines.append(f"    subgraph {layer_name}")
            for n in node_list:
                nid = n["id"]
                name = n.get("name", nid)
                state_icon = "🟢" if n.get("state") == "active" else "🟡" if n.get("state") == "pending" else "🔴" if n.get("state") == "terminated" else "⚪"
                lines.append(f"        {nid}[{state_icon} {name}]")
                style = layer_colors.get(layer_name, layer_colors["UNKNOWN"])
                lines.append(f"        style {nid} {style}")
            lines.append("    end")
            lines.append("")

        # 输出边
        for e in self.edges:
            src = e.get("source", "")
            tgt = e.get("target", "")
            rel = e.get("relation", "")
            if src in self.nodes and tgt in self.nodes:
                lines.append(f"    {src} -->|{rel}| {tgt}")

        content = "\n".join(lines)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
        return content

    # ── transition ─────────────────────────────────────────
    def apply_state_transition(self, node_id, new_state):
        """应用状态转换，联动更新关联节点"""
        if node_id not in self.nodes:
            return {"error": f"节点 {node_id} 不存在"}

        old_state = self.nodes[node_id].get("state", "active")
        self.nodes[node_id]["state"] = new_state

        # 记录历史
        entry = {"time": "2026-06-27T00:00:00Z", "from": old_state, "to": new_state, "trigger": "manual"}
        self.state_history[node_id].append(entry)

        # 联动更新
        cascaded = []
        if new_state == "suspended":
            # 暂停子节点
            for tgt, e in self._adj_out.get(node_id, []):
                child = self.nodes.get(tgt)
                if child and child.get("state") == "active":
                    child["state"] = "pending"
                    cascaded.append({"node": tgt, "action": "active->pending", "reason": "parent_suspended"})
        elif new_state == "terminated":
            # 终止子节点
            for tgt, e in self._adj_out.get(node_id, []):
                child = self.nodes.get(tgt)
                if child and child.get("state") != "terminated":
                    child["state"] = "suspended"
                    cascaded.append({"node": tgt, "action": "->suspended", "reason": "parent_terminated"})

        return {"node": node_id, "old": old_state, "new": new_state, "cascaded": cascaded}


# ═══════════════════════════════════════════════════════════════
#  命令行入口
# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂知识图谱查询引擎")
    parser.add_argument("--data-dir", default=os.environ.get("LHKG_DIR", os.path.expanduser("~/.龍魂/knowledge-graph")), help="数据目录")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="列出节点")
    p_list.add_argument("--type", help="按类型过滤")
    p_list.add_argument("--layer", help="按层级过滤")
    p_list.add_argument("--state", help="按状态过滤")

    p_show = sub.add_parser("show", help="显示节点详情")
    p_show.add_argument("node_id", help="节点ID")

    p_path = sub.add_parser("path", help="查找路径")
    p_path.add_argument("source", help="源节点")
    p_path.add_argument("target", help="目标节点")

    p_state = sub.add_parser("state", help="查看状态历史")
    p_state.add_argument("node_id", help="节点ID")

    p_export = sub.add_parser("export", help="导出Mermaid")
    p_export.add_argument("--output", default="graph.mmd", help="输出文件")
    p_export.add_argument("--layer", help="按层级过滤")

    p_trans = sub.add_parser("transition", help="状态转换")
    p_trans.add_argument("node_id", help="节点ID")
    p_trans.add_argument("new_state", help="新状态")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    g = LongHunGraph(args.data_dir)

    if args.cmd == "list":
        nodes = g.list_nodes(node_type=args.type, layer=args.layer, state=args.state)
        print(color(f"\n📊 共 {len(nodes)} 个节点\n", "bold", "cyan"))
        for n in nodes:
            state_color = "green" if n.get("state") == "active" else "yellow" if n.get("state") == "pending" else "red"
            print(f"  {color(n['id'], 'bold')} | {color(n.get('name', ''), 'white')} | "
                  f"type={color(n.get('type', ''), 'cyan')} | layer={color(n.get('layer', ''), 'blue')} | "
                  f"state={color(n.get('state', ''), state_color)}")

    elif args.cmd == "show":
        result = g.show_node(args.node_id)
        if "error" in result:
            print(color(f"❌ {result['error']}", "red"))
            sys.exit(1)
        n = result["node"]
        print(color(f"\n📋 节点详情: {n['name']}\n", "bold", "cyan"))
        print(f"  ID:       {n['id']}")
        print(f"  类型:     {n.get('type', '')}")
        print(f"  层级:     {n.get('layer', '')}")
        print(f"  状态:     {n.get('state', '')}")
        print(f"  DNA:      {n.get('dna', '')}")
        print(f"  描述:     {n.get('desc', '')}")
        if result["related"]["outgoing"]:
            print(color(f"\n  → 出边 ({len(result['related']['outgoing'])}):", "yellow"))
            for r in result["related"]["outgoing"]:
                print(f"    {r['relation']} → {r['target']}")
        if result["related"]["incoming"]:
            print(color(f"\n  ← 入边 ({len(result['related']['incoming'])}):", "green"))
            for r in result["related"]["incoming"]:
                print(f"    ← {r['relation']} from {r['source']}")

    elif args.cmd == "path":
        path = g.find_path(args.source, args.target)
        if path:
            print(color(f"\n🔗 路径: {' → '.join(path)}\n", "bold", "green"))
        else:
            print(color(f"\n❌ 未找到从 {args.source} 到 {args.target} 的路径", "red"))

    elif args.cmd == "state":
        result = g.get_state_history(args.node_id)
        if "error" in result:
            print(color(f"❌ {result['error']}", "red"))
            sys.exit(1)
        print(color(f"\n📊 节点 {result['node']} 状态历史\n", "bold", "cyan"))
        print(f"  当前状态: {result['current_state']}")
        if result["history"]:
            for h in result["history"]:
                print(f"  {h['time']}: {h['from']} → {h['to']}")
        else:
            print("  (无历史记录)")

    elif args.cmd == "export":
        size = g.export_mermaid(args.output, layer_filter=args.layer)
        print(color(f"\n✅ 已导出到 {args.output} ({len(size)} 字符)\n", "bold", "green"))

    elif args.cmd == "transition":
        result = g.apply_state_transition(args.node_id, args.new_state)
        if "error" in result:
            print(color(f"❌ {result['error']}", "red"))
            sys.exit(1)
        print(color(f"\n🔄 状态转换: {result['old']} → {result['new']}", "bold", "yellow"))
        if result["cascaded"]:
            print(color(f"\n  联动更新 ({len(result['cascaded'])}):", "cyan"))
            for c in result["cascaded"]:
                print(f"    {c['node']}: {c['action']} ({c['reason']})")


if __name__ == "__main__":
    main()
