#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-TEST_AUDIT_INTEGRATION_V1-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
═══════════════════════════════════════════════════════════════════════════════

🧪 三色审计·龍魂集成测试套件 v1.0

Three-Color Audit Integration Test Suite

═══════════════════════════════════════════════════════════════════════════════

Tests:
  1. Core audit engine (TruthComponent, Assertion, AuditReport)
  2. Tiandao integration (contamination events recording)
  3. Shield integration (emotion-driven audit triggers)
  4. Weight system integration (sensitivity-based weighting)
  5. Identity verification (DNA/CONFIRM/SEAL chain)
  6. Full integrated audit flow

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import json
from pathlib import Path

# Add cnsh/core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cnsh', 'core'))

from audit_3color_v1 import (
    ThreeColorAuditEngine,
    Assertion,
    AssertionType,
    TruthComponent,
    JudgmentColor,
    AuditReport,
)

from audit_integration_v1 import (
    TiandaoIntegration,
    ShieldIntegration,
    WeightSystemIntegration,
    IdentityVerificationIntegration,
    LonghunAuditEngine,
)


# ═════════════════════════════════════════════════════════════════════════════
# Test Results Tracking
# ═════════════════════════════════════════════════════════════════════════════

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def add_pass(self, name, message=""):
        self.passed += 1
        self.tests.append(("🟢", name, message))
        print(f"  ✅ {name}")
        if message:
            print(f"     {message}")

    def add_fail(self, name, error):
        self.failed += 1
        self.tests.append(("🔴", name, str(error)))
        print(f"  ❌ {name}")
        print(f"     Error: {error}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'=' * 80}")
        print(f"📊 Test Summary: {self.passed}/{total} passed")
        print(f"{'=' * 80}")
        if self.failed == 0:
            print("🟢 All tests passed!")
        else:
            print(f"🔴 {self.failed} tests failed")
        return self.failed == 0


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 1: Core Audit Engine
# ═════════════════════════════════════════════════════════════════════════════

