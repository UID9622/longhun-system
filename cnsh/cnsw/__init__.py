# -*- coding: utf-8 -*-
"""
CNSW · 国产 AI 围猎钩子传感器（本地 · 无 API）
DNA: #龍芯⚡️2026-05-15-04:57-CN-AI-HOOK-TRACE-v1.0
"""
from __future__ import annotations

from .batch_auditor import (
    audit_messages,
    audit_text_file,
    parse_chat_lines,
    summarize,
    write_csv,
)
from .circuit_breaker import circuit_breaker, set_audit_writer
from .hook_scanner import scan_output, scan_outputs
from .registry import SOVEREIGNTY_HOOKS, SUPPLEMENTAL_HOOKS

__all__ = [
    "SOVEREIGNTY_HOOKS",
    "SUPPLEMENTAL_HOOKS",
    "audit_messages",
    "audit_text_file",
    "circuit_breaker",
    "parse_chat_lines",
    "scan_output",
    "scan_outputs",
    "set_audit_writer",
    "summarize",
    "write_csv",
]
