# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cnsh.algorithms.sancai import (  # noqa: E402
    compute_sancai_decision,
    founder_case_37y,
    normalize_sancai_weights,
    parse_sancai_inputs,
    sancai_complete_check,
    sancai_flow_theta,
)


class TestSancai(unittest.TestCase):
    def test_formula3_founder_37y_passes(self):
        r = founder_case_37y()
        self.assertGreater(r.composite_score, 0.5)
        self.assertTrue(r.passed)
        self.assertAlmostEqual(r.human_weight_dynamic, 0.85, places=4)

    def test_complete_check(self):
        self.assertTrue(sancai_complete_check(0.2, 0.3, 1.0))
        self.assertFalse(sancai_complete_check(0.0, 0.3, 1.0))

    def test_human_floor_yellow(self):
        w = normalize_sancai_weights(0.35, 0.20, 0.45)
        self.assertTrue(w.clamped)
        self.assertEqual(w.tricolor_hint, "🟡")
        self.assertGreaterEqual(w.human, 0.34)

    def test_parse_tags(self):
        self.assertEqual(parse_sancai_inputs({"天": 0.2, "地": 0.3, "人": 1.0}), (0.2, 0.3, 1.0))

    def test_flow_theta_finite(self):
        t = sancai_flow_theta(0.1, 0.2, 0.3)
        self.assertTrue(-3.15 <= t <= 3.15)


if __name__ == "__main__":
    unittest.main()
