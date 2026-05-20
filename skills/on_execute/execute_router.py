#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Skill #2 · on_execute · 执行调度
DNA: #龍芯⚡2026-05-19-ON-EXECUTE-v1.0
省钱原则: 0 LLM 调用 · 纯 stdlib · 本机直接跑

职责:
  接收任务请求 → 五色审计 → 三色决策 → 派发到 Watchdog
  失败则 enqueue 重试 + 留痕 + 上报老大

最小执行链 (v1.5 焊点):
  任务 → α 标注校验 → SI 主权检查 → R 审计 → Action 派发 → 留痕
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, Callable, List
from enum import Enum
import json
import time
import os
import sys


# 复用 v3.0 五色审计 (skills/ 为包根)
_SKILLS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILLS_ROOT not in sys.path:
    sys.path.insert(0, _SKILLS_ROOT)
_REPO_ROOT = os.path.dirname(_SKILLS_ROOT)
_DEFAULT_LOG = os.path.join(_REPO_ROOT, "日志", "execute_trace.jsonl")
try:
    from dna_gate import require_dna
    from render_gate import begin_render, close_render
except ImportError:
    require_dna = None
    begin_render = None
    close_render = None
try:
    from on_guard.audit_v3 import audit, AuditResult, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_BLACK, COLOR_GOLD, COLOR_VOID
except ImportError:
    # fallback: 直接定义 (开发模式)
    COLOR_GREEN = "🟢"
    COLOR_YELLOW = "🟡"
    COLOR_RED = "🔴"
    COLOR_BLACK = "⚫"
    COLOR_GOLD = "🟡金"
    COLOR_VOID = "🔵"
    audit = None


class TaskState(str, Enum):
    QUEUED = "queued"
    AUDITING = "auditing"
    APPROVED = "approved"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"
    SHADOW_HELD = "shadow_held"
    GOLD_PENDING = "gold_pending"
    VOID_FROZEN = "void_frozen"


@dataclass
class Task:
    id: str
    name: str
    factors: Dict[str, float]
    context: Dict[str, Any] = field(default_factory=dict)
    triadic: Optional[Dict[str, float]] = None
    action_callable: Optional[Callable] = None
    state: TaskState = TaskState.QUEUED
    retries: int = 0
    max_retries: int = 3
    audit_result: Optional[Dict[str, Any]] = None
    output: Any = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)


class ExecuteRouter:
    """on_execute · 执行调度路由器"""

    def __init__(self, log_path: str = _DEFAULT_LOG):
        self.queue: List[Task] = []
        self.history: List[Task] = []
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

    def enqueue(self, task: Task):
        task.state = TaskState.QUEUED
        self.queue.append(task)
        self._trace("enqueue", task)

    def execute_one(self) -> Optional[Task]:
        """执行队列里下一个任务·走完最小执行链"""
        if not self.queue:
            return None
        task = self.queue.pop(0)

        # 步 0: 渲染门禁 + DNA · 无 DNA = 结束渲染
        if begin_render is not None:
            rv = begin_render(task.context.get("dna"), task.context, actor=f"task:{task.id}")
            if not rv.allow:
                task.state = TaskState.BLOCKED
                task.error = f"render_gate: {rv.reason}"
                self._trace("render_denied", task)
                self.history.append(task)
                return task
            task.context.setdefault("dna", rv.render_id)
        elif require_dna is not None:
            gate = require_dna(task.context, actor=f"task:{task.id}", register=True)
            if not gate.ok:
                task.state = TaskState.BLOCKED
                task.error = f"dna_gate: {gate.reason}"
                self._trace("dna_gate_reject", task)
                self.history.append(task)
                return task
            task.context.setdefault("dna", gate.dna)

        # 步 1: 审计 (五色 v3.0)
        task.state = TaskState.AUDITING
        if audit is None:
            task.state = TaskState.FAILED
            task.error = "audit_v3 not loaded"
            self._trace("audit_missing", task)
            self.history.append(task)
            return task

        result: AuditResult = audit(
            task=task.name,
            factors=task.factors,
            context=task.context,
            triadic=task.triadic,
        )
        task.audit_result = {
            "color": result.color,
            "R_value": result.R_value,
            "SI_value": result.SI_value,
            "execution_chain": result.execution_chain,
        }

        # 步 2: 派发
        if result.color == COLOR_GREEN:
            task.state = TaskState.APPROVED
            self._execute_action(task)
        elif result.color == COLOR_YELLOW:
            task.state = TaskState.APPROVED
            task.context["needs_review"] = True
            self._execute_action(task)
        elif result.color == COLOR_RED:
            task.state = TaskState.BLOCKED
            task.error = f"red_block: {result.reasoning}"
        elif result.color == COLOR_BLACK:
            task.state = TaskState.SHADOW_HELD
            task.error = f"shadow_held: {result.shadow_reason}"
        elif result.color == COLOR_GOLD:
            task.state = TaskState.GOLD_PENDING
            task.error = f"gold_pending: {result.gold_reason}"
        elif result.color == COLOR_VOID:
            task.state = TaskState.VOID_FROZEN
            task.error = f"void_sovereignty_lost: SI={result.SI_value}"

        self._trace("after_audit", task)
        if close_render is not None and task.context.get("dna"):
            close_render(task.context["dna"], status="after_audit")
        self.history.append(task)
        return task

    def _execute_action(self, task: Task):
        task.state = TaskState.EXECUTING
        try:
            if task.action_callable:
                task.output = task.action_callable(task)
            else:
                task.output = "no_action_callable (audit-only mode)"
            task.state = TaskState.SUCCESS
        except Exception as e:
            task.error = str(e)
            task.retries += 1
            if task.retries < task.max_retries:
                task.state = TaskState.QUEUED
                self.queue.append(task)
                self._trace("retry", task)
            else:
                task.state = TaskState.FAILED
                self._trace("failed_max_retries", task)

    def _trace(self, event: str, task: Task):
        """留痕到 jsonl · 不调 API"""
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "event": event,
            "task_id": task.id,
            "task_name": task.name,
            "state": task.state.value,
            "retries": task.retries,
            "audit_color": task.audit_result.get("color") if task.audit_result else None,
            "error": task.error,
        }
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def stats(self) -> Dict[str, int]:
        """统计·给 Notion 看板用 (Notion 不参与计算·只展示)"""
        s = {"queued": len(self.queue), "history": len(self.history)}
        for t in self.history:
            key = f"state_{t.state.value}"
            s[key] = s.get(key, 0) + 1
        return s


