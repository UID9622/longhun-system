# -*- coding: utf-8 -*-
"""第一道闸门 · 本机通知（🔕 主动层）"""
from __future__ import annotations

import subprocess
from typing import Optional

from .engine import GateDecision


def notify_gate(decision: GateDecision, *, subtitle: str = "龍魂第一道闸门") -> bool:
    """
    macOS: osascript 弹窗 + Glass 音效。
    非 macOS 或失败时静默返回 False（被动层仍写账本）。
    """
    if decision.notify_level == "none":
        return False
    title = f"{decision.audit_color} 闸门"
    body = (decision.decision or "")[:200]
    script = (
        f'display notification "{_escape(body)}" '
        f'with title "{_escape(title)}" subtitle "{_escape(subtitle)}" sound name "Glass"'
    )
    try:
        subprocess.run(["osascript", "-e", script], check=False, timeout=5)
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')
