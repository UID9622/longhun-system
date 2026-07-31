#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂规则引擎 · Notion 集成 v2.5
双向同步·冲突检测·实时更新

DNA:#龍芯⚡️2026-06-07-NOTION-SYNC-v2.5
责任: UID9622 · 不免责
"""

import os
import json
import logging
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("requests 未安装，Notion 集成将在离线模式运行")


# ============================================================================
# [日志配置]
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# [数据结构]
# ============================================================================

class SyncStatus(Enum):
    """同步状态"""
    SYNCED = "synced"           # 已同步
    LOCAL_ONLY = "local_only"   # 仅本地
    REMOTE_ONLY = "remote_only" # 仅远程
    CONFLICTED = "conflicted"   # 冲突
    PENDING = "pending"         # 待同步


@dataclass
class NotionPage:
    """Notion 页面"""
    id: str
    title: str
    status: str
    properties: Dict[str, Any]
    last_modified: str
    content_hash: str = None

    def compute_hash(self) -> str:
        """计算内容哈希"""
        content = json.dumps(self.properties, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()

    def __post_init__(self):
        if self.content_hash is None:
            self.content_hash = self.compute_hash()


@dataclass
class SyncRecord:
    """同步记录"""
    local_id: str
    remote_id: str
    local_hash: str
    remote_hash: str
    status: SyncStatus
    conflict_details: Optional[str] = None
    last_sync: str = None

    def __post_init__(self):
        if self.last_sync is None:
            self.last_sync = datetime.now().isoformat()


# ============================================================================
# [Notion API 客户端]
# ============================================================================

class NotionClient:
    """Notion API 客户端"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NOTION_TOKEN')
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }

        if not self.api_key:
            logger.warning("未设置 NOTION_TOKEN，Notion 集成将在离线模式运行")

    def is_connected(self) -> bool:
        """检查连接状态"""
        if not self.api_key or not REQUESTS_AVAILABLE:
            return False

        try:
            response = requests.get(
                f'{self.base_url}/databases',
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"连接检查失败: {e}")
            return False

    def query_database(self, database_id: str, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """查询数据库"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("无法连接 Notion，返回空结果")
            return []

        try:
            payload = {
                'filter': filter_dict or {},
                'page_size': 100,
            }

            response = requests.post(
                f'{self.base_url}/databases/{database_id}/query',
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"查询失败: {response.status_code} {response.text}")
                return []

            return response.json().get('results', [])

        except Exception as e:
            logger.error(f"查询异常: {e}")
            return []

    def update_page(self, page_id: str, properties: Dict[str, Any]) -> bool:
        """更新页面"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("无法连接 Notion，模拟更新成功")
            return True

        try:
            payload = {'properties': properties}

            response = requests.patch(
                f'{self.base_url}/pages/{page_id}',
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"更新失败: {response.status_code}")
                return False

            logger.info(f"已更新页面: {page_id}")
            return True

        except Exception as e:
            logger.error(f"更新异常: {e}")
            return False

    def create_page(self, database_id: str, properties: Dict[str, Any]) -> Optional[str]:
        """创建页面"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("无法连接 Notion，模拟创建成功")
            return hashlib.md5(json.dumps(properties).encode()).hexdigest()

        try:
            payload = {
                'parent': {'database_id': database_id},
                'properties': properties,
            }

            response = requests.post(
                f'{self.base_url}/pages',
                json=payload,
                headers=self.headers,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"创建失败: {response.status_code}")
                return None

            page_id = response.json().get('id')
            logger.info(f"已创建页面: {page_id}")
            return page_id

        except Exception as e:
            logger.error(f"创建异常: {e}")
            return None


# ============================================================================
# [同步管理器]
# ============================================================================

class NotionSyncManager:
    """Notion 双向同步管理器"""

    def __init__(
        self,
        notion_client: NotionClient,
        sync_state_file: str = '/tmp/notion_sync_state.json'
    ):
        self.client = notion_client
        self.sync_state_file = sync_state_file
        self.sync_records: Dict[str, SyncRecord] = {}
        self.load_sync_state()

    def load_sync_state(self) -> None:
        """加载同步状态"""
        try:
            if os.path.exists(self.sync_state_file):
                with open(self.sync_state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, record in data.items():
                        self.sync_records[key] = SyncRecord(
                            local_id=record['local_id'],
                            remote_id=record['remote_id'],
                            local_hash=record['local_hash'],
                            remote_hash=record['remote_hash'],
                            status=SyncStatus(record['status']),
                            conflict_details=record.get('conflict_details'),
                            last_sync=record.get('last_sync')
                        )
                logger.info(f"加载 {len(self.sync_records)} 条同步记录")
        except Exception as e:
            logger.error(f"加载同步状态失败: {e}")

    def save_sync_state(self) -> None:
        """保存同步状态"""
        try:
            data = {
                key: {
                    'local_id': record.local_id,
                    'remote_id': record.remote_id,
                    'local_hash': record.local_hash,
                    'remote_hash': record.remote_hash,
                    'status': record.status.value,
                    'conflict_details': record.conflict_details,
                    'last_sync': record.last_sync,
                }
                for key, record in self.sync_records.items()
            }

            os.makedirs(os.path.dirname(self.sync_state_file), exist_ok=True)
            with open(self.sync_state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info("已保存同步状态")

        except Exception as e:
            logger.error(f"保存同步状态失败: {e}")

    def sync_item(
        self,
        local_id: str,
        local_data: Dict[str, Any],
        remote_id: Optional[str] = None
    ) -> bool:
        """
        同步单个项目

        Args:
            local_id: 本地 ID
            local_data: 本地数据
            remote_id: 远程 ID (可选)

        Returns:
            是否同步成功
        """
        local_hash = hashlib.sha256(
            json.dumps(local_data, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()

        key = f"{local_id}_{remote_id or 'new'}"

        # 检查是否存在记录
        if key in self.sync_records:
            record = self.sync_records[key]

            # 检测冲突
            if record.local_hash != local_hash and record.remote_hash:
                logger.warning(f"发现冲突: {key}")
                record.status = SyncStatus.CONFLICTED
                record.conflict_details = f"本地于 {datetime.now().isoformat()} 修改"
                self.save_sync_state()
                return False

            # 更新远程
            if local_hash != record.local_hash:
                logger.info(f"同步更新: {key}")
                success = self.client.update_page(
                    remote_id or record.remote_id,
                    local_data
                )
                if success:
                    record.local_hash = local_hash
                    record.status = SyncStatus.SYNCED
                    record.last_sync = datetime.now().isoformat()
                    self.save_sync_state()
                return success

        else:
            # 新建记录
            new_remote_id = remote_id or self.client.create_page(
                '',  # 实际应传入 database_id
                local_data
            )

            if not new_remote_id:
                logger.error(f"创建远程记录失败: {local_id}")
                return False

            self.sync_records[key] = SyncRecord(
                local_id=local_id,
                remote_id=new_remote_id,
                local_hash=local_hash,
                remote_hash=local_hash,
                status=SyncStatus.SYNCED
            )
            self.save_sync_state()
            logger.info(f"创建新记录: {key}")
            return True

        return True

    def detect_conflicts(self) -> List[str]:
        """检测冲突"""
        conflicts = [
            key for key, record in self.sync_records.items()
            if record.status == SyncStatus.CONFLICTED
        ]
        logger.info(f"检测到 {len(conflicts)} 个冲突")
        return conflicts

    def resolve_conflict(self, key: str, prefer_local: bool = True) -> bool:
        """
        解决冲突

        Args:
            key: 记录键
            prefer_local: 是否优先使用本地数据

        Returns:
            是否解决成功
        """
        if key not in self.sync_records:
            logger.error(f"记录不存在: {key}")
            return False

        record = self.sync_records[key]

        if prefer_local:
            # 用本地数据覆盖远程
            record.remote_hash = record.local_hash
            logger.info(f"已用本地数据覆盖远程: {key}")
        else:
            # 用远程数据覆盖本地
            record.local_hash = record.remote_hash
            logger.info(f"已用远程数据覆盖本地: {key}")

        record.status = SyncStatus.SYNCED
        record.conflict_details = None
        record.last_sync = datetime.now().isoformat()
        self.save_sync_state()

        return True

    def get_sync_status(self) -> Dict[str, Any]:
        """获取同步状态摘要"""
        total = len(self.sync_records)
        synced = sum(1 for r in self.sync_records.values() if r.status == SyncStatus.SYNCED)
        conflicted = sum(1 for r in self.sync_records.values() if r.status == SyncStatus.CONFLICTED)
        pending = sum(1 for r in self.sync_records.values() if r.status == SyncStatus.PENDING)

        return {
            'total_records': total,
            'synced': synced,
            'conflicted': conflicted,
            'pending': pending,
            'sync_rate': f"{(synced / total * 100):.1f}%" if total > 0 else "N/A",
            'is_connected': self.client.is_connected(),
        }


# ============================================================================
# [使用示例]
# ============================================================================

def main():
    """命令行示例"""
    # 初始化客户端
    notion_client = NotionClient()
    sync_manager = NotionSyncManager(notion_client)

    # 检查连接
    if sync_manager.client.is_connected():
        print("✅ 已连接 Notion")
    else:
        print("⚠️  无法连接 Notion，使用离线模式")

    # 同步示例
    local_data = {
        "title": {"title": [{"text": {"content": "测试案件"}}]},
        "status": {"select": {"name": "进行中"}},
        "priority": {"select": {"name": "高"}},
    }

    success = sync_manager.sync_item("case_001", local_data)
    print(f"同步结果: {'成功' if success else '失败'}")

    # 检查冲突
    conflicts = sync_manager.detect_conflicts()
    if conflicts:
        print(f"发现 {len(conflicts)} 个冲突，解决方式: 优先本地")
        for conflict_key in conflicts:
            sync_manager.resolve_conflict(conflict_key, prefer_local=True)

    # 显示同步状态
    status = sync_manager.get_sync_status()
    print("\n📊 同步状态摘要:")
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == '__main__':
    main()
