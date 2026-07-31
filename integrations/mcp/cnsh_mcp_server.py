# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
╔══════════════════════════════════════════════════════════════════════╗
║            CNSH 核心 MCP Server v2.0 — CNSH 块写入/查询/审计           ║
║  DNA: #龍芯⚡️2026-07-13-CNSH-CORE-MCP-v2.0                         ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
CNSH 核心块管理 MCP Server — 操作 CNSH 数据块的标准接口。
三 AI 流程：写 → 分级审计 → 链式溯源。

【本 MCP Server 提供什么？】
13 个工具，覆盖 CNSH 块全生命周期：
  📝 cnsh_write        — 写入 CNSH 块（三 AI 流程）
  🔍 cnsh_query        — 查询 CNSH 块
  🛡️ cnsh_audit        — 分级审计
  🧬 cnsh_dna_generate  — 生成 DNA 追溯码
  ✅ cnsh_dna_validate  — 校验 DNA
  🛑 cnsh_redline_check — 红线熔断检查
  📋 cnsh_redline_list  — 红线清单
  🔢 cnsh_digital_root  — 数字根+五行
  📊 cnsh_block_stats   — 块统计
  🔗 cnsh_block_chain   — 查看块链
  🔄 cnsh_sync_state    — 同步状态
  📡 cnsh_event_watch   — 事件监听
  ❤️ cnsh_health        — 健康检查

