#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 · Notion PoW 工作量证明记账系统 v1.0
Notion API Integration + Proof of Work for Sorting Algorithms

DNA追溯碼：#龍芯⚡️2026-05-27-NOTION-POW-ACCOUNTING-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 每次排序完成后，自动生成PoW哈希
  2. 连接Notion API，把数据记录进数据库
  3. 形成不可篡改的工作链（Work Chain）
  4. 支持离线降级（无网络仍可本地记录）

使用：
  # 安装依赖
  pip install notion-client python-dotenv

  # 配置环境变量
  export NOTION_API_KEY="your_integration_token_here"
  export NOTION_DATABASE_ID="your_database_id_here"

  # 调用示例
  from longhun_notion_pow import NotionPoW, hash_work, log_sorting_work
  log_sorting_work(
      comparisons=145,
      swaps=73,
      algorithm_name="快速排序",
      array_size=100
  )
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path

# 可选：Notion Client（若已安装）
try:
    from notion_client import Client
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    print("⚠️  notion-client 未安装。将使用本地SQLite降级模式。")
    print("   要启用Notion集成，请运行: pip install notion-client")

# 可选：python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================================
# L0 数据结构
# ============================================================================

@dataclass
class SortingWorkRecord:
    """排序工作记录"""
    timestamp: str                  # ISO 8601时间戳
    algorithm: str                  # 排序算法名
    array_size: int                 # 数组大小
    comparisons: int                # 比较次数
    swaps: int                      # 交换次数
    pow_hash: str                   # 工作量证明哈希（SHA-256）
    pow_nonce: int = 0              # PoW随机数
    notion_page_id: Optional[str] = None  # Notion页面ID（若上传成功）
    local_id: Optional[str] = None  # 本地数据库ID

    def to_dict(self) -> Dict:
        """转为字典"""
        return asdict(self)

    def to_json(self) -> str:
        """转为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ============================================================================
# L1 工作量证明引擎
# ============================================================================

class ProofOfWork:
    """
    工作量证明（PoW）引擎

    目的：为每次排序操作生成不可篡改的"工作证书"
    算法：SHA-256(timestamp + algorithm + stats + nonce)
    """

    @staticmethod
    def hash_work(
        timestamp: str,
        algorithm: str,
        comparisons: int,
        swaps: int,
        array_size: int,
        nonce: int = 0
    ) -> str:
        """
        生成单次排序的PoW哈希

        Args:
            timestamp: ISO时间戳
            algorithm: 算法名
            comparisons: 比较次数
            swaps: 交换次数
            array_size: 数组大小
            nonce: 随机数（用于证明工作量）

        Returns:
            SHA-256哈希值（64字符）
        """
        payload = f"{timestamp}|{algorithm}|{array_size}|{comparisons}|{swaps}|{nonce}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @staticmethod
    def mine_work(
        timestamp: str,
        algorithm: str,
        comparisons: int,
        swaps: int,
        array_size: int,
        difficulty: int = 2  # 哈希前N位必须是0
    ) -> tuple:
        """
        "挖矿"式生成PoW
        通过递增nonce，直到找到满足条件的哈希

        Args:
            difficulty: 难度（前N个0）

        Returns:
            (最终哈希值, nonce值)
        """
        nonce = 0
        target = "0" * difficulty

        while True:
            hash_val = ProofOfWork.hash_work(
                timestamp, algorithm, comparisons, swaps, array_size, nonce
            )
            if hash_val.startswith(target):
                return hash_val, nonce
            nonce += 1


# ============================================================================
# L2 本地SQLite存储（降级方案）
# ============================================================================

class LocalWorkDB:
    """
    本地SQLite数据库
    用于离线保存排序记录（网络不可用时自动降级）
    """

    def __init__(self, db_path: str = "~/.longhun/work_records.db"):
        """初始化本地数据库"""
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS work_records (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                array_size INTEGER NOT NULL,
                comparisons INTEGER NOT NULL,
                swaps INTEGER NOT NULL,
                pow_hash TEXT NOT NULL,
                pow_nonce INTEGER NOT NULL,
                notion_synced BOOLEAN DEFAULT 0,
                notion_page_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def insert(self, record: SortingWorkRecord) -> str:
        """
        插入一条记录

        Returns:
            本地ID
        """
        local_id = f"local_{int(datetime.now().timestamp() * 1000)}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            INSERT INTO work_records (
                id, timestamp, algorithm, array_size, comparisons, swaps,
                pow_hash, pow_nonce
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                local_id,
                record.timestamp,
                record.algorithm,
                record.array_size,
                record.comparisons,
                record.swaps,
                record.pow_hash,
                record.pow_nonce
            ))
            conn.commit()
        return local_id

    def get_unsync(self) -> List[SortingWorkRecord]:
        """获取未同步到Notion的记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM work_records WHERE notion_synced = 0"
            ).fetchall()
        return [dict(row) for row in rows]

    def mark_synced(self, local_id: str, notion_page_id: str):
        """标记为已同步到Notion"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE work_records
                   SET notion_synced = 1, notion_page_id = ?
                   WHERE id = ?""",
                (notion_page_id, local_id)
            )
            conn.commit()


