from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class RuntimeEvent:
    event: str
    source: str
    payload: dict[str, Any]
    risk: str = "low"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["time"] = datetime.now(timezone.utc).isoformat()
        return data


class EventBus:
    """Simple in-process event bus; can be swapped to ZeroMQ later."""

    def publish(self, event: RuntimeEvent) -> dict[str, Any]:
        return event.to_dict()
