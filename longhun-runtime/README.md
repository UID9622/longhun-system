# CNSH Local Brain Runtime v4.0

## Runtime Goal
Build one sovereign local runtime spine:
- unified event flow
- unified memory flow
- unified authority flow
- unified semantic routing
- unified audit chain

## Current MVP (Phase 1)
1. Event bus (`core/event-bus/event_bus.py`)
2. JSONL audit (`core/audit-engine/audit_logger.py`)
3. Ollama router placeholder (`runtime/task-router/runtime_router.py`)
4. SQLite memory store (`core/memory-engine/memory_store.py`)
5. Session memory bridge (`core/memory_engine/session_memory_bridge.py`)

## Boot
```bash
python3 longhun-system/longhun-runtime/runtime/bootstrap.py
python3 longhun-system/longhun-runtime/runtime/web3_dna/web3_dna_runtime_demo.py
python3 longhun-system/longhun-runtime/runtime/cnsh_fixed_point/integration_runtime.py
```

## Directory Contract
- `core/`: runtime internal engines
- `memory/`: sqlite, vectors, dna, snapshots
- `audit/jsonl/`: append-only audit chain
- `runtime/`: routers and workflow runtime
- `ui/`: shell + protocol-driven render layers
- `ios-bridge/`: iPhone trigger and bridge
- `agents/`: role-based runtime functions
- `cnsh/`: language protocol/grammar/render rules

## Non-movable Sovereign Protocol
- `SOVEREIGN_GOLD`
- `DNA_PURPLE`
- `AUDIT_BLUE`
- `RISK_RED`
- `DNA_CHAIN`
- `CONFIRM_CHAIN`
- `AUDIT_CHAIN`
- `REPLAY_SYSTEM`
