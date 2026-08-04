#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 健康检查引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-HEALTH-CHECK-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能:
  - 一次性巡检：验证所有引擎健康状态
  - 持续监控：按间隔循环巡检+告警联动
  - 历史趋势：记录每次巡检结果到JSONL
  - 自动告警：红>0 → 🔴error告警 / 黄>3 → 🟡warn告警
用法:
  lh 健康检查                  一次性巡检
  lh 健康检查 --alert          巡检+告警
  lh 健康检查 --interval 60    持续监控(每60秒)
  lh 健康检查 --history 10     查看最近10次历史
联动: lh_engine_verify.py（数据源）/ lh_alert_engine.py（告警推送）
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 确保能 import 同目录引擎
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ── 历史记录路径 ──
HISTORY_FILE = Path.home() / ".longhun" / "health_history.jsonl"
STATE_FILE = Path.home() / ".longhun" / "health_state.json"
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

# ── 告警阈值 ──
ALERT_RED_THRESHOLD = 0      # 有任何红色就告警
ALERT_YELLOW_THRESHOLD = 3   # 黄色超过此数告警
MAX_HISTORY_LINES = 1000      # 最多保留1000条历史


def run_check(do_alert: bool = False) -> Dict:
    """
    执行一次健康巡检。
    返回巡检记录dict。
    """
    try:
        from lh_engine_verify import ENGINES, check_engine
    except ImportError as e:
        return {
            "timestamp": time.time(),
            "iso": datetime.now().isoformat(),
            "error": f"引擎验证模块不可用: {e}",
            "total": 0, "green": 0, "yellow": 0, "red": 0,
            "details": [],
        }

    details = []
    for name, config in ENGINES.items():
        r = check_engine(name, config)
        details.append(r)

    total = len(details)
    green = sum(1 for d in details if d["status"] == "🟢")
    yellow = sum(1 for d in details if d["status"] == "🟡")
    red = sum(1 for d in details if d["status"] == "🔴")

    record = {
        "timestamp": time.time(),
        "iso": datetime.now().isoformat(),
        "total": total,
        "green": green,
        "yellow": yellow,
        "red": red,
        "health_pct": round(green / total * 100, 1) if total > 0 else 0,
        "details": details,
    }

    # 追加历史
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 裁剪历史（保留最近N条）
    _trim_history()

    # 输出
    _print_check_result(record)

    # 联动告警
    if do_alert:
        _trigger_alert_if_needed(record)

    # 保存当前状态
    _save_state(record)

    return record


