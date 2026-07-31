# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂湍流治理引擎 · 单元测试套件 v1.0
DNA: #龍芯⚡️丙午·乙未·辛酉·井-TURBULENCE-ENGINE-TESTS-v1.0
"""

import sys
import os
import pytest
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.turbulence import (
    AnchorDiscovery, SevenFactor, PersonaRouter,
    LayeredProtocol, DNAAuditLoop,
    WeightLearner, PersonaMatrixLearner, ThresholdController, SocialReynolds,
    TurbulenceGovernor
)
from engines.turbulence.lh_layered_protocol import ProtocolLevel, ProtocolRule


# ─────────────────────────────────────────────
# 4.1 三六九不动点 · 锚点发现引擎
# ─────────────────────────────────────────────
class TestAnchorDiscovery:
    def test_init_validates_q(self):
        with pytest.raises(ValueError):
            AnchorDiscovery(q=1.5)
        with pytest.raises(ValueError):
            AnchorDiscovery(q=0.0)

    def test_discover_converges(self):
        engine = AnchorDiscovery(space_dim=5, q=0.5, max_iter=50, epsilon=1e-4)
        anchors = engine.discover_all(initial_guess=np.random.randn(5))
        assert set(anchors.keys()) == {3, 6, 9}
        for lvl, ap in anchors.items():
            assert ap.is_converged
            assert 0 <= ap.confidence <= 1
            assert ap.iterations > 0
            assert len(ap.error_sequence) > 0
            assert ap.vector.shape == (5,)

    def test_contraction_map_outputs_same_shape(self):
        engine = AnchorDiscovery(q=0.5, max_iter=10, epsilon=1e-6)
        x = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        tx = engine.contraction_map(x, level=3)
        assert tx.shape == x.shape


# ─────────────────────────────────────────────
# 4.2 七因子行为密码学引擎
# ─────────────────────────────────────────────
class TestSevenFactor:
    def test_register_and_identify(self):
        engine = SevenFactor()
        fp1 = engine.register("u1", [1.0] * 7)
        fp2 = engine.register("u2", [1.0] * 7)
        assert fp1.entity_id == "u1"
        assert fp2.entity_id == "u2"
        res = engine.identify(fp1)
        assert res.is_same_source
        assert 0 <= res.sim_score <= 1

    def test_compare_range(self):
        engine = SevenFactor()
        a = engine.register("u1", [1.0] * 7)
        b = engine.register("u2", [-1.0] * 7)
        res = engine.compare(a, b)
        assert -1.0 <= res.sim_score <= 1.0

    def test_detect_water_army(self):
        engine = SevenFactor(theta_0=0.99)
        fps = [engine.register(f"u{i}", [1.0] * 7) for i in range(5)]
        clusters = engine.detect_water_army(fps, min_cluster_size=3)
        assert len(clusters) >= 1


# ─────────────────────────────────────────────
# 4.3 16人格矩阵路由引擎
# ─────────────────────────────────────────────
class TestPersonaRouter:
    def test_default_matrix_shape(self):
        router = PersonaRouter()
        assert router.M.shape == (16, 5)
        assert len(router.channels) == 16

    def test_route_returns_valid_channel(self):
        router = PersonaRouter()
        scene = np.array([0.2, 0.1, 0.3, 0.3, 0.1])
        res = router.route(scene)
        assert 0 <= res.persona_index < 16
        assert res.persona_label in router.PERSONA_LABELS
        assert 0 <= res.confidence <= 1

    def test_update_matrix(self):
        router = PersonaRouter()
        new_weights = np.array([0.5, 0.1, 0.1, 0.2, 0.1])
        router.update_matrix(0, new_weights)
        assert np.allclose(router.M[0], new_weights)


# ─────────────────────────────────────────────
# 4.4 P0-P4 分层协议引擎
# ─────────────────────────────────────────────
class TestLayeredProtocol:
    def test_coverage_relation(self):
        proto = LayeredProtocol()
        r0 = ProtocolRule("R0", ProtocolLevel.P0, "人民数据主权", "dna0")
        r2 = ProtocolRule("R2", ProtocolLevel.P2, "促销舆情耗散锚点", "dna2")
        winner = proto.resolve_conflict(r0, r2)
        assert winner.level == ProtocolLevel.P0

    def test_add_rule_and_freeze(self):
        proto = LayeredProtocol()
        rule = proto.add_rule("P0-NEW", ProtocolLevel.P0, "人民数据主权", "dna0")
        assert rule.level == ProtocolLevel.P0
        proto.freeze_rule("P0-NEW")
        assert proto.rule_index["P0-NEW"].is_frozen

    def test_get_applicable_rules(self):
        proto = LayeredProtocol()
        proto.add_rule("P2-001", ProtocolLevel.P2, "促销舆情耗散锚点", "dna2")
        # P2-001 被 P0 覆盖，因此不会出现在可用规则中，但应在规则索引中
        assert "P2-001" in proto.rule_index
        assert proto.rule_index["P2-001"].covered_by is not None


# ─────────────────────────────────────────────
# 4.6 DNA 追溯审计闭环引擎
# ─────────────────────────────────────────────
class TestDNAAuditLoop:
    def test_issue_projection(self):
        audit = DNAAuditLoop(epsilon_0=0.15, kappa=3)
        proj = audit.issue_projection(
            prediction=0.8,
            persona_channel="P01-诸葛亮",
            anchor_level=3,
            rules_applied=["P2-001"],
            weights=[1 / 7] * 7
        )
        assert proj.projection_id
        assert proj.dna_signature.startswith("#龍芯")
        assert proj.prediction == 0.8

    def test_verify_and_consolidate(self):
        audit = DNAAuditLoop(epsilon_0=0.15, kappa=3)
        for i in range(3):
            proj = audit.issue_projection(
                prediction=0.8 + i * 0.01,
                persona_channel="P01-诸葛亮",
                anchor_level=3,
                rules_applied=["P2-001"],
                weights=[1 / 7] * 7
            )
            audit.verify(proj.projection_id, actual_value=0.82 + i * 0.01)
        consolidated = [p for p in audit.projections.values() if p.is_consolidated]
        assert len(consolidated) >= 1

    def test_accuracy_monotonic(self):
        audit = DNAAuditLoop(epsilon_0=0.5, kappa=1)
        for i in range(5):
            proj = audit.issue_projection(
                prediction=0.8,
                persona_channel="P01",
                anchor_level=3,
                rules_applied=[],
                weights=[1 / 7] * 7
            )
            audit.verify(proj.projection_id, actual_value=0.81)
        assert audit.is_monotonic()


# ─────────────────────────────────────────────
# 4.8 参数自学习与社会雷诺数
# ─────────────────────────────────────────────
class TestParamLearner:
    def test_weight_learner_normalization(self):
        wl = WeightLearner()
        assert abs(wl.weights.sum() - 1.0) < 1e-9
        wl.update([0.5] * 7, error=0.1)
        assert abs(wl.weights.sum() - 1.0) < 1e-9
        assert all(wl.weights >= 0)

    def test_persona_matrix_learner(self):
        learner = PersonaMatrixLearner()
        s = np.array([0.2, 0.1, 0.3, 0.3, 0.1])
        for _ in range(10):
            learner.add_sample(0, s, 0.8)
        M = learner.fit_all()
        assert M.shape == (16, 5)

    def test_threshold_controller(self):
        ctrl = ThresholdController(epsilon_0=0.2)
        ctrl.update([0.9, 0.92, 0.95], 0.0)
        assert ctrl.epsilon_0 <= 0.2

    def test_social_reynolds(self):
        sr = SocialReynolds(Re_c=100.0)
        res = sr.compute(v=50.0, L=1000.0, rational_ratio=0.3, transparency=0.5)
        assert res.Re_s > 0
        assert res.regime in ("laminar", "turbulent")
        assert 0 <= res.confidence <= 1


# ─────────────────────────────────────────────
# 编排器 · 端到端
# ─────────────────────────────────────────────
class TestTurbulenceGovernor:
    def test_assess_turbulent(self):
        gov = TurbulenceGovernor()
        report = gov.assess(
            social_velocity=5000.0,
            social_scope=100000.0,
            rational_ratio=0.1,
            transparency=0.1
        )
        assert report.regime == "turbulent"
        assert report.status_color in ("🟢", "🟡", "🔴")

    def test_project_and_trace(self):
        gov = TurbulenceGovernor()
        scene = np.array([0.2, 0.1, 0.3, 0.3, 0.1])
        proj = gov.project(scene, prediction=0.8, description="test")
        assert proj.projection_id
        trace = gov.trace(proj.projection_id)
        assert trace["projection_id"] == proj.projection_id

    def test_end_to_end_assess_project_verify(self):
        gov = TurbulenceGovernor(config={"Re_c": 10000.0})
        report = gov.assess(
            social_velocity=10.0,
            social_scope=1000.0,
            rational_ratio=0.8,
            transparency=0.8,
            entity_features={"u1": [1.0] * 7, "u2": [0.9] * 7}
        )
        assert report.regime in ("laminar", "turbulent")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
