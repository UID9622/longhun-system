# -*- coding: utf-8 -*-
"""
三才·六维内核适配层（H武器专用）
对接：cnsh.flow_decision.digital_root / wuxing + cnsh.dna_memory.huangli 卦象
DNA: #龍芯⚡️2026-05-16-08:10-SANCAI-KERNEL-ADAPTER-v1.0
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Tuple

from cnsh.dna_memory.huangli import dr_to_trigram
from cnsh.flow_decision.digital_root import compute_four_source_dr
from cnsh.flow_decision.wuxing_router import element_for_dr

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

FIXED_POINT_NAMES = ("龍", "龍魂", "道德经", "UID9622", "主权", "CNSH", "北辰", "龍芯")


def digital_root(text: str, **kwargs: Any) -> Tuple[int, str]:
    return compute_four_source_dr(text, **kwargs)


def wuxing_from_dr(dr: int) -> str:
    return element_for_dr(dr)


def luoshu_position(dr: int) -> int:
    """洛书九宫格位 1–9（dr 映射到中宫锚 5 为和谐参照）"""
    d = dr % 9
    return 9 if d == 0 else d


def bagua_from_dr(dr: int) -> str:
    return dr_to_trigram(dr)


def encode_pathway(dr: int, text: str) -> int:
    h = hashlib.sha256(f"{dr}|{text[:200]}".encode("utf-8")).hexdigest()
    return int(h[:8], 16) % 64 + 1


def ganzhi_year(year: int) -> str:
    off = (year - 1984) % 60
    return STEMS[off % 10] + BRANCHES[off % 12]


def wuxing_balance(dr: int) -> float:
    d = luoshu_position(dr)
    return max(0.0, min(1.0, 1.0 - abs(5 - d) / 5.0))


def fixed_point_hits(text: str) -> List[str]:
    return [t for t in FIXED_POINT_NAMES if t in text]


def fuse_tricolor_from_dr(dr: int) -> str:
    """简化的天场三色（与流场闸一致的可调启发式）"""
    if dr in (3, 4, 9):
        return "🔴"
    if dr in (2, 5, 8) or dr == 0:
        return "🟡"
    return "🟢"


def sancai_check(text: str, context: str = "H100K", year: int = 2026) -> Dict[str, Any]:
    """
    返回与 H武器协议 §2.2 兼容的结构（扁平 color + 天地人嵌套）。
    """
    dr, dr_src = compute_four_source_dr(text)
    wx = element_for_dr(dr)
    palace = luoshu_position(dr)
    gua = bagua_from_dr(dr)
    hx = encode_pathway(dr, text)
    gz = ganzhi_year(year)
    hits = fixed_point_hits(text)
    fuse = fuse_tricolor_from_dr(dr)
    return {
        "color": fuse,
        "context": context,
        "dr": dr,
        "dr_source": dr_src,
        "wuxing": wx,
        "luoshu_position": palace,
        "bagua": gua,
        "hexagram_64": hx,
        "ganzhi_year": gz,
        "wuxing_harmony": round(wuxing_balance(dr), 4),
        "天": {
            "fuse": {"color": fuse},
            "ganzhi": gz,
        },
        "地": {
            "wuxing": {"text": wx},
            "luoshu": palace,
            "bagua": gua,
            "hexagram_64": hx,
        },
        "人": {
            "hit_names": hits,
        },
    }


class FixedPointNetwork:
    """协议占位：不动点网络（当前为关键词命中列表）"""

    NAMES = FIXED_POINT_NAMES

    @staticmethod
    def hits(text: str) -> List[str]:
        return fixed_point_hits(text)
