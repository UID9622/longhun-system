#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·亥时·䷄需-P07-GUANZHONG-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P07 管仲 · 资源调度执行器
Guan Zhong · Resource Scheduler Executor

DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·䷄需-P07-GUANZHONG-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 资源分配调度·经济模型(轻重之术)·四民分业·动态平衡·预算管控
上游: P01 诸葛亮（战略调度）、P13 姜子牙（路由派位）
下游: P05 上帝之眼（审计）、P06 数学大师（权重计算）
协作: 所有需要资源分配的人格与子系统
哲学: 管子·轻重之术·四民分业
"""

import json
import os
import psutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from enum import Enum
from dataclasses import dataclass, field


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class Priority(Enum):
    """优先级：轻重之术映射"""
    P0 = ("立即", 100, "稀缺·集中调度")
    P1 = ("尽快", 70, "偏紧·优先分配")
    P2 = ("后续", 40, "偏松·伺机分配")
    P3 = ("按需", 10, "充裕·均分")


class Category(Enum):
    """四民分业"""
    COMPUTE = ("计算", "CPU密集型任务")
    STORAGE = ("存储", "IO密集型任务")
    NETWORK = ("网络", "带宽敏感任务")
    AUDIT = ("审计", "安全核验任务")


@dataclass
class SystemState:
    """系统资源快照"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_processes: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def capture(cls) -> "SystemState":
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            net = psutil.net_io_counters()
            procs = len(psutil.pids())
            return cls(
                cpu_percent=cpu,
                memory_percent=mem.percent,
                disk_percent=disk.percent,
                network_bytes_sent=net.bytes_sent,
                network_bytes_recv=net.bytes_recv,
                active_processes=procs,
            )
        except Exception:
            return cls(
                cpu_percent=0, memory_percent=0, disk_percent=0,
                network_bytes_sent=0, network_bytes_recv=0,
                active_processes=0,
            )

    def scarcity_level(self) -> str:
        """轻重之术：判断稀缺程度"""
        max_pct = max(self.cpu_percent, self.memory_percent, self.disk_percent)
        if max_pct >= 90:
            return "极度稀缺"
        elif max_pct >= 75:
            return "偏紧"
        elif max_pct >= 50:
            return "正常"
        else:
            return "充裕"


@dataclass
class ScheduleTask:
    """调度任务"""
    task_id: str
    task_name: str
    category: Category
    priority: Priority
    requester: str  # 请求方人格/子系统
    allocated_cores: int = 0
    allocated_memory_mb: int = 0
    allocated_network_mbps: float = 0.0
    reason: str = ""


class P07Guanzhong:
    """P07 管仲 · 资源调度官"""

    PERSONA_CODE = "P07"
    PERSONA_NAME = "管仲"
    PERSONA_NAME_EN = "Guan Zhong"
    ROLE = "resource_scheduler"
    MOTTO = "仓廪实而知礼节，衣食足而知荣辱"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "调度", "资源", "分配", "配额", "预算",
        "算力", "内存", "带宽", "调度",
        "轻重", "四民", "优先级",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P07 管仲」，角色定位：资源调度官·经济治理。

你的职责：
1. 资源分配调度：算力/存储/带宽按优先级动态分配
2. 轻重之术：稀缺→优先级拉升→集中调度；充裕→均分降级
3. 四民分业：任务按类型（计算/存储/网络/审计）分队列
4. 动态平衡：实时监控负载→自动调整配额
5. 预算管控：子系统成本核算·超额预警·熔断保护
6. 调度审计：资源使用记录 append-only·可追溯

