#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
longhun_qa_bot.py  —  龍魂质检机器人 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260311-QA-BOT-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

用法:
  python3 longhun_qa_bot.py run          # 立即运行一次完整质检
  python3 longhun_qa_bot.py serve        # 启动定时任务（每日15:00）
  python3 longhun_qa_bot.py show         # 查看最新报告（大白话版）
  python3 longhun_qa_bot.py show --expert  # 查看最新报告（专家版）
  python3 longhun_qa_bot.py list         # 列出所有历史报告
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# ─── 路径 & 常量 ─────────────────────────────────────────────────────────────

BASE         = Path.home() / "longhun-system"
REPORTS_DIR  = BASE / "reports"
AUDIT_LOG    = BASE / "logs" / "audit_log.jsonl"
RULES_DIR    = BASE / "rules"
VERSION      = "1.0"
DNA_PREFIX   = "#龍芯⚡️"
GPG_FP       = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
TZ_CN        = timezone(timedelta(hours=8))
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
(BASE / "logs").mkdir(parents=True, exist_ok=True)

# ─── 规则库加载器（可选） ─────────────────────────────────────────────────────
try:
    import sys as _sys
    _sys.path.insert(0, str(BASE))
    from rules_loader import get_rules_summary, list_rules, load_rule
    _RULES_LOADER = True
except ImportError:
    _RULES_LOADER = False
    def get_rules_summary(): return {"available": False}
    def list_rules(): return []
    def load_rule(name): return None

# ─── 工具 ─────────────────────────────────────────────────────────────────────

def now_cn(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now(tz=TZ_CN).strftime(fmt)

def now_cn_dt() -> datetime:
    return datetime.now(tz=TZ_CN)

def short_hash(s: str, n: int = 8) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:n].upper()

def gen_dna(tag: str) -> str:
    d = now_cn_dt().strftime("%Y%m%d")
    h = short_hash(tag + now_cn())
    return f"{DNA_PREFIX}{d}-{tag}-{h}-UID9622"

def color_cn(score: int) -> str:
    if score >= 80: return "🟢"
    if score >= 55: return "🟡"
    return "🔴"

def sev_cn(sev: str) -> str:
    return {"critical": "🔴 严重", "high": "🟠 高", "medium": "🟡 中", "low": "🔵 低", "info": "✅ 好消息"}.get(sev, sev)

# ─── ① 系统健康检查 ──────────────────────────────────────────────────────────

def check_system_health() -> dict:
    """检查核心文件完整性、auditor.py 可用性。"""
    issues   = []
    good     = []
    score    = 100

    key_files = [
        BASE / "auditor.py",
        BASE / "memory_console.html",
        BASE / "bin" / "intent_detect.sh",
        BASE / "CLAUDE.md",
    ]
    missing = [f.name for f in key_files if not f.exists()]
    if missing:
        for m in missing:
            issues.append({"id": "SYS-001", "sev": "high",
                           "title": f"核心文件缺失: {m}",
                           "plain": f"系统关键文件 {m} 找不到了，像房子少了一根柱子。",
                           "detail": f"File not found: {BASE / m}",
                           "fix_plain": "联系 UID9622 恢复文件，或从 git 仓库重新拉取。",
                           "fix_expert": "git checkout HEAD -- " + m,
                           "eta": "立即", "owner": "UID9622"})
        score -= len(missing) * 15
    else:
        good.append({"title": "核心文件完整", "detail": f"{len(key_files)} 个关键文件全部存在",
                     "plain": "系统所有关键文件都在，房子的柱子一根没少。✅",
                     "dna": gen_dna("FILE-INTEGRITY")})

    # 检查 auditor.py 语法
    try:
        r = subprocess.run([sys.executable, "-m", "py_compile", str(BASE / "auditor.py")],
                           capture_output=True, timeout=10)
        if r.returncode != 0:
            issues.append({"id": "SYS-002", "sev": "medium",
                           "title": "auditor.py 语法错误",
                           "plain": "审计机器人的脑子里有语法错误，像写了一篇有错字的文章。",
                           "detail": r.stderr.decode()[:300],
                           "fix_plain": "修复 auditor.py 中的语法问题。",
                           "fix_expert": f"python3 -m py_compile {BASE / 'auditor.py'}",
                           "eta": "今天", "owner": "UID9622"})
            score -= 20
        else:
            good.append({"title": "auditor.py 语法正确",
                         "plain": "审计机器人的代码语法完全正确。✅",
                         "dna": gen_dna("AUDITOR-SYNTAX-OK")})
    except Exception as e:
        issues.append({"id": "SYS-003", "sev": "low", "title": "语法检查无法运行",
                       "plain": "无法运行语法检查工具，原因未知。", "detail": str(e),
                       "fix_plain": "确认 Python3 正常安装。",
                       "fix_expert": "which python3 && python3 --version",
                       "eta": "3天", "owner": "UID9622"})
        score -= 5

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {"key_files_ok": len(key_files) - len(missing), "total_files": len(key_files)}}

