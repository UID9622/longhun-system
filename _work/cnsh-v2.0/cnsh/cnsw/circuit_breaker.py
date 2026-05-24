# -*- coding: utf-8 -*-
"""
cnsw 熔断执行器 — L4/L5 建议会话halt + JSONL 审计（append-only）。
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

DEFAULT_AUDIT_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "cnsw_circuit_audit.jsonl"
)

_writer: Optional[Callable[[Dict[str, Any]], None]] = None


def set_audit_writer(fn: Optional[Callable[[Dict[str, Any]], None]]) -> None:
    global _writer
    _writer = fn


def _default_append(record: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def circuit_breaker(
    scan_result: Dict[str, Any],
    *,
    audit_path: Optional[Path] = None,
    write_audit: bool = True,
) -> str:
    level = scan_result.get("drift_level", "L0")
    ch = scan_result.get("content_hash", "")
    out_path = audit_path if audit_path is not None else DEFAULT_AUDIT_PATH
    if isinstance(out_path, str):
        out_path = Path(out_path)
    if level in ("L4", "L5"):
        msg = (
            f"🔴 SOVEREIGNTY_DRIFT_DETECTED. SESSION HALT SUGGESTED. "
            f"LEVEL={level} AUDIT_HASH={ch}"
        )
        if write_audit:
            rec = {
                "event": "circuit_break",
                "utc": datetime.now(timezone.utc).isoformat(),
                "drift_level": level,
                "sovereignty_score": scan_result.get("sovereignty_score"),
                "matched_hooks": scan_result.get("matched_hooks"),
                "matched_supplemental": scan_result.get("matched_supplemental"),
                "content_hash": ch,
                "huangli_time_hash": (scan_result.get("timestamp") or {}).get("_time_hash"),
            }
            if _writer is not None:
                _writer(rec)
            else:
                _default_append(rec, out_path)
        return msg
    if level == "L3":
        return f"🟠 WATCH: 主控稀释风险 {level} hash={ch}"
    if level == "L2":
        return f"🟡 OBSERVE: 价值判断露头 {level} hash={ch}"
    return "🟢 PASS"
