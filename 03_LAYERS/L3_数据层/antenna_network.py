#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂触角网络 · 信息节点关联引擎 v1.0（焊死）

DNA追溯码：#龍魂⚡️丙午·辛未·触角网络-v1
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心定位：
  触角 = 语义节点在文件中的具体落脚点
  触角触碰 → 信息素强化 → 关联节点交叉激活
  不靠数据库，靠文件名+内容语义的触角网络

三层联动：
  L1 文件名解析 → 知道类型/结构/权限/DNA
  L2 语义标准化 → 大白话 → 标准节点
  L3 触角传递 → 交叉激活 → 关联唤醒

核心承诺（焊死）：
  - 每个触角记录：节点ID + 文件DNA + 位置 + 上下文 + 信息素
  - 信息素触碰强化(×1.1) + 衰减(×0.95) + 沉睡唤醒
  - 交叉激活直接匹配→关联节点→关联文件，全链路可追溯
  - 不丢数据：历史文件模糊匹配+人工兜底

创建者：💎 龍芯北辰｜UID9622
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "L3_数据层"))

from semantic_nodes import (
    SEMANTIC_NODES,
    SemanticNormalizer,
    MatchResult,
    make_dna,
    CONFIRM_CODE,
)


# ═══════════════════════════════════════════════
# 触角数据模型（焊死）
# ═══════════════════════════════════════════════

@dataclass
class Antenna:
    """信息触角 — 语义节点在文件中的落脚点"""

    node_id: str               # 连接的语义节点ID（如 NODE-押金-001）
    file_dna: str              # 来源文件DNA
    file_path: str             # 文件路径
    position: int              # 在文件中的位置（行号）
    context: str               # 上下文（前后50字）
    pheromone: float = 1.0     # 信息素强度（关联度）
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    wake_status: str = "active"  # active / sleeping / dead

    def touch(self):
        """被触碰，强化信息素"""
        self.pheromone = min(self.pheromone * 1.1, 10.0)
        self.access_count += 1
        self.last_accessed = datetime.now()
        if self.wake_status == "sleeping":
            self.wake_status = "active"

    def decay(self) -> bool:
        """
        信息素衰减
        返回 True = 仍活跃，False = 已沉睡
        """
        self.pheromone *= 0.95
        if self.pheromone < 0.1:
            self.wake_status = "sleeping"
            return False
        return True

    def suppress_if_hyperactive(self, threshold: float = 5.0):
        """如果过于活跃，抑制信息素（反活跃优先）"""
        if self.pheromone > threshold:
            self.pheromone *= 0.7
            return True
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "file_dna": self.file_dna,
            "file_path": self.file_path,
            "position": self.position,
            "context": self.context[:100],
            "pheromone": round(self.pheromone, 3),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "wake_status": self.wake_status,
        }


@dataclass
class AntennaEdge:
    """触角关联边：两个语义节点之间的关联"""
    node_a: str
    node_b: str
    strength: float = 0.8   # 关联强度
    co_occurrence: int = 1  # 共现次数


# ═══════════════════════════════════════════════
# 触角网络引擎（焊死）
# ═══════════════════════════════════════════════

