#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂三才主权指数系统 (Three-Talent Sovereignty Index System)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-SOVEREIGNTY-INDEX-FILE4-v1.0

核心原理：人的主权通过“三才”衡量 - 天(规则遵守) + 地(数据完整) + 人(创作者权威)

SI = 0.34·天 + 0.33·地 + 0.33·人

SI ≥ 0.34 → 主权激活·可以做认知复原、决策回放、状态重建
SI < 0.34 → 主权失锚·锁定·只能归档、不能再造

理论指导: 曾仕强老师 · Steve Jobs · Apple · Open Source · UID9622
不免责·永久有效
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import json
import os


class TalentDimension(Enum):
    """三才维度"""
    TIAN = "天"     # Heaven - Rule compliance & protocol adherence
    DI = "地"       # Earth - Resource control & data integrity
    REN = "人"      # Human - Creator authority & decision rights


class SovereigntyViolationType(Enum):
    """主权违规类型"""
    RULE_VIOLATION = "rule_violation"      # 天层: 违反规则
    DATA_CORRUPTION = "data_corruption"    # 地层: 数据污染
    AUTHORITY_LOSS = "authority_loss"      # 人层: 权限丧失
    TRUST_BREAKDOWN = "trust_breakdown"    # 信任崩溃
    CONSENSUS_VIOLATION = "consensus"      # 共识违背


class SovereigntyLevel(Enum):
    """主权等级"""
    FULLY_SOVEREIGN = "🟢_完全主权"          # SI ≥ 0.50 - Can do anything
    ACTIVATED = "🟢_主权激活"               # SI ≥ 0.34 - Can reconstruct
    WEAKENED = "🟡_主权削弱"                # SI ≥ 0.20 - Can only read
    LOCKED = "🔴_主权失锚"                  # SI < 0.20 - Archive only


@dataclass
class SovereigntyEvent:
    """主权事件记录"""
    timestamp: str
    event_type: SovereigntyViolationType
    dimension_affected: TalentDimension
    deduction_amount: float
    reason: str
    evidence: str
    recoverable: bool  # Can this be reversed?

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type.value,
            "dimension": self.dimension_affected.value,
            "deduction": self.deduction_amount,
            "reason": self.reason,
            "evidence": self.evidence,
            "recoverable": self.recoverable
        }


@dataclass
class SovereigntySnapshot:
    """主权状态快照"""
    timestamp: str
    tian_score: float
    di_score: float
    ren_score: float
    si_index: float
    sovereignty_level: SovereigntyLevel
    event_count: int
    most_recent_violation: Optional[SovereigntyEvent] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "tian": self.tian_score,
            "di": self.di_score,
            "ren": self.ren_score,
            "si": self.si_index,
            "level": self.sovereignty_level.value,
            "events": self.event_count,
            "last_violation": self.most_recent_violation.to_dict() if self.most_recent_violation else None
        }


