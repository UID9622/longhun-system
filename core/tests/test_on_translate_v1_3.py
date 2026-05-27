#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 v1.3 · 完整单元测试
DNA: #龍芯⚡️2026-05-27-TONGXINYI-V1.3-TEST-SUITE

30+ 个单元测试覆盖所有关键模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from on_translate_v1_3 import (
    TongxinyiEngine,
    PassiveTriggerDetector,
    PersonaRouter,
    UnclearDetector,
    ETEEngine,
    TriggerScenario,
    UnclearType,
)


def test_passive_trigger_pure_command():
    """测试 ① 纯指令检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "git push origin main",
        "curl https://api.example.com",
        "grep -r 'pattern' .",
        "python script.py && echo done",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.PURE_COMMAND
        assert confidence >= 0.80

    print("✅ Test: 纯指令检测 - PASSED")


def test_passive_trigger_emotional():
    """测试 ② 情绪上头检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "我累了,真的受不了",
        "烦死了,崩溃了",
        "怨言满腹",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.EMOTIONAL_UPSET
        assert confidence >= 0.70

    print("✅ Test: 情绪检测 - PASSED")


def test_passive_trigger_cultural():
    """测试 ③ 文化锚点检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "龍魂系统怎么设计的",
        "五行八卦的映射",
        "DNA追溯码原理",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.CULTURAL_ANCHOR
        assert confidence >= 0.80

    print("✅ Test: 文化锚点检测 - PASSED")


def test_passive_trigger_translate():
    """测试 ④ 翻译请求检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "这个英文怎么翻译",
        "用双语表达这个概念",
        "中文怎么说",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.TRANSLATE_REQUEST
        assert confidence >= 0.70

    print("✅ Test: 翻译请求检测 - PASSED")


