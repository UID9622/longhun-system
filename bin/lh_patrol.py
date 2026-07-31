# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PATROL-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·系统巡逻兵 v1.0                                        ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PATROL-v1.0           ║
# ║  用法: python3 bin/lh_patrol.py                              ║
# ╚══════════════════════════════════════════════════════════════╝
"""
全系统安全巡检：未提交文件、敏感信息、服务健康、lint 报告。
输出: 02_執行記錄/patrol_YYYYMMDD.md
"""

import os
import re
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PATROL-v1.0"

ROOT = Path(__file__).parent.parent
REPORT_DIR = ROOT / "02_執行記錄"
REPORT_DIR.mkdir(exist_ok=True)

SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret[_-]?key|password|token|credential)\s*[:=]\s*['\"][\w\-]{8,}"),
    re.compile(r"(?i)(-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----)"),
    re.compile(r"(?i)(AKID[\w]{16,})"),  # 腾讯云 API Key 近似
]

SERVICE_CHECKS = [
    ("memory-api", "http://127.0.0.1:8771/v1/memory/health"),
    ("persona-api", "http://127.0.0.1:8779/health"),
]


def run_git_status():
    try:
        out = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
        files = [line.strip() for line in out.splitlines() if line.strip()]
        return files
    except Exception as e:
        return [f"git status 失败: {e}"]


def scan_sensitive_files():
    findings = []
    scan_dirs = [ROOT / "bin", ROOT / "engines", ROOT / "portal", ROOT / "tests"]
    for d in scan_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.py"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                for pat in SENSITIVE_PATTERNS:
                    for m in pat.finditer(text):
                        findings.append({"file": str(f.relative_to(ROOT)), "match": m.group(0)[:80]})
            except Exception:
                pass
    return findings


def check_lint_reports():
    reports = []
    lint_dir = ROOT / "reports" / "lint"
    if lint_dir.exists():
        for f in sorted(lint_dir.glob("*.json"), reverse=True):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                reports.append({"file": str(f.relative_to(ROOT)), "summary": data.get("summary", {})})
            except Exception:
                pass
    return reports


def check_services():
    import urllib.request
    results = []
    for name, url in SERVICE_CHECKS:
        try:
            with urllib.request.urlopen(url, timeout=3) as resp:
                results.append({"name": name, "url": url, "status": resp.status, "ok": True})
        except Exception as e:
            results.append({"name": name, "url": url, "status": 0, "ok": False, "error": str(e)})
    return results


def main():
    today = datetime.now().strftime("%Y%m%d")
    report_path = REPORT_DIR / f"patrol_{today}.md"

    print(f"[PATROL] DNA: {DNA}")
    print("[PATROL] 开始全系统巡检...")

    git_files = run_git_status()
    sensitive = scan_sensitive_files()
    lint_reports = check_lint_reports()
    services = check_services()

    red_flags = []
    if sensitive:
        red_flags.append(f"发现 {len(sensitive)} 处潜在敏感信息泄露")
    if any(not s["ok"] for s in services):
        red_flags.append("部分核心服务未在线")

    lines = [
        f"# 龍魂系统巡逻报告 · {datetime.now().isoformat()}",
        f"**DNA**: `{DNA}`",
        f"**巡检人**: UID9622",
        "",
        "## 摘要",
        "",
        f"- 未提交/修改文件: {len(git_files)}",
        f"- 潜在敏感信息: {len(sensitive)}",
        f"- lint 报告: {len(lint_reports)}",
        f"- 服务检查: {sum(1 for s in services if s['ok'])}/{len(services)} 在线",
        f"- 🔴 红旗: {len(red_flags)}",
        "",
    ]

    if red_flags:
        lines.append("### ⚠️ 红旗项")
        for flag in red_flags:
            lines.append(f"- 🔴 {flag}")
        lines.append("")

    lines.extend([
        "## 1. Git 状态",
        "",
        "```",
    ])
    lines.extend(git_files or ["工作区干净"])
    lines.extend(["```", ""])

    lines.extend(["## 2. 敏感信息扫描", ""])
    if sensitive:
        for item in sensitive[:20]:
            lines.append(f"- `{item['file']}`: `{item['match']}`")
        if len(sensitive) > 20:
            lines.append(f"- ... 还有 {len(sensitive) - 20} 项")
    else:
        lines.append("- 🟢 未发现明显敏感信息")
    lines.append("")

    lines.extend(["## 3. Lint 报告", ""])
    if lint_reports:
        for r in lint_reports[:5]:
            lines.append(f"- `{r['file']}`: {json.dumps(r['summary'], ensure_ascii=False)}")
    else:
        lines.append("- 未找到 lint 报告")
    lines.append("")

    lines.extend(["## 4. 服务健康", ""])
    for s in services:
        icon = "🟢" if s["ok"] else "🔴"
        lines.append(f"- {icon} `{s['name']}` ({s['url']}) -> HTTP {s['status']}")
    lines.append("")

    lines.extend(["## 5. 建议", "", "- 修复所有红旗项后再提交代码", "- 定期运行 `python3 bin/lh_patrol.py`", ""])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[PATROL] 报告已保存: {report_path}")
    print(f"[PATROL] 红旗: {len(red_flags)}")
    return 1 if red_flags else 0


if __name__ == "__main__":
    sys.exit(main())
