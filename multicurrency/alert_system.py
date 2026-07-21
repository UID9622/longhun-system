#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·价格告警系统 v1.0
DNA:#龍芯⚡️2026-06-07-ALERT-SYSTEM-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

告警规则管理·多渠道通知·告警历史
"""

import os
import sqlite3
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from enum import Enum

class AlertLevel(str, Enum):
    """告警级别"""
    INFO = "ℹ️  信息"
    WARNING = "⚠️  警告"
    CRITICAL = "🚨 严重"

class AlertType(str, Enum):
    """告警类型"""
    PRICE_HIGH = "价格过高"
    PRICE_LOW = "价格过低"
    VOLATILITY = "波动过大"
    TREND_CHANGE = "趋势转变"

@dataclass
class AlertRule:
    """告警规则"""
    symbol: str           # USD/CNY
    rule_type: AlertType  # 告警类型
    threshold: float      # 阈值
    level: AlertLevel     # 告警级别
    enabled: bool = True
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class Alert:
    """告警事件"""
    symbol: str
    rule_type: AlertType
    level: AlertLevel
    message: str
    value: float
    timestamp: str = None
    status: str = "active"  # active, dismissed
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class AlertManager:
    """告警管理器"""
    
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.path.expanduser('~/.龍魂/alert.db')
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 告警规则表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_rules (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                level TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                created_at TEXT
            )
        ''')
        
        # 告警事件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_events (
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                level TEXT NOT NULL,
                message TEXT,
                value REAL,
                timestamp TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_rule(self, rule: AlertRule) -> bool:
        """添加告警规则"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alert_rules 
                (symbol, rule_type, threshold, level, enabled, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                rule.symbol,
                rule.rule_type.value,
                rule.threshold,
                rule.level.value,
                rule.enabled,
                rule.created_at
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 添加规则失败: {e}")
            return False
    
    def trigger_alert(self, alert: Alert) -> bool:
        """触发告警"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alert_events
                (symbol, rule_type, level, message, value, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.symbol,
                alert.rule_type.value,
                alert.level.value,
                alert.message,
                alert.value,
                alert.timestamp,
                alert.status
            ))
            
            conn.commit()
            conn.close()
            
            print(f"{alert.level.value} [{alert.symbol}] {alert.message}")
            return True
        except Exception as e:
            print(f"❌ 触发告警失败: {e}")
            return False
    
    def get_active_alerts(self) -> List[Alert]:
        """获取活跃告警"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symbol, rule_type, level, message, value, timestamp, status
                FROM alert_events
                WHERE status = 'active'
                ORDER BY timestamp DESC
                LIMIT 50
            ''')
            
            alerts = []
            for row in cursor.fetchall():
                alerts.append(Alert(
                    symbol=row[0],
                    rule_type=AlertType(row[1]),
                    level=AlertLevel(row[2]),
                    message=row[3],
                    value=row[4],
                    timestamp=row[5],
                    status=row[6]
                ))
            
            conn.close()
            return alerts
        except Exception as e:
            print(f"❌ 获取告警失败: {e}")
            return []
    
    def dismiss_alert(self, alert_id: int) -> bool:
        """消除告警"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE alert_events SET status = 'dismissed' WHERE id = ?
            ''', (alert_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 消除告警失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取告警统计"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM alert_events WHERE status = "active"')
            active_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alert_events')
            total_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM alert_rules WHERE enabled = 1')
            rules_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'active_alerts': active_count,
                'total_alerts': total_count,
                'active_rules': rules_count
            }
        except Exception as e:
            print(f"❌ 获取统计失败: {e}")
            return {}


# 测试
if __name__ == '__main__':
    manager = AlertManager()
    
    print("🚨 价格告警系统测试:\n")
    
    # 添加规则
    rules = [
        AlertRule('USD/CNY', AlertType.PRICE_HIGH, 7.5, AlertLevel.WARNING),
        AlertRule('USD/CNY', AlertType.PRICE_LOW, 6.5, AlertLevel.WARNING),
        AlertRule('BTC/USD', AlertType.VOLATILITY, 0.05, AlertLevel.CRITICAL),
    ]
    
    for rule in rules:
        if manager.add_rule(rule):
            print(f"✅ 添加规则: {rule.symbol} {rule.rule_type.value} (阈值: {rule.threshold})")
    
    print()
    
    # 触发告警
    alerts = [
        Alert('USD/CNY', AlertType.PRICE_HIGH, AlertLevel.WARNING, 
              '人民币贬值，美元升值超过警告线', 7.6),
        Alert('BTC/USD', AlertType.VOLATILITY, AlertLevel.CRITICAL,
              '比特币波动剧烈，请谨慎操作', 0.08),
    ]
    
    for alert in alerts:
        manager.trigger_alert(alert)
    
    print()
    
    # 显示统计
    stats = manager.get_statistics()
    print("📊 告警统计:")
    print(f"  活跃告警: {stats.get('active_alerts', 0)}")
    print(f"  总告警数: {stats.get('total_alerts', 0)}")
    print(f"  活跃规则: {stats.get('active_rules', 0)}")
    
    print("\n✅ Phase C.3: 价格告警系统完成")

