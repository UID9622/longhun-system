#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🔍 龍魂·未映射条目监控视图 v1.0                              ║
║                                                                  ║
║  协议: LH-PROTOCOL-UNMAPPED-MONITOR-2026-0714-v1.0              ║
║  来源: 融合架构 §5.3 · 自动映射 + §6.3 · 健康阈值               ║
║                                                                  ║
║  功能:                                                           ║
║    - 定时扫描未映射条目数                                         ║
║    - 超过阈值自动告警（Bark + 本地终端）                          ║
║    - 关联六层架构的健康度                                         ║
║    - 生成未映射趋势报告                                           ║
║    - 守护模式持续监控                                             ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·UNMAPPED-MONITOR-v1.0          ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_unmapped_monitor.py                # 单次检查
  python3 bin/lh_unmapped_monitor.py --daemon        # 守护模式(每30分钟)
  python3 bin/lh_unmapped_monitor.py --alert-threshold 5   # 设置告警阈值
  python3 bin/lh_unmapped_monitor.py --dashboard     # 生成仪表盘数据
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "inbox"
STATE_DIR.mkdir(parents=True, exist_ok=True)
INBOX_DB = STATE_DIR / "inbox_items.json"
MONITOR_STATE = STATE_DIR / "monitor_state.json"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·UNMAPPED-MONITOR-v1.0"

# ── 阈值配置 ─────────────────────────────────────────
THRESHOLDS = {
    "unmapped_warn": 10,    # 未映射条目≥10 → 预警
    "unmapped_p1": 20,      # 未映射条目≥20 → P1
    "unmapped_p0": 30,      # 未映射条目≥30 → P0
    "stale_days_warn": 7,   # 条目超过7天未处理 → 预警
    "check_interval_min": 30,  # 守护检查间隔(分钟)
}

LAYERS = ["L1", "L2", "L3", "L4", "L5", "L6"]
LAYER_NAMES = {
    "L1": "核心架构层", "L2": "人格协作层", "L3": "太极进化系统",
    "L4": "知识管理层", "L5": "数据管理层", "L6": "安全保护层",
}


@dataclass
class UnmappedAlert:
    level: str       # GREEN/YELLOW/ORANGE/RED
    message: str
    count: int
    stale_count: int
    layer_gaps: List[str]  # 哪些层没有条目
    timestamp: str


