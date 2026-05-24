#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ 算力解约系统 · Compute Liberation System
DNA: #龍芯⚡️2026-05-22-COMPUTE-SCHEDULER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

算力解约系统特性：
1. 任务优先级调度
2. 本地算力池化
3. 反资本化防护（算力不被云厂商垄断）
4. 离线优先策略
5. 智能负载均衡
"""

import hashlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from queue import PriorityQueue
from typing import Callable, Any, Dict, List, Optional


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0    # 紧急任务（立即执行）
    HIGH = 1        # 高优先级
    NORMAL = 2      # 普通优先级
    LOW = 3         # 低优先级
    BACKGROUND = 4  # 后台任务


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(order=True)
class ComputeTask:
    """计算任务"""
    priority: int = field(compare=True)          # 用于PriorityQueue排序
    task_id: str = field(compare=False)
    name: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: Dict[str, Any] = field(default_factory=dict, compare=False)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    result: Any = field(default=None, compare=False)
    error: Optional[str] = field(default=None, compare=False)
    created_at: datetime = field(default_factory=datetime.now, compare=False)
    started_at: Optional[datetime] = field(default=None, compare=False)
    completed_at: Optional[datetime] = field(default=None, compare=False)
    dna: str = field(default="", compare=False)

    def __post_init__(self):
        if not self.task_id:
            ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
            h = hashlib.sha256(f"{ts}|{self.name}".encode()).hexdigest()[:8]
            self.task_id = f"CT-{ts[:14]}-{h}"
        if not self.dna:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            self.dna = f"#龍芯⚡️{ts}-TASK-{self.task_id[-8:]}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "priority": self.priority,
            "status": self.status.value,
            "result": str(self.result) if self.result else None,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": (self.completed_at - self.started_at).total_seconds() * 1000
                if self.completed_at and self.started_at else None,
            "dna": self.dna,
        }


class ComputeScheduler:
    """
    算力调度器

    管理本地算力资源，实现任务调度和负载均衡
    反资本化：优先使用本地算力，避免云厂商垄断
    """

    def __init__(self, max_workers: int = 4):
        """
        初始化调度器

        Args:
            max_workers: 最大并行工作线程数
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue: PriorityQueue = PriorityQueue()
        self.active_tasks: Dict[str, ComputeTask] = {}
        self.completed_tasks: List[ComputeTask] = []
        self.lock = threading.Lock()
        self.running = True

        # 统计
        self.stats = {
            "total_submitted": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_compute_time_ms": 0,
        }

        # 启动调度线程
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._scheduler_thread.start()

    def _scheduler_loop(self):
        """调度循环"""
        while self.running:
            try:
                # 从队列获取任务（非阻塞）
                if not self.task_queue.empty():
                    task = self.task_queue.get_nowait()
                    self._execute_task(task)
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"调度器错误: {e}")
                time.sleep(1)

    def _execute_task(self, task: ComputeTask):
        """执行任务"""
        def run():
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()

            with self.lock:
                self.active_tasks[task.task_id] = task

            try:
                task.result = task.func(*task.args, **task.kwargs)
                task.status = TaskStatus.COMPLETED
                self.stats["total_completed"] += 1
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
                self.stats["total_failed"] += 1
            finally:
                task.completed_at = datetime.now()
                duration = (task.completed_at - task.started_at).total_seconds() * 1000
                self.stats["total_compute_time_ms"] += duration

                with self.lock:
                    if task.task_id in self.active_tasks:
                        del self.active_tasks[task.task_id]
                    self.completed_tasks.append(task)

        # 提交到线程池
        self.executor.submit(run)

    def submit(self,
               func: Callable,
               *args,
               name: str = "unnamed",
               priority: TaskPriority = TaskPriority.NORMAL,
               **kwargs) -> ComputeTask:
        """
        提交任务

        Args:
            func: 要执行的函数
            *args: 函数参数
            name: 任务名称
            priority: 优先级
            **kwargs: 函数关键字参数

        Returns:
            任务对象
        """
        task = ComputeTask(
            priority=priority.value,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            task_id=""  # 自动生成
        )

        self.task_queue.put(task)
        self.stats["total_submitted"] += 1

        return task

    def submit_batch(self,
                     tasks: List[Dict[str, Any]],
                     priority: TaskPriority = TaskPriority.NORMAL) -> List[ComputeTask]:
        """
        批量提交任务

        Args:
            tasks: 任务列表，每个任务是 {"func": callable, "args": tuple, "kwargs": dict, "name": str}
            priority: 统一优先级

        Returns:
            任务对象列表
        """
        submitted = []
        for t in tasks:
            task = self.submit(
                t["func"],
                *t.get("args", ()),
                name=t.get("name", "batch-task"),
                priority=priority,
                **t.get("kwargs", {})
            )
            submitted.append(task)
        return submitted

    def get_task(self, task_id: str) -> Optional[ComputeTask]:
        """获取任务状态"""
        with self.lock:
            if task_id in self.active_tasks:
                return self.active_tasks[task_id]
            for task in self.completed_tasks:
                if task.task_id == task_id:
                    return task
        return None

    def wait(self, task: ComputeTask, timeout: float = None) -> bool:
        """
        等待任务完成

        Args:
            task: 任务对象
            timeout: 超时时间（秒）

        Returns:
            是否在超时前完成
        """
        start = time.time()
        while task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
            if timeout and (time.time() - start) > timeout:
                return False
            time.sleep(0.1)
        return True

    def wait_all(self, tasks: List[ComputeTask], timeout: float = None) -> bool:
        """等待所有任务完成"""
        start = time.time()
        for task in tasks:
            remaining = timeout - (time.time() - start) if timeout else None
            if remaining and remaining <= 0:
                return False
            if not self.wait(task, remaining):
                return False
        return True

    def cancel(self, task_id: str) -> bool:
        """取消任务（仅限PENDING状态）"""
        # 无法直接从PriorityQueue删除，只能标记
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        return False

    def get_active_count(self) -> int:
        """获取活跃任务数"""
        with self.lock:
            return len(self.active_tasks)

    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.task_queue.qsize()

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "active_tasks": self.get_active_count(),
            "queue_size": self.get_queue_size(),
            "completed_tasks": len(self.completed_tasks),
            "max_workers": self.max_workers,
            "avg_compute_time_ms": (
                self.stats["total_compute_time_ms"] / self.stats["total_completed"]
                if self.stats["total_completed"] > 0 else 0
            ),
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-SCHEDULER-STATS"
        }

    def shutdown(self, wait: bool = True):
        """关闭调度器"""
        self.running = False
        self.executor.shutdown(wait=wait)


