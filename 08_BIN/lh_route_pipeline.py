#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丁酉·丁亥·未时·䷼中孚-ROUTE-PIPELINE-v1.0-AUTO
# CREATOR: 诸葛鑫 (UID9622)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🧭 龍魂·穩定執行管線 v1.0 — 接收→执行 一条固定路线·不许变来变去
DNA: #龍芯⚡️丙午·丁酉·丁亥·未时·䷼中孚-ROUTE-PIPELINE-v1.0-AUTO

触发源（老大白话焊点 2026-09-05·verbatim）：
  「启动我们的人格，数字人黑天使军团左右互搏，然后各种技能嘛，是不是让我们把这个
   接收到执行，要有一条稳定的路线嘛？不能变来变去嘛，特别是通心意翻译的，译那些
   语义的都要深度集成嘛，也要实时迭代嘛」

翻译（骨架者→编码者）：
  ① 稳定路线 = 任意意图进来必须走同一条固定管线（确定性·同输入同输出）
  ② 黑天使军团 + 左右互搏 = 审计/安全/新码语境自动注入 P77 双人格互审，不能跳过
  ③ 通心译深度集成 = 语义解析是管线的第一道闸，每个节点统一用同一语义护照
  ④ 实时迭代 = 未覆盖语义自动入学习层(overlay)，下次同句走快路径，语义库越用越懂

管线五段（固定·焊死·不可绕路）：
  段① 通心译·语义护照   — 借 IPA 路由 8 维算护照(意图/八卦/五行/数字根/熔断三色/IPA)
  段② 深度语义·学习层   — overlay 快路径命中? 直接复用上次(确定性) : 新护照入学习层
  段③ 人格路由(表驱动)  — 域判定 → 主人格；审计/安全/新码语境 → 强制注入 P77 黑天使左右互搏
  段④ 技能映射          — 人格+域 → 候选引擎/工具（固定意图映射表）
  段⑤ 终裁与留痕        — 三色终裁 + 执行建议 + 每次调用 append 记录(实时迭代数据源)

用法：
  lh route <任意意图>           # 走管线（默认）
  lh route --duel <意图>        # 强制黑天使左右互搏双审（审计必带）
  lh route --json <意图>        # JSON 护照输出
  lh route --learn              # 实时迭代统计（已学词条/快路径命中率）
  lh route --reset              # 清空 overlay 学习层
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
PROJECT = BIN_DIR.parent
sys.path.insert(0, str(BIN_DIR))
sys.path.insert(0, str(PROJECT / "bin"))

# 通心译 IPA 路由引擎（段①·纯标准库）
from lh_tongxinyi_ipa_router import 通心译IPA路由器

# ═══════════════════════════════════════════════════════════
# 学习层（实时迭代数据·本地主权·不入云）
# ═══════════════════════════════════════════════════════════
PIPE_DIR = Path.home() / ".longhun" / "pipeline"
RECORDS_JSONL = PIPE_DIR / "records.jsonl"   # 每次调用留痕
OVERLAY_JSONL = PIPE_DIR / "overlay.jsonl"   # 实时迭代学习层（快路径）

_ipa_router = 通心译IPA路由器()


def _now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ═══════════════════════════════════════════════════════════
# 段③ 人格路由·固定表（焊死·表驱动·不许变）
# ═══════════════════════════════════════════════════════════
# 域 → (主人格, 审计注入, 说明)
DOMAIN_MAP = {
    "audit":     ("P05 上帝之眼", True, "审计/检查/有没有问题 → 主人格P05·黑天使左右互搏必开"),
    "security":  ("P77 黑天使", True, "安全/漏洞/渗透/红蓝 → 黑天使军团四翼齐飞·左右互搏必开"),
    "code":      ("P04 鲁班", True, "开发/写码/修复 → 主人格P04·新码必过左右互搏双审"),
    "semantics": ("P08 仓颉", False, "翻译/语义/术语/通心译 → 主人格P08仓颉·深嵌通心译"),
    "deploy":    ("P14 吕蒙", False, "部署/上线/发布 → 主人格P14·发布前安全双审"),
    "math":      ("P06 数学大师", False, "计算/权重/数字 → 主人格P06·镜像审计"),
    "query":     ("P16 徐霞客", False, "查/找/搜 → 主人格P16全库探索"),
    "culture":   ("P00 智慧总师", False, "文化/哲理/策略 → 主人格P00智慧总师"),
    "create":    ("P21 蔡伦", False, "文章/文档/知识 → 主人格P21知识印刷"),
    "emotion":   ("P02 宝宝", False, "情绪/温度/安抚 → 主人格P02宝宝"),
    "default":   ("P00 智慧总师", False, "意图不明 → 默认总师·先懂再走"),
}

