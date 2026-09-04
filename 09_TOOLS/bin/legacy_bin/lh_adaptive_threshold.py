#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     🧪 龍魂 · 内分泌系统 · 自适应阈值引擎 v1.0               ║
║                                                                  ║
║  生物映射：内分泌系统 → 慢调平衡 → 动态阈值/权重调节              ║
║  五行归属：土                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·内分泌系统-ADAPTIVE-THRESHOLD-v1.0      ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_adaptive_threshold.py --tune         # 根据历史数据调优
  python3 bin/lh_adaptive_threshold.py --status       # 查看当前阈值
  python3 bin/lh_adaptive_threshold.py --calibrate    # 自动校准
"""

import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
ENDOCRINE_STATE = STATE_DIR / "endocrine_state.json"

DNA = "#龍芯⚡️丙午·辛未·内分泌系统-ADAPTIVE-THRESHOLD-v1.0"


@dataclass
class AdaptiveParameter:
    """自适应参数——一个可动态调节的"激素"水平"""
    name: str
    current_value: float
    default_value: float
    min_value: float
    max_value: float
    step: float
    direction: str = "stable"    # increasing / decreasing / stable
    history: List[float] = field(default_factory=list)
    tuned_at: str = ""
    tuning_reason: str = ""

    def tune(self, target_change: float, reason: str):
        """调节激素水平"""
        new_value = self.current_value + target_change * self.step
        self.current_value = round(max(self.min_value, min(self.max_value, new_value)), 3)
        self.tuned_at = datetime.now().isoformat()
        self.tuning_reason = reason
        self.history.append(self.current_value)
        if len(self.history) > 50:
            self.history = self.history[-50:]

        if target_change > 0:
            self.direction = "increasing"
        elif target_change < 0:
            self.direction = "decreasing"
        else:
            self.direction = "stable"


class AdaptiveThresholdEngine:
    """内分泌系统：根据系统反馈动态调节参数"""

    # 自适应参数（激素）
    PARAMETERS = {
        "alert_sensitivity": AdaptiveParameter(
            name="告警灵敏度", current_value=0.7, default_value=0.7,
            min_value=0.3, max_value=0.95, step=0.05,
        ),
        "orphan_tolerance": AdaptiveParameter(
            name="孤儿容忍度", current_value=0.1, default_value=0.1,
            min_value=0.02, max_value=0.3, step=0.01,
        ),
        "stale_days_warning": AdaptiveParameter(
            name="陈旧预警天", current_value=30, default_value=30,
            min_value=7, max_value=90, step=1,
        ),
        "stale_days_critical": AdaptiveParameter(
            name="陈旧严重天", current_value=90, default_value=90,
            min_value=30, max_value=180, step=1,
        ),
        "line_critical": AdaptiveParameter(
            name="行数严重线", current_value=500, default_value=500,
            min_value=200, max_value=1000, step=50,
        ),
        "rb_trigger_rate": AdaptiveParameter(
            name="红蓝触发率", current_value=0.3, default_value=0.3,
            min_value=0.1, max_value=0.8, step=0.05,
        ),
        "signal_decay_rate": AdaptiveParameter(
            name="信号衰减率", current_value=0.01, default_value=0.01,
            min_value=0.001, max_value=0.1, step=0.001,
        ),
    }

    def __init__(self):
        self._load_state()

    def _load_state(self):
        if ENDOCRINE_STATE.exists():
            saved = json.loads(ENDOCRINE_STATE.read_text())
            for name, data in saved.items():
                if name in self.PARAMETERS:
                    p = self.PARAMETERS[name]
                    p.current_value = data["current_value"]
                    p.direction = data.get("direction", "stable")
                    p.history = data.get("history", [])
                    p.tuned_at = data.get("tuned_at", "")

    def _save_state(self):
        data = {
            name: {
                "current_value": p.current_value,
                "direction": p.direction,
                "history": p.history[-20:],
                "tuned_at": p.tuned_at,
                "tuning_reason": p.tuning_reason,
            }
            for name, p in self.PARAMETERS.items()
        }
        ENDOCRINE_STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def get(self, name: str) -> float:
        """获取当前激素水平"""
        return self.PARAMETERS[name].current_value if name in self.PARAMETERS else 0

    def calibrate(self, colony_health: float, alert_count: int,
                  orphan_count: int, rb_count: int, total_scripts: int) -> Dict[str, Any]:
        """
        根据蚁群状态自动校准参数
        
        反馈回路：
        - 健康度高 → 降低灵敏度（减少误报）
        - 健康度低 → 提高灵敏度（加强监测）
        - 孤儿多 → 降低孤儿容忍度（更积极发现孤儿）
        - 告警过多 → 提高陈旧天数（减少噪音）
        """
        changes = []

        # 告警灵敏度：健康度低时降低→增加检测 | 健康度高时提高→减少噪音
        if colony_health < 0.7:
            if self.PARAMETERS["alert_sensitivity"].current_value > 0.4:
                self.PARAMETERS["alert_sensitivity"].tune(-1, f"健康度低({colony_health:.1%})，降低阈值增加灵敏度")
                changes.append(f"告警灵敏度↓ {self.PARAMETERS['alert_sensitivity'].current_value:.2f}")

        elif colony_health > 0.9:
            if self.PARAMETERS["alert_sensitivity"].current_value < 0.9:
                self.PARAMETERS["alert_sensitivity"].tune(1, f"健康度高({colony_health:.1%})，提高阈值减少噪音")
                changes.append(f"告警灵敏度↑ {self.PARAMETERS['alert_sensitivity'].current_value:.2f}")

        # 孤儿容忍度
        if total_scripts > 0:
            orphan_rate = orphan_count / total_scripts
            if orphan_rate > 0.1 and self.PARAMETERS["orphan_tolerance"].current_value > 0.03:
                self.PARAMETERS["orphan_tolerance"].tune(-1, f"孤儿率{orphan_rate:.0%}偏高，降低容忍度")
                changes.append(f"孤儿容忍度↓ {self.PARAMETERS['orphan_tolerance'].current_value:.2f}")

        # 红蓝触发率：告警多时提高触发率加强处理
        if alert_count > 50 and self.PARAMETERS["rb_trigger_rate"].current_value < 0.7:
            self.PARAMETERS["rb_trigger_rate"].tune(2, f"告警数{alert_count}高，提高红蓝触发率")
            changes.append(f"红蓝触发率↑ {self.PARAMETERS['rb_trigger_rate'].current_value:.2f}")
        elif alert_count < 10 and self.PARAMETERS["rb_trigger_rate"].current_value > 0.2:
            self.PARAMETERS["rb_trigger_rate"].tune(-1, f"告警数{alert_count}低，降低红蓝触发率")
            changes.append(f"红蓝触发率↓ {self.PARAMETERS['rb_trigger_rate'].current_value:.2f}")

        # 信号衰减率：信号多时加快衰减防止堆积
        if alert_count > 100 and self.PARAMETERS["signal_decay_rate"].current_value < 0.05:
            self.PARAMETERS["signal_decay_rate"].tune(2, f"信号堆积({alert_count})，加快衰减")
            changes.append(f"信号衰减率↑ {self.PARAMETERS['signal_decay_rate'].current_value:.3f}")

        self._save_state()

        return {
            "dna": DNA,
            "changes_count": len(changes),
            "changes": changes,
            "parameters": {n: p.current_value for n, p in self.PARAMETERS.items()},
            "timestamp": datetime.now().isoformat(),
        }

    def status(self) -> Dict[str, Any]:
        """查看当前激素水平"""
        params = {}
        for name, p in self.PARAMETERS.items():
            params[name] = {
                "description": p.name,
                "current": p.current_value,
                "default": p.default_value,
                "direction": p.direction,
                "range": f"[{p.min_value}, {p.max_value}]",
                "deviation": round((p.current_value - p.default_value) / max(p.default_value, 0.001), 2),
            }

        deviations = [abs(d["deviation"]) for d in params.values()]
        avg_dev = sum(deviations) / len(deviations) if deviations else 0

        return {
            "dna": DNA,
            "parameters": params,
            "average_deviation": round(avg_dev, 2),
            "stability": "🟢 稳定" if avg_dev < 0.2 else "🟡 需关注" if avg_dev < 0.5 else "🔴 剧烈波动",
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·内分泌系统·自适应阈值")
    parser.add_argument("--tune", action="store_true", help="根据历史调优")
    parser.add_argument("--status", action="store_true", help="查看当前阈值")
    parser.add_argument("--calibrate", action="store_true", help="自动校准")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    engine = AdaptiveThresholdEngine()

    if args.calibrate:
        # 读取蚁群状态
        colony_file = STATE_DIR / "colony_state.json"
        if colony_file.exists():
            cs = json.loads(colony_file.read_text())
            result = engine.calibrate(
                colony_health=cs.get("colony_health", 0.9),
                alert_count=cs.get("alerts_firing", 0),
                orphan_count=cs.get("orphan_scripts", 0),
                rb_count=cs.get("rb_confrontations_today", 0),
                total_scripts=cs.get("registered_scripts", 1),
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n🧪 内分泌校准完成 · {result['changes_count']}项调整")
                for c in result["changes"]:
                    print(f"  {c}")
        else:
            print("❌ 无蚁群状态数据，请先运行: python3 bin/lh_ant_colony_orchestrator.py --run")
        return 0

    if args.tune:
        return main()  # 同calibrate

    if args.status:
        s = engine.status()
        if args.json:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            print(f"\n🧪 内分泌系统: {s['stability']} (平均偏差{s['average_deviation']:.2f})")
            for name, p in s["parameters"].items():
                arrow = "▲" if p["direction"] == "increasing" else "▼" if p["direction"] == "decreasing" else "—"
                dev = f"{p['deviation']:+.0%}" if p["deviation"] != 0 else "=默认"
                print(f"  {arrow} {p['description']:<10s}: {p['current']} ({dev}) [{p['range']}]")
        return 0

    # 默认
    s = engine.status()
    print(f"内分泌系统就绪 · {s['stability']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
