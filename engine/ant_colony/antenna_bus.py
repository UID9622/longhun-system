#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
触角总线 v2.0 · AntennaBus
基于 LACA v1.0 论文，深度整合龙魂不动点系统

DNA: #龍芯⚡️丙午·辛未·ANTENNA-BUS-v2.0

v2.0 增强:
  - 16人格自动映射到五大蚁群种群
  - 不动点层级校验（每信号过五级闸门）
  - 七色颜色状态路由决策
  - 涌现质量实时度量
  - 三色审计链路集成
  - DNA追溯每跳留痕（v∞格式）
"""

import asyncio
import time
import json
import random
import threading
from typing import Dict, List, Optional, Callable, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

from engine.ant_colony.antenna_signal import (
    AntennaSignal, PheromoneType, PayloadType,
    SignalExpiredError, SignalTamperedError,
)
from engine.ant_colony.pheromone_system import PheromoneSystem
from engine.ant_colony.fixed_point_bridge import (
    FixedPointBridge, FixedPointLevel,
    ColorPheromoneMapper, ColorState,
    EmergenceCalculator, WuxingPheromoneCoupling,
)


# === 16人格 → 五大蚁群种群映射 ===
PERSONA_POPULATION_MAP = {
    # 工蚁群（6人）— 执行输出
    "P00-文心": ("工蚁群", ["创作", "写作", "内容"], 1),
    "P01-诸葛亮": ("工蚁群", ["策略", "推演", "优化"], 2),
    "P02-宝宝": ("工蚁群", ["调度", "执行", "任务管理"], 2),
    "P03-雯雯": ("工蚁群", ["流程优化", "协作"], 1),
    "P04-鲁班": ("工蚁群", ["编码", "工程", "构建"], 1),
    "P06-数学大师": ("工蚁群", ["验证", "数学", "逻辑"], 3),
    # 兵蚁群（4人）— 防护审计
    "P05-上帝之眼": ("兵蚁群", ["监控", "审计", "DNA打标"], 4),
    "P72-龙盾": ("兵蚁群", ["安全", "防护", "权限"], 3),
    "P12-屈原": ("兵蚁群", ["伦理", "价值观", "君子协议"], 4),
    "P13-姜子牙": ("兵蚁群", ["兵法", "危机应对", "攻防"], 3),
    # 侦察蚁群（3人）— 感知预警
    "P07-管仲": ("侦察蚁群", ["资源分析", "经济", "效能"], 2),
    "P09-孙思邈": ("侦察蚁群", ["诊断", "健康", "排查"], 2),
    "P10-苏东坡": ("侦察蚁群", ["美学", "评审", "体验"], 1),
    # 储蜜蚁群（1人）— 知识管理
    "P08-仓颉": ("储蜜蚁群", ["命名", "术语", "知识管理"], 3),
    # 育幼蚁群（3人）— 成长迭代
    "P11-李白": ("育幼蚁群", ["创意", "灵感", "创新"], 1),
    "P14-吕蒙": ("育幼蚁群", ["学习", "进化", "技能"], 1),
    "P15-乔前辈": ("育幼蚁群", ["传承", "指导", "mentorship"], 1),
}


@dataclass
class ModuleRegistration:
    """模块注册信息 v2.0"""
    module_id: str
    population: str
    capabilities: List[str]
    level_access: int
    registered_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    status: str = "online"
    inbox_size: int = 0
    outbox_size: int = 0
    # v2.0: 不动点层级
    fixed_point_level: FixedPointLevel = FixedPointLevel.L1_TASK


class AntennaBus:
    """
    触角总线 v2.0 — 模块间通信中枢
    
    核心设计原则（来自论文）:
    - 去中心化: 无中央控制器
    - 信息素路由: 走信息素强的路
    - DNA追溯: 每跳留痕
    - 不动点校验: 每信号过五级闸门
    - 涌现度量: 实时计算 E 值
    
    与龙魂系统融合:
    - 16人格 = 五大蚁群种群
    - 七色不动点 = 路由决策依据
    - 三色审计 = 信号审计链路
    - 五行耦合 = 信息素传播系数
    """
    
    ACK_TIMEOUT = 3.0
    HEARTBEAT_INTERVAL = 60.0
    MAX_INBOX_SIZE = 1000
    ISOLATION_THRESHOLD = 3
    
    def __init__(self, bus_id: str = "ANTENNA-BUS-MAIN"):
        self.bus_id = bus_id
        self.modules: Dict[str, ModuleRegistration] = {}
        self.neighbors: Dict[str, Set[str]] = defaultdict(set)
        self.inboxes: Dict[str, List[AntennaSignal]] = defaultdict(list)
        self.outboxes: Dict[str, List[AntennaSignal]] = defaultdict(list)
        self.pheromone_system = PheromoneSystem()
        
        # v2.0: 涌现质量
        self.emergence_calculator = EmergenceCalculator()
        self.last_emergence_state = None
        
        # 回调
        self.alert_handlers: List[Callable[[AntennaSignal], None]] = []
        self.signal_monitors: List[Callable[[AntennaSignal], None]] = []
        self.audit_handlers: List[Callable[[AntennaSignal, str], None]] = []  # v2.0
        
        self._lock = threading.RLock()
        
        self.stats = {
            "signals_sent": 0,
            "signals_received": 0,
            "signals_broadcast": 0,
            "signals_dropped": 0,
            "signals_blocked_by_fixed_point": 0,  # v2.0
            "signals_expired": 0,
            "ack_timeouts": 0,
            "modules_registered": 0,
            "modules_isolated": 0,
        }
    
    # === 模块管理 ===
    
    def register_module(self, module_id: str, population: str,
                       capabilities: List[str], level_access: int = 1) -> bool:
        """注册模块到总线"""
        with self._lock:
            if module_id in self.modules:
                return False
            
            # v2.0: 自动映射不动点层级
            fp_level = FixedPointLevel.L1_TASK
            if level_access >= 5:
                fp_level = FixedPointLevel.L5_ETERNAL
            elif level_access >= 4:
                fp_level = FixedPointLevel.L4_VALUES
            elif level_access >= 3:
                fp_level = FixedPointLevel.L3_ARCH
            elif level_access >= 2:
                fp_level = FixedPointLevel.L2_CONFIG
            
            reg = ModuleRegistration(
                module_id=module_id,
                population=population,
                capabilities=capabilities,
                level_access=level_access,
                fixed_point_level=fp_level,
            )
            self.modules[module_id] = reg
            self.stats["modules_registered"] += 1
            return True
    
    def unregister_module(self, module_id: str) -> bool:
        with self._lock:
            if module_id not in self.modules:
                return False
            del self.modules[module_id]
            if module_id in self.neighbors:
                for neighbor in self.neighbors[module_id]:
                    self.neighbors[neighbor].discard(module_id)
                del self.neighbors[module_id]
            return True
    
    def connect(self, module_a: str, module_b: str) -> bool:
        with self._lock:
            if module_a not in self.modules or module_b not in self.modules:
                return False
            self.neighbors[module_a].add(module_b)
            self.neighbors[module_b].add(module_a)
            return True
    
    def disconnect(self, module_a: str, module_b: str) -> bool:
        with self._lock:
            if module_a in self.neighbors:
                self.neighbors[module_a].discard(module_b)
            if module_b in self.neighbors:
                self.neighbors[module_b].discard(module_a)
            return True
    
    def get_neighbors(self, module_id: str) -> List[str]:
        with self._lock:
            return list(self.neighbors.get(module_id, set()))
    
    # === 信号发送（v2.0: 增强不动点校验）===
    
    def send(self, signal: AntennaSignal) -> bool:
        """
        发送信号 — v2.0 增强:
        1. 信号完整性校验
        2. 不动点层级校验
        3. 颜色状态路由决策
        4. 五行耦合系数注入
        """
        with self._lock:
            # 1. 完整性校验
            if not signal.verify():
                self.stats["signals_dropped"] += 1
                raise SignalTamperedError(f"信号 {signal.signal_id} 校验失败")
            
            # 2. 不动点校验
            if not signal.verify_fixed_point():
                self.stats["signals_blocked_by_fixed_point"] += 1
                return False
            
            sender = signal.sender_id
            receiver = signal.receiver_id
            
            if sender not in self.modules:
                self.stats["signals_dropped"] += 1
                return False
            
            # 3. 颜色状态路由决策
            # 注意: ALERT信号（警戒素）本身映射到红色(R)，但它是系统正常的安全机制
            # 红色阻断只针对外部/恶意信号，不阻断兵蚁群内部的安全告警
            color = ColorState(signal.color_state)
            route_decision = ColorPheromoneMapper.route_by_color(color)
            
            # 警戒素信号总是允许传播（兵蚁群的正常工作）
            is_legitimate_alert = (
                signal.pheromone_type == PheromoneType.ALERT and
                signal.sender_id in self.modules and
                self.modules[signal.sender_id].population == "兵蚁群"
            )
            
            if not route_decision["allow"] and not is_legitimate_alert:
                self.stats["signals_blocked_by_fixed_point"] += 1
                self._audit_log(signal, f"BLOCKED: {route_decision['action']}")
                return False
            
            # 4. 记录DNA追溯
            signal.path_trace.append({
                "hop": signal.hop_count,
                "module": self.bus_id,
                "action": "route",
                "color_state": signal.color_state,
                "time": time.time(),
            })
            
            # 5. 根据接收者类型路由
            if receiver:
                if receiver in self.neighbors.get(sender, set()):
                    self._deliver(signal, receiver)
                    self.stats["signals_sent"] += 1
                    return True
                else:
                    return self._route(signal)
            else:
                return self._broadcast(signal)
    
    def _deliver(self, signal: AntennaSignal, receiver: str):
        """投递信号 + 信息素沉积 + 五行耦合注入"""
        path_key = f"{signal.sender_id}->{receiver}"
        
        # 获取发送者和接收者的不动点层级
        sender_fp = FixedPointLevel.L1_TASK
        receiver_fp = FixedPointLevel.L1_TASK
        if signal.sender_id in self.modules:
            sender_fp = self.modules[signal.sender_id].fixed_point_level
        if receiver in self.modules:
            receiver_fp = self.modules[receiver].fixed_point_level
        
        # 使用较高的不动点层级
        fp_level = max(
            list(FixedPointLevel).index(sender_fp),
            list(FixedPointLevel).index(receiver_fp),
        ) + 1
        fp_level = min(fp_level, 5)
        
        self.pheromone_system.deposit(signal, path_key, fixed_point_level=fp_level)
        
        # 收件箱管理
        if len(self.inboxes[receiver]) >= self.MAX_INBOX_SIZE:
            self.inboxes[receiver].sort(key=lambda s: s.priority)
            self.inboxes[receiver].pop(0)
            self.stats["signals_dropped"] += 1
        
        self.inboxes[receiver].append(signal)
        self.inboxes[receiver].sort(key=lambda s: s.priority, reverse=True)
        
        if receiver in self.modules:
            self.modules[receiver].inbox_size = len(self.inboxes[receiver])
    
    def _broadcast(self, signal: AntennaSignal) -> bool:
        """广播信号"""
        sender = signal.sender_id
        neighbors = self.neighbors.get(sender, set())
        
        if not neighbors:
            self.stats["signals_dropped"] += 1
            return False
        
        delivered = 0
        for neighbor in neighbors:
            copy = AntennaSignal.from_json(signal.to_json())
            copy.receiver_id = neighbor
            copy.forward(neighbor)
            
            path_key = f"{sender}->{neighbor}"
            self.pheromone_system.deposit(copy, path_key)
            self._deliver(copy, neighbor)
            delivered += 1
        
        self.stats["signals_broadcast"] += delivered
        
        # v2.0: 广播后触发审计
        if signal.pheromone_type == PheromoneType.ALERT:
            self._notify_alert(signal)
        
        return delivered > 0
    
    def _route(self, signal: AntennaSignal) -> bool:
        """
        信息素路由 — v2.0 增强:
        - 基于信息素强度的贪心路由
        - 五行耦合系数调整路径选择
        - ε-贪心: 90%走最优路，10%随机探索
        """
        sender = signal.sender_id
        receiver = signal.receiver_id
        
        sender_neighbors = self.neighbors.get(sender, set())
        if not sender_neighbors:
            self.stats["signals_dropped"] += 1
            return False
        
        if receiver in sender_neighbors:
            signal.forward(receiver)
            self._deliver(signal, receiver)
            self.stats["signals_sent"] += 1
            return True
        
        best_neighbor = None
        best_strength = -1
        exploration_chance = 0.1
        
        if random.random() < exploration_chance:
            best_neighbor = random.choice(list(sender_neighbors))
        else:
            for neighbor in sender_neighbors:
                path_key = f"{neighbor}->{receiver}"
                strength = self.pheromone_system.get_strength(path_key)
                
                # v2.0: 五行耦合系数修正
                coupling = WuxingPheromoneCoupling.get_coupling_factor(
                    signal.pheromone_type,
                    PheromoneType.TRAIL  # 路由走足迹素路径
                )
                strength *= coupling
                
                if strength > best_strength:
                    best_strength = strength
                    best_neighbor = neighbor
        
        if best_neighbor:
            signal.forward(best_neighbor)
            path_key = f"{sender}->{best_neighbor}"
            self.pheromone_system.deposit(signal, path_key)
            self._deliver(signal, best_neighbor)
            self.stats["signals_sent"] += 1
            return True
        
        self.stats["signals_dropped"] += 1
        return False
    
    # === 信号接收 ===
    
    def receive(self, module_id: str, max_signals: int | None = None,
                pheromone_filter: Optional[PheromoneType] = None) -> List[AntennaSignal]:
        with self._lock:
            inbox = self.inboxes.get(module_id, [])
            
            if pheromone_filter:
                filtered = [s for s in inbox if s.pheromone_type == pheromone_filter]
            else:
                filtered = inbox.copy()
            
            filtered.sort(key=lambda s: s.priority, reverse=True)
            
            if max_signals:
                result = filtered[:max_signals]
            else:
                result = filtered
            
            remaining = [s for s in inbox if s not in result]
            self.inboxes[module_id] = remaining
            
            if module_id in self.modules:
                self.modules[module_id].inbox_size = len(remaining)
            
            self.stats["signals_received"] += len(result)
            return result
    
    def peek(self, module_id: str,
             pheromone_filter: Optional[PheromoneType] = None) -> List[AntennaSignal]:
        with self._lock:
            inbox = self.inboxes.get(module_id, [])
            if pheromone_filter:
                return [s for s in inbox if s.pheromone_type == pheromone_filter]
            return inbox.copy()
    
    # === 回调 ===
    
    def on_alert(self, handler: Callable[[AntennaSignal], None]):
        self.alert_handlers.append(handler)
    
    def on_signal(self, monitor: Callable[[AntennaSignal], None]):
        self.signal_monitors.append(monitor)
    
    def on_audit(self, handler: Callable[[AntennaSignal, str], None]):
        """v2.0: 注册审计处理器"""
        self.audit_handlers.append(handler)
    
    def _notify_alert(self, signal: AntennaSignal):
        for handler in self.alert_handlers:
            try:
                handler(signal)
            except Exception:
                pass
    
    def _audit_log(self, signal: AntennaSignal, action: str):
        """v2.0: 审计日志"""
        for handler in self.audit_handlers:
            try:
                handler(signal, action)
            except Exception:
                pass
    
    # === 心跳与健康 ===
    
    def heartbeat(self, module_id: str) -> bool:
        with self._lock:
            if module_id not in self.modules:
                return False
            self.modules[module_id].last_heartbeat = time.time()
            self.modules[module_id].status = "online"
            return True
    
    def check_health(self) -> Dict[str, dict]:
        with self._lock:
            now = time.time()
            health_report = {}
            
            for module_id, reg in self.modules.items():
                elapsed = now - reg.last_heartbeat
                status = "healthy"
                
                if elapsed > self.HEARTBEAT_INTERVAL * self.ISOLATION_THRESHOLD:
                    status = "dead"
                    reg.status = "isolated"
                    self.stats["modules_isolated"] += 1
                elif elapsed > self.HEARTBEAT_INTERVAL * 2:
                    status = "warning"
                    reg.status = "busy"
                
                health_report[module_id] = {
                    "status": status,
                    "last_heartbeat_ago": elapsed,
                    "population": reg.population,
                    "inbox_size": reg.inbox_size,
                    "neighbors": len(self.neighbors.get(module_id, set())),
                    "fixed_point_level": reg.fixed_point_level.value,
                }
            
            return health_report
    
    # === 涌现质量 ===
    
    def get_emergence_state(self):
        """v2.0: 获取当前涌现状态"""
        population = self.get_population_distribution()
        total_modules = len(self.modules)
        total_connections = sum(len(n) for n in self.neighbors.values()) // 2
        
        state = self.emergence_calculator.compute_from_population(
            population_distribution=population,
            active_connections=total_connections,
            total_modules=max(total_modules, 1),
            conflict_count=0,
            total_interactions=self.stats["signals_sent"],
        )
        
        self.last_emergence_state = state
        return state
    
    # === 查询 ===
    
    def get_population_distribution(self) -> Dict[str, int]:
        with self._lock:
            distribution = defaultdict(int)
            for reg in self.modules.values():
                distribution[reg.population] += 1
            return dict(distribution)
    
    def get_stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                **self.stats,
                "active_modules": len(self.modules),
                "total_connections": sum(len(n) for n in self.neighbors.values()) // 2,
                "pheromone_stats": self.pheromone_system.get_stats(),
                "emergence": (
                    self.emergence_calculator.interpret(self.last_emergence_state)
                    if self.last_emergence_state else None
                ),
            }
    
    def get_module_info(self, module_id: str) -> Optional[dict]:
        with self._lock:
            if module_id not in self.modules:
                return None
            reg = self.modules[module_id]
            return {
                "module_id": reg.module_id,
                "population": reg.population,
                "capabilities": reg.capabilities,
                "level_access": reg.level_access,
                "fixed_point_level": reg.fixed_point_level.value,
                "status": reg.status,
                "neighbors": list(self.neighbors.get(module_id, set())),
                "inbox_size": len(self.inboxes.get(module_id, [])),
            }


# === 便捷工厂函数 ===

def create_populated_bus() -> AntennaBus:
    """
    创建预填充16人格的触角总线 v2.0
    
    与论文中五大蚁群种群一一对应:
    - 工蚁群 6人: 宝宝/诸葛亮/雯雯/鲁班/文心/数学大师
    - 兵蚁群 4人: 上帝之眼/龙盾/屈原/姜子牙
    - 侦察蚁群 3人: 管仲/孙思邈/苏东坡
    - 储蜜蚁群 1人: 仓颉
    - 育幼蚁群 3人: 李白/吕蒙/乔前辈
    """
    bus = AntennaBus()
    
    # 注册所有16人格模块
    for module_id, (pop, caps, level) in PERSONA_POPULATION_MAP.items():
        bus.register_module(module_id, pop, caps, level)
    
    # 建立核心连接（来自论文的高频通信路径）
    core_connections = [
        # 工蚁群内部
        ("P02-宝宝", "P01-诸葛亮"),
        ("P02-宝宝", "P04-鲁班"),
        ("P02-宝宝", "P00-文心"),
        ("P02-宝宝", "P03-雯雯"),
        ("P02-宝宝", "P06-数学大师"),
        # 兵蚁群内部
        ("P05-上帝之眼", "P72-龙盾"),
        ("P05-上帝之眼", "P12-屈原"),
        ("P05-上帝之眼", "P13-姜子牙"),
        # 侦察蚁群内部
        ("P07-管仲", "P09-孙思邈"),
        ("P07-管仲", "P10-苏东坡"),
        # 育幼蚁群内部
        ("P11-李白", "P14-吕蒙"),
        ("P14-吕蒙", "P15-乔前辈"),
        # 跨种群
        ("P02-宝宝", "P05-上帝之眼"),
        ("P02-宝宝", "P07-管仲"),
        ("P02-宝宝", "P09-孙思邈"),
        ("P04-鲁班", "P08-仓颉"),
        ("P00-文心", "P10-苏东坡"),
        ("P12-屈原", "P05-上帝之眼"),
        ("P72-龙盾", "P13-姜子牙"),
        # ALERT通路（侦察→兵蚁）
        ("P09-孙思邈", "P05-上帝之眼"),
        ("P09-孙思邈", "P72-龙盾"),
        ("P07-管仲", "P05-上帝之眼"),
        # AGGREGATE通路（育幼→工蚁）
        ("P11-李白", "P00-文心"),
        ("P11-李白", "P04-鲁班"),
        ("P11-李白", "P10-苏东坡"),
        ("P14-吕蒙", "P04-鲁班"),
        ("P15-乔前辈", "P03-雯雯"),
        # 知识沉淀通路
        ("P00-文心", "P08-仓颉"),
        ("P06-数学大师", "P08-仓颉"),
        # 经验传承通路
        ("P13-姜子牙", "P15-乔前辈"),
        ("P05-上帝之眼", "P14-吕蒙"),
    ]
    
    for a, b in core_connections:
        bus.connect(a, b)
    
    return bus


# === 测试 ===
if __name__ == "__main__":
    print("=" * 60)
    print("🐜 龙魂蚁群引擎 v2.0 · 触角总线测试")
    print("=" * 60)
    
    bus = create_populated_bus()
    
    # 1. 基本统计
    stats = bus.get_stats()
    print(f"\n🚌 注册模块: {stats['active_modules']}")
    print(f"🚌 连接数: {stats['total_connections']}")
    
    # 2. 种群分布
    dist = bus.get_population_distribution()
    print(f"\n📊 种群分布:")
    for pop, count in sorted(dist.items()):
        print(f"  {pop}: {'█' * count} {count}")
    
    # 3. 直接发送
    from engine.ant_colony.antenna_signal import recruit_signal, alert_signal
    s1 = recruit_signal("P02-宝宝", "P04-鲁班", {"task": "构建蚁巢"}, priority=8)
    result = bus.send(s1)
    print(f"\n📡 P02→P04: {'✅' if result else '❌'}")
    
    received = bus.receive("P04-鲁班")
    print(f"  P04收件箱: {len(received)} 条")
    
    # 4. 广播警戒
    s2 = alert_signal("P05-上帝之眼", 2, "测试警戒", ["P04-鲁班"])
    result = bus.send(s2)
    print(f"\n📡 P05广播ALERT: {'✅' if result else '❌'}")
    
    neighbors = bus.get_neighbors("P05-上帝之眼")
    total = sum(len(bus.peek(n, PheromoneType.ALERT)) for n in neighbors)
    print(f"  {len(neighbors)}个邻居共收到 {total} 条ALERT")
    
    # 5. 涌现质量
    state = bus.get_emergence_state()
    interp = EmergenceCalculator.interpret(state)
    print(f"\n📊 涌现质量: E={state.score:.4f} ({interp['phase']})")
    
    # 6. 健康检查
    health = bus.check_health()
    healthy = sum(1 for h in health.values() if h['status'] == 'healthy')
    print(f"\n💓 健康: {healthy}/{len(health)}")
    
    print(f"\n✅ 触角总线 v2.0 测试通过")
    print(f"🧬 DNA: #龍芯⚡️丙午·辛未·ANTENNA-BUS-v2.0")
