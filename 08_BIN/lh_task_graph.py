#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·任务关联图谱引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-TASK-GRAPH-V1.0-7d3f1a9b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 基于 NetworkX 的任务关联图（节点=历史任务·边=语义/时序/因果）
  - 与意念交流引擎 ROM固化 无缝联动（后处理钩子）
  - 四类边：semantic_similarity / temporal_sequence / same_persona / keyword_overlap
  - 查询：find_related / suggest_next / find_patterns / stats
  - 持久化：data/task_graph.json（NetworkX node-link-data 标准格式）
  - 集成点：
    * 每次意图引擎处理完成后 → add_task() 写节点+自动建边
    * 阶段2历史追溯 → find_related() 增强上下文
    * 阶段9自适应学习 → find_patterns() 发现高频模式

用法:
  python3 bin/lh_task_graph.py add --input "健康检查" --persona P09孙思邈 --success
  python3 bin/lh_task_graph.py related "系统巡检" -k 5
  python3 bin/lh_task_graph.py suggest "部署上线"
  python3 bin/lh_task_graph.py stats
  python3 bin/lh_task_graph.py patterns --min-freq 3
  python3 bin/lh_task_graph.py --interactive

依赖:
  pip install networkx  (已安装: 3.6.1)
"""

import json
import uuid
import hashlib
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter
import argparse
import sys

try:
    import networkx as nx
except ImportError:
    print("❌ 需要 networkx: pip install networkx")
    sys.exit(1)


# ============================================================
# 零、常量 & 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
GRAPH_PATH = PROJECT_ROOT / "data" / "task_graph.json"
INTENT_ARCHIVE = Path.home() / ".longhun" / "intent_archive"

# 边类型
EDGE_TYPES = {
    "semantic_similarity": "语义相似·关键词重叠≥50%",
    "temporal_sequence":   "时序相邻·前后30分钟内",
    "same_persona":        "同一人格触发",
    "keyword_overlap":     "关键词重叠·但不足语义阈值",
    "causal_dependency":   "因果依赖·前置任务→后继任务",
}

# 语义相似度阈值
SEMANTIC_THRESHOLD = 0.5  # 关键词重叠比例≥50%视为语义相关
TEMPORAL_WINDOW_MINUTES = 30  # 30分钟内的任务视为时序相邻
MAX_GRAPH_SIZE = 10000  # 最大节点数，超过自动修剪最旧节点


# ============================================================
# 一、DNA追溯工具（复用意图引擎的格式）
# ============================================================

class DNATrace:
    @staticmethod
    def scene_fingerprint(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    @staticmethod
    def generate(module: str, action: str) -> str:
        now = datetime.datetime.now()
        h = hashlib.sha256(f"{module}{action}{now.isoformat()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{now.strftime('%Y%m%d%H%M%S')}-{module}-{action}-{h}"


# ============================================================
# 二、任务节点 & 边数据结构
# ============================================================

@dataclass
class TaskNode:
    """任务图谱节点"""
    task_id: str
    input_text: str
    task_type: str           # 技术咨询/战略推演/情感支持/查询状态/系统操作/知识查询/通用咨询
    persona: str             # P01诸葛亮/P04鲁班/P02宝宝...
    keywords: List[str]
    emotion_score: float
    success: bool
    response_summary: str
    dna: str
    timestamp: str           # ISO 8601
    rom_hit: bool = False
    audit_mark: str = "🟢"   # 🟢🟡🔴

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "TaskNode":
        return cls(**{k: d.get(k, None) for k in [
            "task_id","input_text","task_type","persona","keywords",
            "emotion_score","success","response_summary","dna","timestamp",
            "rom_hit","audit_mark"
        ]})


# ============================================================
# 三、任务关联图谱引擎
# ============================================================

class TaskGraphEngine:
    """龍魂·任务关联图谱引擎 v1.0"""

    def __init__(self, storage_path: Path = GRAPH_PATH):
        self.storage_path = storage_path
        self.graph = nx.DiGraph()
        self._loaded = False
        self._load()

    # ── 持久化 ─────────────────────────────────
    def _load(self):
        """从磁盘加载图谱"""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                # NetworkX 3.x node_link_graph 兼容
                if "directed" in data and "multigraph" in data \
                   and "nodes" in data and "links" in data:
                    self.graph = nx.node_link_graph(data, edges="links")
                else:
                    # 旧格式兼容
                    self.graph = nx.node_link_graph(data)
                self._loaded = True
            except Exception as e:
                print(f"⚠️ 图谱加载失败: {e}，使用空图")
                self.graph = nx.DiGraph()
        else:
            self.graph = nx.DiGraph()
            self._loaded = True

    def _save(self):
        """持久化到磁盘"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = nx.node_link_data(self.graph, edges="links")
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _prune_if_needed(self):
        """超过最大节点数时修剪最旧节点"""
        if len(self.graph) > MAX_GRAPH_SIZE:
            nodes = sorted(
                self.graph.nodes(data=True),
                key=lambda x: x[1].get("timestamp", "")
            )
            remove_count = len(nodes) - MAX_GRAPH_SIZE + 100
            for n, _ in nodes[:remove_count]:
                self.graph.remove_node(n)
            self._save()

    # ── 关键词提取 ─────────────────────────────
    @staticmethod
    def extract_keywords(text: str, max_k: int = 5) -> List[str]:
        """从输入文本提取中文关键词"""
        过滤 = {"这个","那个","什么","怎么","为什么","的","了","是",
                "一下","帮我","给我","可以","一个","现在","需要",
                "然后","还是","已经","还有","有些","不是","其他"}
        词列表 = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        # 按频率排序，过滤停用词
        freq = Counter(w for w in 词列表 if w not in 过滤)
        return [w for w, _ in freq.most_common(max_k)]

    # ── 语义相似度计算 ─────────────────────────
    @staticmethod
    def semantic_similarity(kw1: List[str], kw2: List[str]) -> float:
        """Jaccard 相似度（关键词集合重叠比例）"""
        s1, s2 = set(kw1), set(kw2)
        if not s1 or not s2:
            return 0.0
        return len(s1 & s2) / len(s1 | s2)

    # ── 添加任务节点 ──────────────────────────
    def add_task(self,
                 input_text: str,
                 task_type: str = "通用咨询",
                 persona: str = "P01诸葛亮",
                 success: bool = True,
                 emotion_score: float = 0.5,
                 response_summary: str = "",
                 audit_mark: str = "🟢",
                 rom_hit: bool = False) -> str:
        """添加任务节点并自动建立与历史任务的边"""
        # 提取关键词
        keywords = self.extract_keywords(input_text)
        timestamp = datetime.datetime.now().isoformat()
        task_id = f"TASK-{uuid.uuid4().hex[:12].upper()}"
        dna = DNATrace.generate("任务图谱", task_type)

        # 创建节点
        node = TaskNode(
            task_id=task_id,
            input_text=input_text,
            task_type=task_type,
            persona=persona,
            keywords=keywords,
            emotion_score=emotion_score,
            success=success,
            response_summary=response_summary[:200],
            dna=dna,
            timestamp=timestamp,
            rom_hit=rom_hit,
            audit_mark=audit_mark,
        )
        self.graph.add_node(task_id, **node.to_dict())

        # 自动建边：与历史任务关联
        self._auto_link(task_id, node)

        # 持久化+修剪
        self._prune_if_needed()
        self._save()

        return task_id

    def _auto_link(self, new_id: str, new_node: TaskNode):
        """自动与新任务建立关联边"""
        new_ts = datetime.datetime.fromisoformat(new_node.timestamp)
        new_kw = new_node.keywords

        for node_id, attrs in self.graph.nodes(data=True):
            if node_id == new_id:
                continue

            old_ts_str = attrs.get("timestamp", "")
            old_kw = attrs.get("keywords", [])
            old_persona = attrs.get("persona", "")

            # 1. 语义相似边（关键词Jaccard≥50%）
            sim = self.semantic_similarity(new_kw, old_kw)
            if sim >= SEMANTIC_THRESHOLD:
                self.graph.add_edge(new_id, node_id,
                    type="semantic_similarity", weight=round(sim, 2))

            # 2. 时序相邻边（前后30分钟内）
            try:
                old_ts = datetime.datetime.fromisoformat(old_ts_str)
                diff = abs((new_ts - old_ts).total_seconds()) / 60
                if diff <= TEMPORAL_WINDOW_MINUTES and diff > 0:
                    self.graph.add_edge(new_id, node_id,
                        type="temporal_sequence", weight=round(1.0 - diff/TEMPORAL_WINDOW_MINUTES, 2))
            except (ValueError, TypeError):
                pass

            # 3. 同一人格边
            if old_persona == new_node.persona:
                self.graph.add_edge(new_id, node_id,
                    type="same_persona", weight=1.0)

            # 4. 关键词重叠边（低于语义阈值但仍有关联）
            if 0 < sim < SEMANTIC_THRESHOLD:
                self.graph.add_edge(new_id, node_id,
                    type="keyword_overlap", weight=round(sim, 1))

    # ── 查询：找相关任务 ───────────────────────
    def find_related(self,
                     query: str,
                     top_k: int = 5,
                     min_similarity: float = 0.0) -> List[Dict]:
        """
        查找与查询文本最相关的历史任务。
        返回: [{task_id, input_text, persona, similarity, timestamp, ...}, ...]
        """
        query_kw = self.extract_keywords(query)
        if not query_kw:
            return []

        scored = []
        for node_id, attrs in self.graph.nodes(data=True):
            old_kw = attrs.get("keywords", [])
            sim = self.semantic_similarity(query_kw, old_kw)
            if sim >= min_similarity:
                scored.append({
                    "task_id": node_id,
                    "input_text": attrs.get("input_text", ""),
                    "persona": attrs.get("persona", ""),
                    "task_type": attrs.get("task_type", ""),
                    "similarity": round(sim, 3),
                    "timestamp": attrs.get("timestamp", ""),
                    "success": attrs.get("success", True),
                    "dna": attrs.get("dna", ""),
                })

        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]

    # ── 查询：基于图结构找相关任务 ─────────────
    def find_graph_related(self,
                           task_id: str,
                           max_depth: int = 2,
                           edge_types: Optional[List[str]] = None) -> List[Dict]:
        """
        基于图结构（边遍历）查找相关任务。
        比纯语义更精准——考虑时序、人格、因果等关系。
        """
        if task_id not in self.graph:
            return []

        related = set()
        # BFS 遍历
        queue = [(task_id, 0)]
        visited = {task_id}

        while queue:
            current, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for _, neighbor in self.graph.out_edges(current):
                if neighbor not in visited:
                    edge_data = self.graph.get_edge_data(current, neighbor)
                    etype = edge_data.get("type", "")
                    # 按边类型过滤
                    if edge_types and etype not in edge_types:
                        continue
                    visited.add(neighbor)
                    related.add(neighbor)

                    if depth + 1 < max_depth:
                        queue.append((neighbor, depth + 1))

        results = []
        for nid in related:
            attrs = self.graph.nodes[nid]
            results.append({
                "task_id": nid,
                "input_text": attrs.get("input_text", ""),
                "persona": attrs.get("persona", ""),
                "task_type": attrs.get("task_type", ""),
                "timestamp": attrs.get("timestamp", ""),
            })

        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return results

    # ── 查询：推荐下一步 ──────────────────────
    def suggest_next(self,
                     query: str,
                     top_k: int = 3) -> List[Dict]:
        """
        基于历史模式推荐下一步。
        逻辑：找相似任务→看它们的时序后继→返回最常见的
        """
        # 找相似任务
        related = self.find_related(query, top_k=10, min_similarity=0.3)
        if not related:
            return []

        # 收集所有时序后继
        successors = []
        for r in related:
            tid = r["task_id"]
            for _, nbr in self.graph.out_edges(tid):
                edge = self.graph.get_edge_data(tid, nbr)
                if edge.get("type") == "temporal_sequence":
                    n_attrs = self.graph.nodes[nbr]
                    successors.append({
                        "task_id": nbr,
                        "input_text": n_attrs.get("input_text", ""),
                        "persona": n_attrs.get("persona", ""),
                        "task_type": n_attrs.get("task_type", ""),
                        "from": r["input_text"][:40],
                        "timestamp": n_attrs.get("timestamp", ""),
                    })

        # 去重，返回最常见的
        seen = set()
        unique = []
        for s in successors:
            key = s["input_text"][:30]
            if key not in seen:
                seen.add(key)
                unique.append(s)

        unique.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return unique[:top_k]

    # ── 查询：发现高频模式 ─────────────────────
    def find_patterns(self,
                      min_freq: int = 3,
                      persona_filter: Optional[str] = None) -> List[Dict]:
        """
        发现高频任务模式。
        统计：(task_type → persona) 的出现频率
        """
        patterns = Counter()
        pattern_tasks = defaultdict(list)

        for node_id, attrs in self.graph.nodes(data=True):
            tt = attrs.get("task_type", "")
            p = attrs.get("persona", "")
            if persona_filter and p != persona_filter:
                continue

            key = f"{tt} → {p}"
            patterns[key] += 1
            pattern_tasks[key].append(attrs.get("input_text", ""))

        results = []
        for key, freq in patterns.most_common():
            if freq >= min_freq:
                tt, p = key.split(" → ", 1)
                tasks = pattern_tasks[key][:5]
                results.append({
                    "pattern": key,
                    "frequency": freq,
                    "task_type": tt,
                    "persona": p,
                    "examples": tasks,
                })

        return results

    # ── 查询：任务时间线 ─────────────────────
    def timeline(self,
                 hours: int = 24,
                 limit: int = 20) -> List[Dict]:
        """获取最近N小时的任务时间线"""
        cutoff = (datetime.datetime.now() - datetime.timedelta(hours=hours)).isoformat()

        nodes = []
        for node_id, attrs in self.graph.nodes(data=True):
            ts = attrs.get("timestamp", "")
            if ts >= cutoff:
                nodes.append({
                    "task_id": node_id,
                    "input_text": attrs.get("input_text", ""),
                    "persona": attrs.get("persona", ""),
                    "task_type": attrs.get("task_type", ""),
                    "success": attrs.get("success", True),
                    "audit_mark": attrs.get("audit_mark", "🟢"),
                    "timestamp": ts,
                })

        nodes.sort(key=lambda x: x["timestamp"], reverse=True)
        return nodes[:limit]

    # ── 统计 ──────────────────────────────────
    def stats(self) -> Dict:
        """图谱统计概览"""
        if not self.graph:
            return {"节点数": 0, "边数": 0, "状态": "空图谱"}

        edge_counts = Counter()
        for _, _, data in self.graph.edges(data=True):
            edge_counts[data.get("type", "unknown")] += 1

        persona_counts = Counter()
        task_type_counts = Counter()
        audit_marks = Counter()
        success_count = 0

        for _, attrs in self.graph.nodes(data=True):
            persona_counts[attrs.get("persona", "")] += 1
            task_type_counts[attrs.get("task_type", "")] += 1
            audit_marks[attrs.get("audit_mark", "🟢")] += 1
            if attrs.get("success", True):
                success_count += 1

        return {
            "节点数": len(self.graph),
            "边数": len(self.graph.edges),
            "成功率": f"{success_count/len(self.graph)*100:.1f}%" if self.graph else "N/A",
            "边类型分布": dict(edge_counts.most_common()),
            "人格分布": dict(persona_counts.most_common(10)),
            "任务类型分布": dict(task_type_counts.most_common()),
            "审计标记": dict(audit_marks),
            "图谱密度": f"{len(self.graph.edges)/max(len(self.graph)*(len(self.graph)-1),1):.4f}",
        }

    # ── 导出 Mermaid ──────────────────────────
    def export_mermaid(self, max_nodes: int = 50) -> str:
        """导出为 Mermaid 格式（可视化用）"""
        lines = ["graph LR"]
        nodes = list(self.graph.nodes(data=True))
        # 取最近的 max_nodes 个节点
        nodes.sort(key=lambda x: x[1].get("timestamp", ""), reverse=True)
        nodes = nodes[:max_nodes]
        node_ids = {n[0] for n in nodes}

        for nid, attrs in nodes:
            label = attrs.get("input_text", "")[:20].replace('"', "'")
            persona = attrs.get("persona", "")
            lines.append(f'    {nid}["{persona}: {label}"]')

        for u, v, data in self.graph.edges(data=True):
            if u in node_ids and v in node_ids:
                etype = data.get("type", "")[:10]
                lines.append(f"    {u} -->|{etype}| {v}")

        return "\n".join(lines)


