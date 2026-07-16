#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNA 追溯公共模块。
DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-CORE-DNA-v1.0
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%f")


def hash_short(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length].upper()


class DNATracer:
    """统一 DNA 生成器：#{PREFIX}-{TYPE}-{YYYYMMDD}-{seq:04d}。"""

    def __init__(self, prefix: str, agent_dna: str):
        self.prefix = prefix.upper()
        self.agent_dna = agent_dna
        self._counter: dict = {}
        self._date_cache: Optional[str] = None

    def generate(self, operation_type: str = "OP") -> str:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        if today != self._date_cache:
            self._date_cache = today
            self._counter = {}
        key = operation_type.upper()
        self._counter[key] = self._counter.get(key, 0) + 1
        return f"#{self.prefix}-{operation_type.upper()}-{today}-{self._counter[key]:04d}"

    def stamp(self, data: dict, operation_type: str = "OP") -> dict:
        data["dna_trace"] = self.generate(operation_type)
        data["agent_dna"] = self.agent_dna
        data["timestamp"] = datetime.now(timezone.utc).isoformat()
        return data


def agent_dna(persona_code: str) -> str:
    """按标准格式生成 Agent DNA：#{CODE}-AGENT-CONFIG-YYYYMMDD-NNN。"""
    code = re.sub(r"[^A-Z0-9]", "", persona_code.upper())
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = hash_short(f"{code}-AGENT-CONFIG-{date_str}", 6)
    seq_num = str(int(seq, 16) % 1000).zfill(3)
    return f"#{code}-AGENT-CONFIG-{date_str}-{seq_num}"


def register_dna(registry_path: Path, persona_code: str, name: str, path: str) -> str:
    """把人格 DNA 写入注册表。"""
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if registry_path.exists():
        try:
            data = json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    dna = agent_dna(persona_code)
    data[persona_code] = {
        "name": name,
        "dna": dna,
        "path": path,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    registry_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return dna
