# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cnsh.flow_decision.persona_collaboration import (  # noqa: E402
    assert_one_primary_per_gate,
    jiang_ziya_exclusive_palace,
    qiao_exclusive_write,
)


class TestPersona(unittest.TestCase):
    def test_gates_static(self):
        self.assertTrue(assert_one_primary_per_gate())
        self.assertTrue(jiang_ziya_exclusive_palace())
        self.assertTrue(qiao_exclusive_write())
