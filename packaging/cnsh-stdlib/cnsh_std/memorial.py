#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-MEMORIAL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · memorial —— 铭碑（append-only 荣耀/里程碑记录 · 不删除只冻结）
"""
import json
import time as _t
from pathlib import Path

_DEFAULT = Path.home() / ".longhun" / "memorial.jsonl"


def record(kind: str, title: str, detail: str = "", path: str = None) -> dict:
    """铭刻一条记录（milestone/荣耀/教训/里程碑）"""
    entry = {
        "ts": _t.strftime("%Y-%m-%d %H:%M:%S"),
        "kind": kind,
        "title": title,
        "detail": detail,
    }
    p = Path(path or _DEFAULT)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def list_records(path: str = None, last: int = 20) -> list:
    """读取铭碑（最近 last 条）"""
    p = Path(path or _DEFAULT)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").strip().splitlines()[-last:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def freeze(path: str = None) -> Path:
    """冻结铭碑（归档为 .freeze-时间戳，不删除原碑）"""
    p = Path(path or _DEFAULT)
    if not p.exists():
        return p
    frozen = p.with_name(f"{p.name}.freeze-{_t.strftime('%Y%m%d')}")
    if not frozen.exists():
        frozen.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    return frozen
