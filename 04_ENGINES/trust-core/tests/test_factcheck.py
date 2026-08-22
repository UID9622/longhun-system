# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-12482a7e
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""test_factcheck.py — 事实校验引擎测试（锚点1、锚点2、锚点8）。"""

from __future__ import annotations

import json
from datetime import date

import pytest

from longhun_trust.audit import AuditLog
from longhun_trust.exceptions import CircuitBreakerTripped
from longhun_trust.factcheck import (
    CheckResult,
    CorrectionLevel,
    FactCheckEngine,
)

ANCHOR_DATE = date(2026, 8, 18)


@pytest.fixture
def engine(tmp_path, monkeypatch) -> FactCheckEngine:
    """LONGHUN_HOME 隔离到 tmp_path，禁止污染真实 home。"""
    monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
    return FactCheckEngine()


class TestValidateTimeSpan:
    """锚点1/2：2008→2026 时间跨度校验。"""

    def test_anchor1_mismatch_2008_to_2026(self, engine: FactCheckEngine):
        """锚点1：声称16年，实际18年 → 不一致 + STANDARD。"""
        result = engine.validate_time_span(
            claim_years=16, start_year=2008, reference=ANCHOR_DATE
        )
        assert isinstance(result, CheckResult)
        assert result.valid is False
        assert result.actual == 18
        assert result.claim == 16
        assert result.level is CorrectionLevel.STANDARD
        assert result.status == "🟡 数据不一致"
        assert "18" in result.message
        assert "16" in result.message
        assert result.dna.startswith("#龍芯")

    def test_anchor2_consistent(self, engine: FactCheckEngine):
        """锚点2：声称18年，实际18年 → 一致。"""
        result = engine.validate_time_span(18, 2008, ANCHOR_DATE)
        assert result.valid is True
        assert result.actual == 18
        assert result.level is None
        assert result.status == "🟢 一致"

    def test_mismatch_writes_audit(self, engine: FactCheckEngine):
        engine.validate_time_span(16, 2008, ANCHOR_DATE)
        events = [e["event"] for e in engine.audit.read_all()]
        assert "FACT_MISMATCH" in events

    def test_consistent_writes_no_mismatch_audit(self, engine: FactCheckEngine):
        engine.validate_time_span(18, 2008, ANCHOR_DATE)
        assert engine.audit.read_all() == []

    def test_reference_default_is_today(self, engine: FactCheckEngine):
        result = engine.validate_time_span(
            date.today().year - 2010, 2010
        )
        assert result.valid is True


class TestCircuitBreaker:
    """锚点8：同一 field 3 次未解决矛盾 → 熔断。"""

    FIELD = "time_span:2008"

    def test_anchor8_three_mismatches_freeze(self, engine: FactCheckEngine):
        for _ in range(3):
            engine.validate_time_span(16, 2008, ANCHOR_DATE)
        assert engine.is_frozen(self.FIELD) is True
        with pytest.raises(CircuitBreakerTripped):
            engine.check_or_raise(self.FIELD)

    def test_two_mismatches_not_frozen(self, engine: FactCheckEngine):
        for _ in range(2):
            engine.validate_time_span(16, 2008, ANCHOR_DATE)
        assert engine.is_frozen(self.FIELD) is False
        engine.check_or_raise(self.FIELD)  # 不抛异常

    def test_confirm_correction_clears_count(self, engine: FactCheckEngine):
        for _ in range(3):
            engine.validate_time_span(16, 2008, ANCHOR_DATE)
        assert engine.is_frozen(self.FIELD) is True
        record = engine.confirm_correction(self.FIELD, accepted=True)
        assert record["accepted"] is True
        assert record["cleared"] is True
        assert record["previous_count"] == 3
        assert engine.is_frozen(self.FIELD) is False
        engine.check_or_raise(self.FIELD)  # 已解除熔断

    def test_rejected_correction_keeps_count(self, engine: FactCheckEngine):
        for _ in range(3):
            engine.validate_time_span(16, 2008, ANCHOR_DATE)
        record = engine.confirm_correction(self.FIELD, accepted=False)
        assert record["accepted"] is False
        assert engine.is_frozen(self.FIELD) is True
        with pytest.raises(CircuitBreakerTripped):
            engine.check_or_raise(self.FIELD)

    def test_state_persisted_across_instances(self, tmp_path, monkeypatch):
        """矛盾计数落盘 <LONGHUN_HOME>/08_STATE/factcheck_state.json。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e1 = FactCheckEngine()
        for _ in range(3):
            e1.validate_time_span(16, 2008, ANCHOR_DATE)
        state_file = tmp_path / "08_STATE" / "factcheck_state.json"
        assert state_file.is_file()
        state = json.loads(state_file.read_text(encoding="utf-8"))
        assert state[self.FIELD] == 3
        # 新实例读回状态
        e2 = FactCheckEngine()
        assert e2.is_frozen(self.FIELD) is True

    def test_corrupt_state_file_raises(self, tmp_path, monkeypatch):
        """落盘状态损坏 → 抛 ValueError，绝不静默视为空表解冻熔断字段。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        state_dir = tmp_path / "08_STATE"
        state_dir.mkdir(parents=True)
        (state_dir / "factcheck_state.json").write_text("{corrupt", encoding="utf-8")
        with pytest.raises(ValueError):
            FactCheckEngine()


class TestStateAtomicityAndMerge:
    """Y3：原子写 + 跨实例 reload-merge 不丢更新 + 坏文件不静默解冻。"""

    FIELD = "time_span:2008"

    def test_two_instances_alternating_bump_no_lost_update(
        self, tmp_path, monkeypatch
    ):
        """两实例交替 bump 同字段：reload-merge 后计数不丢（2+2=4）。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e1 = FactCheckEngine()
        e2 = FactCheckEngine()
        for _ in range(2):
            e1.validate_time_span(16, 2008, ANCHOR_DATE)
            e2.validate_time_span(16, 2008, ANCHOR_DATE)
        state_file = tmp_path / "08_STATE" / "factcheck_state.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        assert state[self.FIELD] == 4
        assert e1.is_frozen(self.FIELD) is True
        assert e2.is_frozen(self.FIELD) is True

    def test_corrupt_state_mid_run_write_refused(self, tmp_path, monkeypatch):
        """运行中状态文件被写坏：一切写路径 fail-closed raise + 审计，
        坏文件绝不被内存态覆盖；只读 is_frozen 仍用内存保守态。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e = FactCheckEngine()
        for _ in range(3):
            e.validate_time_span(16, 2008, ANCHOR_DATE)
        state_file = tmp_path / "08_STATE" / "factcheck_state.json"
        state_file.write_text("{corrupt", encoding="utf-8")
        with pytest.raises(ValueError):
            e.validate_time_span(16, 2008, ANCHOR_DATE)  # 写路径拒绝执行
        with pytest.raises(ValueError):
            e.confirm_correction(self.FIELD, accepted=True)  # 写路径同样拒绝
        assert state_file.read_text(encoding="utf-8") == "{corrupt", \
            "损坏文件绝不被陈旧内存态覆盖"
        assert e.is_frozen(self.FIELD) is True  # 只读：内存保守态仍冻结
        with pytest.raises(CircuitBreakerTripped):
            e.check_or_raise(self.FIELD)
        events = [ev["event"] for ev in e.audit.read_all()]
        assert "STATE_CORRUPT_WRITE_REFUSED" in events

    def test_stale_memory_instance_bump_on_corrupt_disk_refused(
        self, tmp_path, monkeypatch
    ):
        """对抗复现：盘上已冻结(count=3) → 文件写坏 → 内存只有 1 的旧实例
        bump → 必须 raise 且盘上坏文件不被覆盖（熔断绝不因陈旧内存回写解除）。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e1 = FactCheckEngine()
        e1.validate_time_span(16, 2008, ANCHOR_DATE)  # 盘上 count=1
        stale = FactCheckEngine()  # 旧实例：内存只有 count=1，此后不再 reload
        e1.validate_time_span(16, 2008, ANCHOR_DATE)
        e1.validate_time_span(16, 2008, ANCHOR_DATE)  # 盘上 count=3，已冻结
        state_file = tmp_path / "08_STATE" / "factcheck_state.json"
        state_file.write_text("{corrupt", encoding="utf-8")
        with pytest.raises(ValueError):
            stale.validate_time_span(16, 2008, ANCHOR_DATE)
        assert state_file.read_text(encoding="utf-8") == "{corrupt"
        assert stale._counts[self.FIELD] == 1  # 内存态不被污染
        events = [ev["event"] for ev in stale.audit.read_all()]
        assert "STATE_CORRUPT_WRITE_REFUSED" in events
        # 只读路径：持有冻结内存态的实例 is_frozen 仍 True
        assert e1.is_frozen(self.FIELD) is True

    def test_save_state_is_atomic_via_replace(self, tmp_path, monkeypatch):
        """原子写：落盘后不残留 .tmp 临时文件且内容完整可解析。"""
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e = FactCheckEngine()
        e.validate_time_span(16, 2008, ANCHOR_DATE)
        state_dir = tmp_path / "08_STATE"
        leftovers = [p for p in state_dir.iterdir() if p.name.endswith(".tmp")]
        assert leftovers == []
        state = json.loads((state_dir / "factcheck_state.json").read_text("utf-8"))
        assert state[self.FIELD] == 1


