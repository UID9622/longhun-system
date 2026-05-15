# -*- coding: utf-8 -*-
"""
龍魂流场唯一进出口 flow_port()
DNA: #龍芯⚡️2026-05-15-FLOW-PORT-v1.0
宪法: PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md
融合: PROTOCOL__95-5-ROOT-RATIO-v2.0 · PROTOCOL__CNSH-PROTOCOL-LAYER-CIVILIZATION-v2.0
      · PROTOCOL__FIRST-GATE-v3.0（输入海关·默认熔断不执行）
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 民主门：复用 cnsh-core（与 DeepSeek Bridge 同源）
_ROOT = Path(__file__).resolve().parents[2]
_CORE = _ROOT / "cnsh-core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from cnsh.flow_decision import run_flow_decision
from cnsh.flow_decision.cnsh_flow_decision_core import CONFIRM_REQUIRED, GPG_REQUIRED
from cnsh.root_ratio import (
    ROOT_RATIO_DNA,
    apply_95_5_guard,
    handle_cnsh_command,
)
from cnsh.gate_v3 import (
    GATE_DNA,
    append_gate_event,
    consecutive_red_count,
    decide as gate_decide,
    notify_gate,
)
from cnsh.gate_v3.engine import GateDecision
from cnsh.sovereign.container_policy import (
    IMMUTABLE_LAWS,
    PROTOCOL_DNA,
    append_ledger_event,
    bump_tier,
    make_particle_view,
    order_anchor_scan,
    sha256_hex,
)

try:
    from deepseek_bridge import 民主回复计算函数
except ImportError:

    def 民主回复计算函数(ai_reply_text, context=None, special_flags=None):  # type: ignore
        return {"是否通过": True, "总得分": 1.0, "是否熔断": False, "各维度得分": {}, "不通过的具体原因": [], "修正建议": []}


FLOW_PORT_DNA = "#龍芯⚡️2026-05-15-FLOW-PORT-v1.0"
CIVILIZATION_DNA = "#龍芯⚡️2026-05-14-CNSH-PROTOCOL-LAYER-CIVILIZATION-MASTERPIECE-v2.0"
DEFAULT_LEDGER = Path.home() / "longhun" / "data" / "sovereign_ledger.jsonl"


def _ipa_summary(receipts: List[Dict[str, Any]]) -> List[str]:
    return [f"{r.get('ipa_node', '?')}:{r.get('output_signal', '?')}" for r in receipts]


def flow_port(flow_in: Dict[str, Any], *, ledger_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    唯一进出口。吸收先进容器事件，再走流场决策核，出口带粒子层。

    flow_in 常用键:
      message, channel, operator_id, operator_tier (T0–T4),
      tags (dict: title, parent_dna, privacy_mode, action, confirm_code, gpg, ...),
      draft_reply (可选·已有 AI 草稿则跳过生成，仍过民主门)
    """
    ledger = ledger_path or DEFAULT_LEDGER
    message = str(flow_in.get("message") or "").strip()
    operator_id = str(flow_in.get("operator_id") or "anonymous")
    tier = str(flow_in.get("operator_tier") or "T3")
    tags = dict(flow_in.get("tags") or {})
    channel = str(flow_in.get("channel") or "api")

    if not message and not flow_in.get("draft_reply"):
        return _flow_out_error("message 不能为空", tier, operator_id)

    cmd = handle_cnsh_command(message)
    if cmd is not None:
        return {
            "reply": str(cmd),
            "tricolor": "🟢",
            "status": "enter",
            "dna": ROOT_RATIO_DNA,
            "particle": make_particle_view(
                dna=ROOT_RATIO_DNA,
                content_sha256=sha256_hex(message),
                tricolor="🟢",
                operator_id=operator_id,
                operator_tier=tier,
            ),
            "protocol_dna": PROTOCOL_DNA,
            "root_ratio": cmd,
            "civilization_dna": CIVILIZATION_DNA,
            "founder_same_rules": True,
        }

    content_for_hash = message or str(flow_in.get("draft_reply") or "")
    inspiration_mode = bool(tags.get("inspiration_mode") or tags.get("open_chaos_5"))
    content_sha = sha256_hex(content_for_hash)
    auto_execute = bool(
        flow_in.get("auto_execute")
        or tags.get("auto_execute")
        or tags.get("force_execute")
    )

    # L-1 第一道闸门 v3.0（默认熔断不执行·不确定则挂起·可弹窗）
    gate_meta = {
        "dna": tags.get("dna_current") or tags.get("dna"),
        "operator": operator_id,
        "source": channel,
        "timestamp": flow_in.get("timestamp"),
    }
    gate = gate_decide(
        message or content_for_hash,
        metadata=gate_meta,
        evidence=str(flow_in.get("evidence") or ""),
        auto_execute=auto_execute,
    )
    append_gate_event(gate)
    if gate.notify_level == "active":
        notify_gate(gate)
    red_streak = consecutive_red_count()
    if red_streak >= 2:
        gate = gate_decide(
            message,
            metadata={**gate_meta, "p0_block": True},
            auto_execute=False,
        )
        gate.execute_allowed = False
        gate.hold_for_audit = True
        gate.decision = f"连续熔断{red_streak}次·P0阻断·已通知老大"
        gate.audit_color = "🔴"

    if not gate.execute_allowed:
        append_ledger_event(
            ledger,
            "fuse" if gate.audit_color == "🔴" else "hold",
            operator_id=operator_id,
            content_sha256=content_sha,
            dna=gate.dna,
            tricolor=gate.audit_color,
            meta={"gate": gate.meta, "gate_decision": gate.decision, "red_streak": red_streak},
        )
        tricolor = gate.audit_color
        status = "fuse" if tricolor == "🔴" else "hold"
        return {
            "reply": gate.decision,
            "tricolor": tricolor,
            "status": status,
            "dna": gate.dna,
            "particle": make_particle_view(
                dna=gate.dna,
                content_sha256=content_sha,
                tricolor=tricolor,
                operator_id=operator_id,
                operator_tier=tier,
                fuse_reason=gate.decision,
            ),
            "protocol_dna": PROTOCOL_DNA,
            "gate_v3": _gate_out_dict(gate, red_streak),
            "gate_dna": GATE_DNA,
            "execute_allowed": False,
            "hold_for_audit": True,
            "founder_same_rules": True,
        }

    # L0 排序不动点
    order = order_anchor_scan(message)
    if order.get("inversion"):
        tier = bump_tier(tier)
        tags["order_inversion"] = True

    # 吸收 · append-only
    absorb_dna = tags.get("dna_current") or FLOW_PORT_DNA
    append_ledger_event(
        ledger,
        "absorb",
        operator_id=operator_id,
        content_sha256=content_sha,
        dna=absorb_dna,
        tricolor="🟢",
        meta={"channel": channel, "tier": tier, "order": order},
        plaintext_stored=False,
    )

    tags.setdefault("confirm_code", CONFIRM_REQUIRED)
    tags.setdefault("gpg", GPG_REQUIRED)
    tags.setdefault("operator", operator_id)
    tags.setdefault("title", tags.get("title") or "flow_port")

    # L2 流场决策核
    r = run_flow_decision(message or content_for_hash, tags=tags)

    if r.fused:
        append_ledger_event(
            ledger,
            "fuse",
            operator_id=operator_id,
            content_sha256=content_sha,
            dna=absorb_dna,
            tricolor="🔴",
            meta={"reason": r.node.fuse_reason, "laws": r.laws_triggered},
        )
        particle = make_particle_view(
            dna=absorb_dna,
            content_sha256=content_sha,
            tricolor="🔴",
            parent_dna=r.node.parent_dna or "",
            operator_id=operator_id,
            operator_tier=tier,
            gate_trace=list(r.node.gate_trace),
            ipa_summary=_ipa_summary(r.ipa_receipts),
            fuse_reason=r.node.fuse_reason or ";".join(r.laws_triggered),
        )
        return {
            "reply": f"🔴 流场熔断：{r.node.fuse_reason or '见 fuse_reason'}",
            "tricolor": "🔴",
            "status": "fuse",
            "dna": absorb_dna,
            "particle": particle,
            "protocol_dna": PROTOCOL_DNA,
            "flow_port_dna": FLOW_PORT_DNA,
            "order_anchor": order,
            "operator_tier_applied": tier,
            "founder_same_rules": True,
        }

    # 草稿 / 执行结果
    draft = str(flow_in.get("draft_reply") or message)
    dem = 民主回复计算函数(draft, context=flow_in.get("history"))
    if dem.get("是否熔断"):
        append_ledger_event(
            ledger,
            "fuse",
            operator_id=operator_id,
            content_sha256=sha256_hex(draft),
            dna=absorb_dna,
            tricolor="🔴",
            meta={"democratic": dem},
        )
        return {
            "reply": "🔴 民主门主权保护熔断·回复已拦截",
            "tricolor": "🔴",
            "status": "fuse",
            "dna": absorb_dna,
            "particle": make_particle_view(
                dna=absorb_dna,
                content_sha256=sha256_hex(draft),
                tricolor="🔴",
                operator_id=operator_id,
                operator_tier=tier,
                fuse_reason="sovereignty_democratic_fuse",
            ),
            "protocol_dna": PROTOCOL_DNA,
            "democratic": dem,
            "founder_same_rules": True,
        }

    tricolor = r.node.audit_tricolor or "🟢"
    status = r.node.result_status or "enter"
    if not dem.get("是否通过", True):
        tricolor = "🟡"
        status = "hold"

    ratio_guard = apply_95_5_guard(
        draft,
        inspiration_mode=inspiration_mode,
        operator_id=operator_id,
    )
    if ratio_guard.get("fused"):
        append_ledger_event(
            ledger,
            "fuse",
            operator_id=operator_id,
            content_sha256=sha256_hex(draft),
            dna=ROOT_RATIO_DNA,
            tricolor=ratio_guard.get("tricolor", "🔴"),
            meta={"root_ratio": ratio_guard},
        )
        hint = ratio_guard.get("reply_hint", "95/5 限幅熔断")
        return {
            "reply": hint,
            "tricolor": ratio_guard.get("tricolor", "🔴"),
            "status": "fuse" if ratio_guard.get("tricolor") == "🔴" else "hold",
            "dna": ROOT_RATIO_DNA,
            "particle": make_particle_view(
                dna=ROOT_RATIO_DNA,
                content_sha256=sha256_hex(draft),
                tricolor=ratio_guard.get("tricolor", "🔴"),
                operator_id=operator_id,
                operator_tier=tier,
                fuse_reason=hint,
            ),
            "protocol_dna": PROTOCOL_DNA,
            "root_ratio": ratio_guard,
            "civilization_dna": CIVILIZATION_DNA,
            "founder_same_rules": True,
        }

    out_dna = r.node.dna_child or r.node.dna_current or absorb_dna
    sealed = r.node.privacy_mode == "sealed" or status == "hold"
    burn_readable = r.node.privacy_mode == "burn"

    if sealed:
        append_ledger_event(
            ledger,
            "seal",
            operator_id=operator_id,
            content_sha256=content_sha,
            dna=out_dna,
            tricolor=tricolor,
            meta={"seal_proof": r.node.storage_seal_proof},
        )
    if burn_readable:
        append_ledger_event(
            ledger,
            "burn_readable",
            operator_id=operator_id,
            content_sha256=content_sha,
            dna=out_dna,
            tricolor=tricolor,
            meta={"destroy_proof": r.node.storage_destroy_proof},
        )

    append_ledger_event(
        ledger,
        "flow_out",
        operator_id=operator_id,
        content_sha256=sha256_hex(draft),
        dna=out_dna,
        tricolor=tricolor,
        meta={
            "status": status,
            "democratic_score": dem.get("总得分"),
            "root_ratio_p": ratio_guard.get("personality_p"),
        },
    )

    particle = make_particle_view(
        dna=out_dna,
        content_sha256=content_sha,
        tricolor=tricolor,
        parent_dna=r.node.parent_dna or "",
        operator_id=operator_id,
        operator_tier=tier,
        gate_trace=list(r.node.gate_trace),
        ipa_summary=_ipa_summary(r.ipa_receipts),
        sealed=sealed,
        burn_readable=burn_readable,
    )

    return {
        "reply": draft if dem.get("是否通过", True) else f"🟡 待修正输出（民主门）\n{draft[:500]}",
        "tricolor": tricolor,
        "status": status,
        "dna": out_dna,
        "child_dna": r.node.dna_child,
        "particle": particle,
        "protocol_dna": PROTOCOL_DNA,
        "flow_port_dna": FLOW_PORT_DNA,
        "order_anchor": order,
        "operator_tier_applied": tier,
        "ipa_receipts": r.ipa_receipts,
        "gate_trace": r.node.gate_trace,
        "democratic": dem,
        "immutable_laws": list(IMMUTABLE_LAWS),
        "root_ratio": ratio_guard,
        "root_ratio_dna": ROOT_RATIO_DNA,
        "civilization_dna": CIVILIZATION_DNA,
        "gate_dna": GATE_DNA,
        "gate_v3": _gate_out_dict(gate, red_streak),
        "execute_allowed": True,
        "hold_for_audit": False,
        "founder_same_rules": True,
    }


def _gate_out_dict(gate: "GateDecision", red_streak: int) -> Dict[str, Any]:
    return {
        "digital_root": gate.digital_root,
        "gate_color": gate.gate_color_dr,
        "audit_color": gate.audit_color,
        "state": gate.state,
        "route": gate.route,
        "bucket": gate.bucket,
        "decision": gate.decision,
        "execute_allowed": gate.execute_allowed,
        "hold_for_audit": gate.hold_for_audit,
        "red_streak": red_streak,
        "meta": gate.meta,
    }


def _flow_out_error(msg: str, tier: str, operator_id: str) -> Dict[str, Any]:
    return {
        "reply": msg,
        "tricolor": "🔴",
        "status": "fuse",
        "dna": FLOW_PORT_DNA,
        "particle": make_particle_view(
            dna=FLOW_PORT_DNA,
            content_sha256=sha256_hex(msg),
            tricolor="🔴",
            operator_id=operator_id,
            operator_tier=tier,
            fuse_reason=msg,
        ),
        "protocol_dna": PROTOCOL_DNA,
        "founder_same_rules": True,
    }
