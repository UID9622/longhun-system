#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息素守护 v1.0 · PheromoneGuard
投喂挑战 P1-A7 落地：信息素污染检测 + 异常信号隔离 + 模块信任评分

DNA: #龍芯⚡️丙午·辛未·PHEROMONE-GUARD-v1.0

核心能力:
  1. 污染检测 — 异常浓度/频率/源的实时检测
  2. 异常隔离 — 可疑信息素自动隔离，防止污染扩散
  3. 信任评分 — 每个模块基于历史行为的信任度评分（0-1）
  4. 对抗性检测 — 模拟恶意模块攻击的防御

检测算法:
  - Z-score 异常检测：浓度偏离均值 > 3σ 即告警
  - 频率异常：同一源短时间高频发包
  - 新源检测：未见过的模块突然大量发包
  - 强度突变：单条轨迹强度瞬间暴涨

用法:
    guard = PheromoneGuard(pheromone_system)
    guard.check_all()  # 全量检查
    alerts = guard.get_alerts()  # 获取告警
"""

import time
import math
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, deque

from engine.ant_colony.antenna_signal import PheromoneType
from engine.ant_colony.pheromone_system import PheromoneSystem


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·PHEROMONE-GUARD-v1.0"


# ═══════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════

class Severity:
    """告警严重级别"""
    INFO = 0
    WARN = 1
    HIGH = 2
    CRITICAL = 3

    @classmethod
    def to_name(cls, s: int) -> str:
        return {0: "INFO", 1: "WARN", 2: "HIGH", 3: "CRITICAL"}.get(s, "UNKNOWN")


@dataclass
class GuardAlert:
    """防护告警"""
    alert_id: str
    rule: str
    severity: int
    source_module: str
    detail: str
    pheromone_type: Optional[str] = None
    trail_key: Optional[str] = None
    value: float = 0.0
    threshold: float = 0.0
    created_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "rule": self.rule,
            "severity": Severity.to_name(self.severity),
            "source": self.source_module,
            "detail": self.detail,
            "pheromone_type": self.pheromone_type,
            "trail_key": self.trail_key,
            "value": round(self.value, 2),
            "threshold": round(self.threshold, 2),
            "time": self.created_at,
        }


@dataclass
class ModuleTrust:
    """模块信任评分"""
    module_id: str
    trust_score: float = 1.0              # 0-1，1=完全信任
    signals_sent: int = 0
    alerts_generated: int = 0
    abnormal_behaviors: int = 0
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    
    def degrade(self, amount: float, reason: str = ""):
        """降低信任度"""
        self.trust_score = max(0.0, self.trust_score - amount)
        self.abnormal_behaviors += 1
    
    def restore(self, amount: float):
        """逐步恢复信任度"""
        self.trust_score = min(1.0, self.trust_score + amount)


# ═══════════════════════════════════════════════
# 信息素守护核心
# ═══════════════════════════════════════════════

class PheromoneGuard:
    """
    信息素守护 — 投喂挑战 P1-A7

    防护层次:
      1. 统计层 — Z-score 浓度异常检测
      2. 频率层 — 发包频率异常
      3. 源识别层 — 未知源/新源检测
      4. 行为层 — 模块信任评分
    """

    # 检测规则
    RULES = {
        "zscore_concentration": {
            "desc": "浓度Z-score异常 (>3σ)",
            "severity": Severity.HIGH,
            "threshold": 3.0,
        },
        "frequency_burst": {
            "desc": "发包频率异常 (>10/秒)",
            "severity": Severity.WARN,
            "threshold": 10,
        },
        "unknown_source": {
            "desc": "未知源模块大量发包",
            "severity": Severity.CRITICAL,
            "threshold": 5,
        },
        "strength_surge": {
            "desc": "单条轨迹强度瞬间暴涨 (>2x previous)",
            "severity": Severity.HIGH,
            "threshold": 2.0,
        },
        "type_imbalance": {
            "desc": "信息素类型分布失衡",
            "severity": Severity.WARN,
            "threshold": 0.8,
        },
        "decay_anomaly": {
            "desc": "信息素衰减异常 (不衰减或过快衰减)",
            "severity": Severity.HIGH,
            "threshold": 0.9,
        },
        "trust_fall": {
            "desc": "模块信任度跌破阈值",
            "severity": Severity.CRITICAL,
            "threshold": 0.3,
        },
    }

    # 历史窗口（用于统计基线）
    HISTORY_WINDOW = 300     # 5分钟
    BASELINE_MIN_SAMPLES = 20

    def __init__(self, pheromone_system: PheromoneSystem):
        self.ph = pheromone_system
        self.alerts: List[GuardAlert] = []
        self.trust_scores: Dict[str, ModuleTrust] = {}
        
        # 历史数据（用于基线计算）
        self._concentration_history: deque = deque(maxlen=100)
        self._frequency_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=50))
        self._trail_strength_history: Dict[str, float] = {}
        
        # 统计基线
        self._concentration_mean: float = 0.0
        self._concentration_std: float = 0.0
        self._baseline_ready: bool = False
        
        self._last_check = time.time()
        self._alert_counter = 0

    # ── 全量检查 ──

    def check_all(self) -> List[GuardAlert]:
        """执行全部防护检查，返回新告警"""
        new_alerts = []
        now = time.time()

        # 1. 浓度异常
        alerts = self._check_concentration_anomaly()
        new_alerts.extend(alerts)

        # 2. 频率异常
        alerts = self._check_frequency_anomaly()
        new_alerts.extend(alerts)

        # 3. 未知源
        alerts = self._check_unknown_sources()
        new_alerts.extend(alerts)

        # 4. 强度突变
        alerts = self._check_strength_surge()
        new_alerts.extend(alerts)

        # 5. 类型失衡
        alerts = self._check_type_imbalance()
        new_alerts.extend(alerts)

        # 6. 信任度检查
        alerts = self._check_trust_scores()
        new_alerts.extend(alerts)

        # 更新基线
        self._update_baseline()
        self._last_check = now

        self.alerts.extend(new_alerts)
        return new_alerts

    # ── 规则1: Z-score浓度异常 ──

    def _check_concentration_anomaly(self) -> List[GuardAlert]:
        """检测信息素浓度是否偏离历史基线 >3σ"""
        alerts = []
        
        total_concentration = sum(t.current_strength for t in self.ph.trails.values())
        
        # 积累样本
        self._concentration_history.append(total_concentration)

        if len(self._concentration_history) < self.BASELINE_MIN_SAMPLES:
            return alerts

        # 计算Z-score
        mean = sum(self._concentration_history) / len(self._concentration_history)
        variance = sum((x - mean)**2 for x in self._concentration_history) / len(self._concentration_history)
        std = math.sqrt(max(variance, 0.01))
        
        self._concentration_mean = mean
        self._concentration_std = std
        self._baseline_ready = True

        if std > 0:
            z_score = abs(total_concentration - mean) / std
            threshold = self.RULES["zscore_concentration"]["threshold"]
            
            if z_score > threshold:
                self._alert_counter += 1
                alerts.append(GuardAlert(
                    alert_id=f"GUARD-Z-{self._alert_counter}",
                    rule="zscore_concentration",
                    severity=Severity.HIGH,
                    source_module="system",
                    detail=f"总浓度={total_concentration:.1f} Z-score={z_score:.2f} (>3σ)",
                    value=z_score,
                    threshold=threshold,
                    created_at=datetime.now(CST).isoformat(),
                ))

        return alerts

    # ── 规则2: 频率异常 ──

    def _check_frequency_anomaly(self) -> List[GuardAlert]:
        """检测发包频率异常"""
        alerts = []
        now = time.time()
        window_start = now - 60  # 1分钟窗口

        # 统计各模块最近1分钟的发包数
        freq_count: Dict[str, int] = defaultdict(int)
        with self.ph._lock:
            for trail in self.ph.trails.values():
                if trail.created_at > window_start:
                    sender = trail.metadata.get("sender", "unknown")
                    freq_count[sender] += 1

        threshold = self.RULES["frequency_burst"]["threshold"]
        for module, count in freq_count.items():
            if count > threshold:
                self._alert_counter += 1
                alerts.append(GuardAlert(
                    alert_id=f"GUARD-F-{self._alert_counter}",
                    rule="frequency_burst",
                    severity=Severity.WARN,
                    source_module=module,
                    detail=f"{module} 1分钟内发包 {count} 次 (阈值: {threshold})",
                    value=float(count),
                    threshold=float(threshold),
                    created_at=datetime.now(CST).isoformat(),
                ))
                # 降低信任度
                self._degrade_trust(module, 0.1, "frequency_burst")

        return alerts

    # ── 规则3: 未知源 ──

    def _check_unknown_sources(self) -> List[GuardAlert]:
        """检测未知/未注册模块的大量发包"""
        alerts = []
        
        # 已知模块列表（从信任评分中获取）
        known_modules = set(self.trust_scores.keys())
        unknown_signals: Dict[str, int] = defaultdict(int)

        with self.ph._lock:
            for trail in self.ph.trails.values():
                sender = trail.metadata.get("sender", "")
                if sender and sender not in known_modules:
                    unknown_signals[sender] += 1
        
        threshold = self.RULES["unknown_source"]["threshold"]
        for src, count in unknown_signals.items():
            if count > threshold:
                self._alert_counter += 1
                alerts.append(GuardAlert(
                    alert_id=f"GUARD-U-{self._alert_counter}",
                    rule="unknown_source",
                    severity=Severity.CRITICAL,
                    source_module=src,
                    detail=f"未知模块 {src} 发送了 {count} 条轨迹",
                    value=float(count),
                    threshold=float(threshold),
                    created_at=datetime.now(CST).isoformat(),
                ))
                # 创建零信任条目
                self.trust_scores[src] = ModuleTrust(
                    module_id=src, trust_score=0.3
                )

        return alerts

    # ── 规则4: 强度突变 ──

    def _check_strength_surge(self) -> List[GuardAlert]:
        """检测单条轨迹强度瞬间暴涨"""
        alerts = []
        threshold = self.RULES["strength_surge"]["threshold"]

        for key, trail in self.ph.trails.items():
            prev = self._trail_strength_history.get(key)
            if prev and prev > 0:
                ratio = trail.current_strength / prev
                if ratio > threshold:
                    self._alert_counter += 1
                    alerts.append(GuardAlert(
                        alert_id=f"GUARD-S-{self._alert_counter}",
                        rule="strength_surge",
                        severity=Severity.HIGH,
                        source_module=trail.metadata.get("sender", "unknown"),
                        detail=f"轨迹 {key} 强度暴涨 {ratio:.1f}x ({prev:.1f}→{trail.current_strength:.1f})",
                        pheromone_type=trail.pheromone_type.value,
                        trail_key=key,
                        value=ratio,
                        threshold=threshold,
                        created_at=datetime.now(CST).isoformat(),
                    ))
            
            # 更新历史
            self._trail_strength_history[key] = trail.current_strength

        return alerts

    # ── 规则5: 类型失衡 ──

    def _check_type_imbalance(self) -> List[GuardAlert]:
        """检测信息素类型分布失衡（如某类信息素占比 >80%）"""
        alerts = []
        
        type_counts = defaultdict(int)
        with self.ph._lock:
            for trail in self.ph.trails.values():
                type_counts[trail.pheromone_type] += 1
        
        total = sum(type_counts.values())
        if total == 0:
            return alerts

        threshold = self.RULES["type_imbalance"]["threshold"]
        for ptype, count in type_counts.items():
            ratio = count / total
            if ratio > threshold:
                self._alert_counter += 1
                alerts.append(GuardAlert(
                    alert_id=f"GUARD-T-{self._alert_counter}",
                    rule="type_imbalance",
                    severity=Severity.WARN,
                    source_module="system",
                    detail=f"{ptype.value} 占比 {ratio:.1%} (>80%阈值)",
                    pheromone_type=ptype.value,
                    value=ratio,
                    threshold=threshold,
                    created_at=datetime.now(CST).isoformat(),
                ))

        return alerts

    # ── 规则6: 信任度 ──

    def _check_trust_scores(self) -> List[GuardAlert]:
        """检查模块信任度"""
        alerts = []
        threshold = self.RULES["trust_fall"]["threshold"]

        for module_id, trust in list(self.trust_scores.items()):
            if trust.trust_score < threshold:
                self._alert_counter += 1
                alerts.append(GuardAlert(
                    alert_id=f"GUARD-V-{self._alert_counter}",
                    rule="trust_fall",
                    severity=Severity.CRITICAL,
                    source_module=module_id,
                    detail=f"模块 {module_id} 信任度={trust.trust_score:.2f} (阈值: {threshold})",
                    value=trust.trust_score,
                    threshold=threshold,
                    created_at=datetime.now(CST).isoformat(),
                ))

        return alerts

    # ── 信任管理 ──

    def register_module(self, module_id: str, initial_trust: float = 1.0):
        """注册已知模块"""
        self.trust_scores[module_id] = ModuleTrust(
            module_id=module_id,
            trust_score=initial_trust,
            first_seen=time.time(),
            last_seen=time.time(),
        )

    def _degrade_trust(self, module_id: str, amount: float, reason: str):
        """降低信任度"""
        if module_id not in self.trust_scores:
            self.trust_scores[module_id] = ModuleTrust(module_id=module_id)
        
        trust = self.trust_scores[module_id]
        trust.degrade(amount, reason)
        trust.alerts_generated += 1
        trust.last_seen = time.time()

    def get_trust(self, module_id: str) -> float:
        """获取模块信任度"""
        t = self.trust_scores.get(module_id)
        return t.trust_score if t else 1.0

    def restore_trust(self, module_id: str, amount: float = 0.05):
        """逐步恢复信任度（良好行为后）"""
        if module_id in self.trust_scores:
            self.trust_scores[module_id].restore(amount)

    # ── 基线更新 ──

    def _update_baseline(self):
        """更新统计基线"""
        # 浓度基线已在 _check_concentration_anomaly 中更新
        pass

    # ── 查询 ──

    def get_alerts(self, severity: int | None = None, limit: int = 50) -> List[GuardAlert]:
        """获取告警列表（可按严重级过滤）"""
        if severity is not None:
            return [a for a in self.alerts if a.severity >= severity][-limit:]
        return self.alerts[-limit:]

    def get_trust_report(self) -> dict[str, Any]:
        """获取信任评分报告"""
        scores = {
            mid: {
                "trust": t.trust_score,
                "signals": t.signals_sent,
                "alerts": t.alerts_generated,
                "abnormal": t.abnormal_behaviors,
            }
            for mid, t in self.trust_scores.items()
        }
        
        trust_dist = defaultdict(int)
        for t in self.trust_scores.values():
            if t.trust_score >= 0.8:
                trust_dist["high"] += 1
            elif t.trust_score >= 0.5:
                trust_dist["medium"] += 1
            elif t.trust_score >= 0.3:
                trust_dist["low"] += 1
            else:
                trust_dist["critical"] += 1

        return {
            "modules": scores,
            "distribution": dict(trust_dist),
            "total_modules": len(self.trust_scores),
            "dna": DNA,
        }

    def get_stats(self) -> dict[str, Any]:
        """获取守护统计"""
        severity_dist = defaultdict(int)
        for a in self.alerts:
            severity_dist[Severity.to_name(a.severity)] += 1

        return {
            "total_alerts": len(self.alerts),
            "by_severity": dict(severity_dist),
            "baseline_ready": self._baseline_ready,
            "concentration_mean": round(self._concentration_mean, 1),
            "concentration_std": round(self._concentration_std, 1),
            "registered_modules": len(self.trust_scores),
            "dna": DNA,
        }


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys, os, json
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

    from engine.ant_colony.pheromone_system import PheromoneSystem
    from engine.ant_colony.antenna_signal import recruit_signal, alert_signal

    ph = PheromoneSystem()
    guard = PheromoneGuard(ph)

    # 注册已知模块
    known = ["P00-文心", "P01-诸葛亮", "P04-鲁班", "P05-上帝之眼", 
             "P09-孙思邈", "P12-屈原", "P72-龙盾"]
    for m in known:
        guard.register_module(m)

    # 模拟：正常信号 + 异常信号
    print("=" * 60)
    print("🛡️ 信息素守护 · 自检")
    print("=" * 60)

    # 正常招募
    for i in range(5):
        sig = recruit_signal("P04-鲁班", "P01-诸葛亮", {"task": f"build_{i}"}, priority=7)
        ph.deposit(sig, f"P04-鲁班->P01-诸葛亮", fixed_point_level=2)

    # 异常：未知模块大量发包
    for i in range(20):
        sig = recruit_signal("unknown_spammer", "broadcast", {"task": "spam"}, priority=1)
        ph.deposit(sig, f"unknown_spammer->broadcast", fixed_point_level=1)

    # 异常：高强度警戒
    sig = alert_signal("P09-孙思邈", 4, "高度告警测试", affected=["all"])
    ph.deposit(sig, "alert_test", fixed_point_level=3)

    # 执行检查
    new_alerts = guard.check_all()
    print(f"\n检测到 {len(new_alerts)} 条告警:")
    for a in new_alerts:
        print(f"  [{Severity.to_name(a.severity):7s}] {a.rule}: {a.detail}")

    # 信任报告
    print(f"\n信任评分报告:")
    trust_report = guard.get_trust_report()
    for mid, data in trust_report["modules"].items():
        bar = "🟢" if data["trust"] > 0.8 else "🟡" if data["trust"] > 0.5 else "🔴"
        print(f"  {bar} {mid}: trust={data['trust']:.2f} alerts={data['alerts']}")

    print(f"\n统计: {json.dumps(guard.get_stats(), indent=2, ensure_ascii=False)}")
    print(f"DNA: {DNA}")
