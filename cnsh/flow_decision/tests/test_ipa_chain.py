# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cnsh.flow_decision.ipa_route_registry import IPA_CHAIN  # noqa: E402
from cnsh.flow_decision.cnsh_flow_decision_core import (  # noqa: E402
    CONFIRM_REQUIRED,
    GPG_REQUIRED,
    run_flow_decision,
)


class TestIPAChain(unittest.TestCase):
    def test_eleven_nodes_registered(self):
        self.assertEqual(len(IPA_CHAIN), 11)

    def test_full_chain_pass(self):
        r = run_flow_decision(
            "正常通过",
            {"title": "t", "confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
        )
        self.assertFalse(r.fused)
        self.assertEqual(len(r.ipa_receipts), 11)
        self.assertTrue(r.node.ipa_chain_complete)
