# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·ANT-COLONY-RUNTIME-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
蚁群运行时引擎 v2.0 · AntColonyRuntime
将蚁群引擎接入龙魂实际运行链路

DNA: #龍芯⚡️丙午·辛未·ANT-COLONY-RUNTIME-v2.0
# STATUS: ⚠️ DEPRECATED · 本目录为旧版蚁群实现，功能由 engines/ant_colony/ 与 bin/lh_ant_colony_orchestrator.py 统一接管

职责:
  - 主循环: 定时 tick 信息素衰减/触角总线/涌现计算
  - 持久化: 状态自动落盘 SQLite
  - 健康端点: HTTP /health 接口
  - 钩子输出: 对接 lh_unified_hook.py
  - 统计面板: 实时度量导出
"""

import time
import json
import math
import os
import sys
import threading
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from engine.ant_colony.antenna_bus import AntennaBus, create_populated_bus
from engine.ant_colony.pheromone_system import PheromoneSystem
from engine.ant_colony.fixed_point_bridge import (
    FixedPointBridge, EmergenceCalculator, ColorPheromoneMapper,
    FixedPointLevel, WuxingPheromoneCoupling,
)
from engine.ant_colony.antenna_signal import PheromoneType

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·辛未·ANT-COLONY-RUNTIME-v2.0"


@dataclass
class ColonyState:
    """蚁群运行时快照"""
    timestamp: str = ""
    tick_count: int = 0
    active_modules: int = 0
    total_signals_sent: int = 0
    total_signals_blocked: int = 0
    pheromone_trails: int = 0
    emergence_E: float = 0.0
    emergence_grade: str = "初始态"
    population_distribution: Dict[str, int] = field(default_factory=dict)
    pheromone_concentration: Dict[str, float] = field(default_factory=dict)
    top_paths: List[Dict[str, Any]] = field(default_factory=list)
    bus_stats: Dict[str, Any] = field(default_factory=dict)
    dna: str = DNA

    def grade_emergence(self) -> str:
        if self.emergence_E < 0.3:
            return "初始态"
        elif self.emergence_E < 0.6:
            return "积累态"
        elif self.emergence_E < 1.0:
            return "激活态"
        elif self.emergence_E < 1.5:
            return "涌现态"
        else:
            return "超涌现态"

    def summary(self) -> str:
        lines = [
            f"🐜 龙魂蚁群运行时 v2.0",
            f"  tick: {self.tick_count}  活跃: {self.active_modules}/{len(self.population_distribution)}",
            f"  信号: 发送{self.total_signals_sent} 阻断{self.total_signals_blocked}",
            f"  信息素轨迹: {self.pheromone_trails} 条",
            f"  涌现质量 E={self.emergence_E:.4f} ({self.grade_emergence()})",
        ]
        if self.pheromone_concentration:
            lines.append(f"  信息素浓度: " + " | ".join(
                f"{k}={v:.1f}" for k, v in self.pheromone_concentration.items()))
        if self.population_distribution:
            lines.append(f"  种群分布: " + " | ".join(
                f"{k}:{v}" for k, v in self.population_distribution.items()))
        return "\n".join(lines)


class AntColonyRuntime:
    """
    蚁群运行时引擎 · 主循环驱动
    
    用法:
        runtime = AntColonyRuntime()
        runtime.start()       # 启动后台线程
        runtime.tick()        # 手动滴答一次
        state = runtime.snapshot()  # 获取当前快照
        runtime.stop()        # 停止
    """

    # 默认值可通过 set_config() 在运行时热更新
    TICK_INTERVAL = 5.0        # 滴答间隔（秒）
    DECAY_TICK = 10            # 每 N 个 tick 衰减一次
    SNAPSHOT_TICK = 30         # 每 N 个 tick 保存快照
    EMERGENCE_TICK = 20        # 每 N 个 tick 计算涌现
    PERSIST_TICK = 60          # 每 N 个 tick 持久化

    def __init__(self, db_path: Optional[str] = None, verbose: bool = False):
        self.bus = create_populated_bus()
        self.pheromone_system = self.bus.pheromone_system
        # FixedPointBridge/EmergenceCalculator 是纯 @classmethod 工具类，不需要实例化
        self.bridge = FixedPointBridge
        self.emergence_calc = EmergenceCalculator

        # 注册外部通信端点（CLI、钩子等）
        from engine.ant_colony.antenna_bus import ModuleRegistration
        for ext_id, ext_pop in [
            ("CLI", "工蚁群"),
            ("hook_pre_audit", "侦察蚁群"),
            ("hook_on_complete", "储蜜蚁群"),
            ("hook_lifecycle", "侦察蚁群"),
            ("health_endpoint", "兵蚁群"),
            ("global_search_v2", "工蚁群"),
            ("cnsh_compiler", "工蚁群"),
        ]:
            self.bus.modules[ext_id] = ModuleRegistration(
                module_id=ext_id,
                population=ext_pop,
                capabilities=["bridge"],
                level_access=1,
            )
            # 给外部端点连接邻居（至少连一个同类群的模块）
            for mid, mod in self.bus.modules.items():
                if mid != ext_id and mod.population == ext_pop:
                    self.bus.neighbors.setdefault(ext_id, set()).add(mid)
                    self.bus.neighbors.setdefault(mid, set()).add(ext_id)
                    break

        self._tick_count = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._last_snapshot: Optional[ColonyState] = None
        self._last_emergence_E: float = 0.0
        self._event_log: List[Dict[str, Any]] = []
        self._verbose = verbose
        self._quiet = not verbose

        # 配置字典（可被 /config 热更新）
        self._config = {
            "tick_interval": self.TICK_INTERVAL,
            "decay_tick": self.DECAY_TICK,
            "snapshot_tick": self.SNAPSHOT_TICK,
            "emergence_tick": self.EMERGENCE_TICK,
            "persist_tick": self.PERSIST_TICK,
            "verbose": self._verbose,
        }

        # 持久化
        self._db_path = db_path or str(
            ROOT / "data" / "ant_colony_state.db"
        )
        self._init_db()
        self._restore()

    # ═══════════════════════════════════════════════
    # 数据库
    # ═══════════════════════════════════════════════

    def _init_db(self):
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS colony_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick_count INTEGER,
                emergence_E REAL,
                active_modules INTEGER,
                total_signals INTEGER,
                total_blocked INTEGER,
                pheromone_trails INTEGER,
                snapshot_json TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS colony_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                module TEXT,
                signal_type TEXT,
                detail TEXT,
                tick_count INTEGER,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
        conn.close()

    def _restore(self):
        """从数据库恢复上次运行的蚁群状态"""
        try:
            conn = sqlite3.connect(self._db_path)
            row = conn.execute(
                "SELECT tick_count, emergence_E, total_signals, total_blocked, pheromone_trails, snapshot_json "
                "FROM colony_snapshots ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row:
                self._tick_count = row[0] or 0
                self._last_emergence_E = row[1] or 0.0
                if row[5]:
                    snap = json.loads(row[5])
                    # 恢复事件日志（最多保留最后50条）
                    if "event_log" not in snap:
                        events = snap.get("recent_events", [])
                        if events:
                            self._event_log = events[-50:]
                print(f"[ant_colony] 状态恢复: tick#{self._tick_count} "
                      f"E={row[1]:.4f} 信号{row[2] or 0}条 轨迹{row[4] or 0}条")
        except Exception as e:
            print(f"[ant_colony] 恢复状态失败（首次启动正常）: {e}")

    def _persist(self):
        state = self.snapshot()
        try:
            snap_dict = asdict(state)
            snap_dict["event_log"] = self._event_log[-50:]
            conn = sqlite3.connect(self._db_path)
            conn.execute(
                "INSERT INTO colony_snapshots (tick_count, emergence_E, active_modules, total_signals, total_blocked, pheromone_trails, snapshot_json) VALUES (?,?,?,?,?,?,?)",
                (state.tick_count, state.emergence_E, state.active_modules,
                 state.total_signals_sent, state.total_signals_blocked,
                 state.pheromone_trails, json.dumps(snap_dict, ensure_ascii=False))
            )
            conn.commit()
            conn.close()
        except Exception as e:
            self._log(f"持久化失败: {e}")

    # ═══════════════════════════════════════════════
    # 配置
    # ═══════════════════════════════════════════════

    def _log(self, msg: str, force: bool = False):
        """内部日志：默认安静，force=True 时强制输出"""
        if not self._quiet or force:
            print(f"[ant_colony] {msg}")

    def get_config(self) -> Dict[str, Any]:
        """获取当前可调参数"""
        return self._config.copy()

    def set_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """热更新运行时参数（不重启）"""
        allowed = {
            "tick_interval", "decay_tick", "snapshot_tick",
            "emergence_tick", "persist_tick", "verbose"
        }
        changed = {}
        for k, v in updates.items():
            if k not in allowed:
                continue
            if k == "verbose":
                self._verbose = bool(v)
                self._quiet = not self._verbose
            else:
                try:
                    v = float(v) if k == "tick_interval" else int(v)
                    if v <= 0:
                        continue
                except (ValueError, TypeError):
                    continue
            self._config[k] = v
            changed[k] = v
        self._log(f"配置已更新: {changed}")
        return {"changed": changed, "current": self._config.copy()}


    def tick(self) -> ColonyState:
        """单次滴答 — 推进蚁群状态一步"""
        with self._lock:
            self._tick_count += 1
            tc = self._tick_count

            # 1. 信息素衰减
            if tc % self._config["decay_tick"] == 0:
                self.pheromone_system.decay_all()
                self._log_event("decay", "system", "", 
                              f"衰减: {len(self.pheromone_system.trails)} 条轨迹")

            # 2. 触角总线脉冲 — 各模块发心跳
            if tc % 3 == 0:
                for module_id in list(self.bus.modules.keys()):
                    try:
                        from engine.ant_colony.antenna_signal import recruit_signal
                        sig = recruit_signal(
                            sender=module_id,
                            receiver=None,
                            task={"task": "Heartbeat", "tick": tc},
                            priority=8
                        )
                        self.bus.send(sig)
                    except Exception:
                        pass

            # 3. 涌现计算
            if tc % self._config["emergence_tick"] == 0:
                snapshot = self.snapshot()
                self._last_snapshot = snapshot
                self._log_event("emergence", "system", "",
                              f"E={snapshot.emergence_E:.4f} ({snapshot.grade_emergence()})")

            # 4. 持久化
            if tc % self._config["persist_tick"] == 0:
                self._persist()

            return self.snapshot()

    def _log_event(self, event_type: str, module: str, 
                   signal_type: str, detail: str):
        self._event_log.append({
            "tick": self._tick_count,
            "type": event_type,
            "module": module,
            "signal": signal_type,
            "detail": detail,
            "time": datetime.now(CST).isoformat(),
        })
        if len(self._event_log) > 500:
            self._event_log = self._event_log[-300:]

    # ═══════════════════════════════════════════════
    # 快照 & 统计
    # ═══════════════════════════════════════════════

    def snapshot(self) -> ColonyState:
        """获取当前蚁群状态快照"""
        bs = self.bus.stats.copy()
        ps_stats = self.pheromone_system.get_stats()

        # 种群分布
        pop_dist: Dict[str, int] = {}
        for mid, mod in self.bus.modules.items():
            pop = mod.population
            pop_dist[pop] = pop_dist.get(pop, 0) + 1

        # 信息素浓度（各类型路径数 × 平均强度）
        conc: Dict[str, float] = {}
        for pt in PheromoneType:
            paths = self.pheromone_system.get_paths_by_type(pt)
            total_strength = sum(s for _, s in paths)
            conc[pt.value] = total_strength

        # 涌现计算 — 使用 EmergenceCalculator 的实际 API
        # D: 种群分布 Shannon 熵
        D = EmergenceCalculator.calculate_diversity(pop_dist)
        # I: 实际连接 / 最大连接
        active_connections = len(self.pheromone_system.trails)
        total_modules = len(self.bus.modules)
        I = EmergenceCalculator.calculate_interaction_density(active_connections, total_modules)
        # C: 一致性 = 1 - 冲突比例
        conflict_count = sum(
            1 for k, t in self.pheromone_system.trails.items()
            if t.pheromone_type in (PheromoneType.ALERT,) and t.current_strength > 20
        )
        total_interactions = bs.get("signals_sent", 1)
        C = EmergenceCalculator.calculate_coherence(conflict_count, total_interactions)
        # V: 变异容忍 = 1 - HHI
        offline_freqs = [0.01] * max(total_modules, 1)  # 每个模块默认 1% 离线
        V = EmergenceCalculator.calculate_variance_tolerance(offline_freqs)

        emergence_state = EmergenceCalculator.compute(D, I, C, V)
        E = emergence_state.score

        state = ColonyState(
            timestamp=datetime.now(CST).isoformat(),
            tick_count=self._tick_count,
            active_modules=bs.get("active_modules", len(self.bus.modules)),
            total_signals_sent=bs.get("signals_sent", 0),
            total_signals_blocked=bs.get("signals_blocked", 0) + bs.get("signals_blocked_by_fixed_point", 0),
            pheromone_trails=ps_stats.get("total_trails", 0),
            emergence_E=E,
            population_distribution=pop_dist,
            pheromone_concentration=conc,
            top_paths=[{"path": p[0], "strength": p[1], "type": p[2].value}
                       for p in self.pheromone_system.get_highway_paths(5)],
            bus_stats=bs,
        )
        state.emergence_grade = state.grade_emergence()
        return state

    # ═══════════════════════════════════════════════
    # 生命周期
    # ═══════════════════════════════════════════════

    def _run_loop(self):
        """后台主循环"""
        self._log(f"启动 · tick={self._config['tick_interval']}s · DNA={DNA}")
        while self._running:
            try:
                state = self.tick()
                if self._tick_count % 30 == 0:
                    self._log(f"tick#{self._tick_count} E={state.emergence_E:.4f}")
            except Exception as e:
                self._log(f"tick 异常: {e}")
            time.sleep(self._config["tick_interval"])

    def start(self):
        """启动后台运行时"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="ant-colony-runtime"
        )
        self._thread.start()
        self._log(f"运行时已启动 (tid={self._thread.ident})", force=True)

    def stop(self):
        """停止运行时"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=10)
        self._persist()
        self._log(f"运行时已停止 · 最终 tick={self._tick_count}", force=True)

    @property
    def is_running(self) -> bool:
        return self._running

    # ═══════════════════════════════════════════════
    # 命令接口
    # ═══════════════════════════════════════════════

    def send_task(self, task: str, sender: str = "CLI", 
                  priority: int = 7) -> Dict[str, Any]:
        """发送任务到蚁群总线"""
        from engine.ant_colony.antenna_signal import recruit_signal
        sig = recruit_signal(
            sender=sender,
            receiver=None,
            task={"task": task, "source": "CLI"},
            priority=priority,
        )
        ok = self.bus.send(sig)
        self._log_event("task", sender, "RECRUIT", 
                       f"任务: {task[:50]} {'✅' if ok else '❌'}")
        return {"ok": ok, "signal_id": sig.signal_id[:16], 
                "color": sig.color_state}

    def simulate_alert(self, issue: str, severity: int = 3) -> Dict[str, Any]:
        """模拟安全告警 — 以兵蚁群身份发出"""
        from engine.ant_colony.antenna_signal import alert_signal
        # 告警必须从兵蚁群发出才能通过颜色路由
        guard_sender = None
        for mid, mod in self.bus.modules.items():
            if mod.population == "兵蚁群":
                guard_sender = mid
                break
        sender = guard_sender or "CLI"
        sig = alert_signal(
            sender=sender,
            alert_level=severity,
            description=issue,
        )
        ok = self.bus.send(sig)
        self._log_event("alert", sender, "ALERT", 
                       f"告警: {issue[:50]} {'✅' if ok else '❌'}")
        return {"ok": ok, "signal_id": sig.signal_id[:16],
                "escalation": sig.payload.get("auto_escalate", False)}

    def broadcast_aggregate(self, topic: str) -> Dict[str, Any]:
        """发起聚集协作"""
        from engine.ant_colony.antenna_signal import aggregate_signal
        sig = aggregate_signal(
            sender="CLI",
            topic=topic,
            participants=[],
        )
        ok = self.bus.send(sig)
        return {"ok": ok, "signal_id": sig.signal_id[:16],
                "participants": len(self.bus.modules)}

    def get_metrics(self) -> Dict[str, Any]:
        """获取完整运行时指标"""
        s = self.snapshot()
        return {
            "tick": s.tick_count,
            "emergence": {
                "E": round(s.emergence_E, 4),
                "grade": s.emergence_grade,
            },
            "signals": {
                "sent": s.total_signals_sent,
                "blocked": s.total_signals_blocked,
            },
            "pheromones": {
                "trails": s.pheromone_trails,
                "concentration": s.pheromone_concentration,
            },
            "populations": s.population_distribution,
            "top_paths": s.top_paths,
            "recent_events": self._event_log[-10:],
            "dna": DNA,
        }

    def get_health(self) -> Dict[str, Any]:
        """健康检查端点用"""
        s = self.snapshot()
        status = "🟢"
        if s.total_signals_blocked > s.total_signals_sent * 0.5:
            status = "🔴"
        elif s.emergence_E < 0.1:
            status = "🟡"
        return {
            "status": status,
            "service": "ant_colony_runtime",
            "uptime_ticks": s.tick_count,
            "emergence_E": round(s.emergence_E, 4),
            "active_modules": s.active_modules,
            "dna": DNA,
            "timestamp": s.timestamp,
        }


# ═══════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════

_runtime: Optional[AntColonyRuntime] = None
_runtime_lock = threading.Lock()


def get_runtime(auto_start: bool = False, verbose: bool = False) -> AntColonyRuntime:
    """获取全局蚁群运行时单例"""
    global _runtime
    with _runtime_lock:
        if _runtime is None:
            _runtime = AntColonyRuntime(verbose=verbose)
        if auto_start and not _runtime.is_running:
            _runtime.start()
    return _runtime


def stop_runtime():
    global _runtime
    with _runtime_lock:
        if _runtime and _runtime.is_running:
            _runtime.stop()


# ═══════════════════════════════════════════════
# 钩子函数（对接 lh_unified_hook.py）
# ═══════════════════════════════════════════════

def ant_colony_pre_audit_hook(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """蚁群预审计钩子 — 对输入内容进行蚁群感知评估"""
    try:
        runtime = get_runtime()
        content = ctx.get("content", "")[:200]
        if content:
            from engine.ant_colony.antenna_signal import trail_signal
            sig = trail_signal(
                sender="hook_pre_audit",
                receiver="scout_pool",
                trail_type="audit",
                path_data={"content": content, "source": ctx.get("source", "")},
            )
            runtime.bus.send(sig)
        return {"engine": "ant_colony", "action": "pre_audit", 
                "emergence_E": runtime.snapshot().emergence_E}
    except Exception as e:
        return {"engine": "ant_colony", "status": "offline", "error": str(e)}


def ant_colony_on_complete_hook(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """蚁群完成钩子 — 执行后更新信息素轨迹"""
    try:
        runtime = get_runtime()
        state = runtime.snapshot()
        return {
            "engine": "ant_colony",
            "action": "on_complete",
            "emergence_E": round(state.emergence_E, 4),
            "grade": state.emergence_grade,
        }
    except Exception as e:
        return {"engine": "ant_colony", "status": "offline", "error": str(e)}


def ant_colony_lifecycle_hook(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """蚁群生命周期钩子 — 全局事件监听"""
    try:
        runtime = get_runtime()
        stats = runtime.pheromone_system.get_stats()
        # 计算当前告警级别：ALERT 路径的平均强度
        alert_paths = runtime.pheromone_system.get_paths_by_type(PheromoneType.ALERT)
        alert_level = sum(s for _, s in alert_paths) / max(len(alert_paths), 1)
        return {
            "engine": "ant_colony",
            "tick": runtime._tick_count,
            "trails": stats.get("total_trails", 0),
            "alert_level": round(alert_level, 1),
        }
    except Exception as e:
        return {"engine": "ant_colony", "status": "offline", "error": str(e)}


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐜 龙魂蚁群运行时")
    parser.add_argument("--start", action="store_true", help="启动后台运行时")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--metrics", action="store_true", help="完整指标")
    parser.add_argument("--tick", type=int, default=0, help="手动 tick N 次后查看状态")
    parser.add_argument("--task", type=str, help="发送任务到蚁群")
    parser.add_argument("--alert", type=str, help="模拟安全告警")
    parser.add_argument("--aggregate", type=str, help="发起聚集协作")
    parser.add_argument("--stop", action="store_true", help="停止运行时")
    parser.add_argument("--health", action="store_true", help="健康检查 (JSON)")
    args = parser.parse_args()

    runtime = get_runtime()

    if args.start:
        runtime.start()
        print(f"\n  ✅ 蚁群运行时已启动")
        print(f"     初始状态:\n{runtime.snapshot().summary()}")
        print(f"\n  📡 按 Ctrl+C 停止\n")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            runtime.stop()

    elif args.stop:
        runtime.stop()

    elif args.status:
        if not runtime.is_running:
            runtime.start()
            time.sleep(1)
        print(f"\n{runtime.snapshot().summary()}\n")

    elif args.metrics:
        if not runtime.is_running:
            runtime.start()
            time.sleep(1)
        metrics = runtime.get_metrics()
        print(json.dumps(metrics, indent=2, ensure_ascii=False))

    elif args.tick > 0:
        runtime.start()
        for i in range(args.tick):
            runtime.tick()
            if (i + 1) % 10 == 0:
                print(f"  tick {i+1}/{args.tick}...")
            time.sleep(0.1)
        print(f"\n  ✅ {args.tick} 次 tick 完成\n")
        print(runtime.snapshot().summary())
        runtime.stop()

    elif args.task:
        runtime.start()
        print(f"\n  📤 发送任务: {args.task[:50]}...")
        result = runtime.send_task(args.task)
        print(f"  {'✅' if result['ok'] else '❌'} {result}")
        time.sleep(1)
        print(f"\n{runtime.snapshot().summary()}")

    elif args.alert:
        runtime.start()
        print(f"\n  🚨 模拟告警: {args.alert[:50]}...")
        result = runtime.simulate_alert(args.alert)
        print(f"  {'✅' if result['ok'] else '❌'} {result}")
        time.sleep(1)
        print(f"\n{runtime.snapshot().summary()}")

    elif args.aggregate:
        runtime.start()
        print(f"\n  🐝 发起聚集: {args.aggregate[:50]}...")
        result = runtime.broadcast_aggregate(args.aggregate)
        print(f"  {'✅' if result['ok'] else '❌'} 参与模块: {result['participants']}")
        time.sleep(1)
        print(f"\n{runtime.snapshot().summary()}")

    elif args.health:
        if not runtime.is_running:
            runtime.start()
            time.sleep(1)
        print(json.dumps(runtime.get_health(), ensure_ascii=False))

    else:
        print(runtime.snapshot().summary())
        print(f"\n  用法: python3 engine/ant_colony/runtime.py --start|--status|--metrics|...")
        print(f"  快捷: python3 bin/lh_ant_colony_daemon.py")


if __name__ == "__main__":
    main()
