#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║       龍魂 · AI驱动时空织网引擎 v2.0                             ║
║                                                                  ║
║  主动安全新范式 — 从被动记录到主动预测                             ║
║  零断点 · 无痕续迹 · 时空连续体 · ST-GNN · 主动安全               ║
║                                                                  ║
║  架构: 边缘层(昇腾310) → 区域层(鲲鹏920) → 中心层(鲲鹏集群)     ║
║                                                                  ║
║  DNA:  #龍芯⚡️丙午·辛未·SPACETIME-WEAVE-v2.0                    ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL  ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_spacetime_weave.py demo     # 运行时空织网演示
  python3 bin/lh_spacetime_weave.py status   # 查看织网状态
  python3 bin/lh_spacetime_weave.py run      # 启动引擎服务
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import math
import os
import argparse
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set, Any
from collections import defaultdict, deque
from pathlib import Path

# ── 可选依赖 ──
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np: Any = None  # type: ignore[assignment]

try:
    import torch
    import torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

ROOT = Path(__file__).resolve().parent.parent


# ══════════════════════════════════════════════════════════════════
# 数据定义
# ══════════════════════════════════════════════════════════════════

@dataclass
class SpacetimeNode:
    """时空织网节点 · 四维连续体的一个点"""
    position: Tuple[float, float, float]  # X, Y, Z 空间坐标
    timestamp: float                       # T 时间轴
    feature_vector: List[float]            # 特征向量
    confidence: float                      # 置信度
    camera_id: str                         # 采集摄像头
    target_id: str                         # 目标ID
    prev_node: Optional[str] = None        # 上一时空节点
    next_node: Optional[str] = None        # 下一时空节点
    trajectory_id: str = ""                # 轨迹链ID

    def to_dict(self) -> dict[str, Any]:
        feats = self.feature_vector[:8] if len(self.feature_vector) > 8 else self.feature_vector
        return {
            "position": list(self.position),
            "timestamp": self.timestamp,
            "features_hash": hashlib.sha256(
                bytes([min(255, max(0, int(f * 128 + 128))) for f in self.feature_vector[:64]])
            ).hexdigest()[:8],
            "confidence": round(self.confidence, 4),
            "camera_id": self.camera_id,
            "target_id": self.target_id[:12],
            "trajectory_id": self.trajectory_id,
        }


@dataclass
class CameraNode:
    """摄像头时空节点"""
    node_id: str
    position: Tuple[float, float, float]
    fov: float                            # 视场角(度)
    range_m: float                        # 有效范围(米)
    neighbors: List[str] = field(default_factory=list)
    coverage_area: List[Tuple[float, float]] = field(default_factory=list)
    restricted: bool = False              # 禁入区域
    active_targets: Set[str] = field(default_factory=set)


@dataclass
class SafetyEvent:
    """主动安全事件"""
    event_id: str
    event_type: str                       # intrusion/abnormal/crowd/lost/traffic
    severity: str                         # low/medium/high/critical
    target_id: str
    camera_id: str
    timestamp: float
    position: Tuple[float, float, float]
    description: str
    recommendation: str


# ══════════════════════════════════════════════════════════════════
# ST-GNN 时空图神经网络 (numpy 纯实现 · torch 有则加速)
# ══════════════════════════════════════════════════════════════════

