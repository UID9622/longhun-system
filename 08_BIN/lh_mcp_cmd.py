#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-CMD-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 鲲鹏 MCP Server 命令组（lh mcp）
================================================================
Usage:
  lh mcp list                三 Server 一览
  lh mcp health [server]     本地/远端 MCP 端点存活探测 (--remote 走鲲鹏)
  lh mcp config              配置文件摘要（不含密钥）
  lh mcp log <server>        查看指定 Server 操作审计日志尾部
  lh mcp deploy [--admin-on] 部署到鲲鹏(rsync+systemd)
  lh mcp doc                 打印接入指南路径
所有子命令支持 --json。
"""

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # longhun-system/
MCP_DIR = ROOT / "deploy" / "longhun-mcp"

SERVERS = [
    {"name": "lh-mcp-readonly", "port": 8763, "role": "只读层·图谱/铭碑/健康/命令",
     "risk": "低", "file": "lh_mcp_readonly.py"},
    {"name": "lh-mcp-audit", "port": 8764, "role": "审计层·三色审计/耻辱墙/DNA/日志",
     "risk": "读写", "file": "lh_mcp_audit.py"},
    {"name": "lh-mcp-admin", "port": 8767, "role": "高危层·CNSH编译/发布/topo同步/重载",
     "risk": "高危·默认关闭", "file": "lh_mcp_admin.py",
     "port_note": "2026-09-04 裁决: 原8765归鲲鹏longhun-cal → admin迁8767"},
]

GUIDE = ROOT / "docs" / "鲲鹏MCP接入指南-v1.0.md"
KUNPENG = "root@119.13.90.27"
SSH_KEY = "~/.ssh/longhun_kunpeng_ed25519"


def _log(*a):
    print(*a, file=sys.stderr)


def _json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def cmd_list(args) -> dict:
    rows = []
    for s in SERVERS:
        script = MCP_DIR / s["file"]
        rows.append({**s, "exists": script.exists(),
                     "config": "deploy/longhun-mcp/config/mcp-config.json"})
    return {"servers": rows,
            "guide": str(GUIDE),
            "note": "管理入口 lh mcp health|config|log|deploy|doc"}


def _ping(host: str, port: int) -> dict:
    """JSON-RPC ping → 存活/耗时/错误"""
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"}).encode()
    req = urllib.request.Request(f"http://{host}:{port}/mcp", data=payload,
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    t0 = __import__("time").time()
    try:
        with urllib.request.urlopen(req, timeout=4) as r:
            body = json.loads(r.read().decode("utf-8"))
        ms = round((__import__("time").time() - t0) * 1000)
        ok = body.get("result") is not None and body.get("error") is None
        return {"reachable": True, "ok": ok, "ms": ms, "host": host,
                "port": port, "detail": body.get("result") or body.get("error")}
    except Exception as exc:
        return {"reachable": False, "ok": False, "host": host, "port": port,
                "error": f"{type(exc).__name__}: {exc}"}


def cmd_health(args) -> dict:
    which = args.get("server") or ""
    remote = args.get("remote", False)
    results = []
    if remote:
        host = args.get("host") or KUNPENG.split("@")[1]
    else:
        host = "127.0.0.1"
    for s in SERVERS:
        if which and which != s["name"]:
            continue
        if remote:
            try:
                out = subprocess.run(
                    ["ssh", "-i", SSH_KEY, KUNPENG,
                     f"curl -s -m 4 -H 'Accept: application/json' -H 'Content-Type: application/json' "
                     f"--data '{{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"ping\"}}' "
                     f"http://127.0.0.1:{s['port']}/mcp"],
                    capture_output=True, text=True, timeout=12)
                res = json.loads(out.stdout or "{}")
                ok = res.get("result") is not None
                results.append({"server": s["name"], "port": s["port"],
                                "reachable": ok, "ok": ok,
                                "host": "鲲鹏(ssh)", "detail": res.get("result")})
            except Exception as exc:
                results.append({"server": s["name"], "port": s["port"],
                                "reachable": False, "ok": False,
                                "error": f"ssh/curl: {exc}"})
        else:
            r = _ping(host, s["port"])
            results.append({"server": s["name"], **r})
    return {"results": results, "all_up": all(r.get("ok") for r in results)}


def cmd_config(args) -> dict:
    p = MCP_DIR / "config" / "mcp-config.json"
    wl = MCP_DIR / "config" / "admin-whitelist.json"
    cfg = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    whitelist = json.loads(wl.read_text(encoding="utf-8")) if wl.exists() else {}
    safe = {}
    for k, v in cfg.items():
        if k == "meta":
            continue
        auth = dict(v.get("auth") or {})
        auth.pop("token", None)  # 永不打印密钥
        safe[k] = {**v, "auth": auth}
    return {"config_file": str(p), "whitelist_file": str(wl),
            "config": safe,
            "whitelist": {"ips": whitelist.get("ips", []),
                          "tools": whitelist.get("tools", [])}}


def cmd_log(args) -> dict:
    name = args.get("server") or "lh-mcp-readonly"
    lines = int(args.get("lines") or 30)
    f = Path("~/.longhun/logs/mcp").expanduser() / f"{name}.jsonl"
    if not f.exists():
        return {"log": str(f), "exists": False,
                "hint": f"日志不存在：{name} 尚未有调用记录（stdio/HTTP 均可）"}
    data = f.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
    return {"log": str(f), "exists": True, "lines": data}


def cmd_deploy(args) -> dict:
    script = MCP_DIR / "deploy_to_kunpeng.sh"
    if not script.exists():
        return {"ok": False, "error": f"缺少部署脚本 {script}"}
    argv = ["bash", str(script)]
    if args.get("admin_on"):
        argv.append("--admin-on")
    p = subprocess.run(argv, cwd=str(ROOT), text=True, timeout=600)
    return {"ok": p.returncode == 0, "rc": p.returncode,
            "note": "部署日志见上方输出（远端 systemd: lh-mcp-readonly/audit/admin）"}


def cmd_doc(args) -> dict:
    return {"guide": str(GUIDE),
            "exists": GUIDE.exists(),
            "key": "接入 Claude Desktop / Cursor → 见指南 §2 配置示例"}


def main() -> int:
    args = sys.argv[1:]
    # 拆 --flags 与位置参数
    flags, pos = [], []
    for a in args:
        (flags if a.startswith("--") else pos).append(a)
    json_mode = "--json" in flags
    sub = (pos[0] if pos else "list").lower()
    opts = {"json": json_mode}
    if "--admin-on" in flags:
        opts["admin_on"] = True
    if "--remote" in flags:
        opts["remote"] = True
    # server 位置参数（health/log 需要）
    if len(pos) > 1:
        opts["server"] = pos[1]
    handlers = {"list": cmd_list, "health": cmd_health, "config": cmd_config,
                "log": cmd_log, "deploy": cmd_deploy, "doc": cmd_doc}
    fn = handlers.get(sub)
    if not fn:
        _log(f"❌ 未知子命令: {sub}（可用: {'/'.join(handlers)}）")
        return 1
    result = fn(opts)
    if json_mode:
        _json_out(result)
        return 0
    # 人类可读表格输出
    if sub == "list":
        print("🐉 鲲鹏 MCP Server 一览")
        for s in result["servers"]:
            mark = "✅" if s["exists"] else "❌"
            print(f"  {mark} {s['name']:<16} :{s['port']}  {s['role']}  [{s['risk']}]")
        print(f"  接入指南: {result['guide']}")
    elif sub == "health":
        for r in result["results"]:
            if r.get("ok"):
                print(f"  ✅ {r['server']} :{r['port']} 存活 ({r.get('ms', '?')}ms @ {r.get('host')})")
            else:
                print(f"  🟡 {r['server']} :{r['port']} 未就绪 {r.get('error', '')} "
                      f"{'· 高危层默认 disabled 属正常' if '8767' in str(r.get('port')) else '· 本地可 --stdio 试跑'}")
    elif sub == "config":
        print("🐉 MCP 配置摘要（不含密钥）")
        for name, c in result["config"].items():
            print(f"  {name}: :{c['port']} auth={c['auth'].get('mode')} "
                  f"bind={c.get('host')} peer={c.get('peer_allowlist')}")
        print(f"  白名单: IP={result['whitelist']['ips']} 工具={result['whitelist']['tools']}")
    elif sub == "log":
        r = result
        if not r.get("exists"):
            print(f"🟡 {r.get('hint')}")
        else:
            print(f"📜 {r['log']}（尾部 {len(r['lines'])} 行）")
            for line in r["lines"]:
                print(f"  {line}")
    elif sub == "deploy":
        print("✅ 部署完成" if result.get("ok") else f"🔴 部署失败 rc={result.get('rc')}")
    elif sub == "doc":
        print(f"📖 {result['guide']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
