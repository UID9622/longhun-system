#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三色审计公共模块。
DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-CORE-AUDIT-v1.0
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class AuditMark:
    RED = "🔴"
    YELLOW = "🟡"
    GREEN = "🟢"
    BLUE = "🔵"
    PURPLE = "🟣"

    @classmethod
    def tag(cls, mark: str, persona: str, message: str) -> str:
        return f"{mark} [{persona}] {message}"


class TricolorAudit:
    """审计日志归档：绿色/黄色/红色。"""

    def __init__(self, audit_dir: Path):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def _record(self, level: str, persona: str, event: str, details: Dict[str, Any]) -> str:
        ts = datetime.now(timezone.utc).isoformat()
        entry = {
            "timestamp": ts,
            "level": level,
            "persona": persona,
            "event": event,
            "details": details,
        }
        date = ts[:10]
        log_file = self.audit_dir / f"audit_{date}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return ts

    def green(self, persona: str, event: str, details: Dict[str, Any] = None) -> str:
        return self._record("green", persona, event, details or {})

    def yellow(self, persona: str, event: str, details: Dict[str, Any] = None) -> str:
        return self._record("yellow", persona, event, details or {})

    def red(self, persona: str, event: str, details: Dict[str, Any] = None) -> str:
        return self._record("red", persona, event, details or {})

    def dashboard(self) -> Dict[str, Any]:
        counts = {"green": 0, "yellow": 0, "red": 0}
        latest = []
        if self.audit_dir.exists():
            for f in sorted(self.audit_dir.glob("audit_*.jsonl")):
                with open(f, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                            counts[rec.get("level", "green")] = counts.get(rec.get("level", "green"), 0) + 1
                            latest.append(rec)
                        except Exception:
                            continue
        latest.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return {
            "counts": counts,
            "latest": latest[:50],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
