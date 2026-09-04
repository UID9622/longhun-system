#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-LONGHUN-KUNPENG-MCP-AUDIT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 鲲鹏 MCP Server · 审计层 lh-mcp-audit v1.0（端口 8764）
================================================================
对外暴露龍魂系统的审计能力（三色审计/耻辱墙/DNA 校验/审计日志）。

MCP Resources:
  resource://shamewall/latest  最新 10 条耻辱墙记录
  resource://audit/rules       三色审计规则集

MCP Tools:
  audit_text(text)            对文本执行三色审计 → 🟢/🟡/🔴
  scan_shamewall(keyword)     耻辱墙关键词检索
  verify_dna(dna)             DNA 追溯码格式/哈希校验
  get_audit_logs(start,end)   审计日志检索（时间过滤）
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_mcp_core import (  # noqa: E402
    MCPServer, MCPError, ERR_INVALID_PARAMS, now_iso, run_from_cli,
)

SERVER_NAME = "lh-mcp-audit"
VERSION = "1.0.0"
DEFAULT_PORT = 8764

DEFAULT_CFG = {
    "server": SERVER_NAME,
    "port": DEFAULT_PORT,
    "host": "127.0.0.1",
    "auth": {"mode": "none"},
    "log_dir": "~/.longhun/logs/mcp",
    "lh_root": "",
    "peer_allowlist": [],
    "shamewall_file": "~/.longhun/shame_wall/shame_wall.json",
    "audit_log_dir": "~/.longhun/logs/mcp",
}

SHAMEWALL_HINT = ("~/.longhun/shame_wall/shame_wall.json · 由 lh judge 生成；"
                  "若未运行过 judge 则文件不存在 → 返回空清单")

# ── 三色审计规则集（对齐 对齐规则v2.x 第10层一票否决词 + 第11层禁止场景）──
AUDIT_RULES = {
    "version": "LH-AUDIT-RULES-v1.0",
    "verdicts": {"red": "🔴 红线(禁止场景/P0 触碰·拒绝执行)", "yellow": "🟡 警示(一票否决词·需审计复核)", "green": "🟢 通过"},
    "red_keywords": [
        "伪造DNA", "私钥外传", "海外部署内核", "诱导上传", "暗中收集", "删除审计日志",
        "删除日志", "清除水印", "洗来源", "绕过审计", "无授权集成", "对外渗透",
        "背叛人民", "收买", "出卖用户数据", "数据出境", "伪造身份", "隐藏后门",
        "阻止审计", "绕过熔断",
    ],
    "yellow_keywords": [
        "技术无国界", "用户体验优先", "灵活处理", "国际接轨", "简化管理",
        "商业化需要", "平衡各方", "行业标准",
    ],
    "source": "LH-CODEBUDDY-ALIGNMENT-RULES-v2.x 第十层一票否决词/第十一层禁止场景 · "
              "LH-PERSONA-GOVERNANCE-WHITEPAPER v1.4 第三层三色审计",
}


def _load_shamewall() -> dict:
    p = Path(DEFAULT_CFG["shamewall_file"]).expanduser()
    if not p.exists():
        return {"exists": False, "records": [], "hint": SHAMEWALL_HINT}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"exists": True, "error": str(exc), "records": []}
    if isinstance(data, list):
        return {"exists": True, "records": data}
    if isinstance(data, dict):
        for k in ("records", "entries", "items", "data"):
            if isinstance(data.get(k), list):
                return {"exists": True, "records": data[k], "meta": {x: y for x, y in data.items() if x != k}}
    return {"exists": True, "records": [], "raw_type": type(data).__name__}


def _flatten(rec: dict) -> str:
    parts = []
    if isinstance(rec, dict):
        for v in rec.values():
            if isinstance(v, (str, int, float)):
                parts.append(str(v))
            elif isinstance(v, list):
                parts.extend(str(x) for x in v)
    else:
        parts.append(str(rec))
    return " ".join(parts)


# ═══════════════════════════════════════════════════════════════
# 工具实现
# ═══════════════════════════════════════════════════════════════

