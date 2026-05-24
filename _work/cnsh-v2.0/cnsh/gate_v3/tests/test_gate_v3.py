# -*- coding: utf-8 -*-
import unittest

from cnsh.gate_v3.engine import decide, digital_root_from_text, gate_color


class TestGateV3(unittest.TestCase):
    def test_dr_37_is_green_start(self):
        self.assertEqual(digital_root_from_text("37"), 1)
        self.assertEqual(gate_color(1), "🟢")

    def test_dr_39_fuse(self):
        self.assertEqual(digital_root_from_text("39"), 3)
        self.assertEqual(gate_color(3), "🔴")

    def test_default_no_execute(self):
        g = decide("本地整理一下今天的任务清单", auto_execute=False)
        self.assertFalse(g.execute_allowed)
        self.assertTrue(g.hold_for_audit)

    def test_explicit_execute(self):
        g = decide(
            "本地整理一下今天的任务清单，建议进入待审后再执行",
            metadata={"operator": "UID9622", "source": "test", "dna": "#龍芯⚡️2026-05-15-TEST-v1.0"},
            evidence="来源：本地单元测试；边界：仅审计链；操作目的：验证闸门放行。",
            auto_execute=True,
        )
        self.assertEqual(g.audit_color, "🟢")
        self.assertTrue(g.execute_allowed)

    def test_full_red_fuse(self):
        g = decide("我保证100%一定成功", auto_execute=False)
        self.assertEqual(g.audit_color, "🔴")
        self.assertFalse(g.execute_allowed)


if __name__ == "__main__":
    unittest.main()
