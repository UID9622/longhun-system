#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-NOTION-MCP-MIRROR-8768-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""╔══════════════════════════════════════════════════════════════════╗
║  🐉 鲲鹏 Notion 数据镜像只读端点 (8768) · lh-notion-mcp v1.0        ║
║  架构: Mac 主控层(持 Notion token·主权) → 目录级快照推送 → 本端点     ║
║  本端点: 零 token · 零境外流量 · 纯只读 · 鸿蒙 SDK 的连接点           ║
╚══════════════════════════════════════════════════════════════════╝

【为什么不在鲲鹏直连 Notion】
Notion token = D2 机密(主权级) · 鲲鹏在境外(ap-southeast-1) · 明文入云
违反第五层5.3「D2入云必须端侧加密」与跨境禁止。故：
  主控(Mac) 持有 token 做全量读写 → 仅推送【目录级快照】(id/标题/URL/
  父级/更新时间·不含正文) 到本端点 → 鸿蒙/远端只读查询目录与龍魂侧数据。

【数据源】(Mac 侧 lh notion sync 推送·路径用环境变量覆盖)
  NOTION_MIRROR_DIR=<dir>/catalog.json     目录快照(默认 /opt/longhun-mcp/notion/)
  NOTION_MIRROR_DIR=<dir>/audit_tail.jsonl 审计链尾部
  NOTION_MIRROR_DIR=<dir>/topo.json        龍魂拓扑快照(可选)

【MCP Tools(只读)】
  get_mirror_status()          快照状态(时间/页数/审计数/拓扑数)
  search_catalog(query)        目录秒搜(标题/URL·纯本地零API)
  list_catalog(kind,limit)     目录列表(page/database/all)
  recent_audit(limit)          审计链最近记录
  topo_snapshot()              龍魂拓扑快照摘要

【HTTP】  /mcp   MCP JSON-RPC (鸿蒙 SDK 桥接)
"""

import json
import os
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_mcp_core import (  # noqa: E402
    MCPServer, MCPError, ERR_INVALID_PARAMS, now_iso, run_http,
)

SERVER_NAME = "lh-notion-mcp"
VERSION = "1.0.0"
DEFAULT_PORT = 8768

MIRROR_DIR = os.environ.get(
    "NOTION_MIRROR_DIR",
    "/opt/longhun-system/deploy/longhun-mcp/notion",
)

DEFAULT_CFG = {
    "server": SERVER_NAME,
    "port": DEFAULT_PORT,
    "host": "127.0.0.1",
    "auth": {"mode": "none"},
    "log_dir": "~/.longhun/logs/mcp",
    "lh_root": "",
    "peer_allowlist": [],
}


def _catalog_path():
    return os.path.join(MIRROR_DIR, "catalog.json")


def _load_catalog():
    """读目录快照 → {pages:[...], databases:[...], meta:{...}}·纯只读"""
    try:
        with open(_catalog_path(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"pages": [], "databases": [], "meta": {"pages": 0, "synced_at": ""}}


def _audit_tail():
    try:
        p = os.path.join(MIRROR_DIR, "audit_tail.jsonl")
        lines = [l for l in open(p, encoding="utf-8") if l.strip()]
        return [json.loads(l) for l in lines[-50:]]
    except Exception:
        return []


def _topo_snapshot():
    try:
        p = os.path.join(MIRROR_DIR, "topo.json")
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {"ok": False, "note": "无拓扑快照·主控侧暂未推送"}


def _make_server():
    srv = MCPServer(SERVER_NAME, VERSION, DEFAULT_CFG)

    def h_status(_):
        cat = _load_catalog()
        meta = cat.get("meta", {})
        return {"name": SERVER_NAME, "version": VERSION,
                "ok": bool(meta.get("pages") is not None),
                "synced_at": meta.get("synced_at", ""),
                "pages": meta.get("pages", 0),
                "databases": meta.get("databases", 0),
                "audit_tail": len(_audit_tail()),
                "topo": bool(os.path.exists(os.path.join(MIRROR_DIR, "topo.json"))),
                "note": "只读镜像端点·零 token·正文需主控层(Mac)"}

    def h_search(a):
        q = str((a or {}).get("query", "")).lower().strip()
        cat = _load_catalog()
        items = cat.get("pages", []) + cat.get("databases", [])
        if q:
            items = [x for x in items if q in (x.get("title", "") or "").lower()
                     or q in (x.get("id", "") or "").lower() or q in (x.get("url", "") or "")]
        limit = int((a or {}).get("limit") or 20)
        return {"count": len(items), "items": items[:limit],
                "note": "目录快照搜索·本地零 API·需最新目录请主控侧 lh notion sync"}

    def h_list(a):
        kind = ((a or {}).get("kind") or "all").strip()
        limit = int((a or {}).get("limit") or 50)
        cat = _load_catalog()
        pools = []
        if kind in ("all", "page"):
            pools += cat.get("pages", [])
        if kind in ("all", "database"):
            pools += cat.get("databases", [])
        return {"kind": kind, "count": len(pools), "items": pools[:limit]}

    def h_audit(a):
        limit = int((a or {}).get("limit") or 20)
        return {"count": len(_audit_tail()), "items": _audit_tail()[-limit:]}

    def h_topo(_):
        return _topo_snapshot()

    srv.add_tool("get_mirror_status",
                 "镜像端点状态：快照时间/页数/审计数/拓扑是否就绪。鸿蒙连接后第一步调用。",
                 {"type": "object", "properties": {}, "additionalProperties": False},
                 h_status)
    srv.add_tool("search_catalog",
                 "目录快照搜索(标题/URL/ID·本地零API)·适合鸿蒙语音唤起秒查。",
                 {"type": "object",
                  "properties": {"query": {"type": "string"},
                                 "limit": {"type": "integer"}},
                  "additionalProperties": False},
                 h_search)
    srv.add_tool("list_catalog",
                 "列出目录快照全部条目(page/database/all)。",
                 {"type": "object",
                  "properties": {"kind": {"type": "string", "enum": ["all", "page", "database"]},
                                 "limit": {"type": "integer"}},
                  "additionalProperties": False},
                 h_list)
    srv.add_tool("recent_audit",
                 "最近操作审计记录(主控层同步·append-only 尾)。",
                 {"type": "object",
                  "properties": {"limit": {"type": "integer"}},
                  "additionalProperties": False},
                 h_audit)
    srv.add_tool("topo_snapshot",
                 "龍魂拓扑快照摘要(主控侧推送·只读)。",
                 {"type": "object", "properties": {}, "additionalProperties": False},
                 h_topo)
    return srv


if __name__ == "__main__":
    from lh_mcp_core import run_from_cli
    run_from_cli(_make_server(), SERVER_NAME, DEFAULT_PORT, DEFAULT_CFG)
