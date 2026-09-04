# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-CORE-UNNAMED-FILE15-v1.0-18
# 君子协议: 本文件受龍魂DNA追溯保护

# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
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
