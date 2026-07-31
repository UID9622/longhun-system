# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·MVP-COLONY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""🐉 龍魂引擎：mvp_ant_colony
路径：engines/ant_colony/mvp_ant_colony.py
TODO：请补充详细功能说明（不少于20字）。"""
from __future__ import annotations
"""
极简MVP蚁群 v1.0 · MinimalViableColony
投喂挑战 P0-A1 落地：工蚁+侦察蚁 + 招募素+足迹素 + L1-L3

DNA: #龍芯⚡️丙午·辛未·MVP-COLONY-v1.0

设计原则（乔前辈·极简工程）:
  - 只做两群蚂蚁：工蚁(执行) + 侦察蚁(感知)
  - 只做两类信息素：RECRUIT(招募) + TRAIL(足迹)
  - 只做三层不动点：L1(任务) L2(技能) L3(服务)
  - 砍掉：ALERT/AGGREGATE, L4/L5, 兵蚁/储蜜蚁/育幼蚁
  - 目标：1个命令跑通整个蚁群协作闭环

用法:
    python3 engine/ant_colony/mvp_ant_colony.py run     # 启动MVP蚁群
    python3 engine/ant_colony/mvp_ant_colony.py demo    # 演示模式（自动生成任务）
    python3 engine/ant_colony/mvp_ant_colony.py status  # 查看状态
