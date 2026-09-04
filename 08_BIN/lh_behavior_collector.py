#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·行为采集器 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-BEHAVIOR-COLLECTOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

从浏览器史官、如意总开关、TeamOrchestrator的协作记录中，
自动提取七因子行为数据。

全部纯本地处理，不上传云端。

用法:
  python3 bin/lh_behavior_collector.py collect               # 全量采集
  python3 bin/lh_behavior_collector.py collect --source orchestrator  # 从协作记录采集
  python3 bin/lh_behavior_collector.py collect --source ruyi          # 从如意总开关采集
  python3 bin/lh_behavior_collector.py status                # 查看采集状态
"""

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_seven_factor_engine import get_engine

COLLECTOR_DIR = SYSTEM_ROOT / "data" / "behavior_collector"
COLLECTOR_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# 数据源适配器
# ═══════════════════════════════════════════════════════════

class OrchestratorSource:
    """从 TeamOrchestrator 协作记录中提取行为事件"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def collect(self) -> List[Dict[str, Any]]:
        events = []

        # 从 orchestrator 数据目录读取
        orch_dir = self.root / "data" / "orchestrator"
        if not orch_dir.exists():
            return events

        # 读取复盘报告
        aar_dir = orch_dir / "after_action"
        if aar_dir.exists():
            for f in aar_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text())
                    events.extend(self._parse_aar(data, f.stem))
                except Exception:
                    pass

        # 读取运行记录
        runs_dir = orch_dir / "runs"
        if runs_dir.exists():
            for f in runs_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text())
                    events.extend(self._parse_run(data, f.stem))
                except Exception:
                    pass

        return events

    def _parse_aar(self, data: dict, task_id: str) -> List[Dict[str, Any]]:
        """解析复盘报告"""
        events = []
        contributions = data.get("contributions", [])

        for contrib in contributions:
            persona = contrib.get("persona", "UNKNOWN")
            score = contrib.get("score", 0.5)
            task = data.get("task", "")

            events.append({
                "entity_id": persona,
                "entity_type": "persona",
                "promise": f"协作任务: {task[:60]}",
                "fulfilled": score >= 0.4,
                "fulfillment_detail": f"贡献评分: {score}",
                "emotion": "积极" if score >= 0.7 else "中性",
                "audience": "老大",
                "explanation": "不解释",
                "admit": "真改" if score >= 0.6 else "无反应",
                "source": "TeamOrchestrator",
                "tags": ["协作", data.get("formation", "")],
            })

        return events

    def _parse_run(self, data: dict, run_id: str) -> List[Dict[str, Any]]:
        events = []
        results = data.get("results", [])
        for r in results:
            events.append({
                "entity_id": r.get("persona", "UNKNOWN"),
                "entity_type": "persona",
                "promise": r.get("task", f"运行: {run_id}"),
                "fulfilled": r.get("success", False),
                "fulfillment_detail": r.get("output", "")[:80],
                "emotion": "中性",
                "audience": "老大",
                "explanation": "不解释",
                "admit": "无反应",
                "source": "TeamOrchestrator",
                "tags": ["协作", "运行"],
            })
        return events


class RuyiSource:
    """从如意总开关历史中提取行为事件"""


    def collect(self) -> List[Dict[str, Any]]:
        events = []

        # 从如意数据目录读取
        ruyi_dir = self.root / "data" / "ruyi"
        if not ruyi_dir.exists():
            return events

        # 读取指令历史
        cmd_dir = ruyi_dir / "commands"
        if cmd_dir.exists():
            for f in cmd_dir.glob("*.json*"):
                try:
                    data = json.loads(f.read_text())
                    events.extend(self._parse_command(data))
                except Exception:
                    pass

        return events

    def _parse_command(self, data: dict) -> List[Dict[str, Any]]:
        events = []
        cmd_text = data.get("command", data.get("text", ""))
        result = data.get("result", data.get("response", ""))
        success = data.get("success", True)

        # 老大的指令 = 承诺事件（AI承诺执行）
        if cmd_text:
            events.append({
                "entity_id": data.get("executor", "CodeBuddy"),
                "entity_type": "persona",
                "promise": cmd_text[:80],
                "fulfilled": success,
                "fulfillment_detail": str(result)[:80] if result else "",
                "emotion": "积极" if success else "中性",
                "audience": "老大",
                "explanation": "不解释",
                "admit": "真改" if success else "无反应",
                "source": "如意总开关",
                "tags": ["如意", "指令"],
            })

        return events