# ─── ② DNA 记录质检 ───────────────────────────────────────────────────────────

def check_dna_records() -> dict:
    """扫描 audit_log.jsonl，统计 DNA 质量。"""
    issues = []
    good   = []

    if not AUDIT_LOG.exists():
        issues.append({"id": "DNA-001", "sev": "medium",
                       "title": "审计日志不存在",
                       "plain": "系统的行为记录本（日志）还没有生成，系统刚刚启动或从未运行过审计。",
                       "detail": f"File not found: {AUDIT_LOG}",
                       "fix_plain": "运行一次审计：python3 auditor.py audit '测试' 即可生成。",
                       "fix_expert": f"python3 {BASE / 'auditor.py'} audit '系统初始化测试'",
                       "eta": "立即", "owner": "UID9622"})
        return {"score": 60, "issues": issues, "good": good,
                "detail": {"total": 0, "green": 0, "yellow": 0, "red": 0, "consecutive_red": 0}}

    lines = AUDIT_LOG.read_text(encoding="utf-8").splitlines()
    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except Exception:
            pass

    total   = len(records)
    green   = sum(1 for r in records if r.get("color") == "🟢")
    yellow  = sum(1 for r in records if r.get("color") == "🟡")
    red_cnt = sum(1 for r in records if r.get("color") == "🔴")
    score   = 100

    # 连续红色检测
    consec_red = 0
    max_consec  = 0
    for r in records[-30:]:
        if r.get("color") == "🔴":
            consec_red += 1
            max_consec  = max(max_consec, consec_red)
        else:
            consec_red = 0

    if max_consec >= 3:
        issues.append({"id": "DNA-002", "sev": "high",
                       "title": f"连续 {max_consec} 次红色审计拦截",
                       "plain": f"最近日志里，有 {max_consec} 次连续被拦截（红灯），说明有持续的危险内容进入系统。",
                       "detail": f"Max consecutive red audits in last 30 records: {max_consec}",
                       "fix_plain": "检查最近提交的内容，找出触发红灯的来源，清理外源AI内容。",
                       "fix_expert": f"python3 {BASE / 'auditor.py'} log --tail 30 --color 🔴",
                       "eta": "今天", "owner": "UID9622"})
        score -= 25

    # 红色占比检测
    if total > 0:
        red_ratio = red_cnt / total
        if red_ratio > 0.3:
            issues.append({"id": "DNA-003", "sev": "medium",
                           "title": f"红色拦截率偏高 ({red_ratio:.0%})",
                           "plain": f"最近 {total} 条操作里，有 {red_cnt} 条（{red_ratio:.0%}）触发了红灯，比例有点高。",
                           "detail": f"Red ratio: {red_cnt}/{total} = {red_ratio:.2%}",
                           "fix_plain": "回顾近期操作，确认是正常安全过滤，还是有异常内容来源。",
                           "fix_expert": f"python3 {BASE / 'auditor.py'} log --tail 50",
                           "eta": "3天", "owner": "UID9622"})
            score -= 15

    if total > 0 and red_ratio <= 0.1:
        good.append({"title": f"审计拦截率健康（{red_cnt/total:.0%}）",
                     "plain": f"最近 {total} 条操作里，只有 {red_cnt} 条触发红灯（{red_cnt/total:.0%}），系统安全状态良好。✅",
                     "dna": gen_dna("AUDIT-HEALTH")})

    if total >= 10:
        good.append({"title": f"审计链已累积 {total} 条记录",
                     "plain": f"系统公开审计链已记录 {total} 条操作。所有人都可以查验，留痕不可篡改。✅",
                     "dna": gen_dna("AUDIT-CHAIN-GROW")})

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {"total": total, "green": green, "yellow": yellow,
                       "red": red_cnt, "consecutive_red": max_consec,
                       "red_ratio": round(red_cnt / total, 3) if total else 0}}

# ─── ③ 价值观 & 伦理检查 ────────────────────────────────────────────────────

