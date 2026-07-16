#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂知识图谱查询引擎 (LongHun Knowledge Graph Engine)
=====================================================
为龙魂系统(UID9622)构建的轻量级知识图谱查询引擎。

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
#  内建测试数据（当数据目录不存在时使用）
# ═══════════════════════════════════════════════════════════════
BUILTIN_NODES = [
    {"id": "LH9622",    "type": "system",     "name": "龙魂系统",      "layer": "core",    "state": "active",   "desc": "龙魂系统核心本体"},
    {"id": "CORE-01",   "type": "core_mod",   "name": "意识内核",      "layer": "core",    "state": "active",   "desc": "主意识处理模块"},
    {"id": "CORE-02",   "type": "core_mod",   "name": "记忆引擎",      "layer": "core",    "state": "active",   "desc": "长期记忆存储与检索"},
    {"id": "SENS-01",   "type": "sensor",     "name": "视觉感知",      "layer": "input",   "state": "active",   "desc": "图像/视频输入处理"},
    {"id": "SENS-02",   "type": "sensor",     "name": "听觉感知",      "layer": "input",   "state": "standby",  "desc": "音频/语音输入处理"},
    {"id": "ACT-01",    "type": "actuator",   "name": "语音输出",      "layer": "output",  "state": "active",   "desc": "语音合成与输出"},
    {"id": "ACT-02",    "type": "actuator",   "name": "动作执行",      "layer": "output",  "state": "idle",     "desc": "物理动作控制"},
    {"id": "KNOW-01",   "type": "knowledge",  "name": "事实图谱",      "layer": "memory",  "state": "active",   "desc": "结构化知识存储"},
    {"id": "KNOW-02",   "type": "knowledge",  "name": "技能图谱",      "layer": "memory",  "state": "active",   "desc": "技能与能力表示"},
    {"id": "EMO-01",    "type": "emotion",    "name": "情感模块",      "layer": "core",    "state": "active",   "desc": "情感状态管理"},
    {"id": "REAS-01",   "type": "reasoning",  "name": "推理引擎",      "layer": "core",    "state": "active",   "desc": "逻辑推理与规划"},
    {"id": "COMM-01",   "type": "comm",       "name": "通讯接口",      "layer": "io",      "state": "active",   "desc": "外部系统通讯"},
    {"id": "SAFE-01",   "type": "safety",     "name": "安全护盾",      "layer": "core",    "state": "active",   "desc": "安全防护与权限控制"},
    {"id": "META-01",   "type": "meta",       "name": "元认知",        "layer": "core",    "state": "active",   "desc": "自我监控与反思"},
]

