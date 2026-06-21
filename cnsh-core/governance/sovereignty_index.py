#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂三才主權指數系統 (Three-Talent Sovereignty Index System)
DNA:#龍芯⚡️2026-06-03-SOVEREIGNTY-INDEX-FILE4-v1.0

核心原理：人的主權通過「三才」衡量 - 天(規則遵守) + 地(數據完整) + 人(創作者權威)

SI = 0.34·天 + 0.33·地 + 0.33·人

SI ≥ 0.34 → 主權激活·可以做認知復原、決策回放、狀態重建
SI < 0.34 → 主權失錨·鎖定·只能歸檔、不能再造

理論指導: 曾仕强老师 · Steve Jobs · Apple · Open Source · UID9622
不免責·永久有效
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
import os


class TalentDimension(Enum):
    """三才維度"""
    TIAN = "天"     # Heaven - Rule compliance & protocol adherence
    DI = "地"       # Earth - Resource control & data integrity
    REN = "人"      # Human - Creator authority & decision rights


class SovereigntyViolationType(Enum):
    """主權違規類型"""
    RULE_VIOLATION = "rule_violation"      # 天層: 違反規則
    DATA_CORRUPTION = "data_corruption"    # 地層: 數據污染
    AUTHORITY_LOSS = "authority_loss"      # 人層: 權限喪失
    TRUST_BREAKDOWN = "trust_breakdown"    # 信任崩潰
    CONSENSUS_VIOLATION = "consensus"      # 共識違背


class SovereigntyLevel(Enum):
    """主權等級"""
    FULLY_SOVEREIGN = "🟢_完全主權"          # SI ≥ 0.50 - Can do anything
    ACTIVATED = "🟢_主權激活"               # SI ≥ 0.34 - Can reconstruct
    WEAKENED = "🟡_主權削弱"                # SI ≥ 0.20 - Can only read
    LOCKED = "🔴_主權失錨"                  # SI < 0.20 - Archive only


