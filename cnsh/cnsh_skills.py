#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·CNSH 技能系统 v2.0
Skills = Hooks + EventBus + Recovery Matrix

DNA: #龍芯⚡️2026-05-25-CNSH-SKILLS-v2.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

根据 CNSH Local Sovereign AgentOS v2.0 实现
- §4 Hook System (5类钩子)
- §7 EventBus (6 channels)
- §12 Recovery Matrix

理论指导: 曾仕强老师
献礼: 龍魂系统·永恒守护

本地执行·永不外送·禁商业核心
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path


# ════════════════════════════════════════════════════════
# 第一步：事件总线 EventBus (§7)
# ════════════════════════════════════════════════════════

class EventType(Enum):
    """6 个事件频道"""
    SEMANTIC = "semantic.events"
    RUNTIME = "runtime.events"
    AUDIT = "audit.events"
    MEMORY = "memory.events"
    SNAPSHOT = "snapshot.events"
    EVOLUTION = "evolution.events"


class AuditColor(Enum):
    """三色审计"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


@dataclass
class Event:
    """事件包结构"""
    type: EventType
    source: str  # runtime_core | agent | hook | user
    dna: str
    timestamp: str
    payload: Dict[str, Any]
    severity: AuditColor

    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "source": self.source,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "severity": self.severity.value,
        }


class EventBus:
    """事件总线：6 频道发布-订阅"""

    def __init__(self):
        self.channels = {et.value: [] for et in EventType}
        self.subscribers: Dict[str, List[Callable]] = {et.value: [] for et in EventType}

    def subscribe(self, channel: str, handler: Callable) -> None:
        """订阅某频道"""
        if channel in self.subscribers:
            self.subscribers[channel].append(handler)

    def publish(self, event: Event) -> None:
        """发布事件"""
        self.channels[event.type.value].append(event)

        # 触发所有订阅者
        for handler in self.subscribers[event.type.value]:
            try:
                handler(event)
            except Exception as e:
                print(f"  🔴 事件处理失败: {event.type.value} → {e}")

    def list_events(self, channel: str) -> List[Dict]:
        """列出某频道的所有事件"""
        return [e.to_dict() for e in self.channels.get(channel, [])]


# ════════════════════════════════════════════════════════
# 第二步：钩子系统 Hook System (§4)
# ════════════════════════════════════════════════════════

class HookType(Enum):
    """5 类钩子"""
    PRE_INPUT = "pre_input_hook"
    PRE_EXECUTION = "pre_execution_hook"
    POST_EXECUTION = "post_execution_hook"
    PRE_WRITE = "pre_write_hook"
    FAILURE = "failure_hook"


@dataclass
class HookResult:
    """钩子执行结果"""
    success: bool
    message: str
    color: AuditColor = AuditColor.GREEN
    data: Dict[str, Any] = None


class HookRegistry:
    """钩子注册表与执行器"""

    def __init__(self, event_bus: EventBus):
        self.hooks: Dict[str, List[Callable]] = {ht.value: [] for ht in HookType}
        self.event_bus = event_bus

    def register(self, hook_type: str, handler: Callable) -> None:
        """注册钩子"""
        if hook_type in self.hooks:
            self.hooks[hook_type].append(handler)

    def execute(self, hook_type: str, context: Dict) -> List[HookResult]:
        """执行某类所有钩子"""
        results = []
        for handler in self.hooks.get(hook_type, []):
            try:
                result = handler(context)
                results.append(result)
            except Exception as e:
                results.append(
                    HookResult(success=False, message=str(e), color=AuditColor.RED)
                )
        return results


# ════════════════════════════════════════════════════════
# 第三步：恢复矩阵 Recovery Matrix (§12)
# ════════════════════════════════════════════════════════

@dataclass
class Snapshot:
    """快照记录"""
    snapshot_id: str
    timestamp: str
    dna: str
    runtime_state: Dict[str, Any]
    memory_state: Dict[str, Any]
    audit_hash: str


class SnapshotManager:
    """快照管理：append-only"""

    def __init__(self, snapshot_dir: str = "~/.cnsh/snapshots"):
        self.snapshot_dir = Path(snapshot_dir).expanduser()
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: List[Snapshot] = []

    def create_snapshot(self, dna: str, runtime_state: Dict, memory_state: Dict) -> Snapshot:
        """创建快照（append-only）"""
        snapshot_id = f"snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        snapshot = Snapshot(
            snapshot_id=snapshot_id,
            timestamp=datetime.now().isoformat(),
            dna=dna,
            runtime_state=runtime_state,
            memory_state=memory_state,
            audit_hash=str(hash(str(runtime_state) + str(memory_state)))[:16],
        )

        # 追加到文件
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.json"
        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(asdict(snapshot), f, ensure_ascii=False, indent=2)

        self.snapshots.append(snapshot)
        return snapshot

    def restore_from_snapshot(self, snapshot_id: str) -> Optional[Snapshot]:
        """从快照恢复"""
        for snapshot in self.snapshots:
            if snapshot.snapshot_id == snapshot_id:
                return snapshot
        return None


class RecoveryMatrix:
    """恢复矩阵：故障恢复策略"""

    def __init__(self, snapshot_manager: SnapshotManager):
        self.snapshot_manager = snapshot_manager
        self.recovery_strategies = {}

    def register_strategy(self, failure_type: str, strategy: Callable) -> None:
        """注册恢复策略"""
        self.recovery_strategies[failure_type] = strategy

    def recover(self, failure_type: str, context: Dict) -> Dict:
        """执行恢复"""
        strategy = self.recovery_strategies.get(failure_type)
        if not strategy:
            return {"success": False, "message": f"未知故障类型: {failure_type}"}

        try:
            result = strategy(context, self.snapshot_manager)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "message": str(e)}


# ════════════════════════════════════════════════════════
# 第四步：技能集成（Hook + EventBus + Recovery）
# ════════════════════════════════════════════════════════

class CNSHSkillRuntime:
    """CNSH 技能运行时"""

    def __init__(self):
        self.event_bus = EventBus()
        self.hook_registry = HookRegistry(self.event_bus)
        self.snapshot_manager = SnapshotManager()
        self.recovery_matrix = RecoveryMatrix(self.snapshot_manager)
        self.dna_chain: List[str] = []

        # 设置默认钩子
        self._setup_default_hooks()

    def _setup_default_hooks(self):
        """设置默认钩子"""
        # 前置输入钩子
        def pre_input_check(context: Dict) -> HookResult:
            if not context.get("text"):
                return HookResult(success=False, message="输入为空", color=AuditColor.RED)
            return HookResult(success=True, message="输入验证通过", color=AuditColor.GREEN)

        self.hook_registry.register(HookType.PRE_INPUT.value, pre_input_check)

        # 快照钩子
        def create_snapshot_hook(context: Dict) -> HookResult:
            try:
                self.snapshot_manager.create_snapshot(
                    dna=context.get("dna", ""),
                    runtime_state=context.get("state", {}),
                    memory_state=context.get("memory", {})
                )
                return HookResult(success=True, message="快照创建成功", color=AuditColor.GREEN)
            except Exception as e:
                return HookResult(success=False, message=str(e), color=AuditColor.RED)

        self.hook_registry.register(HookType.PRE_EXECUTION.value, create_snapshot_hook)

    def execute_skill(self, skill_name: str, context: Dict) -> Dict:
        """执行技能（完整流程）"""
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H:%M')}-SKILL-{skill_name}"

        # 1. 前置输入检查
        pre_input_results = self.hook_registry.execute(HookType.PRE_INPUT.value, context)
        if not all(r.success for r in pre_input_results):
            return {"success": False, "error": "前置检查失败", "dna": dna}

        # 2. 快照
        pre_exec_results = self.hook_registry.execute(HookType.PRE_EXECUTION.value, context)

        # 3. 执行技能（这里只是示例）
        try:
            execution_result = {"executed": True, "skill": skill_name, "time": time.time()}
        except Exception as e:
            # 失败时触发故障钩子
            self.hook_registry.execute(HookType.FAILURE.value, {"error": str(e)})
            return {"success": False, "error": str(e), "dna": dna}

        # 4. 后置执行（如压缩、DNA 链）
        post_exec_results = self.hook_registry.execute(HookType.POST_EXECUTION.value, execution_result)

        # 5. DNA 链追加
        self.dna_chain.append(dna)

        # 6. 发布事件
        event = Event(
            type=EventType.RUNTIME,
            source="skill_runtime",
            dna=dna,
            timestamp=datetime.now().isoformat(),
            payload={"skill": skill_name, "result": execution_result},
            severity=AuditColor.GREEN,
        )
        self.event_bus.publish(event)

        return {"success": True, "result": execution_result, "dna": dna}

    def get_dna_chain(self) -> List[str]:
        """获取 DNA 链"""
        return self.dna_chain


# ════════════════════════════════════════════════════════
# 示例与测试
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🐉 CNSH 技能系统 v2.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-CNSH-SKILLS-v2.0")
    print("="*60 + "\n")

    # 初始化运行时
    runtime = CNSHSkillRuntime()

    # 测试 1: 基本技能执行
    print("📍 测试 1: 基本技能执行")
    result = runtime.execute_skill(
        "test_skill",
        {"text": "测试输入", "state": {"mode": "test"}}
    )
    print(f"   结果: {result['success']}")
    print(f"   DNA: {result['dna']}\n")

    # 测试 2: 查看 DNA 链
    print("📍 测试 2: DNA 链追踪")
    dna_chain = runtime.get_dna_chain()
    for dna in dna_chain:
        print(f"   → {dna}")
    print()

    # 测试 3: 事件发布
    print("📍 测试 3: 事件总线")
    def event_handler(event: Event):
        print(f"   📢 收到事件: {event.type.value} from {event.source}")

    runtime.event_bus.subscribe(EventType.RUNTIME.value, event_handler)
    event = Event(
        type=EventType.RUNTIME,
        source="test",
        dna="#龍芯⚡️2026-05-25-TEST",
        timestamp=datetime.now().isoformat(),
        payload={"test": True},
        severity=AuditColor.GREEN,
    )
    runtime.event_bus.publish(event)
    print()

    print("="*60)
    print("✅ 技能系统初始化完成")
    print("="*60 + "\n")
    print("🐉 龍魂技能 · 本地执行 · 永不外送 · UID9622不免责")
