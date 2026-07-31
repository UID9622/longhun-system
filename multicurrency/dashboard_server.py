# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·Web 仪表板 v1.0
DNA:#龍芯⚡️2026-06-07-DASHBOARD-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flask Web 服务器·实时数据更新·可视化仪表板
"""

from flask import Flask, render_template_string, jsonify  # type: ignore[import-untyped]
from flask_cors import CORS  # type: ignore[import-untyped]
import json
import os
from datetime import datetime
from multicurrency_service import MultiCurrencyHub
from trend_analyzer import TrendAnalyzer
from alert_system import AlertManager
from currency_database import CurrencyDatabase

app = Flask(__name__)
CORS(app)

# 初始化组件
hub = MultiCurrencyHub(use_real_sources=True)
trend_analyzer = TrendAnalyzer()
alert_manager = AlertManager()
currency_db = CurrencyDatabase()

# ═══════════════════════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════════════════════

@app.route('/api/v1/rates', methods=['GET'])
def get_rates():
    """获取实时汇率"""
    rates = hub.get_all_rates('USD')
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'base': 'USD',
        'rates': {
            code: {
                'rate': rate.rate,
                'color': rate.color_tag.value,
                'source': rate.source
            }
            for code, rate in rates.items()
        }
    })

@app.route('/api/v1/trends/<base>/<target>', methods=['GET'])
def get_trend(base, target):
    """获取趋势分析"""
    trends = trend_analyzer.analyze_multi_period(base, target)
    return jsonify({
        'symbol': f'{base}/{target}',
        '7d': {
            'change': trends['7d'].change_percent,
            'trend': trends['7d'].trend
        } if trends['7d'] else None,
        '30d': {
            'change': trends['30d'].change_percent,
            'trend': trends['30d'].trend
        } if trends['30d'] else None,
        '90d': {
            'change': trends['90d'].change_percent,
            'trend': trends['90d'].trend
        } if trends['90d'] else None,
    })

@app.route('/api/v1/alerts', methods=['GET'])
def get_alerts():
    """获取活跃告警"""
    alerts = alert_manager.get_active_alerts()
    stats = alert_manager.get_statistics()
    return jsonify({
        'alerts': [
            {
                'symbol': a.symbol,
                'type': a.rule_type.value,
                'level': a.level.value,
                'message': a.message,
                'timestamp': a.timestamp
            }
            for a in alerts[:10]
        ],
        'statistics': stats
    })

@app.route('/api/v1/currencies', methods=['GET'])
def get_currencies():
    """获取币种列表"""
    currencies = currency_db.list_all()
    return jsonify({
        'total': len(currencies),
        'currencies': [
            {
                'code': c.code,
                'name': c.name,
                'symbol': c.symbol,
                'category': c.category,
                'priority': c.priority
            }
            for c in currencies[:20]
        ]
    })

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'services': {
            'multicurrency_hub': 'active',
            'trend_analyzer': 'active',
            'alert_system': 'active'
        }
    })

# ═══════════════════════════════════════════════════════════
# 前端页面
# ═══════════════════════════════════════════════════════════

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂多币种·仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #333;
        }
        
        .rate-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .rate-item:last-child { border-bottom: none; }
        
        .rate-code {
            font-weight: 600;
            color: #667eea;
        }
        
        .rate-value {
            font-size: 0.9em;
            color: #666;
        }
        
        .alert {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid;
        }
        
        .alert-info { background: #e3f2fd; border-color: #2196f3; }
        .alert-warning { background: #fff3e0; border-color: #ff9800; }
        .alert-critical { background: #ffebee; border-color: #f44336; }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        
        .stat-box {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.8em;
            font-weight: 600;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #999;
            margin-top: 5px;
        }
        
        .status {
            color: #4caf50;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 龍魂多币种·实时仪表板</h1>
            <p>实时汇率 · 趋势分析 · 价格告警</p>
        </div>
        
        <div class="grid">
            <!-- 实时汇率 -->
            <div class="card">
                <h2>📊 实时汇率</h2>
                <div id="rates-container">加载中...</div>
            </div>
            
            <!-- 告警系统 -->
            <div class="card">
                <h2>🚨 活跃告警</h2>
                <div id="alerts-container">加载中...</div>
            </div>
            
            <!-- 系统状态 -->
            <div class="card">
                <h2>💚 系统状态</h2>
                <div id="health-container">加载中...</div>
            </div>
        </div>
    </div>
    
    <script>
        // 获取实时汇率
        fetch('/api/v1/rates')
            .then(r => r.json())
            .then(data => {
                const html = Object.entries(data.rates || {})
                    .slice(0, 6)
                    .map(([code, info]) => `
                        <div class="rate-item">
                            <span class="rate-code">${code}</span>
                            <span class="rate-value">${info.rate.toFixed(4)}</span>
                        </div>
                    `).join('');
                document.getElementById('rates-container').innerHTML = html || '暂无数据';
            })
            .catch(e => console.error(e));
        
        // 获取告警
        fetch('/api/v1/alerts')
            .then(r => r.json())
            .then(data => {
                if (data.alerts.length === 0) {
                    document.getElementById('alerts-container').innerHTML = '✅ 无活跃告警';
                } else {
                    const html = data.alerts
                        .slice(0, 3)
                        .map(a => `
                            <div class="alert alert-warning">
                                <strong>${a.symbol}</strong> - ${a.message}
                            </div>
                        `).join('');
                    document.getElementById('alerts-container').innerHTML = html;
                }
                
                // 显示统计
                const stats = data.statistics;
                const statsHtml = `
                    <div class="stats">
                        <div class="stat-box">
                            <div class="stat-value">${stats.active_alerts || 0}</div>
                            <div class="stat-label">活跃告警</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${stats.active_rules || 0}</div>
                            <div class="stat-label">活跃规则</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">100%</div>
                            <div class="stat-label">系统运行率</div>
                        </div>
                    </div>
                `;
                document.getElementById('health-container').innerHTML = statsHtml;
            })
            .catch(e => console.error(e));
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """主页面"""
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🌐 龍魂多币种·Web 仪表板启动")
    print("📍 访问地址: http://localhost:5000")
    print("📊 API 文档: http://localhost:5000/api/v1/health")
    
    app.run(debug=False, port=5000, host='127.0.0.1')

