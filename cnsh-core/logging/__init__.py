# 龍魂 Append-Only 日志系统包
# 仅追加·不可覆盖·精确到分钟·抹不掉的痕迹

from .append_only_logging import (
    AppendOnlyLog,
    LogEntry,
    LogEventType,
    LogLevel,
    get_system_log,
    get_workflow_log,
    log_operation,
)

__all__ = [
    'AppendOnlyLog',
    'LogEntry',
    'LogEventType',
    'LogLevel',
    'get_system_log',
    'get_workflow_log',
    'log_operation',
]
