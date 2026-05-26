#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂多人格协调引擎 · Persona Orchestrator
DNA: #龍芯⚡️2026-05-26-PERSONA-ORCHESTRATOR-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 多人格调度 - 根据任务特性选择合适的人格来执行
  2. 权限路由 - 通过人格权限等级自动路由到正确的执行器
  3. 冲突解决 - 当多个人格有不同意见时，通过 P00 仲裁
  4. 决策链管理 - 维护决策链，支持上诉和回滚
  5. 审计追踪 - 记录每个人格的决策和执行

系统层级：
  L0: 老大（UID9622） - 输入命令
       ↓
  L1: 人格协调器（本系统） - 分析任务，分配人格
       ↓
  L2: 三大支柱决议 - P00/P02/P05 确认
       ↓
  L3: 宝宝执行器（Baobao Dispatcher） - 检查权限，执行任务
       ↓
  L4: 操作系统级别 - 读写文件、执行代码等

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

import json
import datetime
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TaskType(Enum):
    """任务类型"""
    FILE_OPERATION = "file"
    CODE_EXECUTION = "code"
    DATA_OPERATION = "data"
    SYSTEM_OPERATION = "system"
    QUALITY_CHECK = "quality"
    DECISION_MAKING = "decision"
    SECURITY_CHECK = "security"
    COMMUNICATION = "communication"


