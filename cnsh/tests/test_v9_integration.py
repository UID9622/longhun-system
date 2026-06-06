#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 v9.0 系統集成測試

DNA: #龍芯⚡️2026-06-06-V9-INTEGRATION-TEST-v1.0
"""

import pytest
from datetime import datetime
from cnsh.v9_system_integration_bridge import (
    V9SystemIntegrationBridge,
    SystemIntegrationTask,
    TaskType,
    ModuleLayer
)


class TestV9SystemIntegrationBridge:
    """v9.0 系統集成測試"""

    @pytest.fixture
    def bridge(self):
        """創建集成橋實例"""
        return V9SystemIntegrationBridge(seed=9622)

    def test_bridge_initialization(self, bridge):
        """測試橋初始化"""
        assert bridge.seed == 9622
        assert len(bridge.task_queue) == 0
        assert len(bridge.execution_history) == 0
        assert len(bridge.system_dna_chain) == 0

    def test_task_registration(self, bridge):
        """測試任務註冊"""
        task = SystemIntegrationTask(
            task_id="TEST-001",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={"ipa": {"ipa_node": "IPA-TEST"}}
        )

        task_id = bridge.register_task(task)
        assert task_id == "TEST-001"
        assert len(bridge.task_queue) == 1

    def test_task_auto_id_generation(self, bridge):
        """測試任務自動 ID 生成"""
        task = SystemIntegrationTask(
            task_id="",
            task_type=TaskType.FLOW_DECISION,
            module_layer=ModuleLayer.V4_1_FLOW_DECISION,
            input_data={}
        )

        task_id = bridge.register_task(task)
        assert task_id.startswith("TASK-V9-")
        assert len(task_id) > 20

    def test_task_routing_flow_decision(self, bridge):
        """測試流程決策任務路由"""
        task = SystemIntegrationTask(
            task_id="ROUTE-001",
            task_type=TaskType.FLOW_DECISION,
            module_layer=ModuleLayer.V4_1_FLOW_DECISION,
            input_data={}
        )

        module, reason = bridge.route_task(task)
        assert module == ModuleLayer.V4_1_FLOW_DECISION
        assert "精確匹配" in reason

    def test_task_routing_sancai_sync(self, bridge):
        """測試三合同步器任務路由"""
        task = SystemIntegrationTask(
            task_id="ROUTE-002",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={}
        )

        module, reason = bridge.route_task(task)
        assert module == ModuleLayer.V1_0_SANCAI_SYNC
        assert "精確匹配" in reason

    def test_task_routing_priority(self, bridge):
        """測試優先級路由"""
        task_high = SystemIntegrationTask(
            task_id="ROUTE-003",
            task_type=TaskType.SYSTEM_CHECK,
            module_layer=ModuleLayer.V4_1_FLOW_DECISION,
            input_data={},
            priority=8
        )

        module, reason = bridge.route_task(task_high)
        assert module == ModuleLayer.V4_1_FLOW_DECISION
        assert "優先級" in reason

    def test_sancai_sync_execution(self, bridge):
        """測試三合同步器執行"""
        task = SystemIntegrationTask(
            task_id="EXEC-001",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={
                "ipa": {
                    "ipa_node": "IPA-TEST-EXEC",
                    "ipa_address": "/test/exec",
                    "main_persona": "P03",
                    "output_signal": "pass"
                },
                "ring": {
                    "age": 100,
                    "radius": 100.0,
                    "strength": 0.8,
                    "x": 400.0,
                    "y": 300.0
                },
                "knowledge_graph": {
                    "nodes": [
                        {"weight": 0.9, "edges": [1, 2]},
                        {"weight": 0.8, "edges": [0]},
                        {"weight": 0.7, "edges": [0, 1]}
                    ]
                }
            }
        )

        bridge.register_task(task)
        result = bridge.execute_task(task)

        assert result.status == "success"
        assert result.module_layer == ModuleLayer.V1_0_SANCAI_SYNC
        assert "particles_count" in result.output_data
        assert "signals_count" in result.output_data
        assert "palaces_count" in result.output_data

    def test_system_health_check(self, bridge):
        """測試系統健康檢查"""
        health = bridge.system_health_check()

        assert "timestamp" in health
        assert "overall_status" in health
        assert "modules" in health
        assert "v4.1_flow_decision" in health["modules"]
        assert "v1.0_sancai_sync" in health["modules"]
        assert "v3.0_breath_brain" in health["modules"]
        assert "v4.0_neural_map" in health["modules"]

    def test_execute_queue(self, bridge):
        """測試隊列執行"""
        # 創建多個任務
        for i in range(3):
            task = SystemIntegrationTask(
                task_id=f"QUEUE-{i:03d}",
                task_type=TaskType.SANCAI_SYNC,
                module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
                input_data={
                    "ipa": {"ipa_node": f"IPA-QUEUE-{i}"},
                    "ring": {"age": 100 + i * 10, "radius": 100.0, "strength": 0.8, "x": 400.0, "y": 300.0},
                    "knowledge_graph": {
                        "nodes": [{"weight": 0.9, "edges": []}]
                    }
                }
            )
            bridge.register_task(task)

        results = bridge.execute_queue()
        assert len(results) == 3
        assert all(r.status in ["success", "failed"] for r in results)

    def test_dna_chain_generation(self, bridge):
        """測試 DNA 鏈生成"""
        task = SystemIntegrationTask(
            task_id="DNA-001",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={
                "ipa": {"ipa_node": "IPA-DNA-TEST"},
                "ring": {"age": 100, "radius": 100.0, "strength": 0.8, "x": 400.0, "y": 300.0},
                "knowledge_graph": {"nodes": [{"weight": 0.9, "edges": []}]}
            }
        )

        bridge.register_task(task)
        result = bridge.execute_task(task)

        assert result.dna_chain.startswith("#龍芯⚡️")
        assert "V9-INTEGRATION" in result.dna_chain
        assert len(bridge.system_dna_chain) > 0

    def test_json_export(self, bridge):
        """測試 JSON 導出"""
        json_str = bridge.to_json()
        assert isinstance(json_str, str)
        assert "v9_integration_bridge" in json_str
        assert "system_dna_chain" in json_str

    def test_success_rate_calculation(self, bridge):
        """測試成功率計算"""
        assert bridge._calculate_success_rate() == 0.0

        task = SystemIntegrationTask(
            task_id="RATE-001",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={
                "ipa": {"ipa_node": "IPA-RATE-TEST"},
                "ring": {"age": 100, "radius": 100.0, "strength": 0.8, "x": 400.0, "y": 300.0},
                "knowledge_graph": {"nodes": [{"weight": 0.9, "edges": []}]}
            }
        )

        bridge.register_task(task)
        bridge.execute_task(task)

        rate = bridge._calculate_success_rate()
        assert rate > 0


class TestV9Integration:
    """v9.0 整體集成測試"""

    def test_three_ring_integration(self):
        """測試三環集成"""
        bridge = V9SystemIntegrationBridge()

        # 創建三環任務
        task = SystemIntegrationTask(
            task_id="THREE-RING-001",
            task_type=TaskType.SANCAI_SYNC,
            module_layer=ModuleLayer.V1_0_SANCAI_SYNC,
            input_data={
                "ipa": {
                    "ipa_node": "IPA-FLOW-GATE-PRIVACY",
                    "ipa_address": "/flow/gate/privacy",
                    "main_persona": "P03",
                    "output_signal": "pass"
                },
                "ring": {
                    "age": 150,
                    "radius": 120.0,
                    "strength": 0.85,
                    "x": 400.0,
                    "y": 300.0
                },
                "knowledge_graph": {
                    "nodes": [
                        {"weight": 0.9, "edges": [1, 2, 3]},
                        {"weight": 0.8, "edges": [0, 2]},
                        {"weight": 0.7, "edges": [0, 1, 3]},
                    ],
                    "parent_dna": "#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-v1.0"
                }
            }
        )

        bridge.register_task(task)
        result = bridge.execute_task(task)

        # 驗證執行結果
        assert result.status == "success"
        assert "particles_count" in result.output_data
        assert "signals_count" in result.output_data
        assert "palaces_count" in result.output_data
        assert "verify_status" in result.output_data
        assert result.output_data["verify_status"] == "🟢"

    def test_system_readiness(self):
        """測試系統準備就緒"""
        bridge = V9SystemIntegrationBridge()
        health = bridge.system_health_check()

        assert health["overall_status"] in ["🟢 healthy", "🟡 degraded"]
        assert health["modules"]["v1.0_sancai_sync"]["status"] in ["healthy", "unhealthy"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
