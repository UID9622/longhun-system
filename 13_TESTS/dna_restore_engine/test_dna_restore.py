#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 DNA 还原引擎 · 测试套件 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-DNA-RESTORE-TEST-V1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from engines.longhun_dna_restore import (
    DNAStamp,
    DNAStampGenerator,
    DNARestoreEngine,
    MultiAISignatureChain,
    SemanticParser,
)


class TestDNAStamp(unittest.TestCase):
    """DNA签章数据结构测试"""

    def test_create_basic_stamp(self):
        s = DNAStamp("v1.0.0", "UID9622", "初始化项目")
        self.assertEqual(s.version, "v1.0.0")
        self.assertEqual(s.author, "UID9622")
        self.assertEqual(s.semantic_diff, "初始化项目")

    def test_hash_deterministic(self):
        s1 = DNAStamp("v1.0.0", "UID9622", "测试", parent_hash="0" * 16)
        h1 = s1.hash()
        h2 = s1.hash()
        self.assertEqual(h1, h2, "同内容哈希应一致")

    def test_hash_different_on_change(self):
        s1 = DNAStamp("v1.0.0", "UID9622", "测试A", parent_hash="0" * 16)
        s2 = DNAStamp("v1.0.0", "UID9622", "测试B", parent_hash="0" * 16)
        self.assertNotEqual(s1.hash(), s2.hash(), "不同内容哈希应不同")

    def test_to_json_roundtrip(self):
        s1 = DNAStamp(
            "v2.0.0",
            "UID9622",
            "测试序列化",
            structured_diff={"type": "feat", "files": ["a.py"]},
        )
        json_str = s1.to_json()
        s2 = DNAStamp.from_json(json_str)
        self.assertEqual(s1.version, s2.version)
        self.assertEqual(s1.structured_diff, s2.structured_diff)
        self.assertEqual(s1.hash(), s2.hash())

    def test_validate_valid(self):
        s = DNAStamp("v1.0.0", "UID9622", "有效签章")
        result = s.validate()
        self.assertTrue(result["valid"], f"应有效: {result['errors']}")

    def test_validate_missing_version(self):
        s = DNAStamp("", "UID9622", "缺版本号")
        result = s.validate()
        self.assertFalse(result["valid"])
        self.assertTrue(any("version" in e for e in result["errors"]))

    def test_validate_bad_parent_hash(self):
        s = DNAStamp("v1.0.0", "UID9622", "异常父哈希", parent_hash="too_short")
        result = s.validate()
        # parent_hash长度异常应出现在errors中
        has_error = any("parent_hash" in e for e in result.get("errors", []))
        self.assertTrue(has_error, f"应检测到parent_hash异常: {result['errors']}")


class TestDNAStampGenerator(unittest.TestCase):
    """DNA签章生成器测试"""

    def setUp(self):
        self.gen = DNAStampGenerator("UID9622")

    def test_create_first_stamp(self):
        s = self.gen.create_stamp("v1.0.0", "初始化")
        self.assertEqual(s.parent_hash, "0" * 16, "第一个签章父哈希应为全零")
        self.assertEqual(len(self.gen.chain), 1)

    def test_chain_linking(self):
        s1 = self.gen.create_stamp("v1.0.0", "A")
        s2 = self.gen.create_stamp("v1.0.1", "B")
        self.assertEqual(s2.parent_hash, s1.hash(), "子签章parent_hash应等于父签章hash")
        self.assertEqual(len(self.gen.chain), 2)

    def test_chain_json_roundtrip(self):
        self.gen.create_stamp("v1.0.0", "A")
        self.gen.create_stamp("v1.0.1", "B")

        json_data = self.gen.get_chain_json()
        gen2 = DNAStampGenerator("UID9622")
        gen2.load_chain(json_data)
        self.assertEqual(len(gen2.chain), 2)
        self.assertEqual(gen2.chain[0].hash(), self.gen.chain[0].hash())

    def test_export_compressed(self):
        self.gen.create_stamp("v1.0.0", "A", compressed=True)
        compressed = self.gen.export_compressed()
        self.assertLess(len(compressed), 5000)
        gen2 = DNAStampGenerator.import_compressed(compressed)
        self.assertEqual(len(gen2.chain), 1)


