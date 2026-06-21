#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 v9.0 · 任務執行器適配層
Task Executor Integration Adapter

將 task_executor_live_v1.py 與 v9.0 統一集成層連接

DNA:#龍芯⚡️2026-06-06-V9-TASK-EXECUTOR-ADAPTER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

UID9622 · 諸葛鑫 · 龍芯北辰
責任: UID9622·不免責
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from enum import Enum

from cnsh.v9_system_integration_bridge import (
    V9SystemIntegrationBridge,
    SystemIntegrationTask,
    TaskType,
    ModuleLayer
)


class V9AgentType(Enum):
    """v9.0 系統智能體類型"""
    FLOW_DECISION = "v9_flow_decision"      # v4.1 決策闢
    SANCAI_SYNC = "v9_sancai_sync"          # v1.0 三合同步器
    NEURAL_ROUTING = "v9_neural_routing"    # v4.0 神經映射
    SYSTEM_CHECK = "v9_system_check"        # 系統檢查


class V9TaskExecutorAdapter:
    """
    v9.0 任務執行器適配層

    功能：
    1. 攔截 task_executor_live 的任務
    2. 判斷是否為 v9 任務
    3. 路由到 v9 系統執行
    4. 返回統一的執行結果
    5. 維持與現有 AGENT 的相容性
    """

    def __init__(self):
        self.bridge = V9SystemIntegrationBridge(seed=9622)
        self.execution_log: List[Dict[str, Any]] = []

        # v9 任務標籤映射
        self.v9_label_map = {
            "flow_decision": V9AgentType.FLOW_DECISION,
            "sancai_sync": V9AgentType.SANCAI_SYNC,
            "neural_routing": V9AgentType.NEURAL_ROUTING,
            "system_check": V9AgentType.SYSTEM_CHECK,
            "決策": V9AgentType.FLOW_DECISION,
            "同步": V9AgentType.SANCAI_SYNC,
            "路由": V9AgentType.NEURAL_ROUTING,
            "檢查": V9AgentType.SYSTEM_CHECK,
        }

    def is_v9_task(self, task: Dict) -> bool:
        """判斷任務是否為 v9 系統任務"""
        # 檢查標籤
        labels = task.get("labels", [])
        for label in labels:
            if label in self.v9_label_map:
                return True

        # 檢查標題
        title = task.get("title", "").lower()
        v9_keywords = ["v9", "決策", "同步", "三環", "集成", "統一"]
        for keyword in v9_keywords:
            if keyword in title:
                return True

        return False

    def convert_to_v9_task(self, task: Dict) -> SystemIntegrationTask:
        """將 task_executor 任務轉換為 v9 任務"""
        # 確定任務類型
        task_type = self._detect_task_type(task)

        # 確定模塊層
        module_layer = self._detect_module_layer(task_type)

        # 構建輸入數據
        input_data = {
            "original_task": task,
            "title": task.get("title", ""),
            "labels": task.get("labels", []),
            "priority": task.get("priority", 3),
            # 根據任務類型添加特定數據
        }

        # 添加 v9 特定的輸入
        if task_type == TaskType.SANCAI_SYNC:
            input_data.update({
                "ipa": {
                    "ipa_node": f"IPA-EXEC-{task.get('task_id', 'UNKNOWN')}",
                    "ipa_address": "/executor/v9",
                    "main_persona": "P00",
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
                    "nodes": [{"weight": 0.9, "edges": []}]
                }
            })

        # 創建 v9 任務
        v9_task = SystemIntegrationTask(
            task_id=task.get("task_id", f"TASK-{datetime.now().timestamp()}"),
            task_type=task_type,
            module_layer=module_layer,
            input_data=input_data,
            priority=task.get("priority", 3),
            labels=task.get("labels", [])
        )

        return v9_task

    def _detect_task_type(self, task: Dict) -> TaskType:
        """檢測任務類型"""
        labels = task.get("labels", [])

        for label in labels:
            if label in self.v9_label_map:
                agent_type = self.v9_label_map[label]
                if agent_type == V9AgentType.FLOW_DECISION:
                    return TaskType.FLOW_DECISION
                elif agent_type == V9AgentType.SANCAI_SYNC:
                    return TaskType.SANCAI_SYNC
                elif agent_type == V9AgentType.NEURAL_ROUTING:
                    return TaskType.NEURAL_ROUTING
                elif agent_type == V9AgentType.SYSTEM_CHECK:
                    return TaskType.SYSTEM_CHECK

        # 預設類型
        return TaskType.SANCAI_SYNC

    def _detect_module_layer(self, task_type: TaskType) -> ModuleLayer:
        """檢測模塊層"""
        type_map = {
            TaskType.FLOW_DECISION: ModuleLayer.V4_1_FLOW_DECISION,
            TaskType.SANCAI_SYNC: ModuleLayer.V1_0_SANCAI_SYNC,
            TaskType.NEURAL_ROUTING: ModuleLayer.V4_0_NEURAL_MAP,
            TaskType.SYSTEM_CHECK: ModuleLayer.V1_0_SANCAI_SYNC,
        }
        return type_map.get(task_type, ModuleLayer.V1_0_SANCAI_SYNC)

    def execute_v9_task(self, task: Dict) -> Dict[str, Any]:
        """執行 v9 任務"""
        # 轉換任務
        v9_task = self.convert_to_v9_task(task)

        # 註冊到 v9 系統
        self.bridge.register_task(v9_task)

        # 執行任務
        result = self.bridge.execute_task(v9_task)

        # 轉換回 task_executor 格式
        executor_result = {
            "task_id": task.get("task_id"),
            "status": "success" if result.status == "success" else "failed",
            "module": result.module_layer.value,
            "v9_status": result.status,
            "output": result.output_data,
            "dna": result.dna_chain,
            "execution_ms": result.execution_time_ms,
            "timestamp": datetime.now().isoformat()
        }

        # 記錄執行日誌
        self.execution_log.append(executor_result)

        return executor_result

    def get_v9_agent_mapping(self) -> Dict[str, str]:
        """
        獲取 v9 任務適配器的智能體映射

        可添加到 task_executor_live_v1.py 的 AGENT_COMMANDS
        """
        return {
            "V9-FLOW-DECISION": "v9_flow_decision",
            "V9-SANCAI-SYNC": "v9_sancai_sync",
            "V9-NEURAL-ROUTING": "v9_neural_routing",
            "V9-SYSTEM-CHECK": "v9_system_check",
        }

    def system_health_check(self) -> Dict[str, Any]:
        """進行系統健康檢查"""
        health = self.bridge.system_health_check()
        return {
            "adapter": "v9_task_executor_adapter",
            "timestamp": datetime.now().isoformat(),
            "tasks_executed": len(self.execution_log),
            "v9_system": health,
            "compatibility": "full"
        }

    def generate_execution_report(self) -> str:
        """生成執行報告"""
        report = f"""# v9.0 任務執行器適配層報告

**生成時間**: {datetime.now().isoformat()}
**DNA**: #龍芯⚡️2026-06-06-V9-TASK-EXECUTOR-ADAPTER-REPORT

## 執行統計

- 總任務數: {len(self.execution_log)}
- 成功: {sum(1 for r in self.execution_log if r['status'] == 'success')}
- 失敗: {sum(1 for r in self.execution_log if r['status'] == 'failed')}

## 系統狀態

"""
        health = self.system_health_check()
        report += f"```json\n{json.dumps(health, indent=2, ensure_ascii=False)}\n```\n"

        return report


