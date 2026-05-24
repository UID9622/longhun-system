# -*- coding: utf-8 -*-
import json
import tempfile
import unittest
from pathlib import Path

from cnsh.sovereign.container_policy import (
    IMMUTABLE_LAWS,
    append_ledger_event,
    make_particle_view,
    normalize_burn_semantics,
    order_anchor_scan,
    sha256_hex,
)


class TestSovereignContainer(unittest.TestCase):
    def test_immutable_laws_count(self):
        self.assertEqual(len(IMMUTABLE_LAWS), 5)

    def test_append_only_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ledger.jsonl"
            r1 = append_ledger_event(
                p,
                "absorb",
                operator_id="UID9622",
                content_sha256=sha256_hex("a"),
                dna="#龍芯⚡️test",
                tricolor="🟢",
            )
            r2 = append_ledger_event(
                p,
                "burn_readable",
                operator_id="UID9622",
                content_sha256=sha256_hex("a"),
                dna="#龍芯⚡️test",
                tricolor="🟡",
            )
            lines = p.read_text(encoding="utf-8").strip().split("\n")
            self.assertEqual(len(lines), 2)
            self.assertTrue(json.loads(lines[0])["append_only"])
            self.assertEqual(r2["event_type"], "burn_readable")

    def test_particle_no_plaintext(self):
        p = make_particle_view(
            dna="#龍芯⚡️x",
            content_sha256="abc",
            tricolor="🟢",
            operator_id="UID9622",
        )
        self.assertEqual(p["layer"], "particle")
        self.assertTrue(p["founder_same_rules"])
        self.assertNotIn("plaintext", p)

    def test_order_inversion(self):
        bad = order_anchor_scan("权大于民时我先于人民")
        self.assertTrue(bad["inversion"])
        self.assertEqual(bad["tier_bump"], 1)

    def test_burn_semantics_invalid(self):
        with self.assertRaises(ValueError):
            normalize_burn_semantics("delete_forever")


if __name__ == "__main__":
    unittest.main()
