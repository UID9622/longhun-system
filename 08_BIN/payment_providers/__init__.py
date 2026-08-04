#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PAYMENT-PROVIDERS-v1.0
# CREATOR: 诸葛鑫（UID9622）
# 功能: 龍魂激活经济舱 · 支付渠道统一入口

import os
import yaml
from pathlib import Path
from decimal import Decimal
from typing import Optional, Dict, Any


def _load_credentials() -> Dict[str, Any]:
    """加载支付凭证，优先真实配置，其次模板"""
    paths = [
        Path(os.path.expanduser("~/.longhun/config/payment_credentials.yaml")),
        Path(__file__).resolve().parents[2] / "config" / "payment_credentials.yaml",
        Path(__file__).resolve().parents[2] / "config" / "payment_credentials.yaml.example",
    ]
    for p in paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
    return {}


CREDENTIALS = _load_credentials()


def _provider(name: str):
    cfg = CREDENTIALS.get(name, {})
    enabled = bool(cfg.get("enabled", False))
    if not enabled:
        return None
    if name == "wechat_pay":
        from .wechat_pay import WechatPayProvider
        return WechatPayProvider(cfg)
    if name == "alipay":
        from .alipay_pay import AlipayProvider
        return AlipayProvider(cfg)
    return None


def get_payment_provider(prefer: str = "wechat_pay") -> Optional[Any]:
    """获取可用的支付渠道，优先用户指定"""
    for name in [prefer, "wechat_pay", "alipay"]:
        p = _provider(name)
        if p:
            return p
    return None


def list_providers() -> Dict[str, bool]:
    """列出各支付渠道是否可用"""
    return {
        "wechat_pay": bool(CREDENTIALS.get("wechat_pay", {}).get("enabled", False)),
        "alipay": bool(CREDENTIALS.get("alipay", {}).get("enabled", False)),
    }
