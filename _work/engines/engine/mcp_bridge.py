#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 协议桥
DNA: #龍芯⚡️2026-04-19-MCP-BRIDGE-v1.0

把本地 MCP server 暴露成 HTTP 给 Chrome 扩展调用
MVP 阶段用占位·后续接官方 mcp-python-sdk
"""

# 占位工具清单（老大自己的本地工具箱子）
PLACEHOLDER_TOOLS = [
    {"name": "fs.read", "desc": "读本地文件", "args": {"path": "string"}},
    {"name": "fs.list", "desc": "列目录内容", "args": {"path": "string"}},
    {"name": "git.status", "desc": "查 git 状态", "args": {"repo": "string"}},
    {"name": "notion.search", "desc": "搜 Notion 库", "args": {"query": "string"}},
    {"name": "dna.sign", "desc": "用 keyring 签 L3 DNA", "args": {"text": "string"}},
]


async def list_tools():
    """列出可用工具"""
    return {
        "tools": PLACEHOLDER_TOOLS,
        "note": "MVP 占位·接入 mcp-python-sdk 后自动拉取真实 MCP server 的工具",
    }


async def call_tool(name: str, args: dict):
    """调用一个工具"""
    if name == "fs.read":
        from pathlib import Path
        p = Path(args.get("path", "")).expanduser()
        if not p.exists() or not p.is_file():
            return {"ok": False, "error": f"路径不存在或非文件: {p}"}
        try:
            content = p.read_text(encoding="utf-8", errors="replace")[:5000]
            return {"ok": True, "tool": name, "result": content}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    if name == "fs.list":
        from pathlib import Path
        p = Path(args.get("path", "~")).expanduser()
        if not p.exists() or not p.is_dir():
            return {"ok": False, "error": f"路径不存在或非目录: {p}"}
        items = [x.name for x in p.iterdir()][:100]
        return {"ok": True, "tool": name, "result": items}

    if name == "notion.search":
        from notion_sync import search_notion
        res = await search_notion(args.get("query", ""))
        return {"ok": True, "tool": name, "result": res}

    if name == "dna.sign":
        import hashlib
        from datetime import datetime
        text = args.get("text", "")
        h = hashlib.sha256(f"{text}|9622|{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return {
            "ok": True,
            "tool": name,
            "result": f"#龍芯⚡️{ts}-MCP-{h}",
        }

    return {
        "ok": False,
        "tool": name,
        "error": f"未知工具·可用: {[t['name'] for t in PLACEHOLDER_TOOLS]}",
    }
