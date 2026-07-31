# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-22-LONGHUN-LAUNCHER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂统一启动器 · LongHun Unified Launcher

解决老大痛点：
  - 指令太多，不知道启动哪个
  - 有些服务会过期/重复启动
  - 想要开机自动，但又想能手动看状态

功能：
  - 统一注册所有龍魂常驻服务
  - 检测端口占用，避免重复启动
  - 按依赖顺序启动/停止
  - 生成状态报告
  - 支持开机自动模式

DNA: #龍芯⚡️2026-06-22-LONGHUN-LAUNCHER-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
STATUS_PATH = LOG_DIR / "lh_launcher-status.json"
PID_DIR = LOG_DIR / "pids"

DNA = "#龍芯⚡️2026-06-22-LONGHUN-LAUNCHER-v1.0"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def _ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PID_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Service:
    id: str
    name: str
    port: int
    script: str
    workdir: pathlib.Path
    health_path: str = "/api/health"
    dependencies: List[str] = field(default_factory=list)
    autostart: bool = True
    env: Dict[str, str] = field(default_factory=dict)
    startup_delay: float = 2.0
    startup_timeout: float = 15.0

    def to_dict(self):
        d = asdict(self)
        d["workdir"] = str(self.workdir)
        return d


# 龍魂常驻服务注册表
SERVICES: List[Service] = [
    Service(
        id="longhun-brain",
        name="龍魂脑干",
        port=9625,
        script="cnsh/core/brain/longhun_brain.py",
        workdir=ROOT,
        health_path="/health",
        autostart=True,
        startup_delay=3.0,
    ),
    Service(
        id="identity-portal",
        name="国家数字身份认证入口",
        port=8444,
        script="sovereignty/portal/api_server.py",
        workdir=ROOT / "sovereignty" / "portal",
        health_path="/api/info",
        autostart=True,
        startup_delay=3.0,
        startup_timeout=30.0,
    ),
    Service(
        id="control-panel",
        name="龍魂操作台",
        port=9622,
        script="control-panel/main.py",
        workdir=ROOT / "control-panel",
        dependencies=["longhun-brain"],
        autostart=True,
        startup_delay=5.0,
    ),
]


