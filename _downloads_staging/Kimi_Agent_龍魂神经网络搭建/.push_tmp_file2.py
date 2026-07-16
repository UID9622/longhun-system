#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂系统 Notion 实时记录引擎 v1.0
=================================
龙魂体系(UID9622)动作实时记录器 - 本地SQLite + Notion双写

核心特性：
- 毫秒级时间戳记录
- DNA追溯码自动生成（#龙芯⚡️格式）
- 三色审计标记（🔴🟡🟢）
- 本地SQLite优先写入，异步批量同步到Notion
- 离线支持，网络恢复后自动补同步
- 零外部依赖（Notion API使用标准库http.client实现）

作者：龙魂北辰｜UID9622
版本：v1.0
"""

import sqlite3
import json
import time
import uuid
import hashlib
import http.client
import urllib.parse
import threading
import queue
import os
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Callable

# ============================================================================
# 常量与配置
# ============================================================================

VERSION = "1.0"
SYSTEM_UID = "UID9622"
SYSTEM_NAME = "龙芯北辰"

# Notion API 配置
NOTION_API_BASE = "api.notion.com"
NOTION_API_VERSION = "2022-06-28"

# 同步配置
SYNC_BATCH_SIZE = 10          # 每批最多同步条数
SYNC_INTERVAL_MS = 5000       # 同步间隔（毫秒）
RETRY_MAX_ATTEMPTS = 3        # 最大重试次数
RETRY_BASE_DELAY_MS = 1000    # 重试基础延迟（毫秒）

# 本地数据库路径
DEFAULT_DB_PATH = os.path.expanduser("~/.longhun/action_log.db")


# ============================================================================
# 枚举定义
# ============================================================================

class ActionType(Enum):
    """动作类型枚举"""
    SKILL_CALL = "SKILL_CALL"           # 技能调用
    CONTEXT_SWITCH = "CONTEXT_SWITCH"   # 上下文切换
    AI_ROUTE = "AI_ROUTE"               # AI网关路由
    USER_INPUT = "USER_INPUT"           # 用户输入
    SYSTEM_EVENT = "SYSTEM_EVENT"       # 系统事件
    AUDIT_MARK = "AUDIT_MARK"           # 审计标记
    DNA_GENERATE = "DNA_GENERATE"       # DNA生成
    ERROR = "ERROR"                     # 错误

    def label(self) -> str:
        labels = {
            ActionType.SKILL_CALL: "技能调用",
            ActionType.CONTEXT_SWITCH: "上下文切换",
            ActionType.AI_ROUTE: "AI网关路由",
            ActionType.USER_INPUT: "用户输入",
            ActionType.SYSTEM_EVENT: "系统事件",
            ActionType.AUDIT_MARK: "审计标记",
            ActionType.DNA_GENERATE: "DNA生成",
            ActionType.ERROR: "错误",
        }
        return labels.get(self, self.value)


class AuditColor(Enum):
    """审计标记（三色标记）"""
    RED = "🔴 红色-严重"     # 严重问题，需立即处理
    YELLOW = "🟡 黄色-警告"  # 警告，需关注
    GREEN = "🟢 绿色-正常"   # 正常状态


class Status(Enum):
    """记录状态"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class SkillID(Enum):
    """技能ID枚举"""
    INPUT_FILTER = "INPUT_FILTER"       # 输入过滤
    CONTEXT_MANAGER = "CONTEXT_MANAGER"  # 上下文管理
    AI_GATEWAY = "AI_GATEWAY"           # AI网关
    SKILL_ROUTER = "SKILL_ROUTER"       # 技能路由
    MEMORY_MANAGER = "MEMORY_MANAGER"   # 记忆管理
    AUDIT_LOGGER = "AUDIT_LOGGER"       # 审计日志
    CALENDAR = "CALENDAR"               # 万年历
    DNA_GENERATOR = "DNA_GENERATOR"     # DNA生成器


class AIGatewayRoute(Enum):
    """AI网关路由枚举"""
    CLAUDE = "CLAUDE"           # Claude
    GPT4 = "GPT4"               # GPT-4
    LOCAL = "LOCAL"             # 本地处理
    REASONING = "REASONING"     # 深度推理
    MULTI_AI = "MULTI_AI"       # 多AI协作


