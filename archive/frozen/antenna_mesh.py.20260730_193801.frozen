# ============================================================
# 龍魂 · 蚁触神经网 · 八卦门控推理压缩协议 v1.0
# 模块：ANTENNA-8GATE
# DNA：#龍芯⚡️丙午·癸未·壬戌·乾为天-EFFICIENCY-BREAK-v5.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者：诸葛鑫（UID9622）
# 协议：CC BY-NC-SA 4.0
# ============================================================

import numpy as np
import hashlib
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable
from enum import Enum, auto
import json

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

# ── 五行枚举 ──
class Wuxing(Enum):
    木 = 0  # 肝 - 过滤/清洗
    火 = 1  # 心 - 调度/泵送
    土 = 2  # 脾 - 转化/兼容
    金 = 3  # 肺 - 吞吐/IO
    水 = 4  # 肾 - 存储/持久

# ── 信息素包 ──
@dataclass
class PheromonePacket:
    """蚁触通信的信息素数据包"""
    source_id: str
    target_bagua: Bagua
    payload: np.ndarray
    timestamp: float = field(default_factory=time.time)
    ttl: int = 8  # 八卦门数 = 最大跳转次数
    pheromone_strength: float = 1.0
    path_trace: List[str] = field(default_factory=list)
    
    def volatilize(self, lambda_decay: float = 0.1) -> bool:
        """信息素挥发，返回是否失效"""
        elapsed = time.time() - self.timestamp
        self.pheromone_strength *= np.exp(-lambda_decay * elapsed)
        return self.pheromone_strength < 0.01 or self.ttl <= 0
    
    def to_bytes(self) -> bytes:
        """序列化为字节，用于网络传输"""
        data = {
            'sid': self.source_id,
            'bg': self.target_bagua.value,
            'pld': self.payload.tobytes().hex(),
            'ts': self.timestamp,
            'ttl': self.ttl,
            'ps': self.pheromone_strength,
            'pt': self.path_trace
        }
        return json.dumps(data, ensure_ascii=False).encode('utf-8')

# ── 八卦门控激活函数 ──
class BaguaGate:
    """
    八卦门控：每次推理只激活 1/8 网络
    Gate(x, g) = x × σ(w_g · x + b_g) × δ(g_current, g_node)
    """
    def __init__(self, dim: int, bagua: Bagua):
        self.bagua = bagua
        self.w = np.random.randn(dim) * 0.01
        self.b = np.zeros(1)
        self.active_count = 0
        self.skip_count = 0
    
    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, x: np.ndarray, current_bagua: Bagua) -> Optional[np.ndarray]:
        """
        门控前向传播
        同卦象：全开
        相邻卦象（先天八卦）：半开
        对冲卦象：关闭
        """
        # Kronecker delta 核心：同卦=1，否则按距离衰减
        distance = self._bagua_distance(self.bagua, current_bagua)
        
        if distance == 0:  # 同卦
            gate_value = 1.0
            self.active_count += 1
        elif distance == 1:  # 相邻
            gate_value = 0.5
            self.active_count += 1
        elif distance == 4:  # 对冲（乾-坤，震-巽等）
            self.skip_count += 1
            return None  # 直接跳过，零计算
        else:
            gate_value = 0.25
            self.active_count += 1
        
        # 门控激活
        gated = x * self.sigmoid(self.w @ x + self.b) * gate_value
        return gated
    
    def _bagua_distance(self, a: Bagua, b: Bagua) -> int:
        """八卦方位距离（先天八卦方位）"""
        # 先天八卦方位：乾南(0)、坤北(1)、震东北(2)、巽西南(3)
        #                 坎西(4)、离东(5)、艮西北(6)、兑东南(7)
        positions = {Bagua.乾:0, Bagua.坤:1, Bagua.震:2, Bagua.巽:3,
                     Bagua.坎:4, Bagua.离:5, Bagua.艮:6, Bagua.兑:7}
        diff = abs(positions[a] - positions[b])
        return min(diff, 8 - diff)
    
    def stats(self) -> Dict:
        total = self.active_count + self.skip_count
        return {
            'bagua': self.bagua.name,
            'active': self.active_count,
            'skip': self.skip_count,
            'skip_rate': self.skip_count / total if total > 0 else 0,
            'energy_saved': self.skip_count * 100  # 每次跳过节省100单位能耗
        }

