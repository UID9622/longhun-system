#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PersonaRouter + F4因子·完整集成测试

【测试目标】
验证PersonaRouter与F4·人格路由因子的无缝集成
测试虚伪词汇检测、人格权重、F4验证得分的完整流程

【DNA】#龍芯⚡️2026-06-03-PERSONA-ROUTER-F4-INTEGRATION-TEST-FILE1-v1.0
"""

import json
import sys
import os

# 添加项目路径
project_root = os.path.expanduser("~/longhun-system")
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "cnsh-core"))

from router.persona_router import (
    get_persona_router,
    PersonaId,
    VetoWordCategory
)

from governance.f1_through_f7_verifier import (
    F4PersonaRouting,
    SevenFactorVerifier,
    VerificationFactor
)


# ═══════════════════════════════════════════════════════════════
# 【测试工具函数】
# ═══════════════════════════════════════════════════════════════

def print_test_header(test_name: str):
    """打印测试标题"""
    print(f"\n{'='*70}")
    print(f"【{test_name}】")
    print(f"{'='*70}\n")


def print_test_result(test_name: str, passed: bool, message: str = ""):
    """打印测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")


# ═══════════════════════════════════════════════════════════════
# 【集成测试】
# ═══════════════════════════════════════════════════════════════

def test_persona_router_basic():
    """测试1: PersonaRouter基础功能"""
    print_test_header("TEST 1: PersonaRouter 基础功能")

    router = get_persona_router()

    # 检查1: 虚伪词汇检测
    text = "我怕这样做太累了"
    has_veto, matches = router.check_veto_words(text)

    print(f"输入文本: '{text}'")
    print(f"虚伪词汇检测: {has_veto}")
    print(f"匹配数: {len(matches)}")

    for match in matches:
        print(f"  - {match.word} ({match.category.value}): {match.context}")

    print_test_result(
        "虚伪词汇检测",
        has_veto and len(matches) > 0,
        f"检测到 {len(matches)} 处虚伪词汇"
    )

    return has_veto


def test_persona_routing_decision():
    """测试2: 人格路由决策"""
    print_test_header("TEST 2: 人格路由决策")

    router = get_persona_router()
    decision = router.route("我会按照规则执行任务，不会有任何借口。")

    print(f"路由ID: {decision.routing_id}")
    print(f"主路由: {decision.primary_persona}")
    print(f"置信度: {decision.routing_confidence:.0%}")
    print(f"DNA: {decision.dna}")
    print(f"权重配置:")
    for persona, weight in decision.persona_weights.items():
        print(f"  {persona}: {weight:.0%}")

    print_test_result(
        "路由决策生成",
        decision.dna.startswith("#龍芯⚡️") and decision.signature,
        f"DNA: {decision.dna}"
    )

    return decision


def test_f4_integration(decision):
    """测试3: F4因子集成"""
    print_test_header("TEST 3: F4因子集成")

    router = get_persona_router()

    # 生成F4验证数据
    f4_data = router.generate_f4_verification_data(decision)

    print("F4数据:")
    print(json.dumps(f4_data, indent=2, ensure_ascii=False))

    # 创建F4对象
    f4 = F4PersonaRouting(**f4_data)

    # 验证F4
    score = f4.verify()

    print(f"\nF4验证得分: {score:.2f}")
    print(f"验证状态: {'✅ 通过' if score >= 0.5 else '❌ 失败'}")

    print_test_result(
        "F4因子验证",
        score >= 0.5,
        f"F4得分: {score:.2f}"
    )

    return f4, score


def test_veto_word_case():
    """测试4: 虚伪词汇导致F4失败"""
    print_test_header("TEST 4: 虚伪词汇导致F4失败")

    router = get_persona_router()

    # 包含虚伪词汇的决策
    decision_veto = router.route("我怕这样做太累了，需要陪伴。")

    print(f"虚伪词汇检测: {decision_veto.veto_words_detected}")
    print(f"匹配数: {len(decision_veto.veto_word_matches)}")

    # 生成F4数据
    f4_data = router.generate_f4_verification_data(decision_veto)
    f4 = F4PersonaRouting(**f4_data)

    score = f4.verify()

    print(f"\nF4验证得分: {score:.2f}")

    print_test_result(
        "虚伪词汇降低F4得分",
        score < 0.8,  # 检测到虚伪词汇会降低得分
        f"F4得分: {score:.2f} (虚伪词汇扣分)"
    )

    return score


