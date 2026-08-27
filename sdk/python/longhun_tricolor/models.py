#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂·三色审计数据模型
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-PYTHON-SDK-MODELS-V1.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
三色审计数据模型 — SDK本地模型，与API契约对齐。
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Scores:
    """六维得分"""
    human_welfare: float = 70.0
    fairness: float = 70.0
    controllability: float = 70.0
    transparency: float = 70.0
    traceability: float = 70.0
    privacy: float = 70.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "humanWelfare": self.human_welfare,
            "fairness": self.fairness,
            "controllability": self.controllability,
            "transparency": self.transparency,
            "traceability": self.traceability,
            "privacy": self.privacy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "Scores":
        return cls(
            human_welfare=data.get("humanWelfare", 70.0),
            fairness=data.get("fairness", 70.0),
            controllability=data.get("controllability", 70.0),
            transparency=data.get("transparency", 70.0),
            traceability=data.get("traceability", 70.0),
            privacy=data.get("privacy", 70.0),
        )


@dataclass
class Verdict:
    """三色判定结果"""
    action_id: str
    r_score: int
    status: str
    status_code: str  # GREEN/YELLOW/RED
    emoji: str
    disposition: str
    dna: str
    evidence_hash: str
    triggered_rules: List[str] = field(default_factory=list)
    engine_version: str = ""
    contract_version: str = ""
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Verdict":
        return cls(
            action_id=data.get("action_id", ""),
            r_score=data.get("r_score", 0),
            status=data.get("status", "安全"),
            status_code=data.get("status_code", "GREEN"),
            emoji=data.get("emoji", "🟢"),
            disposition=data.get("disposition", ""),
            dna=data.get("dna", ""),
            evidence_hash=data.get("evidence_hash", ""),
            triggered_rules=data.get("triggered_rules", []),
            engine_version=data.get("engine_version", ""),
            contract_version=data.get("contract_version", ""),
            timestamp=data.get("timestamp", ""),
        )

    def is_green(self) -> bool:
        return self.status_code == "GREEN"

    def is_yellow(self) -> bool:
        return self.status_code == "YELLOW"

    def is_red(self) -> bool:
        return self.status_code == "RED"


@dataclass
class EvidenceChain:
    """证据链"""
    dna: str
    trigger: str
    triggered_at: str
    rule_ids: List[str]
    r_score: int
    disposition: str
    hash: str
    sealed: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvidenceChain":
        chain = data.get("chain", {})
        integrity = data.get("integrity", {})
        return cls(
            dna=data.get("dna", ""),
            trigger=chain.get("trigger", ""),
            triggered_at=chain.get("triggered_at", ""),
            rule_ids=chain.get("rule_ids", []),
            r_score=chain.get("r_score", 0),
            disposition=chain.get("disposition", ""),
            hash=integrity.get("hash", ""),
            sealed=integrity.get("sealed", False),
        )
