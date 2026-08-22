#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 插件侧 API v1.0
DNA: #龍芯⚡️2026-08-22-SANDBOX-API-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from typing import Dict, Any, Optional
from .capability_gate import CapabilityGate, CapabilityRequest, CapabilityResponse


class SandboxAPI:
    """
    插件侧唯一合法通信接口
    插件只能通过此对象与主系统交互 · 不能直接 import 核心模块
    """

    def __init__(self, plugin_id: str, gate: CapabilityGate, audit_hook):
        self._plugin_id = plugin_id
        self._gate = gate
        self._audit = audit_hook

    def request(self, capability: str, action: str, payload: Dict[str, Any] = None,
                dna: Optional[str] = None) -> Dict[str, Any]:
        if payload is None:
            payload = {}
        req = CapabilityRequest(
            plugin_id=self._plugin_id, capability=capability,
            action=action, payload=payload, dna=dna)
        resp = self._gate.request(req)
        result = {"status": resp.status, "dna": resp.dna}
        if resp.status == "ok":
            result["data"] = resp.data
        else:
            result["error"] = resp.error
        return result

    def request_memory_append(self, content: str, source: str = "plugin") -> Dict[str, Any]:
        return self.request("memory.append", "append", {"content": content, "source": source})

    def request_dna_generate(self, module: str, action: str) -> Dict[str, Any]:
        return self.request("dna.generate", "generate", {"module": module, "action": action})

    def request_agent_call(self, tool: str, args: Dict) -> Dict[str, Any]:
        return self.request("agent.call", "call", {"tool": tool, "args": args})

    def request_fs_read(self, path: str) -> Dict[str, Any]:
        return self.request("fs.read", "read", {"path": path})

    def request_fs_write(self, path: str, content: str) -> Dict[str, Any]:
        return self.request("fs.write", "write", {"path": path, "content": content})
