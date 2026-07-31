# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 底座重组引擎单元测试
DNA: #龍芯⚡️2026-07-25-TEST-BASE-REORGANIZER-v1.0
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# 确保项目根目录在路径中
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_base_reorganizer import (
    ChineseBaseRegistry,
    ConceptRelationshipInjector,
    CNSHScenarioGenerator,
    DNATraceChain,
    BaseReorganizer,
    CHINESE_BASE_WHITELIST,
    ENGLISH_BASE_BLACKLIST,
)


class TestChineseBaseDetection(unittest.TestCase):
    """中文底座识别规则测试"""

    def setUp(self):
        self.registry = ChineseBaseRegistry()

    def test_exact_whitelist_match(self):
        self.assertTrue(self.registry.is_chinese_base("qwen2.5:7b"))
        self.assertTrue(self.registry.is_chinese_base("deepseek-r1:7b"))
        self.assertTrue(self.registry.is_chinese_base("yi-1.5:9b"))

    def test_variant_tags_accepted(self):
        self.assertTrue(self.registry.is_chinese_base("qwen2.5:7b-instruct"))
        self.assertTrue(self.registry.is_chinese_base("qwen2.5:7b:latest"))
        self.assertTrue(self.registry.is_chinese_base("yi-1.5-9b-chat"))

    def test_english_blacklist_rejected(self):
        self.assertFalse(self.registry.is_chinese_base("llama3.1:8b"))
        self.assertFalse(self.registry.is_chinese_base("mistral:7b"))
        self.assertFalse(self.registry.is_chinese_base("gemma:2b"))

    def test_deepseek_llama_masquerade_blocked(self):
        """DeepSeek-R1-Distill-Llama 是 Llama 换皮，必须拦截"""
        self.assertFalse(self.registry.is_chinese_base("deepseek-r1-distill-llama-8b"))
        self.assertFalse(self.registry.is_chinese_base("deepseek-r1-distill-llama:70b"))

    def test_deepseek_qwen_allowed(self):
        """DeepSeek-R1-Distill-Qwen 才是真正的中文底座"""
        self.assertTrue(self.registry.is_chinese_base("deepseek-r1:1.5b"))
        # 归一化后应能识别 Distill-Qwen 变体
        self.assertTrue(self.registry.is_chinese_base("deepseek-r1-distill-qwen-7b"))

    def test_gibberish_not_chinese(self):
        self.assertFalse(self.registry.is_chinese_base("qwen2.5-fake-model"))
        self.assertFalse(self.registry.is_chinese_base("some-random-name"))


class TestConceptRelationshipInjector(unittest.TestCase):
    """概念关系注入测试"""

    def test_generate_pairs_count(self):
        injector = ConceptRelationshipInjector()
        pairs = injector.generate_pairs()
        # 至少每个概念都有若干关系
        self.assertGreater(len(pairs), 50)

    def test_training_data_format(self):
        injector = ConceptRelationshipInjector()
        samples = injector.generate_training_data()
        self.assertGreater(len(samples), 0)
        for sample in samples:
            self.assertIn("messages", sample)
            self.assertIn("dna", sample)
            self.assertEqual(sample["messages"][0]["role"], "user")
            self.assertEqual(sample["messages"][1]["role"], "assistant")

    def test_export_roundtrip(self):
        injector = ConceptRelationshipInjector()
        with tempfile.TemporaryDirectory() as tmp:
            out = injector.export_training_jsonl(output_path=Path(tmp) / "test.jsonl")
            lines = out.read_text(encoding="utf-8").strip().split("\n")
            self.assertGreater(len(lines), 0)
            data = json.loads(lines[0])
            self.assertIn("messages", data)


class TestCNSHScenarioGenerator(unittest.TestCase):
    """CNSH场景生成测试"""

    def test_default_count(self):
        gen = CNSHScenarioGenerator()
        scenarios = gen.generate_scenarios(count_per_type=20)
        by_type = {}
        for s in scenarios:
            by_type.setdefault(s.scenario_type, 0)
            by_type[s.scenario_type] += 1
        self.assertEqual(sum(by_type.values()), 100)
        for t in gen.scenarios:
            self.assertEqual(by_type.get(t, 0), 20, f"{t} 场景数量不足")

    def test_partial_count(self):
        gen = CNSHScenarioGenerator()
        scenarios = gen.generate_scenarios(count_per_type=5)
        self.assertEqual(len(scenarios), 25)

    def test_all_scenario_types_present(self):
        gen = CNSHScenarioGenerator()
        scenarios = gen.generate_scenarios(count_per_type=3)
        types = {s.scenario_type for s in scenarios}
        self.assertEqual(types, set(gen.scenarios.keys()))


class TestDNATraceChain(unittest.TestCase):
    """DNA追溯链测试"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.chain_file = Path(self.tmpdir) / "dna_chain.json"

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_chain_integrity(self):
        chain = DNATraceChain(chain_file=self.chain_file)
        from engines.lh_base_reorganizer import ReorganizePhase

        chain.add_record(ReorganizePhase.REGISTER, "qwen2.5:7b")
        chain.add_record(ReorganizePhase.OVERWRITE, "qwen2.5:7b")
        chain.add_record(ReorganizePhase.INJECT, "qwen2.5:7b")
        chain.add_record(ReorganizePhase.VERIFY, "qwen2.5:7b")

        integrity = chain.verify_integrity()
        self.assertTrue(integrity["chain_integrity"])
        self.assertEqual(integrity["total_records"], 4)
        self.assertIn("merkle_root", integrity)
        self.assertTrue(len(integrity["merkle_root"]) > 0)

    def test_broken_link_detection(self):
        chain = DNATraceChain(chain_file=self.chain_file)
        from engines.lh_base_reorganizer import ReorganizePhase

        r1 = chain.add_record(ReorganizePhase.REGISTER, "qwen2.5:7b")
        r2 = chain.add_record(ReorganizePhase.OVERWRITE, "qwen2.5:7b")
        # 手动破坏 parent_dna
        r2.parent_dna = "fake-dna"
        chain._save()

        # 重新加载验证
        chain2 = DNATraceChain(chain_file=self.chain_file)
        integrity = chain2.verify_integrity()
        self.assertFalse(integrity["chain_integrity"])
        self.assertEqual(len(integrity["broken_links"]), 1)


class TestBaseReorganizerDryRun(unittest.TestCase):
    """重组编排器干运行测试"""

    def test_pipeline_dry_run(self):
        reorganizer = BaseReorganizer()
        report = reorganizer.pipeline("qwen2.5:1.5b", dry_run=True)
        self.assertEqual(report.base_model, "qwen2.5:1.5b")
        self.assertTrue(all(report.phases.values()))
        self.assertGreaterEqual(report.total_concept_pairs, 50)
        self.assertGreaterEqual(report.total_cnsh_scenarios, 15)

    def test_collect_training_data_sources(self):
        reorganizer = BaseReorganizer()
        data_info = reorganizer._collect_training_data()
        self.assertIn("total_samples", data_info)
        self.assertIn("sources", data_info)
        self.assertIsInstance(data_info["total_samples"], int)


if __name__ == "__main__":
    unittest.main(verbosity=2)