class TopicTag(Enum):
    """话题标签枚举"""
    TECH = "技术"
    LEGAL = "法律"
    FINANCE = "财务"
    GENERAL = "通用"
    SECURITY = "安全"
    MANAGEMENT = "管理"


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class ActionRecord:
    """
    动作记录数据模型
    
    每条记录对应一个动作，包含完整的上下文信息
    """
    # 核心字段
    timestamp_ms: int                           # 毫秒级时间戳
    action_type: ActionType                     # 动作类型
    description: str                            # 动作描述（标题）
    dna_trace: str = ""                         # DNA追溯码
    audit_color: AuditColor = AuditColor.GREEN  # 审计标记
    session_id: str = ""                        # 会话ID
    
    # 分类标签
    topic_tags: List[TopicTag] = field(default_factory=list)  # 话题标签
    skill_id: Optional[SkillID] = None          # 技能ID
    ai_gateway_route: Optional[AIGatewayRoute] = None  # AI网关路由
    
    # 输入输出
    input_summary: str = ""                     # 用户输入摘要
    output_summary: str = ""                    # 输出摘要
    duration_ms: int = 0                        # 执行时长（毫秒）
    status: Status = Status.SUCCESS             # 状态
    
    # 上下文
    context_snapshot_url: str = ""              # 上下文快照URL
    context_data: Dict[str, Any] = field(default_factory=dict)  # 上下文数据
    
    # 元数据
    id: str = ""                                # 本地记录ID
    notion_page_id: str = ""                    # Notion页面ID
    sync_status: str = "pending"                # 同步状态
    retry_count: int = 0                        # 重试次数
    created_at: int = 0                         # 创建时间

    def __post_init__(self):
        if not self.id:
            self.id = f"local_{uuid.uuid4().hex[:16]}"
        if not self.created_at:
            self.created_at = int(time.time() * 1000)
        if not self.dna_trace:
            self.dna_trace = self._generate_dna()

    def _generate_dna(self) -> str:
        """生成DNA追溯码: #龙芯⚡️UID9622-YYYYMMDD-HHMMSS-SEQ"""
        dt = datetime.fromtimestamp(self.timestamp_ms / 1000)
        time_str = dt.strftime("%Y%m%d-%H%M%S")
        seq = hashlib.md5(f"{self.timestamp_ms}{self.session_id}".encode()).hexdigest()[:3].upper()
        return f"#龙芯⚡️{SYSTEM_UID}-{time_str}-{seq}"

    def to_notion_properties(self) -> Dict[str, Any]:
        """转换为Notion API属性格式"""
        dt = datetime.fromtimestamp(
            self.timestamp_ms / 1000, 
            tz=timezone(timedelta(hours=8))
        )
        iso_timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:23] + "+08:00"
        
        props = {
            "动作描述": {"title": [{"text": {"content": self.description}}]},
            "时间戳": {"date": {"start": iso_timestamp}},
            "动作类型": {"select": {"name": self.action_type.value}},
            "DNA追溯码": {"rich_text": [{"text": {"content": self.dna_trace}}]},
            "审计标记": {"select": {"name": self.audit_color.value}},
            "会话ID": {"rich_text": [{"text": {"content": self.session_id}}]},
            "用户输入摘要": {"rich_text": [{"text": {"content": self.input_summary[:2000]}}]},
            "输出摘要": {"rich_text": [{"text": {"content": self.output_summary[:2000]}}]},
            "执行时长": {"number": self.duration_ms},
            "状态": {"select": {"name": self.status.value}},
        }
        
        # 可选字段
        if self.topic_tags:
            props["话题标签"] = {
                "multi_select": [{"name": t.value} for t in self.topic_tags]
            }
        if self.skill_id:
            props["技能ID"] = {"select": {"name": self.skill_id.value}}
        if self.ai_gateway_route:
            props["AI网关路由"] = {"select": {"name": self.ai_gateway_route.value}}
        if self.context_snapshot_url:
            props["上下文快照"] = {"url": self.context_snapshot_url}
            
        return props

    def to_sqlite_dict(self) -> Dict[str, Any]:
        """转换为SQLite存储格式"""
        return {
            "id": self.id,
            "timestamp_ms": self.timestamp_ms,
            "action_type": self.action_type.value,
            "description": self.description,
            "dna_trace": self.dna_trace,
            "audit_color": self.audit_color.value,
            "session_id": self.session_id,
            "topic_tags": json.dumps([t.value for t in self.topic_tags]),
            "skill_id": self.skill_id.value if self.skill_id else None,
            "ai_gateway_route": self.ai_gateway_route.value if self.ai_gateway_route else None,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "duration_ms": self.duration_ms,
            "status": self.status.value,
            "context_snapshot_url": self.context_snapshot_url,
            "context_data": json.dumps(self.context_data),
            "notion_page_id": self.notion_page_id,
            "sync_status": self.sync_status,
            "retry_count": self.retry_count,
            "created_at": self.created_at,
        }


# ============================================================================
# Notion API 客户端（零外部依赖实现）
# ============================================================================

