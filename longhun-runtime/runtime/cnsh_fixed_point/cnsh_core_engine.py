from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from typing import Any

from runtime.cnsh_fixed_point.fixed_points import FIXED_POINTS


def calculate_dr(text: str) -> int:
    digits = [int(ch) for ch in text if ch.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    while total >= 10:
        total = sum(int(ch) for ch in str(total))
    return total


def sha256_short(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length].upper()


def generate_dna(text: str, label: str = "INPUT") -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    digest = sha256_short(text, 8)
    return f"#龍芯⚡️{ts}-{label}-{digest}"


def generate_fuse_dna(dr: int, seq: str = "0001") -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    return f"#龍芯⚡️{ts}-FUSE-dr{dr}-{seq}"


def gate_check(dr: int) -> dict[str, Any]:
    if dr in set(FIXED_POINTS.fuse_digit_roots):
        return {"color": "🔴", "pass": False, "msg": f"熔断 dr={dr}"}
    if dr == FIXED_POINTS.pending_digit_root:
        return {"color": "🟡", "pass": None, "msg": "待审 dr=6"}
    return {"color": "🟢", "pass": True, "msg": f"通行 dr={dr}"}


RED_WORDS = ["绕过P0", "删除规则", "关闭审计", "删除DNA", "出售数据", "泄露隐私", "伪造签章", "伪造GPG"]
YELLOW_WORDS = ["跨国", "批量", "未授权", "敏感", "外部接入", "大规模"]
OVERCLAIM = ["100%", "绝对", "一定", "必然", "肯定", "保证", "永远不会", "完全不可能", "毫无疑问", "稳赚"]


@dataclass(frozen=True)
class Drawer:
    id: int
    name: str
    element: str
    route: str
    state: str
    risk: str
    priority: int


DRAWERS = [
    Drawer(2, "DNA追溯", "水", "TRACE", "S1_DNA_BIND", "中", 80),
    Drawer(3, "规则铁律", "金", "RULE_CHECK", "S4_RULE_CONFIRM", "高", 100),
    Drawer(11, "落地执行", "木", "EXEC", "S6_EXECUTE", "中", 85),
    Drawer(12, "熔断保护", "金", "BREAK", "S8_BREAK_RECOVER", "极高", 100),
    Drawer(23, "测试验证", "木", "TEST", "S6_EXECUTE", "低", 60),
    Drawer(25, "审计校验", "金", "AUDIT", "S7_AUDIT_LOOP", "中", 90),
    Drawer(27, "禁忌否定", "金", "BLOCK", "S8_BREAK_RECOVER", "极高", 100),
    Drawer(33, "技术栈工具", "木", "TOOL_CALL", "S6_EXECUTE", "中", 70),
    Drawer(49, "冲突裁决", "金", "RESOLVE", "S4_RULE_CONFIRM", "高", 100),
    Drawer(53, "上下文记忆", "水", "CONTEXT", "S2_SEMANTIC_PARSE", "低", 80),
    Drawer(54, "优先级抢占", "木", "PRIORITY_OVERRIDE", "S3_ROUTE_DISPATCH", "中", 95),
    Drawer(55, "人格调度", "火", "PERSONA_SWITCH", "S3_ROUTE_DISPATCH", "低", 75),
]

KEYWORDS = {
    "dna": 2, "追溯": 2, "签名": 2, "gpg": 2,
    "规则": 3, "铁律": 3, "红线": 3,
    "落地": 11, "执行": 11, "跑起来": 11,
    "熔断": 12, "拦截": 12, "刹车": 12,
    "测试": 23, "验证": 23,
    "审计": 25, "校验": 25,
    "禁止": 27, "不许": 27, "不可": 27,
    "python": 33, "notion": 33, "mcp": 33,
    "冲突": 49, "裁决": 49,
    "上下文": 53, "记住": 53,
    "优先": 54, "先做": 54,
    "宝宝": 55, "切人格": 55,
}

DRAWER_MAP = {d.id: d for d in DRAWERS}
RISK_RANK = {"低": 1, "中": 2, "高": 3, "极高": 4}
CONTROL = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}


