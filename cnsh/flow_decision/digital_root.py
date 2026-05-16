# -*- coding: utf-8 -*-
"""四源数字根 v4.1（§3.3）"""
from __future__ import annotations

import hashlib
import re
from typing import Optional, Tuple


def _digits_from_string(s: str) -> int:
    digs = [int(c) for c in re.findall(r"\d", s)]
    if not digs:
        return 0
    return sum(digs)


def _dr9(n: int) -> int:
    if n <= 0:
        return 9
    return 1 + ((n - 1) % 9)


def _reduce_dr_digits(n: int) -> int:
    if n <= 0:
        return 9
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n if n > 0 else 9


def compute_four_source_dr(
    raw_text: str,
    dna_string: str = "",
    explicit_dr: Optional[int] = None,
    content_for_hash: Optional[str] = None,
) -> Tuple[int, str]:
    """
    返回 (dr, source_name)
    优先级: explicit > dna_digits > content_hash > raw_digits > fallback_zero(土)
    """
    if explicit_dr is not None and 1 <= explicit_dr <= 9:
        return explicit_dr, "explicit_dr"

    dsum = _digits_from_string(dna_string)
    if dsum > 0:
        return _dr9(_reduce_dr_digits(dsum)), "dna_digits"

    body = content_for_hash if content_for_hash is not None else raw_text
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]
    hv = int(h, 16)
    dr_h = _dr9(hv % 99999999 or 9)
    if dr_h:
        return dr_h, "content_hash"

    raw_sum = _digits_from_string(raw_text)
    if raw_sum > 0:
        return _dr9(_reduce_dr_digits(raw_sum)), "raw_digits"

    return 0, "fallback_zero"
