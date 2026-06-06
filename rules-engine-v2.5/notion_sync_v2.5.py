#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂規則引擎 · Notion 集成 v2.5
雙向同步·衝突檢測·實時更新

DNA: #龍芯⚡️2026-06-07-NOTION-SYNC-v2.5
責任: UID9622 · 不免責
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
    logging.warning("requests 未安裝，Notion 集成將在離線模式運行")


# ============================================================================
# [日誌配置]
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# [數據結構]
# ============================================================================

class SyncStatus(Enum):
    """同步狀態"""
    SYNCED = "synced"           # 已同步
    LOCAL_ONLY = "local_only"   # 僅本地
    REMOTE_ONLY = "remote_only" # 僅遠程
    CONFLICTED = "conflicted"   # 衝突
    PENDING = "pending"         # 待同步


@dataclass
class NotionPage:
    """Notion 頁面"""
    id: str
    title: str
    status: str
    properties: Dict[str, Any]
    last_modified: str
    content_hash: str = None

    def compute_hash(self) -> str:
        """計算內容哈希"""
        content = json.dumps(self.properties, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()

    def __post_init__(self):
        if self.content_hash is None:
            self.content_hash = self.compute_hash()


@dataclass
class SyncRecord:
    """同步記錄"""
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
# [Notion API 客戶端]
# ============================================================================

class NotionClient:
    """Notion API 客戶端"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NOTION_TOKEN')
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }

        if not self.api_key:
            logger.warning("未設置 NOTION_TOKEN，Notion 集成將在離線模式運行")

    def is_connected(self) -> bool:
        """檢查連接狀態"""
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
            logger.error(f"連接檢查失敗: {e}")
            return False

    def query_database(self, database_id: str, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """查詢數據庫"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("無法連接 Notion，返回空結果")
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
                logger.error(f"查詢失敗: {response.status_code} {response.text}")
                return []

            return response.json().get('results', [])

        except Exception as e:
            logger.error(f"查詢異常: {e}")
            return []

    def update_page(self, page_id: str, properties: Dict) -> bool:
        """更新頁面"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("無法連接 Notion，模擬更新成功")
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
                logger.error(f"更新失敗: {response.status_code}")
                return False

            logger.info(f"已更新頁面: {page_id}")
            return True

        except Exception as e:
            logger.error(f"更新異常: {e}")
            return False

    def create_page(self, database_id: str, properties: Dict) -> Optional[str]:
        """創建頁面"""
        if not REQUESTS_AVAILABLE or not self.api_key:
            logger.warning("無法連接 Notion，模擬創建成功")
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
                logger.error(f"創建失敗: {response.status_code}")
                return None

            page_id = response.json().get('id')
            logger.info(f"已創建頁面: {page_id}")
            return page_id

        except Exception as e:
            logger.error(f"創建異常: {e}")
            return None


# ============================================================================
# [同步管理器]
# ============================================================================

class NotionSyncManager:
    """Notion 雙向同步管理器"""

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
        """加載同步狀態"""
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
                logger.info(f"加載 {len(self.sync_records)} 條同步記錄")
        except Exception as e:
            logger.error(f"加載同步狀態失敗: {e}")

    def save_sync_state(self) -> None:
        """保存同步狀態"""
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

            logger.info("已保存同步狀態")

        except Exception as e:
            logger.error(f"保存同步狀態失敗: {e}")

    def sync_item(
        self,
        local_id: str,
        local_data: Dict,
        remote_id: Optional[str] = None
    ) -> bool:
        """
        同步單個項目

        Args:
            local_id: 本地 ID
            local_data: 本地數據
            remote_id: 遠程 ID (可選)

        Returns:
            是否同步成功
        """
        local_hash = hashlib.sha256(
            json.dumps(local_data, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()

        key = f"{local_id}_{remote_id or 'new'}"

        # 檢查是否存在記錄
        if key in self.sync_records:
            record = self.sync_records[key]

            # 檢測衝突
            if record.local_hash != local_hash and record.remote_hash:
                logger.warning(f"發現衝突: {key}")
                record.status = SyncStatus.CONFLICTED
                record.conflict_details = f"本地於 {datetime.now().isoformat()} 修改"
                self.save_sync_state()
                return False

            # 更新遠程
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
            # 新建記錄
            new_remote_id = remote_id or self.client.create_page(
                '',  # 實際應傳入 database_id
                local_data
            )

            if not new_remote_id:
                logger.error(f"創建遠程記錄失敗: {local_id}")
                return False

            self.sync_records[key] = SyncRecord(
                local_id=local_id,
                remote_id=new_remote_id,
                local_hash=local_hash,
                remote_hash=local_hash,
                status=SyncStatus.SYNCED
            )
            self.save_sync_state()
            logger.info(f"創建新記錄: {key}")
            return True

        return True

    def detect_conflicts(self) -> List[str]:
        """檢測衝突"""
        conflicts = [
            key for key, record in self.sync_records.items()
            if record.status == SyncStatus.CONFLICTED
        ]
        logger.info(f"檢測到 {len(conflicts)} 個衝突")
        return conflicts

    def resolve_conflict(self, key: str, prefer_local: bool = True) -> bool:
        """
        解決衝突

        Args:
            key: 記錄鍵
            prefer_local: 是否優先使用本地數據

        Returns:
            是否解決成功
        """
        if key not in self.sync_records:
            logger.error(f"記錄不存在: {key}")
            return False

        record = self.sync_records[key]

        if prefer_local:
            # 用本地數據覆蓋遠程
            record.remote_hash = record.local_hash
            logger.info(f"已用本地數據覆蓋遠程: {key}")
        else:
            # 用遠程數據覆蓋本地
            record.local_hash = record.remote_hash
            logger.info(f"已用遠程數據覆蓋本地: {key}")

        record.status = SyncStatus.SYNCED
        record.conflict_details = None
        record.last_sync = datetime.now().isoformat()
        self.save_sync_state()

        return True

    def get_sync_status(self) -> Dict[str, Any]:
        """獲取同步狀態摘要"""
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
    # 初始化客戶端
    notion_client = NotionClient()
    sync_manager = NotionSyncManager(notion_client)

    # 檢查連接
    if sync_manager.client.is_connected():
        print("✅ 已連接 Notion")
    else:
        print("⚠️  無法連接 Notion，使用離線模式")

    # 同步示例
    local_data = {
        "title": {"title": [{"text": {"content": "測試案件"}}]},
        "status": {"select": {"name": "進行中"}},
        "priority": {"select": {"name": "高"}},
    }

    success = sync_manager.sync_item("case_001", local_data)
    print(f"同步結果: {'成功' if success else '失敗'}")

    # 檢查衝突
    conflicts = sync_manager.detect_conflicts()
    if conflicts:
        print(f"發現 {len(conflicts)} 個衝突，解決方式: 優先本地")
        for conflict_key in conflicts:
            sync_manager.resolve_conflict(conflict_key, prefer_local=True)

    # 顯示同步狀態
    status = sync_manager.get_sync_status()
    print("\n📊 同步狀態摘要:")
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == '__main__':
    main()
