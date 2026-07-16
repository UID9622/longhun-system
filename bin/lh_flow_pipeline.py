#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     🩸 龍魂 · 循环系统 · 数据流动管道 v1.0                     ║
║                                                                  ║
║  生物映射：循环系统 → 物质输送 → 数据在各模块间流动                ║
║  五行归属：水                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·循环系统-FLOW-PIPELINE-v1.0              ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_flow_pipeline.py --status      # 查看数据流动状态
  python3 bin/lh_flow_pipeline.py --pulse       # 发送一次心跳脉冲
  python3 bin/lh_flow_pipeline.py --daemon      # 守护模式·持续循环
"""

import hashlib
import json
import os
import sys
import time
import signal
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
FLOW_LOG = STATE_DIR / "flow_pipeline_log.jsonl"
FLOW_STATE = STATE_DIR / "flow_state.json"

DNA = "#龍芯⚡️丙午·辛未·循环系统-FLOW-PIPELINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


@dataclass
class FlowNode:
    """流节点——数据流动的一个站点"""
    node_id: str
    name: str
    node_type: str        # source / relay / sink / pump
    element: str          # 五行
    upstream: List[str] = field(default_factory=list)
    downstream: List[str] = field(default_factory=list)
    throughput: int = 0   # 流经数据量
    last_pulse: str = ""
    health: float = 1.0


class FlowPipeline:
    """循环系统：数据流动管道引擎"""

    FLOW_NODES = {
        # 心脏泵：推动数据循环
        "heart": FlowNode(
            node_id="flow-heart", name="数据心脏泵", node_type="pump", element="火",
            downstream=["memory", "audit", "confrontation", "persona"],
        ),
        # 记忆池：存储与回溯
        "memory": FlowNode(
            node_id="flow-memory", name="记忆池", node_type="sink", element="水",
            upstream=["heart"], downstream=["audit", "trainer"],
        ),
        # 审计过滤器
        "audit": FlowNode(
            node_id="flow-audit", name="审计过滤器", node_type="relay", element="金",
            upstream=["heart", "memory"], downstream=["confrontation", "archive"],
        ),
        # 红蓝对抗区
        "confrontation": FlowNode(
            node_id="flow-rb", name="红蓝对抗区", node_type="relay", element="火",
            upstream=["heart", "audit"], downstream=["persona", "archive"],
        ),
        # 人格注入点
        "persona": FlowNode(
            node_id="flow-persona", name="人格注入点", node_type="relay", element="火",
            upstream=["heart", "confrontation"], downstream=["signing", "archive"],
        ),
        # 签章归档
        "signing": FlowNode(
            node_id="flow-signing", name="签章归档点", node_type="sink", element="金",
            upstream=["persona"], downstream=["archive"],
        ),
        # 永久归档
        "archive": FlowNode(
            node_id="flow-archive", name="永久归档池", node_type="sink", element="土",
            upstream=["audit", "confrontation", "persona", "signing"],
        ),
        # 训练回灌
        "trainer": FlowNode(
            node_id="flow-trainer", name="训练回灌点", node_type="relay", element="木",
            upstream=["memory"], downstream=["heart"],
        ),
    }

    def __init__(self):
        self.state = self._load_state()
        self.log = []

    def _load_state(self) -> Dict[str, Any]:
        if FLOW_STATE.exists():
            return json.loads(FLOW_STATE.read_text())
        return {nid: {"throughput": n.throughput, "health": n.health,
                      "last_pulse": n.last_pulse}
                for nid, n in self.FLOW_NODES.items()}

    def _save_state(self):
        FLOW_STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def _log_flow(self, event: str, from_node: str, to_node: str, data_type: str, volume: int):
        """记录一次数据流动"""
        record = {
            "event": event,
            "from": from_node,
            "to": to_node,
            "data_type": data_type,
            "volume": volume,
            "timestamp": datetime.now().isoformat(),
            "dna": DNA,
        }
        with open(FLOW_LOG, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # 更新吞吐量
        for nid in (from_node, to_node):
            if nid in self.state:
                self.state[nid]["throughput"] += volume
                self.state[nid]["last_pulse"] = record["timestamp"]

    def pulse(self) -> Dict[str, Any]:
        """
        一次心跳脉冲：数据沿着管道流动一圈
        
        流程：
        heart→memory→audit→confrontation→persona→signing→archive
        └→trainer──────────────────────────────┘
        """
        now = datetime.now().isoformat()
        results = {"pulse_time": now, "flows": [], "blockages": []}

        # 心脏泵 → 所有下游
        heart = self.FLOW_NODES["heart"]
        for target in heart.downstream:
            if target in self.FLOW_NODES:
                self._log_flow("pulse", "heart", target, "lifebeat", 1)
                results["flows"].append(f"heart→{target}")

        # 各节点间流动
        flow_chain = [
            ("memory", "audit"),
            ("memory", "trainer"),
            ("audit", "confrontation"),
            ("audit", "archive"),
            ("confrontation", "persona"),
            ("confrontation", "archive"),
            ("persona", "signing"),
            ("signing", "archive"),
            ("trainer", "heart"),
        ]

        for src, dst in flow_chain:
            if src in self.FLOW_NODES and dst in self.FLOW_NODES:
                src_node = self.FLOW_NODES[src]
                # 健康检查
                if src_node.health < 0.3:
                    results["blockages"].append(f"🔴 {src}→{dst} 堵塞(src健康={src_node.health})")
                    continue
                self._log_flow("flow", src, dst, "data", 1)
                results["flows"].append(f"{src}→{dst}")

        # 更新健康度
        self._update_health()
        self._save_state()

        results["total_flows"] = len(results["flows"])
        results["total_blockages"] = len(results["blockages"])
        results["health"] = self.overall_health()

        return results

    def _update_health(self):
        """根据吞吐量变化更新各节点健康度"""
        for nid, node in self.FLOW_NODES.items():
            s = self.state.get(nid, {})
            throughput = s.get("throughput", 0)
            last = s.get("last_pulse", "")
            if last:
                elapsed = (datetime.now() - datetime.fromisoformat(last)).total_seconds()
                # 超过1小时无脉冲 → 降健康度
                if elapsed > 3600:
                    s["health"] = max(0.1, s.get("health", 1.0) - 0.05)
                else:
                    s["health"] = min(1.0, s.get("health", 1.0) + 0.01)
            self.state[nid] = s

    def overall_health(self) -> float:
        """循环系统整体健康度"""
        if not self.state:
            return 0.0
        return round(sum(s.get("health", 0) for s in self.state.values()) / len(self.state), 3)

    def status(self) -> Dict[str, Any]:
        """返回当前循环系统状态"""
        flows_today = 0
        blockages = 0
        if FLOW_LOG.exists():
            for line in FLOW_LOG.read_text().splitlines():
                if "pulse" in line or '"event": "flow"' in line:
                    flows_today += 1
                if "blockage" in line:
                    blockages += 1

        return {
            "dna": DNA,
            "nodes": {
                nid: {
                    "name": node.name,
                    "type": node.node_type,
                    "element": node.element,
                    "health": self.state.get(nid, {}).get("health", 1.0),
                    "throughput": self.state.get(nid, {}).get("throughput", 0),
                }
                for nid, node in self.FLOW_NODES.items()
            },
            "overall_health": self.overall_health(),
            "flows_today": flows_today,
            "blockages": blockages,
        }

    def daemon(self, interval: int = 300):
        """守护模式：每N秒一次心跳"""
        print(f"🩸 循环系统守护启动 · 间隔{interval}s")
        print(f"   {DNA}")
        running = True

        def _stop(sig, frame):
            nonlocal running
            running = False
            print("\n🩸 循环系统正在安全停机...")

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        pulse_count = 0
        while running:
            pulse_count += 1
            result = self.pulse()
            status = "🟢" if result["total_blockages"] == 0 else "🟡"
            print(f"  {status} 心跳#{pulse_count} | "
                  f"流动:{result['total_flows']} | "
                  f"堵塞:{result['total_blockages']} | "
                  f"健康:{result['health']:.1%}")
            time.sleep(interval)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·循环系统·数据流动管道")
    parser.add_argument("--status", action="store_true", help="查看流动状态")
    parser.add_argument("--pulse", action="store_true", help="发送一次心跳")
    parser.add_argument("--daemon", action="store_true", help="守护模式")
    parser.add_argument("--interval", type=int, default=300, help="守护间隔(秒)")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    pipeline = FlowPipeline()

    if args.daemon:
        pipeline.daemon(args.interval)
        return 0

    if args.pulse:
        result = pipeline.pulse()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🩸 心跳脉冲完成")
            print(f"   流动:{result['total_flows']} | 堵塞:{result['total_blockages']} | 健康:{result['health']:.1%}")
            if result["blockages"]:
                for b in result["blockages"]:
                    print(f"   {b}")
        return 0

    if args.status:
        status = pipeline.status()
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(f"\n🩸 循环系统状态 · 健康:{status['overall_health']:.1%}")
            for nid, n in status["nodes"].items():
                icon = "🟢" if n["health"] > 0.7 else "🟡" if n["health"] > 0.3 else "🔴"
                print(f"  {icon} {n['name']:<12s} ({n['type']:<6s}/{n['element']}) "
                      f"吞吐:{n['throughput']:>4} 健康:{n['health']:.1%}")
        return 0

    # 默认：一次心跳
    return main()


if __name__ == "__main__":
    sys.exit(main())
