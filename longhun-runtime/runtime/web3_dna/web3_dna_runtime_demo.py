from __future__ import annotations

from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from core.audit_engine.audit_logger import AuditLogger
from core.event_bus.event_bus import EventBus, RuntimeEvent
from core.memory_engine.memory_store import MemoryStore
from runtime.web3_dna.web3_dna_engine import (
    Web3DNAPolicy,
    longhun_wuxing_calculator_v2,
    run_64gua_audit,
    run_fifth_dimension,
)


def main() -> None:
    event_bus = EventBus()
    audit = AuditLogger(root / "audit" / "jsonl" / "events.jsonl")
    memory = MemoryStore(root / "memory" / "sqlite" / "runtime_memory.db")
    policy = Web3DNAPolicy()

    calc = longhun_wuxing_calculator_v2("甲", "子", "丙", "午", "庚", "申", "壬", "戌")
    fifth = run_fifth_dimension("UID9622-20260527", calc["四柱"])
    gua = run_64gua_audit(
        {
            "innovation": 78,
            "support": 82,
            "response": 75,
            "optimization": 73,
            "risk": 88,
            "expression": 80,
            "defense": 90,
            "collaboration": 72,
        },
        confidence=0.83,
        violate_values=False,
    )

    payload = {
        "policy": {"dna": policy.dna, "confirm": policy.confirm, "gpg": policy.gpg},
        "wuxing": calc,
        "fifth_dimension": fifth,
        "gua_audit": gua,
        "payment_currency": "e-CNY",
    }

    event = RuntimeEvent(
        event="web3_dna_trade_precheck",
        source="WEB3_DNA_ENGINE_V8",
        payload=payload,
        risk="low" if gua["颜色"] != "🔴" else "high",
    )

    record = event_bus.publish(event)
    memory.store(record)
    audit.append(record)

    print("[WEB3-DNA] precheck event emitted")
    print(f"[WEB3-DNA] gua_color={gua['颜色']} action={gua['动作']}")


if __name__ == "__main__":
    main()
