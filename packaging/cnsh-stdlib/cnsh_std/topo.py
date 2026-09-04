#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-TOPO-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · topo —— 龍魂系统拓扑查询（L0-L9 · 192引擎 · 45技能）
默认读取 longhun-system/.codebuddy/longhun_neural_net.json
"""
import json
from pathlib import Path

_DEFAULT = Path.home() / "longhun-system" / ".codebuddy" / "longhun_neural_net.json"


def _load(path: str = None):
    p = Path(path) if path else _DEFAULT
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def layers(path: str = None) -> list:
    """返回九层名（L0-L9）"""
    d = _load(path)
    return list(d.get("layers", d.get("architecture", {})).keys() or [])


def engines(path: str = None) -> int:
    """引擎数量"""
    d = _load(path)
    n = d.get("engines", d.get("engine_count"))
    if isinstance(n, int):
        return n
    return len(d.get("engines", []) if isinstance(d.get("engines"), list) else [])


def skills(path: str = None) -> list:
    """技能清单"""
    d = _load(path)
    return d.get("skills", d.get("skill_list", [])) or []


def personas(path: str = None) -> list:
    """人格清单"""
    d = _load(path)
    return d.get("personas", []) or []


def snapshot(path: str = None) -> dict:
    """拓扑快照摘要"""
    d = _load(path)
    return {
        "found": bool(d),
        "layers": layers(path),
        "engine_count": engines(path),
        "skill_count": len(skills(path)),
        "persona_count": len(personas(path)),
    }
