#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 审计钩子 v1.0
DNA: #龍芯⚡️2026-08-22-AUDIT-HOOK-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

审计钩子 · 所有沙箱操作必须经过此钩子记录 · append-only 不可篡改
DNA 引擎复用 core.longhun_core.dna_trace (现成主权引擎), 失败则内置 sha256 fallback
"""

import json
import time
import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

def generate_dna(module: str = "sandbox", action: str = "audit") -> str:
    """
    优先复用 core.longhun_core.dna_trace 时间戳 DNA 引擎
    不可用时内置 sha256 fallback (禁 md5: 规则第七层加密下界)
    """
    try:
        sys.path.insert(0, str(ROOT))
        from core.longhun_core.dna_trace import generate_dna as lh_generate_dna
        return lh_generate_dna(module=module.upper(), action=action[:20])
    except Exception:
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        seed = f"{module}{action}{ts}{time.time()}"
        h8 = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-{module}-{action}-{h8}"

class AuditHook:
    """审计钩子 · 所有沙箱操作必须经过此钩子记录 · append-only 不可篡改"""

    def __init__(self, log_path: Optional[Path] = None):
        if log_path is None:
            log_path = ROOT / "logs" / "sandbox_audit.jsonl"
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, plugin_id: str, event: str, detail: str,
            tri_color: str = "🟡", dna: Optional[str] = None,
            extra: Optional[dict] = None) -> str:
        if dna is None:
            dna = generate_dna(module="sandbox", action=event[:20])
        entry = {
            "timestamp": datetime.now().isoformat(),
            "plugin_id": plugin_id,
            "event": event,
            "detail": detail,
            "tri_color": tri_color,
            "dna": dna,
            "extra": extra or {},
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return dna

    def get_recent(self, n: int = 50, plugin_id: Optional[str] = None) -> list:
        entries = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if plugin_id is None or entry.get("plugin_id") == plugin_id:
                            entries.append(entry)
        except FileNotFoundError:
            return []
        return entries[-n:]

    def count_violations(self, plugin_id: str) -> int:
        count = 0
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if entry.get("plugin_id") == plugin_id and entry.get("tri_color") == "🔴":
                            count += 1
        except FileNotFoundError:
            return 0
        return count
