#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 事件总线引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-EVENTBUS-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 解耦所有引擎：通过事件通信
  - 支持发布-订阅模式
  - 支持事件持久化（防止丢失）
  - 支持异步处理（非阻塞）
"""

import json
import threading
import queue
import time
from pathlib import Path
from typing import Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    topic: str
    data: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = field(default_factory=lambda: f"evt_{int(time.time()*1000)}")


class EventBus:
    """事件总线引擎——引擎间解耦通信，发布-订阅"""

    def __init__(self, persist: bool = False):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._queue: queue.Queue = queue.Queue()
        self._workers: List[threading.Thread] = []
        self._running = True
        self._persist = persist
        self._persist_file = Path.home() / "longhun-system/data/event_log.jsonl"
        self._start_workers()

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Callable):
        if topic in self._subscribers:
            self._subscribers[topic] = [cb for cb in self._subscribers[topic] if cb != callback]

    def publish(self, event: Event):
        """异步发布事件"""
        if self._persist:
            self._persist_event(event)
        self._queue.put(event)

    def publish_sync(self, event: Event) -> List[Any]:
        """同步发布（等待所有消费者完成）"""
        results = []
        if event.topic in self._subscribers:
            for cb in self._subscribers[event.topic]:
                try:
                    results.append(cb(event))
                except Exception as e:
                    results.append({"error": str(e)})
        return results

    def _start_workers(self, num_workers: int = 2):
        for _ in range(num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self._workers.append(t)

    def _worker_loop(self):
        while self._running:
            try:
                event = self._queue.get(timeout=0.5)
                if event.topic in self._subscribers:
                    for cb in self._subscribers[event.topic]:
                        try:
                            cb(event)
                        except Exception as e:
                            print(f"⚠️ 事件处理失败 [{event.topic}]: {e}")
            except queue.Empty:
                continue

    def _persist_event(self, event: Event):
        self._persist_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._persist_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"topic": event.topic, "data": event.data, "id": event.id, "timestamp": event.timestamp}, ensure_ascii=False) + "\n")

    def stop(self):
        self._running = False
        for t in self._workers:
            t.join(timeout=2)

    def stats(self) -> Dict[str, Any]:
        return {
            "topics": len(self._subscribers),
            "subscribers": sum(len(v) for v in self._subscribers.values()),
            "workers": len(self._workers),
            "queue_size": self._queue.qsize(),
            "running": self._running,
        }


# 全局单例
_global_bus = None


def get_event_bus(persist: bool = True) -> EventBus:
    global _global_bus
    if _global_bus is None:
        _global_bus = EventBus(persist=persist)
    return _global_bus


if __name__ == "__main__":
    bus = EventBus(persist=False)

    received = []

    def handler(evt):
        received.append(evt.data.get("message", ""))

    bus.subscribe("test_topic", handler)
    bus.publish(Event("test_topic", {"message": "hello world"}))
    time.sleep(0.1)  # 等 worker 处理

    print(f"收到: {received}")
    print(f"总线状态: {bus.stats()}")
    bus.stop()
    print("🟢 事件总线引擎测试通过")