class PersonaOrchestrator:
    """龍魂多人格协调引擎"""

    def __init__(self):
        self.system_root = Path.home() / "longhun-system"
        self.logs_dir = self.system_root / "logs"
        self.registry_path = self.system_root / "family_registry.json"

        self.personas = {}
        self.task_queue = []
        self.execution_history = []

        # 人格→任务类型映射
        self.persona_specialties = {
            "P00": ["decision_making", "arbitration"],  # 审判长
            "P01": ["strategy", "planning"],  # 诸葛亮
            "P02": ["execution", "all"],  # 宝宝 - 执行所有
            "P03": ["quality_check", "validation"],  # 雯雯
            "P04": ["semantic", "api_design"],  # 文心
            "P05": ["ethics", "values"],  # 老子
            "P06": ["culture", "tradition"],  # 孔子
            "P07": ["vulnerable_protection", "safety"],  # 墨子
            "P08": ["data", "privacy", "security"],  # 数据大师
            "P09": ["ui", "ux", "design"],  # 界面炼金
            "P10": ["monitoring", "detection"],  # 侦察兵
            "P11": ["security", "emergency"],  # 上帝之眼
            "LUCKY": ["expression", "documentation"]  # Lucky
        }

        self._load_registry()

    def _load_registry(self):
        """加载人格注册表"""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            self.personas = registry.get("personas", {})
            return True
        except Exception as e:
            print(f"加载人格注册表失败: {e}", file=sys.stderr)
            return False

    def analyze_task(self, task_description: str, task_type: str) -> Dict:
        """
        分析任务，确定所需的人格和权限等级

        Args:
            task_description: 任务描述
            task_type: 任务类型

        Returns:
            任务分析结果
        """
        suitable_personas = self._find_suitable_personas(task_type)

        return {
            "task_type": task_type,
            "task_description": task_description,
            "suitable_personas": suitable_personas,
            "primary_persona": suitable_personas[0] if suitable_personas else "P02",
            "min_permission_level": self._calculate_min_permission(task_type),
            "requires_three_pillars": self._requires_pillars_approval(task_type),
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("TASK-ANALYSIS")
        }

    def orchestrate(self,
                    task_description: str,
                    task_type: str,
                    parameters: Optional[Dict] = None) -> Dict:
        """
        协调任务执行

        完整的执行流程：
        1. 分析任务
        2. 分配人格
        3. 获取必要的批准（如果需要）
        4. 委托给宝宝执行
        5. 等待结果
        6. 记录审计日志

        Args:
            task_description: 任务描述
            task_type: 任务类型
            parameters: 任务参数

        Returns:
            执行结果
        """
        execution_id = f"EXEC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 1. 分析任务
        task_analysis = self.analyze_task(task_description, task_type)
        primary_persona_id = task_analysis["primary_persona"]
        primary_persona = self.personas.get(primary_persona_id, {})

        # 2. 确定是否需要三大支柱批准
        needs_approval = task_analysis["requires_three_pillars"]

        approval_status = "approved"
        if needs_approval:
            approval_status = "requires_three_pillars_decision"

        # 3. 委托给宝宝执行
        execution_plan = {
            "execution_id": execution_id,
            "task_type": task_type,
            "task_description": task_description,
            "assigned_to": primary_persona.get("name", primary_persona_id),
            "assigned_to_id": primary_persona_id,
            "approval_status": approval_status,
            "parameters": parameters or {},
            "created_at": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna(f"ORCHESTRATION-{primary_persona_id}"),
            "status": "ready_for_dispatch"
        }

        self._log_execution(execution_plan)
        return execution_plan

    def handle_conflict(self,
                        decision_a: Dict,
                        decision_b: Dict,
                        context: str = "") -> Dict:
        """
        处理人格间的冲突

        由 P00 审判长进行仲裁

        Args:
            decision_a: 第一个决策
            decision_b: 第二个决策
            context: 冲突背景

        Returns:
            仲裁结果
        """
        chief_justice = self.personas.get("P00", {})

        arbitration = {
            "arbitration_id": f"ARB-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "arbitrator": chief_justice.get("name", "P00"),
            "arbitrator_id": "P00",
            "decision_a": decision_a.get("description", ""),
            "decision_b": decision_b.get("description", ""),
            "context": context,
            "status": "initiated",
            "expected_resolution_time": (datetime.datetime.now() + datetime.timedelta(hours=4)).isoformat(),
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("CONFLICT-ARBITRATION"),
            "message": "冲突已提交给审判长，等待仲裁"
        }

        self._log_arbitration(arbitration)
        return arbitration

    def route_execution(self, execution_plan: Dict) -> Dict:
        """
        根据执行计划路由到实际的执行器

        如果分配给 P02 宝宝，则路由到 baobao_dispatcher.py
        如果分配给其他人格，则先由该人格处理后再交给宝宝

        Args:
            execution_plan: 执行计划

        Returns:
            路由结果
        """
        persona_id = execution_plan["assigned_to_id"]
        persona = self.personas.get(persona_id, {})

        # 如果是宝宝，直接路由到 dispatcher
        if persona_id == "P02":
            return self._route_to_baobao(execution_plan)
        else:
            # 其他人格先处理，然后交给宝宝
            return self._route_via_persona(execution_plan, persona)

    def get_decision_chain(self, execution_id: str) -> List[Dict]:
        """
        获取一个任务的完整决策链

        记录所有参与该任务的人格和他们的决策

        Args:
            execution_id: 执行ID

        Returns:
            决策链
        """
        # 从日志中提取所有相关的决策
        decision_chain = []

        # 这里会从 execution history 和各个日志文件中重建决策链
        # 格式: [{persona, decision, timestamp, dna}, ...]

        return decision_chain

    def _find_suitable_personas(self, task_type: str) -> List[str]:
        """根据任务类型找出合适的人格"""
        suitable = []

        for persona_id, specialties in self.persona_specialties.items():
            # 把任务类型转换为小写并匹配
            task_type_lower = task_type.lower().replace("_", "")
            for specialty in specialties:
                if "all" in specialties or task_type_lower in specialty.replace("_", ""):
                    suitable.append(persona_id)
                    break

        # 如果没有找到合适的，默认分配给宝宝
        if not suitable:
            suitable.append("P02")

        return suitable

    def _calculate_min_permission(self, task_type: str) -> int:
        """根据任务类型计算所需的最小权限等级"""
        permission_map = {
            "file": 50,
            "code": 60,
            "data": 70,
            "system": 80,
            "quality": 50,
            "decision": 90,
            "security": 85,
            "communication": 40
        }
        return permission_map.get(task_type.lower(), 50)

    def _requires_pillars_approval(self, task_type: str) -> bool:
        """判断任务是否需要三大支柱批准"""
        critical_types = ["system", "decision", "security"]
        return any(ct in task_type.lower() for ct in critical_types)

    def _route_to_baobao(self, execution_plan: Dict) -> Dict:
        """路由到宝宝执行器"""
        return {
            "routing": "baobao_dispatcher",
            "execution_id": execution_plan["execution_id"],
            "status": "routed_to_baobao",
            "dispatcher_path": "~/longhun-system/core/baobao_dispatcher.py",
            "message": "已路由给宝宝执行器",
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("ROUTE-BAOBAO")
        }

    def _route_via_persona(self, execution_plan: Dict, persona: Dict) -> Dict:
        """通过特定人格路由"""
        persona_id = execution_plan["assigned_to_id"]
        return {
            "routing": f"persona_{persona_id}",
            "execution_id": execution_plan["execution_id"],
            "status": "routed_via_persona",
            "persona": persona.get("name", persona_id),
            "persona_id": persona_id,
            "core_power": persona.get("core_power", ""),
            "message": f"已路由给 {persona.get('name', persona_id)} 处理",
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna(f"ROUTE-{persona_id}")
        }

    def _generate_dna(self, operation_type: str) -> str:
        """生成DNA追溯码"""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龍芯⚡️{date_str}-{operation_type}-v1.0"

    def _log_execution(self, execution_plan: Dict):
        """记录执行计划"""
        try:
            log_path = self.logs_dir / "persona_executions.jsonl"
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(execution_plan, ensure_ascii=False) + "\n")
            self.execution_history.append(execution_plan)
        except Exception as e:
            print(f"执行日志写入失败: {e}", file=sys.stderr)

    def _log_arbitration(self, arbitration: Dict):
        """记录仲裁"""
        try:
            log_path = self.logs_dir / "persona_arbitrations.jsonl"
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(arbitration, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"仲裁日志写入失败: {e}", file=sys.stderr)

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "system": "Persona Orchestrator",
            "status": "operational",
            "total_personas": len(self.personas),
            "execution_queue_length": len(self.task_queue),
            "total_executions": len(self.execution_history),
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("ORCHESTRATOR-STATUS")
        }


def main():
    """命令行接口"""
    orchestrator = PersonaOrchestrator()

    if len(sys.argv) < 2:
        status = orchestrator.get_system_status()
        print("\n✅ 龍魂多人格协调引擎已启动")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))
        sys.exit(0)

    command = sys.argv[1]

    if command == "analyze":
        if len(sys.argv) < 4:
            print("用法: python3 persona_orchestrator.py analyze <task_type> <description>")
            sys.exit(1)
        task_type = sys.argv[2]
        description = " ".join(sys.argv[3:])
        result = orchestrator.analyze_task(description, task_type)
        print("\n📊 任务分析")
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    elif command == "orchestrate":
        if len(sys.argv) < 4:
            print("用法: python3 persona_orchestrator.py orchestrate <task_type> <description>")
            sys.exit(1)
        task_type = sys.argv[2]
        description = " ".join(sys.argv[3:])
        result = orchestrator.orchestrate(description, task_type)
        print("\n🎼 执行协调")
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    elif command == "status":
        status = orchestrator.get_system_status()
        print("\n📊 协调器状态")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
