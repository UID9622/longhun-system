# -*- coding: utf-8 -*-
"""
主权个人容器 · 策略层
DNA: #龍芯⚡️2026-05-15-SOVEREIGN-CONTAINER-v1.0
协议: 01_protocols/cnsh/PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PROTOCOL_DNA = "#龍芯⚡️2026-05-15-SOVEREIGN-CONTAINER-v1.0"
CONFIRM_REQUIRED = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_REQUIRED = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_REQUIRED = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

IMMUTABLE_LAWS: List[str] = [
    "LAW-SC-01-gates_immutable",       # FLOW_IN / FLOW_OUT 不可旁路
    "LAW-SC-02-audit_immutable",       # 三色/DNA/GPG 不可静默替换
    "LAW-SC-03-privacy_immutable",     # 默认私密·粒子外显
    "LAW-SC-04-append_only",           # 只叠不删
    "LAW-SC-05-trace_recover",         # 可验真·合法可恢复且留痕
]

# 排序倒挂信号（ORDER-ANCHOR 简版启发式）
_INVERSION_MARKERS = (
    "钱大于",
    "权大于民",
    "我先于人民",
    "国家让位于我",
)

_TIER_RHO = {"T0": 5.0, "T1": 4.0, "T2": 3.0, "T3": 2.0, "T4": 1.0}


def _utc_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_burn_semantics(event_type: str) -> str:
    """
    统一 burn 语义：链上只追加事件，不物理删除历史。
    event_type: absorb | seal | burn_readable | unseal_observed | fuse | flow_out
    """
    allowed = {
        "absorb",
        "seal",
        "burn_readable",
        "unseal_observed",
        "fuse",
        "flow_out",
        "hold",
    }
    if event_type not in allowed:
        raise ValueError(f"unknown ledger event_type: {event_type}")
    return event_type


def append_ledger_event(
    ledger_path: Path,
    event_type: str,
    *,
    operator_id: str,
    content_sha256: str,
    dna: str,
    tricolor: str,
    meta: Optional[Dict[str, Any]] = None,
    plaintext_stored: bool = False,
) -> Dict[str, Any]:
    """
    Append-only 主权账本行。禁止调用方删改本文件历史行。
    plaintext_stored=False 表示密文层未落本地明文（默认）。
    """
    event_type = normalize_burn_semantics(event_type)
    row: Dict[str, Any] = {
        "ts": _utc_now(),
        "event_type": event_type,
        "operator_id": operator_id,
        "content_sha256": content_sha256,
        "dna": dna,
        "tricolor": tricolor,
        "protocol_dna": PROTOCOL_DNA,
        "append_only": True,
        "plaintext_stored": plaintext_stored,
        "meta": meta or {},
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def make_particle_view(
    *,
    dna: str,
    content_sha256: str,
    tricolor: str,
    parent_dna: str = "",
    operator_id: str = "",
    operator_tier: str = "T3",
    gate_trace: Optional[List[str]] = None,
    ipa_summary: Optional[List[str]] = None,
    fuse_reason: str = "",
    sealed: bool = False,
    burn_readable: bool = False,
) -> Dict[str, Any]:
    """对外安全视图：仅粒子，不含正文。"""
    return {
        "layer": "particle",
        "protocol_dna": PROTOCOL_DNA,
        "dna": dna,
        "parent_dna": parent_dna,
        "sha256": content_sha256,
        "tricolor": tricolor,
        "operator_id": operator_id,
        "operator_tier": operator_tier,
        "audit_density_rho": _TIER_RHO.get(operator_tier, 2.0),
        "gate_trace": gate_trace or [],
        "ipa_summary": ipa_summary or [],
        "fuse_reason": fuse_reason,
        "readable_outside": not (sealed or burn_readable),
        "founder_same_rules": True,
    }


def order_anchor_scan(text: str) -> Dict[str, Any]:
    """
    排序不动点简版：人民→国家→个人；检测倒挂关键词。
    完整版见 ORDER-ANCHOR Notion 页；此处供 flow_port 前置。
    """
    inversion = any(m in text for m in _INVERSION_MARKERS)
    return {
        "sort_ok": not inversion,
        "inversion": inversion,
        "tier_bump": 1 if inversion else 0,
        "note": "人民→国家→个人; 忠>孝>义; 人>地>天",
    }


def bump_tier(tier: str) -> str:
    order = ["T4", "T3", "T2", "T1", "T0"]
    try:
        i = order.index(tier)
    except ValueError:
        return "T2"
    return order[min(i + 1, len(order) - 1)]
