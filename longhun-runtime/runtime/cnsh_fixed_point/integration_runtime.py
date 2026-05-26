from __future__ import annotations

from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from core.audit_engine.audit_logger import AuditLogger
from core.event_bus.event_bus import EventBus, RuntimeEvent
from core.memory_engine.memory_store import MemoryStore
from runtime.cnsh_fixed_point.cnsh_core_engine import process_cnsh
from runtime.cnsh_fixed_point.tongxinyi_core import tongxinyi, to_dict


def run_pipeline(user_input: str) -> dict:
    tx = tongxinyi(user_input)
    cnsh = process_cnsh(tx.cleaned_text)
    return {
        "tongxinyi": to_dict(tx),
        "cnsh": cnsh,
    }


def main() -> None:
    input_text = "宝宝，帮我把这个Notion自动跑起来，带DNA追溯，先审计再执行"
    payload = run_pipeline(input_text)

    event_bus = EventBus()
    audit = AuditLogger(root / "audit" / "jsonl" / "events.jsonl")
    memory = MemoryStore(root / "memory" / "sqlite" / "runtime_memory.db")

    event = RuntimeEvent(
        event="cnsh_fixed_point_pipeline",
        source="CNSH_FIXED_POINT",
        payload=payload,
        risk="high" if payload["cnsh"]["audit_color"] in {"🔴", "🟠"} else "low",
    )
    record = event_bus.publish(event)
    memory.store(record)
    audit.append(record)

    print("[CNSH-FIXED-POINT] pipeline emitted")
    print(f"[CNSH-FIXED-POINT] state={payload['cnsh']['state']} audit={payload['cnsh']['audit_color']}")


if __name__ == "__main__":
    main()
