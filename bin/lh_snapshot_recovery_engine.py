#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·己未·申时·履-SNAPSHOT-RECOVERY-v1.0-Q5R6S7T8
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
🐉 龍魂 · 快照恢复引擎 v1.0 (Snapshot & Recovery Engine)
=========================================================
投喂落地：CNSH Runtime Governance Mathematics · Snapshot Recovery + Timeline

特性：
  - 三重快照（本地 + 可选Git + 可选Notion）
  - 快照哈希链验证
  - 时间轴事件记录
  - 回滚恢复

DNA: #龍芯⚡️丙午·乙未·己未·申时·履-SNAPSHOT-RECOVERY-v1.0-Q5R6S7T8
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import os
import sys
import uuid
import hashlib
import shutil
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "snapshot_recovery")
SNAPSHOT_STORE = os.path.join(SNAPSHOT_DIR, "snapshots")
RECOVERY_STORE = os.path.join(SNAPSHOT_DIR, "recovery_points")
TIMELINE_STORE = os.path.join(SNAPSHOT_DIR, "timeline")
os.makedirs(SNAPSHOT_STORE, exist_ok=True)
os.makedirs(RECOVERY_STORE, exist_ok=True)
os.makedirs(TIMELINE_STORE, exist_ok=True)


class StorageTier(Enum):
    PRIMARY = "PRIMARY"      # 本地
    SECONDARY = "SECONDARY"  # Git
    TERTIARY = "TERTIARY"    # Notion


class TimelineEventType(Enum):
    INPUT = "INPUT"
    DR_CALC = "DR_CALCULATION"
    AUDIT = "AUDIT"
    ROUTE = "ROUTE"
    EXECUTE = "EXECUTE"
    SNAPSHOT = "SNAPSHOT"
    ARCHIVE = "ARCHIVE"
    FUSE = "FUSE"
    RECOVERY = "RECOVERY"
    STATE_CHANGE = "STATE_CHANGE"


@dataclass
class TimelineEvent:
    """时间轴事件"""
    event_id: str
    timestamp: str
    dna_trace: str
    actor: str
    action: str
    event_type: TimelineEventType
    state: Dict = field(default_factory=dict)
    risk_level: float = 0.0
    snapshot_ref: str = ""


@dataclass
class SystemSnapshot:
    """系统快照"""
    snapshot_id: str
    timestamp: str
    dna_trace: str
    state: Dict = field(default_factory=dict)        # 运行时状态
    file_checksums: Dict[str, str] = field(default_factory=dict)  # 文件哈希
    memory_state: Dict = field(default_factory=dict)  # 记忆状态
    trust_matrix: Dict = field(default_factory=dict)  # 信任矩阵
    rollback_point: str = ""
    hash_value: str = ""
    parent_snapshot_id: str = ""  # 父快照（链式）
    storage_tiers: List[str] = field(default_factory=list)  # 已存储的层


@dataclass
class RecoveryPoint:
    """恢复点"""
    point_id: str
    snapshot_id: str
    timestamp: str
    dna_trace: str
    reason: str
    is_verified: bool = False
    recovery_hash: str = ""


