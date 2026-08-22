# 龍魂测试 · 共享 Fixtures
# DNA: #龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-TEST-FIXTURES-v1.0
# 人格: P02张衡(结构) + P03墨子(验证) + P04鲁班(工程)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
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

# 脚本式测试文件（设计为 `python3 tests/test_xxx.py` 独立入口，顶层 sys.exit，
# 无法被 pytest 收集）→ 从 pytest 收集范围排除（2026-08-15 工程适配）
collect_ignore = [
    "test_cnsh_model_router.py",
]


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
    # ═══════════════════════════════════════════════
    # v1.0 完整测试套件 markers (2026-08-15 追加)
    # ═══════════════════════════════════════════════
    config.addinivalue_line("markers", "audit: 代码审计测试 (P05)")
    config.addinivalue_line("markers", "functional: 功能评估测试 (P04)")
    config.addinivalue_line("markers", "smoke: 冒烟测试 (P14)")
    config.addinivalue_line("markers", "auto_iteration: 自动迭代测试 (P04)")
    config.addinivalue_line("markers", "benchmark: 性能基准测试 (P06)")
    config.addinivalue_line("markers", "api: API端到端测试 (P14)")


# ═══════════════════════════════════════════════
# v1.0 测试套件 fixtures (2026-08-15 追加)
# ═══════════════════════════════════════════════

@pytest.fixture(scope="session")
def test_env() -> Dict[str, Any]:
    """测试环境 fixture — 隔离目录 + 核心目录速查"""
    import os
    os.environ["LONGHUN_TEST_MODE"] = "true"
    return {
        "root": PROJECT_ROOT,
        "bin": PROJECT_ROOT / "08_BIN",
        "engines": PROJECT_ROOT / "05_ENGINES",
        "protocols": PROJECT_ROOT / "01_protocols",
        "temp_dir": Path(tempfile.mkdtemp(prefix="longhun_test_env_")),
    }


@pytest.fixture(scope="function")
def clean_env(test_env) -> Generator[None, None, None]:
    """清理测试环境（每个测试函数后）"""
    yield
    import shutil
    shutil.rmtree(test_env["temp_dir"], ignore_errors=True)


@pytest.fixture
def dna_check():
    """DNA追溯码检查 fixture"""
    import re
    def _check(content: str) -> bool:
        return bool(re.search(r'#龍芯⚡️', content))
    return _check


@pytest.fixture(scope="session", autouse=True)
def test_environment_setup() -> Generator[None, None, None]:
    """v1.1 测试环境自动设置与清理（session级·隔离真实数据）"""
    import os
    import shutil
    test_home = Path(tempfile.gettempdir()) / "longhun_test_env"
    test_home.mkdir(parents=True, exist_ok=True)
    os.environ["LONGHUN_HOME"] = str(test_home)
    os.environ["LONGHUN_TEST_MODE"] = "true"

    (test_home / "memory").mkdir(exist_ok=True)
    (test_home / "knowledge_graph").mkdir(exist_ok=True)

    yield

    shutil.rmtree(test_home, ignore_errors=True)
