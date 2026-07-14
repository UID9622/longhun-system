#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 审计与 DNA 追溯
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-AUDITOR-v1.0
"""
import json
import hashlib
import uuid
from datetime import datetime
from pathlib import Path

from config import Config


class Auditor:
    """统一审计器：每次能力调用、规则覆盖、训练操作都写 DNA 追溯日志。"""

    def __init__(self, log_path=None):
        self.log_path = Path(log_path) if log_path else Config.audit_log
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.dna_prefix = Config.dna_prefix

    def _generate_dna(self, action_type):
        ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
        rand = uuid.uuid4().hex[:8].upper()
        seed = f"{ts}-{action_type}-{rand}"
        h = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
        return f"{self.dna_prefix}{ts}-{action_type}-{h}"

    def log(self, action_type, capability=None, input_data=None, output_data=None,
            status="success", metadata=None):
        """记录一条审计日志。"""
        dna = self._generate_dna(action_type)
        record = {
            "dna": dna,
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "capability": capability,
            "input": self._safe_json(input_data),
            "output": self._safe_json(output_data),
            "status": status,
            "metadata": metadata or {},
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return dna

    def _safe_json(self, obj):
        """把对象序列化成可 JSON 的格式。"""
        if obj is None:
            return None
        try:
            return json.loads(json.dumps(obj, ensure_ascii=False, default=str))
        except Exception:
            return str(obj)

    def query(self, dna=None, action_type=None, capability=None, limit=100):
        """查询审计日志。"""
        results = []
        if not self.log_path.exists():
            return results
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if dna and rec.get("dna") != dna:
                    continue
                if action_type and rec.get("action_type") != action_type:
                    continue
                if capability and rec.get("capability") != capability:
                    continue
                results.append(rec)
                if limit and len(results) >= limit:
                    break
        return results