# ============================================================
# 四、意图引擎集成钩子
# ============================================================

class IntentEngineHook:
    """
    意图引擎集成钩子。
    在意图引擎 阶段7 ROM固化 之后调用 add_task，
    在 阶段2 历史追溯 时调用 find_related 增强上下文。
    """

    def __init__(self, graph_engine: TaskGraphEngine = None):
        self.graph = graph_engine or TaskGraphEngine()

    def on_task_complete(self,
                         input_text: str,
                         task_type: str = "通用咨询",
                         persona: str = "P01诸葛亮",
                         success: bool = True,
                         emotion_score: float = 0.5,
                         response: str = "",
                         audit_mark: str = "🟢",
                         rom_hit: bool = False) -> str:
        """
        意图引擎处理完成后调用。
        将任务写入图谱，自动建边。
        返回 task_id。
        """
        return self.graph.add_task(
            input_text=input_text,
            task_type=task_type,
            persona=persona,
            success=success,
            emotion_score=emotion_score,
            response_summary=response[:200],
            audit_mark=audit_mark,
            rom_hit=rom_hit,
        )

    def enhance_context(self, input_text: str, top_k: int = 3) -> List[Dict]:
        """
        增强阶段2历史追溯。
        除了处理历史，还从图谱找语义相关任务。
        """
        return self.graph.find_related(input_text, top_k=top_k, min_similarity=0.3)

    def enhance_learning(self, min_freq: int = 3) -> List[Dict]:
        """
        增强阶段9自适应学习。
        从图谱发现高频模式。
        """
        return self.graph.find_patterns(min_freq=min_freq)


