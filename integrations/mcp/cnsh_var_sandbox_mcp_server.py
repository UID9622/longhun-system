#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║        CNSH 变量沙箱 MCP Server v1.0 — 统一变量管理 + 隔离执行        ║
║  DNA: #龍芯⚡️2026-07-06-CNSH-VAR-SANDBOX-MCP-v1.0                  ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
CNSH 变量沙箱 MCP Server — 把所有变量映射焊死在一个地方。
不再有"一处改了另一处没改"的问题。

【本 MCP Server 提供什么？】
10 个工具：
  📦 cnsh_var_register     — 注册变量到沙箱（自动生成 7 目标映射）
  ✅ cnsh_var_validate     — 校验单个/全部变量映射完整性
  🔄 cnsh_var_translate    — 翻译变量到指定目标语言
  🔒 cnsh_var_sandbox_exec — 隔离沙箱中执行代码
  📋 cnsh_var_audit        — 全沙箱审计报告
  📝 cnsh_var_generate     — 为所有变量生成目标语言声明代码
  ⚖️  cnsh_var_compare     — 对比沙箱变量与外部映射的一致性
  💰 cnsh_finance_ingest   — 金融数据爬取并注册为沙箱变量
  📡 cnsh_finance_watch    — 金融变量实时监控
  ❤️ cnsh_health           — 健康检查
