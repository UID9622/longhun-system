#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 自适应进化中枢 单元测试
DNA: #龍芯⚡️2026-07-25-EVOLUTION-TESTS-v1.0
"""

import json, os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engines.lh_adaptive_evolution import (
    AdaptiveEvolutionHub, RepeatDetector, JumpPuzzler,
    ThresholdTrigger, AntiPlagiarismGuard,
    RepeatType, FragStatus, EvoLevel,
    DATA_DIR, DEFAULT_THRESHOLDS, selftest,
)


class TestRepeatDetector(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.detector = RepeatDetector(self.tmp)

    def tearDown(self):
        for f in self.tmp.glob("*"):
            f.unlink()
        self.tmp.rmdir()

    def test_new_content(self):
        r = self.detector.detect("帮我写一个登录系统")
        self.assertFalse(r["is_repeat"])

    def test_exact_repeat_forgotten(self):
        self.detector.detect("帮我写一个登录系统")
        r = self.detector.detect("帮我写一个登录系统")
        self.assertTrue(r["is_repeat"])
        self.assertEqual(r["repeat_type"], "forgotten")
        self.assertIn("搞定", r["alert"])

    def test_similar_optimized(self):
        self.detector.detect("帮我写一个登录系统")
        r = self.detector.detect("帮我写一个登录系统，要带JWT认证")
        self.assertTrue(r["is_repeat"])
        self.assertEqual(r["repeat_type"], "optimized")
        self.assertIn("suggestion", r)

    def test_completely_different(self):
        self.detector.detect("帮我写一个登录系统")
        r = self.detector.detect("今天的天气怎么样")
        self.assertFalse(r["is_repeat"])

    def test_count_increments(self):
        for _ in range(3):
            self.detector.detect("重复测试内容")
        stats = self.detector.stats()
        self.assertEqual(stats["total"], 1)

    def test_identical_similar_sequence(self):
        """fuzzy then exact match"""
        self.detector.detect("帮我做一个数据分析面板")
        r1 = self.detector.detect("帮我做一个数据分析面板，带实时刷新")
        # After char-bigram fix, this should be detected as optimized
        self.assertTrue(r1["is_repeat"], f"Expected repeat, got: {r1}")
        self.assertIn("repeat_type", r1)
        self.assertIn(r1["repeat_type"], ["optimized", "forgotten"])
        r2 = self.detector.detect("帮我做一个数据分析面板")
        self.assertEqual(r2["repeat_type"], "forgotten")

    def test_empty_content(self):
        r = self.detector.detect("")
        self.assertFalse(r["is_repeat"])


class TestJumpPuzzler(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.puzzler = JumpPuzzler(self.tmp)

    def tearDown(self):
        for f in self.tmp.glob("*"):
            f.unlink()
        self.tmp.rmdir()

    def test_record_single(self):
        f = self.puzzler.record("新增功能A", ["feature"], "core")
        self.assertEqual(f.status, FragStatus.ISOLATED)
        self.assertEqual(f.module, "core")

    def test_auto_link_same_module(self):
        self.puzzler.record("功能A", ["feature"], "core")
        f = self.puzzler.record("功能B", ["feature"], "core")
        # f.linked_to should contain the ID of "功能A"
        self.assertTrue(len(f.linked_to) > 0, "功能B should link to 功能A via same module")
        # Verify linked fragments exist
        for lid in f.linked_to:
            linked = self.puzzler._db.get(lid)
            self.assertIsNotNone(linked, f"Linked fragment {lid} should exist")
            self.assertIn(linked.module, ["core"], f"Linked fragment should be in core module")

    def test_auto_link_same_tag(self):
        self.puzzler.record("功能A", ["evolution"], "core")
        f = self.puzzler.record("功能B", ["evolution"], "portal")
        self.assertEqual(f.status, FragStatus.LINKED)

    def test_three_frags_assemblable(self):
        self.puzzler.record("A", ["sys"], "infra")
        self.puzzler.record("B", ["sys"], "infra")
        f = self.puzzler.record("C", ["sys"], "infra")
        # C should be linked to A and B → assembled
        self.assertIn(f.status, [FragStatus.LINKED, FragStatus.ASSEMBLABLE])

    def test_report(self):
        self.puzzler.record("A", ["sys"], "infra")
        self.puzzler.record("B", ["sys"], "infra")
        self.puzzler.record("C", ["sys"], "infra")
        r = self.puzzler.report()
        self.assertGreater(r["total"], 0)
        self.assertIn("clusters", r)

    def test_different_module_no_link(self):
        self.puzzler.record("A", ["tagA"], "core")
        f = self.puzzler.record("B", ["tagB"], "portal")
        self.assertEqual(f.status, FragStatus.ISOLATED)


class TestThresholdTrigger(unittest.TestCase):
    def setUp(self):
        self.trigger = ThresholdTrigger(DATA_DIR, DEFAULT_THRESHOLDS.copy())

    def test_check_returns_dimensions(self):
        r = self.trigger.check()
        self.assertIn("dimensions", r)
        self.assertIn("should_upgrade", r)

    def test_all_dimensions_present(self):
        r = self.trigger.check()
        dims = [d["dimension"] for d in r["dimensions"]]
        for d in ["engines", "scripts", "protocols", "portals", "personalities", "dna_codes"]:
            self.assertIn(d, dims)

    def test_custom_thresholds(self):
        # Set very high thresholds so nothing triggers
        t = ThresholdTrigger(DATA_DIR, {"engines": 99999, "scripts": 99999,
                                         "protocols": 99999, "portals": 99999,
                                         "personalities": 99999, "dna_codes": 99999})
        r = t.check()
        self.assertFalse(r["should_upgrade"],
                         f"Expected no upgrade with thresholds=99999, got {r['should_upgrade']}")

    def test_low_threshold_triggers(self):
        t = ThresholdTrigger(DATA_DIR, {"engines": 1, "scripts": 1,
                                         "protocols": 1, "portals": 1,
                                         "personalities": 1, "dna_codes": 1})
        r = t.check()
        # Real project has 106 engines, way above threshold of 1
        self.assertTrue(r["should_upgrade"],
                        f"Expected upgrade trigger with thresholds=1, got {r['should_upgrade']}")

    def test_upgrade_plan_has_steps(self):
        t = ThresholdTrigger(DATA_DIR, {"engines": 1, "scripts": 1,
                                         "protocols": 1, "portals": 1,
                                         "personalities": 1, "dna_codes": 1})
        r = t.check()
        if r["should_upgrade"]:
            self.assertIn("upgrade_plan", r)
            self.assertEqual(len(r["upgrade_plan"]["steps"]), 5)
        else:
            self.skipTest("No upgrade triggered (unexpected)")

    def test_stats(self):
        s = self.trigger.stats()
        self.assertIn("counts", s)
        self.assertIn("thresholds", s)


class TestAntiPlagiarismGuard(unittest.TestCase):
    def setUp(self):
        self.guard = AntiPlagiarismGuard()

    def test_allowed_caller(self):
        self.assertTrue(self.guard.guard("uid9622"))
        self.assertTrue(self.guard.guard("lh_evolution"))
        self.assertTrue(self.guard.guard("local"))

    def test_blocked_caller(self):
        self.assertFalse(self.guard.guard("external_hacker"))
        self.assertFalse(self.guard.guard("unknown_ai"))

    def test_meltdown_after_three(self):
        self.guard.guard("bad1")
        self.guard.guard("bad2")
        self.assertFalse(self.guard.melted)
        self.guard.guard("bad3")
        self.assertTrue(self.guard.melted)


class TestAdaptiveEvolutionHub(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.hub = AdaptiveEvolutionHub(self.tmp)

    def tearDown(self):
        for f in self.tmp.glob("*"):
            f.unlink()
        for f in self.tmp.glob("*.json"):
            f.unlink()
        self.tmp.rmdir()

    def test_selftest(self):
        results = selftest()
        for k, v in results.items():
            self.assertEqual(v, "OK", f"{k} failed: {v}")

    def test_global_status(self):
        s = self.hub.global_status()
        self.assertIn("dna", s)
        self.assertIn("repeats", s)
        self.assertIn("puzzles", s)
        self.assertIn("thresholds", s)
        self.assertIn("guard", s)

    def test_full_pipeline(self):
        # 1. Repeat detection
        self.hub.detect_repeat("测试内容A")
        r = self.hub.detect_repeat("测试内容A")
        self.assertTrue(r["is_repeat"])

        # 2. Jump recording
        self.hub.record_jump("新增功能X", ["feature"], "core")
        self.hub.record_jump("新增功能Y", ["feature"], "core")
        self.hub.record_jump("新增功能Z", ["feature"], "core")
        pr = self.hub.puzzle_report()
        self.assertGreater(pr["total"], 0)

        # 3. Threshold check
        tc = self.hub.check_thresholds()
        self.assertIn("should_upgrade", tc)

        # 4. Guard
        self.hub.guard.guard("bad1")
        self.assertFalse(self.hub.guard.melted)

    def test_data_persistence(self):
        """Data should survive hub recreation."""
        self.hub.detect_repeat("持久化测试")
        self.hub.record_jump("碎片A", ["test"], "core")

        # Recreate hub (simulates restart)
        hub2 = AdaptiveEvolutionHub(self.tmp)
        self.assertGreaterEqual(hub2.repeats.stats()["total"], 1)
        self.assertGreaterEqual(hub2.puzzles.stats()["total"], 1)


class TestSimilarityComputation(unittest.TestCase):
    """验证相似度计算的边界情况。"""
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.detector = RepeatDetector(self.tmp, sim_threshold=0.3)

    def tearDown(self):
        for f in self.tmp.glob("*"):
            f.unlink()
        self.tmp.rmdir()

    def test_single_word_difference(self):
        self.detector.detect("hello world")
        r = self.detector.detect("hello world foo")
        self.assertTrue(r["is_repeat"])

    def test_no_overlap(self):
        self.detector.detect("apple banana cherry")
        r = self.detector.detect("dog cat mouse")
        self.assertFalse(r["is_repeat"])

    def test_chinese_similarity(self):
        self.detector.detect("帮我写一个登录页面")
        r = self.detector.detect("帮我写一个登录页面，加验证码功能")
        self.assertTrue(r["is_repeat"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
