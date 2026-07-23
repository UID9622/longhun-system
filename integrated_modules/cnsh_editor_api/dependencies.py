#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH Editor API · 依赖与 tier 校验
DNA: #龍芯⚡️2026-07-04-CNSH-API-DEPS-v1.0
"""
from __future__ import annotations

from fastapi import HTTPException, Request

from .config import TierLimits, get_current_tier


def get_tier() -> TierLimits:
    """获取当前 tier 配置"""
    return get_current_tier()


def require_paid(request: Request, tier: TierLimits = get_tier()) -> None:
    """需要付费 tier 的接口调用此依赖"""
    if tier.name != "paid":
        raise HTTPException(
            status_code=403,
            detail=f"当前为 {tier.name} tier，该功能仅在 paid tier（华为云/鲲鹏完整版）开放",
        )


def check_source_length(source: str, tier: TierLimits = get_tier()) -> None:
    """检查代码长度是否超过 tier 限制"""
    if len(source) > tier.max_source_chars:
        raise HTTPException(
            status_code=413,
            detail=(
                f"代码长度 {len(source)} 超过 {tier.name} tier 限制 "
                f"{tier.max_source_chars} 字符"
            ),
        )


def check_execution_timeout(timeout_ms: int, tier: TierLimits = get_tier()) -> int:
    """检查并限制执行超时"""
    if timeout_ms is None or timeout_ms <= 0:
        return tier.max_execution_time_ms
    if timeout_ms > tier.max_execution_time_ms:
        return tier.max_execution_time_ms
    return timeout_ms
