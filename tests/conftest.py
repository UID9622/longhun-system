#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂测试配置 · pytest conftest

DNA: #龍芯⚡️2026-06-01-TEST-CONFIG-v1.0
"""

import pytest
import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "bridges"))

# Pytest钩子
def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line(
        "markers", "slow: 标记为慢速测试"
    )
    config.addinivalue_line(
        "markers", "integration: 标记为集成测试"
    )


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录"""
    path = Path(__file__).parent / "data"
    path.mkdir(exist_ok=True)
    return path


@pytest.fixture
def mock_logger():
    """模拟日志"""
    import logging
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    return logger
