#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊寅·午时·䷍大有-ENERGY_MONITOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 · 鲲鹏服务器省电监控器
监控CPU/内存负载，统计API调用与省电积分，生成『安静报告』

用法:
    lh energy                  # 终端输出报告
    lh energy --log            # 追加到日志
    lh energy --watch          # 持续监控模式 (仪表盘)
"""

import os
import sys
import json
import time
import datetime
import subprocess
from pathlib import Path

try:
    import psutil
except ImportError:
    print("需要安装 psutil: pip3 install psutil")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "usage.db"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = LOG_DIR / "energy_report.json"

# 假设大模型推理一次平均耗时（秒）
ASSUMED_LLM_INFERENCE_TIME = 2.0


def get_cpu_load() -> dict:
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "load_avg": psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0.0,
        "cores": psutil.cpu_count(),
    }


def get_memory_usage() -> dict:
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 1),
        "used_gb": round(mem.used / (1024**3), 1),
        "percent": mem.percent,
    }


def get_disk_usage() -> dict:
    disk = psutil.disk_usage(str(ROOT))
    return {
        "total_gb": round(disk.total / (1024**3), 1),
        "used_gb": round(disk.used / (1024**3), 1),
        "percent": disk.percent,
    }


def get_usage_stats() -> dict:
    if not DB_PATH.exists():
        return {"total_requests": 0, "total_duration": 0, "avg_duration": 0, "last_24h_requests": 0}

    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usage_records")
        total = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(duration) FROM usage_records WHERE status='success'")
        total_duration = cursor.fetchone()[0] or 0.0
        avg_duration = total_duration / total if total > 0 else 0.0
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        cursor.execute(
            "SELECT COUNT(*) FROM usage_records WHERE created_at > ?", (yesterday,)
        )
        last_24h = cursor.fetchone()[0] or 0
    except Exception:
        total = total_duration = avg_duration = last_24h = 0
    finally:
        conn.close()

    return {
        "total_requests": total,
        "total_duration": round(total_duration, 2),
        "avg_duration": round(avg_duration, 3),
        "last_24h_requests": last_24h,
    }


def get_docker_status() -> dict:
    """检查Docker容器状态"""
    running = 0
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5,
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        running = len(containers)
    except Exception:
        pass
    return {"docker_containers": running}


def calculate_saved_energy(stats: dict) -> float:
    if stats["total_requests"] == 0:
        return 0.0
    saved_per_call = max(0, ASSUMED_LLM_INFERENCE_TIME - stats["avg_duration"])
    return round(saved_per_call * stats["total_requests"], 2)


def generate_report() -> dict:
    cpu = get_cpu_load()
    mem = get_memory_usage()
    disk = get_disk_usage()
    stats = get_usage_stats()
    docker = get_docker_status()
    saved_seconds = calculate_saved_energy(stats)

    if stats["total_requests"] > 0:
        load_factor = max(0, 100 - cpu["cpu_percent"]) / 100
        activity_factor = min(1, stats["last_24h_requests"] / 100)
        quiet_index = round((load_factor * 0.7 + activity_factor * 0.3) * 100, 1)
    else:
        quiet_index = 0.0

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu": cpu,
        "memory": mem,
        "disk": disk,
        "docker": docker,
        "usage": stats,
        "saved_seconds": saved_seconds,
        "quiet_index": quiet_index,
        "assumed_llm_time": ASSUMED_LLM_INFERENCE_TIME,
    }


def print_report(report: dict):
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    cpu = report["cpu"]
    mem = report["memory"]
    disk = report["disk"]
    docker = report["docker"]
    stats = report["usage"]
    saved = report["saved_seconds"]
    quiet = report["quiet_index"]

    cpu_color = GREEN if cpu["cpu_percent"] < 30 else (YELLOW if cpu["cpu_percent"] < 70 else RED)
    mem_color = GREEN if mem["percent"] < 50 else (YELLOW if mem["percent"] < 80 else RED)
    disk_color = GREEN if disk["percent"] < 70 else (YELLOW if disk["percent"] < 90 else RED)

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}🐉 鲲鹏 · 省电安静报告{RESET}")
    print(f"  {report['timestamp']}")
    print(f"{BOLD}{'-'*60}{RESET}")
    print(f"  CPU 使用率: {cpu_color}{cpu['cpu_percent']:.1f}%{RESET}  (负载: {cpu['load_avg']:.2f}, {cpu['cores']} 核)")
    print(f"  内存使用:   {mem_color}{mem['used_gb']:.1f}GB / {mem['total_gb']:.1f}GB ({mem['percent']:.1f}%){RESET}")
    print(f"  磁盘使用:   {disk_color}{disk['used_gb']:.1f}GB / {disk['total_gb']:.1f}GB ({disk['percent']:.1f}%){RESET}")
    print(f"  Docker:     {BLUE}{docker['docker_containers']}{RESET} 个容器运行中")
    print(f"{BOLD}{'-'*60}{RESET}")
    print(f"  📊 API 调用统计")
    print(f"     总请求: {stats['total_requests']}")
    print(f"     成功平均耗时: {stats['avg_duration']:.3f}s")
    print(f"     24h内请求: {stats['last_24h_requests']}")
    print(f"{BOLD}{'-'*60}{RESET}")

    if saved > 0:
        hours = saved / 3600
        print(f"  ⚡ 省电积分: {BOLD}{saved:.1f} 秒{RESET} (≈ {hours:.2f} 小时)")
    else:
        print(f"  ⚡ 省电积分: 暂无")

    if quiet > 0:
        q_emoji = "😌" if quiet > 70 else "😊" if quiet > 40 else "😐"
        print(f"  🔇 安静指数: {BOLD}{quiet:.1f}/100{RESET} {q_emoji}")

    print(f"{BOLD}{'-'*60}{RESET}")
    if quiet > 60 and saved > 10:
        print(f"  ✅ 鲲鹏服务器很安静，省电效果显著！")
    elif quiet > 30:
        print(f"  🟡 服务器负载一般，可继续优化。")
    else:
        print(f"  🔴 服务器较忙，建议减少并发或增加资源。")
    print(f"{BOLD}{'='*60}{RESET}\n")


def save_report_to_log(report: dict):
    log_file = LOG_DIR / "energy_log.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def watch_mode(interval: int = 10):
    print(f"🔄 开始监控鲲鹏服务器，每 {interval} 秒刷新 (Ctrl+C 停止)\n")
    try:
        while True:
            report = generate_report()
            os.system('clear' if os.name == 'posix' else 'cls')
            print_report(report)
            save_report_to_log(report)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n👋 监控停止")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="鲲鹏服务器省电监控器")
    ap.add_argument("--log", action="store_true", help="仅记录到日志")
    ap.add_argument("--watch", action="store_true", help="持续监控模式")
    ap.add_argument("--interval", type=int, default=10, help="监控间隔(秒)")
    ap.add_argument("--json", action="store_true", help="JSON输出")
    args = ap.parse_args()

    if args.watch:
        watch_mode(args.interval)
        return

    report = generate_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.log:
        save_report_to_log(report)
        print(f"✅ 报告已追加到 {LOG_DIR}/energy_log.jsonl")
    else:
        print_report(report)


if __name__ == "__main__":
    main()
