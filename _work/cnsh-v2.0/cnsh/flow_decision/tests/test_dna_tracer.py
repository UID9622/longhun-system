# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cnsh.flow_decision.digital_root import compute_four_source_dr  # noqa: E402
from cnsh.flow_decision.dna_chain_tracer import derive_child_dna  # noqa: E402


class TestDNA(unittest.TestCase):
    def test_explicit_dr(self):
        dr, src = compute_four_source_dr("abc", explicit_dr=7)
        self.assertEqual(dr, 7)
        self.assertEqual(src, "explicit_dr")

    def test_child_chain(self):
        p = "#龍芯⚡️2026-05-03-PARENT-v1.0"
        c = derive_child_dna(p)
        self.assertIn("-CHILD-", c)
        self.assertTrue(c.startswith(p))
