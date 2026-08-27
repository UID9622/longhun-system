# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 事件 · 史官监听
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-EVENTS-UID9622
"""

from datetime import datetime
from typing import Dict, Any
from .core import Event, generate_dna, write_historian

class Historian(Event):
    name = "historian"
    description = "史官事件监听 - 全链路记录"

    def __init__(self):
        self._handlers = {}

    def register_handler(self, event_type: str, handler):
        self._handlers[event_type] = handler

    def trigger(self, event_type: str = "unknown", **kwargs):
        """触发事件"""
        dna = generate_dna("EVENT")
        write_historian(
            operation=event_type,
            dna=dna,
            details={k: str(v)[:500] for k, v in kwargs.items()}
        )

        # 调用注册的处理器
        if event_type in self._handlers:
            try:
                self._handlers[event_type](**kwargs)
            except Exception:
                pass  # 处理器失败不影响主流程
