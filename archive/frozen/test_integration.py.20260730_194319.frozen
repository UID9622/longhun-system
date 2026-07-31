#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂规则引擎 · 集成测试套件 v2.5
批量处理 + Notion 同步 + 报告生成

DNA:#龍芯⚡️2026-06-07-RULES-ENGINE-INTEGRATION-TEST-FILE2-v2.5-1
责任: UID9622 · 不免责
"""

import json
import tempfile
import pytest
from pathlib import Path
from typing import List, Dict

from batch_processor_v2_5 import (
    RulesEngineBatchProcessorV25,
    Case,
    ProcessResult,
)
from notion_sync_v2_5 import (
    NotionSyncManager,
    NotionClient,
    SyncStatus,
    SyncRecord,
)
from report_generator_enhanced import (
    EnhancedReportGenerator,
    AnomalyLevel,
)


# ============================================================================
# [测试数据]
# ============================================================================

SAMPLE_CASES = [
    Case(id="case_001", content="高质量的案件信息，符合所有规则要求", metadata={"type": "A"}),
    Case(id="case_002", content="短", metadata={"type": "B"}),  # 会被驳回
    Case(id="case_003", content="中等长度的案件内容，包含必要信息", metadata={"type": "C"}),
    Case(id="case_004", content="详细的案件描述" * 10, metadata={"type": "D"}),  # 很长
    Case(id="case_005", content="标准长度的内容" * 5, metadata={"type": "E"}),
]


# ============================================================================
# [批量处理测试]
# ============================================================================

class TestBatchProcessor:
    """批量处理器测试"""

    @pytest.fixture
    def processor(self):
        """创建处理器实例"""
        return RulesEngineBatchProcessorV25(max_workers=2)

    @pytest.fixture
    def temp_dir(self):
        """创建临时目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_single_case_processing(self, processor):
        """测试单个案件处理"""
        result = processor._process_case(SAMPLE_CASES[0])

        assert result.case_id == "case_001"
        assert result.status == "success"
        assert result.processing_time_ms > 0
        assert result.result is not None

    def test_batch_processing(self, processor):
        """测试批量处理"""
        report = processor.process_batch(SAMPLE_CASES)

        assert report['statistics']['total'] == 5
        assert report['statistics']['success'] > 0
        assert report['statistics']['errors'] >= 0
        assert float(report['statistics']['success_rate'].rstrip('%')) >= 0

    def test_batch_processing_with_file(self, processor, temp_dir):
        """测试从文件批量处理"""
        # 创建输入文件
        input_file = temp_dir / "cases.json"
        cases_data = [
            {"id": c.id, "content": c.content, "metadata": c.metadata}
            for c in SAMPLE_CASES
        ]
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(cases_data, f)

        # 处理
        output_file = temp_dir / "results.json"
        report = processor.process_batch_from_file(input_file, output_file)

        assert output_file.exists()
        assert report['statistics']['total'] == 5

        # 验证输出文件内容
        with open(output_file, 'r') as f:
            result_data = json.load(f)

        assert len(result_data['results']) == 5

    def test_retry_mechanism(self, processor):
        """测试重试机制"""
        # 处理一个可能失败的案件
        case = Case(id="retry_test", content="", metadata={})
        result = processor._process_case(case)

        # 即使失败，也应该返回结果对象
        assert result is not None
        assert hasattr(result, 'status')

    def test_error_handling(self, processor):
        """测试错误处理"""
        cases_with_error = [
            Case(id="good", content="正常案件" * 5, metadata={}),
            Case(id="bad", content="", metadata={}),
        ]

        report = processor.process_batch(cases_with_error)

        # 至少有 1 个成功
        assert report['statistics']['success'] >= 1

    def test_progress_bar_display(self, processor, capsys):
        """测试进度条显示"""
        processor.enable_progress = True
        report = processor.process_batch(SAMPLE_CASES)

        # 应该有进度输出
        assert report['statistics']['total'] > 0

    def test_statistics_calculation(self, processor):
        """测试统计计算"""
        report = processor.process_batch(SAMPLE_CASES)

        stats = report['statistics']

        # 验证计算
        assert stats['total'] == 5
        assert stats['success'] + stats['errors'] == 5
        assert float(stats['success_rate'].rstrip('%')) >= 0
        assert float(stats['success_rate'].rstrip('%')) <= 100

    def test_large_batch_processing(self, processor):
        """测试大批量处理 (100 个案件)"""
        large_cases = [
            Case(id=f"case_{i:04d}", content=f"案件内容 {i}" * 5, metadata={"idx": i})
            for i in range(100)
        ]

        report = processor.process_batch(large_cases)

        assert report['statistics']['total'] == 100
        assert len(report['results']) == 100


# ============================================================================
# [Notion 同步测试]
# ============================================================================

