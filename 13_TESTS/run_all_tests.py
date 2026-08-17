#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-RUN-ALL-TESTS-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 一键运行所有测试

用法:
  python3 tests/run_all_tests.py           # 运行 v1.0 套件（4核心测试文件）
  python3 tests/run_all_tests.py --all     # 运行全部测试（含历史测试文件）
  python3 tests/run_all_tests.py --audit   # 只运行代码审计
  python3 tests/run_all_tests.py --smoke   # 只运行冒烟测试
  python3 tests/run_all_tests.py --auto    # 自动迭代模式
  python3 tests/run_all_tests.py --report  # 生成测试报告
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_auto_iteration import TestReporter, AutoFixSuggester


def run_pytest(args: List[str], label: str) -> Dict[str, Any]:
    """运行pytest并返回结果"""
    cmd = [sys.executable, "-m", "pytest", "-v", "-s"] + args
    print(f"🔧 运行 {label}: {' '.join(cmd)}")

    start = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=600
    )
    elapsed = time.time() - start

    return {
        "label": label,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "elapsed": elapsed,
        "passed": result.returncode == 0
    }


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂测试套件")
    parser.add_argument("--all", action="store_true", help="运行全部测试（含历史测试文件）")
    parser.add_argument("--audit", action="store_true", help="只运行代码审计")
    parser.add_argument("--smoke", action="store_true", help="只运行冒烟测试")
    parser.add_argument("--auto", action="store_true", help="自动迭代模式")
    parser.add_argument("--report", action="store_true", help="生成测试报告")

    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 完整测试套件 v1.1                                 ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-RUN-ALL-TESTS-UID9622   ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # 确保测试目录存在
    os.chdir(PROJECT_ROOT)

    # 选择测试范围
    if args.all:
        test_args = ["tests/"]  # 全部（含历史测试文件）
    elif args.audit:
        test_args = ["-m", "audit", "tests/test_code_audit.py"]
    elif args.smoke:
        test_args = ["-m", "smoke", "tests/test_smoke.py"]
    elif args.auto:
        test_args = ["-m", "auto_iteration", "tests/test_auto_iteration.py"]
    else:
        # 默认：v1.0 套件 4 核心测试文件
        test_args = [
            "tests/test_code_audit.py",
            "tests/test_functional.py",
            "tests/test_smoke.py",
            "tests/test_auto_iteration.py",
        ]

    # 运行测试
    result = run_pytest(test_args, "完整测试")

    print("\n" + "=" * 60)
    print(f"📊 测试结果: {'✅ 通过' if result['passed'] else '❌ 失败'}")
    print(f"⏱️  耗时: {result['elapsed']:.2f}s")
    print("=" * 60)

    # 生成报告
    if args.report or (not args.audit and not args.smoke and not args.auto):
        reporter = TestReporter(PROJECT_ROOT / "test_reports")
        reporter.add_result(
            "complete_test_suite",
            "passed" if result["passed"] else "failed",
            result["stdout"][:500]
        )
        print(f"📄 报告已保存: {reporter.report_file}")

        # 如果失败，生成修复建议
        if not result["passed"]:
            suggestions = AutoFixSuggester.suggest_fixes(reporter.get_report())
            if suggestions:
                print("\n🔧 自动修复建议:")
                for s in suggestions:
                    print(f"  - {s['test']}: {s['fix']} (优先级: {s['priority']})")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