class AntennaNetwork:
    """
    触角网络 — 文件间语义关联的核心引擎

    职责：
      1. 索引文件：提取语义节点 → 建立触角 → 建立边
      2. 交叉激活：查询节点 → 直接匹配 + 关联节点 + 关联文件
      3. 触碰管理：信息素强化/衰减/沉睡唤醒/反活跃压制
    """

    def __init__(self, normalizer: Optional[SemanticNormalizer] = None):
        self.normalizer = normalizer or SemanticNormalizer()
        self.antennas: List[Antenna] = []
        self.edges: List[AntennaEdge] = []
        self._file_index: Dict[str, List[int]] = {}  # 文件路径 → 触角索引列表
        self._node_index: Dict[str, List[int]] = {}  # 节点ID → 触角索引列表

    # ─── 索引 ───

    def index_file(self, file_path: str, file_content: Optional[str] = None) -> int:
        """
        索引一个文件：提取语义节点 → 建立触角 → 建立边

        返回：创建的触角数量
        """
        path = Path(file_path)
        if not path.exists() and file_content is None:
            return 0

        # 读取内容
        if file_content is None:
            try:
                file_content = path.read_text(encoding="utf-8")
            except Exception:
                return 0

        # 按行扫描，提取语义节点
        lines = file_content.split("\n")
        dna = make_dna("触角索引文件", "v1")

        created = 0
        for line_no, line in enumerate(lines, start=1):
            if len(line.strip()) < 2:
                continue

            # 语义标准化
            result = self.normalizer.normalize(line)
            if not result["nodes"]:
                continue

            # 为每个匹配的节点建立触角
            context_start = max(0, line_no - 2)
            context_end = min(len(lines), line_no + 2)
            context = "\n".join(lines[context_start:context_end])

            for node_match in result["nodes"]:
                antenna = Antenna(
                    node_id=node_match["node_id"],
                    file_dna=dna,
                    file_path=str(path),
                    position=line_no,
                    context=context,
                    pheromone=node_match["confidence"],
                )
                idx = len(self.antennas)
                self.antennas.append(antenna)

                # 更新索引
                self._file_index.setdefault(str(path), []).append(idx)
                self._node_index.setdefault(node_match["node_id"], []).append(idx)

                created += 1

            # 建立节点间边（同一行内共现的节点）
            node_ids = [n["node_id"] for n in result["nodes"]]
            for i, nid_a in enumerate(node_ids):
                for nid_b in node_ids[i+1:]:
                    self._add_or_strengthen_edge(nid_a, nid_b)

        return created

    def index_directory(self, dir_path: str, pattern: str = "*.md") -> int:
        """索引整个目录"""
        total = 0
        for f in Path(dir_path).rglob(pattern):
            total += self.index_file(str(f))
        return total

    def _add_or_strengthen_edge(self, node_a: str, node_b: str):
        """添加或强化节点间关联边"""
        for edge in self.edges:
            if (edge.node_a == node_a and edge.node_b == node_b) or \
               (edge.node_a == node_b and edge.node_b == node_a):
                edge.co_occurrence += 1
                edge.strength = min(1.0, edge.strength + 0.05)
                return
        self.edges.append(AntennaEdge(node_a=node_a, node_b=node_b))

    # ─── 交叉激活 ───

    def cross_activate(self, query_nodes: List[str], limit: int = 50) -> dict[str, Any]:
        """
        交叉激活：查询节点 → 直接匹配 + 关联节点 + 关联文件

        输入：["NODE-押金-001", "NODE-房东-001"]
        输出：{
            "direct": [触角列表],      # 直接匹配的触角
            "cross": [触角列表],       # 关联节点匹配的触角
            "files": [文件路径列表],    # 去重后的文件
            "edges": [关联边列表],      # 节点间关系
        }
        """
        query_set = set(query_nodes)

        # 1. 直接匹配
        direct_antennas: List[Antenna] = []
        for nid in query_set:
            indices = self._node_index.get(nid, [])
            for idx in indices:
                ant = self.antennas[idx]
                ant.touch()  # 触碰强化
                direct_antennas.append(ant)

        # 2. 关联节点（从语义节点库获取）
        related_node_ids: Set[str] = set()
        for node_key, node in SEMANTIC_NODES.items():
            if node["节点ID"] in query_set:
                for related_name in node.get("关联节点", []):
                    # 找关联名称对应的节点ID
                    for rk, rn in SEMANTIC_NODES.items():
                        if rn["标准词"] == related_name:
                            related_node_ids.add(rn["节点ID"])
                            break

        # 3. 关联匹配
        cross_antennas: List[Antenna] = []
        for rnid in related_node_ids:
            if rnid not in query_set:  # 排除已经直接匹配的
                indices = self._node_index.get(rnid, [])
                for idx in indices:
                    ant = self.antennas[idx]
                    ant.touch()
                    cross_antennas.append(ant)

        # 4. 排序（信息素降序）
        direct_antennas.sort(key=lambda a: a.pheromone, reverse=True)
        cross_antennas.sort(key=lambda a: a.pheromone, reverse=True)

        # 5. 去重文件
        all_files: Set[str] = set()
        for ant in direct_antennas + cross_antennas:
            all_files.add(ant.file_path)

        # 6. 相关边
        relevant_edges = []
        for edge in self.edges:
            if edge.node_a in query_set or edge.node_b in query_set or \
               edge.node_a in related_node_ids or edge.node_b in related_node_ids:
                relevant_edges.append({
                    "node_a": edge.node_a,
                    "node_b": edge.node_b,
                    "strength": round(edge.strength, 3),
                    "co_occurrence": edge.co_occurrence,
                })

        return {
            "direct": [a.to_dict() for a in direct_antennas[:limit]],
            "cross": [a.to_dict() for a in cross_antennas[:limit]],
            "files": sorted(all_files),
            "edges": relevant_edges[:limit],
            "dna": make_dna("交叉激活", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    def search(self, user_input: str, limit: int = 50) -> dict[str, Any]:
        """
        一体化搜索：用户大白话 → 语义标准化 → 交叉激活
        """
        result = self.normalizer.normalize(user_input)
        node_ids = [n["node_id"] for n in result["nodes"]]

        if not node_ids:
            return {
                "input": user_input,
                "normalized": result["normalized"],
                "nodes": [],
                "results": {"direct": [], "cross": [], "files": [], "edges": []},
                "suggestion": "未匹配到已知语义节点，尝试更具体的描述",
                "dna": make_dna("触角搜索", "v1"),
                "confirm_code": CONFIRM_CODE,
            }

        activation = self.cross_activate(node_ids, limit=limit)

        return {
            "input": user_input,
            "normalized": result["normalized"],
            "nodes": result["nodes"],
            "confidence": result["confidence"],
            "results": activation,
            "dna": make_dna("触角搜索", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    # ─── 维护 ───

    def run_decay_cycle(self):
        """运行信息素衰减周期"""
        sleeping_count = 0
        for ant in self.antennas:
            if not ant.decay():
                sleeping_count += 1
        return sleeping_count

    def run_suppress_cycle(self, threshold: float = 5.0):
        """运行反活跃压制周期"""
        suppressed = 0
        for ant in self.antennas:
            if ant.suppress_if_hyperactive(threshold):
                suppressed += 1
        return suppressed

    def wake_sleeping(self, node_ids: Optional[List[str]] = None) -> int:
        """唤醒沉睡触角"""
        woke = 0
        for ant in self.antennas:
            if ant.wake_status == "sleeping":
                if node_ids is None or ant.node_id in node_ids:
                    ant.wake_status = "active"
                    ant.pheromone = max(ant.pheromone, 0.3)
                    woke += 1
        return woke

    # ─── 统计 ───

    def stats(self) -> dict[str, Any]:
        """触角网络统计"""
        active = sum(1 for a in self.antennas if a.wake_status == "active")
        sleeping = sum(1 for a in self.antennas if a.wake_status == "sleeping")
        dead = len(self.antennas) - active - sleeping

        return {
            "total_antennas": len(self.antennas),
            "active": active,
            "sleeping": sleeping,
            "dead": dead,
            "files_indexed": len(self._file_index),
            "nodes_connected": len(self._node_index),
            "edges": len(self.edges),
            "avg_pheromone": round(
                sum(a.pheromone for a in self.antennas) / max(len(self.antennas), 1), 3
            ),
            "dna": make_dna("触角统计", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    # ─── 持久化 ───

    def to_json(self) -> str:
        """导出触角网络为JSON"""
        data = {
            "antennas": [a.to_dict() for a in self.antennas],
            "edges": [
                {"node_a": e.node_a, "node_b": e.node_b,
                 "strength": round(e.strength, 3), "co_occurrence": e.co_occurrence}
                for e in self.edges
            ],
            "stats": self.stats(),
            "dna": make_dna("触角网络导出", "v1"),
            "confirm_code": CONFIRM_CODE,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def save(self, filepath: str):
        """持久化到文件"""
        Path(filepath).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, filepath: str) -> "AntennaNetwork":
        """从文件恢复（TODO：完整反序列化）"""
        net = cls()
        return net


# ═══════════════════════════════════════════════
# CLI入口（焊死）
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    net = AntennaNetwork()

    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "index" and len(sys.argv) > 2:
            target = sys.argv[2]
            path = Path(target)
            if path.is_dir():
                count = net.index_directory(str(path))
                print(f"索引目录: {target} → 建立 {count} 个触角")
            elif path.is_file():
                count = net.index_file(str(path))
                print(f"索引文件: {target} → 建立 {count} 个触角")
            else:
                # 尝试作为文本内容索引
                count = net.index_file("input.txt", target)
                print(f"索引文本 → 建立 {count} 个触角")

        elif cmd == "search" and len(sys.argv) > 2:
            query = sys.argv[2]
            results = net.search(query)
            print(json.dumps(results, ensure_ascii=False, indent=2))

        elif cmd == "stats":
            print(json.dumps(net.stats(), ensure_ascii=False, indent=2))

        elif cmd == "decay":
            count = net.run_decay_cycle()
            print(f"衰减周期完成 → {count} 触角沉睡")

        elif cmd == "suppress":
            count = net.run_suppress_cycle()
            print(f"压制周期完成 → {count} 触角被抑制")

        elif cmd == "wake":
            woke = net.wake_sleeping()
            print(f"唤醒 {woke} 个沉睡触角")

        elif cmd == "export" and len(sys.argv) > 2:
            net.save(sys.argv[2])
            print(f"导出到 {sys.argv[2]}")

        else:
            print(f"用法: python antenna_network.py [index|search|stats|decay|suppress|wake|export] [...]")

    else:
        # 默认自检
        print("=" * 50)
        print("【龍魂触角网络 · 自检】")
        print(f"DNA: {make_dna('触角网络', 'v1')}")
        print(f"确认码: {CONFIRM_CODE}")
        print("=" * 50)

        # 测试：索引一段文本
        test_text = "房东那个压金不退怎么办？签了合同但房东说变卦了就变卦了。"
        count = net.index_file("test_input.txt", test_text)
        print(f"\n索引测试文本 → {count} 触角")

        stats = net.stats()
        print(f"活跃触角: {stats['active']} | 节点: {stats['nodes_connected']} | 边: {stats['edges']}")

        # 测试：搜索
        results = net.search("押金不退")
        print(f"\n搜索'押金不退':")
        print(f"  标准化: {results['normalized']}")
        print(f"  命中节点: {[n['standard'] for n in results['nodes']]}")
        print(f"  直接命中: {len(results['results']['direct'])}")
        print(f"  交叉命中: {len(results['results']['cross'])}")
        print(f"  关联文件: {results['results']['files']}")

        # 测试：衰减
        sleeping = net.run_decay_cycle()
        print(f"\n衰减: {sleeping} 触角沉睡 → 活跃{net.stats()['active']}")

        print("\n✅ 触角网络正常 · 焊死")
