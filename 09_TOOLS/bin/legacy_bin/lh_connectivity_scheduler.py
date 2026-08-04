#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂连通性定时巡检调度器 v1.0
================================
基于现有架构扩展：复用 lh_server_checker.run_all_checks() 检测，
复用 feishu_longhun_bridge /webhook 推送飞书卡片。
只在状态变化或延迟超标时推送，不轰炸。

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-CONNECTIVITY-SCHEDULER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

启动:
  python3 bin/lh_connectivity_scheduler.py
  或: python3 bin/lh_connectivity_scheduler.py --interval 120 --once

环境变量:
  FEISHU_BRIDGE_URL  — 飞书桥接地址 (默认 http://127.0.0.1:9637/webhook)
  FEISHU_WEBHOOK_URL — 飞书自定义机器人 Webhook (可选，直接用飞书桥接)
  CHECK_INTERVAL     — 巡检间隔秒数 (默认 300)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-CONNECTIVITY-SCHEDULER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ─── 配置 ───
FEISHU_BRIDGE_URL = os.getenv("FEISHU_BRIDGE_URL", "http://127.0.0.1:9637/webhook")
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # 默认5分钟

# 延迟阈值
LATENCY_WARN_MS = 50    # >50ms 黄色警告
LATENCY_CRIT_MS = 200   # >200ms 红色严重


class ConnectivityScheduler:
    """连通性定时巡检调度器"""

    def __init__(self):
        self.last_state: dict[str, str] = {}       # 上次各节点状态
        self.last_latency: dict[str, int] = {}     # 上次各节点延迟
        self.first_run = True
        self.consecutive_ok = 0                     # 连续正常次数

    def _load_checker(self):
        """动态加载连通性检测器"""
        try:
            from lh_server_checker import run_all_checks
            return run_all_checks
        except ImportError:
            print("[错误] 无法加载 lh_server_checker.run_all_checks", file=sys.stderr)
            return None

    def _should_alert(self, name: str, status: str, latency: int) -> tuple[bool, str]:
        """判定是否需要推送飞书报警
        
        报警规则:
        1. 状态变化: online→offline/degraded 或 offline→online(恢复通知)
        2. 延迟突变: latency 从 <50ms 跳到 >200ms
        3. 首次运行不报恢复通知
        """
        prev_status = self.last_state.get(name)
        prev_latency = self.last_latency.get(name, 0)

        # 首次运行只报异常，不报正常
        if prev_status is None:
            if status != "online":
                return True, "initial_fault"
            return False, "initial_ok"

        # 状态变化: 在线→离线
        if prev_status == "online" and status in ("offline", "degraded"):
            return True, "status_downgrade"

        # 状态变化: 离线→在线 (恢复)
        if prev_status in ("offline", "degraded") and status == "online":
            return True, "status_recovery"

        # 延迟突变: 正常→严重 ( >200ms )
        if prev_latency <= LATENCY_WARN_MS and latency > LATENCY_CRIT_MS:
            return True, "latency_spike"

        # 延迟突变: 恢复 ( >200ms → <50ms )
        if prev_latency > LATENCY_CRIT_MS and latency <= LATENCY_WARN_MS:
            return True, "latency_recovery"

        return False, "no_change"

    def _build_report(self, data: dict[str, Any], alerts: list[dict[str, Any]]) -> str:
        """构建飞书报告文本"""
        s = data["summary"]
        now_str = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            f"🐉 **龍魂连通性定时巡检**",
            f"⏰ {now_str} CST",
            f"📊 总计 {s['total']} | 🟢在线 {s['online']} | 🔴断线 {s['offline']} | 🟡降级 {s['degraded']} | 健康度 {s['health_pct']}%",
            "",
        ]

        if alerts:
            # 分恢复和故障
            recoveries = [a for a in alerts if "recovery" in a["reason"]]
            faults = [a for a in alerts if "recovery" not in a["reason"]]

            if faults:
                lines.append("🔴 **异常节点:**")
                for a in faults:
                    icon = "🔴" if a["status"] in ("offline", "degraded") else "🟡"
                    lines.append(f"{icon} **{a['name']}** — {a['status']} ({a['latency']}ms)")
                    if a.get("error"):
                        lines.append(f"  ↳ {a['error'][:80]}")
                lines.append("")

            if recoveries:
                lines.append("🟢 **已恢复节点:**")
                for a in recoveries:
                    lines.append(f"✅ **{a['name']}** — 已恢复 ({a['latency']}ms)")
                lines.append("")

        # 延迟超标汇总
        slow_nodes = []
        for name, item in data["items"].items():
            if item["latency_ms"] > LATENCY_WARN_MS:
                slow_nodes.append((name, item["latency_ms"], item["status"]))

        if slow_nodes:
            lines.append(f"🐌 **延迟超标 (>50ms): {len(slow_nodes)} 个**")
            for name, lat, _st in slow_nodes:
                icon = "🔴" if lat > LATENCY_CRIT_MS else "🟡"
                lines.append(f"{icon} {name} — {lat}ms")
        else:
            lines.append("✅ 所有节点延迟正常")

        lines.append("")
        lines.append(f"---")
        lines.append(f"🧬 {DNA}")

        return "\n".join(lines)

    def _push_feishu(self, text: str) -> bool:
        """推送到飞书（通过桥接 :9637/webhook）"""
        payload = {"text": text}

        # 如果配置了直接 Webhook URL，优先使用
        if FEISHU_WEBHOOK_URL:
            payload["webhook_url"] = FEISHU_WEBHOOK_URL

        try:
            req = urllib.request.Request(
                FEISHU_BRIDGE_URL,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                json.loads(resp.read())
                return True
        except urllib.error.URLError as e:
            print(f"[飞书] 桥接不可用 ({e.reason})，报告输出到控制台")
            print(f"\n{'='*60}\n{text}\n{'='*60}\n")
            return False
        except Exception as e:
            print(f"[飞书] 推送异常: {e}")
            return False

    def run_once(self) -> dict[str, Any]:
        """执行一次巡检"""
        run_all = self._load_checker()
        if run_all is None:
            return {"error": "checker not available"}

        data = run_all()
        items = data["items"]
        alerts = []

        # 判定每个节点是否需要报警
        for name, item in items.items():
            status = item["status"]
            latency = item.get("latency_ms", 0)
            should, reason = self._should_alert(name, status, latency)

            if should:
                alerts.append({
                    "name": name,
                    "status": status,
                    "latency": latency,
                    "error": item.get("error", ""),
                    "reason": reason,
                    "critical": item.get("critical", False),
                })

            # 更新状态记忆
            self.last_state[name] = status
            self.last_latency[name] = latency

        # 推送飞书（仅在首次运行或有变化时）
        if alerts or self.first_run:
            report = self._build_report(data, alerts)
            self._push_feishu(report)

            if alerts:
                print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 发现 {len(alerts)} 个变化，已推送飞书")
            elif self.first_run:
                print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 首次巡检完成，基线已建立")
        else:
            self.consecutive_ok += 1
            # 每10次无变化打印一次心跳
            if self.consecutive_ok % 10 == 0:
                print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 连续 {self.consecutive_ok} 次正常，无变化")

        self.first_run = False
        return {"summary": data["summary"], "alerts": len(alerts), "pushed": bool(alerts or False)}

    def run_loop(self, interval: int = CHECK_INTERVAL):
        """循环巡检"""

        print(f"""
🐉 龍魂连通性定时巡检调度器
═══════════════════════════
  {DNA}
  巡检间隔: {interval}s ({interval/60:.0f}分钟)
  飞书桥接: {FEISHU_BRIDGE_URL}
  延迟阈值: 警告 {LATENCY_WARN_MS}ms / 严重 {LATENCY_CRIT_MS}ms
  策略: 状态变化/延迟突变时推送，无变化不打扰
""")

        self.run_once()

        while True:
            time.sleep(interval)
            try:
                self.run_once()
            except Exception as e:
                print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] 巡检异常: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂连通性定时巡检调度器")
    parser.add_argument("--interval", "-i", type=int, default=CHECK_INTERVAL,
                        help=f"巡检间隔秒数 (默认 {CHECK_INTERVAL})")
    parser.add_argument("--once", "-1", action="store_true",
                        help="只跑一次，不循环")
    parser.add_argument("--json", action="store_true",
                        help="JSON 输出结果")
    args = parser.parse_args()

    scheduler = ConnectivityScheduler()

    if args.once:
        result = scheduler.run_once()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        scheduler.run_loop(interval=args.interval)


if __name__ == "__main__":
    main()