BUILTIN_EDGES = [
    {"source": "LH9622",  "target": "CORE-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含意识内核"},
    {"source": "LH9622",  "target": "CORE-02", "relation": "contains",    "weight": 1.0, "desc": "系统包含记忆引擎"},
    {"source": "LH9622",  "target": "SENS-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含视觉感知"},
    {"source": "LH9622",  "target": "SENS-02", "relation": "contains",    "weight": 1.0, "desc": "系统包含听觉感知"},
    {"source": "LH9622",  "target": "ACT-01",  "relation": "contains",    "weight": 1.0, "desc": "系统包含语音输出"},
    {"source": "LH9622",  "target": "ACT-02",  "relation": "contains",    "weight": 1.0, "desc": "系统包含动作执行"},
    {"source": "LH9622",  "target": "KNOW-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含事实图谱"},
    {"source": "LH9622",  "target": "KNOW-02", "relation": "contains",    "weight": 1.0, "desc": "系统包含技能图谱"},
    {"source": "LH9622",  "target": "EMO-01",  "relation": "contains",    "weight": 1.0, "desc": "系统包含情感模块"},
    {"source": "LH9622",  "target": "REAS-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含推理引擎"},
    {"source": "LH9622",  "target": "COMM-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含通讯接口"},
    {"source": "LH9622",  "target": "SAFE-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含安全护盾"},
    {"source": "LH9622",  "target": "META-01", "relation": "contains",    "weight": 1.0, "desc": "系统包含元认知"},
    {"source": "CORE-01", "target": "CORE-02", "relation": "depends_on",  "weight": 0.9, "desc": "意识内核依赖记忆引擎"},
    {"source": "CORE-01", "target": "REAS-01", "relation": "uses",        "weight": 0.8, "desc": "意识内核使用推理引擎"},
    {"source": "CORE-01", "target": "EMO-01",  "relation": "influences",  "weight": 0.7, "desc": "意识内核影响情感模块"},
    {"source": "SENS-01", "target": "CORE-01", "relation": "feeds",       "weight": 0.9, "desc": "视觉感知输入到意识内核"},
    {"source": "SENS-02", "target": "CORE-01", "relation": "feeds",       "weight": 0.8, "desc": "听觉感知输入到意识内核"},
    {"source": "CORE-01", "target": "ACT-01",  "relation": "controls",    "weight": 0.9, "desc": "意识内核控制语音输出"},
    {"source": "CORE-01", "target": "ACT-02",  "relation": "controls",    "weight": 0.8, "desc": "意识内核控制动作执行"},
    {"source": "KNOW-01", "target": "REAS-01", "relation": "supports",    "weight": 0.8, "desc": "事实图谱支持推理"},
    {"source": "KNOW-02", "target": "ACT-02",  "relation": "guides",      "weight": 0.7, "desc": "技能图谱指导动作"},
    {"source": "EMO-01",  "target": "CORE-01", "relation": "modulates",   "weight": 0.6, "desc": "情感调节意识处理"},
    {"source": "SAFE-01", "target": "COMM-01", "relation": "monitors",    "weight": 0.9, "desc": "安全护盾监控通讯"},
    {"source": "SAFE-01", "target": "ACT-02",  "relation": "restricts",   "weight": 0.8, "desc": "安全护盾限制动作"},
    {"source": "META-01", "target": "CORE-01", "relation": "observes",    "weight": 0.7, "desc": "元认知观察意识内核"},
    {"source": "META-01", "target": "SAFE-01", "relation": "audits",      "weight": 0.6, "desc": "元认知审计安全护盾"},
    {"source": "COMM-01", "target": "KNOW-01", "relation": "syncs",       "weight": 0.5, "desc": "通讯同步知识数据"},
    {"source": "REAS-01", "target": "META-01", "relation": "reports_to",  "weight": 0.6, "desc": "推理引擎向元认知报告"},
]

BUILTIN_STATES = {
    "states": ["active", "standby", "idle", "error", "maintenance"],
    "transitions": {
        "active":      ["standby", "idle", "error", "maintenance"],
        "standby":     ["active", "error"],
        "idle":        ["active", "standby", "error"],
        "error":       ["maintenance", "active"],
        "maintenance": ["active", "standby"],
    },
    "cascade_rules": {
        "CORE-01": {"contains": ["standby", "idle"]},
        "SAFE-01": {"monitors": ["error"]},
    },
}

BUILTIN_STATE_HISTORY = {
    "LH9622":  [{"time": "2024-01-01T00:00:00", "state": "maintenance", "trigger": "init"},
                 {"time": "2024-01-01T08:00:00", "state": "active",      "trigger": "boot_complete"}],
    "CORE-01": [{"time": "2024-01-01T00:00:00", "state": "maintenance", "trigger": "init"},
                 {"time": "2024-01-01T08:00:00", "state": "active",      "trigger": "boot_complete"}],
    "SENS-02": [{"time": "2024-01-01T00:00:00", "state": "active",      "trigger": "init"},
                 {"time": "2024-06-15T14:30:00", "state": "standby",     "trigger": "power_save"}],
    "ACT-02":  [{"time": "2024-01-01T00:00:00", "state": "active",      "trigger": "init"},
                 {"time": "2024-03-10T09:15:00", "state": "idle",        "trigger": "no_task"}],
}


