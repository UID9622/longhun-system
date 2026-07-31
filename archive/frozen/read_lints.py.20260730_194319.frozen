#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-READ-LINTS-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·Lint 报告读取器 v1.0                                   ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-READ-LINTS-v1.0       ║
# ║  用法: python3 bin/read_lints.py [report_file]               ║
# ╚══════════════════════════════════════════════════════════════╝
"""
读取 lint 报告并输出摘要：错误数、警告数、Top 文件、修复建议。
支持 JSON / Markdown / 文本格式。
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-READ-LINTS-v1.0"

ROOT = Path(__file__).parent.parent


def find_latest_report() -> Path:
    """查找最新的 lint 报告。"""
    candidates = []
    for d in [ROOT / "reports" / "lint", ROOT / "_work" / "logs_archive"]:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and ("lint" in f.name.lower() or f.suffix in (".json", ".md", ".txt")):
                    candidates.append(f)
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.stat().st_mtime)


def parse_json_report(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data
    except Exception as e:
        return {"error": str(e)}


def parse_text_report(path: Path) -> dict:
    """简单解析文本 lint 报告。"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors = len(re.findall(r"(?i)^.*\berror\b.*$", text, re.MULTILINE))
    warnings = len(re.findall(r"(?i)^.*\bwarning\b.*$", text, re.MULTILINE))
    files = Counter(re.findall(r"([\w\-/\\]+\.py):", text)).most_common(10)
    return {
        "format": "text",
        "summary": {"errors": errors, "warnings": warnings},
        "top_files": [{"file": f, "count": c} for f, c in files],
    }


def summarize(data: dict) -> dict:
    summary = data.get("summary", {})
    errors = summary.get("errors", 0) or summary.get("error", 0) or summary.get("E", 0)
    warnings = summary.get("warnings", 0) or summary.get("warning", 0) or summary.get("W", 0)

    top_files = data.get("top_files", data.get("files", []))
    if isinstance(top_files, dict):
        top_files = [{"file": k, "count": v} for k, v in top_files.items()]

    return {
        "errors": errors,
        "warnings": warnings,
        "top_files": top_files[:10],
        "recommendation": "🔴 请先修复 errors" if errors else ("🟡 请关注 warnings" if warnings else "🟢 代码质量良好"),
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂 Lint 报告读取器")
    parser.add_argument("report", nargs="?", help="lint 报告路径，默认找最新")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    report_path = Path(args.report) if args.report else find_latest_report()
    if not report_path or not report_path.exists():
        print(f"[READ-LINTS] 未找到 lint 报告", file=sys.stderr)
        return 1

    print(f"[READ-LINTS] DNA: {DNA}")
    print(f"[READ-LINTS] 读取报告: {report_path}")

    if report_path.suffix == ".json":
        data = parse_json_report(report_path)
    else:
        data = parse_text_report(report_path)

    if "error" in data:
        print(f"[READ-LINTS] 解析失败: {data['error']}", file=sys.stderr)
        return 1

    summary = summarize(data)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"\n错误数: {summary['errors']}")
        print(f"警告数: {summary['warnings']}")
        print(f"建议: {summary['recommendation']}")
        if summary["top_files"]:
            print("\nTop 问题文件:")
            for item in summary["top_files"]:
                print(f"  - {item.get('file', item)}: {item.get('count', '?')} 次")

    return 0 if summary["errors"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
