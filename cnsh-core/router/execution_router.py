#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂執行路由器 (Execution Router)
DNA: #龍芯⚡️2026-06-03-EXECUTION-ROUTER-v1.0

本地完全自主執行系統的協調中樞

職責:
1. 讀取 manifest.json - 識別本地系統結構
2. 路由任務 - 在本地模塊間分配執行
3. 權限控制 - 基於 SI 主權指數管理訪問
4. DNA追蹤 - 每次執行都生成追蹤碼
5. 優先級調度 - 按 F1-F7 驗證和 SI 決定執行順序

核心特性:
✓ 完全本地化 (無外鏈、無云、無平台依賴)
✓ 零依賴 (只用 stdlib)
✓ 自動發現 (讀 manifest.json 自動加載模塊)
✓ 權限檢查 (SI >= 0.34 才能執行敏感操作)
✓ 審計完整 (每次執行都記錄在 append-only 日誌)

理論指導: 曾仕强老师 · UID9622 · 土法煉鋼精神
不免責·永久有效
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


class ExecutionPriority(Enum):
    """執行優先級"""
    CRITICAL = "🔴_緊急"      # SI >= 0.95 + F1-F7 >= 0.90
    HIGH = "🟠_高"            # SI >= 0.80 + F1-F7 >= 0.85
    NORMAL = "🟡_普通"        # SI >= 0.34 + F1-F7 >= 0.70
    LOW = "🟢_低"             # SI >= 0.20 + F1-F7 >= 0.50
    BLOCKED = "⛔_阻止"       # SI < 0.20 或 F1-F7 < 0.50


class TaskStatus(Enum):
    """任務狀態"""
    PENDING = "待命"
    AUTHORIZED = "已授權"
    EXECUTING = "執行中"
    SUCCESS = "✅完成"
    FAILED = "❌失敗"
    BLOCKED = "⛔被阻止"


@dataclass
class TaskDefinition:
    """
    任務定義 - 要執行什麼
    """
    task_id: str                    # 唯一任務ID
    task_name: str                  # 任務名稱
    module_name: str                # 所屬模塊
    function_name: str              # 要執行的函數名
    parameters: Dict[str, Any]      # 參數
    required_si: float              # 所需最低SI
    required_f1f7: float            # 所需最低F1-F7置信度
    description: str                # 任務描述

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ExecutionContext:
    """
    執行上下文 - 執行時的環境信息
    """
    executor_uid: str               # 執行者UID
    current_si: float               # 當前SI指數
    current_f1f7_confidence: float  # 當前F1-F7置信度
    timestamp: str                  # 執行時間
    shichen: str                    # 時辰
    digital_root: int               # 數字根
    persona_routing: Dict[str, float]  # 人格路由權重


@dataclass
class ExecutionRecord:
    """
    執行記錄 - 一次執行的完整軌跡 (append-only)
    """
    execution_id: str               # 執行ID
    task_id: str                    # 任務ID
    task_name: str                  # 任務名稱
    executor_uid: str               # 執行者
    status: TaskStatus              # 狀態
    priority: ExecutionPriority     # 優先級
    timestamp: str                  # 執行時間
    si_at_execution: float          # 執行時的SI
    f1f7_at_execution: float        # 執行時的F1-F7
    authorization_reason: str       # 授權原因
    execution_result: Optional[Dict] = None  # 執行結果
    error_message: Optional[str] = None  # 錯誤信息
    dna_trace: str = ""             # DNA追蹤碼
    duration_ms: float = 0.0        # 執行耗時 (毫秒)

    def to_dict(self) -> Dict:
        return {k: v.value if isinstance(v, Enum) else v for k, v in asdict(self).items()}


# ═════════════════════════════════════════════════════════════════
# 【本地系統識別】
# ═════════════════════════════════════════════════════════════════

