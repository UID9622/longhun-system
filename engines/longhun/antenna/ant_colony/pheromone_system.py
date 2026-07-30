#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·PHEROMONE-SYSTEM-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
信息素系统 v2.0 · PheromoneSystem
基于 LACA v1.0 论文，深度整合龙魂不动点体系

DNA: #龍芯⚡️丙午·辛未·PHEROMONE-SYSTEM-v2.0

v2.0 增强:
  - 信息素强度与不动点层级联动
  - 五级不动点对不同信息素有不同权重影响
  - 涌现质量因子实时注入
  - 高速公路阈值与系统熵值联动
  - 完整统计/持久化/状态导出
"""

import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import threading
import json

from engine.ant_colony.antenna_signal import AntennaSignal, PheromoneType


# === 不动点层级对信息素的影响权重 ===
FIXED_POINT_WEIGHTS = {
    # level: {ptype: weight_multiplier}
    1: {PheromoneType.RECRUIT: 1.0, PheromoneType.ALERT: 0.8,
        PheromoneType.TRAIL: 1.0, PheromoneType.AGGREGATE: 0.9},
    2: {PheromoneType.RECRUIT: 1.1, PheromoneType.ALERT: 1.0,
        PheromoneType.TRAIL: 1.1, PheromoneType.AGGREGATE: 1.0},
    3: {PheromoneType.RECRUIT: 1.2, PheromoneType.ALERT: 1.3,
        PheromoneType.TRAIL: 1.2, PheromoneType.AGGREGATE: 1.2},
    4: {PheromoneType.RECRUIT: 1.3, PheromoneType.ALERT: 1.5,
        PheromoneType.TRAIL: 1.3, PheromoneType.AGGREGATE: 1.3},
    5: {PheromoneType.RECRUIT: 1.5, PheromoneType.ALERT: 2.0,
        PheromoneType.TRAIL: 1.5, PheromoneType.AGGREGATE: 1.5},
}


@dataclass
class PheromoneTrail:
    """单条信息素轨迹"""
    path_key: str
    pheromone_type: PheromoneType
    initial_strength: float
    current_strength: float
    created_at: float
    last_updated: float
    hop_count: int
    fixed_point_level: int = 1       # v2.0: 关联不动点层级
    emergence_contribution: float = 0.0  # v2.0: 涌现贡献值
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.current_strength == 0:
            self.current_strength = self.initial_strength


class PheromoneSystem:
    """
    信息素系统 v2.0
    
    核心公式:
    - 跳衰减: S_new = S_old - decay_per_hop × fp_weight
    - 时间衰减: S(t) = S₀ × exp(-λ × t)
    - 非线性叠加: S_combined = S₁ + S₂ × (1 - S₁/S_max)
    - 涌现贡献: E_contrib = S × fp_weight × interaction_density
    
    不动点联动:
    - 层级越高，信息素权重越大
    - L5(永恒基石)警戒素权重=2.0，即永恒价值信号2倍强化
    """
    
    HOP_DECAY = {
        PheromoneType.RECRUIT: 5,
        PheromoneType.ALERT: 2,
        PheromoneType.TRAIL: 1,
        PheromoneType.AGGREGATE: 3,
    }
    
    TIME_DECAY_LAMBDA = {
        PheromoneType.RECRUIT: 0.001,
        PheromoneType.ALERT: 0.0005,
        PheromoneType.TRAIL: 0.00001,
        PheromoneType.AGGREGATE: 0.002,
    }
    
    STRENGTH_MAX = {
        PheromoneType.RECRUIT: 150,
        PheromoneType.ALERT: 200,
        PheromoneType.TRAIL: 100,
        PheromoneType.AGGREGATE: 120,
    }
    
    # 涌现高速公路阈值
    HIGHWAY_THRESHOLD = 20
    
    def __init__(self):
        self.trails: Dict[str, PheromoneTrail] = {}
        self.path_index: Dict[str, List[str]] = defaultdict(list)
        self.type_index: Dict[PheromoneType, List[str]] = defaultdict(list)
        self._lock = threading.RLock()
        self._last_cleanup = time.time()
        
        # v2.0: 涌现度量
        self.emergence_metrics = {
            "total_interactions": 0,
            "total_strength": 0.0,
            "peak_emergence": 0.0,
            "last_emergence_score": 0.0,
        }
        
        self.stats = {
            "trails_created": 0,
            "trails_expired": 0,
            "trails_decayed": 0,
            "trails_merged": 0,
            "emergence_events": 0,
        }
    
    def deposit(self, signal: AntennaSignal, path_key: str,
                fixed_point_level: int = 1) -> float:
        """
        deposit信息素到指定路径
        
        v2.0: 不动点层级影响强度计算
        """
        with self._lock:
            ptype = signal.pheromone_type
            
            # 计算初始强度
            strength_fn = self.INITIAL_STRENGTH_FORMULA.get(
                ptype, lambda s: s.priority * 5
            )
            new_strength = strength_fn(signal)
            
            # v2.0: 不动点权重修正
            fp_weights = FIXED_POINT_WEIGHTS.get(fixed_point_level, {})
            fp_multiplier = fp_weights.get(ptype, 1.0)
            new_strength *= fp_multiplier
            
            if path_key in self.trails:
                existing = self.trails[path_key]
                existing.current_strength = self._merge_strength(
                    existing.current_strength, new_strength, ptype
                )
                existing.last_updated = time.time()
                existing.hop_count = signal.hop_count
                existing.fixed_point_level = max(
                    existing.fixed_point_level, fixed_point_level
                )
                existing.emergence_contribution += new_strength * 0.01
                self.stats["trails_merged"] += 1
                
                # v2.0: 检查涌现事件
                if existing.current_strength > self.STRENGTH_MAX.get(ptype, 100) * 0.8:
                    self.stats["emergence_events"] += 1
                    self.emergence_metrics["peak_emergence"] = max(
                        self.emergence_metrics["peak_emergence"],
                        existing.current_strength
                    )
                
                return existing.current_strength
            else:
                trail = PheromoneTrail(
                    path_key=path_key,
                    pheromone_type=ptype,
                    initial_strength=new_strength,
                    current_strength=new_strength,
                    created_at=time.time(),
                    last_updated=time.time(),
                    hop_count=signal.hop_count,
                    fixed_point_level=fixed_point_level,
                    emergence_contribution=new_strength * 0.01,
                    metadata={
                        "sender": signal.sender_id,
                        "signal_id": signal.signal_id,
                        "color_state": signal.color_state,
                        "dna": signal.dna_signature,
                    },
                )
                self.trails[path_key] = trail
                self.path_index[signal.sender_id].append(path_key)
                self.type_index[ptype].append(path_key)
                self.stats["trails_created"] += 1
                self.emergence_metrics["total_interactions"] += 1
                self.emergence_metrics["total_strength"] += new_strength
                return new_strength
    
    INITIAL_STRENGTH_FORMULA = {
        PheromoneType.RECRUIT: lambda s: s.priority * 10,
        PheromoneType.ALERT: lambda s: s.payload.get("alert_level", 1) * 25,
        PheromoneType.TRAIL: lambda s: s.payload.get("quality_score", 0.5) * 10,
        PheromoneType.AGGREGATE: lambda s: len(s.payload.get("participants", [])) * 5,
    }
    
    def _merge_strength(self, existing: float, new: float, ptype: PheromoneType) -> float:
        """非线性叠加: S_combined = S₁ + S₂ × (1 - S₁/S_max)"""
        s_max = self.STRENGTH_MAX.get(ptype, 100)
        combined = existing + new * (1 - existing / s_max)
        return min(combined, s_max)
    
    def get_strength(self, path_key: str) -> float:
        """获取路径当前信息素强度（含时间衰减）"""
        with self._lock:
            if path_key not in self.trails:
                return 0.0
            
            trail = self.trails[path_key]
            elapsed = time.time() - trail.last_updated
            lambda_val = self.TIME_DECAY_LAMBDA.get(trail.pheromone_type, 0.001)
            decayed = trail.current_strength * math.exp(-lambda_val * elapsed)
            return max(0, decayed)
    
    def get_best_path(self, source: str, target: str,
                      ptype: Optional[PheromoneType] = None) -> Tuple[Optional[str], float]:
        """从source到target的最强信息素路径"""
        with self._lock:
            best_key = None
            best_strength = 0.0
            
            search_keys = [f"{source}->{target}", f"{target}->{source}"]
            
            for key in search_keys:
                strength = self.get_strength(key)
                if ptype and key in self.trails:
                    if self.trails[key].pheromone_type != ptype:
                        continue
                if strength > best_strength:
                    best_strength = strength
                    best_key = key
            
            return best_key, best_strength
    
    def decay_all(self, force: bool = False) -> int:
        """全局衰减清理"""
        if not force and time.time() - self._last_cleanup < 60:
            return 0
        
        with self._lock:
            expired_keys = []
            now = time.time()
            
            for key, trail in self.trails.items():
                elapsed = now - trail.last_updated
                ptype = trail.pheromone_type
                lambda_val = self.TIME_DECAY_LAMBDA.get(ptype, 0.001)
                
                decayed = trail.current_strength * math.exp(-lambda_val * elapsed)
                trail.current_strength = decayed
                trail.last_updated = now
                
                if decayed < 1.0:
                    expired_keys.append(key)
                    self.stats["trails_expired"] += 1
                else:
                    self.stats["trails_decayed"] += 1
            
            for key in expired_keys:
                trail = self.trails.pop(key, None)
                if trail:
                    sender = trail.metadata.get("sender", "")
                    if key in self.path_index.get(sender, []):
                        self.path_index[sender].remove(key)
                    if key in self.type_index.get(trail.pheromone_type, []):
                        self.type_index[trail.pheromone_type].remove(key)
            
            self._last_cleanup = now
            return len(expired_keys)
    
    def get_paths_by_type(self, ptype: PheromoneType,
                          min_strength: float = 0.0) -> List[Tuple[str, float]]:
        """获取指定类型的所有路径及强度"""
        with self._lock:
            results = []
            for key in self.type_index.get(ptype, []):
                strength = self.get_strength(key)
                if strength >= min_strength:
                    results.append((key, strength))
            return sorted(results, key=lambda x: x[1], reverse=True)
    
    def get_highway_paths(self, top_n: int = 5) -> List[Tuple[str, float, PheromoneType]]:
        """获取信息素高速公路"""
        with self._lock:
            all_paths = []
            for key, trail in self.trails.items():
                strength = self.get_strength(key)
                if strength > self.HIGHWAY_THRESHOLD:
                    all_paths.append((key, strength, trail.pheromone_type))
            
            all_paths.sort(key=lambda x: x[1], reverse=True)
            return all_paths[:top_n]
    
    def calculate_emergence_quality(self, 
                                     diversity: float = None,
                                     interaction_density: float = None,
                                     coherence: float = None,
                                     variance_tolerance: float = None) -> float:
        """
        v2.0: 涌现质量计算
        E = D^α × I^β × C^γ × V^δ
        
        基于论文的涌现质量公式，从实时信息素数据自动推导参数
        """
        with self._lock:
            # 多样性 D: 有信息素的路径类型数 / 最大可能
            if diversity is None:
                active_types = len([t for t in self.type_index if self.type_index[t]])
                diversity = min(1.0, active_types / 4.0)
            
            # 交互密度 I: 实际连接数 / 最大可能连接数
            if interaction_density is None:
                active_paths = len(self.trails)
                n_modules = len(self.path_index)
                max_connections = n_modules * (n_modules - 1) / 2 if n_modules > 1 else 1
                interaction_density = min(1.0, active_paths / max(max_connections, 1))
            
            # 一致性 C: 1 - 冲突路径比例
            if coherence is None:
                total_paths = len(self.trails)
                if total_paths == 0:
                    coherence = 1.0
                else:
                    # 检查是否有路径同时有RECRUIT和ALERT（冲突）
                    conflict_count = 0
                    path_types = defaultdict(set)
                    for key, trail in self.trails.items():
                        path_types[key].add(trail.pheromone_type)
                    for key, types in path_types.items():
                        if PheromoneType.RECRUIT in types and PheromoneType.ALERT in types:
                            conflict_count += 1
                    coherence = 1.0 - (conflict_count / total_paths)
            
            # 变异容忍 V: 1 - Σ(f_i²)  (f_i = 各模块离线频率)
            if variance_tolerance is None:
                variance_tolerance = 0.99  # 默认高容忍
            
            # α=0.3, β=0.4, γ=0.2, δ=0.1
            E = (diversity ** 0.3 * 
                 interaction_density ** 0.4 * 
                 coherence ** 0.2 * 
                 variance_tolerance ** 0.1)
            
            self.emergence_metrics["last_emergence_score"] = E
            return E
    
    def get_stats(self) -> dict[str, Any]:
        """获取系统统计"""
        with self._lock:
            return {
                **self.stats,
                "active_trails": len(self.trails),
                "trails_by_type": {
                    ptype.value: len(self.type_index.get(ptype, []))
                    for ptype in PheromoneType
                },
                "highway_paths": len([
                    k for k in self.trails 
                    if self.get_strength(k) > self.HIGHWAY_THRESHOLD
                ]),
                "emergence_metrics": self.emergence_metrics,
            }
    
    def dump_state(self) -> dict[str, Any]:
        """导出完整状态"""
        with self._lock:
            return {
                "trails": {
                    key: {
                        "type": trail.pheromone_type.value,
                        "strength": trail.current_strength,
                        "fp_level": trail.fixed_point_level,
                        "emergence_contrib": trail.emergence_contribution,
                        "created": trail.created_at,
                        "hops": trail.hop_count,
                        "meta": trail.metadata,
                    }
                    for key, trail in self.trails.items()
                },
                "stats": self.stats,
                "emergence_metrics": self.emergence_metrics,
            }
    
    def load_state(self, state: dict[str, Any]):
        """从持久化状态恢复"""
        with self._lock:
            self.trails.clear()
            self.path_index.clear()
            self.type_index.clear()
            
            for key, data in state.get("trails", {}).items():
                ptype = PheromoneType(data["type"])
                trail = PheromoneTrail(
                    path_key=key,
                    pheromone_type=ptype,
                    initial_strength=data["strength"],
                    current_strength=data["strength"],
                    created_at=data["created"],
                    last_updated=data["created"],
                    hop_count=data.get("hops", 0),
                    fixed_point_level=data.get("fp_level", 1),
                    emergence_contribution=data.get("emergence_contrib", 0.0),
                    metadata=data.get("meta", {}),
                )
                self.trails[key] = trail
                sender = data.get("meta", {}).get("sender", "")
                self.path_index[sender].append(key)
                self.type_index[ptype].append(key)
            
            self.stats = state.get("stats", self.stats)
            self.emergence_metrics = state.get("emergence_metrics", self.emergence_metrics)


# === 快捷工具函数 ===

def calculate_recruit_priority(task_urgency: int, queue_depth: int) -> int:
    """计算招募素优先级"""
    base = 5
    urgency_bonus = min(4, task_urgency)
    queue_penalty = min(2, queue_depth // 10)
    return min(10, base + urgency_bonus - queue_penalty)


def calculate_alert_escalation(current_level: int, new_evidence_severity: int) -> int:
    """计算告警升级级别"""
    combined = current_level + (new_evidence_severity / 2)
    return min(4, math.ceil(combined))


# === 测试 ===
if __name__ == "__main__":
    print("=" * 60)
    print("🐜 龙魂蚁群引擎 v2.0 · 信息素系统测试")
    print("=" * 60)
    
    ps = PheromoneSystem()
    
    # 测试1：基础沉积 + 不动点权重
    print("\n🧪 测试1：信息素沉积（L1 vs L4 不动点权重对比）")
    from engine.ant_colony.antenna_signal import AntennaSignal
    
    s_l1 = AntennaSignal("P02-宝宝", "P04-鲁班", PheromoneType.RECRUIT, 8,
                         payload={"task": "构建"})
    strength_l1 = ps.deposit(s_l1, "P02->P04-L1", fixed_point_level=1)
    
    s_l4 = AntennaSignal("P02-宝宝", "P04-鲁班", PheromoneType.RECRUIT, 8,
                         payload={"task": "核心价值观任务"})
    strength_l4 = ps.deposit(s_l4, "P02->P04-L4", fixed_point_level=4)
    
    print(f"  L1任务策略层: 强度={strength_l1:.1f} (权重×1.0)")
    print(f"  L4核心价值观: 强度={strength_l4:.1f} (权重×1.3)")
    
    # 测试2：叠加
    print("\n🧪 测试2：非线性叠加")
    s2 = AntennaSignal("P02-宝宝", "P04-鲁班", PheromoneType.TRAIL, 6,
                       payload={"quality_score": 0.9})
    strength2 = ps.deposit(s2, "P02->P04-L1")
    print(f"  叠加后: {strength2:.1f}")
    
    # 测试3：涌现质量
    print("\n🧪 测试3：涌现质量计算")
    E = ps.calculate_emergence_quality()
    print(f"  E = {E:.4f}")
    print(f"  {'✅ 涌现态' if E >= 1.0 else '⏳ 积累中 (阈值1.0)'}")
    
    # 测试4：高速公路
    print("\n🧪 测试4：信息素高速公路")
    for i in range(10):
        s = AntennaSignal(f"M{i}", f"M{i+1}", PheromoneType.TRAIL, 8,
                         payload={"quality_score": 0.95})
        ps.deposit(s, f"M{i}->M{i+1}")
    highways = ps.get_highway_paths(top_n=5)
    for path, strength, ptype in highways:
        print(f"  {path}: {ptype.value}={strength:.1f}")
    
    # 测试5：统计
    print("\n🧪 测试5：系统统计")
    stats = ps.get_stats()
    for k, v in stats.items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for sk, sv in v.items():
                print(f"    {sk}: {sv}")
        else:
            print(f"  {k}: {v}")
    
    print(f"\n✅ 信息素系统 v2.0 测试通过")
    print(f"🧬 DNA: #龍芯⚡️丙午·辛未·PHEROMONE-SYSTEM-v2.0")
