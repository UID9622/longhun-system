#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    龍魂体系 · 流场协同引擎 v1.0                                ║
║═══════════════════════════════════════════════════════════════════════════════║
║ #龍芯⚡️2026-07-07-FLOWFIELD-COLLAB-ENGINE-v1.0                                ║
║ UID9622 · 龍芯北辰 · 诸葛鑫                                                   ║
║ 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                                     ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ 核心链路:                                                                      ║
║   多人格/多智能体 → 五行向量场 → 流场融合 → 冲突检测 → 协同决策 → 任务分解     ║
║                                                                                ║
║ 四大引擎:                                                                      ║
║   1. WuxingCollabField      — 五行协同向量场·多人格注册与五行标注              ║
║   2. FlowFieldFusionEngine  — 流场融合·多人格流场合并·协同指数计算             ║
║   3. CollabConflictDetector — 协同冲突检测·相克预警·相容性矩阵                  ║
║   4. CollabTaskDistributor  — 协同任务分解·五行互补任务分配·负载均衡            ║
║                                                                                ║
║ 上游对接: CNSH-FLOW-CORE v3.0 · five_values_unified_engine · 人格路由v3.0      ║
║ 下游对接: orchestrator.py · neural_agent_bridge · MCP自适应引擎v4.0            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 0. 常量与枚举
# ═══════════════════════════════════════════════════════════════════════════════

DNA = "#龍芯⚡️2026-07-07-FLOWFIELD-COLLAB-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
VERSION = "v1.0"

ROOT = Path(__file__).resolve().parent.parent.parent


class WuxingElement(Enum):
    """五行元素"""
    WATER = "水"
    FIRE = "火"
    WOOD = "木"
    METAL = "金"
    EARTH = "土"


class CollabRole(Enum):
    """协同角色类型"""
    COMMANDER = "总指挥"      # 决策者·土
    STRATEGIST = "战略师"     # 规划者·木
    EXECUTOR = "执行者"       # 实干者·火
    AUDITOR = "审计者"        # 守门人·金
    MEMORIZER = "记忆官"      # 归档者·水
    BRIDGE = "桥接者"         # 协调人·土+水
    GUARDIAN = "守护者"       # 安全盾·金+火
    OBSERVER = "观察员"       # 旁观·水+木


class CollabMode(Enum):
    """协同模式"""
    PARALLEL = "并行"      # 多人并行执行不同任务
    PIPELINE = "流水线"    # 串行传递·上家输出下家输入
    CONSENSUS = "共识"     # 多人表决·多数/全票通过
    DELEGATION = "委派"    # 主控委派·接收方全权执行
    FUSION = "融合"        # 多人流场合一·统一输出
    WATCHDOG = "监察"      # 一主多监·监方有否决权


# ── 五行关系矩阵 ──
SHENG = {  # 相生：A生B
    WuxingElement.METAL: WuxingElement.WATER,
    WuxingElement.WATER: WuxingElement.WOOD,
    WuxingElement.WOOD: WuxingElement.FIRE,
    WuxingElement.FIRE: WuxingElement.EARTH,
    WuxingElement.EARTH: WuxingElement.METAL,
}
KE = {  # 相克：A克B
    WuxingElement.METAL: WuxingElement.WOOD,
    WuxingElement.WOOD: WuxingElement.EARTH,
    WuxingElement.EARTH: WuxingElement.WATER,
    WuxingElement.WATER: WuxingElement.FIRE,
    WuxingElement.FIRE: WuxingElement.METAL,
}
BEI_SHENG = {v: k for k, v in SHENG.items()}  # 被生
BEI_KE = {v: k for k, v in KE.items()}  # 被克

# 数字根→五行（与 CNSH-FLOW-CORE v3.0 对齐）
DR_WUXING: Dict[int, WuxingElement] = {
    1: WuxingElement.WATER, 2: WuxingElement.FIRE,
    3: WuxingElement.WOOD,  4: WuxingElement.METAL,
    5: WuxingElement.EARTH, 6: WuxingElement.WATER,
    7: WuxingElement.FIRE,  8: WuxingElement.WOOD,
    9: WuxingElement.METAL, 0: WuxingElement.EARTH,
}

# 五行视觉色（与 CNSH-FLOW-CORE v3.0 对齐）
WUXING_COLORS = {
    WuxingElement.METAL: "#C9A84C",
    WuxingElement.WATER: "#2E6B8A",
    WuxingElement.WOOD: "#3D7A4A",
    WuxingElement.FIRE: "#B83A2A",
    WuxingElement.EARTH: "#A08050",
}

# 角色→推荐五行
ROLE_WUXING = {
    CollabRole.COMMANDER: [WuxingElement.EARTH],
    CollabRole.STRATEGIST: [WuxingElement.WOOD, WuxingElement.WATER],
    CollabRole.EXECUTOR: [WuxingElement.FIRE],
    CollabRole.AUDITOR: [WuxingElement.METAL],
    CollabRole.MEMORIZER: [WuxingElement.WATER],
    CollabRole.BRIDGE: [WuxingElement.EARTH, WuxingElement.WATER],
    CollabRole.GUARDIAN: [WuxingElement.METAL, WuxingElement.FIRE],
    CollabRole.OBSERVER: [WuxingElement.WATER, WuxingElement.WOOD],
}

