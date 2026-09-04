#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬申·亥时·䷕贲-BROWSER-NET-v1.0-9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂浏览器 · 标准网络设置 v1.0（代理 / DNS-over-HTTPS）
==========================================================
龍魂浏览器 = 原生 Chromium 定制，浏览器本身不设任何访问限制。
本工具提供与 Chrome 设置页同款的标准网络能力（全球浏览器标配）：
  - 查看当前代理/DNS 状态
  - 配置标准代理（manual proxy，仅浏览器级，不动系统）
  - 启用/关闭 DNS over HTTPS（DoH，防 DNS 劫持）

用法：
  lh browser-net status                     # 浏览器代理 + DoH + 系统代理状态
  lh browser-net proxy set --server socks5://127.0.0.1:1080   # 浏览器级标准代理
  lh browser-net proxy clear                # 清除浏览器级代理，回退系统代理
  lh browser-net doh on                     # 启用 DoH（默认 dns.alidns.com + dns.google）
  lh browser-net doh on --templates "https://dns.alidns.com/dns-query"
  lh browser-net doh off                    # 关闭 DoH

铁律：
  - 只写浏览器 Preferences（等同 Chrome 设置页），绝不修改系统代理
  - 写入前自动备份 Preferences
  - 不提供、不内置任何翻墙/绕过工具（中国法律为准绳 · P0）
  - 一国一微调：浏览器在各国遵守当地法律，这里只做标准网络设置
