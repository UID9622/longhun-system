# -*- coding: utf-8 -*-
"""IPA 路由注册（11 节点 + 统一回执）"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib


@dataclass
class IPANode:
    ipa_id: str
    path: str
    main_persona: str
    next_ipa: Optional[str]


IPA_CHAIN: List[IPANode] = [
    IPANode("IPA-FLOW-DECISION-CORE-v4.1", "/flow/core", "P00", "IPA-FLOW-GATE-SIGN"),
    IPANode("IPA-FLOW-GATE-SIGN", "/flow/gate/sign", "P05", "IPA-FLOW-GATE-PRIVACY"),
    IPANode("IPA-FLOW-GATE-PRIVACY", "/flow/gate/privacy", "P03", "IPA-FLOW-GATE-DR"),
    IPANode("IPA-FLOW-GATE-DR", "/flow/gate/dr", "P06", "IPA-FLOW-WUXING-MAP"),
    IPANode("IPA-FLOW-WUXING-MAP", "/flow/wuxing", "P06", "IPA-FLOW-GATE-AUDIT"),
    IPANode("IPA-FLOW-GATE-AUDIT", "/flow/gate/audit", "P05", "IPA-FLOW-GATE-SANCAI"),
    IPANode("IPA-FLOW-GATE-SANCAI", "/flow/gate/sancai", "P00", "IPA-FLOW-GATE-SHENGKE"),
    IPANode("IPA-FLOW-GATE-SHENGKE", "/flow/gate/shengke", "P01", "IPA-FLOW-PALACE-ROUTER"),
    IPANode("IPA-FLOW-PALACE-ROUTER", "/flow/palace", "P13", "IPA-FLOW-SANDBOX-BUCKET"),
    IPANode("IPA-FLOW-SANDBOX-BUCKET", "/flow/sandbox", "P03", "IPA-FLOW-DNA-CHAIN"),
    IPANode("IPA-FLOW-DNA-CHAIN", "/flow/dna", "P15", None),
]


def make_receipt(
    ipa_node: str,
    ipa_address: str,
    main_persona: str,
    input_node_id: str,
    output_signal: str,
    next_ipa: Optional[str],
    dna: str,
) -> Dict[str, Any]:
    return {
        "ipa_node": ipa_node,
        "ipa_address": ipa_address,
        "main_persona": main_persona,
        "input_node_id": input_node_id,
        "output_signal": output_signal,
        "next_ipa": next_ipa,
        "dna": dna,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }


def stable_flow_id(seed: str) -> str:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
    return f"FLOW-9622-20260503-{h}"
