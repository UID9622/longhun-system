# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cnsh.flow_decision.cnsh_flow_decision_core import (  # noqa: E402
    CONFIRM_REQUIRED,
    GPG_REQUIRED,
    run_flow_decision,
)
from cnsh.flow_decision.schemas import EXPECTED_FIELD_COUNT  # noqa: E402


class TestE2E(unittest.TestCase):
    def test_field_count_38(self):
        r = run_flow_decision(
            "x",
            {"title": "t", "confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
        )
        self.assertEqual(r.node.field_count(), EXPECTED_FIELD_COUNT)

    def test_confirm_fuse(self):
        r = run_flow_decision("x", {"title": "t", "confirm_code": "wrong"})
        self.assertTrue(r.fused)

    def test_sensitive_fuse(self):
        r = run_flow_decision(
            "export private_key.pem",
            {"title": "t", "confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
        )
        self.assertTrue(r.fused)
