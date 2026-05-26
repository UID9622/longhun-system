from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class SessionMemoryBridge:
    def __init__(self, session_memory_path: str) -> None:
        self.session_memory_path = Path(session_memory_path).expanduser()

    def load(self) -> dict[str, Any] | None:
        if not self.session_memory_path.exists():
            return None

        text = self.session_memory_path.read_text(encoding="utf-8")

        dna = self._extract(text, r"\*\*DNA\*\*:\s*`([^`]+)`")
        gpg = self._extract(text, r"\*\*GPG\*\*:\s*([^\n]+)")
        updated_time = self._extract(text, r"\*\*時間\*\*:\s*([^\n]+)")
        status = self._extract(text, r"\*\*狀態\*\*:\s*([^\n]+)")
        completed_count = len(re.findall(r"^-\s*✅", text, flags=re.MULTILINE))

        return {
            "memory_type": "cross_window_session",
            "session_dna": dna,
            "session_gpg": gpg,
            "last_update": updated_time,
            "status": status,
            "completed_items": completed_count,
            "source_file": str(self.session_memory_path),
        }

    @staticmethod
    def _extract(text: str, pattern: str) -> str | None:
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None