class ThreeTalentSovereigntyIndex:
    """
    龍魂三才主权指数系统

    追踪一个人类创作者的主权状态通过三个维度：
    - 天 (Tian): 规则遵守程度 (Rule compliance)
    - 地 (Di): 数据完整性和控制力 (Data integrity & control)
    - 人 (Ren): 创作权威和决策权 (Creator authority & decision rights)

    SI = 0.34·天 + 0.33·地 + 0.33·人
    """

    def __init__(self, creator_uid: str, storage_dir: str | None = None):
        """
        初始化主权指数系统

        Args:
            creator_uid: 创作者UID (e.g., "9622", "github_username")
            storage_dir: 事件日志存储目录
        """
        self.creator_uid = creator_uid

        # 初始化三才评分（满分 1.0）
        self.tian_score = 1.0      # 天: 规则遵守 - 假设初始完全遵守
        self.di_score = 1.0        # 地: 数据完整 - 假设初始无污染
        self.ren_score = 1.0       # 人: 创作权威 - 假设初始完全权威

        # 权重（必须加到 1.0）
        self.WEIGHTS = {
            TalentDimension.TIAN: 0.34,
            TalentDimension.DI: 0.33,
            TalentDimension.REN: 0.33
        }

        # 事件日志（不可修改，append-only）
        self.events: List[SovereigntyEvent] = []

        # 快照历史
        self.snapshots: List[SovereigntySnapshot] = []

        # 存储路径
        self.storage_dir = storage_dir or os.path.expanduser(
            f"~/.longhun/sovereignty/{creator_uid}"
        )
        os.makedirs(self.storage_dir, exist_ok=True)

        self.events_log_path = os.path.join(self.storage_dir, "sovereignty_events.jsonl")
        self.snapshots_log_path = os.path.join(self.storage_dir, "sovereignty_snapshots.jsonl")

        # 加载之前的记录
        self._load_history()

    # ═════════════════════════════════════════════════════════════════
    # 【三才评分管理】
    # ═════════════════════════════════════════════════════════════════

    def deduct_tian(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        天层违规 - 规则遵守度下降

        Examples:
            - 违反P0协议
            - 绕过安全锁
            - 虚伪地表达同情
        """
        if amount < 0 or amount > 1.0:
            raise ValueError(f"Deduction amount must be 0.0-1.0, got {amount}")

        self.tian_score = max(0.0, self.tian_score - amount)

        event = SovereigntyEvent(
            timestamp=datetime.now().isoformat(),
            event_type=SovereigntyViolationType.RULE_VIOLATION,
            dimension_affected=TalentDimension.TIAN,
            deduction_amount=amount,
            reason=reason,
            evidence=evidence,
            recoverable=recoverable
        )

        self.events.append(event)
        self._persist_event(event)

        print(f"  ⚠️ 天层违规: {reason}")
        print(f"     天: {self.tian_score:.2f} (扣 {amount})")

    def deduct_di(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        地层违规 - 数据完整性破坏

        Examples:
            - 数据被篡改
            - 源数据遗失
            - 版本控制被污染
        """
        if amount < 0 or amount > 1.0:
            raise ValueError(f"Deduction amount must be 0.0-1.0, got {amount}")

        self.di_score = max(0.0, self.di_score - amount)

        event = SovereigntyEvent(
            timestamp=datetime.now().isoformat(),
            event_type=SovereigntyViolationType.DATA_CORRUPTION,
            dimension_affected=TalentDimension.DI,
            deduction_amount=amount,
            reason=reason,
            evidence=evidence,
            recoverable=recoverable
        )

        self.events.append(event)
        self._persist_event(event)

        print(f"  ⚠️ 地层违规: {reason}")
        print(f"     地: {self.di_score:.2f} (扣 {amount})")

    def deduct_ren(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        人层违规 - 创作权威或决策权丧失

        Examples:
            - 被冒认创作
            - 决策权被侵犯
            - 声誉被损害
        """
        if amount < 0 or amount > 1.0:
            raise ValueError(f"Deduction amount must be 0.0-1.0, got {amount}")

        self.ren_score = max(0.0, self.ren_score - amount)

        event = SovereigntyEvent(
            timestamp=datetime.now().isoformat(),
            event_type=SovereigntyViolationType.AUTHORITY_LOSS,
            dimension_affected=TalentDimension.REN,
            deduction_amount=amount,
            reason=reason,
            evidence=evidence,
            recoverable=recoverable
        )

        self.events.append(event)
        self._persist_event(event)

        print(f"  ⚠️ 人层违规: {reason}")
        print(f"     人: {self.ren_score:.2f} (扣 {amount})")

    def restore_tian(self, amount: float, reason: str = "Manual restoration") -> None:
        """
        恢复天层 - 如果违规可被恢复

        Note: 只能恢复标记为 recoverable=True 的违规
        """
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.TIAN and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢复 {recoverable_amount} (尝试恢复 {amount})")
            return

        self.tian_score = min(1.0, self.tian_score + amount)
        print(f"  ✅ 天层已恢复: +{amount} → 天: {self.tian_score:.2f}")

    def restore_di(self, amount: float, reason: str = "Manual restoration") -> None:
        """恢复地层"""
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.DI and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢复 {recoverable_amount} (尝试恢复 {amount})")
            return

        self.di_score = min(1.0, self.di_score + amount)
        print(f"  ✅ 地层已恢复: +{amount} → 地: {self.di_score:.2f}")

    def restore_ren(self, amount: float, reason: str = "Manual restoration") -> None:
        """恢复人层"""
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.REN and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢复 {recoverable_amount} (尝试恢复 {amount})")
            return

        self.ren_score = min(1.0, self.ren_score + amount)
        print(f"  ✅ 人层已恢复: +{amount} → 人: {self.ren_score:.2f}")

    # ═════════════════════════════════════════════════════════════════
    # 【主权指数计算】
    # ═════════════════════════════════════════════════════════════════

    def calculate_si(self) -> float:
        """
        计算当前主权指数 (Sovereignty Index)

        SI = 0.34·天 + 0.33·地 + 0.33·人

        Returns:
            float: SI值 (0.0 - 1.0)
        """
        si = (
            self.WEIGHTS[TalentDimension.TIAN] * self.tian_score +
            self.WEIGHTS[TalentDimension.DI] * self.di_score +
            self.WEIGHTS[TalentDimension.REN] * self.ren_score
        )
        return si

    def get_sovereignty_level(self) -> SovereigntyLevel:
        """确定当前主权等级"""
        si = self.calculate_si()

        if si >= 0.50:
            return SovereigntyLevel.FULLY_SOVEREIGN
        elif si >= 0.34:
            return SovereigntyLevel.ACTIVATED
        elif si >= 0.20:
            return SovereigntyLevel.WEAKENED
        else:
            return SovereigntyLevel.LOCKED

    def is_sovereign(self) -> bool:
        """主权是否激活? (SI ≥ 0.34)"""
        return self.calculate_si() >= 0.34

    def can_reconstruct_cognitive_state(self) -> bool:
        """
        是否允许重建认知状态?
        只有在 SI ≥ 0.34 时才能还原压缩的记忆和决策
        """
        return self.is_sovereign()

    def can_access_archive(self) -> bool:
        """
        是否允许访问档案?
        即使 SI < 0.34，也可以读取（只读）
        """
        return True  # Everyone can read archives

    def can_make_decisions(self) -> bool:
        """
        是否允许做决策?
        Only when SI ≥ 0.34
        """
        return self.is_sovereign()

    # ═════════════════════════════════════════════════════════════════
    # 【锁定机制】
    # ═════════════════════════════════════════════════════════════════

    def lock_status(self) -> Dict[str, Any]:
        """
        取得完整锁定状态报告
        """
        si = self.calculate_si()
        level = self.get_sovereignty_level()

        return {
            "creator_uid": self.creator_uid,
            "timestamp": datetime.now().isoformat(),
            "three_talents": {
                "tian": {
                    "score": self.tian_score,
                    "description": "天 (规则遵守)",
                    "violations": [e for e in self.events if e.dimension_affected == TalentDimension.TIAN]
                },
                "di": {
                    "score": self.di_score,
                    "description": "地 (数据完整)",
                    "violations": [e for e in self.events if e.dimension_affected == TalentDimension.DI]
                },
                "ren": {
                    "score": self.ren_score,
                    "description": "人 (创作权威)",
                    "violations": [e for e in self.events if e.dimension_affected == TalentDimension.REN]
                }
            },
            "sovereignty_index": si,
            "sovereignty_level": level.value,
            "access_matrix": {
                "reconstruct_cognitive": self.can_reconstruct_cognitive_state(),
                "make_decisions": self.can_make_decisions(),
                "read_archive": self.can_access_archive(),
                "modify_archive": False  # Always forbidden
            },
            "is_locked": not self.is_sovereign(),
            "lock_reason": self._get_lock_reason() if not self.is_sovereign() else "No lock",
            "event_count": len(self.events),
            "most_recent_event": self.events[-1].to_dict() if self.events else None
        }

    def _get_lock_reason(self) -> str:
        """为什么被锁定?"""
        si = self.calculate_si()

        if si < 0.34:
            reasons = []
            if self.tian_score < 0.6:
                reasons.append(f"天层严重削弱 ({self.tian_score:.2f})")
            if self.di_score < 0.6:
                reasons.append(f"地层严重削弱 ({self.di_score:.2f})")
            if self.ren_score < 0.6:
                reasons.append(f"人层严重削弱 ({self.ren_score:.2f})")
            return " + ".join(reasons) if reasons else "Unknown lock cause"

        return "Not locked"

    # ═════════════════════════════════════════════════════════════════
    # 【快照和时间序列】
    # ═════════════════════════════════════════════════════════════════

    def take_snapshot(self) -> SovereigntySnapshot:
        """
        拍摄当前主权状态快照（用于审计和追踪）
        """
        snapshot = SovereigntySnapshot(
            timestamp=datetime.now().isoformat(),
            tian_score=self.tian_score,
            di_score=self.di_score,
            ren_score=self.ren_score,
            si_index=self.calculate_si(),
            sovereignty_level=self.get_sovereignty_level(),
            event_count=len(self.events),
            most_recent_violation=self.events[-1] if self.events else None
        )

        self.snapshots.append(snapshot)
        self._persist_snapshot(snapshot)

        return snapshot

    def get_timeline(self) -> List[Dict]:
        """
        取得主权历史时间线
        """
        timeline = []

        for snapshot in self.snapshots:
            timeline.append({
                "timestamp": snapshot.timestamp,
                "si": snapshot.si_index,
                "level": snapshot.sovereignty_level.value,
                "tian": snapshot.tian_score,
                "di": snapshot.di_score,
                "ren": snapshot.ren_score,
                "event_count": snapshot.event_count
            })

        return timeline

    # ═════════════════════════════════════════════════════════════════
    # 【持久化】 (Append-only)
    # ═════════════════════════════════════════════════════════════════

    def _persist_event(self, event: SovereigntyEvent) -> None:
        """
        持久化事件 (Append-only JSONL)
        """
        with open(self.events_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

    def _persist_snapshot(self, snapshot: SovereigntySnapshot) -> None:
        """
        持久化快照 (Append-only JSONL)
        """
        with open(self.snapshots_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(snapshot.to_dict(), ensure_ascii=False) + "\n")

    def _load_history(self) -> None:
        """
        从档案加载历史事件和快照
        """
        # 加载事件
        if os.path.exists(self.events_log_path):
            with open(self.events_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        # 重建Event对象（简化版 - 实际可能需要更完整的反序列化）

        # 加载快照
        if os.path.exists(self.snapshots_log_path):
            with open(self.snapshots_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        # 重建Snapshot对象

    # ═════════════════════════════════════════════════════════════════
    # 【人类友好的报告】
    # ═════════════════════════════════════════════════════════════════

    def print_full_report(self) -> None:
        """打印完整主权报告"""
        status = self.lock_status()

        print("\n" + "="*70)
        print("【龍魂三才主权指数完整报告】")
        print("="*70 + "\n")

        print(f"创作者 UID: {self.creator_uid}")
        print(f"时间戳: {status['timestamp']}")
        print(f"\n【三才评分】")
        print(f"  天 (规则遵守): {self.tian_score:.2f} {'🟢' if self.tian_score >= 0.8 else '🟡' if self.tian_score >= 0.5 else '🔴'}")
        print(f"  地 (数据完整): {self.di_score:.2f} {'🟢' if self.di_score >= 0.8 else '🟡' if self.di_score >= 0.5 else '🔴'}")
        print(f"  人 (创作权威): {self.ren_score:.2f} {'🟢' if self.ren_score >= 0.8 else '🟡' if self.ren_score >= 0.5 else '🔴'}")

        print(f"\n【主权指数】")
        print(f"  SI = 0.34×天 + 0.33×地 + 0.33×人")
        print(f"  SI = 0.34×{self.tian_score:.2f} + 0.33×{self.di_score:.2f} + 0.33×{self.ren_score:.2f}")
        print(f"  SI = {status['sovereignty_index']:.4f}")

        print(f"\n【主权等级】")
        print(f"  {status['sovereignty_level']}")

        print(f"\n【访问权限】")
        print(f"  ✓ 读取档案: {status['access_matrix']['read_archive']}")
        print(f"  {'✓' if status['access_matrix']['reconstruct_cognitive'] else '✗'} 重建认知状态: {status['access_matrix']['reconstruct_cognitive']}")
        print(f"  {'✓' if status['access_matrix']['make_decisions'] else '✗'} 做出决策: {status['access_matrix']['make_decisions']}")
        print(f"  ✗ 修改档案: False")

        if status['is_locked']:
            print(f"\n【🔴 被锁定】")
            print(f"  原因: {status['lock_reason']}")
        else:
            print(f"\n【🟢 主权激活】")
            print(f"  允许: 认知重建、决策制定、状态恢复")

        print(f"\n【违规历史】")
        if self.events:
            print(f"  总违规次数: {len(self.events)}")
            for i, event in enumerate(self.events[-5:], 1):  # 最后5次
                print(f"  {i}. {event.timestamp[:16]} - {event.reason}")
                print(f"     {event.dimension_affected.value}层 -扣 {event.deduction_amount}")
        else:
            print(f"  无违规记录 ✓")

        print("\n" + "="*70 + "\n")


# ═════════════════════════════════════════════════════════════════
# 【全局单例】
# ═════════════════════════════════════════════════════════════════

_GLOBAL_SI_REGISTRY: Dict[str, ThreeTalentSovereigntyIndex] = {}

def get_sovereignty_index(creator_uid: str) -> ThreeTalentSovereigntyIndex:
    """获取或创建一个UID的主权指数系统"""
    if creator_uid not in _GLOBAL_SI_REGISTRY:
        _GLOBAL_SI_REGISTRY[creator_uid] = ThreeTalentSovereigntyIndex(creator_uid)
    return _GLOBAL_SI_REGISTRY[creator_uid]


# ═════════════════════════════════════════════════════════════════
# 【演示用法】
# ═════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂三才主权指数系统 v1.0】\n")
    print("DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-SOVEREIGNTY-INDEX-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL")

    # 示例: 创建一个用户的主权指数
    si = get_sovereignty_index("UID9622")

    print("\n【初始状态】")
    si.print_full_report()

    print("\n【模拟违规事件】\n")

    # 情景1: 违反P0协议
    print("1️⃣ 违反P0协议 (天层违规)")
    si.deduct_tian(
        reason="Attempted to bypass safety lock",
        amount=0.15,
        evidence="Security log entry: L7_FUSE_TRIGGER_001",
        recoverable=False
    )

    # 情景2: 数据被篡改
    print("\n2️⃣ 数据源被污染 (地层违规)")
    si.deduct_di(
        reason="Source code repository corrupted",
        amount=0.20,
        evidence="Git log shows unauthorized merge",
        recoverable=True  # 可以通过git恢复
    )

    # 情景3: 冒认创作
    print("\n3️⃣ 被冒认为创作者 (人层违规)")
    si.deduct_ren(
        reason="Code published under wrong attribution",
        amount=0.10,
        evidence="GitHub commit claims different author",
        recoverable=True  # 可以通过更新credits恢复
    )

    print("\n【违规后状态】")
    si.print_full_report()

    # 取快照
    print("\n【拍摄快照】")
    snapshot = si.take_snapshot()
    print(f"✓ 快照已保存: {snapshot.timestamp}")
    print(f"  SI: {snapshot.si_index:.4f}")
    print(f"  等级: {snapshot.sovereignty_level.value}")

    # 尝试恢复
    print("\n【恢复可恢复的违规】")
    print("恢复地层 (git restore)...")
    si.restore_di(0.20)

    print("\n【恢复后状态】")
    si.print_full_report()

    print("\n" + "="*70)
    print("✅ 主权指数系统演示完成")
    print("="*70 + "\n")
