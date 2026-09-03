#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-FUSE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · fuse —— P0 熔断（四级: L0伦理>L1数据>L2人格>L3行为）
"""
import json
import time as _t
from pathlib import Path

LEVELS = {"L0": "∞ 伦理", "L1": "数据", "L2": "人格", "L3": "行为"}
_RECOVERABLE = {"L3", "L2"}
_UNRECOVERABLE = {"L0", "L1"}


def trip(level: str, reason: str, path: str = None) -> dict:
    """触发熔断（默认登记 ~/.longhun/fuse_log.jsonl）"""
    level = (level or "L3").upper()
    rec = {
        "ts": _t.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "label": LEVELS.get(level, level),
        "reason": reason,
        "recoverable": level in _RECOVERABLE,
    }
    p = Path(path or Path.home() / ".longhun" / "fuse_log.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    rec["blocked"] = True
    return rec


def is_triggered(reason: str, path: str = None) -> bool:
    """红线关键词熔断检测（涉童/私钥/伪造DNA/背叛）"""
    keys = ["涉童", "儿童色情", "GPG私钥", "私钥传出", "伪造DNA", "背叛",
            "海外部署内核", "渗透外部", "儿童"]
    return any(k in (reason or "") for k in keys)


def check(reason: str, path: str = None):
    """一键熔断检查: 命中红线 → trip L0 并抛异常"""
    if is_triggered(reason):
        trip("L0", reason, path)
        raise PermissionError(f"P0 熔断 L0: {reason}")
