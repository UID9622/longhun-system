#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-COVERAGE-CHECK-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 覆盖率门禁检查 v1.1
功能: 检查测试覆盖率是否达到阈值，低于阈值则阻断 CI
用法:
  python3 tests/coverage_check.py [coverage.json] [阈值]
"""

import json
import sys
from pathlib import Path

COVERAGE_THRESHOLD = 75  # 最低覆盖率（默认）


def check_coverage(coverage_file: Path, threshold: float = COVERAGE_THRESHOLD) -> tuple:
    """检查覆盖率，返回 (是否达标, 说明)"""
    if not coverage_file.exists():
        return False, "覆盖率报告不存在（需先运行 pytest --cov 生成）"

    with open(coverage_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    totals = data.get("totals", {})
    covered = totals.get("covered_lines", 0)
    total_lines = totals.get("num_statements", 1)
    coverage = (covered / total_lines) * 100 if total_lines > 0 else 0

    return coverage >= threshold, f"覆盖率: {coverage:.1f}% (阈值: {threshold}%)"


if __name__ == "__main__":
    report_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("coverage.json")
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else COVERAGE_THRESHOLD
    passed, msg = check_coverage(report_file, threshold)
    print(f"📊 {msg}")
    sys.exit(0 if passed else 1)
