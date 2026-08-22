#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 审计钩子 v1.1
DNA: #龍芯⚡️2026-08-22-AUDIT-HOOK-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

审计钩子 · 所有沙箱操作必须经过此钩子记录 · append-only 不可篡改
v1.1 加固：
  1. detail 清洗（去换行/控制字符）—— 防插件用 detail 伪造 JSONL 审计行。
  2. 模块加载时锁安全引用（import 守卫会替换 builtins.open）。
  3. 写入加线程锁，防并发 append 竞态。
  4. DNA 引擎复用 core.longhun_core.dna_trace，不可用时 sha256 fallback
     （禁 md5：规则第七层加密下界）。
"""

import json
import threading
import time
import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

# 模块加载时捕获安全引用（import 守卫会替换 builtins.open / eval 等）
_safe_open = open

# 并发写锁
_write_lock = threading.Lock()

# DNA 引擎引用（模块加载时——import 守卫安装前——缓存。
# 运行时动态 import core 会被守卫拦截，这里提前抓引用，找不到则 fallback）
_SAFE_DNA_ENGINE = None
try:
    from core.longhun_core.dna_trace import generate_dna as _SAFE_DNA_ENGINE
except Exception:
    _SAFE_DNA_ENGINE = None


def _sanitize(text: str, max_len: int = 300) -> str:
    """清洗 detail：去换行/控制字符（防伪造 JSONL 行）· 截断"""
    cleaned = []
    for ch in str(text):
        o = ord(ch)
        if ch in "\r\n" or (o < 32 and ch not in "\t"):
            cleaned.append(" ")
        else:
            cleaned.append(ch)
    return "".join(cleaned).strip()[:_max_len if (_max_len := max_len) else 300]


def generate_dna(module: str = "sandbox", action: str = "audit") -> str:
    """
    优先复用 core.longhun_core.dna_trace 时间戳 DNA 引擎（模块加载时已缓存引用）
    不可用时内置 sha256 fallback (禁 md5: 规则第七层加密下界)
    """
    if _SAFE_DNA_ENGINE is not None:
        try:
            return _SAFE_DNA_ENGINE(module=module.upper(), action=action[:20])
        except Exception:
            pass
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
            "event": _sanitize(event, 40),
            "detail": _sanitize(detail, 300),
            "tri_color": tri_color,
            "dna": dna,
            "extra": extra or {},
        }
        with _write_lock:
            with _safe_open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return dna

    def get_recent(self, n: int = 50, plugin_id: Optional[str] = None) -> list:
        entries = []
        try:
            with _safe_open(self.log_path, "r", encoding="utf-8") as f:
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
            with _safe_open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if entry.get("plugin_id") == plugin_id and entry.get("tri_color") == "🔴":
                            count += 1
        except FileNotFoundError:
            return 0
        return count
