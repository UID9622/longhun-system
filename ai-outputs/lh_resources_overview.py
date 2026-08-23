#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · 资源总览 v1.0
=========================
一键盘点全系统资源家底，为"资源利用"打底：
  ├─ 本地算力 (CPU/内存/磁盘)
  ├─ Mac 服务 (launchd 龍魂服务数量+运行状态)
  ├─ 鲲鹏服务 (SSH 查询 systemd·不可达则标注)
  ├─ 关键端口 (正在监听的龍魂服务)
  ├─ 外部 API (只列可用状态·绝不打印密钥)
  ├─ AI 模型 (Ollama 本地模型)
  └─ 三色健康总判

DNA: #龍芯⚡️2026-08-23-RESOURCES-OVERVIEW-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import json
import os
import socket
import subprocess
import sys
from datetime import datetime


def run(cmd, timeout=8):
    """安全执行命令，失败返回空串。"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def mac_resources():
    """本地算力。"""
    out = {}
    out["cpu"] = run("sysctl -n hw.ncpu 2>/dev/null") or "?"
    mem_b = run("sysctl -n hw.memsize 2>/dev/null") or "0"
    try:
        out["mem_gb"] = f"{int(mem_b) / 1024 ** 3:.0f}"
    except Exception:
        out["mem_gb"] = "?"
    disk = run("df -k / | awk 'NR==2{print int($4/1024/1024)}' 2>/dev/null")
    out["disk_free_gb"] = disk or "?"
    return out


def mac_services():
    """Mac launchd 龍魂服务。"""
    lst = run("ls ~/Library/LaunchAgents/ 2>/dev/null | grep -i longhun")
    files = [f for f in lst.splitlines() if f and not f.endswith((".asc", ".glyph-backup"))]
    total = len(files)
    running = run("launchctl list 2>/dev/null | grep -c 'com\\.longhun\\|com\\.uid9622\\|ai\\.longhun'") or "?"
    return {"total": total, "running": running}


def kunpeng_services():
    """鲲鹏 systemd 服务（SSH·不可达降级）。"""
    cmd = ("ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o ConnectTimeout=8 "
           "-o StrictHostKeyChecking=no root@119.13.90.27 "
           "\"systemctl list-units --type=service --state=running "
           "2>/dev/null | grep -c longhun\" 2>/dev/null")
    n = run(cmd, timeout=12)
    if n:
        return {"reachable": True, "running": n}
    return {"reachable": False, "running": 0}


def key_ports():
    """正在监听的龍魂关键端口。"""
    out = run("lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | grep -E ':(9622|9631|8783|8779|8775|8899|8082|8088|9630|8778|8091|8970|8971|8972|8766|8769)' | awk '{print $9}' | sort -u | tr '\\n' ' '")
    return out or "(无)" + " · 注意: 端口服务可能已按省电协议休眠"


def external_apis():
    """外部 API 可用状态（只列名·不打印密钥）。"""
    env_paths = [os.path.expanduser("~/.env"),
                 os.path.expanduser("~/.longhun/.env"),
                 "/Users/zuimeidedeyihan/longhun-system/deploy/.env"]
    keys = {
        "Notion": ["NOTION_TOKEN", "NOTION_API_KEY"],
        "GitHub": ["GITHUB_TOKEN", "GH_TOKEN"],
        "CloudBase": ["TCB_SECRETID", "TENCENTCLOUD_SECRETID"],
        "混元AI": ["HUNYUAN_API_KEY"],
        "DeepSeek": ["DEEPSEEK_API_KEY"],
        "Bark推送": ["BARK_KEY"],
        "飞书": ["FEISHU_WEBHOOK", "LARK_WEBHOOK"],
    }
    found = {}
    for name, cands in keys.items():
        hit = False
        for p in env_paths:
            if not os.path.exists(p):
                continue
            try:
                with open(p, encoding="utf-8") as f:
                    content = f.read()
                if any(c in content for c in cands):
                    hit = True
                    break
            except Exception:
                continue
        found[name] = hit
    return found


def local_models():
    """Ollama 本地模型。"""
    out = run("ollama list 2>/dev/null | awk 'NR>1{print $1}' | tr '\\n' ' '")
    return out or "(无/未启动)"


def health_color(apis, kunpeng):
    """三色健康判定。"""
    red = [k for k, v in apis.items() if not v]
    if not kunpeng["reachable"]:
        return "🔴", "鲲鹏不可达·外部API缺 " + ",".join(red)
    if red:
        return "🟡", "鲲鹏在线·未配置API: " + ",".join(red)
    return "🟢", "全链路在线"


def main():
    print("=" * 62)
    print("  🐉 龍魂系统 · 资源总览 v1.0")
    print(f"  📍 UID9622 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    res = mac_resources()
    print(f"\n[本地算力]  CPU {res['cpu']}核 · 内存 {res['mem_gb']}GB · 磁盘剩余 {res['disk_free_gb']}GB")

    ms = mac_services()
    print(f"[Mac 服务]  launchd 龍魂服务共 {ms['total']} 个 · 运行中 {ms['running']}")

    kp = kunpeng_services()
    if kp["reachable"]:
        print(f"[鲲鹏服务]  systemd 运行中 {kp['running']} 个 (119.13.90.27)")
    else:
        print("[鲲鹏服务]  🔴 SSH 不可达·请检查网络/隧道")

    print(f"[关键端口]  {key_ports()}")

    apis = external_apis()
    on = [k for k, v in apis.items() if v]
    off = [k for k, v in apis.items() if not v]
    print(f"[外部 API]  ✅ {len(on)} 个已配置: {', '.join(on)}")
    if off:
        print(f"              ⬜ 未配置: {', '.join(off)}")

    print(f"[AI 模型]  {local_models()}")

    color, note = health_color(apis, kp)
    print(f"\n[三色判定]  {color} {note}")
    print("[提示] 资源利用 = 先看得见 → 再串链路 → 分活用\n")


if __name__ == "__main__":
    main()
