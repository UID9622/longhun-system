#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 能力门控 v1.0
DNA: #龍芯⚡️2026-08-22-CAPABILITY-GATE-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from typing import Set, Dict, Any, Optional
from dataclasses import dataclass

# 能力定义表
CAPABILITY_DEFS = {
    "fs.read":      {"desc": "读取指定目录文件", "default": False, "risk": "low"},
    "fs.write":     {"desc": "写入自己的沙箱目录", "default": False, "risk": "medium"},
    "fs.write_system": {"desc": "写入系统目录", "default": False, "risk": "critical"},
    "net.http":     {"desc": "发起受限 HTTP 请求", "default": False, "risk": "medium"},
    "net.socket":   {"desc": "原始网络连接", "default": False, "risk": "critical"},
    "agent.call":   {"desc": "调用 local_agent 的指定工具", "default": False, "risk": "high"},
    "memory.append": {"desc": "向 MEMORY.md 追加记录", "default": False, "risk": "low"},
    "vision.call":  {"desc": "调用视觉模块", "default": False, "risk": "medium"},
    "voice.call":   {"desc": "调用语音模块", "default": False, "risk": "medium"},
    "dna.generate": {"desc": "请求生成 DNA", "default": False, "risk": "low"},
    "dna.verify":   {"desc": "验证 DNA", "default": False, "risk": "low"},
    "audit.log":    {"desc": "写入审计日志", "default": False, "risk": "low"},
}

@dataclass
class CapabilityRequest:
    """能力请求"""
    plugin_id: str
    capability: str
    action: str
    payload: Dict[str, Any]
    dna: Optional[str] = None

@dataclass
class CapabilityResponse:
    """能力响应"""
    status: str  # ok | error | denied
    data: Any = None
    error: Optional[str] = None
    dna: Optional[str] = None

class CapabilityGate:
    """
    能力门控 · 强制执行权限检查
    所有插件请求必须经过此门控才能执行 (默认全拒, 显式授予才放行)
    """

    def __init__(self, audit_hook=None):
        self.audit_hook = audit_hook
        self._grants: Dict[str, Set[str]] = {}

    def grant(self, plugin_id: str, capabilities: list) -> None:
        if plugin_id not in self._grants:
            self._grants[plugin_id] = set()
        for cap in capabilities:
            if cap in CAPABILITY_DEFS:
                self._grants[plugin_id].add(cap)
            else:
                raise ValueError(f"未知能力: {cap}")

    def revoke(self, plugin_id: str) -> None:
        self._grants.pop(plugin_id, None)

    def check(self, plugin_id: str, capability: str) -> bool:
        if plugin_id not in self._grants:
            return False
        return capability in self._grants[plugin_id]

    def request(self, request: CapabilityRequest) -> CapabilityResponse:
        # 1. 能力是否存在
        if request.capability not in CAPABILITY_DEFS:
            if self.audit_hook:
                self.audit_hook.log(request.plugin_id, "CAPABILITY_UNKNOWN",
                                    f"Unknown capability: {request.capability}", "🔴")
            return CapabilityResponse(status="error", error=f"未知能力: {request.capability}")
        # 2. 是否被授予
        if not self.check(request.plugin_id, request.capability):
            if self.audit_hook:
                self.audit_hook.log(request.plugin_id, "CAPABILITY_DENIED",
                                    f"Capability denied: {request.capability}", "🔴")
            return CapabilityResponse(
                status="denied",
                error=f"插件 {request.plugin_id} 未授权使用 {request.capability}")
        # 3. 通过
        if self.audit_hook:
            self.audit_hook.log(request.plugin_id, "CAPABILITY_GRANTED",
                                f"Capability used: {request.capability}", "🟢")
        return CapabilityResponse(
            status="ok", data={"message": f"Capability {request.capability} allowed"},
            dna=request.dna)

    def list_capabilities(self, plugin_id: str) -> list:
        if plugin_id not in self._grants:
            return []
        return list(self._grants[plugin_id])

    def get_capability_def(self, capability: str) -> Optional[Dict]:
        return CAPABILITY_DEFS.get(capability)
