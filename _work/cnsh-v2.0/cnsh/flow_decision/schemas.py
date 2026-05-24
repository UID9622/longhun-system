# -*- coding: utf-8 -*-
"""FlowDecisionNode v4.1 — 44 字段（含三才决策输入/得分）"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FlowDecisionNode:
    title: str = ""
    parent_dna: str = ""
    confirm_code: str = ""
    gpg: str = ""
    eternal_seal: str = ""
    privacy_visibility: str = "internal"
    privacy_trace_mode: str = "chain"
    privacy_mode: str = "normal"
    math_dr: int = 0
    math_element: str = "土"
    sancai_heaven: float = 0.35
    sancai_human: float = 0.50
    sancai_earth: float = 0.15
    sancai_input_heaven: float = 0.5
    sancai_input_earth: float = 0.5
    sancai_input_human: float = 0.8
    sancai_score: float = 0.0
    sancai_advice: str = ""
    sancai_pass: bool = False
    audit_need_uid_confirm: bool = False
    audit_tricolor: str = "🟢"
    route_palace: List[str] = field(default_factory=list)
    route_bucket: str = ""
    storage_notion: bool = False
    storage_jsonl: bool = True
    storage_sqlite: bool = True
    storage_destroy_proof: str = ""
    storage_seal_proof: str = ""
    result_status: str = "enter"
    result_operator: str = ""
    raw_body_allowed: bool = True
    content_fingerprint_sha256: str = ""
    dna_current: str = ""
    dna_child: str = ""
    dna_parent_valid: bool = True
    ipa_chain_complete: bool = False
    gate_trace: List[str] = field(default_factory=list)
    persona_main_trace: List[str] = field(default_factory=list)
    level: str = "L3日常"
    p0_touched: bool = False
    auto_execute: bool = False
    fuse_reason: str = ""
    shengke_note: str = ""
    warmup_score: float = 0.0

    def field_count(self) -> int:
        return len(self.__dataclass_fields__)


EXPECTED_FIELD_COUNT = 44