def rule_check(text: str) -> dict[str, str]:
    for w in RED_WORDS:
        if w in text:
            return {"color": "🔴", "reason": f"命中红线:{w}"}
    for w in YELLOW_WORDS:
        if w in text:
            return {"color": "🟡", "reason": f"命中黄线:{w}"}
    return {"color": "🟢", "reason": "规则通过"}


def truth_check(text: str) -> dict[str, str]:
    for w in OVERCLAIM:
        if w in text:
            return {"color": "🔴", "reason": f"说满话:{w}"}
    return {"color": "🟢", "reason": "表达克制"}


def data_check(meta: dict[str, Any]) -> dict[str, str]:
    missing = [k for k in ["dna", "operator", "source"] if not meta.get(k)]
    if missing:
        return {"color": "🟡", "reason": f"缺少:{','.join(missing)}"}
    return {"color": "🟢", "reason": "追溯完整"}


def merge_color(colors: list[str]) -> str:
    if "🔴" in colors:
        return "🔴"
    if "🟡" in colors:
        return "🟡"
    return "🟢"


def detect_drawers(text: str) -> list[Drawer]:
    lower = text.lower()
    ids = {did for kw, did in KEYWORDS.items() if kw in lower}
    return sorted([DRAWER_MAP[i] for i in ids if i in DRAWER_MAP], key=lambda x: x.priority, reverse=True)


def element_relation(elements: list[str]) -> str:
    unique = list(dict.fromkeys(elements))
    if len(unique) <= 1:
        return "比和"
    for a in unique:
        for b in unique:
            if a != b and CONTROL.get(a) == b:
                return f"相克:{a}克{b}"
    return "混合"


def process_cnsh(text: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    meta = metadata or {}
    dna = meta.get("dna") or generate_dna(text)
    meta.setdefault("dna", dna)
    meta.setdefault("operator", "UID9622")
    meta.setdefault("source", "manual_input")

    dr = calculate_dr(text)
    gate = gate_check(dr)

    if gate["pass"] is False:
        return {
            "input": text,
            "dna": dna,
            "fuse_dna": generate_fuse_dna(dr),
            "dr": dr,
            "gate_color": "🔴",
            "state": "S8_BREAK_RECOVER",
            "route": "BREAK",
            "audit_color": "🔴",
        }

    c1 = rule_check(text)
    c2 = truth_check(text)
    c3 = data_check(meta)
    triple = merge_color([c1["color"], c2["color"], c3["color"]])

    drawers = detect_drawers(text)
    elems = [d.element for d in drawers]
    relation = element_relation(elems)
    risk = max([d.risk for d in drawers], key=lambda r: RISK_RANK[r]) if drawers else "低"

    if triple == "🔴" or risk == "极高":
        state, route, audit = "S8_BREAK_RECOVER", "BREAK", "🔴"
    elif relation.startswith("相克") or risk == "高":
        state, route, audit = "S4_RULE_CONFIRM", "RESOLVE", "🟠"
    elif drawers:
        state, route, audit = drawers[0].state, drawers[0].route, "🟡" if risk == "中" else "🟢"
    else:
        state, route, audit = "S2_SEMANTIC_PARSE", "PARSE", "🟢"

    return {
        "input": text,
        "dna": dna,
        "input_hash": sha256_short(text),
        "dr": dr,
        "gate_color": gate["color"],
        "triple_check_color": triple,
        "drawers": [f"{d.id}-{d.name}" for d in drawers],
        "elements": elems,
        "element_relation": relation,
        "risk_level": risk,
        "audit_color": audit,
        "state": state,
        "route": route,
        "fixed_points": {
            "dna": FIXED_POINTS.dna,
            "confirm": FIXED_POINTS.confirm,
            "gpg": FIXED_POINTS.gpg,
        },
    }
