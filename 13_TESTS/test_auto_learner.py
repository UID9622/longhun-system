#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 自动学习引擎 单元测试
DNA: #龍芯⚡️丙午·乙未·庚子·壬午·䷙大畜-AUTO-LEARNER-TESTS-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
"""

import json, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bin.lh_auto_learner import AutoLearner, FilterResult, Priority, LearningItem
from bin.lh_gap_detector import GapDetector, GapItem
from engines.lh_innovation_engine import InnovationEngine, InnovationReport, AuditMark, PersonaOpinion


class TestAutoLearner(unittest.TestCase):
    """自动学习引擎测试"""

    def setUp(self):
        self.learner = AutoLearner()

    def test_crawl_produces_items(self):
        items = self.learner.crawl_demo()
        self.assertEqual(len(items), 5, f"Expected 5 demo items, got {len(items)}")
        for item in items:
            self.assertTrue(item.item_id, "item_id empty")
            self.assertTrue(item.dna, "DNA empty")

    def test_filter_all_pass(self):
        items = self.learner.crawl_demo()
        filtered, stats = self.learner.filter_items(items)
        self.assertEqual(stats["PASS"] + stats["FAIL"] + stats["SUSPICIOUS"], 5)

    def test_filter_value_conflict(self):
        """价值观冲突的内容应被标记SUSPICIOUS"""
        from bin.lh_auto_learner import LearningItem
        bad_item = LearningItem(
            item_id="bad-1", source="github", source_url="http://bad.com",
            title="用户行为追踪SDK", content="悄悄收集用户数据，绕过隐私",
            language="zh", raw_meta={"stars": 5000}, dna="test"
        )
        filtered, stats = self.learner.filter_items([bad_item])
        self.assertEqual(stats["SUSPICIOUS"], 1)
        self.assertEqual(filtered[0].filter_result, FilterResult.SUSPICIOUS)

    def test_filter_low_quality_github(self):
        """低质量GitHub应被过滤"""
        from bin.lh_auto_learner import LearningItem
        low_item = LearningItem(
            item_id="low-1", source="github", source_url="http://low.com",
            title="small project", content="nothing",
            language="en", raw_meta={"stars": 5}, dna="test"
        )
        filtered, stats = self.learner.filter_items([low_item])
        self.assertEqual(stats["FAIL"], 1)

    def test_cnsh_align_produces_mappings(self):
        self.learner.crawl_demo()
        self.learner.filter_items()
        mappings = self.learner.align_cnsh()
        self.assertGreater(len(mappings), 0, "Should produce at least 1 mapping")
        for m in mappings:
            self.assertTrue(m.cnsh_syntax, "CNSH syntax empty")
            self.assertTrue(m.dna, "DNA empty")

    def test_scenario_sim_produces_reports(self):
        self.learner.crawl_demo()
        self.learner.filter_items()
        self.learner.align_cnsh()
        reports = self.learner.simulate_scenarios()
        self.assertGreater(len(reports), 0)
        for r in reports:
            self.assertTrue(r.innovation_points, "No innovation points")
            self.assertGreater(r.estimated_hours, 0, "Estimated hours zero")

    def test_recommendations_sorted(self):
        self.learner.crawl_demo()
        self.learner.filter_items()
        self.learner.align_cnsh()
        self.learner.simulate_scenarios()
        recs = self.learner.recommend()
        self.assertGreater(len(recs), 0)
        scores = [r["fit_score"] for r in recs]
        self.assertEqual(scores, sorted(scores, reverse=True), "Not sorted descending")

    def test_full_pipeline_completes(self):
        result = self.learner.pipeline()
        self.assertEqual(result["status"], "complete")
        self.assertIn("recommendations", result)

    def test_breakfast_report_contains_keywords(self):
        report = self.learner.breakfast_report()
        self.assertIn("早餐报告", report)
        self.assertIn("学习流水", report)
        self.assertGreater(len(report), 200)

    def test_pipeline_returns_valid_structure(self):
        result = self.learner.pipeline()
        stages = result["stages"]
        for stage in ["crawl", "filter", "cnsh_align", "scenario_sim", "recommend"]:
            self.assertIn(stage, stages, f"Missing stage: {stage}")


class TestGapDetector(unittest.TestCase):
    """空缺检测器测试"""

    def setUp(self):
        self.detector = GapDetector()

    def test_scan_produces_gaps(self):
        gaps = self.detector.scan()
        self.assertGreater(len(gaps), 0)
        for g in gaps:
            self.assertIsInstance(g, GapItem)

    def test_fit_scores_in_range(self):
        gaps = self.detector.scan()
        for g in gaps:
            self.assertGreaterEqual(g.fit_score, 0.0)
            self.assertLessEqual(g.fit_score, 1.0)

    def test_priority_assigned(self):
        gaps = self.detector.scan()
        valid = {"P0-立即补全", "P1-近期规划", "P2-观察储备", "P3-暂不处理"}
        for g in gaps:
            self.assertIn(g.priority, valid)

    def test_gaps_sorted_by_fit_score(self):
        gaps = self.detector.scan()
        scores = [g.fit_score for g in gaps]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_our_features_excluded_from_gaps(self):
        gaps = self.detector.scan()
        gap_ids = {g.gap_id for g in gaps}
        for feat in self.detector.our_features:
            self.assertNotIn(feat, gap_ids, f"Own feature '{feat}' found in gaps!")

    def test_chinese_features_score_higher(self):
        """中文功能应在评分上获得额外加分（基线0.5 + 中文加分0.15 = 0.65起）"""
        gaps = self.detector.scan()
        zh_gaps = [g for g in gaps if any(ord(c) > 0x4e00 for c in g.feature_name + g.description)]
        if zh_gaps:
            for g in zh_gaps:
                # 中文内容至少要有基线加分
                self.assertGreaterEqual(g.fit_score, 0.65,
                    f"Chinese feature '{g.feature_name}' should score >= 0.65, got {g.fit_score}")

    def test_format_report(self):
        gaps = self.detector.scan()
        report = self.detector.format_report(gaps)
        self.assertIn("空缺报告", report)
        self.assertGreater(len(report), 200)

    def test_user_tracking_rejected(self):
        """用户追踪SDK应为低优先级（非P0/P1）"""
        gaps = self.detector.scan()
        tracking = [g for g in gaps if "tracking" in g.gap_id or "追踪" in g.feature_name]
        if tracking:
            self.assertNotIn(tracking[0].priority, ["P0-立即补全", "P1-近期规划"],
                f"User tracking should not be P0/P1, got {tracking[0].priority}")


class TestInnovationEngine(unittest.TestCase):
    """创新推演引擎测试"""

    def setUp(self):
        self.engine = InnovationEngine()

    def test_analyze_single_topic(self):
        report = self.engine.analyze("多Agent协作框架", "GitHub")
        self.assertIsInstance(report, InnovationReport)
        self.assertEqual(len(report.personas_opinions), 11)

    def test_opinions_complete(self):
        report = self.engine.analyze("多Agent协作框架", "GitHub")
        for op in report.personas_opinions:
            self.assertTrue(op.persona)
            self.assertTrue(op.role)
            self.assertTrue(op.opinion)
            self.assertTrue(op.recommendation)
            self.assertIn(op.audit, [AuditMark.GREEN, AuditMark.YELLOW, AuditMark.RED])

    def test_red_audit_marks_non_actionable(self):
        """触发红色审计的主题应为不可落地"""
        report = self.engine.analyze("底座模型升级", "HuggingFace")
        if report.overall_audit == AuditMark.RED:
            self.assertFalse(report.actionability)

    def test_cross_innovation_content(self):
        report = self.engine.analyze("多Agent协作", "GitHub")
        self.assertGreater(len(report.cross_innovation), 20)

    def test_longhun_version_generated(self):
        report = self.engine.analyze("多Agent协作", "GitHub")
        self.assertGreater(len(report.longhun_version), 30)

    def test_batch_analyze(self):
        topics = [
            {"topic": "多Agent协作框架", "source": "GitHub"},
            {"topic": "AI工作流编排", "source": "CSDN"},
        ]
        reports = self.engine.batch_analyze(topics)
        self.assertEqual(len(reports), 2)

    def test_summary_report(self):
        topics = [
            {"topic": "多Agent协作框架", "source": "GitHub"},
            {"topic": "AI工作流编排", "source": "CSDN"},
        ]
        reports = self.engine.batch_analyze(topics)
        summary = self.engine.summary_report(reports)
        self.assertIn("推演汇总", summary)
        self.assertGreater(len(summary), 200)

    def test_risk_score_range(self):
        report = self.engine.analyze("多Agent协作框架", "GitHub")
        self.assertGreaterEqual(report.risk_score, 0.0)
        self.assertLessEqual(report.risk_score, 1.0)

    def test_unknown_topic_gets_generic_opinions(self):
        """未知主题应得到通用推演意见"""
        report = self.engine.analyze("一个完全随机的技术主题", "测试")
        self.assertEqual(len(report.personas_opinions), 11)
        # 应该有黄色的默认标记
        yellows = sum(1 for o in report.personas_opinions if o.audit == AuditMark.YELLOW)
        self.assertGreater(yellows, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