# 域判定词表（固定·含通心译白话映射）
DOMAIN_KEYWORDS = {
    "audit": ["审计", "审查", "检查", "审核", "有没有问题", "合规", "查查", "把关", "验收", "review", "audit"],
    "security": ["安全", "漏洞", "渗透", "红蓝", "攻防", "黑客", "风险", "黑天使", "密码", "注入", "security", "vuln"],
    "code": ["写", "代码", "开发", "编程", "修复", "bug", "重构", "实现", "建", "搭", "code", "train", "训练", "模型"],
    "semantics": ["翻译", "通心译", "语义", "术语", "意思", "人话", "白话", "译", "含义", "translate", "semantic", "解释"],
    "deploy": ["部署", "上线", "发布", "推送", "同步", "deploy", "publish"],
    "math": ["算", "计算", "数字根", "权重", "五行", "数字", "369", "公式", "math"],
    "query": ["查", "找", "搜", "看", "状态", "列表", "list", "status", "search", "怎么", "是什么", "哪些"],
    "culture": ["道德经", "易经", "道", "德", "曾师", "文化", "哲理", "历史", "阴阳"],
    "create": ["写篇", "文档", "文章", "报告", "知识卡片", "总结", "复盘", "摘要", "document", "doc"],
    "emotion": ["情绪", "烦", "气", "累", "安慰", "哄", "挫败", "温暖", "温度"],
}

# 段④ 技能映射·固定意图→候选引擎/工具（工具=08_BIN 实文件·命令=建议执行入口）
SKILL_MAP = {
    "audit":     ["lh_dual_audit_engine.py", "lh_code_security.py", "lh_anti_tamper.py"],
    "security":  ["lh_rb_confrontation_engine.py", "lh_red_team_engine.py", "lh_vuln_detect.py"],
    "code":      ["lh_lora_trainer.py", "lh_cnsh_absorb.py", "lh_persona_orchestrator.py"],
    "semantics": ["lh_tongxinyi_translator.py", "lh_tongxinyi_ipa_router.py", "lh_term_tool.py"],
    "deploy":    ["lh_deploy.py", "lh_military.py", "lh_server_checker.py"],
    "math":      ["lh_wuxing.py", "lh_dna_stamp.py", "lh_fixpoint.py"],
    "query":     ["lh_global_search_v2.py", "lh_health.py", "lh_memory_load.py"],
    "culture":   ["lh_dao_de_jing.py", "lh_bagua_router.py"],
    "create":    ["lh_template_engine.py", "lh_docs_writer.py"],
    "emotion":   ["lh_persona_thought.py"],
    "default":   ["lh.py", "lh_memory_load.py", "lh_brain.py"],
}

# 口語特徵（命中 → 標記段②白话转译）
COLLOQUIAL_MARKERS = ["整一下", "搞一下", "弄一下", "整到一起", "帮我", "咋", "啥", "让", "我们要", "可不可以", "嘛"]


def _detect_domain(text: str) -> str:
    """固定优先级：安全 > 审计 > 语义/文化 > 域词匹配（防变来变去）"""
    低 = text.lower()
    # 黑天使/互搏/红蓝 关键字强优先
    if any(k in text for k in ["黑天使", "互搏", "红蓝", "渗透", "漏洞", "安全", "黑客"]):
        return "security"
    if any(k in text for k in ["审计", "审查", "检查", "有没有问题", "review", "audit", "验收"]):
        return "audit"
    # 通心译/语义 语境（段③ 深嵌通心译优先于 code 的"译"误判）
    if any(k in text for k in ["通心译", "翻译", "语义", "术语", "意思", "白话", "人话"]):
        return "semantics"
    # 其余按词表（query 默认兜底）
    for domain, kws in DOMAIN_KEYWORDS.items():
        if domain in ("audit", "security", "semantics"):
            continue
        if any(k in text for k in kws):
            return domain
    return "default"


def _is_colloquial(text: str) -> bool:
    return any(m in text for m in COLLOQUIAL_MARKERS)


# ═══════════════════════════════════════════════════════════
# 段② 学习层（快路径·确定性）
# ═══════════════════════════════════════════════════════════
def _load_overlay():
    cache = {}
    if OVERLAY_JSONL.exists():
        for line in OVERLAY_JSONL.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                cache[rec["input"]] = rec
            except Exception:
                continue
    return cache


def _lookup_overlay(text):
    cache = _load_overlay()
    return cache.get(text)


