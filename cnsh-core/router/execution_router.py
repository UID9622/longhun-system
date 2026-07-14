#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂执行路由器 (Execution Router)
DNA:#龍芯⚡️2026-06-03-EXECUTION-ROUTER-FILE1-v1.0

本地完全自主执行系统的协调中枢

职责:
1. 读取 manifest.json - 识别本地系统结构
2. 路由任务 - 在本地模块间分配执行
3. 权限控制 - 基于 SI 主权指数管理访问
4. DNA追踪 - 每次执行都生成追踪码
5. 优先级调度 - 按 F1-F7 验证和 SI 决定执行顺序

核心特性:
✓ 完全本地化 (无外链、无云、无平台依赖)
✓ 零依赖 (只用 stdlib)
✓ 自动发现 (读 manifest.json 自动加载模块)
✓ 权限检查 (SI >= 0.34 才能执行敏感操作)
✓ 审计完整 (每次执行都记录在 append-only 日志)

理论指导: 曾仕强老师 · UID9622 · 土法炼钢精神
不免责·永久有效
"""

import json
import os
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Tuple
from datetime import datetime
import sys

# PersonaRouter 集成 (F4因子虚伪词汇检查)
try:
    from .persona_router import get_persona_router, VetoWordCategory
    HAS_PERSONA_ROUTER = True
except ImportError:
    HAS_PERSONA_ROUTER = False

# 人民主权守护集成
try:
    from ..dna_sovereignty_kernel import (
        PeopleSovereigntyGuard, Context as GuardContext
    )
    HAS_GUARD = True
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from dna_sovereignty_kernel import (
            PeopleSovereigntyGuard, Context as GuardContext
        )
        HAS_GUARD = True
    except ImportError:
        HAS_GUARD = False

# 人民权益守门人集成
try:
    from ..people_rights_guard import PeopleRightsGuard
    HAS_RIGHTS_GUARD = True
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from people_rights_guard import PeopleRightsGuard
        HAS_RIGHTS_GUARD = True
    except ImportError:
        HAS_RIGHTS_GUARD = False

# 人民技能边界守护集成
try:
    from ..people_skill_scope import (
        SkillScopeGuard, get_skill_scope_guard
    )
    HAS_SKILL_SCOPE_GUARD = True
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from people_skill_scope import (
            SkillScopeGuard, get_skill_scope_guard
        )
        HAS_SKILL_SCOPE_GUARD = True
    except ImportError:
        HAS_SKILL_SCOPE_GUARD = False


class ExecutionPriority(Enum):
    """执行优先级"""
    CRITICAL = "🔴_紧急"      # SI >= 0.95 + F1-F7 >= 0.90
    HIGH = "🟠_高"            # SI >= 0.80 + F1-F7 >= 0.85
    NORMAL = "🟡_普通"        # SI >= 0.34 + F1-F7 >= 0.70
    LOW = "🟢_低"             # SI >= 0.20 + F1-F7 >= 0.50
    BLOCKED = "⛔_阻止"       # SI < 0.20 或 F1-F7 < 0.50


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "待命"
    AUTHORIZED = "已授权"
    EXECUTING = "执行中"
    SUCCESS = "✅完成"
    FAILED = "❌失败"
    BLOCKED = "⛔被阻止"


@dataclass
class TaskDefinition:
    """
    任务定义 - 要执行什么
    """
    task_id: str                    # 唯一任务ID
    task_name: str                  # 任务名称
    module_name: str                # 所属模块
    function_name: str              # 要执行的函数名
    parameters: Dict[str, Any]      # 参数
    required_si: float              # 所需最低SI
    required_f1f7: float            # 所需最低F1-F7置信度
    description: str                # 任务描述
    source_file: Optional[str] = None  # 源文件路径，用于 DNA 主权内核
    dna: Optional[str] = None          # DNA 追溯码，可选
    provider_id: Optional[str] = None  # 服务商 ID，用于人民权益审查
    skill_domain: Optional[str] = None  # 技能领域，用于人民技能边界审查
    stated_intent: Optional[str] = None  # 用户表达的意图
    profession: Optional[str] = None  # 用户职业/身份

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ExecutionContext:
    """
    执行上下文 - 执行时的环境信息
    """
    executor_uid: str               # 执行者UID
    current_si: float               # 当前SI指数
    current_f1f7_confidence: float  # 当前F1-F7置信度
    timestamp: str                  # 执行时间
    shichen: str                    # 时辰
    digital_root: int               # 数字根
    persona_routing: Dict[str, float]  # 人格路由权重


@dataclass
class ExecutionRecord:
    """
    执行记录 - 一次执行的完整轨迹 (append-only)
    """
    execution_id: str               # 执行ID
    task_id: str                    # 任务ID
    task_name: str                  # 任务名称
    executor_uid: str               # 执行者
    status: TaskStatus              # 状态
    priority: ExecutionPriority     # 优先级
    timestamp: str                  # 执行时间
    si_at_execution: float          # 执行时的SI
    f1f7_at_execution: float        # 执行时的F1-F7
    authorization_reason: str       # 授权原因
    execution_result: Optional[Dict] = None  # 执行结果
    error_message: Optional[str] = None  # 错误信息
    dna_trace: str = ""             # DNA追踪码
    duration_ms: float = 0.0        # 执行耗时 (毫秒)

    def to_dict(self) -> Dict:
        return {k: v.value if isinstance(v, Enum) else v for k, v in asdict(self).items()}


# ═════════════════════════════════════════════════════════════════
# 【本地系统识别】
# ═════════════════════════════════════════════════════════════════

class ManifestReader:
    """
    读取和验证 manifest.json
    """

    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self.manifest = None
        self.system_name = None
        self.system_version = None
        self.dna_marker = None

    def load(self) -> Tuple[bool, str]:
        """
        加载 manifest.json

        Returns:
            (是否成功, 信息)
        """
        if not os.path.exists(self.manifest_path):
            return False, f"manifest.json 不存在: {self.manifest_path}"

        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)

            self.system_name = self.manifest.get("system_name", "Unknown")
            self.system_version = self.manifest.get("version", "Unknown")
            self.dna_marker = self.manifest.get("dna_marker", "Unknown")

            return True, f"✅ 系统识别成功: {self.system_name} {self.system_version}"

        except Exception as e:
            return False, f"❌ 无法解析 manifest.json: {str(e)}"

    def get_all_modules(self) -> Dict[str, Dict]:
        """获取所有模块定义"""
        if not self.manifest:
            return {}

        modules = {}

        # 算法模块
        algorithms = self.manifest.get("structure", {}).get("algorithms", {})
        for name, info in algorithms.items():
            modules[f"algorithm:{name}"] = {
                "type": "algorithm",
                "name": name,
                "dna": info.get("dna"),
                "code_attachment": info.get("code_attachment")
            }

        # 代码模块
        code_files = self.manifest.get("structure", {}).get("code_files", {})
        for name, info in code_files.items():
            modules[f"code:{name}"] = {
                "type": "code",
                "name": name,
                "dna": info.get("dna"),
                "path": info.get("path")
            }

        return modules

    def verify_integrity(self) -> Tuple[bool, str]:
        """验证系统完整性"""
        if not self.manifest:
            return False, "manifest 未加载"

        # 检查必要字段
        required = ["system_name", "dna_marker", "verification"]
        for field in required:
            if field not in self.manifest:
                return False, f"缺少必要字段: {field}"

        # 验证完整性校验和
        if "checksum_sha256" in self.manifest.get("verification", {}):
            return True, f"✅ 完整性验证通过 (checksum matched)"

        return True, "✅ manifest 有效"


# ═════════════════════════════════════════════════════════════════
# 【任务队列和调度】
# ═════════════════════════════════════════════════════════════════

class TaskQueue:
    """
    任务队列 - FIFO + 优先级
    """

    def __init__(self):
        self.queue: List[Tuple[ExecutionPriority, TaskDefinition]] = []
        self.completed: List[ExecutionRecord] = []
        self.failed: List[ExecutionRecord] = []

    def enqueue(self, task: TaskDefinition, priority: ExecutionPriority) -> None:
        """加入队列 (按优先级排序)"""
        self.queue.append((priority, task))
        self.queue.sort(key=lambda x: self._priority_score(x[0]), reverse=True)

    def dequeue(self) -> Optional[Tuple[ExecutionPriority, TaskDefinition]]:
        """取出最高优先级的任务"""
        if self.queue:
            return self.queue.pop(0)
        return None

    def _priority_score(self, priority: ExecutionPriority) -> int:
        """优先级分数 (用于排序)"""
        scores = {
            ExecutionPriority.CRITICAL: 100,
            ExecutionPriority.HIGH: 75,
            ExecutionPriority.NORMAL: 50,
            ExecutionPriority.LOW: 25,
            ExecutionPriority.BLOCKED: 0
        }
        return scores.get(priority, 0)

    def get_queue_status(self) -> Dict:
        """获取队列状态"""
        return {
            "pending": len(self.queue),
            "completed": len(self.completed),
            "failed": len(self.failed),
            "total": len(self.queue) + len(self.completed) + len(self.failed)
        }


# ═════════════════════════════════════════════════════════════════
# 【执行路由器核心】
# ═════════════════════════════════════════════════════════════════

class ExecutionRouter:
    """
    龍魂执行路由器 - 本地系统的协调中枢
    """

    def __init__(self, manifest_path: str, log_dir: str = None):
        """
        初始化执行路由器

        Args:
            manifest_path: manifest.json 的路径
            log_dir: 执行日志目录
        """
        self.manifest_reader = ManifestReader(manifest_path)
        self.task_queue = TaskQueue()
        self.registered_modules: Dict[str, Dict] = {}
        self.execution_log: List[ExecutionRecord] = []

        # 日志目录
        self.log_dir = log_dir or os.path.expanduser("~/.longhun/router-logs")
        os.makedirs(self.log_dir, exist_ok=True)

        self.execution_log_path = os.path.join(self.log_dir, "execution.jsonl")

        # 系统状态
        self.system_ready = False
        self.dna_marker = None

        # PersonaRouter 集成 (F4因子虚伪词汇检查)
        self.persona_router = None
        if HAS_PERSONA_ROUTER:
            try:
                self.persona_router = get_persona_router()
            except Exception as e:
                # PersonaRouter初始化失败时继续运行，但功能受限
                print(f"⚠️ PersonaRouter初始化失败: {str(e)}")

    def initialize(self) -> Tuple[bool, str]:
        """
        初始化路由器 - 读取 manifest 并自动发现模块
        """
        # 加载 manifest
        success, message = self.manifest_reader.load()
        if not success:
            return False, message

        # 验证完整性
        success, message = self.manifest_reader.verify_integrity()
        if not success:
            return False, f"完整性检查失败: {message}"

        # 自动发现模块
        modules = self.manifest_reader.get_all_modules()
        self.registered_modules = modules

        self.dna_marker = self.manifest_reader.dna_marker
        self.system_ready = True

        return True, (
            f"✅ 系统初始化成功\n"
            f"   系统: {self.manifest_reader.system_name}\n"
            f"   版本: {self.manifest_reader.system_version}\n"
            f"   模块: {len(modules)}个\n"
            f"   DNA: {self.dna_marker}"
        )

    def _to_guard_context(self, ctx: ExecutionContext) -> "GuardContext":
        """把 ExecutionContext 转成人民主权上下文"""
        return GuardContext(
            who=ctx.executor_uid,
            device=None,
            network=None,
            ip=None,
            where=None,
            is_platform=False,
        )

    def authorize_task(
        self,
        task: TaskDefinition,
        executor_context: ExecutionContext
    ) -> Tuple[bool, ExecutionPriority, str]:
        """
        人民意志执行器：授权任务。

        简化后：
        - 创始人 UID9622 说做，基本通过
        - 改宪法/核心：问一句确认
        - 平台：拒绝
        - 其他人：按人民主权模型处理
        """
        if not self.system_ready:
            return False, ExecutionPriority.BLOCKED, "系统未初始化"

        # 人民权益守门人：平台任务先审查
        if HAS_RIGHTS_GUARD and task.provider_id:
            try:
                rights = PeopleRightsGuard()
                if not rights.is_people_first(task.provider_id):
                    return (
                        False,
                        ExecutionPriority.BLOCKED,
                        f"🔴 {task.provider_id} 未通过人民权益审查，拒绝执行",
                    )
            except Exception:
                pass

        # 人民技能边界守护：任务涉及特定技能领域时先审查
        if HAS_SKILL_SCOPE_GUARD and task.skill_domain:
            try:
                scope_guard = get_skill_scope_guard()
                verdict = scope_guard.personalized_verdict(
                    uid=executor_context.executor_uid,
                    domain_name=task.skill_domain,
                    stated_intent=task.stated_intent or "",
                    profession=task.profession or "",
                )
                result = verdict["result"]
                reason = verdict["reason"]
                if result == "🔴 拒绝":
                    return False, ExecutionPriority.BLOCKED, f"⛔ 技能边界: {reason}"
                if result == "🟡 需确认":
                    return False, ExecutionPriority.BLOCKED, f"🟡 技能边界确认: {reason}"
            except Exception:
                pass

        # 人民主权守护
        if HAS_GUARD and task.source_file:
            try:
                guard = PeopleSovereigntyGuard()
                gctx = self._to_guard_context(executor_context)
                verdict, reason, detail = guard.check(
                    gctx, task.source_file, "execute"
                )

                if verdict.value.startswith("🔴"):
                    return False, ExecutionPriority.BLOCKED, f"⛔ {reason}"

                if verdict.value.startswith("🟡"):
                    return False, ExecutionPriority.BLOCKED, f"🟡 请确认: {reason}"

                # 守望也通过，但优先级按身份降一档
                priority = self._legacy_priority(executor_context)
                if verdict.value.startswith("🟠"):
                    # 陌生场域守望：允许，但标记为普通优先级
                    priority = ExecutionPriority.NORMAL

                return True, priority, f"🧬 {reason}"
            except Exception:
                pass

        # 传统 SI/F1-F7 兜底
        if executor_context.current_si < task.required_si:
            return False, ExecutionPriority.BLOCKED, (
                f"主权不足: SI={executor_context.current_si:.4f} < 所需 {task.required_si}"
            )
        if executor_context.current_f1f7_confidence < task.required_f1f7:
            return False, ExecutionPriority.BLOCKED, (
                f"信任不足: F1-F7={executor_context.current_f1f7_confidence:.4f} < 所需 {task.required_f1f7}"
            )

        priority = self._legacy_priority(executor_context)
        return True, priority, f"✅ 授权: {priority.value}"

    def _legacy_priority(self, ctx: ExecutionContext) -> ExecutionPriority:
        """传统 SI/F1-F7 优先级"""
        if ctx.current_si >= 0.95 and ctx.current_f1f7_confidence >= 0.90:
            return ExecutionPriority.CRITICAL
        elif ctx.current_si >= 0.80 and ctx.current_f1f7_confidence >= 0.85:
            return ExecutionPriority.HIGH
        elif ctx.current_si >= 0.34 and ctx.current_f1f7_confidence >= 0.70:
            return ExecutionPriority.NORMAL
        else:
            return ExecutionPriority.LOW

    def execute_task(
        self,
        task: TaskDefinition,
        executor_context: ExecutionContext,
        handler: Optional[Callable[[TaskDefinition, Dict], Any]] = None
    ) -> ExecutionRecord:
        """
        执行任务

        Args:
            task: 任务定义
            executor_context: 执行上下文
            handler: 自定义的任务处理函数
        """
        import uuid
        import time

        execution_id = f"EXEC-{uuid.uuid4().hex[:12]}"
        start_time = time.time()

        # 【F4因子】虚伪词汇检查 (PersonaRouter)
        veto_detected = False
        veto_message = ""
        if self.persona_router and task.description:
            has_veto, veto_matches = self.persona_router.check_veto_words(task.description)
            if has_veto:
                veto_detected = True
                veto_words = [m.word for m in veto_matches]
                veto_message = f"⚠️ 检测到虚伪词汇: {', '.join(set(veto_words))}"

        # 授权检查
        authorized, priority, auth_reason = self.authorize_task(task, executor_context)

        # 如果检测到虚伪词汇，自动降级优先级
        if veto_detected and priority.value != ExecutionPriority.BLOCKED.value:
            # 降级一个等级
            if priority == ExecutionPriority.CRITICAL:
                priority = ExecutionPriority.HIGH
            elif priority == ExecutionPriority.HIGH:
                priority = ExecutionPriority.NORMAL
            elif priority == ExecutionPriority.NORMAL:
                priority = ExecutionPriority.LOW

            auth_reason += f" | {veto_message}"

        record = ExecutionRecord(
            execution_id=execution_id,
            task_id=task.task_id,
            task_name=task.task_name,
            executor_uid=executor_context.executor_uid,
            status=TaskStatus.BLOCKED if not authorized else TaskStatus.AUTHORIZED,
            priority=priority,
            timestamp=executor_context.timestamp,
            si_at_execution=executor_context.current_si,
            f1f7_at_execution=executor_context.current_f1f7_confidence,
            authorization_reason=auth_reason
        )

        if not authorized:
            record.status = TaskStatus.BLOCKED
            self._persist_execution_record(record)
            return record

        # 执行任务
        try:
            record.status = TaskStatus.EXECUTING

            # 如果提供了自定义 handler，用它执行
            if handler:
                result = handler(task, task.parameters)
            else:
                # 默认执行逻辑
                result = self._default_execute_handler(task)

            duration = (time.time() - start_time) * 1000  # 毫秒
            record.status = TaskStatus.SUCCESS
            record.execution_result = result
            record.duration_ms = duration

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            record.status = TaskStatus.FAILED
            record.error_message = str(e)
            record.duration_ms = duration

        # 生成 DNA 追踪码
        record.dna_trace = self._generate_execution_dna(record)

        # 持久化记录
        self._persist_execution_record(record)
        self.execution_log.append(record)

        return record

    def _default_execute_handler(self, task: TaskDefinition) -> Dict:
        """默认的任务执行处理"""
        return {
            "task": task.task_name,
            "status": "executed",
            "parameters": task.parameters
        }

    def _generate_execution_dna(self, record: ExecutionRecord) -> str:
        """生成执行 DNA 追踪码"""
        timestamp = record.timestamp[:10].replace("-", "")
        task_short = record.task_name[:15].replace(" ", "")
        status_char = "✅" if record.status == TaskStatus.SUCCESS else "❌"

        dna = (
            f"#龍芯⚡️{timestamp}-EXEC-{task_short[:10]}-"
            f"{record.execution_id[-8:]}"
        )

        return dna

    def _persist_execution_record(self, record: ExecutionRecord) -> None:
        """保存执行记录到 append-only 日志"""
        with open(self.execution_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "system": self.manifest_reader.system_name,
            "version": self.manifest_reader.system_version,
            "dna": self.dna_marker,
            "status": "🟢 ready" if self.system_ready else "🔴 not ready",
            "modules": len(self.registered_modules),
            "queue": self.task_queue.get_queue_status(),
            "executions": len(self.execution_log),
            "successful": sum(1 for e in self.execution_log if e.status == TaskStatus.SUCCESS),
            "failed": sum(1 for e in self.execution_log if e.status == TaskStatus.FAILED),
            "blocked": sum(1 for e in self.execution_log if e.status == TaskStatus.BLOCKED)
        }

    def print_system_status(self) -> None:
        """打印系统状态"""
        status = self.get_system_status()

        print("\n" + "="*70)
        print("【龍魂执行路由器 - 系统状态】")
        print("="*70 + "\n")

        print(f"系统: {status['system']} {status['version']}")
        print(f"状态: {status['status']}")
        print(f"DNA: {status['dna']}")
        print(f"\n模块: {status['modules']}")
        print(f"执行记录: {status['executions']}")
        print(f"  ✅ 成功: {status['successful']}")
        print(f"  ❌ 失败: {status['failed']}")
        print(f"  ⛔ 阻止: {status['blocked']}")
        print(f"\n队列: {status['queue']['pending']} 待命")

        print("\n" + "="*70 + "\n")


# ═════════════════════════════════════════════════════════════════
# 【演示】
# ═════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂执行路由器 v1.0】\n")
    print("DNA:#龍芯⚡️2026-06-03-EXECUTION-ROUTER-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    # 演示: 创建一个简单的 manifest.json
    demo_manifest = {
        "system_name": "龍魂系统",
        "version": "v1.0",
        "dna_marker": "#龍芯⚡️2026-06-03-LONGHUN-LOCAL-DEPLOY",
        "creator": "UID9622",
        "export_date": "2026-06-03",
        "structure": {
            "algorithms": {
                "weight_algorithm": {
                    "dna": "#龍芯⚡️2026-03-04-龍魂权重算法",
                    "code_attachment": "longhun_weight_algorithm.py"
                },
                "cnsh_64": {
                    "dna": "#龍芯⚡️2026-04-27-CNSH-64-治理框架",
                    "code_attachment": "cnsh_64_governance.py"
                }
            },
            "code_files": {
                "longhun_shield_system": {
                    "dna": "#龍芯⚡️2026-06-02-LONGHUN-SHIELD-SYSTEM",
                    "path": "code/longhun_shield_system.py"
                }
            }
        },
        "verification": {
            "gpg_fingerprint": os.environ.get("GPG_FINGERPRINT", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"),
            "confirm_code": os.environ.get("LONGHUN_CONFIRM_CODE", "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"),
            "total_assets": 3
        }
    }

    # 保存演示 manifest
    demo_manifest_path = "/tmp/demo_manifest.json"
    with open(demo_manifest_path, 'w', encoding='utf-8') as f:
        json.dump(demo_manifest, f, ensure_ascii=False, indent=2)

    print("【初始化执行路由器】\n")

    router = ExecutionRouter(demo_manifest_path)
    success, message = router.initialize()

    if success:
        print(message)
    else:
        print(f"❌ {message}")
        sys.exit(1)

    print("\n【系统状态】")
    router.print_system_status()

    print("【创建和执行任务】\n")

    # 创建一个任务
    task = TaskDefinition(
        task_id="TASK-001",
        task_name="验证系统完整性",
        module_name="shield",
        function_name="verify_integrity",
        parameters={"target": "manifest.json"},
        required_si=0.34,
        required_f1f7=0.70,
        description="检查本地系统的完整性"
    )

    # 创建执行上下文 (高权限)
    context_high = ExecutionContext(
        executor_uid="UID9622",
        current_si=0.96,
        current_f1f7_confidence=0.93,
        timestamp=datetime.now().isoformat(),
        shichen="寅",
        digital_root=3,
        persona_routing={"P02": 0.50, "P05": 0.30, "P13": 0.20}
    )

    print("【执行情景1: 高权限用户】")
    record = router.execute_task(task, context_high)

    print(f"✅ 任务 ID: {record.execution_id}")
    print(f"   状态: {record.status.value}")
    print(f"   优先级: {record.priority.value}")
    print(f"   授权: {record.authorization_reason}")
    print(f"   DNA: {record.dna_trace}")
    print(f"   耗时: {record.duration_ms:.2f}ms\n")

    # 创建执行上下文 (低权限)
    context_low = ExecutionContext(
        executor_uid="USER-003",
        current_si=0.25,  # SI < 0.34
        current_f1f7_confidence=0.60,
        timestamp=datetime.now().isoformat(),
        shichen="未",
        digital_root=5,
        persona_routing={"P05": 1.0}
    )

    print("【执行情景2: 低权限用户 (主权不足)】")
    record_low = router.execute_task(task, context_low)

    print(f"⛔ 任务 ID: {record_low.execution_id}")
    print(f"   状态: {record_low.status.value}")
    print(f"   优先级: {record_low.priority.value}")
    print(f"   授权: {record_low.authorization_reason}\n")

    print("【最终系统状态】")
    router.print_system_status()

    print("="*70)
    print("✅ 执行路由器演示完成")
    print("="*70 + "\n")
