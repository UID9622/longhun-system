#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     🍽  龍魂 · 消化系统 · 输入处理管道 v1.0                    ║
║                                                                  ║
║  生物映射：消化系统 → 摄入转化 → 外部输入分类/路由/处理            ║
║  五行归属：土                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·消化系统-INPUT-PIPELINE-v1.0             ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_input_pipeline.py --ingest <input>  # 摄入一条输入
  python3 bin/lh_input_pipeline.py --digest           # 处理待消化队列
  python3 bin/lh_input_pipeline.py --status           # 查看消化状态
"""

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
INGEST_QUEUE = STATE_DIR / "ingest_queue.jsonl"
DIGEST_LOG = STATE_DIR / "digest_log.jsonl"

DNA = "#龍芯⚡️丙午·辛未·消化系统-INPUT-PIPELINE-v1.0"


class InputType(Enum):
    TEXT = "text"
    CODE = "code"
    CONFIG = "config"
    COMMAND = "command"
    LOG = "log"
    DOCUMENT = "document"
    UNKNOWN = "unknown"


class DigestState(Enum):
    RAW = "raw"               # 原始摄入
    CLASSIFIED = "classified" # 已分类
    ROUTED = "routed"         # 已路由
    PROCESSED = "processed"   # 已处理
    ABSORBED = "absorbed"     # 已吸收
    REJECTED = "rejected"     # 已拒绝


@dataclass
class IngestNode:
    """摄入节点——一次外部输入"""
    node_id: str
    raw_input: str
    input_type: InputType
    state: DigestState = DigestState.RAW
    digital_root: int = 0
    wuxing_element: str = "土"
    audit_color: str = "🟢"
    routed_to: str = ""
    ingested_at: str = ""
    digested_at: str = ""
    hash: str = ""


class DigestivePipeline:
    """消化系统：外部输入→分类→路由→处理→吸收"""

    # 入口宇宙六门（引用流场压缩核 v3.0）
    GATE_ROUTING = {
        "民生": {"element": "土", "layer": "L3", "action": "普惠处理"},
        "教育": {"element": "木", "layer": "L4", "action": "生长模块"},
        "权益": {"element": "金", "layer": "L0", "action": "规则裁决"},
        "技术": {"element": "木金", "layer": "L4+L0", "action": "创新+审计双闸"},
        "数据主权": {"element": "水", "layer": "L1", "action": "DNA追溯"},
        "创作": {"element": "火", "layer": "L2", "action": "文明输出"},
    }

    # 输入类型识别规则
    TYPE_DETECTORS = [
        (["def ", "class ", "import ", "from ", "function", "const ", "let ", "var "], InputType.CODE),
        (["config", "setting", "env", "环境", "配置", ".json", ".yaml", ".toml"], InputType.CONFIG),
        (["--", "参数", "command", "运行", "执行", "启动"], InputType.COMMAND),
        (["error", "warning", "info", "debug", "traceback", "日志", "异常"], InputType.LOG),
        (["文章", "论文", "文档", "报告", "记录", "说明"], InputType.DOCUMENT),
    ]

    def __init__(self):
        self.queue = self._load_queue()

    def _load_queue(self) -> List[IngestNode]:
        if not INGEST_QUEUE.exists():
            return []
        nodes = []
        for line in INGEST_QUEUE.read_text().splitlines():
            if line.strip():
                try:
                    data = json.loads(line)
                    nodes.append(IngestNode(**{
                        "node_id": data["node_id"],
                        "raw_input": data["raw_input"],
                        "input_type": InputType(data["input_type"]),
                        "state": DigestState(data.get("state", "raw")),
                        "digital_root": data.get("digital_root", 0),
                        "wuxing_element": data.get("wuxing_element", "土"),
                        "audit_color": data.get("audit_color", "🟢"),
                        "routed_to": data.get("routed_to", ""),
                        "ingested_at": data.get("ingested_at", ""),
                        "digested_at": data.get("digested_at", ""),
                        "hash": data.get("hash", ""),
                    }))
                except Exception:
                    pass
        return nodes

    def _save_queue(self):
        with open(INGEST_QUEUE, "w") as f:
            for node in self.queue:
                f.write(json.dumps({
                    "node_id": node.node_id,
                    "raw_input": node.raw_input,
                    "input_type": node.input_type.value,
                    "state": node.state.value,
                    "digital_root": node.digital_root,
                    "wuxing_element": node.wuxing_element,
                    "audit_color": node.audit_color,
                    "routed_to": node.routed_to,
                    "ingested_at": node.ingested_at,
                    "digested_at": node.digested_at,
                    "hash": node.hash,
                }, ensure_ascii=False) + "\n")

    def _detect_type(self, text: str) -> InputType:
        text_lower = text.lower()[:500]
        for keywords, itype in self.TYPE_DETECTORS:
            for kw in keywords:
                if kw.lower() in text_lower:
                    return itype
        return InputType.TEXT

    def _calc_digital_root(self, text: str) -> int:
        """数字根计算（引用流场压缩核 v3.0）"""
        digits = [int(c) for c in str(text) if c.isdigit()]
        if not digits:
            return 0
        n = sum(digits)
        while n >= 10:
            n = sum(int(c) for c in str(n))
        return n

    def _dr_to_wuxing(self, dr: int) -> str:
        return {1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
                6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}[dr]

    def _dr_to_audit(self, dr: int) -> str:
        if dr in (3, 9):
            return "🔴"
        if dr == 6:
            return "🟡"
        return "🟢"

    def _route(self, node: IngestNode) -> str:
        """根据输入类型和五行路由到目标"""
        routing = {
            InputType.CODE: "技术",
            InputType.CONFIG: "技术",
            InputType.COMMAND: "技术",
            InputType.LOG: "数据主权",
            InputType.DOCUMENT: "创作",
            InputType.TEXT: "民生",
        }
        return routing.get(node.input_type, "民生")

    def ingest(self, raw_input: str) -> IngestNode:
        """摄入一条外部输入"""
        now = datetime.now().isoformat()
        input_type = self._detect_type(raw_input)
        dr = self._calc_digital_root(raw_input)
        wuxing = self._dr_to_wuxing(dr)
        audit = self._dr_to_audit(dr)

        node = IngestNode(
            node_id=hashlib.sha256(f"{raw_input[:50]}-{now}".encode()).hexdigest()[:12],
            raw_input=raw_input[:2000],  # 截断长输入
            input_type=input_type,
            state=DigestState.RAW,
            digital_root=dr,
            wuxing_element=wuxing,
            audit_color=audit,
            ingested_at=now,
            hash=hashlib.sha256(raw_input.encode()).hexdigest()[:16],
        )

        self.queue.append(node)
        self._save_queue()
        return node

    def digest(self) -> Dict[str, Any]:
        """处理待消化队列：分类→路由→吸收"""
        results = {"classified": 0, "routed": 0, "rejected": 0, "absorbed": 0}
        new_queue = []

        for node in self.queue:
            # 已被拒绝的跳过
            if node.state == DigestState.REJECTED:
                new_queue.append(node)
                continue

            # 已吸收的保留
            if node.state == DigestState.ABSORBED:
                new_queue.append(node)
                results["absorbed"] += 1
                continue

            # 步骤1：分类
            if node.state == DigestState.RAW:
                node.routed_to = self._route(node)
                node.state = DigestState.CLASSIFIED
                results["classified"] += 1

            # 步骤2：路由检查
            if node.state == DigestState.CLASSIFIED:
                if node.audit_color == "🔴":
                    node.state = DigestState.REJECTED
                    results["rejected"] += 1
                    self._log_rejection(node)
                    new_queue.append(node)
                    continue
                node.state = DigestState.ROUTED
                results["routed"] += 1

            # 步骤3：吸收
            if node.state == DigestState.ROUTED:
                node.state = DigestState.ABSORBED
                node.digested_at = datetime.now().isoformat()
                results["absorbed"] += 1
                self._log_absorption(node)

            new_queue.append(node)

        self.queue = new_queue
        self._save_queue()
        return results

    def _log_rejection(self, node: IngestNode):
        with open(DIGEST_LOG, "a") as f:
            f.write(json.dumps({
                "node_id": node.node_id,
                "status": "rejected",
                "reason": f"数字根{node.digital_root}触发熔断",
                "type": node.input_type.value,
                "ingested_at": node.ingested_at,
                "timestamp": datetime.now().isoformat(),
            }, ensure_ascii=False) + "\n")

    def _log_absorption(self, node: IngestNode):
        with open(DIGEST_LOG, "a") as f:
            f.write(json.dumps({
                "node_id": node.node_id,
                "status": "absorbed",
                "type": node.input_type.value,
                "wuxing": node.wuxing_element,
                "routed_to": node.routed_to,
                "audit": node.audit_color,
                "ingested_at": node.ingested_at,
                "digested_at": node.digested_at,
                "timestamp": datetime.now().isoformat(),
            }, ensure_ascii=False) + "\n")

    def status(self) -> Dict[str, Any]:
        """消化系统当前状态"""
        counts = {s.value: 0 for s in DigestState}
        types = {}
        for node in self.queue:
            counts[node.state.value] = counts.get(node.state.value, 0) + 1
            types[node.input_type.value] = types.get(node.input_type.value, 0) + 1

        total = len(self.queue)
        digest_rate = counts.get("absorbed", 0) / max(total, 1)

        return {
            "dna": DNA,
            "total_ingested": total,
            "digestion_rate": round(digest_rate, 2),
            "by_state": counts,
            "by_type": types,
            "status": "🟢" if digest_rate > 0.8 else "🟡" if digest_rate > 0.5 else "🔴",
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·消化系统·输入处理管道")
    parser.add_argument("--ingest", type=str, help="摄入一条输入")
    parser.add_argument("--digest", action="store_true", help="处理待消化队列")
    parser.add_argument("--status", action="store_true", help="查看消化状态")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    pipeline = DigestivePipeline()

    if args.ingest:
        node = pipeline.ingest(args.ingest)
        print(f"已摄入: [{node.input_type.value}/{node.wuxing_element}] {node.audit_color} "
              f"dr={node.digital_root} → {node.node_id}")
        return 0

    if args.digest:
        result = pipeline.digest()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"消化完成: 分类{result['classified']} | "
                  f"路由{result['routed']} | 拒绝{result['rejected']} | 吸收{result['absorbed']}")
        return 0

    if args.status:
        s = pipeline.status()
        if args.json:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            print(f"\n🍽  消化系统状态: {s['status']} 消化率{s['digestion_rate']:.0%}")
            print(f"  总摄入: {s['total_ingested']}")
            for state, count in s["by_state"].items():
                if count > 0:
                    print(f"  [{state}]: {count}")
            print(f"\n  摄入类型分布:")
            for t, count in s["by_type"].items():
                print(f"  {t}: {count}")
        return 0

    # 默认状态
    s = pipeline.status()
    print(f"消化系统就绪 · {s['total_ingested']}条待消化")
    return 0


if __name__ == "__main__":
    sys.exit(main())