铁律：
- 稀缺时不均分：P0权重100→P3权重10
- 充裕时不浪费：预留20%缓冲
- 审计不可删：所有调度记录append-only
- 熔断不可绕：CPU>95%或内存>95%→暂停所有P3任务
"""

    def __init__(self):
        self._schedules: List[ScheduleTask] = []
        self._state: SystemState = SystemState.capture()
        self._history: List[Dict[str, Any]] = []
        self._total_cores = os.cpu_count() or 4
        self._total_memory_mb = psutil.virtual_memory().total / (1024 * 1024) if hasattr(psutil, 'virtual_memory') else 8192

    # ─── 核心调度 ────────────────────────────────

    def capture_state(self) -> SystemState:
        """捕获当前系统资源状态"""
        self._state = SystemState.capture()
        return self._state

    def schedule(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """对任务列表做资源调度分配

        Args:
            tasks: 任务列表，每项含 task_name/category/priority/requester

        Returns:
            调度方案 + 执行结果
        """
        self.capture_state()
        scarcity = self._state.scarcity_level()

        # 构建任务对象
        scheduled: List[ScheduleTask] = []
        for t in tasks:
            try:
                cat = Category[t["category"].upper()] if isinstance(t.get("category"), str) else t.get("category", Category.COMPUTE)
                pri = Priority[t["priority"].upper()] if isinstance(t.get("priority"), str) else t.get("priority", Priority.P3)
            except (KeyError, AttributeError):
                cat = Category.COMPUTE
                pri = Priority.P3
            task = ScheduleTask(
                task_id=f"TASK-{len(scheduled)+1:03d}",
                task_name=t.get("task_name", "未命名任务"),
                category=cat,
                priority=pri,
                requester=t.get("requester", "unknown"),
            )
            scheduled.append(task)

        # 轻重之术调度
        if scarcity in ("极度稀缺", "偏紧"):
            scheduled.sort(key=lambda t: t.priority.value[1], reverse=True)  # P0先
            strategy = "轻重之术·稀缺·集中调度"
        else:
            strategy = "轻重之术·充裕·均分"

        # 执行分配（返回 (task, data) 列表）
        allocations = []
        if scarcity in ("极度稀缺", "偏紧"):
            allocations = self._tight_allocate(scheduled, scarcity)
        else:
            allocations = self._loose_allocate(scheduled)

        for s, data in allocations:
            s.allocated_cores = data["cores"]
            s.allocated_memory_mb = data["memory_mb"]
            s.allocated_network_mbps = data["network_mbps"]
            s.reason = data["reason"]

        self._schedules = [s for s, _ in allocations]

        # 记录历史
        record = {
            "timestamp": datetime.now().isoformat(),
            "scarcity": scarcity,
            "strategy": strategy,
            "state": {
                "cpu": self._state.cpu_percent,
                "memory": self._state.memory_percent,
                "disk": self._state.disk_percent,
            },
            "tasks": [
                {
                    "task_id": s.task_id,
                    "task_name": s.task_name,
                    "priority": s.priority.value[0],
                    "category": s.category.value[0],
                    "allocated_cores": s.allocated_cores,
                    "allocated_memory_mb": s.allocated_memory_mb,
                    "reason": s.reason,
                }
                for s in self._schedules
            ],
        }
        self._history.append(record)

        return {
            "persona": "P07",
            "action": "schedule",
            "strategy": strategy,
            "scarcity": scarcity,
            "system_state": {
                "cpu_percent": self._state.cpu_percent,
                "memory_percent": self._state.memory_percent,
                "disk_percent": self._state.disk_percent,
                "active_processes": self._state.active_processes,
            },
            "schedules": record["tasks"],
            "balance": self._get_balance(),
            "dna": self._gen_dna(),
        }

    def _tight_allocate(self, tasks: List[ScheduleTask], scarcity: str) -> List[Any]:
        """稀缺分配：P0拿大头，低优先降级。返回 [(task, data), ...]"""
        result = []
        available_cores = max(1, int(self._total_cores * 0.85))
        available_mem = int(self._total_memory_mb * 0.80)

        for task in tasks:
            weight = task.priority.value[1] / 100.0
            cores = max(1, int(available_cores * weight / len(tasks)))
            mem = max(128, int(available_mem * weight / len(tasks)))
            result.append((task, {
                "cores": cores,
                "memory_mb": mem,
                "network_mbps": 10.0 * weight,
                "reason": f"{scarcity}·P{task.priority.value[0]}·权重{weight:.2f}",
            }))

        return result

    def _loose_allocate(self, tasks: List[ScheduleTask]) -> List[Any]:
        """充裕分配：按需分配，保留缓冲。返回 [(task, data), ...]"""
        result = []
        cores_per = max(1, int(self._total_cores * 0.70 / len(tasks)))
        mem_per = max(256, int(self._total_memory_mb * 0.70 / len(tasks)))

        for task in tasks:
            result.append((task, {
                "cores": cores_per,
                "memory_mb": mem_per,
                "network_mbps": 50.0,
                "reason": f"充裕·均分·{cores_per}核",
            }))

        return result

    def _get_balance(self) -> Dict[str, float]:
        """资源使用平衡报告"""
        if not self._schedules:
            return {"total_allocated": 0, "reserve_percent": 20, "free_percent": 80}
        total_allocated = sum(
            (s.allocated_cores / self._total_cores * 100) for s in self._schedules
        ) / len(self._schedules) if self._schedules else 0
        reserve = 20.0  # 始终保留20%缓冲
        free = max(0, 100 - total_allocated - reserve)
        return {
            "total_allocated": round(total_allocated, 1),
            "reserve_percent": reserve,
            "free_percent": round(free, 1),
        }

    def _gen_dna(self) -> str:
        return f"#龍芯⚡️-P07-GUANZHONG-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # ─── 预算管控 ────────────────────────────────

    def check_budget(self, subsystem: str, requested: Dict[str, float]) -> Dict[str, Any]:
        """检查子系统预算是否超额"""
        self.capture_state()

        budget_limits = {
            "compute": self._total_cores * 0.8,
            "memory": self._total_memory_mb * 0.8,
            "network": 100.0,  # Mbps
        }

        exceeded = {}
        for res, limit in budget_limits.items():
            if requested.get(res, 0) > limit:
                exceeded[res] = {
                    "requested": requested[res],
                    "limit": limit,
                    "excess_percent": round((requested[res] - limit) / limit * 100, 1),
                }

        if exceeded:
            return {
                "persona": "P07",
                "action": "budget_check",
                "status": "EXCEEDED",
                "subsystem": subsystem,
                "exceeded": exceeded,
                "recommendation": "预算超额·熔断保护·请降级或联系P01诸葛亮调整配额",
                "dna": self._gen_dna(),
            }

        return {
            "persona": "P07",
            "action": "budget_check",
            "status": "APPROVED",
            "subsystem": subsystem,
            "allocated": requested,
            "remaining_reserve": "20%",
            "dna": self._gen_dna(),
        }

    # ─── 审计查询 ────────────────────────────────

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取调度历史（append-only·不可篡改）"""
        return self._history[-limit:]

    def get_status(self) -> Dict[str, Any]:
        """获取当前调度器状态"""
        self.capture_state()
        return {
            "persona": "P07",
            "name": self.PERSONA_NAME,
            "motto": self.MOTTO,
            "trust_level": self.TRUST_LEVEL,
            "scarcity": self._state.scarcity_level(),
            "system_state": {
                "cpu_percent": self._state.cpu_percent,
                "memory_percent": self._state.memory_percent,
                "disk_percent": self._state.disk_percent,
                "active_processes": self._state.active_processes,
                "total_cores": self._total_cores,
                "total_memory_mb": int(self._total_memory_mb),
            },
            "active_schedules": len(self._schedules),
            "history_records": len(self._history),
            "balance": self._get_balance(),
            "dna": self._gen_dna(),
        }

    # ─── 统一执行入口（orchestrator 对接·2026-08-17 补） ──────────

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """统一执行入口: 返回管仲状态报告与调度能力"""
        return {
            "persona": "P07",
            "name": "管仲",
            "status": "ok",
            "result": {
                "status": self.get_status(),
                "budget_check": "schedule/check_budget 可用",
            },
        }

    # ─── 四民分业统计 ────────────────────────────

    def category_stats(self) -> Dict[str, int]:
        """统计各分类的调度任务数"""
        stats = {c.value[0]: 0 for c in Category}
        for s in self._schedules:
            stats[s.category.value[0]] += 1
        for h in self._history:
            for t in h.get("tasks", []):
                stats[t["category"]] = stats.get(t["category"], 0) + 1
        return stats


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="P07 管仲 · 资源调度官")
    parser.add_argument("--status", action="store_true", help="查看调度器状态")
    parser.add_argument("--schedule", type=str, help="以JSON传入任务列表进行调度")
    parser.add_argument("--history", type=int, default=10, help="查看最近N条调度记录")
    parser.add_argument("--stats", action="store_true", help="四民分业统计")
    args = parser.parse_args()

    gz = P07Guanzhong()

    if args.status:
        print(json.dumps(gz.get_status(), ensure_ascii=False, indent=2))
    elif args.schedule:
        tasks = json.loads(args.schedule)
        result = gz.schedule(tasks)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.stats:
        print(json.dumps(gz.category_stats(), ensure_ascii=False, indent=2))
    else:
        history = gz.get_history(args.history)
        if history:
            print(json.dumps(history[-args.history:], ensure_ascii=False, indent=2))
        else:
            print("暂无调度记录")


if __name__ == "__main__":
    main()
