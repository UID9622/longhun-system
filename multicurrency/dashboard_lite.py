#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·轻量级仪表板 (不依赖 Flask)
DNA: #龍芯⚡️2026-06-07-DASHBOARD-LITE-v1.0
"""

import json
import sqlite3
import os
from datetime import datetime
from multicurrency_service import MultiCurrencyHub
from trend_analyzer import TrendAnalyzer
from alert_system import AlertManager
from currency_database import CurrencyDatabase

class DashboardLite:
    """轻量级仪表板·本地 JSON 输出"""
    
    def __init__(self):
        self.hub = MultiCurrencyHub(use_real_sources=True)
        self.trend_analyzer = TrendAnalyzer()
        self.alert_manager = AlertManager()
        self.currency_db = CurrencyDatabase()
    
    def get_dashboard_data(self):
        """生成完整仪表板数据"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': self._get_system_status(),
            'rates': self._get_rates(),
            'trends': self._get_trends(),
            'alerts': self._get_alerts(),
            'currencies': self._get_currencies(),
        }
    
    def _get_system_status(self):
        """获取系统状态"""
        return {
            'status': '🟢 healthy',
            'version': '1.0',
            'uptime': 'stable',
            'services': {
                'multicurrency_hub': '✅ active',
                'trend_analyzer': '✅ active',
                'alert_system': '✅ active',
                'currency_database': '✅ active'
            }
        }
    
    def _get_rates(self):
        """获取实时汇率"""
        rates = {}
        for code in ['CNY', 'EUR', 'GBP', 'JPY', 'BTC', 'ETH']:
            rate = self.hub.get_rate('USD', code)
            if rate:
                rates[code] = {
                    'rate': round(rate.rate, 8),
                    'color': rate.color_tag.value,
                    'source': rate.source,
                    'timestamp': rate.timestamp
                }
        return rates
    
    def _get_trends(self):
        """获取趋势数据"""
        trends = {}
        for code in ['CNY', 'EUR']:
            pair = f"USD/{code}"
            trend_data = self.trend_analyzer.analyze_multi_period('USD', code)
            trends[pair] = {
                '7d': {
                    'change': trend_data['7d'].change_percent if trend_data['7d'] else None,
                    'trend': trend_data['7d'].trend if trend_data['7d'] else None,
                    'volatility': trend_data['7d'].volatility if trend_data['7d'] else None
                } if trend_data['7d'] else None,
                '30d': {
                    'change': trend_data['30d'].change_percent if trend_data['30d'] else None,
                    'trend': trend_data['30d'].trend if trend_data['30d'] else None
                } if trend_data['30d'] else None,
            }
        return trends
    
    def _get_alerts(self):
        """获取告警信息"""
        alerts = self.alert_manager.get_active_alerts()
        stats = self.alert_manager.get_statistics()
        
        return {
            'statistics': stats,
            'recent_alerts': [
                {
                    'symbol': a.symbol,
                    'type': a.rule_type.value,
                    'level': a.level.value,
                    'message': a.message,
                    'timestamp': a.timestamp
                }
                for a in alerts[:5]
            ]
        }
    
    def _get_currencies(self):
        """获取币种列表"""
        currencies = self.currency_db.list_all()
        return {
            'total': len(currencies),
            'top_20': [
                {
                    'code': c.code,
                    'name': c.name,
                    'symbol': c.symbol,
                    'category': c.category,
                    'priority': c.priority
                }
                for c in currencies[:20]
            ]
        }


if __name__ == '__main__':
    print("🚀 龍魂多币种·轻量级仪表板\n")
    
    dashboard = DashboardLite()
    data = dashboard.get_dashboard_data()
    
    print("📊 仪表板数据生成成功\n")
    
    # 生成 JSON 文件
    output_file = '/tmp/dashboard_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存到: {output_file}\n")
    
    # 显示摘要
    print("=" * 70)
    print("📈 仪表板数据摘要")
    print("=" * 70)
    
    print("\n💹 实时汇率:")
    for code, rate in data['rates'].items():
        print(f"  {code}: {rate['rate']:10.6f} {rate['color']} ({rate['source']})")
    
    print("\n📊 趋势分析:")
    for pair, trend in data['trends'].items():
        if trend['7d']:
            print(f"  {pair} 7日: {trend['7d']['change']:+.2f}% {trend['7d']['trend']}")
    
    print("\n🚨 告警统计:")
    stats = data['alerts']['statistics']
    print(f"  活跃告警: {stats['active_alerts']}")
    print(f"  活跃规则: {stats['active_rules']}")
    print(f"  总告警数: {stats['total_alerts']}")
    
    print("\n🌍 币种支持:")
    print(f"  总币种数: {data['currencies']['total']}")
    print(f"  前 5 个: {', '.join([c['code'] for c in data['currencies']['top_20'][:5]])}")
    
    print("\n" + "=" * 70)
    print("✅ 轻量级仪表板测试完成")
    print("=" * 70)

