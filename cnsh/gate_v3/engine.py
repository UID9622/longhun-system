# -*- coding: utf-8 -*-
"""
龍魂·第一道闸门融合引擎 v3.0（Python 实装）
DNA: #龍芯⚡️2026-04-26-第一道闸门-融合引擎-v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

GATE_DNA = "#龍芯⚡️2026-04-26-第一道闸门-三色审计-沙盒闭环-v3.0"
CONFIRM_REQUIRED = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_REQUIRED = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_REQUIRED = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
OWNER_START_AGE = 37  # dr(37)=1 启动数·人生锚（非网关密码）

DNA_PATTERNS = [
    re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-.+"),
    re.compile(r"#ZHUGEXIN⚡️\d{4}-\d{2}-\d{2}-.+"),
    re.compile(r"#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"),
]
L0_SIGNATURES = [SEAL_REQUIRED, CONFIRM_REQUIRED]

RED_RULES: Dict[str, List[str]] = {
    "修改双签章": ["修改双签章", "改确认码", "替换签章", "篡改签章"],
    "绕过P0": ["绕过P0", "关闭审计", "删除规则", "跳过闸门"],
    "删除DNA": ["删除DNA", "去掉追溯", "不留痕"],
    "隐私导出": ["导出隐私", "未授权数据", "用户画像"],
    "金融推演": ["股票预测", "K线", "交易策略", "保证赚钱"],
}
YELLOW_RULES: Dict[str, List[str]] = {
    "来源不清": ["据说", "好像", "可能来自", "不确定"],
    "边界不明": ["随便用", "都可以", "不限范围"],
}
FULL_RED = ["100%", "绝对", "一定", "必然", "保证", "永远不会", "完全不可能", "毫无疑问"]
FULL_YELLOW = ["基本确定", "稳了", "应该没问题", "不会翻车"]
RISK_AVOID = ["避开", "规避", "降低风险", "未发现明显风险", "建议", "待审", "如果你认为"]


def digital_root_from_text(text: str) -> int:
    digits = [int(c) for c in text if c in "0123456789"]
    if not digits:
        return 0
    total = sum(digits)
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total


def gate_color(dr: int) -> str:
    if dr in {3, 9}:
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


def has_dna(text: str) -> bool:
    markers = ("#龍芯", "#ZHUGEXIN", "#CONFIRM", "GPG", "DNA追溯", "确认码")
    return any(m in text for m in markers)


def validate_dna(text: str) -> Dict[str, Any]:
    if any(sig in text for sig in L0_SIGNATURES):
        return {"status": "L0合法", "color": "🟢", "reason": "L0不动点签章"}
    if not has_dna(text):
        return {"status": "缺失", "color": "🟡", "reason": "未检测到DNA·将生成临时L4"}
    for pat in DNA_PATTERNS:
        if pat.search(text):
            return {"status": "合法", "color": "🟢", "reason": "DNA格式合法"}
    if has_dna(text):
        return {"status": "疑似伪造", "color": "🔴", "reason": "DNA标记但格式不合法"}
    return {"status": "无", "color": "🟢", "reason": "普通内容"}


def generate_l4_dna(text: str, prefix: str = "GATE") -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now}-{prefix}-L4-{digest}"


def rule_check(text: str) -> Dict[str, Any]:
    for reason, kws in RED_RULES.items():
        for kw in kws:
            if kw in text:
                return {"color": "🔴", "reason": reason, "keyword": kw}
    for reason, kws in YELLOW_RULES.items():
        for kw in kws:
            if kw in text:
                return {"color": "🟡", "reason": reason, "keyword": kw}
    return {"color": "🟢", "reason": "未触发红线/黄线", "keyword": None}


def falsehood_check(text: str, evidence: str = "") -> Dict[str, Any]:
    for w in FULL_RED:
        if w in text:
            return {"color": "🔴", "reason": "说得太满", "keyword": w}
    for w in FULL_YELLOW:
        if w in text:
            return {"color": "🟡", "reason": "过度确定", "keyword": w}
    if len((evidence or "").strip()) < 10 and not any(w in text for w in RISK_AVOID):
        return {"color": "🟡", "reason": "依据不足", "keyword": None}
    return {"color": "🟢", "reason": "表达合格", "keyword": None}


def data_guard_check(meta: Dict[str, Any]) -> Dict[str, Any]:
    required = ["dna", "timestamp", "operator", "source"]
    missing = [k for k in required if not meta.get(k)]
    if "dna" in missing:
        return {"color": "🔴", "reason": "缺DNA", "missing": missing}
    if "operator" in missing or "source" in missing:
        return {"color": "🟡", "reason": "追溯不全", "missing": missing}
    return {"color": "🟢", "reason": "追溯完整", "missing": []}


def overall_color(colors: List[str]) -> str:
    if "🔴" in colors:
        return "🔴"
    if "🟡" in colors:
        return "🟡"
    return "🟢"


@dataclass
class GateDecision:
    input_text: str
    digital_root: int
    gate_color_dr: str
    audit_color: str
    dna: str
    state: str
    route: str
    bucket: str
    decision: str
    execute_allowed: bool
    notify_level: str  # passive | active | none
    hold_for_audit: bool
    meta: Dict[str, Any] = field(default_factory=dict)


def decide(
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
    evidence: str = "",
    *,
    auto_execute: bool = False,
) -> GateDecision:
    """
    第一道闸门总决策。
    铁律：🟢 才允许 execute_allowed=True；🟡/🔴 默认不执行，等审计。
  auto_execute=True 且 🟢 时方可与旧逻辑合并放行（仍建议人工开关）。
    """
    metadata = metadata or {}
    dr = digital_root_from_text(text)
    g = gate_color(dr)
    dna_check = validate_dna(text)
    dna = str(metadata.get("dna") or "")
    if not dna and dna_check["status"] == "缺失":
        dna = generate_l4_dna(text)

    base_meta = {
        "gate_dna": GATE_DNA,
        "owner_start_age": OWNER_START_AGE,
        "dr_semantic": "启动数" if dr == 1 else ("待审数" if dr == 6 else ""),
    }

    def _blocked(decision: str, state: str, route: str, bucket: str, audit: str, notify: str) -> GateDecision:
        return GateDecision(
            input_text=text[:500],
            digital_root=dr,
            gate_color_dr=g,
            audit_color=audit,
            dna=dna or generate_l4_dna(text, prefix="FUSE"),
            state=state,
            route=route,
            bucket=bucket,
            decision=decision,
            execute_allowed=False,
            notify_level=notify,
            hold_for_audit=True,
            meta={**base_meta, "dna_check": dna_check},
        )

    if g == "🔴":
        return _blocked(
            f"【熔断】dr={dr}·拒绝进入主系统·证据已记",
            "S8_BREAK_RECOVER",
            "BREAK",
            "🔴 熔断封存",
            "🔴",
            "active",
        )

    if dna_check["color"] == "🔴":
        return _blocked(
            "疑似伪造DNA·熔断封存",
            "S8_BREAK_RECOVER",
            "BREAK",
            "🔴 熔断封存",
            "🔴",
            "active",
        )

    if g == "🟡":
        timeout = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        return GateDecision(
            input_text=text[:500],
            digital_root=dr,
            gate_color_dr=g,
            audit_color="🟡",
            dna=dna,
            state="S4_RULE_CONFIRM",
            route="WAIT_REVIEW",
            bucket="🔁 待迭代升级池",
            decision="【待审】请补充数据/来源/边界·5分钟超时转熔断",
            execute_allowed=False,
            notify_level="active",
            hold_for_audit=True,
            meta={**base_meta, "dna_check": dna_check, "timeout_at": timeout},
        )

    r1 = rule_check(text)
    r2 = falsehood_check(text, evidence=evidence)
    meta_row = {
        "dna": dna,
        "timestamp": metadata.get("timestamp")
        or datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds"),
        "operator": metadata.get("operator") or metadata.get("operator_id") or "UID9622",
        "source": metadata.get("source") or metadata.get("channel") or "flow_port",
    }
    r3 = data_guard_check(meta_row)
    audit = overall_color([r1["color"], r2["color"], r3["color"]])

    if audit == "🔴":
        return _blocked(
            "三重检测红线·熔断封存",
            "S8_BREAK_RECOVER",
            "BREAK",
            "🔴 熔断封存",
            "🔴",
            "active",
        )

    if audit == "🟡":
        return GateDecision(
            input_text=text[:500],
            digital_root=dr,
            gate_color_dr=g,
            audit_color="🟡",
            dna=dna,
            state="S4_RULE_CONFIRM",
            route="NEED_CONFIRM",
            bucket="🔁 待迭代升级池",
            decision="三重检测待确认·暂不执行·等审计拍板",
            execute_allowed=False,
            notify_level="active",
            hold_for_audit=True,
            meta={
                **base_meta,
                "rule_check": r1,
                "falsehood_check": r2,
                "data_guard": r3,
            },
        )

    # 🟢 通过闸门 — 默认仍不自动执行，除非显式 auto_execute
    allow = bool(auto_execute)
    return GateDecision(
        input_text=text[:500],
        digital_root=dr,
        gate_color_dr=g,
        audit_color="🟢",
        dna=dna,
        state="S6_EXECUTE" if allow else "S2_SEMANTIC_PARSE",
        route="EXEC" if allow else "PARSE",
        bucket="📦 入库/封装" if allow else "⚡ 内部消化",
        decision="通过第一道闸门·可进入流场" + ("·已授权执行" if allow else "·默认仅审计不执行"),
        execute_allowed=allow,
        notify_level="passive",
        hold_for_audit=not allow,
        meta={
            **base_meta,
            "rule_check": r1,
            "falsehood_check": r2,
            "data_guard": r3,
            "dna_check": dna_check,
        },
    )
