# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 数学公式算法核心单元测试
DNA: #龍芯⚡️2026-07-25-TEST-MATH-FORMULA-CORE-v1.0
"""
import sys
import unittest
from math import isclose
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_math_formula_core import (
    AuditColor,
    SOUL_WEIGHTS,
    TruthRow,
    alpha_amp_ok,
    alpha_weight_ok,
    compress_ratio,
    cosine,
    digital_root,
    dna_chain,
    dr_gate,
    element_of,
    element_relation,
    entropy,
    hash_chain,
    magic_ok,
    normalize,
    selftest,
    softmax,
    soul_score,
    sovereignty_index,
    truth_total,
)
from engines.lh_governance_decision_chain import (
    GovernanceDecisionChain,
    GovernanceInput,
    RiskFactor,
)


class TestDigitalRoot(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(digital_root(0), 0)
        self.assertEqual(digital_root(9), 9)
        self.assertEqual(digital_root(10), 1)
        self.assertEqual(digital_root(20260603), 1)

    def test_gate(self):
        self.assertEqual(dr_gate(12), AuditColor.RED)    # dr=3
        self.assertEqual(dr_gate(15), AuditColor.YELLOW) # dr=6
        self.assertEqual(dr_gate(20260603), AuditColor.GREEN)


class TestEntropy(unittest.TestCase):
    def test_fair_coin(self):
        self.assertTrue(isclose(entropy([0.5, 0.5]), 1.0))

    def test_uniform_four(self):
        self.assertTrue(isclose(entropy([0.25] * 4), 2.0))

    def test_compress_ratio(self):
        self.assertTrue(isclose(compress_ratio(1000, 200), 0.8))
        self.assertEqual(compress_ratio(0, 100), 0.0)


class TestCosine(unittest.TestCase):
    def test_same_direction(self):
        self.assertTrue(isclose(cosine([1, 0], [1, 0]), 1.0))

    def test_orthogonal(self):
        self.assertTrue(isclose(cosine([1, 0], [0, 1]), 0.0))

    def test_opposite(self):
        self.assertTrue(isclose(cosine([1, 0], [-1, 0]), -1.0))


class TestNormalization(unittest.TestCase):
    def test_normalize(self):
        self.assertTrue(isclose(sum(normalize([1, 1, 2])), 1.0))

    def test_softmax(self):
        self.assertTrue(isclose(sum(softmax([2.0, 1.0, 0.1])), 1.0))

    def test_alpha_amp(self):
        self.assertTrue(alpha_amp_ok([0.6, 0.8]))
        self.assertFalse(alpha_amp_ok([0.5, 0.5]))

    def test_alpha_weight(self):
        self.assertTrue(alpha_weight_ok([0.4, 0.3, 0.3]))
        self.assertFalse(alpha_weight_ok([0.5, 0.3, 0.3]))


class TestTruthScore(unittest.TestCase):
    def test_clean(self):
        clean = [TruthRow(M=1.0, V=1.0, F=1, rho=3) for _ in range(5)]
        res = truth_total(clean)
        self.assertEqual(res["color"], AuditColor.GREEN)
        self.assertFalse(res["veto"])

    def test_poisoned(self):
        clean = [TruthRow(M=1.0, V=1.0, F=1, rho=3) for _ in range(5)]
        poisoned = clean + [TruthRow(M=0.0, V=0.0, F=0, rho=5)]
        res = truth_total(poisoned)
        self.assertTrue(res["veto"])
        self.assertEqual(res["score"], 0.0)
        self.assertEqual(res["color"], AuditColor.RED)


class TestSOUL(unittest.TestCase):
    def test_full(self):
        self.assertTrue(isclose(soul_score({k: 1.0 for k in SOUL_WEIGHTS}), 1.0))

    def test_zero(self):
        self.assertTrue(isclose(soul_score({k: 0.0 for k in SOUL_WEIGHTS}), 0.0))


class TestHashChain(unittest.TestCase):
    def test_chain(self):
        ch = hash_chain(["a", "b", "c"])
        self.assertEqual(len(ch), 3)
        self.assertEqual(len(set(ch)), 3)

    def test_different_input_different_hash(self):
        self.assertNotEqual(hash_chain(["a"])[0], hash_chain(["b"])[0])


class TestLuoshu(unittest.TestCase):
    def test_magic(self):
        self.assertTrue(magic_ok())

    def test_center(self):
        from engines.lh_math_formula_core import LUOSHU
        self.assertEqual(LUOSHU[1][1], 5)


class TestFiveElements(unittest.TestCase):
    def test_element_mapping(self):
        self.assertEqual(element_of(1), "木")
        self.assertEqual(element_of(5), "土")
        self.assertEqual(element_of(9), "水")

    def test_relations(self):
        self.assertEqual(element_relation("木", "火"), "生")
        self.assertEqual(element_relation("火", "金"), "克")
        self.assertEqual(element_relation("水", "木"), "生")
        self.assertEqual(element_relation("木", "木"), "同")


class TestSovereigntyIndex(unittest.TestCase):
    def test_pass(self):
        res = sovereignty_index(0.95, 0.90, 0.85)
        self.assertEqual(res["color"], AuditColor.GREEN)
        self.assertFalse(res["veto"])

    def test_veto(self):
        res = sovereignty_index(0.3, 0.9, 0.9)
        self.assertTrue(res["veto"])
        self.assertEqual(res["color"], AuditColor.RED)
        self.assertEqual(res["score"], 0.0)


class TestSelftest(unittest.TestCase):
    def test_all_pass(self):
        report = selftest()
        self.assertEqual(report["status"], "🟢")
        self.assertEqual(report["passed"], 11)


class TestGovernanceChain(unittest.TestCase):
    def test_pass(self):
        chain = GovernanceDecisionChain()
        inp = GovernanceInput(
            identifier="safe-plugin",
            tian=0.95, di=0.90, ren=0.85,
            risk_factors=[RiskFactor("x", 1.0, 0.05)],
        )
        res = chain.evaluate(inp)
        self.assertEqual(res["decision"], "PASS")

    def test_veto_tian(self):
        chain = GovernanceDecisionChain()
        inp = GovernanceInput(
            identifier="bad-base",
            tian=0.2, di=0.8, ren=0.8,
        )
        res = chain.evaluate(inp)
        self.assertEqual(res["decision"], "REJECT")

    def test_high_risk(self):
        chain = GovernanceDecisionChain()
        inp = GovernanceInput(
            identifier="risky-api",
            tian=0.75, di=0.6, ren=0.55,
            risk_factors=[RiskFactor("privacy", 2.0, 0.9)],
        )
        res = chain.evaluate(inp)
        self.assertEqual(res["decision"], "REJECT")


# ═══════════════════════════════════════════
# 左右互搏修复后新增测试（2026-07-25）
# ═══════════════════════════════════════════

class TestCosineDimensionMismatch(unittest.TestCase):
    """cosine 维度不匹配 → ValueError（不可静默截断）。"""
    def test_mismatch_raises(self):
        with self.assertRaises(ValueError):
            cosine([1, 2, 3], [1, 2])


class TestNormalizeZeroSum(unittest.TestCase):
    """normalize 全零输入 → 等权重而非全零。"""
    def test_all_zeros(self):
        r = normalize([0.0, 0.0, 0.0])
        self.assertTrue(all(abs(v - 0.333333) < 0.001 for v in r),
                        f"全零应返回等权重 1/N，实际: {r}")

    def test_empty_list(self):
        r = normalize([])
        self.assertEqual(r, [])


class TestTruthTotalEmpty(unittest.TestCase):
    """truth_total 空列表 → 🔴 拒绝。"""
    def test_empty_returns_red(self):
        res = truth_total([])
        self.assertEqual(res["color"], AuditColor.RED)
        self.assertIn("reason", res)


class TestSOULClamp(unittest.TestCase):
    """soul_score >1 的值应被 clamp 到 [0,1]。"""
    def test_clamp_high(self):
        s = soul_score({"技术": 1.5, "语言": -0.2})
        self.assertLessEqual(s, 1.0)
        self.assertGreaterEqual(s, 0.0)

    def test_missing_dim_defaults_zero(self):
        s = soul_score({"身份": 1.0})
        self.assertTrue(isclose(s, 0.05))  # 只有身份维 0.05


class TestCompressRatioBounds(unittest.TestCase):
    """compress_ratio 应在 [0, 1] 范围内。"""
    def test_negative_input(self):
        self.assertEqual(compress_ratio(-5, 100), 0.0)

    def test_expanded(self):
        """压缩后比原文大 → clamp 到 0。"""
        self.assertEqual(compress_ratio(100, 200), 0.0)

    def test_zero_original(self):
        self.assertEqual(compress_ratio(0, 100), 0.0)


class TestSIBadWeights(unittest.TestCase):
    """SI 非归一权重 → 🟡 警告，不崩溃。"""
    def test_non_normalized_weights(self):
        res = sovereignty_index(0.9, 0.8, 0.7, weights=(0.5, 0.3, 0.3))
        self.assertEqual(res["color"], AuditColor.YELLOW)
        self.assertIn("warning", res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
