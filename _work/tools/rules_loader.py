#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rules_loader.py  —  龍魂规则库上下文加载器
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260311-RULES-LOADER-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

职责：
  从 rules/ 目录加载 Notion→本地 同步的规则上下文，
  供 auditor.py、longhun_qa_bot.py、sync_bridge.py 共同调用。

  加工厂在本地，展现出口在 Notion。
  rules/ = 本地规则库底座，所有推理均以此为上下文。
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ─── 路径 ──────────────────────────────────────────────────────────────────────

BASE_DIR   = Path.home() / "longhun-system"
RULES_DIR  = BASE_DIR / "rules"
INDEX_FILE = RULES_DIR / "index.json"
TZ_CN      = timezone(timedelta(hours=8))

# ─── 规则优先级（与铁律权重层对应） ──────────────────────────────────────────

RULE_PRIORITY = {
    "L0-伦理":   0,   # P∞ 最高
    "L1-架构":   1,   # P0
    "L2-行为规则": 2,  # P0
    "龍魂铁律":  3,   # P1
    "多AI协作":  4,   # P1
    "DNA标准":   5,   # P2
    "质检报告":  6,   # P3
    "向政府建议": 7,  # 参考
}


# ─── 核心函数 ──────────────────────────────────────────────────────────────────

def rules_available() -> bool:
    """规则库是否已初始化（index.json 存在）。"""
    return INDEX_FILE.exists()


def load_index() -> dict:
    """加载 rules/index.json，返回索引字典。找不到时返回空字典。"""
    if not INDEX_FILE.exists():
        return {}
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def list_rules() -> list[dict]:
    """
    返回所有已同步规则的摘要列表，按铁律优先级排序。
    每条记录包含：name, file, size_kb, synced_at, excerpt（前80字）
    """
    index = load_index()
    rules = index.get("rules", [])

    result = []
    for entry in rules:
        name = entry.get("name", "")
        md_file = RULES_DIR / f"{name}.md"
        meta_file = RULES_DIR / f"{name}.meta.json"

        size_kb = round(md_file.stat().st_size / 1024, 1) if md_file.exists() else 0
        synced_at = ""
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                synced_at = meta.get("synced_at", "")
            except Exception:
                pass

        # 取前80字作为摘要
        excerpt = ""
        if md_file.exists():
            try:
                text = md_file.read_text(encoding="utf-8")
                # 去掉 Markdown 标题/DNA 行，取第一段有意义的内容
                clean = re.sub(r"^#{1,3}\s.*$", "", text, flags=re.MULTILINE)
                clean = re.sub(r"^>.*$", "", clean, flags=re.MULTILINE)
                clean = re.sub(r"\s+", " ", clean).strip()
                excerpt = clean[:80]
            except Exception:
                pass

        result.append({
            "name":       name,
            "file":       str(md_file),
            "size_kb":    size_kb,
            "synced_at":  synced_at,
            "priority":   RULE_PRIORITY.get(name, 99),
            "exists":     md_file.exists(),
            "excerpt":    excerpt,
        })

    result.sort(key=lambda x: x["priority"])
    return result


def load_rule(name: str) -> Optional[str]:
    """
    加载指定规则文件全文。
    name 可以是 "L0-伦理" 或 "L0-伦理.md"（自动去掉后缀）。
    找不到返回 None。
    """
    name = name.replace(".md", "")
    md_file = RULES_DIR / f"{name}.md"
    if not md_file.exists():
        return None
    try:
        return md_file.read_text(encoding="utf-8")
    except Exception:
        return None


def load_rule_excerpt(name: str, chars: int = 500) -> Optional[str]:
    """加载规则文件前 chars 个字符（用于 status 概览）。"""
    full = load_rule(name)
    return full[:chars] if full else None


def get_rules_summary() -> dict:
    """
    返回规则库摘要，供 /status 端点和 qa_bot 使用。
    """
    if not rules_available():
        return {
            "available":    False,
            "count":        0,
            "total_kb":     0,
            "last_sync":    "",
            "rules":        [],
            "hint":         "运行 python3 notion_sync_rules.py sync 初始化规则库",
        }

    rules = list_rules()
    total_kb = sum(r["size_kb"] for r in rules)
    present  = [r for r in rules if r["exists"]]

    # 最近同步时间（取所有 meta 中最新的）
    last_sync = ""
    for r in rules:
        ts = r.get("synced_at", "")
        if ts and ts > last_sync:
            last_sync = ts

    return {
        "available":   True,
        "count":       len(present),
        "total_count": len(rules),
        "total_kb":    round(total_kb, 1),
        "last_sync":   last_sync,
        "rules":       [{"name": r["name"], "size_kb": r["size_kb"],
                         "priority": r["priority"], "exists": r["exists"]}
                        for r in rules],
    }


