# -*- coding: utf-8 -*-
import tempfile
import unittest
from pathlib import Path

from cnsh.flow_decision.cnsh_flow_decision_core import CONFIRM_REQUIRED, GPG_REQUIRED
from cnsh.flow_field.port import flow_port


class TestFlowPort(unittest.TestCase):
    def test_flow_port_hold_without_auto_execute(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.jsonl"
            out = flow_port(
                {
                    "message": "你好，流场单口测试",
                    "operator_id": "UID9622",
                    "operator_tier": "T2",
                    "tags": {
                        "confirm_code": CONFIRM_REQUIRED,
                        "gpg": GPG_REQUIRED,
                        "title": "test",
                    },
                },
                ledger_path=ledger,
            )
            self.assertIn("particle", out)
            self.assertTrue(out.get("founder_same_rules"))
            self.assertFalse(out.get("execute_allowed", True))
            self.assertTrue(out.get("hold_for_audit"))
            self.assertIn("gate_v3", out)

    def test_flow_port_full_path_with_auto_execute(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.jsonl"
            out = flow_port(
                {
                    "message": "你好，流场单口测试，建议按已有信息处理",
                    "operator_id": "UID9622",
                    "operator_tier": "T2",
                    "auto_execute": True,
                    "evidence": "来源：单元测试；边界：不对外发布；目的：验证全链。",
                    "tags": {
                        "confirm_code": CONFIRM_REQUIRED,
                        "gpg": GPG_REQUIRED,
                        "dna_current": "#龍芯⚡️2026-05-15-FLOW-PORT-TEST-v1.0",
                        "title": "test",
                    },
                },
                ledger_path=ledger,
            )
            self.assertTrue(out.get("execute_allowed"))
            self.assertGreaterEqual(len(ledger.read_text(encoding="utf-8").strip().split("\n")), 2)

    def test_founder_same_rules_flag(self):
        out = flow_port(
            {
                "message": "测试",
                "operator_id": "UID9622",
                "operator_tier": "T0",
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=Path(tempfile.mkdtemp()) / "x.jsonl",
        )
        self.assertTrue(out.get("founder_same_rules"))


if __name__ == "__main__":
    unittest.main()
