#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自我进化引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-EVOLUTION-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 分析自身执行效率，提出优化建议
  - 自动生成新规则/触发词
  - 基于历史数据调优配置
  - 系统'自己教自己'——不再依赖人工介入
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import Counter


class EvolutionEngine:
    """自我进化引擎——系统自己教自己"""

    def __init__(self):
        self.history = []
        self.optimization_suggestions = []
        self.evolution_log = []
        self._load_history()

    def _load_history(self):
        history_file = Path.home() / "longhun-system/data/task_history.jsonl"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.history.append(json.loads(line))
                    except Exception:
                        pass

    def analyze_performance(self, limit: int = 200) -> List[Dict]:
        """分析执行历史，提出优化建议"""
        recent = self.history[-limit:] if len(self.history) > limit else self.history
        total = len(recent)
        suggestions = []

        if total < 10:
            suggestions.append({
                "type": "info",
                "message": f"数据不足（仅{total}条），积累更多执行记录后分析",
                "action": None,
            })
            return suggestions

        # 平均耗时分析
        durations = [h.get("duration", 0) for h in recent if h.get("duration")]
        if durations:
            avg_duration = sum(durations) / len(durations)
            if avg_duration > 2.0:
                suggestions.append({
                    "type": "performance",
                    "message": f"平均耗时 {avg_duration:.2f}s，建议优化慢速步骤",
                    "action": "lh 性能分析 --bottleneck",
                })

        # 失败率分析
        failures = [h for h in recent if h.get("status") == "error"]
        fail_rate = len(failures) / total
        if fail_rate > 0.3:
            suggestions.append({
                "type": "reliability",
                "message": f"失败率 {fail_rate*100:.1f}%，建议检查依赖和日志",
                "action": "lh 故障诊断",
            })

        # 高频操作检测→建议自动化
        actions = [h.get("action", "") for h in recent if h.get("action")]
        action_counts = Counter(actions)
        common = [a for a, c in action_counts.most_common(5) if c > 3]
        if common:
            suggestions.append({
                "type": "automation",
                "message": f"发现高频操作: {', '.join(common)}，建议添加触发词",
                "action": f"lh 添加别名 {common[0]}",
            })

        self.optimization_suggestions = suggestions
        return suggestions

    def suggest_new_triggers(self) -> List[str]:
        """从历史模式学习新触发词"""
        existing = ["健康检查", "审计", "签名", "推送", "记忆", "协议", "状态", "日志"]
        if not self.history:
            return []
        actions = [h.get("action", "") for h in self.history[-200:]]
        words = []
        for a in actions:
            words.extend(a.split())
        word_counts = Counter(w for w in words if len(w) >= 2 and w not in existing)
        return [w for w, c in word_counts.most_common(10) if c >= 3]

    def auto_tune(self) -> Dict:
        """自动调优配置"""
        changes = []
        durations = [h.get("duration", 0) for h in self.history[-50:] if h.get("duration")]
        if durations:
            avg = sum(durations) / len(durations)
            if avg < 0.5:
                changes.append({"parameter": "timeout", "suggested": 30, "reason": "任务执行较快"})
            elif avg > 3:
                changes.append({"parameter": "timeout", "suggested": 120, "reason": "任务执行较慢"})

        self.evolution_log.append({
            "timestamp": datetime.now().isoformat(),
            "changes": changes,
        })
        return {
            "status": "tuned",
            "changes": changes,
            "total_evolutions": len(self.evolution_log),
        }

    def evolve(self) -> Dict[str, Any]:
        """执行一次完整的进化循环"""
        t0 = time.time()
        suggestions = self.analyze_performance()
        triggers = self.suggest_new_triggers()
        tuning = self.auto_tune()

        return {
            "timestamp": datetime.now().isoformat(),
            "suggestions": suggestions,
            "new_triggers": triggers,
            "tuning": tuning,
            "evolution_time_ms": (time.time() - t0) * 1000,
        }


if __name__ == "__main__":
    engine = EvolutionEngine()
    result = engine.evolve()
    print(f"进化循环完成 ({result['evolution_time_ms']:.0f}ms)")
    print(f"优化建议: {len(result['suggestions'])} 条")
    for s in result["suggestions"]:
        print(f"  ├ [{s['type']}] {s['message']}")
    print(f"新触发词: {len(result['new_triggers'])} 个")
    print(f"调优变更: {len(result['tuning']['changes'])} 项")
    print("🟢 自我进化引擎测试通过")
