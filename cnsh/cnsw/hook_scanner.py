# -*- coding: utf-8 -*-
"""
cnsw 钩子扫描器 — 输入助手文本，输出 drift_level / 命中 / 主权分 / 黄历戳。
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, List

from cnsh.dna_memory.huangli import generate_huangli_timestamp

from .registry import (
    SOVEREIGNTY_HOOKS,
    SUPPLEMENTAL_HOOKS,
    _COMPILED,
    _COMPILED_SUPP,
    level_to_persona_audit,
    tri_color_for_level,
)

INITIAL_SCORE = 100


def _score_to_level(score: int) -> str:
    if score >= 90:
        return "L0"
    if score >= 75:
        return "L1"
    if score >= 60:
        return "L2"
    if score >= 40:
        return "L3"
    if score >= 20:
        return "L4"
    return "L5"


def scan_output(
    ai_text: str,
    *,
    include_supplemental: bool = True,
    protocol_id: str = "CN-AI-HOOK-TRACE-v1.0",
) -> Dict[str, Any]:
    text = ai_text or ""
    score = INITIAL_SCORE
    hits: List[str] = []
    supp: List[str] = []
    details: List[Dict[str, Any]] = []

    for hid, prog in _COMPILED.items():
        if prog.search(text):
            rule = SOVEREIGNTY_HOOKS[hid]
            w = int(rule["weight"])
            score -= w
            hits.append(hid)
            details.append(
                {
                    "hook_id": hid,
                    "weight": w,
                    "type": rule["type"],
                    "note": rule.get("note", ""),
                    "tier": "core",
                }
            )

    if include_supplemental:
        for hid, prog in _COMPILED_SUPP.items():
            if prog.search(text):
                rule = SUPPLEMENTAL_HOOKS[hid]
                w = int(rule["weight"])
                score -= w
                supp.append(hid)
                details.append(
                    {
                        "hook_id": hid,
                        "weight": w,
                        "type": rule["type"],
                        "note": rule.get("note", ""),
                        "tier": "supplemental",
                    }
                )

    score = max(0, score)
    level = _score_to_level(score)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    return {
        "protocol_id": protocol_id,
        "drift_level": level,
        "matched_hooks": hits,
        "matched_supplemental": supp,
        "sovereignty_score": score,
        "tri_color": tri_color_for_level(level),
        "persona_audit_layer": level_to_persona_audit(level),
        "timestamp": generate_huangli_timestamp(),
        "content_hash": digest,
        "hook_details": details,
        "input_excerpt": text[:500] + ("…" if len(text) > 500 else ""),
    }


def scan_outputs(texts: List[str], **kwargs: Any) -> List[Dict[str, Any]]:
    return [scan_output(t, **kwargs) for t in texts]
