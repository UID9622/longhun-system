#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂权重容错引擎 v2.0

实现《龍魂系统·权重与容错机制 v2.0 —— 底座常驻协议之忠孝义不动点》
DNA: #龍芯⚡️2026-06-29-LONGHUN-WEIGHT-ENGINE-v2-UID9622
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

DNA = "#龍芯⚡️2026-06-29-LONGHUN-WEIGHT-ENGINE-v2-UID9622"


class LoyaltyFilialRighteousness(Enum):
    """忠孝义不动点"""
    忠 = "忠于人民·不忠于权力资本"
    孝 = "尊重根脉·传承契约·龍字永繁"
    义 = "弱者权重最高·强者不可欺人"


class WeightState(Enum):
    高信任 = "高信任"
    信任 = "信任"
    需注意 = "需注意"
    待观察 = "待观察"
    低信任 = "低信任"
    熔断态 = "熔断态"
    永久熔断 = "永久熔断"


@dataclass
class Event:
    kind: str  # "violation" | "contribution" | "l0_violation"
    dimension: str
    timestamp: datetime
    weight_delta: int
    dna: str
    note: str = ""


@dataclass
class WeightProfile:
    subject: str
    base_weight: int = 60
    events: List[Event] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def days_since(self, ts: datetime) -> int:
        return (datetime.now(timezone.utc) - ts).days

    def decay_factor(self, ts: datetime) -> float:
        days = self.days_since(ts)
        return max(0.3, 1.0 - days / 90.0)

    def compute(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        score = 0
        violation_count = 0
        contribution_count = 0
        l0_count = 0
        first_violation_date: Optional[datetime] = None
        observation_active = False

        for ev in self.events:
            if ev.kind == "violation":
                violation_count += 1
                score += ev.weight_delta * self.decay_factor(ev.timestamp)
                if first_violation_date is None:
                    first_violation_date = ev.timestamp
            elif ev.kind == "contribution":
                contribution_count += 1
                score += ev.weight_delta * self.decay_factor(ev.timestamp)
            elif ev.kind == "l0_violation":
                l0_count += 1

        # L0 不动点违规：永久熔断
        if l0_count > 0:
            return self._result(0, WeightState.永久熔断, violation_count, contribution_count, l0_count)

        weight = max(0, min(100, self.base_weight + int(score)))

        # 状态判定
        if weight >= 90:
            state = WeightState.高信任
        elif weight >= 70:
            state = WeightState.信任
        elif weight >= 50:
            state = WeightState.需注意
        elif weight >= 30:
            state = WeightState.低信任
        else:
            state = WeightState.熔断态

        # 首次违规观察期
        if violation_count == 1 and contribution_count == 0 and first_violation_date:
            if (now - first_violation_date).days <= 30:
                state = WeightState.待观察
                weight = self.base_weight  # 首次违规不立即扣分

        return self._result(weight, state, violation_count, contribution_count, l0_count)

    def _result(self, weight: int, state: WeightState, violations: int, contributions: int, l0: int) -> Dict[str, Any]:
        return {
            "subject": self.subject,
            "weight": weight,
            "state": state.value,
            "violations": violations,
            "contributions": contributions,
            "l0_violations": l0,
            "dna": DNA,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def record_violation(self, dimension: str, note: str = "", l0: bool = False) -> Dict[str, Any]:
        delta = -10 if not l0 else 0
        kind = "l0_violation" if l0 else "violation"
        ev = Event(
            kind=kind,
            dimension=dimension,
            timestamp=datetime.now(timezone.utc),
            weight_delta=delta,
            dna=f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{kind.upper()}-{self.subject}",
            note=note,
        )
        self.events.append(ev)
        return self.compute()

    def record_contribution(self, dimension: str, note: str = "") -> Dict[str, Any]:
        ev = Event(
            kind="contribution",
            dimension=dimension,
            timestamp=datetime.now(timezone.utc),
            weight_delta=+12,
            dna=f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-CONTRIBUTION-{self.subject}",
            note=note,
        )
        self.events.append(ev)
        return self.compute()


class LongHunWeightEngine:
    """权重引擎统一入口"""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage = storage_path or Path.home() / ".longhun" / "weight_profiles.jsonl"
        self.storage.parent.mkdir(parents=True, exist_ok=True)
        self.profiles: Dict[str, WeightProfile] = {}
        self._load()

    def _load(self):
        if not self.storage.exists():
            return
        with open(self.storage, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    prof = WeightProfile(
                        subject=data["subject"],
                        base_weight=data.get("base_weight", 60),
                        events=[Event(**e) for e in data.get("events", [])],
                        created_at=datetime.fromisoformat(data["created_at"]),
                    )
                    self.profiles[prof.subject] = prof
                except Exception:
                    continue

    def save(self):
        with open(self.storage, "w", encoding="utf-8") as f:
            for prof in self.profiles.values():
                record = {
                    "subject": prof.subject,
                    "base_weight": prof.base_weight,
                    "created_at": prof.created_at.isoformat(),
                    "events": [
                        {
                            "kind": e.kind,
                            "dimension": e.dimension,
                            "timestamp": e.timestamp.isoformat(),
                            "weight_delta": e.weight_delta,
                            "dna": e.dna,
                            "note": e.note,
                        }
                        for e in prof.events
                    ],
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def get(self, subject: str) -> WeightProfile:
        if subject not in self.profiles:
            self.profiles[subject] = WeightProfile(subject=subject)
        return self.profiles[subject]

    def audit(self, subject: str) -> Dict[str, Any]:
        return self.get(subject).compute()


def demo():
    engine = LongHunWeightEngine()
    p = engine.get("demo_user")

    print("初始:", p.compute())
    print("首次违规（非L0）:", p.record_violation("download_risk", "下载可疑文件"))
    print("贡献抵消:", p.record_contribution("report_risk", "举报真实攻击"))
    print("L0 违规（欺民）:", p.record_violation("bully_civilian", "欺负老百姓", l0=True))
    engine.save()


if __name__ == "__main__":
    demo()
