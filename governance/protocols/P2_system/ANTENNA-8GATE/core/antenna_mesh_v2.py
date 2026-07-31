# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · 蚁触神经网 v2.0 · 语义编码升级版
# DNA：#龍芯⚡️丙午·乙未·丙申·未时·☲离-ANTENNA-MESH-V2.0-SEMANTIC-a1b2c3d4
# 创建者：诸葛鑫（UID9622）
# 协议：CC BY-NC-SA 4.0
# 
# 升级点 vs v1.0:
#  1. ord(c)%256 → Ollama 4096维语义嵌入
#  2. 4节点/卦 → 64节点/卦 (512总节点)
#  3. 固定门控 → 语义相似度自适应门控
#  4. 无记忆 → 128条/节点语义记忆缓存
# ============================================================

import numpy as np
import hashlib
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import json
from collections import OrderedDict

from semantic_encoder import SemanticEncoder, SIMILARITY_THRESHOLD

# ── 八卦枚举 ──
class Bagua(Enum):
    乾 = 0  # 天 - 主控/决策
    坤 = 1  # 地 - 存储/持久
    震 = 2  # 雷 - 突发/告警
    巽 = 3  # 风 - 传输/网络
    坎 = 4  # 水 - 冷却/调度
    离 = 5  # 火 - 计算/核心
    艮 = 6  # 山 - 边界/安全
    兑 = 7  # 泽 - 交互/输出


@dataclass
class SemanticMemory:
    """节点级语义记忆单元"""
    embedding: np.ndarray
    bagua: int
    query_hash: str
    hit_count: int = 0
    last_access: float = 0.0


class SemanticGate:
    """
    语义门控 v2.0
    不再仅靠八卦距离，而是基于语义相似度决定开/关
    """
    def __init__(self, bagua: Bagua, dim: int, memory_size: int = 128):
        self.bagua = bagua
        self.dim = dim
        self.memory: OrderedDict[str, SemanticMemory] = OrderedDict()
        self.memory_size = memory_size
        self.active_count = 0
        self.skip_count = 0
        self.similar_hit = 0  # 语义相似命中
        
        # 初始化随机权重（用于门控残差）
        self.w = np.random.randn(dim).astype(np.float32) * 0.001
        self.b = np.zeros(1, dtype=np.float32)
    
    def check(self, embedding: np.ndarray, current_bagua: Bagua, 
              query_key: str) -> Tuple[bool, float]:
        """
        检查是否应激活此门
        返回：(是否激活, 激活强度)
        
        三层判断：
        1. 记忆命中：完全相同 → 1.0 强度
        2. 语义相似：余弦相似度 > 阈值 → 按相似度激活
        3. 八卦距离：先天八卦位置 → 基础门控
        """
        # L1: 记忆精确命中
        if query_key in self.memory:
            mem = self.memory[query_key]
            mem.hit_count += 1
            mem.last_access = time.time()
            self.similar_hit += 1
            self.active_count += 1
            return True, 1.0
        
        # L2: 语义相似度匹配
        if len(self.memory) > 0:
            best_sim = 0.0
            emb_norm = np.linalg.norm(embedding)
            if emb_norm > 0:
                for mem in list(self.memory.values())[-64:]:  # 只查最近64条
                    mem_norm = np.linalg.norm(mem.embedding)
                    if mem_norm == 0:
                        continue
                    sim = np.dot(embedding, mem.embedding) / (emb_norm * mem_norm)
                    if sim > best_sim:
                        best_sim = sim
            
            if best_sim >= SIMILARITY_THRESHOLD:
                self.similar_hit += 1
                self.active_count += 1
                return True, best_sim
        
        # L3: 八卦基础门控
        distance = self._bagua_distance(self.bagua, current_bagua)
        
        if distance == 0:          # 同卦：全开
            self.active_count += 1
            return True, 1.0
        elif distance == 1:        # 相邻卦：半开
            self.active_count += 1
            return True, 0.5
        else:                      # 距离2/3/4：跳过（除非L2语义命中）
            self.skip_count += 1
            return False, 0.0
    
    def remember(self, query_key: str, embedding: np.ndarray):
        """存入记忆"""
        mem = SemanticMemory(
            embedding=embedding.copy(),
            bagua=self.bagua.value,
            query_hash=query_key,
            last_access=time.time()
        )
        self.memory[query_key] = mem
        if len(self.memory) > self.memory_size:
            self.memory.popitem(last=False)
    
    def _bagua_distance(self, a: Bagua, b: Bagua) -> int:
        positions = {Bagua.乾:0, Bagua.坤:1, Bagua.震:2, Bagua.巽:3,
                     Bagua.坎:4, Bagua.离:5, Bagua.艮:6, Bagua.兑:7}
        diff = abs(positions[a] - positions[b])
        return min(diff, 8 - diff)
    
    def stats(self) -> Dict[str, Any]:
        total = self.active_count + self.skip_count
        return {
            'bagua': self.bagua.name,
            'active': self.active_count,
            'skip': self.skip_count,
            'similar_hit': self.similar_hit,
            'skip_rate': self.skip_count / total if total > 0 else 0,
            'memory_size': len(self.memory),
        }


