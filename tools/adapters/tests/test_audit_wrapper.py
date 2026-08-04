#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
Tests for Audit Wrapper.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lh_standard_adapter.audit_wrapper import AuditWrapper, audit_wrap


class TestAuditWrapper:
    """Test seven-factor audit wrapping."""

    def __init__(self):
        self.wrapper = AuditWrapper(uid="9622")
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
        print("Test: Audit Wrapper\n")

        self.test_wrap_structure()
        self.test_signature_fields()
        self.test_pattern_classification()
        self.test_behavior_labels()
        self.test_audit_color()
        self.test_convenience_function()
        self.test_wrap_with_complex_payload()
        self.test_pattern_detection_defensive()
        self.test_pattern_detection_destroyer()

        print(f"\n{'='*50}")
        print(f"Results: {self.passed} passed, {self.failed} failed, "
              f"{self.passed + self.failed} total\n")
        return self.failed == 0

    def test_wrap_structure(self):
        print("  test_wrap_structure:")
        result = self.wrapper.wrap({"hello": "world"}, task_type="code", persona="P04")
        self._assert("audit_version" in result, "has audit_version")
        self._assert("behavior_signature" in result, "has behavior_signature")
        self._assert("behavior_pattern" in result, "has behavior_pattern")
        self._assert("behavior_labels" in result, "has behavior_labels")
        self._assert("color" in result, "has color")
        self._assert("timestamp" in result, "has timestamp")
        self._assert("payload_hash" in result, "has payload_hash")

    def test_signature_fields(self):
        print("  test_signature_fields:")
        result = self.wrapper.wrap({"x": 1}, task_type="deploy")
        sig = result["behavior_signature"]
        required = ["P", "F", "T", "E", "C", "R", "A", "X", "Y", "Z"]
        for field in required:
            self._assert(field in sig, f"has field '{field}'")
        self._assert(sig["F"] == "Fulfilled", "F default = Fulfilled")
        self._assert(sig["E"] == "Willing", "E default = Willing")

    def test_pattern_classification(self):
        print("  test_pattern_classification:")
        # Default: StableDisciplined
        sig = {"P": "HasPromise", "F": "Fulfilled", "T": 0, "E": "Willing",
               "C": 0, "R": 0, "A": "Self", "X": "Genuine", "Y": "NoResponse", "Z": 1.0}
        p = self.wrapper._classify(sig)
        self._assert(p == "MODE-StableDisciplined", f"default→StableDisciplined (got {p})")

    def test_pattern_detection_defensive(self):
        print("  test_pattern_detection_defensive:")
        sig = {"P": "HasPromise", "F": "Unfulfilled", "T": 5, "E": "Perfunctory",
               "C": 0, "R": 2, "A": "Self", "X": "OverExplain", "Y": "NoResponse", "Z": 1.0}
        p = self.wrapper._classify(sig)
        self._assert(p == "MODE-DefensiveDefaulter",
                     f"unfulfilled+overexplain→DefensiveDefaulter (got {p})")

    def test_pattern_detection_destroyer(self):
        print("  test_pattern_detection_destroyer:")
        sig = {"P": "HasPromise", "F": "Unfulfilled", "T": 10, "E": "Numb",
               "C": 0, "R": 5, "A": "Partner", "X": "Silent", "Y": "Indifferent", "Z": 1.0}
        p = self.wrapper._classify(sig)
        self._assert(p == "MODE-InternalDestroyer",
                     f"unfulfilled+indifferent→InternalDestroyer (got {p})")

    def test_behavior_labels(self):
        print("  test_behavior_labels:")
        result = self.wrapper.wrap({"test": True}, task_type="audit")
        labels = result["behavior_labels"]
        self._assert(len(labels) > 0, "has labels")
        self._assert(any(l.startswith("7F-") for l in labels), "has 7F- labels")
        self._assert(any(l.startswith("MODE-") for l in labels), "has MODE- label")

    def test_audit_color(self):
        print("  test_audit_color:")
        result = self.wrapper.wrap({"x": 1}, task_type="default")
        color = result["color"]
        self._assert(color in ("🟢", "🟡", "🔴"), f"audit color valid: {color}")

    def test_convenience_function(self):
        print("  test_convenience_function:")
        result = audit_wrap({"foo": "bar"}, task_type="test")
        self._assert("behavior_signature" in result, "convenience func works")

    def test_wrap_with_complex_payload(self):
        print("  test_wrap_with_complex_payload:")
        payload = {
            "code": "def hello(): return 'hello'",
            "language": "python",
            "metadata": {"author": "test", "version": "1.0.0"},
            "tags": ["ai", "ml", "longhun"],
        }
        result = self.wrapper.wrap(payload, task_type="code", persona="P04-Luban")
        self._assert("behavior_signature" in result, "complex payload accepted")
        ph = result.get("payload_hash", "")
        self._assert(len(ph) == 16, f"payload hash is 16 chars: {ph}")


if __name__ == "__main__":
    test = TestAuditWrapper()
    success = test.run_all()
    sys.exit(0 if success else 1)
