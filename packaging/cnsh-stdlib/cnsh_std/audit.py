#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-AUDIT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · audit —— 三色审计 + append-only 审计日志
色: 🟢 通过 · 🟡 待核 · 🔴 红线
"""
import json
import time as _t
from pathlib import Path

COLORS = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}
_BAD = {"red", "fail", "error", "blocked", "致命"}


def verdict(level: str) -> str:
    """归一化三色判定（输入中/英文）"""
    s = (level or "").lower()
    if "green" in s or "通过" in s or "ok" in s or "pass" in s:
        return COLORS["GREEN"]
    if "red" in s or any(b in s for b in _BAD):
        return COLORS["RED"]
    return COLORS["YELLOW"]


def log(path: str, entry: dict) -> Path:
    """审计日志（JSONL append-only）· entry 自动补时间戳/DNA"""
    entry.setdefault("ts", _t.strftime("%Y-%m-%d %H:%M:%S"))
    entry.setdefault("color", verdict(entry.get("verdict", "🟡")))
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return p


def read_log(path: str, last: int = 50) -> list:
    """读审计日志（最近 last 条）"""
    p = Path(path)
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").strip().splitlines()
    out = []
    for ln in lines[-last:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def block(reason: str) -> dict:
    """🔴 红线阻断（返回并记录）"""
    return {"color": "🔴", "blocked": True, "reason": reason}
