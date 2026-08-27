# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 Agent 编排器守护进程 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
P2 · 常驻监听事件总线 · 自动路由 · 多 Agent 协作触发
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-AGENT-DAEMON-v1.0-UID9622
"""

import argparse
import os
import platform
import signal
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
LONGHUN_DIR = HOME / ".longhun"
ORCH_DIR = LONGHUN_DIR / "agent_orchestrator"
PID_FILE = ORCH_DIR / "daemon.pid"
LOG_FILE = ORCH_DIR / "daemon.log"
DAEMON_NAME = "longhun-agent-orchestrator"

ORCH_SCRIPT = Path(__file__).resolve().parent / "lh_agent_orchestrator.py"


def ensure_dirs():
    ORCH_DIR.mkdir(parents=True, exist_ok=True)


def read_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        return int(PID_FILE.read_text().strip())
    except Exception:
        return None


def write_pid(pid: int):
    ensure_dirs()
    PID_FILE.write_text(str(pid))


def remove_pid():
    if PID_FILE.exists():
        PID_FILE.unlink()


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def do_start(args):
    ensure_dirs()
    pid = read_pid()
    if pid and is_running(pid):
        print(f"🟡 守护进程已在运行 (PID {pid})")
        return 0

    log_fp = open(LOG_FILE, "a", encoding="utf-8")
    cmd = [
        sys.executable, str(ORCH_SCRIPT),
        "listen",
        "--interval", str(args.interval),
        "--limit", str(args.limit),
        "--subscriber", args.subscriber,
    ]
    if args.topic and args.topic != "#":
        cmd.extend(["--topic", args.topic])

    proc = subprocess.Popen(
        cmd,
        stdout=log_fp,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    write_pid(proc.pid)
    # 给一点时间确认进程没立即崩溃
    time.sleep(0.5)
    if proc.poll() is not None:
        print(f"🔴 守护进程启动后立即退出 (code {proc.returncode})")
        print(f"   日志: {LOG_FILE}")
        remove_pid()
        return 1
    print(f"🐉 守护进程启动 (PID {proc.pid})")
    print(f"   日志: {LOG_FILE}")
    print(f"   订阅: topic={args.topic or '#'} subscriber={args.subscriber}")
    return 0


def do_stop(args):
    pid = read_pid()
    if not pid:
        print("🟡 未找到 PID 文件，守护进程未运行")
        return 0
    if not is_running(pid):
        print(f"🟡 PID {pid} 已不存在，清理 PID 文件")
        remove_pid()
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
        # 等待最多 5 秒
        for _ in range(50):
            if not is_running(pid):
                break
            time.sleep(0.1)
        if is_running(pid):
            os.kill(pid, signal.SIGKILL)
            time.sleep(0.2)
        remove_pid()
        print(f"🛑 守护进程已停止 (PID {pid})")
        return 0
    except Exception as e:
        print(f"🔴 停止失败: {e}")
        return 1


def do_status(args):
    pid = read_pid()
    if not pid:
        print("⚪ 守护进程未运行（无 PID 文件）")
        return 0
    if is_running(pid):
        print(f"🟢 守护进程运行中 (PID {pid})")
        print(f"   日志: {LOG_FILE}")
        # 显示最近 3 条日志
        if LOG_FILE.exists():
            lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").strip().split("\n")
            print("   最近日志:")
            for line in lines[-3:]:
                print(f"      {line}")
        return 0
    else:
        print(f"🔴 PID {pid} 不存在，可能已崩溃")
        print(f"   日志: {LOG_FILE}")
        remove_pid()
        return 1


def do_restart(args):
    do_stop(args)
    time.sleep(0.5)
    return do_start(args)


def do_install(args):
    """安装为系统服务（macOS launchd / Linux systemd-user）"""
    ensure_dirs()
    system = platform.system()
    if system == "Darwin":
        plist_dir = HOME / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist_path = plist_dir / f"cn.longhun.{DAEMON_NAME}.plist"
        plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>cn.longhun.{DAEMON_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{ORCH_SCRIPT}</string>
        <string>listen</string>
        <string>--interval</string>
        <string>{args.interval}</string>
        <string>--limit</string>
        <string>{args.limit}</string>
        <string>--subscriber</string>
        <string>{args.subscriber}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{LOG_FILE}</string>
    <key>StandardErrorPath</key>
    <string>{LOG_FILE}</string>
    <key>WorkingDirectory</key>
    <string>{Path(__file__).resolve().parent.parent}</string>
</dict>
</plist>
"""
        plist_path.write_text(plist, encoding="utf-8")
        print(f"🍎 launchd plist 已写入: {plist_path}")
        print(f"   加载: launchctl load -w {plist_path}")
        print(f"   卸载: launchctl unload -w {plist_path}")
        return 0
    elif system == "Linux":
        systemd_dir = HOME / ".config" / "systemd" / "user"
        systemd_dir.mkdir(parents=True, exist_ok=True)
        service_path = systemd_dir / f"{DAEMON_NAME}.service"
        service = f"""[Unit]
Description=龍魂 Agent 编排器守护进程
After=network.target

[Service]
Type=simple
ExecStart={sys.executable} {ORCH_SCRIPT} listen --interval {args.interval} --limit {args.limit} --subscriber {args.subscriber}
Restart=always
RestartSec=5
WorkingDirectory={Path(__file__).resolve().parent.parent}
StandardOutput=append:{LOG_FILE}
StandardError=append:{LOG_FILE}

[Install]
WantedBy=default.target
"""
        service_path.write_text(service, encoding="utf-8")
        print(f"🐧 systemd user service 已写入: {service_path}")
        print(f"   加载: systemctl --user daemon-reload && systemctl --user enable --now {DAEMON_NAME}")
        print(f"   查看: systemctl --user status {DAEMON_NAME}")
        return 0
    else:
        print(f"🟡 不支持自动安装为系统服务: {system}，请用 nohup 或手动后台运行")
        return 1


def build_parser():
    p = argparse.ArgumentParser(description="🐉 龍魂 Agent 编排器守护进程 v1.0")
    sub = p.add_subparsers(dest="command")

    for name in ["start", "stop", "status", "restart", "install"]:
        sp = sub.add_parser(name, help=f"{name} 守护进程")
        sp.add_argument("--interval", type=int, default=5, help="监听轮询间隔秒")
        sp.add_argument("--limit", type=int, default=10, help="单次消费条数")
        sp.add_argument("--subscriber", default="agent-orchestrator", help="订阅者 ID")
        sp.add_argument("--topic", default="#", help="订阅 topic")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    ensure_dirs()
    handlers = {
        "start": do_start,
        "stop": do_stop,
        "status": do_status,
        "restart": do_restart,
        "install": do_install,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
