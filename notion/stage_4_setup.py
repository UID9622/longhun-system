#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 集成 · Stage 4 自動化設置

DNA: #龍芯⚇️2026-06-01-STAGE4-SETUP-v1.0
Purpose: 在 Notion 中創建審計日誌數據庫，配置環境變量，執行首次同步

Features:
  - 自動創建 4 個審計數據庫
  - 驗證 API 連接和權限
  - 保存數據庫 ID 到配置文件
  - 執行首次審計日誌同步
  - 生成配置報告
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager, NotionConfig
    from .notion_client import NotionClient, NotionAuthError
    from .audit_sync import AuditNotionSync
except ImportError:
    from notion_config import NotionConfigManager, NotionConfig
    from notion_client import NotionClient, NotionAuthError
    from audit_sync import AuditNotionSync


def print_header(title: str):
    """打印標題"""
    print("\n" + "=" * 70)
    print(f"🐉 {title}")
    print("=" * 70)


def step_1_verify_connection():
    """第一步：驗證連接"""
    print_header("第一步：驗證 Notion API 連接")

    manager = NotionConfigManager()
    try:
        config = manager.load()
    except ValueError as e:
        print(f"❌ {e}")
        return None

    try:
        client = NotionClient(config)
        if not client.test_connection():
            print("❌ 連接測試失敗")
            return None
        print("✅ API 連接正常")
        return client, config
    except NotionAuthError as e:
        print(f"❌ 認證失敗: {e}")
        return None
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return None


def step_2_get_workspace_info():
    """第二步：獲取工作區信息"""
    print_header("第二步：輸入 Notion 工作區信息")

    print("""
請提供要同步審計日誌的 Notion 頁面 ID（工作區 3）。

獲取方法：
1. 在 Notion 中打開要使用的頁面
2. 從瀏覽器地址欄複製 ID：
   https://www.notion.so/YOUR_WORKSPACE_ID?v=...

提取規則：移除所有連字符，例如：
   原: 34d7-125a-9c9f-81d2-be91-d1e3-e3be-34eb
   ID: 34d7125a9c9f81d2be91d1e3e3be34eb

提示：可以與 Stage 2-3 使用不同的工作區，或共享同一個工作區。
    """)

    workspace_3 = input("工作區 3 ID (龍魂審計日誌): ").strip()
    if not workspace_3:
        print("❌ 工作區 ID 不能為空")
        return None

    return workspace_3


def step_3_create_databases(client: NotionClient, workspace_id: str) -> Dict[str, str]:
    """第三步：創建數據庫"""
    print_header("第三步：在 Notion 中創建審計日誌數據庫")

    databases = {
        "健康檢查日誌": {
            "名稱": {"title": {}},
            "狀態": {"rich_text": {}},
            "檢查項數": {"number": {}},
            "DNA": {"rich_text": {}},
        },
        "性能基線": {
            "數字根": {"title": {}},
            "記錄數": {"number": {}},
            "顏色": {"rich_text": {}},
            "DNA": {"rich_text": {}},
        },
        "警告事件": {
            "嚴重性": {"title": {}},
            "事件數": {"number": {}},
            "說明": {"rich_text": {}},
            "DNA": {"rich_text": {}},
        },
        "審計日誌": {
            "操作": {"title": {}},
            "計數": {"number": {}},
            "狀態": {"rich_text": {}},
            "DNA": {"rich_text": {}},
        },
    }

    created_dbs = {}

    for db_name, properties in databases.items():
        try:
            print(f"\n📁 創建: {db_name}...")

            result = client.create_database(
                parent_id=workspace_id,
                title=db_name,
                properties=properties,
            )

            db_id = result.get('id', '')
            if db_id:
                created_dbs[db_name] = db_id
                print(f"   ✅ 創建成功")
                print(f"   ID: {db_id}")
            else:
                print(f"   ❌ 創建失敗：未獲得數據庫 ID")

        except Exception as e:
            print(f"   ❌ 創建失敗: {str(e)[:100]}")

    return created_dbs


def step_4_save_config(created_dbs: Dict[str, str]):
    """第四步：保存配置"""
    print_header("第四步：保存配置到環境變量")

    config_lines = []

    # 映射數據庫名稱到環境變量
    mapping = {
        "健康檢查日誌": "NOTION_HEALTH_DB",
        "性能基線": "NOTION_BASELINE_DB",
        "警告事件": "NOTION_ALERT_DB",
        "審計日誌": "NOTION_AUDIT_DB",
    }

    print("\n請運行以下命令設置環境變量：\n")
    for db_name, env_var in mapping.items():
        db_id = created_dbs.get(db_name, "")
        if db_id:
            config_lines.append(f"export {env_var}='{db_id}'")
            print(f"export {env_var}='{db_id}'")

    # 保存到配置文件
    config_file = Path.home() / ".龍魂_config" / "audit_databases.sh"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# 審計日誌數據庫 ID 配置\n")
        f.write(f"# 生成於: {datetime.now().isoformat()}\n\n")
        for line in config_lines:
            f.write(line + "\n")

    print(f"\n✅ 配置已保存到: {config_file}")
    print(f"使用: source {config_file}")

    return config_lines


def step_5_sync_data(client: NotionClient, config: NotionConfig):
    """第五步：同步數據"""
    print_header("第五步：同步審計日誌數據")

    sync = AuditNotionSync(client, config)
    success = sync.sync_all()

    return success


def main():
    """主函數"""
    print("""
🐉 龍魂 Notion 集成 · Stage 4 自動化設置
DNA: #龍芯⚇️2026-06-01-STAGE4-SETUP-v1.0

本腳本將幫助您快速設置審計日誌數據庫和首次同步。
    """)

    # 第一步：驗證連接
    result = step_1_verify_connection()
    if not result:
        sys.exit(1)

    client, config = result

    # 第二步：獲取工作區信息
    workspace_id = step_2_get_workspace_info()
    if not workspace_id:
        sys.exit(1)

    # 第三步：創建數據庫
    created_dbs = step_3_create_databases(client, workspace_id)

    if not created_dbs:
        print("\n❌ 未能創建任何數據庫")
        sys.exit(1)

    print(f"\n✅ 成功創建 {len(created_dbs)} 個數據庫")

    # 第四步：保存配置
    step_4_save_config(created_dbs)

    # 詢問是否立即同步
    print("\n")
    response = input("是否立即執行審計日誌同步？(y/n): ").strip().lower()

    if response == 'y':
        # 更新配置
        mapping = {
            "健康檢查日誌": "health_db",
            "性能基線": "baseline_db",
            "警告事件": "alert_db",
            "審計日誌": "audit_db",
        }

        for db_name, config_attr in mapping.items():
            db_id = created_dbs.get(db_name, "")
            if db_id:
                setattr(config, config_attr, db_id)

        # 第五步：同步數據
        success = step_5_sync_data(client, config)
        sys.exit(0 if success else 1)
    else:
        print("\n⏭️  跳過審計日誌同步")
        print("稍後可運行: python3 audit_sync.py")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
