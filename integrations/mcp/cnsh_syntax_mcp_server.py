#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          CNSH 语法 MCP Server v1.0 — 龍魂数字主权工具链               ║
║  DNA: #龍芯⚡️2026-07-05-CNSH-SYNTAX-MCP-v1.0                        ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
CNSH = 中文原生语义层级（Chinese Native Semantic Hierarchy）
它是中国自主可控的中文编程语言，全部关键字用中文母语书写，
出了龍魂生态就跑不动——这不是封闭，是数字主权。

【本 MCP Server 提供什么？】
13 个工具，覆盖 CNSH 开发的完整工具链：
  📝 cnsh_lex          — 词法分析：把中文代码拆成 Token
  🌳 cnsh_parse        — 语法分析：生成 AST 抽象语法树
  🔄 cnsh_translate    — 代码转译：CNSH → Python
  ⚙️ cnsh_compile      — 目标编译：CNSH → Python/JS/Rust/C
  📖 cnsh_keywords     — 关键字查询：查 CNSH 所有中文关键字
  🛑 cnsh_redline_check — 红线熔断：检测是否违反人民数据主权
  📋 cnsh_redline_list  — 红线清单：列出全部红线词组及本源
  🧬 cnsh_dna_generate  — DNA 生成：龍魂标准追溯码
  ✅ cnsh_dna_validate  — DNA 校验：检查追溯码是否合法
  🔢 cnsh_digital_root  — 数字根：计算数字根+五行+369闸门
  🎨 cnsh_audit         — 三色审计：🟢通过 / 🟡警告 / 🔴拒绝
  🔍 cnsh_diagnostics   — 四合一诊断：词法+语法+红线+数字根
  ❤️ cnsh_health        — 健康检查：各子模块可用状态

【怎么用？】
在 MCP 客户端配置中加入本 Server，AI 即可调用上述全部工具。
基于 stdio 传输协议，兼容 Claude/Cursor/CodeBuddy 等 MCP 客户端。

