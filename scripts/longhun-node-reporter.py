#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂节点人格上报器 v1.0
DNA: #龍芯⚡️丙午·辛未·NODE-REPORTER-v1.0

每个龍魂节点（Mac/鲲鹏/Docker）定时上报人格指纹到验证服务。
作为 systemd 服务或 LaunchAgent 后台运行。
"""
import json
import os
import signal
import socket
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Any

import requests

DNA = "#龍芯⚡️丙午·辛未·NODE-REPORTER-v1.0"
CST = timezone(timedelta(hours=8))

# ─── 配置 ───
DEFAULT_SERVER = os.environ.get("PERSONA_VERIFY_SERVER", "http://127.0.0.1:9623")
NODE_ID = os.environ.get("NODE_ID", f"UID9622-{socket.gethostname()}")
INTERVAL = int(os.environ.get("REPORT_INTERVAL", "300"))  # 默认5分钟

PERSONA_FILE = Path.home() / "longhun-system" / "persona-chain" / "persona-chain-latest.json"
STATUS_FILE = Path.home() / "longhun-system" / "node-persona-status.json"


def detect_node_type() -> str:
    """自动检测节点类型"""
    hostname = socket.gethostname().lower()
    if "kunpeng" in hostname or "arm" in os.uname().machine.lower():
        return "kunpeng"
    if "darwin" in os.uname().sysname.lower():
        return "mac"
    if os.path.exists("/.dockerenv"):
        return "docker"
    return "unknown"


def load_persona() -> dict[str, Any]:
    """加载本地人格链指纹"""
    if not PERSONA_FILE.exists():
        return {
            "value_fingerprint": "0" * 16,
            "emotion_fingerprint": "0" * 16,
            "decision_count": 0,
            "persona_id": "",
        }

    try:
        data = json.loads(PERSONA_FILE.read_text())
        return {
            "value_fingerprint": data.get("value_fingerprint", "0" * 16),
            "emotion_fingerprint": data.get("emotion_fingerprint", "0" * 16),
            "decision_count": data.get("stats", {}).get("total_decisions", 0),
            "persona_id": data.get("persona_id", ""),
        }
    except Exception:
        return {
            "value_fingerprint": "0" * 16,
            "emotion_fingerprint": "0" * 16,
            "decision_count": 0,
            "persona_id": "",
        }


def report(server: str = DEFAULT_SERVER) -> Optional, Any[dict]:
    """上报人格指纹"""
    persona = load_persona()

    payload = {
        "node_id": NODE_ID,
        "value_fingerprint": persona["value_fingerprint"],
        "emotion_fingerprint": persona["emotion_fingerprint"],
        "decision_count": persona["decision_count"],
        "node_type": detect_node_type(),
        "timestamp": int(time.time()),
    }

    try:
        resp = requests.post(f"{server}/verify", json=payload, timeout=10)
        result = resp.json()

        ts = datetime.now(CST).strftime("%H:%M:%S")
        status_icon = {
            "master": "👑", "high": "✅", "medium": "⚠️",
            "low": "❓", "unverified": "❌",
        }.get(result["trust_level"], "⚪")

        print(f"[{ts}] {status_icon} 上报成功 | "
              f"匹配: {result['match_score']}% | "
              f"等级: {result['trust_level']} | "
              f"DNA: {'✅' if result.get('dna_verified') else '❌'}")

        # 保存本地状态
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATUS_FILE.write_text(json.dumps({
            **result,
            "reported_at": int(time.time()),
            "reported_at_human": datetime.now(CST).isoformat(),
        }, ensure_ascii=False, indent=2))

        return result

    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ⚠️ 无法连接验证服务 ({server})")
        return None
    except Exception as e:
        print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] ❌ 上报失败: {e}")
        return None


running = True


def handle_signal(signum, frame):
    global running
    running = False
    print(f"\n[{datetime.now(CST).strftime('%H:%M:%S')}] 👋 上报器退出")


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂节点人格上报器")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="验证服务地址")
    parser.add_argument("--interval", type=int, default=INTERVAL, help="上报间隔(秒)")
    parser.add_argument("--once", action="store_true", help="仅上报一次")
    parser.add_argument("--node-id", default=NODE_ID, help="节点ID")
    args = parser.parse_args()

    global NODE_ID
    NODE_ID = args.node_id

    print(f"🐉 龍魂节点人格上报器")
    print(f"   节点ID: {NODE_ID}")
    print(f"   类型:   {detect_node_type()}")
    print(f"   服务器: {args.server}")
    print(f"   间隔:   {args.interval}s")
    print(f"   人格:   {load_persona().get('persona_id', '未训练')[:24]}...")
    print("")

    # 首次上报
    report(args.server)

    if args.once:
        return

    # 持续上报
    consecutive_failures = 0
    while running:
        time.sleep(args.interval)
        if not running:
            break

        result = report(args.server)
        if result is None:
            consecutive_failures += 1
            if consecutive_failures > 5:
                print(f"  ⚠️ 连续{consecutive_failures}次上报失败，服务可能离线")
        else:
            consecutive_failures = 0


if __name__ == "__main__":
    main()
