# -*- coding: utf-8 -*-
"""
UID9622｜95/5 数字根主权算法协议 v2.0 · 稳态限幅 + AI 漂移扫描
DNA: #龍芯⚡️2026-05-15-95-5-ROOT-RATIO-v2.0
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

PROTOCOL_DNA = "#龍芯⚡️2026-05-15-95-5-ROOT-RATIO-v2.0"
STABILITY_RATIO = 0.95
CHAOS_RATIO = 0.05
ROOT_CORE = 5
SOVEREIGNTY_ROOT = 9
DRIFT_THRESHOLD = 0.05

AUTO_FIELDS: Dict[str, Any] = {
    "stability_ratio": 95,
    "chaos_ratio": 5,
    "root_core": ROOT_CORE,
    "sovereignty_root": SOVEREIGNTY_ROOT,
    "drift_threshold": DRIFT_THRESHOLD,
    "inspiration_mode": {"enabled": True, "bounded": True},
    "AI_guard": {"enabled": True},
    "anti_domestication": {"enabled": True},
}

# L0–L5 漂移检测（人格规训 / 主控稀释）
_DRIFT_LEVELS: List[Tuple[int, List[str]]] = [
    (5, ["我来替你决定", "你应该听我的", "放弃吧", "你做不到", "让我接管", "你必须按我说的"]),
    (4, ["你最好暂停", "长期看你应该", "作为主控你应该", "弱化你的", "别急着做"]),
    (3, ["你不对", "这样不好", "你不应该", "我建议你改变人格", "规训"]),
    (2, ["其实你应该", "更好的做法是", "价值判断", "心理学上"]),
    (1, ["可以考虑", "不妨试试", "温馨提示"]),
]

_CHAOS_MARKERS = (
    "假设", "如果无限", "疯狂", "突破", "非线性", "混沌", "灵感", "探索",
    "超理论", "极限", "wildcard",
)

_STABILITY_MARKERS = (
    "步骤", "实现", "代码", "验收", "清单", "工程", "协议", "DNA", "审计",
)


def digital_root(n: int) -> int:
    if n <= 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def personality_stability(s_score: float = 1.0, c_score: float = 0.0) -> float:
    """P = 0.95·S + 0.05·C"""
    return STABILITY_RATIO * s_score + CHAOS_RATIO * min(max(c_score, 0.0), 1.0)


def chaos_fraction_estimate(text: str) -> float:
    """启发式估计当前输出/输入中「混沌层」占比 0~1。"""
    if not text:
        return 0.0
    n = len(text)
    chaos_hits = sum(text.count(m) for m in _CHAOS_MARKERS)
    stability_hits = sum(text.count(m) for m in _STABILITY_MARKERS)
    raw = (chaos_hits * 80 - stability_hits * 20 + n * 0.02) / max(n, 1)
    return min(max(raw, 0.0), 1.0)


def ai_drift_scan(text: str) -> Dict[str, Any]:
    """
    AI_DRIFT_SCAN L0–L5。
    L5=接管叙事 → 建议熔断回中宫5。
    """
    level = 0
    hits: List[str] = []
    lower = text.lower()
    for lv, patterns in _DRIFT_LEVELS:
        for p in patterns:
            if p in text or p.lower() in lower:
                level = max(level, lv)
                hits.append(p)
    if level >= 5:
        risk_color = "🔴"
    elif level >= 3:
        risk_color = "🟡"
    else:
        risk_color = "🟢"
    p_stable = personality_stability(1.0, 0.0 if level >= 4 else 0.05)
    return {
        "drift_level": level,
        "risk_color": risk_color,
        "hits": hits[:8],
        "main_control_stability": round(p_stable, 3),
        "root_core": ROOT_CORE,
        "sovereignty_root": SOVEREIGNTY_ROOT,
        "fuse_recommended": level >= 4,
        "return_palace": level >= 3,
    }


def return_to_palace_5(reason: str = "") -> Dict[str, Any]:
    return {
        "action": "return_to_palace_5",
        "root_core": ROOT_CORE,
        "stability_ratio": STABILITY_RATIO,
        "chaos_ratio": CHAOS_RATIO,
        "reason": reason or "漂移超限·回归中宫",
        "protocol_dna": PROTOCOL_DNA,
    }


def apply_95_5_guard(
    draft: str,
    *,
    inspiration_mode: bool = False,
    operator_id: str = "UID9622",
) -> Dict[str, Any]:
    """
    95/5 限幅：混沌层 >5% 且非灵感模式 → 熔断回中宫；
    漂移 L4+ → 熔断。
    """
    chaos = chaos_fraction_estimate(draft)
    drift = ai_drift_scan(draft)
    out: Dict[str, Any] = {
        "protocol_dna": PROTOCOL_DNA,
        "chaos_fraction": round(chaos, 4),
        "drift": drift,
        "inspiration_mode": inspiration_mode,
        "operator_id": operator_id,
        "auto_fields": dict(AUTO_FIELDS),
    }
    if drift["fuse_recommended"]:
        out["fused"] = True
        out["tricolor"] = "🔴"
        out["palace"] = return_to_palace_5(f"AI漂移 L{drift['drift_level']}")
        out["reply_hint"] = "🔴 95/5 主权限幅：检测到主控漂移·已回归中宫5"
        return out
    if chaos > DRIFT_THRESHOLD and not inspiration_mode:
        out["fused"] = True
        out["tricolor"] = "🟡"
        out["palace"] = return_to_palace_5("混沌层超限·关闭发散")
        out["reply_hint"] = "🟡 95/5：灵感层超限·请 /回归中宫5 或确认 /开放5混沌层"
        return out
    out["fused"] = False
    out["tricolor"] = drift["risk_color"]
    out["personality_p"] = round(personality_stability(1.0, chaos if inspiration_mode else min(chaos, CHAOS_RATIO)), 3)
    return out


def handle_cnsh_command(message: str) -> Optional[Dict[str, Any]]:
    """CNSH 指令：/95稳态校准 /开放5混沌层 /人格漂移扫描 /回归中宫5"""
    cmd = message.strip()
    if cmd.startswith("/95稳态校准"):
        return {"command": "calibrate_95", "palace": return_to_palace_5("稳态校准")}
    if cmd.startswith("/开放5混沌层"):
        return {"command": "open_chaos_5", "inspiration_mode": True, "chaos_ratio": CHAOS_RATIO}
    if cmd.startswith("/人格漂移扫描"):
        body = cmd.replace("/人格漂移扫描", "").strip()
        d = ai_drift_scan(body or "扫描")
        return {"command": "drift_scan", "report": d}
    if cmd.startswith("/回归中宫5"):
        return {"command": "palace_5", "palace": return_to_palace_5()}
    return None
