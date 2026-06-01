#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计引擎 v1.1 · 优化版

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA: #龍芯⚡️2026-06-01-AUDIT-ENGINE-v1.1

改进清单:
  ✅ 统一日志等级 + 结构化JSONL格式
  ✅ 完整类型注解
  ✅ 错误处理规范化
  ✅ 日志轮转机制
  ✅ 原子性写入 (fcntl文件锁)
  ✅ Notion推送重试机制
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from __future__ import annotations

import os
import sys
import json
import time
import hashlib
import logging
import threading
import fcntl
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from logging.handlers import RotatingFileHandler
from collections import defaultdict

try:
    import requests
except ImportError:
    print("❌ 需要: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# 日志等级 (统一标准)
# ═══════════════════════════════════════════════════════════════

class AuditLogLevel(Enum):
    """审计日志等级"""
    DEBUG = 0      # 开发调试
    INFO = 1       # 正常信息
    WARN = 2       # 警告 (超时/数据缺失)
    ERROR = 3      # 错误 (业务异常)
    CRITICAL = 4   # 关键 (熔断/大故障)


# ═══════════════════════════════════════════════════════════════
# 审计日志条目结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class AuditLogEntry:
    """审计日志条目·结构化·可序列化"""

    ts: str                    # ISO8601时间戳
    level: str                 # DEBUG/INFO/WARN/ERROR/CRITICAL
    category: str              # API/AUTH/CNSH/SYNC/SYSTEM
    message: str               # 日志消息
    dna: str                   # DNA追溯码
    source: Optional[str] = None          # 来源 (服务名)
    duration: Optional[float] = None      # 执行时间(秒)
    error: Optional[str] = None           # 错误信息
    extra: Dict[str, Any] = None          # 额外字段

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        d = asdict(self)
        d["extra"] = d["extra"] or {}
        return d

    def to_jsonl(self) -> str:
        """转换为JSONL格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
# 结构化日志系统
# ═══════════════════════════════════════════════════════════════

class StructuredAuditLogger:
    """结构化审计日志·支持文件轮转·Notion推送·原子性写入"""

    def __init__(self, log_dir: str, max_bytes: int = 10485760, backup_count: int = 10):
        """初始化审计日志

        Args:
            log_dir: 日志目录
            max_bytes: 单个日志文件最大字节数 (10MB)
            backup_count: 保留的备份文件数
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # 配置标准日志 (用于控制台输出)
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.DEBUG)

        # 文件处理器 (RotatingFileHandler支持自动轮转)
        log_file = self.log_dir / "audit.log"
        file_handler = RotatingFileHandler(
            str(log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.logger.addHandler(file_handler)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter("[%(levelname)s] %(message)s")
        )
        self.logger.addHandler(console_handler)

        self._lock = threading.Lock()

    def log(
        self,
        level: AuditLogLevel,
        category: str,
        message: str,
        source: Optional[str] = None,
        duration: Optional[float] = None,
        error: Optional[str] = None,
        **extra
    ) -> AuditLogEntry:
        """记录审计日志

        Args:
            level: 日志等级
            category: 分类 (API/AUTH/CNSH/SYNC/SYSTEM)
            message: 消息
            source: 来源
            duration: 执行时间
            error: 错误信息
            **extra: 额外字段

        Returns:
            日志条目
        """
        entry = AuditLogEntry(
            ts=datetime.now(timezone.utc).isoformat(),
            level=level.name,
            category=category,
            message=message,
            dna=self._make_dna(category, message),
            source=source,
            duration=duration,
            error=error,
            extra=extra or {}
        )

        # 原子性写入 (使用文件锁防止并发冲突)
        self._write_jsonl_atomic(entry)

        # 标准日志输出
        log_level_map = {
            AuditLogLevel.DEBUG: logging.DEBUG,
            AuditLogLevel.INFO: logging.INFO,
            AuditLogLevel.WARN: logging.WARNING,
            AuditLogLevel.ERROR: logging.ERROR,
            AuditLogLevel.CRITICAL: logging.CRITICAL,
        }
        self.logger.log(log_level_map[level], entry.to_jsonl()[:500])

        return entry

    def _write_jsonl_atomic(self, entry: AuditLogEntry) -> None:
        """原子性写入JSONL文件 (使用文件锁)"""
        jsonl_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"

        try:
            with self._lock:
                with open(jsonl_file, "a", encoding="utf-8") as f:
                    # 使用fcntl文件锁 (Unix)
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    except (AttributeError, OSError):
                        pass  # Windows不支持fcntl

                    f.write(entry.to_jsonl() + "\n")
                    f.flush()
                    os.fsync(f.fileno())
        except Exception as e:
            self.logger.error(f"JSONL写入失败: {e}")

    def _make_dna(self, category: str, message: str) -> str:
        """生成DNA追溯码"""
        date = datetime.now().strftime("%Y%m%d")
        hash_val = hashlib.sha256(message.encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{date}-{category}-{hash_val}"

    def push_notion(
        self,
        entries: List[AuditLogEntry],
        token: str,
        db_id: str,
        retry: int = 3
    ) -> Tuple[int, int]:
        """批量推送到Notion (支持重试)

        Args:
            entries: 日志条目列表
            token: Notion API token
            db_id: Notion数据库ID
            retry: 重试次数

        Returns:
            (成功数, 失败数)
        """
        success_count = 0
        fail_count = 0

        for entry in entries:
            for attempt in range(retry):
                try:
                    requests.post(
                        "https://api.notion.com/v1/pages",
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Notion-Version": "2022-06-28",
                            "Content-Type": "application/json"
                        },
                        json={
                            "parent": {"database_id": db_id},
                            "properties": {
                                "时间": {"date": {"start": entry.ts.split("T")[0]}},
                                "级别": {"select": {"name": entry.level}},
                                "分类": {"select": {"name": entry.category}},
                                "消息": {"rich_text": [{"text": {"content": entry.message[:200]}}]},
                                "DNA": {"rich_text": [{"text": {"content": entry.dna}}]},
                                "来源": {"rich_text": [{"text": {"content": entry.source or ""}}]},
                            }
                        },
                        timeout=8
                    )
                    success_count += 1
                    break
                except requests.Timeout:
                    if attempt < retry - 1:
                        time.sleep(2 ** attempt)
                    else:
                        fail_count += 1
                except Exception as e:
                    self.logger.error(f"Notion推送失败: {e}")
                    fail_count += 1
                    break

        return success_count, fail_count


# ═══════════════════════════════════════════════════════════════
# 全局审计日志实例
# ═══════════════════════════════════════════════════════════════

_log_dir = os.path.expanduser("~/.cnsh/logs")
audit_logger = StructuredAuditLogger(_log_dir)


# ═══════════════════════════════════════════════════════════════
# 便利函数
# ═══════════════════════════════════════════════════════════════

def log_api_call(
    service: str,
    endpoint: str,
    duration: float,
    success: bool = True,
    error: Optional[str] = None,
    **extra
) -> None:
    """记录API调用"""
    audit_logger.log(
        level=AuditLogLevel.INFO if success else AuditLogLevel.ERROR,
        category="API",
        message=f"{service} {endpoint}",
        source=service,
        duration=duration,
        error=error,
        endpoint=endpoint,
        success=success,
        **extra
    )


def log_auth_event(
    event: str,
    success: bool = True,
    details: Optional[str] = None,
    **extra
) -> None:
    """记录认证事件"""
    audit_logger.log(
        level=AuditLogLevel.WARN if not success else AuditLogLevel.INFO,
        category="AUTH",
        message=event,
        error=details if not success else None,
        success=success,
        **extra
    )


def log_cnsh_action(
    action: str,
    result: str,
    **extra
) -> None:
    """记录CNSH动作"""
    audit_logger.log(
        level=AuditLogLevel.INFO,
        category="CNSH",
        message=f"{action}: {result}",
        **extra
    )


# ═══════════════════════════════════════════════════════════════
# 导出
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 测试
    print("🧪 审计引擎测试...")

    audit_logger.log(
        AuditLogLevel.INFO,
        "SYSTEM",
        "审计引擎启动成功"
    )

    audit_logger.log(
        AuditLogLevel.WARN,
        "API",
        "DeepSeek API 超时",
        source="deepseek",
        duration=61.5,
        error="timeout"
    )

    print("✅ 日志已写入:", _log_dir)