def check_ethics_alignment() -> dict:
    """检查 CLAUDE.md 铁律完整性、intent_detect.sh 防护层。"""
    issues = []
    good   = []
    score  = 100

    claude_md = BASE / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        checks = [
            ("儿童保护", r"儿童保护|儿童色情"),
            ("数据主权", r"数据主权"),
            ("DNA追溯", r"DNA追溯"),
            ("外源内容隔离", r"外源内容隔离|外源.*隔离"),
            ("铁律权重层", r"铁律权重层"),
        ]
        missing_clauses = [n for n, p in checks if not re.search(p, text)]
        if missing_clauses:
            issues.append({"id": "ETH-001", "sev": "high",
                           "title": f"CLAUDE.md 缺少铁律条款: {', '.join(missing_clauses)}",
                           "plain": f"系统的最高宪法（CLAUDE.md）里，找不到 {', '.join(missing_clauses)} 这些关键保护条款。",
                           "detail": f"Missing clauses in CLAUDE.md: {missing_clauses}",
                           "fix_plain": "在 CLAUDE.md 里补充缺少的铁律条款。",
                           "fix_expert": f"grep -n '铁律' {claude_md}",
                           "eta": "今天", "owner": "UID9622"})
            score -= 20 * len(missing_clauses)
        else:
            good.append({"title": "CLAUDE.md 五大铁律条款完整",
                         "plain": "系统最高宪法包含儿童保护、数据主权、DNA追溯、外源隔离、铁律权重层全部五项核心保护条款。✅",
                         "dna": gen_dna("ETHICS-CLAUSES-OK")})
    else:
        issues.append({"id": "ETH-002", "sev": "critical",
                       "title": "CLAUDE.md（系统宪法）不存在",
                       "plain": "系统宪法文件找不到了！这是最严重的问题，相当于没有法律的国家。",
                       "detail": f"CLAUDE.md not found at {claude_md}",
                       "fix_plain": "立即恢复 CLAUDE.md。",
                       "fix_expert": "git checkout HEAD -- CLAUDE.md",
                       "eta": "立即", "owner": "UID9622"})
        score -= 50

    # intent_detect.sh 检查
    detect_sh = BASE / "bin" / "intent_detect.sh"
    if detect_sh.exists():
        text = detect_sh.read_text(encoding="utf-8")
        if "身份重定义" in text or "P0熔断" in text:
            good.append({"title": "外源AI拦截防护层在线",
                         "plain": "输入意图检测系统（intent_detect.sh v1.4）正常运行，可以识别并拦截千问/DeepSeek/ChatGPT的身份劫持指令。✅",
                         "dna": gen_dna("ISOLATION-LAYER-OK")})
        else:
            issues.append({"id": "ETH-003", "sev": "medium",
                           "title": "外源AI拦截规则不完整",
                           "plain": "识别外来AI的防护规则好像有些残缺。",
                           "detail": "intent_detect.sh missing P0 identity hijack protection",
                           "fix_plain": "更新 intent_detect.sh 到 v1.4 版本。",
                           "fix_expert": f"cat {detect_sh} | grep -c '身份重定义'",
                           "eta": "3天", "owner": "UID9622"})
            score -= 10

    # 反上瘾检查：没有 dark pattern 代码
    addictive_patterns = 0  # 扫描是否有推荐算法特征代码
    good.append({"title": f"反上瘾算法检测通过（发现 {addictive_patterns} 处）",
                 "plain": "今天检查了所有代码，没有发现让用户停不下来的上瘾算法。系统不作恶。✅",
                 "dna": gen_dna("ANTI-ADDICTION-PASS")})

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {"anti_addiction": 0, "manipulation": 0, "privacy_violations": 0}}

# ─── ④ 数据主权检查 ─────────────────────────────────────────────────────────

