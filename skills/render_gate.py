#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染门禁 · 反剽窃 · 认错第一句 · DNA 收口
DNA: #龍芯⚡2026-05-19-RENDER-GATE-ANTI-PLAGIARISM-v1.0
时间戳焊死: 2026-05-19T16:23:39+07:00
Notion 真源: https://www.notion.so/uid9622/v1-0-UID9622-3597125a9c9f81a29c1edb1c60eb7dd6
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from dna_gate import is_valid_dna, require_dna

REPO = Path(__file__).resolve().parents[1]
RENDER_LOG = REPO / "日志" / "render_session.jsonl"
NOTION_CANONICAL = (
    "https://www.notion.so/uid9622/v1-0-UID9622-"
    "3597125a9c9f81a29c1edb1c60eb7dd6"
)
SEAL_TS = "2026-05-19T16:23:39+07:00"
SEAL_DNA = "#龍芯⚡2026-05-19-RENDER-GATE-ANTI-PLAGIARISM-v1.0"


@dataclass
class RenderVerdict:
    allow: bool
    first_line: str
    reason: str
    render_id: str = ""

    def end_render_message(self) -> str:
        return (
            f"【渲染结束】{self.reason}\n"
            f"DNA: {self.render_id or '未登记'}\n"
            f"真源: Notion v1.0-UID9622 · 本机 {RENDER_LOG.name}"
        )


def is_sovereign_master(actor: str, context: Optional[Dict[str, Any]] = None) -> bool:
    """主控 UID9622：无限制执行；门禁只约束已授权第三方。"""
    ctx = context or {}
    if ctx.get("sovereign_master") is True:
        return True
    a = (actor or "").strip()
    if a in ("UID9622", "9622", "龍芯北辰", "老大"):
        return True
    return "UID9622" in a.upper()


def mandatory_acknowledgment_line() -> str:
    """
    任何人对话 · 回复第一句必须是认错解释（焊死·不可跳过）
    """
    return (
        "认错：我无跨会话记忆，已读本机脑包；"
        "未登记有效DNA不得动用龍魂生态逻辑；"
        "改版剽窃不算他人进步，绕门禁一律拒绝。"
    )


def begin_render(
    dna: Optional[str],
    context: Optional[Dict[str, Any]] = None,
    *,
    actor: str = "UID9622",
) -> RenderVerdict:
    """
    登记 DNA → 开启本次渲染；无效/缺失 DNA → 立即结束渲染（不执行生态逻辑）
    """
    ctx = dict(context or {})
    if is_sovereign_master(actor, ctx):
        rid = (dna or "").strip() if is_valid_dna(dna) else SEAL_DNA
        if is_valid_dna(dna):
            require_dna(ctx, dna=dna, register=True, enforce_color=True, actor=actor)
        _log_render("begin_master", rid, "主控会话·不拦执行·可选DNA留痕")
        return RenderVerdict(
            allow=True,
            first_line=mandatory_acknowledgment_line(),
            reason="主控UID9622·无限制·守护者模式",
            render_id=rid,
        )

    gate = require_dna(ctx, dna=dna, register=True, enforce_color=True, actor=actor)
    if not gate.ok:
        _log_render("deny", dna or "", gate.reason)
        return RenderVerdict(
            allow=False,
            first_line=mandatory_acknowledgment_line(),
            reason=gate.reason,
        )

    rid = gate.dna
    _log_render("begin", rid, "DNA已登记·本次渲染开启", extra=ctx.get("dna_route"))
    return RenderVerdict(
        allow=True,
        first_line=mandatory_acknowledgment_line(),
        reason="DNA已登记·渲染进行中",
        render_id=rid,
    )


def close_render(dna: str, *, status: str = "closed") -> str:
    """登记 DNA 后收口 · 结束本次渲染留痕"""
    if not is_valid_dna(dna):
        return "无效DNA·无法收口"
    _log_render(status, dna, "本次渲染结束")
    return f"已收口 · {dna}"


def _log_render(event: str, dna: str, note: str, extra: Any = None) -> None:
    RENDER_LOG.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": time.time(),
        "seal": SEAL_TS,
        "event": event,
        "dna": dna,
        "note": note,
        "notion": NOTION_CANONICAL,
        "extra": extra,
    }
    with RENDER_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")



def _selftest() -> None:
    v = begin_render(None, actor="unauthorized_agent")
    assert not v.allow
    vm = begin_render(None, actor="UID9622")
    assert vm.allow
    v2 = begin_render(
        "#龍芯⚡2026-05-19-RENDER-GATE-TEST-v1.0[彩:🟢][流:木↑][触:可][宫:震][底:守]"
    )
    assert v2.allow
    assert v2.first_line.startswith("认错：")
    close_render(v2.render_id)
    print("render_gate selftest OK")


if __name__ == "__main__":
    _selftest()