class TestDNARestoreEngine(unittest.TestCase):
    """DNA还原引擎测试"""

    def setUp(self):
        self.engine = DNARestoreEngine()
        self.genesis = "# 测试代码库\nprint('Hello World')\n".encode("utf-8")

    def test_set_genesis(self):
        self.engine.set_genesis(self.genesis)
        self.assertEqual(self.engine.genesis_data, self.genesis)

    def test_restore_empty_chain(self):
        self.engine.set_genesis(self.genesis)
        # 空链在restore时会触发verify_chain_integrity → ChainBrokenError
        with self.assertRaises(Exception):
            self.engine.load_chain([])
            self.engine.restore()

    def test_chain_integrity_valid(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.0", "初始化")
        gen.create_stamp("v1.0.1", "添加功能")
        gen.create_stamp("v1.0.2", "修复bug")

        self.engine.set_genesis(self.genesis)
        self.engine.load_chain(gen.get_chain_json())
        result = self.engine.verify_chain_integrity()
        self.assertTrue(result["valid"], f"链应完整: {result.get('message')}")
        self.assertEqual(result["total_rings"], 3)

    def test_chain_integrity_broken(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.0", "初始化")
        gen.create_stamp("v1.0.1", "添加功能")

        self.engine.set_genesis(self.genesis)
        # 直接构造断裂链：修改链数据后再加载
        chain_data = gen.get_chain_json()
        chain_data[1]["parent_hash"] = "0" * 16  # 篡改父哈希

        # load_chain会检测到断裂并抛异常
        with self.assertRaises(Exception) as ctx:
            self.engine.load_chain(chain_data)
        self.assertIn("断裂", str(ctx.exception))

    def test_restore_with_chain(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp(
            "v1.0.1",
            "添加三色审计核心逻辑",
            structured_diff={"type": "feat", "files": ["core/audit.py"]},
        )
        gen.create_stamp(
            "v1.0.2",
            "优化DNA追溯性能",
            structured_diff={"type": "perf", "files": ["core/dna.py"]},
        )

        self.engine.set_genesis(self.genesis)
        self.engine.load_chain(gen.get_chain_json())
        result = self.engine.restore()

        self.assertGreater(len(result), len(self.genesis), "还原后代码应大于创世版本")
        self.assertIn(b"[FEAT]", result, "应包含新增功能标记")
        self.assertIn(b"[PERF]", result, "应包含性能优化标记")

    def test_restore_report(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.1", "修复登录bug")
        self.engine.set_genesis(self.genesis)
        self.engine.load_chain(gen.get_chain_json())
        self.engine.restore()

        report = self.engine.get_restore_report()
        self.assertIn("v1.0.1", report)

    def test_conflict_detection(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.0", "初始化")
        gen.create_stamp(
            "v1.0.1",
            "有冲突的变更",
            conflicts=[{"file": "a.py", "line": 42, "conflict": "两个AI同时修改"}],
        )

        self.engine.set_genesis(self.genesis)
        self.engine.load_chain(gen.get_chain_json())
        conflicts = self.engine.detect_conflicts()
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["version"], "v1.0.1")

    def test_rollback(self):
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.0", "初始化")
        gen.create_stamp("v1.0.1", "添加功能")

        self.engine.set_genesis(self.genesis)
        self.engine.load_chain(gen.get_chain_json())
        self.engine.restore()

        # 回滚到v1.0.0 = 创世版本 + 第一个签章的变更
        rolled = self.engine.rollback_to("v1.0.0")
        self.assertGreaterEqual(len(rolled), len(self.genesis),
                                "回滚后代码应不小于创世版本")


class TestMultiAISignatureChain(unittest.TestCase):
    """多AI签章接龍测试"""

    def setUp(self):
        self.stamp = DNAStamp("v1.0.0", "UID9622", "测试多AI签名")
        self.chain = MultiAISignatureChain()

    def test_add_signatures(self):
        for ai in ["Kimi", "DeepSeek", "Claude"]:
            ok = self.chain.add_signature(self.stamp, ai, f"sig_{ai}")
            self.assertTrue(ok, f"{ai}签名应成功")

        self.assertEqual(len(self.stamp.signatures), 3)

    def test_idempotent(self):
        self.chain.add_signature(self.stamp, "Kimi", "sig_Kimi")
        # 重复相同签名应幂等
        ok = self.chain.add_signature(self.stamp, "Kimi", "sig_Kimi")
        self.assertTrue(ok, "相同签名应幂等返回True")

    def test_conflict_rejection(self):
        self.chain.add_signature(self.stamp, "Kimi", "sig_Kimi")
        # 不同内容应被拒绝
        ok = self.chain.add_signature(self.stamp, "Kimi", "sig_Kimi_v2")
        self.assertFalse(ok, "签名冲突应返回False")

    def test_verify_stamp_signatures(self):
        self.chain.add_signature(self.stamp, "Kimi", "kimi_sig_001")
        self.chain.add_signature(self.stamp, "DeepSeek", "deepseek_sig_002")

        result = self.chain.verify_stamp_signatures(self.stamp)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["valid"], 2)

    def test_contribution_report(self):
        for ai in ["Kimi", "Kimi", "DeepSeek"]:
            self.chain.add_signature(self.stamp, ai, f"sig_{ai}_{len(self.stamp.signatures)}")

        report = self.chain.get_ai_contribution_report()
        self.assertIn("Kimi", report)
        self.assertIn("DeepSeek", report)

    def test_multi_ai_workflow(self):
        result = MultiAISignatureChain.multi_ai_workflow_example()
        self.assertIsNotNone(result["stamp"])
        self.assertEqual(len(result["stamp"].signatures), 3)


class TestSemanticParser(unittest.TestCase):
    """语义摘要解析器测试"""

    def setUp(self):
        self.parser = SemanticParser()

    def test_parse_structured(self):
        result = self.parser.parse(
            "任意文字",
            structured_diff={"type": "feat", "files": ["a.py", "b.py"]},
        )
        self.assertEqual(result["type"], "feat")
        self.assertEqual(result["files"], ["a.py", "b.py"])
        self.assertGreater(result["confidence"], 0.9)
        self.assertEqual(result["source"], "structured")

    def test_rule_based_feat(self):
        result = self.parser.parse("新增用户认证模块")
        self.assertEqual(result["type"], "feat")

    def test_rule_based_fix(self):
        result = self.parser.parse("修复登录页面XSS漏洞")
        self.assertEqual(result["type"], "fix")

    def test_rule_based_refactor(self):
        result = self.parser.parse("重构路由模块，拆分为3个子模块")
        self.assertEqual(result["type"], "refactor")

    def test_rule_based_perf(self):
        result = self.parser.parse("优化数据库查询性能，从O(n²)降为O(log n)")
        self.assertEqual(result["type"], "perf")

    def test_extract_py_files(self):
        result = self.parser.parse("修改 src/router.py 和 core/dna.py 的导入逻辑")
        self.assertIn("src/router.py", result["files"])
        self.assertIn("core/dna.py", result["files"])

    def test_unknown_type(self):
        result = self.parser.parse("做了一些调整")
        self.assertEqual(result["source"], "rule_based")


class TestEndToEnd(unittest.TestCase):
    """端到端集成测试"""

    def test_full_workflow(self):
        # 1. 生成签章链
        gen = DNAStampGenerator("UID9622")
        gen.create_stamp("v1.0.0", "创建核心引擎",
                         structured_diff={"type": "feat", "files": ["core/engine.py"]})
        gen.create_stamp("v1.0.1", "修复内存泄漏",
                         structured_diff={"type": "fix", "files": ["core/memory.py"]})
        gen.create_stamp("v1.1.0", "重构为微服务架构",
                         structured_diff={"type": "refactor", "files": ["services/"]})

        # 2. 验证链完整性
        engine = DNARestoreEngine()
        engine.set_genesis(b"# DragonSoul v1.0\n")
        engine.load_chain(gen.get_chain_json())

        integrity = engine.verify_chain_integrity()
        self.assertTrue(integrity["valid"], f"链应完整: {integrity.get('message')}")

        # 3. 还原
        restored = engine.restore()
        self.assertGreater(len(restored), 20)

        # 4. 多AI签名
        stamp = gen.chain[-1]
        sig_chain = MultiAISignatureChain()
        sig_chain.add_signature(stamp, "Kimi", "kimi_e2e_sig")
        sig_chain.add_signature(stamp, "DeepSeek", "deepseek_e2e_sig")

        verify = sig_chain.verify_stamp_signatures(stamp)
        self.assertEqual(verify["valid"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
