#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 事件总线引擎 v1.0 (Event Bus Engine)
================================================
投喂落地：CNSH Runtime Governance Mathematics · Event Bus

事件流拓扑：
  INPUT → EventBus → AuditEngine → ExecutionEngine → ArchiveEngine

事件格式：{event, dna, timestamp, source, payload}

DNA: #龍芯⚡️丙午·乙未·己未·申时·履-EVENT-BUS-v1.0-M1N2O3P4
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import os
import sys
import uuid
import hashlib
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict


EVENT_BUS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "event_bus")
os.makedirs(EVENT_BUS_DIR, exist_ok=True)


class EventType(Enum):
    """事件类型"""
    INPUT_ACCEPTED = "INPUT_ACCEPTED"
    INPUT_REJECTED = "INPUT_REJECTED"
    AUDIT_STARTED = "AUDIT_STARTED"
    AUDIT_PASSED = "AUDIT_PASSED"
    AUDIT_FAILED = "AUDIT_FAILED"
    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    FUSE_TRIGGERED = "FUSE_TRIGGERED"
    SNAPSHOT_CREATED = "SNAPSHOT_CREATED"
    RECOVERY_STARTED = "RECOVERY_STARTED"
    RECOVERY_COMPLETED = "RECOVERY_COMPLETED"
    ARCHIVE_COMPLETED = "ARCHIVE_COMPLETED"
    DUAL_BRAIN_STARTED = "DUAL_BRAIN_STARTED"
    DUAL_BRAIN_COMPLETED = "DUAL_BRAIN_COMPLETED"
    MOD9_DECISION = "MOD9_DECISION"
    CHAIN_STEP = "CHAIN_STEP"
    PERSONA_ROUTED = "PERSONA_ROUTED"
    HOOK_TRIGGERED = "HOOK_TRIGGERED"


@dataclass
class Event:
    """事件对象"""
    event_id: str
    event_type: EventType
    timestamp: str
    source: str           # 来源模块
    dna_trace: str
    payload: Dict = field(default_factory=dict)
    parent_event_id: str = ""  # 父事件（因果链）


@dataclass
class EventSubscription:
    """事件订阅"""
    subscriber_id: str
    event_types: List[EventType]
    callback: str         # 回调模块名（实际使用时会转为可调用对象）
    priority: int = 0
    filter_fn: Optional[str] = None


