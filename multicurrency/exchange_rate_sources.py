#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多幣種·數據源集成 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-EXCHANGE-RATE-SOURCES-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 實現 CoinGecko·Fixer.io·Mock 三層數據源·支持故障轉移
"""

import os
import json
import time
import random
import logging
from typing import Dict, Optional, Tuple
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════════════
# 日誌配置
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 數據源抽象基類
# ═══════════════════════════════════════════════════════════════

class ExchangeRateSource(ABC):
    """匯率數據源的抽象基類"""

    def __init__(self, name: str, timeout: int = 10):
        self.name_str = name
        self.timeout = timeout
        self.last_error = None
        self.success_count = 0
        self.error_count = 0

    @abstractmethod
    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """獲取匯率"""
        pass

    def name(self) -> str:
        """數據源名稱"""
        return self.name_str

    def stats(self) -> Dict:
        """獲取統計信息"""
        total = self.success_count + self.error_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        return {
            'source': self.name_str,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': round(success_rate, 2),
            'last_error': self.last_error
        }

    def _record_success(self):
        """記錄成功"""
        self.success_count += 1
        self.last_error = None

    def _record_error(self, error: str):
        """記錄錯誤"""
        self.error_count += 1
        self.last_error = error
        logger.warning(f"{self.name_str} 錯誤: {error}")

# ═══════════════════════════════════════════════════════════════
# CoinGecko 數據源 (加密貨幣)
# ═══════════════════════════════════════════════════════════════

class CoinGeckoSource(ExchangeRateSource):
    """CoinGecko 加密貨幣匯率源"""

    def __init__(self):
        super().__init__('coingecko', timeout=10)
        self.api_key = os.environ.get('COINGECKO_API_KEY', '')
        self.cache = {}
        self.cache_ttl = 300  # 5 分鐘

        # 幣種映射 (code → coingecko id)
        self.coin_mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'CNY': 'cny',
            'USD': 'usd',
            'EUR': 'eur',
            'GBP': 'gbp',
            'JPY': 'jpy'
        }

    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """從 CoinGecko 獲取匯率"""
        try:
            # 檢查快取
            cache_key = f"{base}_{target}"
            if cache_key in self.cache:
                cache_time, cached_rate = self.cache[cache_key]
                if time.time() - cache_time < self.cache_ttl:
                    self._record_success()
                    return cached_rate

            # 構建 API URL
            base_id = self.coin_mapping.get(base)
            target_id = self.coin_mapping.get(target)

            if not base_id or not target_id:
                self._record_error(f"不支持的幣種: {base} or {target}")
                return None

            url = (f"https://api.coingecko.com/api/v3/simple/price"
                   f"?ids={base_id}&vs_currencies={target_id.lower()}")

            # 發送請求
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))

                # 提取匯率
                rate = data.get(base_id, {}).get(target_id.lower())
                if rate is None:
                    self._record_error(f"無法獲取 {base}/{target} 匯率")
                    return None

                # 快取結果
                self.cache[cache_key] = (time.time(), float(rate))
                self._record_success()

                logger.info(f"CoinGecko: {base}/{target} = {rate}")
                return float(rate)

        except urllib.error.URLError as e:
            self._record_error(f"網絡錯誤: {str(e)}")
        except Exception as e:
            self._record_error(f"未知錯誤: {str(e)}")

        return None

# ═══════════════════════════════════════════════════════════════
# Fixer.io 數據源 (法幣)
# ═══════════════════════════════════════════════════════════════

class FixerIOSource(ExchangeRateSource):
    """Fixer.io 法幣匯率源"""

    def __init__(self):
        super().__init__('fixer.io', timeout=10)
        self.api_key = os.environ.get('FIXER_API_KEY', '')
        self.cache = {}
        self.cache_ttl = 300  # 5 分鐘

        # 支持的法幣
        self.fiat_currencies = {
            'CNY', 'USD', 'EUR', 'GBP', 'JPY',
            'CAD', 'AUD', 'CHF', 'SEK', 'NZD'
        }

    def fetch_rate(self, base: str, target: str) -> Optional[float]:
        """從 Fixer.io 獲取匯率"""
        try:
            # 檢查是否支持
            if base not in self.fiat_currencies or target not in self.fiat_currencies:
                return None

            # 檢查快取
            cache_key = f"{base}_{target}"
            if cache_key in self.cache:
                cache_time, cached_rate = self.cache[cache_key]
                if time.time() - cache_time < self.cache_ttl:
                    self._record_success()
                    return cached_rate

            # 如果沒有 API key·回退到 Mock
            if not self.api_key:
                return None

            # 構建 API URL
            url = (f"https://api.fixer.io/latest"
                   f"?access_key={self.api_key}"
                   f"&base={base}")

            # 發送請求
            req = urllib.request.Request(url)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))

                if not data.get('success'):
                    self._record_error(f"API 錯誤: {data.get('error', {}).get('info')}")
                    return None

                # 提取匯率
                rate = data.get('rates', {}).get(target)
                if rate is None:
                    self._record_error(f"無法獲取 {base}/{target} 匯率")
                    return None

                # 快取結果
                self.cache[cache_key] = (time.time(), float(rate))
                self._record_success()

                logger.info(f"Fixer.io: {base}/{target} = {rate}")
                return float(rate)

        except urllib.error.URLError as e:
            self._record_error(f"網絡錯誤: {str(e)}")
        except Exception as e:
            self._record_error(f"未知錯誤: {str(e)}")

        return None

# ═══════════════════════════════════════════════════════════════
# Mock 數據源 (測試·故障轉移)
# ═══════════════════════════════════════════════════════════════

class MockExchangeRateSource(ExchangeRateSource):
    """模擬匯率源 (用於測試和故障轉移)"""

    def __init__(self):
        super().__init__('mock', timeout=1)
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
        try:
            key = (base, target)
            if key not in self.rates:
                return None

            base_rate = self.rates[key]
            # 添加 ±1% 的隨機浮動
            fluctuation = 1 + random.uniform(-0.01, 0.01)
            rate = base_rate * fluctuation

            self._record_success()
            logger.info(f"Mock: {base}/{target} = {rate:.8f}")
            return rate

        except Exception as e:
            self._record_error(f"未知錯誤: {str(e)}")
            return None

# ═══════════════════════════════════════════════════════════════
# 數據源管理器 (故障轉移邏輯)
# ═══════════════════════════════════════════════════════════════

class ExchangeRateSourceManager:
    """管理多個數據源·支持故障轉移"""

    def __init__(self):
        self.sources = [
            CoinGeckoSource(),      # 優先級 1: CoinGecko (加密)
            FixerIOSource(),        # 優先級 2: Fixer.io (法幣)
            MockExchangeRateSource()  # 優先級 3: Mock (故障轉移)
        ]
        self.retry_config = {
            'max_retries': 2,
            'initial_delay': 1.0,   # 1 秒
            'backoff_factor': 2.0   # 指數退避
        }

    def fetch_rate(self, base: str, target: str) -> Tuple[Optional[float], str]:
        """
        嘗試從各數據源獲取匯率·按優先級故障轉移

        Returns:
            (匯率, 數據源名稱) 或 (None, '失敗')
        """
        for attempt in range(self.retry_config['max_retries']):
            for source in self.sources:
                try:
                    rate = source.fetch_rate(base, target)
                    if rate is not None:
                        return rate, source.name()
                except Exception as e:
                    logger.warning(f"{source.name()} 異常: {str(e)}")

            # 指數退避重試
            if attempt < self.retry_config['max_retries'] - 1:
                delay = self.retry_config['initial_delay'] * (
                    self.retry_config['backoff_factor'] ** attempt
                )
                logger.info(f"等待 {delay:.1f}s 後重試...")
                time.sleep(delay)

        logger.error(f"無法獲取 {base}/{target} 匯率·已耗盡所有數據源")
        return None, '失敗'

    def get_stats(self) -> Dict:
        """獲取所有數據源的統計信息"""
        return {
            'timestamp': datetime.now().isoformat(),
            'sources': [source.stats() for source in self.sources],
            'retry_config': self.retry_config
        }

if __name__ == '__main__':
    # 測試數據源
    manager = ExchangeRateSourceManager()

    # 測試匯率查詢
    test_pairs = [
        ('USD', 'CNY'),
        ('USD', 'EUR'),
        ('BTC', 'USD'),
        ('ETH', 'USD'),
    ]

    print("═" * 70)
    print("🐉 龍魂多幣種數據源集成測試")
    print("═" * 70)

    for base, target in test_pairs:
        rate, source = manager.fetch_rate(base, target)
        status = "✅" if rate else "❌"
        rate_str = f"{rate:.8f}" if rate else "N/A"
        print(f"{status} {base}/{target}: {rate_str} ({source})")

    print("\n📊 數據源統計:")
    stats = manager.get_stats()
    for source_stat in stats['sources']:
        print(f"  {source_stat['source']}: "
              f"{source_stat['success_count']}✅ "
              f"{source_stat['error_count']}❌ "
              f"({source_stat['success_rate']}% 成功率)")
