#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·协议落地扫描器 v1.0
扫描 01_protocols/ 下所有协议文档，提取引用的代码路径，检查是否已落地。
DNA: #龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-PROTOCOL-LAND-SCAN-v1.0
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = ROOT / "01_protocols"
REPORT_PATH = ROOT / "state" / "protocol_land_scan_report.md"

CODE_PREFIXES = "bin|engines|deploy|tools|scripts|portal|config|data|governance|papers|01_protocols|state"
CODE_PATTERNS = [
    re.compile(rf"`((?:{CODE_PREFIXES})/[\w\-/.@]+(?:\.py|\.sh|\.yaml|\.json|\.md)?)`"),
    re.compile(rf"\b((?:{CODE_PREFIXES})/[\w\-/.@]+(?:\.py|\.sh|\.yaml|\.json|\.md)?)\b"),
]

SKIP_SUBSTR = {
    "01_protocols/",
}


def extract_references(text):
    refs = set()
    for pat in CODE_PATTERNS:
        for m in pat.finditer(text):
            ref = m.group(1)
            # 过滤掉纯目录或协议引用
            if ref.startswith("01_protocols/"):
                continue
            if ref.endswith("/"):
                continue
            refs.add(ref)
    return sorted(refs)


def check_ref(ref):
    path = ROOT / ref
    return path.exists(), path


def scan():
    if not PROTO_DIR.exists():
        print(f"协议目录不存在: {PROTO_DIR}", file=sys.stderr)
        sys.exit(1)

    reports = []
    total_refs = 0
    missing_refs = 0

    for md_path in sorted(PROTO_DIR.rglob("*.md")):
        rel = md_path.relative_to(ROOT)
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        # 取标题
        title = text.split("\n", 1)[0].lstrip("# ").strip() or rel.name
        refs = extract_references(text)
        if not refs:
            continue
        rows = []
        for ref in refs:
            exists, full = check_ref(ref)
            total_refs += 1
            if not exists:
                missing_refs += 1
            rows.append((ref, "✅" if exists else "🔴缺失", str(full.relative_to(ROOT)) if exists else ""))
        reports.append({
            "title": title,
            "path": str(rel),
            "rows": rows,
            "missing": sum(1 for r in rows if r[1] == "🔴缺失"),
        })

    # 生成报告
    lines = [
        "# 龍魂·协议落地扫描报告",
        f"",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"协议文档数: {len(reports)}",
        f"引用代码总数: {total_refs}",
        f"已落地: {total_refs - missing_refs}",
        f"未落地: {missing_refs}",
        f"落地率: {((total_refs - missing_refs) / total_refs * 100) if total_refs else 0:.1f}%",
        "",
        "---",
        "",
    ]

    for rep in reports:
        lines.append(f"## {rep['title']}")
        lines.append(f"文件: `{rep['path']}`  ·  缺失: {rep['missing']}")
        lines.append("")
        lines.append("| 引用路径 | 状态 | 实际位置 |")
        lines.append("|:---|:---:|:---|")
        for ref, status, loc in rep["rows"]:
            loc_txt = f"`{loc}`" if loc else "—"
            lines.append(f"| `{ref}` | {status} | {loc_txt} |")
        lines.append("")

    # 缺失清单汇总
    lines.append("## 🔴 未落地清单汇总")
    lines.append("")
    any_missing = False
    for rep in reports:
        for ref, status, _ in rep["rows"]:
            if status == "🔴缺失":
                any_missing = True
                lines.append(f"- `{rep['path']}` → `{ref}`")
    if not any_missing:
        lines.append("- 无")
    lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"扫描完成: {REPORT_PATH}")
    print(f"  协议数: {len(reports)}")
    print(f"  引用总数: {total_refs}")
    print(f"  已落地: {total_refs - missing_refs}")
    print(f"  未落地: {missing_refs}")
    print(f"  落地率: {((total_refs - missing_refs) / total_refs * 100) if total_refs else 0:.1f}%")


if __name__ == "__main__":
    scan()
