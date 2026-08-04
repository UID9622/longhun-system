#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2
"""
🐲 龍魂·Agent总线适配器 v2.0
DNA: #龍芯⚡️2026-08-04-AGENT-BUS-ADAPTER-UID9622

封装现有 InterAgentBus:
  register(agent)  - agent需有 PERSONA_CODE 属性
  send(msg)        - 需要 BusMessage 对象
  broadcast(msg)   - 需要 BusMessage 对象
  unregister(code)
"""

import sys
import threading
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

SYSTEM_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_inter_agent_bus import InterAgentBus, get_bus, BusMessage


class AgentBusAdapter:
    """总线适配器 — 统一智能体间通信"""

    def __init__(self, use_global: bool = True):
        if use_global:
            self._bus = get_bus()
        else:
            self._bus = InterAgentBus()
        self._lock = threading.RLock()
        self._registered: Dict[str, Any] = {}

    def register(self, agent: Any) -> bool:
        """注册Agent到总线。Agent需要 PERSONA_ID 属性"""
        with self._lock:
            agent_id = getattr(agent, 'PERSONA_ID', None)
            if not agent_id:
                return False
            # 如果是 LonghunAgent 子类，设置 PERSONA_CODE 给总线用
            if not hasattr(agent, 'PERSONA_CODE'):
                setattr(agent, 'PERSONA_CODE', agent_id)
            try:
                self._bus.register(agent)
                self._registered[agent_id] = agent
                return True
            except Exception:
                return False

    def unregister(self, agent_id: str):
        with self._lock:
            self._registered.pop(agent_id, None)
            try:
                self._bus.unregister(agent_id)
            except Exception:
                pass

    def send(self, sender_id: str, recipient_id: str, content: Any, msg_type: str = "task") -> str:
        msg_id = uuid.uuid4().hex[:12]
        if not isinstance(content, dict):
            content = {"data": content}
        msg = BusMessage(
            msg_id=msg_id, sender=sender_id, recipient=recipient_id,
            msg_type=msg_type, content=content,
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-BUS-{msg_type.upper()}"
        )
        try:
            self._bus.send(msg)
            return msg_id
        except Exception as e:
            return f"error:{e}"

    def broadcast(self, sender_id: str, content: Any, msg_type: str = "broadcast",
                  exclude: Optional[List[str]] = None) -> List[str]:
        exclude = exclude or []
        if not isinstance(content, dict):
            content = {"data": content}
        msg = BusMessage(
            msg_id=uuid.uuid4().hex[:12], sender=sender_id, recipient="*",
            msg_type=msg_type, content=content,
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-BUS-BROADCAST"
        )
        try:
            self._bus.broadcast(msg)
            return ["broadcast_sent"]
        except Exception:
            return []

    def get_bus(self):
        return self._bus

    @property
    def registered_count(self) -> int:
        return len(self._registered)
