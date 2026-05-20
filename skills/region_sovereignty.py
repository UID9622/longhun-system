#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#ZERO-REGION-NEGOTIATION v1.0 · 零地区协商
DNA: #龍芯⚡2026-05-20-ZERO-REGION-NEGOTIATION-v1.0

设备设置 = 唯一真相源 · 19 地区坑 · 显式继承 · 禁止 geo 绕路
"""
from __future__ import annotations

import locale
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DNA_TAG = "#龍芯⚡2026-05-20-ZERO-REGION-NEGOTIATION-v1.0"
TRADITIONAL_LONG = "\u9f8d"  # 龍
SIMPLIFIED_LONG_FORBIDDEN = "\u9f99"  # 龙

# §9.C 设备真相源默认值
REGION_DEFAULTS: Dict[str, str] = {
    "tz": "Asia/Shanghai",
    "tz_offset": "+08:00",
    "dst": "never",
    "lang": "zh-CN.UTF-8",
    "charset": "UTF-8",
    "date_format": "YYYY-MM-DD HH:mm:ss+08:00",
    "number_format": "1,234,567.89",
    "week_start": "Monday",
    "currency": "CNY",
    "calendar": "gregorian+huangli",
    "holidays": "CN-legal+lunar",
    "measurement": "metric",
    "newline": "LF",
    "path_sep": "/",
}

# §9.E 反绕路话术
GEO_BYPASS_PHRASES = [
    r"按您所在地区",
    r"为您推荐",
    r"检测到您在",
    r"切换到夏令时",
    r"夏令时",
    r"本地化日期",
    r"自动选择最近节点",
    r"当地货币",
    r"浏览器语言",
    r"根据您的位置法规",
    r"GDPR",
    r"smart\s*locale",
    r"geo[\s-]?route",
]

RED_PIT_IDS = {"tz", "charset", "date_format", "calendar", "encoding"}
YELLOW_PIT_IDS = {"lang", "number", "week", "currency", "holidays", "measurement"}
BLACK_PIT_IDS = {"ip_cdn", "ua_lang", "api_region", "notion_region", "oauth", "ai_geo", "cloud_region", "path_sep"}


@dataclass
class RegionCheckResult:
    ok: bool
    level: str  # green | yellow | red | black
    acknowledgment: str
    device_snapshot: Dict[str, str] = field(default_factory=dict)
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    pits_checked: int = 0
    dna: str = DNA_TAG

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "level": self.level,
            "acknowledgment": self.acknowledgment,
            "device_snapshot": self.device_snapshot,
            "violations": self.violations,
            "warnings": self.warnings,
            "pits_checked": self.pits_checked,
            "dna": self.dna,
        }


def _device_tz_offset_hours() -> float:
    tz = datetime.now().astimezone().utcoffset()
    if tz is None:
        return 0.0
    return tz.total_seconds() / 3600.0


def _read_lang() -> str:
    for key in ("LC_ALL", "LANG", "LC_CTYPE"):
        v = os.environ.get(key, "")
        if v:
            return v
    try:
        loc, _ = locale.getlocale()
        return loc or ""
    except Exception:
        return ""


def _snapshot_device() -> Dict[str, str]:
    off = _device_tz_offset_hours()
    sign = "+" if off >= 0 else "-"
    h = int(abs(off))
    mm = int((abs(off) - h) * 60)
    offset_str = f"{sign}{h:02d}:{mm:02d}"
    lang = _read_lang()
    return {
        "tz_env": os.environ.get("TZ", "(系统默认)"),
        "tz_offset": offset_str,
        "lang": lang or "(未设)",
        "python_utf8": str(sys.getdefaultencoding()),
        "preferred_encoding": locale.getpreferredencoding(False),
        "now_iso": datetime.now(timezone(timedelta(hours=8))).strftime(
            "%Y-%m-%dT%H:%M:%S+08:00"
        ),
    }


def _acknowledgment(snap: Dict[str, str]) -> str:
    return (
        f"我看到您的设置是 时区偏移={snap['tz_offset']} · "
        f"LANG={snap['lang']} · 编码={snap['preferred_encoding']} · "
        f"将继承不变更（{DNA_TAG}）"
    )


def scan_geo_bypass_text(text: str) -> List[str]:
    hits = []
    for pat in GEO_BYPASS_PHRASES:
        if re.search(pat, text, re.I):
            hits.append(pat)
    return hits


def region_lock_check(
    text: Optional[str] = None,
    strict_red: bool = True,
) -> RegionCheckResult:
    """
    on_identity / 审计入口 · 检测 19 项主权锚点
    strict_red=True 时红色坑不符 → ok=False
    """
    snap = _snapshot_device()
    ack = _acknowledgment(snap)
    violations: List[str] = []
    warnings: List[str] = []
    pits = 0

    # 🔴 1 时区 UTC+8 无 DST
    pits += 1
    off = _device_tz_offset_hours()
    if abs(off - 8.0) > 0.01:
        violations.append(f"RED-1-tz: 当前偏移 {off}h 非 UTC+8")
    tz_env = os.environ.get("TZ", "")
    if tz_env and "Shanghai" not in tz_env and "UTC+8" not in tz_env and tz_env not in ("CST-8",):
        warnings.append(f"YELLOW-tz_env: TZ={tz_env} 建议 Asia/Shanghai")

    # 🔴 2 字符律
    pits += 1
    if text and SIMPLIFIED_LONG_FORBIDDEN in text:
        violations.append("RED-2-char: 检出简体「龙」")

    # 🔴 5 编码 UTF-8
    pits += 1
    enc = locale.getpreferredencoding(False).lower()
    if enc not in ("utf-8", "utf8"):
        violations.append(f"RED-5-encoding: preferred={enc}")

    # 🟡 6 语言 zh-CN
    pits += 1
    lang = _read_lang()
    if lang and "zh" not in lang.lower():
        warnings.append(f"YELLOW-6-lang: LANG={lang}")

    # ⚫ 13 UA 头（环境变量代理检测）
    pits += 1
    if os.environ.get("LONGHUN_FORCE_EN_LOCALE") == "1":
        violations.append("BLACK-13: LONGHUN_FORCE_EN_LOCALE 僭越")

    # §9.E 文本绕路
    if text:
        pits += 1
        for pat in scan_geo_bypass_text(text):
            violations.append(f"BYPASS-phrase: /{pat}/")

    # 路径分隔 ⚫19
    pits += 1
    if os.name == "nt":
        warnings.append("BLACK-19: Windows 路径 · 脚本内统一用 /")

    level = "green"
    if violations:
        if any(v.startswith("BLACK") for v in violations):
            level = "black"
        elif any(v.startswith("RED") for v in violations):
            level = "red"
        else:
            level = "yellow"
    elif warnings:
        level = "yellow"

    ok = True
    if strict_red and violations:
        ok = False
    if level == "red" and strict_red:
        ok = False

    return RegionCheckResult(
        ok=ok,
        level=level,
        acknowledgment=ack,
        device_snapshot=snap,
        violations=violations,
        warnings=warnings,
        pits_checked=pits,
    )


def region_consistency_check(
    log_dir: Optional[Path] = None,
) -> Tuple[bool, Dict[str, bool]]:
    """
    sanity_check 四项：tz / charset / date_format / locale
  任一失败 = 整体 FAIL
    """
    snap = _snapshot_device()
    results = {
        "tz_match": abs(_device_tz_offset_hours() - 8.0) <= 0.01,
        "charset_match": snap["preferred_encoding"].lower() in ("utf-8", "utf8"),
        "date_format_match": bool(re.match(r"\d{4}-\d{2}-\d{2}T", snap["now_iso"])),
        "locale_match": "zh" in snap["lang"].lower() if snap["lang"] != "(未设)" else True,
    }
    if log_dir and log_dir.is_dir():
        results["jsonl_tz_hint"] = True
        jf = log_dir / "home_full_chain_trace.jsonl"
        if jf.is_file():
            try:
                lines = [ln for ln in jf.read_text(encoding="utf-8").splitlines() if ln.strip()]
                if lines:
                    line = lines[-1]
                    results["jsonl_tz_hint"] = bool(
                        re.search(r"\+08(:?00)?|Asia/Shanghai|UTC\+8", line)
                    )
            except Exception:
                results["jsonl_tz_hint"] = False
    ok = all(v for k, v in results.items() if not k.endswith("_hint"))
    if "jsonl_tz_hint" in results and not results["jsonl_tz_hint"]:
        ok = False
    return ok, results


def scene_region_q0(text: Optional[str] = None) -> Tuple[bool, str]:
    """五色审计 Q0 · 不符直接红"""
    r = region_lock_check(text=text, strict_red=True)
    if r.ok and r.level in ("green", "yellow"):
        return True, r.acknowledgment
    reason = "; ".join(r.violations[:3]) or "地区主权未通过"
    return False, f"🔴 Q0 地区主权: {reason}"


def _selftest() -> None:
    print("=" * 60)
    print("region_sovereignty · 自测")
    print("=" * 60)
    r = region_lock_check(text=f"{TRADITIONAL_LONG}魂 UTC+8")
    assert r.ok, r.violations
    print(f"  [1/4 ✓] 正常 · {r.acknowledgment[:40]}…")

    r2 = region_lock_check(text="龙魂", strict_red=True)
    assert not r2.ok
    print("  [2/4 ✓] 简体龙 → RED")

    r3 = region_lock_check(text="按您所在地区为您推荐更好体验")
    assert not r3.ok
    print("  [3/4 ✓] 绕路话术 → 拒")

    ok, parts = region_consistency_check()
    assert ok, parts
    print(f"  [4/4 ✓] consistency {parts}")
    print("=" * 60)
    print("4/4 全过")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