【版本历史】
v1.0 (2026-06-21): 初始版本，4 工具
v2.0 (2026-07-13): 扩展至 13 工具，集成 DNA/红线/数字根
"""

import asyncio
import json
import os
import sys
import time
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Optional

# ── 路径初始化 ──
try:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
except Exception:
    _PROJECT_ROOT = Path(os.environ.get("LONGHUN_ROOT", os.path.expanduser("~/longhun-system")))

_CNSH_MODULE_PATHS = [
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1" / "cnsh_v21",
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1",
    _PROJECT_ROOT / "cnsh-core",
    _PROJECT_ROOT / "cnsh",
    _PROJECT_ROOT,
]
for _p in _CNSH_MODULE_PATHS:
    _sp = str(_p)
    if _sp not in sys.path and _p.exists():
        sys.path.insert(0, _sp)

# ── 核心模块导入 ──
try:
    from cnsh_unified import DNA工具, 数学工具, 审计工具
    _CNSH_UNIFIED = True
except ImportError:
    _CNSH_UNIFIED = False

try:
    from cnsh_redlines import 红线熔断器, 红线本源
    _CNSH_REDLINES = True
except ImportError:
    _CNSH_REDLINES = False

# ── MCP SDK 或裸 JSON-RPC ──
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    _MCP_SDK = True
except ImportError:
    _MCP_SDK = False

# ── API 代理模式 ──
CNSH_API = os.getenv("CNSH_API_URL", "http://localhost:9000")
try:
    import httpx
    _HTTPX = True
except ImportError:
    _HTTPX = False

# ── 服务器实例 ──
if _MCP_SDK:
    app = Server("cnsh-core")
else:
    app = None

# ══════════════════════════════════════════════════════════════════
# DNA 工具函数
# ══════════════════════════════════════════════════════════════════

def _gen_dna(module: str = "CNSH-CORE-MCP", action: str = "TOOL") -> str:
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{ts}-{module}-{action}-UID9622".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-{module}-v2.0-{h}"


def _calc_digital_root(text: str) -> dict[str, Any]:
    """计算数字根+五行+闸门"""
    digits = re.sub(r"[^0-9]", "", text)
    if not digits:
        return {"digital_root": 0, "wuxing": "无极", "gate": "⚪", "note": "无数字内容"}
    n = int(digits)
    while n > 9:
        n = sum(int(d) for d in str(n))
    wuxing_map = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
    gate_map = {3: "🟢 369不动点", 6: "🟢 369不动点", 9: "🟢 369不动点", 0: "⚪ 无极"}
    return {
        "digital_root": n,
        "wuxing": wuxing_map.get(n, "未知"),
        "gate": gate_map.get(n, "🟡"),
        "note": "369不动点·洛书九宫" if n in (3, 6, 9) else ("零位·无极" if n == 0 else ""),
    }


def _simple_redline_check(text: str) -> dict[str, Any]:
    """简易红线检测（不依赖外部模块）"""
    redlines = {
        "P0": ["技术无国界", "数据无国界", "隐私不重要", "生态锁定", "用户数据收割",
               "暗网", "数据奴隶", "AI取代人类", "信息殖民", "数字殖民", "数字霸权"],
        "P1": ["自由市场万能", "监管无用论", "算法中立", "技术中立", "去中心化万能",
               "市场自我调节", "看不见的手", "绝对自由"],
        "P2": ["流量为王", "增长黑客", "用户粘性", "沉没成本", "路径依赖",
               "羊群效应", "信息茧房", "算法推荐至上"],
        "P3": ["加班文化", "996", "狼性文化", "内卷", "躺平", "资本为王",
               "消费主义", "奶头乐", "娱乐至死"],
    }
    hits = []
    for level, words in redlines.items():
        for w in words:
            if w in text:
                hits.append({"level": level, "word": w})
    return {
        "triggered": len(hits) > 0,
        "hits": hits,
        "highest_level": hits[0]["level"] if hits else None,
        "dna": _gen_dna("CNSH-CORE-MCP", "REDLINE"),
    }


# ══════════════════════════════════════════════════════════════════
# 工具处理器
# ══════════════════════════════════════════════════════════════════

async def _api_write(args: dict[str, Any]) -> dict[str, Any]:
    """通过 HTTP API 写入 CNSH 块"""
    if not _HTTPX:
        return {"ok": False, "error": "httpx 不可用", "dna": _gen_dna("CNSH-CORE-MCP", "WRITE-ERROR")}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{CNSH_API}/cnsh/write_block", json={
                "input": args["input"],
                "source_ai": args.get("source_ai", "GPT"),
                "user_id": "UID9622",
                "blocks": args.get("blocks", []),
                "tags": args.get("tags", []),
                "dna": _gen_dna("CNSH-CORE-MCP", "WRITE"),
            })
            data = r.json()
            data["dna"] = _gen_dna("CNSH-CORE-MCP", "WRITE")
            return data
    except Exception as e:
        return {"ok": False, "error": f"API 写入失败: {e}", "dna": _gen_dna("CNSH-CORE-MCP", "WRITE-ERROR")}


async def _api_query(args: dict[str, Any]) -> dict[str, Any]:
    if not _HTTPX:
        return {"ok": False, "error": "httpx 不可用"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            params = {k: v for k, v in args.items() if v and k not in ("dna_format",)}
            r = await client.get(f"{CNSH_API}/cnsh/query", params=params)
            return {"ok": True, "dna": _gen_dna("CNSH-CORE-MCP", "QUERY"), **r.json()}
    except Exception as e:
        return {"ok": False, "error": f"API 查询失败: {e}", "dna": _gen_dna("CNSH-CORE-MCP", "QUERY-ERROR")}


async def _api_audit(args: dict[str, Any]) -> dict[str, Any]:
    if not _HTTPX:
        return {"ok": False, "error": "httpx 不可用"}
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{CNSH_API}/cnsh/audit", json={
                "block_id": args["block_id"],
                "audit_depth": args.get("depth", "standard"),
            })
            return {"ok": True, "dna": _gen_dna("CNSH-CORE-MCP", "AUDIT"), **r.json()}
    except Exception as e:
        return {"ok": False, "error": f"API 审计失败: {e}", "dna": _gen_dna("CNSH-CORE-MCP", "AUDIT-ERROR")}


async def _block_stats(args: dict[str, Any]) -> dict[str, Any]:
    if not _HTTPX:
        return {"ok": False, "error": "httpx 不可用"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{CNSH_API}/cnsh/stats")
            return {"ok": True, "dna": _gen_dna("CNSH-CORE-MCP", "STATS"), **r.json()}
    except Exception:
        return {"ok": True, "dna": _gen_dna("CNSH-CORE-MCP", "STATS"),
                "stats": {"note": "API 后端未连接，统计数据不可用"},
                "api_status": "offline"}


async def _block_chain(args: dict[str, Any]) -> dict[str, Any]:
    if not _HTTPX:
        return {"ok": False, "error": "httpx 不可用"}
    block_id = args.get("block_id", "")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{CNSH_API}/cnsh/chain/{block_id}" if block_id else f"{CNSH_API}/cnsh/chain")
            return {"ok": True, "dna": _gen_dna("CNSH-CORE-MCP", "CHAIN"), **r.json()}
    except Exception as e:
        return {"ok": False, "error": f"API 链查询失败: {e}", "dna": _gen_dna("CNSH-CORE-MCP", "CHAIN-ERROR")}


async def _sync_state(args: dict[str, Any]) -> dict[str, Any]:
    """获取同步状态"""
    try:
        sync_log = _PROJECT_ROOT / "logs" / "sync_state.json"
        if sync_log.exists():
            with open(sync_log) as f:
                state = json.load(f)
            return {"ok": True, "state": state, "dna": _gen_dna("CNSH-CORE-MCP", "SYNC")}
    except Exception:
        pass
    return {"ok": True, "state": {"status": "unknown", "note": "同步状态文件不存在"},
            "dna": _gen_dna("CNSH-CORE-MCP", "SYNC")}


async def _event_watch(args: dict[str, Any]) -> dict[str, Any]:
    """查看最近事件"""
    prefix = args.get("prefix", "")
    limit = int(args.get("limit", 20))
    events = []
    log_file = _PROJECT_ROOT / "logs" / "action_log.jsonl"
    try:
        if log_file.exists():
            lines = log_file.read_text().strip().split("\n")[-limit:]
            for line in lines:
                try:
                    evt = json.loads(line)
                    if not prefix or str(evt).startswith(prefix):
                        events.append(evt)
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    return {"ok": True, "events": events[-limit:], "count": len(events), "dna": _gen_dna("CNSH-CORE-MCP", "EVENTS")}


async def _handle_health(args: dict[str, Any]) -> dict[str, Any]:
    """综合健康检查"""
    modules = {
        "CNSH统一API": _CNSH_UNIFIED,
        "红线引擎": _CNSH_REDLINES,
        "MCP SDK": _MCP_SDK,
        "HTTP客户端": _HTTPX,
    }
    api_up = False
    if _HTTPX:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f"{CNSH_API}/cnsh/health")
                api_up = r.status_code == 200
        except Exception:
            pass

    return {
        "ok": True,
        "server": "cnsh-core",
        "version": "2.0.0",
        "identity_dna": "#龍芯⚡️2026-07-13-CNSH-CORE-MCP-v2.0",
        "modules": modules,
        "api_backend": "up" if api_up else "down",
        "api_url": CNSH_API,
        "project_root": str(_PROJECT_ROOT),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dna": _gen_dna("CNSH-CORE-MCP", "HEALTH"),
    }


def _handle_dna_gen(args: dict[str, Any]) -> dict[str, Any]:
    module = str(args.get("module", "CNSH"))
    version = str(args.get("version", "1.0"))
    if _CNSH_UNIFIED:
        dna = DNA工具.生成(module, version)
        return {"ok": True, "dna": dna, "module": module, "version": version}
    return {"ok": True, "dna": _gen_dna(module, "GEN"), "module": module, "version": version}


def _handle_dna_validate(args: dict[str, Any]) -> dict[str, Any]:
    dna = str(args.get("dna", ""))
    valid = "龍" in dna and ("⚡️" in dna or "⚡" in dna) and len(dna) > 10
    return {
        "ok": True,
        "dna": dna,
        "valid": valid,
        "checks": {
            "has_dragon": "龍" in dna,
            "has_lightning": "⚡️" in dna or "⚡" in dna,
            "min_length": len(dna) > 10,
            "standard_prefix": dna.startswith("#龍芯⚡️") or dna.startswith("#龙芯⚡️"),
        }
    }


def _handle_digital_root(args: dict[str, Any]) -> dict[str, Any]:
    content = str(args.get("content", str(args)))
    result = _calc_digital_root(content)
    if _CNSH_UNIFIED and _calc_digital_root(content)["digital_root"] > 0:
        try:
            dr = _calc_digital_root(content)["digital_root"]
            result["wuxing_system"] = 数学工具.数字根转五行(dr) if hasattr(数学工具, '数字根转五行') else result["wuxing"]
            result["gate_system"] = 数学工具.数字根闸门(dr) if hasattr(数学工具, '数字根闸门') else result["gate"]
        except Exception:
            pass
    return {"ok": True, "content_sample": content[:100], "dna": _gen_dna("CNSH-CORE-MCP", "DIGITAL-ROOT"), **result}


def _handle_redline(args: dict[str, Any]) -> dict[str, Any]:
    text = str(args.get("text", ""))
    if _CNSH_REDLINES:
        try:
            fusing = 红线熔断器()
            result = fusing.熔断检查(text)
            return {
                "ok": True,
                "triggered": result["触发"],
                "highest_level": result["最高级别"],
                "hits": result["命中"],
                "report": fusing.报告(result) if result["触发"] else "🟢 红线扫描通过",
                "dna": result.get("DNA", _gen_dna("CNSH-CORE-MCP", "REDLINE")),
            }
        except Exception as e:
            pass
    result = _simple_redline_check(text)
    return {"ok": True, **result, "engine": "builtin-simple"}


def _handle_redline_list(args: dict[str, Any]) -> dict[str, Any]:
    level = str(args.get("level", "all"))
    if _CNSH_REDLINES:
        try:
            level_map = {"P0": "P0_伦理红线", "P1": "P1_锁定红线", "P2": "P2_收割红线", "P3": "P3_复杂红线"}
            items = []
            for name, info in 红线本源.items():
                lv = info["级别"]
                if level != "all" and lv != level_map.get(level, ""):
                    continue
                items.append({"name": name, "level": lv, "root_concept": info.get("根概念", ""),
                              "definition": info.get("定义", ""), "source_dna": info.get("来源DNA", ""),
                              "aliases": info.get("语义等价", [])})
            return {"ok": True, "level_filter": level, "count": len(items), "redlines": items,
                    "dna": _gen_dna("CNSH-CORE-MCP", "REDLINE-LIST")}
        except Exception:
            pass
    return {"ok": True, "level_filter": level, "note": "红线引擎未加载，使用内置简单检测",
            "dna": _gen_dna("CNSH-CORE-MCP", "REDLINE-LIST-BASIC")}


# ══════════════════════════════════════════════════════════════════
# 统一调度
# ══════════════════════════════════════════════════════════════════

TOOL_HANDLERS = {
    "cnsh_write": {"handler": _api_write, "is_async": True},
    "cnsh_query": {"handler": _api_query, "is_async": True},
    "cnsh_audit": {"handler": _api_audit, "is_async": True},
    "cnsh_dna_generate": {"handler": _handle_dna_gen, "is_async": False},
    "cnsh_dna_validate": {"handler": _handle_dna_validate, "is_async": False},
    "cnsh_redline_check": {"handler": _handle_redline, "is_async": False},
    "cnsh_redline_list": {"handler": _handle_redline_list, "is_async": False},
    "cnsh_digital_root": {"handler": _handle_digital_root, "is_async": False},
    "cnsh_block_stats": {"handler": _block_stats, "is_async": True},
    "cnsh_block_chain": {"handler": _block_chain, "is_async": True},
    "cnsh_sync_state": {"handler": _sync_state, "is_async": True},
    "cnsh_event_watch": {"handler": _event_watch, "is_async": True},
    "cnsh_health": {"handler": _handle_health, "is_async": True},
}

TOOL_DEFINITIONS = [
    Tool(
        name="cnsh_write",
        description="写入 CNSH 块（三 AI 流程）。输入文本+来源AI，经过三级验证后写入 CNSH 块链。",
        inputSchema={
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "要写入的文本内容"},
                "source_ai": {"type": "string", "enum": ["GPT", "Claude", "Grok", "Gemini", "DeepSeek", "Human"],
                              "description": "来源 AI 模型"},
                "blocks": {"type": "array", "description": "关联的块 ID 列表"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表"},
            },
            "required": ["input"],
        },
    ),
    Tool(
        name="cnsh_query",
        description="查询 CNSH 块。支持按 DNA、状态、标签、时间范围查询。",
        inputSchema={
            "type": "object",
            "properties": {
                "dna": {"type": "string", "description": "DNA 追溯码精确匹配"},
                "state": {"type": "string", "description": "块状态过滤"},
                "tag": {"type": "string", "description": "标签过滤"},
                "limit": {"type": "number", "description": "返回条数限制，默认 20"},
                "offset": {"type": "number", "description": "偏移量"},
            },
        },
    ),
    Tool(
        name="cnsh_audit",
        description="对 CNSH 块执行分级审计（basic/standard/deep）。返回审计结果和链式溯源路径。",
        inputSchema={
            "type": "object",
            "properties": {
                "block_id": {"type": "string", "description": "块 ID"},
                "depth": {"type": "string", "enum": ["basic", "standard", "deep"],
                          "description": "审计深度，默认 standard"},
            },
            "required": ["block_id"],
        },
    ),
    Tool(
        name="cnsh_dna_generate",
        description="生成龍魂标准 DNA 追溯码。格式：#龍芯⚡️日期-模块-版本-哈希8位",
        inputSchema={
            "type": "object",
            "properties": {
                "module": {"type": "string", "description": "模块名"},
                "version": {"type": "string", "description": "版本号"},
            },
            "required": ["module"],
        },
    ),
    Tool(
        name="cnsh_dna_validate",
        description="校验 DNA 追溯码格式合法性。检查前缀、闪电符号、长度。",
        inputSchema={
            "type": "object",
            "properties": {
                "dna": {"type": "string", "description": "要校验的 DNA 码"},
            },
            "required": ["dna"],
        },
    ),
    Tool(
        name="cnsh_redline_check",
        description="对文本执行红线词组熔断检查（P0-P3）。检测是否违反人民数据主权。",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要检查的文本"},
                "context": {"type": "string", "description": "可选的上下文"},
            },
            "required": ["text"],
        },
    ),
    Tool(
        name="cnsh_redline_list",
        description="列出所有已注册的红线词组，按 P0→P3 分级展示。",
        inputSchema={
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["P0", "P1", "P2", "P3", "all"],
                          "description": "按级别筛选，默认 all"},
            },
        },
    ),
    Tool(
        name="cnsh_digital_root",
        description="计算内容的数字根（digital root），返回五行属性和三色闸门。",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "要计算的内容"},
            },
            "required": ["content"],
        },
    ),
    Tool(
        name="cnsh_block_stats",
        description="CNSH 块系统统计：总块数、状态分布、类型分布。",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="cnsh_block_chain",
        description="查看块的完整溯源链。追踪一个块的前驱和后继。",
        inputSchema={
            "type": "object",
            "properties": {
                "block_id": {"type": "string", "description": "块 ID（不填则看全部链）"},
            },
        },
    ),
    Tool(
        name="cnsh_sync_state",
        description="查看 CNSH 系统的同步状态（本地↔云端）。",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="cnsh_event_watch",
        description="查看最近的系统事件日志。支持按前缀过滤。",
        inputSchema={
            "type": "object",
            "properties": {
                "prefix": {"type": "string", "description": "事件前缀过滤"},
                "limit": {"type": "integer", "description": "最多返回条数，默认 20"},
            },
        },
    ),
    Tool(
        name="cnsh_health",
        description="CNSH 核心 MCP Server 综合健康检查：模块可用性、API 连接、版本信息。",
        inputSchema={"type": "object", "properties": {}},
    ),
]


# ══════════════════════════════════════════════════════════════════
# MCP SDK 模式
# ══════════════════════════════════════════════════════════════════

if _MCP_SDK:
    @app.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOL_DEFINITIONS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:
        try:
            info = TOOL_HANDLERS.get(name)
            if not info:
                return [TextContent(type="text", text=json.dumps(
                    {"ok": False, "error": f"未知工具: {name}"}, ensure_ascii=False, indent=2))]
            if info["is_async"]:
                result = await info["handler"](arguments)
            else:
                result = info["handler"](arguments)
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({
                "ok": False, "error": str(e), "error_type": type(e).__name__,
                "dna": _gen_dna("CNSH-CORE-MCP", "ERROR"),
            }, ensure_ascii=False, indent=2))]

    async def main_sdk():
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())


# ══════════════════════════════════════════════════════════════════
# 裸 JSON-RPC 模式（无 MCP SDK 时的回退）
# ══════════════════════════════════════════════════════════════════

def _jsonrpc_main():
    """纯 JSON-RPC 2.0 over stdin/stdout"""
    import asyncio as _asyncio

    def _log(msg: str):
        print(f"[cnsh-core-mcp] {msg}", file=sys.stderr, flush=True)

    def _send(data: dict[str, Any]):
        sys.stdout.write(json.dumps(data, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def _handle(msg: dict[str, Any]) -> Optional[dict[str, Any]]:
        msg_id = msg.get("id")
        method = msg.get("method")

        if method == "initialize":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "cnsh-core", "version": "2.0.0"},
            }}

        if method == "notifications/initialized":
            return None

        if method == "tools/list":
            tools = [{"name": t.name, "description": t.description, "inputSchema": t.inputSchema}
                     for t in TOOL_DEFINITIONS]
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}}

        if method == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if tool_name not in TOOL_HANDLERS:
                return {"jsonrpc": "2.0", "id": msg_id,
                        "error": {"code": -32601, "message": f"未知工具: {tool_name}"}}

            try:
                info = TOOL_HANDLERS[tool_name]
                if info["is_async"]:
                    result = _asyncio.run(info["handler"](arguments))
                else:
                    result = info["handler"](arguments)
                return {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                }}
            except Exception as e:
                return {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "content": [{"type": "text", "text": f"错误: {e}"}], "isError": True,
                }}

        if method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        return {"jsonrpc": "2.0", "id": msg_id,
                "error": {"code": -32601, "message": f"未知方法: {method}"}}

    _log(f"🐉 CNSH 核心 MCP Server v2.0 启动 (JSON-RPC 模式)")
    _log(f"   项目根: {_PROJECT_ROOT}")
    _log(f"   工具数: {len(TOOL_HANDLERS)}")
    _log(f"   API: {CNSH_API}")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = _handle(msg)
        if response is not None:
            _send(response)


# ══════════════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if _MCP_SDK:
        asyncio.run(main_sdk())
    else:
        try:
            _jsonrpc_main()
        except KeyboardInterrupt:
            sys.exit(0)