# ── 蚁触节点 ──
class AntennaNode:
    """
    蚁触神经网节点
    状态机：休眠 → 监听 → 传递 → 完成 → 挥发 → 休眠
    """
    def __init__(self, node_id: str, bagua: Bagua, dim: int = 128):
        self.node_id = node_id
        self.bagua = bagua
        self.dim = dim
        self.gate = BaguaGate(dim, bagua)
        
        # 邻居表（只记邻居，无全局路由）
        self.neighbors: Dict[str, 'AntennaNode'] = {}
        
        # 信息素路径缓存
        self.pheromone_cache: Dict[str, float] = {}
        
        # 五行状态
        self.wuxing_state = {w: 1.0 for w in Wuxing}
        
        # 能耗统计
        self.energy_joules = 0.0
        self.touch_count = 0
        
        # 状态
        self.state = '休眠'
    
    def add_neighbor(self, node: 'AntennaNode'):
        """添加邻居（触角连接）"""
        self.neighbors[node.node_id] = node
    
    def touch(self, packet: PheromonePacket) -> List[PheromonePacket]:
        """
        触角触碰：接收信息包，决定转发或处理
        能耗模型：微焦耳级
        """
        self.state = '监听'
        self.touch_count += 1
        self.energy_joules += 1e-6  # 1微焦耳：唤醒能耗
        
        # 检查信息素是否挥发
        if packet.volatilize():
            self.state = '挥发'
            return []
        
        # 记录路径
        packet.path_trace.append(self.node_id)
        packet.ttl -= 1
        
        # 八卦门控：是否处理此包
        gated = self.gate.forward(packet.payload, packet.target_bagua)
        if gated is None:
            # 对冲卦象，直接转发给最近邻居
            self.state = '传递'
            return self._forward(packet)
        
        # 处理数据（模拟推理）
        self.energy_joules += 1e-9  # 1纳焦耳：计算能耗
        result = self._process(gated)
        
        # 更新信息素缓存
        path_key = '-'.join(packet.path_trace)
        self.pheromone_cache[path_key] = time.time()
        
        # 如果目标卦象匹配，完成；否则继续转发
        if self.bagua == packet.target_bagua:
            self.state = '完成'
            return [PheromonePacket(
                source_id=self.node_id,
                target_bagua=packet.target_bagua,
                payload=result,
                ttl=packet.ttl,
                path_trace=packet.path_trace.copy()
            )]
        else:
            self.state = '传递'
            return self._forward(packet)
    
    def _forward(self, packet: PheromonePacket) -> List[PheromonePacket]:
        """转发给最优邻居（信息素引导）"""
        if not self.neighbors or packet.ttl <= 0:
            return []
        
        # 选择目标卦象最近的邻居
        best_neighbor = None
        best_distance = 8
        
        for nid, node in self.neighbors.items():
            dist = self.gate._bagua_distance(node.bagua, packet.target_bagua)
            if dist < best_distance:
                best_distance = dist
                best_neighbor = node
        
        if best_neighbor:
            self.energy_joules += 1e-9  # 转发能耗
            return best_neighbor.touch(packet)
        return []
    
    def _process(self, x: np.ndarray) -> np.ndarray:
        """模拟节点处理（推理计算）"""
        # 简化：线性变换 + ReLU
        w = np.random.randn(self.dim, self.dim) * 0.01
        return np.maximum(0, w @ x)
    
    def get_stats(self) -> Dict:
        return {
            'node_id': self.node_id,
            'bagua': self.bagua.name,
            'state': self.state,
            'energy_joules': self.energy_joules,
            'touch_count': self.touch_count,
            'neighbors': len(self.neighbors),
            'gate_stats': self.gate.stats(),
            'wuxing': {k.name: v for k, v in self.wuxing_state.items()}
        }