"""
import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

UID = "9622"
ROOT = Path(__file__).resolve().parent.parent

# 龍魂浏览器 profile（Chromium 定制版，目录名保持 Chromium）
PROFILES = {
    "mac": Path.home() / "Library/Application Support/Chromium/Default/Preferences",
    "linux": Path("/root/.config/chromium/Default/Preferences"),
}

DOH_TEMPLATES_DEFAULT = "https://dns.alidns.com/dns-query https://dns.google/dns-query"

sys.path.insert(0, str(ROOT / "bin"))
try:
    from lh_time_engine import get_output_stamp
    _STAMP_OK = True
except Exception:
    _STAMP_OK = False


def stamp_compact() -> str:
    try:
        if _STAMP_OK:
            return get_output_stamp(format_type="compact")
    except Exception:
        pass
    return "#龍芯⚡️丙午·丙申·壬申·亥时·䷕贲"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def audit(msg: str) -> None:
    f = ROOT / ".audit" / "browser_net.log"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(f"[{now_iso()}] {msg}\n")


def pick_prefs() -> Path | None:
    p = PROFILES["mac"] if sys.platform == "darwin" else PROFILES["linux"]
    if p.exists():
        return p
    for cand in PROFILES.values():
        if cand.exists():
            return cand
    return None


def load_prefs(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_prefs(path: Path, data: dict) -> None:
    backup = path.with_suffix(".prefs.bak")
    try:
        shutil.copy2(path, backup)
    except Exception:
        pass
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit(f"SAVE prefs backup={backup.name}")


def system_proxy_summary() -> str:
    try:
        import subprocess
        r = subprocess.run(["scutil", "--proxy"], capture_output=True, text=True, timeout=5)
        out = r.stdout or ""
        bits = []
        for key in ("HTTPEnable", "HTTPProxy", "HTTPPort", "SOCKSEnable", "SOCKSProxy", "SOCKSPort"):
            for line in out.splitlines():
                line = line.strip()
                if line.startswith(key + " :"):
                    bits.append(line.split(":", 1)[1].strip())
                    break
        return " · ".join(bits) if bits else "(无系统代理)"
    except Exception:
        return "(无法读取系统代理)"


def cmd_status(args):
    path = pick_prefs()
    if not path:
        print(f"❌ 未找到浏览器 Preferences（{PROFILES['mac']}）")
        return 1
    data = load_prefs(path)
    proxy = data.get("proxy") or {}
    doh = data.get("dns_over_https") or {}
    print(f"=== 龍魂浏览器网络状态 ===")
    print(f"Preferences : {path}")
    print(f"浏览器代理  : {proxy.get('mode', 'system(跟随系统)')}")
    if proxy.get("server"):
        print(f"  代理服务器 : {proxy['server']}")
    print(f"DoH(DNS)    : {doh.get('mode', 'automatic(浏览器自动)')}")
    if doh.get("templates"):
        print(f"  DoH 模板   : {doh['templates']}")
    print(f"系统代理    : {system_proxy_summary()}")
    print(f"\n说明: 浏览器本身无任何访问限制；能否访问某站点取决于网络通道，各国按当地法律。")
    return 0


def cmd_proxy_set(args):
    path = pick_prefs()
    if not path:
        print("❌ 未找到浏览器 Preferences")
        return 1
    server = args.server.strip()
    if not server.startswith(("http://", "https://", "socks5://", "socks4://")):
        print("❌ 代理格式: http://host:port | https://host:port | socks5://host:port")
        return 1
    data = load_prefs(path)
    data["proxy"] = {"mode": "fixed_servers", "server": server}
    save_prefs(path, data)
    audit(f"PROXY SET {server}")
    print(f"✅ 已写入浏览器级代理: {server}")
    print("   ⚠️ 重启龍魂浏览器后生效（浏览器运行中 Preferences 会被覆盖）")
    print("   提示: 代理须为合法合规网络通道；龍魂不内置/不教翻墙工具。")
    return 0


def cmd_proxy_clear(args):
    path = pick_prefs()
    if not path:
        print("❌ 未找到浏览器 Preferences")
        return 1
    data = load_prefs(path)
    if "proxy" in data:
        del data["proxy"]
        save_prefs(path, data)
        audit("PROXY CLEAR")
        print("✅ 已清除浏览器级代理，回退系统代理")
    else:
        print("ℹ️ 浏览器本就无代理设置（跟随系统）")
    return 0


def cmd_doh_on(args):
    path = pick_prefs()
    if not path:
        print("❌ 未找到浏览器 Preferences")
        return 1
    templates = args.templates or DOH_TEMPLATES_DEFAULT
    data = load_prefs(path)
    data["dns_over_https"] = {"mode": "secure", "templates": templates}
    save_prefs(path, data)
    audit(f"DOH ON {templates}")
    print(f"✅ DoH 已启用（secure）")
    print(f"   模板: {templates}")
    print("   重启龍魂浏览器后生效。")
    return 0


def cmd_doh_off(args):
    path = pick_prefs()
    if not path:
        print("❌ 未找到浏览器 Preferences")
        return 1
    data = load_prefs(path)
    if "dns_over_https" in data:
        del data["dns_over_https"]
        save_prefs(path, data)
        audit("DOH OFF")
        print("✅ DoH 已关闭，回退系统 DNS")
    else:
        print("ℹ️ 浏览器本就未启用 DoH")
    return 0


def main():
    p = argparse.ArgumentParser(prog="lh browser-net", description="龍魂浏览器 · 标准网络设置（代理/DoH）")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="查看代理/DoH 状态").set_defaults(fn=cmd_status)

    sp = sub.add_parser("proxy", help="代理设置")
    sp2 = sp.add_subparsers(dest="proxy_cmd", required=True)
    sps = sp2.add_parser("set", help="设置浏览器级标准代理")
    sps.add_argument("--server", required=True, help="http://host:port | socks5://host:port")
    sps.set_defaults(fn=cmd_proxy_set)
    sp2.add_parser("clear", help="清除浏览器级代理").set_defaults(fn=cmd_proxy_clear)

    sp = sub.add_parser("doh", help="DNS over HTTPS")
    sp2 = sp.add_subparsers(dest="doh_cmd", required=True)
    spd = sp2.add_parser("on", help="启用 DoH")
    spd.add_argument("--templates", default="", help="DoH 模板（空格分隔，默认 阿里DNS+谷歌DNS）")
    spd.set_defaults(fn=cmd_doh_on)
    sp2.add_parser("off", help="关闭 DoH").set_defaults(fn=cmd_doh_off)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
