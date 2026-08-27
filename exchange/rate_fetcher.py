#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计链 · 汇率获取模块 v1.1
DNA: #龍芯⚡️2026-08-23-RATE-FETCHER-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

设计原则:
  · 零配置可用（用免费公开API）
  · 四源降级：腾讯 → Frankfurter → ExchangeRate-API → 兜底固定汇率
  · 加密货币通过 CoinGecko 免费接口
  · 本地缓存5分钟，减少外部调用
  · v1.1: 新增腾讯/新浪国内直连源，解决境外API被墙导致的🟡降级
"""

import json, time, urllib.request, urllib.error
from typing import Dict, Optional
from datetime import datetime

# 兜底汇率（API全挂时用，定期人工更新）
FALLBACK_RATES_TO_CNY = {
    "USD": 7.25,
    "EUR": 7.85,
    "JPY": 0.048,
    "GBP": 9.15,
    "HKD": 0.928,
    "SGD": 5.38,
    "THB": 0.207,
    "VND": 0.000290,
    "KRW": 0.00538,
    "AUD": 4.73,
    "CAD": 5.35,
    "CHF": 8.18,
    # 加密货币兜底（相对稳定估值）
    "BTC": 450000.0,
    "ETH": 24000.0,
    "USDT": 7.25,
    "USDC": 7.25,
}

# 内存缓存
_cache: Dict[str, dict] = {}
CACHE_TTL = 300  # 5分钟

def _get(url: str, timeout: int = 5) -> Optional[dict]:
    """通用 HTTP GET，失败返回 None"""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "LonghunAuditChain/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None

def _from_tencent(currency: str) -> Optional[float]:
    """
    国内实时汇率（可直连·无需Key·不上境外）
    首选: 腾讯行情 wh{cur}CNY（qt.gtimg.cn·白名单货币对）
    备用: 新浪财经 fx_s{cur}cny（hq.sinajs.cn·需 Referer）
    仅支持法币，不含加密货币
    """
    if currency in ("BTC", "ETH", "USDT", "USDC"):
        return None
    # 腾讯行情（实测白名单，2026-08-23）
    if currency in ("USD", "EUR", "GBP", "HKD", "SGD", "AUD", "CAD", "CHF", "TWD"):
        url = f"https://qt.gtimg.cn/q=wh{currency}CNY"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                text = resp.read().decode("gbk", errors="ignore")
                if "none_match" not in text and '"' in text:
                    parts = text.split('"')[1].split("~")
                    if len(parts) > 4 and parts[3]:
                        return float(parts[3])  # 第4字段=当前价
        except Exception:
            pass
    # 备用: 新浪财经（买价在 index 5）
    url2 = f"https://hq.sinajs.cn/list=fx_s{currency.lower()}cny"
    try:
        req = urllib.request.Request(
            url2,
            headers={"Referer": "https://finance.sina.com.cn",
                     "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode("gbk", errors="ignore")
            if '="' in text and '""' not in text:
                payload = text.split('="')[1].rstrip('";\n')
                parts = payload.split(",")
                if len(parts) > 5 and parts[5]:
                    return float(parts[5])  # 买价
    except Exception:
        pass
    return None

def _from_frankfurter(currency: str) -> Optional[float]:
    """
    欧洲央行数据，免费无需KEY
    https://api.frankfurter.app/latest?from=USD&to=CNY
    """
    # BTC/ETH不在法币API里
    if currency in ("BTC", "ETH", "USDT", "USDC"):
        return None
    data = _get(f"https://api.frankfurter.app/latest?from={currency}&to=CNY")
    if data and "rates" in data and "CNY" in data["rates"]:
        return float(data["rates"]["CNY"])
    return None

def _from_exchangerate(currency: str) -> Optional[float]:
    """
    ExchangeRate-API 免费端点（无需KEY，每日1500次）
    """
    if currency in ("BTC", "ETH", "USDT", "USDC"):
        return None
    data = _get(f"https://open.er-api.com/v6/latest/{currency}")
    if data and "rates" in data and "CNY" in data["rates"]:
        return float(data["rates"]["CNY"])
    return None

def _from_coingecko(currency: str) -> Optional[float]:
    """
    CoinGecko 免费加密货币价格（CNY计价）
    """
    coin_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "USDT": "tether",
        "USDC": "usd-coin",
    }
    coin_id = coin_map.get(currency)
    if not coin_id:
        return None
    data = _get(
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies=cny"
    )
    if data and coin_id in data and "cny" in data[coin_id]:
        return float(data[coin_id]["cny"])
    return None

def get_rate_to_cny(currency: str) -> dict:
    """
    获取任意货币到 CNY（=eCNY）的汇率
    返回: { rate, source, timestamp, is_fallback }
    """
    currency = currency.upper()
    if currency == "CNY" or currency == "ECNY":
        return {"rate": 1.0, "source": "identity",
                "timestamp": datetime.now().isoformat(), "is_fallback": False}

    # 检查缓存
    cache_key = currency
    cached = _cache.get(cache_key)
    if cached and (time.time() - cached["fetched_at"]) < CACHE_TTL:
        return cached["data"]

    # 三源降级
    rate = None
    source = "fallback"

    if currency in ("BTC", "ETH", "USDT", "USDC"):
        r = _from_coingecko(currency)
        if r:
            rate, source = r, "coingecko"
    else:
        # 法币：腾讯 → Frankfurter → ExchangeRate → 兜底
        r = _from_tencent(currency)
        if r:
            rate, source = r, "tencent"
        else:
            r = _from_frankfurter(currency)
            if r:
                rate, source = r, "frankfurter"
            else:
                r = _from_exchangerate(currency)
                if r:
                    rate, source = r, "exchangerate"

    is_fallback = False
    if rate is None:
        rate = FALLBACK_RATES_TO_CNY.get(currency)
        if rate is None:
            raise ValueError(f"不支持的货币: {currency}")
        source = "fallback"
        is_fallback = True

    result = {
        "rate": rate,
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "is_fallback": is_fallback,
    }
    # 写缓存
    _cache[cache_key] = {"data": result, "fetched_at": time.time()}
    return result
