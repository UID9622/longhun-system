#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂安全巡檢 · LongHun Security Patrol
═══════════════════════════════════════════
# DNA:#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-PATROL-SECURITY-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬CODE-P01
# 创建者：UID9622（诸葛鑫）
# 权重级别：L1（核心安全）
# 三色审计状态：🟢 通过
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
═══════════════════════════════════════════

主动测边界·不躲避·定期扫·立即修

扫描维度：
  P0 🔴 — 密钥泄露 · 命令注入 · RCE · 公网暴露
  P1 🟡 — 不安全的反序列化 · XSS · 弱配置
  P2 🟢 — 信息泄露 · 代码规范偏离

用法：
  python3 bin/patrol_security.py              # 全量扫描
  python3 bin/patrol_security.py --quick       # 快速扫P0
  python3 bin/patrol_security.py --report      # 输出JSON报告
  lh patrol                                    # 通过lh入口
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── 配置 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {
    "__pycache__", ".git", ".codebuddy", "node_modules",
    ".venv", "venv", "env", ".tox", ".mypy_cache",
    "backups", "_archived_reports", "downloads-imports",
    "reports",
}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
SCAN_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".tsx", ".html", ".yaml", ".yml", ".cnsh", ".json", ".md"}

# ── P0 规则：密钥泄露 ──
P0_SECRET_PATTERNS = [
    (r"(?:api[_-]?key|API_KEY|apikey)\s*[:=]\s*['\"]([A-Za-z0-9_\-]{20,})['\"]", "API Key 硬编码"),
    (r"(?:secret|SECRET)\s*[:=]\s*['\"]([A-Za-z0-9_\-]{16,})['\"]", "Secret 硬编码"),
    (r"(?:password|PASSWORD|passwd)\s*[:=]\s*['\"]([^'\"]{4,})['\"]", "密码硬编码"),
    (r"(?:token|TOKEN)\s*[:=]\s*['\"]([A-Za-z0-9_\-]{16,})['\"]", "Token 硬编码"),
    (r"(?:private[_-]?key|PRIVATE KEY)", "私钥暴露"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI/类API Key"),
    (r"ntn_[A-Za-z0-9]{20,}", "Notion Token"),
    (r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----", "PEM私钥"),
]

# ── P0 规则：命令注入 / RCE ──
P0_RCE_PATTERNS = [
    (r"os\.system\s*\(.*f[\"']", "os.system 拼接用户输入"),
    (r"subprocess\..*shell\s*=\s*True", "subprocess shell=True"),
    (r"\beval\s*\([^)]*\)", "eval() 调用"),
    (r"\bexec\s*\([^)]*\)", "exec() 调用"),
    (r"\bpickle\.loads?\(", "pickle 反序列化"),
    (r"yaml\.load\s*\([^,)]*\)", "yaml.load 不安全"),
    (r"marshal\.loads?\(", "marshal 反序列化"),
]

# ── P0 规则：公网暴露 ──
P0_EXPOSE_PATTERNS = [
    (r"host\s*=\s*['\"]0\.0\.0\.0['\"]", "绑定 0.0.0.0"),
    (r"debug\s*=\s*True", "debug=True"),
    (r"ssl\s*=\s*False", "SSL关闭"),
]

# ── P1 规则 ──
P1_PATTERNS = [
    (r"innerHTML\s*=", "innerHTML 直接赋值 (XSS风险)"),
    (r"dangerouslySetInnerHTML", "React dangerouslySetInnerHTML"),
    (r"verify\s*=\s*False", "SSL验证禁用"),
    (r"chmod\s+777", "chmod 777"),
    (r"curl.*\|\s*(?:bash|sh)", "curl pipe bash"),
    (r"wget.*-O\s*-\s*\|\s*(?:bash|sh)", "wget pipe bash"),
]

# ── P2 规则 ──
P2_PATTERNS = [
    (r"TODO.*[Ff]ix|[Ff]ixme|HACK|XXX", "待修复标记"),
    (r"print\s*\(\s*['\"]\s*$", "print调试残留"),
]


def 安全巡检(项目路径: Path | None = None, 快速模式: bool = False) -> dict[str, Any]:
    """执行全量安全巡检"""
    项目路径 = 项目路径 or PROJECT_ROOT
    开始时间 = datetime.now(timezone.utc)

    findings: dict[str, list[dict[str, Any]]] = {
        "P0_密钥泄露": [],
        "P0_命令注入RCE": [],
        "P0_公网暴露": [],
        "P1_风险配置": [],
        "P2_代码规范": [],
    }
    扫描文件数 = 0

    for 文件路径 in 项目路径.rglob("*"):
        # 过滤目录
        路径部分 = set(文件路径.parts)
        if 路径部分 & EXCLUDE_DIRS:
            continue
        if 文件路径.name in EXCLUDE_FILES:
            continue
        if 文件路径.suffix not in SCAN_EXTENSIONS and not 快速模式:
            if 文件路径.suffix not in SCAN_EXTENSIONS.union({".key", ".pem", ".env", ".cfg"}):
                # 快速模式也扫常见配置/密钥文件
                continue

        扫描文件数 += 1

        try:
            with open(文件路径, "r", encoding="utf-8", errors="ignore") as f:
                内容 = f.read()
        except Exception:
            continue

        相对路径 = str(文件路径.relative_to(项目路径))

        # P0 扫描
        for 模式, 描述 in P0_SECRET_PATTERNS:
            for m in re.finditer(模式, 内容, re.IGNORECASE | re.MULTILINE):
                行号 = 内容[:m.start()].count("\n") + 1
                findings["P0_密钥泄露"].append({
                    "文件": 相对路径, "行": 行号, "描述": 描述,
                    "匹配": m.group(0)[:60] + ("..." if len(m.group(0)) > 60 else ""),
                })

        for 模式, 描述 in P0_RCE_PATTERNS:
            for m in re.finditer(模式, 内容):
                行号 = 内容[:m.start()].count("\n") + 1
                findings["P0_命令注入RCE"].append({
                    "文件": 相对路径, "行": 行号, "描述": 描述,
                    "匹配": m.group(0)[:80],
                })

        for 模式, 描述 in P0_EXPOSE_PATTERNS:
            for m in re.finditer(模式, 内容):
                行号 = 内容[:m.start()].count("\n") + 1
                findings["P0_公网暴露"].append({
                    "文件": 相对路径, "行": 行号, "描述": 描述,
                    "匹配": m.group(0)[:80],
                })

        if 快速模式:
            continue

        # P1 扫描
        for 模式, 描述 in P1_PATTERNS:
            for m in re.finditer(模式, 内容):
                行号 = 内容[:m.start()].count("\n") + 1
                findings["P1_风险配置"].append({
                    "文件": 相对路径, "行": 行号, "描述": 描述,
                })

        # P2 扫描
        for 模式, 描述 in P2_PATTERNS:
            for m in re.finditer(模式, 内容, re.IGNORECASE):
                行号 = 内容[:m.start()].count("\n") + 1
                findings["P2_代码规范"].append({
                    "文件": 相对路径, "行": 行号, "描述": 描述,
                })

    # 汇总
    p0_count = len(findings["P0_密钥泄露"]) + len(findings["P0_命令注入RCE"]) + len(findings["P0_公网暴露"])
    p1_count = len(findings["P1_风险配置"])
    p2_count = len(findings["P2_代码规范"])
    总发现数 = p0_count + p1_count + p2_count

    report = {
        "DNA": f"#龍芯⚡️{开始时间.strftime('%Y-%m-%d')}-PATROL-REPORT-v1.0",
        "时间": 开始时间.isoformat(),
        "扫描文件数": 扫描文件数,
        "摘要": {"P0": p0_count, "P1": p1_count, "P2": p2_count, "总计": 总发现数},
        "详情": findings,
        "结论": "🟢 安全" if p0_count == 0 else ("🟡 需关注" if p0_count < 5 else "🔴 立即修复"),
    }

    # 写入审计日志
    日志目录 = Path.home() / ".longhun" / "audit"
    日志目录.mkdir(parents=True, exist_ok=True)
    日志文件 = 日志目录 / "patrol_security.jsonl"
    with open(日志文件, "a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")

    return report


def 格式化输出(report: dict[str, Any], 简洁: bool = False):
    """人类可读输出"""
    s = report["摘要"]
    print(f"\n{'='*60}")
    print(f"🐉 龍魂安全巡检 · {report['DNA']}")
    print(f"{'='*60}")
    print(f"扫描: {report['扫描文件数']} 文件")
    print(f"P0🔴: {s['P0']}  |  P1🟡: {s['P1']}  |  P2🟢: {s['P2']}  |  结论: {report['结论']}")
    print(f"{'='*60}")

    if s["P0"] > 0:
        print(f"\n{'─'*40}")
        print("🔴 P0 — 立即修复")
        for 类别, 项目列表 in [("密钥泄露", report["详情"]["P0_密钥泄露"]),
                            ("命令注入/RCE", report["详情"]["P0_命令注入RCE"]),
                            ("公网暴露", report["详情"]["P0_公网暴露"])]:
            if 项目列表:
                print(f"\n  📍 {类别} ({len(项目列表)}项)")
                for item in 项目列表[:10]:
                    print(f"    {item['文件']}:{item['行']} — {item['描述']}")
                    if "匹配" in item:
                        print(f"      → {item['匹配']}")

    if not 简洁 and s["P1"] > 0:
        print(f"\n{'─'*40}")
        print("🟡 P1 — 尽快修复")
        for item in report["详情"]["P1_风险配置"][:10]:
            print(f"  {item['文件']}:{item['行']} — {item['描述']}")

    if not 简洁 and s["P2"] > 0:
        print(f"\n{'─'*40}")
        print("🟢 P2 — 计划修复")
        for item in report["详情"]["P2_代码规范"][:10]:
            print(f"  {item['文件']}:{item['行']} — {item['描述']}")

    print(f"\n{'='*60}")
    if s["P0"] == 0:
        print("✅ 未发现 P0 级威胁 · 系统安全")
    else:
        print(f"⚠️ 发现 {s['P0']} 个 P0 级威胁 · 建议立即修复")
    print(f"审计日志: ~/.longhun/audit/patrol_security.jsonl")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    快速 = "--quick" in sys.argv or "-q" in sys.argv
    仅报告 = "--report" in sys.argv or "-r" in sys.argv
    简洁 = "--short" in sys.argv or "-s" in sys.argv

    report = 安全巡检(快速模式=快速)

    if 仅报告:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        格式化输出(report, 简洁=简洁)

    # 返回码
    sys.exit(1 if report["摘要"]["P0"] > 0 else 0)
