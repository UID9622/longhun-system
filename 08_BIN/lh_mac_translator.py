#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Mac 身体翻译官
DNA: #龍芯⚡️丙午·癸未·丁未-MAC-PULSE-TRANSLATOR-v1.0
功能：把 Mac 系统监控数据（CPU/内存/磁盘/网络/电池/进程/定时器）
      翻译成普通人能看懂的大白话，同时保留技术原始值。
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DNA = "#龍芯⚡️丙午·癸未·丁未-MAC-PULSE-TRANSLATOR-v1.0"


def run(cmd: List[str], timeout: int = 5) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.stdout if proc.returncode == 0 else ""
    except Exception:
        return ""


def _to_float(text: str) -> Optional[float]:
    try:
        return float(text)
    except Exception:
        return None


def get_cpu() -> Dict:
    """读取 CPU 负载"""
    text = run(["top", "-l", "2", "-n", "0", "-F"], timeout=8)
    # 取最后一组 CPU usage
    match = re.findall(r"CPU usage:\s+(\d+\.?\d*)%\s+user,\s+(\d+\.?\d*)%\s+sys,\s+(\d+\.?\d*)%\s+idle", text)
    if match:
        user, sys, idle = map(float, match[-1])
        return {"user": user, "sys": sys, "idle": idle, "used": round(user + sys, 1)}
    return {"user": 0, "sys": 0, "idle": 0, "used": 0}


def get_memory() -> Dict:
    """读取内存使用"""
    text = run(["vm_stat"])
    pagesize = 4096  # macOS 默认页大小
    values = {}
    for line in text.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().replace(".", "").replace("M", "").replace("G", "")
            num = _to_float(val)
            if num is not None:
                values[key.strip()] = num * pagesize / (1024 ** 3)  # GB

    total = run(["sysctl", "-n", "hw.memsize"])
    total_gb = _to_float(total.strip()) / (1024 ** 3) if total.strip() else 16.0

    free = values.get("Pages free", 0) + values.get("Pages inactive", 0) + values.get("Pages speculative", 0)
    used = total_gb - free
    used = max(0, used)
    pct = round(used / total_gb * 100, 1) if total_gb else 0
    return {"total_gb": round(total_gb, 2), "used_gb": round(used, 2), "free_gb": round(free, 2), "used_pct": pct}


def get_disk() -> List[Dict]:
    """读取磁盘使用"""
    text = run(["df", "-h"])
    disks = []
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 9 and parts[0].startswith("/dev/"):
            disks.append({
                "device": parts[0],
                "size": parts[1],
                "used": parts[2],
                "free": parts[3],
                "pct": parts[4].replace("%", ""),
                "mount": parts[8],
            })
    return disks


def _get_primary_iface() -> str:
    """找当前活跃的非环回网卡"""
    text = run(["ifconfig"])
    candidates = []
    current = None
    for line in text.splitlines():
        if line and not line.startswith("\t"):
            current = line.split(":")[0]
        if current and "status: active" in line and current != "lo0":
            candidates.append(current)
    # 优先常见物理网卡
    for preferred in ("en0", "en1", "en2", "en3", "en4", "en5", "en6"):
        if preferred in candidates:
            return preferred
    return candidates[0] if candidates else "en0"


def get_network() -> Dict:
    """读取网络流量（取主网卡）"""
    iface = _get_primary_iface()
    text = run(["netstat", "-I", iface, "-b", "-n"])
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) >= 2:
        parts = lines[1].split()
        if len(parts) >= 10:
            ibytes = _to_float(parts[6]) or 0
            obytes = _to_float(parts[9]) or 0
            return {
                "iface": iface,
                "ibytes": ibytes,
                "obytes": obytes,
                "in_mb": round(ibytes / (1024 ** 2), 2),
                "out_mb": round(obytes / (1024 ** 2), 2),
            }
    return {"iface": iface, "ibytes": 0, "obytes": 0, "in_mb": 0, "out_mb": 0}


def get_battery() -> Dict:
    """读取电池状态"""
    text = run(["pmset", "-g", "batt"])
    pct = re.search(r"(\d+)%", text)
    status = re.search(r"(\w+)\s*;", text)
    time_left = re.search(r"(\d+:\d+)\s*(remaining|left)?", text)
    return {
        "pct": int(pct.group(1)) if pct else None,
        "status": status.group(1) if status else "未知",
        "time_left": time_left.group(1) if time_left else "--",
    }


def get_uptime() -> str:
    return run(["uptime"]).strip()


def get_top_processes(n: int = 8) -> List[Dict]:
    """读取最耗 CPU 的进程"""
    text = run(["top", "-l", "1", "-n", str(n), "-o", "cpu", "-F"], timeout=6)
    procs = []
    lines = text.splitlines()
    in_procs = False
    for line in lines:
        if line.startswith("PID"):
            in_procs = True
            continue
        if in_procs and line.strip():
            parts = line.split()
            # top -F 格式：PID COMMAND %CPU TIME #TH #WQ #PORTS MEM PURG CMPRS PGRP PPID STATE ...
            if len(parts) >= 12:
                try:
                    pid = int(parts[0])
                    name = parts[1]
                    cpu = parts[2]
                    mem = parts[7]
                    procs.append({"pid": pid, "name": name, "cpu": cpu, "mem": mem})
                except Exception:
                    pass
        if in_procs and not line.strip():
            break
    return procs[:n]


