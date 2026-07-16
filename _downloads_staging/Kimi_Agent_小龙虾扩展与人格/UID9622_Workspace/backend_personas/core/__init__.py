#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backend_personas.core - 小龙虾人格公共核心库
DNA: #龍芯⚡️2026-06-27-BACKEND-PERSONAS-CORE-v1.0
"""
from .audit import AuditMark, TricolorAudit
from .config import load_config, workspace_root
from .dna import DNATracer, register_dna
from .hashing import hash_file, hash_string
from .logger import setup_logging
from .messenger import Messenger
from .security import SecurityFilter
from .telemetry import TelemetryCollector, compute_scores, get_runs, get_summary
from .dashboard import generate_html, print_summary

__all__ = [
    "AuditMark",
    "TricolorAudit",
    "load_config",
    "workspace_root",
    "DNATracer",
    "register_dna",
    "hash_file",
    "hash_string",
    "setup_logging",
    "Messenger",
    "SecurityFilter",
    "TelemetryCollector",
    "compute_scores",
    "get_runs",
    "get_summary",
    "generate_html",
    "print_summary",
]
