#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 集成 · Stage 2 自动化设置

DNA: #龍芯⚇️2026-06-01-STAGE2-SETUP-v1.0
Purpose: 在 Notion 中创建 CNSH 数据库，配置环境变量，执行首次同步

Features:
  - 自动创建 4 个 CNSH 数据库
  - 验证 API 连接和权限
  - 保存数据库 ID 到配置文件
  - 执行首次数据同步
  - 生成配置报告
"""

import os
import json
import sys
from pathlib import Path

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager, NotionConfig
    from .notion_client import NotionClient, NotionAuthError
    from .cnsh_sync import CNSHNotionSync
except ImportError:
    from notion_config import NotionConfigManager, NotionConfig
    from notion_client import NotionClient, NotionAuthError
    from cnsh_sync import CNSHNotionSync


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"🐉 {title}")
    print("=" * 70)


def step_1_verify_connection():
    """第一步：验证连接"""
    print_header("第一步：验证 Notion API 连接")

    manager = NotionConfigManager()
    try:
        config = manager.load()
    except ValueError as e:
        print(f"❌ {e}")
        return None

    try:
        client = NotionClient(config)
        if not client.test_connection():
            print("❌ 连接测试失败")
            return None
        print("✅ API 连接正常")
        return client, config
    except NotionAuthError as e:
        print(f"❌ 认证失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return None


def step_2_get_workspace_info():
    """第二步：获取工作区信息"""
    print_header("第二步：输入 Notion 工作区信息")

    print("""
请提供要同步数据的 Notion 页面 ID（工作区）。

获取方法：
1. 在 Notion 中打开要使用的页面
2. 从浏览器地址栏复制 ID：
   https://www.notion.so/YOUR_WORKSPACE_ID?v=...