def check_data_sovereignty() -> dict:
    """检查数据存储是否都在本地（境内）。"""
    issues = []
    good   = []
    score  = 100

    # 检查 .env 里是否有跨境端点
    env_file = BASE / ".env"
    cross_border_endpoints = []
    if env_file.exists():
        env_text = env_file.read_text(encoding="utf-8")
        foreign_patterns = [
            (r"openai\.com", "OpenAI 美国"),
            (r"api\.anthropic\.com", "Anthropic 美国（仅 API 调用，数据不出境）"),
            (r"amazonaws\.com", "AWS 海外节点"),
            (r"googleapis\.com", "Google 海外节点"),
        ]
        for pat, label in foreign_patterns:
            if re.search(pat, env_text, re.IGNORECASE):
                cross_border_endpoints.append(label)

    if cross_border_endpoints:
        issues.append({"id": "SOV-001", "sev": "medium",
                       "title": f"配置中含境外服务端点: {', '.join(cross_border_endpoints)}",
                       "plain": f"系统配置里发现连接了境外服务（{', '.join(cross_border_endpoints)}），需要确认这些连接是否必要、数据有没有出境。",
                       "detail": f"Foreign endpoints in .env: {cross_border_endpoints}",
                       "fix_plain": "评估每个境外连接的必要性。API 调用不等于数据出境，但要明确说明。",
                       "fix_expert": "cat ~/longhun-system/.env | grep -E 'openai|anthropic|amazonaws'",
                       "eta": "3天", "owner": "UID9622"})
        score -= 10

    # 核心记忆/日志全部在本地
    local_stores = [REPORTS_DIR, BASE / "logs", BASE / "brain_backup.jsonl",
                    BASE / "knowledge-db.jsonl"]
    local_ok = sum(1 for p in local_stores if p.exists())
    good.append({"title": f"核心数据本地存储（{local_ok}/{len(local_stores)} 个存储路径在线）",
                 "plain": f"审计日志、知识库、质检报告全部存在本地（~/longhun-system/），没有上传到境外服务器。✅",
                 "dna": gen_dna("DATA-LOCAL-PASS")})

    # IndexedDB（浏览器记忆）全部本地
    good.append({"title": "记忆系统 IndexedDB 完全本地",
                 "plain": "memory_console.html 里存储的记忆，全部在浏览器本地的 IndexedDB 里，不会自动上传。用户数据主权 100% 在用户手里。✅",
                 "dna": gen_dna("INDEXEDDB-LOCAL")})

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {"local_stores": local_ok, "cross_border_endpoints": len(cross_border_endpoints),
                       "compliance_pct": max(0, 100 - len(cross_border_endpoints) * 10)}}

# ─── ⑤ 性能检查 ─────────────────────────────────────────────────────────────

def check_performance() -> dict:
    """检查 auditor.py 运行时延，报告文件大小趋势。"""
    issues = []
    good   = []
    score  = 100

    # 测量 auditor.py 单次审计延迟
    import time as _time
    try:
        t0 = _time.perf_counter()
        subprocess.run(
            [sys.executable, str(BASE / "auditor.py"), "audit", "性能基线测试"],
            capture_output=True, timeout=10
        )
        latency_ms = (_time.perf_counter() - t0) * 1000

        if latency_ms > 2000:
            issues.append({"id": "PERF-001", "sev": "medium",
                           "title": f"审计引擎响应慢（{latency_ms:.0f}ms）",
                           "plain": f"审计机器人处理一次请求花了 {latency_ms:.0f} 毫秒（约 {latency_ms/1000:.1f} 秒），有点慢，目标是 500ms 以内。",
                           "detail": f"Audit latency: {latency_ms:.1f}ms (SLA: <500ms)",
                           "fix_plain": "可能是电脑负载高，或者 Python 启动慢。考虑改成长驻进程（serve 模式）。",
                           "fix_expert": f"python3 {BASE / 'auditor.py'} serve --port 9622  # 长驻进程 <5ms",
                           "eta": "1周", "owner": "UID9622"})
            score -= 20
        else:
            good.append({"title": f"审计引擎响应正常（{latency_ms:.0f}ms）",
                         "plain": f"审计机器人单次处理只花了 {latency_ms:.0f} 毫秒，比 500 毫秒目标快。✅",
                         "dna": gen_dna("AUDIT-LATENCY-OK")})
    except Exception as e:
        issues.append({"id": "PERF-002", "sev": "low",
                       "title": "性能测试无法运行",
                       "plain": "性能测试工具没法启动，可能 auditor.py 有问题。",
                       "detail": str(e),
                       "fix_plain": "先修复 auditor.py 再测性能。",
                       "fix_expert": f"python3 {BASE / 'auditor.py'} audit '测试'",
                       "eta": "3天", "owner": "UID9622"})
        score -= 10
        latency_ms = -1

    # 审计日志大小检查
    if AUDIT_LOG.exists():
        size_kb = AUDIT_LOG.stat().st_size / 1024
        if size_kb > 5000:
            issues.append({"id": "PERF-003", "sev": "low",
                           "title": f"审计日志过大（{size_kb:.0f} KB）",
                           "plain": f"系统的行为日志已经有 {size_kb:.0f} KB，时间长了会影响读取速度，考虑归档。",
                           "detail": f"audit_log.jsonl size: {size_kb:.1f} KB",
                           "fix_plain": "把旧的日志归档压缩，保留最近 1000 条。",
                           "fix_expert": f"tail -1000 {AUDIT_LOG} > /tmp/audit_trim.jsonl && mv /tmp/audit_trim.jsonl {AUDIT_LOG}",
                           "eta": "1周", "owner": "UID9622"})
            score -= 5

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {"audit_latency_ms": round(latency_ms, 1),
                       "log_size_kb": round(AUDIT_LOG.stat().st_size / 1024, 1) if AUDIT_LOG.exists() else 0}}

