#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌-COMMAND-CATALOG-v1.0-AST-CLASSIFY
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（思想层） · License: MulanPSL v2（工程层）
"""
龍魂·lh 命令分类目录引擎 v1.0
================================
功能：
  - AST 解析 bin/lh.py 的 SUB_DISPATCH，全量命令自动归类
  - 别名识别（qfind=quick 等）→ 归档标记
  - 旧命令识别（下划线老引擎）→ 归档标记（不删除只冻结）
  - 最新命令白名单（2026-08 新增）→ 优先展示
  - 终端输出分类目录总览

用法：
  python3 bin/lh_command_catalog.py            # 分类总览（12大类）
  python3 bin/lh_command_catalog.py new        # 只看最新命令
  python3 bin/lh_command_catalog.py old        # 只看归档命令（旧+别名）
  python3 bin/lh_command_catalog.py gen        # 生成归档清单 JSON
  python3 bin/lh_command_catalog.py <关键词>   # 按关键词搜索命令
  python3 bin/lh_command_catalog.py --json     # 输出 JSON（供 lh.py 复用）

归档原则：不删除只冻结（P0天条第5条）
"""
from __future__ import annotations

import ast
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LH_PY = ROOT / "bin" / "lh.py"

# ── 十二大分类关键词规则（按命令名+描述匹配）──────────────────────────
CATEGORY_RULES = [
    ("🧠 认知·索引", ["idx", "kg", "matrix", "knowledge-pull", "ai-index", "ai-find", "ai-scan", "ai-report", "quick", "qfind", "search", "cognitive", "universal_completion", "mirror_index", "knowledge_source", "知识图谱", "索引", "检索", "搜索"]),
    ("🤖 人格·调度", ["persona", "military", "duty", "roster", "think", "persona-life", "skill", "persona-mcp", "persona-governance", "persona_router", "persona_sync", "feed_baby", "agent-embed", "人格", "调度", "花名册"]),
    ("🛠️ 工程·开发", ["cnsh", "factory", "test", "deps", "syntax", "benchmark", "load-test", "unify", "update", "visual", "uv", "seven_dimension", "math_explore", "math_automate", "cnsh_env", "cnsh_stamp", "编程", "编译", "测试", "开发"]),
    ("🔒 安全·审计", ["audit", "transparent-audit", "bcm", "behavioral-crypto", "protect", "plagiarize", "guard", "sovereignty", "safeai", "platform-audit", "pa", "compliance", "regulatory", "three_color", "loyalty", "triple_audit", "quantum-evidence", "qe", "安全", "审计", "主权", "熔断", "防火墙", "watermark"]),
    ("🧬 DNA·追溯", ["dna", "dna-gen", "dna-chain", "trust-chain", "imprint", "dna_validate", "验", "追溯", "签章", "盖章"]),
    ("🌐 门户·同步", ["portal", "notion", "proto", "protocols", "wiki", "feishu-wiki", "handoff", "vault", "landing", "bridge", "同步", "门户", "交接", "保险柜", "知识库"]),
    ("🎬 创作·媒体", ["video", "material", "avs3", "vvc", "capture", "merge", "semantic-merge", "smerge", "pipeline_3d", "视频", "素材", "采集", "合并", "编码", "水印"]),
    ("💰 经济·生态", ["xpay", "wish", "eco", "passport", "merchant", "gateway", "loyalty", "支付", "许愿", "生态", "经济", "商户"]),
    ("🧩 插件·集成", ["plugin", "adapter", "browser", "browser-dev", "browserctl", "browser-gw", "hub", "ai-hub", "prompt-router", "pr", "config-pull", "cp", "setup-all", "插件", "适配", "浏览器", "网关"]),
    ("⚖️ 治理·合规", ["governance", "protocol-reign", "preign", "truth", "zhenhua", "regulatory", "intent", "capability", "dynamic_goal", "治理", "合规", "统治", "真话", "意图"]),
    ("📊 状态·运维", ["status", "service-control", "flow-field", "auto-context", "guardian", "auto_heal", "system_health", "health", "状态", "运维", "健康", "仪表", "流场", "服务"]),
    ("📚 知识·学习", ["ddj", "daodejing", "term", "xue", "learn", "evolution", "evo", "fortified", "fort", "tongxinyi", "nl", "naming", "mode", "knowledge_source", "道德经", "学习", "进化", "命名", "术语"]),
]

# ── 别名表：别名 → 主命令（别名标归档·不删除）─────────────────────────
ALIAS_MAP = {
    "qfind": "quick",
    "smerge": "semantic-merge",
    "browserctl": "browser-dev",
    "km": "matrix",
    "pa": "platform-audit",
    "te": "time-engine",
    "ddj": "daodejing",
    "pr": "prompt-router",
    "kp": "knowledge-pull",
    "cp": "config-pull",
    "preign": "protocol-reign",
    "zhenhua": "truth",
    "behavioral-crypto": "bcm",
    "feishu-wiki": "wiki",
    "quantum-evidence": "qe",
    "fort": "fortified",
    "evo": "evolution",
    "visual": "uv",
    "protocols": "proto",
    "syntax-lint": "syntax",
    "syntax-fix": "syntax",
    "dna-gen": "dna",
}

