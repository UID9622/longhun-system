# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂君子协议 · 诚信评级与违约清算算法核心
DNA: #龍芯⚡️2026-06-26-LONGHUN-TRUST-CORE-v1.0

以中华人民共和国法律为底线，以人民为基石，
量化道德值 M、人品值 P、诚信值 I，输出综合信用分 S。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class Grade(Enum):
    AAA = "AAA"  # 90~100 🟢
    AA = "AA"    # 80~89 🟢
    A = "A"      # 70~79 🟡
    B = "B"      # 60~69 🟡
    C = "C"      # 50~59 🔴
    D = "D"      # <50 🔴


class SlaughterLevel(Enum):
    NONE = 0
    WARNING = 1      # 1级：警示，降级至B，限期整改
    PUNISHMENT = 2   # 2级：惩戒，降级至C，强制贡献证明
    SLAUGHTER = 3    # 3级：杀猪，D级，链上永久标记


class EventType(Enum):
    MORAL = "moral"
    CHARACTER = "character"
    INTEGRITY = "integrity"
    VIOLATION = "violation"
    CONTRIBUTION = "contribution"
    REPORT = "report"
    SLAUGHTER_TRIGGER = "slaughter_trigger"
    REDEMPTION = "redemption"


@dataclass
class TrustEvent:
    event_type: EventType
    delta: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "delta": self.delta,
            "description": self.description,
            "timestamp": self.timestamp,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TrustEvent":
        return cls(
            event_type=EventType(d["event_type"]),
            delta=d.get("delta", {}),
            description=d.get("description", ""),
            timestamp=d.get("timestamp", datetime.now(timezone.utc).isoformat()),
            meta=d.get("meta", {}),
        )


