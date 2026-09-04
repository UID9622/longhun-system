#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cal_client.py - 龍魂 CAL 客户端 (Mac/任意端)
# DNA: #龍芯⚡️丙午·丙申·丙寅·丁酉·䷰革-CAL-CLIENT-MAC-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法:
#   python3 bin/cal_client.py              → 交互模式
#   python3 bin/cal_client.py health       → 一键执行白名单命令
#   python3 bin/cal_client.py "系统状态"   → 自然语言路由
# Token 来源: $LONGHUN_CAL_TOKEN 或 ~/.config/longhun/cal_token (600)

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

CAL_URL = "https://uid9622.cn/cal"
WHITELIST = ["health", "audit", "push", "personas", "dashboard", "engine",
             "brain", "hub", "xuanji", "ping_local", "disk", "uptime"]

def get_token() -> str:
    env = os.environ.get("LONGHUN_CAL_TOKEN", "")
    if env:
        return env.strip()
    p = Path.home() / ".config" / "longhun" / "cal_token"
    try:
        return p.read_text().strip()
    except Exception:
        return ""

def call(payload: dict) -> dict:
    token = get_token()
    if not token:
        print("❌ 未找到令牌：设置 LONGHUN_CAL_TOKEN 或写入 ~/.config/longhun/cal_token")
        sys.exit(2)
    req = urllib.request.Request(
        CAL_URL + "/api/run",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "X-CAL-Token": token},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"status": "error", "exit": e.code, "output": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"status": "error", "exit": -1, "output": f"连接失败: {e}"}

def run_one(arg: str):
    if arg in WHITELIST:
        payload = {"cmd": arg}
    else:
        payload = {"text": arg}
    print(f"🐉 → {arg}")
    d = call(payload)
    out = d.get("output", d.get("detail", "(无输出)"))
    print(out)
    print(f"\n[{d.get('status','?')} | exit={d.get('exit','?')} | {d.get('ts','?')}]")
    return 0 if d.get("exit") == 0 else 1

def interactive():
    print("🐉 龍魂 CAL 客户端 · 公网 wss https://uid9622.cn/cal/")
    print("   白名单: " + " / ".join(WHITELIST))
    print("   或说人话自动路由 | exit 退出\n")
    while True:
        try:
            s = input("龍魂> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见")
            break
        if not s:
            continue
        if s.lower() in ("exit", "quit", "q"):
            print("👋 再见")
            break
        run_one(s)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(run_one(" ".join(sys.argv[1:])))
    interactive()
