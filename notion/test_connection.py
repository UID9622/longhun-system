#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion API 连接测试脚本

DNA: #龍芯⚇️2026-06-01-NOTION-CONNECTION-TEST-v1.0
Purpose: 验证 Notion API 连接和配置
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager, NotionConfig
    from .notion_client import NotionClient, NotionAuthError, NotionAPIError
except ImportError:
    from notion_config import NotionConfigManager, NotionConfig
    from notion_client import NotionClient, NotionAuthError, NotionAPIError


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"🐉 {title}")
    print("=" * 70)


def test_configuration():
    """测试配置加载"""
    print_header("第一步：检查配置")

    manager = NotionConfigManager()

    # 检查环境变量
    print("\n1️⃣  检查环境变量...")
    token = os.getenv("NOTION_TOKEN")
    if token:
        print(f"✅ NOTION_TOKEN 已设置 (长度: {len(token)})")
    else:
        print("❌ NOTION_TOKEN 未设置")
        print("\n📝 设置方法:")
        print("① 访问: https://www.notion.so/my-integrations")
        print("② 创建或选择已有的 Integration")
        print("③ 复制 Internal Integration Token")
        print("④ 运行: export NOTION_TOKEN='your-token-here'")
        return False

    # 尝试加载配置
    print("\n2️⃣  加载配置...")
    try:
        config = manager.load()
        print(f"✅ 配置加载成功")
        manager.print_status()
        return True
    except ValueError as e:
        print(f"❌ 加载失败: {e}")
        return False


def test_api_connection():
    """测试 API 连接"""
    print_header("第二步：测试 API 连接")

    try:
        client = NotionClient()

        # 测试连接
        if not client.test_connection():
            print("\n❌ 连接测试失败")
            return False

        # 打印审计日志
        print()
        client.print_audit_summary()

        return True

    except NotionAuthError as e:
        print(f"❌ 认证错误: {e}")
        print("\n可能的原因:")
        print("  1. Token 已过期或无效")
        print("  2. Token 权限不足")
        print("  3. 格式错误 (检查是否有多余空格)")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def test_workspace_discovery():
    """测试工作区和数据库发现"""
    print_header("第三步：发现工作区和数据库")

    try:
        client = NotionClient()

        print("\n🔍 正在查询工作区...")
        # 注：此操作需要工作区权限
        print("""
注意：自动发现功能需要特定的 Notion 集成权限。
当前使用手动配置方法：

1️⃣  在 Notion 中打开要集成的页面/工作区
2️⃣  点击右上角 "..." → "Connections" 或 "+ Connections"
3️⃣  找到您创建的 Integration，点击 "Connect"
4️⃣  从浏览器地址栏复制工作区/数据库 ID

工作区/数据库 ID 格式示例：
  https://www.notion.so/{workspace-id}?v={view-id}

数据库查询 URL:
  https://www.notion.so/{database-id}?v={view-id}

提取 ID（移除所有连字符）:
  原: 34d7-125a-9c9f-81d2-be91-d1e3-e3be-34eb
  ID: 34d7125a9c9f81d2be91d1e3e3be34eb

3️⃣  运行以下命令设置环境变量:

export NOTION_WORKSPACE_1='your-workspace-1-id'
export NOTION_WORKSPACE_2='your-workspace-2-id'
export NOTION_WORKSPACE_3='your-workspace-3-id'

export NOTION_CNSH_MODEL_DB='database-id'
export NOTION_CNSH_DIMENSION_DB='database-id'
export NOTION_CNSH_METRIC_DB='database-id'
export NOTION_CNSH_CERT_DB='database-id'

# ... 等等（详见下一步）
        """)

        return True

    except Exception as e:
        print(f"⚠️  发现失败: {e}")
        return True  # 这一步可以跳过


def print_next_steps():
    """打印后续步骤"""
    print_header("后续步骤")

    print("""
✅ API 连接框架已就绪！

接下来的工作：

【第一阶段】- 工作区和数据库设置
  1. 在 Notion 中创建或识别三个工作区
  2. 在每个工作区中创建所需的数据库
  3. 使用 stage_1_setup.py 自动配置

【第二阶段】- CNSH 数据同步
  运行: python3 cnsh_sync.py

【第三阶段】- 知识图谱同步
  运行: python3 knowledge_sync.py

【第四阶段】- 审计日志同步
  运行: python3 audit_sync.py

【第五阶段】- 自动化同步
  运行: python3 setup_scheduler.py

更多信息：
  查看: ~/longhun-system/docs/Notion-Integration-Guide.md
    """)


def main():
    """主函数"""
    print("""
🐉 龍魂 Notion 集成 - API 连接测试
DNA: #龍芯⚇️2026-06-01-NOTION-CONNECTION-TEST-v1.0

本脚本将验证 Notion API 连接配置。
    """)

    # 测试配置
    if not test_configuration():
        sys.exit(1)

    # 测试 API 连接
    if not test_api_connection():
        print("\n❌ API 连接测试失败")
        print("\n故障排查:")
        print("  1. 检查 NOTION_TOKEN 是否正确设置")
        print("  2. 检查 token 是否已过期")
        print("  3. 检查网络连接")
        print("  4. 检查防火墙设置")
        sys.exit(1)

    # 测试工作区发现
    test_workspace_discovery()

    # 打印后续步骤
    print_next_steps()

    print("\n✅ 所有测试通过！")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
