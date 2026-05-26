from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT NOT NULL,
                    event TEXT NOT NULL,
                    source TEXT NOT NULL,
                    risk TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )

    def store(self, record: dict[str, Any]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO memory_events (time, event, source, risk, payload_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    record.get("time", ""),
                    record.get("event", "unknown"),
                    record.get("source", "unknown"),
                    record.get("risk", "low"),
                    json.dumps(record.get("payload", {}), ensure_ascii=False),
                ),
            )
