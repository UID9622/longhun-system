"""
龍魂·第一道闸门融合引擎包

DNA: #龍芯⚡️2026-04-26-LONGHUN-GATE-PKG-v1.0
作者：龍芯北辰｜UID9622
理论指导：曾仕强老師（永恒显示）

公开 API：
    from longhun_gate import decide, digital_root_from_text, validate_dna
"""
from .gate_engine import (
    decide,
    digital_root_from_text,
    gate_color,
    validate_dna,
    generate_l4_dna,
    rule_check,
    falsehood_check,
    data_guard_check,
    detect_drawers,
    element_relation,
    DrawerRule,
    DRAWERS,
    KEYWORDS,
    OWNER_UID,
    CONFIRM_CODE,
)

__version__ = "1.0.0"
__all__ = [
    "decide",
    "digital_root_from_text",
    "gate_color",
    "validate_dna",
    "generate_l4_dna",
    "rule_check",
    "falsehood_check",
    "data_guard_check",
    "detect_drawers",
    "element_relation",
    "DrawerRule",
    "DRAWERS",
    "KEYWORDS",
    "OWNER_UID",
    "CONFIRM_CODE",
]
