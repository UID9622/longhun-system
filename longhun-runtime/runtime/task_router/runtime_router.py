from __future__ import annotations

from typing import Any


class RuntimeRouter:
    """MVP semantic router; replace classify() with Ollama route later."""

    def classify(self, record: dict[str, Any]) -> str:
        text = str(record.get("payload", {})).lower()
        if "password" in text or "key" in text:
            return "security"
        if "code" in text or "error" in text:
            return "developer"
        if "design" in text or "ui" in text:
            return "designer"
        return "general"

    def route(self, record: dict[str, Any]) -> dict[str, Any]:
        routed = dict(record)
        routed["route"] = self.classify(record)
        return routed
