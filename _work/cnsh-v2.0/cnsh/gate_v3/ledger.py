# -*- coding: utf-8 -*-
"""第一道闸门 · append-only 审计账本"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .engine import GateDecision

DEFAULT_LEDGER = Path.home() / "longhun" / "data" / "gate_v3_ledger.jsonl"


def append_gate_event(decision: GateDecision, *, ledger_path: Path | None = None) -> Dict[str, Any]:
    path = ledger_path or DEFAULT_LEDGER
    row = {
        "ts": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "digital_root": decision.digital_root,
        "gate_color": decision.gate_color_dr,
        "audit_color": decision.audit_color,
        "dna": decision.dna,
        "state": decision.state,
        "route": decision.route,
        "bucket": decision.bucket,
        "execute_allowed": decision.execute_allowed,
        "hold_for_audit": decision.hold_for_audit,
        "decision": decision.decision,
        "append_only": True,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def consecutive_red_count(*, ledger_path: Path | None = None, window: int = 20) -> int:
    path = ledger_path or DEFAULT_LEDGER
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    tail = lines[-window:] if len(lines) > window else lines
    count = 0
    for line in reversed(tail):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            break
        if row.get("audit_color") == "🔴":
            count += 1
        else:
            break
    return count