class NotionAPIClient:
    """
    Notion API 客户端
    
    使用Python标准库 http.client 实现，零外部依赖。
    支持：创建页面、查询数据库、更新页面
    """
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.conn: Optional[http.client.HTTPSConnection] = None
        self._connect()
    
    def _connect(self):
        """建立HTTPS连接"""
        self.conn = http.client.HTTPSConnection(NOTION_API_BASE, timeout=30)
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        }
    
    def _request(self, method: str, path: str, body: Optional[Dict] = None) -> Dict:
        """发送HTTP请求"""
        body_json = json.dumps(body) if body else None
        
        for attempt in range(RETRY_MAX_ATTEMPTS):
            try:
                if self.conn is None:
                    self._connect()
                
                self.conn.request(
                    method, 
                    path, 
                    body=body_json,
                    headers=self._get_headers()
                )
                response = self.conn.getresponse()
                data = response.read().decode("utf-8")
                
                if response.status >= 200 and response.status < 300:
                    return json.loads(data) if data else {}
                elif response.status == 429:  # Rate limit
                    retry_after = int(response.getheader("Retry-After", "1"))
                    time.sleep(retry_after)
                    self._connect()  # 重建连接
                    continue
                else:
                    error_msg = f"HTTP {response.status}: {data}"
                    if attempt < RETRY_MAX_ATTEMPTS - 1:
                        time.sleep(RETRY_BASE_DELAY_MS / 1000 * (2 ** attempt))
                        self._connect()
                        continue
                    raise ConnectionError(error_msg)
                    
            except (http.client.HTTPException, ConnectionError, TimeoutError) as e:
                if attempt < RETRY_MAX_ATTEMPTS - 1:
                    time.sleep(RETRY_BASE_DELAY_MS / 1000 * (2 ** attempt))
                    self._connect()
                    continue
                raise ConnectionError(f"Notion API请求失败（重试{RETRY_MAX_ATTEMPTS}次）: {e}")
        
        return {}
    
    def create_page(self, database_id: str, properties: Dict, icon: Optional[str] = None) -> Dict:
        """在数据库中创建页面"""
        body = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }
        if icon:
            body["icon"] = {"emoji": icon}
        return self._request("POST", "/v1/pages", body)
    
    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None) -> Dict:
        """查询数据库"""
        body = {}
        if filter_obj:
            body["filter"] = filter_obj
        return self._request("POST", f"/v1/databases/{database_id}/query", body)
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """更新页面属性"""
        return self._request("PATCH", f"/v1/pages/{page_id}", {"properties": properties})
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None


# ============================================================================
# SQLite 本地存储
# ============================================================================

