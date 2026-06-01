#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计引擎单元测试

DNA: #龍芯⚡️2026-06-01-TEST-AUDIT-v1.0
"""

import pytest
import json
import tempfile
from pathlib import Path
from audit_engine_v1_1 import (
    AuditLogLevel,
    AuditLogEntry,
    StructuredAuditLogger,
    log_api_call,
    log_auth_event,
    log_cnsh_action,
)


class TestAuditLogLevel:
    """日志等级测试"""

    def test_audit_log_level_enum(self):
        """等级枚举"""
        assert AuditLogLevel.DEBUG.value == 0
        assert AuditLogLevel.INFO.value == 1
        assert AuditLogLevel.WARN.value == 2
        assert AuditLogLevel.ERROR.value == 3
        assert AuditLogLevel.CRITICAL.value == 4

    def test_audit_log_level_names(self):
        """等级名称"""
        assert AuditLogLevel.DEBUG.name == "DEBUG"
        assert AuditLogLevel.CRITICAL.name == "CRITICAL"


class TestAuditLogEntry:
    """审计日志条目测试"""

    def test_entry_creation(self):
        """条目创建"""
        entry = AuditLogEntry(
            ts="2026-06-01T10:00:00Z",
            level="INFO",
            category="API",
            message="Test message",
            dna="#龍芯⚡️20260601-API-ABC123"
        )

        assert entry.ts == "2026-06-01T10:00:00Z"
        assert entry.level == "INFO"
        assert entry.category == "API"
        assert entry.message == "Test message"

    def test_entry_to_dict(self):
        """转换为字典"""
        entry = AuditLogEntry(
            ts="2026-06-01T10:00:00Z",
            level="INFO",
            category="AUTH",
            message="Login success",
            dna="#龍芯⚡️20260601-AUTH-XYZ789",
            source="auth_service"
        )

        d = entry.to_dict()
        assert d["ts"] == "2026-06-01T10:00:00Z"
        assert d["level"] == "INFO"
        assert d["source"] == "auth_service"
        assert "extra" in d

    def test_entry_to_jsonl(self):
        """转换为JSONL"""
        entry = AuditLogEntry(
            ts="2026-06-01T10:00:00Z",
            level="WARN",
            category="API",
            message="Timeout",
            dna="#龍芯⚡️20260601-API-TIMEOUT",
            duration=61.5,
            error="timeout"
        )

        jsonl = entry.to_jsonl()
        parsed = json.loads(jsonl)

        assert parsed["level"] == "WARN"
        assert parsed["duration"] == 61.5
        assert parsed["error"] == "timeout"

    def test_entry_with_extra_fields(self):
        """带额外字段"""
        entry = AuditLogEntry(
            ts="2026-06-01T10:00:00Z",
            level="INFO",
            category="SYSTEM",
            message="System started",
            dna="#龍芯⚡️20260601-SYSTEM-START",
            extra={"version": "1.1", "environment": "production"}
        )

        d = entry.to_dict()
        assert d["extra"]["version"] == "1.1"


class TestStructuredAuditLogger:
    """结构化审计日志测试"""

    @pytest.fixture
    def temp_log_dir(self):
        """临时日志目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_logger_init(self, temp_log_dir):
        """日志初始化"""
        logger = StructuredAuditLogger(temp_log_dir)
        assert logger.log_dir == Path(temp_log_dir)
        assert logger.max_bytes == 10485760

    def test_logger_log(self, temp_log_dir):
        """日志记录"""
        logger = StructuredAuditLogger(temp_log_dir)

        entry = logger.log(
            level=AuditLogLevel.INFO,
            category="API",
            message="Test API call",
            source="gateway"
        )

        assert entry.level == "INFO"
        assert entry.category == "API"
        assert entry.source == "gateway"
        assert entry.dna.startswith("#龍芯⚡️")

    def test_logger_log_with_duration(self, temp_log_dir):
        """带执行时间的日志"""
        logger = StructuredAuditLogger(temp_log_dir)

        entry = logger.log(
            level=AuditLogLevel.INFO,
            category="API",
            message="API call completed",
            source="deepseek",
            duration=2.5
        )

        assert entry.duration == 2.5

    def test_logger_log_error(self, temp_log_dir):
        """错误日志"""
        logger = StructuredAuditLogger(temp_log_dir)

        entry = logger.log(
            level=AuditLogLevel.ERROR,
            category="API",
            message="API call failed",
            source="claude",
            error="Connection timeout"
        )

        assert entry.level == "ERROR"
        assert entry.error == "Connection timeout"

    def test_logger_multiple_logs(self, temp_log_dir):
        """多条日志"""
        logger = StructuredAuditLogger(temp_log_dir)

        for i in range(5):
            logger.log(
                level=AuditLogLevel.INFO,
                category="API",
                message=f"Message {i}",
                source="test"
            )

        # 验证日志文件存在
        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

    def test_logger_dna_generation(self, temp_log_dir):
        """DNA生成"""
        logger = StructuredAuditLogger(temp_log_dir)

        entry1 = logger.log(
            AuditLogLevel.INFO,
            "API",
            "Message 1"
        )

        entry2 = logger.log(
            AuditLogLevel.INFO,
            "API",
            "Message 2"
        )

        # 同一日期不同消息应该有不同DNA
        assert entry1.dna != entry2.dna

    def test_logger_jsonl_atomic_write(self, temp_log_dir):
        """JSONL原子性写入"""
        logger = StructuredAuditLogger(temp_log_dir)

        # 写入多条日志
        entries = []
        for i in range(3):
            entry = logger.log(
                level=AuditLogLevel.INFO,
                category="TEST",
                message=f"Test {i}"
            )
            entries.append(entry)

        # 验证文件内容
        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

        # 读取日志文件验证格式
        with open(log_files[0], "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                assert "ts" in data
                assert "level" in data
                assert "category" in data


class TestConvenienceFunctions:
    """便利函数测试"""

    @pytest.fixture
    def temp_log_dir(self):
        """临时日志目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_log_api_call_success(self, temp_log_dir):
        """API调用成功日志"""
        # 重新初始化全局logger
        import audit_engine_v1_1
        audit_engine_v1_1.audit_logger = StructuredAuditLogger(temp_log_dir)

        log_api_call(
            service="claude",
            endpoint="/chat",
            duration=1.5,
            success=True
        )

        # 验证日志写入
        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

    def test_log_api_call_failure(self, temp_log_dir):
        """API调用失败日志"""
        import audit_engine_v1_1
        audit_engine_v1_1.audit_logger = StructuredAuditLogger(temp_log_dir)

        log_api_call(
            service="deepseek",
            endpoint="/v1/messages",
            duration=30.0,
            success=False,
            error="Timeout after 30s"
        )

        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

    def test_log_auth_event_success(self, temp_log_dir):
        """认证成功日志"""
        import audit_engine_v1_1
        audit_engine_v1_1.audit_logger = StructuredAuditLogger(temp_log_dir)

        log_auth_event(
            event="user_login",
            success=True
        )

        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

    def test_log_auth_event_failure(self, temp_log_dir):
        """认证失败日志"""
        import audit_engine_v1_1
        audit_engine_v1_1.audit_logger = StructuredAuditLogger(temp_log_dir)

        log_auth_event(
            event="invalid_token",
            success=False,
            details="Token expired"
        )

        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0

    def test_log_cnsh_action(self, temp_log_dir):
        """CNSH动作日志"""
        import audit_engine_v1_1
        audit_engine_v1_1.audit_logger = StructuredAuditLogger(temp_log_dir)

        log_cnsh_action(
            action="decision_made",
            result="approved"
        )

        log_files = list(Path(temp_log_dir).glob("audit_*.jsonl"))
        assert len(log_files) > 0


# ═══════════════════════════════════════════════════════════════
# 集成测试
# ═══════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestAuditIntegration:
    """审计系统集成测试"""

    def test_full_audit_flow(self, tmp_path):
        """完整审计流程"""
        logger = StructuredAuditLogger(str(tmp_path))

        # API调用
        entry1 = logger.log(
            AuditLogLevel.INFO,
            "API",
            "deepseek /completions",
            source="deepseek",
            duration=2.5
        )

        # 认证
        entry2 = logger.log(
            AuditLogLevel.WARN,
            "AUTH",
            "invalid_token",
            error="Token expired"
        )

        # 系统事件
        entry3 = logger.log(
            AuditLogLevel.CRITICAL,
            "SYSTEM",
            "Memory threshold exceeded",
            error="Memory > 90%"
        )

        # 验证日志
        assert entry1.level == "INFO"
        assert entry2.level == "WARN"
        assert entry3.level == "CRITICAL"

        # 验证文件
        log_files = list(tmp_path.glob("audit_*.jsonl"))
        assert len(log_files) > 0