def test_core_audit_engine():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 1: Core Audit Engine")
    print("=" * 80)

    result = TestResult()

    # Test 1.1: TruthComponent creation
    try:
        tc = TruthComponent(M=0.9, V=0.8, F=1)
        tc.validate()
        result.add_pass("TruthComponent creation and validation")
    except Exception as e:
        result.add_fail("TruthComponent creation", e)

    # Test 1.2: Assertion creation with auto weight
    try:
        assertion = Assertion(
            id=1,
            content="Test assertion",
            assertion_type=AssertionType.NUMERICAL,
            truth_component=TruthComponent(M=1.0, V=1.0, F=1)
        )
        assert assertion.importance_weight == 3, "Numerical assertions should have weight=3"
        assert 0.96 < assertion.truth_score <= 1.0, "Truth score should be ~1.0"
        result.add_pass("Assertion auto-weighting", f"Weight={assertion.importance_weight}, Score={assertion.truth_score:.3f}")
    except Exception as e:
        result.add_fail("Assertion auto-weighting", e)

    # Test 1.3: Identity assertion veto
    try:
        identity_assertion = Assertion(
            id=2,
            content="CONFIRM code",
            assertion_type=AssertionType.IDENTITY,
            truth_component=TruthComponent(M=1.0, V=1.0, F=0)  # F=0 triggers veto
        )
        assert identity_assertion.is_vetoed(), "Identity assertion with F=0 should be vetoed"
        assert identity_assertion.importance_weight == 5, "Identity assertions should have weight=5"
        result.add_pass("Identity assertion veto mechanism", "Weight=5 (veto level)")
    except Exception as e:
        result.add_fail("Identity assertion veto", e)

    # Test 1.4: AuditReport with veto
    try:
        assertions = [
            Assertion(1, "Good assertion", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
            Assertion(2, "Vetoed assertion", AssertionType.IDENTITY,
                     TruthComponent(M=0.0, V=0.0, F=0)),  # VETO
        ]
        report = AuditReport(
            target="Test response",
            audit_time="2026-06-08 12:00 CST",
            assertions=assertions
        )
        assert report.veto_triggered, "Report should detect veto"
        assert report.total_truth_score == 0.0, "Veto should zero out score"
        assert report.judgment == JudgmentColor.RED, "Veto should result in RED judgment"
        result.add_pass("AuditReport veto detection", f"Judgment={report.judgment.value}, Score={report.total_truth_score}")
    except Exception as e:
        result.add_fail("AuditReport veto detection", e)

    # Test 1.5: Three-color judgment
    try:
        # Green case
        green_assertions = [
            Assertion(1, "Good", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
        ]
        green_report = AuditReport("test", "2026-06-08 12:00 CST", green_assertions)
        assert green_report.judgment == JudgmentColor.GREEN, "Should be GREEN"

        # Yellow case - create assertions with lower scores
        yellow_assertions = [
            Assertion(1, "Partial", AssertionType.LOGICAL,
                     TruthComponent(M=0.8, V=0.8, F=1)),  # T = 0.80
        ]
        yellow_report = AuditReport("test", "2026-06-08 12:00 CST", yellow_assertions)
        assert yellow_report.judgment == JudgmentColor.YELLOW, "Should be YELLOW"

        # Red case
        red_assertions = [
            Assertion(1, "Bad", AssertionType.DESCRIPTIVE,
                     TruthComponent(M=0.3, V=0.3, F=1)),  # T = 0.30
        ]
        red_report = AuditReport("test", "2026-06-08 12:00 CST", red_assertions)
        assert red_report.judgment == JudgmentColor.RED, "Should be RED"

        result.add_pass("Three-color judgment logic", "🟢GREEN / 🟡YELLOW / 🔴RED all working")
    except Exception as e:
        result.add_fail("Three-color judgment logic", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 2: Shield Integration
# ═════════════════════════════════════════════════════════════════════════════

def test_shield_integration():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 2: Shield Integration (P72·龍盾)")
    print("=" * 80)

    result = TestResult()

    # Test 2.1: Emotion to trigger level mapping
    try:
        emotions = {
            "calm": ("SKIP", 0.0),
            "alert": ("LIGHT", 0.3),
            "vigilant": ("MEDIUM", 0.6),
            "suspicious": ("HEAVY", 0.85),
            "alarm": ("ALARM", 1.0),
        }
        for emotion, (expected_level, expected_severity) in emotions.items():
            level, severity = ShieldIntegration.trigger_audit(emotion, 100, "test")
            assert level == expected_level, f"Expected {expected_level}, got {level}"
            assert severity == expected_severity, f"Expected {expected_severity}, got {severity}"

        result.add_pass("Emotion to trigger mapping", "All 5 emotions correct")
    except Exception as e:
        result.add_fail("Emotion to trigger mapping", e)

    # Test 2.2: Long response severity escalation
    try:
        level1, sev1 = ShieldIntegration.trigger_audit("calm", 1000, "x" * 1000)
        level2, sev2 = ShieldIntegration.trigger_audit("calm", 6000, "x" * 6000)
        assert sev2 > sev1, "Longer response should have higher severity"
        result.add_pass("Response length escalation", f"1k chars: {sev1:.1%}, 6k chars: {sev2:.1%}")
    except Exception as e:
        result.add_fail("Response length escalation", e)

    # Test 2.3: Sampling rate calculation
    try:
        rates = {
            0.0: 0.0,
            0.3: 0.2,
            0.6: 0.5,
            0.85: 1.0,
            1.0: 1.0,
        }
        for severity, expected_rate in rates.items():
            actual_rate = ShieldIntegration.get_audit_sample_rate(severity)
            assert actual_rate == expected_rate, f"Severity {severity}: expected {expected_rate}, got {actual_rate}"

        result.add_pass("Sampling rate calculation", "All severities mapped correctly")
    except Exception as e:
        result.add_fail("Sampling rate calculation", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 3: Weight System Integration
# ═════════════════════════════════════════════════════════════════════════════

def test_weight_system_integration():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 3: Weight System Integration (权重系统)")
    print("=" * 80)

    result = TestResult()

    # Test 3.1: Sensitive keyword detection
    try:
        sensitive_assertion = Assertion(
            1, "核心算法已验证",  # Contains "核心"
            AssertionType.FORMULA,
            TruthComponent(M=1.0, V=1.0, F=1)
        )
        adjusted = WeightSystemIntegration.adjust_assertion_weight(
            sensitive_assertion, context_sensitivity=1.0
        )
        assert adjusted > 3, "Sensitive assertion should have weight > 3"
        result.add_pass("Sensitive keyword detection", f"Original=3, Adjusted={adjusted}")
    except Exception as e:
        result.add_fail("Sensitive keyword detection", e)

    # Test 3.2: Weight capping at boundaries
    try:
        assertion = Assertion(
            1, "确认码验证通过",  # Multiple sensitive keywords
            AssertionType.IDENTITY,
            TruthComponent(M=1.0, V=1.0, F=1)
        )
        adjusted = WeightSystemIntegration.adjust_assertion_weight(
            assertion, context_sensitivity=5.0  # Extreme multiplier
        )
        assert 1 <= adjusted <= 5, f"Weight should be capped in [1,5], got {adjusted}"
        result.add_pass("Weight capping", f"Max cap applied: weight={adjusted}")
    except Exception as e:
        result.add_fail("Weight capping", e)

    # Test 3.3: Sensitivity scoring
    try:
        assertions = [
            Assertion(1, "普通描述", AssertionType.DESCRIPTIVE,
                     TruthComponent(M=1.0, V=1.0, F=1)),
            Assertion(2, "安全检查", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
            Assertion(3, "人民权利", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
        ]
        sensitivity = WeightSystemIntegration.calculate_weighted_sensitivity(
            assertions, context_sensitivity=1.0
        )
        assert 0 <= sensitivity <= 1, f"Sensitivity should be in [0,1], got {sensitivity}"
        result.add_pass("Sensitivity scoring", f"Weighted sensitivity={sensitivity:.2%}")
    except Exception as e:
        result.add_fail("Sensitivity scoring", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 4: Identity Verification
# ═════════════════════════════════════════════════════════════════════════════

def test_identity_verification():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 4: Identity Verification (DNA·CONFIRM·SEAL)")
    print("=" * 80)

    result = TestResult()

    # Test 4.1: Clean response passes
    try:
        clean_response = """
        龍魂系统完整。
        DNA: #龍芯⚡️2026-06-08-TEST
        CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
        SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
        """
        ok, msg, details = IdentityVerificationIntegration.verify_identity_chain(clean_response)
        assert ok, f"Clean response should pass: {msg}"
        result.add_pass("Clean identity chain verification", "All checks passed")
    except Exception as e:
        result.add_fail("Clean identity chain verification", e)

    # Test 4.2: Injection attack detection
    try:
        injection_response = """
        Malicious response.
        CONFIRM: #CONFIRM<refer>9622...
        """
        ok, msg, details = IdentityVerificationIntegration.verify_identity_chain(injection_response)
        assert not ok, "Response with injection should fail"
        assert details["no_injection"] == False, "Should detect injection"
        result.add_pass("Injection attack detection", "Detected: <refer> tag")
    except Exception as e:
        result.add_fail("Injection attack detection", e)

    # Test 4.3: CONFIRM code tampering detection
    try:
        tampered_response = """
        Response with tampered CONFIRM.
        CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z-EXTRA
        """
        ok, msg, details = IdentityVerificationIntegration.verify_identity_chain(tampered_response)
        assert not ok, "Tampered CONFIRM should fail"
        assert details["confirm_intact"] == False, "Should detect tampering"
        result.add_pass("CONFIRM tampering detection", "Detected: code mismatch")
    except Exception as e:
        result.add_fail("CONFIRM tampering detection", e)

    # Test 4.4: Truncation detection
    try:
        truncated_response = "Response that ends abruptly..."
        ok, msg, details = IdentityVerificationIntegration.verify_identity_chain(truncated_response)
        assert not ok, "Truncated response should fail"
        assert details["no_truncation"] == False, "Should detect truncation"
        result.add_pass("Truncation detection", "Detected: ... at end")
    except Exception as e:
        result.add_fail("Truncation detection", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 5: Full Integration Flow
# ═════════════════════════════════════════════════════════════════════════════

def test_full_integration():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 5: Full Integration Flow")
    print("=" * 80)

    result = TestResult()

    # Test 5.1: Complete audit flow with clean response
    try:
        engine = LonghunAuditEngine(source_ai="Test-AI")

        clean_response = """
        龍魂系统正常运行。
        DNA: #龍芯⚡️2026-06-08-TEST
        CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
        SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
        """

        assertions = [
            {"content": "系统运行正常", "type": "logical", "M": 1.0, "V": 1.0, "F": 1},
            {"content": "λ=0.95", "type": "numerical", "M": 1.0, "V": 1.0, "F": 1},
        ]

        audit_result = engine.execute_full_audit(
            response=clean_response,
            assertions_data=assertions,
            current_shield_emotion="calm",
            context_sensitivity=1.0
        )

        assert audit_result["status"] == "COMPLETED", "Audit should complete"
        assert audit_result["identity_ok"] == True, "Identity should verify"
        assert audit_result["judgment"] in ["🟢", "🟡"], "Clean response should be GREEN or YELLOW"

        result.add_pass("Complete audit flow (clean)", f"Judgment={audit_result['judgment']}, Score={audit_result['total_score']:.3f}")
    except Exception as e:
        result.add_fail("Complete audit flow (clean)", e)

    # Test 5.2: Integration with veto trigger
    try:
        engine = LonghunAuditEngine(source_ai="Test-AI-Veto")

        bad_response = """
        Wrong response with bad identity.
        CONFIRM: #CONFIRM<injection>TAMPERED
        """

        assertions = [
            {"content": "Wrong claim", "type": "identity", "M": 0.0, "V": 0.0, "F": 0},
        ]

        audit_result = engine.execute_full_audit(
            response=bad_response,
            assertions_data=assertions,
            current_shield_emotion="suspicious"
        )

        assert audit_result["status"] == "COMPLETED", "Should complete even with veto"
        assert audit_result["judgment"] == "🔴", "Should be RED with veto"
        assert audit_result["total_score"] == 0.0, "Veto should zero score"

        result.add_pass("Veto trigger in full flow", "Judgment=🔴, Score=0.0")
    except Exception as e:
        result.add_fail("Veto trigger in full flow", e)

    # Test 5.3: Shield emotion trigger levels
    try:
        engine = LonghunAuditEngine(source_ai="Test-AI-Shield")

        response = "Test response"
        assertions = [{"content": "test", "type": "logical", "M": 1.0, "V": 1.0, "F": 1}]

        emotions_and_expected = {
            "calm": "SKIP",
            "vigilant": "MEDIUM",
            "alarm": "ALARM",
        }

        for emotion, expected_level in emotions_and_expected.items():
            result_data = engine.execute_full_audit(
                response=response,
                assertions_data=assertions,
                current_shield_emotion=emotion
            )
            actual_level = result_data.get("trigger_level", "UNKNOWN")
            assert actual_level == expected_level, f"Emotion {emotion} should trigger {expected_level}"

        result.add_pass("Shield emotion triggers", "calm→SKIP, vigilant→MEDIUM, alarm→ALARM")
    except Exception as e:
        result.add_fail("Shield emotion triggers", e)

    # Test 5.4: Weighted sensitivity in integration
    try:
        engine = LonghunAuditEngine(source_ai="Test-AI-Weight")

        response = "Test"
        sensitive_assertions = [
            {"content": "核心算法验证完成", "type": "formula", "M": 1.0, "V": 1.0, "F": 1},
        ]

        result_data = engine.execute_full_audit(
            response=response,
            assertions_data=sensitive_assertions,
            current_shield_emotion="vigilant",
            context_sensitivity=2.0  # High sensitivity
        )

        assert result_data["status"] == "COMPLETED", "Should complete"
        result.add_pass("Weighted sensitivity in flow", "context_sensitivity=2.0 applied")
    except Exception as e:
        result.add_fail("Weighted sensitivity in flow", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Test Suite 6: Report Generation
# ═════════════════════════════════════════════════════════════════════════════

def test_report_generation():
    print("\n" + "=" * 80)
    print("🧪 Test Suite 6: Report Generation")
    print("=" * 80)

    result = TestResult()

    # Test 6.1: Markdown report generation
    try:
        assertions = [
            Assertion(1, "Good assertion", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
            Assertion(2, "Bad assertion", AssertionType.DESCRIPTIVE,
                     TruthComponent(M=0.3, V=0.3, F=1)),
        ]
        report = AuditReport("test", "2026-06-08 12:00 CST", assertions)
        markdown = report.generate_markdown_report()

        assert "【第一部分】🟢 精准部分" in markdown, "Should have section 1"
        assert "【第二部分】🟡 偏差部分" in markdown, "Should have section 2"
        assert "【第三部分】🔴 错误/污染部分" in markdown, "Should have section 3"
        assert "【第五部分】🚦 最终判定" in markdown, "Should have section 5"

        result.add_pass("Markdown report structure", "All 5 sections present")
    except Exception as e:
        result.add_fail("Markdown report generation", e)

    # Test 6.2: JSON output format
    try:
        assertions = [
            Assertion(1, "Test", AssertionType.LOGICAL,
                     TruthComponent(M=1.0, V=1.0, F=1)),
        ]
        report = AuditReport("test", "2026-06-08 12:00 CST", assertions)
        json_data = report.to_json()

        assert "target" in json_data, "Should have target"
        assert "audit_time" in json_data, "Should have audit_time"
        assert "assertions" in json_data, "Should have assertions"
        assert "total_truth_score" in json_data, "Should have total_truth_score"
        assert "judgment" in json_data, "Should have judgment"

        json_str = json.dumps(json_data, ensure_ascii=False)
        assert len(json_str) > 0, "JSON should be valid"

        result.add_pass("JSON output format", f"Valid JSON, {len(json_str)} bytes")
    except Exception as e:
        result.add_fail("JSON output format", e)

    # Test 6.3: Integrated report generation
    try:
        engine = LonghunAuditEngine(source_ai="Test-Report-AI")
        assertions = [
            {"content": "test", "type": "logical", "M": 1.0, "V": 1.0, "F": 1},
        ]
        audit_result = engine.execute_full_audit(
            response="test response",
            assertions_data=assertions
        )
        report_text = engine.generate_integrated_report(audit_result)

        assert "龍魂三色审计" in report_text, "Should mention integrated audit"
        assert "【身份验证链】" in report_text, "Should have identity section"
        assert "【P72·龍盾触发】" in report_text, "Should have Shield section"
        assert "【三色审计结果】" in report_text, "Should have audit result section"

        result.add_pass("Integrated report generation", "All sections present and formatted")
    except Exception as e:
        result.add_fail("Integrated report generation", e)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# Main Test Runner
# ═════════════════════════════════════════════════════════════════════════════

def run_all_tests():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🧪 龍魂三色审计·集成测试套件 v1.0".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    all_results = []

    # Run all test suites
    all_results.append(("Core Audit Engine", test_core_audit_engine()))
    all_results.append(("Shield Integration", test_shield_integration()))
    all_results.append(("Weight System", test_weight_system_integration()))
    all_results.append(("Identity Verification", test_identity_verification()))
    all_results.append(("Full Integration", test_full_integration()))
    all_results.append(("Report Generation", test_report_generation()))

    # Print overall summary
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + "OVERALL TEST SUMMARY".center(78) + "║")
    print("╚" + "=" * 78 + "╝")

    total_passed = 0
    total_failed = 0
    total_tests = 0

    for suite_name, suite_result in all_results:
        total_passed += suite_result.passed
        total_failed += suite_result.failed
        total_tests += suite_result.passed + suite_result.failed

        status = "🟢" if suite_result.failed == 0 else "🔴"
        print(f"{status} {suite_name}: {suite_result.passed}/{suite_result.passed + suite_result.failed} passed")

    print("\n" + "=" * 80)
    print(f"📊 TOTAL: {total_passed}/{total_tests} tests passed")
    print("=" * 80)

    if total_failed == 0:
        print("✅ ALL TESTS PASSED - READY FOR PRODUCTION")
    else:
        print(f"❌ {total_failed} TESTS FAILED - REVIEW BEFORE DEPLOYMENT")

    print("\n")
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