def get_timers() -> Dict:
    """读取系统定时器（launchctl + cron）"""
    launchctl = run(["launchctl", "list"], timeout=5)
    cron = run(["crontab", "-l"], timeout=3)
    agents = []
    for line in launchctl.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3 and parts[2]:
            agents.append({"pid": parts[0], "status": parts[1], "label": parts[2]})
    cron_lines = [l for l in cron.splitlines() if l.strip() and not l.strip().startswith("#")]
    return {"launchctl_count": len(agents), "cron_count": len(cron_lines), "agents": agents[:10], "cron": cron_lines[:5]}


def _level(value: float, warn: float, crit: float) -> str:
    if value >= crit:
        return "🔴 危险"
    if value >= warn:
        return "🟡 偏高"
    return "🟢 正常"


def _battery_status(pct: Optional[int], status: str) -> str:
    if pct is None:
        return "🔌 可能是台式机或未检测到电池"
    if status.lower() in ("charging", "ac"):
        return f"🔌 充电中，当前 {pct}%"
    if pct <= 20:
        return f"🪫 电量低（{pct}%），建议充电"
    if pct <= 50:
        return f"🟡 电量中等（{pct}%）"
    return f"🟢 电量充足（{pct}%）"


def print_simple(cpu, mem, disk, net, battery, uptime, timers, procs):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        🐉 龍魂·Mac 身体翻译官（大白话版）                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║ 检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<43} ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    print(f"🧠 大脑活跃度（CPU）：{cpu['used']}%  {_level(cpu['used'], 70, 90)}")
    print(f"   → 解释：{cpu['used']}% 的算力正在干活。超过 70% 会开始卡，90% 以上基本动不了。\n")

    print(f"💾 记忆仓库（内存）：已用 {mem['used_gb']:.1f}G / 总共 {mem['total_gb']:.1f}G  ({mem['used_pct']}%)  {_level(mem['used_pct'], 75, 90)}")
    print(f"   → 解释：内存就像办公桌，堆太满会慢。建议保留 20% 以上空闲。\n")

    print("💿 仓库容量（磁盘）：")
    # 优先显示有风险的卷，最多显示 6 个
    risky = [d for d in disk if (_to_float(d["pct"]) or 0) >= 80]
    shown = (risky + disk)[:6]
    for d in shown:
        pct = _to_float(d["pct"]) or 0
        print(f"   • {d['mount']}: 已用 {d['used']} / 总共 {d['size']} ({pct}%)  {_level(pct, 80, 95)}")
    print("   → 解释：磁盘太满（>90%）会导致系统卡顿、软件崩溃。\n")

    print(f"🌐 网络流量：当前主网卡 {net['iface']}")
    print(f"   → 已接收 {net['in_mb']:.1f} MB，已发送 {net['out_mb']:.1f} MB\n")

    print(f"🔋 电池状态：{_battery_status(battery['pct'], battery['status'])}")
    print(f"   → 预计剩余时间：{battery['time_left']}\n")

    print(f"⏱️ 系统定时器：{timers['launchctl_count']} 个后台服务，{timers['cron_count']} 条定时任务")
    print("   → 解释：这些是 Mac 自动执行的任务，包括系统更新、同步、守护进程等。\n")

    print("🏃 当前最忙的进程：")
    for p in procs[:5]:
        print(f"   • {p['name']:<20} CPU {p['cpu']:>5}  内存 {p['mem']:>5}")

    print(f"\n🧬 DNA: {DNA}")


def print_tech(cpu, mem, disk, net, battery, uptime, timers, procs):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        🐉 龍魂·Mac 身体翻译官（技术版）                      ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    print(f"CPU: user={cpu['user']}% sys={cpu['sys']}% idle={cpu['idle']}% used={cpu['used']}%")
    print(f"MEM: total={mem['total_gb']}G used={mem['used_gb']}G free={mem['free_gb']}G pct={mem['used_pct']}%")
    print(f"NET: iface={net['iface']} in={net['in_mb']}MB out={net['out_mb']}MB")
    print(f"BATT: pct={battery['pct']} status={battery['status']} time_left={battery['time_left']}")
    print(f"UPTIME: {uptime}")
    print(f"TIMERS: launchctl={timers['launchctl_count']} cron={timers['cron_count']}")
    print("\nDISK:")
    for d in disk:
        print(f"  {d['device']} -> {d['mount']}: {d['used']}/{d['size']} ({d['pct']}%) free={d['free']}")
    print("\nTOP PROCESSES:")
    for p in procs:
        print(f"  pid={p['pid']:<7} cpu={p['cpu']:>6} mem={p['mem']:>6} {p['name']}")
    print("\nSAMPLE TIMERS:")
    for a in timers["agents"][:8]:
        print(f"  [{a['status']}] {a['label']}")
    for c in timers["cron"]:
        print(f"  [cron] {c}")

    print(f"\n🧬 DNA: {DNA}")


def main():
    parser = argparse.ArgumentParser(description="龍魂·Mac 身体翻译官")
    parser.add_argument("--tech", action="store_true", help="显示技术原始数据")
    parser.add_argument("--procs", type=int, default=8, help="显示进程数量")
    args = parser.parse_args()

    cpu = get_cpu()
    mem = get_memory()
    disk = get_disk()
    net = get_network()
    battery = get_battery()
    uptime = get_uptime()
    timers = get_timers()
    procs = get_top_processes(args.procs)

    if args.tech:
        print_tech(cpu, mem, disk, net, battery, uptime, timers, procs)
    else:
        print_simple(cpu, mem, disk, net, battery, uptime, timers, procs)


if __name__ == "__main__":
    main()
