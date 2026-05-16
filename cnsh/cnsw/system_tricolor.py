# -*- coding: utf-8 -*-
"""
CNSW × 流场 × P05 对齐层 — 工程用「三闸」口径（🟢🟡🔴）

Notion「上帝之眼·64卦审计算法」P05 是全量指标体系；本仓 **实时链** 以：
  - cnsw：围猎钩子 drift_level + sovereignty_score
  - gate_v3：数字根 dr 语义（3/9🔴·6🟡）
为准。此处把 CNSW 的 🟠（L3）**并入 🟡**，与同一条流场语义对齐，避免橙/黄双轨。

DNA: #龍芯⚡️2026-05-16-CNSW-SYSTEM-TRICOLOR-v1.0
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .registry import tri_color_for_level

_LEVEL_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}


def worst_drift_level(levels: List[str]) -> str:
    if not levels:
        return "L0"
    return max(levels, key=lambda x: _LEVEL_ORDER.get(x, 0))


def flow_tricolor(drift_level: str) -> str:
    """
    与 gate_v3 / flow_port 家族一致的三色（仅 🟢🟡🔴）。
    L4/L5 → 🔴；L2/L3 → 🟡；L0/L1 → 🟢。
    """
    if drift_level in ("L4", "L5"):
        return "🔴"
    if drift_level in ("L2", "L3"):
        return "🟡"
    return "🟢"


def engineering_tricolor(drift_level: str, sovereignty_score: int) -> Dict[str, Any]:
    """
    鲁班工程链判定：是否允许「自动本地提交」等高危动作。

    commit_allowed：仅当 flow 为 🟢（即 L0/L1）且主权分仍达 L1 门槛（≥75）。
    """
    fl = flow_tricolor(drift_level)
    cnsw = tri_color_for_level(drift_level)
    # 分数与 level 偶有边界浮动：双锚更稳
    score_ok = sovereignty_score >= 75
    commit_ok = fl == "🟢" and score_ok and drift_level in ("L0", "L1")
    return {
        "flow_tricolor": fl,
        "cnsw_tricolor": cnsw,
        "drift_level": drift_level,
        "sovereignty_score": sovereignty_score,
        "commit_allowed": commit_ok,
        "p05_lane": (
            "简并：围猎 drift × 主权分；全量指标见 Notion。总索引（分层导航）"
            "https://www.notion.so/dcb73d6fbff9409a98780964bcbc3e30 — "
            "仅作图谱入口，正文与可执行定义以本仓为准，有界迭代。"
        ),
    }


def aggregate_engineering_from_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """批量审计后汇总最坏 drift + 对应工程三色。"""
    if not rows:
        return engineering_tricolor("L0", 100)
    levels = [str(r.get("drift_level") or "L0") for r in rows]
    scores = [int(r.get("sovereignty_score") or 0) for r in rows]
    worst = worst_drift_level(levels)
    worst_row_score = min(scores) if scores else 0
    base = engineering_tricolor(worst, worst_row_score)
    base["rounds"] = len(rows)
    base["worst_drift_level"] = worst
    base["min_sovereignty_score"] = worst_row_score
    return base


def combine_gate_dr(*, flow: str, gate_dr_color: str) -> Tuple[str, bool]:
    """
    gate_v3 对「提交说明」的数字根色与原 CNSW flow 合并，取最严（与 engine.overall_color 同构）。
    """
    colors = [flow, gate_dr_color]
    if "🔴" in colors:
        return "🔴", False
    if "🟡" in colors:
        return "🟡", False
    return "🟢", True
