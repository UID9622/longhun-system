#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
Tests for Validator.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lh_standard_adapter import LongHunAdapter
from lh_standard_adapter.validator import Validator, quick_validate


class TestValidator:
    """Test full-cycle validation."""

    def __init__(self):
        self.adapter = LongHunAdapter(uid="9622", device="HM-9622-001")
        self.validator = Validator()
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
        print("Test: Validator\n")

        self.test_full_cycle_valid()
        self.test_wrap_and_validate()
        self.test_quick_validate()
        self.test_empty_payload()
        self.test_invalid_dna()
        self.test_missing_key()
        self.test_uid_mismatch()
        self.test_invalid_signature_fields()
        self.test_multiple_wraps()
        self.test_get_schemas()

        print(f"\n{'='*50}")
        print(f"Results: {self.passed} passed, {self.failed} failed, "
              f"{self.passed + self.failed} total\n")
        return self.failed == 0

    def test_full_cycle_valid(self):
        print("  test_full_cycle_valid:")
        wrapped = self.adapter.wrap(
            data={"action": "deploy", "target": "portal"},
            task_type="deploy",
            persona="P14-Lvmeng",
        )
        result = self.adapter.validate(wrapped)
        self._assert(result["valid"], f"valid: {result['summary']}")

    def test_wrap_and_validate(self):
        print("  test_wrap_and_validate:")
        codes = [
            'print("hello")',
            'def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)',
            'import numpy as np; np.array([1,2,3])',
        ]
        for code in codes:
            wrapped = self.adapter.wrap(
                data={"code": code, "language": "python"},
                task_type="code",
                persona="P04-Luban",
            )
            result = self.adapter.validate(wrapped)
            self._assert(result["valid"], f"valid: {result['summary']}")

    def test_quick_validate(self):
        print("  test_quick_validate:")
        wrapped = self.adapter.wrap({"test": True}, task_type="test")
        self._assert(quick_validate(wrapped), "quick_validate passes")
        self._assert(not quick_validate({}), "quick_validate rejects empty")
        self._assert(not quick_validate({"dna": "bad"}), "quick_validate rejects partial")

    def test_empty_payload(self):
        print("  test_empty_payload:")
        result = self.adapter.validate({})
        self._assert(not result["valid"], f"empty rejected: {result['summary']}")

    def test_invalid_dna(self):
        print("  test_invalid_dna:")
        wrapped = self.adapter.wrap({"test": True}, task_type="test")
        wrapped["dna"] = "#BadDNA-xxx"
        result = self.adapter.validate(wrapped)
        self._assert(not result["valid"], f"bad DNA rejected: {result['summary']}")

    def test_missing_key(self):
        print("  test_missing_key:")
        wrapped = self.adapter.wrap({"test": True}, task_type="test")
        del wrapped["audit"]
        result = self.adapter.validate(wrapped)
        self._assert(not result["valid"], f"missing audit rejected: {result['summary']}")

    def test_uid_mismatch(self):
        print("  test_uid_mismatch:")
        wrapped = self.adapter.wrap({"test": True}, task_type="test")
        wrapped["audit"]["uid"] = "UID9876"  # Mismatch with meta.uid
        result = self.adapter.validate(wrapped)
        self._assert(not result["valid"], f"UID mismatch rejected: {result['summary']}")

    def test_invalid_signature_fields(self):
        print("  test_invalid_signature_fields:")
        wrapped = self.adapter.wrap({"test": True}, task_type="test")
        wrapped["audit"]["behavior_signature"]["F"] = "INVALID_VALUE"
        result = self.adapter.validate(wrapped)
        # Should still be structurally valid but have warnings
        self._assert(len(result.get("warnings", [])) > 0, "warnings for invalid fields")

    def test_multiple_wraps(self):
        print("  test_multiple_wraps:")
        adapter = LongHunAdapter()
        tasks = [
            ({"op": "scan"}, "audit", "P05-Shangdi"),
            ({"op": "build"}, "code", "P04-Luban"),
            ({"op": "deploy"}, "deploy", "P14-Lvmeng"),
        ]
        for payload, task, persona in tasks:
            wrapped = adapter.wrap(data=payload, task_type=task, persona=persona)
            result = adapter.validate(wrapped)
            self._assert(result["valid"], f"{task}/{persona}: {result['summary']}")

    def test_get_schemas(self):
        print("  test_get_schemas:")
        schemas = self.adapter.get_schemas()
        self._assert("dna_schema" in schemas, "has dna_schema")
        self._assert("audit_schema" in schemas, "has audit_schema")
        self._assert(isinstance(schemas["dna_schema"], dict), "dna_schema is dict")
        self._assert(isinstance(schemas["audit_schema"], dict), "audit_schema is dict")


if __name__ == "__main__":
    test = TestValidator()
    success = test.run_all()
    sys.exit(0 if success else 1)
