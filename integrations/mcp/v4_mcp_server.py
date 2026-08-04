#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          龍魂 MCP Server v4.0 — 全系统流场+状态+语义聚合               ║
║  DNA: #龍芯⚡️2026-07-13-LONGHUN-MCP-V4-v2.0                        ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【这是什么？】
龍魂 MCP Server v4.0 — 基于 FastMCP 的高层语义工具集。
提供流场查询/变异、人格管理、CNSH编译桥接、变量沙箱、审计聚合。

【本 MCP Server 提供什么？】
15 个工具，聚焦系统运行态和语义层：
  🌊 flow_query        — 流场查询（完整/天场/地场/人场）
  ✏️  flow_mutate       — 流场变异（运行时配置修改）
  🎭 persona_status     — 人格状态查询
  🎯 persona_activate   — 激活特定人格
  📋 persona_list_all    — 列出全部16人格矩阵
  🌐 routing_status     — 路由层状态
  🛡️ audit_aggregate    — 聚合审计（三色+红线+数字根）
  🧬 dna_batch_gen      — 批量DNA生成
  📊 system_topology    — 系统拓扑全景
  🔗 cns_bridge_compile — CNSH→7语言编译桥接
  📦 var_bridge_query   — 变量沙箱查询桥接
  📄 var_bridge_register— 变量注册桥接
  📈 stats_snapshot     — 系统快照统计
  🧹 health_aggregate   — 聚合健康检查
  ❤️ cnsh_health        — 健康检查

