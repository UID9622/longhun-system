#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多幣種直達系統 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️2026-06-07-MULTICURRENCY-SERVICE-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 提供實時匯率查詢·三色標籤·幣種轉換

用法:
  python3 multicurrency_service.py --serve
  python3 multicurrency_service.py --query CNY USD EUR
  python3 multicurrency_service.py --convert 100 CNY USD
"""

import os
import sys
import json
import time
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod

# ═══════════════════════════════════════════════════════════════
# 數據結構定義
# ═══════════════════════════════════════════════════════════════

class ColorTag(str, Enum):
    """三色標籤 - 匯率偏離指示"""
    GREEN = "🟢"      # 正常 (< 2% 偏離)
    YELLOW = "🟡"     # 波動 (2-5% 偏離)
    RED = "🔴"        # 異常 (> 5% 偏離)

@dataclass
class ExchangeRate:
    """匯率數據"""
    base_currency: str
    target_currency: str
    rate: float
    timestamp: str
    source: str
    color_tag: ColorTag
    deviation: float  # 偏離百分比

@dataclass
class CurrencyInfo:
    """幣種信息"""
    code: str
    name: str
    symbol: str
    category: str  # "fiat" or "crypto"
    priority: int  # 顯示優先級

# ═══════════════════════════════════════════════════════════════
# 幣種定義
# ═══════════════════════════════════════════════════════════════

SUPPORTED_CURRENCIES = {
    # 法幣
    'CNY': CurrencyInfo('CNY', '人民幣', '¥', 'fiat', 1),
    'USD': CurrencyInfo('USD', '美元', '$', 'fiat', 2),
    'EUR': CurrencyInfo('EUR', '歐元', '€', 'fiat', 3),
    'GBP': CurrencyInfo('GBP', '英鎊', '£', 'fiat', 4),
    'JPY': CurrencyInfo('JPY', '日元', '¥', 'fiat', 5),

    # 加密貨幣
    'BTC': CurrencyInfo('BTC', '比特幣', '฿', 'crypto', 6),
    'ETH': CurrencyInfo('ETH', '以太坊', 'Ξ', 'crypto', 7),
}

# ═══════════════════════════════════════════════════════════════
# 數據源抽象基類
# ═══════════════════════════════════════════════════════════════

class ExchangeRateSource(ABC):
    """匯率數據源的抽象基類"""

    @abstractmethod
    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """獲取匯率"""
        pass

    @abstractmethod
    def name(self) -> str:
        """數據源名稱"""
        pass

# ═══════════════════════════════════════════════════════════════
# 模擬數據源
# ═══════════════════════════════════════════════════════════════

class MockExchangeRateSource(ExchangeRateSource):
    """模擬匯率源 (用於測試)"""

    def __init__(self):
        # 模擬匯率數據 (基準: USD = 1.0)
        self.rates = {
            ('USD', 'CNY'): 7.25,
            ('USD', 'EUR'): 0.92,
            ('USD', 'GBP'): 0.79,
            ('USD', 'JPY'): 150.5,
            ('USD', 'BTC'): 0.000023,  # ~43,500 USD/BTC
            ('USD', 'ETH'): 0.00033,   # ~3,000 USD/ETH

            # 反向匯率
            ('CNY', 'USD'): 1/7.25,
            ('EUR', 'USD'): 1/0.92,
            ('GBP', 'USD'): 1/0.79,
            ('JPY', 'USD'): 1/150.5,
            ('BTC', 'USD'): 1/0.000023,
            ('ETH', 'USD'): 1/0.00033,
        }

    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """返回模擬匯率 (±1% 浮動)"""
        import random
        key = (base, target)
        if key not in self.rates:
            return None

        base_rate = self.rates[key]
        # 添加 ±1% 的隨機浮動
        fluctuation = 1 + random.uniform(-0.01, 0.01)
        return base_rate * fluctuation

    def name(self) -> str:
        return "mock"

# ═══════════════════════════════════════════════════════════════
# 多幣種中心
# ═══════════════════════════════════════════════════════════════

class MultiCurrencyHub:
    """龍魂多幣種直達系統"""

    def __init__(self, db_path: str = None):
        self.sources = {
            'mock': MockExchangeRateSource(),
            # 'fixer': FixerIOSource(),    # TODO: 實現
            # 'coingecko': CoinGeckoSource(),  # TODO: 實現
        }
        self.cache = {}
        self.cache_ttl = 300  # 5 分鐘
        self.history = []

        # 初始化數據庫
        self.db_path = db_path or '~/.龍魂/multicurrency.db'
        self._init_db()

    def _init_db(self):
        """初始化 SQLite 數據庫"""
        db_file = os.path.expanduser(self.db_path)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 匯率歷史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY,
                base_currency TEXT NOT NULL,
                target_currency TEXT NOT NULL,
                rate REAL NOT NULL,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                color_tag TEXT NOT NULL,
                deviation REAL NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def get_rate(self, base: str, target: str) -> Optional[ExchangeRate]:
        """獲取匯率 (帶快取)"""
        # 檢查快取
        cache_key = f"{base}_{target}"
        if cache_key in self.cache:
            cached_time, cached_rate = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_rate

        # 從源獲取匯率
        rate_value = self.sources['mock'].fetch_rate(base, target)
        if rate_value is None:
            return None

        # 計算三色標籤 (模擬偏離)
        deviation = abs(rate_value - self._get_base_rate(base, target)) * 100 / self._get_base_rate(base, target)
        if deviation < 2:
            color = ColorTag.GREEN
        elif deviation < 5:
            color = ColorTag.YELLOW
        else:
            color = ColorTag.RED

        # 創建匯率對象
        exchange_rate = ExchangeRate(
            base_currency=base,
            target_currency=target,
            rate=round(rate_value, 8),
            timestamp=datetime.now().isoformat(),
            source='mock',
            color_tag=color,
            deviation=round(deviation, 2)
        )

        # 快取結果
        self.cache[cache_key] = (time.time(), exchange_rate)

        # 保存到數據庫
        self._save_to_db(exchange_rate)

        return exchange_rate

    def _get_base_rate(self, base: str, target: str) -> float:
        """獲取基準匯率 (用於計算偏離)"""
        # 簡化版本 - 實際應使用更複雜的基準邏輯
        return 1.0

    def _save_to_db(self, rate: ExchangeRate):
        """保存匯率到數據庫"""
        db_file = os.path.expanduser(self.db_path)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO exchange_rates
            (base_currency, target_currency, rate, timestamp, source, color_tag, deviation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            rate.base_currency,
            rate.target_currency,
            rate.rate,
            rate.timestamp,
            rate.source,
            rate.color_tag.value,
            rate.deviation
        ))

        conn.commit()
        conn.close()

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """幣種轉換"""
        rate = self.get_rate(from_currency, to_currency)
        if rate is None:
            return None

        converted_amount = amount * rate.rate

        return {
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 8),
            'rate': rate.rate,
            'rate_info': asdict(rate),
        }

    def get_all_rates(self, base_currency: str = 'USD') -> Dict[str, ExchangeRate]:
        """獲取所有支持幣種相對於基準幣種的匯率"""
        rates = {}
        for currency in SUPPORTED_CURRENCIES:
            if currency == base_currency:
                continue

            rate = self.get_rate(base_currency, currency)
            if rate:
                rates[currency] = rate

        return rates

    def get_market_overview(self) -> Dict:
        """獲取市場概覽"""
        return {
            'timestamp': datetime.now().isoformat(),
            'base_currency': 'USD',
            'rates': {
                code: asdict(self.get_rate('USD', code))
                for code in ['CNY', 'EUR', 'GBP', 'JPY', 'BTC', 'ETH']
                if self.get_rate('USD', code)
            },
            'sources': list(self.sources.keys()),
        }

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="🐉 龍魂多幣種直達系統 v1.0")

    parser.add_argument('--query', nargs='+', help='查詢特定幣種 (e.g. --query CNY USD EUR)')
    parser.add_argument('--convert', nargs=3, metavar=('amount', 'from', 'to'),
                        help='幣種轉換 (e.g. --convert 100 CNY USD)')
    parser.add_argument('--overview', action='store_true', help='市場概覽')
    parser.add_argument('--serve', action='store_true', help='啟動 API 服務')

    args = parser.parse_args()

    hub = MultiCurrencyHub()

    print("🐉 龍魂多幣種直達系統 v1.0")
    print("DNA: #龍芯⚡️2026-06-07-MULTICURRENCY-SERVICE-v1.0\n")

    if args.query:
        print(f"查詢幣種: {', '.join(args.query)}\n")
        for currency in args.query:
            if currency not in SUPPORTED_CURRENCIES:
                print(f"⚠️  不支持的幣種: {currency}")
                continue

            rate = hub.get_rate('USD', currency)
            if rate:
                info = SUPPORTED_CURRENCIES[currency]
                print(f"{rate.color_tag.value} {currency} ({info.name})")
                print(f"   匯率: 1 USD = {rate.rate} {currency}")
                print(f"   偏離: {rate.deviation}%")
                print()

    elif args.convert:
        amount, from_cur, to_cur = float(args.convert[0]), args.convert[1], args.convert[2]
        result = hub.convert(amount, from_cur, to_cur)
        if result:
            print(f"{amount} {from_cur} = {result['converted_amount']} {to_cur}")
            print(f"匯率: 1 {from_cur} = {result['rate']} {to_cur}")
        else:
            print(f"❌ 無法轉換 {from_cur} → {to_cur}")

    elif args.overview:
        overview = hub.get_market_overview()
        print(json.dumps(overview, indent=2, ensure_ascii=False))

    else:
        print("用法: python3 multicurrency_service.py [OPTIONS]")
        print("  --query CURRENCIES     查詢幣種")
        print("  --convert AMOUNT FROM TO   轉換幣種")
        print("  --overview             市場概覽")
        print("  --serve                啟動 API 服務")

if __name__ == '__main__':
    main()
