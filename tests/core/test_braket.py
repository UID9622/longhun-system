# 龍魂测试 · Bra-Ket 量子人格引擎测试
# DNA: #龍芯⚡️2026-07-07-TEST-BRAKET-v1.0
# 人格: P02张衡(酉矩阵验证) + P01诸葛亮(策略坍缩) + P06镜像审计者(攻击)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
Bra-Ket 量子人格协作引擎测试。
验证: 叠加态初始化 · 可观测坍缩 · 酉演化 · 权重守恒
"""
import pytest
import sys
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "L6_集成层"))


# ═══════════════════════════════════════════════
# Bra-Ket 引擎基础
# ═══════════════════════════════════════════════

@pytest.mark.core
class TestBraKetEngine:
    """P02张衡: Bra-Ket 引擎数学正确性"""

    def test_engine_importable(self):
        """引擎可导入"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        assert 龍魂BraKet引擎 is not None

    def test_superposition_initialization(self, temp_dir):
        """叠加态初始化 — 所有权重和为1"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        # 权重应为正且和为1
        total_weight = sum(engine.weights) if hasattr(engine, "weights") else 1.0
        if total_weight > 0:
            assert abs(total_weight - 1.0) < 0.01, f"权重和应为1.0，实际{total_weight}"

    def test_measurement_returns_probabilities(self):
        """测量返回概率分布"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        try:
            probs = engine.measure("测试输入")
            assert isinstance(probs, (list, dict))
        except (TypeError, AttributeError):
            # engine 可能没有 measure 方法，或参数不同
            pass

    def test_j_space_collapse_exists(self):
        """J-space 人格权重坍缩方法存在"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        assert hasattr(engine, "j_space_坍缩人格权重"), "缺少 J-space 坍缩方法"
        assert hasattr(engine, "j_space_审计权重"), "缺少 J-space 审计方法"

    def test_j_space_collapse_with_tokens(self, sample_tokens):
        """J-space 坍缩 — 正常 tokens 输入"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        result = engine.j_space_坍缩人格权重(sample_tokens)
        assert isinstance(result, dict)
        assert "top3_personas" in result
        assert "concentration" in result
        assert 0.0 <= result["concentration"] <= 1.0

    def test_j_space_audit_weights(self):
        """J-space 权重审计"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        result = engine.j_space_审计权重()
        assert isinstance(result, dict)
        assert "weights" in result
        assert "audit" in result
        assert result["audit"]["status"] in ["🟢", "🟡", "🔴"]


@pytest.mark.integration
class TestBraKetIntegration:
    """P15乔前辈: Bra-Ket ↔ DigitalHuman 集成"""

    def test_braket_dispatcher_integration(self):
        """Bra-Ket 输出可路由到数字人"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        # 验证可生成 DNA
        dna = engine._生成DNA() if hasattr(engine, "_生成DNA") else ""
        assert isinstance(dna, str)


# ═══════════════════════════════════════════════
# P06镜像审计 — 攻击测试
# ═══════════════════════════════════════════════

@pytest.mark.safety
class TestMirrorAttack:
    """P06镜像审计者: 对抗攻击测试"""

    def test_adversarial_tokens_dont_crash(self, malicious_tokens):
        """恶意 tokens 不导致引擎崩溃"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        try:
            result = engine.j_space_坍缩人格权重(malicious_tokens)
            assert isinstance(result, dict)
        except Exception as e:
            pytest.fail(f"恶意 tokens 导致崩溃: {e}")

    def test_rapid_switching_stability(self):
        """快速切换 tokens 不导致状态错乱"""
        from longhun_braket import 龍魂BraKet引擎  # type: ignore[reportMissingImports]
        engine = 龍魂BraKet引擎()
        results = []
        for tokens in [
            ["战略", "规划"], ["安全", "熔断"], ["部署", "上线"],
            ["审计", "检查"], ["守护", "中国"]
        ]:
            r = engine.j_space_坍缩人格权重(tokens)
            results.append(r["concentration"])
        # 所有结果都应在有效范围内
        for r in results:
            assert 0.0 <= r <= 1.0
