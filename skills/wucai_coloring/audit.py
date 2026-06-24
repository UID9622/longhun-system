#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂五色审计引擎 v1.0

把 UID9622 的「五色」直觉固化为可执行代码：
看到颜色就知道要做什么。

DNA: #龍芯⚡️2026-06-23-WUCAI-AUDIT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
from __future__ import annotations

import dataclasses
import textwrap
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

CST = timezone(timedelta(hours=8))


@dataclasses.dataclass
class AuditResult:
    color: str          # G / Y / R / K / AU
    color_name: str     # 绿色 / 黄色 / 红色 / 黑色 / 金色
    symbol: str         # 🟢 / 🟡 / 🔴 / ⚫ / 🟡（金）
    R_value: float      # 0.0 - 1.0
    action: str         # 人要执行的动作
    factors: Dict[str, float]
    context: Dict[str, Any]
    dna: str
    timestamp: str

    def to_yaml(self) -> str:
        lines = [
            f"color: {self.color}",
            f"color_name: {self.color_name}",
            f"symbol: {self.symbol}",
            f"R_value: {self.R_value:.4f}",
            f"action: {self.action}",
            "factors:",
        ]
        for k, v in self.factors.items():
            lines.append(f"  {k}: {v:.4f}")
        lines += [
            "context:",
            f"  data_incomplete: {self.context.get('data_incomplete', False)}",
            f"  grey_collision: {self.context.get('grey_collision', False)}",
            f"  blackbox_suspicion: {self.context.get('blackbox_suspicion', False)}",
            f"  fingerprint_fail: {self.context.get('fingerprint_fail', False)}",
            f"  factor_unmeasurable: {self.context.get('factor_unmeasurable', False)}",
            f"  master_confirm_token: {self.context.get('master_confirm_token')}",
            f"dna: {self.dna}",
            f"timestamp: {self.timestamp}",
        ]
        return "\n".join(lines)


# 五色动作表
COLOR_TABLE = {
    "G": {
        "name": "绿色",
        "symbol": "🟢",
        "action": "自动放行 · 留痕",
        "wuxing": "木",
        "direction": "东",
        "meaning": "生长 · 新建",
    },
    "Y": {
        "name": "黄色",
        "symbol": "🟡",
        "action": "二次确认 · 加证据",
        "wuxing": "土",
        "direction": "中",
        "meaning": "承载 · 待补",
    },
    "R": {
        "name": "红色",
        "symbol": "🔴",
        "action": "立即停止 · 上报主控",
        "wuxing": "火",
        "direction": "南",
        "meaning": "熔断 · 决策",
    },
    "K": {
        "name": "黑色",
        "symbol": "⚫",
        "action": "进观察池 · 冻结 24h",
        "wuxing": "水",
        "direction": "北",
        "meaning": "影子 · 静默",
    },
    "AU": {
        "name": "金色",
        "symbol": "🟡",
        "action": "主控签字 · 永存档",
        "wuxing": "金",
        "direction": "西",
        "meaning": "光明 · 主控",
    },
}


def _clamp(v: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, v))


def _compute_R(factors: Dict[str, float]) -> float:
    """
    R = F2 * 0.4 + F6 * 0.4 + F3 * 0.2 - F1 * 0.5 - F5 * 0.3
    """
    F2 = factors.get("sharpness", 0.0)
    F6 = factors.get("long_term", 0.0)
    F3 = factors.get("density", 0.0)
    F1 = factors.get("absence", 0.0)
    F5 = factors.get("pleasing", 0.0)
    r = F2 * 0.4 + F6 * 0.4 + F3 * 0.2 - F1 * 0.5 - F5 * 0.3
    return _clamp(r)


def _check_black(ctx: Dict[str, Any]) -> Optional[str]:
    """任一触发即黑色。"""
    black_triggers = [
        ("data_incomplete", "数据不全"),
        ("factor_unmeasurable", "因子测不准"),
        ("grey_collision", "灰色相遇/五行相克"),
        ("blackbox_suspicion", "黑箱嫌疑"),
        ("fingerprint_fail", "第6重指纹认证失败"),
    ]
    for key, reason in black_triggers:
        if ctx.get(key):
            return reason
    return None


def _check_gold(ctx: Dict[str, Any]) -> Optional[str]:
    """金色：必须含 CONFIRM 徽记 + 至少一条触发条件。"""
    token = ctx.get("master_confirm_token")
    expected = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    if token != expected and token != "#CONFIRM_9622-ONLY-ONCE_LK9X-772Z":
        return None
    gold_conditions = [
        ("involves_minor", "涉及子女"),
        ("sovereignty_redline", "主权红线触碰"),
        ("uncomputable_doubt", "不可算 + 主控有疑虑"),
        ("explicit_gold_request", "老大明确要求金色判决"),
    ]
    for key, reason in gold_conditions:
        if ctx.get(key):
            return reason
    return None


def audit(
    task: str,
    factors: Dict[str, float],
    context: Optional[Dict[str, Any]] = None,
) -> AuditResult:
    """
    执行五色审计。

    Args:
        task: 任务描述（仅用于留痕）
        factors: {sharpness, long_term, density, absence, pleasing}，取值 0~1
        context: 黑色/金色触发条件 + master_confirm_token
    """
    ctx = dict(context or {})
    r = _compute_R(factors)

    # 金色优先
    gold_reason = _check_gold(ctx)
    if gold_reason:
        color = "AU"
    else:
        black_reason = _check_black(ctx)
        if black_reason:
            color = "K"
        elif r < 0.30:
            color = "G"
        elif r < 0.67:
            color = "Y"
        else:
            color = "R"

    info = COLOR_TABLE[color]
    action = info["action"]
    if color == "K":
        action += f"（原因：{black_reason}）"
    elif color == "AU":
        action += f"（原因：{gold_reason}）"

    return AuditResult(
        color=color,
        color_name=info["name"],
        symbol=info["symbol"],
        R_value=r,
        action=action,
        factors=factors,
        context=ctx,
        dna="#龍芯⚡️" + datetime.now(CST).strftime("%Y%m%d%H%M%S") + f"-WUCAI-{task[:20]}",
        timestamp=datetime.now(CST).isoformat(),
    )


def main() -> None:
    print("🐉 龍魂五色审计引擎示例\n")
    samples = [
        {
            "task": "发布公开文章",
            "factors": {"sharpness": 0.5, "long_term": 0.6, "density": 0.4, "absence": 0.3, "pleasing": 0.2},
            "context": {},
        },
        {
            "task": "删除本地备份",
            "factors": {"sharpness": 0.9, "long_term": 0.2, "density": 0.8, "absence": 0.1, "pleasing": 0.0},
            "context": {"grey_collision": True},
        },
        {
            "task": "涉及子女数据出境",
            "factors": {"sharpness": 0.5, "long_term": 0.5, "density": 0.5, "absence": 0.0, "pleasing": 0.0},
            "context": {
                "involves_minor": True,
                "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            },
        },
    ]
    for s in samples:
        res = audit(**s)
        print(f"任务：{s['task']}")
        print(f"颜色：{res.symbol} {res.color_name} ({res.color})  R={res.R_value:.2f}")
        print(f"动作：{res.action}")
        print("-" * 40)
        print(res.to_yaml())
        print()


if __name__ == "__main__":
    main()