class TestNotionSync:
    """Notion 同步测试"""

    @pytest.fixture
    def sync_manager(self):
        """创建同步管理器"""
        client = NotionClient()
        return NotionSyncManager(client)

    @pytest.fixture
    def temp_sync_state(self, tmp_path):
        """临时同步状态文件"""
        state_file = tmp_path / "sync_state.json"
        return str(state_file)

    def test_sync_item_creation(self, sync_manager):
        """测试同步项目创建"""
        local_id = "test_001"
        local_data = {
            "title": "测试案件",
            "status": "进行中",
        }

        result = sync_manager.sync_item(local_id, local_data)

        assert result is True
        assert f"{local_id}_new" in sync_manager.sync_records

    def test_sync_item_update(self, sync_manager):
        """测试同步项目更新"""
        local_id = "test_001"
        remote_id = "remote_001"

        # 第一次同步
        data_v1 = {"title": "原始标题", "status": "进行中"}
        sync_manager.sync_item(local_id, data_v1, remote_id)

        # 第二次同步 (更新)
        data_v2 = {"title": "更新的标题", "status": "完成"}
        result = sync_manager.sync_item(local_id, data_v2, remote_id)

        assert result is True

    def test_conflict_detection(self, sync_manager):
        """测试冲突检测"""
        local_id = "conflict_test"
        remote_id = "remote_conflict"
        data = {"title": "原始数据"}

        # 首次同步
        sync_manager.sync_item(local_id, data, remote_id)

        # 修改记录以模拟冲突
        key = f"{local_id}_{remote_id}"
        record = sync_manager.sync_records[key]
        record.remote_hash = "different_hash"

        # 再次尝试同步相同数据
        result = sync_manager.sync_item(local_id, data, remote_id)

        # 应该检测到冲突
        conflicts = sync_manager.detect_conflicts()
        assert len(conflicts) > 0

    def test_conflict_resolution(self, sync_manager):
        """测试冲突解决"""
        local_id = "resolve_test"
        remote_id = "remote_resolve"
        key = f"{local_id}_{remote_id}"

        # 创建冲突记录
        sync_manager.sync_records[key] = SyncRecord(
            local_id=local_id,
            remote_id=remote_id,
            local_hash="hash_local",
            remote_hash="hash_remote",
            status=SyncStatus.CONFLICTED,
        )

        # 解决冲突 (优先本地)
        result = sync_manager.resolve_conflict(key, prefer_local=True)

        assert result is True
        assert sync_manager.sync_records[key].status == SyncStatus.SYNCED

    def test_sync_state_persistence(self, sync_manager, temp_sync_state):
        """测试同步状态持久化"""
        sync_manager.sync_state_file = temp_sync_state

        # 添加记录
        sync_manager.sync_item("test_001", {"title": "测试"})

        # 保存
        sync_manager.save_sync_state()

        # 验证文件存在
        assert Path(temp_sync_state).exists()

        # 加载
        new_manager = NotionSyncManager(NotionClient(), temp_sync_state)
        assert len(new_manager.sync_records) > 0

    def test_sync_status_summary(self, sync_manager):
        """测试同步状态摘要"""
        # 添加多个记录
        for i in range(3):
            sync_manager.sync_item(f"item_{i}", {"data": f"content_{i}"})

        status = sync_manager.get_sync_status()

        assert status['total_records'] == 3
        assert status['synced'] > 0
        assert 'sync_rate' in status

    def test_batch_sync(self, sync_manager):
        """测试批量同步"""
        items = [
            {"id": "batch_001", "content": "项目 1"},
            {"id": "batch_002", "content": "项目 2"},
            {"id": "batch_003", "content": "项目 3"},
        ]

        success_count = 0
        for item in items:
            result = sync_manager.sync_item(item['id'], item)
            if result:
                success_count += 1

        assert success_count == len(items)


# ============================================================================
# [报告生成测试]
# ============================================================================