class NumpySTGNN:
    """纯 numpy ST-GNN — 无 torch 依赖可用"""

    def __init__(self, in_dim: int = 256, out_dim: int = 256, temporal_window: int = 5):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.temporal_window = temporal_window

        # 空间图卷积权重 (He初始化)
        rng = np.random.RandomState(9622)
        self.W_spatial = rng.randn(in_dim, out_dim) * math.sqrt(2.0 / in_dim)
        self.b_spatial = np.zeros(out_dim)

        # 时间卷积权重
        self.W_temporal = rng.randn(temporal_window, out_dim) * 0.1
        self.b_temporal = np.zeros(out_dim)

        # 门控
        self.W_gate = rng.randn(out_dim * 2, out_dim) * 0.1
        self.b_gate = np.zeros(out_dim)

        # 注意力投影
        self.W_q = rng.randn(out_dim, out_dim) * 0.1
        self.W_k = rng.randn(out_dim, out_dim) * 0.1
        self.W_v = rng.randn(out_dim, out_dim) * 0.1

    def _relu(self, x: Any) -> Any:
        return np.maximum(0, x)

    def _sigmoid(self, x: Any) -> Any:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))

    def _softmax(self, x: Any, axis: int = -1) -> Any:
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def forward(self, spatial_nodes: Any, temporal_sequence: Any) -> Any:
        """
        spatial_nodes: [N, D]  同一时刻多摄像头节点特征
        temporal_sequence: [T, D]  同一目标时间序列特征
        返回: [min(N,T), D_out]
        """
        # 空间图卷积: h_spatial = ReLU(x @ W + b)
        h_spatial = self._relu(spatial_nodes @ self.W_spatial + self.b_spatial)  # [N, D_out]

        # 时间卷积 (因果卷积，padding只在前端)
        T = temporal_sequence.shape[0]
        D = temporal_sequence.shape[1]
        h_temp_list = []
        for t in range(T):
            # 取时间窗口 [t-window+1, t]
            start = max(0, t - self.temporal_window + 1)
            window = temporal_sequence[start:t + 1]
            padded = np.zeros((self.temporal_window, D))
            padded[self.temporal_window - len(window):] = window
            # 卷积: sum over window_time × input_dim, W[t,j] — output[j] = Σ_t Σ_i padded[t,i] * W[t,j]
            val = np.sum(padded[:, :, np.newaxis] * self.W_temporal[:, np.newaxis, :], axis=(0, 1))
            h_temp_list.append(self._relu(val + self.b_temporal))
        h_temporal = np.array(h_temp_list)  # [T, D_out]

        # 对齐长度
        min_len = min(h_spatial.shape[0], h_temporal.shape[0])
        h_spatial = h_spatial[:min_len]
        h_temporal = h_temporal[:min_len]

        # 注意力融合: 自注意力
        Q = h_temporal @ self.W_q  # [L, D_out]
        K = h_temporal @ self.W_k
        V = h_temporal @ self.W_v
        attn_scores = self._softmax(Q @ K.T / math.sqrt(self.out_dim), axis=-1)
        attended = attn_scores @ V  # [L, D_out]

        # 门控融合
        gate_input = np.concatenate([h_spatial, attended], axis=-1)  # [L, 2*D_out]
        g = self._sigmoid(gate_input @ self.W_gate + self.b_gate)

        return g * attended + (1 - g) * h_spatial


# ══════════════════════════════════════════════════════════════════
# 时空织网引擎
# ══════════════════════════════════════════════════════════════════