# 三才默认权重（与 CNSH-FLOW-CORE v3.0 对齐）
SANCAI_DEFAULT = {"heaven": 0.35, "earth": 0.15, "human": 0.50}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. 协同流场节点
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class CollabNode:
    """
    协同流场中的单个节点（一个人格/智能体/数字人）

    核心属性:
    - wuxing: 本节点的五行属性
    - energy: 当前能量值 (0-100)
    - role: 协同角色
    - values_weight: 五大核心价值观权重 {"根":0.3,"魂":0.5,...}
    - trust: 信任度 (0-1)
    - active: 是否激活参与协同
    """
    id: str
    name: str
    wuxing: WuxingElement
    digital_root: int
    energy: float = 50.0
    role: Optional[CollabRole] = None
    persona_id: Optional[str] = None
    values_weight: Dict[str, float] = field(default_factory=dict)
    sancai: Dict[str, float] = field(default_factory=lambda: dict(SANCAI_DEFAULT))
    trust: float = 0.8
    active: bool = True
    _node_dna: str = ""

    def __post_init__(self):
        if not self._node_dna:
            hash8 = hashlib.sha256(f"{self.id}{self.name}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
            self._node_dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-COLLAB-NODE-{hash8}"

    def get_key(self) -> str:
        return self.id

    def get_flow_vector(self) -> Dict[str, Any]:
        """生成单个节点的流场向量（与 CNSH-FLOW-CORE 对齐）"""
        return {
            "node_id": f"COLLAB-{self.id}-{datetime.now().strftime('%Y%m%d')}",
            "name": self.name,
            "wuxing": self.wuxing.value,
            "digital_root": self.digital_root,
            "energy": self.energy,
            "role": self.role.value if self.role else "N/A",
            "sancai": self.sancai,
            "trust": self.trust,
            "dna": self._node_dna,
            "visual": {"color": WUXING_COLORS.get(self.wuxing, "#888")},
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "wuxing": self.wuxing.value,
            "digital_root": self.digital_root,
            "energy": self.energy,
            "role": self.role.value if self.role else None,
            "persona_id": self.persona_id,
            "values_weight": self.values_weight,
            "sancai": self.sancai,
            "trust": self.trust,
            "active": self.active,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 五行协同向量场
# ═══════════════════════════════════════════════════════════════════════════════


class WuxingCollabField:
    """
    五行协同向量场

    管理多个协同节点的注册、五行标注、能量更新。
    作为流场协同的基础数据层。
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.nodes: Dict[str, CollabNode] = {}
        self._history: List[Dict[str, Any]] = []

    def register(self, node: CollabNode) -> str:
        """注册协同节点"""
        key = node.get_key()
        self.nodes[key] = node
        self._history.append({
            "action": "register",
            "node": key,
            "name": node.name,
            "wuxing": node.wuxing.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return key

    def remove(self, node_id: str) -> bool:
        if node_id in self.nodes:
            self._history.append({
                "action": "remove",
                "node": node_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            del self.nodes[node_id]
            return True
        return False

    def get_active_nodes(self) -> List[CollabNode]:
        return [n for n in self.nodes.values() if n.active]

    def get_wuxing_distribution(self) -> Dict[str, int]:
        """获取激活节点的五行分布"""
        dist = {e.value: 0 for e in WuxingElement}
        for node in self.get_active_nodes():
            dist[node.wuxing.value] += 1
        return dist

    def get_wuxing_energy_sum(self) -> Dict[str, float]:
        """获取各五行能量总和"""
        energy = {e.value: 0.0 for e in WuxingElement}
        for node in self.get_active_nodes():
            energy[node.wuxing.value] += node.energy
        return energy

    def get_team_balance_score(self) -> Tuple[float, str]:
        """
        计算团队五行均衡指数 (0-100)
        使用 CV 均衡法：均衡度 = 1 - σ/μ
        """
        dist = self.get_wuxing_distribution()
        values = [v for v in dist.values()]
        mean = sum(values) / max(len(values), 1)
        if mean == 0:
            return 0.0, "🔴 无活跃节点"
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance)
        cv = std / mean if mean > 0 else 1.0
        balance = max(0, 100 * (1 - cv))

        if balance >= 70:
            status = "🟢 五行均衡"
        elif balance >= 40:
            status = "🟡 偏重"
        else:
            status = "🔴 严重失衡"
        return round(balance, 2), status

    def suggest_complement(self) -> List[Dict[str, Any]]:
        """
        建议五行补位——分析缺失/过弱的五行，推荐补充角色
        """
        active = self.get_active_nodes()
        if len(active) < 2:
            return []

        dist = self.get_wuxing_distribution()
        total = sum(dist.values())
        suggestions = []

        for elem in WuxingElement:
            count = dist[elem.value]
            ratio = count / max(total, 1)
            if ratio == 0:
                suggestions.append({
                    "wuxing": elem.value,
                    "severity": "🔴 缺失",
                    "recommend_role": [r.value for r in CollabRole if elem in ROLE_WUXING.get(r, [])],
                    "reason": f"团队缺少{elem.value}行，可能导致{GENERATE_REASON(elem)}",
                })
            elif ratio < 0.15:
                suggestions.append({
                    "wuxing": elem.value,
                    "severity": "🟡 偏弱",
                    "recommend_role": [r.value for r in CollabRole if elem in ROLE_WUXING.get(r, [])],
                    "reason": f"{elem.value}行仅占{ratio:.0%}，建议加强",
                })

        return suggestions

    def to_report(self) -> Dict[str, Any]:
        """导出协同向量场完整报告"""
        balance_score, balance_status = self.get_team_balance_score()
        return {
            "field_name": self.name,
            "node_count": len(self.nodes),
            "active_count": len(self.get_active_nodes()),
            "wuxing_distribution": self.get_wuxing_distribution(),
            "wuxing_energy_sum": self.get_wuxing_energy_sum(),
            "team_balance": {"score": balance_score, "status": balance_status},
            "complement_suggestions": self.suggest_complement(),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "dna": DNA,
        }


def GENERATE_REASON(elem: WuxingElement) -> str:
    reasons = {
        WuxingElement.METAL: "规则断层·无审计·无边界",
        WuxingElement.WATER: "记忆断层·无追溯·无归档",
        WuxingElement.WOOD: "增长断层·无创新·无扩展",
        WuxingElement.FIRE: "动力断层·无执行·无热情",
        WuxingElement.EARTH: "根基断层·无承载·无中心",
    }
    return reasons.get(elem, "五行缺失")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 流场融合引擎
# ═══════════════════════════════════════════════════════════════════════════════


class FlowFieldFusionEngine:
    """
    流场融合引擎

    将多个协同节点的流场向量融合为统一的协同流场。
    输出：融合指数、协同强度、集体三才权重、五行合力向量。
    """

    def __init__(self, collab_field: WuxingCollabField):
        self.field = collab_field
        self._last_fusion: Optional[Dict[str, Any]] = None

    def compute_fusion(self) -> Dict[str, Any]:
        """
        计算多人格流场融合结果

        核心算法：
        1. 各节点流场向量加权平均 → 集体流场向量
        2. 五行生克链计算集体合力
        3. 三才权重融合（人场守卫：集体人场≥0.34）
        4. 协同指数 = 平衡度 × 信任度 × 能量充足度
        """
        active = self.field.get_active_nodes()
        n = len(active)
        if n == 0:
            return {"status": "empty", "fusion_index": 0.0}

        # ── 1. 加权平均：集体流场向量 ──
        # 五行能量分布
        collective_energy = {e.value: 0.0 for e in WuxingElement}
        for node in active:
            collective_energy[node.wuxing.value] += node.energy

        # 归一化
        total_energy = sum(collective_energy.values())
        if total_energy > 0:
            collective_energy = {k: round(v / total_energy, 4) for k, v in collective_energy.items()}

        # 集体主导五行
        dom_wuxing = max(collective_energy, key=collective_energy.get)  # type: ignore[reportArgumentType]

        # ── 2. 三才融合 ──
        fused_sancai = {"heaven": 0.0, "earth": 0.0, "human": 0.0}
        total_trust = sum(n.trust for n in active)
        for node in active:
            w = node.trust / max(total_trust, 0.01)
            fused_sancai["heaven"] += node.sancai.get("heaven", 0.35) * w
            fused_sancai["earth"] += node.sancai.get("earth", 0.15) * w
            fused_sancai["human"] += node.sancai.get("human", 0.50) * w

        # 人场守卫：不低于 0.34
        if fused_sancai["human"] < 0.34:
            fused_sancai["human"] = 0.34
            # 从天场扣除
            excess = 0.34 - fused_sancai["human"]
            if fused_sancai["heaven"] > excess:
                fused_sancai["heaven"] -= excess
            else:
                fused_sancai["earth"] -= (excess - fused_sancai["heaven"])
                fused_sancai["heaven"] = 0.05

        # ── 3. 五行合力向量（相生链传播计算） ──
        forces = self._compute_collective_forces(active)

        # ── 4. 协同指数 ──
        balance_score, _ = self.field.get_team_balance_score()
        avg_trust = sum(n.trust for n in active) / max(n, 1)
        energy_adequacy = min(1.0, total_energy / (n * 50))
        fusion_index = round(
            (balance_score / 100) * 0.4 + avg_trust * 0.35 + energy_adequacy * 0.25, 4
        )

        if fusion_index >= 0.7:
            fusion_status = "🟢 高协同"
        elif fusion_index >= 0.4:
            fusion_status = "🟡 中等协同"
        else:
            fusion_status = "🔴 低协同·建议调整团队"

        self._last_fusion = {
            "node_count": n,
            "collective_energy": collective_energy,
            "dominant_wuxing": dom_wuxing,
            "fused_sancai": fused_sancai,
            "collective_forces": forces,
            "fusion_index": fusion_index,
            "fusion_status": fusion_status,
            "dna": DNA,
        }
        return self._last_fusion

    def _compute_collective_forces(self, nodes: List[CollabNode]) -> Dict[str, float]:
        """计算五行协同合力向量（生克链传播）"""
        # 按五行分组
        by_wuxing: Dict[WuxingElement, List[CollabNode]] = defaultdict(list)
        for node in nodes:
            by_wuxing[node.wuxing].append(node)

        forces = {"sheng_flow": 0.0, "ke_tension": 0.0, "harmony": 0.0, "creative": 0.0}

        elem_order = [
            WuxingElement.METAL, WuxingElement.WATER,
            WuxingElement.WOOD, WuxingElement.FIRE, WuxingElement.EARTH,
        ]

        for elem in elem_order:
            sheng_target = SHENG.get(elem)
            ke_target = KE.get(elem)

            cur_energy = sum(n.energy for n in by_wuxing.get(elem, []))

            # 相生传播：当前行流向下一行
            if sheng_target and by_wuxing.get(sheng_target):
                target_energy = sum(n.energy for n in by_wuxing[sheng_target])
                forces["sheng_flow"] += min(cur_energy, target_energy) / max(cur_energy + target_energy, 1)

            # 相克张力：过旺的克方会压制被克方
            if ke_target and by_wuxing.get(ke_target):
                target_energy = sum(n.energy for n in by_wuxing[ke_target])
                if cur_energy > target_energy * 1.5:
                    forces["ke_tension"] += (cur_energy - target_energy) / max(cur_energy, 1)

        # 生克和谐度 = 生流 - 克张
        total = max(forces["sheng_flow"] + forces["ke_tension"], 0.01)
        forces["harmony"] = round(max(0, forces["sheng_flow"] / total), 4)
        forces["creative"] = round(forces["sheng_flow"] * 0.7 + (1 - forces["ke_tension"]) * 0.3, 4)

        return forces


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 协同冲突检测器
# ═══════════════════════════════════════════════════════════════════════════════


class CollabConflictDetector:
    """
    协同冲突检测器

    检测多节点之间的五行冲突、角色冲突、价值观冲突、信任风险。
    输出冲突矩阵 + 相容性评分 + 预警清单。
    """

    def __init__(self, collab_field: WuxingCollabField):
        self.field = collab_field
        self.conflicts: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

    def detect_all(self) -> Dict[str, Any]:
        """全量检测"""
        active = self.field.get_active_nodes()
        n = len(active)
        self.conflicts = []
        self.warnings = []

        if n < 2:
            return self._empty_result()

        # ── 1. 五行相克冲突 ──
        compatibility_matrix = {}
        for i, a in enumerate(active):
            for j, b in enumerate(active):
                if i >= j:
                    continue
                pair_key = f"{a.name}↔{b.name}"

                # 相克检测
                ke_score = self._ke_conflict_score(a, b)
                # 相生检测
                sheng_score = self._sheng_harmony_score(a, b)
                # 比和检测
                bihe = a.wuxing == b.wuxing

                compat = round(sheng_score * 0.6 + (1 - ke_score) * 0.4, 4)
                compatibility_matrix[pair_key] = {
                    "a": a.name, "a_wuxing": a.wuxing.value,
                    "b": b.name, "b_wuxing": b.wuxing.value,
                    "ke_tension": ke_score,
                    "sheng_harmony": sheng_score,
                    "bihe": bihe,
                    "compatibility": compat,
                    "status": "🟢 相容" if compat >= 0.65 else "🟡 需关注" if compat >= 0.4 else "🔴 冲突",
                }

                if compat < 0.4:
                    self.conflicts.append({
                        "type": "wuxing_ke",
                        "pair": pair_key,
                        "severity": "🔴",
                        "detail": f"{a.name}({a.wuxing.value})克{b.name}({b.wuxing.value})·相容性{compat:.2f}",
                        "suggestion": self._ke_remedy_suggestion(a, b),
                    })
                elif compat < 0.55:
                    self.warnings.append({
                        "type": "wuxing_tension",
                        "pair": pair_key,
                        "severity": "🟡",
                        "detail": f"{a.name}({a.wuxing.value})与{b.name}({b.wuxing.value})存在张力·相容性{compat:.2f}",
                    })

        # ── 2. 角色冲突 ──
        self._detect_role_conflicts(active)

        # ── 3. 信任风险 ──
        self._detect_trust_risks(active)

        # ── 4. 能量极差 ──
        energies = [n.energy for n in active]
        energy_range = max(energies) - min(energies)
        if energy_range > 60:
            self.warnings.append({
                "type": "energy_imbalance",
                "severity": "🟡",
                "detail": f"能量极差{energy_range:.0f}·高能量节点可能主导决策",
            })

        return {
            "node_count": n,
            "conflict_count": len(self.conflicts),
            "warning_count": len(self.warnings),
            "conflicts": self.conflicts,
            "warnings": self.warnings,
            "compatibility_matrix": compatibility_matrix,
            "overall_status": "🔴 存在冲突" if self.conflicts else "🟡 存在预警" if self.warnings else "🟢 相容",
            "dna": DNA,
        }

    def _ke_conflict_score(self, a: CollabNode, b: CollabNode) -> float:
        """计算五行相克冲突分 (0=无冲突, 1=严重冲突)"""
        if KE.get(a.wuxing) == b.wuxing:
            # a 克 b
            ratio = a.energy / max(b.energy, 1)
            return min(1.0, ratio * 0.8)
        elif KE.get(b.wuxing) == a.wuxing:
            # b 克 a
            ratio = b.energy / max(a.energy, 1)
            return min(1.0, ratio * 0.8)
        return 0.0

    def _sheng_harmony_score(self, a: CollabNode, b: CollabNode) -> float:
        """计算五行相生和谐分"""
        if SHENG.get(a.wuxing) == b.wuxing:
            # a 生 b → 高和谐
            return 0.9
        elif SHENG.get(b.wuxing) == a.wuxing:
            # b 生 a → 中等和谐
            return 0.75
        elif a.wuxing == b.wuxing:
            # 比和 → 同类合并
            return 0.85
        return 0.5  # 无直接关系

    def _ke_remedy_suggestion(self, a: CollabNode, b: CollabNode) -> str:
        """五行相克补救建议"""
        remedies = {
            (WuxingElement.METAL, WuxingElement.WOOD): "引入水行桥接者（金生水·水生木）或降低金行决策权重",
            (WuxingElement.WOOD, WuxingElement.EARTH): "引入火行执行者（木生火·火生土）或增加土行资源",
            (WuxingElement.EARTH, WuxingElement.WATER): "引入金行审计者（土生金·金生水）或降低土行约束",
            (WuxingElement.WATER, WuxingElement.FIRE): "引入木行战略师（水生木·木生火）或降低水行压制",
            (WuxingElement.FIRE, WuxingElement.METAL): "引入土行总指挥（火生土·土生金）或降低火行强度",
        }
        return remedies.get((a.wuxing, b.wuxing), "建议引入第三方桥接角色缓冲")

    def _detect_role_conflicts(self, nodes: List[CollabNode]):
        """检测角色冲突"""
        role_count = defaultdict(int)
        for n in nodes:
            if n.role:
                role_count[n.role.value] += 1
        for role, count in role_count.items():
            if count > 2 and role in ["总指挥", "审计者"]:
                self.warnings.append({
                    "type": "role_duplicate",
                    "severity": "🟡",
                    "detail": f"角色「{role}」有{count}人·建议单一负责人",
                })

    def _detect_trust_risks(self, nodes: List[CollabNode]):
        """检测信任风险"""
        low_trust = [n for n in nodes if n.trust < 0.5]
        for n in low_trust:
            self.warnings.append({
                "type": "low_trust",
                "severity": "🟡" if n.trust >= 0.3 else "🔴",
                "detail": f"{n.name}信任度仅{n.trust:.2f}·建议降低其决策权重",
            })

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "node_count": 0, "conflict_count": 0, "warning_count": 0,
            "conflicts": [], "warnings": [],
            "compatibility_matrix": {},
            "overall_status": "N/A",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 协同任务分解器
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class CollabTask:
    """协同任务"""
    id: str
    title: str
    description: str = ""
    required_wuxing: List[WuxingElement] = field(default_factory=list)
    required_role: Optional[CollabRole] = None
    mode: CollabMode = CollabMode.PARALLEL
    priority: int = 3
    estimated_energy: float = 30.0
    assigned_to: List[str] = field(default_factory=list)
    status: str = "pending"


class CollabTaskDistributor:
    """
    协同任务分解器

    根据五行互补原则和节点能量，将协同任务智能分配给最合适的节点。
    """

    def __init__(self, collab_field: WuxingCollabField):
        self.field = collab_field
        self.task_queue: List[CollabTask] = []

    def add_task(self, task: CollabTask) -> None:
        self.task_queue.append(task)

    def auto_assign(self, task: CollabTask) -> Dict[str, Any]:
        """
        自动匹配任务→协同节点

        优先级算法：
        1. 五行匹配度（required_wuxing 与节点五行一致 = +30分）
        2. 角色匹配度（required_role 与节点角色一致 = +25分）
        3. 能量充足度（节点剩余能量 = +20分）
        4. 信任度（trust = +15分）
        5. 负载均衡（未被分配过的节点优先 = +10分）
        """
        active = self.field.get_active_nodes()
        if not active:
            return {"status": "fail", "reason": "无可用协同节点"}

        scores = []
        for node in active:
            score = 0.0

            # 五行匹配
            if task.required_wuxing and node.wuxing in task.required_wuxing:
                score += 30
            elif not task.required_wuxing:
                score += 15  # 无要求则均分

            # 角色匹配
            if task.required_role and node.role == task.required_role:
                score += 25

            # 能量充足度
            energy_ratio = node.energy / 100
            if energy_ratio >= 0.5:
                score += 20 * energy_ratio
            else:
                score += 5  # 低能量惩罚

            # 信任度
            score += 15 * node.trust

            # 负载均衡
            assigned_count = sum(1 for t in self.task_queue if node.id in t.assigned_to)
            if assigned_count == 0:
                score += 10

            scores.append((node, score))

        # 按模式分配
        if task.mode in (CollabMode.PARALLEL, CollabMode.CONSENSUS):
            # 并行/共识：分配给所有高分节点（前3）
            ranked = sorted(scores, key=lambda x: x[1], reverse=True)
            selected = [r[0] for r in ranked[:3]]
        elif task.mode == CollabMode.PIPELINE:
            # 流水线：按五行相生顺序分配
            selected = self._pipeline_assign(scores, task)
        elif task.mode == CollabMode.DELEGATION:
            # 委派：只分配给最高分节点
            best = max(scores, key=lambda x: x[1])
            selected = [best[0]]
        elif task.mode == CollabMode.WATCHDOG:
            # 监察：高分执行 + 金行审计
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            executor = sorted_scores[0][0] if sorted_scores else None
            auditor = next(
                (n for n, s in scores if n.wuxing == WuxingElement.METAL and n.id != (executor.id if executor else "")),
                None,
            )
            selected = [n for n in [executor, auditor] if n]
        else:
            # 融合：所有激活节点
            selected = [n for n, _ in scores]

        task.assigned_to = [n.id for n in selected]
        task.status = "assigned"

        return {
            "task_id": task.id,
            "mode": task.mode.value,
            "assigned_to": [{"id": n.id, "name": n.name, "score": round(s, 1)}
                            for n, s in scores if n in selected],
            "all_scores": [{"id": n.id, "name": n.name, "score": round(s, 1), "wuxing": n.wuxing.value}
                           for n, s in sorted(scores, key=lambda x: x[1], reverse=True)],
            "dna": DNA,
        }

    def _pipeline_assign(self, scores: List[Tuple[CollabNode, float]],
                         task: CollabTask) -> List[CollabNode]:
        """流水线模式：按五行相生顺序分配"""
        wuxing_order = [WuxingElement.METAL, WuxingElement.WATER,
                        WuxingElement.WOOD, WuxingElement.FIRE, WuxingElement.EARTH]
        selected = []
        for wx in wuxing_order:
            candidates = [(n, s) for n, s in scores if n.wuxing == wx and n.id not in [x.id for x in selected]]
            if candidates:
                best = max(candidates, key=lambda x: x[1])
                selected.append(best[0])
            if len(selected) >= 4:
                break
        return selected

    def get_collab_plan(self) -> Dict[str, Any]:
        """获取完整协同计划"""
        return {
            "pending_tasks": len([t for t in self.task_queue if t.status == "pending"]),
            "assigned_tasks": len([t for t in self.task_queue if t.status == "assigned"]),
            "tasks": [
                {
                    "id": t.id, "title": t.title, "mode": t.mode.value,
                    "priority": t.priority, "assigned_to": t.assigned_to, "status": t.status,
                }
                for t in self.task_queue
            ],
            "dna": DNA,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 6. 默认数字人/人格注册表（预配置）
# ═══════════════════════════════════════════════════════════════════════════════

def create_default_collab_field() -> WuxingCollabField:
    """
    创建预配置的默认协同向量场
    包含 6 大核心数字人 + MCP 引擎 5 人格
    """
    field = WuxingCollabField("龍魂核心协同场")

    # ── 6 大核心数字人 ──
    personas = [
        # id, name, wuxing, dr, energy, role, trust
        ("master", "主身份", WuxingElement.EARTH, 5, 85.0, CollabRole.COMMANDER, 1.0),
        ("wuxin", "文心P00", WuxingElement.FIRE, 2, 75.0, CollabRole.STRATEGIST, 0.95),
        ("longxin", "龍芯P02", WuxingElement.METAL, 4, 80.0, CollabRole.EXECUTOR, 0.98),
        ("godseye", "上帝之眼P05", WuxingElement.METAL, 9, 78.0, CollabRole.AUDITOR, 0.95),
        ("heiangel", "黑天使P77", WuxingElement.WATER, 1, 72.0, CollabRole.GUARDIAN, 0.92),
        ("zenglaoshi", "曾老师", WuxingElement.WATER, 6, 80.0, CollabRole.STRATEGIST, 0.96),
    ]

    for pid, pname, wx, dr, energy, role, trust in personas:
        node = CollabNode(
            id=pid, name=pname, wuxing=wx, digital_root=dr,
            energy=energy, role=role, persona_id=pid, trust=trust,
        )
        node.values_weight = PERSONA_VALUES.get(pid, {})
        field.register(node)

    # ── MCP 引擎 5 人格 ──
    mcp_personas = [
        ("wenwen", "雯雯P03", WuxingElement.METAL, 4, 65.0, CollabRole.MEMORIZER, 0.9),
        ("baobao_p72", "宝宝P72·龍盾", WuxingElement.EARTH, 5, 82.0, CollabRole.GUARDIAN, 0.97),
        ("scout", "侦察兵", WuxingElement.FIRE, 7, 60.0, CollabRole.OBSERVER, 0.85),
        ("architect", "架构师", WuxingElement.WOOD, 3, 68.0, CollabRole.STRATEGIST, 0.88),
        ("syncer", "同步官", WuxingElement.WATER, 6, 55.0, CollabRole.BRIDGE, 0.82),
    ]

    for pid, pname, wx, dr, energy, role, trust in mcp_personas:
        node = CollabNode(
            id=pid, name=pname, wuxing=wx, digital_root=dr,
            energy=energy, role=role, persona_id=pid, trust=trust,
        )
        field.register(node)

    return field


# 五大核心价值观权重（与 five_values_unified_engine.py 对齐）
PERSONA_VALUES = {
    "master": {"根": 0.30, "魂": 0.35, "信": 0.20, "爱": 0.10, "传": 0.05},
    "wuxin": {"根": 0.15, "魂": 0.35, "信": 0.25, "爱": 0.15, "传": 0.10},
    "longxin": {"根": 0.10, "魂": 0.30, "信": 0.35, "爱": 0.10, "传": 0.15},
    "godseye": {"根": 0.05, "魂": 0.20, "信": 0.50, "爱": 0.05, "传": 0.20},
    "heiangel": {"根": 0.10, "魂": 0.30, "信": 0.35, "爱": 0.05, "传": 0.20},
    "zenglaoshi": {"根": 0.40, "魂": 0.15, "信": 0.20, "爱": 0.15, "传": 0.10},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 7. 自测
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests() -> Dict[str, bool]:
    results = {}
    print("=" * 60)
    print("🐉 流场协同引擎 v1.0 · 自检验证")
    print("=" * 60)

    # ── 测试1: 默认协同场注册 ──
    print("\n🧪 测试1: 默认协同场初始化")
    field = create_default_collab_field()
    assert len(field.nodes) == 11, f"期望11个节点，实际{len(field.nodes)}"
    active = field.get_active_nodes()
    print(f"   ✅ 注册 {len(field.nodes)} 个节点 · 激活 {len(active)} 个")
    results["test1_init"] = True

    # ── 测试2: 五行分布 ──
    print("\n🧪 测试2: 五行分布")
    dist = field.get_wuxing_distribution()
    for elem, count in dist.items():
        print(f"   {elem}: {count}人")
    total = sum(dist.values())
    assert total == 11, f"总人数应为11，实际{total}"
    results["test2_distribution"] = True

    # ── 测试3: 团队均衡指数 ──
    print("\n🧪 测试3: 团队均衡指数")
    balance, status = field.get_team_balance_score()
    print(f"   均衡指数: {balance} · 状态: {status}")
    assert balance > 0, "均衡指数应>0"
    results["test3_balance"] = True

    # ── 测试4: 五行补位建议 ──
    print("\n🧪 测试4: 五行补位建议")
    suggestions = field.suggest_complement()
    if suggestions:
        for s in suggestions:
            print(f"   {s['severity']} {s['wuxing']}: {s['reason']}")
    else:
        print("   ✅ 无缺失·五行齐全")
    results["test4_complement"] = True

    # ── 测试5: 流场融合 ──
    print("\n🧪 测试5: 流场融合")
    fusion = FlowFieldFusionEngine(field)
    result = fusion.compute_fusion()
    print(f"   融合指数: {result['fusion_index']:.4f} · {result['fusion_status']}")
    print(f"   主导五行: {result['dominant_wuxing']}")
    print(f"   融合三才: 天{result['fused_sancai']['heaven']:.2f} "
          f"地{result['fused_sancai']['earth']:.2f} "
          f"人{result['fused_sancai']['human']:.2f}")
    print(f"   合力向量: 生流{result['collective_forces']['sheng_flow']:.3f} "
          f"克张{result['collective_forces']['ke_tension']:.3f} "
          f"和谐度{result['collective_forces']['harmony']:.3f}")
    assert result['fusion_index'] > 0, "融合指数应>0"
    assert result['fused_sancai']['human'] >= 0.34, "人场不应低于0.34"
    results["test5_fusion"] = True

    # ── 测试6: 冲突检测 ──
    print("\n🧪 测试6: 冲突检测")
    detector = CollabConflictDetector(field)
    conflicts = detector.detect_all()
    print(f"   冲突数: {conflicts['conflict_count']} · 预警数: {conflicts['warning_count']}")
    print(f"   总体状态: {conflicts['overall_status']}")
    for c in conflicts['conflicts']:
        print(f"   🔴 {c['detail']} → {c['suggestion']}")
    for w in conflicts['warnings']:
        print(f"   🟡 {w['detail']}")
    compat_count = len(conflicts['compatibility_matrix'])
    print(f"   相容性矩阵: {compat_count} 对关系")
    results["test6_conflicts"] = True

    # ── 测试7: 任务分配 ──
    print("\n🧪 测试7: 协同任务分配")
    distributor = CollabTaskDistributor(field)

    # 7a: 安全审计任务 → 金行优先
    task1 = CollabTask(
        id="T001", title="全系统安全审计",
        required_wuxing=[WuxingElement.METAL],
        required_role=CollabRole.AUDITOR,
        mode=CollabMode.WATCHDOG, priority=1,
    )
    r1 = distributor.auto_assign(task1)
    print(f"   任务T001(审计): 分配 → {', '.join(a['name'] for a in r1['assigned_to'])}")
    assert len(r1['assigned_to']) >= 1
    results["test7a_audit_assign"] = True

    # 7b: 创意任务 → 木行优先
    task2 = CollabTask(
        id="T002", title="新架构设计",
        required_wuxing=[WuxingElement.WOOD],
        required_role=CollabRole.STRATEGIST,
        mode=CollabMode.PARALLEL, priority=2,
    )
    r2 = distributor.auto_assign(task2)
    print(f"   任务T002(设计): 分配 → {', '.join(a['name'] for a in r2['assigned_to'])}")
    results["test7b_design_assign"] = True

    # 7c: 流水线任务
    task3 = CollabTask(
        id="T003", title="构建-审计-部署",
        required_wuxing=[WuxingElement.METAL, WuxingElement.FIRE],
        mode=CollabMode.PIPELINE, priority=1,
    )
    r3 = distributor.auto_assign(task3)
    print(f"   任务T003(流水线): 分配 → {', '.join(a['name'] for a in r3['assigned_to'])}")
    results["test7c_pipeline_assign"] = True

    # ── 测试8: 小团队协同（仅3人） ──
    print("\n🧪 测试8: 三人小团队协同")
    small_field = WuxingCollabField("三人小队")
    small_field.register(CollabNode("s1", "指挥", WuxingElement.EARTH, 5, 80, CollabRole.COMMANDER, 0.95))  # type: ignore[reportArgumentType]
    small_field.register(CollabNode("s2", "执行", WuxingElement.FIRE, 2, 70, CollabRole.EXECUTOR, 0.9))  # type: ignore[reportArgumentType]
    small_field.register(CollabNode("s3", "守护", WuxingElement.METAL, 4, 75, CollabRole.AUDITOR, 0.92))  # type: ignore[reportArgumentType]

    balance3, status3 = small_field.get_team_balance_score()
    print(f"   均衡指数: {balance3} · {status3}")
    sugg3 = small_field.suggest_complement()
    for s in sugg3:
        print(f"   建议补充: {s['severity']} {s['wuxing']}·{s['reason']}")

    fusion3 = FlowFieldFusionEngine(small_field).compute_fusion()
    print(f"   融合指数: {fusion3['fusion_index']:.4f} · {fusion3['fusion_status']}")
    assert len(sugg3) > 0, "三人团队应有补位建议（缺木和水）"
    results["test8_small_team"] = True

    # ── 测试9: 角色冲突团队 ──
    print("\n🧪 测试9: 角色冲突检测")
    conflict_field = WuxingCollabField("冲突测试")
    conflict_field.register(CollabNode("c1", "审计甲", WuxingElement.METAL, 4, 80, CollabRole.AUDITOR, 0.9))  # type: ignore[reportArgumentType]
    conflict_field.register(CollabNode("c2", "审计乙", WuxingElement.METAL, 9, 75, CollabRole.AUDITOR, 0.85))  # type: ignore[reportArgumentType]
    conflict_field.register(CollabNode("c3", "审计丙", WuxingElement.METAL, 4, 70, CollabRole.AUDITOR, 0.8))  # type: ignore[reportArgumentType]
    cd = CollabConflictDetector(conflict_field)
    cr = cd.detect_all()
    role_warns = [w for w in cr['warnings'] if w['type'] == 'role_duplicate']
    print(f"   角色重复预警: {len(role_warns)}条")
    assert len(role_warns) >= 1, "应有角色重复预警"
    results["test9_role_conflict"] = True

    # ── 测试10: 导出报告 ──
    print("\n🧪 测试10: 完整报告导出")
    report = field.to_report()
    fusion_report = FlowFieldFusionEngine(field).compute_fusion()
    conflict_report = CollabConflictDetector(field).detect_all()
    plan = distributor.get_collab_plan()

    full_report = {
        "version": VERSION,
        "dna": DNA,
        "confirm": CONFIRM,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "field": report,
        "fusion": fusion_report,
        "conflicts": conflict_report,
        "task_plan": plan,
        "system_health": {
            "balance": report["team_balance"],
            "fusion_index": fusion_report["fusion_index"],
            "conflict_free": conflict_report["conflict_count"] == 0,
        },
    }
    print(f"   报告生成完成 · 健康度: {round(fusion_report['fusion_index'], 4)}")
    print(f"   {json.dumps(full_report['system_health'], ensure_ascii=False)}")
    results["test10_report"] = True

    # ── 汇总 ──
    print("\n" + "=" * 60)
    passed = sum(results.values())
    total = len(results)
    print(f"🐉 自检完成: {passed}/{total} 通过")
    for k, v in results.items():
        status = "✅" if v else "❌"
        print(f"   {status} {k}")
    print("=" * 60)
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 8. CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if "--test" in sys.argv or len(sys.argv) == 1:
        results = run_tests()
        all_pass = all(results.values())
        sys.exit(0 if all_pass else 1)

    elif "--report" in sys.argv:
        field = create_default_collab_field()
        fusion = FlowFieldFusionEngine(field).compute_fusion()
        conflicts = CollabConflictDetector(field).detect_all()
        dist = CollabTaskDistributor(field)

        print(json.dumps({
            "field": field.to_report(),
            "fusion": fusion,
            "conflicts": conflicts,
            "plan": dist.get_collab_plan(),
        }, ensure_ascii=False, indent=2))

    elif "--balance" in sys.argv:
        field = create_default_collab_field()
        balance, status = field.get_team_balance_score()
        print(f"均衡指数: {balance} · {status}")
        dist = field.get_wuxing_distribution()
        for elem, count in dist.items():
            bar = "█" * count
            print(f"  {elem}: {bar} ({count})")

    elif "--conflicts" in sys.argv:
        field = create_default_collab_field()
        conflicts = CollabConflictDetector(field).detect_all()
        print(f"冲突: {conflicts['conflict_count']} · 预警: {conflicts['warning_count']}")
        for c in conflicts['conflicts']:
            print(f"  🔴 {c['detail']}")
            print(f"     建议: {c['suggestion']}")
        for w in conflicts['warnings']:
            print(f"  🟡 {w['detail']}")

    elif "--fusion" in sys.argv:
        field = create_default_collab_field()
        fusion = FlowFieldFusionEngine(field).compute_fusion()
        print(f"融合指数: {fusion['fusion_index']:.4f} · {fusion['fusion_status']}")
        print(f"主导五行: {fusion['dominant_wuxing']}")
        print(f"能量分布: {fusion['collective_energy']}")

    elif "--cmd" in sys.argv:
        # v1.1: 命令字符串模式 — 对接语义路由
        try:
            cmd_idx = sys.argv.index("--cmd")
            sub_cmd = sys.argv[cmd_idx + 1] if cmd_idx + 1 < len(sys.argv) else ""
        except (ValueError, IndexError):
            print("❌ --cmd 需要子命令: 状态|均衡|冲突|融合|报告|任务")
            sys.exit(1)

        field = create_default_collab_field()

        if sub_cmd in ("状态", "status"):
            dist = field.get_wuxing_distribution()
            cnt = len(field.nodes)
            print(f"协同场节点: {cnt}")
            for elem, count in dist.items():
                print(f"  {elem}: {count}")
            balance, status = field.get_team_balance_score()
            print(f"均衡指数: {balance} · {status}")

        elif sub_cmd in ("均衡", "balance"):
            balance, status = field.get_team_balance_score()
            print(f"均衡指数: {balance} · {status}")
            dist = field.get_wuxing_distribution()
            for elem, count in dist.items():
                bar = "█" * count
                print(f"  {elem}: {bar} ({count})")
            # 五行补位提示
            min_elem = min(dist, key=dist.get)  # type: ignore[reportArgumentType]
            if dist[min_elem] == 0:
                print(f"\n⚠️ {min_elem}行缺失，建议补充对应角色")

        elif sub_cmd in ("冲突", "conflicts"):
            conflicts = CollabConflictDetector(field).detect_all()
            print(f"冲突: {conflicts['conflict_count']} · 预警: {conflicts['warning_count']}")
            for c in conflicts['conflicts']:
                print(f"  🔴 {c['detail']}")
                print(f"     建议: {c['suggestion']}")
            for w in conflicts['warnings']:
                print(f"  🟡 {w['detail']}")

        elif sub_cmd in ("融合", "fusion"):
            fusion = FlowFieldFusionEngine(field).compute_fusion()
            print(f"融合指数: {fusion['fusion_index']:.4f} · {fusion['fusion_status']}")
            print(f"主导五行: {fusion['dominant_wuxing']}")
            sc = fusion['fused_sancai']
            print(f"集体三才: 天={sc['heaven']:.2f} 地={sc['earth']:.2f} 人={sc['human']:.2f}")

        elif sub_cmd in ("报告", "report"):
            fusion = FlowFieldFusionEngine(field).compute_fusion()
            conflicts = CollabConflictDetector(field).detect_all()
            balance, status = field.get_team_balance_score()
            dist = field.get_wuxing_distribution()

            print("═══ 流场协同完整报告 ═══")
            print(f"\n📊 节点: {len(field.nodes)}")
            for elem, count in dist.items():
                print(f"  {elem}: {count}")
            print(f"\n⚖️ 均衡指数: {balance} · {status}")
            print(f"🔥 融合指数: {fusion['fusion_index']:.4f} · {fusion['fusion_status']}")
            print(f"☯️ 主导五行: {fusion['dominant_wuxing']}")
            sc = fusion['fused_sancai']
            print(f"☯️ 集体三才: 天={sc['heaven']:.2f} 地={sc['earth']:.2f} 人={sc['human']:.2f}")
            print(f"\n⚠️ 冲突: {conflicts['conflict_count']} · 预警: {conflicts['warning_count']}")
            for c in conflicts['conflicts'][:5]:
                print(f"  🔴 {c['detail']}")

        elif sub_cmd in ("任务", "task"):
            dist = CollabTaskDistributor(field)
            plan = dist.get_collab_plan()
            print(f"待分配: {plan['pending_tasks']} · 已分配: {plan['assigned_tasks']}")
            for t in plan.get('tasks', [])[:5]:
                print(f"  {t.get('id', 'N/A')}: {t.get('title', 'N/A')}")

        else:
            print(f"❌ 未知子命令: {sub_cmd}")
            print("可用: 状态|均衡|冲突|融合|报告|任务")
            sys.exit(1)

    else:
        print("用法: python3 flowfield_collab_engine.py [--test|--report|--balance|--conflicts|--fusion|--cmd 状态|均衡|冲突|融合|报告|任务]")
