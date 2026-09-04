#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-TEST-REPORT-GEN-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 测试报告生成器
生成 Markdown 格式测试报告（含 v1.1 三色审计）
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def tricolor_audit(total: int, passed: int, failed: int) -> str:
    """对测试结果进行三色审计（v1.1 增强）"""
    if total == 0:
        return "🔴 无测试"
    if failed == 0:
        return "🟢 全部通过"
    if failed <= total * 0.1:
        return "🟡 轻微失败"
    return "🔴 严重失败"


def generate_report():
    report_file = PROJECT_ROOT / "test_reports" / "test_report.json"
    if not report_file.exists():
        print("❌ 测试报告不存在，请先运行: python3 tests/run_all_tests.py")
        return

    with open(report_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = data.get("total", 0)
    passed = data.get("passed", 0)
    failed = data.get("failed", 0)
    skipped = data.get("skipped", 0)
    error = data.get("error", 0)
    tricolor = tricolor_audit(total, passed, failed)
    pass_rate = (passed / total * 100) if total > 0 else 0

    lines = [
        "# 🐉 龍魂系统测试报告",
        "",
        f"**生成时间:** {datetime.now().isoformat()}",
        f"**DNA:** #龍芯⚡️丙午·丙酉·丙寅·申时-TEST-REPORT-UID9622",
        f"**三色审计:** {tricolor}",
        "",
        "## 📊 测试统计",
        "",
        "| 状态 | 数量 |",
        "|------|------|",
        f"| ✅ 通过 | {passed} |",
        f"| ❌ 失败 | {failed} |",
        f"| ⏭️ 跳过 | {skipped} |",
        f"| ⚠️ 错误 | {error} |",
        f"| **总计** | **{total}** |",
        "",
        f"**通过率:** {pass_rate:.1f}%",
        "",
        "## 📋 详细结果",
        ""
    ]

    for result in data.get("results", [])[:50]:
        status_icon = {
            "passed": "✅",
            "failed": "❌",
            "skipped": "⏭️",
            "error": "⚠️"
        }.get(result.get("status"), "❓")
        lines.append(f"- {status_icon} **{result.get('test_name')}**")
        if result.get("message"):
            lines.append(f"  - {result.get('message')}")
        if result.get("details"):
            lines.append(f"  - 详情: {json.dumps(result.get('details'), ensure_ascii=False)[:100]}")
        lines.append("")

    if failed > 0:
        lines.append("## 🔴 失败项（耻辱墙候选）")
        lines.append("")
        lines.append("> 严重失败将自动入耻辱墙。修复后复测，通过即撤销。")
        lines.append("")

    report_path = PROJECT_ROOT / "test_reports" / "report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding='utf-8')
    print(f"✅ 报告已生成: {report_path}")
    print(f"🟢 三色审计: {tricolor}")


if __name__ == "__main__":
    generate_report()
