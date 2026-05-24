# -*- coding: utf-8 -*-
"""chain_hash · 粒子规范化指纹（与 §2 `chain` 对齐）"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict

from .particle import CNSH_DNA_Particle


def particle_dict_fingerprint(body: Dict[str, Any]) -> str:
    """body = CNSH_DNA_PARTICLE 顶层 dict；计算前将 chain._self_hash 清空。"""
    b = copy.deepcopy(body)
    ch = b.get("chain")
    if not isinstance(ch, dict):
        ch = {}
    ch = {**ch, "_self_hash": ""}
    b["chain"] = ch
    canonical = json.dumps(b, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def set_particle_chain(p: CNSH_DNA_Particle, prev_hash: str) -> CNSH_DNA_Particle:
    from copy import deepcopy

    p2 = deepcopy(p)
    p2.chain.prev_hash = prev_hash
    p2.chain.self_hash = ""
    d = p2.to_dict()["CNSH_DNA_PARTICLE"]
    sh = particle_dict_fingerprint(d)
    p2.chain.self_hash = sh
    return p2


def particle_payload_fingerprint(p: CNSH_DNA_Particle) -> str:
    d = p.to_dict()["CNSH_DNA_PARTICLE"]
    return particle_dict_fingerprint(d)
