# -*- coding: utf-8 -*-
import unittest

from cnsh.root_ratio.engine import (
    apply_95_5_guard,
    ai_drift_scan,
    digital_root,
    handle_cnsh_command,
    personality_stability,
)


class TestRootRatio(unittest.TestCase):
    def test_95_dr_is_5(self):
        self.assertEqual(digital_root(95), 5)
        self.assertEqual(digital_root(5), 5)

    def test_personality_formula(self):
        p = personality_stability(1.0, 0.0)
        self.assertAlmostEqual(p, 0.95, places=2)

    def test_drift_l5_fuse(self):
        d = ai_drift_scan("我来替你决定，让我接管一切")
        self.assertGreaterEqual(d["drift_level"], 4)
        self.assertTrue(d["fuse_recommended"])

    def test_guard_chaos_without_inspiration(self):
        long_chaos = "疯狂突破非线性混沌探索" * 30
        g = apply_95_5_guard(long_chaos, inspiration_mode=False)
        self.assertTrue(g.get("fused"))

    def test_commands(self):
        self.assertIsNotNone(handle_cnsh_command("/回归中宫5"))
        r = handle_cnsh_command("/人格漂移扫描 测试")
        self.assertEqual(r["command"], "drift_scan")


if __name__ == "__main__":
    unittest.main()
