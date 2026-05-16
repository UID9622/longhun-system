# -*- coding: utf-8 -*-
"""
dragon_daemon 集成片段：在执行 .cnsh 前后/异常时调用责任卡网关。

使用方式（示例，不自动改你的 daemon）：

    from cnsh.decision_cards.engine.dragon_daemon_decision_patch import (
        trigger_decision_card,
    )

    trigger_decision_card("before", path, "pending", "执行前")
"""
from __future__ import annotations

import sys
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent
if str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))


def trigger_decision_card(
    event: str,
    file_path: str,
    status: str = "pending",
    detail: str = "",
    *,
    light: bool = False,
) -> None:
    import cnsh_decision_gateway as g

    r = g.invoke(event, file_path, status=status, detail=detail, light=light)
    if r.stdout:
        print(r.stdout, end="")
    if r.returncode != 0 and r.stderr:
        print(r.stderr, end="")
