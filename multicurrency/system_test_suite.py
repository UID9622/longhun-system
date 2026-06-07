#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多幣種·系統測試套件 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️2026-06-07-SYSTEM-TEST-SUITE-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 端到端系統測試·性能測試·監控指標

用法:
  python3 system_test_suite.py --full      # 完整測試
  python3 system_test_suite.py --quick     # 快速測試
  python3 system_test_suite.py --load      # 負載測試
  python3 system_test_suite.py --report    # 生成報告
"""

import os
import json
import time
import sqlite3
import logging
from typing import Dict, List, Tuple
from datetime import datetime
import statistics
import argparse

# 導入本地模塊
from multicurrency_service import MultiCurrencyHub
from exchange_rate_sources import ExchangeRateSourceManager
from notion_multicurrency_sync import NotionMulticurrencySyncManager, NotionAPI

# ═══════════════════════════════════════════════════════════════
# 日誌配置
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 測試套件
# ═══════════════════════════════════════════════════════════════

class SystemTestSuite:
    """龍魂多幣種系統測試套件"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0
            }
        }
        self.metrics = {
            'response_times': [],
            'error_count': 0,
            'success_count': 0
        }

    def _log_test(self, name: str, status: str, duration: float = 0, error: str = None):
        """記錄測試結果"""
        self.results['tests'].append({
            'name': name,
            'status': status,
            'duration': duration,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })

        if status == 'passed':
            self.results['summary']['passed'] += 1
            self.metrics['success_count'] += 1
        elif status == 'failed':
            self.results['summary']['failed'] += 1
            self.metrics['error_count'] += 1
        elif status == 'skipped':
            self.results['summary']['skipped'] += 1

        self.results['summary']['total'] += 1

    # ═══════════════════════════════════════════════════════════════
    # 模塊測試
    # ═══════════════════════════════════════════════════════════════

    def test_multicurrency_hub(self) -> bool:
        """測試 MultiCurrencyHub 初始化和基本功能"""
        test_name = "test_multicurrency_hub"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)
            assert hub is not None, "Hub 初始化失敗"

            # 測試 get_rate
            rate = hub.get_rate('USD', 'CNY')
            assert rate is not None, "無法獲取 USD/CNY 匯率"
            assert rate.rate > 0, "匯率值無效"

            duration = time.time() - start_time
            self.metrics['response_times'].append(duration)
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: USD/CNY = {rate.rate} ({duration:.3f}s)")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_exchange_rate_sources(self) -> bool:
        """測試 ExchangeRateSourceManager·故障轉移"""
        test_name = "test_exchange_rate_sources"
        start_time = time.time()

        try:
            manager = ExchangeRateSourceManager()

            # 測試多個幣種對
            test_pairs = [
                ('USD', 'CNY'),
                ('USD', 'EUR'),
                ('BTC', 'USD'),
            ]

            success_count = 0
            for base, target in test_pairs:
                rate, source = manager.fetch_rate(base, target)
                if rate is not None:
                    success_count += 1
                    logger.info(f"  {base}/{target}: {rate} ({source})")

            assert success_count > 0, f"無法獲取任何匯率 (0/{len(test_pairs)})"

            duration = time.time() - start_time
            self.metrics['response_times'].append(duration)
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: {success_count}/{len(test_pairs)} 對成功")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_sqlite_persistence(self) -> bool:
        """測試 SQLite 數據持久化"""
        test_name = "test_sqlite_persistence"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 獲取匯率會自動保存到 SQLite
            rate = hub.get_rate('USD', 'EUR')
            assert rate is not None, "無法獲取匯率"

            # 驗證數據庫
            db_file = os.path.expanduser('~/.龍魂/multicurrency.db')
            assert os.path.exists(db_file), "數據庫文件不存在"

            # 查詢數據庫
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM exchange_rates WHERE base_currency = 'USD'")
            count = cursor.fetchone()[0]
            conn.close()

            assert count > 0, "數據庫中無匯率記錄"

            duration = time.time() - start_time
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: 數據庫包含 {count} 條記錄")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_notion_api_config(self) -> bool:
        """測試 Notion API 配置檢查"""
        test_name = "test_notion_api_config"
        start_time = time.time()

        try:
            api = NotionAPI()
            is_configured = api.is_configured()

            duration = time.time() - start_time
            if is_configured:
                self._log_test(test_name, 'passed', duration)
                logger.info(f"✅ {test_name}: Notion API 已配置")
                return True
            else:
                self._log_test(test_name, 'skipped', duration)
                logger.info(f"⏭️  {test_name}: Notion API 未配置 (跳過)")
                return True  # 不配置不算失敗

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_three_color_tagging(self) -> bool:
        """測試三色標籤系統"""
        test_name = "test_three_color_tagging"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 取得多個匯率並檢查色標籤
            test_pairs = [('USD', 'CNY'), ('USD', 'EUR'), ('USD', 'GBP')]
            color_counts = {'🟢': 0, '🟡': 0, '🔴': 0}

            for base, target in test_pairs:
                rate = hub.get_rate(base, target)
                if rate:
                    color = rate.color_tag.value
                    if color in color_counts:
                        color_counts[color] += 1

            assert sum(color_counts.values()) > 0, "無色標籤被分配"

            duration = time.time() - start_time
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: 🟢 {color_counts['🟢']} 🟡 {color_counts['🟡']} 🔴 {color_counts['🔴']}")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_currency_conversion(self) -> bool:
        """測試幣種轉換功能"""
        test_name = "test_currency_conversion"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 測試轉換
            result = hub.convert(100, 'USD', 'CNY')
            assert result is not None, "轉換失敗"
            assert result['amount'] == 100, "金額不符"
            assert result['converted_amount'] > 0, "轉換金額無效"

            duration = time.time() - start_time
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: 100 USD = {result['converted_amount']} CNY")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════
    # 性能測試
    # ═══════════════════════════════════════════════════════════════

    def test_performance_load(self, iterations: int = 100) -> bool:
        """性能/負載測試"""
        test_name = f"test_performance_load_{iterations}x"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)
            response_times = []

            logger.info(f"開始 {iterations} 次循環負載測試...")

            for i in range(iterations):
                iter_start = time.time()
                rate = hub.get_rate('USD', 'CNY')
                iter_duration = time.time() - iter_start

                if rate:
                    response_times.append(iter_duration)
                    if (i + 1) % 20 == 0:
                        logger.info(f"  完成 {i + 1}/{iterations} 次")

            # 計算統計
            if response_times:
                avg_time = statistics.mean(response_times)
                median_time = statistics.median(response_times)
                max_time = max(response_times)
                min_time = min(response_times)

                duration = time.time() - start_time
                self._log_test(test_name, 'passed', duration)

                logger.info(f"✅ {test_name}:")
                logger.info(f"   平均: {avg_time*1000:.2f}ms")
                logger.info(f"   中位: {median_time*1000:.2f}ms")
                logger.info(f"   最大: {max_time*1000:.2f}ms")
                logger.info(f"   最小: {min_time*1000:.2f}ms")
                return True
            else:
                raise Exception("無可用的響應時間數據")

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════
    # 測試套件執行
    # ═══════════════════════════════════════════════════════════════

    def run_quick_tests(self) -> Dict:
        """快速測試 (5 分鐘·基本功能)"""
        logger.info("═" * 70)
        logger.info("🧪 快速測試套件開始")
        logger.info("═" * 70)

        tests = [
            self.test_multicurrency_hub,
            self.test_exchange_rate_sources,
            self.test_sqlite_persistence,
            self.test_three_color_tagging,
            self.test_currency_conversion,
        ]

        for test_func in tests:
            test_func()

        return self.results

    def run_full_tests(self) -> Dict:
        """完整測試 (15 分鐘·包含負載測試)"""
        logger.info("═" * 70)
        logger.info("🧪 完整測試套件開始")
        logger.info("═" * 70)

        # 先執行快速測試
        self.run_quick_tests()

        # 再執行額外測試
        logger.info("\n🔧 配置測試...")
        self.test_notion_api_config()

        # 負載測試
        logger.info("\n⚡ 性能測試...")
        self.test_performance_load(iterations=50)

        return self.results

    def generate_report(self) -> str:
        """生成測試報告"""
        report = []
        report.append("═" * 70)
        report.append("🐉 龍魂多幣種系統測試報告")
        report.append("═" * 70)
        report.append(f"時間: {self.results['timestamp']}")
        report.append(f"總計: {self.results['summary']['total']} 個測試")
        report.append(f"✅ 通過: {self.results['summary']['passed']}")
        report.append(f"❌ 失敗: {self.results['summary']['failed']}")
        report.append(f"⏭️  跳過: {self.results['summary']['skipped']}")

        if self.metrics['response_times']:
            avg_time = statistics.mean(self.metrics['response_times'])
            report.append(f"\n性能指標:")
            report.append(f"  平均響應時間: {avg_time*1000:.2f}ms")
            report.append(f"  總請求數: {self.metrics['success_count']}")
            report.append(f"  總錯誤數: {self.metrics['error_count']}")

        # 測試詳情
        report.append(f"\n詳細結果:")
        for test in self.results['tests']:
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'skipped': '⏭️ '
            }.get(test['status'], '❓')
            report.append(f"  {status_icon} {test['name']}: {test['duration']:.3f}s")
            if test['error']:
                report.append(f"     錯誤: {test['error']}")

        report.append("\n" + "═" * 70)
        success_rate = (self.results['summary']['passed'] / self.results['summary']['total'] * 100) if self.results['summary']['total'] > 0 else 0
        report.append(f"成功率: {success_rate:.1f}%")
        report.append("═" * 70)

        return "\n".join(report)

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂多幣種·系統測試套件 v1.0")

    parser.add_argument('--full', action='store_true', help='完整測試 (含負載測試)')
    parser.add_argument('--quick', action='store_true', help='快速測試')
    parser.add_argument('--load', action='store_true', help='負載測試 (100 次循環)')
    parser.add_argument('--report', action='store_true', help='生成報告')

    args = parser.parse_args()

    suite = SystemTestSuite()

    print("🐉 龍魂多幣種·系統測試套件 v1.0")
    print("DNA: #龍芯⚡️2026-06-07-SYSTEM-TEST-SUITE-v1.0\n")

    if args.full:
        suite.run_full_tests()
    elif args.load:
        suite.test_performance_load(iterations=100)
    elif args.quick:
        suite.run_quick_tests()
    else:
        suite.run_quick_tests()

    report = suite.generate_report()
    print(report)

    # 保存報告
    report_path = os.path.expanduser('~/.龍魂/system_test_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📊 報告已保存: {report_path}")

if __name__ == '__main__':
    main()
