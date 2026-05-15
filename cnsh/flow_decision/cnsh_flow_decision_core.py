# -*- coding: utf-8 -*-
"""
CNSH 流场决策总核 v4.1 — 主入口
DNA: #龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1-人格协作×IPA×DNA重铸增量
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .schemas import EXPECTED_FIELD_COUNT, FlowDecisionNode
from .digital_root import compute_four_source_dr
from .dna_tag_policy import burn_proof, parse_dna_tail_tags, seal_proof, validate_parent_chain
from .wuxing_router import element_for_dr
from .sancai_weight import normalize_sancai
from .shengke_relation import relation_to_parent
from .palace_router import route_palaces
from .sandbox_bucket import contribution_heat, pick_bucket
from .audit_gate import audit_color, map_result_status
from .ipa_route_registry import IPA_CHAIN, make_receipt, stable_flow_id
from .dna_chain_tracer import derive_child_dna
from .persona_collaboration import assert_one_primary_per_gate, jiang_ziya_exclusive_palace, qiao_exclusive_write

CONFIRM_REQUIRED = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_REQUIRED = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_REQUIRED = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

_SENS = re.compile(
    r"(?i)(token|private_key|secret_key|\bsecret\b|\.env\b|api[_-]?key)",
)


@dataclass
class FlowRunResult:
    node: FlowDecisionNode
    ipa_receipts: List[Dict[str, Any]] = field(default_factory=list)
    fused: bool = False
    laws_triggered: List[str] = field(default_factory=list)


def _fp(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parent_element(parent_dna: str) -> str:
    dr, _src = compute_four_source_dr(parent_dna, parent_dna)
    return element_for_dr(dr if dr else 5)


def run_flow_decision(raw_input: str, tags: Optional[Dict[str, Any]] = None, known_parent_roots: Optional[set] = None) -> FlowRunResult:
    """
    tags 常用键: title, parent_dna, confirm_code, gpg, eternal_seal, eternal_seal_expected,
    privacy_mode (normal|sealed|burn), visibility, trace_mode, operator, level, auto_execute, action, explicit_dr, dna_string
    """
    assert assert_one_primary_per_gate() and jiang_ziya_exclusive_palace() and qiao_exclusive_write()
    tags = tags or {}
    laws: List[str] = []
    receipts: List[Dict[str, Any]] = []
    fused = False
    flow_id = stable_flow_id(raw_input[:200] + str(tags.get("title", "")))

    n = FlowDecisionNode()
    n.title = str(tags.get("title") or "untitled")[:500]
    n.parent_dna = str(tags.get("parent_dna") or "")
    n.confirm_code = str(tags.get("confirm_code") or "")
    n.gpg = str(tags.get("gpg") or GPG_REQUIRED)
    n.eternal_seal = str(tags.get("eternal_seal") or SEAL_REQUIRED)
    n.result_operator = str(tags.get("operator") or "local_engine")
    n.privacy_visibility = str(tags.get("visibility") or "internal")
    n.privacy_trace_mode = str(tags.get("trace_mode") or "chain")
    n.privacy_mode = str(tags.get("privacy_mode") or "normal").lower()
    n.level = str(tags.get("level") or "L3日常")
    n.auto_execute = bool(tags.get("auto_execute", False))
    action = str(tags.get("action") or "")

    dna_blob = str(tags.get("dna_string") or tags.get("dna_current") or "")
    tagv = parse_dna_tail_tags(dna_blob)
    if tagv.visibility != "internal":
        n.privacy_visibility = tagv.visibility
    if tagv.trace_mode != "chain":
        n.privacy_trace_mode = tagv.trace_mode
    n.p0_touched = tagv.p0_touched
    n.level = tagv.level or n.level

    base_dna = str(tags.get("dna_current") or dna_blob or "#龍芯⚡️2026-05-03-FLOW-RUN-v4.1")

    def emit(ipa_idx: int, signal: str, dna_line: str) -> None:
        node_def = IPA_CHAIN[ipa_idx]
        receipts.append(
            make_receipt(
                node_def.ipa_id,
                node_def.path,
                node_def.main_persona,
                flow_id,
                signal,
                node_def.next_ipa,
                dna_line,
            )
        )

    # --- IPA 0 入口 ---
    emit(0, "pass", base_dna)
    n.gate_trace.append("core:enter")

    # ① 签章闸
    if n.confirm_code.strip() != CONFIRM_REQUIRED:
        laws.append("LAW-01-confirm_missing")
        fused = True
        emit(1, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "confirm_code 缺失或错误")
    if tags.get("eternal_seal_expected") and str(tags.get("eternal_seal_expected")) != n.eternal_seal:
        laws.append("LAW-02-seal_tamper")
        fused = True
        emit(1, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "eternal_seal 不匹配")
    emit(1, "pass", base_dna)
    n.persona_main_trace.append("P05@签章")
    n.gate_trace.append("sign:ok")
    if n.gpg.strip() != GPG_REQUIRED:
        laws.append("LAW-gpg-mismatch")
        emit(1, "fuse", base_dna)
        return _finalize_fuse(n, receipts, True, laws, "GPG 指纹不匹配")

    # ② 隐私闸
    if n.privacy_mode == "sealed":
        laws.append("LAW-03-sealed")
        n.raw_body_allowed = False
        n.content_fingerprint_sha256 = _fp(raw_input)
        ts = receipts[-1]["timestamp"]
        n.storage_seal_proof = seal_proof(n.content_fingerprint_sha256, ts, n.result_operator)
        n.storage_notion = False
        n.storage_jsonl = True
        emit(2, "hold", base_dna)
        n.persona_main_trace.extend(["P03@隐私", "P05@审计", "P72@封存"])
        return _finalize_sealed(n, receipts, laws)

    if n.privacy_mode == "burn":
        # burn：对外销毁可读性；链上保留 burn_proof（append-only，见 SOVEREIGN-CONTAINER 铁律4）
        laws.append("LAW-04-burn")
        n.raw_body_allowed = False
        fp = _fp(raw_input)
        n.content_fingerprint_sha256 = fp
        ts = receipts[-1]["timestamp"]
        n.storage_destroy_proof = burn_proof(fp, ts, n.result_operator)
        emit(2, "pass", base_dna)
        n.persona_main_trace.append("P03@burn")
        n.gate_trace.append("privacy:burn_append_only")
        n.storage_notion = False
    else:
        n.content_fingerprint_sha256 = _fp(raw_input)
        emit(2, "pass", base_dna)
        n.gate_trace.append("privacy:normal")

    # 敏感 → 强制 sealed 行为（§6.1-10）不在此改 privacy_mode 已 normal 时仍熔断外存
    if _SENS.search(raw_input):
        laws.append("LAW-10-sensitive")
        n.privacy_mode = "sealed"
        n.raw_body_allowed = False
        n.storage_notion = False
        fused = True
        emit(2, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "命中敏感词·强制封存路径")

    # ⑤ trace + export
    if n.privacy_trace_mode == "no_external" and ("export" in action.lower() or "外发" in action):
        laws.append("LAW-05-no_export")
        fused = True
        emit(5, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "no_external 禁止外发")

    explicit = tags.get("explicit_dr")
    ex = int(explicit) if explicit is not None and str(explicit).isdigit() else None
    dr, dr_src = compute_four_source_dr(raw_input, dna_blob, ex, raw_input)
    n.math_dr = dr
    n.gate_trace.append(f"dr:{dr_src}")
    emit(3, "pass", base_dna)
    emit(4, "pass", base_dna)

    el = element_for_dr(dr)
    n.math_element = el
    n.persona_main_trace.append("P06@dr+wuxing")

    sc = normalize_sancai(n.sancai_heaven, n.sancai_human, n.sancai_earth)
    n.sancai_heaven, n.sancai_human, n.sancai_earth = sc.heaven, sc.human, sc.earth
    if sc.clamped:
        laws.append("LAW-06-human_floor")
    if n.level.startswith("L0"):
        n.audit_need_uid_confirm = True
        laws.append("LAW-09-L0")

    col = audit_color(dr, n.auto_execute, n.level)
    n.audit_tricolor = col
    if dr in (3, 9) and n.auto_execute:
        laws.append("LAW-07-dr39_autoexec")
        fused = True
        emit(5, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "dr∈{3,9} 禁止自动执行")

    emit(5, "pass" if col == "🟢" else "hold", base_dna)
    emit(6, "pass", base_dna)

    parent_el = _parent_element(n.parent_dna) if n.parent_dna else n.math_element
    n.shengke_note = relation_to_parent(n.math_element, parent_el)
    if not validate_parent_chain(n.parent_dna, known_parent_roots):
        laws.append("LAW-DNA-parent_missing")
        fused = True
        emit(7, "fuse", base_dna)
        return _finalize_fuse(n, receipts, fused, laws, "parent_dna 链断裂")

    emit(7, "pass", base_dna)

    pal = route_palaces(n.math_element, n.privacy_trace_mode, action)
    n.route_palace = pal
    emit(8, "pass", base_dna)
    n.persona_main_trace.append("P13@palace")

    n.warmup_score = contribution_heat(n.level, dr)
    n.route_bucket = pick_bucket(col, n.privacy_mode, fuse=False)
    emit(9, "pass", base_dna)

    n.dna_current = base_dna
    n.dna_child = derive_child_dna(base_dna)
    emit(10, "pass", base_dna)
    n.persona_main_trace.append("P15@chain")

    n.result_status = map_result_status(col)
    n.storage_notion = n.privacy_mode == "normal" and col == "🟢"
    n.ipa_chain_complete = len(receipts) == len(IPA_CHAIN)
    n.fuse_reason = ""
    return FlowRunResult(node=n, ipa_receipts=receipts, fused=False, laws_triggered=laws)


def _finalize_fuse(node: FlowDecisionNode, receipts: List[Dict], fused: bool, laws: List[str], reason: str) -> FlowRunResult:
    node.result_status = "fuse"
    node.audit_tricolor = "🔴"
    node.route_bucket = pick_bucket("🔴", node.privacy_mode, fuse=True)
    node.fuse_reason = reason
    node.ipa_chain_complete = False
    return FlowRunResult(node=node, ipa_receipts=receipts, fused=True, laws_triggered=laws + [reason])


def _finalize_sealed(node: FlowDecisionNode, receipts: List[Dict], laws: List[str]) -> FlowRunResult:
    node.result_status = "hold"
    node.audit_tricolor = "🟡"
    node.route_bucket = pick_bucket("🟡", "sealed", fuse=False)
    node.ipa_chain_complete = len(receipts) >= 3
    return FlowRunResult(node=node, ipa_receipts=receipts, fused=False, laws_triggered=laws + ["sealed_pipeline"])