def create_v9_executor_wrapper():
    """
    創建一個包裝器，集成 task_executor_live_v1 和 v9.0 系統

    使用方式：
    1. 在 task_executor_live_v1.py 中導入此模塊
    2. 在 LiveTaskExecutor.route_task() 中檢查 v9 標籤
    3. 如果是 v9 任務，委派給 V9TaskExecutorAdapter
    """
    return V9TaskExecutorAdapter()


# ═══════════════════════════════════════════════════════════════════════════
# 示例集成代碼（供參考，可添加到 task_executor_live_v1.py）
# ═══════════════════════════════════════════════════════════════════════════

INTEGRATION_EXAMPLE = """
# 在 task_executor_live_v1.py 中添加：

from cnsh.v9_task_executor_adapter import V9TaskExecutorAdapter

class LiveTaskExecutorWithV9(LiveTaskExecutor):
    \"\"\"整合 v9.0 系統的任務執行器\"\"\"

    def __init__(self):
        super().__init__()
        self.v9_adapter = V9TaskExecutorAdapter()

    def route_task(self, task: Dict) -> Tuple[List[str], str]:
        \"\"\"路由任務（整合 v9）\"\"\"

        # 檢查是否為 v9 任務
        if self.v9_adapter.is_v9_task(task):
            return ["V9-SYSTEM"], "v9.0 系統路由"

        # 否則使用原有邏輯
        return super().route_task(task)

    def execute_agent(self, agent_id: str) -> Dict:
        \"\"\"執行智能體（整合 v9）\"\"\"

        # v9 系統代理
        if agent_id.startswith("V9-"):
            return {
                "agent_id": agent_id,
                "status": "success",
                "message": "v9 系統執行"
            }

        # 原有邏輯
        return super().execute_agent(agent_id)
"""


if __name__ == "__main__":
    # 測試適配器
    adapter = V9TaskExecutorAdapter()

    # 模擬任務
    test_task = {
        "task_id": "TEST-V9-001",
        "title": "三環同步測試",
        "labels": ["sancai_sync"],
        "priority": 5
    }

    # 執行
    print("【v9.0 任務執行器適配層】")
    print(f"是否為 v9 任務: {adapter.is_v9_task(test_task)}")
    result = adapter.execute_v9_task(test_task)
    print(f"執行結果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print(f"\n系統健康檢查: {json.dumps(adapter.system_health_check(), indent=2, ensure_ascii=False)}")