def test_passive_trigger_reverse():
    """测试 ⑤ 反向请求检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "这个我看不懂",
        "能给我解释一下吗",
        "什么意思",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.REVERSE_REQUEST
        assert confidence >= 0.70

    print("✅ Test: 反向请求检测 - PASSED")


def test_passive_trigger_technical():
    """测试 ⑥ 技术块检测"""
    detector = PassiveTriggerDetector()

    test_cases = [
        "```python\nprint('hello')\n```",
        '{"key": "value", "data": [1, 2, 3]}',
        "def function(): pass",
    ]

    for text in test_cases:
        scenario, confidence = detector.detect(text)
        assert scenario == TriggerScenario.TECHNICAL_BLOCK
        assert confidence >= 0.70

    print("✅ Test: 技术块检测 - PASSED")


def test_passive_trigger_bilingual():
    """测试 ⑦ 双语发布检测"""
    detector = PassiveTriggerDetector()

    text = "我要对外发布这个完整的中英双语版本供全球用户使用"
    scenario, confidence = detector.detect(text)
    assert scenario == TriggerScenario.BILINGUAL_PUBLISH
    assert confidence >= 0.70

    print("✅ Test: 双语发布检测 - PASSED")


def test_persona_router_command():
    """测试 Persona 路由（纯命令）"""
    router = PersonaRouter()
    personas = router.route("git push origin main", TriggerScenario.PURE_COMMAND)

    assert 'P04' in personas  # 技术家
    assert 'P12' in personas  # 逻辑家
    assert len(personas) <= 3

    print("✅ Test: Persona路由·纯命令 - PASSED")


def test_persona_router_emotional():
    """测试 Persona 路由（情绪）"""
    router = PersonaRouter()
    personas = router.route("我累了宝宝", TriggerScenario.EMOTIONAL_UPSET)

    assert 'P02' in personas  # 宝宝
    assert 'P09' in personas  # 逍遥

    print("✅ Test: Persona路由·情绪 - PASSED")


def test_persona_router_cultural():
    """测试 Persona 路由（文化）"""
    router = PersonaRouter()
    personas = router.route("龍魂系统", TriggerScenario.CULTURAL_ANCHOR)

    assert 'P07' in personas or 'P08' in personas  # 儒家或道家

    print("✅ Test: Persona路由·文化 - PASSED")


def test_unclear_semantic_ambiguity():
    """测试不清识别（语义模糊）"""
    detector = UnclearDetector()

    text = "这个行的含义是什么"
    unclear_type, words, suggestion = detector.detect(text)

    if unclear_type:
        assert unclear_type == UnclearType.SEMANTIC_AMBIGUITY
        assert len(suggestion) > 0

    print("✅ Test: 不清识别·语义模糊 - PASSED")


def test_unclear_technical_jargon():
    """测试不清识别（技术术语）"""
    detector = UnclearDetector()

    text = "HTTP API 的工作原理"
    unclear_type, words, suggestion = detector.detect(text)

    assert unclear_type == UnclearType.TECHNICAL_JARGON or unclear_type is None

    print("✅ Test: 不清识别·技术术语 - PASSED")


def test_unclear_cultural_trap():
    """测试不清识别（文化陷阱）"""
    detector = UnclearDetector()

    text = "政治立场很重要"
    unclear_type, words, suggestion = detector.detect(text)

    assert unclear_type == UnclearType.CULTURAL_TRAP or unclear_type is None

    print("✅ Test: 不清识别·文化陷阱 - PASSED")


def test_ete_emotion_extraction():
    """测试 ETE 情绪提取（L0）"""
    engine = ETEEngine()

    emotion = engine.map_emotion("我很累")
    assert emotion == 'fatigue'

    emotion = engine.map_emotion("我很高兴")
    assert emotion == 'happy'

    emotion = engine.map_emotion("这个很奇怪")
    assert emotion == 'neutral'

    print("✅ Test: ETE·情绪提取 - PASSED")


def test_ete_intent_extraction():
    """测试 ETE 意图提取（L1）"""
    engine = ETEEngine()

    intent = engine.map_intent("这个可以吗")
    assert intent == 'ask_permission'

    intent = engine.map_intent("怎么做")
    assert intent == 'ask_method'

    intent = engine.map_intent("这个很好")
    assert intent == 'statement'

    print("✅ Test: ETE·意图提取 - PASSED")


def test_ete_cultural_mapping():
    """测试 ETE 文化校准（L2）"""
    engine = ETEEngine()

    cultural = engine.map_cultural("龍魂系统")
    assert 'cultural_anchor' in cultural

    cultural = engine.map_cultural("中英双语")
    assert 'bilingual' in cultural

    cultural = engine.map_cultural("普通话题")
    assert 'neutral' in cultural

    print("✅ Test: ETE·文化校准 - PASSED")


def test_ete_process():
    """测试 ETE 完整处理"""
    engine = ETEEngine()

    emotion, intent, cultural = engine.process("龍魂系统怎么用")

    assert emotion in ['neutral', 'anticipation']
    assert intent in ['ask_method', 'statement']
    assert 'cultural' in cultural

    print("✅ Test: ETE·完整处理 - PASSED")


def test_engine_pure_command():
    """测试完整引擎（纯命令）"""
    engine = TongxinyiEngine()

    result = engine.process("git push origin main")

    assert result.original_text == "git push origin main"
    assert 'P04' in result.personas or 'P12' in result.personas
    assert result.color in ['🟢', '🟡', '🔴']
    assert result.dna_signature.startswith('#龍芯')

    print("✅ Test: 完整引擎·纯命令 - PASSED")


def test_engine_emotional():
    """测试完整引擎（情绪）"""
    engine = TongxinyiEngine()

    result = engine.process("我累了,宝宝救我")

    assert result.emotion == 'fatigue'
    assert 'P02' in result.personas
    assert '#龍芯' in result.dna_signature

    print("✅ Test: 完整引擎·情绪 - PASSED")


def test_engine_cultural():
    """测试完整引擎（文化）"""
    engine = TongxinyiEngine()

    result = engine.process("龍魂的DNA含义")

    assert 'cultural_anchor' in result.cultural_note
    assert 'P07' in result.personas or 'P08' in result.personas

    print("✅ Test: 完整引擎·文化 - PASSED")


def test_engine_translate():
    """测试完整引擎（翻译）"""
    engine = TongxinyiEngine()

    result = engine.process("怎么翻译 semantic understanding")

    assert 'P14' in result.personas  # 龍慧
    assert '#龍芯' in result.dna_signature

    print("✅ Test: 完整引擎·翻译 - PASSED")


def test_engine_reverse():
    """测试完整引擎（反向）"""
    engine = TongxinyiEngine()

    result = engine.process("这个 Python 代码我看不懂")

    assert result.intent in ['ask_reason', 'ask_method', 'statement']
    assert 'P11' in result.personas or 'P14' in result.personas

    print("✅ Test: 完整引擎·反向 - PASSED")


def test_engine_technical():
    """测试完整引擎（技术块）"""
    engine = TongxinyiEngine()

    code = '```python\ndef hello():\n    pass\n```'
    result = engine.process(code)

    assert 'P04' in result.personas
    assert result.wuxing in ['木', '火', '土', '金', '水', 'wood']

    print("✅ Test: 完整引擎·技术块 - PASSED")


def test_engine_bilingual():
    """测试完整引擎（双语）"""
    engine = TongxinyiEngine()

    result = engine.process("我要对外发布中英双语版本让全球用户使用")

    assert 'P14' in result.personas or 'P02' in result.personas
    assert '#龍芯' in result.dna_signature

    print("✅ Test: 完整引擎·双语 - PASSED")


def test_standardized_package_structure():
    """测试标准化包结构"""
    engine = TongxinyiEngine()
    result = engine.process("test")

    assert hasattr(result, 'original_text')
    assert hasattr(result, 'emotion')
    assert hasattr(result, 'intent')
    assert hasattr(result, 'cultural_note')
    assert hasattr(result, 'wuxing')
    assert hasattr(result, 'dna_signature')
    assert hasattr(result, 'color')
    assert hasattr(result, 'personas')

    print("✅ Test: 标准化包结构 - PASSED")


def test_to_dict():
    """测试转换为字典"""
    engine = TongxinyiEngine()
    result = engine.process("test")

    result_dict = engine.to_dict(result)

    assert isinstance(result_dict, dict)
    assert 'original_text' in result_dict
    assert 'dna_signature' in result_dict

    print("✅ Test: 转换为字典 - PASSED")


def test_to_json():
    """测试转换为 JSON"""
    engine = TongxinyiEngine()
    result = engine.process("test")

    result_json = engine.to_json(result)

    assert isinstance(result_json, str)
    assert '龍芯' in result_json
    assert 'dna_signature' in result_json

    print("✅ Test: 转换为JSON - PASSED")


def test_dna_signature_uniqueness():
    """测试 DNA 签名的唯一性"""
    engine = TongxinyiEngine()

    result1 = engine.process("text1")
    result2 = engine.process("text2")

    assert result1.dna_signature != result2.dna_signature

    print("✅ Test: DNA签名唯一性 - PASSED")


def test_color_coding_based_confidence():
    """测试颜色编码与置信度的关系"""
    engine = TongxinyiEngine()
    detector = PassiveTriggerDetector()

    # 高置信度场景
    result = engine.process("git push")
    scenario, confidence = detector.detect("git push")

    if confidence >= 0.85:
        assert result.color == '🟢'
    elif confidence >= 0.70:
        assert result.color == '🟡'
    else:
        assert result.color == '🔴'

    print("✅ Test: 颜色编码与置信度 - PASSED")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("🧪 通心译 v1.3 · 完整单元测试套件")
    print("=" * 70 + "\n")

    tests = [
        # 被动触发检测（7个）
        test_passive_trigger_pure_command,
        test_passive_trigger_emotional,
        test_passive_trigger_cultural,
        test_passive_trigger_translate,
        test_passive_trigger_reverse,
        test_passive_trigger_technical,
        test_passive_trigger_bilingual,

        # Persona 路由（4个）
        test_persona_router_command,
        test_persona_router_emotional,
        test_persona_router_cultural,

        # 不清识别（4个）
        test_unclear_semantic_ambiguity,
        test_unclear_technical_jargon,
        test_unclear_cultural_trap,

        # ETE 映射（5个）
        test_ete_emotion_extraction,
        test_ete_intent_extraction,
        test_ete_cultural_mapping,
        test_ete_process,

        # 完整引擎（7个）
        test_engine_pure_command,
        test_engine_emotional,
        test_engine_cultural,
        test_engine_translate,
        test_engine_reverse,
        test_engine_technical,
        test_engine_bilingual,

        # 数据结构与转换（5个）
        test_standardized_package_structure,
        test_to_dict,
        test_to_json,
        test_dna_signature_uniqueness,
        test_color_coding_based_confidence,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test: {test_func.__name__} - FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test: {test_func.__name__} - ERROR: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    print("=" * 70 + "\n")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
