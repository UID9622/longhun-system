# -*- coding: utf-8 -*-
"""flow_port ↔ engine/defense 桥接（避免 cnsh 硬依赖 engine 包路径）"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

_ROOT = Path(__file__).resolve().parents[1]
_ENGINE = _ROOT / "engine"


def defense_scan(text: str, *, direction: str = "in", url: str = "") -> Dict[str, Any]:
    if not (text or "").strip():
        return {"ok": True, "allowed": True, "skipped": True}
    try:
        if str(_ENGINE) not in sys.path:
            sys.path.insert(0, str(_ENGINE))
        from defense.background_daemon import scan_text  # type: ignore

        return scan_text(text, direction=direction, url=url)
    except Exception as exc:
        return {
            "ok": False,
            "allowed": True,
            "skipped": True,
            "error": str(exc),
            "stance": "防御桥接失败·放行并留痕",
        }