提取规则：移除所有连字符，例如：
   原: 34d7-125a-9c9f-81d2-be91-d1e3-e3be-34eb
   ID: 34d7125a9c9f81d2be91d1e3e3be34eb
    """)

    workspace_1 = input("工作区 1 ID (CNSH 基准测试): ").strip()
    if not workspace_1:
        print("❌ 工作区 ID 不能为空")
        return None

    return workspace_1


def step_3_create_databases(client: NotionClient, workspace_id: str) -> Dict[str, str]:
    """第三步：创建数据库"""
    print_header("第三步：在 Notion 中创建 CNSH 数据库")

    databases = {
        "模型认证记录": {
            "prop_名称": {"title": {}},
            "prop_综合得分": {"rich_text": {}},
            "prop_评级": {"select": {
                "options": [
                    {"name": "🟢 优秀"},
                    {"name": "🟡 合格"},
                    {"name": "🟠 警戒"},
                    {"name": "🔴 危险"},
                ]
            }},
            "prop_权限等级": {"rich_text": {}},
            "prop_维度通过": {"rich_text": {}},
            "prop_DNA": {"rich_text": {}},
        },
        "维度测试结果": {
            "prop_维度": {"select": {
                "options": [
                    {"name": "中文错别字"},
                    {"name": "代码缩进"},
                    {"name": "DNA标记大小写"},
                    {"name": "中英混排空格"},
                    {"name": "数学公式"},
                    {"name": "多码点组合Emoji"},
                    {"name": "代码注释规范"},
                    {"name": "中英混合处理"},
                    {"name": "龍魂系统认知"},
                ]
            }},
            "prop_测试ID": {"rich_text": {}},
            "prop_模型": {"rich_text": {}},
            "prop_得分": {"rich_text": {}},
            "prop_得分率": {"rich_text": {}},
            "prop_DNA": {"rich_text": {}},
        },
        "性能指标": {
            "prop_名称": {"title": {}},
            "prop_模型": {"rich_text": {}},
            "prop_综合得分": {"rich_text": {}},
        },
        "认证证书": {
            "prop_名称": {"title": {}},
            "prop_模型": {"rich_text": {}},
            "prop_认证等级": {"select": {
                "options": [
                    {"name": "一级合作伙伴 (Premier Partner)"},
                    {"name": "二级合作伙伴 (Senior Partner)"},
                    {"name": "禁用"},
                ]
            }},
            "prop_权限范围": {"rich_text": {}},
            "prop_有效期": {"rich_text": {}},
            "prop_DNA": {"rich_text": {}},
        },
    }

    created_dbs = {}

    for db_name, properties in databases.items():
        try:
            print(f"\n📁 创建: {db_name}...")

            # 修复属性名称（Notion API 要求）
            properties_fixed = {}
            for key, value in properties.items():
                clean_name = key.replace("prop_", "")
                properties_fixed[clean_name] = value

            result = client.create_database(
                parent_id=workspace_id,
                title=db_name,
                properties=properties_fixed,
            )

            db_id = result.get('id', '')
            if db_id:
                created_dbs[db_name] = db_id
                print(f"   ✅ 创建成功")
                print(f"   ID: {db_id}")
            else:
                print(f"   ❌ 创建失败：未获得数据库 ID")

        except Exception as e:
            print(f"   ❌ 创建失败: {str(e)[:100]}")

    return created_dbs


def step_4_save_config(created_dbs: Dict[str, str]):
    """第四步：保存配置"""
    print_header("第四步：保存配置到环境变量")

    config_lines = []

    # 映射数据库名称到环境变量
    mapping = {
        "模型认证记录": "NOTION_CNSH_MODEL_DB",
        "维度测试结果": "NOTION_CNSH_DIMENSION_DB",
        "性能指标": "NOTION_CNSH_METRIC_DB",
        "认证证书": "NOTION_CNSH_CERT_DB",
    }

    print("\n请运行以下命令设置环境变量：\n")
    for db_name, env_var in mapping.items():
        db_id = created_dbs.get(db_name, "")
        if db_id:
            config_lines.append(f"export {env_var}='{db_id}'")
            print(f"export {env_var}='{db_id}'")

    # 保存到配置文件
    config_file = Path.home() / ".龍魂_config" / "cnsh_databases.sh"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# CNSH 数据库 ID 配置\n")
        f.write(f"# 生成于: {datetime.now().isoformat()}\n\n")
        for line in config_lines:
            f.write(line + "\n")

    print(f"\n✅ 配置已保存到: {config_file}")
    print(f"使用: source {config_file}")

    return config_lines


def step_5_sync_data(client: NotionClient, config: NotionConfig):
    """第五步：同步数据"""
    print_header("第五步：同步基准测试数据")

    sync = CNSHNotionSync(client, config)
    success = sync.sync_all()

    return success


def main():
    """主函数"""
    print("""
🐉 龍魂 Notion 集成 · Stage 2 自动化设置
DNA: #龍芯⚇️2026-06-01-STAGE2-SETUP-v1.0

本脚本将帮助您快速设置 CNSH 数据库和首次同步。
    """)

    # 第一步：验证连接
    result = step_1_verify_connection()
    if not result:
        sys.exit(1)

    client, config = result

    # 第二步：获取工作区信息
    workspace_id = step_2_get_workspace_info()
    if not workspace_id:
        sys.exit(1)

    # 第三步：创建数据库
    created_dbs = step_3_create_databases(client, workspace_id)

    if not created_dbs:
        print("\n❌ 未能创建任何数据库")
        sys.exit(1)

    print(f"\n✅ 成功创建 {len(created_dbs)} 个数据库")

    # 第四步：保存配置
    step_4_save_config(created_dbs)

    # 询问是否立即同步
    print("\n")
    response = input("是否立即执行数据同步？(y/n): ").strip().lower()

    if response == 'y':
        # 更新配置
        mapping = {
            "模型认证记录": "cnsh_model_db",
            "维度测试结果": "cnsh_dimension_db",
            "性能指标": "cnsh_metric_db",
            "认证证书": "cnsh_cert_db",
        }

        for db_name, config_attr in mapping.items():
            db_id = created_dbs.get(db_name, "")
            if db_id:
                setattr(config, config_attr, db_id)

        # 第五步：同步数据
        success = step_5_sync_data(client, config)
        sys.exit(0 if success else 1)
    else:
        print("\n⏭️  跳过数据同步")
        print("稍后可运行: python3 cnsh_sync.py")
        sys.exit(0)


if __name__ == "__main__":
    from datetime import datetime
    from typing import Dict

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
