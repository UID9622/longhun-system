#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 登记门禁 · 没 DNA 不执行生态逻辑
DNA: #龍芯⚡2026-05-19-DNA-GATE-v1.0

规则（小白版）:
  任何任务/脚本/对外动作 · context 里必须有 dna 字段
  格式: #龍芯⚡ 开头 · 否则逻辑拒绝执行（不是静默跳过）
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# 接受 #龍芯⚡ 或 #龍芯⚡️（部分文档用 variation selector）
DNA_PATTERN = re.compile(r"^#龍芯⚡\uFE0F?[\w\-:.]+", re.UNICODE)

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_LOG = REPO_ROOT / "日志" / "dna_registry.jsonl"


@dataclass
class DnaGateResult:
    ok: bool
    dna: str
    reason: str = ""

    def to_dict(self) -> dict:
        return {"ok": self.ok, "dna": self.dna, "reason": self.reason}


def is_valid_dna(dna: Optional[str]) -> bool:
    if not dna or not isinstance(dna, str):
        return False
    s = dna.strip()
    return bool(DNA_PATTERN.match(s))


def require_dna(
    context: Optional[Dict[str, Any]] = None,
    *,
    dna: Optional[str] = None,
    register: bool = True,
    actor: str = "unknown",
    enforce_color: bool = True,
) -> DnaGateResult:
    """
    检查 DNA · 可选写入登记册（本机 jsonl · 不上传）
    context 优先取 context['dna'] · 其次参数 dna
    """
    ctx = context or {}
    code = dna or ctx.get("dna") or ctx.get("DNA") or ctx.get("dna_trace")

    if not is_valid_dna(code):
        return DnaGateResult(
            ok=False,
            dna=str(code or ""),
            reason="未登记DNA或格式不对·须 #龍芯⚡ 开头·逻辑不执行",
        )

    code = code.strip()

    if enforce_color:
        try:
            from dna_color_codec import enforce_color_barrier, parse_color_dna

            ok_c, reason_c, route = enforce_color_barrier(code, ctx)
            if not ok_c:
                return DnaGateResult(ok=False, dna=code, reason=reason_c)
            ctx["dna_route"] = {
                "glance": route.glance_card(),
                "color": route.color,
                "flow": route.flow,
                "touch": route.touch,
                "palace": route.palace,
            }
        except ImportError:
            pass

    if register:
        meta = {"source": ctx.get("source", "gate")}
        if ctx.get("dna_route"):
            meta["dna_route"] = ctx["dna_route"]
        _append_registry(code, actor=actor, meta=meta)

    glance = (ctx.get("dna_route") or {}).get("glance", "")
    return DnaGateResult(
        ok=True,
        dna=code,
        reason=f"DNA已登记·允许进入生态逻辑" + (f" · {glance}" if glance else ""),
    )


def _append_registry(dna: str, actor: str, meta: Optional[dict] = None) -> None:
    REGISTRY_LOG.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": time.time(),
        "dna": dna,
        "actor": actor,
        "meta": meta or {},
    }
    with REGISTRY_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _selftest() -> None:
    assert is_valid_dna("#龍芯⚡2026-05-19-TEST-v1.0")
    assert not is_valid_dna("龙魂测试")
    assert not is_valid_dna(None)
    r = require_dna({"dna": "#龍芯⚡2026-05-19-GATE-SELFTEST-v1.0"}, register=False)
    assert r.ok
    r2 = require_dna({})
    assert not r2.ok
    print("dna_gate selftest OK")


if __name__ == "__main__":
    _selftest()
