#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·癸未·卯时·䷚颐-LH-HEALTH-BOARD-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🖥️ 龍魂系统健康看板 v1.0（2026-09-06·六方向②拍板）
用法: lh health [--json] [--watch N秒]
五检: memory-sync 8787(鲲鹏·经nginx) · memory-hub 本地 · autofill 引擎
      lh-memory-sync systemd 服务 · 鲲鹏 SSH 可达
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
SSH_HOST = "root@119.13.90.27"
SSH_KEY = str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519")


def check_local(name, script, args, ok_kw=""):
    try:
        r = subprocess.run([PY, str(ROOT / "bin" / script)] + args,
                           capture_output=True, text=True, timeout=20)
        out = r.stdout + r.stderr
        ok = (ok_kw in out) if ok_kw else (r.returncode == 0)
        first = next((ln.strip() for ln in out.splitlines() if ln.strip()), "")
        return {"name": name, "ok": ok, "detail": first[:80]}
    except Exception as e:  # noqa: BLE001
        return {"name": name, "ok": False, "detail": str(e)[:80]}


def check_ssh(name, ssh_cmd, ok_kw=""):
    try:
        r = subprocess.run(
            ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
             "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", SSH_HOST, ssh_cmd],
            capture_output=True, text=True, timeout=20)
        out = r.stdout.strip()
        ok = (ok_kw in out) if ok_kw else (r.returncode == 0)
        return {"name": name, "ok": ok, "detail": out[:80]}
    except Exception as e:  # noqa: BLE001
        return {"name": name, "ok": False, "detail": str(e)[:80]}


def run_all():
    res = []
    res.append(check_local("memory-sync 8787", "lh_memory_sync_client.py",
                           ["health"], "ok"))
    res.append(check_local("memory-hub 本地", "lh_memory_hub.py", ["status"]))
    res.append(check_local("autofill 引擎", "lh_autofill.py", ["--help"]))
    res.append(check_ssh("lh-memory-sync systemd",
                         "systemctl is-active lh-memory-sync", "active"))
    res.append(check_ssh("鲲鹏 SSH 可达", "echo PONG", "PONG"))
    return res


def print_board(res):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'═' * 58}")
    print(f"  🖥️  龍魂系统健康看板  {ts}")
    print(f"{'═' * 58}")
    all_ok = True
    for r in res:
        icon = "🟢" if r["ok"] else "🔴"
        status = "OK  " if r["ok"] else "FAIL"
        print(f"  {icon} {status} │ {r['name']:<26} │ {r['detail'][:24]}")
        if not r["ok"]:
            all_ok = False
    print(f"{'─' * 58}")
    print(f"  总体状态: {'🟢 全系统正常' if all_ok else '🔴 有服务异常，请排查'}")
    print(f"{'═' * 58}\n")
    return all_ok


def main():
    p = argparse.ArgumentParser(description="🖥️ 龍魂系统健康看板 v1.0")
    p.add_argument("--json", action="store_true")
    p.add_argument("--watch", type=int, default=0, help="轮询秒数")
    a = p.parse_args()
    while True:
        res = run_all()
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print_board(res)
        if not a.watch:
            return 0 if all(r["ok"] for r in res) else 1
        time.sleep(a.watch)


if __name__ == "__main__":
    sys.exit(main())
