#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·AUDIT-ANT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
审计蚁 v1.0 · AuditAnt
投喂挑战 P0-A2 落地：信息素追溯链路 + 决策可审计性

DNA: #龍芯⚡️丙午·辛未·AUDIT-ANT-v1.0
# STATUS: ⚠️ DEPRECATED · 本目录为旧版蚁群实现，功能由 engines/ant_colony/ 与 bin/lh_ant_colony_orchestrator.py 统一接管

核心能力:
  1. 决策追溯 — 任意集体决策 → 完整信息素路径 + 模块响应链
  2. audit_level 激活 — antenna_signal.py 中定义但未使用的审计标记
  3. 审计链存证 — 每个决策生成不可篡改的审计证物
  4. 异常行为基线 — 偏离预期路径的告警
  5. 三色审计联动 — 与 color_fixpoint 的 GREEN/YELLOW/RED 对齐

用法:
    from engine.ant_colony.audit_ant import AuditAnt
    auditor = AuditAnt(bus, pheromone_system)
    report = auditor.trace_decision("signal_abc123")
    print(report.verdict)  # GREEN / YELLOW / RED
"""

import time
import hashlib
import json
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict

from engine.ant_colony.antenna_signal import (
    AntennaSignal, PheromoneType, PayloadType,
)
from engine.ant_colony.pheromone_system import PheromoneSystem, PheromoneTrail


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·AUDIT-ANT-v1.0"


# ═══════════════════════════════════════════════
# 审计级别定义（三色审计）
# ═══════════════════════════════════════════════

class AuditLevel:
    """三色审计级别 — 与不动点七色对齐"""
    GREEN = 0   # 正常·留痕
    YELLOW = 1  # 关注·待确认
    RED = 2     # 异常·需熔断
    BLACK = 3   # 严重·隔离

    @classmethod
    def to_name(cls, level: int) -> str:
        return {0: "GREEN·正常", 1: "YELLOW·关注", 2: "RED·异常", 3: "BLACK·严重"}.get(level, "UNKNOWN")

    @classmethod
    def is_ok(cls, level: int) -> bool:
        return level <= AuditLevel.YELLOW


# ═══════════════════════════════════════════════
# 审计数据类
# ═══════════════════════════════════════════════

@dataclass
class TraceNode:
    """追溯链节点 — 一次信号跳转"""
    hop: int
    module_id: str
    signal_id: str
    pheromone_type: str
    payload_summary: str
    timestamp: float
    fixed_point_level: int
    color_state: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "hop": self.hop,
            "module": self.module_id,
            "signal_id": self.signal_id,
            "pheromone": self.pheromone_type,
            "payload": self.payload_summary,
            "time": datetime.fromtimestamp(self.timestamp, CST).isoformat(),
            "fp_level": self.fixed_point_level,
            "color": self.color_state,
        }


@dataclass
class AuditReport:
    """审计报告"""
    decision_id: str
    trace_chain: List[TraceNode] = field(default_factory=list)
    total_hops: int = 0
    max_fp_level: int = 1
    pheromone_path: List[str] = field(default_factory=list)
    verdict: str = "GREEN"
    audit_level: int = 0
    anomalies: List[str] = field(default_factory=list)
    evidence_hash: str = ""
    audit_dna: str = DNA
    audited_at: str = ""

    def summary(self) -> str:
        lines = [
            f"🧿 审计报告 | {self.decision_id[:12]}...",
            f"  追溯链: {self.total_hops} 跳",
            f"  信息素路径: {' → '.join(self.pheromone_path) if self.pheromone_path else '无'}",
            f"  最高不动点层级: L{self.max_fp_level}",
            f"  审计判定: {AuditLevel.to_name(self.audit_level)}",
            f"  证物哈希: {self.evidence_hash[:16]}...",
        ]
        if self.anomalies:
            lines.append(f"  ⚠️ 异常: {len(self.anomalies)} 项")
            for a in self.anomalies[:3]:
                lines.append(f"     - {a}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "trace_chain": [n.to_dict() for n in self.trace_chain],
            "total_hops": self.total_hops,
            "max_fp_level": self.max_fp_level,
            "pheromone_path": self.pheromone_path,
            "verdict": self.verdict,
            "audit_level": self.audit_level,
            "anomalies": self.anomalies,
            "evidence_hash": self.evidence_hash,
            "dna": self.audit_dna,
            "audited_at": self.audited_at,
        }


# ═══════════════════════════════════════════════
# 审计蚁核心
# ═══════════════════════════════════════════════

class AuditAnt:
    """
    审计蚁 — 投喂挑战 P0-A2

    职责:
      - trace_decision(): 追溯任意集体决策的完整信号路径
      - audit_signal(): 给信号打审计标记（激活 audit_level）
      - check_anomalies(): 检测异常信息素模式
      - generate_evidence(): 生成不可篡改的审计证物
    """

    # 异常检测规则
    ANOMALY_RULES = {
        "hop_exceeded": ("跳数超过阈值(>10)", AuditLevel.RED),
        "unexpected_alert": ("非安全模块发出ALERT", AuditLevel.YELLOW),
        "fp_level_jump": ("不动点层级跳跃>2级", AuditLevel.YELLOW),
        "missing_trace": ("路径节点丢失", AuditLevel.RED),
        "recursive_loop": ("检测到回环路径", AuditLevel.RED),
        "low_quality_path": ("信息素强度<5", AuditLevel.YELLOW),
        "unauthorized_module": ("模块越权访问高层级", AuditLevel.RED),
    }

    def __init__(self, pheromone_system: PheromoneSystem, bus=None):
        self.ph = pheromone_system
        self.bus = bus
        self._audit_log: List[AuditReport] = []
        self._evidence_store: Dict[str, str] = {}  # signal_id → evidence_hash
        self._anomaly_counter: Dict[str, int] = defaultdict(int)

    # ── 核心能力 1: 决策追溯 ──

    def trace_decision(self, signal_id: str, max_depth: int = 20) -> AuditReport:
        """
        追溯一个决策信号的完整信息素路径

        算法:
          1. 从 signal_id 开始，沿 path_trace 字段逐跳回溯
          2. 同时从信息素系统中查找相关轨迹
          3. 重建完整的模块响应链
          4. 检测异常并给出审计判定
        """
        report = AuditReport(
            decision_id=signal_id,
            audited_at=datetime.now(CST).isoformat(),
        )

        # 1. 从信息素系统中查找所有相关轨迹
        related_trails = self._find_related_trails(signal_id)

        # 2. 构建追溯链
        trace_nodes = []
        pheromone_types = []
        max_level = 1

        for trail_key, trail in related_trails:
            metadata = trail.metadata
            hop = trail.hop_count

            node = TraceNode(
                hop=hop,
                module_id=metadata.get("sender", "unknown"),
                signal_id=metadata.get("signal_id", signal_id),
                pheromone_type=trail.pheromone_type.value,
                payload_summary=self._summarize_payload(metadata),
                timestamp=trail.created_at,
                fixed_point_level=trail.fixed_point_level,
                color_state=metadata.get("color_state", "G"),
            )
            trace_nodes.append(node)
            pheromone_types.append(trail.pheromone_type.value)
            max_level = max(max_level, trail.fixed_point_level)

        # 排序：按hop递增
        trace_nodes.sort(key=lambda n: n.hop)

        report.trace_chain = trace_nodes
        report.total_hops = len(trace_nodes)
        report.max_fp_level = max_level
        report.pheromone_path = pheromone_types

        # 3. 异常检测
        anomalies = self._detect_anomalies(trace_nodes, signal_id)
        report.anomalies = anomalies

        # 4. 判定审计级别
        report.audit_level = self._determine_audit_level(anomalies, trace_nodes)
        report.verdict = AuditLevel.to_name(report.audit_level)

        # 5. 生成证物哈希
        report.evidence_hash = self._generate_evidence(trace_nodes)

        # 6. 存档
        self._audit_log.append(report)
        self._evidence_store[signal_id] = report.evidence_hash

        return report

    def _find_related_trails(self, signal_id: str) -> List[Tuple[str, PheromoneTrail]]:
        """查找与 signal_id 相关的所有信息素轨迹"""
        related = []
        with self.ph._lock:
            for key, trail in self.ph.trails.items():
                meta_sid = trail.metadata.get("signal_id", "")
                if meta_sid == signal_id or signal_id in key:
                    related.append((key, trail))
        return related

    def _summarize_payload(self, metadata: dict[str, Any]) -> str:
        """提取 payload 摘要"""
        payload = metadata.get("payload", metadata.get("task", ""))
        if isinstance(payload, dict):
            return payload.get("task", payload.get("type", str(payload)[:40]))
        return str(payload)[:40]

    # ── 核心能力 2: 信号审计标记 ──

    def audit_signal(self, signal: AntennaSignal) -> int:
        """
        给信号打审计标记 — 激活 antenna_signal.py 中未使用的 audit_level

        审计规则:
          0 (GREEN):  正常信号，无需关注
          1 (YELLOW): 来自未知模块 / 不常见路径 / 低优先级
          2 (RED):    ALERT信息素异常 / 层级越权 / 高频重复
          3 (BLACK):  疑似伪造 / 完整性校验失败 / 来自隔离模块
        """
        level = AuditLevel.GREEN

        # 检查发送者是否已知
        if self.bus and signal.sender_id not in self.bus.modules:
            level = max(level, AuditLevel.YELLOW)

        # ALERT 信息素的额外检查
        if signal.pheromone_type == PheromoneType.ALERT:
            if signal.payload.get("alert_level", 0) >= 3:
                level = max(level, AuditLevel.RED)

        # 跳数检查
        if signal.hop_count > 8:
            level = max(level, AuditLevel.YELLOW)
        if signal.hop_count > 15:
            level = max(level, AuditLevel.RED)

        # 不动点层级越权检查
        if signal.level_required > 3 and self.bus:
            sender_mod = self.bus.modules.get(signal.sender_id)
            if sender_mod and sender_mod.level_access < signal.level_required:
                level = max(level, AuditLevel.RED)

        # 高频重复检测（同一发送者短时间内重复同一信号）
        sig_fingerprint = f"{signal.sender_id}:{signal.pheromone_type.value}:{signal.payload_type.value}"
        self._anomaly_counter[sig_fingerprint] += 1
        if self._anomaly_counter[sig_fingerprint] > 50:
            level = max(level, AuditLevel.RED)

        # 应用审计级别到信号
        signal.audit_level = level
        return level

    # ── 核心能力 3: 异常检测 ──

    def _detect_anomalies(self, trace_nodes: List[TraceNode], signal_id: str) -> List[str]:
        """检测追溯链中的异常"""
        anomalies = []

        if not trace_nodes:
            anomalies.append(self.ANOMALY_RULES["missing_trace"][0])
            return anomalies

        # 1. 跳数异常
        if len(trace_nodes) > 10:
            anomalies.append(self.ANOMALY_RULES["hop_exceeded"][0])

        # 2. 不动点层级跳跃
        levels = [n.fixed_point_level for n in trace_nodes]
        for i in range(1, len(levels)):
            if abs(levels[i] - levels[i-1]) > 2:
                anomalies.append(self.ANOMALY_RULES["fp_level_jump"][0])
                break

        # 3. 回环检测
        seen_modules = set()
        for node in trace_nodes:
            if node.module_id in seen_modules and node.hop > 1:
                anomalies.append(self.ANOMALY_RULES["recursive_loop"][0])
                break
            seen_modules.add(node.module_id)

        # 4. 非安全模块 ALERT 检测
        for node in trace_nodes:
            if node.pheromone_type == "ALERT":
                if node.module_id not in ("P05-上帝之眼", "P72-龙盾", "P12-屈原", "P13-姜子牙"):
                    anomalies.append(self.ANOMALY_RULES["unexpected_alert"][0])
                    break

        return anomalies

    def _determine_audit_level(self, anomalies: List[str], trace_nodes: List[TraceNode]) -> int:
        """根据异常确定审计级别"""
        if not anomalies:
            return AuditLevel.GREEN

        max_level = AuditLevel.GREEN
        for anomaly in anomalies:
            for rule_name, (_, level) in self.ANOMALY_RULES.items():
                if rule_name in anomaly or anomaly.startswith(self.ANOMALY_RULES[rule_name][0]):
                    max_level = max(max_level, level)

        return max_level

    # ── 核心能力 4: 证物生成 ──

    def _generate_evidence(self, trace_nodes: List[TraceNode]) -> str:
        """生成不可篡改的审计证物哈希"""
        evidence_data = json.dumps(
            [n.to_dict() for n in trace_nodes],
            sort_keys=True, ensure_ascii=False
        )
        return hashlib.blake2b(
            evidence_data.encode('utf-8'),
            digest_size=32
        ).hexdigest()

    # ── 核心能力 5: 批量审计 ──

    def audit_all_recent(self, seconds: float = 3600) -> List[AuditReport]:
        """批量审计最近N秒内的所有决策"""
        cutoff = time.time() - seconds
        reports = []

        with self.ph._lock:
            recent_trails = {
                k: v for k, v in self.ph.trails.items()
                if v.created_at > cutoff
            }

        seen_ids = set()
        for trail in recent_trails.values():
            sid = trail.metadata.get("signal_id", "")
            if sid and sid not in seen_ids:
                seen_ids.add(sid)
                report = self.trace_decision(sid)
                reports.append(report)

        return reports

    # ── 统计 ──

    def get_audit_stats(self) -> dict[str, Any]:
        """获取审计统计数据"""
        levels = defaultdict(int)
        for report in self._audit_log:
            levels[report.verdict] += 1

        return {
            "total_audits": len(self._audit_log),
            "total_evidence": len(self._evidence_store),
            "by_verdict": dict(levels),
            "anomaly_counts": dict(self._anomaly_counter),
            "dna": DNA,
        }


# ═══════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

    from engine.ant_colony.pheromone_system import PheromoneSystem
    from engine.ant_colony.antenna_signal import recruit_signal, alert_signal

    ph = PheromoneSystem()
    auditor = AuditAnt(ph)

    # 模拟：生成一些信息素轨迹
    sig1 = recruit_signal("P04-鲁班", "P01-诸葛亮", {"task": "build_mvp"}, priority=8)
    ph.deposit(sig1, "P04-鲁班->P01-诸葛亮", fixed_point_level=2)

    sig2 = recruit_signal("P01-诸葛亮", "P00-文心", {"task": "review_plan"}, priority=7)
    ph.deposit(sig2, "P01-诸葛亮->P00-文心", fixed_point_level=2)

    sig3 = alert_signal("P09-孙思邈", 2, "P09发出中度告警", affected=["health_check"])
    ph.deposit(sig3, "P09-孙思邈->broadcast", fixed_point_level=3)

    # 审计追溯
    print("=" * 60)
    print("🧿 审计蚁 自检")
    print("=" * 60)

    for sid in [sig1.signal_id, sig2.signal_id, sig3.signal_id]:
        report = auditor.trace_decision(sid)
        print(report.summary())
        print()

    # 信号审计标记
    print("信号审计标记测试:")
    for sig in [sig1, sig2, sig3]:
        level = auditor.audit_signal(sig)
        print(f"  {sig.signal_id[:12]}... → audit_level={level} ({AuditLevel.to_name(level)})")

    print(f"\n审计统计: {json.dumps(auditor.get_audit_stats(), indent=2, ensure_ascii=False)}")
    print("✅ 审计蚁 自检完成, DNA:", DNA)
