# -*- coding: utf-8 -*-
"""
DNA 记忆压缩与可逆重建 · v1.0 代码实装
DNA: #龍芯⚡️2026-05-16-CNSH-DNA-MEMORY-COMPRESS-v1.0
"""
from __future__ import annotations

from .chain_store import append_particle, default_db_path, find_dna_ids_by_trigger, init_db, verify_chain
from .compress import compress_dialogue
from .huangli import generate_huangli_timestamp, verify_time_hash, detect_schedule_anomaly
from .particle import CNSH_DNA_Particle, particle_from_flat_dict
from .restore import (
    Context,
    RestoredCognitiveContext,
    restore_by_trigger,
    restore_cognitive_state,
    verify_particle_self_hash,
)

__all__ = [
    "CNSH_DNA_Particle",
    "append_particle",
    "compress_dialogue",
    "Context",
    "default_db_path",
    "detect_schedule_anomaly",
    "find_dna_ids_by_trigger",
    "generate_huangli_timestamp",
    "init_db",
    "particle_from_flat_dict",
    "RestoredCognitiveContext",
    "restore_by_trigger",
    "restore_cognitive_state",
    "verify_chain",
    "verify_particle_self_hash",
    "verify_time_hash",
]