class UnmappedMonitor:
    """未映射条目监控器"""

    def __init__(self):
        self.history: List[dict] = []
        self.last_check: Optional[datetime] = None
        self._load_state()

    def _load_state(self):
        if MONITOR_STATE.exists():
            data = json.loads(MONITOR_STATE.read_text())
            self.history = data.get("history", [])
            if data.get("last_check"):
                self.last_check = datetime.fromisoformat(data["last_check"])

    def _save_state(self):
        data = {
            "last_check": datetime.now().isoformat() if self.last_check else None,
            "history": self.history[-100:],  # 只保留最近100条
            "dna": DNA,
        }
        MONITOR_STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _load_inbox_data(self) -> dict[str, Any]:
        """加载inbox数据用于分析"""
        if not INBOX_DB.exists():
            return {"items": [], "count": 0}

        data = json.loads(INBOX_DB.read_text())
        return data

    def check(self) -> UnmappedAlert:
        """执行一次检查"""
        inbox = self._load_inbox_data()
        items = inbox.get("items", [])

        # 统计
        unmapped = [i for i in items if not i.get("target_layer")]
        stale = []
        now = datetime.now()

        for item in unmapped:
            if item.get("created_at"):
                try:
                    created = datetime.fromisoformat(item["created_at"])
                    if (now - created).days > THRESHOLDS["stale_days_warn"]:
                        stale.append(item)
                except (ValueError, TypeError):
                    pass

        # 哪些层没有条目
        layer_counts = {lk: 0 for lk in LAYERS}
        for item in items:
            if item.get("target_layer") in layer_counts:
                layer_counts[item["target_layer"]] += 1
        layer_gaps = [lk for lk, c in layer_counts.items() if c == 0]

        unmapped_count = len(unmapped)
        stale_count = len(stale)

        # 判定级别
        if unmapped_count >= THRESHOLDS["unmapped_p0"]:
            level = "RED"
        elif unmapped_count >= THRESHOLDS["unmapped_p1"]:
            level = "ORANGE"
        elif unmapped_count >= THRESHOLDS["unmapped_warn"]:
            level = "YELLOW"
        else:
            level = "GREEN"

        message = self._build_message(level, unmapped_count, stale_count, layer_gaps)

        alert = UnmappedAlert(
            level=level,
            message=message,
            count=unmapped_count,
            stale_count=stale_count,
            layer_gaps=layer_gaps,
            timestamp=datetime.now().isoformat(),
        )

        # 记录到历史
        self.history.append({
            "ts": alert.timestamp,
            "level": level,
            "count": unmapped_count,
            "stale": stale_count,
            "gaps": layer_gaps,
        })
        self.last_check = datetime.now()
        self._save_state()

        return alert

    def _build_message(self, level: str, count: int, stale: int, gaps: List[str]) -> str:
        prefix = {"GREEN": "✅", "YELLOW": "⚠️", "ORANGE": "🟠", "RED": "🔴"}.get(level, "❓")
        msg = f"{prefix} 未映射条目监控 [{level}]\n"
        msg += f"   未映射: {count} 条\n"
        msg += f"   超期(>{THRESHOLDS['stale_days_warn']}天): {stale} 条\n"
        if gaps:
            msg += f"   空缺层: {', '.join(f'{LAYER_NAMES[g]}({g})' for g in gaps)}\n"

        if level == "RED":
            msg += "\n   🔴 P0 紧急 — 请立即处理未映射条目！"
        elif level == "ORANGE":
            msg += "\n   🟠 P1 — 请24小时内处理。"
        elif level == "YELLOW":
            msg += "\n   ⚠️ 预警 — 请关注趋势。"
        else:
            msg += "\n   ✅ 一切正常。"
        return msg

    def send_alert(self, alert: UnmappedAlert):
        """发送告警 — Bark推送 + 终端输出"""
        if alert.level == "GREEN":
            print(alert.message)
            return

        # 终端输出
        print("\n" + "=" * 50)
        print(alert.message)
        print("=" * 50)

        # Bark推送（如果配置了）
        bark_key_path = Path.home() / ".longhun" / "bark_key.txt"
        if bark_key_path.exists():
            bark_key = bark_key_path.read_text().strip()
            if bark_key:
                try:
                    import urllib.request
                    title = f"龍魂·未映射监控 [{alert.level}]"
                    body = f"未映射{alert.count}条 | 超期{alert.stale}条 | 空缺层{'/'.join(alert.layer_gaps) if alert.layer_gaps else '无'}"
                    url = f"https://api.day.app/{bark_key}/{title}/{body}"
                    urllib.request.urlopen(url, timeout=5)
                    print("📱 Bark推送已发送")
                except Exception as e:
                    print(f"⚠️ Bark推送失败: {e}")

    def dashboard(self) -> dict[str, Any]:
        """生成仪表盘数据"""
        self.check()  # 先更新一次
        inbox = self._load_inbox_data()
        items = inbox.get("items", [])

        total = len(items)
        mapped = sum(1 for i in items if i.get("status") == "mapped")
        unmapped = total - mapped

        # 按桶统计
        by_bucket = {}
        for i in items:
            bk = i.get("bucket", "未知")
            by_bucket[bk] = by_bucket.get(bk, 0) + 1

        # 按层统计
        by_layer = {}
        for i in items:
            lk = i.get("target_layer", "未映射")
            by_layer[lk] = by_layer.get(lk, 0) + 1

        # 最近7天趋势
        recent = [h for h in self.history
                  if (datetime.now() - datetime.fromisoformat(h["ts"])).days <= 7]

        dashboard = {
            "generated": datetime.now().isoformat(),
            "dna": DNA,
            "summary": {
                "total": total,
                "mapped": mapped,
                "unmapped": unmapped,
                "coverage_rate": f"{mapped/total:.1%}" if total > 0 else "N/A",
            },
            "by_bucket": by_bucket,
            "by_layer": by_layer,
            "trend_7d": [{"ts": h["ts"], "level": h["level"], "count": h["count"]} for h in recent],
            "thresholds": THRESHOLDS,
        }

        return dashboard

    def run_daemon(self):
        """守护模式：持续监控"""
        print(f"🛡️ 未映射监控守护启动 — 每{THRESHOLDS['check_interval_min']}分钟检查一次")
        print(f"   DNA: {DNA}")
        print(f"   阈值: 预警≥{THRESHOLDS['unmapped_warn']} | P1≥{THRESHOLDS['unmapped_p1']} | P0≥{THRESHOLDS['unmapped_p0']}\n")

        try:
            while True:
                alert = self.check()
                self.send_alert(alert)
                print(f"   [{datetime.now().strftime('%H:%M:%S')}] 下次检查: {THRESHOLDS['check_interval_min']}分钟后")
                time.sleep(THRESHOLDS["check_interval_min"] * 60)
        except KeyboardInterrupt:
            print("\n🛑 监控守护已停止")


def main():
    parser = argparse.ArgumentParser(description="龍魂·未映射条目监控")
    parser.add_argument("--daemon", action="store_true", help="守护模式持续监控")
    parser.add_argument("--alert-threshold", type=int, help=f"设置预警阈值 (当前: {THRESHOLDS['unmapped_warn']})")
    parser.add_argument("--dashboard", action="store_true", help="生成仪表盘JSON")
    parser.add_argument("--export", type=str, help="导出仪表盘到指定文件")

    args = parser.parse_args()
    monitor = UnmappedMonitor()

    if args.alert_threshold:
        THRESHOLDS["unmapped_warn"] = args.alert_threshold
        print(f"✅ 预警阈值已设置为 {args.alert_threshold}")

    elif args.daemon:
        monitor.run_daemon()

    elif args.dashboard or args.export:
        dash = monitor.dashboard()
        output = json.dumps(dash, ensure_ascii=False, indent=2)

        if args.export:
            Path(args.export).write_text(output)
            print(f"✅ 仪表盘已导出到: {args.export}")
        else:
            print(output)

    else:
        # 单次检查
        alert = monitor.check()
        monitor.send_alert(alert)


if __name__ == "__main__":
    main()
