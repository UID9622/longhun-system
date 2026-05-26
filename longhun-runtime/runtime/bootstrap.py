from __future__ import annotations

from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from core.audit_engine.audit_logger import AuditLogger
from core.event_bus.event_bus import EventBus, RuntimeEvent
from core.memory_engine.memory_store import MemoryStore
from core.memory_engine.session_memory_bridge import SessionMemoryBridge
from runtime.task_router.runtime_router import RuntimeRouter


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    event_bus = EventBus()
    router = RuntimeRouter()
    memory = MemoryStore(root / "memory" / "sqlite" / "runtime_memory.db")
    audit = AuditLogger(root / "audit" / "jsonl" / "events.jsonl")

    startup_event = RuntimeEvent(
        event="runtime_boot",
        source="LOCAL_BRAIN_RUNTIME",
        payload={
            "dna": "#龍芯⚡️2026-05-27-CNSH-LOCAL-BRAIN-RUNTIME-v4.0",
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "state": "STABLE",
        },
        risk="low",
    )

    record = event_bus.publish(startup_event)
    routed = router.route(record)
    memory.store(routed)
    audit.append(routed)

    memory_bridge = SessionMemoryBridge(
        "~/.claude/projects/-Users-zuimeidedeyihan/memory/SESSION_MEMORY.md"
    )
    memory_snapshot = memory_bridge.load()
    if memory_snapshot:
        memory_event = RuntimeEvent(
            event="session_memory_sync",
            source="SESSION_MEMORY_BRIDGE",
            payload=memory_snapshot,
            risk="low",
        )
        memory_record = router.route(event_bus.publish(memory_event))
        memory.store(memory_record)
        audit.append(memory_record)

    print("[LOCAL-BRAIN] boot complete")
    print(f"[LOCAL-BRAIN] route={routed['route']} audit={root / 'audit' / 'jsonl' / 'events.jsonl'}")
    if memory_snapshot:
        print(
            f"[LOCAL-BRAIN] session_memory synced: completed_items={memory_snapshot['completed_items']}"
        )


if __name__ == "__main__":
    main()
