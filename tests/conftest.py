# ═══════════════════════════════════════════════════════════════════
# 龍魂系统 · 测试共享 fixtures
# DNA: #龍芯⚡️2026-07-06-TESTS-CONFTEST-v1.0-B2E5D8F7
# ═══════════════════════════════════════════════════════════════════

import sys
import os
import pytest

# 将仓库根目录加入 Python 路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "bin"))
sys.path.insert(0, os.path.join(ROOT, "audit"))
sys.path.insert(0, os.path.join(ROOT, "cnsh-core"))
sys.path.insert(0, os.path.join(ROOT, "cnsh-core", "engines"))


@pytest.fixture
def root_dir():
    """龍魂系统根目录路径"""
    return ROOT


@pytest.fixture
def sample_timestamp():
    """固定时间戳以便确定性测试"""
    return "1700000000"


@pytest.fixture
def sample_metrics():
    """返回一套平衡的 8 维度指标，用于 64 卦审计测试"""
    return {
        "innovation": 75.0,
        "support": 70.0,
        "response": 65.0,
        "optimization": 60.0,
        "risk_control": 80.0,
        "communication": 72.0,
        "defense": 85.0,
        "collaboration": 68.0,
    }


@pytest.fixture
def unhealthy_metrics():
    """返回一套高风险指标（应触发 🔴 或 🟡 审计结果）"""
    return {
        "innovation": 30.0,
        "support": 25.0,
        "response": 20.0,
        "optimization": 15.0,
        "risk_control": 10.0,
        "communication": 35.0,
        "defense": 12.0,
        "collaboration": 28.0,
    }
