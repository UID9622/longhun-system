# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-SECOND-BRAIN-MODELS-v1.0"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Note:
    note_id: str
    path: str
    title: str
    content: str
    content_hash: str
    created: str
    modified: str
    tags: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    dna: str = ""
    audit: str = "🟢"


@dataclass
class Chunk:
    chunk_id: str
    note_id: str
    text: str
    seq: int = 0


@dataclass
class Edge:
    source: str
    target: str
    type: str = "wiki_link"
    weight: float = 1.0
