#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多幣種·Notion 實時同步 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-NOTION-MULTICURRENCY-SYNC-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 5 分鐘實時同步匯率到 Notion·自動更新色標籤·錯誤恢復

用法:
  python3 notion_multicurrency_sync.py --watch      # 5 分鐘循環同步
  python3 notion_multicurrency_sync.py --once       # 執行一次同步
  python3 notion_multicurrency_sync.py --status     # 顯示同步狀態
"""

import os
import json
import time
import sqlite3
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import asdict
import urllib.request
import urllib.error
import argparse

# 導入本地模塊
from multicurrency_service import MultiCurrencyHub, ExchangeRate

# ═══════════════════════════════════════════════════════════════
# 日誌配置
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.龍魂/notion_multicurrency_sync.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# Notion API 配置和工具
# ═══════════════════════════════════════════════════════════════

from integrated_modules.longhun_config import getenv


class NotionAPI:
    """Notion API 客戶端"""

    def __init__(self):
        self.token = getenv('NOTION_TOKEN', '')
        self.database_id = getenv('DB_AL', '')
        self.api_version = '2022-06-28'
        self.base_url = 'https://api.notion.com/v1'
        self.timeout = 10

    def is_configured(self) -> bool:
        """檢查是否已配置"""
        return bool(self.token) and bool(self.database_id)

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Optional[Dict]:
        """發送 Notion API 請求"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Notion-Version': self.api_version,
                'Content-Type': 'application/json'
            }

            if data:
                body = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=body, headers=headers, method=method)
            else:
                req = urllib.request.Request(url, headers=headers, method=method)

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))

        except urllib.error.URLError as e:
            logger.error(f"Notion API 網絡錯誤: {str(e)}")
        except Exception as e:
            logger.error(f"Notion API 錯誤: {str(e)}")

        return None

    def query_database(self, filter_obj: Dict = None) -> Optional[List[Dict]]:
        """查詢 Notion 數據庫"""
        data = {
            'page_size': 100
        }
        if filter_obj:
            data['filter'] = filter_obj

        response = self._make_request('POST', f'/databases/{self.database_id}/query', data)
        if response:
            return response.get('results', [])
        return None

    def get_page(self, page_id: str) -> Optional[Dict]:
        """取得頁面信息"""
        return self._make_request('GET', f'/pages/{page_id}')

    def update_page(self, page_id: str, properties: Dict) -> bool:
        """更新頁面屬性"""
        data = {
            'properties': properties
        }
        response = self._make_request('PATCH', f'/pages/{page_id}', data)
        return response is not None

    def create_page(self, properties: Dict) -> Optional[str]:
        """在數據庫中創建新頁面"""
        data = {
            'parent': {'database_id': self.database_id},
            'properties': properties
        }
        response = self._make_request('POST', '/pages', data)
        if response:
            return response.get('id')
        return None

# ═══════════════════════════════════════════════════════════════
# 同步管理器
# ═══════════════════════════════════════════════════════════════

