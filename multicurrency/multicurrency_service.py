# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种直达系统 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-MULTICURRENCY-SERVICE-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 提供实时汇率查询·三色标签·币种转换

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
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod

# 导入数据源管理器
try:
    from exchange_rate_sources import ExchangeRateSourceManager
    USE_REAL_SOURCES = True
except ImportError:
    USE_REAL_SOURCES = False

# ═══════════════════════════════════════════════════════════════
# 数据结构定义
# ═══════════════════════════════════════════════════════════════

class ColorTag(str, Enum):
    """三色标签 - 汇率偏离指示"""
    GREEN = "🟢"      # 正常 (< 2% 偏离)
    YELLOW = "🟡"     # 波动 (2-5% 偏离)
    RED = "🔴"        # 异常 (> 5% 偏离)

@dataclass
class ExchangeRate:
    """汇率数据"""
    base_currency: str
    target_currency: str
    rate: float
    timestamp: str
    source: str
    color_tag: ColorTag
    deviation: float  # 偏离百分比

@dataclass
class CurrencyInfo:
    """币种信息"""
    code: str
    name: str
    symbol: str
    category: str  # "fiat" or "crypto"
    priority: int  # 显示优先级

# ═══════════════════════════════════════════════════════════════
# 币种定义
# ═══════════════════════════════════════════════════════════════

SUPPORTED_CURRENCIES = {
    # 法币
    'CNY': CurrencyInfo('CNY', '人民币', '¥', 'fiat', 1),
    'USD': CurrencyInfo('USD', '美元', '$', 'fiat', 2),
    'EUR': CurrencyInfo('EUR', '欧元', '€', 'fiat', 3),
    'GBP': CurrencyInfo('GBP', '英镑', '£', 'fiat', 4),
    'JPY': CurrencyInfo('JPY', '日元', '¥', 'fiat', 5),

    # 加密货币
    'BTC': CurrencyInfo('BTC', '比特币', '฿', 'crypto', 6),
    'ETH': CurrencyInfo('ETH', '以太坊', 'Ξ', 'crypto', 7),
}

# ═══════════════════════════════════════════════════════════════
# 数据源抽象基类
# ═══════════════════════════════════════════════════════════════

class ExchangeRateSource(ABC):
    """汇率数据源的抽象基类"""

    @abstractmethod
    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """获取汇率"""
        pass

    @abstractmethod
    def name(self) -> str:
        """数据源名称"""
        pass

# ═══════════════════════════════════════════════════════════════
# 模拟数据源
# ═══════════════════════════════════════════════════════════════

class MockExchangeRateSource(ExchangeRateSource):
    """模拟汇率源 (用于测试)"""

    def __init__(self):
        # 模拟汇率数据 (基准: USD = 1.0)
        self.rates = {
            ('USD', 'CNY'): 7.25,
            ('USD', 'EUR'): 0.92,
            ('USD', 'GBP'): 0.79,
            ('USD', 'JPY'): 150.5,
            ('USD', 'BTC'): 0.000023,  # ~43,500 USD/BTC
            ('USD', 'ETH'): 0.00033,   # ~3,000 USD/ETH

            # 反向汇率
            ('CNY', 'USD'): 1/7.25,
            ('EUR', 'USD'): 1/0.92,
            ('GBP', 'USD'): 1/0.79,
            ('JPY', 'USD'): 1/150.5,
            ('BTC', 'USD'): 1/0.000023,
            ('ETH', 'USD'): 1/0.00033,
        }

    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """返回模拟汇率 (±1% 浮动)"""
        import random
        key = (base, target)
        if key not in self.rates:
            return None

        base_rate = self.rates[key]
        # 添加 ±1% 的随机浮动
        fluctuation = 1 + random.uniform(-0.01, 0.01)
        return base_rate * fluctuation

    def name(self) -> str:
        return "mock"

# ═══════════════════════════════════════════════════════════════
# 多币种中心
# ═══════════════════════════════════════════════════════════════