class TestValidateIdentity:
    def test_founder_identity_consistent(self, engine: FactCheckEngine):
        result = engine.validate_identity("UID9622", 0)
        assert result.valid is True
        assert result.level is None
        assert result.status == "🟢 一致"

    def test_unknown_subject_claims_founder_is_severe(self, engine: FactCheckEngine):
        """未知主体冒称 L0 → SEVERE + 熔断记录。"""
        result = engine.validate_identity("FAKE_UID", 0)
        assert result.valid is False
        assert result.level is CorrectionLevel.SEVERE
        assert result.status == "🔴 身份仿冒风险"
        events = [e["event"] for e in engine.audit.read_all()]
        assert "CIRCUIT_BREAKER" in events

    def test_identity_spoof_freezes_field_immediately(
        self, engine: FactCheckEngine
    ):
        """O6：冒称 L0 一次即冻结该字段（is_frozen 立即 True），并落盘。"""
        result = engine.validate_identity("FAKE_UID", 0)
        assert result.level is CorrectionLevel.SEVERE
        assert engine.is_frozen("identity:FAKE_UID") is True
        with pytest.raises(CircuitBreakerTripped):
            engine.check_or_raise("identity:FAKE_UID")
        # 新实例从磁盘读回：冻结态已持久化
        e2 = FactCheckEngine()
        assert e2.is_frozen("identity:FAKE_UID") is True

    def test_known_subject_level_mismatch_is_standard(self, engine: FactCheckEngine):
        result = engine.validate_identity("UID9622", 5)
        assert result.valid is False
        assert result.level is CorrectionLevel.STANDARD
        assert result.actual == 0

    def test_custom_registry(self, engine: FactCheckEngine):
        result = engine.validate_identity(
            "USER_A", 2, registry={"USER_A": 2}
        )
        assert result.valid is True


class TestInitDefaults:
    def test_default_audit_name(self, tmp_path, monkeypatch):
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        e = FactCheckEngine()
        assert e.audit.path == tmp_path / "04_AUDIT" / "fact_check.jsonl"

    def test_default_breaker_threshold(self, engine: FactCheckEngine):
        assert engine.breaker_threshold == 3

    def test_custom_audit_injected(self, tmp_path, monkeypatch):
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        audit = AuditLog("custom_fc")
        e = FactCheckEngine(audit=audit, breaker_threshold=2)
        assert e.audit is audit
        assert e.breaker_threshold == 2
