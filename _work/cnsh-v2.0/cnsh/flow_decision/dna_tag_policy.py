# -*- coding: utf-8 -*-
"""DNA 多标签解析（§3.2）·父子链校验（§3.4 简化）"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DnaTagView:
    visibility: str = "internal"
    trace_mode: str = "chain"
    operator: str = "local_engine"
    p0_touched: bool = False
    level: str = "L3日常"


_TAG_RE = re.compile(
    r"\[visibility:(?P<v>public|internal|private)\]"
    r"|\[trace:(?P<t>chain|local_only|no_external)\]"
    r"|\[operator:(?P<o>[^\]]+)\]"
    r"|\[p0:(?P<p0>true|false)\]"
    r"|\[level:(?P<l>L0永恒|L1百年|L2十年|L3日常|L5临时)\]",
    re.I,
)


def parse_dna_tail_tags(dna_or_blob: str) -> DnaTagView:
    v = DnaTagView()
    if not dna_or_blob:
        return v
    for m in _TAG_RE.finditer(dna_or_blob):
        if m.group("v"):
            v.visibility = m.group("v").lower()
        if m.group("t"):
            v.trace_mode = m.group("t").lower()
        if m.group("o"):
            v.operator = m.group("o").strip()
        if m.group("p0"):
            v.p0_touched = m.group("p0").lower() == "true"
        if m.group("l"):
            v.level = m.group("l")
    return v


def burn_proof(content_hash: str, ts: str, operator: str) -> str:
    """
    SOVEREIGN-CONTAINER 语义：burn = 对外不可读，链上只追加本证明事件，不物理删历史。
    见 01_protocols/cnsh/PROTOCOL__SOVEREIGN-CONTAINER-v1.0.md 铁律4。
    """
    return f"burn_proof:sha256:{content_hash}+{ts}+{operator}"


def seal_proof(content_hash: str, ts: str, operator: str, p72_sig: str = "P72") -> str:
    """
    封存证明：密文层保留；外显仅粒子（DNA+SHA256）；解封须 unseal_observed 账本事件。
    """
    return f"seal_proof:sha256:{content_hash}+{ts}+{operator}+{p72_sig}"


def validate_parent_chain(parent_dna: str, known_roots: Optional[set] = None) -> bool:
    """parent 为空视为首条；非空且提供 known_roots 时可验存在性。"""
    if not parent_dna or not parent_dna.strip():
        return True
    if known_roots is None:
        return True
    return parent_dna.strip() in known_roots
