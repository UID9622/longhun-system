#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-SERVICE-RECONCILE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·本机服务对账修复器 v1.0
用途：把散落在终端会话里的核心 API 全部收进 launchd，清理重复/失效任务。
DNA: #龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-SERVICE-RECONCILE-v1.0
"""

import os
import plistlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
ROOT = HOME / "longhun-system"
LAUNCH_AGENTS = HOME / "Library" / "LaunchAgents"
PYTHON = HOME / ".longhun" / "bin" / "python3"
LOG_DIR = ROOT / "logs" / "launchd"
BACKUP_DIR = ROOT / "state" / "launchd_backup"
UID = os.getuid()

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def log(msg, color=GREEN):
    print(f"{color}[SERVICE-RECONCILE]{NC} {msg}")


def warn(msg):
    log(msg, YELLOW)


def err(msg):
    log(msg, RED)


def run(cmd, check=False, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"命令失败: {cmd}\n{result.stderr}")
    return result


def is_loaded(label):
    r = run(f"launchctl list | grep -E '^{label}$' || true", capture=True)
    return label in r.stdout


def unload_plist(path):
    run(f"launchctl unload -w '{path}' 2>/dev/null || true")


def load_plist(path):
    run(f"launchctl load -w '{path}'", check=True)


def port_pids(port):
    r = run(f"lsof -iTCP:{port} -sTCP:LISTEN -t 2>/dev/null || true", capture=True)
    return [p for p in r.stdout.strip().split("\n") if p.isdigit()]


def kill_port(port, reason=""):
    for pid in port_pids(port):
        warn(f"  释放端口 {port} 上的进程 {pid}{reason}")
        run(f"kill {pid} 2>/dev/null || kill -9 {pid} 2>/dev/null || true")
        time.sleep(0.5)


def write_plist(label, program_args, working_dir, logs_name, env=None, keep_alive=True, run_at_load=True, start_interval=None, start_calendar=None):
    path = LAUNCH_AGENTS / f"{label}.plist"
    plist = {
        "Label": label,
        "ProgramArguments": program_args,
        "WorkingDirectory": str(working_dir),
        "RunAtLoad": run_at_load,
        "StandardOutPath": str(LOG_DIR / f"{logs_name}.out.log"),
        "StandardErrorPath": str(LOG_DIR / f"{logs_name}.err.log"),
        "EnvironmentVariables": {
            "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "PYTHONUNBUFFERED": "1",
            "LANG": "zh_CN.UTF-8",
        },
    }
    if env:
        plist["EnvironmentVariables"].update(env)
    if keep_alive:
        plist["KeepAlive"] = True
    if start_interval:
        plist["StartInterval"] = start_interval
    if start_calendar:
        plist["StartCalendarInterval"] = start_calendar
    path.write_bytes(plistlib.dumps(plist))
    return path


def ensure_dirs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LAUNCH_AGENTS.mkdir(parents=True, exist_ok=True)


def backup_old_plist(label):
    src = LAUNCH_AGENTS / f"{label}.plist"
    if src.exists():
        dst = BACKUP_DIR / f"{label}.plist"
        shutil.copy2(src, dst)


def remove_broken_plists():
    broken = {
        "com.longhun.dailyreview": "旧版复盘脚本 daily_review.py 已不存在",
        "com.longhun.capability-web": "capabilities/src 目录已不存在",
        "com.longhun.mcp-mini": "brain/claude_arch 目标已不存在",
        "com.uid9622.longhun.autostart": "longhun-autostart.sh 目标已不存在",
    }
    for label, reason in broken.items():
        path = LAUNCH_AGENTS / f"{label}.plist"
        if path.exists():
            warn(f"移除失效任务: {label}（{reason}）")
            unload_plist(path)
            backup_old_plist(label)
            path.unlink()


def fix_memory_api():
    label = "com.longhun.memory-api"
    port = 8771
    log(f"修复 {label}（端口 {port}）")
    path = LAUNCH_AGENTS / f"{label}.plist"
    backup_old_plist(label)
    unload_plist(path)
    kill_port(port, "  杀掉游离进程")
    path = write_plist(
        label,
        [str(PYTHON), str(ROOT / "bin" / "lh_memory_api.py"), "--host", "127.0.0.1", "--port", str(port)],
        ROOT,
        "memory_api",
    )
    load_plist(path)
    time.sleep(1)


def fix_knowledge_hub_api():
    label = "com.longhun.kg-api"
    port = 8766
    log(f"修复 {label}（端口 {port}）")
    path = LAUNCH_AGENTS / f"{label}.plist"
    backup_old_plist(label)
    unload_plist(path)
    kill_port(port, "  杀掉游离进程")
    path = write_plist(
        label,
        [str(PYTHON), str(ROOT / "bin" / "lh_knowledge_hub_api.py")],
        ROOT,
        "knowledge_hub_api",
    )
    load_plist(path)
    time.sleep(1)


def create_api_service(label, script_name, port, env=None, extra_args=None):
    log(f"创建/修复 {label}（端口 {port}）")
    path = LAUNCH_AGENTS / f"{label}.plist"
    backup_old_plist(label)
    unload_plist(path)
    kill_port(port, "  杀掉游离进程")
    args = [str(PYTHON), str(ROOT / "bin" / script_name), "--host", "127.0.0.1", "--port", str(port)]
    if extra_args:
        args.extend(extra_args)
    path = write_plist(label, args, ROOT, label.replace(".", "_"), env=env)
    load_plist(path)
    time.sleep(1)


def fix_daily_review():
    label = "com.longhun.daily-review"
    old_label = "com.longhun.dailyreview"
    log("修复每日复盘服务")
    # 先删除旧版
    old_path = LAUNCH_AGENTS / f"{old_label}.plist"
    if old_path.exists():
        warn(f"  移除旧版 {old_label}")
        unload_plist(old_path)
        backup_old_plist(old_label)
        old_path.unlink()

    # 创建 runner
    scripts_dir = ROOT / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    runner = scripts_dir / "daily_review_runner.sh"
    runner.write_text(f"""#!/bin/bash
