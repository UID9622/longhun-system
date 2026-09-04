#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-READONLY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 鲲鹏 MCP Server · 只读层 lh-mcp-readonly v1.0（端口 8763）
================================================================
对外暴露龍魂系统的只读数据（图谱/铭碑/健康/命令），供 AI 应用安全调用。

MCP Resources:
  resource://topo/<图谱名>   图谱完整结构（空名 = 图谱清单）
  resource://topo/list       图谱清单（alias）
  resource://memorial/root   铭碑根哈希
  resource://health/status   系统健康状态

MCP Tools:
  get_topo(name)             获取指定图谱完整结构
  verify_memorial(root_hash) 校验铭碑根哈希
  list_commands()            列出可用 lh 命令
  get_health()               系统健康状态(JSON)
"""

import json
import platform
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_mcp_core import (  # noqa: E402
    MCPServer, MCPError, ERR_INVALID_PARAMS, now_iso, run_from_cli,
    find_topo_files, load_topo, read_memorial, topo_root_hash,
)

SERVER_NAME = "lh-mcp-readonly"
VERSION = "1.0.0"
DEFAULT_PORT = 8763

DEFAULT_CFG = {
    "server": SERVER_NAME,
    "port": DEFAULT_PORT,
    "host": "127.0.0.1",
    "auth": {"mode": "none"},
    "log_dir": "~/.longhun/logs/mcp",
    "lh_root": "",
    "peer_allowlist": [],
}

# 高频常用命令（供 AI 快速上手指南）
HIGH_FREQ_CMDS = [
    {"cmd": "lh health --json", "desc": "健康基线(图谱/模型/服务)"},
    {"cmd": "lh topo list", "desc": "图谱清单"},
    {"cmd": "lh topo verify <图谱>", "desc": "图谱一致性校验"},
    {"cmd": "lh model list", "desc": "模型注册表 + Ollama 实时"},
    {"cmd": "lh audit", "desc": "归一审计(三色)"},
    {"cmd": "lh judge view", "desc": "耻辱墙查看"},
    {"cmd": "lh search <kw>", "desc": "搜索引擎"},
    {"cmd": "lh te --stamp", "desc": "干支时间戳/卦象"},
    {"cmd": "lh brain search <kw>", "desc": "超级大脑记忆检索"},
    {"cmd": "lh mcp list", "desc": "鲲鹏 MCP Server 一览"},
    {"cmd": "python3 08_BIN/lh_memorial.py --root", "desc": "铭碑 Merkle 根"},
]

_SUB_RE = re.compile(
    r"'([\w-]+)':\s*\(\s*'([\w.]+\.py)',\s*'([^']*)',\s*'([^']*)'")


def _extract_sub_dispatch(root: Path) -> list:
    """静态解析 lh.py SUB_DISPATCH → [{cmd, engine, desc}]（不 import·零开销）"""
    f = root / "08_BIN" / "lh.py"
    if not f.exists():
        return []
    out = []
    try:
        text = f.read_text(encoding="utf-8")
    except Exception:
        return []
    for m in _SUB_RE.finditer(text):
        name, engine, emoji, desc = m.groups()
        if name.startswith("lh-") and name not in ("lh-kunpeng",):
            continue
        out.append({"cmd": f"lh {name}", "engine": engine,
                    "emoji": emoji, "desc": desc.strip()})
    # 去重保序
    seen, uniq = set(), []
    for c in out:
        if c["cmd"] not in seen:
            seen.add(c["cmd"])
            uniq.append(c)
    return uniq


# ── TTL 内存缓存（任务5.4：图谱/铭碑缓存到内存·30s 过期）──
_cache: dict = {}


def _ttl(key: str, ttl: float, loader):
    now = time.time()
    hit = _cache.get(key)
    if hit and now - hit[0] < ttl:
        return hit[1]
    val = loader()
    _cache[key] = (now, val)
    return val


def _load_topo_cached(name: str):
    return _ttl(f"topo:{name}", 30, lambda: _load_topo(name))


def _load_topo(name: str):
    root = _server_root()
    return load_topo(root, name)


def _server_root() -> Path:
    return Path(__file__).resolve().parents[2]  # longhun-system/


# ═══════════════════════════════════════════════════════════════
# 工具实现
# ═══════════════════════════════════════════════════════════════

def _tool_get_topo(args: dict) -> dict:
    """获取指定图谱的完整结构（name 留空 = 图谱清单）"""
    name = str(args.get("name") or "").strip()
    data = _load_topo_cached(name)
    if name == "" or isinstance(data, dict) and "graphs" in data:
        return data  # 清单
    # 完整图谱 → 摘要 + 树状节点（去掉超大字段）
    groups, subgraphs = data.get("groups", []), data.get("subgraphs", [])
    green = yellow = neutral = 0
    node_count = 0
    for g in groups:
        for a in g.get("assets", []):
            node_count += 1
            s = (a.get("status") or "").strip()
            if s.startswith("🟢"):
                green += 1
            elif s.startswith("🟡"):
                yellow += 1
            else:
                neutral += 1
    for sg in subgraphs:
        node_count += 1
        for a in sg.get("assets", []):
            node_count += 1
    return {
        "topo_name": data.get("topo_name") or data.get("display"),
        "display": data.get("display", ""),
        "last_sync": data.get("last_sync", "?"),
        "root_hash": topo_root_hash(data),
        "stats": {"nodes": node_count, "green": green,
                  "yellow": yellow, "neutral": neutral},
        "groups": [{"name": g.get("name", ""),
                    "assets": [{"name": a.get("name"), "dna": a.get("dna"),
                                "status": (a.get("status") or "").strip(),
                                "link": a.get("link", "")}
                               for a in g.get("assets", [])]}
                   for g in groups],
        "subgraphs": [{"name": sg.get("name", ""), "dna": sg.get("dna"),
                       "status": (sg.get("status") or "").strip(),
                       "meta": sg.get("subgraph_meta")}
                      for sg in subgraphs],
    }


def _tool_verify_memorial(args: dict) -> dict:
    """验证铭碑根哈希：传 root_hash 则与当前铭碑比对"""
    want = str(args.get("root_hash") or "").strip().upper()
    m = read_memorial(_server_root())
    current = (m.get("root_hash") or "").strip().upper()
    if not current:
        return {"ok": False, "reason": m.get("reason", "铭碑未构建"),
                "current_root": None}
    if want:
        match = want == current
        return {"ok": match, "match": match, "expected": want,
                "current_root": current,
                "summary": ("🟢 铭碑根哈希一致" if match else
                            "🔴 铭碑根哈希不一致（可能被改动）")}
    return {"ok": True, "current_root": current,
            "contributors": m.get("contributors"),
            "updated": m.get("updated")}


def _tool_list_commands(args: dict) -> dict:
    """列出所有可用 lh 命令（SUB_DISPATCH 静态解析 + 高频速查）"""
    root = _server_root()
    subs = _extract_sub_dispatch(root)
    return {"total": len(subs) + len(HIGH_FREQ_CMDS),
            "high_frequency": HIGH_FREQ_CMDS,
            "commands": subs}


def _tool_get_health(args: dict) -> dict:
    """系统健康状态 JSON"""
    root = _server_root()
    topo_files = find_topo_files(root)
    main_topo = {}
    try:
        main_topo = load_topo(root, "通心译")
        if "graphs" not in main_topo:
            main_topo = {"root_hash": topo_root_hash(main_topo),
                         "nodes": sum(len(g.get("assets", [])) for g in
                                      main_topo.get("groups", []))}
    except Exception:
        pass
    mem = read_memorial(root)
    neural = root / ".codebuddy" / "longhun_neural_net.json"
    return {
        "ok": True,
        "server": SERVER_NAME,
        "version": VERSION,
        "uid": "UID9622",
        "attribution": "诸葛鑫 | UID9622 · 龍芯北辰",
        "python": platform.python_version(),
        "lh_root": str(root),
        "lh_root_ready": root.is_dir(),
        "topo": {"graphs": len(topo_files),
                 "main": main_topo if "root_hash" in main_topo else {}},
        "memorial": {"loaded": mem.get("loaded"),
                     "root_hash": mem.get("root_hash")},
        "neural_net": {"exists": neural.exists()},
        "ts": now_iso(),
        "audit": "🟢",
    }


# ═══════════════════════════════════════════════════════════════
# 资源实现
# ═══════════════════════════════════════════════════════════════

def _res_topo(uri: str) -> dict:
    name = uri[len("resource://topo/"):]
    if name in ("", "list"):
        return load_topo(_server_root(), "")
    return _load_topo_cached(name)


def _res_memorial(uri: str) -> dict:
    return read_memorial(_server_root())


def _res_health(uri: str) -> dict:
    return _tool_get_health({})


def build_server() -> MCPServer:
    srv = MCPServer(SERVER_NAME, VERSION, DEFAULT_CFG)
    # 工具（全部只读·无 confirm）
    srv.add_tool("get_topo",
                 "获取指定龍魂知识图谱的完整结构；name 留空返回全部图谱清单（通心译/深度学习等）",
                 {"type": "object",
                  "properties": {"name": {"type": "string",
                                          "description": "图谱名/关键词，如 通心译、深度学习；留空=清单"}}},
                 _tool_get_topo)
    srv.add_tool("verify_memorial",
                 "验证贡献者铭碑 Merkle 根哈希；传 root_hash 则与当前铭碑比对是否被篡改",
                 {"type": "object",
                  "properties": {"root_hash": {"type": "string",
                                               "description": "期望根哈希(可选)；留空返回当前根"}}},
                 _tool_verify_memorial)
    srv.add_tool("list_commands",
                 "列出所有可用的 lh 命令（高频速查 + SUB_DISPATCH 全表）",
                 {"type": "object", "properties": {}}, _tool_list_commands)
    srv.add_tool("get_health",
                 "获取龍魂系统健康状态（图谱/铭碑/根路径/Python 版本）",
                 {"type": "object", "properties": {}}, _tool_get_health)
    # 资源
    srv.add_resource("resource://topo/*", "龍魂图谱",
                     "指定图谱完整结构；尾部为图谱名（通心译/深度学习…），空=清单",
                     _res_topo)
    srv.add_resource("resource://memorial/root", "贡献者铭碑根",
                     "铭碑 Merkle 根哈希与状态", _res_memorial)
    srv.add_resource("resource://health/status", "系统健康状态",
                     "只读健康 JSON", _res_health)
    return srv


if __name__ == "__main__":
    sys.exit(run_from_cli(build_server(), SERVER_NAME, DEFAULT_PORT, DEFAULT_CFG))