def is_port_open(port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def http_health_ok(port: int, path: str) -> bool:
    try:
        url = f"http://127.0.0.1:{port}{path}"
        with urllib.request.urlopen(url, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def find_pid_by_port(port: int) -> Optional[int]:
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout.strip():
            return int(result.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None


def get_service_status(svc: Service) -> Dict[str, Any]:
    port_open = is_port_open(svc.port)
    pid = find_pid_by_port(svc.port) if port_open else None
    healthy = False
    if port_open:
        healthy = http_health_ok(svc.port, svc.health_path)
    return {
        "id": svc.id,
        "name": svc.name,
        "port": svc.port,
        "running": port_open,
        "healthy": healthy,
        "pid": pid,
    }


def save_status(report: Dict[str, Any]) -> None:
    _ensure_dirs()
    STATUS_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def load_status() -> Optional[Dict]:
    if STATUS_PATH.exists():
        return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    return None


def start_service(svc: Service) -> Dict[str, Any]:
    status = get_service_status(svc)
    if status["running"]:
        return {**status, "action": "already_running"}

    _ensure_dirs()
    script_path = ROOT / svc.script
    if not script_path.exists():
        return {
            "id": svc.id,
            "error": f"脚本不存在: {script_path}",
            "action": "failed",
        }

    log_file = LOG_DIR / f"{svc.id}.log"
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{ROOT}{':' + env.get('PYTHONPATH', '')}"
    env.update(svc.env)

    # 用 nohup 启动，脱离终端
    cmd = [
        "nohup",
        sys.executable,
        str(script_path),
    ]

    proc = subprocess.Popen(
        cmd,
        cwd=svc.workdir,
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT,
        env=env,
        start_new_session=True,
    )

    # 轮询等待服务启动（重服务导入慢，不能只看一次）
    deadline = time.time() + svc.startup_timeout
    # 先给最小启动时间
    time.sleep(min(svc.startup_delay, svc.startup_timeout))
    while time.time() < deadline:
        status = get_service_status(svc)
        if status["running"] and status["healthy"]:
            status["action"] = "started"
            status["pid_after_start"] = proc.pid
            return status
        time.sleep(1.0)

    # 超时后最终状态
    status = get_service_status(svc)
    status["action"] = "started" if status["running"] else "start_failed"
    status["pid_after_start"] = proc.pid
    return status


def stop_service(svc: Service) -> Dict[str, Any]:
    status = get_service_status(svc)
    if not status["running"]:
        return {**status, "action": "not_running"}

    pid = status.get("pid")
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
            # 如果还活着，强制 kill
            if is_port_open(svc.port):
                os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except PermissionError:
            return {**status, "action": "permission_denied"}

    new_status = get_service_status(svc)
    new_status["action"] = "stopped" if not new_status["running"] else "stop_failed"
    return new_status


def resolve_order(services: List[Service]) -> List[Service]:
    """拓扑排序，按依赖顺序返回服务。"""
    svc_map = {s.id: s for s in services}
    visited: set[str] = set()
    order: List[Service] = []

    def visit(sid: str):
        if sid in visited:
            return
        visited.add(sid)
        svc = svc_map.get(sid)
        if not svc:
            return
        for dep in svc.dependencies:
            visit(dep)
        order.append(svc)

    for svc in services:
        visit(svc.id)
    return order


def cmd_start(args) -> None:
    services = [s for s in SERVICES if s.autostart] if args.autostart else SERVICES
    order = resolve_order(services)

    print(f"🐉 龍魂统一启动器 · DNA: {DNA}")
    print(f"   时间: {_now()}")
    print(f"   模式: {'开机自动' if args.autostart else '手动全部'}")
    print(f"   服务数: {len(order)}")
    print()

    results = []
    for svc in order:
        print(f"▶ 启动 [{svc.name}] :{svc.port} ...", end=" ", flush=True)
        result = start_service(svc)
        results.append(result)
        if result.get("error"):
            print(f"❌ {result['error']}")
        elif result["action"] == "already_running":
            print(f"✅ 已在运行 (pid={result.get('pid')})")
        elif result["running"]:
            print(f"✅ 启动成功 (pid={result.get('pid')})")
        else:
            print(f"⚠️ 启动失败，查看日志: logs/{svc.id}.log")

    report = {
        "dna": _dna("LAUNCHER-START"),
        "timestamp": _now(),
        "mode": "autostart" if args.autostart else "manual",
        "services": results,
    }
    save_status(report)
    print(f"\n状态报告: {STATUS_PATH}")


def cmd_stop(args) -> None:
    services = resolve_order(SERVICES)[::-1]  # 反向停止
    print(f"🛑 停止龍魂服务 ...")
    results = []
    for svc in services:
        print(f"▶ 停止 [{svc.name}] :{svc.port} ...", end=" ", flush=True)
        result = stop_service(svc)
        results.append(result)
        if result["action"] == "not_running":
            print("⚪ 未运行")
        elif result["action"] == "stopped":
            print("✅ 已停止")
        else:
            print("❌ 停止失败")

    report = {
        "dna": _dna("LAUNCHER-STOP"),
        "timestamp": _now(),
        "services": results,
    }
    save_status(report)


def cmd_status(args) -> None:
    print(f"🐉 龍魂服务状态 · {_now()}\n")
    print(f"{'服务':<25} {'端口':<8} {'运行':<8} {'健康':<8} {'PID':<10}")
    print("-" * 65)
    all_healthy = True
    results = []
    for svc in SERVICES:
        st = get_service_status(svc)
        results.append(st)
        running = "🟢" if st["running"] else "🔴"
        healthy = "🟢" if st["healthy"] else ("⚪" if not st["running"] else "🔴")
        pid = str(st.get("pid") or "-")
        print(f"{svc.name:<25} {svc.port:<8} {running:<8} {healthy:<8} {pid:<10}")
        if st["running"] and not st["healthy"]:
            all_healthy = False

    # 显示分层治理状态
    gov_status_path = ROOT / "var" / "governance" / "governance_status.json"
    if gov_status_path.exists():
        try:
            gov = json.loads(gov_status_path.read_text(encoding="utf-8"))
            summary = gov.get("summary", {})
            print("\n【分层治理自愈】")
            print(f"  综合评分: {summary.get('overall_score', 0):.4f}  {summary.get('overall_tricolor', '⚪')}")
            print(f"  🟢 {summary.get('ok', 0)}  🟡 {summary.get('warning', 0)}  🔴 {summary.get('error', 0)}  🧊 {summary.get('frozen', 0)}")
            layers = gov.get("layers", {})
            for lid in ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7"]:
                info = layers.get(lid)
                if info:
                    print(f"  {lid} {info['name']:<18} {info['tricolor']} {info['score']:.2f}")
        except Exception:
            pass

    report = {
        "dna": _dna("LAUNCHER-STATUS"),
        "timestamp": _now(),
        "all_healthy": all_healthy,
        "services": results,
    }
    save_status(report)
    print(f"\n状态报告: {STATUS_PATH}")


def cmd_restart(args) -> None:
    cmd_stop(args)
    print()
    time.sleep(2)
    cmd_start(args)


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂统一启动器")
    parser.add_argument("command", choices=["start", "stop", "restart", "status"])
    parser.add_argument("--autostart", action="store_true", help="开机自动模式：只启动 autostart=True 的服务")
    args = parser.parse_args()

    if args.command == "start":
        cmd_start(args)
    elif args.command == "stop":
        cmd_stop(args)
    elif args.command == "restart":
        cmd_restart(args)
    elif args.command == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
