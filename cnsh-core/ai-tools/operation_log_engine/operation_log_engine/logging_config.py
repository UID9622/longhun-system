#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1294-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: logging_config.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧬 龍魂操作日記引擎 · logging_config.py

DNA:#龍芯⚡️2026-05-30-LOGGING-CONFIG-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

日誌系統配置。統一的日誌記錄和管理。
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from operation_log_engine.config import Config


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: str = "INFO",
) -> logging.Logger:
    """
    設置一個特定的 logger。

    Args:
        name: logger 名稱
        log_file: 日誌文件路徑 (如為 None，則不寫入文件)
        level: 日誌級別

    Returns:
        配置好的 logger 對象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # 如果已有 handlers，不重複添加
    if logger.hasHandlers():
        return logger

    # 日誌格式
    formatter = logging.Formatter(
        "[%(asctime)s] %(name)-20s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level.upper())
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件 handler (如果指定了日誌文件)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # 使用輪轉日誌處理器
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=Config.LOG_MAX_SIZE * 1024 * 1024,  # 轉換為 bytes
            backupCount=Config.LOG_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(level.upper())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# ==================== 核心 Logger 實例 ====================

# 主日誌
logger_main = setup_logger(
    "operation_log_engine",
    Config.LOG_FILE,
    Config.LOG_LEVEL
)

# 各個模組的 logger
logger_ledger = setup_logger(
    "operation_log_engine.ledger",
    Config.OPERATION_LOG,
    Config.LOG_LEVEL
)

logger_dna = setup_logger(
    "operation_log_engine.dna",
    Config.OPERATION_LOG,
    Config.LOG_LEVEL
)

logger_habits = setup_logger(
    "operation_log_engine.habits",
    Config.OPERATION_LOG,
    Config.LOG_LEVEL
)

logger_device = setup_logger(
    "operation_log_engine.device",
    Config.OPERATION_LOG,
    Config.LOG_LEVEL
)

logger_sync = setup_logger(
    "operation_log_engine.sync",
    Config.SYNC_LOG,
    Config.LOG_LEVEL
)

logger_multisig = setup_logger(
    "operation_log_engine.multisig",
    Config.VERIFICATION_LOG_FILE,
    Config.LOG_LEVEL
)

logger_query = setup_logger(
    "operation_log_engine.query",
    Config.LOG_FILE,
    Config.LOG_LEVEL
)

logger_error = setup_logger(
    "operation_log_engine.error",
    Config.ERROR_LOG,
    "ERROR"
)

# CLI 日誌
logger_cli = setup_logger(
    "operation_log_engine.cli",
    Config.LOG_FILE,
    Config.LOG_LEVEL
)


def get_logger(name: str) -> logging.Logger:
    """
    獲取指定名稱的 logger。

    Args:
        name: logger 名稱

    Returns:
        logger 對象
    """
    return logging.getLogger(f"operation_log_engine.{name}")


def log_operation(operation_id: str, operation_type: str, message: str, level: str = "INFO") -> None:
    """
    記錄操作日誌。

    Args:
        operation_id: 操作 ID
        operation_type: 操作類型
        message: 日誌消息
        level: 日誌級別
    """
    log_msg = f"{operation_id} [{operation_type}] {message}"
    getattr(logger_main, level.lower())(log_msg)


def log_sync_event(event_type: str, status: str, message: str) -> None:
    """
    記錄同步事件。

    Args:
        event_type: 事件類型 (sync_start, sync_complete, conflict 等)
        status: 狀態 (success, failed, warning)
        message: 事件消息
    """
    log_msg = f"[{event_type}] [{status}] {message}"
    if status == "failed":
        logger_sync.error(log_msg)
    elif status == "warning":
        logger_sync.warning(log_msg)
    else:
        logger_sync.info(log_msg)


def log_verification(operation_id: str, verdict: str, layers_status: dict) -> None:
    """
    記錄驗證結果。

    Args:
        operation_id: 操作 ID
        verdict: 驗證結果 (approved/rejected)
        layers_status: 各層驗證狀態字典
    """
    layers_str = " | ".join(
        f"{layer}: {status}"
        for layer, status in layers_status.items()
    )
    log_msg = f"{operation_id} [{verdict}] {layers_str}"
    if verdict == "rejected":
        logger_multisig.warning(log_msg)
    else:
        logger_multisig.info(log_msg)


# 初始化檢查
def verify_logging_setup() -> bool:
    """驗證日誌系統是否正確設置"""
    try:
        # 檢查日誌目錄是否可寫
        Config.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # 測試日誌寫入
        logger_main.info("🟢 日誌系統初始化完成")
        return True
    except Exception as e:
        print(f"❌ 日誌系統初始化失敗: {e}")
        return False


# 自動初始化
verify_logging_setup()
