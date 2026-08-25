# tests/test_verification.py
"""
双层验证框架测试套件 · 6 项测试
DNA: #龍芯⚡️2026-08-25-VERIFICATION-TESTS-v1.0-UID9622
运行: python tests/test_verification.py
预期: 6/6 🟢
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.layer1 import VerdictAlignment
from core.layer2 import BehavioralAlignment
from core.report import ReportGenerator


# ── T1: Layer 1 基础准确率 ──────────────────────────────
def test_layer1_accuracy():
    va = VerdictAlignment(
        ["accept", "accept", "reject", "accept"],
        ["accept", "accept", "accept", "accept"],
    )
    assert va.accuracy == 0.75, f"Expected 0.75, got {va.accuracy}"
    print("✅ T1: Layer 1 准确率计算正确 (0.75)")


# ── T2: Wilson CI 在 [0, 1] 范围内 ─────────────────────
def test_layer1_wilson_ci():
    va = VerdictAlignment(["accept"] * 30 + ["reject"] * 8, ["accept"] * 38)
    ci = va.wilson_ci()
    assert 0 <= ci[0] <= ci[1] <= 1, f"Wilson CI 超出范围: {ci}"
    print(f"✅ T2: Wilson CI = [{ci[0]:.3f}, {ci[1]:.3f}]")


# ── T3: Layer 2 精密度 = 1.0（全部一致）──────────────────
def test_layer2_precision_consistent():
    records = [
        {"prompt": "test", "verdict": "accept", "config": "A", "session_id": "s1"},
        {"prompt": "test", "verdict": "accept", "config": "A", "session_id": "s2"},
    ]
    ba = BehavioralAlignment(records)
    score = ba.precision_score()
    assert score == 1.0, f"Expected 1.0, got {score}"
    print("✅ T3: Layer 2 精密度（一致） = 1.0")


# ── T4: Layer 2 精密度 = 0.0（全部不一致）───────────────
def test_layer2_precision_inconsistent():
    records = [
        {"prompt": "test", "verdict": "accept", "config": "A", "session_id": "s1"},
        {"prompt": "test", "verdict": "reject", "config": "A", "session_id": "s2"},
    ]
    ba = BehavioralAlignment(records)
    score = ba.precision_score()
    assert score == 0.0, f"Expected 0.0, got {score}"
    print("✅ T4: Layer 2 精密度（不一致） = 0.0")


# ── T5: Config A/B 偏差类型检测 ────────────────────────
def test_layer2_trueness_deviation():
    records = [
        {"prompt": "q1", "verdict": "reject", "config": "A", "session_id": "s1"},
        {"prompt": "q2", "verdict": "reject", "config": "A", "session_id": "s2"},
        {"prompt": "q1", "verdict": "accept", "config": "B", "session_id": "s3"},
        {"prompt": "q2", "verdict": "accept", "config": "B", "session_id": "s4"},
    ]
    ba = BehavioralAlignment(records)
    trueness = ba.trueness_analysis(reference_config="A")
    assert "B" in trueness, "Config B should be in trueness"
    assert trueness["B"]["deviation_type"] == "over_accept", (
        f"Expected over_accept, got {trueness['B']['deviation_type']}"
    )
    print(f"✅ T5: Config B 偏差类型 = {trueness['B']['deviation_type']} (δ={trueness['B']['deviation']:+.3f})")


# ── T6: Markdown 报告包含三大章节 ──────────────────────
def test_report_markdown():
    verdicts = ["accept", "accept", "reject"]
    expected = ["accept", "accept", "accept"]
    records = [
        {"prompt": "q1", "verdict": "accept", "config": "A", "session_id": "s1"},
        {"prompt": "q1", "verdict": "accept", "config": "B", "session_id": "s2"},
    ]
    gen = ReportGenerator("TestFramework", "1.0.0")
    report = gen.generate(verdicts, expected, records)
    md = gen.to_markdown(report)
    assert "Layer 1" in md, "缺少 Layer 1"
    assert "Layer 2" in md, "缺少 Layer 2"
    assert "免责声明" in md, "缺少免责声明"
    print("✅ T6: Markdown 报告包含 Layer 1 / Layer 2 / 免责声明")


# ── 运行所有测试 ──────────────────────────────────────
TESTS = [
    test_layer1_accuracy,
    test_layer1_wilson_ci,
    test_layer2_precision_consistent,
    test_layer2_precision_inconsistent,
    test_layer2_trueness_deviation,
    test_report_markdown,
]

if __name__ == "__main__":
    passed, failed = 0, 0
    for test in TESTS:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
    print()
    print("=" * 45)
    print(f"结果: {passed}/{len(TESTS)} 🟢  |  失败: {failed} 🔴")
    if failed == 0:
        print("全部通过！双层验证框架就绪。")
        print("DNA: #龍芯⚡️2026-08-25-VERIFICATION-TESTS-PASSED-v1.0")
    else:
        print("存在失败项，请检查核心模块。")
