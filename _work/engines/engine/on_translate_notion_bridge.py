#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 通心译 v1.3 × Notion 集成桥接

DNA: #龍芯⚡️2026-05-27-TONGXINYI-NOTION-BRIDGE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能：
1. 从 Notion 数据库读取消息
2. 使用通心译 v1.3 处理消息
3. 将结果写回 Notion
4. 完整的错误处理和日志记录
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# 假设通心译 v1.3 已在同级目录或已安装
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.on_translate_v1_3 import TongxinyiEngine, StandardizedPackage


# ═══════════════════════════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Notion API 配置
# ═══════════════════════════════════════════════════════════════════════════

class NotionConfig:
    """Notion API 配置类"""

    def __init__(self, token: Optional[str] = None, database_id: Optional[str] = None):
        """
        初始化 Notion 配置

        参数:
            token: Notion Integration Token (从环境变量或参数读取)
            database_id: Notion 数据库 ID
        """
        self.token = token or os.environ.get('NOTION_TOKEN')
        self.database_id = database_id or os.environ.get('NOTION_DATABASE_ID')
        self.api_version = "2022-06-28"
        self.api_base = "https://api.notion.com/v1"

        if not self.token:
            logger.warning("NOTION_TOKEN 未设置。请设置环境变量或传入参数。")
        if not self.database_id:
            logger.warning("NOTION_DATABASE_ID 未设置。请设置环境变量或传入参数。")

    def get_headers(self) -> Dict[str, str]:
        """获取 Notion API 请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.api_version,
            "Content-Type": "application/json",
        }


# ═══════════════════════════════════════════════════════════════════════════
# Notion 消息读取器
# ═══════════════════════════════════════════════════════════════════════════

class NotionMessageReader:
    """从 Notion 数据库读取消息"""

    def __init__(self, config: NotionConfig):
        """初始化读取器"""
        self.config = config
        self.engine = TongxinyiEngine()

    def query_database(self, filter_clause: Optional[Dict] = None) -> List[Dict]:
        """
        查询 Notion 数据库

        参数:
            filter_clause: Notion 过滤条件 (可选)

        返回:
            页面列表
        """
        # 注意：这是模拟实现。实际使用需要安装 requests 库
        # pip install requests
        try:
            import requests
        except ImportError:
            logger.error("需要安装 requests 库: pip install requests")
            return []

        url = f"{self.config.api_base}/databases/{self.config.database_id}/query"
        headers = self.config.get_headers()

        payload = {}
        if filter_clause:
            payload['filter'] = filter_clause

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            logger.error(f"查询数据库失败: {e}")
            return []

    def extract_message_from_page(self, page: Dict) -> Optional[Dict]:
        """
        从 Notion 页面提取消息内容

        参数:
            page: Notion 页面对象

        返回:
            {
                'page_id': str,
                'content': str,
                'created_time': str,
                'properties': dict
            }
        """
        try:
            page_id = page.get('id')
            properties = page.get('properties', {})

            # 假设消息内容存储在名为 "Content" 或 "Message" 的字段中
            content = ""
            for prop_name, prop_value in properties.items():
                if prop_name.lower() in ['content', 'message', 'text']:
                    if prop_value.get('type') == 'rich_text':
                        content = ''.join([
                            t['plain_text']
                            for t in prop_value.get('rich_text', [])
                        ])
                    elif prop_value.get('type') == 'title':
                        content = ''.join([
                            t['plain_text']
                            for t in prop_value.get('title', [])
                        ])
                    break

            if not content:
                logger.warning(f"页面 {page_id} 中未找到内容")
                return None

            return {
                'page_id': page_id,
                'content': content,
                'created_time': page.get('created_time'),
                'properties': properties,
            }

        except Exception as e:
            logger.error(f"提取页面内容失败: {e}")
            return None

    def read_messages(self, limit: int = 10) -> List[Dict]:
        """
        读取消息

        参数:
            limit: 最多读取的消息数

        返回:
            消息列表
        """
        logger.info(f"开始查询 Notion 数据库 (最多 {limit} 条)...")

        pages = self.query_database()
        if not pages:
            logger.info("未找到任何页面")
            return []

        messages = []
        for page in pages[:limit]:
            msg = self.extract_message_from_page(page)
            if msg:
                messages.append(msg)

        logger.info(f"成功读取 {len(messages)} 条消息")
        return messages


# ═══════════════════════════════════════════════════════════════════════════
# Notion 结果写入器
# ═══════════════════════════════════════════════════════════════════════════

class NotionResultWriter:
    """将通心译结果写回 Notion"""

    def __init__(self, config: NotionConfig):
        """初始化写入器"""
        self.config = config

    def update_page(self, page_id: str, properties: Dict) -> bool:
        """
        更新 Notion 页面属性

        参数:
            page_id: 页面 ID
            properties: 要更新的属性字典

        返回:
            是否成功更新
        """
        try:
            import requests
        except ImportError:
            logger.error("需要安装 requests 库")
            return False

        url = f"{self.config.api_base}/pages/{page_id}"
        headers = self.config.get_headers()

        payload = {'properties': properties}

        try:
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"成功更新页面 {page_id}")
            return True
        except Exception as e:
            logger.error(f"更新页面失败: {e}")
            return False

    def write_result(
        self,
        page_id: str,
        result: StandardizedPackage,
        scenario: str,
        confidence: float
    ) -> bool:
        """
        将通心译结果写入 Notion 页面

        参数:
            page_id: 页面 ID
            result: StandardizedPackage 对象
            scenario: 检测场景
            confidence: 置信度

        返回:
            是否成功写入
        """
        # 构建 Notion 属性字典
        # 注意：这需要根据您的实际 Notion 数据库结构调整
        properties = {
            # 文本字段（示例）
            'Emotion': {
                'select': {
                    'name': result.emotion[:20]  # Notion select 最多 20 字
                }
            },
            'Intent': {
                'select': {
                    'name': result.intent[:20]
                }
            },
            # 多选字段（Persona 列表）
            'Personas': {
                'multi_select': [
                    {'name': p[:20]} for p in result.personas
                ]
            },
            # 单行文本字段
            'Scenario': {
                'rich_text': [
                    {'text': {'content': scenario}}
                ]
            },
            'DNA': {
                'rich_text': [
                    {'text': {'content': result.dna_signature}}
                ]
            },
            'Confidence': {
                'number': confidence
            },
            'Processed': {
                'checkbox': True
            },
            'ProcessedTime': {
                'date': {
                    'start': datetime.now().isoformat()
                }
            },
        }

        return self.update_page(page_id, properties)


# ═══════════════════════════════════════════════════════════════════════════
# 完整的集成流程
# ═══════════════════════════════════════════════════════════════════════════

class TongxinyiNotionBridge:
    """通心译 × Notion 完整集成"""

    def __init__(self, notion_token: Optional[str] = None, database_id: Optional[str] = None):
        """
        初始化集成桥接

        参数:
            notion_token: Notion Integration Token
            database_id: Notion 数据库 ID
        """
        self.config = NotionConfig(notion_token, database_id)
        self.reader = NotionMessageReader(self.config)
        self.writer = NotionResultWriter(self.config)
        self.engine = TongxinyiEngine()

        logger.info("通心译 × Notion 集成桥接已初始化")

    def process_message(self, message: Dict) -> bool:
        """
        处理单条消息

        参数:
            message: 包含 content 和 page_id 的消息字典

        返回:
            是否处理成功
        """
        try:
            page_id = message['page_id']
            content = message['content']

            logger.info(f"处理页面 {page_id}: {content[:50]}...")

            # 1. 使用通心译处理消息
            result = self.engine.process(content)

            # 2. 获取检测场景和置信度
            scenario, confidence = self.reader.engine.trigger_detector.detect(content)

            # 3. 写入结果到 Notion
            success = self.writer.write_result(
                page_id,
                result,
                scenario.value,
                confidence
            )

            if success:
                logger.info(f"✅ 页面 {page_id} 处理成功")
                logger.info(f"   情绪: {result.emotion}")
                logger.info(f"   意图: {result.intent}")
                logger.info(f"   Persona: {result.personas}")
                logger.info(f"   DNA: {result.dna_signature}")
            else:
                logger.warning(f"⚠️ 页面 {page_id} 写入失败")

            return success

        except Exception as e:
            logger.error(f"处理消息失败: {e}")
            return False

    def process_batch(self, limit: int = 10) -> Dict[str, int]:
        """
        批量处理消息

        参数:
            limit: 最多处理的消息数

        返回:
            {
                'total': 总数,
                'success': 成功数,
                'failed': 失败数
            }
        """
        logger.info("=" * 70)
        logger.info("🌐 通心译 × Notion 批量处理开始")
        logger.info("=" * 70)

        # 1. 从 Notion 读取消息
        messages = self.reader.read_messages(limit)

        if not messages:
            logger.info("没有消息需要处理")
            return {
                'total': 0,
                'success': 0,
                'failed': 0
            }

        # 2. 批量处理
        success_count = 0
        failed_count = 0

        for i, message in enumerate(messages, 1):
            logger.info(f"\n[{i}/{len(messages)}] 处理消息...")
            if self.process_message(message):
                success_count += 1
            else:
                failed_count += 1

        # 3. 生成报告
        logger.info("\n" + "=" * 70)
        logger.info("📊 处理完成")
        logger.info(f"   总数: {len(messages)}")
        logger.info(f"   ✅ 成功: {success_count}")
        logger.info(f"   ❌ 失败: {failed_count}")
        logger.info("=" * 70)

        return {
            'total': len(messages),
            'success': success_count,
            'failed': failed_count
        }

    def sync_continuous(self, interval: int = 60, max_iterations: Optional[int] = None):
        """
        持续同步模式

        参数:
            interval: 每次查询的间隔（秒）
            max_iterations: 最多迭代次数（None 表示无限循环）
        """
        import time

        logger.info("进入持续同步模式")
        logger.info(f"间隔: {interval} 秒")

        iteration = 0
        while True:
            iteration += 1

            if max_iterations and iteration > max_iterations:
                logger.info("达到最大迭代次数，停止同步")
                break

            logger.info(f"\n--- 迭代 {iteration} ---")
            result = self.process_batch(limit=10)

            if result['total'] == 0:
                logger.info(f"等待 {interval} 秒后再试...")
                time.sleep(interval)
            else:
                logger.info("有新消息，立即重新查询")


# ═══════════════════════════════════════════════════════════════════════════
# 演示和测试
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """演示如何使用通心译 × Notion 集成"""

    print("\n" + "=" * 70)
    print("🌐 通心译 v1.3 × Notion 集成 · 使用演示")
    print("=" * 70 + "\n")

    # 1. 配置 Notion API
    print("【步骤 1】配置 Notion API")
    print("-" * 70)

    # 从环境变量读取（推荐方式）
    notion_token = os.environ.get('NOTION_TOKEN')
    database_id = os.environ.get('NOTION_DATABASE_ID')

    if not notion_token or not database_id:
        print("\n⚠️  未设置 Notion 环境变量")
        print("\n【手动设置方式】")
        print("export NOTION_TOKEN='your_integration_token'")
        print("export NOTION_DATABASE_ID='your_database_id'")
        print("\n【或在代码中直接设置】")
        print("notion_token = 'ntn_xxx...'")
        print("database_id = 'xxx...'")
        print("\n📖 获取 Token: https://developers.notion.com/docs/getting-started")
        return

    print(f"✅ Notion Token: {notion_token[:20]}...")
    print(f"✅ Database ID: {database_id[:10]}...")

    # 2. 初始化集成桥接
    print("\n【步骤 2】初始化集成")
    print("-" * 70)

    bridge = TongxinyiNotionBridge(notion_token, database_id)
    print("✅ 通心译 × Notion 集成桥接已初始化")

    # 3. 处理消息
    print("\n【步骤 3】处理消息")
    print("-" * 70)

    result = bridge.process_batch(limit=5)

    # 4. 显示结果
    print("\n【步骤 4】处理结果")
    print("-" * 70)
    print(f"\n✅ 总处理数: {result['total']}")
    print(f"✅ 成功: {result['success']}")
    print(f"❌ 失败: {result['failed']}")

    if result['success'] > 0:
        print("\n🎉 集成成功！")
        print("所有处理结果已写回 Notion 数据库")


if __name__ == '__main__':
    main()
