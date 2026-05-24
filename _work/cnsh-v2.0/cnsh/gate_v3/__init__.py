# 第一道闸门 v3.0 · 输入海关
# DNA: #龍芯⚡️2026-04-26-第一道闸门-三色审计-沙盒闭环-v3.0

from .engine import (
    GATE_DNA,
    decide,
    digital_root_from_text,
    gate_color,
    validate_dna,
)
from .ledger import append_gate_event, consecutive_red_count
from .notify import notify_gate

__all__ = [
    "GATE_DNA",
    "decide",
    "digital_root_from_text",
    "gate_color",
    "validate_dna",
    "append_gate_event",
    "consecutive_red_count",
    "notify_gate",
]
