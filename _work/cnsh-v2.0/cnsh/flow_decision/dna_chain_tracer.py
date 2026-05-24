# -*- coding: utf-8 -*-
"""DNA 父子链（§3.4 简化）"""
from __future__ import annotations

import hashlib
from typing import Optional


def derive_child_dna(current_dna: str, suffix: str = "CHILD") -> str:
    h8 = hashlib.sha256(f"{current_dna}|{suffix}".encode()).hexdigest()[:8]
    return f"{current_dna}-CHILD-{h8}"
