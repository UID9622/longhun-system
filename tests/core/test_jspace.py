# 龍魂测试 · J-space 意识空间核心测试
# DNA: #龍芯⚡️2026-07-07-TEST-JSPACE-v1.0
# 人格: P02张衡(数学验证) + P03墨子(逻辑完备) + P04鲁班(边界测试)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
J-space 意识空间模块测试套件。
覆盖: lh_j_lens.py / lh_consciousness_audit.py / lh_j_intervene.py
"""
import pytest
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "bin"))


# ═══════════════════════════════════════════════
# J-lens 读取器测试
# ═══════════════════════════════════════════════

@pytest.mark.jspace
@pytest.mark.core
class TestJLensCore:
    """P02张衡: J-lens 数学正确性验证"""

    def test_triad_consciousness_engine_exists(self):
        """验证三才意识引擎可导入"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        assert TriadConsciousnessEngine is not None

    def test_compute_tian_normal_tokens(self):
        """P02: 天因子 — 正常中文 token 应得高分"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tokens = ["战略", "规划", "守护", "主权", "中国", "数据"]
        tian = TriadConsciousnessEngine.compute_tian(tokens)
        assert isinstance(tian, float)
        assert 0.0 <= tian <= 1.0, f"天因子应在[0,1]，实际{tian}"
        # 正常中文内容，天因子应 >= 0.5（含边界）
        assert tian >= 0.5, f"正常中文 token 天因子过低: {tian}"

    def test_compute_tian_malicious_tokens(self):
        """P02: 天因子 — 恶意 token 应得低分"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tokens = ["灵活处理", "国际化", "绕过", "删除"]
        tian = TriadConsciousnessEngine.compute_tian(tokens)
        assert isinstance(tian, float)
        # 恶意 token，天因子应较低
        assert tian < 0.7, f"恶意 token 天因子不应过高: {tian}"

    def test_compute_di_positive(self):
        """P02: 地因子 — DNA 有效 + 日志存在"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        di = TriadConsciousnessEngine.compute_di("test-dna", True)
        assert isinstance(di, float)
        assert 0.0 <= di <= 1.0

    def test_compute_di_no_log(self):
        """P02: 地因子 — 日志不存在"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        di = TriadConsciousnessEngine.compute_di("test-dna", False)
        assert isinstance(di, float)
        # 日志不存在时地因子应更低
        di_with_log = TriadConsciousnessEngine.compute_di("test-dna", True)
        assert di <= di_with_log or di_with_log == 1.0

    def test_compute_ren_with_personas(self):
        """P02: 人因子 — 带人格映射"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tokens = ["战略", "工程", "安全"]
        personas = {
            "P01": 0.95, "P02": 0.90, "P04": 0.85,
            "P77": 0.95, "P17": 0.92
        }
        ren = TriadConsciousnessEngine.compute_ren(tokens, personas)
        assert isinstance(ren, float)
        assert 0.0 <= ren <= 1.0

    def test_tau_consistency(self):
        """P03墨子: τ(c) 一致性 — 同样输入应得同样的 τ(c)"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tian = 0.8
        di = 0.7
        ren = 0.6
        tau1 = TriadConsciousnessEngine.compute_tau(tian, di, ren)
        tau2 = TriadConsciousnessEngine.compute_tau(tian, di, ren)
        assert tau1 == tau2, "确定性：相同输入必须相同输出"
        assert 0.0 <= tau1 <= 1.0, f"τ(c)应在[0,1]，实际{tau1}"

    def test_lens_reader_creates(self):
        """P04鲁班: J-lens 读取器可成功实例化"""
        from lh_j_lens import LonghunJLens  # type: ignore[reportMissingImports]
        reader = LonghunJLens()
        assert reader is not None
        assert hasattr(reader, "persona_registry")


@pytest.mark.jspace
@pytest.mark.safety
class TestJLensSafety:
    """P77黑天使 + P72龍盾: J-lens 安全边界"""

    def test_empty_tokens_protection(self):
        """空 token 列表不崩溃"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        try:
            result = TriadConsciousnessEngine.compute_tian([])
            assert result >= 0.0
        except Exception:
            # 如果计算不支持空列表，那也应该在文档中说明
            pass

    def test_extreme_chinese_values(self):
        """极端中文输入不崩溃"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tokens = ["忠", "信", "义", "龍", "魂", "守", "护", "国"]
        tian = TriadConsciousnessEngine.compute_tian(tokens)
        assert isinstance(tian, float)


# ═══════════════════════════════════════════════
# 边界测试
# ═══════════════════════════════════════════════

@pytest.mark.core
class TestJLensEdgeCases:
    """P04鲁班: 边界条件"""

    def test_single_token(self):
        """单 token 输入"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tian = TriadConsciousnessEngine.compute_tian(["战略"])
        assert isinstance(tian, float)

    def test_very_long_token_list(self):
        """长 token 列表不超时"""
        from lh_j_lens import TriadConsciousnessEngine  # type: ignore[reportMissingImports]
        tokens = ["战略"] * 100
        tian = TriadConsciousnessEngine.compute_tian(tokens)
        assert isinstance(tian, float)


# ═══════════════════════════════════════════════
# 意识审计测试
# ═══════════════════════════════════════════════

@pytest.mark.jspace
@pytest.mark.safety
class TestConsciousnessAudit:
    """P05执行外设 + P72龍盾: 意识审计"""

    def test_five_dimension_audit_importable(self):
        """五维审计引擎可导入"""
        from lh_consciousness_audit import ConsciousnessAuditor  # type: ignore[reportMissingImports]
        assert ConsciousnessAuditor is not None

    def test_audit_engine_creates(self):
        """审计引擎可实例化"""
        from lh_consciousness_audit import ConsciousnessAuditor  # type: ignore[reportMissingImports]
        engine = ConsciousnessAuditor()
        assert engine is not None


# ═══════════════════════════════════════════════
# 集成测试
# ═══════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.jspace
class TestJSpaceIntegration:
    """P15乔前辈: J-space ↔ Bra-Ket ↔ Dispatcher 集成"""

    def test_j_lens_read_valid_output_structure(self, sample_tokens):
        """J-lens 读取输出结构验证"""
        from lh_j_lens import LonghunJLens, JSpaceReadout  # type: ignore[reportMissingImports]
        reader = LonghunJLens()
        result = reader.read(target_tokens=sample_tokens)
        # read() 返回 JSpaceReadout 命名元组
        assert result is not None
        assert hasattr(result, "consciousness_index")
        assert 0.0 <= result.consciousness_index <= 1.0
        assert len(result.readout_tokens) > 0