# ── 最新命令白名单（2026-08 新增·cat-new 展示）───────────────────────
NEW_COMMANDS = {
    # 快速索引 v1.0 (08-16)
    "idx", "idx-build", "idx-search", "idx-touch", "idx-suggest", "idx-rank", "idx-status",
    # 知识图谱 v2.0 (08-15)
    "kg", "kg-init", "kg-status", "kg-search", "kg-repair", "kg-export", "kg-tree", "kg-path", "kg-mermaid", "kg-clipboard", "kg-server",
    # 测试/工厂/互通 (08-15)
    "test", "test-orch", "test-report", "test-audit", "test-smoke", "test-data", "test-cov",
    "factory", "factory-run", "factory-status", "factory-gate", "factory-release", "factory-rollback", "factory-monitor", "factory-learn",
    "unify", "unify-install", "unify-sync", "unify-backup", "unify-daemon", "unify-restore",
    # 采集/合并 (08-15)
    "capture", "capture-serve", "capture-all", "capture-merge", "merge", "semantic-merge",
    # 浏览器 (08-15)
    "browser-dev", "browser-dev-start", "browser-dev-stop", "browser-dev-status", "browser-dev-config", "browser-dev-kill", "browser-dev-serve", "browser-gw", "browser-gw-serve",
    # 军事化编制 v2.0 (08-16)
    "military", "military-status", "military-roster", "military-branch", "military-rollcall", "military-order", "military-orders", "military-phase", "military-collab", "military-test", "military-help",
    # 生态/经济
    "eco", "passport", "xpay", "wish", "merchant", "merchant-serve", "gateway-quickstart",
    # 安全/主权
    "sovereignty", "protect", "plagiarize", "guard", "bcm", "transparent-audit", "protocol-reign", "truth",
    # 认知/知识
    "auto-context", "handoff", "vault", "duty", "hub", "ai-hub", "prompt-router", "knowledge-pull", "config-pull", "setup-all",
    "wiki", "ai-index", "ai-find", "ai-scan", "ai-report", "roster", "think", "persona-life", "cnsh-stamp",
    "time-engine", "matrix", "platform-audit", "dna", "dna-chain", "trust-chain", "avs3enc", "avs3dec", "vvcenc",
    "service-control", "flow-field", "status", "benchmark", "load-test", "term", "syntax", "agent-embed", "landing", "naming",
}


