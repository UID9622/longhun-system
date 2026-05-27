#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂系統 · 配置讀取器 v1.0
Dragon Soul Configuration Manager

從統一的配置文件中讀取所有參數
所有服務都通過這個模塊獲取配置

使用方法：
  from 配置读取器 import get_config, CONFIG

  port = CONFIG.MAIN_API_PORT
  db_path = CONFIG.LOCAL_DB_PATH
"""

import os
from pathlib import Path
from typing import Optional

class SystemConfig:
    """系統配置管理器"""

    def __init__(self):
        self.config_file = Path(__file__).parent / ".longhunsystemconfig"
        self.config_dict = {}
        self.load_config()

    def load_config(self):
        """讀取配置文件"""
        if not self.config_file.exists():
            print(f"⚠️  配置文件不存在: {self.config_file}")
            print("   將使用默認值")
            self._set_defaults()
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # 跳過註釋和空行
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # 解析 KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # 類型轉換
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        elif value.replace('.', '', 1).isdigit():
                            value = float(value)

                        self.config_dict[key] = value

            print(f"✅ 配置文件已加載: {self.config_file}")

        except Exception as e:
            print(f"❌ 讀取配置文件失敗: {e}")
            self._set_defaults()

    def _set_defaults(self):
        """設置默認值"""
        self.config_dict = {
            # 統一入口
            'MAIN_API_HOST': '0.0.0.0',
            'MAIN_API_PORT': 8888,

            # 內部服務
            'CNSH_FASTAPI_PORT': 8000,
            'THREE_SYSTEM_API_PORT': 5000,
            'CNSH_TRANSLATOR_QUEUE_MODE': True,

            # 本地存儲
            'LOCAL_DB_PATH': '~/.longhun/work_records.db',
            'NOTION_CACHE_PATH': '~/.notion_cache',
            'LOG_PATH': '~/.longhun/logs',

            # Notion
            'NOTION_API_KEY': '',
            'NOTION_DATABASE_ID': '',

            # 服務控制
            'AUTO_START_CNSH_TRANSLATOR': True,
            'AUTO_START_FASTAPI': True,
            'AUTO_START_THREE_SYSTEM': True,

            # 日誌
            'LOG_LEVEL': 'INFO',
            'SAVE_LOG_TO_FILE': True,

            # 隊列
            'QUEUE_CHECK_INTERVAL': 0.5,
            'MAX_RETRIES': 3,

            # 性能
            'MAX_CONCURRENT_TASKS': 5,
            'MAX_QUEUE_LENGTH': 1000,

            # 安全
            'CORS_ORIGINS': '*',
            'API_AUTH_TOKEN': '',
        }

    def get(self, key: str, default=None):
        """獲取配置值"""
        value = self.config_dict.get(key, default)

        # 展開路徑中的 ~ 符號
        if isinstance(value, str) and value.startswith('~'):
            value = os.path.expanduser(value)

        return value

    def __getattr__(self, key: str):
        """允許用 CONFIG.KEY 的方式訪問"""
        value = self.get(key)
        if value is None:
            raise AttributeError(f"配置 {key} 不存在")
        return value

    def print_summary(self):
        """打印配置摘要"""
        print("\n" + "=" * 80)
        print("🐉 龍魂系統配置摘要")
        print("=" * 80)
        print(f"\n📍 統一入口:")
        print(f"   地址: http://localhost:{self.get('MAIN_API_PORT')}")
        print(f"   主機: {self.get('MAIN_API_HOST')}")

        print(f"\n🔌 內部服務:")
        print(f"   CNSH FastAPI: {self.get('CNSH_FASTAPI_PORT')}")
        print(f"   三系統 API: {self.get('THREE_SYSTEM_API_PORT')}")
        print(f"   CNSH 翻譯: 後台監聽")

        print(f"\n💾 本地存儲:")
        print(f"   數據庫: {self.get('LOCAL_DB_PATH')}")
        print(f"   緩存: {self.get('NOTION_CACHE_PATH')}")
        print(f"   日誌: {self.get('LOG_PATH')}")

        print(f"\n⚙️  服務控制:")
        print(f"   自動啟動翻譯: {self.get('AUTO_START_CNSH_TRANSLATOR')}")
        print(f"   自動啟動 FastAPI: {self.get('AUTO_START_FASTAPI')}")
        print(f"   自動啟動三系統: {self.get('AUTO_START_THREE_SYSTEM')}")

        notion_configured = bool(self.get('NOTION_API_KEY'))
        print(f"\n🌐 Notion 集成:")
        print(f"   配置狀態: {'✅ 已配置' if notion_configured else '⏹️  未配置（使用本地 SQLite）'}")

        print("\n" + "=" * 80)

    def validate(self):
        """驗證配置"""
        print("\n🔍 驗證配置...")

        issues = []

        # 檢查端口範圍
        port = self.get('MAIN_API_PORT')
        if not isinstance(port, int) or port < 1024 or port > 65535:
            issues.append(f"端口 {port} 無效（應在 1024-65535）")

        # 檢查路徑
        for path_key in ['LOCAL_DB_PATH', 'NOTION_CACHE_PATH', 'LOG_PATH']:
            path = Path(self.get(path_key))
            parent = path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                    print(f"  ✅ 已創建目錄: {parent}")
                except Exception as e:
                    issues.append(f"無法創建目錄 {parent}: {e}")

        if issues:
            print("\n⚠️  發現問題:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ 配置驗證通過")
            return True


# 全局配置實例
CONFIG = SystemConfig()


def get_config(key: str, default=None):
    """便捷函數：獲取配置"""
    return CONFIG.get(key, default)


def print_config_help():
    """打印配置幫助"""
    print("""
🐉 龍魂系統配置管理

【查看配置】
  cat ~/.longhunsystemconfig

【編輯配置】
  nano ~/.longhunsystemconfig

【重要配置項】

  MAIN_API_PORT=8888
    └─ 統一入口端口（最重要！）

  LOCAL_DB_PATH=~/.longhun/work_records.db
    └─ 本地任務數據庫

  NOTION_API_KEY=
    └─ Notion API 密鑰（可選）

  NOTION_DATABASE_ID=
    └─ Notion 數據庫 ID（可選）

【修改後】
  killall -9 python3
  python3 龍魂統一控制臺.py

【檢查當前配置】
  python3 -c "from 配置读取器 import CONFIG; CONFIG.print_summary()"
    """)


if __name__ == "__main__":
    # 直接運行此文件時，打印配置信息
    CONFIG.print_summary()
    CONFIG.validate()
    print_config_help()
