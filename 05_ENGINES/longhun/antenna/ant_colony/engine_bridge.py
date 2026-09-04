#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·ANT-COLONY-ENGINE-BRIDGE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂蚁群·引擎桥接层 v1.0 · AntColonyEngineBridge
将蚁群涌现指标注入龍魂现有引擎决策链路。

DNA: #龍芯⚡️丙午·辛未·ANT-COLONY-ENGINE-BRIDGE-v1.0
# STATUS: ⚠️ DEPRECATED · 本目录为旧版蚁群实现，功能由 engines/ant_colony/ 与 bin/lh_ant_colony_orchestrator.py 统一接管

桥接目标:
  1. 双脑互搏 (lh_dual_brain_engine.py)    → 蚁群投票加权
  2. 模9治理 (lh_mod9_runtime_engine.py)   → 蚁群路由融合
  3. Braket量子  (lh_braket_persona_engine.py) → 涌现质量联动
  4. 统一钩子 (lh_unified_hook.py)          → 审计增强

用法:
  from engine.ant_colony.engine_bridge import AntColonyEngineBridge
  bridge = AntColonyEngineBridge()
  result = bridge.weigh_decision(decision_data)
  quality = bridge.augment_audit(audit_context)
"""

import sys
import os
import json
import math
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·ANT-COLONY-ENGINE-BRIDGE-v1.0"
CST = timezone(timedelta(hours=8))


# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

@dataclass
class BridgeDecision:
    """桥接决策结果"""
    original_score: float                    # 原引擎评分
    ant_colony_weight: float                 # 蚁群权重
    adjusted_score: float                    # 调整后评分
    emergence_influence: float               # 涌现影响因子
    colony_consensus: float                  # 蚁群共识度 (0-1)
    recommendation: str                      # green/yellow/red
    details: Dict[str, Any] = field(default_factory=dict)
    dna: str = DNA


@dataclass
class BridgeAudit:
    """桥接审计增强"""
    original_verdict: str                    # 原审计结果
    enhanced_verdict: str                    # 增强后结果
    pheromone_trail: str                     # 信息素轨迹ID
    alert_level: float                       # 蚁群告警级别
    fixed_point_check: Dict                  # 不动点检查结果
    dna: str = DNA


# ═══════════════════════════════════════════════
# 桥接引擎
# ═══════════════════════════════════════════════

class AntColonyEngineBridge:
    """
    蚁群·引擎桥接层
    
    非侵入式接入现有引擎，所有调用都是 try/except 包裹的降级模式。
    蚁群 offline 时不影响主引擎运行。
    """

    # 涌现质量映射到权重的 S 曲线参数
    EMERGENCE_WEIGHT_MIDPOINT = 0.6     # E=0.6 时权重=0.5
    EMERGENCE_WEIGHT_STEEPNESS = 5.0    # S 曲线陡峭度

    # 蚁群共识对决策的影响力上限
    MAX_COLONY_INFLUENCE = 0.35         # 最多 influence 35%

    def __init__(self):
        self._runtime = None
        self._initialized = False
        self._lock = threading.Lock()

    @property
    def runtime(self):
        """懒加载蚁群运行时（单例）"""
        if self._runtime is None:
            try:
                from engine.ant_colony.runtime import get_runtime
                self._runtime = get_runtime(auto_start=False)
            except Exception:
                self._runtime = None
        return self._runtime

    @property
    def is_available(self) -> bool:
        return self.runtime is not None

    # ═══════════════════════════════
    # 1. 决策加权 → 双脑互搏
    # ═══════════════════════════════

    def weigh_decision(self, decision: Dict[str, Any]) -> BridgeDecision:
        """
        用蚁群涌现指标加权双脑决策。
        
        Args:
            decision: {
                "left_brain_score": float,   # 左脑（生成）评分
                "right_brain_score": float,  # 右脑（攻击）评分
                "tricolor": str,             # 原始三色
                "context": str,              # 决策上下文
            }
        Returns:
            BridgeDecision 调整后决策
        """
        left = decision.get("left_brain_score", 0.5)
        right = decision.get("right_brain_score", 0.5)
        original = (left * 0.6 + right * 0.4)  # 左脑权重略高

        try:
            rt = self.runtime
            if rt is None:
                return BridgeDecision(
                    original_score=original,
                    ant_colony_weight=0.0,
                    adjusted_score=original,
                    emergence_influence=0,
                    colony_consensus=0,
                    recommendation=decision.get("tricolor", "yellow"),
                )

            # 获取涌现质量
            state = rt.snapshot()
            E = state.emergence_E or 0.0

            # S 曲线映射：低 E → 低权重，高 E → 高权重
            # weight = 1 / (1 + exp(-steepness * (E - midpoint)))
            colony_weight = 1.0 / (1.0 + math.exp(
                -self.EMERGENCE_WEIGHT_STEEPNESS * (E - self.EMERGENCE_WEIGHT_MIDPOINT)
            ))

            # 信息素共识度
            total_trails = max(state.pheromone_trails, 1)
            alert_trails = state.pheromone_concentration.get("ALERT", 0)
            recruit_trails = state.pheromone_concentration.get("RECRUIT", 0)
            consensus = min(recruit_trails / max(alert_trails + recruit_trails, 1), 1.0)

            # 调整后的分数
            influence = colony_weight * self.MAX_COLONY_INFLUENCE
            adjusted = original * (1 - influence) + consensus * influence

            # 推荐
            if adjusted > 0.75:
                rec = "🟢 green"
            elif adjusted > 0.4:
                rec = "🟡 yellow"
            else:
                rec = "🔴 red"

            # 记录信息素轨迹
            result = BridgeDecision(
                original_score=round(original, 4),
                ant_colony_weight=round(colony_weight, 4),
                adjusted_score=round(adjusted, 4),
                emergence_influence=round(influence, 4),
                colony_consensus=round(consensus, 4),
                recommendation=rec,
                details={
                    "E": round(E, 4),
                    "grade": state.emergence_grade,
                    "trails": state.pheromone_trails,
                }
            )

            # 发送信息素轨迹
            try:
                from engine.ant_colony.antenna_signal import trail_signal
                sig = trail_signal(
                    sender="bridge_weigh",
                    receiver="dual_brain_engine",
                    trail_type="decision",
                    path_data=asdict(result),
                )
                rt.bus.send(sig)
            except Exception:
                pass

            return result

        except Exception:
            return BridgeDecision(
                original_score=original,
                ant_colony_weight=0.0,
                adjusted_score=original,
                emergence_influence=0,
                colony_consensus=0,
                recommendation=decision.get("tricolor", "green"),
            )

    # ═══════════════════════════════
    # 2. 审计增强 → 统一钩子
    # ═══════════════════════════════

    def augment_audit(self, audit_ctx: Dict[str, Any]) -> BridgeAudit:
        """
        用蚁群感知增强审计结果。

        Args:
            audit_ctx: {
                "verdict": str,       # green/yellow/red
                "engine": str,        # 来源引擎
                "evidence": List[Any],
            }
        """
        verdict = audit_ctx.get("verdict", "green")

        try:
            rt = self.runtime
            if rt is None:
                return BridgeAudit(
                    original_verdict=verdict,
                    enhanced_verdict=verdict,
                    pheromone_trail="N/A",
                    alert_level=0,
                    fixed_point_check={},
                )

            state = rt.snapshot()

            # 不动点检查
            fixed_checks = {}
            try:
                from engine.ant_colony.fixed_point_bridge import FixedPointBridge, FixedPointLevel
                # L3=架构级别，不可变
                l3_ok = FixedPointBridge.verify_level(
                    FixedPointLevel.L3_ARCHITECTURE,
                    {"verdict": verdict, "engine": audit_ctx.get("engine", "")}
                )
                fixed_checks["L3_architecture"] = l3_ok
                # L4=核心价值观
                l4_ok = FixedPointBridge.verify_level(
                    FixedPointLevel.L4_CORE_VALUES,
                    {"verdict": verdict}
                )
                fixed_checks["L4_core_values"] = l4_ok
            except Exception:
                fixed_checks = {"status": "unavailable"}

            # 蚁群告警级别
            try:
                from engine.ant_colony.antenna_signal import PheromoneType
                alert_paths = rt.pheromone_system.get_paths_by_type(PheromoneType.ALERT)
                alert_level = sum(s for _, s in alert_paths) / max(len(alert_paths), 1)
            except Exception:
                alert_level = 0

            # 增强裁决
            if alert_level > 50:
                enhanced = "🔴 red"
            elif alert_level > 20:
                enhanced = f"🟡 yellow"
            else:
                enhanced = verdict  # 保持原判

            # 发送信息素轨迹
            trail_id = "N/A"
            try:
                from engine.ant_colony.antenna_signal import trail_signal
                sig = trail_signal(
                    sender="bridge_audit",
                    receiver="unified_hook",
                    trail_type="audit",
                    path_data={"verdict": enhanced, "ctx": str(audit_ctx)[:200]},
                )
                rt.bus.send(sig)
                trail_id = sig.signal_id[:16]
            except Exception:
                pass

            return BridgeAudit(
                original_verdict=verdict,
                enhanced_verdict=enhanced,
                pheromone_trail=trail_id,
                alert_level=round(alert_level, 1),
                fixed_point_check=fixed_checks,
            )

        except Exception:
            return BridgeAudit(
                original_verdict=verdict,
                enhanced_verdict=verdict,
                pheromone_trail="N/A",
                alert_level=0,
                fixed_point_check={},
            )

    # ═══════════════════════════════
    # 3. 涌现质量快照 → Braket联动
    # ═══════════════════════════════

    def emergence_snapshot(self) -> Dict[str, Any]:
        """获取当前涌现质量快照，供 Braket 量子引擎联动"""
        try:
            rt = self.runtime
            if rt is None:
                return {"available": False}

            state = rt.snapshot()
            return {
                "available": True,
                "E": round(state.emergence_E, 4),
                "grade": state.emergence_grade,
                "populations": state.population_distribution,
                "pheromone_concentration": {
                    k: round(v, 1) for k, v in state.pheromone_concentration.items()
                },
                "top_paths": [
                    {"path": p["path"], "strength": round(p["strength"], 1), "type": p["type"]}
                    for p in state.top_paths[:3]
                ],
                "tick": state.tick_count,
                "timestamp": state.timestamp,
                "dna": DNA,
            }
        except Exception as e:
            return {"available": False, "error": str(e)}

    # ═══════════════════════════════
    # 4. 路由决策 → 模9治理
    # ═══════════════════════════════

    def route_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于蚁群信息素热度做路由推荐。
        
        用于模9治理引擎：根据当前信息素浓度推荐最优治理路径。
        """
        try:
            rt = self.runtime
            if rt is None:
                return {"route": "default", "confidence": 0}

            state = rt.snapshot()
            pheromones = state.pheromone_concentration

            recruit = pheromones.get("RECRUIT", 0)
            alert = pheromones.get("ALERT", 0)
            trail = pheromones.get("TRAIL", 0)
            aggregate = pheromones.get("AGGREGATE", 0)

            total = max(recruit + alert + trail + aggregate, 1)

            if alert / total > 0.4:
                route = "audit_first"       # 告警高 → 先审计
            elif recruit / total > 0.5:
                route = "fast_track"        # 招募高 → 快车道
            elif aggregate / total > 0.3:
                route = "collaborative"     # 聚集高 → 协作模式
            else:
                route = "standard"

            return {
                "route": route,
                "confidence": round(max(recruit, alert, trail, aggregate) / total, 3),
                "pheromone_breakdown": {
                    "RECRUIT": round(recruit, 1),
                    "ALERT": round(alert, 1),
                    "TRAIL": round(trail, 1),
                    "AGGREGATE": round(aggregate, 1),
                },
                "tick": state.tick_count,
            }
        except Exception as e:
            return {"route": "default", "confidence": 0, "error": str(e)}


