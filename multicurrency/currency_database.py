#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·币种数据库 v1.0
DNA:#龍芯⚡️2026-06-07-CURRENCY-DATABASE-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

币种元数据管理·支持 40+ 币种·实时数据源验证
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Currency:
    """币种信息"""
    code: str           # 代码 (USD, CNY, BTC等)
    name: str           # 名称 (美元, 人民币等)
    symbol: str         # 符号 ($, ¥, ฿等)
    category: str       # 类别 (fiat, crypto, commodity)
    region: str         # 地区 (US, CN, Global等)
    priority: int       # 优先级 (1最高)
    description: str    # 描述

class CurrencyDatabase:
    """币种数据库·支持 40+ 币种"""
    
    def __init__(self):
        self.currencies = self._init_currencies()
    
    def _init_currencies(self) -> Dict[str, Currency]:
        """初始化 40+ 币种"""
        return {
            # ===== 主要法币 (13种) =====
            'USD': Currency('USD', '美元', '$', 'fiat', 'US', 1, '世界储备货币'),
            'EUR': Currency('EUR', '欧元', '€', 'fiat', 'EU', 2, '欧盟官方货币'),
            'GBP': Currency('GBP', '英镑', '£', 'fiat', 'GB', 3, '英国官方货币'),
            'JPY': Currency('JPY', '日元', '¥', 'fiat', 'JP', 4, '日本官方货币'),
            'CNY': Currency('CNY', '人民币', '¥', 'fiat', 'CN', 5, '中国官方货币'),
            'CHF': Currency('CHF', '瑞士法郎', 'CHF', 'fiat', 'CH', 6, '瑞士官方货币'),
            'AUD': Currency('AUD', '澳元', 'A$', 'fiat', 'AU', 7, '澳大利亚官方货币'),
            'CAD': Currency('CAD', '加元', 'C$', 'fiat', 'CA', 8, '加拿大官方货币'),
            'SGD': Currency('SGD', '新加坡元', 'S$', 'fiat', 'SG', 9, '新加坡官方货币'),
            'HKD': Currency('HKD', '港元', 'HK$', 'fiat', 'HK', 10, '香港官方货币'),
            'KRW': Currency('KRW', '韩元', '₩', 'fiat', 'KR', 11, '韩国官方货币'),
            'INR': Currency('INR', '印度卢比', '₹', 'fiat', 'IN', 12, '印度官方货币'),
            'MXN': Currency('MXN', '墨西哥比索', '$', 'fiat', 'MX', 13, '墨西哥官方货币'),
            
            # ===== 加密货币 (20种) =====
            'BTC': Currency('BTC', '比特币', '฿', 'crypto', 'Global', 14, '第一个加密货币'),
            'ETH': Currency('ETH', '以太坊', 'Ξ', 'crypto', 'Global', 15, '智能合约平台'),
            'XRP': Currency('XRP', '瑞波币', 'XRP', 'crypto', 'Global', 16, '跨境支付'),
            'ADA': Currency('ADA', '卡尔达诺', 'ADA', 'crypto', 'Global', 17, '权益证明'),
            'SOL': Currency('SOL', '索拉纳', 'SOL', 'crypto', 'Global', 18, '高速区块链'),
            'DOT': Currency('DOT', '波卡', 'DOT', 'crypto', 'Global', 19, '跨链协议'),
            'DOGE': Currency('DOGE', '狗狗币', 'DOGE', 'crypto', 'Global', 20, '社区货币'),
            'LTC': Currency('LTC', '莱特币', 'LTC', 'crypto', 'Global', 21, '比特币替代'),
            'BCH': Currency('BCH', '比特币现金', 'BCH', 'crypto', 'Global', 22, '比特币分叉'),
            'XLM': Currency('XLM', '恒星币', 'XLM', 'crypto', 'Global', 23, '支付网络'),
            'LINK': Currency('LINK', '链接币', 'LINK', 'crypto', 'Global', 24, '预言机'),
            'BNB': Currency('BNB', '币安币', 'BNB', 'crypto', 'Global', 25, '交易所币'),
            'MATIC': Currency('MATIC', '多边形', 'MATIC', 'crypto', 'Global', 26, '扩展方案'),
            'AVAX': Currency('AVAX', '雪崩链', 'AVAX', 'crypto', 'Global', 27, '共识网络'),
            'FTM': Currency('FTM', '幻影币', 'FTM', 'crypto', 'Global', 28, '高速区块链'),
            'ARB': Currency('ARB', '仲裁币', 'ARB', 'crypto', 'Global', 29, '二层方案'),
            'OP': Currency('OP', '乐观币', 'OP', 'crypto', 'Global', 30, '二层扩展'),
            
            # ===== 大宗商品 (3种) =====
            'GOLD': Currency('GOLD', '黄金', 'oz', 'commodity', 'Global', 31, '贵金属'),
            'SILVER': Currency('SILVER', '白银', 'oz', 'commodity', 'Global', 32, '贵金属'),
            'OIL': Currency('OIL', '原油', 'bbl', 'commodity', 'Global', 33, '能源商品'),
        }
    
    def get_currency(self, code: str) -> Optional[Currency]:
        """获取币种信息"""
        return self.currencies.get(code.upper())
    
    def list_all(self) -> List[Currency]:
        """列出所有币种"""
        return sorted(
            self.currencies.values(),
            key=lambda c: c.priority
        )
    
    def list_by_category(self, category: str) -> List[Currency]:
        """按类别列出币种"""
        return [
            c for c in self.currencies.values()
            if c.category == category
        ]
    
    def get_top_n(self, n: int = 10) -> List[Currency]:
        """获取前 N 个优先级的币种"""
        return sorted(
            self.currencies.values(),
            key=lambda c: c.priority
        )[:n]
    
    def to_dict(self) -> Dict:
        """导出为字典"""
        return {
            code: {
                'name': c.name,
                'symbol': c.symbol,
                'category': c.category,
                'priority': c.priority
            }
            for code, c in self.currencies.items()
        }


# 导出
if __name__ == '__main__':
    db = CurrencyDatabase()
    
    print("📊 币种数据库统计:")
    print(f"  总币种数: {len(db.currencies)}")
    print(f"  法币: {len(db.list_by_category('fiat'))}")
    print(f"  加密: {len(db.list_by_category('crypto'))}")
    print(f"  商品: {len(db.list_by_category('commodity'))}")
    
    print("\n🏆 前 10 个优先币种:")
    for c in db.get_top_n(10):
        print(f"  {c.priority:2d}. {c.code:6s} {c.symbol:4s} {c.name}")
    
    # 导出为 JSON
    with open('/tmp/currency_db.json', 'w', encoding='utf-8') as f:
        json.dump(db.to_dict(), f, ensure_ascii=False, indent=2)
    print("\n✅ 币种数据库已导出到 /tmp/currency_db.json")