【知识补全：几个你不会但需要知道的概念】
• Token（词法单元）：代码的最小有意义单元，比如 "如果" 是一个关键字 Token
• AST（抽象语法树）：代码的结构化表示，去掉语法糖，只保留语义骨架
• 数字根（Digital Root）：一个数各位反复相加直到 1-9 的结果，是 CNSH 体系的数学锚点
• 五行：金木水火土，数字根 1/6→水 2/7→火 3/8→木 4/9→金 5→土
• 369不动点：数字根 3、6、9 是龍魂数学的稳定点，源自洛书九宫
• 红线熔断：内置检测机制，发现违反人民数据主权的词组时自动阻断
"""

import asyncio
import json
import os
import sys
import re
from pathlib import Path
from typing import Any

# ══════════════════════════════════════════════════════════════════
# 路径初始化：找到龍魂系统根目录并注册所有 CNSH 子模块
# ══════════════════════════════════════════════════════════════════
# 向上走两层找到龍魂系统根目录（本文件在 integrations/mcp/ 下）
try:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
except Exception:
    # 如果解析失败，尝试环境变量
    _PROJECT_ROOT = Path(os.environ.get("LONGHUN_ROOT", os.path.expanduser("~/longhun-system")))  # pyright: ignore[reportConstantRedefinition]

# 按依赖顺序注册路径：cnsh_v21（最底层）→ cnsh-core → cnsh → 根目录
_CNSH_MODULE_PATHS = [
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1" / "cnsh_v21",  # CNSH v2.1 核心包
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1",                 # CNSH v2.1 顶层
    _PROJECT_ROOT / "cnsh-core",                                # CNSH 统一 API
    _PROJECT_ROOT / "cnsh",                                     # 转译器 + 红线引擎
    _PROJECT_ROOT,                                              # 项目根（工具脚本）
]
for _p in _CNSH_MODULE_PATHS:
    _sp = str(_p)
    if _sp not in sys.path and _p.exists():
        sys.path.insert(0, _sp)

# ══════════════════════════════════════════════════════════════════
# 核心模块导入
# ══════════════════════════════════════════════════════════════════
from cnsh_v21.lexer import Lexer  # pyright: ignore[reportMissingImports]
from cnsh_v21.parser import Parser  # pyright: ignore[reportMissingImports]
from cnsh_v21.tokens import Token, KEYWORDS as CNSH_KEYWORDS  # pyright: ignore[reportMissingImports]
from cnsh_v21.errors import CNSHError, CNSHLexError, CNSHParseError  # pyright: ignore[reportMissingImports]
from cnsh_unified import (  # pyright: ignore[reportMissingImports]
    DNA工具, 数学工具, 审计工具,
    数字根转五行, 数字根闸门,
)
from cnsh_redlines import 红线熔断器, 红线本源  # pyright: ignore[reportMissingImports]

# ══════════════════════════════════════════════════════════════════
# 可选模块导入（某些环境下可能不完整）
# ══════════════════════════════════════════════════════════════════
try:
    from cnsh_runner import translate_cnsh as _cnsh_to_python  # pyright: ignore[reportMissingImports]
except ImportError:
    _cnsh_to_python = None

try:
    from cnsh_v21 import compile_source as _cnsh_compile  # pyright: ignore[reportMissingImports]
    from cnsh_v21 import get_compiler as _get_cnsh_compiler  # pyright: ignore[reportMissingImports]
except ImportError:
    _cnsh_compile = None
    _get_cnsh_compiler = None

# ══════════════════════════════════════════════════════════════════
# MCP SDK
# ══════════════════════════════════════════════════════════════════
from mcp.server import Server  # pyright: ignore[reportMissingImports]
from mcp.server.stdio import stdio_server  # pyright: ignore[reportMissingImports]
from mcp.types import Tool, TextContent  # pyright: ignore[reportMissingImports]

# ══════════════════════════════════════════════════════════════════
# 服务器实例
# ══════════════════════════════════════════════════════════════════
app = Server("cnsh-syntax")  # pyright: ignore[reportUnknownVariableType]


# ══════════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════════

def _gen_dna(module: str = "CNSH-MCP", action: str = "TOOL-CALL") -> str:
    """
    生成龍魂标准 DNA 追溯码。
    使用统一的 DNA工具.生成 保证格式一致。
    格式: #龍芯⚡️YYYY-MM-DD-模块动作-v版本-哈希8位
    """
    return DNA工具.生成(f"{module}-{action}", "1.0")


def _serialize_token(tok: Token) -> dict[str, object]:
    """将 CNSH Token 对象转为 JSON 兼容字典"""
    return {
        "type": tok.type,       # Token 类型，如 关键字/标识符/运算符
        "value": tok.value,     # Token 原始文本
        "line": tok.line,       # 所在行号（1-based）
        "column": tok.column,   # 所在列号（1-based）
        "file": tok.file,       # 来源文件名
    }


def _serialize_ast(node: Any, depth: int = 0) -> dict[str, object] | None:  # pyright: ignore[reportUnusedParameter]
    """
    递归序列化 AST 节点为 JSON 兼容字典。
    注意：这个函数很重要——AST 是代码的结构化表示，
    把中文代码先变成 Token 再组织成树状结构，就像把一句话拆成主谓宾。
    """
    if node is None:
        return None

    result: dict[str, object] = {"node_type": type(node).__name__}

    for attr in dir(node):
        # 跳过私有属性和方法
        if attr.startswith("_"):
            continue
        val = getattr(node, attr)
        if callable(val):
            continue
        # 列表：递归处理每个元素
        if isinstance(val, list):
            result[attr] = [
                _serialize_ast(item) if hasattr(item, "__class__") and item.__class__.__module__ != "builtins"
                else str(item) if not isinstance(item, (int, float, str, bool, type(None)))
                else item
                for item in val
            ]
        # Token 对象：单独序列化
        elif isinstance(val, Token):
            result[attr] = _serialize_token(val)
        # 其他 AST 节点：递归
        elif hasattr(val, "__class__") and val.__class__.__module__ not in ("builtins",):  # pyright: ignore[reportUnknownMemberType]
            result[attr] = _serialize_ast(val)  # pyright: ignore[reportArgumentType]
        # 基础类型：直接保留
        elif isinstance(val, (int, float, str, bool, type(None))):
            result[attr] = val  # pyright: ignore[reportArgumentType]
        else:
            result[attr] = str(val)

    return result


# ══════════════════════════════════════════════════════════════════
# MCP 工具注册
# ══════════════════════════════════════════════════════════════════

@app.list_tools()  # pyright: ignore[reportUntypedFunctionDecorator,reportUnknownMemberType]
async def list_tools() -> list[Tool]:  # pyright: ignore[reportUnknownVariableType]
    return [
        # ── 词法 / 语法分析 ──
        Tool(
            name="cnsh_lex",
            description="对 CNSH 代码执行词法分析，返回 Token 列表。输入 CNSH 中文代码，输出所有词法单元（类型、值、行列位置）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "要分析的 CNSH 源代码",
                    },
                    "file": {
                        "type": "string",
                        "description": "可选文件名，用于错误报告",
                    },
                },
                "required": ["source"],
            },
        ),
        Tool(
            name="cnsh_parse",
            description="对 CNSH 代码执行语法分析，返回 AST（抽象语法树）。支持模块、类、函数、枚举、数据类、Bra-Ket 人格协作等所有 CNSH 语法结构。",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "要解析的 CNSH 源代码",
                    },
                    "file": {
                        "type": "string",
                        "description": "可选文件名",
                    },
                },
                "required": ["source"],
            },
        ),
        # ── 编译 / 转译 ──
        Tool(
            name="cnsh_translate",
            description="将 CNSH 代码转译为 Python 代码。支持全中文关键字、控制流、函数定义、类型声明等。返回等价的 Python 代码。",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "要转译的 CNSH 源代码",
                    },
                    "dump_only": {
                        "type": "boolean",
                        "description": "若为 true，只返回 Python 代码不执行红线检查",
                    },
                },
                "required": ["source"],
            },
        ),
        Tool(
            name="cnsh_compile",
            description="将 CNSH 代码编译到指定目标语言（python/cpp/c/objc/swift/js/rust）。使用 CNSH v2.1 编译器管线：词法→语法→类型检查→代码生成。",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "要编译的 CNSH 源代码",
                    },
                    "target": {
                        "type": "string",
                        "enum": ["python", "cpp", "c++", "c", "objc", "objective-c", "swift", "js", "javascript", "rust"],
                        "description": "编译目标语言，默认 python。支持：python/cpp/c/objc/swift/js/rust",
                    },
                    "optimize_level": {
                        "type": "integer",
                        "description": "优化级别 0-3，默认 0",
                    },
                },
                "required": ["source"],
            },
        ),
        # ── 关键字查询 ──
        Tool(
            name="cnsh_keywords",
            description="查询 CNSH 关键字注册表。可按类别筛选：控制流、数据类型、类与对象、龍魂专属、Bra-Ket 人格协作、装饰器、运算符等。",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["all", "控制流", "数据类型", "类与对象", "龍魂专属", "Bra-Ket", "装饰器", "运算符", "操作符"],
                        "description": "关键字类别筛选，默认 all 返回全部",
                    },
                    "search": {
                        "type": "string",
                        "description": "模糊搜索关键字名称（中文或英文）",
                    },
                },
            },
        ),
        # ── 红线熔断 ──
        Tool(
            name="cnsh_redline_check",
            description="对文本执行红线词组熔断检查（P0 伦理红线/P1 锁定红线/P2 收割红线/P3 复杂红线）。检测是否包含违反人民数据主权的红线内容，支持多语言别名和语义等价变体。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要检查的文本或代码",
                    },
                    "context": {
                        "type": "string",
                        "description": "可选的上下文说明",
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="cnsh_redline_list",
            description="列出所有已注册的红线词组，按 P0→P3 分级展示，包含根概念、定义和本源 DNA。",
            inputSchema={
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["P0", "P1", "P2", "P3", "all"],
                        "description": "按级别筛选，默认 all",
                    },
                },
            },
        ),
        # ── DNA 追溯码 ──
        Tool(
            name="cnsh_dna_generate",
            description="生成龍魂标准 DNA 追溯码（格式：#龍芯⚡️日期-模块-版本-哈希8位）。每次代码/规则/决策产生时必须附带。",
            inputSchema={
                "type": "object",
                "properties": {
                    "module": {
                        "type": "string",
                        "description": "模块名（中英文均可）",
                    },
                    "version": {
                        "type": "string",
                        "description": "版本号，如 1.0",
                    },
                },
                "required": ["module"],
            },
        ),
        Tool(
            name="cnsh_dna_validate",
            description="校验 DNA 追溯码是否合法。检查前缀是否为繁体'龍'、格式是否标准、是否存在简化字违规。",
            inputSchema={
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "要校验的 DNA 追溯码",
                    },
                },
                "required": ["dna"],
            },
        ),
        # ── 数字根 / 五行 ──
        Tool(
            name="cnsh_digital_root",
            description="计算文本或数字的数字根（digital root），并返回五行属性与三色闸门判定。数字根是 CNSH 体系中的核心数学锚点。",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "要计算的文本或数字（内容中的数字会被提取计算）",
                    },
                },
                "required": ["content"],
            },
        ),
        # ── 三色审计 ──
        Tool(
            name="cnsh_audit",
            description="三色审计判定。根据分数或状态返回 🟢(通过) / 🟡(警告) / 🔴(拒绝)。",
            inputSchema={
                "type": "object",
                "properties": {
                    "score": {
                        "type": "number",
                        "description": "审计分数 (0-10)，>=8 为 🟢，>=5 为 🟡，<5 为 🔴",
                    },
                    "status": {
                        "type": "string",
                        "description": "状态字符串 (pass/warn/ok/green/yellow/通过/正常/警告/风险 等)",
                    },
                },
            },
        ),
        # ── 一体化诊断 ──
        Tool(
            name="cnsh_diagnostics",
            description="对 CNSH 代码执行完整诊断：词法+语法+红线+数字根 四合一检查，返回所有问题汇总。适合编辑器集成。",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "要诊断的 CNSH 源代码",
                    },
                },
                "required": ["source"],
            },
        ),
        # ── 健康检查 ──
        Tool(
            name="cnsh_health",
            description="检查 CNSH MCP Server 健康状态，包括各子模块可用性、版本信息。",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ══════════════════════════════════════════════════════════════════
# MCP 工具调用处理
# ══════════════════════════════════════════════════════════════════

@app.call_tool()  # pyright: ignore[reportUntypedFunctionDecorator,reportUnknownMemberType]
async def call_tool(name: str, arguments: dict[str, object]) -> list[TextContent]:  # pyright: ignore[reportUnknownVariableType]
    try:
        result = await _dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except CNSHError as e:
        return [TextContent(type="text", text=json.dumps({
            "ok": False,
            "error": str(e),
            "error_type": "CNSHError",
            "line": getattr(e, "line", None),
            "column": getattr(e, "column", None),
            "dna": _gen_dna("CNSH-MCP", "ERROR"),
        }, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "ok": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "dna": _gen_dna("CNSH-MCP", "ERROR"),
        }, ensure_ascii=False, indent=2))]


async def _dispatch(name: str, args: dict[str, object]) -> dict[str, object]:
    if name == "cnsh_lex":
        return _handle_lex(args)
    elif name == "cnsh_parse":
        return _handle_parse(args)
    elif name == "cnsh_translate":
        return _handle_translate(args)
    elif name == "cnsh_compile":
        return _handle_compile(args)
    elif name == "cnsh_keywords":
        return _handle_keywords(args)
    elif name == "cnsh_redline_check":
        return _handle_redline_check(args)
    elif name == "cnsh_redline_list":
        return _handle_redline_list(args)
    elif name == "cnsh_dna_generate":
        return _handle_dna_generate(args)
    elif name == "cnsh_dna_validate":
        return _handle_dna_validate(args)
    elif name == "cnsh_digital_root":
        return _handle_digital_root(args)
    elif name == "cnsh_audit":
        return _handle_audit(args)
    elif name == "cnsh_diagnostics":
        return _handle_diagnostics(args)
    elif name == "cnsh_health":
        return _handle_health(args)
    else:
        return {"ok": False, "error": f"未知工具: {name}"}


# ══════════════════════════════════════════════════════════════════
# 处理函数
# ══════════════════════════════════════════════════════════════════

def _handle_lex(args: dict[str, object]) -> dict[str, object]:
    source = str(args["source"])
    file = str(args.get("file", "<cnsh>"))
    lexer = Lexer(source, file=file)
    try:
        tokens = lexer.tokenize()
    except CNSHLexError as e:
        return {
            "ok": False,
            "error": str(e),
            "line": e.line,
            "column": e.column,
            "dna": _gen_dna("CNSH-MCP", "LEX-ERROR"),
        }

    token_list = [_serialize_token(t) for t in tokens]
    # 统计
    stats = {}
    for t in token_list:
        stats[t["type"]] = stats.get(t["type"], 0) + 1

    return {  # pyright: ignore[reportReturnType]
        "ok": True,
        "token_types": stats,
        "tokens": token_list,
        "dna": _gen_dna("CNSH-MCP", "LEX"),
    }


def _handle_parse(args: dict[str, object]) -> dict[str, object]:
    source = str(args["source"])
    file = str(args.get("file", "<cnsh>"))
    lexer = Lexer(source, file=file)

    try:
        tokens = lexer.tokenize()
    except CNSHLexError as e:
        return {
            "ok": False,
            "phase": "lex",
            "error": str(e),
            "line": e.line,
            "column": e.column,
            "dna": _gen_dna("CNSH-MCP", "PARSE-LEX-ERROR"),
        }

    parser = Parser(tokens)
    try:
        ast = parser.parse()
    except CNSHParseError as e:
        return {
            "ok": False,
            "phase": "parse",
            "error": str(e),
            "line": e.line,
            "column": e.column,
            "dna": _gen_dna("CNSH-MCP", "PARSE-ERROR"),
        }

    return {
        "ok": True,
        "statement_count": len(ast.statements),
        "ast": _serialize_ast(ast),
        "dna": _gen_dna("CNSH-MCP", "PARSE"),
    }


def _handle_translate(args: dict[str, object]) -> dict[str, object]:
    """CNSH → Python 转译。默认只输出不执行，保证安全。"""
    if _cnsh_to_python is None:
        return {
            "ok": False,
            "error": "cnsh_runner 转译模块不可用，请确保 cnsh/cnsh_runner.py 存在",
            "dna": _gen_dna("CNSH-MCP", "TRANSLATE-UNAVAILABLE"),
        }

    source = str(args["source"])
    # dumpOnly=false 时才会同时执行红线检查（MCP 中默认只输出）
    dump_only = bool(args.get("dumpOnly", args.get("dump_only", True)))

    try:
        py_code = _cnsh_to_python(source)
    except Exception as e:
        return {
            "ok": False,
            "error": f"转译失败: {e}",
            "dna": _gen_dna("CNSH-MCP", "TRANSLATE-ERROR"),
        }

    # 红线检查：扫描源码+生成的 Python 代码是否含有违规词组
    redline_result = None
    if not dump_only:
        fusing = 红线熔断器()
        redline_result = fusing.熔断检查(source + "\n" + py_code)

    return {
        "ok": True,
        "python_code": py_code,
        "redline": redline_result,
        "dna": _gen_dna("CNSH-MCP", "TRANSLATE"),
    }


def _handle_compile(args: dict[str, object]) -> dict[str, object]:
    if _cnsh_compile is None:
        return {
            "ok": False,
            "error": "CNSH v2.1 编译器不可用",
            "dna": _gen_dna("CNSH-MCP", "COMPILE-UNAVAILABLE"),
        }

    source = str(args["source"])
    target = str(args.get("target", "python")).lower()
    optimize = int(args.get("optimize_level", 0))  # pyright: ignore[reportArgumentType]

    # 标准化 target 名
    target_map = {
        "js": "javascript", "py": "python", "rs": "rust",
        "c": "c", "cc": "c", "c++": "cpp", "cpp": "cpp",
        "objc": "objc", "objective-c": "objc",
        "swift": "swift",
    }
    target = target_map.get(target, target)

    try:
        code = _cnsh_compile(source, target=target, optimize_level=optimize, type_check=True, strict_types=False)
    except Exception as e:
        return {
            "ok": False,
            "error": f"编译失败 ({target}): {e}",
            "dna": _gen_dna("CNSH-MCP", "COMPILE-ERROR"),
        }

    return {
        "ok": True,
        "target": target,
        "code": code,
        "dna": _gen_dna("CNSH-MCP", "COMPILE"),
    }


def _handle_keywords(args: dict[str, object]) -> dict[str, object]:
    category = str(args.get("category", "all"))
    search = str(args.get("search", "")).lower()

    # 分类所有关键字
    categories = {
        "控制流": ["如果", "否则如果", "否则", "当", "对于", "在", "返回",
                   "跳出", "继续", "尝试", "捕获", "最终", "抛出", "通过",
                   "产生", "产生于", "使用", "作为", "异步", "等待"],
        "数据类型": ["文本", "字符串", "整数", "浮点数", "小数", "布尔", "真假",
                   "列表", "映射", "空", "真", "假"],
        "类与对象": ["类", "定义", "自己", "超类", "初始化", "调用", "变量", "常量"],
        "装饰器": ["属性", "类方法", "静态方法", "抽象方法", "枚举类", "枚举唯一", "数据类", "字段", "默认工厂"],
        "龍魂专属": ["三色审计", "DNA追溯", "量子纠缠", "熔断", "回滚", "钩子",
                   "天道", "六层来源链", "君子协议", "内容主权"],
        "Bra-Ket": ["人格基态", "人格空间", "角色", "职责", "权重", "测量",
                  "酉演化", "协作概率", "执行任务", "叠加态", "场景", "系统"],
        "运算符": {"且": "AND", "或": "OR", "非": "NOT", "等于": "EQ", "不等于": "NE",
                 "大于": "GT", "小于": "LT", "大于等于": "GE", "小于等于": "LE"},
        "操作符": {"+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH", "%": "PERCENT",
                 "=": "ASSIGN", "==": "EQ", "!=": "NE", "<": "LT", ">": "GT",
                 "<=": "LE", ">=": "GE", "&&": "AND", "||": "OR", "!": "NOT"},
    }

    # 获取完整关键字映射
    all_kw = dict(CNSH_KEYWORDS)

    if category == "all":
        output = {}
        for cat_name, kw_list in categories.items():
            if isinstance(kw_list, dict):
                filtered = {k: v for k, v in kw_list.items() if not search or search in k.lower()}
            else:
                filtered = {k: all_kw.get(k, k) for k in kw_list if not search or search in k.lower()}
            if filtered:
                output[cat_name] = filtered
    elif category in categories:
        kw_list = categories[category]
        if isinstance(kw_list, dict):
            output = {category: {k: v for k, v in kw_list.items() if not search or search in k.lower()}}
        else:
            output = {category: {k: all_kw.get(k, k) for k in kw_list if not search or search in k.lower()}}
    else:
        return {"ok": False, "error": f"未知类别: {category}"}

    return {
        "ok": True,
        "keywords": output,
        "total_count": sum(len(v) for v in output.values()),
        "dna": _gen_dna("CNSH-MCP", "KEYWORDS"),
    }


def _handle_redline_check(args: dict[str, object]) -> dict[str, object]:
    text = str(args["text"])
    context = str(args.get("context", ""))
    fusing = 红线熔断器()
    result = fusing.熔断检查(text, context)

    return {
        "ok": True,
        "triggered": result["触发"],
        "highest_level": result["最高级别"],
        "hits": result["命中"],
        "report": fusing.报告(result) if result["触发"] else "🟢 红线扫描通过",
        "dna": result["DNA"],
    }


def _handle_redline_list(args: dict[str, object]) -> dict[str, object]:
    level = str(args.get("level", "all"))
    level_map = {
        "P0": "P0_伦理红线",
        "P1": "P1_锁定红线",
        "P2": "P2_收割红线",
        "P3": "P3_复杂红线",
    }

    items = []
    for name, info in 红线本源.items():
        lv = info["级别"]
        if level != "all" and lv != level_map.get(level, ""):
            continue
        items.append({
            "name": name,
            "level": lv,
            "root_concept": info.get("根概念", ""),
            "definition": info.get("定义", ""),
            "source_dna": info.get("来源DNA", ""),
            "aliases": info.get("语义等价", []),
        })

    return {
        "ok": True,
        "level_filter": level,
        "count": len(items),
        "redlines": items,
        "dna": _gen_dna("CNSH-MCP", "REDLINE-LIST"),
    }


def _handle_dna_generate(args: dict[str, object]) -> dict[str, object]:
    module = str(args["module"])
    version = str(args.get("version", "1.0"))
    dna = DNA工具.生成(module, version)

    return {
        "ok": True,
        "dna": dna,
        "standard_prefix": DNA工具.标准前缀,
        "module": module,
        "version": version,
    }


def _handle_dna_validate(args: dict[str, object]) -> dict[str, object]:
    dna = str(args["dna"])
    result = DNA工具.校验(dna)

    # 🔄 繁简归一：简/繁均合法，仅记录用于审计
    checks = {
        "has_simplified_dragon": "龍芯" in dna or "龍魂" in dna,  # 相容接收，仅记录
        "has_proper_dragon": "龍" in dna,
        "has_lightning": "⚡️" in dna or "⚡" in dna,
        "length": len(dna),
    }

    return {
        "ok": True,
        "dna": dna,
        "valid": result["合法"],
        "recommended_format": result.get("推荐", False),
        "reason": result.get("原因"),
        "parsed": result.get("解析"),
        "extra_checks": checks,
    }


def _handle_digital_root(args: dict[str, object]) -> dict[str, object]:
    """
    计算文本中数字的数字根、五行属性、369 闸门。
    这是 CNSH 体系的数学锚点——任何决策、代码、文本都可以算出数字根，
    用于三色审计判定和流场方向引导。
    """
    content = str(args["content"])

    # 提取文本中的所有数字
    digits_text = re.sub(r"[^0-9]", "", str(content))

    if not digits_text:
        return {
            "ok": True,
            "content": content,
            "extracted_digits": "",
            "digital_root": 0,
            "wuxing": 数学工具.数字根转五行(0),
            "gate": 数学工具.数字根闸门(0),
            "special_note": "零位 — 无极/混沌态（无数字内容）",
            "dna": _gen_dna("CNSH-MCP", "DIGITAL-ROOT"),
        }

    # 计算数字根：把提取的数字加起来，结果如果 ≥10 继续加，直到 1-9
    dr = 数学工具.计算数字根(int(digits_text) if digits_text else 0)
    wuxing = 数学工具.数字根转五行(dr)
    gate = 数学工具.数字根闸门(dr)

    # 369 不动点说明（龍魂数学的核心稳定点）
    special = ""
    if dr in (3, 6, 9):
        special = "369不动点 — 龍魂数学稳定锚点，洛书九宫核心"
    elif dr == 0:
        special = "零位 — 无极/混沌态"

    return {
        "ok": True,
        "content": content,
        "extracted_digits": digits_text,
        "digital_root": dr,
        "wuxing": wuxing,
        "gate": gate,
        "special_note": special,
        "dna": _gen_dna("CNSH-MCP", "DIGITAL-ROOT"),
    }


def _handle_audit(args: dict[str, object]) -> dict[str, object]:
    score = args.get("score")
    status = args.get("status")

    if score is not None:
        result = 审计工具.三色审计(score)
        return {
            "ok": True,
            "input_type": "score",
            "score": score,
            "result": result,
            "dna": _gen_dna("CNSH-MCP", "AUDIT"),
        }
    elif status is not None:
        result = 审计工具.三色状态(status)
        return {
            "ok": True,
            "input_type": "status",
            "status": status,
            "result": result,
            "dna": _gen_dna("CNSH-MCP", "AUDIT"),
        }
    else:
        return {
            "ok": False,
            "error": "请提供 score 或 status 参数",
            "dna": _gen_dna("CNSH-MCP", "AUDIT-NO-INPUT"),
        }


def _handle_diagnostics(args: dict[str, object]) -> dict[str, object]:
    """四合一完整诊断：词法+语法+红线+数字根"""
    source = str(args["source"])
    issues = []
    warnings = []
    passes = []

    # 1. 词法检查
    try:
        lexer = Lexer(source, file="<diagnostics>")
        tokens = lexer.tokenize()
        passes.append("词法分析通过")
    except CNSHLexError as e:
        issues.append({
            "phase": "lex",
            "severity": "error",
            "message": str(e),
            "line": e.line,
            "column": e.column,
        })

    # 2. 语法检查
    try:
        lexer = Lexer(source, file="<diagnostics>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        passes.append(f"语法分析通过 ({len(ast.statements)} 条语句)")
    except CNSHLexError as e:
        pass  # 已在词法阶段捕获
    except CNSHParseError as e:
        issues.append({
            "phase": "parse",
            "severity": "error",
            "message": str(e),
            "line": e.line,
            "column": e.column,
        })
    except Exception as e:
        issues.append({
            "phase": "parse",
            "severity": "error",
            "message": str(e),
        })

    # 3. 红线检查
    try:
        fusing = 红线熔断器()
        redline_result = fusing.熔断检查(source)
        if redline_result["触发"]:
            for hit in redline_result["命中"]:
                issues.append({
                    "phase": "redline",
                    "severity": "error" if "P0" in hit["级别"] else "warning",
                    "message": f"[{hit['级别']}] {hit['红线词组']}: {hit['定义']}",
                    "root_concept": hit.get("根概念"),
                    "source_dna": hit.get("来源DNA"),
                })
        else:
            passes.append("红线检查通过")
    except Exception as e:
        warnings.append({
            "phase": "redline",
            "message": f"红线检查异常: {e}",
        })

    # 4. 数字根检查
    try:
        digits = re.sub(r"[^0-9]", "", source)
        if digits:
            dr = 数学工具.计算数字根(int(digits))
            gate = 数学工具.数字根闸门(dr)
            if gate == "🔴":
                issues.append({
                    "phase": "digital_root",
                    "severity": "warning",
                    "message": f"数字根 {dr} ({数学工具.数字根转五行(dr)}) 触发红色闸门",
                })
            else:
                passes.append(f"数字根: {dr} ({数学工具.数字根转五行(dr)}) {gate}")
        else:
            passes.append("数字根: 无数字内容")
    except Exception as e:
        warnings.append({
            "phase": "digital_root",
            "message": f"数字根计算异常: {e}",
        })

    # 汇总
    error_count = sum(1 for i in issues if i.get("severity") == "error")
    warning_count = sum(1 for i in issues if i.get("severity") == "warning")

    summary = "🟢 全部通过" if error_count == 0 else f"🔴 {error_count} 错误, 🟡 {warning_count} 警告"

    return {
        "ok": error_count == 0,
        "summary": summary,
        "error_count": error_count,
        "warning_count": warning_count,
        "issues": issues,
        "warnings": warnings,
        "passes": passes,
        "dna": _gen_dna("CNSH-MCP", "DIAGNOSTICS"),
    }


def _handle_health(args: dict[str, object]) -> dict[str, object]:  # pyright: ignore[reportUnusedParameter]
    """
    健康检查：报告所有子模块的可用状态。
    如果某个模块显示 False，说明对应文件缺失或导入失败，
    需要检查对应目录是否存在。
    """
    return {
        "ok": True,
        "server": "cnsh-syntax",
        "version": "1.0.0",
        "identity_dna": "#龍芯⚡️2026-07-05-CNSH-SYNTAX-MCP-v1.0",
        "modules": {
            "词法分析器_lexer": True,
            "语法分析器_parser": True,
            "转译器_translator": _cnsh_to_python is not None,
            "编译器v21_compiler": _cnsh_compile is not None,
            "红线引擎_redlines": True,
            "DNA追溯工具": True,
            "数学工具_五行数字根": True,
            "审计工具_三色": True,
        },
        "available_targets": (["python", "c", "cpp", "objc", "swift", "javascript", "rust"] if _cnsh_compile else []),
        "project_root": str(_PROJECT_ROOT),
        "dna": _gen_dna("CNSH-MCP", "HEALTH"),
    }


# ══════════════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════════════

async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
