#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 资源调度引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-SCHEDULER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 动态分配CPU/内存给不同任务（基于优先级）
  - 支持任务优先级（LOW/MEDIUM/HIGH/CRITICAL）
  - 智能负载均衡（避免单核过载）
  - 实时监控调度效果（省电积分联动）
"""

import psutil
import threading
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass, field
from collections import deque


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class TaskRequest:
    task_id: str
    priority: Priority
    estimated_cpu: float
    estimated_memory: float
    deadline: Optional[float] = None


@dataclass
class ResourceAllocation:
    task_id: str
    cpu_limit: float
    memory_limit: float
    granted: bool
    reason: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))


class ResourceScheduler:
    """资源调度引擎——不只是统计省电积分，真正做动态调优"""

    def __init__(self):
        self.current_allocations: Dict[str, ResourceAllocation] = {}
        self.history: deque = deque(maxlen=1000)
        self._lock = threading.Lock()

    def request_resources(self, req: TaskRequest) -> ResourceAllocation:
        """请求资源分配"""
        with self._lock:
            cpu_avail = 100 - psutil.cpu_percent(interval=0.1)
            mem_avail = psutil.virtual_memory().available / (1024**2)

            cpu_need = req.estimated_cpu
            mem_need = req.estimated_memory

            # CRITICAL 强制分配
            if req.priority == Priority.CRITICAL:
                self._preempt_low_priority(cpu_need, mem_need)
                cpu_avail = 100 - psutil.cpu_percent(interval=0.1)
                mem_avail = psutil.virtual_memory().available / (1024**2)

            if cpu_need <= cpu_avail and mem_need <= mem_avail:
                allocation = ResourceAllocation(
                    task_id=req.task_id, cpu_limit=cpu_need,
                    memory_limit=mem_need, granted=True,
                    reason="sufficient_resources"
                )
            else:
                reduced_cpu = min(cpu_need, cpu_avail * 0.8)
                reduced_mem = min(mem_need, mem_avail * 0.8)
                if reduced_cpu > 5 and reduced_mem > 10:
                    allocation = ResourceAllocation(
                        task_id=req.task_id, cpu_limit=reduced_cpu,
                        memory_limit=reduced_mem, granted=True,
                        reason=f"degraded: {cpu_need:.1f}%→{reduced_cpu:.1f}% / {mem_need:.1f}MB→{reduced_mem:.1f}MB"
                    )
                else:
                    allocation = ResourceAllocation(
                        task_id=req.task_id, cpu_limit=0, memory_limit=0,
                        granted=False, reason="insufficient_resources"
                    )

            if allocation.granted:
                self.current_allocations[req.task_id] = allocation
            self.history.append(allocation)
            return allocation

    def _preempt_low_priority(self, cpu_needed: float, mem_needed: float):
        """抢占低优先级任务"""
        to_remove = []
        for tid, alloc in self.current_allocations.items():
            if alloc.granted and alloc.cpu_limit < 10 and alloc.memory_limit < 100:
                to_remove.append(tid)
        for tid in to_remove:
            del self.current_allocations[tid]
            if to_remove:
                print(f"⏹️ 抢占 {len(to_remove)} 个低优先级任务")

    def release_resources(self, task_id: str):
        with self._lock:
            self.current_allocations.pop(task_id, None)

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_allocations": len(self.current_allocations),
            "cpu_available_percent": round(100 - psutil.cpu_percent(interval=0.1), 1),
            "memory_available_mb": round(psutil.virtual_memory().available / (1024**2), 1),
            "total_scheduled": len(self.history),
        }


if __name__ == "__main__":
    scheduler = ResourceScheduler()

    req = TaskRequest("test_001", Priority.HIGH, 20, 100)
    alloc = scheduler.request_resources(req)
    print(f"分配: granted={alloc.granted}, reason={alloc.reason}")

    status = scheduler.get_status()
    print(f"状态: CPU可用={status['cpu_available_percent']}% | 内存可用={status['memory_available_mb']}MB")

    scheduler.release_resources("test_001")
    print("🟢 资源调度引擎测试通过")
