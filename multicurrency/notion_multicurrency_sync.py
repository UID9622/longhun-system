#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多币种·Notion 实时同步 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA:#龍芯⚡️2026-06-07-NOTION-MULTICURRENCY-SYNC-v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能: 5 分钟实时同步汇率到 Notion·自动更新色标签·错误恢复

用法:
  python3 notion_multicurrency_sync.py --watch      # 5 分钟循环同步
  python3 notion_multicurrency_sync.py --once       # 执行一次同步
  python3 notion_multicurrency_sync.py --status     # 显示同步状态
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

# 导入本地模块
from multicurrency_service import MultiCurrencyHub, ExchangeRate

# ═══════════════════════════════════════════════════════════════
# 日志配置
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
    """Notion API 客户端"""

    def __init__(self):
        self.token = getenv('NOTION_TOKEN', '')
        self.database_id = getenv('DB_AL', '')
        self.api_version = '2022-06-28'
        self.base_url = 'https://api.notion.com/v1'
        self.timeout = 10

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.token) and bool(self.database_id)

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Optional[Dict]:
        """发送 Notion API 请求"""
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
            logger.error(f"Notion API 网络错误: {str(e)}")
        except Exception as e:
            logger.error(f"Notion API 错误: {str(e)}")

        return None

    def query_database(self, filter_obj: Dict = None) -> Optional[List[Dict]]:
        """查询 Notion 数据库"""
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
        """取得页面信息"""
        return self._make_request('GET', f'/pages/{page_id}')

    def update_page(self, page_id: str, properties: Dict) -> bool:
        """更新页面属性"""
        data = {
            'properties': properties
        }
        response = self._make_request('PATCH', f'/pages/{page_id}', data)
        return response is not None

    def create_page(self, properties: Dict) -> Optional[str]:
        """在数据库中创建新页面"""
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
    """Notion 多币种同步管理器"""

    def __init__(self):
        self.hub = MultiCurrencyHub(use_real_sources=True)
        self.notion_api = NotionAPI()
        self.db_path = os.path.expanduser('~/.龍魂/notion_sync.db')
        self._init_db()

        # 统计信息
        self.sync_count = 0
        self.success_count = 0
        self.error_count = 0
        self.last_sync_time = None

    def _init_db(self):
        """初始化同步纪录数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 同步纪录表
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

        # 页面映射表
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
        """取得或创建币种对的 Notion 页面"""
        pair = f"{base}/{target}"

        # 检查本地映射
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT notion_page_id FROM page_mappings WHERE pair = ?', (pair,))
        row = cursor.fetchone()

        if row:
            conn.close()
            return row[0]

        # 若未找到·尝试查询 Notion
        if not self.notion_api.is_configured():
            logger.warning(f"Notion 未配置·无法同步 {pair}")
            conn.close()
            return None

        pages = self.notion_api.query_database({
            'property': '币种对',
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

        # 创建新页面
        properties = {
            '币种对': {
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
        """同步单个币种对的汇率"""
        try:
            # 从 Hub 获取汇率
            rate_obj = self.hub.get_rate(base, target)
            if not rate_obj:
                logger.warning(f"无法获取 {base}/{target} 汇率")
                self.error_count += 1
                return False

            # 取得或创建 Notion 页面
            page_id = self._get_or_create_page(base, target)
            if not page_id:
                logger.warning(f"无法创建/取得 {base}/{target} 的 Notion 页面")
                self.error_count += 1
                return False

            # 准备 Notion 属性
            properties = {
                '汇率': {
                    'number': rate_obj.rate
                },
                '基础币': {
                    'select': {
                        'name': base
                    }
                },
                '目标币': {
                    'select': {
                        'name': target
                    }
                },
                '状态': {
                    'status': {
                        'name': rate_obj.color_tag.value + ' ' + self._get_status_name(rate_obj.color_tag.value)
                    }
                },
                '偏离': {
                    'number': rate_obj.deviation
                },
                '数据源': {
                    'select': {
                        'name': rate_obj.source
                    }
                },
                '更新时间': {
                    'date': {
                        'start': rate_obj.timestamp.split('T')[0]
                    }
                },
                '备注': {
                    'rich_text': [
                        {
                            'text': {
                                'content': f'自动同步·时间: {rate_obj.timestamp}'
                            }
                        }
                    ]
                }
            }

            # 更新 Notion 页面
            if self.notion_api.update_page(page_id, properties):
                # 记录同步
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
                logger.error(f"❌ Notion 更新失败: {base}/{target}")
                return False

        except Exception as e:
            logger.error(f"❌ 同步异常 {base}/{target}: {str(e)}")
            self.error_count += 1
            return False

    def _get_status_name(self, color_tag: str) -> str:
        """根据颜色标签返回状态名称"""
        if color_tag == '🟢':
            return '正常'
        elif color_tag == '🟡':
            return '波动'
        elif color_tag == '🔴':
            return '异常'
        return '未知'

    def sync_all(self) -> Dict:
        """同步所有支持的币种对"""
        logger.info("=" * 70)
        logger.info("🔄 开始多币种同步")
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
        logger.info(f"✅ 同步完成: {self.success_count} 成功, {self.error_count} 失败")
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
        """取得同步状态"""
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
    parser = argparse.ArgumentParser(description="🐉 龍魂多币种·Notion 实时同步 v1.0")

    parser.add_argument('--watch', action='store_true', help='5 分钟循环同步')
    parser.add_argument('--once', action='store_true', help='执行一次同步')
    parser.add_argument('--status', action='store_true', help='显示同步状态')
    parser.add_argument('--interval', type=int, default=300, help='同步间隔秒数 (默认 300)')

    args = parser.parse_args()

    manager = NotionMulticurrencySyncManager()

    print("🐉 龍魂多币种·Notion 实时同步 v1.0")
    print("DNA:#龍芯⚡️2026-06-07-NOTION-MULTICURRENCY-SYNC-v1.0\n")

    if args.watch:
        print(f"⏱️  进入监视模式·每 {args.interval} 秒同步一次\n")
        try:
            while True:
                result = manager.sync_all()
                print(f"\n⏳ 等待 {args.interval} 秒...")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n⏹️  用户中断")

    elif args.once:
        result = manager.sync_all()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.status:
        status = manager.get_status()
        print("📊 同步状态:")
        print(f"  Notion 配置: {'✅ 已配置' if status['notion_configured'] else '❌ 未配置'}")
        print(f"  Hub 初始化: {'✅ 已初始化' if status['hub_initialized'] else '❌ 失败'}")
        print(f"  同步次数: {status['sync_count']}")
        print(f"  成功: {status['success_count']}")
        print(f"  失败: {status['error_count']}")
        print(f"  成功率: {status['success_rate']}%")
        if status['last_sync_time']:
            print(f"  最后同步: {status['last_sync_time']}")

    else:
        print("用法: python3 notion_multicurrency_sync.py [OPTIONS]")
        print("  --watch                监视模式 (5 分钟循环)")
        print("  --once                 执行一次同步")
        print("  --status               显示同步状态")
        print("  --interval SECONDS     自定义同步间隔 (默认 300 秒)")

if __name__ == '__main__':
    main()
