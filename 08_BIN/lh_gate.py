#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·己酉·甲子·䷉履-GATE-CLI-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·操盘网关 CLI v1.0
用法:
  lh gate status          查看网关状态+各AI钥匙
  lh gate audit           查看最近审计(master)
  lh gate write on|off    开/关写操作
  lh gate restart         重启网关(launchd)
  lh gate key <name>      给新AI发钥匙
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parent.parent
CONFIG = SYSTEM_ROOT / "config" / "control_gate.json"
HOST = "127.0.0.1"
PORT = 18790
LABEL = "com.longhun.control-gate"


def _cfg():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _save(cfg):
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def _curl(method, path, payload=None, key=None):
    cmd = ["curl", "-s", "-X", method, f"http://{HOST}:{PORT}{path}"]
    if key:
        cmd += ["-H", f"X-Gate-Key: {key}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def _restart():
    r = subprocess.run(["launchctl", "kickstart", "-k",
                        f"gui/{os.getuid()}/{LABEL}"],
                       capture_output=True, text=True)
    print("🔄 网关已重启" if r.returncode == 0 else f"重启失败: {r.stderr}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    cfg = _cfg()
    master = cfg.get("master_key", "")

    if cmd == "status":
        print(f"🐉 网关: http://{HOST}:{PORT}")
        print(f"   写操作: {'开' if cfg.get('enable_write') else '关(只读)'}")
        print(f"   master_key: {master}")
        for name, info in cfg.get("ais", {}).items():
            mark = "✅" if info.get("enabled", True) else "⛔"
            print(f"   {mark} {name}: {info['key']}")
    elif cmd == "audit":
        out = _curl("POST", "/v1/audit", {}, master)
        try:
            d = json.loads(out)
            print(f"审计共 {d.get('count', 0)} 条，最近:")
            for e in d.get("recent", [])[-15:]:
                print(f"  [{e.get('ts', '')}] {e.get('ai', '')} {e.get('action', '')} "
                      f"{e.get('verdict', '')} {e.get('command', e.get('path', ''))}")
        except Exception:
            print(out)
    elif cmd == "write":
        if len(args) < 2 or args[1] not in ("on", "off"):
            print("用法: lh gate write on|off")
            return
        cfg["enable_write"] = (args[1] == "on")
        _save(cfg)
        print(f"✅ 写操作已{'开启' if cfg['enable_write'] else '关闭(只读)'}")
        _restart()
    elif cmd == "restart":
        _restart()
    elif cmd == "key":
        if len(args) < 2:
            print("用法: lh gate key <名字>")
            return
        out = _curl("POST", "/v1/keygen", {"name": args[1]}, master)
        print(out)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
