#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 v9.0 · 任务执行器适配层
Task Executor Integration Adapter

将 task_executor_live_v1.py 与 v9.0 统一集成层连接

DNA:#龍芯⚡️2026-06-06-V9-TASK-EXECUTOR-ADAPTER-FILE2-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

UID9622 · 诸葛鑫 · 龍芯北辰
责任: UID9622·不免责
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
    """v9.0 系统智能体类型"""
    FLOW_DECISION = "v9_flow_decision"      # v4.1 决策辟
    SANCAI_SYNC = "v9_sancai_sync"          # v1.0 三合同步器
    NEURAL_ROUTING = "v9_neural_routing"    # v4.0 神经映射
    SYSTEM_CHECK = "v9_system_check"        # 系统检查


class V9TaskExecutorAdapter:
    """
    v9.0 任务执行器适配层

    功能：
    1. 拦截 task_executor_live 的任务
    2. 判断是否为 v9 任务
    3. 路由到 v9 系统执行
    4. 返回统一的执行结果
    5. 维持与现有 AGENT 的相容性
    """

    def __init__(self):
        self.bridge = V9SystemIntegrationBridge(seed=9622)
        self.execution_log: List[Dict[str, Any]] = []

        # v9 任务标签映射
        self.v9_label_map = {
            "flow_decision": V9AgentType.FLOW_DECISION,
            "sancai_sync": V9AgentType.SANCAI_SYNC,
            "neural_routing": V9AgentType.NEURAL_ROUTING,
            "system_check": V9AgentType.SYSTEM_CHECK,
            "决策": V9AgentType.FLOW_DECISION,
            "同步": V9AgentType.SANCAI_SYNC,
            "路由": V9AgentType.NEURAL_ROUTING,
            "检查": V9AgentType.SYSTEM_CHECK,
        }

    def is_v9_task(self, task: Dict) -> bool:
        """判断任务是否为 v9 系统任务"""
        # 检查标签
        labels = task.get("labels", [])
        for label in labels:
            if label in self.v9_label_map:
                return True

        # 检查标题
        title = task.get("title", "").lower()
        v9_keywords = ["v9", "决策", "同步", "三环", "集成", "统一"]
        for keyword in v9_keywords:
            if keyword in title:
                return True

        return False

    def convert_to_v9_task(self, task: Dict) -> SystemIntegrationTask:
        """将 task_executor 任务转换为 v9 任务"""
        # 确定任务类型
        task_type = self._detect_task_type(task)

        # 确定模块层
        module_layer = self._detect_module_layer(task_type)

        # 构建输入数据
        input_data = {
            "original_task": task,
            "title": task.get("title", ""),
            "labels": task.get("labels", []),
            "priority": task.get("priority", 3),
            # 根据任务类型添加特定数据
        }

        # 添加 v9 特定的输入
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

        # 创建 v9 任务
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
        """检测任务类型"""
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

        # 预设类型
        return TaskType.SANCAI_SYNC

    def _detect_module_layer(self, task_type: TaskType) -> ModuleLayer:
        """检测模块层"""
        type_map = {
            TaskType.FLOW_DECISION: ModuleLayer.V4_1_FLOW_DECISION,
            TaskType.SANCAI_SYNC: ModuleLayer.V1_0_SANCAI_SYNC,
            TaskType.NEURAL_ROUTING: ModuleLayer.V4_0_NEURAL_MAP,
            TaskType.SYSTEM_CHECK: ModuleLayer.V1_0_SANCAI_SYNC,
        }
        return type_map.get(task_type, ModuleLayer.V1_0_SANCAI_SYNC)

    def execute_v9_task(self, task: Dict) -> Dict[str, Any]:
        """执行 v9 任务"""
        # 转换任务
        v9_task = self.convert_to_v9_task(task)

        # 注册到 v9 系统
        self.bridge.register_task(v9_task)

        # 执行任务
        result = self.bridge.execute_task(v9_task)

        # 转换回 task_executor 格式
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

        # 记录执行日志
        self.execution_log.append(executor_result)

        return executor_result

    def get_v9_agent_mapping(self) -> Dict[str, str]:
        """
        获取 v9 任务适配器的智能体映射

        可添加到 task_executor_live_v1.py 的 AGENT_COMMANDS
        """
        return {
            "V9-FLOW-DECISION": "v9_flow_decision",
            "V9-SANCAI-SYNC": "v9_sancai_sync",
            "V9-NEURAL-ROUTING": "v9_neural_routing",
            "V9-SYSTEM-CHECK": "v9_system_check",
        }

    def system_health_check(self) -> Dict[str, Any]:
        """进行系统健康检查"""
        health = self.bridge.system_health_check()
        return {
            "adapter": "v9_task_executor_adapter",
            "timestamp": datetime.now().isoformat(),
            "tasks_executed": len(self.execution_log),
            "v9_system": health,
            "compatibility": "full"
        }

    def generate_execution_report(self) -> str:
        """生成执行报告"""
        report = f"""# v9.0 任务执行器适配层报告

**生成时间**: {datetime.now().isoformat()}
**DNA**: #龍芯⚡️2026-06-06-V9-TASK-EXECUTOR-ADAPTER-REPORT

## 执行统计

- 总任务数: {len(self.execution_log)}
- 成功: {sum(1 for r in self.execution_log if r['status'] == 'success')}
- 失败: {sum(1 for r in self.execution_log if r['status'] == 'failed')}

## 系统状态

"""
        health = self.system_health_check()
        report += f"```json\n{json.dumps(health, indent=2, ensure_ascii=False)}\n```\n"

        return report