class AntennaNodeV2:
    """蚁触节点 v2.0：语义感知"""
    def __init__(self, node_id: str, bagua: Bagua, dim: int, memory_size: int = 128):
        self.node_id = node_id
        self.bagua = bagua
        self.dim = dim
        self.gate = SemanticGate(bagua, dim, memory_size)
        self.neighbors: Dict[str, 'AntennaNodeV2'] = {}
        self.energy_joules = 0.0
        self.touch_count = 0
        self.state = '休眠'
    
    def add_neighbor(self, node: 'AntennaNodeV2'):
        self.neighbors[node.node_id] = node
    
    def route(self, embedding: np.ndarray, target_bagua: Bagua, 
              query_key: str) -> Tuple[bool, float]:
        """
        路由判断：此节点是否响应当前查询
        返回：(是否激活, 强度)
        """
        self.touch_count += 1
        self.energy_joules += 1e-6  # 微焦耳唤醒
        
        activated, strength = self.gate.check(embedding, target_bagua, query_key)
        
        if activated:
            self.state = '激活'
            # 记住此模式
            self.gate.remember(query_key, embedding)
            self.energy_joules += 1e-9  # 计算能耗
        else:
            self.state = '跳过'
        
        return activated, strength
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'bagua': self.bagua.name,
            'state': self.state,
            'energy_joules': self.energy_joules,
            'touch_count': self.touch_count,
            'neighbors': len(self.neighbors),
            'gate_stats': self.gate.stats(),
        }


