#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-22-LONGHUN-STATUS-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统状态看板 · LongHun Status Dashboard

双击或在终端运行，一屏看清所有龍魂服务状态。

DNA: #龍芯⚡️2026-06-22-LONGHUN-STATUS-v1.0
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "logs" / "lh_launcher-status.json"


def load_status():
    if STATUS_PATH.exists():
        return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    return None


def check_port(port: int) -> bool:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def http_ok(port: int, path: str = "/api/health") -> bool:
    try:
        url = f"http://127.0.0.1:{port}{path}"
        with urllib.request.urlopen(url, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def main():
    print("🐉 龍魂系统状态看板\n")

    services = [
        ("龍魂操作台", 9622, "/api/health"),
        ("龍魂脑干", 9625, "/health"),
        ("数字身份入口", 8444, "/api/info"),
        ("统一知识中枢", None, None),  # 通过 launcher 状态判断
    ]

    print(f"{'服务':<20} {'状态':<10} {'访问地址/说明':<40}")
    print("-" * 75)
    for name, port, path in services:
        if port is None:
            print(f"{name:<20} {'查看启动器日志':<10} {'logs/lh_launcher-status.json':<40}")
            continue
        running = check_port(port)
        healthy = http_ok(port, path) if running else False
        if running and healthy:
            status = "🟢 健康"
            url = f"http://127.0.0.1:{port}"
        elif running:
            status = "🟡 运行中"
            url = f"端口占用但健康检查失败"
        else:
            status = "🔴 未启动"
            url = f"http://127.0.0.1:{port}"
        print(f"{name:<20} {status:<10} {url:<40}")

    status = load_status()
    if status:
        print(f"\n最后启动: {status.get('timestamp', '未知')}")
        print(f"启动DNA: {status.get('dna', '-')}")

    # 分层治理自愈状态
    gov_status_path = ROOT / "var" / "governance" / "governance_status.json"
    if gov_status_path.exists():
        try:
            gov = json.loads(gov_status_path.read_text(encoding="utf-8"))
            summary = gov.get("summary", {})
            print("\n🛡️ 分层治理自愈状态")
            print(f"{'综合评分':<12} {summary.get('overall_score', 0):.4f}  {summary.get('overall_tricolor', '⚪')}")
            print(f"{'检查项':<12} 🟢 {summary.get('ok', 0)}  🟡 {summary.get('warning', 0)}  🔴 {summary.get('error', 0)}  🧊 {summary.get('frozen', 0)}")
            layers = gov.get("layers", {})
            print(f"{'层':<4} {'名称':<18} {'状态':<6} {'评分':<8}")
            print("-" * 45)
            for lid in ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7"]:
                info = layers.get(lid)
                if info:
                    print(f"{lid:<4} {info['name']:<18} {info['tricolor']:<6} {info['score']:.2f}")
            print(f"\n治理报告: var/governance/governance_status.json")
        except Exception:
            pass

    print("\n💡 快速操作：")
    print("  启动全部:    python3 bin/lh_launcher.py start")
    print("  停止全部:    python3 bin/lh_launcher.py stop")
    print("  刷新状态:    python3 bin/lh_launcher.py status")
    print("  治理巡检:    python3 bin/lh_governance.py status")
    print("  治理自愈:    python3 bin/lh_governance.py heal")

    # 启动精神燃料
    fuel_script = pathlib.Path.home() / '.龍魂' / 'victory_lookbacks' / 'startup_fuel.py'
    if fuel_script.exists():
        try:
            import subprocess as _sp
            out = _sp.run([sys.executable, str(fuel_script)], capture_output=True, text=True, timeout=10)
            if out.stdout:
                print(out.stdout.rstrip())
        except Exception:
            pass


if __name__ == "__main__":
    main()