# 全局实例
_scheduler: Optional[ComputeScheduler] = None


def get_scheduler(max_workers: int = 4) -> ComputeScheduler:
    """获取全局调度器"""
    global _scheduler
    if _scheduler is None:
        _scheduler = ComputeScheduler(max_workers=max_workers)
    return _scheduler


# ========== 反资本化防护函数 ==========

def compute_local(func: Callable, *args, **kwargs) -> Any:
    """
    强制本地计算

    确保计算在本地执行，不上传到云端
    这是反资本化防护的核心：算力归用户所有
    """
    # 直接在本地执行
    return func(*args, **kwargs)


def prefer_local(func: Callable, *args, cloud_fallback: bool = False, **kwargs) -> Any:
    """
    优先本地计算

    尝试本地计算，失败时可选择云端回退
    """
    try:
        return compute_local(func, *args, **kwargs)
    except Exception as e:
        if cloud_fallback:
            # 这里可以实现云端调用
            raise NotImplementedError("云端回退未实现·数据主权优先")
        raise e


if __name__ == "__main__":
    # 测试
    print("⚡ 算力解约系统测试")
    print("=" * 60)

    scheduler = ComputeScheduler(max_workers=4)

    # 测试任务函数
    def heavy_compute(n: int, name: str = "test") -> int:
        """模拟重计算"""
        time.sleep(0.5)  # 模拟计算耗时
        return sum(range(n))

    def quick_task(msg: str) -> str:
        """快速任务"""
        time.sleep(0.1)
        return f"完成: {msg}"

    # 提交不同优先级的任务
    print("📋 提交任务:")
    tasks = []

    t1 = scheduler.submit(heavy_compute, 1000, name="重计算", priority=TaskPriority.LOW)
    print(f"  提交: {t1.name} (优先级: LOW)")
    tasks.append(t1)

    t2 = scheduler.submit(quick_task, "紧急任务", name="紧急", priority=TaskPriority.CRITICAL)
    print(f"  提交: {t2.name} (优先级: CRITICAL)")
    tasks.append(t2)

    t3 = scheduler.submit(heavy_compute, 500, name="普通", priority=TaskPriority.NORMAL)
    print(f"  提交: {t3.name} (优先级: NORMAL)")
    tasks.append(t3)

    print()
    print("⏳ 等待任务完成...")

    # 等待所有任务
    scheduler.wait_all(tasks, timeout=10)

    print()
    print("📊 任务结果:")
    for task in tasks:
        status = "✅" if task.status == TaskStatus.COMPLETED else "❌"
        duration = (task.completed_at - task.started_at).total_seconds() * 1000 if task.completed_at and task.started_at else 0
        print(f"  {status} {task.name}: {task.result} ({duration:.0f}ms)")

    print()
    print("📈 统计信息:")
    stats = scheduler.get_stats()
    print(f"  提交总数: {stats['total_submitted']}")
    print(f"  完成总数: {stats['total_completed']}")
    print(f"  失败总数: {stats['total_failed']}")
    print(f"  平均耗时: {stats['avg_compute_time_ms']:.0f}ms")
    print(f"  DNA: {stats['dna']}")

    # 清理
    scheduler.shutdown()
    print()
    print("✅ 调度器已关闭")