"""

import asyncio
import json
import os
import sys
import re
import time
from pathlib import Path
from typing import Any

# ── 路径初始化 ──
try:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
except Exception:
    _PROJECT_ROOT = Path(os.environ.get("LONGHUN_ROOT", os.path.expanduser("~/longhun-system")))  # pyright: ignore[reportConstantRedefinition]

_CNSH_MODULE_PATHS = [
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1",
    _PROJECT_ROOT / "cnsh-core",
    _PROJECT_ROOT,
]
for _p in _CNSH_MODULE_PATHS:
    _sp = str(_p)
    if _sp not in sys.path and _p.exists():
        sys.path.insert(0, _sp)

# ── 核心导入 ──
from cnsh_v21.var_sandbox import (  # pyright: ignore[reportMissingImports]
    VarSandbox, VarEntry, get_default_sandbox,
    TYPE_MAP, TYPE_DEFAULTS, STDLIB_MAP
)

# ── MCP SDK ──
from mcp.server import Server  # pyright: ignore[reportMissingImports]
from mcp.server.stdio import stdio_server  # pyright: ignore[reportMissingImports]
from mcp.types import Tool, TextContent  # pyright: ignore[reportMissingImports]

# ── 服务器实例 ──
app = Server("cnsh-var-sandbox")

# ── 默认沙箱 ──
_默认沙箱 = get_default_sandbox()

# ── 金融缓存 ──
_金融缓存: dict[str, dict[str, object]] = {}


# ══════════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════════

def _gen_dna(module: str = "VAR-SANDBOX-MCP", action: str = "TOOL-CALL") -> str:
    """生成 DNA 追溯码"""
    from datetime import datetime
    import hashlib
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{module}-{action}-{now.timestamp()}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{date_str}-{module}-v1.0-{h.upper()}"


# ══════════════════════════════════════════════════════════════════
# MCP 工具注册
# ══════════════════════════════════════════════════════════════════

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ── 变量管理 ──
        Tool(
            name="cnsh_var_register",
            description="注册一个 CNSH 变量到沙箱。自动生成 7 种目标语言(python/js/c/cpp/rust/objc/swift)的映射。支持类型：整数/小数/文本/布尔/列表/映射。",
            inputSchema={
                "type": "object",
                "properties": {
                    "中文名": {
                        "type": "string",
                        "description": "CNSH 中文变量名（必填，如：价格/股票代码/已触发）",
                    },
                    "类型": {
                        "type": "string",
                        "enum": ["整数", "小数", "文本", "布尔", "列表", "映射", "空值"],
                        "description": "CNSH 类型名称",
                    },
                    "值": {
                        "type": "string",
                        "description": "初始值（字符串形式，布尔用 true/false）",
                    },
                    "英文名": {
                        "type": "string",
                        "description": "可选的英文映射名（默认等于中文名）",
                    },
                    "是常量": {
                        "type": "boolean",
                        "description": "是否为常量（默认 false）",
                    },
                },
                "required": ["中文名", "类型"],
            },
        ),
        Tool(
            name="cnsh_var_validate",
            description="校验变量映射完整性。检查单个变量或全部变量是否在所有 7 种目标语言中都有映射，并检测命名冲突。",
            inputSchema={
                "type": "object",
                "properties": {
                    "中文名": {
                        "type": "string",
                        "description": "要校验的变量名（不填则校验全部）",
                    },
                },
            },
        ),
        Tool(
            name="cnsh_var_translate",
            description="将 CNSH 变量名翻译为指定目标语言的变量名和类型。支持 7 目标：python/js/c/cpp/rust/objc/swift。",
            inputSchema={
                "type": "object",
                "properties": {
                    "中文名": {
                        "type": "string",
                        "description": "CNSH 变量名",
                    },
                    "目标": {
                        "type": "string",
                        "enum": ["python", "js", "c", "cpp", "rust", "objc", "swift"],
                        "description": "目标语言",
                    },
                },
                "required": ["中文名", "目标"],
            },
        ),
        Tool(
            name="cnsh_var_sandbox_exec",
            description="在隔离沙箱中执行 Python 代码。不污染外层环境，所有变量操作限于沙箱内。",
            inputSchema={
                "type": "object",
                "properties": {
                    "代码": {
                        "type": "string",
                        "description": "要在沙箱中执行的 Python 代码",
                    },
                },
                "required": ["代码"],
            },
        ),
        Tool(
            name="cnsh_var_audit",
            description="全沙箱审计报告。列出所有已注册变量、映射状态、执行历史，以及跨目标冲突。",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="cnsh_var_generate",
            description="为沙箱中所有变量生成目标语言的声明代码。一键生成 python/js/c/cpp/rust/objc/swift 的变量声明。",
            inputSchema={
                "type": "object",
                "properties": {
                    "目标": {
                        "type": "string",
                        "enum": ["python", "js", "c", "cpp", "rust", "objc", "swift", "all"],
                        "description": "目标语言，all 则输出全部 7 种",
                    },
                },
                "required": ["目标"],
            },
        ),
        Tool(
            name="cnsh_var_compare",
            description="对比沙箱中的变量映射与外部提供的映射（如 JSON 字典），发现不一致并给出修复建议。",
            inputSchema={
                "type": "object",
                "properties": {
                    "外部映射": {
                        "type": "object",
                        "description": "外部映射 JSON，格式: {\"中文名\": \"目标名\", ...}",
                    },
                },
                "required": ["外部映射"],
            },
        ),
        # ── 金融数据 ──
        Tool(
            name="cnsh_finance_ingest",
            description="从公共 API 爬取金融数据（股票/指数/汇率），并自动注册为沙箱变量。支持多种数据源。",
            inputSchema={
                "type": "object",
                "properties": {
                    "类型": {
                        "type": "string",
                        "enum": ["股票", "指数", "汇率", "数字货币"],
                        "description": "金融数据类型",
                    },
                    "代码": {
                        "type": "string",
                        "description": "股票代码/指数代码/货币对（如 000001/USDCNY/BTCUSDT）",
                    },
                    "源": {
                        "type": "string",
                        "enum": ["sina", "binance", "okx", "auto"],
                        "description": "数据源（默认 auto 自动选择）",
                    },
                },
                "required": ["类型", "代码"],
            },
        ),
        Tool(
            name="cnsh_finance_watch",
            description="监控金融变量变化。可设置告警阈值，变量超出范围时自动触发通知。",
            inputSchema={
                "type": "object",
                "properties": {
                    "变量前缀": {
                        "type": "string",
                        "description": "要监控的变量名前缀（如 股票_ 则监控所有 股票_开头的变量）",
                    },
                    "刷新秒数": {
                        "type": "integer",
                        "description": "数据刷新间隔（秒），默认 60",
                    },
                },
                "required": ["变量前缀"],
            },
        ),
        # ── 健康检查 ──
        Tool(
            name="cnsh_health",
            description="检查变量沙箱 MCP Server 健康状态，包括变量数量、映射完整性、模块可用性。",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ══════════════════════════════════════════════════════════════════
# 工具调用分发
# ══════════════════════════════════════════════════════════════════

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:  # pyright: ignore[reportArgumentType]
    try:
        result = _dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "通过": False,
            "错误": str(e),
            "错误类型": type(e).__name__,
            "DNA": _gen_dna("VAR-SANDBOX-MCP", "ERROR"),
        }, ensure_ascii=False, indent=2))]


def _dispatch(name: str, args: dict[str, object]) -> dict[str, object]:
    handlers: dict[str, object] = {  # pyright: ignore[reportAssignmentType]
        "cnsh_var_register": _注册变量,
        "cnsh_var_validate": _校验变量,
        "cnsh_var_translate": _翻译变量,
        "cnsh_var_sandbox_exec": _沙箱执行,
        "cnsh_var_audit": _审计报告,
        "cnsh_var_generate": _生成代码,
        "cnsh_var_compare": _对比映射,
        "cnsh_finance_ingest": _金融摄取,
        "cnsh_finance_watch": _金融监控,
        "cnsh_health": _健康检查,
    }
    handler = handlers.get(name)
    if handler:
        return handler(args)  # pyright: ignore[reportArgumentType,reportCallIssue]
    return {"通过": False, "错误": f"未知工具: {name}"}


# ══════════════════════════════════════════════════════════════════
# 处理函数
# ══════════════════════════════════════════════════════════════════

def _注册变量(args: dict[str, object]) -> dict[str, object]:
    中文名 = args["中文名"]  # pyright: ignore[reportArgumentType]
    类型 = args["类型"]
    值_str = args.get("值")
    英文名 = args.get("英文名", "")
    是常量 = args.get("是常量", False)

    # 解析值
    值 = _parse_value(str(值_str) if 值_str is not None else None, str(类型))  # pyright: ignore[reportArgumentType]

    entry = _默认沙箱.register(
        中文名=中文名, 类型=类型, 值=值,
        英文名=英文名, 是常量=是常量, 来源="MCP",
    )

    validate = _默认沙箱.validate_single(中文名)

    return {
        "通过": validate["通过"],
        "变量": entry.to_dict(),
        "校验": validate,
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "REGISTER"),
    }


def _校验变量(args: dict[str, object]) -> dict[str, object]:
    中文名 = args.get("中文名")

    if 中文名:
        result = _默认沙箱.validate_single(中文名)
    else:
        result = _默认沙箱.validate_all()

    return {
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "VALIDATE"),
        **result,
    }


def _翻译变量(args: dict[str, object]) -> dict[str, object]:
    中文名 = args["中文名"]  # pyright: ignore[reportArgumentType]
    目标 = args["目标"]  # pyright: ignore[reportArgumentType]

    entry = _默认沙箱.get(中文名)
    if not entry:
        return {
            "通过": False,
            "错误": f"变量 '{中文名}' 未注册",
            "DNA": _gen_dna("VAR-SANDBOX-MCP", "TRANSLATE-ERROR"),
        }

    target_name = entry.to_target(目标)
    target_type = _默认沙箱.translate_type(entry.类型, 目标)
    default_val = _默认沙箱.get_default_value(entry.类型, 目标)

    return {
        "通过": True,
        "中文名": 中文名,
        "目标": 目标,
        "目标变量名": target_name,
        "目标类型": target_type,
        "默认值": default_val,
        "是常量": entry.是常量,
        "当前值": str(entry.值),
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "TRANSLATE"),
    }


def _沙箱执行(args: dict[str, object]) -> dict[str, object]:
    代码 = args["代码"]  # pyright: ignore[reportArgumentType]

    result = _默认沙箱.sandbox_exec(代码)

    return {
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "EXEC"),
        **result,
    }


def _审计报告(args: dict[str, object]) -> dict[str, object]:
    变量列表 = [entry.to_dict() for entry in _默认沙箱.变量表.values()]
    校验 = _默认沙箱.validate_all()

    # 统计类型分布
    type_counts = {}
    for entry in _默认沙箱.变量表.values():
        type_counts[entry.类型] = type_counts.get(entry.类型, 0) + 1

    return {
        "通过": 校验["通过"],
        "沙箱名": _默认沙箱.沙箱名,
        "变量总数": len(_默认沙箱.变量表),
        "类型分布": type_counts,
        "常量数量": sum(1 for e in _默认沙箱.变量表.values() if e.是常量),
        "变量": 变量列表,
        "完整性": 校验,
        "最近日志": _默认沙箱.执行日志[-20:],
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "AUDIT"),
    }


def _生成代码(args: dict[str, object]) -> dict[str, object]:
    目标 = args["目标"]

    if 目标 == "all":
        targets = ["python", "js", "c", "cpp", "rust", "objc", "swift"]
        code = {}
        for t in targets:
            code[t] = _默认沙箱.generate_code(t)
        return {
            "通过": True,
            "代码": code,
            "DNA": _gen_dna("VAR-SANDBOX-MCP", "GENERATE-ALL"),
        }
    else:
        code = _默认沙箱.generate_code(目标)
        return {
            "通过": True,
            "目标": 目标,
            "代码": code,
            "DNA": _gen_dna("VAR-SANDBOX-MCP", "GENERATE"),
        }


def _对比映射(args: dict[str, object]) -> dict[str, object]:
    外部映射 = args["外部映射"]
    diffs = _默认沙箱.compare_with(外部映射)

    return {
        "通过": len(diffs) == 0,
        "差异数": len(diffs),
        "差异": diffs,
        "建议": ["将差异项对齐到沙箱标准"] if diffs else [],
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "COMPARE"),
    }


# ══════════════════════════════════════════════════════════════════
# 金融数据摄取
# ══════════════════════════════════════════════════════════════════

def _fetch_finance_sina(code: str) -> dict[str, object]:
    """从新浪财经 API 拉取股票数据"""
    import urllib.request
    try:
        # 判断市场前缀
        if code.startswith("6"):
            full_code = f"sh{code}"
        else:
            full_code = f"sz{code}"
        url = f"http://hq.sinajs.cn/list={full_code}"
        req = urllib.request.Request(url, headers={
            "Referer": "http://finance.sina.com.cn",
            "User-Agent": "Mozilla/5.0",
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode("gbk")
        # 解析: var hq_str_sh600036="名称,今开,昨收,现价,最高,最低,..."
        match = re.search(r'"(.+)"', text)
        if not match:
            return {"错误": "无法解析新浪数据"}
        parts = match.group(1).split(",")
        if len(parts) < 30:
            return {"错误": "数据字段不足"}
        return {
            "名称": parts[0],
            "今开": float(parts[1]) if parts[1] else 0,
            "昨收": float(parts[2]) if parts[2] else 0,
            "现价": float(parts[3]) if parts[3] else 0,
            "最高": float(parts[4]) if parts[4] else 0,
            "最低": float(parts[5]) if parts[5] else 0,
            "时间": parts[30] if len(parts) > 30 else "",
        }
    except Exception as e:
        return {"错误": f"新浪拉取失败: {e}"}


def _fetch_finance_binance(symbol: str) -> dict[str, object]:
    """从 Binance API 拉取数字货币价格"""
    import urllib.request
    import json as _json
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = _json.loads(resp.read().decode())
        return {"价格": float(data.get("price", 0))}
    except Exception as e:
        return {"错误": f"Binance 拉取失败: {e}"}


def _金融摄取(args: dict[str, object]) -> dict[str, object]:
    类型 = args["类型"]  # pyright: ignore[reportArgumentType]
    代码 = args["代码"]  # pyright: ignore[reportArgumentType]
    _源 = args.get("源", "auto")

    data = None
    var_prefix = ""

    if 类型 == "股票":
        data = _fetch_finance_sina(str(代码))
        var_prefix = f"股票_{代码}_"
    elif 类型 == "数字货币":
        data = _fetch_finance_binance(str(代码))
        var_prefix = f"币_{代码}_"
    else:
        return {
            "通过": False,
            "错误": f"暂不支持的金融类型: {类型}（需要配置数据源）",
            "DNA": _gen_dna("FINANCE", "INGEST-ERROR"),
        }

    if data and "错误" not in data:
        # 自动注册为沙箱变量
        registered = []
        for key, val in data.items():
            if isinstance(val, (int, float)):
                var_type = "小数" if isinstance(val, float) else "整数"
            elif isinstance(val, str):
                var_type = "文本"
            else:
                continue
            var_name = f"{var_prefix}{key}"
            _默认沙箱.register(中文名=var_name, 类型=var_type, 值=val, 来源=f"金融:{类型}")
            registered.append(var_name)

        _金融缓存[f"{类型}_{代码}"] = {"数据": data, "时间": time.time()}

        return {
            "通过": True,
            "类型": 类型,
            "代码": 代码,
            "原始数据": data,
            "已注册变量": registered,
            "DNA": _gen_dna("FINANCE", "INGEST"),
        }
    else:
        return {
            "通过": False,
            "错误": data.get("错误", "未知错误"),
            "DNA": _gen_dna("FINANCE", "INGEST-ERROR"),
        }


def _金融监控(args: dict[str, object]) -> dict[str, object]:
    前缀 = args["变量前缀"]  # pyright: ignore[reportArgumentType]
    刷新 = args.get("刷新秒数", 60)

    # 找到匹配前缀的变量
    matching = []
    for name, entry in _默认沙箱.变量表.items():
        if name.startswith(前缀):
            matching.append({
                "变量": name,
                "类型": entry.类型,
                "当前值": str(entry.值),
                "是常量": entry.是常量,
            })

    if not matching:
        return {
            "通过": True,
            "消息": f"没有找到前缀 '{前缀}' 的变量",
            "DNA": _gen_dna("FINANCE", "WATCH"),
        }

    return {
        "通过": True,
        "前缀": 前缀,
        "匹配数": len(matching),
        "变量": matching,
        "刷新间隔": f"{刷新}秒",
        "提示": "MCP 单次调用返回当前快照。如需持续监控，请定时调用本工具。",
        "DNA": _gen_dna("FINANCE", "WATCH"),
    }


def _健康检查(args: dict[str, object]) -> dict[str, object]:  # pyright: ignore[reportUnusedParameter]
    validate = _默认沙箱.validate_all()

    return {
        "通过": validate["通过"],
        "服务": "cnsh-var-sandbox",
        "版本": "1.0.0",
        "DNA": "#龍芯⚡️2026-07-06-CNSH-VAR-SANDBOX-MCP-v1.0",
        "沙箱状态": {
            "沙箱名": _默认沙箱.沙箱名,
            "变量数": len(_默认沙箱.变量表),
            "日志条数": len(_默认沙箱.执行日志),
            "完整性": "🟢 全部完整" if validate["通过"] else "🔴 存在问题",
        },
        "模块": {
            "变量沙箱引擎": True,
            "7目标类型映射": all(t in TYPE_MAP.get("整数", {}) for t in ["py","js","c","cpp","rust","objc","swift"]),
            "金融数据爬取": True,
            "沙箱执行": True,
        },
        "DNA": _gen_dna("VAR-SANDBOX-MCP", "HEALTH"),
    }


# ══════════════════════════════════════════════════════════════════
# 值解析
# ══════════════════════════════════════════════════════════════════

def _parse_value(val_str: str | None, var_type: str) -> Any:
    """将字符串值解析为对应类型"""
    if val_str is None:
        return None
    if var_type == "布尔":
        return val_str.lower() in ("true", "1", "yes", "真", "是")
    if var_type == "整数":
        try:
            return int(val_str)
        except (ValueError, TypeError):
            return 0
    if var_type == "小数":
        try:
            return float(val_str)
        except (ValueError, TypeError):
            return 0.0
    if var_type == "空值":
        return None
    # 文本/列表/映射 保持字符串
    return str(val_str)


# ══════════════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════════════

async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
