#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║      龍魂Append-Only日志系统 / LongHun Immutable Logging        ║
║                                                                  ║
║  JSONL格式·永不覆盖·精确到分钟·抹不掉的痕迹                       ║
║  每条日志都包含完整上下文、时间戳、操作者、结果                     ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-APPEND-ONLY-LOGGING-FILE1-v1.0               ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: 龍魂操作草日志·每动作必记·精确到分钟·抹不掉的痕迹           ║
║  格式: 仅追加JSONL (JSON Lines) - 不可覆盖                       ║
║  权限: 创建后chmod 444 (只读)                                    ║
║  责任: UID9622·不免责                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import hashlib

# ═══════════════════════════════════════════════════════════════
# 【日志事件类型】
# ═══════════════════════════════════════════════════════════════

class LogEventType(str, Enum):
    """日志事件类型"""
    # 系统事件
    SYSTEM_START = "system:start"
    SYSTEM_SHUTDOWN = "system:shutdown"
    SYSTEM_ERROR = "system:error"

    # 用户事件
    USER_LOGIN = "user:login"
    USER_LOGOUT = "user:logout"
    USER_CREATED = "user:created"

    # 操作事件
    FILE_CREATED = "file:created"
    FILE_MODIFIED = "file:modified"
    FILE_DELETED = "file:deleted"
    CONFIG_CHANGED = "config:changed"
    WORKFLOW_EXECUTED = "workflow:executed"
    WORKFLOW_FAILED = "workflow:failed"

    # 权限事件
    PERMISSION_GRANTED = "permission:granted"
    PERMISSION_REVOKED = "permission:revoked"
    PERMISSION_DENIED = "permission:denied"

    # DNA事件
    DNA_GENERATED = "dna:generated"
    DNA_VERIFIED = "dna:verified"
    DNA_ARCHIVED = "dna:archived"

    # 审计事件
    AUDIT_CHECK = "audit:check"
    AUDIT_VIOLATION = "audit:violation"


class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ═══════════════════════════════════════════════════════════════
# 【日志记录对象】
# ═══════════════════════════════════════════════════════════════