class MultiCurrencyHub:
    """龍魂多币种直达系统"""

    def __init__(self, db_path: str | None = None, use_real_sources: bool = True):
        # 使用新的数据源管理器或回退到 Mock
        if use_real_sources and USE_REAL_SOURCES:
            self.source_manager = ExchangeRateSourceManager()
            self.use_real_sources = True
        else:
            self.source_manager = None
            self.use_real_sources = False
            self.sources = {
                'mock': MockExchangeRateSource(),
            }

        self.cache = {}
        self.cache_ttl = 300  # 5 分钟
        self.history = []

        # 初始化数据库
        self.db_path = db_path or '~/.龍魂/multicurrency.db'
        self._init_db()

    def _init_db(self):
        """初始化 SQLite 数据库"""
        db_file = os.path.expanduser(self.db_path)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 汇率历史表
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
        """获取汇率 (带快取)"""
        # 检查快取
        cache_key = f"{base}_{target}"
        if cache_key in self.cache:
            cached_time, cached_rate = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_rate

        # 从源获取汇率
        if self.use_real_sources:
            rate_value, source = self.source_manager.fetch_rate(base, target)
        else:
            rate_value = self.sources['mock'].fetch_rate(base, target)
            source = 'mock'

        if rate_value is None:
            return None

        # 计算三色标签 (模拟偏离)
        deviation = abs(rate_value - self._get_base_rate(base, target)) * 100 / self._get_base_rate(base, target)
        if deviation < 2:
            color = ColorTag.GREEN
        elif deviation < 5:
            color = ColorTag.YELLOW
        else:
            color = ColorTag.RED

        # 创建汇率对象
        exchange_rate = ExchangeRate(
            base_currency=base,
            target_currency=target,
            rate=round(rate_value, 8),
            timestamp=datetime.now().isoformat(),
            source=source,
            color_tag=color,
            deviation=round(deviation, 2)
        )

        # 快取结果
        self.cache[cache_key] = (time.time(), exchange_rate)

        # 保存到数据库
        self._save_to_db(exchange_rate)

        return exchange_rate

    def _get_base_rate(self, base: str, target: str) -> float:
        """获取基准汇率 (用于计算偏离)"""
        # 简化版本 - 实际应使用更复杂的基准逻辑
        return 1.0

    def _save_to_db(self, rate: ExchangeRate):
        """保存汇率到数据库"""
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
        """币种转换"""
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
        """获取所有支持币种相对于基准币种的汇率"""
        rates = {}
        for currency in SUPPORTED_CURRENCIES:
            if currency == base_currency:
                continue

            rate = self.get_rate(base_currency, currency)
            if rate:
                rates[currency] = rate

        return rates

    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概览"""
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

    parser = argparse.ArgumentParser(description="🐉 龍魂多币种直达系统 v1.0")

    parser.add_argument('--query', nargs='+', help='查询特定币种 (e.g. --query CNY USD EUR)')
    parser.add_argument('--convert', nargs=3, metavar=('amount', 'from', 'to'),
                        help='币种转换 (e.g. --convert 100 CNY USD)')
    parser.add_argument('--overview', action='store_true', help='市场概览')
    parser.add_argument('--serve', action='store_true', help='启动 API 服务')

    args = parser.parse_args()

    hub = MultiCurrencyHub()

    print("🐉 龍魂多币种直达系统 v1.0")
    print("DNA:#龍芯⚡️2026-06-07-MULTICURRENCY-SERVICE-v1.0\n")

    if args.query:
        print(f"查询币种: {', '.join(args.query)}\n")
        for currency in args.query:
            if currency not in SUPPORTED_CURRENCIES:
                print(f"⚠️  不支持的币种: {currency}")
                continue

            rate = hub.get_rate('USD', currency)
            if rate:
                info = SUPPORTED_CURRENCIES[currency]
                print(f"{rate.color_tag.value} {currency} ({info.name})")
                print(f"   汇率: 1 USD = {rate.rate} {currency}")
                print(f"   偏离: {rate.deviation}%")
                print()

    elif args.convert:
        amount, from_cur, to_cur = float(args.convert[0]), args.convert[1], args.convert[2]
        result = hub.convert(amount, from_cur, to_cur)
        if result:
            print(f"{amount} {from_cur} = {result['converted_amount']} {to_cur}")
            print(f"汇率: 1 {from_cur} = {result['rate']} {to_cur}")
        else:
            print(f"❌ 无法转换 {from_cur} → {to_cur}")

    elif args.overview:
        overview = hub.get_market_overview()
        print(json.dumps(overview, indent=2, ensure_ascii=False))

    else:
        print("用法: python3 multicurrency_service.py [OPTIONS]")
        print("  --query CURRENCIES     查询币种")
        print("  --convert AMOUNT FROM TO   转换币种")
        print("  --overview             市场概览")
        print("  --serve                启动 API 服务")

if __name__ == '__main__':
    main()