# ============================================================================
# L3 Notion 集成
# ============================================================================

class NotionPoW:
    """
    Notion 工作量证明记账系统

    连接Notion数据库，把排序记录写入·形成永久档案
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        database_id: Optional[str] = None
    ):
        """
        初始化Notion集成

        Args:
            api_key: Notion Integration Token (默认从环境变量读取)
            database_id: Notion Database ID (默认从环境变量读取)
        """
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        self.local_db = LocalWorkDB()

        if NOTION_AVAILABLE and self.api_key and self.database_id:
            self.client = Client(auth=self.api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            if not (self.api_key and self.database_id):
                print("⚠️  Notion配置不完整。请设置环境变量:")
                print("   export NOTION_API_KEY='...'")
                print("   export NOTION_DATABASE_ID='...'")

    def log_sorting_work(
        self,
        comparisons: int,
        swaps: int,
        algorithm_name: str,
        array_size: int = 100,
        difficulty: int = 1  # PoW难度（挖矿用）
    ) -> SortingWorkRecord:
        """
        记录一次排序工作

        主流程：
          1. 生成时间戳
          2. 计算PoW哈希（可选：挖矿模式）
          3. 创建本地记录
          4. 尝试上传到Notion
          5. 如果失败，保存到本地SQLite

        Args:
            comparisons: 比较次数
            swaps: 交换次数
            algorithm_name: 算法名
            array_size: 数组大小
            difficulty: PoW难度（1=简单，2=中等，3=困难）

        Returns:
            SortingWorkRecord 对象
        """
        timestamp = datetime.now().isoformat()

        # 生成PoW
        print(f"⛏️  正在生成PoW (difficulty={difficulty})...", end=" ", flush=True)
        pow_hash, pow_nonce = ProofOfWork.mine_work(
            timestamp=timestamp,
            algorithm=algorithm_name,
            comparisons=comparisons,
            swaps=swaps,
            array_size=array_size,
            difficulty=difficulty
        )
        print(f"✅ nonce={pow_nonce}")

        # 创建记录
        record = SortingWorkRecord(
            timestamp=timestamp,
            algorithm=algorithm_name,
            array_size=array_size,
            comparisons=comparisons,
            swaps=swaps,
            pow_hash=pow_hash,
            pow_nonce=pow_nonce
        )

        # 保存到本地
        local_id = self.local_db.insert(record)
        record.local_id = local_id

        # 尝试上传到Notion
        if self.enabled:
            print("📤 上传到Notion...", end=" ", flush=True)
            try:
                page_id = self._upload_to_notion(record)
                record.notion_page_id = page_id
                self.local_db.mark_synced(local_id, page_id)
                print(f"✅ {page_id[:8]}...")
            except Exception as e:
                print(f"⚠️  失败: {e}")
                print("💾 已保存到本地SQLite，稍后可同步")
        else:
            print("💾 Notion不可用，已保存到本地SQLite")

        return record

    def _upload_to_notion(self, record: SortingWorkRecord) -> str:
        """
        上传记录到Notion数据库

        假设Notion数据库有以下字段：
          - Title (排序算法名 + 时间)
          - Comparisons (数字)
          - Swaps (数字)
          - PoWHash (文本)
          - ArraySize (数字)
          - PoWNonce (数字)

        Returns:
            创建的页面ID
        """
        if not self.client or not self.database_id:
            raise ValueError("Notion客户端未初始化")

        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": f"{record.algorithm} · {record.timestamp[:19]}"
                            }
                        }
                    ]
                },
                "Comparisons": {"number": record.comparisons},
                "Swaps": {"number": record.swaps},
                "PoWHash": {"rich_text": [{"text": {"content": record.pow_hash}}]},
                "ArraySize": {"number": record.array_size},
                "PoWNonce": {"number": record.pow_nonce},
            }
        )
        return response["id"]

    def sync_pending(self) -> int:
        """
        同步所有待同步的本地记录到Notion

        Returns:
            成功同步的数量
        """
        if not self.enabled:
            print("⚠️  Notion不可用，无法同步")
            return 0

        unsync = self.local_db.get_unsync()
        count = 0

        for rec in unsync:
            try:
                record = SortingWorkRecord(**rec)
                page_id = self._upload_to_notion(record)
                self.local_db.mark_synced(rec["id"], page_id)
                count += 1
                print(f"✅ 同步 {rec['algorithm']} ({count}/{len(unsync)})")
            except Exception as e:
                print(f"❌ 同步失败: {e}")

        return count


# ============================================================================
# L4 便捷调用接口
# ============================================================================

# 全局实例
_pow_system = NotionPoW()


def log_sorting_work(
    comparisons: int,
    swaps: int,
    algorithm_name: str,
    array_size: int = 100
) -> SortingWorkRecord:
    """
    快捷记录排序工作

    使用示例：
    ```python
    from longhun_notion_pow import log_sorting_work

    result = log_sorting_work(
        comparisons=145,
        swaps=73,
        algorithm_name="快速排序",
        array_size=100
    )
    print(f"PoW哈希: {result.pow_hash}")
    print(f"本地ID: {result.local_id}")
    ```
    """
    return _pow_system.log_sorting_work(
        comparisons=comparisons,
        swaps=swaps,
        algorithm_name=algorithm_name,
        array_size=array_size
    )


def hash_work(
    timestamp: str,
    algorithm: str,
    comparisons: int,
    swaps: int,
    array_size: int,
    nonce: int = 0
) -> str:
    """计算单次排序的哈希"""
    return ProofOfWork.hash_work(
        timestamp, algorithm, comparisons, swaps, array_size, nonce
    )


def sync_to_notion() -> int:
    """同步所有待同步的记录到Notion"""
    return _pow_system.sync_pending()


# ============================================================================
# 测试与示例
# ============================================================================

def test_pow_system():
    """测试PoW系统"""
    print("\n" + "=" * 80)
    print("🐉 龍魂 · Notion PoW 工作量证明系统 · 测试")
    print("=" * 80 + "\n")

    # 测试1：快速排序
    print("【测试1】快速排序")
    result1 = log_sorting_work(
        comparisons=145,
        swaps=73,
        algorithm_name="快速排序",
        array_size=100
    )
    print(f"  PoW哈希: {result1.pow_hash[:16]}...")
    print(f"  本地ID: {result1.local_id}")
    print(f"  Notion: {result1.notion_page_id or '待同步'}\n")

    # 测试2：冒泡排序
    print("【测试2】冒泡排序")
    result2 = log_sorting_work(
        comparisons=4950,
        swaps=2475,
        algorithm_name="冒泡排序",
        array_size=100
    )
    print(f"  PoW哈希: {result2.pow_hash[:16]}...")
    print(f"  本地ID: {result2.local_id}\n")

    # 测试3：同步待同步的记录
    print("【测试3】同步待同步的记录到Notion")
    count = sync_to_notion()
    print(f"  成功同步: {count} 条\n")

    # 显示本地数据库状态
    print("【测试4】查看本地数据库")
    print(f"  数据库路径: {_pow_system.local_db.db_path}")
    unsync = _pow_system.local_db.get_unsync()
    print(f"  待同步: {len(unsync)} 条")

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_pow_system()