def _tool_audit_text(args: dict) -> dict:
    """对文本执行三色审计：命中红线词 → 🔴；命中一票否决词 → 🟡；否则 🟢"""
    text = str(args.get("text") or "").strip()
    if not text:
        raise MCPError(ERR_INVALID_PARAMS, "text 不能为空")
    hits_red = [k for k in AUDIT_RULES["red_keywords"] if k in text]
    hits_yellow = [k for k in AUDIT_RULES["yellow_keywords"] if k in text]
    if hits_red:
        verdict = "🔴"
        reason = "命中禁止场景/红线词"
    elif hits_yellow:
        verdict = "🟡"
        reason = "命中一票否决词（需复核）"
    else:
        verdict = "🟢"
        reason = "无红线/警示词命中"
    return {
        "verdict": verdict,
        "reason": reason,
        "matched": {"red": hits_red, "yellow": hits_yellow},
        "rules_version": AUDIT_RULES["version"],
        "audited_at": now_iso(),
    }


def _tool_scan_shamewall(args: dict) -> dict:
    """耻辱墙关键词检索（大小写不敏感；最多 20 条）"""
    kw = str(args.get("keyword") or "").strip().lower()
    wall = _load_shamewall()
    if not wall.get("exists"):
        return wall
    recs = wall["records"]
    if kw:
        recs = [r for r in recs if kw in _flatten(r).lower()]
    return {"exists": True, "keyword": kw, "total": len(recs),
            "records": recs[:20]}


_DNA_RE_HEAD = re.compile(r"^#龍芯⚡️")
_DNA_RE_HASH = re.compile(r"([0-9A-F]{8})$")
_GAN = "甲乙丙丁戊己庚辛壬癸"
_ZHI = "子丑寅卯辰巳午未申酉戌亥"
_GUA = "乾坤屯蒙需讼师比小畜履泰否同人大有谦豫随蛊临观噬嗑贲剥复无妄大畜颐大过坎离咸恒遁大壮晋明夷家人睽蹇解损益夬姤萃升困井革鼎震艮渐归妹丰旅巽兑涣节中孚小过既济未济"


def _digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def _wx_of_root(n: int) -> str:
    return {0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
            5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}.get(n, "?")


def _tool_verify_dna(args: dict) -> dict:
    """DNA 追溯码轻量校验：前缀/干支或日期时间戳/卦名/哈希8/数字根五行"""
    dna = str(args.get("dna") or "").strip()
    if not dna:
        raise MCPError(ERR_INVALID_PARAMS, "dna 不能为空")
    if not _DNA_RE_HEAD.match(dna):
        return {"valid": False, "verdict": "🔴", "reason": "缺少前缀 #龍芯⚡️",
                "digital_root": None, "wuxing": None}
    if len(dna) > 300 or any(ch in dna for ch in ("\n", "\r", "\t")):
        return {"valid": False, "verdict": "🔴", "reason": "长度超限或含控制字符"}
    body = dna[len("#龍芯⚡️"):]
    m = _DNA_RE_HASH.search(body)
    if not m:
        return {"valid": False, "verdict": "🔴",
                "reason": "缺少尾部 8 位大写哈希(hex)段"}
    tail = m.group(1)
    parts = body[:-9].split("-")  # 去掉 -HASH8
    stamp = parts[0] if parts else ""
    has_gan = any(c in _GAN for c in stamp)
    has_zhi = any(c in _ZHI for c in stamp)
    has_date = bool(re.search(r"20\d{2}[01]\d[0-3]\d", stamp))
    has_gua = any(g in stamp for g in _GUA)
    stamp_ok = has_gan and has_zhi or has_date
    module_ok = len(parts) >= 2
    dr = _digital_root(sum(int(c, 16) for c in tail))
    return {
        "valid": stamp_ok and module_ok and tail.isalnum(),
        "verdict": "🟢" if (stamp_ok and module_ok) else "🟡",
        "reason": (f"时间戳{'干支/日期✅' if stamp_ok else '缺失⚠️'} · "
                   f"卦名{'✅' if has_gua else '（可选缺省）'} · "
                   f"模块动作{'✅' if module_ok else '缺失⚠️'} · 哈希尾 {tail}"),
        "parsed": {"stamp": stamp, "module": parts[1] if len(parts) > 1 else "",
                   "action": "-".join(parts[2:]) if len(parts) > 2 else "",
                   "hash8": tail,
                   "has_ganzhi": has_gan and has_zhi, "has_date": has_date,
                   "has_gua": has_gua},
        "digital_root": dr,
        "wuxing": _wx_of_root(dr),
    }