# 龍魂每日復盤·LaunchAgent 運行器（自動生成）
set -e
ROOT="{ROOT}"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

# 加載龍魂密鑰（如果存在）
if [ -f "$HOME/longhun-system/_private/密钥资料/启动脚本/activate_longhun_keys.sh" ]; then
    set -a
    source "$HOME/longhun-system/_private/密钥资料/启动脚本/activate_longhun_keys.sh"
    set +a
fi

# 加載可選 webhook 通道
if [ -f "$HOME/.longhun/webhooks.env" ]; then
    set -a
    source "$HOME/.longhun/webhooks.env"
    set +a
fi

# 運行復盤引擎
{PYTHON} "$ROOT/tools/logging/daily_review_enhanced.py" \
    >> "$LOG_DIR/daily_review_enhanced.out.log" 2>> "$LOG_DIR/daily_review_enhanced.err.log"
""")
    runner.chmod(0o755)

    path = LAUNCH_AGENTS / f"{label}.plist"
    backup_old_plist(label)
    unload_plist(path)
    path = write_plist(
        label,
        ["/bin/bash", str(runner)],
        ROOT,
        "daily_review_enhanced",
        keep_alive=False,
        run_at_load=False,
        start_calendar={"Hour": 23, "Minute": 30},
    )
    load_plist(path)
    log("  每日复盘运行器已就绪（每天 23:30 执行）")


def clean_threshold_pycache():
    log("清理阈值触发器 pycache")
    pyc = ROOT / "bin" / "__pycache__"
    if pyc.exists():
        count = 0
        for f in pyc.glob("lh_threshold_trigger*.pyc"):
            f.unlink()
            count += 1
        log(f"  已删除 {count} 个旧 pyc")
    r = run(f"{PYTHON} {ROOT / 'bin' / 'lh_threshold_trigger.py'} --check health", capture=True)
    if r.returncode == 0:
        log("  阈值触发器健康检查通过")
    else:
        warn(f"  阈值触发器仍异常：{(r.stderr or r.stdout)[:200]}")


def verify_services():
    log("验证核心端口...")
    checks = [
        ("memory-api", 8771, "/v1/memory/health"),
        ("knowledge-hub", 8766, "/v1/li/status"),
        ("antenna-8gate", 8769, "/health"),
        ("guanlan", 8770, "/health"),
        ("xiaoyi-bridge", 8799, "/"),
    ]
    results = []
    for name, port, endpoint in checks:
        pids = port_pids(port)
        if not pids:
            err(f"  🔴 {name}:{port} 未监听")
            results.append((name, False))
            continue
        r = run(f"curl -s -m 2 http://127.0.0.1:{port}{endpoint} | head -c 80", capture=True)
        ok = r.returncode == 0 and len(r.stdout) > 5
        status = "🟢" if ok else "🔴"
        log(f"  {status} {name}:{port} PID={','.join(pids)} 响应={ok}")
        results.append((name, ok))
    return results


def main():
    if os.geteuid() == 0:
        err("本脚本不要以 root 运行")
        sys.exit(1)

    log("开始本机服务对账修复")
    ensure_dirs()

    remove_broken_plists()
    fix_memory_api()
    fix_knowledge_hub_api()
    create_api_service("com.longhun.antenna-8gate", "lh_antenna_8gate_api.py", 8769)
    create_api_service("com.longhun.guanlan", "lh_guanlan_api.py", 8770)
    create_api_service("com.longhun.xiaoyi-bridge", "lh_xiaoyi_bridge_v2.py", 8799)
    fix_daily_review()
    clean_threshold_pycache()

    time.sleep(2)
    results = verify_services()
    ok = all(r[1] for r in results)
    if ok:
        log("🎯 核心服务全部收编进 launchd")
    else:
        warn("部分服务未就绪，请查看日志")

    log(f"备份旧 plist 在：{BACKUP_DIR}")
    log(f"日志目录：{LOG_DIR}")


if __name__ == "__main__":
    main()
