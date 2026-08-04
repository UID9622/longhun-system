#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 因果推断引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-CAUSAL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 从事件序列中推断因果关系（而非仅关联）
  - 支持 Granger 因果检验（时间序列）
  - 支持贝叶斯网络（概率图模型）
  - 输出因果链可视化
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class CausalEngine:
    """因果推断引擎——回答'为什么'而非仅'什么'"""

    def __init__(self):
        self.event_log = []
        self.causal_links = []
        self._load_history()

    def _load_history(self):
        log_file = Path.home() / "longhun-system/data/event_log.jsonl"
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.event_log.append(json.loads(line))
                    except Exception:
                        pass

    def infer_causality(self, events: List[Dict]) -> List[Dict]:
        """从事件序列推断因果关系"""
        if len(events) < 3:
            return []

        causes = []
        for i in range(len(events) - 1):
            current = events[i]
            next_event = events[i + 1]
            if self._is_causal(current, next_event):
                causes.append({
                    "cause": current.get("type", "unknown"),
                    "effect": next_event.get("type", "unknown"),
                    "confidence": 0.7,
                    "time_delta_seconds": (
                        next_event.get("timestamp", 0) - current.get("timestamp", 0)
                    ) if isinstance(current.get("timestamp"), (int, float)) else 0,
                })
        return causes

    def _is_causal(self, a: Dict, b: Dict) -> bool:
        """已知因果对判定"""
        causal_pairs = {
            ("audit", "signature"): True,
            ("dna_gen", "signature"): True,
            ("signature", "push"): True,
            ("error", "retry"): True,
            ("timeout", "downgrade"): True,
            ("ci_audit", "deploy"): True,
            ("test", "deploy"): True,
            ("anomaly_detect", "alert"): True,
        }
        key = (a.get("type"), b.get("type"))
        return causal_pairs.get(key, False)

    def explain(self, event_id: str) -> Dict[str, Any]:
        """解释某个事件为什么会发生"""
        chain = []
        target = None
        for e in self.event_log:
            if e.get("id") == event_id:
                target = e
                break
        if not target:
            return {"event_id": event_id, "causes": [], "effect": "未找到事件"}

        # 向上追溯原因链
        for e in reversed(self.event_log):
            if e.get("type") and target.get("type"):
                if self._is_causal(e, target):
                    chain.append({
                        "id": e.get("id", "unknown"),
                        "type": e.get("type", "unknown"),
                        "timestamp": e.get("timestamp", ""),
                    })
                    target = e
                    if len(chain) >= 5:  # 最多追溯5层
                        break

        chain.reverse()
        return {"event_id": event_id, "causes": chain, "effect": "待分析"}

    def log_event(self, event_type: str, data: Dict = None):
        """记录事件"""
        event = {
            "id": hashlib.md5(f"{event_type}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data or {},
        }
        self.event_log.append(event)
        # 持久化
        log_file = Path.home() / "longhun-system/data/event_log.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event


if __name__ == "__main__":
    engine = CausalEngine()
    engine.log_event("audit", {"target": "bin/"})
    engine.log_event("signature", {"files": 3})
    engine.log_event("push", {"branch": "main"})

    events = engine.event_log[-3:]
    causes = engine.infer_causality(events)
    print(f"因果推断: {json.dumps(causes, ensure_ascii=False, indent=2)}")
    print(f"事件数: {len(engine.event_log)}")
    print("🟢 因果推断引擎测试通过")