def load_sub_dispatch() -> dict:
    """AST 解析 lh.py 提取 SUB_DISPATCH 字典"""
    tree = ast.parse(LH_PY.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "SUB_DISPATCH":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        # 兜底：正则提取
                        text = LH_PY.read_text(encoding="utf-8")
                        m = re.search(r"SUB_DISPATCH\s*=\s*\{(.*?)\n\}", text, re.S)
                        if not m:
                            return {}
                        return _parse_shallow(m.group(1))
    return {}


def _parse_shallow(body: str) -> dict:
    """简易解析 SUB_DISPATCH（兜底）"""
    result = {}
    for line in body.splitlines():
        m = re.match(r"""\s*'([^']+)':\s*\('([^']+)',\s*'([^']*)',\s*'([^']*)'""", line)
        if m:
            name, script, emoji, label = m.groups()
            result[name] = {"script": script, "emoji": emoji, "label": label}
    return result


# ── 命令名精确映射（优先于关键词·避免参数误伤）─────────────────────────
NAME_CAT = {
    "benchmark": "📊 状态·运维",
    "load-test": "📊 状态·运维",
    "quick": "🧠 认知·索引",
    "qfind": "🧠 认知·索引",
    "capture": "🎬 创作·媒体",
    "capture-serve": "🎬 创作·媒体",
    "capture-all": "🎬 创作·媒体",
    "capture-merge": "🎬 创作·媒体",
    "merge": "🎬 创作·媒体",
    "semantic-merge": "🎬 创作·媒体",
    "smerge": "🎬 创作·媒体",
    "duty": "🤖 人格·调度",
    "guard": "🔒 安全·审计",
    "plagiarize": "🔒 安全·审计",
    "hub": "🧩 插件·集成",
    "ai-hub": "🧩 插件·集成",
    "gateway-quickstart": "💰 经济·生态",
    "merchant": "💰 经济·生态",
    "merchant-serve": "💰 经济·生态",
    "handoff": "🌐 门户·同步",
    "vault": "🌐 门户·同步",
    "auto-context": "📊 状态·运维",
    "service-control": "📊 状态·运维",
    "flow-field": "📊 状态·运维",
    "status": "📊 状态·运维",
    "time-engine": "📊 状态·运维",
    "te": "📊 状态·运维",
    "term": "📚 知识·学习",
    "wiki": "🌐 门户·同步",
    "feishu-wiki": "🌐 门户·同步",
    "syntax": "🛠️ 工程·开发",
    "syntax-fix": "🛠️ 工程·开发",
    "dna": "🧬 DNA·追溯",
    "dna-gen": "🧬 DNA·追溯",
    "dna-chain": "🧬 DNA·追溯",
    "trust-chain": "🧬 DNA·追溯",
    "imprint": "🧬 DNA·追溯",
    "sovereignty": "🔒 安全·审计",
    "bcm": "🔒 安全·审计",
    "truth": "⚖️ 治理·合规",
    "zhenhua": "⚖️ 治理·合规",
    "protocol-reign": "⚖️ 治理·合规",
    "preign": "⚖️ 治理·合规",
    "xpay": "💰 经济·生态",
    "wish": "💰 经济·生态",
    "eco": "💰 经济·生态",
    "passport": "💰 经济·生态",
}


def classify(name: str, label: str) -> str:
    """按命令名精确映射优先，关键词兜底（剥离参数防误伤）"""
    if name in NAME_CAT:
        return NAME_CAT[name]
    # 剥离 --参数 与 路径片段，只留描述正文
    cleaned = re.sub(r"--\S+", "", label)
    text = f"{name} {cleaned}".lower()
    for cat, kws in CATEGORY_RULES:
        for kw in kws:
            if kw in text or kw.lower() in name:
                return cat
    return "📦 其他"


def build_catalog() -> dict:
    """构建分类目录"""
    raw = load_sub_dispatch()
    catalog = {}
    for name, meta in raw.items():
        if isinstance(meta, tuple):
            script, emoji, label = meta[0], meta[1], meta[2]
        elif isinstance(meta, dict):
            script = meta.get("script", "")
            emoji = meta.get("emoji", "·")
            label = meta.get("label", "")
        else:
            continue
        cat = classify(name, label)
        entry = {
            "name": name,
            "script": script,
            "emoji": emoji or "·",
            "label": label,
            "alias_of": ALIAS_MAP.get(name),
            "is_new": name in NEW_COMMANDS,
            "is_alias": name in ALIAS_MAP,
            "is_old": "_" in name and name not in NEW_COMMANDS,
        }
        entry["archived"] = entry["is_alias"] or entry["is_old"]
        catalog.setdefault(cat, []).append(entry)
    # 分类内排序：最新在前，其余按名称
    for cat in catalog:
        catalog[cat].sort(key=lambda e: (not e["is_new"], e["name"]))
    return catalog


def render(catalog: dict, mode: str = "all", keyword: str = "") -> str:
    """渲染分类目录"""
    lines = []
    total = sum(len(v) for v in catalog.values())
    total_new = sum(1 for v in catalog.values() for e in v if e["is_new"])
    total_old = sum(1 for v in catalog.values() for e in v if e["archived"])
    header = f"🐉 lh 命令分类目录 v1.0 | 共 {total} 条 · 最新 {total_new} · 归档 {total_old}"
    lines.append(header)
    lines.append("=" * 62)

    for cat, entries in catalog.items():
        if mode == "new":
            entries = [e for e in entries if e["is_new"]]
        elif mode == "old":
            entries = [e for e in entries if e["archived"]]
        if keyword:
            entries = [e for e in entries if keyword.lower() in f"{e['name']} {e['label']}".lower()]
        if not entries:
            continue
        lines.append(f"\n{cat}  ({len(entries)})")
        lines.append("-" * 62)
        for e in entries:
            flag = ""
            if e["is_new"] and not e["archived"]:
                flag = " ✨新"
            elif e["is_alias"]:
                flag = f" ➜{e['alias_of']}"
            elif e["is_old"]:
                flag = " 📦旧"
            lines.append(f"  {e['emoji']} lh {e['name']:<22} {e['label'][:42]}{flag}")
    return "\n".join(lines)


def gen_archive_json() -> str:
    """生成归档清单 JSON（旧+别名命令·不删除只冻结）"""
    catalog = build_catalog()
    archived = []
    for cat, entries in catalog.items():
        for e in entries:
            if e["archived"]:
                archived.append({**e, "category": cat, "reason": "别名" if e["is_alias"] else "旧引擎"})
    return json.dumps(archived, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description="龍魂 lh 命令分类目录引擎")
    ap.add_argument("mode", nargs="?", default="all", help="all/new/old/gen/关键词")
    ap.add_argument("keyword", nargs="?", default="")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    catalog = build_catalog()
    mode = args.mode if args.mode in ("all", "new", "old", "gen") else "all"
    keyword = args.keyword or ("" if args.mode in ("all", "new", "old", "gen") else args.mode)

    if args.json:
        print(json.dumps(catalog, ensure_ascii=False, indent=2))
        return

    if args.mode == "gen":
        out = ROOT / "_archive" / "lh_command_archive_v1.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(gen_archive_json(), encoding="utf-8")
        print(f"📦 归档清单已生成: {out}")
        return

    print(render(catalog, mode, keyword))


if __name__ == "__main__":
    main()