def _record(entry: dict):
    PIPE_DIR.mkdir(parents=True, exist_ok=True)
    with open(RECORDS_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _learn(overlay_entry: dict):
    PIPE_DIR.mkdir(parents=True, exist_ok=True)
    with open(OVERLAY_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(overlay_entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════════
# 主流程：五段管线
# ═══════════════════════════════════════════════════════════
def run_pipeline(text: str, force_duel: bool = False) -> dict:
    text = text.strip()
    ts = _now()

    # ── 段② 快路径（实时迭代·确定性·先于重算） ──
    cached = _lookup_overlay(text)
    fast_path = cached is not None
    if fast_path and not force_duel:
        base = dict(cached)
        base["fast_path"] = True
        base["ts"] = ts
        _record({"input": text, "ts": ts, "fast_path": True, "domain": base.get("domain"),
                 "persona": base.get("persona_main"), "color": base.get("color")})
        return base

    # ── 段① 通心译·语义护照（8维·深度集成） ──
    r = _ipa_router.路由(text, trust_score=95.0)
    passport = {
        "意图": r.意图动作, "八卦": r.八卦路由, "数字根": r.数字根,
        "熔断": r.熔断状态, "五行": {k: v for k, v in r.五行向量.items() if v > 0},
        "语境类型": r.语境类型, "情绪": r.情绪等级,
        "命中IPA": [{"ipa": h["ipa_id"], "name": h["name"], "score": h["score"]} for h in r.命中IPA],
        "路径哈希": r.路径哈希,
    }

    # ── 段③ 人格路由（固定表） ──
    domain = _detect_domain(text)
    persona_main, inject_duel, persona_note = DOMAIN_MAP[domain]
    duel_on = inject_duel or force_duel or "互搏" in text or "双审" in text

    # ── 段④ 技能映射 ──
    tools = SKILL_MAP[domain]

    # ── 段⑤ 终裁 ──
    color = "🔴" if "🔴" in r.熔断状态 else ("🟡" if "🟡" in r.熔断状态 else "🟢")
    colloquial = _is_colloquial(text)
    advice = []
    if duel_on:
        advice.append(f"黑天使左右互搏: 左保守者/右探索者双审 → 明暗天使攻击面 + 明天使代码审计 → 融合终裁")
    for t in tools[:2]:
        advice.append(f"候选工具: {t}")

    result = {
        "input": text, "ts": ts, "fast_path": False,
        "白话": colloquial, "domain": domain,
        "passport": passport,
        "persona_main": persona_main, "persona_note": persona_note,
        "duel_audit": duel_on,
        "tools": tools, "advice": advice,
        "color": color,
    }

    # 实时迭代：新输入 → 入学习层（累积后供蒸馏回语义注册表）
    _learn({k: v for k, v in result.items()
            if k in ("input", "domain", "persona_main", "duel_audit", "tools", "color",
                     "passport", "白话", "advice")})
    _record({"input": text, "ts": ts, "fast_path": False, "domain": domain,
             "persona": persona_main, "duel": duel_on, "color": color, "dr": r.数字根})
    return result


def learn_stats() -> dict:
    overlay = _load_overlay()
    n_rec = 0
    if RECORDS_JSONL.exists():
        n_rec = sum(1 for _ in RECORDS_JSONL.open())
    n_fast = 0
    if RECORDS_JSONL.exists():
        for line in RECORDS_JSONL.open():
            try:
                if json.loads(line).get("fast_path"):
                    n_fast += 1
            except Exception:
                pass
    return {"learned": len(overlay), "records": n_rec, "fast_hits": n_fast,
            "fast_rate": round(n_fast / n_rec, 3) if n_rec else 0.0}


def _reset_learn():
    if OVERLAY_JSONL.exists():
        OVERLAY_JSONL.unlink()
    return "overlay 学习层已清空"


# ═══════════════════════════════════════════════════════════
# 展示
# ═══════════════════════════════════════════════════════════
def _pretty(r: dict) -> str:
    lines = []
    lines.append("🧭 龍魂穩定執行管線 v1.0 — 固定路线·同输入同输出")
    lines.append(f"📥 意图: {r['input']}" + ("  [白话→通心译转译]" if r.get("白话") else ""))
    if r.get("fast_path"):
        lines.append(f"⚡ 快路径命中(实时迭代): {r['color']}")
    else:
        p = r["passport"]
        top_ipa = p["命中IPA"][0]["name"] if p["命中IPA"] else "未覆盖(已入学习层)"
        lines.append(f"① 通心译·语义护照: 意图={p['意图']} · 卦={p['八卦']} · dr={p['数字根']} · 熔断={p['熔断']} · IPA={top_ipa}")
    lines.append(f"③ 人格路由: 主人格={r['persona_main']}")
    if r["duel_audit"]:
        lines.append(f"   🪖 黑天使左右互搏: 注入双审 ✔")
    lines.append(f"④ 技能映射({r['domain']}): " + " | ".join(r["tools"][:3]))
    for a in r["advice"][:2]:
        lines.append(f"   → {a}")
    lines.append(f"⑤ 终裁: {r['color']}  建议: 走上方工具链路执行·审计语境不可跳过双审")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="🧭 龍魂穩定執行管線 v1.0")
    p.add_argument("text", nargs="?", help="任意意图/需求（白话亦可）")
    p.add_argument("--duel", action="store_true", help="强制黑天使左右互搏双审")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--learn", action="store_true", help="实时迭代统计")
    p.add_argument("--reset", action="store_true", help="清空学习层")
    args = p.parse_args()

    if args.reset:
        print(_reset_learn())
        return 0
    if args.learn:
        print(json.dumps(learn_stats(), ensure_ascii=False, indent=2))
        return 0
    if not args.text:
        print(__doc__)
        return 0

    r = run_pipeline(args.text, force_duel=args.duel)
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else _pretty(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
