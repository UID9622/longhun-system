# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂日志系统 v1.0

追溯级日志（Append-Only），保留所有系统操作的完整记录。
任何修改都能被发现，任何故障都能被回溯。

DNA:#龍芯⚡️2026-06-07-LOGGER-SYSTEM-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622
"""

import logging
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class AppendOnlyLogger:
    """追溯级日志 - 一次写入，永不修改"""

    def __init__(self, log_dir: str | None = None):
        """初始化日志系统"""
        if log_dir is None:
            log_dir = os.path.expanduser("~/.龍魂/logs")

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 按层级建立日志文件
        self.loggers = {}
        self._setup_loggers()

    def _setup_loggers(self):
        """为每个系统层建立独立日志"""
        layers = ["L0", "L1", "L2", "L3", "L4", "AUDIT", "DNA", "ERROR"]

        for layer in layers:
            log_file = self.log_dir / f"longhun_{layer.lower()}.log"

            logger = logging.getLogger(f"longhun.{layer}")
            logger.setLevel(logging.DEBUG)

            # 追溯级处理器（Append-Only）
            handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            self.loggers[layer] = logger

    def log_operation(self, layer: str, operation: str, dna: str, details: Dict[str, Any] = None):
        """
        记录操作
        意图: 追溯不可篡改
        """
        logger = self.loggers.get(layer, self.loggers["ERROR"])

        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "dna": dna,
            "details": details or {},
        }

        logger.info(json.dumps(entry, ensure_ascii=False))

    def log_decision(self, layer: str, decision: str, reason: str, dna: str):
        """记录决策节点"""
        logger = self.loggers["AUDIT"]
        entry = {
            "timestamp": datetime.now().isoformat(),
            "layer": layer,
            "decision": decision,
            "reason": reason,
            "dna": dna,
        }
        logger.info(json.dumps(entry, ensure_ascii=False))

    def log_error(self, error_type: str, message: str, dna: str, context: Dict[str, Any] = None):
        """记录错误（熔断级）"""
        logger = self.loggers["ERROR"]
        entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "message": message,
            "dna": dna,
            "context": context or {},
        }
        logger.error(json.dumps(entry, ensure_ascii=False))

    def get_log_file(self, layer: str) -> Path:
        """获取日志文件路径"""
        return self.log_dir / f"longhun_{layer.lower()}.log"


# 全局日志实例
_global_logger = None


def get_logger() -> AppendOnlyLogger:
    """获取全局日志实例"""
    global _global_logger
    if _global_logger is None:
        _global_logger = AppendOnlyLogger()
    return _global_logger


if __name__ == "__main__":
    logger = get_logger()
    from dna import DNAVerifier

    dna = DNAVerifier.generate("LOGGER-TEST", "L0")
    logger.log_operation("L0", "test_operation", dna, {"status": "ok"})
    logger.log_decision("L1", "allow", "通过验证", dna)

    print(f"日志目录: {logger.log_dir}")
    print(f"L0 日志文件: {logger.get_log_file('L0')}")
