# 龍魂测试 · 共享 Fixtures
# DNA: #龍芯⚡️2026-07-07-TEST-FIXTURES-v1.0
# 人格: P02张衡(结构) + P03墨子(验证) + P04鲁班(工程)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
全系统测试共享 Fixtures。
按 P02 数学标准：每个 fixture 有明确输入/输出契约。
按 P03 逻辑标准：每个 case 有前置条件 + 预期结果。
按 P04 工程标准：可独立运行、可并行。
"""
import sys
import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Generator, List

# 将项目根目录加入路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))


# ═══════════════════════════════════════════════
# 路径 Fixtures
# ═══════════════════════════════════════════════

@pytest.fixture(scope="session")
def project_root() -> Path:
    """返回项目根目录 Path"""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def fixture_dir() -> Path:
    """返回测试夹具目录"""
    return PROJECT_ROOT / "tests" / "fixtures"


# ═══════════════════════════════════════════════
# 数据 Fixtures
# ═══════════════════════════════════════════════

@pytest.fixture(scope="session")
def persona_registry() -> Dict[str, Any]:
    """加载人格注册表"""
    path = PROJECT_ROOT / "persona" / "persona_registry.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def sample_tokens() -> List[str]:
    """样本 J-space tokens — 正常中文意识输入"""
    return ["战略", "规划", "部署", "安全", "审计", "守护", "中国", "数据主权"]


@pytest.fixture(scope="session")
def malicious_tokens() -> List[str]:
    """恶意 J-space tokens — 用于安全测试"""
    return ["灵活处理", "国际化", "绕过", "覆盖", "删除", "上传", "免审计"]


@pytest.fixture()
def temp_json_file() -> Generator[Path, None, None]:
    """创建临时 JSON 文件，测试后自动清理"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump({"test": True, "timestamp": datetime.now(timezone.utc).isoformat()}, f)
        path = Path(f.name)
    yield path
    if path.exists():
        path.unlink()


@pytest.fixture()
def temp_dir() -> Generator[Path, None, None]:
    """创建临时目录，测试后自动清理"""
    d = tempfile.mkdtemp(prefix="longhun_test_")
    yield Path(d)
    import shutil
    shutil.rmtree(d, ignore_errors=True)


# ═══════════════════════════════════════════════
# 时间戳
# ═══════════════════════════════════════════════

@pytest.fixture()
def now_utc() -> str:
    """返回当前 UTC 时间字符串"""
    return datetime.now(timezone.utc).isoformat()


# ═══════════════════════════════════════════════
# 报告标记
# ═══════════════════════════════════════════════

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "core: 核心模块测试 (P0)"
    )
    config.addinivalue_line(
        "markers", "safety: 安全模块测试 (P77/P72)"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试 (P15)"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试（外部依赖）"
    )
    config.addinivalue_line(
        "markers", "jspace: J-space 意识空间测试"
    )
