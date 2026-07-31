# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·系统测试套件 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-SYSTEM-TEST-SUITE-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 端到端系统测试·性能测试·监控指标

用法:
  python3 system_test_suite.py --full      # 完整测试
  python3 system_test_suite.py --quick     # 快速测试
  python3 system_test_suite.py --load      # 负载测试
  python3 system_test_suite.py --report    # 生成报告
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

# 导入本地模块
from multicurrency_service import MultiCurrencyHub
from exchange_rate_sources import ExchangeRateSourceManager
from notion_multicurrency_sync import NotionMulticurrencySyncManager, NotionAPI

# ═══════════════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# 测试套件
# ═══════════════════════════════════════════════════════════════

class SystemTestSuite:
    """龍魂多币种系统测试套件"""

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
        """记录测试结果"""
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
    # 模块测试
    # ═══════════════════════════════════════════════════════════════

    def test_multicurrency_hub(self) -> bool:
        """测试 MultiCurrencyHub 初始化和基本功能"""
        test_name = "test_multicurrency_hub"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)
            assert hub is not None, "Hub 初始化失败"

            # 测试 get_rate
            rate = hub.get_rate('USD', 'CNY')
            assert rate is not None, "无法获取 USD/CNY 汇率"
            assert rate.rate > 0, "汇率值无效"

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
        """测试 ExchangeRateSourceManager·故障转移"""
        test_name = "test_exchange_rate_sources"
        start_time = time.time()

        try:
            manager = ExchangeRateSourceManager()

            # 测试多个币种对
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

            assert success_count > 0, f"无法获取任何汇率 (0/{len(test_pairs)})"

            duration = time.time() - start_time
            self.metrics['response_times'].append(duration)
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: {success_count}/{len(test_pairs)} 对成功")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_sqlite_persistence(self) -> bool:
        """测试 SQLite 数据持久化"""
        test_name = "test_sqlite_persistence"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 获取汇率会自动保存到 SQLite
            rate = hub.get_rate('USD', 'EUR')
            assert rate is not None, "无法获取汇率"

            # 验证数据库
            db_file = os.path.expanduser('~/.龍魂/multicurrency.db')
            assert os.path.exists(db_file), "数据库文件不存在"

            # 查询数据库
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM exchange_rates WHERE base_currency = 'USD'")
            count = cursor.fetchone()[0]
            conn.close()

            assert count > 0, "数据库中无汇率记录"

            duration = time.time() - start_time
            self._log_test(test_name, 'passed', duration)
            logger.info(f"✅ {test_name}: 数据库包含 {count} 条记录")
            return True

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_notion_api_config(self) -> bool:
        """测试 Notion API 配置检查"""
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
                logger.info(f"⏭️  {test_name}: Notion API 未配置 (跳过)")
                return True  # 不配置不算失败

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    def test_three_color_tagging(self) -> bool:
        """测试三色标签系统"""
        test_name = "test_three_color_tagging"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 取得多个汇率并检查色标签
            test_pairs = [('USD', 'CNY'), ('USD', 'EUR'), ('USD', 'GBP')]
            color_counts = {'🟢': 0, '🟡': 0, '🔴': 0}

            for base, target in test_pairs:
                rate = hub.get_rate(base, target)
                if rate:
                    color = rate.color_tag.value
                    if color in color_counts:
                        color_counts[color] += 1

            assert sum(color_counts.values()) > 0, "无色标签被分配"

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
        """测试币种转换功能"""
        test_name = "test_currency_conversion"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)

            # 测试转换
            result = hub.convert(100, 'USD', 'CNY')
            assert result is not None, "转换失败"
            assert result['amount'] == 100, "金额不符"
            assert result['converted_amount'] > 0, "转换金额无效"

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
    # 性能测试
    # ═══════════════════════════════════════════════════════════════

    def test_performance_load(self, iterations: int = 100) -> bool:
        """性能/负载测试"""
        test_name = f"test_performance_load_{iterations}x"
        start_time = time.time()

        try:
            hub = MultiCurrencyHub(use_real_sources=True)
            response_times = []

            logger.info(f"开始 {iterations} 次循环负载测试...")

            for i in range(iterations):
                iter_start = time.time()
                rate = hub.get_rate('USD', 'CNY')
                iter_duration = time.time() - iter_start

                if rate:
                    response_times.append(iter_duration)
                    if (i + 1) % 20 == 0:
                        logger.info(f"  完成 {i + 1}/{iterations} 次")

            # 计算统计
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
                raise Exception("无可用的响应时间数据")

        except Exception as e:
            duration = time.time() - start_time
            self._log_test(test_name, 'failed', duration, str(e))
            logger.error(f"❌ {test_name}: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════
    # 测试套件执行
    # ═══════════════════════════════════════════════════════════════

    def run_quick_tests(self) -> Dict:
        """快速测试 (5 分钟·基本功能)"""
        logger.info("═" * 70)
        logger.info("🧪 快速测试套件开始")
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
        """完整测试 (15 分钟·包含负载测试)"""
        logger.info("═" * 70)
        logger.info("🧪 完整测试套件开始")
        logger.info("═" * 70)

        # 先执行快速测试
        self.run_quick_tests()

        # 再执行额外测试
        logger.info("\n🔧 配置测试...")
        self.test_notion_api_config()

        # 负载测试
        logger.info("\n⚡ 性能测试...")
        self.test_performance_load(iterations=50)

        return self.results

    def generate_report(self) -> str:
        """生成测试报告"""
        report = []
        report.append("═" * 70)
        report.append("🐉 龍魂多币种系统测试报告")
        report.append("═" * 70)
        report.append(f"时间: {self.results['timestamp']}")
        report.append(f"总计: {self.results['summary']['total']} 个测试")
        report.append(f"✅ 通过: {self.results['summary']['passed']}")
        report.append(f"❌ 失败: {self.results['summary']['failed']}")
        report.append(f"⏭️  跳过: {self.results['summary']['skipped']}")

        if self.metrics['response_times']:
            avg_time = statistics.mean(self.metrics['response_times'])
            report.append(f"\n性能指标:")
            report.append(f"  平均响应时间: {avg_time*1000:.2f}ms")
            report.append(f"  总请求数: {self.metrics['success_count']}")
            report.append(f"  总错误数: {self.metrics['error_count']}")

        # 测试详情
        report.append(f"\n详细结果:")
        for test in self.results['tests']:
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'skipped': '⏭️ '
            }.get(test['status'], '❓')
            report.append(f"  {status_icon} {test['name']}: {test['duration']:.3f}s")
            if test['error']:
                report.append(f"     错误: {test['error']}")

        report.append("\n" + "═" * 70)
        success_rate = (self.results['summary']['passed'] / self.results['summary']['total'] * 100) if self.results['summary']['total'] > 0 else 0
        report.append(f"成功率: {success_rate:.1f}%")
        report.append("═" * 70)

        return "\n".join(report)

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂多币种·系统测试套件 v1.0")

    parser.add_argument('--full', action='store_true', help='完整测试 (含负载测试)')
    parser.add_argument('--quick', action='store_true', help='快速测试')
    parser.add_argument('--load', action='store_true', help='负载测试 (100 次循环)')
    parser.add_argument('--report', action='store_true', help='生成报告')

    args = parser.parse_args()

    suite = SystemTestSuite()

    print("🐉 龍魂多币种·系统测试套件 v1.0")
    print("DNA:#龍芯⚡️2026-06-07-SYSTEM-TEST-SUITE-v1.0\n")

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

    # 保存报告
    report_path = os.path.expanduser('~/.龍魂/system_test_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📊 报告已保存: {report_path}")

if __name__ == '__main__':
    main()