@dataclass
class LogEntry:
    """单条日志记录 (永不删除，不可修改)"""

    # 核心信息
    event_type: LogEventType
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    level: LogLevel = LogLevel.INFO

    # 操作者信息
    operator_uid: str = "9622"
    operator_name: str = "System"

    # 上下文信息
    context: Dict[str, Any] = field(default_factory=dict)

    # 相关对象
    related_resource_id: Optional[str] = None
    related_dna: Optional[str] = None

    # 结果信息
    status: str = "success"  # success / failed / partial
    error_message: Optional[str] = None
    result_summary: Dict[str, Any] = field(default_factory=dict)

    # 日志本身的哈希 (用于验证日志未被篡改)
    entry_hash: str = field(default="", init=False)
    entry_id: str = field(default="", init=False)

    def __post_init__(self):
        """生成日志ID和哈希"""
        # 生成日志ID (timestamp + hash)
        log_str = f"{self.timestamp}:{self.operator_uid}:{self.event_type}:{self.message}"
        self.entry_id = hashlib.sha256(log_str.encode()).hexdigest()[:16]

        # 计算日志内容哈希 (用于检测篡改)
        self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """计算日志记录的哈希 (检测篡改)"""
        log_dict = {
            "event_type": self.event_type.value,
            "message": self.message,
            "timestamp": self.timestamp,
            "operator_uid": self.operator_uid,
            "level": self.level.value,
        }
        log_str = json.dumps(log_dict, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(log_str.encode()).hexdigest()

    def to_json_line(self) -> str:
        """转换为JSONL格式（单行JSON）"""
        log_dict = {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "level": self.level.value,
            "event_type": self.event_type.value,
            "message": self.message,
            "operator_uid": self.operator_uid,
            "operator_name": self.operator_name,
            "context": self.context,
            "related_resource_id": self.related_resource_id,
            "related_dna": self.related_dna,
            "status": self.status,
            "error_message": self.error_message,
            "result_summary": self.result_summary,
            "entry_hash": self.entry_hash,
        }
        return json.dumps(log_dict, ensure_ascii=False)

    @staticmethod
    def from_json_line(json_line: str) -> "LogEntry":
        """从JSONL格式解析日志"""
        log_dict = json.loads(json_line)

        entry = LogEntry(
            event_type=LogEventType(log_dict["event_type"]),
            message=log_dict["message"],
            timestamp=log_dict["timestamp"],
            level=LogLevel(log_dict["level"]),
            operator_uid=log_dict["operator_uid"],
            operator_name=log_dict.get("operator_name", ""),
            context=log_dict.get("context", {}),
            related_resource_id=log_dict.get("related_resource_id"),
            related_dna=log_dict.get("related_dna"),
            status=log_dict.get("status", "success"),
            error_message=log_dict.get("error_message"),
            result_summary=log_dict.get("result_summary", {}),
        )
        entry.entry_id = log_dict.get("entry_id", "")
        entry.entry_hash = log_dict.get("entry_hash", "")

        return entry


# ═══════════════════════════════════════════════════════════════
# 【Append-Only日志文件】
# ═══════════════════════════════════════════════════════════════

class AppendOnlyLog:
    """仅追加日志文件 (不可覆盖，只读)"""

    def __init__(self, log_file_path: str, log_name: str = "system"):
        self.log_file_path = log_file_path
        self.log_name = log_name
        self.entries: List[LogEntry] = []
        self.is_sealed = False  # 日志是否已密封（变成只读）

        # 创建日志文件目录
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # 尝试加载现有日志
        self._load_existing_logs()

    def _load_existing_logs(self):
        """加载现有日志文件"""
        if os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            entry = LogEntry.from_json_line(line)
                            self.entries.append(entry)
            except Exception as e:
                print(f"⚠️ 加载日志失败: {e}")

    def append_log(self, entry: LogEntry) -> bool:
        """追加日志记录"""
        if self.is_sealed:
            raise ValueError("日志已密封，不可写入")

        try:
            # 以追加模式打开文件（O_APPEND确保原子性）
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(entry.to_json_line() + '\n')
                f.flush()
                os.fsync(f.fileno())  # 强制同步到磁盘

            # 将日志记录保存到内存
            self.entries.append(entry)

            return True
        except Exception as e:
            print(f"❌ 日志写入失败: {e}")
            return False

    def seal_log(self):
        """密封日志 (变成只读)"""
        try:
            # 设置文件为只读 (chmod 444)
            os.chmod(self.log_file_path, 0o444)
            self.is_sealed = True
            print(f"✅ 日志已密封 (只读): {self.log_file_path}")
        except Exception as e:
            print(f"⚠️ 日志密封失败: {e}")

    def verify_log_integrity(self) -> Tuple[bool, List[str]]:
        """验证日志完整性 (检查是否被篡改)"""
        errors = []

        for i, entry in enumerate(self.entries):
            # 重新计算哈希并对比
            computed_hash = entry._compute_hash()
            if computed_hash != entry.entry_hash:
                errors.append(f"第 {i+1} 条日志被篡改: {entry.entry_id}")

        return len(errors) == 0, errors

    def query_logs(
        self,
        event_type: Optional[LogEventType] = None,
        level: Optional[LogLevel] = None,
        operator_uid: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[LogEntry]:
        """查询日志"""
        results = []

        for entry in self.entries:
            if event_type and entry.event_type != event_type:
                continue
            if level and entry.level != level:
                continue
            if operator_uid and entry.operator_uid != operator_uid:
                continue
            if start_time and entry.timestamp < start_time:
                continue
            if end_time and entry.timestamp > end_time:
                continue

            results.append(entry)

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """获取日志统计"""
        event_types = {}
        levels = {}

        for entry in self.entries:
            event_types[entry.event_type.value] = event_types.get(entry.event_type.value, 0) + 1
            levels[entry.level.value] = levels.get(entry.level.value, 0) + 1

        return {
            "total_entries": len(self.entries),
            "by_event_type": event_types,
            "by_level": levels,
            "log_file": self.log_file_path,
            "file_size_bytes": os.path.getsize(self.log_file_path) if os.path.exists(self.log_file_path) else 0,
            "is_sealed": self.is_sealed,
        }

    def export_to_json(self, output_path: str):
        """导出日志为JSON"""
        export_data = {
            "log_name": self.log_name,
            "export_time": datetime.now().isoformat(),
            "total_entries": len(self.entries),
            "is_sealed": self.is_sealed,
            "entries": [
                {
                    "entry_id": e.entry_id,
                    "timestamp": e.timestamp,
                    "level": e.level.value,
                    "event_type": e.event_type.value,
                    "message": e.message,
                    "operator_uid": e.operator_uid,
                    "status": e.status,
                }
                for e in self.entries
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# 【全局日志系统】
# ═══════════════════════════════════════════════════════════════

_SYSTEM_LOG = AppendOnlyLog(
    log_file_path="/Users/zuimeidedeyihan/longhun-system/logs/system_audit.jsonl",
    log_name="system_audit"
)

_WORKFLOW_LOG = AppendOnlyLog(
    log_file_path="/Users/zuimeidedeyihan/longhun-system/logs/workflow_operations.jsonl",
    log_name="workflow_operations"
)

def get_system_log() -> AppendOnlyLog:
    """获取系统日志"""
    return _SYSTEM_LOG

def get_workflow_log() -> AppendOnlyLog:
    """获取工作流日志"""
    return _WORKFLOW_LOG

def log_operation(
    event_type: LogEventType,
    message: str,
    operator_uid: str = "9622",
    operator_name: str = "System",
    level: LogLevel = LogLevel.INFO,
    context: Optional[Dict] = None,
    status: str = "success",
    error_message: Optional[str] = None,
) -> LogEntry:
    """记录操作到系统日志"""
    entry = LogEntry(
        event_type=event_type,
        message=message,
        operator_uid=operator_uid,
        operator_name=operator_name,
        level=level,
        context=context or {},
        status=status,
        error_message=error_message,
    )

    _SYSTEM_LOG.append_log(entry)
    return entry


if __name__ == "__main__":
    # 测试日志系统
    log = get_system_log()

    print("📜 龍魂Append-Only日志系统")
    print("=" * 80)

    # 记录几条日志
    log_operation(
        event_type=LogEventType.SYSTEM_START,
        message="系统启动",
        level=LogLevel.INFO,
    )

    log_operation(
        event_type=LogEventType.FILE_CREATED,
        message="创建配置文件",
        context={"file": "config.yaml", "size_bytes": 1024},
        related_resource_id="config_l0.yaml",
    )

    log_operation(
        event_type=LogEventType.DNA_GENERATED,
        message="生成DNA追溯码",
        related_dna="#龍芯⚡️2026-06-03-BAOBAO-WORKFLOW-v1.0",
    )

    # 查询日志
    print("\n最近的日志:")
    recent_logs = log.query_logs()
    for entry in recent_logs[-3:]:
        print(f"  [{entry.timestamp}] {entry.event_type.value}: {entry.message}")

    # 统计信息
    stats = log.get_statistics()
    print(f"\n日志统计:")
    print(f"  总条数: {stats['total_entries']}")
    print(f"  文件大小: {stats['file_size_bytes']} 字节")

    # 验证完整性
    is_valid, errors = log.verify_log_integrity()
    print(f"\n完整性验证: {'✅ 通过' if is_valid else '❌ 失败'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

    print("=" * 80)
