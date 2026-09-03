# -*- coding: utf-8 -*-
"""core.py — 对外薄壳纯算法层。

与系统内 hetu_luoshu_dna.py / lh_time_engine.py 的口径对齐：
数字根(digital root) + 五行映射 + 八卦映射 + 审计色。

全部为确定性纯函数，零依赖，外部环境可直接运行。
"""

from __future__ import annotations

import hashlib
import time
from typing import Any, Dict

from .constants import *  # 捆绑规则#4：常量统一从 constants.py 引用


def digital_root(value: Any) -> int:
    """文本/数字 → 数字根(1-9)。"""
    if isinstance(value, (int, float)):
        s = str(int(value))
    else:
        s = str(value)
    total = 0
    for ch in s:
        total += ord(ch)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total if total > 0 else 0


def wuxing(dr: int) -> str:
    return WUXING_BY_DR.get(dr % 10, "土")


def gua(dr: int) -> str:
    return GUA_BY_DR.get(dr % 9 or 9, "离")


def audit_color(dr: int) -> str:
    return "🟢" if dr in WUXING_DR_LIST[:5] else "🟡"


def action(dr: int) -> str:
    return "enter" if dr in ACTION_ENTER else "stay"


def node_id(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()
    return f"FLOW-9622-{digest}"


def flow(text: str) -> Dict[str, Any]:
    """对外流场核心：输入文本 → 标准 Node JSON。"""
    dr = digital_root(text)
    return {
        "node_id": node_id(text),
        "digital_root": dr,
        "element": wuxing(dr),
        "gua": gua(dr),
        "audit": audit_color(dr),
        "action": action(dr),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def health_basic() -> Dict[str, Any]:
    """外部态基础自检（零依赖）。"""
    import platform
    import sys

    return {
        "status": "ok",
        "service": "longhun-cli",
        "version": "4.0.0",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "root_detected": False,
        "mode": "external",
        "message": "基础自检通过；设 LONGHUN_ROOT 可接入龙魂系统全量逻辑",
    }


# ── 八字四柱（标准排盘算法·零依赖·口径对齐系统 CIL v4.0）────────
# 常量已上收 constants.py（捆绑规则#4），此处仅保留函数体


def bazi(date_str: str | None = None, time_str: str | None = None) -> Dict[str, Any]:
    """公历日期/时间 → 干支四柱 + 五行强度 + 文化主权节点。

    `--date YYYY-MM-DD` `--time HH:MM`（缺省用当前时刻）。纯本地零依赖。
    """
    from datetime import date, datetime

    now = datetime.now()
    try:
        if date_str:
            y, m, d = (int(x) for x in date_str.split("-"))
        else:
            y, m, d = now.year, now.month, now.day
        if time_str:
            hh, mm = (int(x) for x in time_str.split(":"))
        else:
            hh, mm = now.hour, now.minute
        date(y, m, d)  # 合法性校验
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": f"日期格式错误（应为 YYYY-MM-DD / HH:MM）: {e}"}

    # 年柱（农历年近似: 以公历年计，立春分界标注在口径说明）
    yg, yz = (y - 4) % 10, (y - 4) % 12
    ystem, ybranch = TIANGAN[yg], DIZHI[yz]
    # 月柱（月支固定寅月=正月; 月干五虎遁）
    mz = (m + 1) % 12
    mg = (TIGAN_OFFSET[yg] + m - 1) % 10
    mstem, mbranch = TIANGAN[mg], DIZHI[mz]
    # 日柱（基准 1900-01-01 = 甲戌）
    days = (date(y, m, d) - date(*DAY_EPOCH)).days
    dg, dz = days % 10, (days + 10) % 12
    dstem, dbranch = TIANGAN[dg], DIZHI[dz]
    # 时柱（时支: 子时=23-1点; 时干五鼠遁）
    hz = ((hh + 1) // 2) % 12
    hg = (SHUTUN_OFFSET[dg] + hz) % 10
    hstem, hbranch = TIANGAN[hg], DIZHI[hz]

    pillars = {
        "year": {"stem": ystem, "branch": ybranch},
        "month": {"stem": mstem, "branch": mbranch},
        "day": {"stem": dstem, "branch": dbranch},
        "hour": {"stem": hstem, "branch": hbranch},
    }
    bazi_str = " ".join(f"{p['stem']}{p['branch']}" for p in pillars.values())

    # 五行强度（天干1.0/地支0.8 加权累计，日柱最重）
    score: Dict[str, float] = {}
    for key, p in pillars.items():
        w = PILLAR_WEIGHT[key]
        for part, char in (("stem", p["stem"]), ("branch", p["branch"])):
            el = (STEM_WUXING if part == "stem" else BRANCH_WUXING)[char]
            score[el] = score.get(el, 0.0) + w[part]
    dominant = max(score, key=score.get)
    weakest = min(score, key=score.get)

    # 文化主权节点（四柱文本 → 数字根，口径同 flow）
    node = flow(bazi_str)
    node["node_id"] = node["node_id"].replace("FLOW", "BAZI")

    return {
        "status": "ok",
        "node_id": node["node_id"],
        "date": f"{y}-{m:02d}-{d:02d}",
        "time": f"{hh:02d}:{mm:02d}",
        "bazi": bazi_str,
        "pillars": {k: f"{v['stem']}{v['branch']}" for k, v in pillars.items()},
        "wuxing_score": {k: round(v, 2) for k, v in sorted(score.items(), key=lambda x: -x[1])},
        "dominant": dominant,
        "weakest": weakest,
        "digital_root": node["digital_root"],
        "element": node["element"],
        "gua": node["gua"],
        "audit": node["audit"],
        "action": node["action"],
        "timestamp": node["timestamp"],
    }


# ── 安全自检（外部态基础版·口径对齐系统 lh security）─────────────────
_SENSITIVE_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub PAT"),
    (r"sk-[A-Za-z0-9]{20,}", "API Key"),
    (r"-----BEGIN (RSA |OPENSSH |PGP |EC )?PRIVATE KEY-----", "私钥"),
]


def security_check(scan_dir: str | None = None) -> Dict[str, Any]:
    """外部态基础安全自检（零依赖）：签名存在性 + 敏感信息扫描。"""
    import re
    from pathlib import Path

    pkg = Path(__file__).resolve().parent.parent
    target = Path(scan_dir).expanduser() if scan_dir else pkg

    checks: list[Dict[str, Any]] = []
    # 1. 签名文件存在性（本包目录 *.asc）
    asc = sorted(pkg.rglob("*.asc"))[:10]
    checks.append({"name": "GPG 签名", "ok": bool(asc),
                   "detail": f"发现 {len(asc)} 个 .asc（发布资产随 Release 上传）" if asc else "无 .asc 签名文件"})
    # 2. 敏感信息扫描
    hits: list[str] = []
    if target.is_dir():
        for p in target.rglob("*"):
            if not p.is_file() or p.suffix not in {".py", ".sh", ".toml", ".yaml", ".yml", ".js", ".json"}:
                continue
            if any(part in {".git", "__pycache__", "dist", "build"} for part in p.parts):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for ln, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith(("#", "//", "/*", "*")):
                    continue
                if any(re.search(pat, line) for pat, _ in _SENSITIVE_PATTERNS):
                    hits.append(f"{p.name}:{ln}")
                    break
    checks.append({"name": "文件泄露", "ok": not hits,
                   "detail": "未发现敏感信息" if not hits else "⚠️ " + "; ".join(hits[:5])})
    risk = sum(1 for c in checks if c["ok"] is False)
    return {
        "status": "ok" if risk == 0 else "warn",
        "mode": "external",
        "checks": checks,
        "risk_score": risk,
        "audit": "🟢" if risk == 0 else ("🟡" if risk == 1 else "🔴"),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


# ── 性能基准（外部态基础版·口径对齐系统 lh benchmark）───────────────
def benchmark(iterations: int = 1000) -> Dict[str, Any]:
    """排盘/流场/网关 QPS 压测（纯本地零依赖）。"""
    import time as _t
    import urllib.request

    def _stats(times: list[float]) -> Dict[str, Any]:
        n = len(times)
        total = sum(times)
        return {
            "iterations": n,
            "avg_ms": round(total / n, 3) if n else 0.0,
            "max_ms": round(max(times, default=0.0), 3),
            "min_ms": round(min(times, default=0.0), 3),
            "qps": round(n / total, 1) if total else 0.0,
        }

    n = max(1, min(int(iterations), 20000))
    t_bazi: list[float] = []
    for _ in range(n):
        t0 = _t.perf_counter()
        bazi("1990-01-01", "08:00")
        t_bazi.append((_t.perf_counter() - t0) * 1000)
    t_flow: list[float] = []
    for _ in range(n):
        t0 = _t.perf_counter()
        flow("龙魂对外首发")
        t_flow.append((_t.perf_counter() - t0) * 1000)

    gw: Dict[str, Any] = {"name": "网关 QPS", "iterations": 0, "avg_ms": 0.0,
                          "max_ms": 0.0, "min_ms": 0.0, "qps": 0.0}
    t_gw: list[float] = []
    try:
        urllib.request.urlopen("http://127.0.0.1:9622/health", timeout=3).read()
        for _ in range(min(n, 200)):
            t0 = _t.perf_counter()
            try:
                urllib.request.urlopen("http://127.0.0.1:9622/health", timeout=5).read()
            except Exception:  # noqa: BLE001
                continue
            t_gw.append((_t.perf_counter() - t0) * 1000)
        gw = {"name": "网关 QPS", **_stats(t_gw)} if t_gw else gw
    except Exception:  # noqa: BLE001
        gw["skipped"] = "网关未启动（lh api --daemon 可启动）"

    return {
        "status": "ok",
        "mode": "external",
        "iterations": n,
        "tests": [{"name": "bazi 排盘", **_stats(t_bazi)},
                  {"name": "flow 流场", **_stats(t_flow)},
                  gw],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