def _print_check_result(record: Dict):
    """终端友好输出"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n╔══════════════════════════════════════════════════╗")
    print(f"║  🩺 龍魂 · 健康检查  {now}     ║")
    print(f"╠══════════════════════════════════════════════════╣")

    bar_len = 30
    filled = int(bar_len * record["health_pct"] / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    color = "🟢" if record["health_pct"] >= 80 else "🟡" if record["health_pct"] >= 50 else "🔴"
    print(f"  {color} 健康度: [{bar}] {record['health_pct']}%")
    print(f"  🟢 {record['green']:2d}   🟡 {record['yellow']:2d}   🔴 {record['red']:2d}   📊 总计 {record['total']}")

    # 只显示异常项
    problems = [d for d in record.get("details", []) if d["status"] != "🟢"]
    if problems:
        print(f"  ─────────────────────────────────────────────")
        for p in problems:
            err = p.get("error", "")
            print(f"  {p['status']} {p['name']:<16s} {err}")
    else:
        print(f"  ✅ 所有引擎正常")

    print(f"╚══════════════════════════════════════════════════╝")


def _trigger_alert_if_needed(record: Dict):
    """根据巡检结果触发告警"""
    red = record.get("red", 0)
    yellow = record.get("yellow", 0)

    try:
        from lh_alert_engine import send_alert
    except ImportError:
        print("  ⚠️ 告警引擎不可用，跳过告警推送")
        return

    if red > ALERT_RED_THRESHOLD:
        red_engines = [d["name"] for d in record.get("details", [])
                       if d["status"] == "🔴"]
        title = f"🔴 龍魂健康告警: {red}个服务不可用"
        body = f"不可用服务: {', '.join(red_engines)}\n"
        body += f"健康度: {record['health_pct']}%\n"
        body += f"时间: {record['iso']}"
        sent = send_alert(title, body, "error")
        if sent:
            print(f"  🚨 已发送告警: {', '.join(sent)}")

    elif yellow > ALERT_YELLOW_THRESHOLD:
        title = f"🟡 龍魂健康警告: {yellow}个服务异常"
        body = f"健康度: {record['health_pct']}%\n时间: {record['iso']}"
        sent = send_alert(title, body, "warn")
        if sent:
            print(f"  ⚠️ 已发送警告: {', '.join(sent)}")


def _trim_history():
    """裁剪历史文件到最近N条"""
    try:
        lines = []
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        if len(lines) > MAX_HISTORY_LINES:
            with open(HISTORY_FILE, "w") as f:
                f.writelines(lines[-MAX_HISTORY_LINES:])
    except (IOError, OSError):
        pass


def _save_state(record: Dict):
    """保存当前状态快照"""
    state = {
        "last_check": record["iso"],
        "health_pct": record["health_pct"],
        "green": record["green"],
        "yellow": record["yellow"],
        "red": record["red"],
        "total": record["total"],
    }
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def show_history(n: int = 10):
    """查看最近N次巡检历史"""
    if not HISTORY_FILE.exists():
        print("📋 暂无巡检历史")
        return

    lines = []
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()

    recent = lines[-n:]

    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  📈 龍魂 · 最近 {len(recent)} 次健康检查历史                ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"  {'时间':<20s} {'🟢':>4s} {'🟡':>4s} {'🔴':>4s} {'健康度':>8s}")
    print(f"  {'─'*48}")

    for line in recent:
        try:
            r = json.loads(line)
            ts = r.get("iso", "")[:19].replace("T", " ")
            print(f"  {ts:<20s} {r['green']:>4d} {r['yellow']:>4d} {r['red']:>4d} {r.get('health_pct',0):>7.1f}%")
        except (json.JSONDecodeError, KeyError):
            continue

    print(f"╚══════════════════════════════════════════════════╝")
    print(f"  完整历史: {HISTORY_FILE}")


def show_current_state():
    """显示当前状态快照"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
            print(f"📊 最近一次巡检: {state['last_check']}")
            print(f"   🟢{state['green']} 🟡{state['yellow']} 🔴{state['red']}  健康度: {state['health_pct']}%")
        except (json.JSONDecodeError, KeyError, IOError):
            print("⚠️ 状态文件损坏，将重新巡检")
            run_check(do_alert=False)
    else:
        print("📊 暂无状态快照，执行首次巡检...")
        run_check(do_alert=False)


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·健康检查引擎 — 定期巡检+告警联动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 健康检查                  一次性全量巡检
  lh 健康检查 --alert          巡检+自动告警
  lh 健康检查 --interval 60    每60秒持续监控
  lh 健康检查 --history 10     查看最近10次记录
  lh 健康检查 --state          查看当前状态快照
        """
    )
    parser.add_argument("--alert", action="store_true",
                        help="巡检后自动告警")
    parser.add_argument("--interval", type=int, metavar="SECONDS",
                        help="持续监控间隔（秒）")
    parser.add_argument("--history", type=int, nargs="?", const=10,
                        metavar="N", help="查看最近N次历史（默认10）")
    parser.add_argument("--state", action="store_true",
                        help="查看当前状态快照")
    parser.add_argument("--quiet", action="store_true",
                        help="安静模式（仅输出告警）")

    args = parser.parse_args()

    if args.state:
        show_current_state()
        return

    if args.history is not None:
        show_history(args.history)
        return

    if args.interval:
        print(f"🔄 持续监控模式启动（间隔 {args.interval}s）")
        print(f"   按 Ctrl+C 停止")
        print()
        try:
            while True:
                run_check(do_alert=args.alert)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
    else:
        run_check(do_alert=args.alert)


if __name__ == "__main__":
    main()
