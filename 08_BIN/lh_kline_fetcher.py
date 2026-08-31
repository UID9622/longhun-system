#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 K线 数据采集器 v1.0
DNA: #龍芯⚡️2026-08-31-KLINE-FETCHER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 真实数据多源采集（新浪A股日K · 币安加密K线 · Alpha Vantage 美股）
数据真实性: 全部来自公开行情接口，零造假；无 Key 时 A股/加密 开箱即用
"""

import json
import os
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request

# ─── 配置 ───
CACHE_DIR = Path.home() / ".longhun" / "kline_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL = 55  # 秒：缓存有效期（新浪快照接口限频）

# Alpha Vantage Key（可选）：优先环境变量，不硬编码密钥
# 注册: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "").strip()

# 默认行情池：A股(新浪·零配置) + 加密(币安·零配置) + 美股(需 AlphaVantage Key)
DEFAULT_SYMBOLS = {
    # ── A股 · 新浪 · 零配置真实日K ──
    "sh600036": {"name": "招商银行", "exchange": "上交所·SSE"},
    "sh600519": {"name": "贵州茅台", "exchange": "上交所·SSE"},
    "sz000001": {"name": "平安银行", "exchange": "深交所·SZSE"},
    "sz300750": {"name": "宁德时代", "exchange": "深交所·SZSE"},
    "sh601318": {"name": "中国平安", "exchange": "上交所·SSE"},
    # ── 加密货币 · 币安 · 零配置真实K线 ──
    "BTCUSDT": {"name": "Bitcoin 比特币", "exchange": "Binance·CRYPTO"},
    "ETHUSDT": {"name": "Ethereum 以太坊", "exchange": "Binance·CRYPTO"},
    # ── 美股 · Alpha Vantage · 需配置 Key ──
    "AAPL": {"name": "Apple Inc.", "exchange": "NASDAQ·美股(需Key)"},
    "TSLA": {"name": "Tesla Inc.", "exchange": "NASDAQ·美股(需Key)"},
}

UA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Referer": "https://finance.sina.com.cn/",
}


def _http_json(url: str, headers: Optional[Dict] = None, timeout: int = 8):
    """HTTP GET → JSON（urllib，零三方依赖）"""
    req = urllib.request.Request(url, headers=headers or UA_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    # 新浪接口偶发 BOM/空白前缀
    return json.loads(raw.lstrip("\ufeff \r\n\t"))


def _price(x: str, default: float = 0.0) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


class KLineFetcher:
    """K线数据采集器：新浪(A股) · 币安(加密) · AlphaVantage(美股) 三源真实数据"""

    def __init__(self):
        self.cache: Dict = {}
        self.cache_ts: Dict[str, float] = {}
        self.lock = threading.Lock()
        self._load_cache()

    # ── 缓存 ──
    def _load_cache(self):
        cache_file = CACHE_DIR / "kline_cache.json"
        try:
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
        except Exception:
            self.cache = {}

    def _save_cache(self):
        try:
            with open(CACHE_DIR / "kline_cache.json", "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False)
        except Exception:
            pass

    def _cache_get(self, symbol: str) -> Optional[Dict]:
        with self.lock:
            ts = self.cache_ts.get(symbol, 0)
            if time.time() - ts < CACHE_TTL and symbol in self.cache:
                return self.cache[symbol]
            return None

    def _cache_put(self, symbol: str, data: Dict):
        with self.lock:
            self.cache[symbol] = data
            self.cache_ts[symbol] = time.time()
            self._save_cache()

    # ── 数据源1 · 新浪 A股（真实日K历史·零配置） ──
    def fetch_sina(self, symbol: str, datalen: int = 100) -> Optional[Dict]:
        """新浪财经 K线接口：getKLineData 真实历史日K
        scale=240 → 日线；datalen 最大约 1023 根"""
        url = (
            "https://quotes.sina.cn/cn/api/json_v2.php/"
            f"CN_MarketDataService.getKLineData?symbol={symbol}"
            f"&scale=240&ma=no&datalen={datalen}"
        )
        rows = _http_json(url, timeout=8)
        if not isinstance(rows, list) or not rows:
            return None
        data = [
            {
                "date": r["day"],
                "open": _price(r.get("open")),
                "high": _price(r.get("high")),
                "low": _price(r.get("low")),
                "close": _price(r.get("close")),
                "volume": _price(r.get("volume")),
            }
            for r in rows
        ]
        return {
            "symbol": symbol,
            "source": "新浪财经·真实日K",
            "last_updated": datetime.now().isoformat(),
            "data": data[-100:],
        }

    # ── 数据源2 · 币安 加密（真实K线·零配置） ──
    def fetch_binance(self, symbol: str, interval: str = "1d") -> Optional[Dict]:
        """币安公开 K线接口：BTCUSDT/ETHUSDT 等真实K线
        双通道: urllib 直连优先 → 失败降级 curl（本地 TLS 指纹被重置时 curl 可通）"""
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        rows = None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA_HEADERS["User-Agent"]})
            with urllib.request.urlopen(req, timeout=8) as resp:
                rows = json.loads(resp.read().decode("utf-8", errors="replace"))
        except Exception:
            rows = None
        if not rows:
            try:
                proc = subprocess.run(
                    ["curl", "-s", "--max-time", "8", url],
                    capture_output=True, text=True, timeout=10,
                )
                rows = json.loads(proc.stdout)
            except Exception:
                rows = None
        if not isinstance(rows, list) or not rows:
            return None
        data = []
        for c in rows:
            data.append({
                "date": datetime.fromtimestamp(c[0] / 1000).strftime("%Y-%m-%d"),
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5]),
            })
        return {
            "symbol": symbol,
            "source": "Binance·真实K线",
            "last_updated": datetime.now().isoformat(),
            "data": data,
        }

    # ── 数据源3 · Alpha Vantage 美股（需 Key·可选） ──
    def fetch_alpha_vantage(self, symbol: str) -> Optional[Dict]:
        """Alpha Vantage 美股日线（需 ALPHA_VANTAGE_KEY 环境变量）"""
        if not ALPHA_VANTAGE_KEY:
            return None
        url = (
            "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
            f"&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
        )
        try:
            data = _http_json(url, timeout=10)
        except Exception:
            return None
        ts = data.get("Time Series (Daily)") if isinstance(data, dict) else None
        if not ts:
            return None
        rows = []
        for date_str in sorted(ts.keys()):
            v = ts[date_str]
            rows.append({
                "date": date_str,
                "open": float(v["1. open"]),
                "high": float(v["2. high"]),
                "low": float(v["3. low"]),
                "close": float(v["4. close"]),
                "volume": float(v["5. volume"]),
            })
        return {
            "symbol": symbol,
            "source": "AlphaVantage·真实日线",
            "last_updated": datetime.now().isoformat(),
            "data": rows[-100:],
        }

    # ── 自动路由 ──
    def fetch(self, symbol: str) -> Optional[Dict]:
        """按标的类型自动选择数据源（缓存优先·降级兜底）"""
        cached = self._cache_get(symbol)
        if cached:
            return cached

        result = None
        if symbol.startswith(("sh", "sz")):
            result = self.fetch_sina(symbol)
        elif symbol.endswith("USDT") or symbol.endswith("USDC"):
            result = self.fetch_binance(symbol)
        else:
            result = self.fetch_alpha_vantage(symbol)

        if result:
            self._cache_put(symbol, result)
        else:
            result = self.cache.get(symbol)  # 兜底：返回历史缓存
        return result

    def fetch_all(self) -> Dict:
        """拉取全部默认标的"""
        results = {}
        for symbol in DEFAULT_SYMBOLS:
            data = self.fetch(symbol)
            if data:
                results[symbol] = data
            time.sleep(0.35)  # 接口限频保护
        return results


# 单例（供服务层导入）
fetcher = KLineFetcher()


if __name__ == "__main__":
    print("🐉 龍魂 K线 数据采集器 v1.0 — 真实数据自检")
    for sym in list(DEFAULT_SYMBOLS)[:4]:
        d = fetcher.fetch(sym)
        if d and d.get("data"):
            last = d["data"][-1]
            print(f"  ✅ {sym:10s} [{d['source']}] 根数={len(d['data']):3d} "
                  f"最新={last['date']} 收={last['close']}")
        else:
            print(f"  ⚠️ {sym:10s} 无数据")
