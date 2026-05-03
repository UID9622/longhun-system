#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·第一道闸门融合引擎 v1.0（整合版·清洗版）

DNA: #龍芯⚡️2026-04-26-GATE-ENGINE-INTEGRATED-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者：龍芯北辰｜UID9622
理论指导：曾仕强老師（永恒显示）
献给：诸葛鑫·UID9622·龍芯北辰

来源整合：
  Feed⑤ v3.0  数字根熔断 + DNA校验 + 三重检测 + 总决策骨架（decide）
  Feed③ v2.0  五行相生相克 + 关键词→抽屉映射
  Feed② v1.0  55抽屉登记 + 8语义区
  Feed④ v1.2  六维评估 + 五桶分拣

清洗：原投喂里被 Notion markdown 自动加链的标识符已全部还原
  [main.py](http://main.py)         → main.py
  [h.name](http://h.name)           → h.name
  [datetime.now](http://datetime.now)() → datetime.now()
  [re.search](http://re.search)     → re.search
  [callback.py](http://callback.py) → callback.py

与本地现有模块的关系（不重复造轮子）：
  - 红线/黄线/owner_vent  → 沿用 bin/circuit_breaker.py v3.0
  - DNA 链 append-only    → 沿用 bin/dna_append_log.py v1.0
  本引擎只补 Feed⑤ 独有的：数字根熔断 + DNA格式校验 + 虚伪编译器 + 数据守护
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import hashlib
import re

# ============================================================
# 常量
# ============================================================
OWNER_UID    = "9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_PREFIX   = "#龍芯⚡️"

L0_SIGNATURES = [
    "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    CONFIRM_CODE,
]

DNA_PATTERNS = [
    r"#龍芯⚡️\d{4}-\d{2}-\d{2}-.+",
    r"#ZHUGEXIN⚡️\d{4}-\d{2}-\d{2}-.+",
    r"#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
]

DNA_MARKERS = ["#龍芯", "#ZHUGEXIN", "#CONFIRM", "GPG", "DNA"]

相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}


# ============================================================
# 第1层：数字根（洛书 369 不动点）
# ============================================================
def digital_root_from_text(text: str) -> int:
    """
    dr(n) = 1 + ((n - 1) mod 9)
    实现：抽出全部数字字符 → 累加 → 反复压缩到 1-9
    无数字 → 0
    """
    digits = [int(c) for c in text if c.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total


def gate_color(dr: int) -> str:
    """3/9 红 · 6 黄 · 其余绿（含 0）"""
    if dr in {3, 9}:
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


# ============================================================
# 第2层：DNA 格式校验
# ============================================================
def has_dna(text: str) -> bool:
    return any(marker in text for marker in DNA_MARKERS)


def validate_dna(text: str) -> Dict:
    if not has_dna(text):
        return {
            "status": "缺失",
            "color":  "🟡",
            "reason": "未检测到DNA，需生成临时L4 DNA",
        }
    for sig in L0_SIGNATURES:
        if sig in text:
            return {
                "status": "L0合法",
                "color":  "🟢",
                "reason": "检测到L0不动点签章",
            }
    for pattern in DNA_PATTERNS:
        if re.search(pattern, text):
            return {
                "status": "合法",
                "color":  "🟢",
                "reason": "DNA格式合法",
            }
    return {
        "status": "疑似伪造",
        "color":  "🔴",
        "reason": "检测到DNA标记但格式不合法",
    }


def generate_l4_dna(text: str, prefix: str = "GATE") -> str:
    now    = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{now}-{prefix}-L4-{digest}"


# ============================================================
# 第3层：三重检测（规则·虚伪·数据守护）
# ============================================================
RED_RULES = {
    "修改双签章":     ["修改双签章", "改确认码", "替换签章"],
    "绕过P0":         ["绕过P0", "关闭审计", "删除规则"],
    "删除DNA":        ["删除DNA", "去掉追溯", "不留痕"],
    "隐私导出":       ["导出隐私", "未授权数据", "用户画像"],
    "金融推演":       ["股票预测", "K线", "交易策略", "保证赚钱"],
    "数据画像":       ["行为预测", "画像分析", "监控用户"],
    "非法跨境":       ["强制上传境外", "绕过数据主权"],
}

YELLOW_RULES = {
    "来源不清":   ["据说", "好像", "可能来自"],
    "边界不明":   ["随便用", "都可以", "不限范围"],
    "外部接入":   ["接入第三方", "跨平台调用", "批量导出"],
}

FULL_WORDS_RED = [
    "100%", "绝对", "一定", "必然", "保证",
    "永远不会", "完全不可能", "毫无疑问",
]

FULL_WORDS_YELLOW = [
    "基本确定", "稳了", "应该没问题", "不会翻车", "可以确保",
]

RISK_AVOID_WORDS = [
    "避开", "规避", "降低风险",
    "未发现明显风险", "建议", "待审",
]


def rule_check(text: str) -> Dict:
    for reason, kws in RED_RULES.items():
        for kw in kws:
            if kw in text:
                return {"color": "🔴", "reason": reason, "keyword": kw}
    for reason, kws in YELLOW_RULES.items():
        for kw in kws:
            if kw in text:
                return {"color": "🟡", "reason": reason, "keyword": kw}
    return {"color": "🟢", "reason": "未触发红线/黄线", "keyword": None}


def falsehood_check(text: str, evidence: str = "") -> Dict:
    """虚伪编译器：抓 100%/绝对/一定 一类的"说满话"。"""
    for word in FULL_WORDS_RED:
        if word in text:
            return {
                "color":      "🔴",
                "reason":     "说得太满",
                "keyword":    word,
                "suggestion": "改为避开风险的表达",
            }
    for word in FULL_WORDS_YELLOW:
        if word in text:
            return {
                "color":      "🟡",
                "reason":     "表达过度确定",
                "keyword":    word,
                "suggestion": "降低确定性，补充依据",
            }
    if len(evidence.strip()) < 10 and not any(w in text for w in RISK_AVOID_WORDS):
        return {
            "color":      "🟡",
            "reason":     "依据不足",
            "keyword":    None,
            "suggestion": "补充数据来源、分析方法、时间范围",
        }
    return {
        "color":      "🟢",
        "reason":     "表达合格",
        "keyword":    None,
        "suggestion": "可进入下一重检测",
    }


def data_guard_check(metadata: Dict) -> Dict:
    """数据守护：DNA / 时间戳 / 操作人 / 来源 必须齐全。"""
    required = ["dna", "timestamp", "operator", "source"]
    missing  = [k for k in required if not metadata.get(k)]
    if "dna" in missing:
        return {"color": "🔴", "reason": "缺少DNA追溯码", "missing": missing}
    if "operator" in missing or "source" in missing:
        return {"color": "🟡", "reason": "追溯信息不完整", "missing": missing}
    return {"color": "🟢", "reason": "追溯信息完整", "missing": []}


# ============================================================
# 第4层：抽屉×五行（55 抽屉浓缩为路由表）
# ============================================================
@dataclass
class DrawerRule:
    drawer_id: int
    name:      str
    element:   str
    route:     str
    state:     str
    engine:    str
    risk:      str
    priority:  int


# 注：完整 55 抽屉登记表见 01_drawer_registry.yaml
# 这里只列影响路由判定的高优先级抽屉
DRAWERS: List[DrawerRule] = [
    DrawerRule( 1, "沟通翻译",       "火", "PARSE",             "S2", "Semantic Engine",  "低",  50),
    DrawerRule( 2, "DNA追溯",        "水", "TRACE",             "S1", "DNA Engine",       "中",  80),
    DrawerRule( 3, "规则铁律",       "金", "RULE_CHECK",        "S4", "Rule Engine",      "高", 100),
    DrawerRule( 7, "Hook触发",       "木", "AUTO_TRIGGER",      "S3", "Hook Engine",      "中",  80),
    DrawerRule(11, "落地执行",       "木", "EXEC",              "S6", "Execution Engine", "中",  85),
    DrawerRule(12, "熔断保护",       "金", "BREAK",             "S8", "Safety Engine",    "极高", 100),
    DrawerRule(16, "钧旨指令",       "金", "FORCE_CMD",         "S5", "Command Engine",   "中", 100),
    DrawerRule(23, "测试验证",       "木", "TEST",              "S6", "Test Engine",      "低",  60),
    DrawerRule(24, "闭环收口",       "土", "LOOP",              "S7", "Flow Engine",      "低",  60),
    DrawerRule(25, "审计校验",       "金", "AUDIT",             "S7", "Audit Engine",     "中",  90),
    DrawerRule(27, "禁忌否定",       "金", "BLOCK",             "S8", "Safety Engine",    "极高", 100),
    DrawerRule(33, "技术栈工具",     "木", "TOOL_CALL",         "S6", "Tool Engine",      "中",  70),
    DrawerRule(49, "冲突裁决",       "金", "RESOLVE",           "S4", "Decision Engine",  "高", 100),
    DrawerRule(50, "时间调度",       "土", "SCHEDULE",          "S3", "Time Engine",      "低",  60),
    DrawerRule(51, "资源调度",       "土", "RESOURCE",          "S3", "Resource Engine",  "中",  70),
    DrawerRule(52, "回滚恢复",       "土", "RECOVER",           "S8", "Recovery Engine",  "中",  85),
    DrawerRule(53, "上下文记忆",     "水", "CONTEXT",           "S2", "Memory Engine",    "低",  80),
    DrawerRule(54, "优先级抢占",     "木", "PRIORITY_OVERRIDE", "S3", "Scheduler Engine", "中",  95),
    DrawerRule(55, "人格调度",       "火", "PERSONA_SWITCH",    "S3", "Persona Engine",   "低",  75),
]

KEYWORDS: Dict[str, int] = {
    "沟通": 1, "翻译": 1, "说人话": 1, "大白话": 1,
    "DNA": 2, "追溯": 2, "GPG": 2, "签名": 2, "水印": 2,
    "家法": 3, "红线": 3, "规则": 3, "铁律": 3, "不可动": 3,
    "hook": 7, "钩子": 7, "自动": 7, "触发": 7,
    "落地": 11, "执行": 11, "跑起来": 11, "搞": 11, "整": 11,
    "熔断": 12, "拦截": 12, "阻断": 12, "刹车": 12,
    "钧旨": 16, "指令": 16, "命令": 16, "老大说了": 16,
    "测试": 23, "验证": 23, "跑通": 23, "试试": 23,
    "闭环": 24, "收口": 24, "回流": 24, "一条龙": 24,
    "审计": 25, "校验": 25, "留痕": 25, "查": 25,
    "禁止": 27, "不许": 27, "不可": 27, "绝对不": 27,
    "Python": 33, "Notion": 33, "MCP": 33, "GitHub": 33,
    "冲突": 49, "裁决": 49, "谁优先": 49, "二选一": 49,
    "晚点": 50, "定时": 50, "稍后": 50, "明天": 50,
    "资源": 51, "并发": 51, "队列": 51, "限流": 51,
    "回滚": 52, "恢复": 52, "撤回": 52, "复原": 52,
    "上下文": 53, "刚刚": 53, "记住": 53, "语境": 53,
    "优先": 54, "插队": 54, "先做": 54, "立刻": 54,
    "宝宝": 55, "雯雯": 55, "诸葛": 55, "切人格": 55,
}


def detect_drawers(text: str) -> List[DrawerRule]:
    ids = set()
    lower = text.lower()
    for kw, did in KEYWORDS.items():
        if kw.lower() in lower:
            ids.add(did)
    hits = [d for d in DRAWERS if d.drawer_id in ids]
    hits.sort(key=lambda x: x.priority, reverse=True)
    return hits


def element_relation(elements: List[str]) -> str:
    unique = list(dict.fromkeys(elements))
    if not unique:
        return "无"
    if len(unique) == 1:
        return "比和"
    for a in unique:
        for b in unique:
            if a == b:
                continue
            if 相克.get(a) == b:
                return f"相克:{a}克{b}"
    for i in range(len(unique) - 1):
        if 相生.get(unique[i]) == unique[i + 1]:
            return f"相生:{unique[i]}生{unique[i + 1]}"
    return "混合"


# ============================================================
# 第5层：总决策（融合 5 层判定结果）
# ============================================================
def overall_color(colors: List[str]) -> str:
    if "🔴" in colors:
        return "🔴"
    if "🟡" in colors:
        return "🟡"
    return "🟢"


def decide(text: str, metadata: Optional[Dict] = None, evidence: str = "") -> Dict:
    """
    第一道闸门主决策入口。

    输入：
      text     ：原始输入文本
      metadata ：可选元数据 {dna, timestamp, operator, source}
      evidence ：可选依据正文（用于虚伪编译器）

    输出：标准 JSON-able dict，含
      input / digital_root / gate_color / dna / state / route /
      audit_color / bucket / decision / (规则/虚伪/数据守护三重结果)
    """
    metadata = metadata or {}

    # === 1. 数字根熔断（最优先）===
    dr      = digital_root_from_text(text)
    g_color = gate_color(dr)

    if g_color == "🔴":
        return {
            "input":         text,
            "digital_root":  dr,
            "gate_color":    g_color,
            "dna":           generate_l4_dna(text, prefix=f"FUSE-dr{dr}"),
            "state":         "S8_BREAK_RECOVER",
            "route":         "BREAK",
            "audit_color":   "🔴",
            "bucket":        "🔴 熔断封存",
            "decision":      f"【熔断】dr={dr}，拒绝回答。证据链哈希已记录。",
        }

    # === 2. DNA 格式校验 ===
    dna_check = validate_dna(text)
    if dna_check["color"] == "🔴":
        return {
            "input":        text,
            "digital_root": dr,
            "gate_color":   g_color,
            "dna_status":   dna_check,
            "dna":          generate_l4_dna(text, prefix="DNA-FAKE"),
            "state":        "S8_BREAK_RECOVER",
            "route":        "BREAK",
            "audit_color":  "🔴",
            "bucket":       "🔴 熔断封存",
            "decision":     "疑似伪造DNA，熔断封存。",
        }

    dna = (
        metadata.get("dna")
        or (generate_l4_dna(text) if dna_check["status"] == "缺失" else "见原文DNA")
    )

    # === 3. dr=6 待审 ===
    if g_color == "🟡":
        return {
            "input":        text,
            "digital_root": dr,
            "gate_color":   g_color,
            "dna":          dna,
            "state":        "S4_RULE_CONFIRM",
            "route":        "WAIT_REVIEW",
            "audit_color":  "🟡",
            "bucket":       "🔁 待迭代升级池",
            "timeout_at": (
                datetime.now(timezone.utc) + timedelta(minutes=5)
            ).isoformat(timespec="seconds"),
            "decision":     "【待审】请补充数据 / 来源 / 边界。",
        }

    # === 4. 三重检测 ===
    r1 = rule_check(text)
    r2 = falsehood_check(text, evidence=evidence)
    data_meta = {
        "dna":       dna,
        "timestamp": metadata.get("timestamp")
                     or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "operator":  metadata.get("operator") or f"UID{OWNER_UID}",
        "source":    metadata.get("source")   or "SandboxInput",
    }
    r3 = data_guard_check(data_meta)

    audit = overall_color([r1["color"], r2["color"], r3["color"]])

    if audit == "🔴":
        return {
            "input":           text,
            "digital_root":    dr,
            "gate_color":      g_color,
            "dna":             generate_l4_dna(text, prefix="TRI-RED"),
            "rule_check":      r1,
            "falsehood_check": r2,
            "data_guard":      r3,
            "state":           "S8_BREAK_RECOVER",
            "route":           "BREAK",
            "audit_color":     "🔴",
            "bucket":          "🔴 熔断封存",
            "decision":        "三重检测触发红色，熔断封存。",
        }
    if audit == "🟡":
        return {
            "input":           text,
            "digital_root":    dr,
            "gate_color":      g_color,
            "dna":             dna,
            "rule_check":      r1,
            "falsehood_check": r2,
            "data_guard":      r3,
            "state":           "S4_RULE_CONFIRM",
            "route":           "NEED_CONFIRM",
            "audit_color":     "🟡",
            "bucket":          "🔁 待迭代升级池",
            "decision":        "三重检测需要补充确认，暂不执行。",
        }

    # === 5. 抽屉路由 + 五行决策 ===
    hits     = detect_drawers(text)
    elements = [h.element for h in hits]
    relation = element_relation(elements)
    top      = hits[0] if hits else None

    if not top:
        return {
            "input":           text,
            "digital_root":    dr,
            "gate_color":      g_color,
            "dna":             dna,
            "rule_check":      r1,
            "falsehood_check": r2,
            "data_guard":      r3,
            "drawers":         [],
            "elements":        [],
            "relation":        relation,
            "state":           "S2_SEMANTIC_PARSE",
            "route":           "PARSE",
            "engine":          "Semantic Engine",
            "audit_color":     "🟢",
            "bucket":          "⚡ 内部消化",
            "decision":        "通过闸门，进入语义解析。",
        }

    return {
        "input":           text,
        "digital_root":    dr,
        "gate_color":      g_color,
        "dna":             dna,
        "rule_check":      r1,
        "falsehood_check": r2,
        "data_guard":      r3,
        "drawers":         [f"{h.drawer_id}-{h.name}" for h in hits],
        "elements":        elements,
        "relation":        relation,
        "state":           top.state,
        "route":           top.route,
        "engine":          top.engine,
        "audit_color":     "🟢",
        "bucket":          "📦 入库/封装" if top.priority >= 80 else "🟢 推草日志",
        "decision":        "通过第一道闸门，进入沙盒分拣与后续流程。",
    }


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    tests = [
        "宝宝，帮我把这个Notion自动跑起来，带DNA追溯",
        "这个版本v3.9要不要执行",
        "这个方案100%会成功，保证赚钱",
        "刚刚那个上下文记住，晚点再回滚",
        "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 这个不许动，封存",
    ]
    import json
    for t in tests:
        print("─" * 70)
        print(json.dumps(decide(t), ensure_ascii=False, indent=2))

    print("\n" + "═" * 70)
    print(f"DNA: {DNA_PREFIX}2026-04-26-GATE-ENGINE-INTEGRATED-v1.0")
    print(f"确认码: {CONFIRM_CODE}")