class NotionMulticurrencySyncManager:
    """Notion 多幣種同步管理器"""

    def __init__(self):
        self.hub = MultiCurrencyHub(use_real_sources=True)
        self.notion_api = NotionAPI()
        self.db_path = os.path.expanduser('~/.龍魂/notion_sync.db')
        self._init_db()

        # 統計信息
        self.sync_count = 0
        self.success_count = 0
        self.error_count = 0
        self.last_sync_time = None

    def _init_db(self):
        """初始化同步紀錄數據庫"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 同步紀錄表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY,
                pair TEXT NOT NULL,
                notion_page_id TEXT,
                rate REAL,
                source TEXT,
                sync_time TEXT,
                status TEXT
            )
        ''')

        # 頁面映射表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_mappings (
                id INTEGER PRIMARY KEY,
                pair TEXT UNIQUE NOT NULL,
                notion_page_id TEXT NOT NULL,
                created_time TEXT,
                last_sync TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def _get_or_create_page(self, base: str, target: str) -> Optional[str]:
        """取得或創建幣種對的 Notion 頁面"""
        pair = f"{base}/{target}"

        # 檢查本地映射
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT notion_page_id FROM page_mappings WHERE pair = ?', (pair,))
        row = cursor.fetchone()

        if row:
            conn.close()
            return row[0]

        # 若未找到·嘗試查詢 Notion
        if not self.notion_api.is_configured():
            logger.warning(f"Notion 未配置·無法同步 {pair}")
            conn.close()
            return None

        pages = self.notion_api.query_database({
            'property': '幣種對',
            'title': {
                'equals': pair
            }
        })

        if pages:
            page_id = pages[0]['id']
            # 保存到本地映射
            cursor.execute('''
                INSERT OR REPLACE INTO page_mappings (pair, notion_page_id, created_time)
                VALUES (?, ?, ?)
            ''', (pair, page_id, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return page_id

        # 創建新頁面
        properties = {
            '幣種對': {
                'title': [
                    {
                        'text': {
                            'content': pair
                        }
                    }
                ]
            }
        }

        page_id = self.notion_api.create_page(properties)
        if page_id:
            cursor.execute('''
                INSERT INTO page_mappings (pair, notion_page_id, created_time)
                VALUES (?, ?, ?)
            ''', (pair, page_id, datetime.now().isoformat()))
            conn.commit()

        conn.close()
        return page_id

    def sync_rate(self, base: str, target: str) -> bool:
        """同步單個幣種對的匯率"""
        try:
            # 從 Hub 獲取匯率
            rate_obj = self.hub.get_rate(base, target)
            if not rate_obj:
                logger.warning(f"無法獲取 {base}/{target} 匯率")
                self.error_count += 1
                return False

            # 取得或創建 Notion 頁面
            page_id = self._get_or_create_page(base, target)
            if not page_id:
                logger.warning(f"無法創建/取得 {base}/{target} 的 Notion 頁面")
                self.error_count += 1
                return False

            # 準備 Notion 屬性
            properties = {
                '匯率': {
                    'number': rate_obj.rate
                },
                '基礎幣': {
                    'select': {
                        'name': base
                    }
                },
                '目標幣': {
                    'select': {
                        'name': target
                    }
                },
                '狀態': {
                    'status': {
                        'name': rate_obj.color_tag.value + ' ' + self._get_status_name(rate_obj.color_tag.value)
                    }
                },
                '偏離': {
                    'number': rate_obj.deviation
                },
                '數據源': {
                    'select': {
                        'name': rate_obj.source
                    }
                },
                '更新時間': {
                    'date': {
                        'start': rate_obj.timestamp.split('T')[0]
                    }
                },
                '備註': {
                    'rich_text': [
                        {
                            'text': {
                                'content': f'自動同步·時間: {rate_obj.timestamp}'
                            }
                        }
                    ]
                }
            }

            # 更新 Notion 頁面
            if self.notion_api.update_page(page_id, properties):
                # 記錄同步
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sync_log (pair, notion_page_id, rate, source, sync_time, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (f"{base}/{target}", page_id, rate_obj.rate, rate_obj.source,
                      datetime.now().isoformat(), 'success'))

                cursor.execute('''
                    UPDATE page_mappings SET last_sync = ? WHERE pair = ?
                ''', (datetime.now().isoformat(), f"{base}/{target}"))

                conn.commit()
                conn.close()

                logger.info(f"✅ 同步成功: {base}/{target} = {rate_obj.rate} ({rate_obj.source})")
                self.success_count += 1
                return True
            else:
                self.error_count += 1
                logger.error(f"❌ Notion 更新失敗: {base}/{target}")
                return False

        except Exception as e:
            logger.error(f"❌ 同步異常 {base}/{target}: {str(e)}")
            self.error_count += 1
            return False

    def _get_status_name(self, color_tag: str) -> str:
        """根據顏色標籤返回狀態名稱"""
        if color_tag == '🟢':
            return '正常'
        elif color_tag == '🟡':
            return '波動'
        elif color_tag == '🔴':
            return '異常'
        return '未知'

    def sync_all(self) -> Dict:
        """同步所有支持的幣種對"""
        logger.info("=" * 70)
        logger.info("🔄 開始多幣種同步")
        logger.info("=" * 70)

        pairs = [
            ('USD', 'CNY'),
            ('USD', 'EUR'),
            ('USD', 'GBP'),
            ('USD', 'JPY'),
            ('USD', 'BTC'),
            ('USD', 'ETH'),
        ]

        self.sync_count += 1
        for base, target in pairs:
            self.sync_rate(base, target)

        self.last_sync_time = datetime.now()

        logger.info("=" * 70)
        logger.info(f"✅ 同步完成: {self.success_count} 成功, {self.error_count} 失敗")
        logger.info("=" * 70)

        return {
            'timestamp': datetime.now().isoformat(),
            'sync_count': self.sync_count,
            'success': self.success_count,
            'error': self.error_count,
            'success_rate': round(self.success_count / (self.success_count + self.error_count) * 100, 2)
            if (self.success_count + self.error_count) > 0 else 0
        }

    def get_status(self) -> Dict:
        """取得同步狀態"""
        return {
            'notion_configured': self.notion_api.is_configured(),
            'hub_initialized': self.hub is not None,
            'sync_count': self.sync_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
            'success_rate': round(self.success_count / (self.success_count + self.error_count) * 100, 2)
            if (self.success_count + self.error_count) > 0 else 0
        }

# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂多幣種·Notion 實時同步 v1.0")

    parser.add_argument('--watch', action='store_true', help='5 分鐘循環同步')
    parser.add_argument('--once', action='store_true', help='執行一次同步')
    parser.add_argument('--status', action='store_true', help='顯示同步狀態')
    parser.add_argument('--interval', type=int, default=300, help='同步間隔秒數 (默認 300)')

    args = parser.parse_args()

    manager = NotionMulticurrencySyncManager()

    print("🐉 龍魂多幣種·Notion 實時同步 v1.0")
    print("DNA:#龍芯⚡️2026-06-07-NOTION-MULTICURRENCY-SYNC-v1.0\n")

    if args.watch:
        print(f"⏱️  進入監視模式·每 {args.interval} 秒同步一次\n")
        try:
            while True:
                result = manager.sync_all()
                print(f"\n⏳ 等待 {args.interval} 秒...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n⏹️  用戶中斷")

    elif args.once:
        result = manager.sync_all()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.status:
        status = manager.get_status()
        print("📊 同步狀態:")
        print(f"  Notion 配置: {'✅ 已配置' if status['notion_configured'] else '❌ 未配置'}")
        print(f"  Hub 初始化: {'✅ 已初始化' if status['hub_initialized'] else '❌ 失敗'}")
        print(f"  同步次數: {status['sync_count']}")
        print(f"  成功: {status['success_count']}")
        print(f"  失敗: {status['error_count']}")
        print(f"  成功率: {status['success_rate']}%")
        if status['last_sync_time']:
            print(f"  最後同步: {status['last_sync_time']}")

    else:
        print("用法: python3 notion_multicurrency_sync.py [OPTIONS]")
        print("  --watch                監視模式 (5 分鐘循環)")
        print("  --once                 執行一次同步")
        print("  --status               顯示同步狀態")
        print("  --interval SECONDS     自定義同步間隔 (默認 300 秒)")

if __name__ == '__main__':
    main()