class TrustProfile:
    """
    单个参与者的君子协议信用档案。
    """

    M0 = 80.0
    P0 = 75.0
    I0 = 90.0

    CONTRIBUTION_VALUES: Dict[str, float] = {
        "bug_report": 5.0,
        "governance_vote": 2.0,
        "help_others": 10.0,
        "code_protocol": 30.0,
        "compensation": 20.0,
    }

    REDEMPTION_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "B2A": {"from": Grade.B, "to": Grade.A, "contrib": 50.0, "days": 0},
        "C2B": {"from": Grade.C, "to": Grade.B, "contrib": 80.0, "days": 0},
        "D2C": {"from": Grade.D, "to": Grade.C, "contrib": 120.0, "days": 90},
    }

    def __init__(self, uid: str, name: str = ""):
        self.uid = uid
        self.name = name or uid
        self.moral = self.M0
        self.character = self.P0
        self.integrity = self.I0
        self.violations = 0
        self.contributions = 0.0
        self.slaughter_count = 0
        self.events: List[TrustEvent] = []
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.last_updated = self.created_at

    # ---------- 评分计算 ----------
    def update_scores(self) -> None:
        self.moral = max(0.0, min(100.0, self.moral))
        self.character = max(0.0, min(100.0, self.character))
        self.integrity = max(0.0, min(100.0, self.integrity))
        self.last_updated = datetime.now(timezone.utc).isoformat()

    @property
    def score(self) -> float:
        return 0.4 * self.moral + 0.3 * self.character + 0.3 * self.integrity

    @property
    def grade(self) -> Grade:
        s = self.score
        if s >= 90:
            return Grade.AAA
        if s >= 80:
            return Grade.AA
        if s >= 70:
            return Grade.A
        if s >= 60:
            return Grade.B
        if s >= 50:
            return Grade.C
        return Grade.D

    # ---------- 事件应用 ----------
    def apply(self, event: TrustEvent) -> None:
        self.events.append(event)
        d = event.delta
        if "moral" in d:
            self.moral += d["moral"]
        if "character" in d:
            self.character += d["character"]
        if "integrity" in d:
            self.integrity += d["integrity"]
        if "contributions" in d:
            self.contributions += d["contributions"]
        self.update_scores()

    # ---------- 道德 / 人品 / 诚信 行为 ----------
    def moral_action(self, action: str, description: str = "") -> TrustEvent:
        """
        action: breach_acknowledged, word_game, malicious_delay,
                active_remedy, exceed_expectation, verified_report
        """
        rules = {
            "breach_acknowledged": {"moral": -30.0},
            "word_game": {"moral": -20.0},
            "malicious_delay": {"moral": -25.0},
            "active_remedy": {"moral": +15.0},
            "exceed_expectation": {"moral": +10.0},
            "verified_report": {"moral": +5.0},
        }
        delta = rules.get(action, {})
        evt = TrustEvent(EventType.MORAL, delta, description or action)
        self.apply(evt)
        return evt

    def character_action(self, action: str, description: str = "") -> TrustEvent:
        """
        action: info_asymmetry, abuse_ecosystem, rude_after_breach,
                open_info, help_others, monthly_contrib
        """
        rules = {
            "info_asymmetry": {"character": -35.0},
            "abuse_ecosystem": {"character": -30.0},
            "rude_after_breach": {"character": -25.0},
            "open_info": {"character": +15.0},
            "help_others": {"character": +10.0},
            "monthly_contrib": {"character": +5.0},
        }
        delta = rules.get(action, {})
        evt = TrustEvent(EventType.CHARACTER, delta, description or action)
        self.apply(evt)
        return evt

    def integrity_action(self, action: str, description: str = "") -> TrustEvent:
        """
        action: no_violation_12m, active_audit
        """
        rules = {
            "no_violation_12m": {"integrity": +10.0},
            "active_audit": {"integrity": +5.0},
        }
        delta = rules.get(action, {})
        evt = TrustEvent(EventType.INTEGRITY, delta, description or action)
        self.apply(evt)
        return evt

    # ---------- 违约 ----------
    def violate(self, description: str = "", evidence: str = "") -> TrustEvent:
        """
        记录一次上链违约。诚信值惩罚逐次递增：20, 40, 60, ...
        """
        self.violations += 1
        penalty = 20.0 * self.violations
        evt = TrustEvent(
            EventType.VIOLATION,
            {"integrity": -penalty},
            description or f"第{self.violations}次违约",
            meta={"violation_count": self.violations, "penalty": penalty, "evidence": evidence},
        )
        self.apply(evt)
        return evt

    # ---------- 贡献 ----------
    def contribute(self, contrib_type: str, description: str = "") -> TrustEvent:
        """
        contrib_type: bug_report, governance_vote, help_others,
                      code_protocol, compensation
        """
        value = self.CONTRIBUTION_VALUES.get(contrib_type, 0.0)
        evt = TrustEvent(
            EventType.CONTRIBUTION,
            {"contributions": value, "character": 5.0, "moral": 5.0},
            description or contrib_type,
            meta={"contrib_type": contrib_type, "value": value},
        )
        self.apply(evt)
        return evt

    # ---------- 举报 ----------
    def report(self, target_uid: str, description: str = "", verified: bool = False) -> TrustEvent:
        """记录一次举报事件；如核实，对举报者的人品值进行奖励。"""
        meta = {"target_uid": target_uid, "verified": verified, "description": description}
        if verified:
            evt = TrustEvent(EventType.REPORT, {"character": +5.0}, f"核实举报 {target_uid}", meta=meta)
        else:
            evt = TrustEvent(EventType.REPORT, {}, f"举报 {target_uid}（待核实）", meta=meta)
        self.apply(evt)
        return evt

    # ---------- 杀猪清算 ----------
    def check_slaughter(self) -> Dict[str, Any]:
        """
        触发条件（满足任意两条）：
        1. S < 50
        2. 违约次数 >= 3
        3. 被有效举报 >= 3
        4. 利用信息差造成实际损失
        5. 恶意破坏生态
        """
        conditions = [
            ("score_below_50", self.score < 50),
            ("violations_ge_3", self.violations >= 3),
            ("reports_ge_3", self._verified_reports_against() >= 3),
            ("info_asymmetry_loss", False),  # 需外部证据输入
            ("malicious_damage", False),
        ]
        met = [name for name, ok in conditions if ok]
        triggered = len(met) >= 2

        result = {
            "triggered": triggered,
            "conditions": {name: ok for name, ok in conditions},
            "met": met,
            "level": SlaughterLevel.NONE,
        }

        if triggered:
            self.slaughter_count += 1
            if self.slaughter_count == 1:
                result["level"] = SlaughterLevel.WARNING
            elif self.slaughter_count == 2:
                result["level"] = SlaughterLevel.PUNISHMENT
            else:
                result["level"] = SlaughterLevel.SLAUGHTER

            evt = TrustEvent(
                EventType.SLAUGHTER_TRIGGER,
                {},
                f"触发{result['level'].name}级清算",
                meta={"level": result["level"].value, "conditions": met},
            )
            self.apply(evt)

        return result

    def _verified_reports_against(self) -> int:
        # 简化：当前档案里不含他人对自己的举报，预留接口
        return 0

    # ---------- 赎回 ----------
    def can_redeem(self, target_grade: Grade) -> Dict[str, Any]:
        """检查是否可以从当前等级赎回至目标等级。"""
        current = self.grade
        mapping = {
            (Grade.B, Grade.A): self.REDEMPTION_THRESHOLDS["B2A"],
            (Grade.C, Grade.B): self.REDEMPTION_THRESHOLDS["C2B"],
            (Grade.D, Grade.C): self.REDEMPTION_THRESHOLDS["D2C"],
        }
        rule = mapping.get((current, target_grade))
        if not rule:
            return {"ok": False, "reason": f"不支持从 {current.value} 赎回至 {target_grade.value}"}
        ok = self.contributions >= rule["contrib"]
        # 观察期简化：以 created_at 与当前时间差估算天数
        days_since = self._days_since_created()
        ok = ok and days_since >= rule["days"]
        return {
            "ok": ok,
            "required_contrib": rule["contrib"],
            "current_contrib": self.contributions,
            "required_days": rule["days"],
            "days_since_created": days_since,
        }

    def redeem(self, target_grade: Grade) -> TrustEvent:
        info = self.can_redeem(target_grade)
        if not info["ok"]:
            raise ValueError(info["reason"])
        evt = TrustEvent(
            EventType.REDEMPTION,
            {"integrity": +25.0},
            f"赎回至 {target_grade.value}",
            meta={"target_grade": target_grade.value, "contributions": self.contributions},
        )
        self.apply(evt)
        return evt

    def _days_since_created(self) -> int:
        try:
            created = datetime.fromisoformat(self.created_at)
            return (datetime.now(timezone.utc) - created).days
        except Exception:
            return 0

    # ---------- 序列化 ----------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "moral": self.moral,
            "character": self.character,
            "integrity": self.integrity,
            "score": self.score,
            "grade": self.grade.value,
            "violations": self.violations,
            "contributions": self.contributions,
            "slaughter_count": self.slaughter_count,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TrustProfile":
        p = cls(d["uid"], d.get("name", d["uid"]))
        p.moral = d.get("moral", cls.M0)
        p.character = d.get("character", cls.P0)
        p.integrity = d.get("integrity", cls.I0)
        p.violations = d.get("violations", 0)
        p.contributions = d.get("contributions", 0.0)
        p.slaughter_count = d.get("slaughter_count", 0)
        p.created_at = d.get("created_at", datetime.now(timezone.utc).isoformat())
        p.last_updated = d.get("last_updated", p.created_at)
        p.events = [TrustEvent.from_dict(e) for e in d.get("events", [])]
        return p