# ============================================================
# 五、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·任务关联图谱引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s add --input "健康检查全部服务" --persona P09孙思邈 --success
  %(prog)s related "系统巡检" -k 5
  %(prog)s suggest "部署上线"
  %(prog)s stats
  %(prog)s patterns --min-freq 3
  %(prog)s timeline --hours 24
  %(prog)s --hook-test "帮我检查一下服务器状态"
  %(prog)s --interactive
        """)

    sub = parser.add_subparsers(dest="command", help="子命令")

    # add
    p_add = sub.add_parser("add", help="添加任务节点")
    p_add.add_argument("--input", "-i", required=True, help="用户输入文本")
    p_add.add_argument("--type", "-t", default="通用咨询", help="任务类型")
    p_add.add_argument("--persona", "-p", default="P01诸葛亮", help="触发人格")
    p_add.add_argument("--success", action="store_true", default=True, help="是否成功")
    p_add.add_argument("--fail", action="store_true", help="标记失败")
    p_add.add_argument("--emotion", "-e", type=float, default=0.5, help="情绪分数")
    p_add.add_argument("--response", "-r", default="", help="响应摘要")
    p_add.add_argument("--audit", "-a", default="🟢", help="审计标记")

    # related
    p_rel = sub.add_parser("related", help="查找相关任务")
    p_rel.add_argument("query", help="查询文本")
    p_rel.add_argument("-k", type=int, default=5, help="返回数量")

    # suggest
    p_sug = sub.add_parser("suggest", help="推荐下一步")
    p_sug.add_argument("query", help="当前任务描述")

    # patterns
    p_pat = sub.add_parser("patterns", help="发现高频模式")
    p_pat.add_argument("--min-freq", type=int, default=3, help="最小频次")
    p_pat.add_argument("--persona", default=None, help="按人格过滤")

    # stats
    sub.add_parser("stats", help="图谱统计")

    # timeline
    p_tl = sub.add_parser("timeline", help="任务时间线")
    p_tl.add_argument("--hours", type=int, default=24, help="最近N小时")
    p_tl.add_argument("--limit", type=int, default=20, help="最大返回数")

    # export
    p_exp = sub.add_parser("export", help="导出 Mermaid")
    p_exp.add_argument("--max-nodes", type=int, default=50, help="最大节点数")

    # graph-related
    p_gr = sub.add_parser("graph-related", help="基于图结构查找关联（非纯语义）")
    p_gr.add_argument("task_id", help="任务ID")
    p_gr.add_argument("--depth", type=int, default=2, help="遍历深度")
    p_gr.add_argument("--edge-types", nargs="*", default=None, help="边类型过滤")

    # hook-test
    p_ht = sub.add_parser("hook-test", help="测试意图引擎集成钩子")
    p_ht.add_argument("input_text", help="模拟用户输入")

    # interactive
    parser.add_argument("--interactive", "-I", action="store_true", help="交互模式")

    args = parser.parse_args()
    engine = TaskGraphEngine()

    if args.command == "add":
        success = False if getattr(args, "fail", False) else args.success
        tid = engine.add_task(
            input_text=args.input,
            task_type=args.type,
            persona=args.persona,
            success=success,
            emotion_score=args.emotion,
            response_summary=args.response,
            audit_mark=args.audit,
        )
        print(f"✅ 节点已添加: {tid}")
        print(f"   DNA: {engine.graph.nodes[tid].get('dna','')}")

    elif args.command == "related":
        results = engine.find_related(args.query, top_k=args.k)
        if not results:
            print("📭 未找到相关任务")
        else:
            print(f"🔗 找到 {len(results)} 个相关任务：\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. [{r['similarity']:.0%}] {r['persona']} | {r['input_text'][:60]}")
                print(f"     {r['timestamp'][:19]} | {'🟢' if r['success'] else '🔴'} | {r['task_type']}")
                print()

    elif args.command == "suggest":
        results = engine.suggest_next(args.query)
        if not results:
            print("📭 暂无推荐（图谱数据不足或无明显模式）")
        else:
            print(f"💡 基于历史模式，推荐下一步：\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['persona']} | {r['input_text'][:60]}")
                print(f"     来源: ...→{r['from']}")

    elif args.command == "patterns":
        results = engine.find_patterns(
            min_freq=args.min_freq,
            persona_filter=getattr(args, "persona", None)
        )
        if not results:
            print(f"📭 未发现频率≥{args.min_freq}的模式")
        else:
            print(f"📊 高频任务模式（频率≥{args.min_freq}）：\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. [×{r['frequency']}] {r['pattern']}")
                for ex in r['examples'][:3]:
                    print(f"     └ {ex[:60]}")
                print()

    elif args.command == "stats":
        s = engine.stats()
        print(f"📊 任务关联图谱统计\n{'='*40}")
        for k, v in s.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            else:
                print(f"{k}: {v}")

    elif args.command == "timeline":
        results = engine.timeline(hours=args.hours, limit=args.limit)
        if not results:
            print("📭 该时段无任务记录")
        else:
            print(f"⏱️ 最近{args.hours}小时任务时间线：\n")
            for i, r in enumerate(results, 1):
                ts = r['timestamp'][:19] if r['timestamp'] else ''
                print(f"  {i:2d}. {ts} | {r['audit_mark']} | {r['persona']}")
                print(f"      {r['input_text'][:70]}")
                print()

    elif args.command == "export":
        mermaid = engine.export_mermaid(max_nodes=args.max_nodes)
        print(mermaid)

    elif args.command == "graph-related":
        results = engine.find_graph_related(
            args.task_id,
            max_depth=args.depth,
            edge_types=args.edge_types,
        )
        if not results:
            print(f"📭 任务 {args.task_id} 无图结构关联")
        else:
            print(f"🔗 图结构关联（深度={args.depth}）：\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['persona']} | {r['task_type']} | {r['input_text'][:60]}")

    elif args.command == "hook-test":
        hook = IntentEngineHook(engine)
        tid = hook.on_task_complete(
            input_text=args.input_text,
            task_type="系统操作",
            persona="P09孙思邈",
            success=True,
        )
        related = hook.enhance_context(args.input_text)
        print(f"✅ 集成测试完成")
        print(f"   任务ID: {tid}")
        print(f"   关联任务: {len(related)} 个")
        for r in related:
            print(f"     - [{r['similarity']:.0%}] {r['input_text'][:50]}")

    elif args.interactive:
        print("\n" + "=" * 50)
        print("🐉 龍魂·任务关联图谱引擎 v1.0")
        print("=" * 50)
        print("命令: add <任务> | rel <查询> | sug <当前> | stats")
        print("      pat [频次] | tl [小时] | q 退出")
        print("=" * 50 + "\n")

        n_added = 0
        while True:
            try:
                cmd = input("📊 图谱> ").strip()
                if not cmd:
                    continue
                parts = cmd.split(maxsplit=1)
                action = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if action == "q":
                    break
                elif action == "add":
                    tid = engine.add_task(input_text=arg, task_type="交互输入")
                    n_added += 1
                    print(f"  ✅ {tid}")
                elif action == "rel":
                    results = engine.find_related(arg)
                    for i, r in enumerate(results, 1):
                        print(f"  {i}. [{r['similarity']:.0%}] {r['input_text'][:50]}")
                elif action == "sug":
                    results = engine.suggest_next(arg)
                    for i, r in enumerate(results, 1):
                        print(f"  💡{i}. {r['input_text'][:50]}")
                elif action == "stats":
                    s = engine.stats()
                    for k, v in s.items():
                        print(f"  {k}: {v}")
                elif action == "pat":
                    min_f = int(arg) if arg.isdigit() else 3
                    for r in engine.find_patterns(min_freq=min_f):
                        print(f"  [×{r['frequency']}] {r['pattern']}")
                elif action == "tl":
                    hours = int(arg) if arg.isdigit() else 24
                    for r in engine.timeline(hours=hours):
                        print(f"  {r['timestamp'][:19]} | {r['persona']} | {r['input_text'][:50]}")
                else:
                    # 默认当作添加任务
                    tid = engine.add_task(input_text=cmd, task_type="交互输入")
                    n_added += 1
                    print(f"  ✅ {tid} (已添加 {n_added} 个节点)")
            except KeyboardInterrupt:
                break

        print(f"\n👋 本次添加 {n_added} 个节点，图谱已保存。")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