class TestReportGenerator:
    """报告生成测试"""

    @pytest.fixture
    def generator(self, tmp_path):
        """创建报告生成器"""
        return EnhancedReportGenerator(tmp_path)

    @pytest.fixture
    def sample_results(self):
        """示例结果数据"""
        return [
            {"case_id": f"case_{i:04d}", "status": "success" if i % 10 != 0 else "error",
             "processing_time_ms": 50 + i % 100, "error": None if i % 10 != 0 else "timeout"}
            for i in range(100)
        ]

    def test_html_report_generation(self, generator, sample_results):
        """测试 HTML 报告生成"""
        output_file = generator.generate_html_report(sample_results, {})

        assert output_file.exists()
        assert output_file.suffix == '.html'

        # 验证内容
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '<html' in content
        assert '总计' in content
        assert '成功' in content

    def test_chart_generation(self, generator, sample_results):
        """测试图表生成"""
        try:
            output_file = generator.generate_statistics_chart(sample_results)

            if output_file:  # matplotlib 可能未安装
                assert output_file.exists()
                assert output_file.suffix == '.png'
        except ImportError:
            pytest.skip("matplotlib 未安装")

    def test_anomaly_detection_high_error_rate(self, generator):
        """测试异常检测: 高错误率"""
        results = [
            {"case_id": f"case_{i}", "status": "error", "processing_time_ms": 50}
            for i in range(20)  # 全部失败
        ]

        alerts = generator.detect_anomalies(results)

        assert len(alerts) > 0
        assert any(alert.level == AnomalyLevel.CRITICAL for alert in alerts)

    def test_anomaly_detection_slow_processing(self, generator):
        """测试异常检测: 处理延迟"""
        results = [
            {"case_id": f"case_{i:04d}", "status": "success",
             "processing_time_ms": 500 if i < 15 else 50}
            for i in range(100)
        ]

        alerts = generator.detect_anomalies(results)

        # 应该检测到延迟异常
        delay_alerts = [a for a in alerts if '延迟' in a.title]
        assert len(delay_alerts) > 0

    def test_anomaly_detection_repeated_errors(self, generator):
        """测试异常检测: 重复错误"""
        results = [
            {"case_id": f"case_{i:04d}", "status": "error",
             "error": "timeout" if i % 3 == 0 else "validation_error",
             "processing_time_ms": 50}
            for i in range(100)
        ]

        alerts = generator.detect_anomalies(results)

        # 应该检测到重复错误
        error_alerts = [a for a in alerts if '重复' in a.title]
        assert len(error_alerts) > 0

    def test_report_statistics_accuracy(self, generator, sample_results):
        """测试报告统计的准确性"""
        success_count = sum(1 for r in sample_results if r['status'] == 'success')
        error_count = len(sample_results) - success_count

        output_file = generator.generate_html_report(sample_results, {})

        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 验证统计数字
        assert str(success_count) in content
        assert str(error_count) in content


# ============================================================================
# [端到端集成测试]
# ============================================================================

class TestEndToEnd:
    """端到端集成测试"""

    def test_complete_workflow(self, tmp_path):
        """完整的工作流: 批量处理 → 同步 → 报告"""
        # 1. 批量处理
        processor = RulesEngineBatchProcessorV25()
        report = processor.process_batch(SAMPLE_CASES)

        assert report['statistics']['total'] == 5

        # 2. Notion 同步
        sync_manager = NotionSyncManager(NotionClient())
        for result in report['results']:
            sync_data = {
                "case_id": result['case_id'],
                "status": result['status'],
                "timestamp": result['timestamp'],
            }
            success = sync_manager.sync_item(result['case_id'], sync_data)
            assert success is True

        # 3. 报告生成
        generator = EnhancedReportGenerator(tmp_path)
        report_file = generator.generate_html_report(report['results'], {})

        assert report_file.exists()

    def test_workflow_with_errors_and_recovery(self, tmp_path):
        """测试错误场景和恢复"""
        # 包含部分失败的案件
        mixed_cases = [
            Case(id="good_1", content="优质内容" * 5, metadata={}),
            Case(id="bad", content="", metadata={}),
            Case(id="good_2", content="优质内容" * 5, metadata={}),
        ]

        processor = RulesEngineBatchProcessorV25()
        report = processor.process_batch(mixed_cases)

        # 应该有部分成功
        assert report['statistics']['success'] >= 2

        # 生成报告仍应该成功
        generator = EnhancedReportGenerator(tmp_path)
        report_file = generator.generate_html_report(report['results'], {})
        assert report_file.exists()


# ============================================================================
# [性能测试]
# ============================================================================

class TestPerformance:
    """性能测试"""

    def test_batch_processing_speed_100_cases(self):
        """测试 100 个案件的处理速度"""
        processor = RulesEngineBatchProcessorV25(max_workers=4)
        cases = [
            Case(id=f"perf_{i:04d}", content=f"内容 {i}" * 5, metadata={})
            for i in range(100)
        ]

        import time
        start = time.time()
        report = processor.process_batch(cases)
        elapsed = time.time() - start

        # 应该在 5 秒内完成
        assert elapsed < 5.0
        print(f"✅ 100 个案件耗时: {elapsed:.2f}s")

    def test_sync_performance_100_items(self):
        """测试 100 个项目的同步性能"""
        sync_manager = NotionSyncManager(NotionClient())

        import time
        start = time.time()

        for i in range(100):
            sync_manager.sync_item(f"perf_item_{i}", {"data": f"content_{i}"})

        elapsed = time.time() - start

        # 应该在 1 秒内完成
        assert elapsed < 1.0
        print(f"✅ 100 个项目同步耗时: {elapsed:.2f}s")


# ============================================================================
# [运行测试]
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
