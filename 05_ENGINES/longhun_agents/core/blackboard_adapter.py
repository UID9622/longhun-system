#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2
"""
🐲 龍魂·黑板适配器 v2.0
DNA: #龍芯⚡️2026-08-04-BLACKBOARD-ADAPTER-UID9622

封装现有 SharedBlackboard，提供多智能体框架语义。
SharedBlackboard API: put(key, value, writer) / get(key) / keys() / delete(key) / size()
"""

import json
import threading
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

SYSTEM_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_shared_blackboard import SharedBlackboard, get_blackboard


class BlackboardAdapter:
    """黑板适配器 — 为多智能体框架提供统一知识仓库"""

    def __init__(self, use_global: bool = True, log_dir: Optional[Path] = None):
        self._use_global = use_global
        if use_global:
            self._board = get_blackboard()
        else:
            self._board = SharedBlackboard(str(log_dir or Path("blackboard")))
        self._lock = threading.RLock()
        self._markdown_cache: Dict[str, str] = {}

    # ── JSON 数据存取 ──

    def write(self, key: str, data: Any, agent: str = "system") -> bool:
        with self._lock:
            try:
                self._board.put(key, data, agent)
                return True
            except Exception as e:
                print(f"❌ 黑板写入 [{key}]: {e}")
                return False

    def read(self, key: str) -> Optional[Any]:
        try:
            return self._board.get(key)
        except Exception:
            return None

    # ── Markdown 报告 ──

    def write_md(self, key: str, content: str, agent: str = "integrator") -> bool:
        if not key.endswith('.md'):
            key = f"{key}.md"
        self._markdown_cache[key] = content
        return self.write(key, {"type": "markdown_report", "content": content, "agent": agent}, agent)

    def read_md(self, key: str) -> Optional[str]:
        if not key.endswith('.md'):
            key = f"{key}.md"
        if key in self._markdown_cache:
            return self._markdown_cache[key]
        data = self.read(key)
        if data and isinstance(data, dict):
            content = data.get("content", "")
            if content:
                self._markdown_cache[key] = content
            return content
        return None

    # ── 上下文摘要 ──

    def get_context(self) -> Dict[str, Any]:
        keys = self._board.keys()
        context = {"entries": len(keys) if keys else 0, "summary": {}}
        limited = list(keys)[:20] if keys else []
        for k in limited:
            data = self.read(k)
            if data is None:
                continue
            if isinstance(data, dict):
                context["summary"][k] = {
                    "keys": list(data.keys())[:8],
                    "preview": json.dumps(data, ensure_ascii=False, default=str)[:200]
                }
            elif isinstance(data, list):
                context["summary"][k] = {"count": len(data), "sample": data[:2]}
            else:
                context["summary"][k] = str(data)[:150]
        return context

    def list_all(self) -> List[str]:
        k = self._board.keys()
        return list(k) if k else []

    def clear(self, key: Optional[str] = None):
        if key:
            self._board.delete(key)
            self._markdown_cache.pop(key, None)
        else:
            for k in list(self._board.keys() or []):
                self._board.delete(k)
            self._markdown_cache.clear()
