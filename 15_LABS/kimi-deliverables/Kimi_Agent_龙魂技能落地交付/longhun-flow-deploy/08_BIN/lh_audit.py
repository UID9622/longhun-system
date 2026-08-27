#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#龍芯⚡️丙午·丙申·己未·乙亥时·䷞旅-AUDIT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
"""
🐉 龍魂 · 史官 + 耻辱墙 公共模块
落盘位置:
  审计链  /opt/longhun/audit/audit.jsonl   (prev_hash 哈希链, 真实可校验)
  耻辱墙  /opt/longhun/audit/shame_wall.jsonl

修正21: verify_chain 为真实 prev_hash 链校验 (非 stub)。
修正22: generate_dna 掺 uuid4 随机段, 杜绝同秒撞码。
正式干支口径见 bin/lh_dna_generator.py (锚点 2000-01-01=戊午 / 2024-01-01=甲子);
若该生成器在 sys.path 中可导入则复用其算法, 否则回退到本模块的等口径实现。
"""

import hashlib
import json
import os
import sys
import threading
import uuid
from datetime import datetime
from pathlib import Path

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

AUDIT_DIR = Path(os.environ.get("LONGHUN_AUDIT_DIR", "/opt/longhun/audit"))
AUDIT_PATH = AUDIT_DIR / "audit.jsonl"
SHAME_PATH = AUDIT_DIR / "shame_wall.jsonl"

_lock = threading.Lock()
GENESIS_HASH = "0" * 64  # 创世 prev_hash

# 尝试复用正式干支生成器 (SPEC: DNA 一律由 bin/lh_dna_generator.py 算法生成)
try:
    from lh_dna_generator import day_ganzhi as _dz, year_ganzhi as _yz, \
        month_ganzhi as _mz, hour_ganzhi as _hz, gua_of_day as _gua
    _HAS_GANZHI = True
except ImportError:
    _HAS_GANZHI = False


def _four_pillars(now: datetime) -> str:
    """四柱·卦 段。优先复用生成器算法; 不可导入时以日期哈希代替(标🟡)。"""
    if _HAS_GANZHI:
        dg, didx = _dz(now.date())
        return f"{_yz(now.date())}·{_mz(now.date())}·{dg}·{_hz(now.hour, dg[0])}时·䷞{_gua(didx)}"
    # 回退: 不手写干支, 以 ISO 日期占位, 真机部署时 bin/lh_dna_generator.py 应在路径中
    return now.strftime("%Y-%m-%d")


def generate_dna(action: str = "GEN", version: str = "v1.0") -> str:
    """生成运行时 DNA 追溯码。修正22: 掺 uuid4 随机段防同秒撞码。"""
    now = datetime.now()
    rand = uuid.uuid4().hex[:8].upper()
    return f"#龍芯⚡️{_four_pillars(now)}-{action}-{version}-{rand}-UID{UID}"


def _hash_entry(entry_without_hash: dict) -> str:
    canonical = json.dumps(entry_without_hash, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _last_hash() -> str:
    """读取当前链尾 hash (只取最后一行的 hash 字段)。"""
    if not AUDIT_PATH.exists() or AUDIT_PATH.stat().st_size == 0:
        return GENESIS_HASH
    last_line = ""
    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line.strip()
    try:
        return json.loads(last_line).get("hash", GENESIS_HASH)
    except json.JSONDecodeError:
        return GENESIS_HASH


class Historian:
    """史官: 全操作审计, DNA 追溯, prev_hash 哈希链。"""

    @staticmethod
    def record(operation: str, dna: str, details: dict, service: str = "") -> dict:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "operation": operation,
            "dna": dna,
            "details": details,
            "prev_hash": _last_hash(),
        }
        entry["hash"] = _hash_entry(entry)
        with _lock:
            AUDIT_DIR.mkdir(parents=True, exist_ok=True)
            with open(AUDIT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    @staticmethod
    def verify_chain() -> dict:
        """真实校验 prev_hash 哈希链 (修正21)。
        逐条重算: 1) entry.hash 是否等于内容重算值; 2) entry.prev_hash 是否等于上一条 hash。
        返回 {"valid": bool, "entries": n, "broken_at": 行号或None}。
        """
        if not AUDIT_PATH.exists():
            return {"valid": True, "entries": 0, "broken_at": None, "message": "暂无记录"}
        prev = GENESIS_HASH
        count = 0
        with open(AUDIT_PATH, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                count += 1
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    return {"valid": False, "entries": count,
                            "broken_at": lineno, "message": f"第{lineno}行 JSON 损坏"}
                stored_hash = entry.get("hash")
                body = {k: v for k, v in entry.items() if k != "hash"}
                if stored_hash != _hash_entry(body):
                    return {"valid": False, "entries": count,
                            "broken_at": lineno, "message": f"第{lineno}行内容哈希不匹配(疑似篡改)"}
                if entry.get("prev_hash") != prev:
                    return {"valid": False, "entries": count,
                            "broken_at": lineno, "message": f"第{lineno}行 prev_hash 链断裂"}
                prev = stored_hash
        return {"valid": True, "entries": count, "broken_at": None, "message": "哈希链完整"}


class ShameWall:
    """耻辱墙: 违规记录, 问责追踪。"""

    @staticmethod
    def register(error_type: str, details: dict, severity: str = "HIGH") -> dict:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "severity": severity,
            "dna": generate_dna("SHAME"),
            "details": details,
        }
        with _lock:
            AUDIT_DIR.mkdir(parents=True, exist_ok=True)
            with open(SHAME_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        # 耻辱墙事件同步进审计链, 保证可追溯
        Historian.record("shame_wall_register", entry["dna"],
                         {"type": error_type, "severity": severity})
        return entry

    @staticmethod
    def list_all() -> list:
        if not SHAME_PATH.exists():
            return []
        with open(SHAME_PATH, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]


def require_dna(request_headers, service: str, path: str) -> str:
    """P0 契约: 无 X-Dragon-DNA 头 → 返回 None (调用方应 403), 同时上耻辱墙。
    有头 → 返回 dna 字符串。此检查为审计标记(修正5), 鉴权见 API 网关 /auth/verify。
    """
    dna = request_headers.get("x-dragon-dna")
    if not dna:
        ShameWall.register("P0_DNA_MISSING",
                           {"service": service, "path": path},
                           severity="HIGH")
    return dna


if __name__ == "__main__":
    # 自检: 写3条 → 校验链 → 演示撞库检测
    print("DNA 样例:", generate_dna("SELFTEST"))
    for i in range(3):
        Historian.record("selftest", generate_dna("SELFTEST"), {"seq": i}, service="audit-selftest")
    print("链校验:", json.dumps(Historian.verify_chain(), ensure_ascii=False))
    print("调用方: python3 lh_audit.py  (写 $LONGHUN_AUDIT_DIR 或 /opt/longhun/audit)")
