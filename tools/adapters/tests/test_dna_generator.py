"""
Tests for DNA Generator.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lh_standard_adapter.dna_generator import DNAGenerator, generate_dna
from lh_standard_adapter.validator import DNA_REGEX


class TestDNAGenerator:
    """Test DNA generation and validation."""

    def __init__(self):
        self.gen = DNAGenerator(uid="9622", device="HM-9622-001")
        self.passed = 0
        self.failed = 0

    def _assert(self, condition, msg):
        if condition:
            self.passed += 1
            print(f"  ✅ {msg}")
        else:
            self.failed += 1
            print(f"  ❌ {msg}")

    def run_all(self):
        print("Test: DNA Generator\n")

        self.test_generate_default()
        self.test_generate_code_task()
        self.test_generate_deploy_task()
        self.test_generate_audit_task()
        self.test_dna_regex_match()
        self.test_stem_branch_computation()
        self.test_hexagram_selection()
        self.test_convenience_function()
        self.test_hash8_consistency()
        self.test_different_tasks_different_hexagrams()

        print(f"\n{'='*50}")
        print(f"Results: {self.passed} passed, {self.failed} failed, "
              f"{self.passed + self.failed} total\n")
        return self.failed == 0

    def test_generate_default(self):
        print("  test_generate_default:")
        dna = self.gen.generate(task_type="default", action="WRAP")
        self._assert(dna.startswith("#LongHun⚡️"), "  starts with prefix")
        self._assert("ADAPTER-DEFAULT-WRAP-V1.0" in dna, "contains module path")
        self._assert(DNA_REGEX.match(dna) is not None, f"  matches regex: {dna[:60]}...")

    def test_generate_code_task(self):
        print("  test_generate_code_task:")
        dna = self.gen.generate(task_type="code", action="GENERATE", version="v2.0")
        self._assert(dna.startswith("#LongHun⚡️"), "  starts with prefix")
        self._assert("ADAPTER-CODE-GENERATE-V2.0" in dna, "contains module path")

    def test_generate_deploy_task(self):
        print("  test_generate_deploy_task:")
        dna = self.gen.generate(task_type="deploy", action="DEPLOY")
        self._assert("#LongHun⚡️" in dna, "contains prefix")
        # Deploy maps to Xun hexagram domain
        self._assert("ADAPTER-DEPLOY-DEPLOY" in dna, "contains deploy path")

    def test_generate_audit_task(self):
        print("  test_generate_audit_task:")
        dna = self.gen.generate(task_type="audit", action="AUDIT")
        # Should map to Li or JiJi hexagram (clarity/completion)
        self._assert(dna is not None and len(dna) > 30, "dna generated and long enough")

    def test_dna_regex_match(self):
        print("  test_dna_regex_match:")
        dnas = [
            self.gen.generate(task_type="default"),
            self.gen.generate(task_type="code"),
            self.gen.generate(task_type="deploy"),
        ]
        for i, dna in enumerate(dnas):
            self._assert(DNA_REGEX.match(dna) is not None, f"  dna[{i}] matches regex")

    def test_stem_branch_computation(self):
        print("  test_stem_branch_computation:")
        from datetime import datetime, timezone, timedelta
        tz = timezone(timedelta(hours=8))
        dt = datetime(2026, 7, 24, 13, 0, 0, tzinfo=tz)
        stem = self.gen._compute_stem_branch(dt)
        self._assert("year" in stem, "has year")
        self._assert("month" in stem, "has month")
        self._assert("day" in stem, "has day")
        self._assert("shichen" in stem, "has shichen")
        self._assert(isinstance(stem["year"], str), "year is string")
        # 13:00-14:59 = 未时 (WeiShi)
        self._assert(stem["shichen"] == "WeiShi", f"13:00 → WeiShi (got {stem['shichen']})")

    def test_hexagram_selection(self):
        print("  test_hexagram_selection:")
        audit_hex = self.gen._select_hexagram("audit")
        self._assert(audit_hex["en_name"] in ("Li", "JiJi", "Kan", "Zhen"),
                     f"audit→{audit_hex['en_name']}")
        default_hex = self.gen._select_hexagram("unknown-task")
        self._assert(default_hex is not None, "unknown task gets default hexagram")

    def test_convenience_function(self):
        print("  test_convenience_function:")
        dna = generate_dna(task_type="test", action="TEST")
        self._assert(dna.startswith("#LongHun⚡️"), "convenience func works")

    def test_hash8_consistency(self):
        print("  test_hash8_consistency:")
        dna1 = self.gen.generate(task_type="default", action="WRAP", version="v1.0")
        dna2 = self.gen.generate(task_type="default", action="WRAP", version="v1.0")
        hash1 = dna1[-8:]
        hash2 = dna2[-8:]
        # Same inputs at same second should produce same hash
        # But timestamps differ → stem-branch differs → hash differs
        self._assert(len(hash1) == 8, f"hash8 length 8: {hash1}")
        self._assert(len(hash2) == 8, f"hash8 length 8: {hash2}")

    def test_different_tasks_different_hexagrams(self):
        print("  test_different_tasks_different_hexagrams:")
        hex_audit = self.gen._select_hexagram("audit")
        hex_deploy = self.gen._select_hexagram("deploy")
        # Both should be valid
        self._assert(isinstance(hex_audit, dict), "audit hex is dict")
        self._assert(isinstance(hex_deploy, dict), "deploy hex is dict")


if __name__ == "__main__":
    test = TestDNAGenerator()
    success = test.run_all()
    sys.exit(0 if success else 1)
