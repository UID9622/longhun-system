#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-NOTION-MIRROR-SYNC-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""🐉 lh notion mirror · Mac主控层 → 鲲鹏8768 目录级快照推送引擎 v1.0
================================================================
架构: Mac(持 Notion token·主权) → 目录级快照 → 鲲鹏 8768 只读端点(鸿蒙连接点)
【只推目录元数据】(id/标题/URL/父级/更新时间/图标) · 不含正文内容
     = 正文主权留在主控层 · 鲲鹏/鸿蒙只见目录 → 数据主权边界清晰

用法:
  python3 08_BIN/lh_notion_mirror.py sync [--no-push] [--topo <名>]
  python3 08_BIN/lh_notion_mirror.py status [--json]
  经 lh:  lh notion sync / lh notion status
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DB = os.path.expanduser("~/.longhun/notion_index.db")
AUDIT_JSONL = os.path.expanduser("~/.longhun/notion_audit.jsonl")
LOCAL_MIRROR = os.path.expanduser("~/.longhun/notion_mirror")
REMOTE_DIR = "/opt/longhun-system/deploy/longhun-mcp/notion"
KUNPENG = "root@119.13.90.27"
SSH_KEY = os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519")


def _load_catalog():
    """从本地 notion_index.db 导出目录级快照(仅元数据·无正文)"""
    pages, dbs = [], []
    try:
        con = sqlite3.connect(INDEX_DB)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id,parent_id,title,url,icon,updated_at,scanned_at FROM pages"
            " WHERE status='ok' ORDER BY updated_at DESC").fetchall()
        for r in rows:
            title = r["title"] or ""
            if not title:
                continue
            item = {"id": r["id"], "title": title[:120], "url": r["url"],
                    "parent_id": r["parent_id"] or "", "icon": r["icon"] or "",
                    "updated_at": r["updated_at"] or r["scanned_at"] or ""}
            pages.append(item)  # 本地索引未区分类型·统一按页入目录
        con.close()
    except Exception as e:
        print(f"🟡 读索引失败: {e}")
        return {"pages": [], "databases": [], "meta": {"pages": 0, "synced_at": "", "error": str(e)}}
    meta = {"pages": len(pages), "databases": len(dbs),
            "synced_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "source": "Mac-notion-index", "schema": "catalog-v1"}
    return {"meta": meta, "pages": pages, "databases": dbs}


def _audit_tail():
    """审计链尾 100 条(append-only·只推尾)"""
    try:
        lines = [l for l in open(AUDIT_JSONL, encoding="utf-8") if l.strip()]
        return [json.loads(l) for l in lines[-100:]]
    except Exception:
        return []


def _export(dest_dir, with_topo=None):
    os.makedirs(dest_dir, exist_ok=True)
    cat = _load_catalog()
    with open(os.path.join(dest_dir, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=1)
    tail = _audit_tail()
    with open(os.path.join(dest_dir, "audit_tail.jsonl"), "w", encoding="utf-8") as f:
        for e in tail:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    topo_path = None
    if with_topo:
        cand = os.path.join(ROOT, "docs", "topology", f"{with_topo}_topo.json")
        if os.path.isfile(cand):
            topo_path = cand
            with open(topo_path, encoding="utf-8") as f:
                d = json.load(f)
            with open(os.path.join(dest_dir, "topo.json"), "w", encoding="utf-8") as f:
                json.dump({"topo_name": with_topo, "groups": d.get("groups", []),
                           "nodes": sum(len(g.get("assets", [])) for g in d.get("groups", [])),
                           "synced_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                          f, ensure_ascii=False, indent=1)
    return cat["meta"]["pages"], cat["meta"]["databases"], len(tail), topo_path


def _push():
    """scp 到鲲鹏(私有镜像目录·只读端点读取)"""
    try:
        ssh = ["-e", f"ssh -i {SSH_KEY} -o ConnectTimeout=10"]
        subprocess.run(["ssh", "-i", SSH_KEY, KUNPENG,
                        "mkdir -p " + REMOTE_DIR], check=True, timeout=20)
        subprocess.run(["rsync", "-az"] + ssh + [LOCAL_MIRROR + "/",
                                                 f"{KUNPENG}:{REMOTE_DIR}/"],
                       check=True, timeout=60)
        return True
    except Exception as e:
        print(f"🟡 推送失败: {e}")
        return False


def cmd_sync(args):
    p, d, a, topo = _export(LOCAL_MIRROR, args.topo)
    print(f"📡 快照导出: 页 {p} · 库 {d} · 审计尾 {a}" +
          (f" · topo {topo}" if topo else ""))
    if not args.no_push:
        ok = _push()
        print("✅ 已推送鲲鹏 8768 镜像目录" if ok else "🟡 推送失败(本地快照已备)")
    else:
        print("ℹ️ --no-push: 仅本地导出（可用 status 查看）")
    # 本地审计链留痕
    try:
        with open(AUDIT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                "kind": "mirror_sync", "agent": "lh-notion-mirror",
                                "dna": "#龍芯⚡️2026-09-04-NOTION-MIRROR-v1.0-UID9622",
                                "pages": p, "dbs": d}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def cmd_status(args):
    cat = _load_catalog()
    meta = cat["meta"]
    out = {"ok": True, "local_index": INDEX_DB,
           "pages": meta.get("pages", 0), "databases": meta.get("databases", 0),
           "synced_at": meta.get("synced_at", ""),
           "audit_tail": len(_audit_tail()),
           "note": "目录快照(Mac→鲲鹏8768)·正文主权留在主控层"}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"📡 Notion 镜像状态")
        print(f"  · 本地索引: {out['pages']} 页 / {out['databases']} 库")
        print(f"  · 最近同步: {out['synced_at']}")
        print(f"  · 审计尾: {out['audit_tail']} 条")
        print(f"  · 推送目标: 鲲鹏 8768 ({REMOTE_DIR})")


def main():
    ap = argparse.ArgumentParser(description="lh notion mirror · Mac→鲲鹏8768 目录快照")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("sync", help="导出快照并推送鲲鹏")
    s.add_argument("--no-push", action="store_true", help="仅本地导出不推送")
    s.add_argument("--topo", help="附推指定拓扑名(如 通心译)")
    st = sub.add_parser("status", help="查看镜像状态")
    st.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "sync":
        cmd_sync(a)
    elif a.cmd == "status":
        cmd_status(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