# ═══════════════════════════════════════════════════════════════
#  LongHunGraph 核心类
# ═══════════════════════════════════════════════════════════════
class LongHunGraph:
    """龙魂知识图谱查询引擎"""

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
        """从指定目录加载 JSON 数据文件"""
        nodes_path = os.path.join(data_dir, "nodes.json")
        edges_path = os.path.join(data_dir, "edges.json")
        states_path = os.path.join(data_dir, "states.json")
        history_path = os.path.join(data_dir, "state_history.json")

        for p in [nodes_path, edges_path, states_path]:
            if not os.path.isfile(p):
                print(color(f"[WARN] 未找到 {p}，回退到内建测试数据", "yellow"), file=sys.stderr)
                self._load_builtin()
                return

        with open(nodes_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.nodes = {n["id"]: n for n in (raw if isinstance(raw, list) else raw.get("nodes", []))}

        with open(edges_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.edges = raw if isinstance(raw, list) else raw.get("edges", [])

        with open(states_path, "r", encoding="utf-8") as f:
            self.state_machine = json.load(f)

        if os.path.isfile(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self.state_history = defaultdict(list, json.load(f))
        else:
            self.state_history = defaultdict(list, {})

    def _load_builtin(self):
        """加载内建测试数据"""
        self.nodes = {n["id"]: n for n in BUILTIN_NODES}
        self.edges = list(BUILTIN_EDGES)
        self.state_machine = dict(BUILTIN_STATES)
        self.state_history = defaultdict(list, {k: list(v) for k, v in BUILTIN_STATE_HISTORY.items()})

    def _build_index(self):
        """构建邻接索引"""
        self._adj_out.clear()
        self._adj_in.clear()
        for e in self.edges:
            self._adj_out[e["source"]].append((e["target"], e))
            self._adj_in[e["target"]].append((e["source"], e))

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
        """显示节点详情 + 所有关联节点"""
        if node_id not in self.nodes:
            return None
        node = self.nodes[node_id]
        related = self.get_related(node_id)
        return {"node": node, "related": related}

    # ── get_related ────────────────────────────────────────
    def get_related(self, node_id, relation=None, direction="both"):
        """
        获取关联节点
        direction: 'out' | 'in' | 'both'
        """
        rels = []
        if direction in ("out", "both"):
            for tgt, e in self._adj_out.get(node_id, []):
                if relation is None or e.get("relation") == relation:
                    rels.append({"direction": "out", "edge": e, "node": self.nodes.get(tgt)})
        if direction in ("in", "both"):
            for src, e in self._adj_in.get(node_id, []):
                if relation is None or e.get("relation") == relation:
                    rels.append({"direction": "in", "edge": e, "node": self.nodes.get(src)})
        return rels

    # ── path (BFS) ─────────────────────────────────────────
    def find_path(self, source, target):
        """BFS 查找两个节点之间的最短路径"""
        if source not in self.nodes or target not in self.nodes:
            return None
        if source == target:
            return [source]

        visited = {source}
        queue = deque([(source, [source])])

        while queue:
            current, path = queue.popleft()
            for nxt, _ in self._adj_out.get(current, []):
                if nxt not in visited:
                    new_path = path + [nxt]
                    if nxt == target:
                        return new_path
                    visited.add(nxt)
                    queue.append((nxt, new_path))
        return None  # 无路径

    # ── state ──────────────────────────────────────────────
    def get_state_history(self, node_id):
        """获取节点状态历史"""
        if node_id not in self.nodes:
            return None
        hist = self.state_history.get(node_id, [])
        if not hist:
            current = self.nodes[node_id].get("state", "unknown")
            hist = [{"time": "now", "state": current, "trigger": "current"}]
        return hist

    # ── export ─────────────────────────────────────────────
    def export_mermaid(self, output_path=None, layer_filter=None):
        """导出 Mermaid 格式关系图"""
        lines = ["graph TD"]

        # 节点定义（按 layer 分组用 subgraph）
        layers = defaultdict(list)
        for nid, n in self.nodes.items():
            if layer_filter and n.get("layer") != layer_filter:
                continue
            layers[n.get("layer", "default")].append(n)

        # 子图
        layer_colors = {
            "core":    "#ff9999",
            "input":   "#99ff99",
            "output":  "#9999ff",
            "memory":  "#ffff99",
            "io":      "#ffcc99",
        }

        for layer, nodes in sorted(layers.items()):
            lines.append(f"    subgraph {layer.upper()}")
            for n in nodes:
                nid = n["id"]
                name = n.get("name", nid)
                state = n.get("state", "unknown")
                bg = layer_colors.get(layer, "#cccccc")
                style = f' style {nid} fill:{bg},stroke:#333,stroke-width:2px'
                state_emoji = {"active": "🟢", "standby": "🟡", "idle": "⚪", "error": "🔴", "maintenance": "🔵"}.get(state, "⚫")
                lines.append(f"        {nid}[{state_emoji} {name}<br/><small>{nid}</small>]{style}")
            lines.append("    end")

        # 边定义
        for e in self.edges:
            src, tgt = e["source"], e["target"]
            if layer_filter:
                src_layer = self.nodes.get(src, {}).get("layer")
                tgt_layer = self.nodes.get(tgt, {}).get("layer")
                if src_layer != layer_filter and tgt_layer != layer_filter:
                    continue
            rel = e.get("relation", "")
            w = e.get("weight", 1.0)
            style = "-->"
            if w < 0.5:
                style = "-.->"
            elif w >= 0.9:
                style = "==>"
            lines.append(f'    {src} {style}|{rel}| {tgt}')

        mermaid = "\n".join(lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(mermaid)
        return mermaid

    # ── transition ─────────────────────────────────────────
    def apply_state_transition(self, node_id, new_state):
        """
        应用状态转换，联动更新关联节点
        返回 (success: bool, messages: list, affected_nodes: list)
        """
        if node_id not in self.nodes:
            return False, [color(f"[ERROR] 节点 '{node_id}' 不存在", "red")], []

        valid_states = self.state_machine.get("states", [])
        transitions = self.state_machine.get("transitions", {})
        cascade_rules = self.state_machine.get("cascade_rules", {})

        if new_state not in valid_states:
            return False, [color(f"[ERROR] 无效状态 '{new_state}'，有效状态: {valid_states}", "red")], []

        node = self.nodes[node_id]
        current = node.get("state", "unknown")

        if new_state not in transitions.get(current, []):
            allowed = transitions.get(current, [])
            return False, [color(f"[ERROR] 不能从 '{current}' 转换到 '{new_state}'，允许: {allowed}", "red")], []

        messages = []
        affected = []

        # 执行转换
        node["state"] = new_state
        affected.append(node_id)
        messages.append(color(f"[OK] {node_id} ({node.get('name', '')}): {current} -> {new_state}", "green"))

        # 记录历史
        import datetime
        self.state_history[node_id].append({
            "time": datetime.datetime.now().isoformat(),
            "state": new_state,
            "trigger": "manual_transition"
        })

        # 级联更新
        if node_id in cascade_rules:
            rules = cascade_rules[node_id]
            for rel_type, trigger_states in rules.items():
                if new_state in trigger_states:
                    for tgt, e in self._adj_out.get(node_id, []):
                        if e.get("relation") == rel_type and tgt in self.nodes:
                            tgt_node = self.nodes[tgt]
                            if tgt_node.get("state") != new_state:
                                old = tgt_node["state"]
                                tgt_node["state"] = new_state
                                affected.append(tgt)
                                messages.append(
                                    color(f"    [CASCADE] {tgt} ({tgt_node.get('name', '')}): {old} -> {new_state} "
                                          f"(via {rel_type})", "cyan")
                                )
                                self.state_history[tgt].append({
                                    "time": datetime.datetime.now().isoformat(),
                                    "state": new_state,
                                    "trigger": f"cascade_from_{node_id}"
                                })

        return True, messages, affected


# ═══════════════════════════════════════════════════════════════
#  CLI 格式化输出
# ═══════════════════════════════════════════════════════════════
def print_banner():
    print(color("╔══════════════════════════════════════════════════════════════╗", "cyan"))
    print(color("║         龙魂知识图谱查询引擎  v1.0  (UID9622)               ║", "cyan", "bold"))
    print(color("╚══════════════════════════════════════════════════════════════╝", "cyan"))


def print_list(nodes):
    if not nodes:
        print(color("(无匹配节点)", "dim"))
        return

    # 表头
    print(color(f"{'ID':<12} {'名称':<14} {'类型':<12} {'层级':<8} {'状态':<10} 描述", "bold"))
    print(color("─" * 80, "dim"))

    state_colors = {
        "active": "green", "standby": "yellow", "idle": "dim",
        "error": "red", "maintenance": "blue",
    }
    for n in nodes:
        sid = n.get("id", "")
        name = n.get("name", "")
        typ = n.get("type", "")
        layer = n.get("layer", "")
        state = n.get("state", "")
        desc = n.get("desc", "")
        sc = state_colors.get(state, "white")
        print(f"  {color(sid, 'bold'):<12} {name:<14} {typ:<12} {layer:<8} "
              f"{color(state, sc):<16} {desc}")
    print(color(f"\n共 {len(nodes)} 个节点", "dim"))


def print_show(result):
    if result is None:
        print(color("[ERROR] 节点不存在", "red"))
        return

    node = result["node"]
    related = result["related"]

    print(color("┌─ 节点详情", "bold"))
    print(f"  {color('ID:', 'bold')}    {node.get('id', '')}")
    print(f"  {color('名称:', 'bold')}  {node.get('name', '')}")
    print(f"  {color('类型:', 'bold')}  {node.get('type', '')}")
    print(f"  {color('层级:', 'bold')}  {node.get('layer', '')}")
    print(f"  {color('状态:', 'bold')}  {node.get('state', '')}")
    print(f"  {color('描述:', 'bold')}  {node.get('desc', '')}")

    print(color("\n┌─ 关联节点", "bold"))
    if not related:
        print("  (无关联)")
    else:
        print(color(f"  {'方向':<8} {'关系':<14} {'目标ID':<12} {'目标名称':<14} {'权重':<6}", "dim"))
        for r in related:
            d = "→ 输出" if r["direction"] == "out" else "← 输入"
            e = r["edge"]
            n = r["node"] or {}
            print(f"  {d:<10} {e.get('relation', ''):<14} {n.get('id', ''):<12} "
                  f"{n.get('name', ''):<14} {e.get('weight', '')}")
    print()


def print_path(graph, source, target, path):
    if path is None:
        print(color(f"[INFO] {source} 与 {target} 之间无路径", "yellow"))
        return

    print(color(f"\n路径: {source} → {target} (共 {len(path)} 个节点)", "bold"))
    for i, nid in enumerate(path):
        n = graph.nodes.get(nid, {})
        arrow = " → " if i < len(path) - 1 else ""
        print(f"  {color(nid, 'bold')}({n.get('name', '')}){arrow}", end="")
    print("\n")

    # 详细路径
    print(color("详细路径:", "bold"))
    for i in range(len(path) - 1):
        src, tgt = path[i], path[i + 1]
        edge_info = None
        for t, e in graph._adj_out.get(src, []):
            if t == tgt:
                edge_info = e
                break
        if edge_info:
            print(f"  [{i+1}] {src} --[{edge_info.get('relation', '')}, w={edge_info.get('weight', '')}]--> {tgt}")
        else:
            print(f"  [{i+1}] {src} --> {tgt}")


def print_state_history(node_id, history):
    if history is None:
        print(color("[ERROR] 节点不存在", "red"))
        return

    print(color(f"\n节点 {node_id} 的状态历史:", "bold"))
    print(color(f"  {'时间':<24} {'状态':<14} {'触发器':<20}", "dim"))
    print(color("  " + "─" * 60, "dim"))
    state_colors = {
        "active": "green", "standby": "yellow", "idle": "dim",
        "error": "red", "maintenance": "blue",
    }
    for h in history:
        t = h.get("time", "")
        s = h.get("state", "")
        tr = h.get("trigger", "")
        sc = state_colors.get(s, "white")
        print(f"  {t:<24} {color(s, sc):<20} {tr}")


# ═══════════════════════════════════════════════════════════════
#  主入口 & 参数解析
# ═══════════════════════════════════════════════════════════════
def main():
    data_dir = os.environ.get("LHKG_DIR", os.path.join(os.path.expanduser("~"), ".龍魂", "knowledge-graph"))

    parser = argparse.ArgumentParser(
        prog="longhun_kg.py",
        description=color("龙魂知识图谱查询引擎", "bold"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python longhun_kg.py list
  python longhun_kg.py list --type core_mod --state active
  python longhun_kg.py show CORE-01
  python longhun_kg.py path SENS-01 ACT-01
  python longhun_kg.py state CORE-01
  python longhun_kg.py export --output graph.mmd
  python longhun_kg.py transition ACT-02 active
        """
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # list
    p_list = sub.add_parser("list", help="列出节点")
    p_list.add_argument("--type",  dest="node_type", help="按类型过滤")
    p_list.add_argument("--layer", help="按层级过滤")
    p_list.add_argument("--state", help="按状态过滤")
    p_list.add_argument("--data-dir", default=data_dir, help="数据目录")

    # show
    p_show = sub.add_parser("show", help="显示节点详情")
    p_show.add_argument("node_id", help="节点 ID")
    p_show.add_argument("--data-dir", default=data_dir, help="数据目录")

    # path
    p_path = sub.add_parser("path", help="查找两节点间路径")
    p_path.add_argument("source", help="源节点 ID")
    p_path.add_argument("target", help="目标节点 ID")
    p_path.add_argument("--data-dir", default=data_dir, help="数据目录")

    # state
    p_state = sub.add_parser("state", help="查看节点状态历史")
    p_state.add_argument("node_id", help="节点 ID")
    p_state.add_argument("--data-dir", default=data_dir, help="数据目录")

    # export
    p_export = sub.add_parser("export", help="导出 Mermaid 关系图")
    p_export.add_argument("--output", help="输出文件路径（可选，默认 stdout）")
    p_export.add_argument("--layer", dest="layer_filter", help="仅导出指定层级")
    p_export.add_argument("--data-dir", default=data_dir, help="数据目录")

    # transition
    p_trans = sub.add_parser("transition", help="应用状态转换")
    p_trans.add_argument("node_id", help="节点 ID")
    p_trans.add_argument("new_state", help="新状态")
    p_trans.add_argument("--data-dir", default=data_dir, help="数据目录")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    # 初始化图
    graph = LongHunGraph(getattr(args, "data_dir", data_dir))

    if args.command == "list":
        nodes = graph.list_nodes(
            node_type=args.node_type,
            layer=args.layer,
            state=args.state,
        )
        print_list(nodes)

    elif args.command == "show":
        result = graph.show_node(args.node_id)
        print_show(result)

    elif args.command == "path":
        path = graph.find_path(args.source, args.target)
        print_path(graph, args.source, args.target, path)

    elif args.command == "state":
        hist = graph.get_state_history(args.node_id)
        print_state_history(args.node_id, hist)

    elif args.command == "export":
        mermaid = graph.export_mermaid(args.output, args.layer_filter)
        if not args.output:
            print(color("\n```mermaid", "dim"))
            print(mermaid)
            print(color("```\n", "dim"))
        else:
            print(color(f"[OK] Mermaid 图已导出到: {args.output}", "green"))

    elif args.command == "transition":
        ok, msgs, affected = graph.apply_state_transition(args.node_id, args.new_state)
        for m in msgs:
            print(m)
        if ok:
            print(color(f"\n共影响 {len(affected)} 个节点: {affected}", "dim"))


if __name__ == "__main__":
    main()