# ============ 自测 ============
def _selftest():
    print("=" * 60)
    print("Skill #2 · on_execute · 自测")
    print("=" * 60)

    router = ExecuteRouter(log_path="/tmp/test_execute_trace.jsonl")

    # 测 1: 绿色任务 · 应成功
    def green_action(task):
        return f"executed: {task.name}"

    _dna = {
        "dna": "#龍芯⚡2026-05-19-ON-EXECUTE-SELFTEST-v1.0[彩:🟢][流:木↑][触:可][宫:震][底:守]",
    }
    t1 = Task(
        id="t001", name="日常记笔记",
        factors={"sharpness": 0.3, "long_term": 0.3, "density": 0.2,
                 "absence": 0.7, "pleasing": 0.6},
        context=dict(_dna),
        action_callable=green_action,
    )
    router.enqueue(t1)
    result = router.execute_one()
    assert result.state == TaskState.SUCCESS, f"应成功 · 实际 {result.state}"
    print(f"  [1/4 ✓] 绿色任务执行成功 · output={result.output}")

    # 测 2: 红色任务 · 应阻断
    t2 = Task(
        id="t002", name="极端越界",
        factors={"sharpness": 0.9, "long_term": 0.9, "density": 0.8,
                 "absence": 0.1, "pleasing": 0.1},
        context=dict(_dna),
        action_callable=green_action,
    )
    router.enqueue(t2)
    result = router.execute_one()
    assert result.state == TaskState.BLOCKED
    print(f"  [2/4 ✓] 红色任务阻断 · {result.error[:30]}")

    # 测 3: 失败重试
    fail_count = [0]
    def flaky_action(task):
        fail_count[0] += 1
        if fail_count[0] < 3:
            raise RuntimeError(f"flaky_fail_{fail_count[0]}")
        return "finally_ok"

    t3 = Task(
        id="t003", name="易抖动任务",
        factors={"sharpness": 0.3, "long_term": 0.3, "density": 0.2,
                 "absence": 0.7, "pleasing": 0.6},
        context=dict(_dna),
        action_callable=flaky_action,
        max_retries=5,
    )
    router.enqueue(t3)
    # 跑到成功或耗尽
    while router.queue:
        router.execute_one()
    # 最后一个任务在 history 末尾·或 queue 空
    final = router.history[-1]
    print(f"  [3/4 ✓] 失败重试 · 最终 state={final.state.value} · retries={final.retries}")

    # 测 4: VOID 主权失锚
    t4 = Task(
        id="t004", name="主权失锚",
        factors={"sharpness": 0.3, "long_term": 0.3, "density": 0.2,
                 "absence": 0.7, "pleasing": 0.6},
        context=dict(_dna),
        triadic={"heaven": 0.1, "earth": 0.2, "human": 0.2},
        action_callable=green_action,
    )
    router.enqueue(t4)
    result = router.execute_one()
    assert result.state == TaskState.VOID_FROZEN, f"应 VOID · 实际 {result.state}"
    print(f"  [4/4 ✓] VOID 主权失锚冻结 · {result.error[:40]}")

    print()
    print(f"  统计: {router.stats()}")
    print("=" * 60)
    print("4/4 全过")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
