#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     ⚡ 龍魂 · 神经系统 · 信号中继站 v1.0                       ║
║                                                                  ║
║  生物映射：神经系统 → 信号传导 → 阈值告警/事件分发                 ║
║  五行归属：水                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·神经系统-SIGNAL-RELAY-v1.0               ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_signal_relay.py --dispatch    # 分派一次待处理信号
  python3 bin/lh_signal_relay.py --monitor     # 监测信号队列
  python3 bin/lh_signal_relay.py --listen      # 守护监听模式
"""

import hashlib
import json
import os
import sys
import time
import signal
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
SIGNAL_QUEUE = STATE_DIR / "signal_queue.jsonl"
SIGNAL_STATE = STATE_DIR / "signal_relay_state.json"
PHEROMONE_FILE = STATE_DIR / "pheromone_network.jsonl"

DNA = "#龍芯⚡️丙午·辛未·神经系统-SIGNAL-RELAY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


@dataclass
class Signal:
    """神经信号——一次告警/事件的传递"""
    signal_id: str
    signal_type: str        # alert / heartbeat / threshold / audit / persona
    source: str
    target: str
    priority: str           # P0/P1/P2/P3
    content: Dict[str, Any]
    intensity: float        # 0.0~1.0
    sent_at: str
    received_at: str = ""
    acknowledged: bool = False
    response_time_ms: float = 0
    ttl_minutes: int = 60


class SignalRelay:
    """神经系统中继站：接收→路由→转发→确认"""

    # 信号路由表：每条信号的终点
    ROUTE_TABLE = {
        "alert": ["rb_confrontation_engine", "audit_pipeline", "overseer"],
        "heartbeat": ["flow_pipeline", "colony_orchestrator"],
        "threshold": ["rb_confrontation_engine", "sentinel", "overseer"],
        "audit": ["audit_pipeline", "signing_engine", "archive"],
        "persona": ["persona_orchestrator", "signing_engine"],
    }

    # 信号优先级衰减表（超时未响应的降级）
    PRIORITY_TIMEOUT = {"P0": 5, "P1": 15, "P2": 30, "P3": 60}  # 分钟

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if SIGNAL_STATE.exists():
            return json.loads(SIGNAL_STATE.read_text())
        return {
            "signals_sent": 0,
            "signals_received": 0,
            "signals_dropped": 0,
            "avg_response_ms": 0,
            "latency_history": [],
            "last_dispatch": "",
        }

    def _save_state(self):
        SIGNAL_STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def emit(self, signal_type: str, source: str, priority: str,
             content: Dict[str, Any], intensity: float = 0.8,
             target: str = "auto") -> Signal:
        """发射一个神经信号"""
        if target == "auto":
            targets = self.ROUTE_TABLE.get(signal_type, ["colony_orchestrator"])
            target = targets[0]

        signal_id = hashlib.sha256(
            f"{source}-{signal_type}-{time.time()}".encode()
        ).hexdigest()[:12]

        s = Signal(
            signal_id=signal_id,
            signal_type=signal_type,
            source=source,
            target=target,
            priority=priority,
            content=content,
            intensity=intensity,
            sent_at=datetime.now().isoformat(),
        )

        # 写入信号队列
        with open(SIGNAL_QUEUE, "a") as f:
            f.write(json.dumps({
                "signal_id": s.signal_id,
                "type": s.signal_type,
                "source": s.source,
                "target": s.target,
                "priority": s.priority,
                "content": s.content,
                "intensity": s.intensity,
                "sent_at": s.sent_at,
            }, ensure_ascii=False) + "\n")

        self.state["signals_sent"] += 1
        self._save_state()
        return s

    def dispatch(self) -> Dict[str, Any]:
        """
        分派待处理信号到目标系统
        模拟神经递质释放到突触间隙
        """
        if not SIGNAL_QUEUE.exists():
            return {"dispatched": 0, "dropped": 0, "status": "队列空"}

        dispatched = 0
        dropped = 0
        now = datetime.now()
        remaining = []

        for line in SIGNAL_QUEUE.read_text().splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                sent_at = datetime.fromisoformat(record["sent_at"])
                elapsed = (now - sent_at).total_seconds() / 60  # 分钟

                # 超时检查
                timeout = self.PRIORITY_TIMEOUT.get(record["priority"], 60)
                if elapsed > timeout:
                    dropped += 1
                    self.state["signals_dropped"] += 1
                    # 死信记录到信息素网络
                    self._log_dead_letter(record, elapsed)
                    continue

                # 转发：写入目标系统的信息素
                self._forward_signal(record)
                dispatched += 1

            except Exception:
                dropped += 1
                continue

        self.state["last_dispatch"] = now.isoformat()
        self._save_state()

        return {
            "dispatched": dispatched,
            "dropped": dropped,
            "total_pending": dispatched + dropped,
            "dispatch_rate": round(dispatched / max(dispatched + dropped, 1), 2),
        }

    def _forward_signal(self, record: Dict[str, Any]):
        """将信号转发到目标系统"""
        # 写入信息素网络（所有目标系统监听此网络）
        with open(PHEROMONE_FILE, "a") as f:
            f.write(json.dumps({
                "id": record["signal_id"],
                "type": "alarm" if record["priority"] in ("P0", "P1") else "event",
                "source": f"signal_relay:{record['source']}",
                "target": record["target"],
                "intensity": record["intensity"],
                "content": {
                    "signal_type": record["type"],
                    "priority": record["priority"],
                    **record["content"],
                },
                "timestamp": datetime.now().isoformat(),
                "ttl": 3600,
            }, ensure_ascii=False) + "\n")

    def _log_dead_letter(self, record: Dict[str, Any], elapsed: float):
        """记录未送达的死亡信号"""
        with open(PHEROMONE_FILE, "a") as f:
            f.write(json.dumps({
                "id": f"dead-{record['signal_id']}",
                "type": "alarm",
                "source": "signal_relay",
                "target": record["target"],
                "intensity": 0.01,  # 微弱信号 · 已死
                "content": {
                    "original_signal": record["type"],
                    "priority": record["priority"],
                    "elapsed_minutes": round(elapsed, 1),
                    "status": "dead_letter",
                },
                "timestamp": datetime.now().isoformat(),
                "ttl": 86400,
            }, ensure_ascii=False) + "\n")

    def monitor(self) -> Dict[str, Any]:
        """监测当前信号队列"""
        pending = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        types = {}
        total = 0

        if SIGNAL_QUEUE.exists():
            now = datetime.now()
            for line in SIGNAL_QUEUE.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                    sent = datetime.fromisoformat(r["sent_at"])
                    elapsed = (now - sent).total_seconds() / 60
                    timeout = self.PRIORITY_TIMEOUT.get(r["priority"], 60)
                    if elapsed < timeout:
                        pending[r["priority"]] = pending.get(r["priority"], 0) + 1
                        types[r["type"]] = types.get(r["type"], 0) + 1
                        total += 1
                except Exception:
                    pass

        congestion = "🟢"
        if total > 50:
            congestion = "🟡"
        if total > 100:
            congestion = "🔴"

        return {
            "dna": DNA,
            "total_pending": total,
            "congestion": congestion,
            "by_priority": pending,
            "by_type": types,
            "stats": self.state,
        }

    def listen(self, interval: int = 60):
        """守护监听模式：持续监测并分派信号"""
        print(f"⚡ 神经系统中继站启动 · 监听间隔{interval}s")
        print(f"   {DNA}")
        running = True

        def _stop(sig, frame):
            nonlocal running
            running = False
            print("\n⚡ 神经系统安全停机...")

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        while running:
            result = self.dispatch()
            if result["total_pending"] > 0:
                print(f"  ⚡ 分派:{result['dispatched']} | "
                      f"丢弃:{result['dropped']} | "
                      f"率:{result['dispatch_rate']:.0%}")
            time.sleep(interval)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·神经系统·信号中继站")
    parser.add_argument("--dispatch", action="store_true", help="分派信号")
    parser.add_argument("--monitor", action="store_true", help="监测信号队列")
    parser.add_argument("--listen", action="store_true", help="守护监听")
    parser.add_argument("--interval", type=int, default=60, help="监听间隔(秒)")
    parser.add_argument("--emit", action="store_true", help="发送测试信号")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    relay = SignalRelay()

    if args.listen:
        relay.listen(args.interval)
        return 0

    if args.emit:
        s = relay.emit("heartbeat", "signal_relay", "P3",
                       {"message": "神经系统自检信号", "source_module": "signal_relay"})
        print(f"信号已发送: {s.signal_id} → {s.target}")
        return 0

    if args.dispatch:
        result = relay.dispatch()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"信号分派完成: {result['dispatched']}已派/{result['dropped']}丢弃")
        return 0

    if args.monitor:
        m = relay.monitor()
        if args.json:
            print(json.dumps(m, ensure_ascii=False, indent=2))
        else:
            print(f"\n⚡ 信号队列: {m['congestion']} {m['total_pending']}条待处理")
            for p, count in m["by_priority"].items():
                if count > 0:
                    print(f"  {p}: {count}条")
            for t, count in m["by_type"].items():
                print(f"  [{t}]: {count}条")
            print(f"  📊 总发送:{m['stats']['signals_sent']} | 丢弃:{m['stats']['signals_dropped']}")
        return 0

    # 默认：监测
    m = relay.monitor()
    print(f"信号队列: {m['total_pending']}条待处理 · 总发送{m['stats']['signals_sent']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