"""

import time
import json
import random
import threading
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict

from engine.ant_colony.antenna_signal import (
    AntennaSignal, PheromoneType, PayloadType,
    recruit_signal, trail_signal,
)
from engine.ant_colony.pheromone_system import PheromoneSystem
from engine.ant_colony.fixed_point_bridge import EmergenceCalculator


CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·辛未·MVP-COLONY-v1.0"


# ═══════════════════════════════════════════════
# MVP 蚂蚁定义
# ═══════════════════════════════════════════════

@dataclass
class AntState:
    """蚂蚁状态"""
    ant_id: str
    ant_type: str      # "worker" | "scout"
    population: str    # "工蚁群" | "侦察蚁群"
    persona: str       # 关联人格
    capabilities: List[str] = field(default_factory=list)
    busy: bool = False
    current_task: Optional[str] = None
    tasks_completed: int = 0
    signals_sent: int = 0
    signals_received: int = 0
    last_active: float = field(default_factory=time.time)


class WorkerAnt:
    """工蚁 — 执行任务，发放招募素，留足迹"""
    
    def __init__(self, ant_id: str, persona: str, capabilities: List[str]):
        self.state = AntState(
            ant_id=ant_id, ant_type="worker",
            population="工蚁群", persona=persona,
            capabilities=capabilities,
        )
    
    def execute(self, task: dict[str, Any], colony: 'MVPColony') -> Optional[AntennaSignal]:
        """执行任务 → 发放招募素 + 留足迹"""
        self.state.busy = True
        self.state.current_task = task.get("task", str(task))
        self.state.last_active = time.time()
        
        task_id = task.get("task_id", f"task_{int(time.time())}")
        
        # 1. 发放招募素 — 告诉同伴"这里有任务"
        recruit = recruit_signal(
            sender=self.state.ant_id,
            receiver=None,  # 广播
            task={
                "task": self.state.current_task,
                "task_id": task_id,
                "requested_capability": task.get("need_capability", "general"),
            },
            priority=task.get("priority", 5),
        )
        colony.ph.deposit(recruit, f"{self.state.ant_id}->broadcast", fixed_point_level=2)
        self.state.signals_sent += 1
        
        # 2. 执行任务（模拟工作量）
        time.sleep(random.uniform(0.1, 0.3))
        
        # 3. 留足迹 — 沉淀知识路径
        trail = trail_signal(
            sender=self.state.ant_id,
            receiver="储蜜蚁群",
            trail_type="task_completed",
            path_data={
                "task_id": task_id,
                "task": self.state.current_task,
                "executor": self.state.persona,
                "duration_ms": int((time.time() - self.state.last_active) * 1000),
                "success": True,
                "quality_score": random.uniform(0.7, 1.0),
            },
        )
        colony.ph.deposit(trail, f"{self.state.ant_id}->knowledge", fixed_point_level=1)
        self.state.signals_sent += 1
        
        self.state.tasks_completed += 1
        self.state.busy = False
        
        return recruit


class ScoutAnt:
    """侦察蚁 — 感知环境，发现任务，引导工蚁"""
    
    def __init__(self, ant_id: str, persona: str, capabilities: List[str]):
        self.state = AntState(
            ant_id=ant_id, ant_type="scout",
            population="侦察蚁群", persona=persona,
            capabilities=capabilities,
        )
    
    def scout(self, colony: 'MVPColony') -> List[AntennaSignal]:
        """侦察 → 发现需求 → 发放招募素"""
        signals = []
        
        # 1. 侦察：从信息素环境中嗅探
        best_paths = colony.ph.get_highway_paths(top_n=5)
        
        # 2. 如果有待处理任务，发放招募素
        if colony.task_queue:
            task = colony.task_queue.pop(0)
            recruit = recruit_signal(
                sender=self.state.ant_id,
                receiver=None,
                task=task,
                priority=task.get("priority", 6),
            )
            colony.ph.deposit(recruit, f"{self.state.ant_id}->broadcast", fixed_point_level=1)
            signals.append(recruit)
            self.state.signals_sent += 1
        
        # 3. 留侦察足迹
        if best_paths:
            trail = trail_signal(
                sender=self.state.ant_id,
                receiver="工蚁群",
                trail_type="scout_report",
                path_data={
                    "top_paths": [{"path": p[0], "strength": p[1]} for p in best_paths[:3]],
                    "active_trails": len(colony.ph.trails),
                    "timestamp": time.time(),
                },
            )
            colony.ph.deposit(trail, f"{self.state.ant_id}->worker_swarm", fixed_point_level=1)
            signals.append(trail)
            self.state.signals_sent += 1
        
        self.state.last_active = time.time()
        return signals


# ═══════════════════════════════════════════════
# MVP 蚁群运行时
# ═══════════════════════════════════════════════

# MVP 蚂蚁定义（只用工蚁+侦察蚁，对应16人格的子集）
MVP_ANTS = {
    # 工蚁群 — 执行输出
    "P04-鲁班":     WorkerAnt("P04-鲁班", "鲁班",     ["编码", "工程", "构建"]),
    "P01-诸葛亮":   WorkerAnt("P01-诸葛亮", "诸葛亮", ["策略", "推演", "规划"]),
    "P00-文心":     WorkerAnt("P00-文心", "文心",     ["创作", "统筹", "写作"]),
    "P06-数学大师": WorkerAnt("P06-数学大师", "数学大师", ["验证", "数学", "逻辑"]),
    "P03-雯雯":     WorkerAnt("P03-雯雯", "雯雯",     ["归档", "流程", "协作"]),
    # 侦察蚁群 — 感知预警
    "P09-孙思邈":   ScoutAnt("P09-孙思邈", "孙思邈",  ["诊断", "健康", "排查"]),
    "P10-苏东坡":   ScoutAnt("P10-苏东坡", "苏东坡",  ["美学", "评审", "体验"]),
}


class MVPColony:
    """
    极简MVP蚁群

    原则:
      - 工蚁(5) + 侦察蚁(2) = 7只蚂蚁
      - 只使用 RECRUIT + TRAIL 信息素
      - 只校验 L1-L3 不动点
      - 目标: 单命令跑通协作闭环
    """

    TICK_INTERVAL = 2.0  # 秒

    def __init__(self):
        self.workers: Dict[str, WorkerAnt] = {}
        self.scouts: Dict[str, ScoutAnt] = {}
        self.ph = PheromoneSystem()
        self.task_queue: List[dict[str, Any]] = []
        
        # 注册蚂蚁
        for ant_id, ant in MVP_ANTS.items():
            if isinstance(ant, WorkerAnt):
                self.workers[ant_id] = ant
            elif isinstance(ant, ScoutAnt):
                self.scouts[ant_id] = ant
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._tick = 0
        self._active_tasks: List[dict[str, Any]] = []

    # ── 主循环 ──

    def tick(self) -> dict[str, Any]:
        """单次滴答 — MVP蚁群一步"""
        self._tick += 1
        tc = self._tick
        signals_sent = 0

        # 1. 侦察蚁轮询（每隔2 tick）
        if tc % 2 == 0:
            for scout in self.scouts.values():
                sigs = scout.scout(self)
                signals_sent += len(sigs)

        # 2. 工蚁执行（每隔3 tick）
        if tc % 3 == 0 and self.task_queue:
            # 分配任务给空闲工蚁
            for worker in self.workers.values():
                if not worker.state.busy and self.task_queue:
                    task = self.task_queue.pop(0)
                    self._active_tasks.append(task)
                    sig = worker.execute(task, self)
                    if sig:
                        signals_sent += 1

        # 3. 信息素衰减（每隔10 tick）
        if tc % 10 == 0:
            self.ph.decay_all()

        # 4. 涌现计算
        E = self._calculate_emergence()

        return {
            "tick": tc,
            "workers_active": sum(1 for w in self.workers.values() if w.state.busy),
            "tasks_queued": len(self.task_queue),
            "trails": len(self.ph.trails),
            "signals_this_tick": signals_sent,
            "emergence_E": E,
            "time": datetime.now(CST).isoformat(),
        }

    def _calculate_emergence(self) -> float:
        """MVP版涌现计算 — 只用 D(多样性) 和 I(交互密度)"""
        # D: 种群分布
        pop_dist = {
            "工蚁群": len(self.workers),
            "侦察蚁群": len(self.scouts),
        }
        D = EmergenceCalculator.calculate_diversity(pop_dist)
        
        # I: 交互密度
        active_connections = len(self.ph.trails)
        total_modules = len(self.workers) + len(self.scouts)
        I = EmergenceCalculator.calculate_interaction_density(active_connections, total_modules)
        
        # 简化版E公式（只取D和I）
        E = (D ** 0.5) * (I ** 0.5)
        return E

    # ── 任务管理 ──

    def add_task(self, task_type: str, description: str, priority: int = 5,
                 need_capability: str = "general"):
        """向蚁群投喂一个任务"""
        task = {
            "task_id": f"mvp_{len(self.task_queue)}_{int(time.time()*1000)}",
            "task": description,
            "priority": priority,
            "need_capability": need_capability,
            "created_at": time.time(),
        }
        self.task_queue.append(task)
        return task["task_id"]

    def generate_demo_tasks(self):
        """演示模式 — 自动生成一批代表性任务"""
        demo_tasks = [
            ("编码", "实现用户认证模块", 8, "编码"),
            ("策略", "推演下周迭代计划", 7, "策略"),
            ("创作", "写一篇蚁群架构介绍", 6, "创作"),
            ("验证", "验证E公式参数稳定性", 8, "验证"),
            ("归档", "整理今日执行日志", 5, "归档"),
            ("诊断", "检查信息素衰减是否正常", 7, "诊断"),
            ("编码", "优化触角总线路由算法", 9, "编码"),
            ("策略", "评估MVP下一步扩展方向", 6, "策略"),
            ("创作", "生成MVP运行报告", 5, "创作"),
            ("验证", "蒙特卡洛模拟涌现态", 8, "验证"),
        ]
        for task_type, desc, priority, cap in demo_tasks:
            self.add_task(task_type, desc, priority, cap)
        return len(demo_tasks)

    # ── 运行时 ──

    def run(self, ticks: int = 50, demo: bool = True):
        """运行MVP蚁群"""
        if demo and not self.task_queue:
            n = self.generate_demo_tasks()
            print(f"📋 生成了 {n} 个演示任务")

        print(f"\n{'='*60}")
        print(f"🐜 龙魂MVP蚁群 启动")
        print(f"   工蚁: {len(self.workers)} 只 | 侦察蚁: {len(self.scouts)} 只")
        print(f"   信息素: RECRUIT + TRAIL | 不动点: L1-L3")
        print(f"   目标: 跑通协作闭环 | DNA: {DNA}")
        print(f"{'='*60}\n")

        self._running = True
        snapshots = []

        try:
            for i in range(ticks):
                state = self.tick()
                snapshots.append(state)
                
                if i % 5 == 0 or i == ticks - 1:
                    self._print_tick(state)

                time.sleep(self.TICK_INTERVAL / 10)  # MVP加速10倍

        except KeyboardInterrupt:
            print("\n⏹ MVP蚁群被中断")
        finally:
            self._running = False

        # 终态报告
        self._print_final_report(snapshots)

    def _print_tick(self, state: dict[str, Any]):
        """打印tick状态"""
        bar = "=" * min(20, int(state["emergence_E"] * 30))
        print(f"[t={state['tick']:3d}] 工蚁活跃:{state['workers_active']} "
              f"待处理:{state['tasks_queued']} "
              f"轨迹:{state['trails']} "
              f"E={state['emergence_E']:.3f} {bar}")

    def _print_final_report(self, snapshots: list[Any]):
        """终态报告"""
        if not snapshots:
            return
        
        final = snapshots[-1]
        total_tasks_done = sum(w.state.tasks_completed for w in self.workers.values())
        total_signals = sum(
            w.state.signals_sent + s.state.signals_sent
            for w in self.workers.values()
            for s in self.scouts.values()
        )
        E_max = max(s["emergence_E"] for s in snapshots)
        E_avg = sum(s["emergence_E"] for s in snapshots) / len(snapshots)

        print(f"\n{'='*60}")
        print(f"📊 MVP蚁群 终态报告")
        print(f"{'='*60}")
        print(f"  总tick: {final['tick']}")
        print(f"  完成任务: {total_tasks_done}")
        print(f"  发送信号: {total_signals}")
        print(f"  信息素轨迹: {final['trails']} 条")
        print(f"  涌现质量: 峰值 E={E_max:.3f}  均值 E={E_avg:.3f}")
        
        grade = "涌现态 🔥" if E_max > 1.0 else "临界态 ⚡" if E_max > 0.8 else "积累态 📈"
        print(f"  状态: {grade}")

        # 高速公路
        highways = self.ph.get_highway_paths(5)
        if highways:
            print(f"\n  信息素高速公路 Top5:")
            for path, strength, ptype in highways:
                print(f"    {path:30s} {strength:6.1f} [{ptype.value}]")

        print(f"\n  DNA: {DNA}")
        print(f"{'='*60}")


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"

    colony = MVPColony()

    if cmd == "run":
        # 纯运行模式（不自动生成任务）
        print("MVP蚁群 · 运行模式（需手动 add_task）")
        colony.run(ticks=30, demo=False)

    elif cmd == "demo":
        # 演示模式（自动生成演示任务）
        colony.run(ticks=50, demo=True)

    elif cmd == "status":
        # 查看当前状态
        snap = colony.tick()
        colony._print_tick(snap)
        print(f"\n工蚁: {len(colony.workers)} | 侦察蚁: {len(colony.scouts)}")
        print(f"任务队列: {len(colony.task_queue)} | 轨迹: {len(colony.ph.trails)}")

    elif cmd == "bench":
        # 基准测试：跑100 tick 看涌现
        print("MVP蚁群 · 基准测试 (100 tick)")
        colony.run(ticks=100, demo=True)

    else:
        print(f"用法: python3 {__file__} [run|demo|status|bench]")