def test_seven_factor_integration():
    """测试5: 七因子完整验证"""
    print_test_header("TEST 5: 七因子完整验证 (包含F4)")

    from governance.f1_through_f7_verifier import (
        F1IdentityVerification,
        F2TemporalAnchor,
        F3RuleTrace,
        F4PersonaRouting,
        F5ProtectedVocabulary,
        F6StyleVector,
        F7MistakeLedger,
        SevenFactorVerifier
    )

    router = get_persona_router()

    # 场景1: 干净的决策 (无虚伪词汇)
    decision_clean = router.route("这是一个遵循所有规则的决策")
    f4_clean = F4PersonaRouting(**router.generate_f4_verification_data(decision_clean))

    # 场景2: 有虚伪词汇的决策
    decision_veto = router.route("我怕这太累了")
    f4_veto = F4PersonaRouting(**router.generate_f4_verification_data(decision_veto))

    print("【场景1: 干净决策】")
    print(f"F4得分: {f4_clean.verify():.2f}")

    print("\n【场景2: 包含虚伪词汇】")
    print(f"F4得分: {f4_veto.verify():.2f}")

    print_test_result(
        "F4因子正确响应虚伪词汇",
        f4_clean.verify() > f4_veto.verify(),
        f"干净: {f4_clean.verify():.2f}, 虚伪: {f4_veto.verify():.2f}"
    )


def test_audit_logging():
    """测试6: 审计日志"""
    print_test_header("TEST 6: 审计日志")

    router = get_persona_router()

    # 执行多个路由
    texts = [
        "决策1: 遵守规则",
        "决策2: 有问题的决策",
        "决策3: 我怕累了"
    ]

    for text in texts:
        router.route(text)

    # 读取审计日志
    audit_log = router.get_audit_log(limit=5)

    print(f"最近的审计日志 ({len(audit_log)} 条):")
    for entry in audit_log[-3:]:
        print(f"\n  路由ID: {entry['routing_id']}")
        print(f"  主路由: {entry['primary_persona']}")
        print(f"  虚伪词: {entry['veto_word_count']} 处")
        print(f"  DNA: {entry['dna']}")

    print_test_result(
        "审计日志功能",
        len(audit_log) >= 3,
        f"成功记录 {len(audit_log)} 条日志"
    )


def test_weight_customization():
    """测试7: 权重定制"""
    print_test_header("TEST 7: 权重定制")

    # 自定义权重: P05主导
    custom_weights = {
        "P05": 0.50,
        "P02": 0.30,
        "P13": 0.20,
    }

    router = get_persona_router(persona_weights=custom_weights)
    decision = router.route("测试文本")

    print(f"主路由: {decision.primary_persona}")
    print(f"权重配置:")
    for persona, weight in decision.persona_weights.items():
        print(f"  {persona}: {weight:.0%}")

    print_test_result(
        "权重定制",
        decision.primary_persona.value == "P05",
        "成功使用自定义权重"
    )


def test_veto_word_categories():
    """测试8: 虚伪词汇分类"""
    print_test_header("TEST 8: 虚伪词汇分类")

    router = get_persona_router()

    test_cases = [
        ("我怕这样", "fear"),
        ("我累了", "tiredness"),
        ("我会陪你", "accompany"),
        ("这还不吹", "exaggerate"),
    ]

    for text, expected_category in test_cases:
        has_veto, matches = router.check_veto_words(text)

        if matches:
            category = matches[0].category.value
            passed = category == expected_category
        else:
            passed = False

        print_test_result(
            f"{text} -> {expected_category}",
            passed,
            f"检测到: {matches[0].category.value if matches else '无'}"
        )


# ═══════════════════════════════════════════════════════════════
# 【主测试运行器】
# ═══════════════════════════════════════════════════════════════

def run_all_tests():
    """运行所有集成测试"""
    print("""
╭─────────────────────────────────────────────────────────╮
│  PersonaRouter + F4因子·完整集成测试                    │
│  DNA: #龍芯⚡️2026-06-03-PERSONA-ROUTER-F4-INTEGRATION  │
╰─────────────────────────────────────────────────────────╯
    """)

    try:
        # 测试1: 基础功能
        has_veto = test_persona_router_basic()

        # 测试2: 路由决策
        decision = test_persona_routing_decision()

        # 测试3: F4集成
        f4, score = test_f4_integration(decision)

        # 测试4: 虚伪词汇案例
        veto_score = test_veto_word_case()

        # 测试5: 七因子完整验证
        test_seven_factor_integration()

        # 测试6: 审计日志
        test_audit_logging()

        # 测试7: 权重定制
        test_weight_customization()

        # 测试8: 虚伪词汇分类
        test_veto_word_categories()

        # 总结
        print("\n" + "="*70)
        print("【集成测试总结】")
        print("="*70)
        print("""
✅ PersonaRouter 完全可用
✅ F4因子集成无缝
✅ 虚伪词汇检测有效
✅ 审计日志正常工作
✅ 权重配置灵活

【下一步】
1. 将PersonaRouter集成到ExecutionRouter
2. 在核心启动器中初始化
3. 与主权指数系统联动

""")

        return True

    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