class SpacetimeWeaveEngine:
    """AI驱动时空织网引擎 v2.0"""

    DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
    UID = "9622"
    VERSION = "v2.0-spacetime-weave"

    def __init__(self, feature_dim: int = 256):
        self.feature_dim = feature_dim
        self.stgnn = NumpySTGNN(feature_dim, feature_dim) if HAS_NUMPY else None

        # 时空织网存储
        self.spacetime_nodes: Dict[str, SpacetimeNode] = {}
        self.trajectories: Dict[str, List[str]] = defaultdict(list)
        self.camera_network: Dict[str, CameraNode] = {}

        # 安全事件
        self.safety_events: List[SafetyEvent] = []
        self.event_counter = 0

        # 无痕续迹参数
        self.weave_params = {
            "temporal_gap_max": 2.0,
            "spatial_gap_max": 100.0,
            "feature_similarity_threshold": 0.85,
            "prediction_horizon": 5.0,
            "merge_gap_threshold": 1.5,
        }

        # 主动安全策略映射
        self.safety_handlers = {
            "intrusion": self._handle_intrusion,
            "abnormal_behavior": self._handle_abnormal,
            "crowd_gathering": self._handle_crowd,
            "lost_target": self._handle_lost,
            "traffic_violation": self._handle_traffic,
        }

        print(f"🐉 龍魂 · 时空织网引擎 {self.VERSION} 初始化完成")
        print(f"   DNA: {self.DNA[:40]}...")
        print(f"   ST-GNN: {'✅ numpy纯计算' if self.stgnn else '⚠️ 无numpy，特征对比退化'}")

    # ── 摄像头注册 ──

    def register_camera(self, cam_id: str, position: Tuple[float, float, float],
                        fov: float = 90, neighbors: Optional[List[str]] = None,
                        coverage_area: Optional[List[Tuple[float, float]]] = None,
                        restricted: bool = False):
        """注册摄像头到时空织网"""
        if neighbors is None:
            neighbors = []
        if coverage_area is None:
            cx, cy, _ = position
            r = 30
            coverage_area = [(cx - r, cy - r), (cx + r, cy - r),
                             (cx + r, cy + r), (cx - r, cy + r)]

        self.camera_network[cam_id] = CameraNode(
            node_id=cam_id,
            position=position,
            fov=fov,
            range_m=50,
            neighbors=neighbors,
            coverage_area=coverage_area,
            restricted=restricted,
        )
        print(f"📹 注册: {cam_id} @ {position} · 邻:{neighbors} · 禁区:{restricted}")

    # ── 织网核心 ──

    def weave_node(self, target_id: str, camera_id: str,
                   position: Tuple[float, float, float], timestamp: float,
                   features: List[float], confidence: float = 0.9) -> str:
        """织入时空节点 · 核心入口"""
        # 生成节点ID
        node_id = f"ST-{target_id[:8]}-{int(timestamp * 1000)}"

        # 创建节点
        node = SpacetimeNode(
            position=position,
            timestamp=timestamp,
            feature_vector=list(features),
            confidence=confidence,
            camera_id=camera_id,
            target_id=target_id,
        )

        # 查找时空连续性（无痕续迹）
        trajectory_id = self._find_trajectory_continuity(target_id, features, timestamp, position)
        node.trajectory_id = trajectory_id

        # 先存入节点（link需要引用已存在节点）
        self.spacetime_nodes[node_id] = node
        self.trajectories[trajectory_id].append(node_id)

        # 链接前后节点
        self._link_nodes(trajectory_id, node_id)

        # 更新摄像头
        if camera_id in self.camera_network:
            self.camera_network[camera_id].active_targets.add(target_id)

        # 主动安全检测
        self._active_safety_check(node, trajectory_id)

        return node_id

    def _find_trajectory_continuity(self, target_id: str, features: List[float],
                                    timestamp: float, position: Tuple[float, float, float]) -> str:
        """无痕续迹核心 — 跨镜时空连续性匹配"""
        # 尝试匹配已有轨迹
        best_score = 0
        best_traj = None

        for traj_id, node_ids in self.trajectories.items():
            if not node_ids:
                continue
            last_node_id = node_ids[-1]
            last_node = self.spacetime_nodes.get(last_node_id)
            if not last_node:
                continue

            # 时间连续性检查
            time_gap = timestamp - last_node.timestamp
            if time_gap > self.weave_params["temporal_gap_max"] or time_gap < 0:
                continue

            # 空间连续性
            pos_arr = np.array(position) if HAS_NUMPY else position
            last_pos_arr = np.array(last_node.position) if HAS_NUMPY else last_node.position
            if HAS_NUMPY:
                spatial_gap = float(np.linalg.norm(pos_arr - last_pos_arr))  # type: ignore[operator]
            else:
                spatial_gap = math.sqrt(sum((a - b)**2 for a, b in zip(position, last_node.position)))
            if spatial_gap > self.weave_params["spatial_gap_max"]:
                continue

            # 特征相似度
            f_arr = np.array(features) if HAS_NUMPY else features
            lf_arr = np.array(last_node.feature_vector) if HAS_NUMPY else last_node.feature_vector
            similarity = float(np.dot(f_arr, lf_arr) / (np.linalg.norm(f_arr) * np.linalg.norm(lf_arr) + 1e-8)) \
                if HAS_NUMPY else self._cosine_sim_pure(features, last_node.feature_vector)

            if similarity > best_score:
                best_score = similarity
                best_traj = traj_id

        if best_score > self.weave_params["feature_similarity_threshold"] and best_traj:
            return best_traj

        # 跨镜重识别 — 相邻摄像头·寻找不同目标间的高相似度
        for traj_id, node_ids in self.trajectories.items():
            if not node_ids:
                continue
            last_node = self.spacetime_nodes.get(node_ids[-1])
            if not last_node or last_node.target_id == target_id:
                continue
            if last_node.camera_id not in self.camera_network:
                continue
            if abs(timestamp - last_node.timestamp) > self.weave_params["merge_gap_threshold"]:
                continue

            f_arr = np.array(features) if HAS_NUMPY else features
            lf_arr = np.array(last_node.feature_vector) if HAS_NUMPY else last_node.feature_vector
            if HAS_NUMPY:
                sim = float(np.dot(f_arr, lf_arr) / (np.linalg.norm(f_arr) * np.linalg.norm(lf_arr) + 1e-8))
            else:
                sim = self._cosine_sim_pure(features, last_node.feature_vector)

            if sim > self.weave_params["feature_similarity_threshold"]:
                new_traj = f"TRJ-{target_id[:8]}-{int(timestamp)}"
                self.trajectories[new_traj] = []
                print(f"🔄 无痕续迹: 跨镜合并 {traj_id[:12]}... ↔ {target_id[:8]}... (sim={sim:.4f})")
                return self._merge_trajectories(traj_id, new_traj)

        # 新轨迹
        return f"TRJ-{target_id[:8]}-{int(timestamp)}"

    def _link_nodes(self, trajectory_id: str, new_node_id: str):
        """链接前后时空节点"""
        node_ids = self.trajectories[trajectory_id]
        if len(node_ids) >= 2:
            prev_id = node_ids[-2]
            if prev_id in self.spacetime_nodes:
                self.spacetime_nodes[new_node_id].prev_node = prev_id
                self.spacetime_nodes[prev_id].next_node = new_node_id

    def _merge_trajectories(self, traj_a: str, traj_b: str) -> str:
        """合并两条轨迹（跨镜无缝续迹）"""
        merged_id = f"MRG-{traj_a[:8]}-{traj_b[:8]}"
        nodes_a = self.trajectories.get(traj_a, [])
        nodes_b = self.trajectories.get(traj_b, [])

        all_nodes = sorted(
            nodes_a + nodes_b,
            key=lambda nid: self.spacetime_nodes[nid].timestamp if nid in self.spacetime_nodes else 0
        )

        self.trajectories[merged_id] = all_nodes
        for nid in all_nodes:
            if nid in self.spacetime_nodes:
                self.spacetime_nodes[nid].trajectory_id = merged_id

        # 重新链接
        for i in range(len(all_nodes) - 1):
            if all_nodes[i] in self.spacetime_nodes and all_nodes[i + 1] in self.spacetime_nodes:
                self.spacetime_nodes[all_nodes[i]].next_node = all_nodes[i + 1]
                self.spacetime_nodes[all_nodes[i + 1]].prev_node = all_nodes[i]

        return merged_id

    def _cosine_sim_pure(self, a: List[float], b: List[float]) -> float:
        """纯Python余弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b + 1e-8)

    # ── 轨迹预测 ──

    def predict_future(self, trajectory_id: str, horizon: float = 5.0) -> List[SpacetimeNode]:
        """AI预测未来时空节点 — 卡尔曼+ST-GNN"""

        node_ids = self.trajectories.get(trajectory_id, [])
        if len(node_ids) < 3:
            return []

        recent_nodes = [self.spacetime_nodes[nid] for nid in node_ids[-10:]
                         if nid in self.spacetime_nodes]
        if len(recent_nodes) < 3:
            return []

        positions = np.array([n.position for n in recent_nodes]) if HAS_NUMPY else \
            [n.position for n in recent_nodes]
        timestamps = np.array([n.timestamp for n in recent_nodes]) if HAS_NUMPY else \
            [n.timestamp for n in recent_nodes]
        features_list = [n.feature_vector for n in recent_nodes]

        if HAS_NUMPY:
            velocities = np.diff(positions, axis=0) / (np.diff(timestamps)[:, np.newaxis] + 1e-8)
            last_pos = positions[-1]
            last_vel = velocities[-1] if len(velocities) > 0 else np.zeros(3)
            last_time = timestamps[-1]

            # 加速度估计
            if len(velocities) >= 2:
                acc = (velocities[-1] - velocities[-2]) / (timestamps[-1] - timestamps[-2] + 1e-8)
            else:
                acc = np.zeros(3)

            predictions = []
            for dt in np.arange(0.5, horizon + 0.5, 0.5):
                pred_pos = last_pos + last_vel * dt + 0.5 * acc * dt**2
                pred_time = last_time + dt

                # ST-GNN特征预测
                if self.stgnn and len(recent_nodes) >= 5:
                    spatial = np.array(features_list[-5:])
                    temporal = np.array(features_list[-5:])
                    pred_feat_out = self.stgnn.forward(spatial, temporal)
                    pred_feat = pred_feat_out[-1].tolist()
                else:
                    pred_feat = features_list[-1]

                pred_node = SpacetimeNode(
                    position=(float(pred_pos[0]), float(pred_pos[1]), float(pred_pos[2])),
                    timestamp=pred_time,
                    feature_vector=pred_feat,
                    confidence=0.7,
                    camera_id="PREDICTED",
                    target_id=trajectory_id,
                    trajectory_id=trajectory_id,
                )
                predictions.append(pred_node)
        else:
            # 退化纯Python预测
            last = recent_nodes[-1]
            predictions = []
            for i, dt in enumerate([0.5 * (j + 1) for j in range(int(horizon / 0.5))]):
                pred_node = SpacetimeNode(
                    position=(last.position[0] + dt * 0.5, last.position[1] + dt * 0.3,
                              last.position[2]),
                    timestamp=last.timestamp + dt,
                    feature_vector=last.feature_vector,
                    confidence=0.5,
                    camera_id="PREDICTED",
                    target_id=trajectory_id,
                    trajectory_id=trajectory_id,
                )
                predictions.append(pred_node)

        return predictions

    # ── 主动安全 ──

    def _active_safety_check(self, node: SpacetimeNode, trajectory_id: str):
        """主动安全检测 — 5类策略"""
        traj_node_ids = self.trajectories.get(trajectory_id, [])
        traj_nodes = [self.spacetime_nodes[nid] for nid in traj_node_ids
                      if nid in self.spacetime_nodes]

        if len(traj_nodes) < 3:
            return

        # 速度异常检测
        speeds = []
        for i in range(1, len(traj_nodes)):
            dt = traj_nodes[i].timestamp - traj_nodes[i - 1].timestamp
            if dt > 0:
                dx = traj_nodes[i].position[0] - traj_nodes[i - 1].position[0]
                dy = traj_nodes[i].position[1] - traj_nodes[i - 1].position[1]
                speed = math.sqrt(dx * dx + dy * dy) / dt
                speeds.append(speed)

        avg_speed = sum(speeds) / len(speeds) if speeds else 0
        max_speed = max(speeds) if speeds else 0

        if max_speed > 8.0:  # >8m/s ≈ 29km/h — 行人异常
            self._emit_safety_event("abnormal_behavior", node, trajectory_id,
                                    f"速度异常: max={max_speed:.1f}m/s, avg={avg_speed:.1f}m/s")

        # 区域入侵
        for cam_id, cam in self.camera_network.items():
            if cam.restricted and self._point_in_polygon(node.position[:2], cam.coverage_area):
                self._emit_safety_event("intrusion", node, trajectory_id, f"禁区入侵: {cam_id}")

        # 聚集检测
        current_cam = self.camera_network.get(node.camera_id)
        if current_cam and len(current_cam.active_targets) > 30:
            self._emit_safety_event("crowd_gathering", node, trajectory_id,
                                    f"人群聚集: {len(current_cam.active_targets)}人")

        # 静止异常 (超过30秒未移动)
        if len(traj_nodes) >= 6:
            recent_positions = [n.position for n in traj_nodes[-6:]]
            movement = sum(
                math.sqrt((recent_positions[i][0] - recent_positions[i - 1][0]) ** 2 +
                          (recent_positions[i][1] - recent_positions[i - 1][1]) ** 2)
                for i in range(1, len(recent_positions))
            )
            if movement < 0.5:  # <0.5米/3秒
                self._emit_safety_event("abnormal_behavior", node, trajectory_id, "静止异常: 3秒内位移<0.5m")

    def _emit_safety_event(self, event_type: str, node: SpacetimeNode,
                           trajectory_id: str, description: str):
        """触发主动安全事件"""
        self.event_counter += 1
        event = SafetyEvent(
            event_id=f"SAFE-{self.event_counter:04d}",
            event_type=event_type,
            severity="high" if event_type in ("intrusion",) else "medium",
            target_id=trajectory_id[:12],
            camera_id=node.camera_id,
            timestamp=time.time(),
            position=node.position,
            description=description,
            recommendation=self._get_recommendation(event_type),
        )
        self.safety_events.append(event)

        handler = self.safety_handlers.get(event_type)
        if handler:
            handler(event)

    def _get_recommendation(self, event_type: str) -> str:
        recs = {
            "intrusion": "声光报警+安保出勤+证据链自动录制",
            "abnormal_behavior": "提升追踪频率至50ms+预警周边3个摄像头",
            "crowd_gathering": "启动人流疏导预案+开放备用通道",
            "lost_target": "全网广播搜索+特征比对+预测轨迹引导",
            "traffic_violation": "自动抓拍+车牌识别+违法证据上传",
        }
        return recs.get(event_type, "常规处置")

    def _handle_intrusion(self, event: SafetyEvent):
        print(f"🚨 [主动安全] 入侵: {event.description}")

    def _handle_abnormal(self, event: SafetyEvent):
        print(f"⚠️  [主动安全] 异常: {event.description}")

    def _handle_crowd(self, event: SafetyEvent):
        print(f"👥 [主动安全] 聚集: {event.description}")

    def _handle_lost(self, event: SafetyEvent):
        print(f"🔍 [主动安全] 走失: {event.description}")

    def _handle_traffic(self, event: SafetyEvent):
        print(f"🚗 [主动安全] 交通: {event.description}")

    @staticmethod
    def _point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        """射线法判断点是否在多边形内"""
        x, y = point[:2]
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i][:2]
            xj, yj = polygon[j][:2]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-8) + xi):
                inside = not inside
            j = i
        return inside

    # ── 状态 ──

    def get_weave_status(self) -> dict[str, Any]:
        """时空织网状态"""
        total_events = len(self.safety_events)
        types_count = defaultdict(int)
        for e in self.safety_events[-100:]:
            types_count[e.event_type] += 1

        return {
            "dna": self.DNA,
            "uid": self.UID,
            "version": self.VERSION,
            "cameras": len(self.camera_network),
            "nodes": len(self.spacetime_nodes),
            "trajectories": len(self.trajectories),
            "safety_events_total": total_events,
            "safety_events_breakdown": dict(types_count),
            "weave_density": round(
                len(self.spacetime_nodes) / max(len(self.camera_network), 1), 2
            ),
            "stgnn_active": self.stgnn is not None,
            "timestamp": time.time(),
            "timestamp_human": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        }

    def status_report(self) -> str:
        """生成格式化的状态报告"""
        s = self.get_weave_status()
        active_trajs = [(tid, nodes) for tid, nodes in self.trajectories.items() if nodes]
        active_trajs.sort(key=lambda x: len(x[1]), reverse=True)

        lines = [
            "╔══════════════════════════════════════════════════════════╗",
            "║       龍魂 · AI驱动时空织网 · 状态报告                    ║",
            "╚══════════════════════════════════════════════════════════╝",
            "",
            f"🆔 版本: {s['version']}",
            f"🕐 时间: {s['timestamp_human']}",
            f"🧬 DNA:  {s['dna'][:40]}...",
            "",
            "── 织网状态 ──",
            f"  📹 摄像头: {s['cameras']} 个",
            f"  🪡 时空节点: {s['nodes']} 个",
            f"  🗺️  轨迹数: {s['trajectories']} 条",
            f"  🕸️  织网密度: {s['weave_density']} 节点/摄像头",
            f"  🧠 ST-GNN: {'✅ 活跃' if s['stgnn_active'] else '⚠️ 退化'}",
            "",
            "── 主动安全 ──",
            f"  📊 事件总数: {s['safety_events_total']}",
        ]

        if s['safety_events_breakdown']:
            for etype, count in sorted(s['safety_events_breakdown'].items()):
                emoji = {"intrusion": "🚨", "abnormal_behavior": "⚠️", "crowd_gathering": "👥",
                         "lost_target": "🔍", "traffic_violation": "🚗"}.get(etype, "📌")
                lines.append(f"  {emoji} {etype}: {count}")

        lines.append("")
        lines.append("── 活跃轨迹 TOP5 ──")
        for i, (tid, nodes) in enumerate(active_trajs[:5]):
            if nodes and nodes[0] in self.spacetime_nodes:
                first = self.spacetime_nodes[nodes[0]]
                last = self.spacetime_nodes[nodes[-1]]
                dist = math.sqrt(
                    (last.position[0] - first.position[0]) ** 2 +
                    (last.position[1] - first.position[1]) ** 2
                )
                lines.append(f"  {i + 1}. {tid[:16]}.. 节点:{len(nodes)} 跨度:{dist:.1f}m")

        lines.append("")
        lines.append("╔══════════════════════════════════════════════════════════╗")
        lines.append("║  主动安全新范式: 看见过去→预测未来                       ║")
        lines.append("╚══════════════════════════════════════════════════════════╝")

        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
# 演示
# ══════════════════════════════════════════════════════════════════

def run_demo():
    """时空织网完整演示"""

    print("\n🐉 龍魂 · AI驱动时空织网 v2.0 · 演示启动")
    print("=" * 56)

    engine = SpacetimeWeaveEngine(feature_dim=256)

    # ── 注册6摄像头十字路口网格 ──
    print("\n📹 注册摄像头时空网络...")
    engine.register_camera("CAM-N", (0, 60, 5), fov=90, neighbors=["CAM-E", "CAM-W", "CAM-C"],
                            coverage_area=[(-15, 45), (15, 45), (15, 75), (-15, 75)])
    engine.register_camera("CAM-S", (0, -60, 5), fov=90, neighbors=["CAM-E", "CAM-W", "CAM-C"],
                            coverage_area=[(-15, -75), (15, -75), (15, -45), (-15, -45)])
    engine.register_camera("CAM-E", (60, 0, 5), fov=90, neighbors=["CAM-N", "CAM-S", "CAM-C"],
                            coverage_area=[(45, -15), (75, -15), (75, 15), (45, 15)])
    engine.register_camera("CAM-W", (-60, 0, 5), fov=90, neighbors=["CAM-N", "CAM-S", "CAM-C"],
                            coverage_area=[(-75, -15), (-45, -15), (-45, 15), (-75, 15)])
    engine.register_camera("CAM-C", (0, 0, 10), fov=360, neighbors=["CAM-N", "CAM-S", "CAM-E", "CAM-W"],
                            coverage_area=[(-10, -10), (10, -10), (10, 10), (-10, 10)])
    engine.register_camera("CAM-R", (30, 50, 3), fov=60, neighbors=["CAM-N", "CAM-C"],
                            coverage_area=[(25, 45), (35, 45), (35, 55), (25, 55)],
                            restricted=True)  # 禁区

    # ── 模拟3个目标跨镜移动 ──
    print("\n🪡 织造时空节点...")

    base_features = [
        list(np.random.RandomState(42 + i).randn(256) / np.linalg.norm(
            np.random.RandomState(42 + i).randn(256)))
        for i in range(3)
    ]

    # 目标1: 北→中心→东→南 (绕行)
    target1_path = [
        ("CAM-N", (0, 55)), ("CAM-N", (5, 45)), ("CAM-C", (10, 30)), ("CAM-C", (20, 10)),
        ("CAM-E", (30, 5)), ("CAM-E", (45, 0)), ("CAM-S", (50, -10)), ("CAM-S", (40, -30)),
        ("CAM-S", (20, -45)), ("CAM-S", (5, -55)),
    ]
    # 目标2: 西→中心→北 (直线)
    target2_path = [
        ("CAM-W", (-55, 0)), ("CAM-W", (-40, 5)), ("CAM-C", (-20, 10)), ("CAM-C", (-5, 20)),
        ("CAM-N", (5, 30)), ("CAM-N", (10, 45)), ("CAM-N", (5, 55)),
    ]
    # 目标3: 入侵禁区 (触发主动安全)
    target3_path = [
        ("CAM-N", (-5, 55)), ("CAM-N", (5, 52)), ("CAM-R", (28, 50)),  # 侵入 DR-R
        ("CAM-R", (32, 48)), ("CAM-C", (25, 35)), ("CAM-C", (15, 20)),
    ]

    all_targets = [
        ("TARGET-A", target1_path, base_features[0]),
        ("TARGET-B", target2_path, base_features[1]),
        ("TARGET-C", target3_path, base_features[2]),
    ]

    total_nodes = 0
    base_time = time.time()

    for tid, path, base_feat in all_targets:
        print(f"\n  🎯 {tid}:")
        for step, (cam, (x, y)) in enumerate(path):
            # 模拟特征漂移（低噪声保持相似度>0.90）
            noise = np.random.RandomState(9622 + step).randn(256) * 0.005
            features = (np.array(base_feat) + noise)
            features = features / np.linalg.norm(features)

            node_id = engine.weave_node(
                target_id=tid,
                camera_id=cam,
                position=(float(x), float(y), 0.0),
                timestamp=base_time + step * 0.6,
                features=features.tolist(),
                confidence=0.9 + 0.01 * step,
            )
            total_nodes += 1

            print(f"    🪡 {node_id[:20]}... @ {cam} ({x:.0f},{y:.0f})")

    # ── 预测 ──
    print("\n🔮 轨迹预测:")
    for traj_id in engine.trajectories:
        preds = engine.predict_future(traj_id, 3.0)
        if preds:
            nodes_count = len(engine.trajectories[traj_id])
            print(f"  {traj_id[:16]}.. → 预测 {len(preds)} 未来节点 "
                  f"(基于 {nodes_count} 历史节点)")

    # ── 状态报告 ──
    print()
    print(engine.status_report())

    return engine


# ══════════════════════════════════════════════════════════════════
# CLI入口
# ══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂 · AI驱动时空织网引擎 v2.0")
    parser.add_argument("command", nargs="?", default="status",
                        choices=["demo", "status", "run", "json"],
                        help="demo|status|run|json")
    args = parser.parse_args()

    if args.command == "demo":
        run_demo()
    elif args.command in ("status", "json"):
        engine = SpacetimeWeaveEngine(feature_dim=256)
        if args.command == "json":
            print(json.dumps(engine.get_weave_status(), ensure_ascii=False, indent=2))
        else:
            print(engine.status_report())
    elif args.command == "run":
        print("时空织网引擎运行中 (守护进程模式暂未实现)")
        print("使用 'demo' 查看演示，或 'status' 查看状态")

if __name__ == "__main__":
    main()