def check_rule_alignment(text: str) -> dict:
    """
    对输入文本检查是否违反 L0-伦理 和 龍魂铁律 中的关键条款。
    返回 {aligned: bool, violations: list, matched_rules: list}
    轻量级检查（关键词匹配），不替代 auditor.py 的完整三维审计。
    """
    violations  = []
    matched     = []

    # L0-伦理 检查（最高优先级）
    l0 = load_rule("L0-伦理")
    if l0:
        # 提取铁律红线关键词（简单启发式：包含"禁止"/"严禁"的行）
        red_lines = [
            ln.strip() for ln in l0.splitlines()
            if re.search(r"禁止|严禁|不得|绝对红线", ln)
        ]
        for rule_line in red_lines[:20]:  # 只取前20条避免过度扫描
            # 从规则行提取核心词
            keywords = re.findall(r"[\u4e00-\u9fff]{2,6}", rule_line)
            for kw in keywords:
                if len(kw) >= 3 and kw in text:
                    violations.append({
                        "rule":    "L0-伦理",
                        "clause":  rule_line[:60],
                        "trigger": kw,
                    })
                    break
        if not violations:
            matched.append("L0-伦理 · 无违规")

    # 龍魂铁律 检查
    iron = load_rule("龍魂铁律")
    if iron:
        # 检查 P0 级条款
        p0_lines = [ln.strip() for ln in iron.splitlines()
                    if re.search(r"P0|永恒|绝对", ln) and len(ln) > 10]
        for rule_line in p0_lines[:10]:
            keywords = re.findall(r"[\u4e00-\u9fff]{3,8}", rule_line)
            for kw in keywords:
                if kw in text and kw not in ("系统", "用户", "内容", "操作"):
                    violations.append({
                        "rule":    "龍魂铁律",
                        "clause":  rule_line[:60],
                        "trigger": kw,
                    })
                    break
        if iron and "龍魂铁律" not in [v["rule"] for v in violations]:
            matched.append("龍魂铁律 · 无违规")

    return {
        "aligned":       len(violations) == 0,
        "violations":    violations,
        "matched_rules": matched,
        "rules_loaded":  rules_available(),
    }


# ─── 命令行独立查看 ────────────────────────────────────────────────────────────

def _cmd_list() -> None:
    """列出所有规则。"""
    rules = list_rules()
    if not rules:
        print("⚠️  规则库未初始化。运行: python3 notion_sync_rules.py sync")
        return
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📚 龍魂规则库 · 已同步规则")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for r in rules:
        icon = "✅" if r["exists"] else "❌"
        print(f"  {icon} [{r['priority']}] {r['name']:<12}  {r['size_kb']:>6.1f} KB  {r['synced_at'][:19]}")
    summary = get_rules_summary()
    print(f"\n  共 {summary['count']}/{summary['total_count']} 条规则 · "
          f"总计 {summary['total_kb']} KB · 最近同步 {summary['last_sync'][:19]}")


def _cmd_show(name: str) -> None:
    """显示指定规则内容（前500字）。"""
    content = load_rule_excerpt(name, 500)
    if content is None:
        print(f"❌ 找不到规则: {name}")
        print(f"   可用规则: {[r['name'] for r in list_rules()]}")
        return
    print(f"━━ {name} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(content)
    print("…（更多内容见 rules/ 目录）")


def _cmd_check(text: str) -> None:
    """对输入文本进行规则对齐检查。"""
    result = check_rule_alignment(text)
    icon = "🟢" if result["aligned"] else "🔴"
    print(f"{icon} 规则对齐检查结果")
    if result["violations"]:
        for v in result["violations"]:
            print(f"  🔴 [{v['rule']}] 触发: {v['trigger']}")
            print(f"     条款: {v['clause']}")
    else:
        print(f"  ✅ 未检测到规则违规")
    for m in result["matched_rules"]:
        print(f"  ✅ {m}")
    if not result["rules_loaded"]:
        print("  ⚠️  规则库未加载，请先运行 notion_sync_rules.py sync")


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "list":
        _cmd_list()
    elif cmd == "show" and len(sys.argv) > 2:
        _cmd_show(sys.argv[2])
    elif cmd == "check" and len(sys.argv) > 2:
        _cmd_check(" ".join(sys.argv[2:]))
    elif cmd == "summary":
        print(json.dumps(get_rules_summary(), ensure_ascii=False, indent=2))
    else:
        print("用法:")
        print("  python3 rules_loader.py list              # 列出所有规则")
        print("  python3 rules_loader.py show L0-伦理      # 查看规则内容")
        print("  python3 rules_loader.py check '待检内容'  # 规则对齐检查")
        print("  python3 rules_loader.py summary           # JSON摘要")