class BrowserHistorianSource:
    """从浏览器史官数据中提取行为模式"""


    def collect(self) -> List[Dict[str, Any]]:
        events = []
        bh_dir = self.root / "data" / "browser_historian"
        if not bh_dir.exists():
            return events

        # 读取周报或分析数据
        for pattern_file in bh_dir.glob("*report*.json"):
            try:
                data = json.loads(pattern_file.read_text())
                events.extend(self._parse_report(data))
            except Exception:
                pass

        return events

    def _parse_report(self, data: dict) -> List[Dict[str, Any]]:
        events = []
        insights = data.get("insights", data.get("analysis", []))
        for insight in insights:
            if isinstance(insight, dict):
                events.append({
                    "entity_id": "UID9622",
                    "entity_type": "user",
                    "promise": insight.get("title", insight.get("summary", "浏览器行为分析"))[:60],
                    "fulfilled": True,
                    "fulfillment_detail": str(insight.get("detail", ""))[:80],
                    "emotion": "中性",
                    "audience": "自己",
                    "explanation": "不解释",
                    "admit": "无反应",
                    "source": "浏览器史官",
                    "tags": ["浏览器", "行为分析"],
                })
        return events


# ═══════════════════════════════════════════════════════════
# 主采集器
# ═══════════════════════════════════════════════════════════

class BehaviorCollector:
    """行为采集器 — 从多源自动提取七因子数据"""

    def __init__(self):
        self.engine = get_engine()
        self.sources = {
            "orchestrator": OrchestratorSource(),
            "ruyi": RuyiSource(),
            "browser": BrowserHistorianSource(),
        }
        self._stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        sf = COLLECTOR_DIR / "stats.json"
        if sf.exists():
            try:
                return json.loads(sf.read_text())
            except Exception:
                pass
        return {"total_collected": 0, "last_collection": "", "by_source": {}}

    def _save_stats(self):
        self._stats["last_collection"] = datetime.now(timezone.utc).isoformat()
        (COLLECTOR_DIR / "stats.json").write_text(json.dumps(self._stats, indent=2, ensure_ascii=False))

    def collect(self, source: str = "all") -> Dict[str, Any]:
        """全量采集"""
        collected = 0
        by_source = {}

        sources_to_run = [source] if source != "all" else list(self.sources.keys())

        for src_name in sources_to_run:
            if src_name not in self.sources:
                continue
            src = self.sources[src_name]
            try:
                raw_events = src.collect()
            except Exception as e:
                raw_events = []

            submitted = 0
            dedup_hashes = set()

            # 加载已有去重哈希
            dedup_file = COLLECTOR_DIR / f"dedup_{src_name}.json"
            if dedup_file.exists():
                try:
                    dedup_hashes = set(json.loads(dedup_file.read_text()))
                except Exception:
                    pass

            for ev_data in raw_events:
                # 去重
                dedup_key = hashlib.sha256(
                    json.dumps(ev_data, sort_keys=True, ensure_ascii=False).encode()
                ).hexdigest()
                if dedup_key in dedup_hashes:
                    continue
                dedup_hashes.add(dedup_key)

                try:
                    self.engine.submit_event(ev_data["entity_id"], ev_data)
                    submitted += 1
                except Exception:
                    pass

            # 保存去重
            dedup_file.write_text(json.dumps(list(dedup_hashes)))

            by_source[src_name] = submitted
            collected += submitted

        self._stats["total_collected"] += collected
        self._stats["by_source"] = {
            k: self._stats["by_source"].get(k, 0) + by_source.get(k, 0)
            for k in sources_to_run
        }
        self._save_stats()

        return {
            "status": "ok",
            "collected": collected,
            "by_source": by_source,
            "total": self._stats["total_collected"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def status(self) -> Dict[str, Any]:
        return {
            **self._stats,
            "engine_entities": len(self.engine._profiles),
            "engine_events": len(self.engine._events),
        }


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·行为采集器")
    sub = parser.add_subparsers(dest="cmd")

    p_collect = sub.add_parser("collect", help="采集行为事件")
    p_collect.add_argument("--source", default="all", 
                           choices=["all", "orchestrator", "ruyi", "browser"])

    sub.add_parser("status", help="查看采集状态")

    args = parser.parse_args()
    collector = BehaviorCollector()

    if args.cmd == "collect":
        result = collector.collect(args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == "status":
        print(json.dumps(collector.status(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