# ═══════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════

_bridge: Optional[AntColonyEngineBridge] = None
_bridge_lock = threading.Lock()


def get_bridge() -> AntColonyEngineBridge:
    global _bridge
    with _bridge_lock:
        if _bridge is None:
            _bridge = AntColonyEngineBridge()
    return _bridge


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐜 蚁群·引擎桥接层")
    parser.add_argument("--weigh", type=str, help="决策加权测试 (JSON)")
    parser.add_argument("--audit", type=str, help="审计增强测试 (JSON)")
    parser.add_argument("--emergence", action="store_true", help="涌现快照")
    parser.add_argument("--route", action="store_true", help="路由推荐")
    args = parser.parse_args()

    bridge = get_bridge()

    if args.weigh:
        decision = json.loads(args.weigh)
        result = bridge.weigh_decision(decision)
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    elif args.audit:
        audit = json.loads(args.audit)
        result = bridge.augment_audit(audit)
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    elif args.emergence:
        result = bridge.emergence_snapshot()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.route:
        result = bridge.route_decision({})
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print("🐜 蚁群·引擎桥接层 v1.0")
        print(f"  DNA: {DNA}")
        print(f"  可用: {'✅' if bridge.is_available else '🔴'}")
        if bridge.is_available:
            snap = bridge.emergence_snapshot()
            if snap.get("available"):
                print(f"  涌现: E={snap['E']} ({snap['grade']})")
                print(f"  tick: {snap['tick']}")
        print()
        print("  用法:")
        print("    python3 engine/ant_colony/engine_bridge.py --weigh '{\"left_brain_score\":0.8,...}'")
        print("    python3 engine/ant_colony/engine_bridge.py --audit '{\"verdict\":\"green\",...}'")
        print("    python3 engine/ant_colony/engine_bridge.py --emergence")
        print("    python3 engine/ant_colony/engine_bridge.py --route")


if __name__ == "__main__":
    main()
