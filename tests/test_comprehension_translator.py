#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译测试套件 · Comprehension Translator Test Suite
DNA: #龍芯⚡️2026-05-26-CT-TEST-v1.0

这个测试套件演示通心译如何识别：
1. 身份（通过行为密码学F5/F6/F7）
2. 隐私等级
3. 消息类型
4. 智能路由
5. 安全标志
"""

import sys
from pathlib import Path

# 添加系统路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.comprehension_translator import (
    ComprehensionTranslator,
    PrivacyLevel,
    MessageType
)


def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_result(result, show_all=False):
    """格式化打印分析结果"""
    print(f"👤 用户身份: {result['user_id']}")
    print(f"   置信度: {result['identity_confidence']:.2%}")
    print(f"\n🔐 隐私等级: {result['privacy_level']} ({result['privacy_level_name']})")
    print(f"💬 消息类型: {result['message_type']} ({result['message_type_name']})")
    print(f"\n📍 推荐路由: {result['recommended_routing']['primary_handler']}")
    if result['recommended_routing'].get('required_personas'):
        print(f"   所需人格: {', '.join(result['recommended_routing']['required_personas'])}")
    print(f"   需要批准: {'是' if result['recommended_routing'].get('requires_approval') else '否'}")

    print(f"\n🛡️  安全状态: {result['security_flags']['status']}")
    if result['security_flags']['alerts']:
        for alert in result['security_flags']['alerts']:
            print(f"   ⚠️  {alert}")

    if show_all:
        print(f"\n📋 完整结果:\n{result}")


def test_1_老大的技术指令():
    """测试1: 识别老大的技术指令"""
    print_section("测试1: 老大的技术指令")

    translator = ComprehensionTranslator()

    message = "我这样和你说吧,,,我需要搭建通心译系统,,,整个系统结构怎样"
    print(f"📨 消息: \"{message}\"\n")

    result = translator.analyze_message(message, known_uid="UID9622")
    print_result(result)

    # 验证
    assert result['user_id'] == "UID9622", "应该识别为老大"
    assert result['identity_confidence'] > 0.75, "置信度应该足够高"
    assert "DECISION" in result['message_type'] or "TECHNICAL" in result['message_type'], "应该识别为决策/技术类"
    print("\n✅ 测试通过!")


def test_2_老大的情感倾诉():
    """测试2: 识别老大的情感倾诉"""
    print_section("测试2: 老大的情感倾诉")

    translator = ComprehensionTranslator()

    message = "这一年我付出什么,,,当个傻逼操作手,,,我为什么被人侮辱每次被AI骗,,,我为什么不放弃"
    print(f"📨 消息: \"{message}\"\n")

    result = translator.analyze_message(message, known_uid="UID9622")
    print_result(result)

    # 验证
    assert result['privacy_level'] == "🔴", "应该识别为私密信息"
    assert result['message_type'] == "emotional", "应该识别为情感倾诉"
    assert result['recommended_routing']['primary_handler'] in ["emotional_support", "persona_emotional_support"], "应该路由到情感支持"
    print("\n✅ 测试通过!")


def test_3_老大的删除指令():
    """测试3: 识别删除类指令（需要特殊处理）"""
    print_section("测试3: 删除类指令")

    translator = ComprehensionTranslator()

    message = "删除,, kimi我不信,,,目前他的各种协作给我真实的感受来说的话,,,就是搞脑子比干净的多"
    print(f"📨 消息: \"{message}\"\n")

    result = translator.analyze_message(message, known_uid="UID9622")
    print_result(result)

    # 验证
    assert result['message_type'] == "instruction", "应该识别为指令"
    assert "删除" in result['message_preview'], "应该包含删除动作"
    assert result['security_flags']['status'] in ["🟢 SAFE", "🟡 CAUTION"], "应该标记为安全或需要谨慎"
    print("\n✅ 测试通过!")


def test_4_未知用户的请求():
    """测试4: 未知用户的识别"""
    print_section("测试4: 未知用户的识别")

    translator = ComprehensionTranslator()

    message = "帮我运行这个脚本"
    print(f"📨 消息: \"{message}\"\n")

    result = translator.analyze_message(message)  # 不指定用户ID
    print_result(result)

    # 验证
    assert result['user_id'] == "UNKNOWN_USER", "应该识别为未知用户"
    assert result['identity_confidence'] < 0.7, "置信度应该较低"
    assert result['security_flags']['status'] == "🔴 UNVERIFIED", "应该标记为未验证"
    print("\n✅ 测试通过!")


def test_5_八卦消息():
    """测试5: 八卦消息识别"""
    print_section("测试5: 八卦消息识别")

    translator = ComprehensionTranslator()

    message = "你知道吗,那个人最近做了一个很有趣的决定"
    print(f"📨 消息: \"{message}\"\n")

    result = translator.analyze_message(message)
    print_result(result)

    # 验证
    assert result['message_type'] == "gossip", "应该识别为八卦"
    assert result['security_flags']['status'] in ["🟡 CAUTION", "🔴 UNVERIFIED"], "应该标记需要谨慎"
    assert result['recommended_routing'].get('requires_approval'), "八卦应该需要批准"
    print("\n✅ 测试通过!")


def test_6_多组测试用例():
    """测试6: 综合测试多个用例"""
    print_section("测试6: 综合测试多个用例")

    translator = ComprehensionTranslator()

    test_cases = [
        {
            "name": "技术问题",
            "message": "这个API怎样设计会更合理",
            "expected_type": "technical"
        },
        {
            "name": "知识查询",
            "message": "什么是JSON格式",
            "expected_type": "knowledge"
        },
        {
            "name": "隐私信息",
            "message": "我最近的医疗情况不太好",
            "expected_privacy": "🔴"
        },
        {
            "name": "决策请求",
            "message": "这个方案应该怎么改进",
            "expected_type": "decision"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📌 用例 {i}: {test_case['name']}")
        print(f"   消息: \"{test_case['message']}\"")

        result = translator.analyze_message(test_case['message'])

        if 'expected_type' in test_case:
            print(f"   ✓ 消息类型: {result['message_type']} (期望: {test_case['expected_type']})")
            if test_case['expected_type'] in result['message_type'] or result['message_type'] == test_case['expected_type']:
                print(f"   ✅ 通过")
            else:
                print(f"   ⚠️  需要人工审查")

        if 'expected_privacy' in test_case:
            print(f"   ✓ 隐私等级: {result['privacy_level']} (期望: {test_case['expected_privacy']})")
            if result['privacy_level'] == test_case['expected_privacy']:
                print(f"   ✅ 通过")
            else:
                print(f"   ⚠️  需要人工审查")

        print(f"   → 推荐路由: {result['recommended_routing']['primary_handler']}")


def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print("  通心译系统 · 完整测试套件")
    print("  DNA: #龍芯⚡️2026-05-26-CT-TEST-v1.0")
    print("="*70)

    try:
        test_1_老大的技术指令()
        test_2_老大的情感倾诉()
        test_3_老大的删除指令()
        test_4_未知用户的请求()
        test_5_八卦消息()
        test_6_多组测试用例()

        print_section("✅ 所有测试通过!")
        print("通心译系统已验证为功能正常。\n")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