def create_v9_executor_wrapper():
    """
    创建一个包装器，集成 task_executor_live_v1 和 v9.0 系统

    使用方式：
    1. 在 task_executor_live_v1.py 中导入此模块
    2. 在 LiveTaskExecutor.route_task() 中检查 v9 标签
    3. 如果是 v9 任务，委派给 V9TaskExecutorAdapter
    """
    return V9TaskExecutorAdapter()


# ═══════════════════════════════════════════════════════════════════════════
# 示例集成代码（供参考，可添加到 task_executor_live_v1.py）
# ═══════════════════════════════════════════════════════════════════════════

INTEGRATION_EXAMPLE = """
# 在 task_executor_live_v1.py 中添加：

from cnsh.v9_task_executor_adapter import V9TaskExecutorAdapter

class LiveTaskExecutorWithV9(LiveTaskExecutor):
    \"\"\"整合 v9.0 系统的任务执行器\"\"\"

    def __init__(self):
        super().__init__()
        self.v9_adapter = V9TaskExecutorAdapter()

    def route_task(self, task: Dict) -> Tuple[List[str], str]:
        \"\"\"路由任务（整合 v9）\"\"\"

        # 检查是否为 v9 任务
        if self.v9_adapter.is_v9_task(task):
            return ["V9-SYSTEM"], "v9.0 系统路由"

        # 否则使用原有逻辑
        return super().route_task(task)

    def execute_agent(self, agent_id: str) -> Dict:
        \"\"\"执行智能体（整合 v9）\"\"\"

        # v9 系统代理
        if agent_id.startswith("V9-"):
            return {
                "agent_id": agent_id,
                "status": "success",
                "message": "v9 系统执行"
            }

        # 原有逻辑
        return super().execute_agent(agent_id)
"""


if __name__ == "__main__":
    # 测试适配器
    adapter = V9TaskExecutorAdapter()

    # 模拟任务
    test_task = {
        "task_id": "TEST-V9-001",
        "title": "三环同步测试",
        "labels": ["sancai_sync"],
        "priority": 5
    }

    # 执行
    print("【v9.0 任务执行器适配层】")
    print(f"是否为 v9 任务: {adapter.is_v9_task(test_task)}")
    result = adapter.execute_v9_task(test_task)
    print(f"执行结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print(f"\n系统健康检查: {json.dumps(adapter.system_health_check(), indent=2, ensure_ascii=False)}")