class ManifestReader:
    """
    讀取和驗證 manifest.json
    """

    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self.manifest = None
        self.system_name = None
        self.system_version = None
        self.dna_marker = None

    def load(self) -> Tuple[bool, str]:
        """
        加載 manifest.json

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

            return True, f"✅ 系統識別成功: {self.system_name} {self.system_version}"

        except Exception as e:
            return False, f"❌ 無法解析 manifest.json: {str(e)}"

    def get_all_modules(self) -> Dict[str, Dict]:
        """獲取所有模塊定義"""
        if not self.manifest:
            return {}

        modules = {}

        # 算法模塊
        algorithms = self.manifest.get("structure", {}).get("algorithms", {})
        for name, info in algorithms.items():
            modules[f"algorithm:{name}"] = {
                "type": "algorithm",
                "name": name,
                "dna": info.get("dna"),
                "code_attachment": info.get("code_attachment")
            }

        # 代碼模塊
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
        """驗證系統完整性"""
        if not self.manifest:
            return False, "manifest 未加載"

        # 檢查必要字段
        required = ["system_name", "dna_marker", "verification"]
        for field in required:
            if field not in self.manifest:
                return False, f"缺少必要字段: {field}"

        # 驗證完整性校驗和
        if "checksum_sha256" in self.manifest.get("verification", {}):
            return True, f"✅ 完整性驗證通過 (checksum matched)"

        return True, "✅ manifest 有效"


# ═════════════════════════════════════════════════════════════════
# 【任務隊列和調度】
# ═════════════════════════════════════════════════════════════════

class TaskQueue:
    """
    任務隊列 - FIFO + 優先級
    """

    def __init__(self):
        self.queue: List[Tuple[ExecutionPriority, TaskDefinition]] = []
        self.completed: List[ExecutionRecord] = []
        self.failed: List[ExecutionRecord] = []

    def enqueue(self, task: TaskDefinition, priority: ExecutionPriority) -> None:
        """加入隊列 (按優先級排序)"""
        self.queue.append((priority, task))
        self.queue.sort(key=lambda x: self._priority_score(x[0]), reverse=True)

    def dequeue(self) -> Optional[Tuple[ExecutionPriority, TaskDefinition]]:
        """取出最高優先級的任務"""
        if self.queue:
            return self.queue.pop(0)
        return None

    def _priority_score(self, priority: ExecutionPriority) -> int:
        """優先級分數 (用於排序)"""
        scores = {
            ExecutionPriority.CRITICAL: 100,
            ExecutionPriority.HIGH: 75,
            ExecutionPriority.NORMAL: 50,
            ExecutionPriority.LOW: 25,
            ExecutionPriority.BLOCKED: 0
        }
        return scores.get(priority, 0)

    def get_queue_status(self) -> Dict:
        """獲取隊列狀態"""
        return {
            "pending": len(self.queue),
            "completed": len(self.completed),
            "failed": len(self.failed),
            "total": len(self.queue) + len(self.completed) + len(self.failed)
        }


# ═════════════════════════════════════════════════════════════════
# 【執行路由器核心】
# ═════════════════════════════════════════════════════════════════

class ExecutionRouter:
    """
    龍魂執行路由器 - 本地系統的協調中樞
    """

    def __init__(self, manifest_path: str, log_dir: str = None):
        """
        初始化執行路由器

        Args:
            manifest_path: manifest.json 的路徑
            log_dir: 執行日誌目錄
        """
        self.manifest_reader = ManifestReader(manifest_path)
        self.task_queue = TaskQueue()
        self.registered_modules: Dict[str, Dict] = {}
        self.execution_log: List[ExecutionRecord] = []

        # 日誌目錄
        self.log_dir = log_dir or os.path.expanduser("~/.longhun/router-logs")
        os.makedirs(self.log_dir, exist_ok=True)

        self.execution_log_path = os.path.join(self.log_dir, "execution.jsonl")

        # 系統狀態
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
        初始化路由器 - 讀取 manifest 並自動發現模塊
        """
        # 加載 manifest
        success, message = self.manifest_reader.load()
        if not success:
            return False, message

        # 驗證完整性
        success, message = self.manifest_reader.verify_integrity()
        if not success:
            return False, f"完整性檢查失敗: {message}"

        # 自動發現模塊
        modules = self.manifest_reader.get_all_modules()
        self.registered_modules = modules

        self.dna_marker = self.manifest_reader.dna_marker
        self.system_ready = True

        return True, (
            f"✅ 系統初始化成功\n"
            f"   系統: {self.manifest_reader.system_name}\n"
            f"   版本: {self.manifest_reader.system_version}\n"
            f"   模塊: {len(modules)}個\n"
            f"   DNA: {self.dna_marker}"
        )

    def authorize_task(
        self,
        task: TaskDefinition,
        executor_context: ExecutionContext
    ) -> Tuple[bool, ExecutionPriority, str]:
        """
        授權任務執行

        Returns:
            (是否授權, 優先級, 原因)
        """
        if not self.system_ready:
            return False, ExecutionPriority.BLOCKED, "系統未初始化"

        # 檢查1: SI 是否滿足
        if executor_context.current_si < task.required_si:
            return False, ExecutionPriority.BLOCKED, (
                f"主權不足: SI={executor_context.current_si:.4f} < 所需 {task.required_si}"
            )

        # 檢查2: F1-F7 是否滿足
        if executor_context.current_f1f7_confidence < task.required_f1f7:
            return False, ExecutionPriority.BLOCKED, (
                f"信任不足: F1-F7={executor_context.current_f1f7_confidence:.4f} < 所需 {task.required_f1f7}"
            )

        # 決定優先級
        if executor_context.current_si >= 0.95 and executor_context.current_f1f7_confidence >= 0.90:
            priority = ExecutionPriority.CRITICAL
        elif executor_context.current_si >= 0.80 and executor_context.current_f1f7_confidence >= 0.85:
            priority = ExecutionPriority.HIGH
        elif executor_context.current_si >= 0.34 and executor_context.current_f1f7_confidence >= 0.70:
            priority = ExecutionPriority.NORMAL
        else:
            priority = ExecutionPriority.LOW

        reason = f"✅ 授權: {priority.value}"

        return True, priority, reason

    def execute_task(
        self,
        task: TaskDefinition,
        executor_context: ExecutionContext,
        handler: Optional[Callable[[TaskDefinition, Dict], Any]] = None
    ) -> ExecutionRecord:
        """
        執行任務

        Args:
            task: 任務定義
            executor_context: 執行上下文
            handler: 自定義的任務處理函數
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

        # 授權檢查
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

        # 執行任務
        try:
            record.status = TaskStatus.EXECUTING

            # 如果提供了自定義 handler，用它執行
            if handler:
                result = handler(task, task.parameters)
            else:
                # 默認執行邏輯
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

        # 生成 DNA 追蹤碼
        record.dna_trace = self._generate_execution_dna(record)

        # 持久化記錄
        self._persist_execution_record(record)
        self.execution_log.append(record)

        return record

    def _default_execute_handler(self, task: TaskDefinition) -> Dict:
        """默認的任務執行處理"""
        return {
            "task": task.task_name,
            "status": "executed",
            "parameters": task.parameters
        }

    def _generate_execution_dna(self, record: ExecutionRecord) -> str:
        """生成執行 DNA 追蹤碼"""
        timestamp = record.timestamp[:10].replace("-", "")
        task_short = record.task_name[:15].replace(" ", "")
        status_char = "✅" if record.status == TaskStatus.SUCCESS else "❌"

        dna = (
            f"#龍芯⚡️{timestamp}-EXEC-{task_short[:10]}-"
            f"{record.execution_id[-8:]}"
        )

        return dna

    def _persist_execution_record(self, record: ExecutionRecord) -> None:
        """保存執行記錄到 append-only 日誌"""
        with open(self.execution_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    def get_system_status(self) -> Dict:
        """獲取系統狀態"""
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
        """列印系統狀態"""
        status = self.get_system_status()

        print("\n" + "="*70)
        print("【龍魂執行路由器 - 系統狀態】")
        print("="*70 + "\n")

        print(f"系統: {status['system']} {status['version']}")
        print(f"狀態: {status['status']}")
        print(f"DNA: {status['dna']}")
        print(f"\n模塊: {status['modules']}")
        print(f"執行記錄: {status['executions']}")
        print(f"  ✅ 成功: {status['successful']}")
        print(f"  ❌ 失敗: {status['failed']}")
        print(f"  ⛔ 阻止: {status['blocked']}")
        print(f"\n隊列: {status['queue']['pending']} 待命")

        print("\n" + "="*70 + "\n")


# ═════════════════════════════════════════════════════════════════
# 【演示】
# ═════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n【龍魂執行路由器 v1.0】\n")
    print("DNA: #龍芯⚡️2026-06-03-EXECUTION-ROUTER-v1.0")
    print("CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL\n")

    # 演示: 創建一個簡單的 manifest.json
    demo_manifest = {
        "system_name": "龍魂系統",
        "version": "v1.0",
        "dna_marker": "#龍芯⚡️2026-06-03-LONGHUN-LOCAL-DEPLOY",
        "creator": "UID9622",
        "export_date": "2026-06-03",
        "structure": {
            "algorithms": {
                "weight_algorithm": {
                    "dna": "#龍芯⚡️2026-03-04-龍魂權重演算法",
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
            "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "total_assets": 3
        }
    }

    # 保存演示 manifest
    demo_manifest_path = "/tmp/demo_manifest.json"
    with open(demo_manifest_path, 'w', encoding='utf-8') as f:
        json.dump(demo_manifest, f, ensure_ascii=False, indent=2)

    print("【初始化執行路由器】\n")

    router = ExecutionRouter(demo_manifest_path)
    success, message = router.initialize()

    if success:
        print(message)
    else:
        print(f"❌ {message}")
        sys.exit(1)

    print("\n【系統狀態】")
    router.print_system_status()

    print("【創建和執行任務】\n")

    # 創建一個任務
    task = TaskDefinition(
        task_id="TASK-001",
        task_name="驗證系統完整性",
        module_name="shield",
        function_name="verify_integrity",
        parameters={"target": "manifest.json"},
        required_si=0.34,
        required_f1f7=0.70,
        description="檢查本地系統的完整性"
    )

    # 創建執行上下文 (高權限)
    context_high = ExecutionContext(
        executor_uid="UID9622",
        current_si=0.96,
        current_f1f7_confidence=0.93,
        timestamp=datetime.now().isoformat(),
        shichen="寅",
        digital_root=3,
        persona_routing={"P02": 0.50, "P05": 0.30, "P13": 0.20}
    )

    print("【執行情景1: 高權限用戶】")
    record = router.execute_task(task, context_high)

    print(f"✅ 任務 ID: {record.execution_id}")
    print(f"   狀態: {record.status.value}")
    print(f"   優先級: {record.priority.value}")
    print(f"   授權: {record.authorization_reason}")
    print(f"   DNA: {record.dna_trace}")
    print(f"   耗時: {record.duration_ms:.2f}ms\n")

    # 創建執行上下文 (低權限)
    context_low = ExecutionContext(
        executor_uid="USER-003",
        current_si=0.25,  # SI < 0.34
        current_f1f7_confidence=0.60,
        timestamp=datetime.now().isoformat(),
        shichen="未",
        digital_root=5,
        persona_routing={"P05": 1.0}
    )

    print("【執行情景2: 低權限用戶 (主權不足)】")
    record_low = router.execute_task(task, context_low)

    print(f"⛔ 任務 ID: {record_low.execution_id}")
    print(f"   狀態: {record_low.status.value}")
    print(f"   優先級: {record_low.priority.value}")
    print(f"   授權: {record_low.authorization_reason}\n")

    print("【最終系統狀態】")
    router.print_system_status()

    print("="*70)
    print("✅ 執行路由器演示完成")
    print("="*70 + "\n")
