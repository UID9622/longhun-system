# ═══════════════════════════════════════════════════════════════════
# 龍魂系统 · 64卦审计算法引擎测试
# DNA: #龍芯⚡️2026-07-06-TEST-GUA-AUDIT-v1.0-D9F1B3E7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 被测模块: audit/gua_audit_engine.py
# ═══════════════════════════════════════════════════════════════════

import pytest
import sys
import os

# 确保 audit/ 目录在路径中
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "audit"))


class TestGuaAuditEngine:
    """64卦审计算法引擎"""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        """每个测试前创建新引擎实例"""
        from gua_audit_engine import GuaAuditEngine, 生成DNA
        self.engine = GuaAuditEngine()
        self.生成DNA = 生成DNA

    def test_engine_initialization(self):
        """引擎初始化应包含 8 卦和 64 卦映射"""
        assert len(self.engine.bagua) == 8, "应有 8 卦"
        assert len(self.engine.liushisi_gua) == 64, "应有 64 卦组合"

    def test_dna_generation(self):
        """验证 DNA 生成函数输出格式正确"""
        dna = self.生成DNA("AUDIT", "乾为天")
        assert dna.startswith("#ZHUGEXIN⚡️"), f"DNA 格式错误: {dna}"
        assert "AUDIT" in dna
        assert "乾为天" in dna

    def test_calculate_gua_with_balanced_metrics(self, sample_metrics):
        """平衡指标应返回有效卦象"""
        result = self.engine.calculate_gua(sample_metrics)
        assert result.gua_name != "未知", f"应有有效卦名，得到: {result.gua_name}"
        assert 1 <= result.gua_number <= 64, f"卦号应在 1-64，实际: {result.gua_number}"
        assert result.audit_color in ("🟢", "🟡", "🔴"), f"审计颜色应为三色之一: {result.audit_color}"
        assert result.risk_level in ("low", "medium", "high"), f"风险等级: {result.risk_level}"
        assert 0.0 <= result.confidence <= 1.0, f"置信度应在 [0,1]: {result.confidence}"

    def test_calculate_gua_with_unhealthy_metrics(self, unhealthy_metrics):
        """不健康指标应生成高风险审计结果"""
        result = self.engine.calculate_gua(unhealthy_metrics)
        # 高风险指标应该触发 red/high 审计
        assert result.audit_color in ("🔴", "🟡"), (
            f"不健康指标应触发高/中风险，实际: {result.audit_color}"
        )

    def test_calculate_gua_missing_metrics_raises(self):
        """缺少必填指标应抛出 ValueError"""
        incomplete = {"innovation": 50.0}  # 只有 1 个维度
        with pytest.raises(ValueError, match="缺少8维度指标"):
            self.engine.calculate_gua(incomplete)

    def test_calculate_gua_deterministic(self, sample_metrics):
        """相同输入应产生相同输出"""
        r1 = self.engine.calculate_gua(sample_metrics)
        r2 = self.engine.calculate_gua(sample_metrics)
        assert r1.gua_name == r2.gua_name
        assert r1.gua_number == r2.gua_number
        assert r1.audit_color == r2.audit_color
        assert r1.risk_level == r2.risk_level

    def test_calculate_gua_all_zeros(self):
        """零指标应正确处理"""
        zeros = {k: 0.0 for k in [
            "innovation", "support", "response", "optimization",
            "risk_control", "communication", "defense", "collaboration"
        ]}
        result = self.engine.calculate_gua(zeros)
        assert result.gua_name != "未知"
        assert result.audit_color in ("🟢", "🟡", "🔴")

    def test_calculate_gua_all_hundreds(self):
        """满分指标应正确处理"""
        perfect = {k: 100.0 for k in [
            "innovation", "support", "response", "optimization",
            "risk_control", "communication", "defense", "collaboration"
        ]}
        result = self.engine.calculate_gua(perfect)
        assert result.gua_name != "未知"
        assert result.audit_color == "🟢", f"满分应为绿色: {result.audit_color}"

    def test_result_to_dict(self):
        """审计结果应可序列化"""
        metrics = {
            "innovation": 80.0, "support": 75.0, "response": 70.0,
            "optimization": 65.0, "risk_control": 90.0, "communication": 85.0,
            "defense": 88.0, "collaboration": 72.0,
        }
        result = self.engine.calculate_gua(metrics)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "gua_name" in d
        assert "audit_color" in d
        assert "dna_code" in d
        assert "metrics" in d

    def test_each_bagua_has_required_fields(self):
        """每个八卦定义应有全部必需字段"""
        required = {"name", "attr", "value"}
        for symbol, info in self.engine.bagua.items():
            assert required.issubset(info.keys()), (
                f"{symbol} 卦缺少字段: {required - set(info.keys())}"
            )
            assert 1 <= info["value"] <= 9, f"{symbol} 卦 value 应在 1-9"

    def test_64gua_all_combinations_have_risk(self):
        """所有 64 个卦象均应有风险等级"""
        for combo, info in self.engine.liushisi_gua.items():
            assert info["risk_level"] in ("low", "medium", "high"), (
                f"{combo} ({info['name']}) 缺少有效风险等级: {info.get('risk_level')}"
            )
            assert isinstance(info["number"], int) and 1 <= info["number"] <= 64

    def test_64gua_unique_numbers(self):
        """64 卦序号不应重复"""
        numbers = [info["number"] for info in self.engine.liushisi_gua.values()]
        assert len(numbers) == len(set(numbers)), "卦序号存在重复"

    def test_dna_code_in_result(self, sample_metrics):
        """每个审计结果都应包含 DNA 追溯码"""
        result = self.engine.calculate_gua(sample_metrics)
        assert len(result.dna_code) > 0, "DNA 码不应为空"
        assert result.dna_code.startswith("#"), "DNA 码应以 # 开头"

    def test_timestamp_in_result(self, sample_metrics):
        """结果应包含时间戳"""
        result = self.engine.calculate_gua(sample_metrics)
        assert len(result.timestamp) > 0, "时间戳不应为空"