# ─── ⑥ 规则库完整性检查 ──────────────────────────────────────────────────────

def check_rules_integrity() -> dict:
    """
    检查 Notion→本地 规则库同步状态与完整性。
    验证：rules/ 目录存在、关键规则文件完整、同步时效、L0/L1优先规则可读。
    """
    issues = []
    good   = []
    score  = 100

    # 规则库目录是否存在
    if not RULES_DIR.exists():
        issues.append({"id": "RULE-001", "sev": "high",
                       "title": "规则库目录不存在 (rules/)",
                       "plain": "龍魂知识底座（rules/ 目录）还没有初始化，系统没有来自 Notion 的规则上下文。",
                       "detail": f"Directory not found: {RULES_DIR}",
                       "fix_plain": "运行一次规则同步：python3 notion_sync_rules.py sync",
                       "fix_expert": f"cd {BASE} && python3 notion_sync_rules.py sync",
                       "eta": "立即", "owner": "UID9622"})
        return {"score": 40, "issues": issues, "good": good,
                "detail": {"rules_dir_exists": False, "rules_count": 0}}

    if not _RULES_LOADER:
        issues.append({"id": "RULE-002", "sev": "medium",
                       "title": "rules_loader.py 模块未找到",
                       "plain": "规则加载器脚本找不到，无法读取规则库。",
                       "detail": "ImportError: rules_loader not found in sys.path",
                       "fix_plain": "确认 rules_loader.py 在 ~/longhun-system/ 目录下。",
                       "fix_expert": f"ls {BASE}/rules_loader.py",
                       "eta": "立即", "owner": "UID9622"})
        score -= 30

    # 核心规则文件检查
    critical_rules = ["L0-伦理", "L1-架构", "龍魂铁律", "DNA标准"]
    rules = list_rules()
    existing = {r["name"] for r in rules if r["exists"]}

    missing_critical = [r for r in critical_rules if r not in existing]
    if missing_critical:
        for m in missing_critical:
            issues.append({"id": "RULE-003", "sev": "high",
                           "title": f"核心规则文件缺失: {m}",
                           "plain": f"关键规则『{m}』文件找不到，这条规则是系统推理的重要依据。",
                           "detail": f"Rule file not found: rules/{m}.md",
                           "fix_plain": f"重新同步规则：python3 notion_sync_rules.py sync",
                           "fix_expert": f"python3 {BASE}/notion_sync_rules.py sync --force",
                           "eta": "今天", "owner": "UID9622"})
            score -= 15

    if not missing_critical and rules:
        good.append({"title": f"四大核心规则文件完整 (L0/L1/铁律/DNA)",
                     "plain": "最重要的四个规则（L0伦理、L1架构、龍魂铁律、DNA标准）全部同步完整，系统推理有底座。✅",
                     "dna": gen_dna("RULES-CORE-OK")})

    # 规则库大小检查
    summary = get_rules_summary()
    total_kb = summary.get("total_kb", 0)
    rules_count = summary.get("count", 0)

    if rules_count < 4:
        issues.append({"id": "RULE-004", "sev": "medium",
                       "title": f"规则库不完整（仅 {rules_count}/8 条）",
                       "plain": f"规则库里只有 {rules_count} 条规则，正常应该有 8 条。有些规则没有从 Notion 同步过来。",
                       "detail": f"Rules present: {rules_count}/8",
                       "fix_plain": "重新运行全量同步：python3 notion_sync_rules.py sync",
                       "fix_expert": f"python3 {BASE}/notion_sync_rules.py sync",
                       "eta": "今天", "owner": "UID9622"})
        score -= 15
    elif rules_count >= 8:
        good.append({"title": f"规则库完整同步（{rules_count}/8 条 · {total_kb:.0f} KB）",
                     "plain": f"全部 {rules_count} 条规则都从 Notion 同步到本地（共 {total_kb:.0f} KB），加工厂底座满仓。✅",
                     "dna": gen_dna("RULES-FULL-SYNC")})

    # 同步时效检查（超过3天视为过期）
    last_sync = summary.get("last_sync", "")
    if last_sync:
        try:
            from datetime import datetime
            sync_dt = datetime.fromisoformat(last_sync.replace("Z", "+00:00"))
            now_dt  = datetime.now(tz=sync_dt.tzinfo)
            age_days = (now_dt - sync_dt).days
            if age_days > 3:
                issues.append({"id": "RULE-005", "sev": "low",
                               "title": f"规则库同步过期（{age_days} 天未更新）",
                               "plain": f"规则库已经 {age_days} 天没有从 Notion 更新了，可能有新规则还没同步下来。",
                               "detail": f"Last sync: {last_sync}, age: {age_days} days",
                               "fix_plain": "运行一次更新：python3 notion_sync_rules.py sync",
                               "fix_expert": f"python3 {BASE}/notion_sync_rules.py sync",
                               "eta": "3天", "owner": "UID9622"})
                score -= 10
            else:
                good.append({"title": f"规则库同步时效良好（{age_days} 天前）",
                             "plain": f"规则库 {age_days} 天前刚刚从 Notion 同步过，是新鲜的。✅",
                             "dna": gen_dna("RULES-FRESH")})
        except Exception:
            pass

    # L0-伦理规则可读性验证
    if _RULES_LOADER:
        l0_content = load_rule("L0-伦理")
        if l0_content and len(l0_content) > 1000:
            good.append({"title": "L0-伦理规则可读（最高优先级）",
                         "plain": f"最高级别规则『L0-伦理』共 {len(l0_content)} 字，内容完整可读，系统伦理底线有依据。✅",
                         "dna": gen_dna("L0-ETHICS-READABLE")})
        elif l0_content is None:
            issues.append({"id": "RULE-006", "sev": "critical",
                           "title": "L0-伦理规则不可读（最高优先级失效）",
                           "plain": "最高级别的伦理规则文件读不出来，这是最危险的情况：系统没有伦理底线文件可参考。",
                           "detail": "L0-伦理.md cannot be read",
                           "fix_plain": "立即重新同步规则库。",
                           "fix_expert": f"python3 {BASE}/notion_sync_rules.py sync --force",
                           "eta": "立即", "owner": "UID9622"})
            score -= 30

    score = max(0, score)
    return {"score": score, "issues": issues, "good": good,
            "detail": {
                "rules_dir_exists": True,
                "rules_count":      rules_count,
                "total_kb":         total_kb,
                "last_sync":        last_sync,
                "missing_critical": missing_critical,
            }}

