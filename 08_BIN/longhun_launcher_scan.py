#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LONGHUN-LAUNCHER-SCAN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · 启动指令清点器  (LongHun Launcher Inventory)
锚点: UID9622 · 龍芯北辰
跨平台: macOS(本地 M4) + Linux(华为云 ECS)
只读扫描 · 不改动任何文件

DNA: #龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LONGHUN-LAUNCHER-SCAN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

用法:
    python3 longhun_launcher_scan.py                 # 扫描+打印报告
    python3 longhun_launcher_scan.py --json out.json # 同时写一份 JSON
    python3 longhun_launcher_scan.py --root ~/某目录  # 追加扫描目录
    python3 longhun_launcher_scan.py --stale 60      # 60天没动才算"长期没动"
"""

import os, re, json, hashlib, subprocess, platform, argparse, time
from pathlib import Path
from datetime import datetime, timezone

# ==================== 配置区(按需改) ====================
HOME = Path.home()
DEFAULT_ROOTS = [
    HOME / ".龍魂",
    HOME / "longhun-system",
    HOME / "龍盾宝宝",
    HOME / "既检查代码底座",
    HOME / "终端底座",
]
REGISTRY_CANDIDATES = [
    HOME / "longhun-system" / "system_registry.json",
    HOME / ".龍魂" / "system_registry.json",
]
MEMORY_CANDIDATES = [
    HOME / "longhun-system" / "memory.jsonl",
    HOME / ".龍魂" / "memory.jsonl",
]
SCRIPT_EXT = {".py", ".sh", ".command"}
SKIP_EXT   = {".json", ".md", ".txt", ".png", ".jpg", ".log", ".lock", ".pyc", ".html", ".css"}
STALE_DAYS = 30                # 超过这么多天没动 = 长期没动
SERVER_HINTS = re.compile(
    r"(flask|fastapi|uvicorn|gunicorn|http\.server|socketserver|websocket|"
    r"while\s+True|app\.run|serve_forever|\.listen\(|:8080|:9622|:443\b|:80\b)",
    re.IGNORECASE,
)
# ========================================================

def sha256(path):
    """计算文件SHA256"""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def days_since(ts):
    """计算多少天没改过"""
    return round((time.time() - ts) / 86400, 1)

def discover(roots):
    """扫描所有启动脚本"""
    found = {}
    for root in roots:
        root = Path(root).expanduser()
        if not root.exists():
            continue
        for p in root.rglob("*"):
            try:
                if not p.is_file():
                    continue
                ext = p.suffix.lower()
                exe = os.access(p, os.X_OK)
                if ext in SKIP_EXT:
                    continue
                if ext in SCRIPT_EXT or exe:
                    st = p.stat()
                    found[str(p)] = {
                        "path": str(p), "name": p.name, "ext": ext,
                        "size": st.st_size, "mtime": st.st_mtime,
                        "mtime_str": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                        "stale_days": days_since(st.st_mtime),
                        "executable": exe, "sha256": sha256(p),
                    }
            except (PermissionError, OSError):
                continue
    return found

def extract_launch(info):
    """提取启动指令和参数"""
    path = Path(info["path"])
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        text = ""

    info["is_server"] = bool(SERVER_HINTS.search(text))
    cmds, opts = [], []

    if info["ext"] == ".py":
        base = f"python3 {info['path']}"
        opts = sorted(set(re.findall(r"add_argument\(\s*['\"](--[\w\-]+)['\"]", text)))
        if "__main__" in text or opts:
            cmds.append(base)
            cmds += [f"{base} {o}" for o in opts]
    elif info["ext"] in {".sh", ".command"}:
        cmds.append(f"bash {info['path']}")
        opts = sorted(set(re.findall(r"(--[\w\-]+)\)", text)))
        cmds += [f"bash {info['path']} {o}" for o in opts]

    info["launch_cmds"] = cmds or [info["path"]]
    info["options"] = opts
    return info

def load_first(cands):
    """找到第一个存在的候选文件"""
    for c in cands:
        if c.exists():
            return c
    return None

def registry_index(reg):
    """把注册表拍平成 {名字: 记录}"""
    idx = {}
    def walk(node):
        if isinstance(node, dict):
            name = node.get("name") or node.get("module") or node.get("id")
            if name and any(k in node for k in ("version", "path", "file", "hash", "sha256")):
                idx[str(name)] = node
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(reg)
    return idx

def detect_boot():
    """检测开机自启"""
    out = {"systemd": [], "launchd": [], "cron": []}
    sysname = platform.system()

    for d in [HOME/".config"/"systemd"/"user", Path("/etc/systemd/system")]:
        if d.exists():
            out["systemd"] += [str(s) for s in d.glob("*.service")]

    if sysname == "Linux":
        try:
            r = subprocess.run(["systemctl","list-unit-files","--state=enabled","--no-pager"],
                               capture_output=True, text=True, timeout=8)
            out["systemd"] += [l.split()[0] for l in r.stdout.splitlines()
                               if ".service" in l and "enabled" in l]
        except Exception:
            pass

    if sysname == "Darwin":
        for d in [HOME/"Library"/"LaunchAgents", Path("/Library/LaunchDaemons")]:
            if d.exists():
                out["launchd"] += [str(p) for p in d.glob("*.plist")]

    try:
        r = subprocess.run(["crontab","-l"], capture_output=True, text=True, timeout=8)
        out["cron"] += [l.strip() for l in r.stdout.splitlines() if l.strip() and not l.startswith("#")]
    except Exception:
        pass

    return {k: sorted(set(v)) for k, v in out.items()}

def main():
    ap = argparse.ArgumentParser(description="龍魂启动指令清点器")
    ap.add_argument("--root", action="append", default=[], help="追加扫描目录")
    ap.add_argument("--json", help="把完整结果写到这个 JSON 文件")
    ap.add_argument("--stale", type=int, default=STALE_DAYS, help="多少天没动算长期没动")
    args = ap.parse_args()

    roots = DEFAULT_ROOTS + [Path(r).expanduser() for r in args.root]
    print(f"\n╔════════════════════════════════════════════════════════════════════╗")
    print(f"║           🐉 龍魂启动指令清点器 v1.0 🐉                        ║")
    print(f"║        {datetime.now().strftime('%Y-%m-%d %H:%M')} · {platform.system():6s} · {platform.node()}            ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝\n")

    live = [str(r) for r in roots if Path(r).expanduser().exists()]
    print(f"扫描目录: {', '.join(live) or '(一个都不存在,改下配置区的 DEFAULT_ROOTS)'}\n")

    found = discover(roots)
    for k in found:
        extract_launch(found[k])

    reg_path = load_first(REGISTRY_CANDIDATES)
    try:
        reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path else None
    except Exception:
        reg = None
    ridx = registry_index(reg) if reg else {}

    mem_path = load_first(MEMORY_CANDIDATES)
    mem_text = mem_path.read_text(encoding="utf-8", errors="ignore") if mem_path else ""
    for v in found.values():
        v["in_memory"] = v["name"] in mem_text

    disk_names = {v["name"] for v in found.values()}
    unregistered = sorted(v["name"] for v in found.values() if v["name"] not in ridx)
    registered_missing = sorted(n for n in ridx if n not in disk_names)
    upgraded = []
    for v in found.values():
        rec = ridx.get(v["name"])
        if rec:
            old = str(rec.get("hash") or rec.get("sha256") or "")
            if old and v["sha256"] and not v["sha256"].startswith(old[:12]):
                upgraded.append(v["name"])

    stale   = sorted([v for v in found.values() if v["stale_days"] >= args.stale], key=lambda x:-x["stale_days"])
    servers = [v for v in found.values() if v["is_server"]]
    boot    = detect_boot()
    L = lambda: print("─"*70)

    print(f"📦 共找到启动脚本 {len(found)} 个\n")
    L(); print("① 全部启动指令(可直接复制):"); L()
    for v in sorted(found.values(), key=lambda x:x["path"]):
        flag = "🌐服务" if v["is_server"] else ("🔧可执行" if v["executable"] else "📄脚本")
        rg = "✅登记" if v["name"] in ridx else "❓未登记"
        mm = "🧠记忆有" if v["in_memory"] else "🆕记忆无"
        print(f"\n[{flag}·{rg}·{mm}·{v['stale_days']:>5.1f}天前改]")
        print(f"  路径: {v['path']}")
        print(f"  DNA:  {v['sha256'][:16]}...")
        for c in v["launch_cmds"]:
            print(f"  $ {c}")

    L(); print(f"② 长期没动(≥{args.stale}天,可能你忘了的):"); L()
    if stale:
        print("\n".join(f"   {v['stale_days']:>6.1f}天  {v['path']}" for v in stale))
    else:
        print("   (无)")

    L(); print("③ 跟注册表 + 记忆核对:"); L()
    print(f"   注册表: {reg_path or '没找到 system_registry.json'}")
    print(f"   记忆库: {mem_path or '没找到 memory.jsonl'}")
    print(f"   ❓ 磁盘有、注册表没登记 ({len(unregistered)}): {', '.join(unregistered) or '无'}")
    print(f"   ⚠️  注册表有、磁盘找不到(改名/移走?) ({len(registered_missing)}): {', '.join(registered_missing) or '无'}")
    print(f"   🔼 疑似升级过(hash 对不上) ({len(upgraded)}): {', '.join(upgraded) or '无'}")

    L(); print("④ 开机自启(systemd / launchd / cron):"); L()
    for k, vs in boot.items():
        print(f"   [{k}] {len(vs)} 项")
        for x in (vs[:3] + ["..."] if len(vs) > 3 else vs):
            print(f"       {x}")

    L(); print("⑤ 常驻服务候选(上华为云公开要防断片的):"); L()
    if servers:
        print("   这些像是要一直跑的服务。上 ECS 公开时别直接 python3 跑——")
        print("   要用 systemd 守护,挂了能自动拉起,才不会老断片:\n")
        for v in servers:
            unit = v["name"].rsplit(".",1)[0]
            print(f"   ▶ {v['path']}")
            print(f"     建议写 ~/.config/systemd/user/{unit}.service :")
            print( "       [Unit]")
            print(f"       Description=龍魂 {unit}")
            print( "       [Service]")
            print(f"       ExecStart=/usr/bin/python3 {v['path']}")
            print( "       Restart=always")
            print( "       RestartSec=3")
            print( "       [Install]")
            print( "       WantedBy=default.target")
            print()
        print(f"   装好后: systemctl --user daemon-reload && systemctl --user enable --now <名字>")
        print( "   ★ 关键(防你一退出登录就断): sudo loginctl enable-linger $USER")
    else:
        print("   (没扫到明显的常驻服务)")

    if args.json:
        blob = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "host": platform.node(), "os": platform.system(),
            "registry_path": str(reg_path) if reg_path else None,
            "memory_path": str(mem_path) if mem_path else None,
            "scripts": list(found.values()),
            "unregistered": unregistered, "registered_missing": registered_missing,
            "upgraded": upgraded, "stale": [v["path"] for v in stale],
            "boot": boot, "servers": [v["path"] for v in servers],
        }
        Path(args.json).write_text(json.dumps(blob, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n💾 完整结果已写入: {args.json}")

    print("\n🐉 完。只读扫描,没碰你任何文件。")

if __name__ == "__main__":
    main()