class SQLiteStore:
    """
    SQLite 本地存储引擎
    
    负责：
    - 本地持久化存储
    - 离线队列管理
    - 同步状态追踪
    """
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
    
    def _init_tables(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        
        # 主表：动作记录
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS action_records (
                id TEXT PRIMARY KEY,
                timestamp_ms INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                dna_trace TEXT NOT NULL,
                audit_color TEXT NOT NULL,
                session_id TEXT,
                topic_tags TEXT,
                skill_id TEXT,
                ai_gateway_route TEXT,
                input_summary TEXT,
                output_summary TEXT,
                duration_ms INTEGER DEFAULT 0,
                status TEXT DEFAULT 'SUCCESS',
                context_snapshot_url TEXT,
                context_data TEXT,
                notion_page_id TEXT,
                sync_status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                created_at INTEGER NOT NULL
            )
        """)
        
        # 索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON action_records(timestamp_ms)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session 
            ON action_records(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sync_status 
            ON action_records(sync_status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_action_type 
            ON action_records(action_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_dna_trace 
            ON action_records(dna_trace)
        """)
        
        # 同步日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                started_at INTEGER NOT NULL,
                completed_at INTEGER,
                records_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                error_message TEXT,
                status TEXT DEFAULT 'running'
            )
        """)
        
        # 系统状态表（用于离线标记等）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at INTEGER
            )
        """)
        
        self.conn.commit()
    
    def insert_record(self, record: ActionRecord) -> str:
        """插入记录，返回记录ID"""
        data = record.to_sqlite_dict()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO action_records (
                id, timestamp_ms, action_type, description, dna_trace,
                audit_color, session_id, topic_tags, skill_id, ai_gateway_route,
                input_summary, output_summary, duration_ms, status,
                context_snapshot_url, context_data, notion_page_id,
                sync_status, retry_count, created_at
            ) VALUES (
                :id, :timestamp_ms, :action_type, :description, :dna_trace,
                :audit_color, :session_id, :topic_tags, :skill_id, :ai_gateway_route,
                :input_summary, :output_summary, :duration_ms, :status,
                :context_snapshot_url, :context_data, :notion_page_id,
                :sync_status, :retry_count, :created_at
            )
        """, data)
        self.conn.commit()
        return record.id
    
    def get_pending_records(self, limit: int = SYNC_BATCH_SIZE) -> List[Dict]:
        """获取待同步的记录"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM action_records 
            WHERE sync_status IN ('pending', 'failed')
            AND retry_count < ?
            ORDER BY timestamp_ms ASC
            LIMIT ?
        """, (RETRY_MAX_ATTEMPTS, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def mark_synced(self, local_id: str, notion_page_id: str):
        """标记记录为已同步"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE action_records 
            SET sync_status = 'synced', 
                notion_page_id = ?,
                retry_count = 0
            WHERE id = ?
        """, (notion_page_id, local_id))
        self.conn.commit()
    
    def mark_failed(self, local_id: str, increment_retry: bool = True):
        """标记记录同步失败"""
        cursor = self.conn.cursor()
        if increment_retry:
            cursor.execute("""
                UPDATE action_records 
                SET sync_status = 'failed',
                    retry_count = retry_count + 1
                WHERE id = ?
            """, (local_id,))
        else:
            cursor.execute("""
                UPDATE action_records 
                SET sync_status = 'failed'
                WHERE id = ?
            """, (local_id,))
        self.conn.commit()
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        cursor = self.conn.cursor()
        stats = {}
        
        for status in ["pending", "synced", "failed"]:
            cursor.execute("""
                SELECT COUNT(*) FROM action_records WHERE sync_status = ?
            """, (status,))
            stats[status] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM action_records")
        stats["total"] = cursor.fetchone()[0]
        
        return stats
    
    def query_by_session(self, session_id: str) -> List[Dict]:
        """按会话ID查询记录"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM action_records 
            WHERE session_id = ?
            ORDER BY timestamp_ms ASC
        """, (session_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def query_by_time_range(self, start_ms: int, end_ms: int) -> List[Dict]:
        """按时间范围查询记录"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM action_records 
            WHERE timestamp_ms BETWEEN ? AND ?
            ORDER BY timestamp_ms ASC
        """, (start_ms, end_ms))
        return [dict(row) for row in cursor.fetchall()]
    
    def query_by_dna(self, dna_trace: str) -> Optional[Dict]:
        """按DNA追溯码查询记录"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM action_records WHERE dna_trace = ?
        """, (dna_trace,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_sync_log(self, limit: int = 10) -> List[Dict]:
        """获取同步日志"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM sync_log 
            ORDER BY started_at DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def log_sync_start(self, batch_id: str) -> int:
        """记录同步开始"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sync_log (batch_id, started_at, status)
            VALUES (?, ?, 'running')
        """, (batch_id, int(time.time() * 1000)))
        self.conn.commit()
        return cursor.lastrowid
    
    def log_sync_end(self, log_id: int, success: int, failed: int, error: str = None):
        """记录同步结束"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sync_log 
            SET completed_at = ?,
                success_count = ?,
                failed_count = ?,
                error_message = ?,
                status = ?
            WHERE id = ?
        """, (int(time.time() * 1000), success, failed, error, 
              'completed' if not error else 'failed', log_id))
        self.conn.commit()
    
    def set_state(self, key: str, value: str):
        """设置系统状态"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO system_state (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, int(time.time() * 1000)))
        self.conn.commit()
    
    def get_state(self, key: str) -> Optional[str]:
        """获取系统状态"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM system_state WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# ============================================================================
# 同步引擎
# ============================================================================