class EventBus:
    """
    事件总线引擎
    
    特性：
    - 发布/订阅模式
    - 事件因果链（parent_event_id）
    - append-only 事件日志
    - 按优先级分发
    - 事件回放
    """

    def __init__(self):
        self.subscriptions: Dict[str, EventSubscription] = {}
        self.event_log: List[Event] = []
        self.callbacks: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._load_log()

    def _load_log(self):
        log_file = os.path.join(EVENT_BUS_DIR, "event_log.jsonl")
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            self.event_log.append(Event(
                                event_id=data.get('event_id', ''),
                                event_type=EventType(data['event_type']),
                                timestamp=data.get('timestamp', ''),
                                source=data.get('source', ''),
                                dna_trace=data.get('dna_trace', ''),
                                payload=data.get('payload', {}),
                                parent_event_id=data.get('parent_event_id', ''),
                            ))
                        except (json.JSONDecodeError, ValueError):
                            pass

    def _save_event(self, event: Event):
        log_file = os.path.join(EVENT_BUS_DIR, "event_log.jsonl")
        with open(log_file, 'a', encoding='utf-8') as f:
            d = asdict(event)
            d['event_type'] = event.event_type.value
            f.write(json.dumps(d, ensure_ascii=False) + '\n')

    def subscribe(self, subscriber_id: str, event_types: List[EventType],
                  callback: str, priority: int = 0, filter_fn: Optional[str] = None):
        """订阅事件"""
        with self._lock:
            self.subscriptions[subscriber_id] = EventSubscription(
                subscriber_id=subscriber_id,
                event_types=event_types,
                callback=callback,
                priority=priority,
                filter_fn=filter_fn,
            )

    def unsubscribe(self, subscriber_id: str):
        """取消订阅"""
        with self._lock:
            self.subscriptions.pop(subscriber_id, None)

    def register_callback(self, name: str, fn: Callable):
        """注册回调函数"""
        self.callbacks[name] = fn

    def publish(self, event_type: EventType, source: str, dna_trace: str = "",
                payload: Optional[Dict] = None, parent_event_id: str = "") -> Event:
        """
        发布事件
        
        返回: Event对象
        """
        event = Event(
            event_id=f"EVT-{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source=source,
            dna_trace=dna_trace or f"#龍芯⚡️丙午·乙未·己未·申时·履-EVT-{uuid.uuid4().hex[:8]}",
            payload=payload or {},
            parent_event_id=parent_event_id,
        )

        # 保存事件
        self._save_event(event)
        self.event_log.append(event)

        # 分发事件
        self._dispatch(event)

        return event

    def _dispatch(self, event: Event):
        """按优先级分发事件给订阅者"""
        matching = []
        for sub in self.subscriptions.values():
            if event.event_type in sub.event_types:
                matching.append(sub)

        # 按优先级排序
        matching.sort(key=lambda s: s.priority, reverse=True)

        for sub in matching:
            if sub.callback in self.callbacks:
                try:
                    self.callbacks[sub.callback](event)
                except Exception as e:
                    # 记录分发失败但不中断其他订阅者
                    error_event = Event(
                        event_id=f"EVT-ERR-{uuid.uuid4().hex[:8]}",
                        event_type=EventType.EXECUTION_FAILED,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        source="EventBus",
                        dna_trace="",
                        payload={"error": str(e), "callback": sub.callback, "original_event": event.event_id},
                    )
                    self._save_event(error_event)
                    self.event_log.append(error_event)

    def get_event_chain(self, event_id: str) -> List[Event]:
        """获取事件的因果链（从根事件到目标事件）"""
        chain = []
        current_id = event_id
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            found = None
            for e in self.event_log:
                if e.event_id == current_id:
                    chain.insert(0, e)
                    current_id = e.parent_event_id
                    found = True
                    break
            if not found:
                break

        return chain

    def query_events(self, event_type: Optional[EventType] = None,
                     source: Optional[str] = None,
                     limit: int = 50) -> List[Event]:
        """查询事件"""
        results = self.event_log
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if source:
            results = [e for e in results if e.source == source]
        return results[-limit:]

    def replay(self, from_index: int = 0) -> List[Event]:
        """事件回放"""
        return self.event_log[from_index:]

    def stats(self) -> Dict[str, Any]:
        """事件总线统计"""
        type_counts = defaultdict(int)
        source_counts = defaultdict(int)
        for e in self.event_log:
            type_counts[e.event_type.value] += 1
            source_counts[e.source] += 1

        return {
            "total_events": len(self.event_log),
            "subscribers": len(self.subscriptions),
            "callbacks_registered": len(self.callbacks),
            "event_type_distribution": dict(type_counts),
            "source_distribution": dict(source_counts),
            "latest_event": self.event_log[-1].event_id if self.event_log else None,
        }

    def visualize_flow(self, last_n: int = 10) -> str:
        """可视化事件流"""
        recent = self.event_log[-last_n:]
        lines = []
        for e in recent:
            indent = "  " if e.parent_event_id else ""
            arrow = "├─" if e.parent_event_id else "▶ "
            lines.append(f"{indent}{arrow} [{e.event_type.value}] {e.source} → {e.event_id[:12]}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 🧪 CLI 演示
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 70)
    print("🐉 龍魂 · 事件总线引擎 v1.0")
    print("=" * 70)

    bus = EventBus()

    # 注册回调
    def audit_handler(event: Event):
        print(f"   📋 [审计处理] 收到事件: {event.event_type.value} from {event.source}")

    def execution_handler(event: Event):
        print(f"   ⚙️ [执行处理] 收到事件: {event.event_type.value} from {event.source}")

    def fuse_handler(event: Event):
        print(f"   🚨 [熔断处理] 收到事件: {event.event_type.value} from {event.source}")

    bus.register_callback("audit_handler", audit_handler)
    bus.register_callback("execution_handler", execution_handler)
    bus.register_callback("fuse_handler", fuse_handler)

    # 订阅
    bus.subscribe("audit_system", [EventType.INPUT_ACCEPTED, EventType.AUDIT_STARTED, EventType.AUDIT_PASSED, EventType.AUDIT_FAILED], "audit_handler", priority=10)
    bus.subscribe("exec_system", [EventType.EXECUTION_STARTED, EventType.EXECUTION_COMPLETED, EventType.EXECUTION_FAILED], "execution_handler", priority=5)
    bus.subscribe("fuse_system", [EventType.FUSE_TRIGGERED], "fuse_handler", priority=1)

    # 模拟事件流
    print("\n📡 模拟事件流:")
    print("-" * 40)

    input_evt = bus.publish(EventType.INPUT_ACCEPTED, "InputGate", payload={"text": "审计系统安全"})
    audit_start = bus.publish(EventType.AUDIT_STARTED, "AuditEngine", parent_event_id=input_evt.event_id)
    audit_pass = bus.publish(EventType.AUDIT_PASSED, "AuditEngine", parent_event_id=audit_start.event_id)
    exec_start = bus.publish(EventType.EXECUTION_STARTED, "ExecutionEngine", parent_event_id=audit_pass.event_id)
    exec_done = bus.publish(EventType.EXECUTION_COMPLETED, "ExecutionEngine", parent_event_id=exec_start.event_id)
    archive = bus.publish(EventType.ARCHIVE_COMPLETED, "ArchiveEngine", parent_event_id=exec_done.event_id)

    # 模拟熔断
    bus.publish(EventType.FUSE_TRIGGERED, "RiskEngine", payload={"reason": "高风险检测", "risk_score": 0.85})

    print(f"\n{'='*70}")
    print("📊 事件流可视化:")
    print(f"{'='*70}")
    print(bus.visualize_flow(8))

    # 因果链
    print(f"\n{'='*70}")
    print("🔗 事件因果链 (exec_done):")
    print(f"{'='*70}")
    chain = bus.get_event_chain(exec_done.event_id)
    for e in chain:
        print(f"   → [{e.event_type.value}] {e.source}")

    stats = bus.stats()
    print(f"\n{'='*70}")
    print(f"📊 总线统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")

    return bus


if __name__ == "__main__":
    demo()