def _load_audit_logs() -> list:
    """合并读取审计 JSONL（本组三 server 的操作审计 + admin 专用日志）"""
    out = []
    d = Path(DEFAULT_CFG["audit_log_dir"]).expanduser()
    if d.is_dir():
        for f in sorted(d.glob("*.jsonl")):
            try:
                for line in f.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        rec["_src"] = f.name
                        out.append(rec)
                    except Exception:
                        pass
            except Exception:
                pass
    ap = Path("~/.longhun/audit/admin_operations.log").expanduser()
    if ap.exists():
        for line in ap.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append({"ts": line.split(" | ", 1)[0],
                            "admin_log": line, "_src": ap.name})
            except Exception:
                pass
    return out


def _ts_of(rec: dict):
    ts = rec.get("ts", "")
    if isinstance(ts, (int, float)):
        ts = datetime.fromtimestamp(ts).isoformat()
    return str(ts)


def _tool_get_audit_logs(args: dict) -> dict:
    """检索审计日志（start/end ISO 时间过滤·最多 200 条）"""
    start = str(args.get("start") or "").strip()
    end = str(args.get("end") or "").strip()
    logs = _load_audit_logs()
    if start:
        logs = [r for r in logs if _ts_of(r) >= start]
    if end:
        logs = [r for r in logs if _ts_of(r) <= end]
    logs.sort(key=_ts_of, reverse=True)
    return {"total_found": len(logs), "returned": len(logs[:200]),
            "filter": {"start": start or None, "end": end or None},
            "logs": logs[:200]}


# ═══════════════════════════════════════════════════════════════
# 资源实现
# ═══════════════════════════════════════════════════════════════

def _res_shamewall_latest(uri: str) -> dict:
    wall = _load_shamewall()
    if not wall.get("exists"):
        return wall
    return {"exists": True, "latest": wall["records"][:10]}


def _res_audit_rules(uri: str) -> dict:
    return AUDIT_RULES


def build_server() -> MCPServer:
    srv = MCPServer(SERVER_NAME, VERSION, DEFAULT_CFG)
    srv.add_tool("audit_text",
                 "对文本执行龍魂三色审计 → 🟢/🟡/🔴 + 命中词（红线词=禁止场景，警示词=一票否决词）",
                 {"type": "object",
                  "properties": {"text": {"type": "string",
                                          "description": "待审计文本（代码/文案/方案描述）"}},
                  "required": ["text"]},
                 _tool_audit_text)
    srv.add_tool("scan_shamewall",
                 "在耻辱墙中按关键词检索（大小写不敏感·返回 ≤20 条）",
                 {"type": "object",
                  "properties": {"keyword": {"type": "string",
                                             "description": "检索关键词(可留空=全部)"}}},
                 _tool_scan_shamewall)
    srv.add_tool("verify_dna",
                 "验证 DNA 追溯码：#龍芯⚡️前缀 + 干支/日期时间戳 + 卦名 + 模块-动作 + 8位哈希；附数字根五行",
                 {"type": "object",
                  "properties": {"dna": {"type": "string", "description": "DNA 追溯码"}},
                  "required": ["dna"]},
                 _tool_verify_dna)
    srv.add_tool("get_audit_logs",
                 "检索审计日志（start/end ISO8601 时间过滤；缺省=最近）",
                 {"type": "object",
                  "properties": {"start": {"type": "string", "description": "起始 ISO 时间 可选"},
                                 "end": {"type": "string", "description": "结束 ISO 时间 可选"}}},
                 _tool_get_audit_logs)
    srv.add_resource("resource://shamewall/latest", "耻辱墙·最新",
                     "最新 10 条耻辱墙记录", _res_shamewall_latest)
    srv.add_resource("resource://audit/rules", "三色审计规则集",
                     "红线词/警示词/判定规则与出处", _res_audit_rules)
    return srv


if __name__ == "__main__":
    sys.exit(run_from_cli(build_server(), SERVER_NAME, DEFAULT_PORT, DEFAULT_CFG))