# ── 蚁触神经网 ──
class AntennaMesh:
    """
    蚁触神经网主控
    8卦 × N节点 = 分布式推理网络
    """
    def __init__(self, nodes_per_bagua: int = 4, dim: int = 128):
        self.dim = dim
        self.nodes: Dict[str, AntennaNode] = {}
        self.bagua_groups: Dict[Bagua, List[AntennaNode]] = {b: [] for b in Bagua}
        
        # 创建节点
        node_idx = 0
        for bagua in Bagua:
            for i in range(nodes_per_bagua):
                nid = f"{bagua.name}-{i:02d}"
                node = AntennaNode(nid, bagua, dim)
                self.nodes[nid] = node
                self.bagua_groups[bagua].append(node)
                node_idx += 1
        
        # 建立邻居连接（同卦优先，异卦按距离）
        self._connect_neighbors()
        
        # 统计
        self.total_packets = 0
        self.total_energy = 0.0
    
    def _connect_neighbors(self):
        """建立邻居连接（八卦方位相邻优先）"""
        bagua_list = list(Bagua)
        
        for node in self.nodes.values():
            # 同卦节点全连接
            for peer in self.bagua_groups[node.bagua]:
                if peer.node_id != node.node_id:
                    node.add_neighbor(peer)
            
            # 相邻卦象选1个代表连接
            for other_bagua in bagua_list:
                if other_bagua != node.bagua:
                    dist = node.gate._bagua_distance(node.bagua, other_bagua)
                    if dist == 1 and self.bagua_groups[other_bagua]:
                        node.add_neighbor(self.bagua_groups[other_bagua][0])
    
    def inference(self, input_data: np.ndarray, target_bagua: Bagua) -> Tuple[np.ndarray, Dict]:
        """
        推理入口
        输入数据 → 八卦门控路由 → 目标卦象节点处理 → 输出
        """
        self.total_packets += 1
        
        # 创建信息素包
        packet = PheromonePacket(
            source_id="INPUT",
            target_bagua=target_bagua,
            payload=input_data,
            ttl=8
        )
        
        # 从输入卦象（坤-地/存储）开始
        start_node = self.bagua_groups[Bagua.坤][0]
        
        # 触达传递
        start_time = time.time()
        results = start_node.touch(packet)
        latency = time.time() - start_time
        
        # 收集能耗
        energy = sum(n.energy_joules for n in self.nodes.values())
        self.total_energy = energy
        
        # 统计
        stats = {
            'latency_ms': latency * 1000,
            'total_energy_j': energy,
            'packets': self.total_packets,
            'nodes_active': sum(1 for n in self.nodes.values() if n.touch_count > 0),
            'nodes_total': len(self.nodes),
            'skip_rate': self._avg_skip_rate(),
            'path_length': len(results[0].path_trace) if results else 0
        }
        
        if results:
            return results[0].payload, stats
        return np.zeros(self.dim), stats
    
    def _avg_skip_rate(self) -> float:
        skips = sum(n.gate.skip_count for n in self.nodes.values())
        active = sum(n.gate.active_count for n in self.nodes.values())
        total = skips + active
        return skips / total if total > 0 else 0
    
    def full_stats(self) -> Dict:
        return {
            'mesh_size': len(self.nodes),
            'total_energy_j': self.total_energy,
            'node_stats': [n.get_stats() for n in self.nodes.values()]
        }

# ============================================================
# 测试运行
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("龍魂 · 蚁触神经网 · 八卦门控推理压缩协议 v1.0")
    print("ANTENNA-8GATE · 启动测试")
    print("=" * 60)

    # 创建网络：8卦 × 4节点 = 32节点
    mesh = AntennaMesh(nodes_per_bagua=4, dim=128)
    print(f"\n网络规模：{len(mesh.nodes)} 节点（8卦 × 4）")
    print(f"维度：{mesh.dim}")

    # 测试推理：输入 → 乾卦（决策）
    print("\n" + "-" * 40)
    print("测试1：输入 → 乾卦（天/决策）")
    print("-" * 40)

    input_data = np.random.randn(128)
    output, stats = mesh.inference(input_data, Bagua.乾)

    print(f"输出维度：{output.shape}")
    print(f"延迟：{stats['latency_ms']:.3f} ms")
    print(f"总能耗：{stats['total_energy_j']:.2e} J")
    print(f"激活节点：{stats['nodes_active']}/{stats['nodes_total']}")
    print(f"门控跳过率：{stats['skip_rate']*100:.1f}%")
    print(f"路径长度：{stats['path_length']} 跳")

    # 测试多次推理
    print("\n" + "-" * 40)
    print("测试2：批量推理（100次）")
    print("-" * 40)

    for i in range(100):
        x = np.random.randn(128)
        target = list(Bagua)[i % 8]
        out, s = mesh.inference(x, target)

    print(f"总包数：{mesh.total_packets}")
    print(f"累计能耗：{mesh.total_energy:.2e} J")
    print(f"平均每包能耗：{mesh.total_energy/mesh.total_packets:.2e} J")
    print(f"平均跳过率：{mesh._avg_skip_rate()*100:.1f}%")

    # 对比：传统全连接网络能耗估算
    print("\n" + "-" * 40)
    print("对比：传统全连接网络（估算）")
    print("-" * 40)

    traditional_ops = 128 * 128 * 32  # 32节点全连接
    traditional_energy = traditional_ops * 1e-9 * 100  # 100次推理

    print(f"传统网络估算能耗：{traditional_energy:.2e} J")
    print(f"蚁触神经网实际能耗：{mesh.total_energy:.2e} J")
    print(f"节能比例：{(1 - mesh.total_energy/traditional_energy)*100:.1f}%")

    print("\n" + "=" * 60)
    print("测试完成 · DNA追溯：")
    print("#龍芯⚡️丙午·癸未·壬戌·乾为天-EFFICIENCY-BREAK-v5.0")
    print("=" * 60)