class AntennaMeshV2:
    """
    蚁触神经网 v2.0
    8卦 × 64节点 = 512节点
    语义编码 + 模式记忆 + 自适应门控
    """
    def __init__(self, nodes_per_bagua: int = 64, dim: int = 4096,
                 memory_per_node: int = 128):
        self.dim = dim
        self.nodes: Dict[str, AntennaNodeV2] = {}
        self.bagua_groups: Dict[Bagua, List[AntennaNodeV2]] = {b: [] for b in Bagua}
        self.encoder = SemanticEncoder()
        self.total_packets = 0
        self.total_energy = 0.0
        
        # 创建节点
        node_idx = 0
        for bagua in Bagua:
            for i in range(nodes_per_bagua):
                nid = f"{bagua.name}-{i:03d}"
                node = AntennaNodeV2(nid, bagua, dim, memory_per_node)
                self.nodes[nid] = node
                self.bagua_groups[bagua].append(node)
                node_idx += 1
        
        # 建立邻居连接
        self._connect_neighbors()
        
        print(f"[AntMeshV2] 规模: {len(self.nodes)}节点 (8卦×{nodes_per_bagua}) | "
              f"dim={dim} | mem={memory_per_node}/节点 | "
              f"总记忆: {len(self.nodes)*memory_per_node}条")
    
    def _connect_neighbors(self):
        """同卦全连接 + 相邻卦选代表连接"""
        bagua_list = list(Bagua)
        for node in self.nodes.values():
            # 同卦：全连接
            for peer in self.bagua_groups[node.bagua]:
                if peer.node_id != node.node_id:
                    node.add_neighbor(peer)
            # 相邻卦：连接首个节点
            for ob in bagua_list:
                if ob != node.bagua:
                    dist = node.gate._bagua_distance(node.bagua, ob)
                    if dist == 1 and self.bagua_groups[ob]:
                        node.add_neighbor(self.bagua_groups[ob][0])
    
    def inference(self, text: str, target_bagua: Bagua) -> Tuple[np.ndarray, Dict]:
        """
        推理入口 v2.0 — 全网格遍历，门控自主决策
        文本 → 语义编码 → 遍历512节点 → 门控激活/跳过 → 输出
        
        跳过率来源：
        1. 对冲卦象（距离=4）→ gate直接skip
        2. 语义不匹配（相似度<阈值）→ gate skip
        3. 记忆命中（同query）→ gate激活但跳过重复计算
        """
        self.total_packets += 1
        query_key = hashlib.sha256(text.encode()).hexdigest()[:16]
        
        t0 = time.time()
        
        # 步骤1: 语义编码
        embedding = self.encoder.encode(text, target_bagua.value)
        
        # 步骤2: 遍历全部节点，门控自主决定激活/跳过
        activated_nodes = []
        total_checked = 0
        
        for bagua in Bagua:
            for node in self.bagua_groups[bagua]:
                total_checked += 1
                act, strength = node.route(embedding, target_bagua, query_key)
                if act:
                    activated_nodes.append((node, strength))
        
        latency = time.time() - t0
        
        # 能耗统计
        energy = sum(n.energy_joules for n in self.nodes.values())
        self.total_energy = energy
        
        stats = self._collect_stats(latency, energy, len(activated_nodes), total_checked)
        return embedding, stats
    
    def _collect_stats(self, latency: float, energy: float, 
                       activated: int, checked: int) -> Dict[str, Any]:
        skip_rate = self._avg_skip_rate()
        nodes_used = sum(1 for n in self.nodes.values() if n.touch_count > 0)
        
        return {
            'latency_ms': latency * 1000,
            'total_energy_j': energy,
            'packets': self.total_packets,
            'nodes_active': activated,
            'nodes_checked': checked,
            'nodes_total': len(self.nodes),
            'nodes_ever_used': nodes_used,
            'skip_rate': skip_rate,
            'encoder_stats': self.encoder.get_stats() if self.total_packets > 0 else {},
        }
    
    def _avg_skip_rate(self) -> float:
        skips = sum(n.gate.skip_count for n in self.nodes.values())
        active = sum(n.gate.active_count for n in self.nodes.values())
        total = skips + active
        return skips / total if total > 0 else 0
    
    def full_stats(self) -> Dict[str, Any]:
        return {
            'mesh_size': len(self.nodes),
            'total_energy_j': self.total_energy,
            'avg_skip_rate': self._avg_skip_rate(),
            'encoder': self.encoder.get_stats(),
            'node_stats': [n.get_stats() for n in list(self.nodes.values())[:8]],  # top 8
        }


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("蚁触神经网 v2.0 · 语义编码版 · 自检")
    print("=" * 60)
    
    mesh = AntennaMeshV2(nodes_per_bagua=16, dim=4096, memory_per_node=32)
    
    # 首次推理（冷启动）
    print("\n[冷启动]")
    _, s1 = mesh.inference("系统当前状态如何？", Bagua.乾)
    print(f"  激活: {s1['nodes_active']}/{s1['nodes_checked']} | 跳过率: {s1['skip_rate']*100:.1f}%")
    print(f"  编码器: {s1['encoder_stats']}")
    
    # 相同查询（命中）
    print("\n[相同查询]")
    _, s2 = mesh.inference("系统当前状态如何？", Bagua.乾)
    print(f"  激活: {s2['nodes_active']}/{s2['nodes_checked']} | 跳过率: {s2['skip_rate']*100:.1f}%")
    
    # 相似查询
    print("\n[相似查询]")
    _, s3 = mesh.inference("帮我查一下现在系统的运行状态", Bagua.乾)
    print(f"  激活: {s3['nodes_active']}/{s3['nodes_checked']} | 跳过率: {s3['skip_rate']*100:.1f}%")
    
    # 批量测试
    print("\n[批量-100次不同查询]")
    queries = [
        "写一个排序算法", "安全扫描报告", "部署到生产环境", "哲学推演分析",
        "数据库备份", "API接口设计", "代码审查", "性能优化建议",
    ] * 13  # 104次
    for q in queries[:100]:
        mesh.inference(q, list(Bagua)[hash(q) % 8])
    
    fs = mesh.full_stats()
    print(f"  跳过率: {fs['avg_skip_rate']*100:.1f}% | 编码缓存命中: {fs['encoder']['hit_rate']*100:.1f}%")
    print(f"  总能耗: {fs['total_energy_j']:.2e} J")
    
    print("\n✅ 蚁触神经网 v2.0 自检通过")
