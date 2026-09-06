#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-06-NOTION-SYNC-COLLECT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""📡 龍魂 Notion 第三批数据源采集器 v1.0
================================================================
为 model/deploy/feedback 三模块提供结构化数据源(引擎读取 JSON/JSONL):
  model    → ~/.longhun/model_state/YYYY-MM-DD.json  (ollama list + 服务状态)
  deploy   → ~/.longhun/deploy_status/YYYY-MM-DD.json (launchd/systemctl 龍魂服务)
  feedback → ~/.longhun/feedback/feedback_*.jsonl     (已有·社区反馈/羞耻墙式记录)

用法:
  python3 08_BIN/lh_notion_collect.py all|model|deploy|feedback [--quiet]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LH = Path.home() / ".longhun"
ROOT = Path(__file__).resolve().parent.parent
GPG_SIGN = ROOT / "bin" / "lh_gpg_sign.py"
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _run(cmd, timeout=60, quiet=True):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           cwd=str(ROOT), env=dict(os.environ, HTTP_PROXY="", HTTPS_PROXY=""))
        return (r.stdout or "").strip() + (("\n" + r.stderr) if r.stderr and not quiet else "").strip()
    except Exception as e:  # noqa: BLE001
        return f"ERR:{e}"


def _date():
    return datetime.now().strftime("%Y-%m-%d")


def collect_model(quiet=True):
    """ollama 模型/服务状态 → model_state/YYYY-MM-DD.json"""
    out = {"version": "1.0", "generated": datetime.now().astimezone().isoformat(),
           "kind": "model_state", "models": [], "service": {}}
    out["service"]["ollama_bin"] = _run(["which", "ollama"]) or "not-found"
    svc = _run(["bash", "-lc", "launchctl list 2>/dev/null | grep -i ollama || systemctl is-active ollama 2>/dev/null"])
    out["service"]["runner"] = svc if svc else "unknown"
    raw = _run(["ollama", "list"])
    for line in raw.splitlines()[1:]:
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 4:
            out["models"].append({"name": parts[0], "id": parts[1],
                                  "size": parts[2], "modified": parts[3]})
    p = LH / "model_state" / f"{_date()}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _sign(p)
    if not quiet:
        print(f"✅ model_state: {p} ({len(out['models'])} 模型)")
    return 0


def collect_deploy(quiet=True):
    """launchd/systemctl 龍魂服务 → deploy_status/YYYY-MM-DD.json"""
    out = {"version": "1.0", "generated": datetime.now().astimezone().isoformat(),
           "kind": "deploy_status", "services": []}
    mac = _run(["bash", "-lc",
                "launchctl list 2>/dev/null | grep -iE 'longhun|uid9622|龍' | head -40"])
    for line in mac.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            out["services"].append({"host": "Mac", "status": parts[0], "pid": parts[1],
                                    "label": parts[2].replace("com.longhun.", "")})
    # 鲲鹏远端(systemd) — 用配置的密钥静默探测, 失败不阻塞
    ssh_key = Path.home() / ".ssh" / "longhun_kunpeng_ed25519"
    if ssh_key.is_file():
        r = _run(["ssh", "-i", str(ssh_key), "-o", "ConnectTimeout=6", "-o", "BatchMode=yes",
                  "root@119.13.90.27",
                  "systemctl list-units --type=service --no-pager --no-legend 2>/dev/null | "
                  "grep -iE 'longhun|uid9622' | awk '{print $1,$3,$4}' | head -30"], timeout=20)
        if r and not r.startswith("ERR"):
            for line in r.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    out["services"].append({"host": "Kunpeng", "service": parts[0],
                                            "status": parts[1], "pid": parts[2]})
    p = LH / "deploy_status" / f"{_date()}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _sign(p)
    if not quiet:
        print(f"✅ deploy_status: {p} ({len(out['services'])} 服务)")
    return 0


def collect_feedback(quiet=True):
    """核对 feedback JSONL 可读性(源已存在·滚动累积)"""
    files = sorted(Path.home().glob("~/.longhun/feedback/feedback_*.jsonl") if False
                   else LH.glob("feedback/feedback_*.jsonl"))
    n = 0
    if files:
        for f in files:
            n += sum(1 for l in f.read_text(encoding="utf-8").splitlines() if l.strip())
    if not quiet:
        print(f"✅ feedback: {len(files)} 文件 · {n} 条")
    return 0


def _sign(p):
    try:
        if GPG_SIGN.is_file():
            _run([sys.executable, str(GPG_SIGN), "sign", str(p)], timeout=30)
    except Exception:  # noqa: BLE001
        pass


def main():
    ap = argparse.ArgumentParser(description="📡 龍魂 Notion 第三批数据源采集器")
    ap.add_argument("target", nargs="?", default="all", choices=["all", "model", "deploy", "feedback"])
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.target in ("all", "model"):
        collect_model(quiet=args.quiet)
    if args.target in ("all", "deploy"):
        collect_deploy(quiet=args.quiet)
    if args.target in ("all", "feedback"):
        collect_feedback(quiet=args.quiet)
    if not args.quiet:
        print("📡 采集完成 · 待 lh_notion_sync.py 建库推送")
    return 0


if __name__ == "__main__":
    sys.exit(main())