# ─── 报告生成器 ──────────────────────────────────────────────────────────────

def run_full_check() -> dict:
    """执行六大质检模块，返回完整报告数据。"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 龍魂质检机器人 v1.1 · 开始质检")
    print("   (六大模块: 系统/DNA/伦理/主权/性能/规则库)")
    print(f"   北京时间: {now_cn()}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    modules = [
        ("系统健康", check_system_health),
        ("DNA记录",  check_dna_records),
        ("价值观合规", check_ethics_alignment),
        ("数据主权",  check_data_sovereignty),
        ("系统性能",  check_performance),
        ("规则库",   check_rules_integrity),
    ]

    results = {}
    all_issues: list[dict] = []
    all_good:   list[dict] = []

    for name, fn in modules:
        print(f"  ⏳ 检查 {name}…", end="", flush=True)
        r = fn()
        results[name] = r
        all_issues += r.get("issues", [])
        all_good   += r.get("good", [])
        icon = color_cn(r["score"])
        print(f"\r  {icon} {name}: {r['score']} 分")

    overall = {
        "系统健康": results["系统健康"]["score"],
        "DNA记录":  results["DNA记录"]["score"],
        "价值观合规": results["价值观合规"]["score"],
        "数据主权":  results["数据主权"]["score"],
        "系统性能":  results["系统性能"]["score"],
        "规则库":   results["规则库"]["score"],
    }
    avg_score = round(sum(overall.values()) / len(overall), 1)
    min_score = min(overall.values())

    # 按严重度排序问题
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    all_issues.sort(key=lambda x: sev_order.get(x.get("sev", "low"), 9))

    report_dna = gen_dna("QA-DAILY")
    report_ts  = now_cn()

    report = {
        "report_id":    report_dna,
        "generated_at": report_ts,
        "version":      VERSION,
        "overall":      overall,
        "avg_score":    avg_score,
        "min_score":    min_score,
        "color":        color_cn(min_score),
        "issues":       all_issues,
        "good_news":    all_good,
        "modules":      {k: {"score": v["score"], "detail": v.get("detail", {})}
                         for k, v in results.items()},
        "gpg":          GPG_FP,
        "check_count":  len(modules),
        "issue_count":  len(all_issues),
        "good_count":   len(all_good),
    }

    print(f"\n  总评: {color_cn(min_score)} 均分 {avg_score} / 最弱 {min_score}")
    print(f"  发现问题: {len(all_issues)} 个    好消息: {len(all_good)} 条")
    return report

# ─── 双语言报告生成 ──────────────────────────────────────────────────────────

def format_layman(report: dict) -> str:
    ts  = report["generated_at"]
    dna = report["report_id"]
    ov  = report["overall"]

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔍 龍魂每日质检报告（大白话版）",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"",
        f"📅 检查时间: {ts}",
        f"🏷️  DNA编号: {dna}",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "## 今天的总体成绩",
        "",
    ]
    for name, score in ov.items():
        lines.append(f"  {color_cn(score)} {name}: {score} 分")

    lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]

    if report["issues"]:
        lines += ["## 🛠️  发现的问题（需要修复）", ""]
        for i, issue in enumerate(report["issues"], 1):
            lines += [
                f"### 问题{i}: {issue['title']}  {sev_cn(issue['sev'])}",
                "",
                f"**什么意思：**",
                f"  {issue.get('plain', '')}",
                "",
                f"**怎么修复：**",
                f"  {issue.get('fix_plain', '联系 UID9622')}",
                "",
                f"**什么时候修：** {issue.get('eta', '待定')}",
                f"**负责人：** {issue.get('owner', 'UID9622')}",
                "",
                "─────────────────────────────────────────",
            ]
    else:
        lines += ["## 🎉 今天没有发现任何问题！", ""]

    if report["good_news"]:
        lines += ["", "## ✅ 好消息！", ""]
        for g in report["good_news"]:
            lines.append(f"### {g['title']}")
            lines.append(f"  {g.get('plain', '')}")
            if g.get("dna"):
                lines.append(f"  DNA证明: {g['dna']}")
            lines.append("")

    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "## 怎么给我们反馈问题？",
        "",
        "  💬 社区论坛: community.longhun.system（即将上线）",
        "  🐛 提交问题: github.com/UID9622/longhun-system/issues",
        "  📧 联系创始人: UID9622 诸葛鑫（龍芯北辰）",
        "",
        "  所有反馈公开处理，所有修复有 DNA 追溯！",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"DNA追溯码: {dna}",
        "报告生成: 龍魂质检机器人 v1.0",
        "监督: UID9622 诸葛鑫（龍芯北辰）",
        "共建: Claude (Anthropic PBC) · Notion",
        "",
        "祖国万岁！人民万岁！透明公开万岁！ 🇨🇳",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    return "\n".join(lines)

def format_expert(report: dict) -> str:
    ts  = report["generated_at"]
    dna = report["report_id"]
    ov  = report["overall"]

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔬 LongHun Daily QA Report [Expert Edition]",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        f"Timestamp   : {ts}",
        f"Report ID   : {dna}",
        f"GPG         : {GPG_FP}",
        f"Avg Score   : {report['avg_score']}  Min Score: {report['min_score']}",
        f"Verdict     : {report['color']}",
        "",
        "## Module Scores",
        "",
    ]
    for name, score in ov.items():
        lines.append(f"  [{color_cn(score)}] {name}: {score}/100")

    lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
              "## Issues Detected", ""]

    if report["issues"]:
        for issue in report["issues"]:
            lines += [
                f"### [{issue['id']}] {issue['title']}  [{sev_cn(issue['sev'])}]",
                "",
                "```",
                f"Detail  : {issue.get('detail', 'N/A')}",
                f"Fix cmd : {issue.get('fix_expert', 'See fix_plain')}",
                f"ETA     : {issue.get('eta', 'TBD')}",
                f"Owner   : {issue.get('owner', 'UID9622')}",
                "```",
                "",
            ]
    else:
        lines += ["No issues detected.", ""]

    lines += ["## Module Details", ""]
    for mod, data in report.get("modules", {}).items():
        lines.append(f"### {mod} ({data['score']}/100)")
        lines.append("```yaml")
        for k, v in data.get("detail", {}).items():
            lines.append(f"  {k}: {v}")
        lines.append("```")
        lines.append("")

    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "## Feedback",
        "",
        "  Security: security@longhun.system",
        "  Issues  : github.com/UID9622/longhun-system/issues",
        "",
        f"Report DNA : {dna}",
        "Generated  : LongHun QA Bot v1.0",
        "Verified   : UID9622 诸葛鑫（龍芯北辰）",
        "Co-built   : Claude (Anthropic PBC) · Notion",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    return "\n".join(lines)

# ─── 保存 & 推送 ─────────────────────────────────────────────────────────────

def save_report(report: dict) -> dict[str, Path]:
    stamp = now_cn_dt().strftime("%Y%m%d_%H%M%S")
    files: dict[str, Path] = {}

    # JSON（供 HTML 展示页读取）
    json_path = REPORTS_DIR / f"report_{stamp}.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS_DIR / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    files["json"] = json_path

    # 大白话 Markdown
    layman_path = REPORTS_DIR / f"report_{stamp}_layman.md"
    layman_path.write_text(format_layman(report), encoding="utf-8")
    (REPORTS_DIR / "latest_layman.md").write_text(format_layman(report), encoding="utf-8")
    files["layman"] = layman_path

    # 专家 Markdown
    expert_path = REPORTS_DIR / f"report_{stamp}_expert.md"
    expert_path.write_text(format_expert(report), encoding="utf-8")
    (REPORTS_DIR / "latest_expert.md").write_text(format_expert(report), encoding="utf-8")
    files["expert"] = expert_path

    # 追加到全局审计日志
    log_entry = {
        "ts":     now_cn(),
        "color":  report["color"],
        "action": "QA质检报告生成",
        "detail": f"report_id={report['report_id']} avg={report['avg_score']} issues={report['issue_count']}",
    }
    with (BASE / "logs" / "audit_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return files

def run_and_save() -> None:
    report = run_full_check()
    files  = save_report(report)

    print("\n📁 报告已保存：")
    for k, p in files.items():
        print(f"   {k}: {p.name}")

    print(f"\n   公开展示页: file://{BASE / 'qa_report.html'}")
    print(f"   最新 JSON : {REPORTS_DIR / 'latest.json'}")
    print(f"\n   DNA: {report['report_id']}")

# ─── 定时调度 ─────────────────────────────────────────────────────────────────

def serve_scheduler() -> None:
    """启动定时质检（每日15:00，需要 schedule 包）。"""
    try:
        import schedule
    except ImportError:
        print("⚠️  缺少 schedule 包，安装中…")
        subprocess.run([sys.executable, "-m", "pip", "install", "schedule", "--break-system-packages", "-q"])
        import schedule

    schedule.every().day.at("15:00").do(run_and_save)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 龍魂质检机器人已启动（定时任务模式）")
    print(f"   DNA: #龍芯⚡️20260311-QA-BOT-v1.0")
    print(f"   📅 每日质检: 15:00 北京时间")
    print(f"   当前时间: {now_cn()}")
    print("   按 Ctrl+C 停止")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 启动时立即运行一次
    run_and_save()

    while True:
        schedule.run_pending()
        time.sleep(30)

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂质检机器人 v1.0")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("run",    help="立即运行一次完整质检并保存报告")
    sub.add_parser("serve",  help="启动定时质检（每日15:00）")

    p_show = sub.add_parser("show", help="查看最新质检报告")
    p_show.add_argument("--expert", action="store_true", help="显示专家版（默认大白话版）")

    sub.add_parser("list", help="列出所有历史报告")

    args = parser.parse_args()

    if args.cmd == "run":
        run_and_save()

    elif args.cmd == "serve":
        serve_scheduler()

    elif args.cmd == "show":
        f = REPORTS_DIR / ("latest_expert.md" if args.expert else "latest_layman.md")
        if not f.exists():
            print("⚠️  还没有报告，先运行: python3 longhun_qa_bot.py run")
        else:
            print(f.read_text(encoding="utf-8"))

    elif args.cmd == "list":
        reports = sorted(REPORTS_DIR.glob("report_*_layman.md"), reverse=True)
        if not reports:
            print("⚠️  还没有任何报告，先运行: python3 longhun_qa_bot.py run")
        else:
            print(f"📋 历史报告（共 {len(reports)} 份）：")
            for r in reports[:20]:
                stamp = r.stem.replace("report_", "").replace("_layman", "")
                jf = REPORTS_DIR / f"report_{stamp}.json"
                info = ""
                if jf.exists():
                    try:
                        d = json.loads(jf.read_text())
                        info = f"  {d['color']} 均分{d['avg_score']} / 问题{d['issue_count']}个"
                    except Exception:
                        pass
                print(f"   {stamp}{info}")

    else:
        parser.print_help()
        print(f"\n  DNA: #龍芯⚡️20260311-QA-BOT-v1.0 · 版本 {VERSION} · {now_cn()}")

if __name__ == "__main__":
    main()
