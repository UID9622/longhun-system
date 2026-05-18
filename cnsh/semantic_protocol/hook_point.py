# -*- coding: utf-8 -*-
"""
语义协议 · Hook 点 Phase 1
DNA: #龍芯⚡2026-05-18-SEMANTIC-PROTOCOL-HOOK-v1.0

与 cnsh/cnsw/registry.SOVEREIGNTY_HOOKS 不同：
  - registry = 国产 AI 围猎话术检测
  - 本模块 = 老大梦境「意识流 Hook 点」插桩留痕

真源协议: 01_protocols/cnsh/PROTOCOL__SEMANTIC-PROTOCOL-MODEL-v1.0.local.md
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TRACE_PATH = _REPO_ROOT / "logs" / "semantic_hook_trace.jsonl"
_PROTOCOL_DNA = "#龍芯⚡2026-05-18-SEMANTIC-PROTOCOL-HOOK-v1.0"


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def digital_root(text: str) -> int:
    """369 数字根占位（与三色 gate 对齐用）。"""
    total = sum(ord(c) for c in text)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total if total else 9


def capture_at_moment(extra: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    """L1 物理输入占位：时间戳 + 环境 + 可选传感器字段。"""
    sig: Dict[str, Any] = {
        "ts": _now_iso(),
        "host": os.uname().nodename if hasattr(os, "uname") else "local",
        "pid": os.getpid(),
        "layer": "L1",
    }
    if extra:
        sig.update(dict(extra))
    return sig


def interpret(sig: Mapping[str, Any], thought_signal: str) -> Dict[str, Any]:
    """L5 语义解释占位：dr + 简短摘要（Phase 2 接 gate_v3 / CNSH-64 D(s,e)）。"""
    dr = digital_root(thought_signal)
    audit = "🔴" if dr in (3, 9) else ("🟡" if dr == 6 else "🟢")
    return {
        "layer": "L5",
        "thought_preview": thought_signal[:240],
        "dr": dr,
        "audit": audit,
        "policy": "fuse" if dr in (3, 9) else "pass",
        "captured_ts": sig.get("ts"),
    }


def compress_record(sem: Mapping[str, Any]) -> Dict[str, Any]:
    """L2 水生记忆占位：短 hash + 协议 DNA。"""
    blob = json.dumps(sem, ensure_ascii=False, sort_keys=True)
    short = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
    return {
        "layer": "L2",
        "dna": _PROTOCOL_DNA,
        "parti_id": f"hook-{short}",
        "sem": dict(sem),
        "compressed_at": _now_iso(),
    }


def persist(parti: Mapping[str, Any], path: Path | None = None) -> Path:
    """append-only 留痕。"""
    target = path or _TRACE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(parti, ensure_ascii=False) + "\n")
    return target


def hook(
    thought_signal: str,
    *,
    operator_id: str = "UID9622",
    sensor_extra: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    意识流 Hook 点 · Phase 1 可执行 spec。

    thought_signal: 当前意识流片段（文本/键入/口述转写）
  operator_id: 主权主体，默认 UID9622
    """
    if not thought_signal or not str(thought_signal).strip():
        raise ValueError("thought_signal 不能为空")

    sig = capture_at_moment(sensor_extra)
    sig["operator_id"] = operator_id
    sem = interpret(sig, str(thought_signal).strip())
    parti = compress_record(sem)
    parti["hook"] = {
        "phase": "P1",
        "operator_id": operator_id,
        "sig": sig,
    }
    persist(parti)
    return parti


def cli_main(argv: list[str] | None = None) -> int:
    import sys

    args = argv if argv is not None else sys.argv[1:]
    text = " ".join(args).strip()
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    if not text:
        print("用法: python -m cnsh.semantic_protocol.hook_point \"意识流片段\"", file=sys.stderr)
        return 2
    out = hook(text)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
