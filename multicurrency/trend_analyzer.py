#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·趋势分析引擎 v1.0
DNA:#龍芯⚡️2026-06-07-TREND-ANALYZER-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7日/30日/90日趋势·移动平均·异常检测
"""

import os
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Tuple
import statistics

@dataclass
class TrendData:
    """趋势数据"""
    symbol: str
    period: str           # '7d', '30d', '90d'
    current_price: float
    avg_price: float
    high_price: float
    low_price: float
    change_percent: float
    volatility: float     # 标准差
    trend: str            # 'UP', 'DOWN', 'STABLE'

class TrendAnalyzer:
    """趋势分析引擎"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.expanduser('~/.龍魂/multicurrency.db')
    
    def _get_historical_prices(self, base: str, target: str, days: int) -> List[float]:
        """获取历史价格"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT rate FROM exchange_rates
                WHERE base_currency = ? AND target_currency = ?
                AND timestamp >= ?
                ORDER BY timestamp
            ''', (base, target, start_date.isoformat()))
            
            prices = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return prices
        except Exception as e:
            print(f"❌ 获取历史价格失败: {e}")
            return []
    
    def analyze_trend(self, base: str, target: str, days: int = 7) -> TrendData:
        """分析趋势"""
        prices = self._get_historical_prices(base, target, days)
        
        if not prices:
            return None
        
        current = prices[-1] if prices else 0
        avg = statistics.mean(prices) if prices else 0
        high = max(prices) if prices else 0
        low = min(prices) if prices else 0
        volatility = statistics.stdev(prices) if len(prices) > 1 else 0
        
        # 计算变化百分比
        if avg > 0:
            change_percent = ((current - avg) / avg) * 100
        else:
            change_percent = 0
        
        # 判断趋势
        if change_percent > 2:
            trend = '📈 UP'
        elif change_percent < -2:
            trend = '📉 DOWN'
        else:
            trend = '➡️  STABLE'
        
        period_map = {7: '7d', 30: '30d', 90: '90d'}
        
        return TrendData(
            symbol=f"{base}/{target}",
            period=period_map.get(days, f"{days}d"),
            current_price=round(current, 8),
            avg_price=round(avg, 8),
            high_price=round(high, 8),
            low_price=round(low, 8),
            change_percent=round(change_percent, 2),
            volatility=round(volatility, 8),
            trend=trend
        )
    
    def analyze_multi_period(self, base: str, target: str) -> Dict[str, TrendData]:
        """分析多个时期的趋势"""
        return {
            '7d': self.analyze_trend(base, target, days=7),
            '30d': self.analyze_trend(base, target, days=30),
            '90d': self.analyze_trend(base, target, days=90),
        }
    
    def detect_anomalies(self, base: str, target: str, days: int = 30) -> List[Tuple[str, float]]:
        """检测异常值 (±2σ)"""
        prices = self._get_historical_prices(base, target, days)
        
        if len(prices) < 3:
            return []
        
        mean = statistics.mean(prices)
        stdev = statistics.stdev(prices)
        threshold = 2 * stdev
        
        anomalies = [
            (i, price) for i, price in enumerate(prices)
            if abs(price - mean) > threshold
        ]
        
        return anomalies


# 测试
if __name__ == '__main__':
    analyzer = TrendAnalyzer()
    
    print("📊 趋势分析测试:\n")
    
    # 创建测试数据
    conn = sqlite3.connect(analyzer.db_path)
    cursor = conn.cursor()
    
    # 生成7天的模拟数据 (如果不存在)
    import random
    base_rate = 7.0
    for i in range(7):
        rate = base_rate + random.uniform(-0.1, 0.1)
        timestamp = (datetime.now() - timedelta(days=7-i)).isoformat()
        cursor.execute('''
            INSERT OR IGNORE INTO exchange_rates
            (base_currency, target_currency, rate, timestamp, source, color_tag, deviation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('USD', 'CNY', rate, timestamp, 'test', '🟢', 0.5))
    
    conn.commit()
    conn.close()
    
    # 分析趋势
    trend_7d = analyzer.analyze_trend('USD', 'CNY', days=7)
    if trend_7d:
        print(f"🔍 {trend_7d.symbol} (7日)")
        print(f"  当前: {trend_7d.current_price}")
        print(f"  均价: {trend_7d.avg_price}")
        print(f"  高低: {trend_7d.high_price} / {trend_7d.low_price}")
        print(f"  变化: {trend_7d.change_percent}%")
        print(f"  波动: {trend_7d.volatility}")
        print(f"  趋势: {trend_7d.trend}\n")
    
    print("✅ Phase C.2: 趋势分析引擎完成")