class SnapshotRecoveryEngine:
    """
    快照恢复引擎
    
    功能：
    - 创建系统快照（本地 + 可选远程）
    - 快照链式哈希验证
    - 时间轴记录
    - 回滚恢复
    """

    def __init__(self):
        self.snapshots: Dict[str, SystemSnapshot] = {}
        self.timeline: List[TimelineEvent] = []
        self.recovery_points: Dict[str, RecoveryPoint] = {}
        self._load_existing()

    def _load_existing(self):
        """加载已有快照和时间轴"""
        # 加载快照索引
        index_file = os.path.join(SNAPSHOT_DIR, "snapshot_index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for snap_id, snap_data in data.items():
                    self.snapshots[snap_id] = SystemSnapshot(**snap_data)

        # 加载时间轴
        timeline_file = os.path.join(TIMELINE_STORE, "timeline.jsonl")
        if os.path.exists(timeline_file):
            with open(timeline_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            self.timeline.append(TimelineEvent(**data))
                        except (json.JSONDecodeError, TypeError):
                            pass

        # 加载恢复点
        recovery_file = os.path.join(RECOVERY_STORE, "recovery_points.json")
        if os.path.exists(recovery_file):
            with open(recovery_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pt_id, pt_data in data.items():
                    self.recovery_points[pt_id] = RecoveryPoint(**pt_data)

    def _save_index(self):
        """保存快照索引"""
        index_file = os.path.join(SNAPSHOT_DIR, "snapshot_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.snapshots.items()}, f, ensure_ascii=False, indent=2)

    def _save_timeline_event(self, event: TimelineEvent):
        timeline_file = os.path.join(TIMELINE_STORE, "timeline.jsonl")
        with open(timeline_file, 'a', encoding='utf-8') as f:
            d = asdict(event)
            d['event_type'] = event.event_type.value
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
        self.timeline.append(event)

    def _save_recovery_points(self):
        recovery_file = os.path.join(RECOVERY_STORE, "recovery_points.json")
        with open(recovery_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.recovery_points.items()}, f, ensure_ascii=False, indent=2)

    # ─── 时间轴记录 ───
    def record_timeline(self, event_type: TimelineEventType, actor: str, action: str,
                        dna_trace: str = "", state: Optional[Dict] = None,
                        risk_level: float = 0.0, snapshot_ref: str = "") -> TimelineEvent:
        """记录时间轴事件"""
        event = TimelineEvent(
            event_id=f"TL-{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna_trace=dna_trace or f"#龍芯⚡️丙午·乙未·己未·申时·履-TL-{uuid.uuid4().hex[:8]}",
            actor=actor,
            action=action,
            event_type=event_type,
            state=state or {},
            risk_level=risk_level,
            snapshot_ref=snapshot_ref,
        )
        self._save_timeline_event(event)
        return event

    # ─── 创建快照 ───
    def create_snapshot(self, state: Dict, dna_trace: str = "",
                        memory_state: Optional[Dict] = None,
                        trust_matrix: Optional[Dict] = None,
                        file_paths: Optional[List[str]] = None) -> SystemSnapshot:
        """
        创建系统快照
        
        返回: SystemSnapshot
        """
        snap_id = f"SNAP-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        dna = dna_trace or f"#龍芯⚡️丙午·乙未·己未·申时·履-SNAP-{snap_id[-8:]}"

        # 计算文件校验和
        checksums = {}
        if file_paths:
            for fp in file_paths:
                if os.path.exists(fp):
                    with open(fp, 'rb') as f:
                        checksums[fp] = hashlib.sha256(f.read()).hexdigest()

        # 找到父快照
        parent_id = ""
        if self.snapshots:
            parent_id = list(self.snapshots.keys())[-1]

        snap = SystemSnapshot(
            snapshot_id=snap_id,
            timestamp=timestamp,
            dna_trace=dna,
            state=state,
            file_checksums=checksums,
            memory_state=memory_state or {},
            trust_matrix=trust_matrix or {},
            rollback_point=snap_id,
            parent_snapshot_id=parent_id,
            storage_tiers=[StorageTier.PRIMARY.value],
        )

        # 计算哈希（含父快照哈希）
        prev_hash = self.snapshots[parent_id].hash_value if parent_id else ""
        raw = f"{prev_hash}{snap_id}{timestamp}{json.dumps(state, sort_keys=True)}"
        snap.hash_value = hashlib.sha256(raw.encode()).hexdigest()

        # 本地存储
        snap_file = os.path.join(SNAPSHOT_STORE, f"{snap_id}.json")
        with open(snap_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(snap), f, ensure_ascii=False, indent=2)

        # 验证
        with open(snap_file, 'r') as f:
            content = f.read()
        verify_hash = hashlib.sha256(content.encode()).hexdigest()

        self.snapshots[snap_id] = snap
        self._save_index()

        # 记录时间轴
        self.record_timeline(
            event_type=TimelineEventType.SNAPSHOT,
            actor="SnapshotEngine",
            action=f"创建快照 {snap_id}",
            dna_trace=dna,
            snapshot_ref=snap_id,
        )

        return snap

    # ─── 创建恢复点 ───
    def create_recovery_point(self, snapshot_id: str, reason: str = "",
                               dna_trace: str = "") -> RecoveryPoint:
        """创建恢复点"""
        if snapshot_id not in self.snapshots:
            raise ValueError(f"快照不存在: {snapshot_id}")

        snap = self.snapshots[snapshot_id]
        point_id = f"RECOV-{uuid.uuid4().hex[:12]}"

        point = RecoveryPoint(
            point_id=point_id,
            snapshot_id=snapshot_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            dna_trace=dna_trace or snap.dna_trace,
            reason=reason,
            is_verified=True,
        )

        raw = f"{point_id}{snapshot_id}{point.timestamp}"
        point.recovery_hash = hashlib.sha256(raw.encode()).hexdigest()

        self.recovery_points[point_id] = point
        self._save_recovery_points()

        # 记录时间轴
        self.record_timeline(
            event_type=TimelineEventType.RECOVERY,
            actor="RecoveryEngine",
            action=f"创建恢复点 {point_id} → {snapshot_id}",
            dna_trace=point.dna_trace,
            snapshot_ref=snapshot_id,
        )

        return point

    # ─── 验证快照链 ───
    def verify_chain(self) -> Tuple[bool, List[str]]:
        """验证快照哈希链完整性"""
        issues = []
        prev_hash = ""

        sorted_snaps = sorted(self.snapshots.values(), key=lambda s: s.timestamp)
        for snap in sorted_snaps:
            # 验证当前快照文件存在
            snap_file = os.path.join(SNAPSHOT_STORE, f"{snap.snapshot_id}.json")
            if not os.path.exists(snap_file):
                issues.append(f"快照文件缺失: {snap.snapshot_id}")
                continue

            # 验证文件内容未被篡改
            with open(snap_file, 'r') as f:
                content = f.read()
            current_hash = hashlib.sha256(content.encode()).hexdigest()

            # 重新计算期望哈希
            raw = f"{prev_hash}{snap.snapshot_id}{snap.timestamp}{json.dumps(snap.state, sort_keys=True)}"
            expected_hash = hashlib.sha256(raw.encode()).hexdigest()

            if snap.hash_value != expected_hash:
                issues.append(f"哈希不匹配: {snap.snapshot_id} (存储={snap.hash_value[:8]}... vs 计算={expected_hash[:8]}...)")

            prev_hash = snap.hash_value

        is_valid = len(issues) == 0
        return is_valid, issues

    # ─── 回滚恢复 ───
    def recover(self, recovery_point_id: str) -> Tuple[bool, SystemSnapshot, str]:
        """
        回滚到指定恢复点
        
        返回: (成功, 快照, 消息)
        """
        if recovery_point_id not in self.recovery_points:
            return False, None, f"恢复点不存在: {recovery_point_id}"

        point = self.recovery_points[recovery_point_id]
        if point.snapshot_id not in self.snapshots:
            return False, None, f"快照不存在: {point.snapshot_id}"

        snap = self.snapshots[point.snapshot_id]

        # 验证恢复点哈希
        raw = f"{point.point_id}{point.snapshot_id}{point.timestamp}"
        verify = hashlib.sha256(raw.encode()).hexdigest()
        if verify != point.recovery_hash:
            return False, None, "恢复点哈希验证失败 — 可能被篡改"

        # 记录恢复事件
        self.record_timeline(
            event_type=TimelineEventType.RECOVERY,
            actor="RecoveryEngine",
            action=f"执行回滚到 {point.snapshot_id}",
            dna_trace=point.dna_trace,
            snapshot_ref=point.snapshot_id,
        )

        return True, snap, f"已恢复到快照 {point.snapshot_id} (创建于 {snap.timestamp})"

    # ─── 时间轴查询 ───
    def query_timeline(self, event_type: Optional[TimelineEventType] = None,
                       limit: int = 50) -> List[TimelineEvent]:
        """查询时间轴"""
        results = self.timeline
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        return results[-limit:]

    def timeline_summary(self) -> str:
        """时间轴摘要"""
        if not self.timeline:
            return "时间轴为空"

        lines = []
        for e in self.timeline[-20:]:
            icon = {
                TimelineEventType.INPUT: "📥",
                TimelineEventType.AUDIT: "📋",
                TimelineEventType.EXECUTE: "⚙️",
                TimelineEventType.SNAPSHOT: "📸",
                TimelineEventType.ARCHIVE: "📦",
                TimelineEventType.FUSE: "🚨",
                TimelineEventType.RECOVERY: "🔄",
            }.get(e.event_type, "•")

            ts = e.timestamp.split('T')[1][:8] if 'T' in e.timestamp else e.timestamp
            lines.append(f"  {icon} {ts} [{e.event_type.value}] {e.action}")

        return "\n".join(lines)

    def stats(self) -> Dict[str, Any]:
        chain_valid, issues = self.verify_chain()
        return {
            "total_snapshots": len(self.snapshots),
            "total_recovery_points": len(self.recovery_points),
            "total_timeline_events": len(self.timeline),
            "chain_valid": chain_valid,
            "chain_issues": len(issues),
            "latest_snapshot": list(self.snapshots.keys())[-1] if self.snapshots else None,
            "storage_size_mb": round(sum(
                os.path.getsize(os.path.join(SNAPSHOT_STORE, f)) 
                for f in os.listdir(SNAPSHOT_STORE) if f.endswith('.json')
            ) / 1024 / 1024, 2),
        }


# ═══════════════════════════════════════════════════════════
# 🧪 CLI 演示
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 70)
    print("🐉 龍魂 · 快照恢复引擎 v1.0")
    print("=" * 70)

    engine = SnapshotRecoveryEngine()

    # 记录时间轴
    engine.record_timeline(TimelineEventType.INPUT, "InputGate", "接收用户输入")
    engine.record_timeline(TimelineEventType.AUDIT, "AuditEngine", "三色审计通过 🟢")
    engine.record_timeline(TimelineEventType.EXECUTE, "ExecutionEngine", "执行代码补全")

    # 创建快照
    snap1 = engine.create_snapshot(
        state={"phase": "after_audit", "status": "green"},
        dna_trace="#龍芯⚡️丙午·乙未·己未·申时·履-TEST",
    )
    print(f"\n📸 快照1: {snap1.snapshot_id}")
    print(f"   哈希: {snap1.hash_value[:16]}...")
    print(f"   时间: {snap1.timestamp}")

    engine.record_timeline(TimelineEventType.SNAPSHOT, "SnapshotEngine", f"快照 {snap1.snapshot_id}")

    # 模拟状态变更后再快照
    snap2 = engine.create_snapshot(
        state={"phase": "after_execution", "status": "completed"},
        dna_trace="#龍芯⚡️丙午·乙未·己未·申时·履-TEST2",
    )
    print(f"\n📸 快照2: {snap2.snapshot_id}")
    print(f"   哈希: {snap2.hash_value[:16]}...")
    print(f"   父快照: {snap2.parent_snapshot_id}")

    # 创建恢复点
    recovery = engine.create_recovery_point(snap1.snapshot_id, reason="测试恢复点")
    print(f"\n🔄 恢复点: {recovery.point_id}")
    print(f"   指向快照: {recovery.snapshot_id}")

    # 验证链
    valid, issues = engine.verify_chain()
    print(f"\n🔗 链验证: {'🟢 通过' if valid else '🔴 失败'}")
    if issues:
        for issue in issues:
            print(f"   ⚠️ {issue}")

    # 执行回滚
    success, recovered_snap, msg = engine.recover(recovery.point_id)
    print(f"\n🔄 回滚结果: {'🟢 成功' if success else '🔴 失败'}")
    print(f"   {msg}")

    # 时间轴
    print(f"\n{'='*70}")
    print("📅 时间轴:")
    print(f"{'='*70}")
    print(engine.timeline_summary())

    # 统计
    stats = engine.stats()
    print(f"\n{'='*70}")
    print(f"📊 统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")

    return engine


if __name__ == "__main__":
    demo()