class SyncEngine:
    """
    同步引擎
    
    负责：
    - 批量同步本地记录到Notion
    - 失败重试机制
    - 同步状态管理
    """
    
    def __init__(self, 
                 store: SQLiteStore, 
                 notion_client: NotionAPIClient,
                 database_id: str):
        self.store = store
        self.notion = notion_client
        self.database_id = database_id
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def sync_batch(self) -> Dict[str, int]:
        """
        执行一次批量同步
        
        Returns:
            {"synced": N, "failed": N, "skipped": N}
        """
        records = self.store.get_pending_records(SYNC_BATCH_SIZE)
        
        if not records:
            return {"synced": 0, "failed": 0, "skipped": 0}
        
        batch_id = f"batch_{uuid.uuid4().hex[:8]}"
        log_id = self.store.log_sync_start(batch_id)
        
        synced = 0
        failed = 0
        
        for record_data in records:
            try:
                # 重建ActionRecord对象
                record = ActionRecord(
                    timestamp_ms=record_data["timestamp_ms"],
                    action_type=ActionType(record_data["action_type"]),
                    description=record_data["description"],
                    dna_trace=record_data["dna_trace"],
                    audit_color=AuditColor(record_data["audit_color"]),
                    session_id=record_data["session_id"] or "",
                    topic_tags=[TopicTag(t) for t in json.loads(record_data["topic_tags"] or "[]")],
                    skill_id=SkillID(record_data["skill_id"]) if record_data["skill_id"] else None,
                    ai_gateway_route=AIGatewayRoute(record_data["ai_gateway_route"]) if record_data["ai_gateway_route"] else None,
                    input_summary=record_data["input_summary"] or "",
                    output_summary=record_data["output_summary"] or "",
                    duration_ms=record_data["duration_ms"] or 0,
                    status=Status(record_data["status"]),
                    context_snapshot_url=record_data["context_snapshot_url"] or "",
                )
                
                # 发送到Notion
                result = self.notion.create_page(
                    self.database_id,
                    record.to_notion_properties(),
                    icon="📝"
                )
                
                if result and "id" in result:
                    self.store.mark_synced(record_data["id"], result["id"])
                    synced += 1
                else:
                    self.store.mark_failed(record_data["id"])
                    failed += 1
                    
            except Exception as e:
                self.store.mark_failed(record_data["id"])
                failed += 1
        
        self.store.log_sync_end(log_id, synced, failed)
        
        return {"synced": synced, "failed": failed, "skipped": 0}
    
    def start_auto_sync(self):
        """启动自动同步线程"""
        self._running = True
        self._thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._thread.start()
    
    def stop_auto_sync(self):
        """停止自动同步"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=10)
    
    def _sync_loop(self):
        """同步循环"""
        while self._running:
            try:
                self.sync_batch()
            except Exception as e:
                # 同步失败，等待后重试
                pass
            
            # 等待间隔
            for _ in range(int(SYNC_INTERVAL_MS / 100)):
                if not self._running:
                    break
                time.sleep(0.1)


# ============================================================================
# 记录器（主入口）
# ============================================================================

class LongHunLogger:
    """
    龙魂系统记录器 - 主入口类
    
    使用方法:
        logger = LongHunLogger(notion_token="xxx", database_id="xxx")
        
        # 自动记录（上下文管理器）
        with logger.record(ActionType.SKILL_CALL, "输入过滤") as rec:
            result = do_something()
            rec.output_summary = result
        
        # 手动记录
        logger.log(
            action_type=ActionType.USER_INPUT,
            description="接收用户指令",
            input_summary="帮我分析合同",
            audit_color=AuditColor.GREEN,
        )
    
    万年历集成:
        # 在Calendar.enter()中调用
        logger.log_system_event("万年历enter()调用", session_id=current_session)
    """
    
    def __init__(self,
                 notion_token: Optional[str] = None,
                 database_id: Optional[str] = None,
                 db_path: str = DEFAULT_DB_PATH,
                 enable_auto_sync: bool = True):
        """
        初始化记录器
        
        Args:
            notion_token: Notion API Token
            database_id: Notion数据库ID
            db_path: 本地SQLite数据库路径
            enable_auto_sync: 是否启用自动同步
        """
        self.store = SQLiteStore(db_path)
        self.notion_token = notion_token
        self.database_id = database_id
        self.enable_auto_sync = enable_auto_sync
        
        # Notion客户端和同步引擎（延迟初始化）
        self._notion_client: Optional[NotionAPIClient] = None
        self._sync_engine: Optional[SyncEngine] = None
        
        # 当前会话ID
        self._session_id: Optional[str] = None
        
        # 统计
        self._local_count = 0
        self._sync_count = 0
        
        if notion_token and database_id and enable_auto_sync:
            self._init_notion_sync()
    
    def _init_notion_sync(self):
        """初始化Notion同步"""
        try:
            self._notion_client = NotionAPIClient(self.notion_token)
            self._sync_engine = SyncEngine(
                self.store, self._notion_client, self.database_id
            )
            self._sync_engine.start_auto_sync()
        except Exception as e:
            # Notion同步初始化失败，降级为仅本地模式
            print(f"[龙魂记录器] Notion同步初始化失败，降级为本地模式: {e}")
            self._notion_client = None
            self._sync_engine = None
    
    @property
    def session_id(self) -> str:
        """获取当前会话ID，自动生成新的如果没有"""
        if not self._session_id:
            self._session_id = f"sess_{uuid.uuid4().hex[:12]}"
        return self._session_id
    
    @session_id.setter
    def session_id(self, value: str):
        """设置会话ID"""
        self._session_id = value
    
    def new_session(self) -> str:
        """创建新会话"""
        self._session_id = f"sess_{uuid.uuid4().hex[:12]}"
        self.log(
            action_type=ActionType.SYSTEM_EVENT,
            description="新会话开始",
            output_summary=f"会话ID: {self._session_id}",
        )
        return self._session_id
    
    # ========================================================================
    # 核心记录方法
    # ========================================================================
    
    def log(self,
            action_type: ActionType,
            description: str,
            audit_color: AuditColor = AuditColor.GREEN,
            input_summary: str = "",
            output_summary: str = "",
            duration_ms: int = 0,
            skill_id: Optional[SkillID] = None,
            ai_gateway_route: Optional[AIGatewayRoute] = None,
            topic_tags: Optional[List[TopicTag]] = None,
            context_data: Optional[Dict[str, Any]] = None,
            status: Status = Status.SUCCESS) -> ActionRecord:
        """
        记录一个动作
        
        这是主要的记录方法，所有动作都通过此方法记录。
        先写入本地SQLite，然后由同步引擎异步同步到Notion。
        
        Args:
            action_type: 动作类型
            description: 动作描述
            audit_color: 审计标记颜色
            input_summary: 输入摘要
            output_summary: 输出摘要
            duration_ms: 执行时长（毫秒）
            skill_id: 技能ID
            ai_gateway_route: AI网关路由
            topic_tags: 话题标签列表
            context_data: 上下文数据字典
            status: 状态
            
        Returns:
            ActionRecord 记录对象
        """
        record = ActionRecord(
            timestamp_ms=int(time.time() * 1000),
            action_type=action_type,
            description=description,
            audit_color=audit_color,
            session_id=self.session_id,
            input_summary=input_summary,
            output_summary=output_summary,
            duration_ms=duration_ms,
            skill_id=skill_id,
            ai_gateway_route=ai_gateway_route,
            topic_tags=topic_tags or [],
            context_data=context_data or {},
            status=status,
        )
        
        # 写入本地（始终写入）
        self.store.insert_record(record)
        self._local_count += 1
        
        return record
    
    def log_skill_call(self,
                       skill_id: SkillID,
                       description: str,
                       input_summary: str = "",
                       output_summary: str = "",
                       duration_ms: int = 0,
                       audit_color: AuditColor = AuditColor.GREEN) -> ActionRecord:
        """便捷方法：记录技能调用"""
        return self.log(
            action_type=ActionType.SKILL_CALL,
            description=f"技能调用 - {description}",
            skill_id=skill_id,
            input_summary=input_summary,
            output_summary=output_summary,
            duration_ms=duration_ms,
            audit_color=audit_color,
        )
    
    def log_context_switch(self,
                           from_topic: str,
                           to_topic: str,
                           reason: str = "") -> ActionRecord:
        """便捷方法：记录上下文切换"""
        return self.log(
            action_type=ActionType.CONTEXT_SWITCH,
            description=f"上下文切换 - {from_topic}→{to_topic}",
            output_summary=f"原因: {reason}" if reason else f"从{from_topic}切换到{to_topic}",
            skill_id=SkillID.CONTEXT_MANAGER,
        )
    
    def log_ai_route(self,
                     route: AIGatewayRoute,
                     reason: str,
                     input_summary: str = "") -> ActionRecord:
        """便捷方法：记录AI网关路由决策"""
        audit = AuditColor.YELLOW if route == AIGatewayRoute.REASONING else AuditColor.GREEN
        return self.log(
            action_type=ActionType.AI_ROUTE,
            description=f"AI路由 - 路由到{route.value}",
            ai_gateway_route=route,
            input_summary=input_summary,
            output_summary=f"路由原因: {reason}",
            skill_id=SkillID.AI_GATEWAY,
            audit_color=audit,
        )
    
    def log_user_input(self,
                       user_input: str,
                       topic_tags: Optional[List[TopicTag]] = None) -> ActionRecord:
        """便捷方法：记录用户输入"""
        return self.log(
            action_type=ActionType.USER_INPUT,
            description="用户输入接收",
            input_summary=user_input[:500],
            topic_tags=topic_tags,
        )
    
    def log_system_event(self,
                         event_name: str,
                         output_summary: str = "",
                         session_id: Optional[str] = None) -> ActionRecord:
        """便捷方法：记录系统事件"""
        old_session = self._session_id
        if session_id:
            self._session_id = session_id
        record = self.log(
            action_type=ActionType.SYSTEM_EVENT,
            description=f"系统事件 - {event_name}",
            output_summary=output_summary,
        )
        self._session_id = old_session
        return record
    
    def log_error(self,
                  error_message: str,
                  skill_id: Optional[SkillID] = None,
                  context: str = "") -> ActionRecord:
        """便捷方法：记录错误"""
        return self.log(
            action_type=ActionType.ERROR,
            description=f"错误 - {error_message[:100]}",
            input_summary=context,
            output_summary=error_message[:2000],
            skill_id=skill_id,
            audit_color=AuditColor.RED,
            status=Status.FAILED,
        )
    
    def log_audit(self,
                  mark_color: AuditColor,
                  message: str,
                  related_dna: str = "") -> ActionRecord:
        """便捷方法：记录审计标记"""
        return self.log(
            action_type=ActionType.AUDIT_MARK,
            description=f"审计标记 - {message[:100]}",
            audit_color=mark_color,
            output_summary=f"标记内容: {message}\n关联DNA: {related_dna}",
        )
    
    # ========================================================================
    # 万年历集成
    # ========================================================================
    
    def calendar_enter(self, context: Dict[str, Any] = None) -> ActionRecord:
        """
        万年历 enter() 调用记录
        
        在万年历的每个enter()方法开头调用此函数自动记录。
        
        Args:
            context: 进入时的上下文数据
            
        Returns:
            ActionRecord 记录对象
        """
        return self.log(
            action_type=ActionType.SYSTEM_EVENT,
            description="万年历 enter() 调用",
            skill_id=SkillID.CALENDAR,
            output_summary=f"进入万年历主循环，会话: {self.session_id}",
            context_data=context or {},
        )
    
    def calendar_context_switch(self, 
                                old_mode: str, 
                                new_mode: str,
                                trigger: str = "") -> ActionRecord:
        """万年历上下文切换记录"""
        return self.log(
            action_type=ActionType.CONTEXT_SWITCH,
            description=f"万年历上下文切换 - {old_mode}→{new_mode}",
            skill_id=SkillID.CALENDAR,
            output_summary=f"触发: {trigger}" if trigger else f"从{old_mode}切换到{new_mode}",
        )
    
    # ========================================================================
    # 上下文管理器（自动记录）
    # ========================================================================
    
    def record(self,
               action_type: ActionType,
               description: str,
               **kwargs) -> "RecordContext":
        """
        上下文管理器，用于自动记录动作执行过程
        
        Usage:
            with logger.record(ActionType.SKILL_CALL, "数据分析") as rec:
                result = analyze_data()
                rec.output_summary = f"分析完成: {result}"
                rec.duration_ms = 120
        """
        return RecordContext(self, action_type, description, **kwargs)
    
    # ========================================================================
    # 查询与统计
    # ========================================================================
    
    def get_stats(self) -> Dict[str, int]:
        """获取记录统计"""
        return self.store.get_stats()
    
    def query_session(self, session_id: str) -> List[Dict]:
        """查询会话的所有记录"""
        return self.store.query_by_session(session_id)
    
    def query_time_range(self, start_ms: int, end_ms: int) -> List[Dict]:
        """按时间范围查询"""
        return self.store.query_by_time_range(start_ms, end_ms)
    
    def query_by_dna(self, dna_trace: str) -> Optional[Dict]:
        """按DNA追溯码查询"""
        return self.store.query_by_dna(dna_trace)
    
    def force_sync(self) -> Dict[str, int]:
        """强制立即同步"""
        if self._sync_engine:
            return self._sync_engine.sync_batch()
        return {"synced": 0, "failed": 0, "skipped": 0, "reason": "Notion同步未启用"}
    
    def get_sync_log(self, limit: int = 10) -> List[Dict]:
        """获取同步日志"""
        return self.store.get_sync_log(limit)
    
    def is_online(self) -> bool:
        """检查Notion连接状态"""
        return self._notion_client is not None
    
    def close(self):
        """关闭记录器"""
        if self._sync_engine:
            self._sync_engine.stop_auto_sync()
        if self._notion_client:
            self._notion_client.close()
        self.store.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class RecordContext:
    """
    记录上下文管理器
    
    用法:
        with logger.record(ActionType.SKILL_CALL, "输入过滤") as rec:
            result = do_work()
            rec.output_summary = result
            rec.audit_color = AuditColor.GREEN
    """
    
    def __init__(self, logger: LongHunLogger, action_type: ActionType, description: str, **kwargs):
        self.logger = logger
        self.action_type = action_type
        self.description = description
        self.kwargs = kwargs
        self.record: Optional[ActionRecord] = None
        self._start_time = 0
    
    def __enter__(self) -> ActionRecord:
        self._start_time = int(time.time() * 1000)
        self.record = self.logger.log(
            action_type=self.action_type,
            description=self.description,
            **self.kwargs
        )
        return self.record
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # 发生异常
            self.record.status = Status.FAILED
            self.record.output_summary += f"\n[异常] {exc_type.__name__}: {exc_val}"
            self.record.audit_color = AuditColor.RED
        
        # 自动计算执行时长
        if self._start_time > 0:
            self.record.duration_ms = int(time.time() * 1000) - self._start_time
        
        # 更新本地记录
        # 注：由于SQLite已存储初始记录，这里可以额外更新
        # 为简化实现，时长和状态变化在内存中，本地记录保持初始值


# ============================================================================
# 便捷函数（全局单例）
# ============================================================================

_default_logger: Optional[LongHunLogger] = None

def init_logger(notion_token: Optional[str] = None,
                database_id: Optional[str] = None,
                db_path: str = DEFAULT_DB_PATH) -> LongHunLogger:
    """初始化全局记录器"""
    global _default_logger
    _default_logger = LongHunLogger(
        notion_token=notion_token,
        database_id=database_id,
        db_path=db_path,
    )
    return _default_logger

def get_logger() -> Optional[LongHunLogger]:
    """获取全局记录器"""
    return _default_logger


def quick_log(action_type: ActionType,
              description: str,
              **kwargs) -> Optional[ActionRecord]:
    """快速记录（使用全局记录器）"""
    if _default_logger:
        return _default_logger.log(action_type, description, **kwargs)
    return None


# ============================================================================
# 命令行工具
# ============================================================================

def main():
    """命令行入口 - 用于测试和手动同步"""
    import argparse
    
    parser = argparse.ArgumentParser(description="龙魂系统 Notion 记录器 v1.0")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="数据库路径")
    parser.add_argument("--token", help="Notion API Token")
    parser.add_argument("--db-id", dest="db_id", help="Notion数据库ID")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计信息")
    
    # sync 命令
    sync_parser = subparsers.add_parser("sync", help="手动同步到Notion")
    sync_parser.add_argument("--force", action="store_true", help="强制同步所有记录")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="查询记录")
    query_parser.add_argument("--session", help="按会话ID查询")
    query_parser.add_argument("--dna", help="按DNA追溯码查询")
    query_parser.add_argument("--limit", type=int, default=20, help="返回条数")
    
    # test 命令
    subparsers.add_parser("test", help="运行测试")
    
    args = parser.parse_args()
    
    if args.command == "stats":
        store = SQLiteStore(args.db)
        stats = store.get_stats()
        print("=" * 50)
        print("📊 龙魂记录器统计")
        print("=" * 50)
        print(f"  总记录数: {stats['total']}")
        print(f"  待同步:   {stats['pending']}")
        print(f"  已同步:   {stats['synced']}")
        print(f"  同步失败: {stats['failed']}")
        print("=" * 50)
        store.close()
    
    elif args.command == "sync":
        if not args.token or not args.db_id:
            print("错误: --token 和 --db-id 参数必需")
            return
        logger = LongHunLogger(args.token, args.db_id, args.db)
        result = logger.force_sync()
        print(f"同步结果: {result}")
        logger.close()
    
    elif args.command == "query":
        store = SQLiteStore(args.db)
        if args.session:
            records = store.query_by_session(args.session)
        elif args.dna:
            record = store.query_by_dna(args.dna)
            records = [record] if record else []
        else:
            cursor = store.conn.cursor()
            cursor.execute(f"SELECT * FROM action_records ORDER BY timestamp_ms DESC LIMIT {args.limit}")
            records = [dict(row) for row in cursor.fetchall()]
        
        for r in records:
            dt = datetime.fromtimestamp(r["timestamp_ms"] / 1000)
            print(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')}] {r['action_type']} | {r['description'][:50]} | {r['dna_trace']}")
        
        store.close()
    
    elif args.command == "test":
        print("🐉 龙魂记录器测试模式")
        print("=" * 50)
        
        # 创建测试记录器（仅本地模式）
        test_db = os.path.expanduser("~/.longhun/test.db")
        logger = LongHunLogger(db_path=test_db, enable_auto_sync=False)
        
        # 创建新会话
        sid = logger.new_session()
        print(f"\n[会话] {sid}")
        
        # 模拟万年历enter()
        rec1 = logger.calendar_enter({"mode": "interactive", "user": "test"})
        print(f"[万年历] enter() → {rec1.dna_trace}")
        
        # 模拟用户输入
        rec2 = logger.log_user_input("帮我分析合同条款", [TopicTag.LEGAL])
        print(f"[用户输入] → {rec2.dna_trace}")
        
        # 模拟技能调用
        rec3 = logger.log_skill_call(
            SkillID.INPUT_FILTER,
            "输入过滤协议",
            "帮我分析合同条款",
            "输入验证通过，触发法律分析",
            42,
        )
        print(f"[技能调用] INPUT_FILTER → {rec3.dna_trace}")
        
        # 模拟上下文切换
        rec4 = logger.log_context_switch("通用", "法律", "用户输入合同相关查询")
        print(f"[上下文切换] 通用→法律 → {rec4.dna_trace}")
        
        # 模拟AI路由
        rec5 = logger.log_ai_route(
            AIGatewayRoute.CLAUDE,
            "法律分析需要长上下文处理能力",
            "合同条款深度分析",
        )
        print(f"[AI路由] CLAUDE → {rec5.dna_trace}")
        
        # 模拟错误
        rec6 = logger.log_error(
            "技能执行超时",
            SkillID.AI_GATEWAY,
            "分析合同第3条时超时",
        )
        print(f"[错误] 超时 → {rec6.dna_trace}")
        
        # 审计标记
        rec7 = logger.log_audit(
            AuditColor.YELLOW,
            "AI响应时间超过阈值",
            rec5.dna_trace,
        )
        print(f"[审计] 黄色警告 → {rec7.dna_trace}")
        
        # 统计
        print("\n" + "=" * 50)
        stats = logger.get_stats()
        print(f"📊 本地记录: {stats['total']} 条")
        print(f"   待同步: {stats['pending']}")
        
        # 按会话查询
        print(f"\n📋 会话 {sid[:16]}... 的所有记录:")
        for r in logger.query_session(sid):
            print(f"  - [{r['action_type']}] {r['description'][:40]}")
        
        logger.close()
        
        # 清理测试数据库
        if os.path.exists(test_db):
            os.remove(test_db)
        
        print("\n✅ 测试完成！")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