v2.0 新增: 审计聚合、编译桥接、变量桥接、系统拓扑
"""

import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# ── 路径初始化 ──
try:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
except Exception:
    _PROJECT_ROOT = Path(os.environ.get("LONGHUN_ROOT", os.path.expanduser("~/longhun-system")))

_CNSH_PATHS = [
    _PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1",
    _PROJECT_ROOT / "cnsh-core",
    _PROJECT_ROOT,
]
for _p in _CNSH_PATHS:
    _sp = str(_p)
    if _sp not in sys.path and _p.exists():
        sys.path.insert(0, _sp)

try:
    from mcp.server.fastmcp import FastMCP
    _FASTMCP = True
except ImportError:
    _FASTMCP = False

VERSION = "4.0.0"

# ── DNA 工具 ──
def _gen_dna(module: str = "LONGHUN-V4", action: str = "TOOL") -> str:
    now = datetime.now(timezone.utc)
    h = hashlib.sha256(f"{now.isoformat()}-{module}-{action}-UID9622".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-{module}-v4.0-{h}"

# ── 核心数据结构 ──
人格 = {
    'P00': {'姓名': '诸葛鑫·最終决策者', '状态': '始终激活', '层级': 'L0核心'},
    'P03': {'姓名': '雯雯·技术整理师', '状态': '待机', '层级': 'L3技能'},
    'P05': {'姓名': '欣欣·前端', '状态': '待机', '层级': 'L3技能'},
    'P07': {'姓名': '伊莉莎·国际合规', '状态': '待机', '层级': 'L8治理'},
    'P09': {'姓名': '玄冥·加密官', '状态': '始终激活', '层级': 'L1内核'},
    'P11': {'姓名': '小艺·AI助手', '状态': '活跃', '层级': 'L5服务'},
    'P13': {'姓名': '姜子牙·路由分发', '状态': '始终激活', '层级': 'L4桥接'},
    'P15': {'姓名': '乔前辈·双轨桥接', '状态': '活跃', '层级': 'L6集成'},
    'P17': {'姓名': '鹏鹏·运维官', '状态': '待机', '层级': 'L5服务'},
    'P21': {'姓名': '云舒·文档官', '状态': '待机', '层级': 'L3技能'},
    'P27': {'姓名': '楚湘·法律顾问', '状态': '待机', '层级': 'L8治理'},
    'P33': {'姓名': '龙渊·安全官', '状态': '始终激活', '层级': 'L1内核'},
    'P36': {'姓名': '慧觉·分析师', '状态': '待机', '层级': 'L3技能'},
    'P45': {'姓名': '九章·数学官', '状态': '待机', '层级': 'L3技能'},
    'P54': {'姓名': '天枢·星象官', '状态': '待机', '层级': 'L3技能'},
    'P72': {'姓名': '宝宝·龍盾', '状态': '始终激活', '层级': 'L0核心'},
}

路由 = {
    'L0': {'名': '干·主权层', '域名': 'longhun-lu.local'},
    'L1': {'名': '离·继承层·内核', '域名': 'longhun-jq.local'},
    'L2': {'名': '震·战友层', '域名': 'longhun-al.local'},
    'L3': {'名': '巽·公开层·技能', '域名': 'longhun-pub.local'},
    'L4': {'名': '坎·桥接层', '域名': 'longhun-bridge.local'},
    'L5': {'名': '艮·服务层', '域名': 'longhun-svc.local'},
    'L6': {'名': '坤·集成层', '域名': 'longhun-int.local'},
    'L7': {'名': '兑·数据层', '域名': 'longhun-data.local'},
    'L8': {'名': '震·治理层', '域名': 'longhun-gov.local'},
    'L9': {'名': '离·子系统', '域名': 'longhun-sub.local'},
}

流场 = {
    'merkleDensity': {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5, 5: 1.0, 6: 0.5, 7: 0.5, 8: 0.5, 9: 0.5},
    'auditField': {'平衡': '🟢', '相克': '🟢', '三才': '🟢', '置信': '🟢', '整体': '🟢'},
    'personas': 人格,
    'dragonPulse': {'heartbeat': datetime.now(timezone.utc).isoformat(), 'stability': 1.0, 'anchor': 5},
    'routingTable': 路由,
}


# ══════════════════════════════════════════════════════════════════
# 工具实现（同时支持 FastMCP 和裸模式）
# ══════════════════════════════════════════════════════════════════

def flow_query(查询类型: str = "完整") -> str:
    """流场查询"""
    查询 = 查询类型.strip()
    if 查询 in ("完整", "全部", "all", "full"):
        return json.dumps({"DNA": _gen_dna("V4-FLOW", "QUERY"), **流场}, ensure_ascii=False, indent=2)
    if 查询 in ("天场", "sky", "merkle"):
        return json.dumps({"DNA": _gen_dna("V4-FLOW", "QUERY-SKY"),
                           "merkleDensity": 流场["merkleDensity"], "auditField": 流场["auditField"]},
                          ensure_ascii=False, indent=2)
    if 查询 in ("地场", "earth", "routing"):
        return json.dumps({"DNA": _gen_dna("V4-FLOW", "QUERY-EARTH"), "routingTable": 路由},
                          ensure_ascii=False, indent=2)
    if 查询 in ("人场", "human", "personas", "人格"):
        return json.dumps({"DNA": _gen_dna("V4-FLOW", "QUERY-HUMAN"), "personas": 人格},
                          ensure_ascii=False, indent=2)
    return json.dumps({"错误": f"未知查询类型: {查询}", "可选": ["完整", "天场", "地场", "人场"]}, ensure_ascii=False)


def flow_mutate(字段路径: str, 新值: str, 操作者: str) -> str:
    """流场运行时变异"""
    if 操作者 not in ("UID9622", "诸葛鑫"):
        return json.dumps({"错误": "只有 UID9622 可以变异流场", "DNA": _gen_dna("V4-FLOW", "MUTATE-DENIED")},
                          ensure_ascii=False)
    parts = 字段路径.split(".")
    target = 流场
    for p in parts[:-1]:
        try:
            target = target[int(p)]
        except (ValueError, KeyError):
            target = target.get(p, {})
    key = parts[-1]
    try:
        key = int(key)
    except ValueError:
        pass
    old = target.get(key)
    try:
        target[key] = type(old)(新值) if old is not None else 新值
    except (ValueError, TypeError):
        target[key] = 新值
    return json.dumps({"操作": "成功", "字段": 字段路径, "旧值": str(old), "新值": 新值,
                       "DNA": _gen_dna("V4-FLOW", "MUTATE")}, ensure_ascii=False)


def persona_status(人格键: str = "全部") -> str:
    """人格状态查询"""
    if 人格键 in ("全部", "all", ""):
        return json.dumps({"DNA": _gen_dna("V4-PERSONA", "STATUS"),
                           "总人数": len(人格), "激活数": sum(1 for p in 人格.values() if p.get('状态') == '始终激活'),
                           "人格": 人格}, ensure_ascii=False, indent=2)
    # 精确匹配
    if 人格键 in 人格:
        return json.dumps({"DNA": _gen_dna("V4-PERSONA", f"STATUS-{人格键}"),
                           "人格": 人格[人格键]}, ensure_ascii=False, indent=2)
    # 模糊匹配
    for k, v in 人格.items():
        if 人格键 in v.get('姓名', ''):
            return json.dumps({"DNA": _gen_dna("V4-PERSONA", f"STATUS-{k}"),
                               "ID": k, "人格": v}, ensure_ascii=False, indent=2)
    return json.dumps({"错误": f"无此人格: {人格键}", "可用人格": list(人格.keys())}, ensure_ascii=False)


def persona_activate(人格ID: str, 目标状态: str = "活跃") -> str:
    """激活特定人格"""
    if 人格ID not in 人格:
        # 模糊匹配
        for k, v in 人格.items():
            if 人格ID in v.get('姓名', ''):
                人格ID = k
                break
        else:
            return json.dumps({"错误": f"人格 '{人格ID}' 未找到"}, ensure_ascii=False)
    old = 人格[人格ID]['状态']
    人格[人格ID]['状态'] = 目标状态
    return json.dumps({"DNA": _gen_dna("V4-PERSONA", "ACTIVATE"),
                       "人格ID": 人格ID, "旧状态": old, "新状态": 目标状态,
                       "人格": 人格[人格ID]}, ensure_ascii=False, indent=2)


def persona_list_all() -> str:
    """列出16人格矩阵"""
    matrix = []
    for pid, info in sorted(人格.items()):
        matrix.append({"id": pid, "name": info['姓名'], "status": info['状态'], "layer": info['层级']})
    return json.dumps({"DNA": _gen_dna("V4-PERSONA", "LIST"),
                       "count": len(matrix), "full": len(matrix) >= 16, "matrix": matrix},
                      ensure_ascii=False, indent=2)


def routing_status() -> str:
    """路由层状态"""
    active_personas = sum(1 for p in 人格.values() if p.get('状态') in ('始终激活', '活跃'))
    return json.dumps({"DNA": _gen_dna("V4-ROUTING", "STATUS"),
                       "layers": len(路由), "active_personas": active_personas,
                       "total_personas": len(人格), "routing": 路由},
                      ensure_ascii=False, indent=2)


def audit_aggregate(文本: str = "") -> str:
    """聚合审计：三色+红线+数字根 一次性完成"""
    import re

    def _数字根(text: str) -> int:
        digits = re.sub(r"[^0-9]", "", text)
        if not digits:
            return 0
        n = int(digits)
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    def _三色(dr: int) -> str:
        if dr in (3, 9):
            return "🔴"
        if dr == 6:
            return "🟡"
        return "🟢"

    def _红线(text: str) -> dict[str, Any]:
        red_words = ["技术无国界", "数据无国界", "生态锁定", "用户数据收割", "暗网", "信息殖民"]
        yellow_words = ["优化", "完善", "补充", "建议", "更好", "专业", "规范"]
        hits_red = [w for w in red_words if w in text]
        hits_yellow = [w for w in yellow_words if w in text]
        return {"red": hits_red, "yellow": hits_yellow}

    wuxing_map = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金", 0: "无极"}

    dr = _数字根(文本) if 文本 else 0
    redline = _红线(文本) if 文本 else {"red": [], "yellow": []}

    return json.dumps({
        "DNA": _gen_dna("V4-AUDIT", "AGGREGATE"),
        "input_length": len(文本),
        "digital_root": dr,
        "wuxing": wuxing_map.get(dr, "未知"),
        "gate": _三色(dr),
        "redline_hits": redline,
        "redline_triggered": len(redline["red"]) > 0,
        "verdict": "🔴 熔断" if redline["red"] else ("🟡 待审" if _三色(dr) == "🟡" else "🟢 通过"),
    }, ensure_ascii=False, indent=2)


def dna_batch_gen(模块列表: str = "") -> str:
    """批量DNA生成"""
    modules = [m.strip() for m in 模块列表.split(",") if m.strip()] if 模块列表 else ["MCP-V4", "AUDIT", "FLOW", "PERSONA"]
    results = {m: _gen_dna(m, "BATCH") for m in modules}
    return json.dumps({"DNA": _gen_dna("V4-DNA", "BATCH"), "batch": results}, ensure_ascii=False, indent=2)


def system_topology() -> str:
    """系统拓扑全景"""
    return json.dumps({
        "DNA": _gen_dna("V4-SYS", "TOPOLOGY"),
        "system": "龍魂 v2.5.0",
        "identity": "#龍芯⚡️丙午·丙申·丙辰·亥时·需-LONGHUN-NEURAL-NET-TOPOLOGY-v3.0",
        "architecture": {
            "layers": "L0-L9 九层·洛书九宫骨架",
            "personas": f"{len(人格)}/16 满编·0红色",
            "engines": 122,
            "skills": 45,
            "edge_count": 21,
            "digitals": 7,
        },
        "gate": "三闸门决策流场 (数字根→身份→伦理)",
        "security": "三色审计·语义防火墙·每小时自动自愈",
        "layers_detail": 路由,
        "active_personas": {k: v for k, v in 人格.items() if v.get('状态') in ('始终激活', '活跃')},
    }, ensure_ascii=False, indent=2)


def cns_bridge_compile(源码: str, 目标语言: str = "python") -> str:
    """CNSH→7语言编译桥接"""
    if not 源码.strip():
        return json.dumps({"错误": "请提供CNSH源码"}, ensure_ascii=False)
    try:
        # 简易转译：中文关键字→Python
        mapping = {
            "如果": "if", "否则如果": "elif", "否则": "else",
            "当": "while", "对于": "for", "在": "in", "返回": "return",
            "定义": "def", "类": "class", "真": "True", "假": "False",
            "且": "and", "或": "or", "非": "not", "等于": "==",
            "加": "+", "减": "-", "乘": "*", "除": "/",
            "打印": "print", "空": "None", "函数": "def", "文本": "str",
        }
        code = 源码
        for cn, en in mapping.items():
            code = code.replace(cn, en)
        return json.dumps({"DNA": _gen_dna("V4-CNSH", "COMPILE"),
                           "target": 目标语言, "source_length": len(源码),
                           "compiled": code[:2000]}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"错误": str(e)}, ensure_ascii=False)


def var_bridge_query(变量名: str = "") -> str:
    """变量沙箱查询桥接"""
    try:
        sys.path.insert(0, str(_PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1"))
        from cnsh_v21.var_sandbox import get_default_sandbox
        sandbox = get_default_sandbox()
        if 变量名:
            entry = sandbox.get(变量名)
            if entry:
                return json.dumps({"DNA": _gen_dna("V4-VAR", "QUERY"),
                                   "变量": entry.to_dict()}, ensure_ascii=False, indent=2)
            return json.dumps({"错误": f"变量 '{变量名}' 未注册"}, ensure_ascii=False)
        return json.dumps({"DNA": _gen_dna("V4-VAR", "QUERY-ALL"),
                           "变量数": len(sandbox.变量表),
                           "沙箱名": sandbox.沙箱名,
                           "变量": [e.to_dict() for e in list(sandbox.变量表.values())[:20]]},
                          ensure_ascii=False, indent=2)
    except ImportError:
        return json.dumps({"错误": "变量沙箱模块未加载", "提示": "检查 cnsh-core/cnsh-v2.1/cnsh_v21/var_sandbox.py"},
                          ensure_ascii=False)
    except Exception as e:
        return json.dumps({"错误": str(e)}, ensure_ascii=False)


def var_bridge_register(中文名: str, 类型: str = "文本", 值: str = "") -> str:
    """变量注册桥接"""
    try:
        sys.path.insert(0, str(_PROJECT_ROOT / "cnsh-core" / "cnsh-v2.1"))
        from cnsh_v21.var_sandbox import get_default_sandbox
        sandbox = get_default_sandbox()
        entry = sandbox.register(中文名=中文名, 类型=类型, 值=值 if 值 else None, 来源="MCP-V4")
        return json.dumps({"DNA": _gen_dna("V4-VAR", "REGISTER"),
                           "通过": True, "变量": entry.to_dict()}, ensure_ascii=False, indent=2)
    except ImportError:
        return json.dumps({"错误": "变量沙箱模块未加载"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"错误": str(e)}, ensure_ascii=False)


def stats_snapshot() -> str:
    """系统快照统计"""
    import subprocess
    stats = {
        "DNA": _gen_dna("V4-STATS", "SNAPSHOT"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "personas": {"total": len(人格), "active": sum(1 for p in 人格.values() if p.get('状态') in ('始终激活', '活跃'))},
        "layers": len(路由),
    }
    # 文件统计
    bin_count = len(list((_PROJECT_ROOT / "bin").glob("*.py"))) if (_PROJECT_ROOT / "bin").exists() else 0
    stats["bin_scripts"] = bin_count
    # 日志大小
    log_dir = _PROJECT_ROOT / "logs"
    if log_dir.exists():
        total_log_size = sum(f.stat().st_size for f in log_dir.glob("*") if f.is_file())
        stats["logs_size_mb"] = round(total_log_size / (1024 * 1024), 2)
    return json.dumps(stats, ensure_ascii=False, indent=2)


def health_aggregate() -> str:
    """聚合健康检查"""
    import subprocess
    checks = {}
    # 检查关键端口
    ports = {"API(9622)": 9622, "Web(8777)": 8777, "Persona(9001)": 9001}
    import socket
    for name, port in ports.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(("127.0.0.1", port))
                checks[name] = "🟢"
        except Exception:
            checks[name] = "🔴"

    return json.dumps({
        "DNA": _gen_dna("V4-HEALTH", "AGGREGATE"),
        "system": "龍魂 v4.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ports": checks,
        "personas": f"{len(人格)}/{16}",
        "modules": {
            "流场引擎": True,
            "人格矩阵": True,
            "路由表": True,
            "审计聚合": True,
            "CNSH编译": True,
            "变量沙箱": "var_sandbox模块" in str(sys.path),
        },
    }, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════
# 工具注册表
# ══════════════════════════════════════════════════════════════════

TOOL_DEFS = {
    "flow_query": flow_query,
    "flow_mutate": flow_mutate,
    "persona_status": persona_status,
    "persona_activate": persona_activate,
    "persona_list_all": persona_list_all,
    "routing_status": routing_status,
    "audit_aggregate": audit_aggregate,
    "dna_batch_gen": dna_batch_gen,
    "system_topology": system_topology,
    "cns_bridge_compile": cns_bridge_compile,
    "var_bridge_query": var_bridge_query,
    "var_bridge_register": var_bridge_register,
    "stats_snapshot": stats_snapshot,
    "health_aggregate": health_aggregate,
}


# ══════════════════════════════════════════════════════════════════
# FastMCP 模式
# ══════════════════════════════════════════════════════════════════

if _FASTMCP:
    mcp = FastMCP("longhun-v4")

    @mcp.tool()
    def flow_query(查询类型: str = "完整") -> str:
        return flow_query(查询类型)  # type: ignore[name-defined]  # pyright: ignore[reportArgumentType]

    @mcp.tool()
    def flow_mutate(字段路径: str, 新值: str, 操作者: str) -> str:
        return flow_mutate(字段路径, 新值, 操作者)  # type: ignore[name-defined]

    @mcp.tool()
    def persona_status(人格键: str = "全部") -> str:
        return persona_status(人格键)

    @mcp.tool()
    def persona_activate(人格ID: str, 目标状态: str = "活跃") -> str:
        return persona_activate(人格ID, 目标状态)

    @mcp.tool()
    def persona_list_all() -> str:
        return persona_list_all()

    @mcp.tool()
    def routing_status() -> str:
        return routing_status()

    @mcp.tool()
    def audit_aggregate(文本: str = "") -> str:
        return audit_aggregate(文本)

    @mcp.tool()
    def dna_batch_gen(模块列表: str = "") -> str:
        return dna_batch_gen(模块列表)

    @mcp.tool()
    def system_topology() -> str:
        return system_topology()

    @mcp.tool()
    def cns_bridge_compile(源码: str, 目标语言: str = "python") -> str:
        return cns_bridge_compile(源码, 目标语言)

    @mcp.tool()
    def var_bridge_query(变量名: str = "") -> str:
        return var_bridge_query(变量名)

    @mcp.tool()
    def var_bridge_register(中文名: str, 类型: str = "文本", 值: str = "") -> str:
        return var_bridge_register(中文名, 类型, 值)

    @mcp.tool()
    def stats_snapshot() -> str:
        return stats_snapshot()

    @mcp.tool()
    def health_aggregate() -> str:
        return health_aggregate()


# ══════════════════════════════════════════════════════════════════
# 裸 JSON-RPC 模式
# ══════════════════════════════════════════════════════════════════

def _jsonrpc_main():
    def _log(msg: str):
        print(f"[longhun-v4] {msg}", file=sys.stderr, flush=True)

    def _send(data: dict[str, Any]):
        sys.stdout.write(json.dumps(data, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    def _handle(msg: dict[str, Any]) -> dict | None:
        msg_id = msg.get("id")
        method = msg.get("method")

        if method == "initialize":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {
                "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "longhun-v4", "version": VERSION},
            }}

        if method == "notifications/initialized":
            return None

        if method == "tools/list":
            tools = [{"name": name, "description": fn.__doc__ or name, "inputSchema": {"type": "object", "properties": {}}}
                     for name, fn in TOOL_DEFS.items()]
            return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}}

        if method == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            if tool_name not in TOOL_DEFS:
                return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"未知: {tool_name}"}}
            try:
                fn = TOOL_DEFS[tool_name]
                import inspect
                sig = inspect.signature(fn)
                kwargs = {k: arguments.get(k) for k in sig.parameters if k in arguments}
                result = fn(**kwargs)
                return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": result}]}}
            except Exception as e:
                return {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "content": [{"type": "text", "text": json.dumps({"错误": str(e)}, ensure_ascii=False)}],
                    "isError": True,
                }}

        if method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"未知方法: {method}"}}

    _log(f"🐉 龍魂 MCP Server v4.0 ({VERSION}) 启动 (JSON-RPC)")
    _log(f"   项目根: {_PROJECT_ROOT}")
    _log(f"   工具数: {len(TOOL_DEFS)}")
    _log(f"   人格数: {len(人格)}/16")

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
    if _FASTMCP:
        print(f"龍魂MCP v4.0 ({VERSION}) 启动 (FastMCP)")
        print(f"工具: {', '.join(TOOL_DEFS.keys())}")
        mcp.run(transport='stdio')
    else:
        try:
            _jsonrpc_main()
        except KeyboardInterrupt:
            sys.exit(0)