@dataclass
class SovereigntyEvent:
    """主權事件記錄"""
    timestamp: str
    event_type: SovereigntyViolationType
    dimension_affected: TalentDimension
    deduction_amount: float
    reason: str
    evidence: str
    recoverable: bool  # Can this be reversed?

    def to_dict(self) -> Dict:
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
    """主權狀態快照"""
    timestamp: str
    tian_score: float
    di_score: float
    ren_score: float
    si_index: float
    sovereignty_level: SovereigntyLevel
    event_count: int
    most_recent_violation: Optional[SovereigntyEvent] = None

    def to_dict(self) -> Dict:
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
    龍魂三才主權指數系統

    追蹤一個人類創作者的主權狀態通過三個維度：
    - 天 (Tian): 規則遵守程度 (Rule compliance)
    - 地 (Di): 數據完整性和控制力 (Data integrity & control)
    - 人 (Ren): 創作權威和決策權 (Creator authority & decision rights)

    SI = 0.34·天 + 0.33·地 + 0.33·人
    """

    def __init__(self, creator_uid: str, storage_dir: str = None):
        """
        初始化主權指數系統

        Args:
            creator_uid: 創作者UID (e.g., "9622", "github_username")
            storage_dir: 事件日誌存儲目錄
        """
        self.creator_uid = creator_uid

        # 初始化三才評分（滿分 1.0）
        self.tian_score = 1.0      # 天: 規則遵守 - 假設初始完全遵守
        self.di_score = 1.0        # 地: 數據完整 - 假設初始無污染
        self.ren_score = 1.0       # 人: 創作權威 - 假設初始完全權威

        # 權重（必須加到 1.0）
        self.WEIGHTS = {
            TalentDimension.TIAN: 0.34,
            TalentDimension.DI: 0.33,
            TalentDimension.REN: 0.33
        }

        # 事件日誌（不可修改，append-only）
        self.events: List[SovereigntyEvent] = []

        # 快照歷史
        self.snapshots: List[SovereigntySnapshot] = []

        # 存儲路徑
        self.storage_dir = storage_dir or os.path.expanduser(
            f"~/.longhun/sovereignty/{creator_uid}"
        )
        os.makedirs(self.storage_dir, exist_ok=True)

        self.events_log_path = os.path.join(self.storage_dir, "sovereignty_events.jsonl")
        self.snapshots_log_path = os.path.join(self.storage_dir, "sovereignty_snapshots.jsonl")

        # 加載之前的記錄
        self._load_history()

    # ═════════════════════════════════════════════════════════════════
    # 【三才評分管理】
    # ═════════════════════════════════════════════════════════════════

    def deduct_tian(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        天層違規 - 規則遵守度下降

        Examples:
            - 違反P0協議
            - 繞過安全鎖
            - 虛偽地表達同情
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

        print(f"  ⚠️ 天層違規: {reason}")
        print(f"     天: {self.tian_score:.2f} (扣 {amount})")

    def deduct_di(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        地層違規 - 數據完整性破壞

        Examples:
            - 數據被篡改
            - 源數據遺失
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

        print(f"  ⚠️ 地層違規: {reason}")
        print(f"     地: {self.di_score:.2f} (扣 {amount})")

    def deduct_ren(self, reason: str, amount: float, evidence: str = "", recoverable: bool = False) -> None:
        """
        人層違規 - 創作權威或決策權喪失

        Examples:
            - 被冒認創作
            - 決策權被侵犯
            - 聲譽被損害
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

        print(f"  ⚠️ 人層違規: {reason}")
        print(f"     人: {self.ren_score:.2f} (扣 {amount})")

    def restore_tian(self, amount: float, reason: str = "Manual restoration") -> None:
        """
        恢復天層 - 如果違規可被恢復

        Note: 只能恢復標記為 recoverable=True 的違規
        """
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.TIAN and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢復 {recoverable_amount} (嘗試恢復 {amount})")
            return

        self.tian_score = min(1.0, self.tian_score + amount)
        print(f"  ✅ 天層已恢復: +{amount} → 天: {self.tian_score:.2f}")

    def restore_di(self, amount: float, reason: str = "Manual restoration") -> None:
        """恢復地層"""
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.DI and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢復 {recoverable_amount} (嘗試恢復 {amount})")
            return

        self.di_score = min(1.0, self.di_score + amount)
        print(f"  ✅ 地層已恢復: +{amount} → 地: {self.di_score:.2f}")

    def restore_ren(self, amount: float, reason: str = "Manual restoration") -> None:
        """恢復人層"""
        recoverable_amount = sum(
            e.deduction_amount for e in self.events
            if e.dimension_affected == TalentDimension.REN and e.recoverable
        )

        if amount > recoverable_amount:
            print(f"  ❌ 只能恢復 {recoverable_amount} (嘗試恢復 {amount})")
            return

        self.ren_score = min(1.0, self.ren_score + amount)
        print(f"  ✅ 人層已恢復: +{amount} → 人: {self.ren_score:.2f}")

    # ═════════════════════════════════════════════════════════════════
    # 【主權指數計算】
    # ═════════════════════════════════════════════════════════════════

    def calculate_si(self) -> float:
        """
        計算當前主權指數 (Sovereignty Index)

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
        """確定當前主權等級"""
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
        """主權是否激活? (SI ≥ 0.34)"""
        return self.calculate_si() >= 0.34

    def can_reconstruct_cognitive_state(self) -> bool:
        """
        是否允許重建認知狀態?
        只有在 SI ≥ 0.34 時才能還原壓縮的記憶和決策
        """
        return self.is_sovereign()

    def can_access_archive(self) -> bool:
        """
        是否允許訪問檔案?
        即使 SI < 0.34，也可以讀取（只讀）
        """
        return True  # Everyone can read archives

    def can_make_decisions(self) -> bool:
        """
        是否允許做決策?
        Only when SI ≥ 0.34
        """
        return self.is_sovereign()

    # ═════════════════════════════════════════════════════════════════
    # 【鎖定機制】
    # ═════════════════════════════════════════════════════════════════

    def lock_status(self) -> Dict:
        """
        取得完整鎖定狀態報告
        """
        si = self.calculate_si()
        level = self.get_sovereignty_level()

        return {
            "creator_uid": self.creator_uid,
            "timestamp": datetime.now().isoformat(),
            "three_talents": {
                "tian": {
                    "score": self.tian_score,
                    "description": "天 (規則遵守)",
                    "violations": [e for e in self.events if e.dimension_affected == TalentDimension.TIAN]
                },
                "di": {
                    "score": self.di_score,
                    "description": "地 (數據完整)",
                    "violations": [e for e in self.events if e.dimension_affected == TalentDimension.DI]
                },
                "ren": {
                    "score": self.ren_score,
                    "description": "人 (創作權威)",
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
        """為什麼被鎖定?"""
        si = self.calculate_si()

        if si < 0.34:
            reasons = []
            if self.tian_score < 0.6:
                reasons.append(f"天層嚴重削弱 ({self.tian_score:.2f})")
            if self.di_score < 0.6:
                reasons.append(f"地層嚴重削弱 ({self.di_score:.2f})")
            if self.ren_score < 0.6:
                reasons.append(f"人層嚴重削弱 ({self.ren_score:.2f})")
            return " + ".join(reasons) if reasons else "Unknown lock cause"

        return "Not locked"

    # ═════════════════════════════════════════════════════════════════
    # 【快照和時間序列】
    # ═════════════════════════════════════════════════════════════════

    def take_snapshot(self) -> SovereigntySnapshot:
        """
        拍攝當前主權狀態快照（用於審計和追蹤）
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
        取得主權歷史時間線
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
        從檔案加載歷史事件和快照
        """
        # 加載事件
        if os.path.exists(self.events_log_path):
            with open(self.events_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        # 重建Event對象（簡化版 - 實際可能需要更完整的反序列化）

        # 加載快照
        if os.path.exists(self.snapshots_log_path):
            with open(self.snapshots_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        # 重建Snapshot對象

    # ═════════════════════════════════════════════════════════════════
    # 【人類友好的報告】
    # ═════════════════════════════════════════════════════════════════

    def print_full_report(self) -> None:
        """列印完整主權報告"""
        status = self.lock_status()

        print("\n" + "="*70)
        print("【龍魂三才主權指數完整報告】")
        print("="*70 + "\n")

        print(f"創作者 UID: {self.creator_uid}")
        print(f"時間戳: {status['timestamp']}")
        print(f"\n【三才評分】")
        print(f"  天 (規則遵守): {self.tian_score:.2f} {'🟢' if self.tian_score >= 0.8 else '🟡' if self.tian_score >= 0.5 else '🔴'}")
        print(f"  地 (數據完整): {self.di_score:.2f} {'🟢' if self.di_score >= 0.8 else '🟡' if self.di_score >= 0.5 else '🔴'}")
        print(f"  人 (創作權威): {self.ren_score:.2f} {'🟢' if self.ren_score >= 0.8 else '🟡' if self.ren_score >= 0.5 else '🔴'}")

        print(f"\n【主權指數】")
        print(f"  SI = 0.34×天 + 0.33×地 + 0.33×人")
        print(f"  SI = 0.34×{self.tian_score:.2f} + 0.33×{self.di_score:.2f} + 0.33×{self.ren_score:.2f}")
        print(f"  SI = {status['sovereignty_index']:.4f}")

        print(f"\n【主權等級】")
        print(f"  {status['sovereignty_level']}")

        print(f"\n【訪問權限】")
        print(f"  ✓ 讀取檔案: {status['access_matrix']['read_archive']}")
        print(f"  {'✓' if status['access_matrix']['reconstruct_cognitive'] else '✗'} 重建認知狀態: {status['access_matrix']['reconstruct_cognitive']}")
        print(f"  {'✓' if status['access_matrix']['make_decisions'] else '✗'} 做出決策: {status['access_matrix']['make_decisions']}")
        print(f"  ✗ 修改檔案: False")

        if status['is_locked']:
            print(f"\n【🔴 被鎖定】")
            print(f"  原因: {status['lock_reason']}")
        else:
            print(f"\n【🟢 主權激活】")
            print(f"  允許: 認知重建、決策制定、狀態恢復")

        print(f"\n【違規歷史】")
        if self.events:
            print(f"  總違規次數: {len(self.events)}")
            for i, event in enumerate(self.events[-5:], 1):  # 最後5次
                print(f"  {i}. {event.timestamp[:16]} - {event.reason}")
                print(f"     {event.dimension_affected.value}層 -扣 {event.deduction_amount}")
        else:
            print(f"  無違規記錄 ✓")

        print("\n" + "="*70 + "\n")


# ═════════════════════════════════════════════════════════════════
# 【全局單例】
# ═════════════════════════════════════════════════════════════════

_GLOBAL_SI_REGISTRY: Dict[str, ThreeTalentSovereigntyIndex] = {}

def get_sovereignty_index(creator_uid: str) -> ThreeTalentSovereigntyIndex:
    """獲取或創建一個UID的主權指數系統"""
    if creator_uid not in _GLOBAL_SI_REGISTRY:
        _GLOBAL_SI_REGISTRY[creator_uid] = ThreeTalentSovereigntyIndex(creator_uid)
    return _GLOBAL_SI_REGISTRY[creator_uid]


# ═════════════════════════════════════════════════════════════════
# 【演示用法】
# ═════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂三才主權指數系統 v1.0】\n")
    print("DNA:#龍芯⚡️2026-06-03-SOVEREIGNTY-INDEX-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL")

    # 示例: 創建一個用戶的主權指數
    si = get_sovereignty_index("UID9622")

    print("\n【初始狀態】")
    si.print_full_report()

    print("\n【模擬違規事件】\n")

    # 情景1: 違反P0協議
    print("1️⃣ 違反P0協議 (天層違規)")
    si.deduct_tian(
        reason="Attempted to bypass safety lock",
        amount=0.15,
        evidence="Security log entry: L7_FUSE_TRIGGER_001",
        recoverable=False
    )

    # 情景2: 數據被篡改
    print("\n2️⃣ 數據源被污染 (地層違規)")
    si.deduct_di(
        reason="Source code repository corrupted",
        amount=0.20,
        evidence="Git log shows unauthorized merge",
        recoverable=True  # 可以通過git恢復
    )

    # 情景3: 冒認創作
    print("\n3️⃣ 被冒認為創作者 (人層違規)")
    si.deduct_ren(
        reason="Code published under wrong attribution",
        amount=0.10,
        evidence="GitHub commit claims different author",
        recoverable=True  # 可以通過更新credits恢復
    )

    print("\n【違規後狀態】")
    si.print_full_report()

    # 取快照
    print("\n【拍攝快照】")
    snapshot = si.take_snapshot()
    print(f"✓ 快照已保存: {snapshot.timestamp}")
    print(f"  SI: {snapshot.si_index:.4f}")
    print(f"  等級: {snapshot.sovereignty_level.value}")

    # 嘗試恢復
    print("\n【恢復可恢復的違規】")
    print("恢復地層 (git restore)...")
    si.restore_di(0.20)

    print("\n【恢復後狀態】")
    si.print_full_report()

    print("\n" + "="*70)
    print("✅ 主權指數系統演示完成")
    print("="*70 + "\n")
